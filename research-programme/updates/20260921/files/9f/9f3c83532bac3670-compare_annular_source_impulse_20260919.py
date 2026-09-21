from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.integrate import simpson
import contextlib
import csv
import hashlib
import json
import math
import numpy as np
import sympy as sp


def signed_source(evidence, folder):
    path = evidence.output.parent/folder/'status.json'
    status = json.loads(path.read_text())
    if status['state'] != 'complete' or not all(row['passed'] for row in status['checks']):
        raise RuntimeError('Incomplete input: '+folder)
    for category in ['inputs', 'outputs']:
        for name, expected in status[category].items():
            source = evidence.root/name
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if actual != expected:
                raise RuntimeError('Changed signed input: '+name)
            evidence.own(source)
    evidence.own(path)
    return status


def material_functional(samples, duration, fraction, power):
    end = int(round((len(samples)-1)*fraction))
    times = np.array([row['time'] for row in samples[:end+1]])
    momenta = np.array([row['material_momentum'] for row in samples[:end+1]])
    forces = np.array([row['raw_material'] for row in samples[:end+1]])
    coefficients = simpson(np.eye(len(times)), x=times, axis=1)
    if np.any(coefficients <= 0) or (len(times)-1) % 2:
        raise ValueError('Positive composite Simpson rule required.')
    weight = (times/duration)**power
    derivative = np.zeros_like(times) if power == 0 else power/duration*(times/duration)**(power-1)
    shifted = momenta-momenta[0]
    value = weight[-1]*shifted[-1]-coefficients @ (derivative*shifted+weight*forces)
    return float(value), dict(coefficients=coefficients, weight=weight, derivative=derivative,
        shifted=shifted, forces=forces, momenta=momenta)


def algebra(evidence):
    mass, lapse, root = sp.symbols('m N U', positive=True)
    velocity = sp.symbols('v', real=True)
    lapse_radial, root_radial = sp.symbols('N_R U_R', real=True)
    clock = sp.sqrt(lapse**2-velocity**2/root**2)
    gradient = lapse*lapse_radial+velocity**2*root_radial/root**3
    momentum = mass*velocity/(root**2*clock)
    force = -mass*gradient/clock
    momentum_derivatives = [mass*lapse**2/(root**2*clock**3),
        -mass*velocity*lapse/(root**2*clock**3),
        -2*mass*velocity/(root**3*clock)-mass*velocity**3/(root**5*clock**3)]
    force_derivatives = [-mass*(2*velocity*root_radial/(root**3*clock)+gradient*velocity/(root**2*clock**3)),
        -mass*lapse_radial/clock+mass*gradient*lapse/clock**3,
        3*mass*velocity**2*root_radial/(root**4*clock)+mass*gradient*velocity**2/(root**3*clock**3),
        -mass*lapse/clock, -mass*velocity**2/(root**3*clock)]
    for variable, expected in zip([velocity, lapse, root], momentum_derivatives):
        evidence.check('material_momentum_derivative_'+str(variable), sp.simplify(sp.diff(momentum, variable)-expected) == 0)
    for variable, expected in zip([velocity, lapse, root, lapse_radial, root_radial], force_derivatives):
        evidence.check('material_force_derivative_'+str(variable), sp.simplify(sp.diff(force, variable)-expected) == 0)
    canonical = sp.symbols('P', real=True)
    energy = sp.sqrt(mass**2+root**2*canonical**2)
    canonical_velocity = lapse*root**2*canonical/energy
    evidence.check('material_momentum_is_characteristic_canonical_P', sp.simplify(momentum.subs(velocity, canonical_velocity)-canonical) == 0)
    characteristic_force = -energy*lapse_radial-lapse*root*root_radial*canonical**2/energy
    evidence.check('material_force_is_characteristic_metric_force', sp.simplify(force.subs(velocity, canonical_velocity)-characteristic_force) == 0)
    time, duration = sp.symbols('t T', positive=True)
    total = time**5-3*time**3+7
    wave = 2*time**4-time+4
    radiation = sp.diff(total-wave, time)-(time**2+1)
    raw_wave = sp.diff(total, time)-(time**2+1)
    for power in [0, 1, 2, 4]:
        weight = (time/duration)**power
        direct = sp.integrate(weight*radiation, (time, 0, duration))
        wave_form = sp.integrate(weight*raw_wave, (time, 0, duration))-weight.subs(time, duration)*(wave.subs(time, duration)-wave.subs(time, 0))+sp.integrate(sp.diff(weight, time)*(wave-wave.subs(time, 0)), (time, 0, duration))
        evidence.check('weighted_integration_by_parts_'+str(power), sp.simplify(direct-wave_form) == 0)
    evidence.report['symbolic_derivatives'] = dict(momentum=[str(value) for value in momentum_derivatives],
        force=[str(value) for value in force_derivatives])


