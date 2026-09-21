from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import cholesky, eigh, solve_triangular
import numpy as np
import json


def weight_log_bounds(system, window):
    inner,outer = system.radii[[0,-1]]
    alpha = 2*system.background_mass
    distance = min(window[0]-inner,outer-window[1])
    if distance <= 0 or inner <= alpha:
        raise ValueError('Positive prescribed coefficient and interior source window required.')
    if np.any(system.sampling.data<0):
        raise ValueError('Positive sampling combination required for the Gram weight proof.')
    mass = 1/distance+3/inner+1/(inner-alpha)
    stiffness = 1/distance+1/inner+1/(inner-alpha)
    if alpha==0:
        mass = stiffness = 1/distance+2/inner
    return dict(mass=float(mass),stiffness=float(stiffness),eigenvalue=float(mass+stiffness))


def eigenvalue_enclosure_estimate(mass,stiffness):
    values,vectors = eigh(stiffness,mass)
    lower = cholesky(mass,lower=True)
    residual = solve_triangular(lower,stiffness @ vectors-(mass @ vectors)*values[None,:],lower=True)
    orthogonality = float(np.linalg.norm(vectors.T @ mass @ vectors-np.eye(len(values)),ord=np.inf))
    if orthogonality>=1:
        raise ValueError('Unresolved generalized eigenbasis orthogonality.')
    root = np.sqrt(1-orthogonality)
    polar_bound = 2*orthogonality*np.max(abs(values))/(root*(1+root))+np.linalg.norm(residual)/root
    roundoff_allowance = 128*np.finfo(float).eps*len(values)*np.max(abs(values))
    return values,dict(orthogonality=orthogonality,polar_residual_estimate=float(polar_bound),
        roundoff_allowance=float(roundoff_allowance),radius=float(polar_bound+roundoff_allowance))


def main():
    evidence = EvidenceRun('annular-chart-window-gap-attempt01',__file__)
    try:
        path = evidence.root/'source-intake/navier-stokes/20260914/annular-anchored-chart-qualification-attempt03/status.json'
        evidence.own(path)
        qualified = json.loads(path.read_text())
        evidence.check('charted_qualification_complete',qualified['state']=='complete')
        for gram in [False,True]:
            branch = 'MTS' if gram else 'reference'
            row = next(row for row in qualified['cases'] if row['branch']==branch and row['base_count']==129)
            survey = row['selection_survey']
            system = LocallyRefinedSourceAction(129,gram,background_mass=0.,source_splits=8)
            bounds = weight_log_bounds(system,survey['window'])
            positions = np.linspace(*survey['window'],survey['samples'])
            radius = float(np.max(np.diff(positions))/2)
            retained = np.zeros(system.count,dtype=bool)
            retained[survey['retained_indices']] = True
            boundaries = np.flatnonzero(retained[:-1]!=retained[1:])
            spectra,enclosures,margins = [],[],[]
            for position in positions:
                matrices = field_matrices(system,float(position))
                values,enclosure = eigenvalue_enclosure_estimate(matrices['mass'].toarray(),matrices['stiffness'].toarray())
                upper = (values[boundaries]+enclosure['radius'])*np.exp(bounds['eigenvalue']*radius)
                lower = (values[boundaries+1]-enclosure['radius'])*np.exp(-bounds['eigenvalue']*radius)
                margins.append(lower-upper)
                spectra.append(values)
                enclosures.append(enclosure)
            spectra,margins = np.array(spectra),np.array(margins)
            normalized = margins/np.maximum(1.,spectra[:,boundaries+1])
            evidence.check(branch+'_positive_weight_structure',np.all(system.sampling.data>=0) and bounds['mass']>0 and bounds['stiffness']>0)
            evidence.check(branch+'_whole_window_gap_envelope_positive_in_float',float(np.min(margins))>0,
                dict(minimum_absolute_margin=float(np.min(margins)),minimum_relative_margin=float(np.min(normalized))))
            evidence.check(branch+'_floating_enclosure_below_gap_margin',max(item['radius'] for item in enclosures)<float(np.min(margins))/10)
            path = evidence.output/(branch+'-window-spectrum.npz')
            np.savez_compressed(path,positions=positions,spectra=spectra,boundaries=boundaries,gap_margins=margins,
                floating_enclosure_radii=np.array([row['radius'] for row in enclosures]))
            evidence.own(path,'outputs')
            evidence.report['cases'].append(dict(branch=branch,window=survey['window'],survey_count=len(positions),
                covering_cell_radius=radius,retained_count=int(np.sum(retained)),boundary_indices=boundaries.tolist(),
                logarithmic_weight_bounds=bounds,minimum_absolute_gap_margin=float(np.min(margins)),
                minimum_relative_gap_margin=float(np.min(normalized)),maximum_enclosure_radius=max(row['radius'] for row in enclosures),
                theorem='If the center eigenvalue enclosures are valid, positive exponential gap margins exclude all retained/omitted crossings in the entire covered window.',
                floating_evaluation_not_interval_arithmetic=True,rigorous_interval_certificate=False))
            evidence.save()
        synthetic_values = np.array([1.,1.000001])
        separated = synthetic_values[1]*np.exp(-.01)-synthetic_values[0]*np.exp(.01)>0
        evidence.check('undersampled_near_crossing_not_certified',not separated)
        evidence.report.update(analytic_uniform_gap_criterion_derived=True,
            continuous_gap_numerically_supported=True,rigorous_interval_certificate=False,
            proof_depends_on_certified_eigenvalue_enclosures=True,no_claim_of_new_physical_limit=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
