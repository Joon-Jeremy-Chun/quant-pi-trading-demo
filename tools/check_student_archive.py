"""Rehearse Download ZIP instructions in a fresh, package-free Python environment.

No data download, account, external browser service or device connection is used.
Only the public checkout is copied; temporary files are outside the worktree.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import zipfile

from check_publication import ROOT, checkout_files


def run(command, cwd, expected_code=0):
    result = subprocess.run(command, cwd=cwd, text=True, encoding='utf-8',
                            capture_output=True, timeout=90)
    if result.returncode != expected_code:
        # Do not copy environment paths or arbitrary output into a public log.
        raise RuntimeError(f'Classroom command failed: {Path(command[1]).name}; exit {result.returncode}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional new JSON evidence file.')
    args = parser.parse_args()
    checks = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='classroom-archive-') as folder:
        temporary = Path(folder)
        archive = temporary/'classroom.zip'
        names, _ = checkout_files()
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
            for name in sorted(names):
                path = ROOT/name
                if path.is_file() and not path.is_symlink():
                    output.write(path, 'classroom/'+name)
        with zipfile.ZipFile(archive) as source:
            source.extractall(temporary/'download')
        classroom = temporary/'download'/'classroom'
        assert not (classroom/'.git').exists()
        checks.append('public ZIP copy without Git metadata')
        environment = temporary/'python-environment'
        run([sys.executable, '-m', 'venv', '--without-pip', str(environment)], temporary)
        python = environment/('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
        result = run([str(python), '-I', '-c',
                      'import importlib.metadata,sys; assert sys.prefix != sys.base_prefix; '
                      'assert not list(importlib.metadata.distributions()); print("empty")'], classroom)
        assert result.stdout.strip() == 'empty'
        checks.append('fresh venv with zero third-party packages')
        evidence = classroom/'docs'/'validation'
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in evidence.iterdir() if p.is_file()}
        run([str(python), 'tools/verify_classroom.py', '--check'], classroom)
        checks.append('three guide CLI examples and answer snippet')
        run([str(python), '-m', 'unittest', 'discover', '-s', 'tests', '-v'], classroom)
        checks.append('Python classroom tests from the archive')
        run([str(python), 'tools/validate_documentation.py'], classroom)
        checks.append('archive documentation references and source syntax')
        result = run([str(python), 'tools/check_publication.py'], classroom)
        assert json.loads(result.stdout)['source_mode'] == 'archive'
        checks.append('publication check without a Git checkout')
        result = run([str(python), 'tools/check_publication.py', '--history'], classroom, 2)
        assert 'requires Git and a repository checkout' in result.stderr
        checks.append('clear explanation for unavailable Git history')

        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        process = subprocess.Popen([str(python), 'src/demo_dashboard.py', '--port', str(port)],
                                   cwd=classroom, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, encoding='utf-8')
        try:
            deadline = time.monotonic()+15
            while True:
                connection = http.client.HTTPConnection('127.0.0.1', port, timeout=1)
                try:
                    connection.request('GET', '/?view=2d')
                    response = connection.getresponse()
                    content = response.read()
                    assert response.status == 200 and b'Little Quant Lab' in content
                    break
                except (ConnectionError, OSError):
                    if time.monotonic() >= deadline:
                        raise RuntimeError('Local classroom server did not start.') from None
                    time.sleep(.1)
                finally:
                    connection.close()
            checks.append('documented server CLI starts and serves the local 2D route')
            for resource in ['/app.js', '/styles.css', '/sample_state.json']:
                connection = http.client.HTTPConnection('127.0.0.1', port, timeout=3)
                connection.request('GET', resource)
                response = connection.getresponse()
                assert response.status == 200
                response.read(); connection.close()
            checks.append('all public browser assets are available')
            connection = http.client.HTTPConnection('127.0.0.1', port, timeout=3)
            connection.request('GET', '/README.md')
            response = connection.getresponse()
            assert response.status == 404
            response.read(); connection.close()
            checks.append('repository documents are outside the static server allowlist')
        finally:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill(); process.communicate(timeout=5)

        after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in evidence.iterdir() if p.is_file()}
        assert before == after
        checks.append('published historical evidence remains unchanged')
        report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                  'record_class': 'operational-verification',
                  'scenario': 'public ZIP + fresh package-free venv',
                  'python': sys.version.split()[0], 'platform': sys.platform,
                  'public_archive_files': len(names), 'third_party_packages': 0,
                  'checks': checks, 'all_passed': True,
                  'elapsed_seconds': round(time.monotonic()-started, 3),
                  'limits': ['agent technical rehearsal, not feedback from real students',
                             'HTTP startup check does not execute browser WebGL or CDN imports']}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