def selected(case, fraction, power, stride=1):
    return next(row for row in case['integrals'] if row['fraction'] == fraction and row['power'] == power and row['stride'] == stride)


def canonical_reconstruction_closure(samples, duration, fraction, power):
    end = int(round((len(samples)-1)*fraction))
    chosen = samples[:end+1]
    times = np.array([row['time'] for row in chosen])
    force_split = np.array([math.fsum([row['raw_wave'], row['raw_material'], -row['raw_total']]) for row in chosen])
    momentum_split = np.array([math.fsum([row['wave_momentum'], row['material_momentum'], -row['canonical_source_momentum']]) for row in chosen])
    shifted = momentum_split-momentum_split[0]
    weight = (times/duration)**power
    derivative = np.zeros_like(times) if power == 0 else power/duration*(times/duration)**(power-1)
    return float(simpson(weight*force_split+derivative*shifted, x=times)-weight[-1]*shifted[-1])


def oracle_moment(case, fraction, power):
    return next(row['impulse'] for row in case['moments'] if row['fraction'] == fraction and row['power'] == power)


def main():
    evidence = EvidenceRun('annular-P2-source-impulse-comparison-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            original_instantaneous_force_requirement_unchanged=True, no_new_finite_element_evolution=True,
            finite_polynomial_family_not_a_weak_convergence_proof=True,
            sampled_bounds_not_continuous_time_supremum_bounds=True, no_threshold_tuned_to_pass=True,
            empirical_refinement_differences_not_rigorous_error_bounds=True)
        algebra(evidence)
        oracle = signed_source(evidence, 'annular-continuum-source-impulse-attempt01')
        cases = {}
        for branch in ['reference', 'MTS']:
            normal = signed_source(evidence, 'annular-P2-saved-impulse-'+branch+'-attempt01')
            coarse = signed_source(evidence, 'annular-P2-saved-impulse-coarse16-'+branch+'-attempt01')
            for case in normal['cases']+coarse['cases']:
                cases[branch, case['base_count'], case['steps']] = case
        tight = next(row for row in oracle['cases'] if row['degree'] == 512 and row['divisions'] == 16)
        looser_time = next(row for row in oracle['cases'] if row['degree'] == 512 and row['divisions'] == 8)
        looser_space = next(row for row in oracle['cases'] if row['degree'] == 384 and row['divisions'] == 16)
        duration = 4e-5
        rows = []
        for (branch, count, steps), case in cases.items():
            samples = case['samples'][::steps//16]
            evidence.check(branch+'_'+str(count)+'_'+str(steps)+'_same_17_times', len(samples) == 17
                and np.max(abs(np.array([row['time'] for row in samples])-np.array([row['time'] for row in tight['observables']]))) < 1e-18)
            for fraction in [.25, .5, .75, 1.]:
                for power in [0, 1, 2]:
                    label = branch+'_'+str(count)+'_'+str(steps)+'_'+str(fraction)+'_'+str(power)
                    measured = selected(case, fraction, power)
                    quadrature_half = selected(case, fraction, power, 2)
                    finite_common, finite_data = material_functional(samples, duration, fraction, power)
                    continuum_common, continuum_data = material_functional(tight['observables'], duration, fraction, power)
                    impulse = oracle_moment(tight, fraction, power)
                    shifted_difference = finite_data['shifted']-continuum_data['shifted']
                    force_difference = finite_data['forces']-continuum_data['forces']
                    coefficients, weight, derivative = [finite_data[name] for name in ['coefficients', 'weight', 'derivative']]
                    common_bound = abs(weight[-1]*shifted_difference[-1])+float(coefficients @ (abs(derivative*shifted_difference)+abs(weight*force_difference)))
                    common_difference = float(weight[-1]*shifted_difference[-1]-coefficients @ (derivative*shifted_difference+weight*force_difference))
                    outer_finite = measured['impulse']-finite_common
                    outer_continuum = continuum_common-impulse
                    difference = measured['impulse']-impulse
                    budget = abs(outer_finite)+common_bound+abs(outer_continuum)
                    evidence.check(label+'_discrete_telescope_and_bound',
                        abs(difference-outer_finite-common_difference-outer_continuum) < 2e-22
                        and abs(common_difference) <= common_bound+2e-22 and abs(difference) <= budget+2e-22)
                    reconstruction_closure = canonical_reconstruction_closure(case['samples'], duration, fraction, power)
                    evidence.check(label+'_canonical_balance_includes_inverse_and_split_residuals',
                        abs(measured['independent_momentum_balance_difference']-measured['canonical_quadrature_balance_defect']-reconstruction_closure) < 5e-21)
                    row = dict(branch=branch, base_count=count, steps=steps, fraction=fraction, power=power,
                        impulse=measured['impulse'], continuum_impulse=impulse, signed_error=difference,
                        relative_error=abs(difference/impulse) if impulse else None,
                        same_path_quadrature_difference=abs(measured['impulse']-quadrature_half['impulse']),
                        canonical_balance_defect=measured['canonical_quadrature_balance_defect'],
                        material_identity_difference=measured['independent_momentum_balance_difference'],
                        canonical_reconstruction_closure=reconstruction_closure,
                        raw_cancellation_scale=measured['cancellation_scale'],
                        continuum_time_difference=abs(impulse-oracle_moment(looser_time, fraction, power)),
                        continuum_space_difference=abs(impulse-oracle_moment(looser_space, fraction, power)),
                        finite_common_outer_defect=outer_finite, continuum_common_outer_defect=outer_continuum,
                        discrete_common_material_difference=common_difference,
                        discrete_common_material_bound=common_bound, computed_telescope_bound=budget,
                        common_node_maximum_momentum_difference=float(np.max(abs(finite_data['momenta']-continuum_data['momenta']))),
                        common_node_maximum_gravity_difference=float(np.max(abs(force_difference))),
                        valid_for_claim=False, source_path=case['source_path'])
                    rows.append(row)
        refinements = []
        for branch in ['reference', 'MTS']:
            final_steps = 128 if branch == 'MTS' else 64
            pairs = [('coarse_time', (257, 16), (257, 32)),
                ('fine_time', (513, final_steps//2), (513, final_steps)),
                ('space_and_resolved_time', (257, 32), (513, final_steps))]
            for kind, first, second in pairs:
                for fraction in [.25, .5, .75, 1.]:
                    for power in [0, 1, 2]:
                        left = selected(cases[(branch,)+first], fraction, power)['impulse']
                        right = selected(cases[(branch,)+second], fraction, power)['impulse']
                        refinements.append(dict(branch=branch, kind=kind, first=list(first), second=list(second),
                            fraction=fraction, power=power, signed_change=right-left, valid_for_claim=False))
        evidence.report.update(cases=rows, refinements=refinements,
            original_endpoint_MTS_discrepancy_remains_unresolved=True,
            instantaneous_and_integrated_requirements_not_interchangeable=True)
        evidence.check('96_matched_moments_and_72_fair_refinements', len(rows) == 96 and len(refinements) == 72)
        path = evidence.output/'matched-impulses.csv'
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with path.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        evidence.check('all_rows_parse_and_sources_exist', len(parsed) == 96 and all(None not in row
            and row['valid_for_claim'] == 'False' and (evidence.root/row['source_path']).is_file() for row in parsed))
        evidence.own(path, 'outputs')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        summary = [row for row in rows if row['fraction'] == 1 and row['power'] == 0]
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), endpoint_impulses=summary)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
