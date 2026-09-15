"""Build, verify, archive, or export srstack's explicitly bounded runtime content."""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT
MANIFEST = "release-manifest.json"
VERSION = "0.2.0"
SCRIPT_FILES = {"scripts/scenario.py", "scripts/snapshot.py", "scripts/price.py"}
TOP_FILES = {"SKILL.md", "README.md", "LICENSE", MANIFEST}
REPOSITORY_DIRS = {"maintenance", ".github", ".git", "dist"}
CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
REPOSITORY_FILES = {".gitignore", ".git"}


def runtime_path(path):
    """Reject ambiguous names before classifying runtime versus repository content."""
    parts = path.split("/")
    if (not path or any(part in {"", ".", ".."} for part in parts)
            or "\\" in path or ":" in path or any(ord(c) < 32 for c in path)):
        raise ValueError(f"Unsafe package path: {path!r}")
    if (parts[0] in REPOSITORY_DIRS | REPOSITORY_FILES
            or any(part in CACHE_DIRS for part in parts)
            or parts[-1] == ".DS_Store" or PurePosixPath(path).suffix in {".pyc", ".pyo", ".pyd"}):
        return False
    if path in TOP_FILES | SCRIPT_FILES:
        return True
    if parts[0] in {"assets", "references"} and len(parts) > 1 and PurePosixPath(path).suffix in {".md", ".json"}:
        return True
    raise ValueError(f"Unexpected runtime file: {path}")


def require_runtime(files):
    for path in files:
        if not runtime_path(path):
            raise ValueError(f"Repository-only path in runtime: {path}")
    for required in (TOP_FILES - {MANIFEST}) | SCRIPT_FILES:
        if required not in files:
            raise ValueError(f"Missing {required}")


def package_files():
    if PACKAGE.is_symlink() or not PACKAGE.is_dir():
        raise ValueError("Package root must be a real directory, not a symlink")
    files = {}
    for directory, dirs, names in os.walk(PACKAGE, followlinks=False):
        dirs[:] = sorted(name for name in dirs
                         if name not in CACHE_DIRS
                         and not (Path(directory) == PACKAGE and name in REPOSITORY_DIRS))
        base = Path(directory)
        for name in dirs:
            if (base / name).is_symlink():
                raise ValueError(f"Symlink not allowed: {base / name}")
        for name in sorted(names):
            if name == ".git":
                continue
            if Path(directory) == PACKAGE and name in REPOSITORY_FILES:
                continue
            path = base / name
            if path.is_symlink():
                raise ValueError(f"Symlink not allowed: {path}")
            if not path.is_file():
                raise ValueError(f"Nonregular runtime file: {path}")
            relative = path.relative_to(PACKAGE).as_posix()
            if runtime_path(relative):
                files[relative] = path.read_bytes()
    require_runtime(files)
    return files


def fingerprints(files):
    contents = {p: b for p, b in files.items() if p != MANIFEST}
    digest = hashlib.sha256()
    for path, content in sorted(contents.items()):
        digest.update(path.encode("utf-8") + b"\0" + content)
    return {
        "content_files": {p: hashlib.sha256(b).hexdigest() for p, b in sorted(contents.items())},
        "content_sha256": digest.hexdigest(),
    }


def local_target(owner, target, files):
    if target.startswith(("https://", "http://", "mailto:")):
        return
    path, _, anchor = target.partition("#")
    parts = []
    for part in (PurePosixPath(owner).parent / path).parts if path else PurePosixPath(owner).parts:
        if part == "..":
            if not parts:
                raise ValueError(f"Escaping link: {owner}: {target}")
            parts.pop()
        elif part not in {".", ""}:
            parts.append(part)
    resolved = "/".join(parts)
    if target.startswith("/") or resolved not in files:
        raise ValueError(f"Missing/unsafe link: {owner}: {target}")
    if anchor and resolved.endswith(".md"):
        headings = re.findall(r"^#+\s+(.+)$", files[resolved].decode(), re.M)
        slugs = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
        if anchor not in slugs:
            raise ValueError(f"Missing heading: {owner}: {target}")


