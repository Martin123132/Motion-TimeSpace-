import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
import sympy as sp
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_source_gravity_collar_20260914 import DustGravityCollar


def main():
    evidence=EvidenceRun('annular-source-gravity-algebra-attempt01',__file__)
    try:
        radius,mass,source,momentum,lapse,coupling,weight,jacobian=sp.symbols('R mu S p N kappa w J',positive=True)
        geometry=1-2*mass/radius
        root=sp.sqrt(geometry)
        energy=sp.sqrt(source**2+geometry*momentum**2)
        loading=coupling*weight*root*energy
        loading_derivative=-coupling*weight*(source**2+2*geometry*momentum**2)/(radius*root*energy)
        evidence.check('radial_constraint_exact_Newton_derivative',sp.simplify(sp.diff(loading,mass)-loading_derivative)==0)
        mass_radial=loading/jacobian
        root_radial=(mass/radius**2-mass_radial/radius)/root
        lapse_radial=lapse*(mass/(radius**2*geometry)+coupling*weight*root*momentum**2/(radius*energy*jacobian))
        raw_force=-energy*lapse_radial-lapse*root*root_radial*momentum**2/energy
        reduced_force=-lapse*mass/radius**2*(energy/geometry+momentum**2/energy)
        evidence.check('source_force_density_cancellation',sp.simplify(raw_force-reduced_force)==0)
        velocity=lapse*geometry*momentum/energy
        evidence.check('source_current_is_advective_mass_transport',
                       sp.simplify(velocity*loading-coupling*lapse*root**3*momentum*weight)==0)
        proper_rate=geometry*momentum/source
        proper_clock=lapse*source/energy
        derivative=(sp.diff(proper_rate,radius)*velocity+sp.diff(proper_rate,momentum)*reduced_force)/proper_clock
        evidence.check('conditional_proper_time_GR_acceleration',sp.simplify(derivative+mass/radius**2)==0)
        binding=root*energy/source
        derivative_binding=sp.diff(binding,radius)*velocity+sp.diff(binding,momentum)*reduced_force
        evidence.check('conditional_material_binding_first_integral',sp.simplify(derivative_binding)==0)
        phase=sp.symbols('eta',positive=True)
        initial=sp.symbols('R0',positive=True)
        exact_radius=initial*(1+sp.cos(phase))/2
        exact_clock=sp.sqrt(initial**3/(8*mass))*(phase+sp.sin(phase))
        exact_rate=sp.diff(exact_radius,phase)/sp.diff(exact_clock,phase)
        exact_acceleration=sp.diff(exact_rate,phase)/sp.diff(exact_clock,phase)
        evidence.check('independent_cycloid_solves_GR_equation',sp.trigsimp(exact_acceleration+mass/exact_radius**2)==0)
        for width in [.001,.00001]:
            system=DustGravityCollar(16,width)
            state=system.initial_state.copy()
            state[system.count:2*system.count]=-.00008*(1+.03*system.offsets)
            data=system.geometry(state)
            flow=system.rhs(0,state)
            perturbed=system.geometry(state.astype(complex)+1e-25j*flow)
            material_mass_rate=perturbed['mass'].imag/1e-25
            evidence.check(str(width)+'_constraint_recomputed_material_mass_identity',
                           np.max(abs(material_mass_rate))<2e-11,float(np.max(abs(material_mass_rate))))
            momentum_rate=flow[system.count:2*system.count]
            radial_mass=data['mass_z']/data['position_z']
            radial_U=(data['mass']/data['position']**2-radial_mass/data['position'])/data['U']
            radial_N=data['N']*data['log_N_z']/data['position_z']
            unsimplified=-data['E']*radial_N-data['N']*data['U']*radial_U*data['momentum']**2/data['E']
            evidence.check(str(width)+'_raw_metric_gradient_force_matches',
                           np.max(abs(unsimplified-momentum_rate))<2e-13,float(np.max(abs(unsimplified-momentum_rate))))
            initial_data=system.initial_geometry
            acceleration=-initial_data['N']**2*initial_data['mass']/initial_data['position']**2
            direct_gradient=system.derivative @ acceleration
            formula,leading,duration=system.initial_focusing()
            evidence.check(str(width)+'_derived_initial_label_focusing',
                           np.max(abs(formula-direct_gradient))<2e-11,float(np.max(abs(formula-direct_gradient))))
        evidence.report.update(scope='Independent pressureless source layers and live spherical canonical gravity, scalar identically zero.',
                               source_parameters_parent_derived=False,
                               full_scalar_gravity_coupling_evolved=False)
        for name in ['DERIVATION-20260914-moving-finite-collar-source-action.md',
                     'DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md']:
            evidence.own(evidence.root/name)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

