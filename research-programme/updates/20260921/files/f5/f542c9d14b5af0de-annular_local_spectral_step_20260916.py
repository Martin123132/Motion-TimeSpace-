import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
from annular_variational_initial_projection_20260916_v2 import projection_features,assemble_matrix


def spectral_step(system,state):
    coordinates,rates = np.split(state[:-1],2)
    data = system.evaluate(0.,coordinates,rates)
    indices,shape,radial = projection_features(system,system.reference_radius)
    radius,jacobian,displacement = system.mapping(system.reference_radius,coordinates[-1])
    temporal_weight = data['weight']*radius**4/data['coefficient']
    mass = assemble_matrix(system,indices,shape,temporal_weight)
    stiffness = assemble_matrix(system,indices,radial/jacobian[:,None],data['weight']*data['coefficient'])
    node_radius,node_jacobian,unused = system.mapping(system.radii,coordinates[-1])
    gram_weight = np.asarray(system.sampling @ (system.coefficient(0.,node_radius)/node_jacobian))/system.gram_spacing
    stiffness += system.lifted.T @ diags(gram_weight) @ system.lifted
    values,vectors = eigsh(stiffness,k=1,M=mass,which='LM',tol=1e-11,v0=np.linspace(1.,2.,system.count))
    eigenvalue,vector = float(values[0]),vectors[:,0]
    residual = float(np.linalg.norm(stiffness @ vector-eigenvalue*(mass @ vector))/np.linalg.norm(stiffness @ vector))
    lapse,root = system.metric(0.,coordinates[-1])
    material = system.source_mass*lapse**2/(root**2*data['clock']**3)
    coupled_factor = float(np.sqrt(data['source_inertia']/material))
    frequency = np.sqrt(eigenvalue)*coupled_factor
    return dict(largest_field_eigenvalue=eigenvalue,eigen_residual=residual,coupled_factor=coupled_factor,
        frequency_estimate=float(frequency),maximum_step=float(min(.2*system.spacing,.8/(1.25*frequency))),
        frozen_spectrum_is_not_a_nonlinear_stability_proof=True)
