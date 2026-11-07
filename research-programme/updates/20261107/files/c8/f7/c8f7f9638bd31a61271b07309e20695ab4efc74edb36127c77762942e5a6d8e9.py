from derive_annular_source_gravity_20260914 import EvidenceRun
import hashlib
import json


def main():
    evidence = EvidenceRun('annular-wave-recovery-preflight-history-attempt02', __file__)
    try:
        intake = evidence.output.parent
        failure_path = intake/'annular-wave-flux-events-reference-third-attempt02/status.json'
        parent_path = intake/'annular-wave-flux-events-reference-third-attempt01/status.json'
        boundary_path = parent_path.parent/'status-running-at-two-rule-boundary.json'
        log_path = intake/'annular-wave-flux-events-reference-third-attempt01.log'
        for path in [failure_path, parent_path, boundary_path, log_path]:
            evidence.own(path)
        failure = json.loads(failure_path.read_text())
        parent_key = str(parent_path.relative_to(evidence.root))
        expected = failure['inputs'][parent_key]
        evidence.check('failed_setup_only', failure['state'] == 'failed' and not failure['cases']
            and 'parent_safe_boundary' in failure['error'])
        newline = '\r\n' if b'\r\n' in boundary_path.read_bytes() else '\n'
        snapshot = json.loads(boundary_path.read_text())
        evidence.check('observed_running_snapshot', snapshot['state'] == 'running' and len(snapshot['cases']) == 2)
        recovered = None
        for line in log_path.read_text(encoding='utf-8-sig').splitlines():
            try:
                progress = json.loads(line)
            except json.JSONDecodeError:
                continue
            if set(progress) != {'stage', 'seconds'}:
                continue
            candidate = dict(snapshot, progress=progress)
            raw = (json.dumps(candidate, indent=2)+'\n').replace('\n', newline).encode('utf-8')
            if hashlib.sha256(raw).hexdigest() == expected:
                recovered = raw
                break
        evidence.check('exact_captured_digest_reconstructed', recovered is not None, expected)
        destination = evidence.output/'historical-running-parent-owned-by-reference-recovery02.json'
        with destination.open('xb') as stream:
            stream.write(recovered)
        evidence.own(destination, 'outputs')
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False,
            historical_status_only=True, scientific_arrays_changed=False,
            method='Reconstruct only progress from observed boundary snapshot and log; require exact captured SHA256',
            historical_input_replay=dict(owner=str(failure_path.relative_to(evidence.root)),
                original_path=parent_key, expected_sha256=expected,
                recovered_snapshot=str(destination.relative_to(evidence.root))),
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
