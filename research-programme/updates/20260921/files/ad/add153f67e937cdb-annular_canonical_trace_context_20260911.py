from pathlib import Path

import numpy as numerical
import sympy as symbolic

from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
from annular_canonical_inverse_boundary_20260911 import InverseBoundaryInitialData
from annular_canonical_reference_fields_20260911 import ConstructedGRFields, SavedCanonicalFields, local_rate_families
from annular_canonical_rate_completion_20260911 import OriginalFrames, bubbles, complete_phase


def load_archive(path):
    with numerical.load(path, allow_pickle=False) as saved:
        return {name: saved[name].copy() for name in saved.files}


class TraceContext:
    def __init__(self, root, branch):
        import json

        self.root, self.branch = Path(root), branch
        intake = self.root / 'source-intake/navier-stokes/20260911'
        self.source_path = self.root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz')
        self.saved_path = intake / 'annular-canonical-inverse-boundary-attempt01' / ('N16_' + branch + '_outer_clock.npz')
        self.parameter_path = self.root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        source = load_archive(self.source_path)
        self.saved = load_archive(self.saved_path)
        self.basis = MixedActionBasis(source['basis_radii'])
        basis, count = self.basis, self.basis.radii.size
        configuration, momenta = source['original_configuration'], source['original_momenta']
        packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(self.parameter_path.read_text())['parameters'].items()}
        self.links = MetricLinkQuadrature(basis)
        self.check_links = MetricLinkQuadrature(basis, order=12)
        self.system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], self.links)
        self.model = InverseBoundaryInitialData(self.system, packed, configuration, branch != 'GR', self.saved['boundary_velocity'].copy(), normalize_clock=True)
        self.model.pi_coeff_seed = self.saved['pi_coefficients'].copy()
        self.model.set_state(self.saved['state'])
        self.original = OriginalFrames(self.model)
        self.knots = self.original.knots
        self.points, self.weights = self.quadrature(12)
        self.check_points, self.check_weights = self.quadrature(16)
        self.surfaces = {'quad': self.points, 'check': self.check_points, 'nodes': basis.radii, 'links': self.links.points, 'links_check': self.check_links.points}
        self.old_frames = {phase: {} for phase in ['mass', 'scalar']}
        self.reservoir = {}
        for surface, points in self.surfaces.items():
            maps = self.original.evaluate(points)
            for phase in self.old_frames:
                self.old_frames[phase][surface] = maps[phase]
            value, gradient = bubbles(self.knots, points, 4)
            self.reservoir[surface] = {'q': value, 'qr': gradient}
        self.reference_path = intake / 'annular-canonical-gr-boundary-reference-attempt01/constructed_GR_first_jet.npz'
        self.reference = ConstructedGRFields(basis, load_archive(self.reference_path), self.system.outer_clock) if branch == 'GR' else None

    def quadrature(self, order):
        nodes, weights = numerical.polynomial.legendre.leggauss(order)
        halfwidth = numerical.diff(self.knots) / 2
        return ((self.knots[:-1] + self.knots[1:])[:, None] / 2 + halfwidth[:, None] * nodes).ravel(), (halfwidth[:, None] * weights).ravel()

    def build(self, saved=None):
        selected = self.saved if saved is None else saved
        physical = self.reference if self.branch == 'GR' else SavedCanonicalFields(self.model, selected)
        data = {}
        families = {phase: {} for phase in self.old_frames}
        for surface, points in self.surfaces.items():
            eta, eta_r = linear_value_gradient(self.basis.radii, points)
            data[surface] = physical.evaluate(points)
            data[surface].update({'R': points, 'eta': eta, 'eta_r': eta_r})
            rates = local_rate_families(data[surface], points, eta, eta_r)
            for phase in families:
                families[phase][surface] = {kind: rates[phase + '_' + kind] for kind in ['q', 'qr', 'p']}
        frames, diagnostics = {}, {}
        for phase in self.old_frames:
            frames[phase], diagnostics[phase] = complete_phase(self.old_frames[phase], families[phase], self.reservoir, self.weights)
        return data, frames, diagnostics
