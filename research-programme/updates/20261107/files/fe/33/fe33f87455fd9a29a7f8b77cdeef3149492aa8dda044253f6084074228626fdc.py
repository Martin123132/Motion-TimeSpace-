from emission_common import *


def main():
    modest()
    output = ROOT / 'ACCURACY-REVIEW.json'
    assert not output.exists()
    excluded = {}
    for model in ['heavy', 'cold']:
        for suffix in ['standard-basis36-over32', 'infrared40-over32', 'infrared56-over48']:
            excluded['results/' + model + '-' + suffix + '/status.json'] = dict(
                reason='Unresolved lowest-frequency structure in the trial spectral basis, with original0.002 gate retained.',
                superseded_by=['results/' + model + '-polynomialdc-infrared96-over88/status.json'])
        for suffix in ['dcbr-infrared72-over64', 'dcbr-infrared88-over80']:
            excluded['results/' + model + '-' + suffix + '/status.json'] = dict(
                reason='DC plus BR reopens the lowest-band basis gate; refined source spectra are tested without widening the threshold.',
                superseded_by=['results/' + model + '-dcbr-infrared96-over88/status.json',
                               'results/' + model + '-integrated-infrared96-over88/status.json'])
    for suffix in ['cold-emitting-geometry', 'cold-emitting-geometry-v2']:
        excluded['results/' + suffix + '/status.json'] = dict(
            reason='Tiny cold-parent field increments are lost in differencing total fields and in constructing a dense total-field polynomial. Repaired by evolving affine field increments; physical equations unchanged.',
            superseded_by=['results/cold-emitting-geometry-v3/status.json', 'results/dense-derivative/status.json',
                           'results/geometry-coordinate-equivalence/status.json'])
    mandatory = ['results/start-guard/status.json', 'results/sourced-emission/status.json',
                 'results/integrated-dc/status.json', 'results/emission-temperature-identity/status.json',
                 'results/br-jacobian/status.json', 'results/dense-derivative/status.json',
                 'results/physical-summary/status.json', 'results/geometry-coordinate-equivalence/status.json']
    for model in ['heavy', 'cold']:
        mandatory.extend(['results/' + model + '-emitting-geometry-v3/status.json',
                          'results/' + model + '-integrated-time6400-over3200/status.json',
                          'results/' + model + '-integrated-infrared96-over88/status.json',
                          'results/' + model + '-integrated-infrared96-over88-6400/status.json'])
        for kind in ['q1000', 'e8', 'lowcut', 't17', 'emission']:
            mandatory.append('results/' + model + '-integrated-' + kind + '-refinement/status.json')
        for kind in ['none', 'dc', 'integrated']:
            mandatory.append('backgrounds/' + model + '-ir96-' + kind + '-6400/status.json')
    packets = {path.relative_to(ROOT).as_posix(): json.loads(path.read_text())
               for category in ['results', 'banks', 'backgrounds'] for path in (ROOT / category).glob('*/status.json')}
    for name in mandatory:
        assert name in packets and packets[name]['all_checks_passed'], name
    for name, packet in packets.items():
        assert (ROOT / name).parent.joinpath('COMPLETE').is_file()
        if name in excluded:
            assert not packet['all_checks_passed'], name
            for successor in excluded[name]['superseded_by']:
                assert successor in packets and packets[successor]['all_checks_passed'], successor
        else:
            assert packet['all_checks_passed'], name
    assert set(excluded).issubset(packets)
    write_json(output, dict(
        accepted_scope='Matched emitting background on a=1e-6 to1e-5 for both retained parents: unchanged finite-shift Compton plus integrated Planck-ambient Gould DC and tabulated H/He BR, finite gas heat, sourced number balance and leading-heat FLRW stress. Individual0.002 refinement gates pass; original models and fits unchanged.',
        all_requested_numerical_gates_closed=True, open_numerical_gate=None, unchanged_numerical_response_gate=.002,
        retained_unaccepted_accuracy_trials=excluded, required_accepted_packets=sorted(set(mandatory)),
        accuracy_boundaries=[
            'Individual numerical refinement tests are not an aggregate uncertainty bound or a full physical error budget.',
            'BR uses merged NR/BHE Gaunt data; full EH, electron-electron BR, full DC redistribution and polarized/anisotropic production remain outside this model.',
            'Rates use the Planck reference at leading background heat order. The gas finite heat capacity is retained; the complete nonlinear kinetic expansion is not.',
            'The background DC14.16 theta_star correction is Planck-specific. Its physical spectrum variation must be sourced or bounded before retaining that relativistic order in mixed waves.',
            'Dense stress is conservative and checked against actual spectral moments. Initial electron relaxation is not resolved pointwise.',
            'Corrected Friedmann/scalar geometry is leading heat order; kinetic rates are not nonlinearly iterated on that corrected geometry.',
            'No emitted-wave response or visibility/light-cone sky spectrum is computed here. Source derivatives are prepared for that next step.',
            'The original comparator completed its data packet before a NumPy-boolean console serialization error; v2 repairs only printing. The original packet is retained.',
            'Both cold geometry failures remain stored; evolving field increments repairs solver dense-output cancellation, not a physical instability.',
            'No new empirical fit or claim of derived G, alpha, electron mass or species abundance is introduced.'],
        conclusion='Photon number now changes through sourced DC and BR while radiation and ordinary matter exchange the same energy moment. Both emitting parent backgrounds and stress pass the scoped gates. Proceed to perturb this matched emitting background using the actual finite-frequency ambient and BR derivatives, not the old no-emission source.'))
    print(json.dumps(dict(packets=len(packets), excluded=len(excluded), required=len(set(mandatory)))), flush=True)


if __name__ == '__main__':
    main()
