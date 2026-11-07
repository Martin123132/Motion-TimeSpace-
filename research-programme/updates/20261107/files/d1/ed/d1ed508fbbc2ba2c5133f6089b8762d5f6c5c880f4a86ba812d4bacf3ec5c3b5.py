from derive_annular_source_gravity_20260914 import EvidenceRun
import ctypes
import sympy as sp


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-moving-native-transmission-algebra-attempt01', __file__)
    try:
        evidence.own(evidence.root / 'DERIVATION-20261002-moving-native-transmission-and-third-jets.md')
        alpha, beta, speed, trace_rate, slope = sp.symbols('alpha beta V trace_rate g', real=True)
        temporal = trace_rate - speed * slope
        momentum = beta * slope + speed * alpha * temporal
        density = (alpha * temporal**2 - beta * slope**2) / 2
        coefficient = beta - alpha * speed**2
        evidence.check('moving_trace_coefficient', sp.expand(momentum - coefficient * slope - alpha * speed * trace_rate) == 0)
        evidence.check('moving_position_coefficient', sp.expand(momentum * slope + density - coefficient * slope**2 / 2 - alpha * trace_rate**2 / 2) == 0)
        field_load, position_load = sp.symbols('A C', nonzero=True)
        left = -position_load / field_load - field_load / (2 * coefficient)
        right = -position_load / field_load + field_load / (2 * coefficient)
        evidence.check('moving_field_jump', sp.simplify(coefficient * (right - left) - field_load) == 0)
        evidence.check('moving_pressure_balance', sp.simplify(coefficient * (right**2 - left**2) / 2 + position_load) == 0)
        time = sp.symbols('t', real=True)
        beta_second, support_acceleration = sp.symbols('beta_second support_acceleration', real=True)
        dynamic = beta + time**2 * beta_second / 2 - alpha * (time * support_acceleration)**2
        evidence.check('effective_jump_coefficient_second_derivative', sp.diff(dynamic, time, 2).subs(time, 0) == beta_second - 2 * alpha * support_acceleration**2)
        mean, mean_second, load_second, position_second = sp.symbols('mean mean_second load_second position_second')
        shape = (field_load + time**2 * load_second / 2) * (mean + time**2 * mean_second / 2) + position_load + time**2 * position_second / 2
        evidence.check('shape_second_jet', sp.diff(shape, time, 2).subs(time, 0) == field_load * mean_second + load_second * mean + position_second)
        coordinate = sp.symbols('x')
        width = sp.symbols('h', positive=True)
        left_third, right_third = sp.symbols('ell_left ell_right')
        lift = width**3 * coordinate**3 * (1 - coordinate)**3 * (left_third * (1 - coordinate) - right_third * coordinate) / 6
        for endpoint in [0, 1]:
            for order in range(3):
                evidence.check('lift_endpoint_' + str(endpoint) + '_order_' + str(order), sp.diff(lift, coordinate, order).subs(coordinate, endpoint) == 0)
        evidence.check('independent_left_third_jet', sp.simplify(sp.diff(lift, coordinate, 3).subs(coordinate, 0) / width**3 - left_third) == 0)
        evidence.check('independent_right_third_jet', sp.simplify(sp.diff(lift, coordinate, 3).subs(coordinate, 1) / width**3 - right_third) == 0)
        evidence.report.update(moving_law_derived=True, third_jet_lift_derived=True, higher_order_state_constructed=False,
            live_preservation_repair_solved=False, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
