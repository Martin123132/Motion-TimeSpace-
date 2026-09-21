from derive_annular_source_gravity_20260914 import EvidenceRun, DustGravityCollar
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
import json


def main():
    evidence=EvidenceRun('annular-source-gravity-limit-algebra-attempt01',__file__)
    try:
        radius,mass,source,momentum,coupling,weight,slope=sp.symbols('R mu S p kappa w J',positive=True)
        geometry=1-2*mass/radius
        root=sp.sqrt(geometry)
        energy=sp.sqrt(source**2+geometry*momentum**2)
        loading=coupling*weight*root*energy
        root_log_z=(mass*slope/radius**2-loading/radius)/geometry
        lapse_log_z=slope*mass/(radius**2*geometry)+coupling*weight*root*momentum**2/(radius*energy)
        kernel=coupling*weight*(source**2+2*geometry*momentum**2)/(radius*root*energy)
        evidence.check('derivative_free_lapse_identity',sp.simplify(lapse_log_z-root_log_z-kernel)==0)
        system=DustGravityCollar(24,.001)
        state=system.initial_state.copy()
        state[system.count:2*system.count]=-.0002*(1+.04*system.offsets)
        data=system.geometry(state)
        integrand=system.coupling*system.shape*(system.source_mass**2+2*data['F']*data['momentum']**2)
        integrand/=data['position']*data['U']*data['E']
        primitive=system.integral @ integrand
        alternative=data['U']*np.exp(primitive-primitive[-1])
        difference=float(np.max(abs(alternative-data['N'])))
        evidence.check('independent_lapse_evaluation',difference<2e-11,difference)
        reverse=state.copy()
        reverse[system.count:2*system.count]*=-1
        forward_flow=system.rhs(0,state)
        reverse_flow=system.rhs(0,reverse)
        evidence.check('reversible_source_flow',
                       np.max(abs(forward_flow[:system.count]+reverse_flow[:system.count]))<1e-14 and
                       np.max(abs(forward_flow[system.count:]-reverse_flow[system.count:]))<1e-14)
        formal=DustGravityCollar(24,0.)
        coordinate=formal.offsets+.5
        primitive=3*coordinate**2-2*coordinate**3
        initial_root=np.sqrt(1-2*formal.central_mass/formal.initial_radius)
        exact_root=initial_root-formal.coupling*formal.source_mass/formal.initial_radius*primitive
        exact_mass=formal.initial_radius*(1-exact_root**2)/2
        evidence.check('formal_zero_width_initial_mass_profile',
                       np.max(abs(exact_mass-formal.initial_geometry['mass']))<2e-13)
        evidence.check('formal_zero_width_initial_lapse_is_constant',
                       np.max(abs(formal.initial_geometry['N']-exact_root[-1]))<2e-13)
        charge=sp.symbols('m0',positive=True)
        predicted_jump=charge*root-charge**2/(2*radius)
        integrated_jump=radius*(1-(root-charge/radius)**2)/2-mass
        evidence.check('thin_initial_mass_jump_is_Israel_rest_jump',
                       sp.simplify(integrated_jump-predicted_jump)==0)
        outer_root=initial_root-formal.coupling*formal.source_mass/formal.initial_radius
        def coefficient(label):
            mapped=label+.5
            local_root=initial_root-formal.coupling*formal.source_mass/formal.initial_radius*(3*mapped**2-2*mapped**3)
            return outer_root**2*formal.coupling*formal.source_mass*6*mapped*(1-mapped)*local_root/formal.initial_radius**2
        peak=minimize_scalar(lambda label:-coefficient(label),bounds=(-.5,.5),method='bounded',
                             options={'xatol':1e-14})
        maximum=coefficient(peak.x)
        constant=np.sqrt(2/maximum)
        evidence.check('positive_uniform_limit_focusing_coefficient',peak.success and maximum>0)
        status_path=evidence.root/'source-intake/navier-stokes/20260914/annular-source-gravity-focusing-attempt01/status.json'
        previous=json.loads(status_path.read_text())
        evidence.own(status_path)
        narrow=[row for row in previous['cases'] if row['degree']==16 and row['steps']==100 and row['width']<=1e-6]
        errors=[abs(row['time_over_sqrt_width']/constant-1) for row in narrow]
        evidence.check('observed_event_constant_matches_exact_limit',
                       previous['state']=='complete' and len(errors)==3 and errors[-1]<1e-4 and
                       all(later<earlier for earlier,later in zip(errors,errors[1:])),errors)
        control=DustGravityCollar(16,1e-7,coupling=0,central_mass=.8)
        solution=solve_ivp(control.rhs,(0,1.6),control.initial_state,method='DOP853',rtol=2e-11,
                           atol=2e-14,max_step=.01)
        raw=evidence.output/'central-GR-test-dust-control.npz'
        np.savez_compressed(raw,times=solution.t,states=solution.y)
        evidence.own(raw,'outputs')
        minimum=min(control.minimum_jacobian(state) for state in solution.y.T)
        evidence.check('central_gravity_without_self_loading_does_not_cause_early_crossing',
                       solution.success and minimum>.99e-7,float(minimum))
        evidence.report.update(derived_limit_constant=float(constant),coefficient_maximum=float(maximum),
                               coefficient_peak_label=float(peak.x),narrow_constant_relative_errors=errors,
                               measured_exponent=previous['measured_thin_width_exponent'],
                               zero_width_state_used_as_formal_material_ODE_extension_only=True,
                               zero_width_state_is_physical_solution=False,
                               ordered_dust_fixed_time_thin_limit_obstructed=True,
                               weak_thin_shell_limit_ruled_out=False,
                               full_scalar_gravity_coupling_evolved=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

