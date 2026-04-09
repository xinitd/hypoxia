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


class ForensicLog:
    def __init__(self, log_path):
        self.log_path = log_path
        self.f = open(log_path, 'a')
        self._write('SESSION_START', f'Forensic log initialized: {log_path.name}')

    def _write(self, event_type, message):
        timestamp = datetime.datetime.now().isoformat()
        self.f.write(f'{timestamp}\t{event_type}\t{message}\n')
        self.f.flush()

    def file_copied(self, source, destination, file_hash=None):
        msg = f'{source} -> {destination}'
        if file_hash:
            msg += f' [{file_hash}]'
        self._write('FILE_COPIED', msg)

    def file_skipped(self, source, reason):
        self._write('FILE_SKIPPED', f'{source} ({reason})')

    def file_error(self, source, error_msg):
        self._write('FILE_ERROR', f'{source}: {error_msg}')

    def warning(self, message):
        self._write('WARNING', message)

    def complete(self, files_copied, files_skipped, total_bytes):
        self._write('SUMMARY', f'copied={files_copied} skipped={files_skipped} bytes={total_bytes}')
        self._write('SESSION_END', 'Collection complete')
        self.f.close()
