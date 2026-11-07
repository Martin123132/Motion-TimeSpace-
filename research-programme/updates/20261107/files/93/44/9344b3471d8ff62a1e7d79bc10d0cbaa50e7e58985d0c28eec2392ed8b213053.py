from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_material_integral_v2_20260930 import material_density_rows, base_kinematics, decimal_density
from annular_C0_boundary_integral_20260930 import density_rows
from annular_position_support_column_20260930 import analytic_volume_column
from validate_annular_position_support_manufactured_20260930 import family
from validate_annular_C0_boundaries_20260930 import toy_data, metric
from decimal import Decimal, localcontext
import ctypes
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot set one core')
    evidence = EvidenceRun('annular-C0-material-manufactured-attempt02', __file__)
    try:
        with localcontext() as context:
            context.prec = 70
            local = np.array([.07, .29, .63, .91])
            radius = 5.5+1.2*local
            for branch in [0, 1]:
                old, direction = family(local, branch)
                data = toy_data(radius, single=True)
                amount = 1e-25j
                rows = material_density_rows(data, radius+amount*direction['movement'],
                    direction['values']+amount*direction['material_values'],
                    direction['radial']+amount*direction['material_radial'],
                    direction['time']+amount*direction['material_time'], amount)*(1+amount*direction['movement_r'])
                error = float(np.max(abs(rows.imag/amount.imag-analytic_volume_column(old, direction))))
                evidence.check('independent_material_product_rule:'+str(branch), error < 2e-11, error)
                kinematics = base_kinematics(data, radius)
                convert = lambda values:np.array([Decimal.from_float(float(value)) for value in values.ravel()], dtype=object).reshape(values.shape)
                values, radial, time = [convert(value) for value in metric(radius, branch)]
                exact_radius = convert(radius)
                base = decimal_density(kinematics, exact_radius, values, radial, time)
                replay = density_rows(data, radius, *metric(radius, branch))
                evidence.check('decimal_density_replay:'+str(branch), np.max(abs(np.asarray(base, float)-replay)) < 2e-12)
                right = values.copy()
                right[0] += Decimal('1e-25')
                jump = np.asarray(decimal_density(kinematics, exact_radius, right, radial, time)-base, float)
                floating_values, floating_radial, floating_time = metric(radius, branch)
                floating_values = floating_values.astype(complex)
                floating_values[0] += 1e-20j
                expected = density_rows(data, radius, floating_values, floating_radial, floating_time).imag/1e-20*1e-25
                error = float(np.max(abs(jump-expected)))
                evidence.check('tiny_trace_jump_preserved:'+str(branch), np.max(abs(jump)) > 1e-28 and error < 2e-38, error)
                rounded = values.astype(float)
                evidence.check('rounded_trace_negative_control:'+str(branch), np.array_equal(right.astype(float), rounded))
        evidence.report.update(actual_C0_integrated=False, full_physics_claim=False, github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()


