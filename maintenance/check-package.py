"""Offline package/export regressions; never part of the installed runtime."""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("package.py")


def load_package(script):
    spec = importlib.util.spec_from_file_location("srstack_package", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def directory_bytes(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


class PackageChecks(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="srstack-package-check-")
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name).resolve()
        self.root = self.work / "repository"
        self.root.mkdir()
        self.destination = self.work / "installed"
        source = load_package(SCRIPT)
        self.runtime = source.package_files()
        self.runtime[source.MANIFEST] = (json.dumps(source.make_manifest(self.runtime), indent=2) + "\n").encode()
        for path, content in self.runtime.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.script = self.root / "maintenance/package.py"
        self.script.parent.mkdir()
        shutil.copyfile(SCRIPT, self.script)
        for name in ("maintenance/private.json", ".github/workflows/validate.yml", ".gitignore",
                     "dist/old.zip", "scripts/__pycache__/snapshot.pyc", ".DS_Store"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("repository-only\n")
        self.package = load_package(self.script)
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                           GIT_AUTHOR_DATE="2000-01-01T00:00:00+00:00",
                           GIT_COMMITTER_DATE="2000-01-01T00:00:00+00:00")
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, environment, clear=True).start()
        self.git("init", "--quiet", "--object-format=sha1")
        self.git("config", "user.name", "Package Regression")
        self.git("config", "user.email", "package@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", os.devnull)
        self.commit = self.commit_tree()

    def git(self, *arguments):
        return subprocess.run(["git", "-C", str(self.root), *arguments], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()

    def commit_tree(self):
        self.git("add", "--all", "--force")
        self.git("commit", "--quiet", "--no-verify", "-m", "Isolated package fixture")
        return self.git("rev-parse", "HEAD")

    def invoke(self, *arguments):
        return subprocess.run([sys.executable, "-B", str(self.script), *arguments],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)

    def assert_no_install(self):
        self.assertFalse(os.path.lexists(self.destination))
        self.assertEqual([], list(self.work.glob(".srstack-export-*")))

    def test_export_matches_committed_manifest_not_dirty_worktree(self):
        (self.root / "README.md").write_text("invalid uncommitted runtime\n")
        (self.root / "assets/untracked.json").write_text("not valid JSON")
        result = self.invoke("export", "--commit", self.commit, "--destination", str(self.destination))
        self.assertEqual(0, result.returncode, result.stderr.decode())
        self.assertEqual(self.runtime, directory_bytes(self.destination))
        report = json.loads(result.stdout)
        manifest = json.loads(self.runtime[self.package.MANIFEST])
        self.assertEqual(manifest["content_sha256"], report["content_sha256"])
        self.assertEqual(self.commit, report["commit"])

    def test_export_supports_default_installed_integrity(self):
        result = self.invoke("export", "--commit", self.commit, "--destination", str(self.destination))
        self.assertEqual(0, result.returncode, result.stderr.decode())
        result = subprocess.run(
            [sys.executable, "-B", "-I", str(self.destination / "scripts/verify.py")],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=70,
        )
        self.assertEqual(0, result.returncode, result.stderr.decode() + result.stdout.decode())
        report = json.loads(result.stdout)
        self.assertEqual("ok", report["status"])
        self.assertEqual([("integrity", "ok")],
                         [(stage["name"], stage["status"]) for stage in report["stages"]])
        self.assertEqual(self.runtime, directory_bytes(self.destination))

    def test_build_verify_and_deterministic_archive_exclude_repository_files(self):
        (self.root / "README.md").write_bytes(self.runtime["README.md"] + b"\nReviewed update.\n")
        self.assertNotEqual(0, self.invoke("verify").returncode)
        for action in ("build", "verify", "archive"):
            result = self.invoke(action)
            self.assertEqual(0, result.returncode, result.stderr.decode())
        archive = self.root / f"dist/srstack-{self.package.VERSION}.zip"
        first = archive.read_bytes()
        expected = dict(self.runtime)
        expected["README.md"] = (self.root / "README.md").read_bytes()
        expected[self.package.MANIFEST] = (self.root / self.package.MANIFEST).read_bytes()
        with zipfile.ZipFile(archive) as bundled:
            self.assertEqual({"srstack/" + p: b for p, b in expected.items()},
                             {name: bundled.read(name) for name in bundled.namelist()})
        result = self.invoke("archive")
        self.assertEqual(0, result.returncode, result.stderr.decode())
        self.assertEqual(first, archive.read_bytes())

    def test_build_rejects_paths_the_installed_verifier_cannot_accept(self):
        for relative in ("assets/control\x7f.json", "assets/" + "deep/" * 7 + "bad.json",
                         "assets/" + "a" * 121 + "/" + "b" * 121 + "/x.json"):
            with self.subTest(path=relative):
                target = self.root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}")
                try:
                    result = self.invoke("build")
                    self.assertNotEqual(0, result.returncode)
                finally:
                    target.unlink()

    def test_bad_commit_cannot_create_target(self):
        for commit in (self.commit[:12], "not-a-sha", "f" * 40):
            with self.subTest(commit=commit):
                result = self.invoke("export", "--commit", commit, "--destination", str(self.destination))
                self.assertNotEqual(0, result.returncode)
                self.assertEqual(b"", result.stdout)
                self.assert_no_install()

    def test_failed_checkout_leaves_wrong_head_and_export_refuses(self):
        (self.root / "maintenance/private.json").write_text("next commit\n")
        newer = self.commit_tree()
        failed = subprocess.run(["git", "-C", str(self.root), "checkout", "f" * 40],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(0, failed.returncode)
        self.assertEqual(newer, self.git("rev-parse", "HEAD"))
        result = self.invoke("export", "--commit", self.commit, "--destination", str(self.destination))
        self.assertNotEqual(0, result.returncode)
        self.assert_no_install()

    def test_invalid_manifest_hash_aggregate_and_membership_refuse_export(self):
        original = json.loads(self.runtime[self.package.MANIFEST])
        corruptions = (
            lambda doc: doc["content_files"].__setitem__("README.md", "0" * 64),
            lambda doc: doc.__setitem__("content_sha256", "0" * 64),
            lambda doc: doc["content_files"].pop("README.md"),
            lambda doc: doc["content_files"].__setitem__("../escaped", "0" * 64),
            lambda doc: doc["content_files"].__setitem__("maintenance/private.json", "0" * 64),
        )
        for corrupt in corruptions:
            document = json.loads(json.dumps(original))
            corrupt(document)
            (self.root / self.package.MANIFEST).write_text(json.dumps(document))
            commit = self.commit_tree()
            with self.assertRaises(ValueError):
                self.package.export_package(commit, self.destination)
            self.assert_no_install()

    def test_committed_content_change_without_manifest_refuses_export(self):
        (self.root / "README.md").write_bytes(self.runtime["README.md"] + b"\nUnreviewed delta.\n")
        commit = self.commit_tree()
        with self.assertRaises(ValueError):
            self.package.export_package(commit, self.destination)
        self.assert_no_install()

    def test_source_index_requires_exact_records_and_group_membership(self):
        for mutation in ("extra-id", "missing-group"):
            files = dict(self.runtime)
            index = json.loads(files["assets/sources.json"])
            if mutation == "extra-id":
                index["groups"][0]["record_ids"].append("nonexistent-source")
            else:
                index["groups"].pop()
            files["assets/sources.json"] = json.dumps(index).encode()
            files[self.package.MANIFEST] = json.dumps(self.package.make_manifest(files)).encode()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.package.verify_manifest(files)

    def test_existing_directory_file_and_dangling_symlink_are_preserved(self):
        self.destination.mkdir()
        # Even an empty pre-existing directory belongs to its caller.
        with self.assertRaises(FileExistsError):
            self.package.export_package(self.commit, self.destination)
        self.assertTrue(self.destination.is_dir())
        self.destination.rmdir()
        self.destination.write_bytes(b"owner data")
        with self.assertRaises(FileExistsError):
            self.package.export_package(self.commit, self.destination)
        self.assertEqual(b"owner data", self.destination.read_bytes())
        self.destination.unlink()
        self.destination.symlink_to(self.work / "absent")
        with self.assertRaises(ValueError):
            self.package.export_package(self.commit, self.destination)
        self.assertTrue(self.destination.is_symlink())
        self.assertFalse((self.work / "absent").exists())

    def test_runtime_symlink_and_unexpected_file_refuse_export(self):
        extra = self.root / "assets/unsafe.json"
        extra.symlink_to(self.work / "outside")
        commit = self.commit_tree()
        with self.assertRaises(ValueError):
            self.package.export_package(commit, self.destination)
        self.assert_no_install()
        extra.unlink()
        (self.root / "secret.txt").write_text("not in the runtime boundary")
        commit = self.commit_tree()
        with self.assertRaises(ValueError):
            self.package.export_package(commit, self.destination)
        self.assert_no_install()

    def test_failed_git_archive_does_not_create_target(self):
        # A failing producer may still emit a completely valid archive. Its exit
        # status, not just parseable output, must prevent a successful install.
        archive = self.work / "failed-archive.tar"
        archive.write_bytes(self.package.git("archive", "--format=tar", self.commit))
        wrapper = self.work / "failing-git.py"
        wrapper.write_text(
            "import os, pathlib, sys\n"
            "if sys.argv[3] == 'archive':\n"
            f"    sys.stdout.buffer.write(pathlib.Path({str(archive)!r}).read_bytes())\n"
            "    sys.exit(71)\n"
            f"os.execv({shutil.which('git')!r}, ['git', *sys.argv[1:]])\n"
        )
        real_run = subprocess.run

        def run_with_wrapper(command, **kwargs):
            if command[0] == "git":
                command = [sys.executable, "-B", str(wrapper), *command[1:]]
            return real_run(command, **kwargs)

        with patch.object(subprocess, "run", side_effect=run_with_wrapper):
            with self.assertRaises(subprocess.CalledProcessError):
                self.package.export_package(self.commit, self.destination)
        self.assert_no_install()

    def test_corrupt_traversing_link_and_incomplete_archives_are_not_extracted(self):
        bad_archives = [b"not a tar archive"]
        for name, kind in (("../escaped", tarfile.REGTYPE), ("README.md", tarfile.SYMTYPE),
                           ("README.md", tarfile.REGTYPE)):
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode="w") as archive:
                member = tarfile.TarInfo(name)
                member.type = kind
                if kind == tarfile.SYMTYPE:
                    member.linkname = "../escaped"
                    archive.addfile(member)
                else:
                    member.size = 4
                    archive.addfile(member, io.BytesIO(b"evil"))
            bad_archives.append(stream.getvalue())
        real_git = self.package.git
        for payload in bad_archives:
            def replaced_archive(*arguments):
                return payload if arguments[0] == "archive" else real_git(*arguments)
            with patch.object(self.package, "git", side_effect=replaced_archive):
                with self.assertRaises((ValueError, tarfile.TarError)):
                    self.package.export_package(self.commit, self.destination)
            self.assert_no_install()
            self.assertFalse((self.work / "escaped").exists())

    def test_head_change_during_source_read_cannot_publish(self):
        real_git = self.package.git

        def moving_head(*arguments):
            result = real_git(*arguments)
            if arguments[0] == "archive":
                (self.root / "maintenance/private.json").write_text("HEAD moved\n")
                self.commit_tree()
            return result

        with patch.object(self.package, "git", side_effect=moving_head):
            with self.assertRaises(ValueError):
                self.package.export_package(self.commit, self.destination)
        self.assert_no_install()

    def test_publish_failure_cleans_target_before_skill_discovery(self):
        real_rename = Path.rename
        moved = []

        def fail_after_first(path, target):
            if path.parent.name.startswith(".srstack-export-"):
                if moved:
                    self.assertFalse((self.destination / "SKILL.md").exists())
                    raise OSError("injected publication failure")
                moved.append(path.name)
            return real_rename(path, target)

        with patch.object(Path, "rename", fail_after_first):
            with self.assertRaises(OSError):
                self.package.export_package(self.commit, self.destination)
        self.assert_no_install()

    def test_archive_write_failure_leaves_no_partial_archive(self):
        with patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("injected write failure")):
            with self.assertRaises(OSError):
                self.package.create_archive(self.runtime)
        self.assertFalse((self.root / f"dist/srstack-{self.package.VERSION}.zip").exists())
        self.assertFalse((self.root / f"dist/srstack-{self.package.VERSION}.zip.sha256").exists())
        self.assertEqual([], list((self.root / "dist").glob(".srstack-archive-*")))


if __name__ == "__main__":
    unittest.main()
