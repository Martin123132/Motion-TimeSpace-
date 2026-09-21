import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

import json
import numpy as np
from annular_reference_continuum_shell_20260914 import (
    EvidenceRun, continuum_initial, initial_case, independent_radial_collars)
from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_constrained_mass_relative_energy_20260914 import quadrature, density_energy, uniform_constants


def run():
    evidence = EvidenceRun('annular-reference-continuum-shell-independent-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        main_path = intake/'annular-reference-continuum-shell-attempt01/status.json'
        main = json.loads(main_path.read_text())
        evidence.own(main_path)
        evidence.check('main_complete',main['state']=='complete' and all(row['passed'] for row in main['checks']))
        refined = continuum_initial(3e-13,.001)
        evidence.check('continuum_IVP_refinement',
                       abs(refined[0].y[0,-1]-main['continuum_initial_mass_minus'])<2e-11)
        for count in [33,129,257]:
            original = next(row for row in main['cases'] if row['count']==count)
            replacement = initial_case(count,16,refined)
            boundary_error = max(abs(replacement[key]-original[key]) for key in
                                 ['shell_mass_jump','outer_clock','required_surface_pressure'])
            evidence.check(str(count)+'_layer_radial_refinement',boundary_error<1e-10,boundary_error)
            moment_error = max(abs(np.array(replacement['weak_moments'])-original['weak_moments']))
            evidence.check(str(count)+'_density_refinement',moment_error<1e-9,moment_error)
        for count in [33,129]:
            case = independent_radial_collars(count)
            evidence.report['cases'].append(case)
            evidence.check(str(count)+'_adaptive_radial_mass',case['mass_error']<1e-10,case['mass_error'])
            evidence.check(str(count)+'_adaptive_radial_lapse',case['log_lapse_error']<1e-10,case['log_lapse_error'])
        constants = uniform_constants()
        radius,ceiling = constants['radius_lower'],constants['radius_upper']
        coefficient_min = radius**2*constants['weight_lower']
        source_bound_constant = ceiling**4/(2*coefficient_min**2)
        offsets,weights = quadrature(32)
        for count in [33,65,129]:
            path = intake/'annular-compatible-h-evolution-main-attempt01'/('GR_control_count'+str(count)+'.npz')
            evidence.own(path)
            trajectory = np.load(path)
            system = CompatibleEvolution(count,False,degree=8)
            for index in [0,8,16]:
                time,state = trajectory['times'][index],trajectory['states'][index]
                geometry = system.geometry(time,state)
                velocity = system.rhs(time,state)
                energy_velocity = float(density_energy(system,velocity))
                data = geometry.layer(offsets)
                source_energy = float(weights @ data['potential'][:,-1])
                bound = source_bound_constant*system.spacing*energy_velocity
                evidence.check(str(count)+'_'+str(index)+'_source_scalar_energy_bound',source_energy<=bound+1e-13,
                               dict(actual=source_energy,bound=bound,EV=energy_velocity,time=float(time)))
                edge_coefficient = (data['C'][:,:-1]+data['C'][:,1:])/2
                edge_flux = edge_coefficient*np.diff(data['chi'],axis=1)/system.spacing
                left_norm_square = float(weights @ edge_flux[:,0]**2)
                left_bound = 2*ceiling**2*system.node_weights[0]*energy_velocity
                evidence.check(str(count)+'_'+str(index)+'_left_flux_bound',left_norm_square<=left_bound+1e-13)
        evidence.report['source_scalar_boundary_energy_bound_constant'] = source_bound_constant
        evidence.report['saved_trajectory_checks_do_not_extend_proven_time_interval'] = True
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

