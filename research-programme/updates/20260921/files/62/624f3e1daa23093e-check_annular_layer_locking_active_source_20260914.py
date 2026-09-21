import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_reference_layer_locking_20260914 import pair_diagnostics
from annular_constrained_mass_relative_energy_20260914 import density_energy


def prepare(count):
    system = CompatibleEvolution(count,False,degree=8)
    state = system.initial_state.copy()
    middle = (system.radii[:-1]+system.radii[1:])/2
    target_force = .004*np.sin(np.pi*(middle-5)/2)
    target_force_rate_part = .0003*np.sin(np.pi*(middle-5)/2)
    for iteration in range(24):
        geometry = system.geometry(0.,state)
        data = geometry.layer(system.grid.offsets)
        edge = (data['C'][:,:-1]+data['C'][:,1:])/2
        kinetic = data['N']*data['U']/data['R']**2
        scalar = -system.spacing*np.cumsum((target_force/edge)[:,::-1],axis=1)[:,::-1]
        velocity = -system.spacing*np.cumsum((target_force_rate_part/edge)[:,::-1],axis=1)[:,::-1]
        momentum = velocity/kinetic[:,:-1]
        values = np.column_stack([scalar,momentum,np.zeros(len(system.grid.offsets)),
                                  np.full(len(system.grid.offsets),.003)])
        replacement = system.pack(values,0.)
        error = float(abs(replacement-state).max())
        state = replacement
        if error<3e-15:
            break
    else:
        raise RuntimeError('Flux-compatible preparation did not converge.')
    data = system.geometry(0.,state).layer(system.grid.offsets)
    edge = (data['C'][:,:-1]+data['C'][:,1:])/2
    force = edge*np.diff(data['chi'],axis=1)/system.spacing
    return system,state,float(abs(force-target_force).max()),iteration+1


def run():
    evidence = EvidenceRun('annular-reference-layer-locking-active-source-attempt01',__file__)
    try:
        evidence.report['scope'] = 'Different explicitly manufactured flux-compatible initial data; actual constrained reference equations, not the original compact preparation or a new trajectory.'
        for count in [33,65,129]:
            system,state,defect,iterations = prepare(count)
            row,raw = pair_diagnostics(system,0.,state,order=16)
            row.update(flux_preparation_defect=defect,preparation_iterations=iterations,
                       state_energy=float(density_energy(system,state)))
            evidence.report['cases'].append(row)
            label = str(count)
            evidence.check(label+'_flux_preparation',defect<1e-11,defect)
            evidence.check(label+'_nonzero_source_force',float(abs(raw['force'][:,-1]).min())>.003)
            evidence.check(label+'_nonzero_boundary_forcing',row['force_boundary_residual_square']>1e-18,
                           row['force_boundary_residual_square'])
            evidence.check(label+'_live_pair_identity',row['balance_error']<1e-13)
            evidence.check(label+'_actual_energy_below_common_ceiling',row['state_energy']<2.08222448216064)
            evidence.check(label+'_analytic_forcing_bound',row['forcing_square']<=row['analytic_forcing_square_bound'])
            path = evidence.output/('active_source_count'+str(count)+'.npz')
            np.savez_compressed(path,state=state)
            evidence.own(path,'outputs')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