def verify_content(files):
    parsed = {p: json.loads(b) for p, b in files.items() if p.endswith(".json") and p != MANIFEST}
    skill = files["SKILL.md"].decode()
    if not skill.startswith("---\n") or "\nname: srstack\n" not in skill:
        raise ValueError("Missing srstack skill frontmatter")
    if f'version: "{VERSION}"' not in skill:
        raise ValueError("Unexpected version; update release tooling deliberately")
    source_ids = set()
    index = parsed["assets/sources.json"]
    source_paths = set()
    for group in index["groups"]:
        path = group["path"]
        if path not in parsed or not path.startswith("assets/sources/"):
            raise ValueError(f"Invalid source group path: {path}")
        if path in source_paths:
            raise ValueError(f"Duplicate source group path: {path}")
        source_paths.add(path)
        if group["record_ids"] != [record["id"] for record in parsed[path]["records"]]:
            raise ValueError(f"Source index mismatch: {path}")
        for record in parsed[path]["records"]:
            if record["id"] in source_ids:
                raise ValueError(f"Duplicate source ID: {record['id']}")
            source_ids.add(record["id"])
            for field in ["url", "publisher", "retrieved_at", "review_depth", "claim_stage"]:
                if not record.get(field):
                    raise ValueError(f"Missing source {field}: {record['id']}")
    if source_paths != {path for path in parsed if path.startswith("assets/sources/")}:
        raise ValueError("Source index group membership mismatch")
    def walk(value, owner):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "source_ids":
                    if not isinstance(item, list) or not set(item) <= source_ids:
                        raise ValueError(f"Unknown source IDs in {owner}: {item}")
                walk(item, owner)
        elif isinstance(value, list):
            for item in value:
                walk(item, owner)
    for owner, data in parsed.items():
        walk(data, owner)
    for owner, content in files.items():
        if not owner.endswith(".md"):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", content.decode()):
            local_target(owner, target, files)
    records = []
    for group in parsed["assets/parameters.json"]["groups"]:
        path = group["path"]
        if path not in parsed or not path.startswith("assets/parameters/"):
            raise ValueError(f"Invalid parameter group path: {path}")
        group_records = parsed[path]["records"]
        if group["record_ids"] != [r["id"] for r in group_records]:
            raise ValueError(f"Parameter index mismatch: {path}")
        records.extend(group_records)
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("Duplicate parameter IDs")
    entity_index = parsed["assets/entity-index.json"]
    entities = []
    for group in entity_index.get("groups", []):
        path = group["path"]
        if path not in parsed or not path.startswith("assets/entities/"):
            raise ValueError(f"Missing/invalid entity group {path}")
        catalog = parsed[path]
        group_records = catalog["records"]
        if group["record_ids"] != [record["id"] for record in group_records]:
            raise ValueError(f"Entity index mismatch: {path}")
        if group["chain_id"] != catalog["chain"]["id"]:
            raise ValueError(f"Entity group chain mismatch: {path}")
        for record in group_records:
            address = record["address"]
            if record["chain_id"] != group["chain_id"] or not re.fullmatch(r"0x[0-9a-fA-F]{40}", address):
                raise ValueError(f"Invalid entity identity: {record['id']}")
            if record["chain_id"] != 4663 or record["explorer_url"] != f"https://robin.etherscan.io/address/{address}#code":
                raise ValueError(f"Wrong-chain/nonpreferred explorer: {record['id']}")
            if record["attribution"]["status"] != "publisher-listed" or not record["attribution"]["source_ids"]:
                raise ValueError(f"Missing publisher attribution: {record['id']}")
        entities.extend(group_records)
    identities = {(record["chain_id"], record["address"].lower()) for record in entities}
    if len(identities) != len(entities) or len({record["id"] for record in entities}) != len(entities):
        raise ValueError("Duplicate entity identity or record ID")
    if entity_index["publisher_attributed_records"] != len(entities):
        raise ValueError("Entity attribution count mismatch")
    return {"files": len(files), "sources": len(source_ids), "parameters": len(records),
            "entities": len(entities),
            "max_file_bytes": max(map(len, files.values()))}


def make_manifest(files):
    return {
        "schema_version": 1, "name": "srstack", "version": VERSION,
        "scope": "Runtime knowledge, fixed public readers and scenario planner; excludes manifest, repository maintenance, CI, Git metadata, and build/cache artifacts",
        "digest_convention": "SHA-256 of lexicographically sorted UTF-8 POSIX path + NUL + exact file bytes; excludes manifest",
        **fingerprints(files),
    }


def verify_manifest(files):
    require_runtime(files)
    report = verify_content(files)
    expected = make_manifest(files)
    if MANIFEST not in files or json.loads(files[MANIFEST]) != expected:
        raise ValueError("Manifest does not match package; deliberately rebuild after review")
    report["content_sha256"] = expected["content_sha256"]
    return report


def git(*arguments):
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments], check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def reviewed_head(commit):
    if not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        raise ValueError("Export requires a full 40-hex reviewed commit")
    if Path(os.fsdecode(git("rev-parse", "--show-toplevel")).strip()).resolve() != ROOT:
        raise ValueError("Export must run from the public repository's own checkout")
    if git("rev-parse", "--verify", "HEAD").decode().strip() != commit.lower():
        raise ValueError("HEAD is not the supplied reviewed commit")
    if git("cat-file", "-t", commit).strip() != b"commit":
        raise ValueError("Reviewed object is not a commit")


