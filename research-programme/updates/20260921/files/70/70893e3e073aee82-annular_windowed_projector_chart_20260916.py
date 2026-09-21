import numpy as np
from scipy.linalg import eigh
from annular_boundary_response_20260916 import field_matrices
from annular_moving_spectral_frame_20260916 import spectral_clusters
from annular_anchored_projector_chart_20260916 import AnchoredProjectorChart


class WindowedProjectorChart(AnchoredProjectorChart):
    def __init__(self, system, retained, cluster_gap=1e-3, gap_floor=1e-4, half_width=.001, survey_count=201):
        if half_width <= 0 or survey_count < 3:
            raise ValueError('A positive window and at least three survey positions are required.')
        self.window = (system.anchor-half_width, system.anchor+half_width)
        positions = np.linspace(*self.window, survey_count)
        parent = np.arange(system.count)

        def representative(index):
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        minimum_adjacent_gap = 1.
        for position in positions:
            matrices = field_matrices(system,float(position))
            values = eigh(matrices['stiffness'].toarray(),matrices['mass'].toarray(),eigvals_only=True)
            scale = np.maximum(1.,np.maximum(abs(values[1:]),abs(values[:-1])))
            minimum_adjacent_gap = min(minimum_adjacent_gap,float(np.min(np.diff(values)/scale)))
            for cluster in spectral_clusters(values,cluster_gap):
                for index in cluster[1:]:
                    parent[representative(index)] = representative(cluster[0])
        roots = {representative(index) for index in retained}
        completed = [index for index in range(system.count) if representative(index) in roots]
        super().__init__(system,completed,cluster_gap,gap_floor)
        self.survey = dict(window=list(self.window),samples=survey_count,cluster_gap=cluster_gap,
            requested_count=len(retained),completed_count=self.count,
            added_indices=sorted(set(self.retained)-set(retained)),retained_indices=self.retained,
            minimum_adjacent_gap=minimum_adjacent_gap,continuous_gap_certificate=False,
            rule='Transitive union of entire spectral clusters over a prespecified position survey; no trajectory fitting.')

    def at(self, position):
        if not self.window[0] <= np.real(position) <= self.window[1]:
            raise ValueError('Source left surveyed chart window; stop rather than extrapolate.')
        return super().at(position)
