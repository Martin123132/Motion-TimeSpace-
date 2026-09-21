from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import radial_weights
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
import numpy as np
import sympy as sp


def symbolic_energy_checks(evidence):
    radius, lapse, metric, coupling, source_mass = sp.symbols('r N F kappa m_s', positive=True)
    temporal, gradient, gram, density, velocity = sp.symbols('A B g sigma V', real=True)
    clock = sp.sqrt(lapse**2-velocity**2/metric)
    source_action = -source_mass*density*clock
    source_legendre = sp.diff(source_action, velocity)*velocity-source_action
    source_expected = source_mass*density*lapse**2/clock
    evidence.check('symbolic_source_clock_Legendre_identity', sp.simplify(source_legendre-source_expected) == 0)
    kinetic = radius**2*temporal/(2*lapse*sp.sqrt(metric))
    potential = radius**2*lapse*sp.sqrt(metric)*(gradient/2+gram)
    matter_hamiltonian = kinetic+potential+source_expected
    mass_rhs = coupling*radius**2*metric*(temporal/(2*lapse**2*metric)+gradient/2+gram)
    mass_rhs += coupling*source_mass*density*sp.sqrt(metric)*lapse/clock
    gravity = lapse*mass_rhs/(coupling*sp.sqrt(metric))
    evidence.check('symbolic_full_Gram_wave_dust_cancels_gravitational_bulk', sp.simplify(matter_hamiltonian-gravity) == 0)
    evidence.check('symbolic_reference_same_boundary_identity', sp.simplify((matter_hamiltonian-gravity).subs(gram, 0)) == 0)
    speed, root = sp.symbols('beta U', positive=True)
    source_mass_loading = source_mass*density*sp.sqrt(metric)*lapse/clock
    expected = source_mass*density*root/sp.sqrt(1-speed**2)
    evidence.check('symbolic_source_energy_redshift_times_Lorentz_factor',
        sp.simplify(source_mass_loading.subs({metric:root**2, velocity:lapse*root*speed})-expected) == 0)
    expansion, potential_size, speed_square = sp.symbols('epsilon potential_size speed_square', real=True)
    series = sp.series(sp.sqrt(1-2*expansion*potential_size)/sp.sqrt(1-expansion*speed_square), expansion, 0, 2).removeO()
    evidence.check('symbolic_conditional_Newtonian_dust_energy', sp.expand(series-(1+expansion*(speed_square/2-potential_size))) == 0)
    rate, momentum, momentum_rate, force, acceleration, explicit_time = sp.symbols('v p p_dot L_q a L_t')
    total_derivative = momentum_rate*rate+momentum*acceleration-(force*rate+momentum*acceleration+explicit_time)
    evidence.check('symbolic_autonomous_Noether_balance', sp.expand(total_derivative-(rate*(momentum_rate-force)-explicit_time)) == 0)


def decimals(values):
    return np.array([[Decimal(value) for value in row] for row in values])


def energy_channels(current, target_momenta, rates, preconditioner):
    solver = current['solver']
    solution = current['solution']
    radius = solver.nodes.ravel()
    mass, log_lapse = solution['state'].reshape(2, -1)
    lapse, metric = np.exp(log_lapse), 1-2*mass/radius
    root = np.sqrt(metric)
    fields = solver.fields
    velocity = fields['velocity']
    clock = np.sqrt(lapse**2-velocity**2/metric)
    gram = next(iter(fields['gram'].values()))
    kinetic = radius**2*fields['temporal_square']/(2*lapse*root)
    potential = radius**2*lapse*root*(fields['gradient_square']/2+gram)
    source = solver.owner.source_mass*fields['source_density']*lapse**2/clock
    matter_hamiltonian = kinetic+potential+source
    extension = next(iter(fields['gram']))
    mass_rhs = solver.rhs(solution['state'], extension)[0]
    gravity = lapse*mass_rhs/(solver.owner.coupling*root)
    weights = radial_weights(solver)
    with localcontext() as context:
        context.prec = 64
        measured = decimal_array(current['momentum'])
        decimal_rates, measure = decimal_array(rates), decimal_array(weights)
        target_pairing = np.sum(target_momenta*decimal_rates)
        computed_pairing = np.sum(measured*decimal_rates)
        matter_action = Decimal.from_float(current['matter_action'])
        gravity_bulk = np.sum(measure*decimal_array(gravity))
        boundary_integral = np.sum(measure*decimal_array(mass_rhs))/Decimal.from_float(solver.owner.coupling)
        boundary_endpoint = (Decimal.from_float(float(mass[-1]))-Decimal.from_float(solver.owner.central_mass))/Decimal.from_float(solver.owner.coupling)
        radial_matter_hamiltonian = np.sum(measure*decimal_array(matter_hamiltonian))
        legendre_defect = computed_pairing-matter_action-gravity_bulk
        inverse_energy_error = target_pairing-computed_pairing
        total = target_pairing-matter_action-gravity_bulk+boundary_integral
        endpoint_total = total+boundary_endpoint-boundary_integral
        residual = np.asarray(target_momenta-measured, float)
        terms = abs(target_pairing)+abs(matter_action)+abs(gravity_bulk)+abs(boundary_integral)
        inverse_bound = float(np.linalg.norm(residual.ravel()/preconditioner.original_scale)*
            np.linalg.norm(preconditioner.original_scale*rates.ravel()))
        floor = max(32*np.finfo(float).eps*float(terms), abs(float(legendre_defect)),
            abs(float(boundary_endpoint-boundary_integral)), inverse_bound)
        values = dict(target_pairing=target_pairing, computed_pairing=computed_pairing,
            matter_action=matter_action, gravity_bulk=gravity_bulk, boundary_integral=boundary_integral,
            boundary_endpoint=boundary_endpoint, radial_matter_hamiltonian=radial_matter_hamiltonian,
            mixed_quadrature_Legendre_defect=legendre_defect,
            pointwise_identity_integral_defect=radial_matter_hamiltonian-gravity_bulk,
            inverse_energy_error=inverse_energy_error, full_shifted_hamiltonian=total,
            endpoint_boundary_shifted_hamiltonian=endpoint_total,
            without_boundary=total-boundary_integral, without_gravity_bulk=total+gravity_bulk,
            central_energy_offset=Decimal.from_float(solver.owner.central_mass)/Decimal.from_float(solver.owner.coupling))
    numeric = dict(pointwise_radial_Legendre_relative_defect=float(np.max(abs(matter_hamiltonian-gravity)) /
        max(np.max(abs(matter_hamiltonian)), 1e-30)), inverse_energy_Cauchy_bound=inverse_bound,
        diagnostic_resolution_scale=floor, resolution_scale_is_not_certified_error_bound=True,
        float_epsilon=float(np.finfo(float).eps), longdouble_epsilon=float(np.finfo(np.longdouble).eps))
    raw = dict(radius=radius, weights=weights, mass=mass, log_lapse=log_lapse, mass_rhs=mass_rhs,
        temporal_square=fields['temporal_square'], gradient_square=fields['gradient_square'], gram=gram,
        source_density=fields['source_density'], source_velocity=velocity, target_momenta=np.array(target_momenta, dtype=str),
        computed_momenta=current['momentum'], endpoint_rates=rates, matter_action=current['matter_action'],
        coupling=solver.owner.coupling, source_mass=solver.owner.source_mass, central_mass=solver.owner.central_mass)
    return {name:str(value) for name, value in values.items()}, numeric, raw