def committed_files(commit):
    """Read only checked Git output; never checkout or extract archive paths."""
    entries = {}
    directories = set()
    for entry in git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, _ = metadata.split()
        path = raw_path.decode("utf-8")
        included = runtime_path(path)
        if mode not in {b"100644", b"100755"} or kind != b"blob":
            raise ValueError(f"Nonregular committed file: {path}")
        if path in entries:
            raise ValueError(f"Duplicate committed path: {path}")
        entries[path] = included
        directories.update(parent.as_posix() for parent in PurePosixPath(path).parents
                           if parent != PurePosixPath("."))
    archive_bytes = git("archive", "--format=tar", commit)
    files = {}
    seen = set()
    seen_directories = set()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive:
            path = member.name.rstrip("/") if member.isdir() else member.name
            # Classification also rejects absolute, traversal, and ambiguous names.
            if member.isdir():
                if path not in directories or path in seen_directories:
                    raise ValueError(f"Unexpected archive directory: {path}")
                seen_directories.add(path)
                continue
            included = runtime_path(path)
            if not member.isfile() or path not in entries or path in seen:
                raise ValueError(f"Unexpected/nonregular archive member: {path}")
            seen.add(path)
            if included:
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"Unreadable archive member: {path}")
                with stream:
                    files[path] = stream.read()
                if len(files[path]) != member.size:
                    raise ValueError(f"Truncated archive member: {path}")
    if seen != set(entries):
        raise ValueError("Git archive does not match committed tree membership")
    return files


def export_package(commit, destination):
    """Validate the reviewed commit, stage it, then exclusively claim the target.

    Dirty working-tree runtime files are intentionally irrelevant. A failed Git
    operation, mismatched HEAD, invalid content, or manifest mismatch cannot
    create a target. Publication uses exclusive mkdir (not overwrite-prone
    rename); a later write/move failure removes only the directory we created.
    """
    reviewed_head(commit)
    files = committed_files(commit)
    report = verify_manifest(files)
    destination = Path(destination).expanduser()
    if ".." in destination.parts:
        raise ValueError("Destination must not contain parent traversal")
    destination = destination.absolute()
    for ancestor in (destination, *destination.parents):
        if ancestor.is_symlink():
            raise ValueError(f"Symlink destination/ancestor: {ancestor}")
    if os.path.lexists(destination):
        raise FileExistsError(f"Destination already exists: {destination}")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must already exist")
    with tempfile.TemporaryDirectory(prefix=".srstack-export-", dir=destination.parent) as temporary:
        staging = Path(temporary)
        for path, content in sorted(files.items()):
            output = staging / path
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
            output.chmod(0o644)
        reviewed_head(commit)
        destination.mkdir()
        try:
            # Discovery must not see a SKILL.md until all other runtime content exists.
            for child in sorted(staging.iterdir(), key=lambda path: (path.name == "SKILL.md", path.name)):
                child.rename(destination / child.name)
        except BaseException:
            shutil.rmtree(destination)
            raise
    report.update(commit=commit.lower(), destination=str(destination))
    return report


def create_archive(files):
    directory = ROOT / "dist"
    if directory.is_symlink():
        raise ValueError("Archive output directory must not be a symlink")
    directory.mkdir(exist_ok=True)
    dest = directory / f"srstack-{VERSION}.zip"
    checksum_dest = dest.with_suffix(".zip.sha256")
    if dest.is_symlink() or checksum_dest.is_symlink():
        raise ValueError("Archive output must not be a symlink")
    with tempfile.TemporaryDirectory(prefix=".srstack-archive-", dir=directory) as temporary:
        staged = Path(temporary) / dest.name
        with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path, content in sorted(files.items()):
                member = zipfile.ZipInfo("srstack/" + path, date_time=(2026, 9, 14, 0, 0, 0))
                member.external_attr = 0o100644 << 16
                member.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(member, content)
        with zipfile.ZipFile(staged) as archive:
            expected_members = {"srstack/" + p: b for p, b in files.items()}
            if archive.namelist() != sorted(expected_members):
                raise ValueError("Archive membership mismatch")
            for path, content in expected_members.items():
                if archive.read(path) != content:
                    raise ValueError(f"Archive bytes mismatch: {path}")
        checksum = hashlib.sha256(staged.read_bytes()).hexdigest()
        staged_checksum = staged.with_suffix(".zip.sha256")
        staged_checksum.write_text(f"{checksum}  {dest.name}\n")
        staged.replace(dest)
        staged_checksum.replace(checksum_dest)
    return {"archive": dest.relative_to(ROOT).as_posix(), "archive_sha256": checksum}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "verify", "archive", "export"])
    parser.add_argument("--commit", help="Reviewed full 40-hex commit; must equal HEAD")
    parser.add_argument("--destination", type=Path, help="New runtime directory; parent must exist")
    args = parser.parse_args()
    if args.action == "export":
        if args.commit is None or args.destination is None:
            parser.error("export requires --commit and --destination")
        report = export_package(args.commit, args.destination)
    else:
        if args.commit is not None or args.destination is not None:
            parser.error("--commit and --destination are only valid for export")
        files = package_files()
        if args.action == "build":
            report = verify_content(files)
            expected = make_manifest(files)
            (PACKAGE / MANIFEST).write_text(json.dumps(expected, indent=2) + "\n")
            report["content_sha256"] = expected["content_sha256"]
        else:
            report = verify_manifest(files)
        if args.action == "archive":
            report.update(create_archive(files))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
