from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from scipy.linalg import eigvalsh
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-frozen-frequencies-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            source_and_metric_frozen_for_spectral_diagnostic=True,
            full_coupled_stability_theorem=False, no_modes_discarded=True,
            full_live_P2_force_convergence_proven=False)
        for count in [17,33,65]:
            for gram in [False,True]:
                system = PrimitiveP2System(count,gram,layer_degree=14,radial_degree=18,action_order=32,label_order=20)
                coordinates, unused, rates, geometry = system.initial()
                layer = system.layer(0.,geometry)
                values = coordinates[len(system.labels)//2]
                data = layer.evaluate(0.,values,np.zeros_like(values))
                indices, radial = layer.reference_indices, layer.reference_radial
                radius, jacobian, unused = layer.mapping(layer.reference_radius,values[-1])
                coefficient = layer.coefficient(0.,radius)
                weights = layer.reference_weight*coefficient/jacobian
                stiffness = np.zeros((system.count,system.count))
                for first in range(3):
                    for second in range(3):
                        np.add.at(stiffness,(indices[:,first],indices[:,second]),weights*radial[:,first]*radial[:,second])
                nodal, nodal_jacobian, unused = layer.mapping(layer.radii,values[-1])
                lifted = layer.lifted.toarray()
                factor_weight = np.asarray(layer.sampling @ (layer.coefficient(0.,nodal)/nodal_jacobian))/layer.gram_spacing
                stiffness += lifted.T @ (factor_weight[:,None]*lifted)
                mass = np.zeros_like(stiffness)
                for column in range(system.count):
                    for row in range(max(0,column-2),min(system.count,column+3)):
                        mass[row,column] = data['mass_bands'][2+row-column,column]
                eigenvalues = eigvalsh(stiffness,mass,check_finite=False)
                maximum = float(eigenvalues[-1])
                frequency = float(np.sqrt(maximum))
                branch = 'MTS' if gram else 'reference'
                row = dict(branch=branch,base_count=count,scalar_nodes=system.count,
                    minimum_eigenvalue=float(eigenvalues[0]),maximum_eigenvalue=maximum,
                    maximum_angular_frequency=frequency,shortest_period=float(2*np.pi/frequency),
                    shortest_periods_in_first_segment=float(.001*frequency/(2*np.pi)),
                    omega_times_requested_maximum_step=frequency*.0005)
                evidence.report['cases'].append(row)
                evidence.save()
                evidence.check(branch+str(count)+'_positive_frozen_scalar_pencil',eigenvalues[0]>0 and np.isfinite(maximum),row)
                probe = np.sin(np.arange(system.count)+.3)*.001
                tested = np.append(probe,values[-1])
                covector = layer.evaluate(0.,tested,np.zeros_like(tested))['scalar_covector']
                error = float(max(abs(covector+stiffness@probe)))
                evidence.check(branch+str(count)+'_stiffness_matches_existing_action',error < 2e-8,error)
                print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
