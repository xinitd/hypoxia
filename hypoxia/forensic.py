import hashlib
import json
import datetime
from pathlib import Path


def compute_hash(filepath, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def create_manifest(manifest_entries, task_id, manifest_path, algorithm):
    manifest = {
        'task_id': task_id,
        'created_at': datetime.datetime.now().isoformat(),
        'hash_algorithm': algorithm,
        'total_files': len(manifest_entries),
        'files': manifest_entries
    }

    manifest_json = json.dumps(manifest, indent=2)

    manifest_checksum = hashlib.sha256(manifest_json.encode()).hexdigest()
    manifest['manifest_checksum'] = manifest_checksum

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    return manifest_path, manifest_checksum
