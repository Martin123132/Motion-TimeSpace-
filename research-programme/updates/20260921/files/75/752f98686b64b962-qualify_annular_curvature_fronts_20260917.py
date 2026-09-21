from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import profile
from fractions import Fraction
import argparse
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            interval_arithmetic=False,manufactured_fronts_not_actual_GR_solution=True,
            finite_front_regularities_of_actual_solution_proven=False,
            continuum_initial_profile_not_spectral_endpoint_test=True)
        radius=Fraction(603,100)
        gradient=Fraction(1,100)
        speed=Fraction(3,50)
        source_force=radius**2*(1-speed**2)*(gradient**2-gradient**2)/2
        defect=2*gradient/radius
        points=float(radius)+np.array([-1e-4,0.,1e-4])
        scalar,observed_gradient=profile(points)
        evidence.check('original_profile_locally_linear',max(abs(scalar-.01*(points-float(radius))))<2e-15
            and max(abs(observed_gradient-.01))<2e-15)
        evidence.check('initial_equal_traces_zero_acceleration',source_force==0)
        evidence.check('second_corner_compatibility_is_nonzero',defect==Fraction(2,603),str(defect))
        evidence.report['initial_corner']=dict(radius=float(radius),gradient=float(gradient),speed=float(speed),
            physical_mixed_derivative=0.,physical_second_radial_derivative=0.,source_acceleration=0.,
            second_material_Dirichlet_derivative=float(defect),exact_defect=str(defect),
            C2_up_to_initial_source_corner_justified=False)
        for count in [33,65,129,257,513,1025,2049]:
            system=LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=8)
            offsets=system.radii-system.anchor
            bulk=system.base_radii-system.anchor
            spacing=system.gram_spacing
            edge=np.searchsorted(system.edges,system.anchor)
            left,right=system.anchor-system.edges[edge-1],system.edges[edge+1]-system.anchor
            entries=[]
            for instant in [0.,.01,.11,.21,.39]:
                fronts=np.array([-.8*instant,.7*instant])
                amplitudes=np.array([.4,-.3])
                slopes=np.where(offsets<0.,.7,1.1)
                curvature=np.where(offsets<0.,-.2,.3)
                values=slopes*offsets+curvature*offsets**2/2
                for position,amplitude in zip(fronts,amplitudes):
                    anchor_hinge=max(-position,0.)
                    values+=amplitude*(np.maximum(offsets-position,0.)**2-anchor_hinge**2-2*anchor_hinge*offsets)/2
                breaks=np.append(fronts,0.)
                affected=np.array([any(lower<=front<=upper for front in breaks) for lower,upper in zip(bulk[:-3],bulk[3:])])
                maximum_curvature=1.
                raw_bound=2*maximum_curvature*spacing**2*affected
                trace_bound=maximum_curvature*(left+right)/3
                bound=float(np.linalg.norm(raw_bound)/np.sqrt(8)+np.linalg.norm(system.lifted_hinge)*trace_bound)
                actual=float(np.linalg.norm(system.lifted @ values))
                entries.append(dict(time=instant,fronts=fronts.tolist(),affected_bulk_stencils=int(sum(affected)),
                    factor_norm=actual,factor_bound=bound,scaled_factor=actual/spacing**2))
            evidence.check(str(count)+'_bounded_curvature_front_consistency',all(row['factor_norm']<=row['factor_bound']+3e-13 for row in entries))
            evidence.report['cases'].append(dict(count=count,front_cases=entries,uniform_curvature_bound=1.))
            evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
