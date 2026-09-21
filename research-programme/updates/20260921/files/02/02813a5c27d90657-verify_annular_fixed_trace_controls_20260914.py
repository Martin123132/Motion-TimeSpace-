from derive_annular_source_gravity_20260914 import EvidenceRun, DustGravityCollar
from annular_fixed_grid_moving_trace_20260914 import FixedGridMovingTrace
from qualify_annular_fixed_grid_moving_trace_20260914 import tangent_preparation
import numpy as np
from scipy.integrate import solve_ivp
import json


def radial_control(geometry):
    system=geometry.system
    previous=np.array([system.central_mass,0.])
    saved=[]
    for piece in geometry.pieces:
        lower,upper=float(piece['lower']),float(piece['upper'])
        if piece['gap']:
            mass=previous[0]
            previous=np.array([mass,previous[1]+.5*np.log((1-2*mass/upper)/(1-2*mass/lower))])
            continue
        def rhs(radius,state):
            locations=np.array([radius])
            packets=[geometry.packet(locations,node) for node in piece['active']]
            loading,unused,lapse=geometry.loadings(locations,np.array([state[0]]),packets)
            return [loading[0],state[0]/(radius**2*(1-2*state[0]/radius))+lapse[0]]
        result=solve_ivp(rhs,(lower,upper),previous,method='DOP853',rtol=2e-12,atol=2e-14,
                         max_step=(upper-lower)/12,dense_output=True)
        if not result.success:
            raise RuntimeError(result.message)
        probes=np.linspace(lower,upper,7)[1:-1]
        saved.append((probes,result.sol(probes)))
        previous=result.y[:,-1]
    normalization=np.log(np.sqrt(1-2*previous[0]/geometry.edges[-1]))-previous[1]
    errors=[]
    for radii,expected in saved:
        actual=geometry.metric(radii)
        errors.append([np.max(abs(actual['mu']-expected[0])),
                       np.max(abs(np.log(actual['N'])-expected[1]-normalization))])
    return np.max(errors,axis=0)


def main():
    evidence=EvidenceRun('annular-fixed-trace-independent-controls-attempt01',__file__)
    try:
        for gram in [False,True]:
            for width in [.001,.16]:
                system=FixedGridMovingTrace(33,gram,degree=4,radial_degree=18,width=width)
                state=tangent_preparation(system)
                evaluated=system.evaluate(0,state)
                geometry=evaluated['geometry']
                errors=radial_control(geometry)
                row=dict(branch='MTS' if gram else 'reference',width=width,
                         maximum_overlap=geometry.maximum_overlap,
                         independent_radial_mass_error=float(errors[0]),
                         independent_radial_log_lapse_error=float(errors[1]))
                evidence.report['cases'].append(row)
                evidence.check(row['branch']+str(width)+'_independent_radial_ODE',max(errors)<2e-9,row)
                if width>.1:
                    evidence.check(row['branch']+'_overlapping_bands_actually_exercised',geometry.maximum_overlap>=2)
                probes=geometry.material(np.array([-.25,.15]))['R'].ravel()
                target=geometry.mass_current(probes,evaluated['multipliers'])['total']
                differences=[]
                for step in [.002,.001]:
                    mass={factor:system.geometry(state+factor*step*evaluated['rhs']).metric(probes)['mu']
                          for factor in [-2,-1,1,2]}
                    derivative=(mass[-2]-8*mass[-1]+8*mass[1]-mass[2])/(12*step)
                    differences.append(float(np.max(abs(derivative-target))))
                evidence.check(row['branch']+str(width)+'_real_five_point_time_derivative',min(differences)<2e-7,differences)
                if width>.1:
                    varied=system.geometry(state.astype(complex)+1e-22j*evaluated['rhs'])
                    error=float(np.max(abs(varied.metric(probes)['mu'].imag/1e-22-target)))
                    evidence.check(row['branch']+'_overlap_temporal_current',error<2e-7,error)
        system=FixedGridMovingTrace(33,False,amplitude=0,degree=6,radial_degree=20)
        state=system.initial_state.copy()
        system.values(state)[:,2*system.count+1]=-.00008*(1+.03*system.offsets)
        evaluated=system.evaluate(0,state)
        dust=DustGravityCollar(6,width=.001,initial_radius=6.03)
        dust_state=dust.initial_state.copy()
        dust_state[dust.count:2*dust.count]=system.values(state)[:,2*system.count+1]
        independent=dust.rhs(0,dust_state).reshape(3,dust.count).T
        error=float(np.max(abs(system.values(evaluated['rhs'])[:,2*system.count:]-independent)))
        evidence.check('zero_wave_independent_live_GR_dust',error<2e-9,error)
        for gram in [False,True]:
            flat=FixedGridMovingTrace(33,gram,coupling=0,central_mass=0)
            state=tangent_preparation(flat)
            evaluated=flat.evaluate(0,state)
            def energy(current):
                values=flat.values(current)
                radius=flat.radii[None,:]+flat.width*flat.offsets[:,None]
                amplitudes=(flat.factors @ values[:,:flat.count].T).T
                field=np.sum(values[:,flat.count:2*flat.count]**2/(2*flat.node_weights*radius**2),axis=1)
                field+=np.sum(amplitudes**2*(flat.sampling @ radius.T**2).T,axis=1)/(2*flat.spacing)
                particle=np.sqrt(flat.source_mass**2+values[:,2*flat.count+1]**2)
                return field+particle
            drift=energy(state.astype(complex)+1e-22j*evaluated['rhs']).imag/1e-22
            evidence.check(str(gram)+'_independent_flat_field_plus_particle_energy',np.max(abs(drift))<2e-12,
                           float(np.max(abs(drift))))
        evidence.report.update(no_conservation_projection=True,independent_ODE_is_same_declared_source_model=True,
                               observational_validation=False,full_GR_limit_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

