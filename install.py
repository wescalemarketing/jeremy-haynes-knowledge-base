#!/usr/bin/env python3
"""Install this verified research package into a new explicitly selected directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def verify(root):
    manifest = json.loads((root / 'reports/manifest.json').read_text())
    seen = set()
    for item in manifest['files']:
        rel = PurePosixPath(item['path'])
        if rel.is_absolute() or '..' in rel.parts or not rel.parts or item['path'] in seen:
            raise ValueError('Unsafe/duplicate manifest path')
        seen.add(item['path'])
        path = root.joinpath(*rel.parts)
        if path.is_symlink() or root.resolve() not in path.resolve().parents:
            raise ValueError('Source path escapes package')
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Checksum mismatch: ' + item['path'])
    for required in ('SKILL.md', 'tools/agent.py', 'tools/kb.py', 'data/sources.jsonl', 'data/claims.jsonl'):
        if required not in seen:
            raise ValueError('Missing package component: ' + required)
    return manifest

def install(source, destination):
    source, destination = source.resolve(), destination.expanduser().absolute()
    manifest = verify(source)
    if destination.exists():
        existing = verify(destination)
        if existing != manifest:
            raise ValueError('Different installation exists; choose a new destination')
        subprocess.run([sys.executable, str(destination / 'tools/agent.py'), 'setup'], check=True)
        return {'status': 'already_installed', 'path': str(destination), 'version': manifest['version']}
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.jeremy-kb-', dir=str(destination.parent)))
    try:
        for item in manifest['files']:
            rel = Path(item['path']); target = temporary / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / rel, target)
        shutil.copyfile(source / 'reports/manifest.json', temporary / 'reports/manifest.json')
        subprocess.run([sys.executable, str(temporary / 'tools/agent.py'), 'setup'], check=True)
        temporary.rename(destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return {'status': 'installed', 'path': str(destination), 'version': manifest['version'], 'query_command': [sys.executable, str(destination / 'tools/agent.py'), 'search', 'confirmation trust urgency']}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dest', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(install(ROOT, a.dest), indent=2))
