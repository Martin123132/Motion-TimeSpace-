from common235 import *


def main():
    modest()
    config = protocol()
    target = ROOT / 'results/mass-angular.json'
    assert not target.exists()
    write(ROOT / 'mass-angular-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        audit_orders=[2, 8, 12], qualification_orders=[8, 12], tolerance=1e-10,
        source_bank_rule_changed=False, scope='Independent numerical check of the analytic invariant mass-moment angular integral'))
    checks, records = [], []
    for row in config['events']:
        parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
        for order in (2, 8, 12):
            sums = {degree: np.zeros((1, 3, 9)[degree]) for degree in config['multipoles']}
            wrong = np.zeros(3)
            for direction, weight in angular.inherited.source.angular_nodes(order):
                doppler = angular.inherited.source.dot(parameters['bath'], np.r_[1., direction])
                lab = parameters['transform'] @ np.r_[1., direction]
                lab_direction = lab[1:] / np.linalg.norm(lab[1:])
                for degree in config['multipoles']:
                    sums[degree] += weight / doppler**2 * angular.angular_feature(lab_direction, degree)
                wrong += weight / doppler**2 * direction
            error = {}
            for degree in config['multipoles']:
                expected = np.array([4 * np.pi]) if degree == 0 else np.zeros_like(sums[degree])
                error[degree] = float(np.linalg.norm(sums[degree] - expected) / (4 * np.pi))
                if order in (8, 12):
                    check(checks, f'{row["label"]}:order{order}:l{degree}:invariant angular moment', error[degree])
            wrong_error = float(np.linalg.norm(wrong) / (4 * np.pi))
            if order in (8, 12):
                check(checks, f'{row["label"]}:order{order}:rest-angle substitution rejected', int(wrong_error <= 1e-10), 0)
            records.append(dict(anchor=row['label'], order=order, angular_errors=error, wrong_rest_dipole=wrong_error,
                coarse_order_recorded_not_silently_zeroed=order == 2))
    failed = [entry for entry in checks if not entry['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now(),
        mass_response_used='Exact full-angle scalar identity, not numerical projection of the original eight rays'))
    print(json.dumps(dict(checks=len(checks), failed=failed, records=records)), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()
