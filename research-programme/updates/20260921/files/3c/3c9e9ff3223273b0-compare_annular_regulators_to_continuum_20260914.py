import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from scipy.interpolate import CubicSpline
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_constrained_mass_relative_energy_20260914 import quadrature,density_energy
from annular_independent_continuum_20260914 import ContinuumEvolution


def compare(system,time,state,archive,time_index):
    offsets,weights = quadrature(20)
    geometry = system.geometry(time,state)
    data = geometry.layer(offsets)
    count = len(system.radii)
    continuous_count = len(archive['radii'])
    stride = (continuous_count-1)//(count-1)
    if stride*(count-1)!=continuous_count-1 or stride%2:
        raise ValueError('Use nested continuum nodes and edge midpoints.')
    continuous = archive['states'][time_index].reshape(3,continuous_count)
    scalar = continuous[0,::stride]
    gradient = continuous[1,stride//2:-1:stride]
    momentum = continuous[2,::stride]
    edge_radius = (system.radii[:-1]+system.radii[1:])/2
    raw_gradient = np.diff(data['chi'],axis=1)/system.spacing
    chi_norm = np.sqrt(weights @ np.sum(system.node_weights*(data['chi']-scalar)**2,axis=1))
    momentum_norm = np.sqrt(weights @ np.sum(system.node_weights*(data['p']-momentum)**2/system.radii**2,axis=1))
    gradient_norm = np.sqrt(weights @ np.sum(system.spacing*edge_radius**2*(raw_gradient-gradient)**2,axis=1))
    probes = np.linspace(5.,5.95,193)
    metric = geometry.metric(probes)
    target_mass = CubicSpline(archive['radii'],archive['masses'][time_index])(probes)
    target_lapse = CubicSpline(archive['radii'],archive['log_lapses'][time_index])(probes)
    continuous_system = ContinuumEvolution(continuous_count)
    continuous_geometry = continuous_system.geometry(archive['states'][time_index])
    boundary = geometry.metric([geometry.edges[-1]])
    base_energy = float(density_energy(system,state))
    extra_energy = float(density_energy(system,state,extra=True)) if system.gram else 0.
    result = dict(count=count,time=float(time),chi_L2=float(chi_norm),
                  momentum_energy_norm=float(momentum_norm),gradient_energy_norm=float(gradient_norm),
                  energy_error=float((momentum_norm**2+gradient_norm**2)/2),
                  mass_max_error=float(abs(metric['mu']-target_mass).max()),
                  log_lapse_max_error=float(abs(metric['log_N']-target_lapse).max()),
                  total_mass_error=float(abs(boundary['mu'][0]-continuous_geometry['mass_plus'])),
                  raw_base_energy_error=float(abs(base_energy-archive['energies'][time_index])),
                  raw_total_energy_error=float(abs(base_energy+extra_energy-archive['energies'][time_index])),
                  raw_base_energy=base_energy,extra_Gram_energy=extra_energy,
                  outer_clock=float(boundary['N'][0]/boundary['U'][0]),
                  target_outer_clock=float(continuous_geometry['outer_clock']))
    profiles = dict(node_radii=system.radii,edge_radii=edge_radius,
                    scalar_mean=weights @ data['chi'],momentum_mean=weights @ data['p'],
                    gradient_mean=weights @ raw_gradient,
                    metric_probes=probes,mass_difference=metric['mu']-target_mass,
                    log_lapse_difference=metric['log_N']-target_lapse)
    return result,profiles


def target_refinement_noise(count,fine,coarse,index):
    nodes = np.linspace(5.,6.,count)
    edges = (nodes[:-1]+nodes[1:])/2
    weight = np.full(count,1/(count-1))
    weight[[0,-1]] /= 2
    fine_state = fine['states'][index].reshape(3,len(fine['radii']))
    coarse_state = coarse['states'][index].reshape(3,len(coarse['radii']))
    difference = [CubicSpline(fine['radii'],fine_state[field])(nodes)-
                  CubicSpline(coarse['radii'],coarse_state[field])(nodes) for field in [0,2]]
    gradient_difference = CubicSpline(fine['radii'],fine_state[1])(edges)-CubicSpline(coarse['radii'],coarse_state[1])(edges)
    probes = np.linspace(5.,5.95,193)
    return dict(chi_L2=float(np.sqrt(np.sum(weight*difference[0]**2))),
                momentum_energy_norm=float(np.sqrt(np.sum(weight*difference[1]**2/nodes**2))),
                gradient_energy_norm=float(np.sqrt(np.sum(edges**2*gradient_difference**2)/(count-1))),
                mass_max_error=float(abs(CubicSpline(fine['radii'],fine['masses'][index])(probes)-
                                             CubicSpline(coarse['radii'],coarse['masses'][index])(probes)).max()),
                log_lapse_max_error=float(abs(CubicSpline(fine['radii'],fine['log_lapses'][index])(probes)-
                                                  CubicSpline(coarse['radii'],coarse['log_lapses'][index])(probes)).max()))


def run():
    evidence = EvidenceRun('annular-continuum-regulator-comparison-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        baseline = intake/'annular-independent-continuum-attempt01'
        status_path = baseline/'status.json'
        baseline_status = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('continuum_baseline_passed',baseline_status['state']=='complete' and
                       all(row['passed'] for row in baseline_status['checks']))
        archives = {}
        for count in [1025,2049]:
            path = baseline/('continuum_count'+str(count)+'.npz')
            evidence.own(path)
            archives[count] = dict(np.load(path,allow_pickle=False))
        evidence.report['comparison_convention'] = 'Joint-layer canonical p/gradient energy and scalar L2 at common base nodes; mass/lapse at fixed physical radii5..5.95; source full-support mass separately.'
        evidence.report['no_parameters_refitted'] = True
        evidence.report['continuum_refinement_noise_is_not_a_rigorous_error_bound'] = True
        evidence.report['time_0002_within_proof_interval_long_times_diagnostic_only'] = True
        for count in [33,65,129]:
            noise = {str(time):target_refinement_noise(count,archives[2049],archives[1025],index)
                     for index,time in enumerate(archives[2049]['times'])}
            for gram,label in [(False,'reference'),(True,'MTS')]:
                system = CompatibleEvolution(count,gram,degree=8)
                if gram:
                    short_solution = system.integrate(duration=.0002,divisor=4)
                    short_state = short_solution.y[:,-1]
                    short_path = evidence.output/('MTS_short_count'+str(count)+'.npz')
                    np.savez_compressed(short_path,state=short_state,time=.0002)
                    evidence.own(short_path,'outputs')
                else:
                    short_path = intake/'annular-reference-layer-locking-attempt01'/('reference_count'+str(count)+'.npz')
                    evidence.own(short_path)
                    short_state = np.load(short_path)['states'][-1]
                path = intake/'annular-compatible-h-evolution-main-attempt01'/(
                    ('metric_Gram' if gram else 'GR_control')+'_count'+str(count)+'.npz')
                evidence.own(path)
                saved = np.load(path,allow_pickle=False)
                states = [saved['states'][0],short_state,saved['states'][8],saved['states'][16]]
                evidence.check(label+str(count)+'_saved_times_match',
                               np.allclose(saved['times'][[0,8,16]],[0.,.03,.06],atol=1e-15,rtol=0))
                for index,(time,state) in enumerate(zip(archives[2049]['times'],states)):
                    row,profiles = compare(system,time,state,archives[2049],index)
                    row.update(branch=label,continuum_refinement_noise=noise[str(time)])
                    evidence.report['cases'].append(row)
                    prefix = label+str(count)+'_'+str(time)
                    evidence.check(prefix+'_finite_metrics',all(np.isfinite(row[key]) for key in
                                   ['chi_L2','momentum_energy_norm','gradient_energy_norm','energy_error',
                                    'mass_max_error','log_lapse_max_error']))
                    for key,value in row['continuum_refinement_noise'].items():
                        evidence.check(prefix+'_target_resolved_'+key,value<=.02*row[key]+1e-14,
                                       dict(target_difference=value,regulator_error=row[key]))
                    if count==129 and time==.06:
                        plot_path = evidence.output/(label+'_final_profiles.npz')
                        np.savez_compressed(plot_path,**profiles)
                        evidence.own(plot_path,'outputs')
                evidence.save()
                print(label+' '+str(count)+' compared',flush=True)
        for label in ['reference','MTS']:
            for time in archives[2049]['times']:
                selected = [row for row in evidence.report['cases'] if row['branch']==label and row['time']==time]
                for key in ['chi_L2','momentum_energy_norm','gradient_energy_norm','energy_error',
                            'mass_max_error','log_lapse_max_error','total_mass_error']:
                    values = [row[key] for row in selected]
                    evidence.check(label+'_'+str(time)+'_refines_'+key,
                                   all(second<first for first,second in zip(values,values[1:])),values)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

