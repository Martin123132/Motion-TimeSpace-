from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import psutil


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', type=int, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    folder = root / 'source-intake/navier-stokes/20260914/annular-position-time-radial-attempt03'
    status_path = folder / 'status.json'
    initial = json.loads(status_path.read_text())
    if initial['state'] != 'running' or len(initial['cases']) != 3:
        raise RuntimeError('Stop only at the three-completed-case boundary')
    process = psutil.Process(args.pid)
    if process.name().lower() != 'python.exe' or not any(
        value.endswith('derive_annular_position_time_radial_v3_20260929.py') for value in process.cmdline()):
        raise RuntimeError('PID does not belong to this exact calculation')
    suspended = False
    try:
        process.suspend()
        suspended = True
        try:
            raw = status_path.read_bytes()
            status = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            status = initial
            raw = (json.dumps(status, indent=2) + '\n').encode('utf-8')
        if status['state'] != 'running' or len(status['cases']) != 3:
            raise RuntimeError('The worker already passed the requested safe boundary')
        process.terminate()
        process.wait(timeout=10)
        suspended = False
        snapshot = folder / 'running-status-at-safe-boundary.json'
        with snapshot.open('xb') as stream:
            stream.write(raw)
        status['outputs'][str(snapshot.relative_to(root))] = hashlib.sha256(raw).hexdigest()
        status.update(state='failed', external_safe_boundary_stop=True,
            error='Controlled stop after three complete cases to resume the last case with incremental saves and a fresh bounded runtime.',
            numerical_failure=False, stopped_at=datetime.now(timezone.utc).isoformat(), stopped_pid=args.pid,
            controller_source=str(Path(__file__).resolve().relative_to(root)))
        status['inputs'][str(Path(__file__).resolve().relative_to(root))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        status_path.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(dict(state='saved_safe_boundary', completed_cases=3, stopped_pid=args.pid,
            numerical_failure=False, snapshot=str(snapshot))))
    finally:
        if suspended and process.is_running():
            process.resume()


if __name__ == '__main__':
    main()
