from __future__ import annotations

from pathlib import Path
import numpy as np
import sympy as sp

from interior_common import ROOT, modest_process, read_json, save
from local_system_v2 import LocalSystem, scalar_schur


def main():
    modest_process()
    report = read_json(ROOT/'results/reduced-v2/status.json')
    symbols = sp.symbols(' '.join(report['symbols']), positive=True)
    environment = dict(zip(report['symbols'], symbols))
    parse = lambda value: sp.sympify(value, locals=environment)
    radius, alpha, metric, field, gradient, rotation, potential, force, second = symbols
    hessian = sp.Matrix([[parse(value) for value in row] for row in report['reduced_hessian']])
    principal = hessian.extract([0,2],[0,2])
    mixed = hessian.extract([0,2],[1,3])
    kinetic = metric*gradient**2+rotation**2*field**2
    density, pressure = kinetic/2+potential, kinetic/2-potential
    metric_prime = (1-metric)/radius-2*alpha*radius*density
    lapse_gradient = (1-metric+2*alpha*radius**2*pressure)/(2*radius*metric)
    field_second = (force-rotation**2*field)/metric-(2/radius+lapse_gradient+metric_prime/(2*metric))*gradient
    seed_log_derivative = metric_prime/(2*metric)+field_second/gradient
    scalar_pivot = 2*metric**2/(3*alpha*radius**2*metric*gradient**2+2*metric)
    flows = [1,0,metric_prime,gradient,field_second,-lapse_gradient*rotation,force*gradient,second*gradient,0]
    system = LocalSystem()
    background = system.background
    position = background.radius*np.r_[.0005,.001,np.linspace(.005,.995,199),.999,.9995]
    data, coefficients, derivatives, local, contacts = system.values(position)
    phase, principal_values, mixed_values, potential_values = scalar_schur(local)
    arguments = [position,background.alpha,data['metric'],data['field'],data['gradient'],background.frequency/data['lapse'],data['energy'],data['force'],data['second']]
    pressure_values = (data['metric']*data['gradient']**2+data['rotation2']*data['field']**2)/2-data['energy']
    lapse_gradient_values = (1-data['metric']+2*background.alpha*position**2*pressure_values)/(2*position*data['metric'])
    measure_gradient = lapse_gradient_values+2/position-data['metric_prime']/(2*data['metric'])
    scales = np.stack([np.sqrt(2*background.alpha/3)*position,np.ones_like(position)], axis=1)
    rows = []
    for label, seed_coefficient in [('symmetric-only',sp.S.Zero),('scalar-diagonal-seed',principal[1,1]),('scalar-pivot-seed',scalar_pivot)]:
        deformation = (mixed+mixed.T)/2+sp.diag(0,seed_coefficient*seed_log_derivative)
        assert all(not value.has(second) for value in deformation)
        deformation_prime = deformation.applyfunc(lambda value:sum(sp.diff(value, symbol)*flow for symbol,flow in zip(symbols,flows)))
        evaluator = sp.lambdify(symbols,list(deformation)+list(deformation_prime),'numpy',cse=True)
        evaluated = np.array([np.broadcast_to(value,position.shape) for value in evaluator(*arguments)])
        deformation_values = np.moveaxis(evaluated[:4].reshape(2,2,len(position)),-1,0)
        derivative_values = np.moveaxis(evaluated[4:].reshape(2,2,len(position)),-1,0)
        remainder_mixed = mixed_values-deformation_values
        corrected = potential_values-derivative_values-measure_gradient[:,None,None]*deformation_values
        corrected -= np.matmul(np.swapaxes(remainder_mixed,1,2),np.linalg.solve(principal_values,remainder_mixed))
        normalized = corrected*scales[:,:,None]*scales[:,None,:]*position[:,None,None]**2
        eigenvalues = np.linalg.eigvalsh(normalized)
        worst = int(np.argmin(eigenvalues[:,0]))
        rows.append(dict(method=label,samples=len(position),minimum_scaled_potential_eigenvalue=float(eigenvalues[worst,0]),
            worst_radius_fraction=float(position[worst]/background.radius),negative_samples=int(np.count_nonzero(eigenvalues[:,0]<0)),
            samples_are_continuum_proof=False,values=[dict(radius_fraction=float(location/background.radius),eigenvalues=values.tolist()) for location,values in zip(position,eigenvalues)]))
        print({key:value for key,value in rows[-1].items() if key!='values'},flush=True)
    save('potential-probe-v2',Path(__file__),dict(rows=rows,
        deformation_identity='V_P=C-Pprime-(a_prime/a)P-(B-P)^T A^-1(B-P); E=.5int a[(Yprime+A^-1(B-P)Y)^T A (Yprime+A^-1(B-P)Y)+Y^T V_P Y]+.5[a Y^T P Y].',
        seed='zeta=sqrt(F) h_prime; P=sym(B)+diag(0,coefficient*zeta_prime/zeta)',
        scope='Interior numerical scouting only on the saved background; no eigenvalue or continuum potential positivity proof.',
        derivatives='Exact symbolic background chain rule, not finite differences.',
        new_background_or_wave_solves=0),[ROOT/'results/reduced-v2/status.json',ROOT/'results/energy-v2/status.json',background.profile.path])


if __name__ == '__main__':
    main()
