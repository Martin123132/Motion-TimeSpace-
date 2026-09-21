from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.sparse import csr_matrix
from scipy.linalg import cholesky_banded, cho_solve_banded
import numpy as np


def quadrature_maps(layer, position):
    radius, jacobian, motion = layer.mapping(layer.reference_radius, position)
    rows = np.repeat(np.arange(len(radius)), 3)
    columns = layer.reference_indices.ravel()
    shape = csr_matrix((layer.reference_shape.ravel(), (rows, columns)), shape=(len(radius), layer.count))
    gradient = csr_matrix((layer.reference_radial.ravel(), (rows, columns)), shape=shape.shape)
    material = (-motion/jacobian)[:, None]*layer.reference_radial
    material_map = csr_matrix((material.ravel(), (rows, columns)), shape=shape.shape)
    coefficient = layer.coefficient(0., radius)
    weight = layer.reference_weight*jacobian*radius**4/coefficient
    gradient_weight = layer.reference_weight*coefficient/jacobian
    nodes, node_jacobian, unused = layer.mapping(layer.radii, position)
    gram_weight = (layer.sampling @ (layer.coefficient(0., nodes)/node_jacobian))/layer.gram_spacing
    return shape, gradient, material_map, weight, gradient_weight, gram_weight


class FullSchurForce:
    def __init__(self, layer, tangent_layer, position, source_velocity):
        self.layer, self.tangent_layer = layer, tangent_layer
        self.position, self.source_velocity = float(position), float(source_velocity)
        step = 1e-24
        shape, gradient, material, weight, gradient_weight, gram_weight = quadrature_maps(layer, position)
        partial = quadrature_maps(layer, position+1j*step)
        moving = quadrature_maps(tangent_layer, position+1j*step*source_velocity)
        self.shape, self.gradient, self.material = shape, gradient, material
        self.weight, self.gradient_weight, self.gram_weight = weight, gradient_weight, gram_weight
        self.gram = layer.lifted.tocsr()
        self.material_partial = partial[2].imag/step
        self.weight_partial = partial[3].imag/step
        self.gradient_partial = partial[4].imag/step
        self.gram_partial = partial[5].imag/step
        self.material_rate = moving[2].imag/step
        self.weight_rate = moving[3].imag/step
        zeros = np.zeros(layer.count)
        coordinates = np.append(zeros, position)
        rates = np.append(zeros, source_velocity)
        data = layer.evaluate(0., coordinates, rates)
        self.mass_bands = data['mass_bands']
        self.mass_factor = cholesky_banded(self.mass_bands[2:].copy(), lower=True, check_finite=False)
        lapse, root = layer.metric(0., position)
        self.inertia = float(layer.source_mass*lapse**2/(root**2*data['clock']**3))
        changed = tangent_layer.evaluate(0., coordinates.astype(complex)+1j*step*rates, rates)
        self.dust_drive = float(layer.source_covector(0., coordinates, rates)-changed['material_momentum'].imag/step)
        if self.inertia <= 0 or np.any(weight <= 0):
            raise ValueError('Positive kinetic weights and timelike dust inertia required.')

    def solve(self, values):
        return cho_solve_banded((self.mass_factor, True), values, check_finite=False)

    def stiffness(self, values, partial=False):
        gradient_weight = self.gradient_partial if partial else self.gradient_weight
        gram_weight = self.gram_partial if partial else self.gram_weight
        return self.gradient.T @ (gradient_weight*(self.gradient @ values))+self.gram.T @ (gram_weight*(self.gram @ values))

    def evaluate(self, scalar, velocity, with_gradient=False):
        source_velocity = self.source_velocity
        shape, material = self.shape, self.material
        motion = material @ scalar
        temporal = shape @ velocity+source_velocity*motion
        transport_motion = self.material_rate @ scalar+material @ velocity
        partial_motion = self.material_partial @ scalar
        raw = (.5*float(temporal @ (self.weight_partial*temporal))
            +source_velocity*float(temporal @ (self.weight*partial_motion))
            -.5*float(scalar @ self.stiffness(scalar, partial=True)))
        transport = float(transport_motion @ (self.weight*temporal)
            +motion @ (self.weight_rate*temporal)+source_velocity*motion @ (self.weight*transport_motion))
        right_side = (source_velocity*(material.T @ (self.weight*temporal))-self.stiffness(scalar)
            -shape.T @ (self.weight_rate*temporal+source_velocity*self.weight*transport_motion))
        cross = shape.T @ (self.weight*motion)
        projected = self.solve(cross)
        free_acceleration = self.solve(right_side)
        coupling = float(cross @ free_acceleration)
        drive = raw-transport-coupling
        complement = motion-shape @ projected
        ratio = float(complement @ (self.weight*complement))/self.inertia
        force = (drive-ratio*self.dust_drive)/(1+ratio)
        result = dict(force=force, free_wave_drive=drive, inertia_ratio=ratio,
            dust_drive=self.dust_drive, dust_inertia=self.inertia,
            raw_wave=raw, source_transport=transport, scalar_projection=coupling,
            cancellation_scale=abs(raw)+abs(transport)+abs(coupling)+abs(ratio*self.dust_drive))
        if with_gradient:
            raw_scalar = (source_velocity*(material.T @ (self.weight_partial*temporal))
                +source_velocity**2*(material.T @ (self.weight*partial_motion))
                +source_velocity*(self.material_partial.T @ (self.weight*temporal))-self.stiffness(scalar, partial=True))
            raw_velocity = shape.T @ (self.weight_partial*temporal+source_velocity*self.weight*partial_motion)
            partial_temporal = self.weight*transport_motion+self.weight_rate*motion
            partial_motion_load = self.weight_rate*temporal+source_velocity*self.weight*transport_motion
            partial_transport = self.weight*(temporal+source_velocity*motion)
            transport_scalar = (source_velocity*(material.T @ partial_temporal)
                +material.T @ partial_motion_load+self.material_rate.T @ partial_transport)
            transport_velocity = shape.T @ partial_temporal+material.T @ partial_transport
            projected_shape = shape @ projected
            dual_temporal = source_velocity*self.weight*(material @ projected)-self.weight_rate*projected_shape
            dual_transport = -source_velocity*self.weight*projected_shape
            projection_scalar = (material.T @ (self.weight*(shape @ free_acceleration))
                +source_velocity*(material.T @ dual_temporal)-self.stiffness(projected)
                +self.material_rate.T @ dual_transport)
            projection_velocity = shape.T @ dual_temporal+material.T @ dual_transport
            grad_drive = np.stack([raw_scalar-transport_scalar-projection_scalar,
                raw_velocity-transport_velocity-projection_velocity])
            complement_dual = self.weight*complement
            complement_dual -= self.weight*(shape @ self.solve(shape.T @ complement_dual))
            grad_ratio = np.stack([2*(material.T @ complement_dual)/self.inertia, np.zeros_like(scalar)])
            result.update(gradient_drive=grad_drive, gradient_ratio=grad_ratio,
                gradient_force=(grad_drive-(self.dust_drive+force)*grad_ratio)/(1+ratio))
        return result

    def secant(self, first, last):
        before, after = self.evaluate(*first), self.evaluate(*last)
        middle = self.evaluate(*((first+last)/2), with_gradient=True)
        covector = (middle['gradient_drive']-(self.dust_drive+before['force'])*middle['gradient_ratio'])/(1+after['inertia_ratio'])
        return covector, before, after


def schur_difference(first, last):
    denominator = 1+last['inertia_ratio']
    drive = (last['free_wave_drive']-first['free_wave_drive'])/denominator
    gravity = -last['inertia_ratio']*(last['dust_drive']-first['dust_drive'])/denominator
    inertia = -(last['inertia_ratio']-first['inertia_ratio'])*(first['dust_drive']+first['force'])/denominator
    return dict(wave_drive=drive, dust_drive=gravity, inertia=inertia, total=drive+gravity+inertia,
        direct=last['force']-first['force'])
