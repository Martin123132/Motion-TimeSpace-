from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_live_gravity_20260914 import MovingLiveGravity
import numpy as np
import sympy as sp
import json


def case(width,degree,radial_degree,gram):
    system=MovingLiveGravity(33,gram,degree=degree,radial_degree=radial_degree,width=width)
    state=system.initial_state.copy()
    values=system.values(state)
    values[:,system.free:2*system.free]=.005*values[:,:system.free]
    values[:,2*system.free+1]=-.00008*(1+.03*system.offsets)
    evaluated=system.evaluate(0,state)
    geometry=evaluated['geometry']
    radii=geometry.material(np.array([-.3,0.,.3]))['R'].ravel()
    current=geometry.mass_current(radii)
    changed=system.geometry(state.astype(complex)+1e-22j*evaluated['rhs'])
    derivative=changed.metric(radii)['mu'].imag/1e-22
    residual=derivative-current['total']
    return dict(branch='MTS' if gram else 'reference',width=width,degree=degree,radial_degree=radial_degree,
                maximum_error=float(np.max(abs(residual))),
                width_times_error=float(width*np.max(abs(residual))),
                outer_mass_rate=float(changed.outer_mass.imag/1e-22))


def main():
    evidence=EvidenceRun('annular-affine-moving-current-obstruction-attempt01',__file__)
    try:
        kinetic,potential,velocity=sp.symbols('k v W',real=True)
        coefficient=(kinetic+potential)*velocity-2*potential*velocity
        evidence.check('weak_gravity_unmatched_density_derivative_coefficient',
                       sp.expand(coefficient-(kinetic-potential)*velocity)==0)
        lapse,geometry,particle,energy=sp.symbols('N F p E',positive=True)
        source_speed=lapse*geometry*particle/energy
        evidence.check('dust_source_density_derivative_cancels',
                       sp.simplify(energy*source_speed-lapse*geometry*particle)==0)
        for gram in [False,True]:
            standard=case(.001,6,16,gram)
            refined=case(.001,10,24,gram)
            narrow=[case(width,6,16,gram) for width in [.0005,.00025]]
            evidence.report['cases'].extend([standard,refined]+narrow)
            evidence.check(standard['branch']+'_source_quadrature_not_the_cause',
                           abs(refined['maximum_error']-standard['maximum_error'])<2e-8 and
                           refined['maximum_error']>2e-7,dict(standard=standard,refined=refined))
            scaled=[row['width_times_error'] for row in [standard]+narrow]
            evidence.check(standard['branch']+'_inverse_width_leading_defect',
                           max(scaled)/min(scaled)<1.03,scaled)
            evidence.check(standard['branch']+'_global_energy_does_not_certify_local_gravity',
                           abs(standard['outer_mass_rate'])<2e-10 and standard['maximum_error']>2e-7)
        failed_path=evidence.root/'source-intake/navier-stokes/20260914/annular-moving-live-gravity-qualification-attempt01/status.json'
        failed=json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('original_failure_remains_failed',failed['state']=='failed')
        evidence.report.update(affine_moving_grid_local_gravity_gate_pass=False,
                               diagnostic_checks_not_a_physics_pass=True,
                               unmatched_distributional_coefficient_scope='Leading weak-backreaction transport term; finite-width numerical tests accompany it.',
                               zero_width_or_full_GR_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

