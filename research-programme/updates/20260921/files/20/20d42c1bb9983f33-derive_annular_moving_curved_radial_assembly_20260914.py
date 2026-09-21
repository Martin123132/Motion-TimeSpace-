from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_scalar_action_20260912 import full_spatial_factors
import numpy as np
import sympy as sp
from scipy.optimize import brentq


class CurvedSlice:
    def __init__(self,count,gram):
        self.count=count
        self.coordinate=np.linspace(0.,1.,count)
        self.delta=1/(count-1)
        self.quadrature=np.full(count,self.delta)
        self.quadrature[[0,-1]]/=2
        self.factors,self.sampling=full_spatial_factors(count,gram)
        base,sampling=full_spatial_factors(count,False)
        derivative=(sampling.T @ base)/self.quadrature[:,None]
        self.transport=self.coordinate[:,None]*derivative
        self.scalar=.011*np.sin(np.pi*self.coordinate)+.002*np.sin(3*np.pi*self.coordinate)
        self.rate=.006*np.sin(2*np.pi*self.coordinate)+.003*np.sin(np.pi*self.coordinate)
        self.scalar[-1]=self.rate[-1]=0.
        self.source=.003

    def evaluate(self,position=6.03,velocity=.17,scalar=None,rate=None,lapse=None,mass=None):
        scalar=self.scalar if scalar is None else scalar
        rate=self.rate if rate is None else rate
        length=position-3
        radius=3+length*self.coordinate
        lapse=.89+.01*(radius-5)+.002*(radius-5)**2 if lapse is None else lapse
        mass=.8+.0003*(radius-3)+.0001*(radius-3)**2 if mass is None else mass
        lapse_radial=.01+.004*(radius-5)
        mass_radial=.0003+.0002*(radius-3)
        geometry=1-2*mass/radius
        root=np.sqrt(geometry)
        root_radial=(mass/radius**2-mass_radial/radius)/root
        measure=length*self.quadrature
        spacing=length*self.delta
        kinetic_weight=measure*radius**2/(lapse*root)
        transport=self.transport/length
        transported=transport @ scalar
        eulerian=rate-velocity*transported
        canonical=kinetic_weight*eulerian
        amplitudes=self.factors @ scalar
        coefficients=self.sampling @ (radius**2*lapse*root)/spacing
        potential=radius**2*(self.sampling.T @ amplitudes**2)/(2*spacing)
        density=canonical**2/(2*measure*radius**2)+potential
        proper=np.sqrt(lapse[-1]**2-velocity**2/geometry[-1])
        source_momentum=self.source*velocity/(geometry[-1]*proper)
        energy=self.source*lapse[-1]/proper
        lagrangian=np.sum(kinetic_weight*eulerian**2)/2-np.sum(coefficients*amplitudes**2)/2-self.source*proper
        edge_inertia=kinetic_weight[-1]*transported[-1]**2
        total_source=source_momentum+edge_inertia*velocity-canonical[:-1] @ transported[:-1]
        lapse_gradient=-root*density
        lapse_gradient[-1]-=energy
        mass_gradient=lapse*density/(radius*root)
        mass_gradient[-1]+=lapse[-1]*source_momentum**2/(radius[-1]*energy)
        metric_log_radial=lapse_radial/lapse+root_radial/root
        kinetic_b=kinetic_weight*(1/length+2*self.coordinate/radius-self.coordinate*metric_log_radial)
        coefficient_b=self.sampling @ (self.coordinate*(2*radius*lapse*root+
                            radius**2*(lapse_radial*root+lapse*root_radial)))/spacing-coefficients/length
        edge_b=edge_inertia*(2/position-1/length-metric_log_radial[-1])
        source_force=-energy*lapse_radial[-1]-lapse[-1]*root[-1]*root_radial[-1]*source_momentum**2/energy
        position_gradient=np.sum(kinetic_b[:-1]*eulerian[:-1]**2)/2
        position_gradient+=velocity/length*(canonical[:-1] @ transported[:-1])
        position_gradient+=edge_b*velocity**2/2-np.sum(coefficient_b*amplitudes**2)/2+source_force
        scalar_gradient=-velocity*transport[:-1,:-1].T @ canonical[:-1]
        scalar_gradient-=self.factors[:,:-1].T @ (coefficients*amplitudes)
        scalar_gradient+=velocity**2*kinetic_weight[-1]*transported[-1]*transport[-1,:-1]
        return dict(action=lagrangian,radius=radius,N=lapse,mass=mass,U=root,measure=measure,
                    source_momentum=source_momentum,source_energy=energy,canonical=canonical,
                    total_source=total_source,lapse_gradient=lapse_gradient,mass_gradient=mass_gradient,
                    position_gradient=position_gradient,scalar_gradient=scalar_gradient,
                    edge_slope=transported[-1],transported=transported,density=density)


