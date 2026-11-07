from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_position_precision_20260929 import NativePrecision
from annular_physical_native_kernel_20260928 import decimals
from annular_position_reaction_20260929 import second_radial
from annular_old_field_reaction_20260929 import coefficient_data
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal
import numpy as np


class TangentPrecisionRepair(NativePrecision):
    def packet(self, label, mode='decimal_tangents'):
        if mode != 'decimal_tangents':
            return super().packet(label, mode)
        data = physical_data(self.native, self.loads, self.action, float(label))
        cardinal = decimals(data['cardinal'])
        field_change = cardinal @ self.decimal_fields
        edge_change = cardinal @ self.decimal_edges + data['displacement'] * sum(cardinal * self.decimal_source, Decimal(0))
        radius = np.asarray(data['edges'][self.native.native_edges], float)
        movement = np.asarray(edge_change[self.native.native_edges], float)
        values, radial = self.action.solver.values(self.action.solution, radius)
        second = second_radial(self.action.solver, self.action.solution, radius)
        variation, variation_r = self.position.at(radius)
        unused, beta, unused2, beta_r = coefficient_data(radius + 1e-25j * movement,
            values + 1e-25j * (variation + radial * movement),
            radial + 1e-25j * (variation_r + second * movement))
        data['cardinal'] = cardinal
        return data, field_change, edge_change, decimals(beta.imag / 1e-25), decimals(beta_r.imag / 1e-25)


def repair_engine(engine):
    return TangentPrecisionRepair(engine.native, engine.loads, engine.action, engine.field_direction,
        engine.source_direction, engine.edge_vertices, engine.position)
