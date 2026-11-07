from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
import ctypes
import numpy as np
import sympy as sp


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-pinned-source-P2-layer-law-attempt01',__file__)
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-pinned-source-P2-acceleration-layer.md')
        local = sp.symbols('local',real=True)
        basis = sp.Matrix([(1-local)*(1-2*local),4*local*(1-local),local*(2*local-1)])
        mass = sp.integrate(basis*basis.T,(local,0,1))
        stiffness = sp.integrate(basis.diff(local)*basis.diff(local).T,(local,0,1))
        evidence.check('consistent_P2_mass_exact',mass==sp.Matrix([[4,2,-1],[2,16,2],[-1,2,4]])/30)
        evidence.check('constant_load_exact',sp.integrate(basis,(local,0,1))==sp.Matrix([1,4,1])/6)
        previous,current,following = sp.symbols('previous current following')
        midpoint_left,midpoint_right = -(previous+current)/8,-(current+following)/8
        vertex = 8*current-previous-following+2*midpoint_left+2*midpoint_right
        evidence.check('assembled_vertex_recurrence',sp.expand(vertex+sp.Rational(5,4)*(following-6*current+previous))==0)
        ratio = 3-2*sp.sqrt(2)
        evidence.check('bounded_characteristic_root',sp.simplify(ratio**2-6*ratio+1)==0 and bool(ratio>0) and bool(ratio<1))
        vector = sp.Matrix([-1,(1+ratio)/8,-ratio])
        evidence.check('midpoint_equation_exact',sp.simplify(2*vector[0]+16*vector[1]+2*vector[2])==0)
        mass_coefficient = sp.simplify((vector.T*mass*vector)[0]/(1-ratio**2))
        gradient_coefficient = sp.simplify((vector.T*stiffness*vector)[0]/(1-ratio**2))
        evidence.check('positive_L2_and_gradient_series_constants',bool(mass_coefficient>0) and bool(gradient_coefficient>0))
        evidence.report.update(rho=str(ratio),rho_numeric=float(ratio),
            nearest_midpoint_error_ratio=str(sp.simplify((1+ratio)/8)),
            L2_squared_coefficient=str(mass_coefficient),gradient_L2_squared_coefficient=str(gradient_coefficient),
            scope='Exact frozen-coefficient half-line mass projection; actual full-parent profiles are diagnostic comparisons, not replaced.')
        predicted = np.array([float((1+ratio)*ratio**cell/8) if member==0 else -float(ratio**(cell+1))
            for cell in range(4) for member in range(2)])
        for level in ['fine','third']:
            report = verify_report(evidence,'source-intake/navier-stokes/20260914/annular-Neumann-source-corner-profile-'+level+'-attempt01/status.json')
            evidence.check(level+':source_profile_complete',report['state']=='complete')
            for side_index,side in enumerate(['left','right']):
                rows = report['nearest_source_nodes'][side]
                distances = np.abs([row['distance'] for row in rows])
                scaled = np.array([row['error'] for row in rows])/report['source_trace_limits'][side_index]
                mismatch = scaled-predicted
                evidence.check(level+':'+side+':first_cells_uniform',np.max(np.abs(distances/distances[0]-np.arange(1,9)))<1e-7)
                evidence.check(level+':'+side+':parameter_free_first_four_pattern',np.max(np.abs(mismatch[:4]))<1e-4,
                    float(np.max(np.abs(mismatch[:4]))))
                evidence.report['cases'].append(dict(level=level,side=side,
                    trace_amplitude_from_coupled_equations=report['source_trace_limits'][side_index],
                    observed_error_ratios=scaled.tolist(),predicted_error_ratios=predicted.tolist(),
                    maximum_first_four_ratio_error=float(np.max(np.abs(mismatch[:4]))),
                    maximum_first_eight_ratio_error=float(np.max(np.abs(mismatch)))))
                evidence.save()
        evidence.report.update(source_acceleration_fitted=False,profile_replaced=False,weak_limit_not_excluded=True,
            smooth_source_jet_not_established=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

