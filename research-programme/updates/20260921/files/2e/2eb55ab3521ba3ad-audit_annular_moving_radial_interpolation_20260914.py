import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import warnings
import numpy as np
from scipy.interpolate import PchipInterpolator, CubicHermiteSpline
from annular_moving_wave_20260914 import MovingWave
from annular_reference_continuum_shell_20260914 import EvidenceRun


def stable_slopes(coordinate, values):
    widths=np.diff(coordinate)
    secants=np.diff(values)/widths
    slopes=np.zeros_like(values)
    selected=(secants[:-1]!=0)&(secants[1:]!=0)&(np.sign(secants[:-1])==np.sign(secants[1:]))
    first=2*widths[1:]+widths[:-1]
    second=widths[1:]+2*widths[:-1]
    scale=np.minimum(abs(secants[:-1][selected]),abs(secants[1:][selected]))
    denominator=(first[selected]*(scale/abs(secants[:-1][selected]))+
                 second[selected]*(scale/abs(secants[1:][selected])))
    slopes[1:-1][selected]=np.sign(secants[:-1][selected])*scale*((first[selected]+second[selected])/denominator)
    def edge(width_a,width_b,secant_a,secant_b):
        value=((2*width_a+width_b)*secant_a-width_a*secant_b)/(width_a+width_b)
        if np.sign(value)!=np.sign(secant_a):
            return 0.
        if np.sign(secant_a)!=np.sign(secant_b) and abs(value)>3*abs(secant_a):
            return 3*secant_a
        return value
    slopes[0]=edge(widths[0],widths[1],secants[0],secants[1])
    slopes[-1]=edge(widths[-1],widths[-2],secants[-1],secants[-2])
    return slopes


def run():
    evidence=EvidenceRun('annular-moving-radial-interpolation-attempt01',__file__)
    try:
        evidence.report.update(scope='Audit SciPy PCHIP reciprocal-overflow warning on subnormal tails using an algebraically equivalent scaled harmonic mean. No density clipping or changes to PDE.',
                               copied_data_threshold=None,coupled_moving_GR_scalar_PDE_tested=True)
        path=evidence.output.parent/'annular-moving-GR-PDE-attempt01/count4097.npz'
        evidence.own(path)
        archive=np.load(path)
        system=MovingWave(4097,coupling=.1)
        for index in [16,32,56]:
            data=system.geometry(archive['states'][index])
            radii,energy=data['radii'],data['density']
            with warnings.catch_warnings(record=True) as observed:
                warnings.simplefilter('always')
                original=PchipInterpolator(radii,energy)
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                slopes=stable_slopes(radii,energy)
                alternate=CubicHermiteSpline(radii,energy,slopes)
            interval=np.diff(radii)
            difference=abs(original.c-alternate.c)
            bound=float(np.max(np.sum(difference*interval[None,:]**np.array([3,2,1,0])[:,None],axis=0)))
            probes=np.concatenate([radii,(radii[:-1]+radii[1:])/2])
            evidence.check(str(index)+'_both_polynomials_finite',np.isfinite(original.c).all() and np.isfinite(alternate.c).all())
            evidence.check(str(index)+'_scaled_harmonic_mean_same_curve',bound<2e-15,bound)
            evidence.check(str(index)+'_same_nodal_data_without_clipping',np.max(abs(alternate(radii)-energy))<2e-15)
            evidence.check(str(index)+'_sampled_difference_within_coefficient_bound',np.max(abs(original(probes)-alternate(probes)))<=bound+2e-17)
            evidence.report['cases'].append(dict(index=index,warning_messages=[str(row.message) for row in observed],
                                                 maximum_interval_polynomial_difference_bound=bound,
                                                 minimum_positive_density=float(np.min(energy[energy>0])),
                                                 maximum_sample_difference=float(np.max(abs(original(probes)-alternate(probes))))))
            evidence.save()
        synthetic_coordinate=np.arange(5,dtype=float)
        synthetic_values=np.array([0.,1e-310,2e-310,4e-310,8e-310])
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            synthetic=stable_slopes(synthetic_coordinate,synthetic_values)
        evidence.check('subnormal_positive_slopes_not_forced_to_zero',np.all(synthetic[1:-1]>0) and np.isfinite(synthetic).all())
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    run()

