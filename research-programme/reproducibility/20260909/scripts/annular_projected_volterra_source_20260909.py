import numpy as numerical

from annular_boundary_preserving_completion_20260909 import project_interior_scalar_and_complete
from annular_volterra_source_completion_20260909 import complete_without_scalar_projection


def complete_projected_volterra(raw, gradient, band, outer_derivative, scalar_weight, spacing, moments=None):
    if raw.shape != (4, gradient.shape[-1]):
        raise ValueError("Expected one coordinate-source vector")
    projected = project_interior_scalar_and_complete(raw[None], gradient, band, outer_derivative, scalar_weight)[0]
    result, diagnostics = complete_without_scalar_projection(projected, gradient, spacing, moments=moments)
    if not numerical.array_equal(result[[0, 1, 3]], projected[[0, 1, 3]]):
        raise ValueError("Mass-only completion changed the projected scalar/lapse source")
    diagnostics["centered_mass_source"] = projected[2]
    return result, diagnostics
