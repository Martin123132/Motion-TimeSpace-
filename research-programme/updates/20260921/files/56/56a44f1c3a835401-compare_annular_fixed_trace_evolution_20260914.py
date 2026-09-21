from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_fixed_grid_moving_trace_20260914 import FixedGridMovingTrace
import numpy as np
import json


def main():
    evidence=EvidenceRun('annular-fixed-trace-evolution-comparison-attempt01',__file__)
    try:
        root=evidence.root
        folders={key:root/'source-intake/navier-stokes/20260914'/name for key,name in [
            ('stencil_preparation','annular-fixed-grid-moving-trace-evolution-attempt01'),
            ('smooth_preparation','annular-fixed-grid-moving-trace-smooth-evolution-attempt01')]}
        statuses={}
        for key,folder in folders.items():
            path=folder/'status.json'
            status=json.loads(path.read_text())
            evidence.check(key+'_complete_preserved_series',status['state']=='complete' and
                           len(status['cases'])==8 and all(row['passed'] for row in status['checks']))
            evidence.own(path)
            statuses[key]=status
        probes=np.linspace(3.,7.,4097)
        trajectories={}
        for row in statuses['smooth_preparation']['cases']:
            if row['tag']:
                continue
            count,branch,degree=row['count'],row['branch'],row['degree']
            label=branch+'-'+str(count)+'-degree-'+str(degree)
            path=folders['smooth_preparation']/(label+'.npz')
            evidence.own(path)
            data=np.load(path)
            values=data['states'].reshape(degree+1,2*count+3,len(data['times']))
            central=values[degree//2]
            weights=np.full(count,4/(count-1))
            weights[[0,-1]]/=2
            scalar=np.array([np.interp(probes,data['radii'],central[:count,index]) for index in range(len(data['times']))])
            momentum=np.array([np.interp(probes,data['radii'],central[count:2*count,index]/weights) for index in range(len(data['times']))])
            trajectories[count,branch]=dict(q=scalar,p=momentum,b=central[2*count],clock=central[-1],times=data['times'])
        def norm(profile):
            return np.sqrt(np.trapezoid(profile**2,probes,axis=-1))
        def compare(coarse,fine):
            return dict(max_relative_scalar_L2=float(np.max(norm(coarse['q']-fine['q'])/np.maximum(norm(fine['q']),1e-20))),
                        final_relative_scalar_L2=float(norm(coarse['q'][-1]-fine['q'][-1])/norm(fine['q'][-1])),
                        max_absolute_momentum_density_L2=float(np.max(norm(coarse['p']-fine['p']))),
                        max_source_position_difference=float(np.max(abs(coarse['b']-fine['b']))),
                        max_source_clock_difference=float(np.max(abs(coarse['clock']-fine['clock']))))
        refinements=[]
        for branch in ['reference','MTS']:
            for coarse,fine in [(33,65),(65,129)]:
                row=dict(branch=branch,coarse=coarse,fine=fine,**compare(trajectories[coarse,branch],trajectories[fine,branch]))
                refinements.append(row)
                evidence.check(branch+str(fine)+'_finite_refinement_diagnostics',all(np.isfinite(value) for key,value in row.items()
                               if key not in ['branch','coarse','fine']),row)
        between=[]
        for count in [33,65,129]:
            between.append(dict(count=count,**compare(trajectories[count,'MTS'],trajectories[count,'reference'])))
        evidence.report.update(refinements=refinements,between_branches=between,
                               scalar_refinement_decreases={branch:refinements[index+1]['max_relative_scalar_L2']<
                               refinements[index]['max_relative_scalar_L2'] for branch,index in [('reference',0),('MTS',2)]},
                               same_resolution_is_not_independent_continuum_truth=True,
                               standalone_continuum_waveform_accuracy_qualified=False,
                               full_GR_limit_proven=False)
        source=folders['smooth_preparation']
        for branch in ['reference','MTS']:
            data=np.load(source/(branch+'-129-degree-4.npz'))
            system=FixedGridMovingTrace(129,branch=='MTS',degree=4,radial_degree=18)
            final=system.preparation(data['states'][:,-1])
            final_state=data['states'][:,-1]
            offgrid=final['geometry'].layer(np.linspace(-.5,.5,49))
            rate=offgrid['N'][:,:129]*offgrid['U'][:,:129]*offgrid['pi']/(system.node_weights*offgrid['R'][:,:129]**2)
            phi=np.sum(offgrid['trace_weights']*offgrid['q'],axis=1)
            phi_rate=np.sum(offgrid['trace_weights']*rate,axis=1)+offgrid['V']*np.sum(offgrid['trace_gradient']*offgrid['q'],axis=1)
            offgrid_error=float(max(np.max(abs(phi)),np.max(abs(phi_rate))))
            evidence.check(branch+'_offgrid_source_trace',offgrid_error<2e-9,offgrid_error)
            finer=FixedGridMovingTrace(129,branch=='MTS',degree=8,radial_degree=24)
            coefficients=system.grid.inverse @ system.values(final_state)
            finer_state=np.polynomial.chebyshev.chebval(2*finer.offsets,coefficients).T.ravel()
            finer_rhs=finer.values(finer.rhs(.2,finer_state))
            projected=np.polynomial.chebyshev.chebval(2*system.offsets,finer.grid.inverse @ finer_rhs).T
            degree_error=float(np.max(abs(projected-system.values(system.rhs(.2,final_state)))))
            evidence.check(branch+'_finer_layer_and_radial_RHS',degree_error<2e-7,degree_error)
            derivative=final['geometry'].b_derivative
            roots=np.polynomial.chebyshev.chebroots(np.polynomial.chebyshev.chebder(derivative))
            critical=roots.real[(abs(roots.imag)<1e-10)&(roots.real>-1)&(roots.real<1)]
            exact_polynomial_min=float(np.min(np.polynomial.chebyshev.chebval(np.concatenate([[-1.,1.],critical]),derivative)))
            evidence.check(branch+'_final_source_polynomial_ordered',exact_polynomial_min>0,exact_polynomial_min)
            evidence.report['cases'].append(dict(branch=branch,final_radius=float(final['data']['b'][2]),
                    final_coordinate_speed=float(final['data']['V'][2]),
                    final_proper_radial_speed=float(final['data']['U'][2,-1]**2*final['data']['p_s'][2]/system.source_mass),
                    final_proper_clock=float(final['data']['theta'][2]),
                    final_minimum_source_jacobian=final['geometry'].minimum_source_jacobian,
                    offgrid_trace_error=offgrid_error,finer_layer_RHS_error=degree_error,
                    final_polynomial_minimum_jacobian=exact_polynomial_min))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
