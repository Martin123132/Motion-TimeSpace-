from __future__ import annotations

from pathlib import Path
import numpy as np
import sympy as sp

from interior_common import ROOT, modest_process, save
from local_system import LocalSystem as SupersededSystem
from local_system_v2 import LocalSystem, scalar_schur


def constraint_residual(system, factors):
    background = system.background
    radius = background.radius
    position = radius*np.linspace(.025,.975,39)
    data, coefficients, derivatives, matrix, contact = system.values(position)
    coordinate = sp.symbols('x',positive=True)
    master = coordinate**3/(1+coordinate**5)
    matter = coordinate**2*(1-coordinate)**2
    evaluate = sp.lambdify(coordinate,[master,sp.diff(master,coordinate),sp.diff(master,coordinate,2),matter,sp.diff(matter,coordinate),sp.diff(matter,coordinate,2)],'numpy')
    profiles = evaluate(position/radius)
    master_values, master_first, master_second = factors[0]*profiles[0], factors[0]*profiles[1]/radius, factors[0]*profiles[2]/radius**2
    scalar, scalar_first, scalar_second = factors[1]*profiles[3], factors[1]*profiles[4]/radius, factors[1]*profiles[5]/radius**2
    phase, phase_first = factors[2]*profiles[3], factors[2]*profiles[4]/radius
    vector = np.array([master_first,master_values,scalar_first,scalar,phase])
    vector_first = np.array([master_second,master_first,scalar_second,scalar_first,phase_first])
    names = ['k_Zprime','k_Z','k_wprime','k_w','k_pibar']
    angular = sum(coefficients[name]*vector[index] for index,name in enumerate(names))
    angular_prime = sum(derivatives[name]*vector[index]+coefficients[name]*vector_first[index] for index,name in enumerate(names))
    difference = coefficients['beta']/data['metric']*(3*master_values/position-angular)
    difference_prime = (derivatives['beta']/data['metric']-coefficients['beta']*data['metric_prime']/data['metric']**2)*(3*master_values/position-angular)+coefficients['beta']/data['metric']*(3*master_first/position-3*master_values/position**2-angular_prime)
    radial = position*angular_prime+difference
    amplitude = scalar+coefficients['a']*angular
    amplitude_prime = scalar_first+coefficients['a_prime']*angular+coefficients['a']*angular_prime
    momentum = phase+coefficients['c']*angular_prime+coefficients['d']*angular
    curvature = 2*data['metric']/position*difference_prime+((6+2*data['metric'])/position**2+2*data['metric_prime']/position)*difference+((6-2*data['metric'])/position+data['metric_prime'])*angular_prime+4*angular/position**2
    density = background.frequency*data['field']/data['lapse']*momentum-data['rotation2']*data['field']**2*(radial+2*angular)/2-data['rotation2']*data['field']*amplitude-data['metric']*data['gradient']**2*radial/2+data['metric']*data['gradient']*amplitude_prime+data['force']*amplitude
    scale = max(np.max(abs(curvature)),np.max(abs(4*background.alpha*density)),1e-30)
    return float(np.max(abs(curvature-4*background.alpha*density))/scale)


def main():
    modest_process()
    correct, superseded = LocalSystem(), SupersededSystem()
    background = correct.background
    gravity_scale = np.sqrt(background.alpha)*background.radius
    configurations = [('gravity',[gravity_scale,0.,0.]),('scalar',[0.,1.,0.]),('phase',[0.,0.,1.]),('mixed',[gravity_scale,.3,-.2])]
    rows = []
    for label, factors in configurations:
        current = constraint_residual(correct,factors)
        rejected = constraint_residual(superseded,factors)
        assert current < 1e-10 and rejected > 1e-4, (label,current,rejected)
        rows.append(dict(profile=label,correct_v2_relative_error=current,superseded_v1_relative_error=rejected))
    position = background.radius*np.linspace(.005,.995,199)
    data, coefficients, derivatives, matrix, contact = correct.values(position)
    phase, principal, mixed, potential = scalar_schur(matrix)
    generator = np.random.default_rng(47)
    vector = generator.normal(size=(len(position),5))
    vector[:,:2] *= np.sqrt(background.alpha)*position[:,None]
    original = np.einsum('qi,qij,qj->q',vector,matrix,vector)
    shift = np.einsum('qi,qi->q',matrix[:,:4,4],vector[:,:4])/phase
    spatial = matrix[:,:4,:4]-np.einsum('qi,qj->qij',matrix[:,:4,4],matrix[:,:4,4])/phase[:,None,None]
    completed = phase*(vector[:,4]+shift)**2+np.einsum('qi,qij,qj->q',vector[:,:4],spatial,vector[:,:4])
    phase_error = float(np.max(abs(original-completed))/max(np.max(abs(original)),1e-30))
    phase_load = background.alpha*position**2*data['rotation2']*data['field']**2
    gradient_load = background.alpha*position**2*data['metric']*data['gradient']**2
    beta = coefficients['beta']
    denominator = 3*(beta+gradient_load)**2+phase_load*(3*gradient_load+2*data['metric'])
    gravity = 9*beta**2*(3*gradient_load+2*data['metric'])/(4*background.alpha*position**2*denominator)
    eta = 2*background.alpha*position**2*data['metric']*data['gradient']*(3*beta-2*data['metric'])/(3*beta*(3*gradient_load+2*data['metric']))
    pivot = 2*data['metric']**2/(3*gradient_load+2*data['metric'])
    derivative_vector = vector[:,[0,2]]
    original_gradient = np.einsum('qi,qij,qj->q',derivative_vector,principal,derivative_vector)
    squared_gradient = gravity*(derivative_vector[:,0]+eta*derivative_vector[:,1])**2+pivot*derivative_vector[:,1]**2
    gradient_error = float(np.max(abs(original_gradient-squared_gradient))/np.max(abs(original_gradient)))
    assert phase_error < 1e-12 and gradient_error < 1e-12
    save('controls-v2',Path(__file__),dict(constraint_rows=rows,phase_completion_relative_error=phase_error,
        principal_square_relative_error=gradient_error,seed=47,random_vectors=len(position),
        superseded_attempt_detected=True,old_files_used_only_as_negative_control=True),
        [ROOT/'results/energy-v2/status.json',ROOT/'results/energy/status.json',background.profile.path])
    print(dict(rows=rows,phase_error=phase_error,gradient_error=gradient_error),flush=True)


if __name__ == '__main__':
    main()
