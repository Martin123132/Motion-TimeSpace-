from __future__ import annotations

from datetime import datetime, timezone
import json

import psutil
import sympy as sy

from wave_network import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sy.factor(sy.expand(expression))
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'passed': True, 'residual': str(residual)})

    time, coordinate = sy.symbols('tau zeta', real=True)
    field = sy.Function('psi')(time, coordinate)
    potential = sy.Function('V')(coordinate)
    source = sy.Function('S')(time, coordinate)
    energy_density = (sy.diff(field, time)**2+sy.diff(field, coordinate)**2+potential*field**2)/2
    flux = -sy.diff(field, time)*sy.diff(field, coordinate)
    local = sy.diff(energy_density, time)+sy.diff(flux, coordinate)-source*sy.diff(field, time)
    check('sourced_wave_local_work_identity', local.subs(sy.diff(field, time, 2),
          sy.diff(field, coordinate, 2)-potential*field+source))
    interface_velocity, inner_traction, outer_traction = sy.symbols('qdot p_in p_out', real=True)
    outward, horizon, source_work = sy.symbols('Pout PH Wdot', real=True)
    inner_rate = interface_velocity*inner_traction-horizon
    outer_rate = source_work-interface_velocity*outer_traction-outward
    check('variational_interface_cancels_internal_work', (inner_rate+outer_rate-source_work+outward+horizon).subs(outer_traction, inner_traction))
    body_storage, reference_storage, body_work, reference_work = sy.symbols('EB EH WB WH')
    body_out, reference_out, absorbed = sy.symbols('OB OH H')
    check('finite_history_difference_budget', ((body_work-reference_work)-(body_storage-reference_storage)-
          (body_out-reference_out)+absorbed).subs({body_work: body_storage+body_out,
                                                 reference_work: reference_storage+reference_out+absorbed}))
    frequency, damping, mass, stiffness, force = sy.symbols('k C M K g', real=True)
    transfer = 1/(stiffness-frequency**2*mass-sy.I*frequency*damping)
    check('discrete_retarded_passivity', sy.im(transfer)-frequency*damping*sy.conjugate(transfer)*transfer)
    check('one_quadrature_harmonic_work', frequency*force**2*sy.im(transfer)/2
          -frequency**2*damping*force**2*sy.conjugate(transfer)*transfer/2)
    response_imag, normalizer, radius = sy.symbols('ImDG kappa R', real=True)
    generating_imag_pair = normalizer*force**2*response_imag/(2*radius)
    check('pair_response_optical_factor', 2*(frequency/radius)*generating_imag_pair
          -normalizer*frequency*force**2*response_imag/radius**2)
    generating_imag_real = generating_imag_pair/2
    check('one_real_quadrature_optical_factor', 2*(frequency/radius)*generating_imag_real
          -normalizer*frequency*force**2*response_imag/(2*radius**2))
    old_position, new_position, old_velocity, new_velocity, step = sy.symbols('u0 u1 v0 v1 dt', real=True)
    midpoint_velocity = (new_velocity+old_velocity)/2
    midpoint_position = (new_position+old_position)/2
    discrete_energy_change = (mass*(new_velocity**2-old_velocity**2)+stiffness*(new_position**2-old_position**2))/2
    kinematic = {new_position: old_position+step*midpoint_velocity}
    residual = (mass*(new_velocity-old_velocity)+step*stiffness*midpoint_position+step*damping*midpoint_velocity-step*force)
    check('midpoint_exact_discrete_work_law', (discrete_energy_change-step*midpoint_velocity*force+
          step*damping*midpoint_velocity**2-midpoint_velocity*residual).subs(kinematic))
    left = (mass+step*damping/2+step**2*stiffness/4)*new_velocity
    right = (mass-step*damping/2-step**2*stiffness/4)*old_velocity-step*stiffness*old_position+step*force
    check('midpoint_update_formula', left-right-residual.subs(kinematic))
    outgoing_slope, inside_slope = sy.symbols('yout yin', complex=True)
    inside_value, outside_value = sy.symbols('U V', nonzero=True)
    wronskian = inside_value*outside_value*(outgoing_slope-inside_slope)
    check('delta_source_Green_diagonal', -inside_value*outside_value/wronskian-1/(inside_slope-outgoing_slope))
    amplitude = sy.symbols('g_real', real=True)
    source_jump, value_jump = -amplitude, sy.S.Zero
    difference_field = sy.symbols('DeltaPsi')
    overlap = source_jump*difference_field-value_jump
    check('stage27_pair_source_action_for_delta_source', -normalizer*overlap/2-normalizer*amplitude*difference_field/2)
    compactness, radial, tortoise = sy.symbols('c x zeta', positive=True)
    radial_map = radial-1+compactness*sy.log((radial-compactness)/(1-compactness))
    check('Schwarzschild_tortoise_derivative', sy.diff(radial_map, radial)-1/(1-compactness/radial))
    auxiliary = sy.symbols('w', positive=True)
    check('Wright_omega_inverse_map', sy.simplify(radial_map.subs(radial, compactness*(1+auxiliary))
          -(compactness*(auxiliary+sy.log(auxiliary))+compactness-1+compactness*sy.log(compactness/(1-compactness)))))
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'exact_checks': len(checks), 'checks': checks,
              'continuum_identity': 'W=E_inner+E_outer+escaped_outer+absorbed_horizon, initially unexcited',
              'difference_identity': 'DeltaW=DeltaE+Deltaescaped_outer-absorbed_BH_horizon',
              'source_scope': 'Driven smooth-in-time delta master source at fixed exterior radius, not an orbital stress-tensor derivation.',
              'discrete_balance_scope': 'Midpoint balance is structural; independent continuum response and refinements test the equations beyond bookkeeping.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
