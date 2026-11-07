from __future__ import annotations

import csv

import numpy as np

from budget import (ROOT, BRANCH, CLOCK, read_json, digest, save, modest_process, dependencies,
                    polar_vacuum, frozen_boundary, carrier_flux, sideband_response, sideband_flux,
                    project_rates, orbit_series)


def main():
    modest_process()
    inputs, nodes, controls, actions, regressions, static_boundaries = {}, [], [], [], [], []

    def load(path):
        inputs[str(path)] = digest(path)
        result = read_json(path)
        assert result['state'] == 'complete'
        return result

    action = load(BRANCH/'conservative-eccentric-action-20261005/results/action/status.json')
    for settings in ['fine', 'coarse']:
        body = action['raw_nodes'][settings][0]
        mass, radius, deformability = [body[key] for key in ['mass', 'radius', 'tidal_lambda']]
        basis = polar_vacuum.static_master_basis(radius, mass, 1.).real
        static_vector = basis@np.array([1., 3*deformability])
        static_slope = float(static_vector[1]/static_vector[0])
        static_boundaries.append(dict(settings=settings, mass=mass, radius=radius,
            tidal_lambda=deformability, slope=static_slope))
        carriers = []
        for plan in ['pilot', 'nodes', 'extension']:
            directory = CLOCK/'results'/(plan+'-'+settings)
            for row in load(directory/'status.json')['rows']:
                carriers.append((row, directory/row['archive']))
        bands = []
        for directory in [BRANCH/'near-circular-quadrupole-20261005/results'/('analytic-'+settings),
                          BRANCH/'near-circular-inspiral-20261005/results'/('nodes-'+settings)]:
            for row in load(directory/'status.json')['rows']:
                if 5.-1e-10 <= row['separation_over_radius'] <= 10.+1e-10:
                    bands.append((row, directory/row['archive']))
        inherited = load(CLOCK/'results'/('analysis-full-'+settings)/'status.json')
        for separation in sorted({row['separation'] for row, path in carriers}):
            semilatus = separation*radius/mass
            circular = {key:[] for key in ['point_out', 'horizon', 'frozen_polar', 'dynamic_polar', 'odd_response', 'wave_square']}
            sidebands = {key:[] for key in circular}
            action_parts = dict(frozen0=0., frozen2=0., full_polar0=0., full_polar2=0., odd0=0., odd2=0.)
            alpha = orbit_series(semilatus)['angular_frequency_fraction']
            for sector, azimuth in [('polar', 2), ('odd', 1)]:
                selected = [(row, path) for row, path in carriers if row['sector'] == sector and abs(row['separation']-separation) < 1e-10]
                full = carrier_flux([row for row, path in selected])
                alternate = carrier_flux([row for row, path in selected], .001)
                center = next(row for row, path in selected if row['fractional_frequency_shift'] == 0.)
                if sector == 'polar':
                    frozen_rows = []
                    for row, path in selected:
                        inputs[str(path)] = digest(path)
                        with np.load(path, allow_pickle=False) as archive:
                            frozen, diagnostic = frozen_boundary(row, archive, static_slope)
                        frozen_rows.append(frozen)
                        controls.append(dict(settings=settings, role='carrier', **diagnostic))
                    frozen = carrier_flux(frozen_rows)
                    frozen_alternate = carrier_flux(frozen_rows, .001)
                for component in circular:
                    values = ([0., 0.] if component in ['frozen_polar', 'dynamic_polar'] and sector != 'polar' else
                        full['reference'] if component == 'point_out' else
                        full['horizon'] if component == 'horizon' else
                        full['nonlinear_difference'] if component == 'wave_square' else
                        frozen['difference'] if component == 'frozen_polar' else
                        np.array(full['difference'])-frozen['difference'] if component == 'dynamic_polar' else
                        full['difference'] if sector == 'odd' else [0., 0.])
                    circular[component].append(dict(azimuth=azimuth, frequency=center['frequency'],
                        alpha=alpha, power0=float(values[0]), power2=float(values[1])))
                if sector == 'polar':
                    action_parts.update(frozen0=frozen['action'][0], frozen2=frozen['action'][1],
                        full_polar0=full['action'][0], full_polar2=full['action'][1])
                    controls.append(dict(settings=settings, role='frequency_stencil', separation=separation,
                        frozen_power2_error=abs(frozen['difference'][1]-frozen_alternate['difference'][1])/max(abs(frozen['difference'][1]), 1e-300),
                        full_power2_error=abs(full['difference'][1]-alternate['difference'][1])/max(abs(full['difference'][1]), 1e-300)))
                else:
                    action_parts.update(odd0=full['action'][0], odd2=full['action'][1])
            selected_bands = [(row, path) for row, path in bands if abs(row['separation_over_radius']-separation) < 1e-10]
            assert len(selected_bands) == 7, (settings, separation, len(selected_bands))
            for row, path in selected_bands:
                if row['harmonic'] == 0:
                    continue
                response = sideband_response(row)
                full = sideband_flux(response)
                if row['sector'] == 'polar':
                    inputs[str(path)] = digest(path)
                    with np.load(path, allow_pickle=False) as archive:
                        frozen_row, diagnostic = frozen_boundary(response, archive, static_slope)
                    frozen = sideband_flux(frozen_row)
                    action_parts['frozen2'] += complex(*frozen_row['responses'][0]['action']).real
                    action_parts['full_polar2'] += row['retarded_action_real']
                    controls.append(dict(settings=settings, role='sideband', **diagnostic))
                else:
                    action_parts['odd2'] += row['retarded_action_real']
                for component in sidebands:
                    value = (0. if component in ['frozen_polar', 'dynamic_polar'] and row['sector'] != 'polar' else
                        full['reference'] if component == 'point_out' else
                        full['horizon'] if component == 'horizon' else
                        full['nonlinear_difference'] if component == 'wave_square' else
                        frozen['difference'] if component == 'frozen_polar' else
                        full['difference']-frozen['difference'] if component == 'dynamic_polar' else
                        full['difference'] if row['sector'] == 'odd' else 0.)
                    sidebands[component].append(dict(azimuth=row['azimuth'], harmonic=row['harmonic'],
                        frequency=row['frequency'], power=float(value)))
            current = {}
            for component in circular:
                result = project_rates(mass, semilatus, circular[component], sidebands[component])
                record = dict(settings=settings, separation=separation, semilatus=semilatus, component=component, **result)
                nodes.append(record)
                current[component] = result
            prior = next(row for row in inherited['shrinkage_laws'] if row['component'] == 'combined_ell2'
                and row['channel'] == 'difference' and abs(row['separation']-separation) < 1e-10)
            reference_prior = next(row for row in inherited['shrinkage_laws'] if row['component'] == 'combined_ell2'
                and row['channel'] == 'BH' and abs(row['separation']-separation) < 1e-10)
            regression = dict(settings=settings, separation=separation)
            for key, original in [('P0', 'P0'), ('G0', 'Gamma0'), ('P2', 'P2')]:
                difference = sum(current[component][key] for component in ['frozen_polar', 'dynamic_polar', 'odd_response'])-current['horizon'][key]
                reference = current['point_out'][key]+current['horizon'][key]
                regression[key+'_difference_error'] = abs(difference/prior[original]-1)
                regression[key+'_reference_error'] = abs(reference/reference_prior[original]-1)
            parent_action = next(row for row in action['raw_nodes'][settings] if abs(row['separation']-separation) < 1e-10)
            for order in [0, 2]:
                action_parts['frozen'+str(order)] += parent_action['static'+str(order)]
                action_parts['full_polar'+str(order)] += parent_action['static'+str(order)]
                total = action_parts['full_polar'+str(order)]+action_parts['odd'+str(order)]
                regression['action'+str(order)+'_error'] = abs(total/parent_action['total'+str(order)]-1)
                weak = 1.5*deformability/(mass*semilatus)**6*(1.5 if order else 1.)
                actions.append(dict(settings=settings, separation=separation, order=order, weak=weak,
                    frozen_polar=action_parts['frozen'+str(order)],
                    dynamic_polar=action_parts['full_polar'+str(order)]-action_parts['frozen'+str(order)],
                    odd_response=action_parts['odd'+str(order)], full=total,
                    fractional_frozen_remainder=action_parts['frozen'+str(order)]/weak-1,
                    fractional_dynamic= (action_parts['full_polar'+str(order)]-action_parts['frozen'+str(order)])/weak,
                    fractional_odd=action_parts['odd'+str(order)]/weak, fractional_total=total/weak-1))
            regressions.append(regression)
    report = save('nodes', __file__, dict(input_hashes={**inputs, **dependencies()}, nodes=nodes,
        controls=controls, conservative_actions=actions, regressions=regressions, static_boundaries=static_boundaries,
        new_wave_or_background_solves=0, boundary_control='Real surface master logarithmic derivative frozen at its static value; all source/exterior frequency dependence retained.',
        interpretation='Fixed matching-surface diagnostic, not a unique covariant material-versus-geometry partition.'))
    for name, rows in [('rates.csv', nodes), ('conservative-budget.csv', actions)]:
        with (ROOT/'results/nodes'/name).open('x', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(dict(state='complete', nodes=len(nodes), frozen_boundary_evaluations=sum(row['role'] != 'frequency_stencil' for row in controls),
        maximum_reconstruction=max(row.get('maximum_direct_error', 0.) for row in controls),
        maximum_optical=max(row.get('maximum_optical_error', 0.) for row in controls),
        maximum_prior_regression=max(value for row in regressions for key, value in row.items() if key.endswith('_error')),
        action_endpoints=[row for row in actions if row['settings']=='fine' and row['separation'] in [5.,10.]]), flush=True)


if __name__ == '__main__':
    main()
