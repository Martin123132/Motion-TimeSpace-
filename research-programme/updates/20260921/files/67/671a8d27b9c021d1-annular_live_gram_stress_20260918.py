from derive_annular_source_gravity_20260914 import EvidenceRun
import numpy as np


def weight(labels):
    return 6*(labels+.5)*(.5-labels)


def metric(radius):
    radius = np.asarray(radius)
    root = np.sqrt(1-1.4/radius)
    lapse = root*np.exp(.01*np.sin(1.3*radius))
    radial_root = root*np.exp(.006*np.cos(.7*radius))
    return lapse, radial_root


def coefficient(radius):
    lapse, root = metric(radius)
    return np.asarray(radius)**2*lapse*root


def coefficient_radial(radius):
    radius = np.asarray(radius)
    return coefficient(radius)*(2/radius+1.4/(radius**2*(1-1.4/radius))
        +.013*np.cos(1.3*radius)-.0042*np.sin(.7*radius))


class GramPushforward:
    def __init__(self, system, field, material=(.015, .022, .004), amplitude=(1., .2, .05), width=.02):
        self.system, self.field, self.width = system, np.asarray(field), width
        self.material, self.amplitude = np.asarray(material), np.asarray(amplitude)
        self.direction = np.array([.3, .4, -.1])
        factors = system.lifted @ self.field
        full_gamma = np.asarray(system.sampling.T @ factors**2)/(2*system.gram_spacing)
        selected = np.asarray(system.sampling.sum(axis=0)).ravel() != 0
        self.nodes = system.radii[selected]
        self.gamma = full_gamma[selected]
        self.selected = selected
        unused, unused2, self.displacement = system.mapping(self.nodes, system.anchor)
        self.jacobian_slope = np.where(self.nodes < system.anchor,
            1/(system.anchor-system.radii[0]), -1/(system.radii[-1]-system.anchor))

    def amplitudes(self, labels):
        return np.polynomial.polynomial.polyval(np.asarray(labels), self.amplitude)

    def geometry(self, labels, parameter=0.):
        labels = np.atleast_1d(labels)
        material = self.material+parameter*self.direction
        offset = np.polynomial.polynomial.polyval(labels, material)
        derivative = material[1]+2*material[2]*labels
        radius = self.nodes[None, :]+self.displacement[None, :]*offset[:, None]
        radius += (1-self.displacement[None, :])*self.width*labels[:, None]
        jacobian = 1+self.jacobian_slope[None, :]*(offset-self.width*labels)[:, None]
        label_jacobian = self.width+self.displacement[None, :]*(derivative-self.width)[:, None]
        if min(np.min(np.real(jacobian)), np.min(np.real(label_jacobian))) <= 0:
            raise ValueError('Gram map left the ordered positive-Jacobian branch.')
        return radius, jacobian, label_jacobian

    def edges(self, parameter=0.):
        return np.unique(self.geometry([-.5, .5], parameter)[0].ravel())

    def density(self, radius, parameter=0., wrong_label_jacobian=False):
        radii = np.atleast_1d(radius)
        endpoints = self.geometry([-.5, .5], parameter)[0]
        selected = (radii[:, None] >= endpoints[0]) & (radii[:, None] <= endpoints[1])
        targets, atoms = np.nonzero(selected)
        material = self.material+parameter*self.direction
        shift = radii[targets]-self.nodes[atoms]-self.displacement[atoms]*material[0]
        linear = self.width+self.displacement[atoms]*(material[1]-self.width)
        quadratic = self.displacement[atoms]*material[2]
        labels = 2*shift/(linear+np.sqrt(linear**2+4*quadratic*shift))
        labels = np.clip(labels, -.5, .5)
        offset = np.polynomial.polynomial.polyval(labels, material)
        jacobian = 1+self.jacobian_slope[atoms]*(offset-self.width*labels)
        label_jacobian = self.width+self.displacement[atoms]*(material[1]+2*material[2]*labels-self.width)
        denominator = self.width if wrong_label_jacobian else label_jacobian
        values = weight(labels)*self.gamma[atoms]*self.amplitudes(labels)**2/(jacobian*denominator)
        return np.bincount(targets, weights=values, minlength=len(radii))

    def weak(self, test, parameter=0., order=48):
        points, weights = np.polynomial.legendre.leggauss(order)
        labels, measure = points/2, weights/2
        radius, jacobian, unused = self.geometry(labels, parameter)
        loading = self.gamma[None, :]*self.amplitudes(labels)[:, None]**2/jacobian
        return np.sum(measure[:, None]*weight(labels)[:, None]*loading*test(radius))

    def shape_derivative(self, test, test_radial, order=48):
        points, weights = np.polynomial.legendre.leggauss(order)
        labels, measure = points/2, weights/2
        radius, jacobian, unused = self.geometry(labels)
        direction = np.polynomial.polynomial.polyval(labels, self.direction)
        loading = weight(labels)[:, None]*self.gamma[None, :]*self.amplitudes(labels)[:, None]**2
        transport = np.sum(measure[:, None]*direction[:, None]*loading*self.displacement[None, :]*test_radial(radius)/jacobian)
        dilation = -np.sum(measure[:, None]*direction[:, None]*loading*test(radius)*self.jacobian_slope[None, :]/jacobian**2)
        return float(transport+dilation), float(transport), float(dilation)


class GramLoadedSnapshot:
    def __init__(self, baseline, atoms):
        self.__dict__.update(baseline.__dict__)
        self.baseline, self.atoms = baseline, atoms
        self.edges = np.unique(np.concatenate([baseline.edges, atoms.edges()]))
        if self.edges[0] < self.lower-1e-12 or self.edges[-1] > self.upper+1e-12:
            raise ValueError('Gram bands extend beyond source snapshot domain.')
        self.edges[[0, -1]] = self.lower, self.upper

    def energy(self, radius):
        radius = np.asarray(radius)
        return self.baseline.energy(radius)+radius**2*self.atoms.density(radius).reshape(radius.shape)

    def source(self, radius, shift=0.):
        return self.baseline.source(radius, shift)

    def directions(self, radius):
        radius = np.asarray(radius)
        return radius**2*self.atoms.density(radius).reshape(radius.shape), np.zeros_like(radius), np.zeros_like(radius)
