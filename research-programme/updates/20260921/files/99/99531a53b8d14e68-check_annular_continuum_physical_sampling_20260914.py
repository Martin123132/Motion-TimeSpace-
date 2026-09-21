import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
from scipy.interpolate import CubicSpline
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_constrained_mass_relative_energy_20260914 import quadrature


def run():
    evidence = EvidenceRun('annular-continuum-physical-sampling-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path = intake/'annular-independent-continuum-attempt01/continuum_count2049.npz'
        evidence.own(path)
        target = np.load(path)
        coarse_path = intake/'annular-independent-continuum-attempt01/continuum_count1025.npz'
        evidence.own(coarse_path)
        coarse = np.load(coarse_path)
        offsets,weights = quadrature(20)
        evidence.report['scope'] = 'Supplement: compare at actual collar positions, not base labels. Scalar and momentum on strictly interior nodes; gradient on all edge midpoints. No extrapolation or refitting.'
        for count in [33,65,129]:
            for gram,label in [(False,'reference'),(True,'MTS')]:
                system = CompatibleEvolution(count,gram)
                filename = ('metric_Gram' if gram else 'GR_control')+'_count'+str(count)+'.npz'
                path = intake/'annular-compatible-h-evolution-main-attempt01'/filename
                evidence.own(path)
                archive = np.load(path)
                for time_index,saved_index in [(2,8),(3,16)]:
                    time = float(target['times'][time_index])
                    data = system.geometry(time,archive['states'][saved_index]).layer(offsets)
                    nodes = data['R'][:,1:-1]
                    edges = (data['R'][:,:-1]+data['R'][:,1:])/2
                    fields = target['states'][time_index].reshape(3,-1)
                    reference = [CubicSpline(target['radii'],fields[index]) for index in range(3)]
                    momentum_difference = data['p'][:,1:-1]-reference[2](nodes)
                    gradient_difference = np.diff(data['chi'],axis=1)/system.spacing-reference[1](edges)
                    scalar_difference = data['chi'][:,1:-1]-reference[0](nodes)
                    pnorm = float(np.sqrt(weights @ np.sum(system.spacing*momentum_difference**2/nodes**2,axis=1)))
                    unorm = float(np.sqrt(weights @ np.sum(system.spacing*edges**2*gradient_difference**2,axis=1)))
                    cnorm = float(np.sqrt(weights @ np.sum(system.spacing*scalar_difference**2,axis=1)))
                    coarse_fields = coarse['states'][time_index].reshape(3,-1)
                    pnoise = reference[2](nodes)-CubicSpline(coarse['radii'],coarse_fields[2])(nodes)
                    unoise = reference[1](edges)-CubicSpline(coarse['radii'],coarse_fields[1])(edges)
                    pnoise_norm = float(np.sqrt(weights @ np.sum(system.spacing*pnoise**2/nodes**2,axis=1)))
                    unoise_norm = float(np.sqrt(weights @ np.sum(system.spacing*edges**2*unoise**2,axis=1)))
                    row = dict(branch=label,count=count,time=time,chi_L2=cnorm,
                               momentum_energy_norm=pnorm,gradient_energy_norm=unorm,
                               energy_error=.5*(pnorm**2+unorm**2),momentum_refinement_noise=pnoise_norm,
                               gradient_refinement_noise=unoise_norm)
                    evidence.report['cases'].append(row)
                    prefix = label+str(count)+'_'+str(time)
                    evidence.check(prefix+'_inside_domain',nodes.min()>5 and nodes.max()<6 and edges.min()>5 and edges.max()<6)
                    evidence.check(prefix+'_target_resolved',pnoise_norm<.02*pnorm and unoise_norm<.02*unorm)
        for label in ['reference','MTS']:
            for time in [.03,.06]:
                rows = [row for row in evidence.report['cases'] if row['branch']==label and row['time']==time]
                for key in ['chi_L2','momentum_energy_norm','gradient_energy_norm','energy_error']:
                    evidence.check(label+str(time)+'_refines_'+key,
                                   all(second[key]<first[key] for first,second in zip(rows,rows[1:])))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

