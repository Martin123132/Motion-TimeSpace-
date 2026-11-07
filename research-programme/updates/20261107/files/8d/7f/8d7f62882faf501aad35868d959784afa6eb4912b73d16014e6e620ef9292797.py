from quadrature_common import *
import hashlib
import psutil


def main():
    modest()
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.pid == os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            assert Path(process.cwd()).resolve() != ROOT, process.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    hashes = {}
    def verified(mapping):
        for name, expected in mapping.items():
            path = Path(name)
            if name not in hashes:
                hashes[name] = digest(path)
            assert hashes[name] == expected, name
    proof = local_packet(ROOT / 'results/arithmetic-proof')
    assert proof['all_checks_passed']
    verified(proof['input_hashes'])
    banks = []
    total_checks = len(proof['checks'])
    for variant in VARIANTS:
        for upper in [.04, .02]:
            folder = ROOT / 'results' / f'bank-{variant}-m{int(upper * 1000)}'
            complete = (folder / 'COMPLETE').is_file()
            receipts = sorted(folder.glob('event-*.json'))
            rows, checks, steps = [], [], []
            if receipts:
                fingerprint = json.loads((folder / 'INPUTS.json').read_text())
                verified(fingerprint)
                fingerprint_hash = hashlib.sha256(json.dumps(fingerprint, sort_keys=True).encode()).hexdigest()
                for path in receipts:
                    receipt = json.loads(path.read_text())
                    assert receipt['input_fingerprint_sha256'] == fingerprint_hash, path
                    verified({str(path.with_suffix('.npz')): receipt['archive_sha256']})
                    assert all(item['passed'] for item in receipt['checks']), path
                    steps.append(receipt['row']['step'])
                    rows.append(receipt['row'])
                    checks.extend(receipt['checks'])
                assert steps == ODD_STEPS[:len(steps)].tolist()
            if complete:
                packet = local_packet(folder)
                verified(packet['input_hashes'])
                assert packet['all_checks_passed'] and len(receipts) == 16
                assert packet['checks'] == checks and packet['rows'] == rows
                assert packet['count'] == len(checks)
            total_checks += len(checks)
            banks.append(dict(bank=folder.name, complete=complete, verified_receipts=len(receipts),
                pending_steps=ODD_STEPS[len(steps):].tolist(), passing_checks=len(checks)))
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SEAL
    for script in ROOT.glob('*.py'):
        compile(script.read_bytes(), str(script), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    workbench = POST.parent / 'formalization-workbench'
    assert workbench.is_dir()
    changed = [str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    assert not changed, changed
    snapshot = dict(state='safe_partial_checkpoint', full_stage_complete=False,
        verified_utc=datetime.now(timezone.utc).isoformat(), parent_seal_sha256=PARENT_SEAL,
        banks=banks, complete_banks=sum(bank['complete'] for bank in banks),
        verified_temperature_receipts=sum(bank['verified_receipts'] for bank in banks),
        passing_saved_checks=total_checks, rehashed_files=len(hashes),
        verified_hashes=hashes, owned_compute_workers=0, response_comparisons_complete=False,
        protected_workbench_recent_modified_file_count=0,
        pending='Finish remaining banks, four response comparisons, independent validation and final seal.')
    write_json(ROOT / 'RESUME-SNAPSHOT.json', snapshot)
    print(json.dumps({key: value for key, value in snapshot.items() if key not in ['verified_hashes', 'banks']}), flush=True)


if __name__ == '__main__':
    main()