def main():
    evidence=EvidenceRun('annular-moving-curved-radial-assembly-attempt01',__file__)
    try:
        radius,mass,lapse,lapse_R,coupling,scalar_density,source_density,source,p_s=sp.symbols(
            'R mu N N_R kappa e rho S p',positive=True)
        geometry=1-2*mass/radius
        root=sp.sqrt(geometry)
        energy=sp.sqrt(source**2+geometry*p_s**2)
        mass_R=coupling*(geometry*scalar_density+root*energy*source_density)
        log_N_R=mass/(radius**2*geometry)+coupling*scalar_density/radius
        log_N_R+=coupling*root*p_s**2*source_density/(radius*energy)
        root_R=(mass/radius**2-mass_R/radius)/root
        raw=-energy*lapse*log_N_R-lapse*root*root_R*p_s**2/energy
        reduced=-lapse*mass/radius**2*(energy/geometry+p_s**2/energy)
        reduced-=coupling*lapse*source**2*scalar_density/(radius*energy)
        evidence.check('scalar_loaded_source_gravitational_force',sp.simplify(raw-reduced)==0)
        gravity_covector=-lapse_R/(coupling*root)+lapse*mass/(coupling*radius**2*root**3)
        matter_covector=lapse*scalar_density/(radius*root)+lapse*p_s**2*source_density/(radius*energy)
        evidence.check('canonical_Pdot_zero_gives_radial_lapse',
                       sp.simplify((gravity_covector+matter_covector).subs(lapse_R,lapse*log_N_R))==0)
        weight,slope=sp.symbols('omega dchi',positive=True)
        endpoint=weight*radius**2*root*p_s*slope**2/energy
        monotonic=1+weight*radius**2*root*source**2*slope**2/energy**3
        evidence.check('endpoint_canonical_map_positive_derivative',
                       sp.simplify(sp.diff(p_s+endpoint,p_s)-monotonic)==0)
        for count in [17,33]:
            for gram in [False,True]:
                system=CurvedSlice(count,gram)
                data=system.evaluate()
                label=('MTS' if gram else 'reference')+'-'+str(count)
                direction=.3+.1*np.cos(system.coordinate)
                step=1e-25
                lapse_value=system.evaluate(lapse=data['N'].astype(complex)+1j*step*direction)['action'].imag/step
                mass_value=system.evaluate(mass=data['mass'].astype(complex)+1j*step*direction)['action'].imag/step
                source_value=system.evaluate(velocity=.17+1j*step)['action'].imag/step
                position_value=system.evaluate(position=6.03+1j*step)['action'].imag/step
                scalar_direction=np.sin(2.7*system.coordinate)
                scalar_direction[-1]=0.
                scalar_value=system.evaluate(scalar=system.scalar.astype(complex)+1j*step*scalar_direction)['action'].imag/step
                rate_value=system.evaluate(rate=system.rate.astype(complex)+1j*step*scalar_direction)['action'].imag/step
                expected=dict(lapse=data['lapse_gradient'] @ direction,mass=data['mass_gradient'] @ direction,
                              source=data['total_source'],position=data['position_gradient'],
                              scalar=data['scalar_gradient'] @ scalar_direction[:-1],
                              scalar_rate=data['canonical'] @ scalar_direction)
                observed=dict(lapse=lapse_value,mass=mass_value,source=source_value,position=position_value,
                              scalar=scalar_value,scalar_rate=rate_value)
                errors={key:float(abs(observed[key]-value)) for key,value in expected.items()}
                for key,error in errors.items():
                    evidence.check(label+'_'+key+'_action_derivative',error<3e-12,error)
                difference_step=.0002
                values={multiple:system.evaluate(position=6.03+multiple*difference_step)['action']
                        for multiple in [-2,-1,1,2]}
                independent=(values[-2]-8*values[-1]+8*values[1]-values[2])/(12*difference_step)
                evidence.check(label+'_independent_curved_embedding_difference',
                               abs(independent-data['position_gradient'])<3e-11,float(abs(independent-data['position_gradient'])))
                target=data['total_source']+data['canonical'][:-1] @ data['transported'][:-1]
                coefficient=data['measure'][-1]*data['radius'][-1]**2*data['U'][-1]*data['edge_slope']**2
                def canonical_map(momentum):
                    energy=np.sqrt(system.source**2+data['U'][-1]**2*momentum**2)
                    return momentum+coefficient*momentum/energy
                recovered=brentq(lambda momentum:canonical_map(momentum)-target,-1.,1.,xtol=1e-15)
                evidence.check(label+'_positive_endpoint_inversion',
                               abs(recovered-data['source_momentum'])<3e-13,
                               float(abs(recovered-data['source_momentum'])))
                wrong=data['source_momentum']-data['canonical'][:-1] @ data['transported'][:-1]
                evidence.check(label+'_endpoint_inertia_cannot_be_dropped',abs(wrong-data['total_source'])>1e-8)
                evidence.report['cases'].append(dict(branch='MTS' if gram else 'reference',count=count,
                                                    derivative_errors=errors,endpoint_canonical_correction=float(data['total_source']-wrong),
                                                    independent_embedding_error=float(abs(independent-data['position_gradient']))))
        evidence.report.update(live_curved_evolution_completed=False,
                               radial_and_lapse_matter_covectors_checked=True,
                               total_source_embedding_covector_checked=True,
                               endpoint_inversion_monotone_at_fixed_geometry=True,
                               combined_nonlinear_metric_uniqueness_proven=False,
                               temporal_canonical_current_evolution_checked=False,
                               physical_width_or_material_coefficients_parent_derived=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

