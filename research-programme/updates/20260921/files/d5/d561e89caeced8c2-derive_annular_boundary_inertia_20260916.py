from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
from run_annular_source_fitted_crossing_20260915 import initial
from annular_variational_initial_projection_20260916_v2 import projection_features
from scipy.linalg import solve_banded
import numpy as np


def boundary_inertia(system, state):
    coordinates,rates = np.split(state[:-1],2)
    data = system.evaluate(0.,coordinates,rates)
    half_band = (len(data['mass_bands'])-1)//2
    projection = solve_banded((half_band,half_band),data['mass_bands'],data['cross'])
    indices,shape,radial = projection_features(system,system.reference_radius)
    radius,jacobian,displacement = system.mapping(system.reference_radius,coordinates[-1])
    generator = -displacement*data['field_radial']
    projected_generator = np.sum(shape*projection[indices],axis=1)
    temporal_measure = data['weight']*radius**4/data['coefficient']
    complement = generator-projected_generator
    added_mass = float(temporal_measure @ complement**2)
    lapse,root = system.metric(0.,coordinates[-1])
    material_inertia = system.source_mass*lapse**2/(root**2*data['clock']**3)
    schur = float(data['source_inertia']-data['cross'] @ projection)
    moved = system.evaluate(1e-24j,coordinates+1e-24j*rates,rates)
    right = np.append(data['scalar_covector'],system.source_covector(0.,coordinates,rates))-moved['momenta'].imag/1e-24
    free_field = solve_banded((half_band,half_band),data['mass_bands'],right[:-1])
    drive = float(right[-1]-data['cross'] @ free_field)
    acceleration = system.acceleration(0.,coordinates,rates)
    force = float(material_inertia*acceleration[-1])
    leading = float(-2*added_mass/coordinates[-1]*material_inertia/(material_inertia+added_mass))
    near = abs(system.reference_radius-system.anchor) < .05
    return dict(added_mass=added_mass,material_inertia=float(material_inertia),schur=schur,
        schur_identity_error=abs(schur-material_inertia-added_mass),eliminated_drive=drive,
        mechanical_force=force,eliminated_force=float(material_inertia*drive/schur),
        locally_constant_profile_force_estimate=leading,
        estimate_relative_error=float(abs(leading-force)/max(abs(force),1e-30)),
        near_source_complement_fraction=float(np.dot(temporal_measure[near],complement[near]**2)/added_mass),
        dimensionless_boundary_capacity=float(added_mass/(coordinates[-1]**2*.01**2*getattr(system,'gram_spacing',system.spacing))))


def main():
    evidence = EvidenceRun('annular-boundary-inertia-attempt01',__file__)
    try:
        for degree,constructor in [(1,SourceFittedAction),(2,QuadraticSourceFittedAction)]:
            for count in [33,65,129,257,513,1025,2049]:
                for gram in [False,True]:
                    branch = 'MTS' if gram else 'reference'
                    system = constructor(count,gram,background_mass=0.)
                    row = boundary_inertia(system,initial(system))
                    row.update(degree=degree,count=count,branch=branch)
                    evidence.check(str(degree)+branch+str(count)+'_positive_orthogonal_complement_Schur',row['added_mass'] > 0 and row['schur_identity_error'] < 2e-14,row['schur_identity_error'])
                    evidence.check(str(degree)+branch+str(count)+'_exact_eliminated_source_force',abs(row['mechanical_force']-row['eliminated_force']) < 2e-14)
                    evidence.report['cases'].append(row)
                    evidence.save()
        evidence.report.update(scope='Exact finite-action kinetic projection identity, plus an explicitly approximate local initial-force law; not a force subtraction.',
            local_initial_law_not_asserted_exact=True,all_source_inertia_retained=True,
            full_GR_limit_proven=False,valid_for_physics_claim=False,live_quadratic_geometry_qualified=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
