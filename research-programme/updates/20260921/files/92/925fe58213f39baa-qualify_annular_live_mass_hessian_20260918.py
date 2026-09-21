from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_radial_response_20260918 import SnapshotLoads, integration_nodes
from annular_live_radial_response_v2_20260918 import RadialResponse
import hashlib
import json
import numpy as np


class CanonicalDirectionLoads:
    def __init__(self, base, field_scale, momentum_scale, parameter=0.):
        self.__dict__.update(base.__dict__)
        self.base, self.field_scale, self.momentum_scale, self.parameter = base, field_scale, momentum_scale, parameter

    def shape(self, radius):
        return self.field_scale*(1+.2*np.sin(3*np.asarray(radius)))

    def energy(self, radius):
        return self.base.energy(radius)*(1+self.parameter*self.shape(radius))**2

    def source(self, radius, shift=0.):
        density, momentum = self.base.source(radius, shift)
        return density, momentum+self.parameter*self.momentum_scale

    def directions(self, radius):
        radius = np.asarray(radius)
        return 2*self.base.energy(radius)*self.shape(radius), np.zeros_like(radius), self.momentum_scale*np.ones_like(radius)


def main():
    evidence = EvidenceRun('annular-live-mass-hessian-attempt01', __file__)
    try:
        snapshot = evidence.root/'source-intake/navier-stokes/20260914/annular-live-continuum-snapshot-attempt01/degree64.npz'
        status_path = snapshot.parent/'status.json'
        status = json.loads(status_path.read_text())
        evidence.check('source_snapshot_hash', status['state'] == 'complete' and hashlib.sha256(snapshot.read_bytes()).hexdigest()
            == status['outputs'][str(snapshot.relative_to(evidence.root))])
        evidence.own(snapshot)
        evidence.own(status_path)
        system = BarycentricLiveContinuum(64, 4, 10, radial_spacing=.1, label_order=8)
        with np.load(snapshot) as saved:
            loads = SnapshotLoads(system, system.solve(saved['state']), 24)
        radius_min, metric_floor, source = loads.lower, .5, system.source_mass
        coupling, energy_cap, momentum_cap, density_L1 = system.coupling, .05, .005, 1.
        wave_norm = np.sqrt(2*energy_cap)
        source_input = momentum_cap/source*np.sqrt(density_L1)
        log_eta_cap = coupling*(2*energy_cap/radius_min+density_L1*(source**2+2*momentum_cap**2)/(radius_min*np.sqrt(metric_floor)*source))
        eta_min = np.exp(-log_eta_cap)
        q_mm_cap = source/(radius_min**2*metric_floor**1.5)
        q_mp_cap = momentum_cap*(3*source**2+2*momentum_cap**2)/(radius_min*source**3)
        positive = np.diag([metric_floor*eta_min, eta_min*metric_floor**1.5*source**2/(source**2+momentum_cap**2)**1.5])
        binding = np.array([[4*coupling*wave_norm**2/radius_min+q_mm_cap*density_L1*coupling**2*wave_norm**2,
            2*coupling*wave_norm*source_input/radius_min+q_mm_cap*density_L1*coupling**2*wave_norm*source_input
                +q_mp_cap*np.sqrt(density_L1)*coupling*wave_norm],
            [0., q_mm_cap*density_L1*coupling**2*source_input**2+2*q_mp_cap*np.sqrt(density_L1)*coupling*source_input]])
        binding[1, 0] = binding[0, 1]
        lower_matrix = positive-binding
        lower_eigenvalue = float(np.linalg.eigvalsh(lower_matrix)[0])
        evidence.check('analytic_joint_fixed_position_coercivity', lower_eigenvalue > 0,
            dict(positive=positive.tolist(), binding= binding.tolist(), lower_matrix=lower_matrix.tolist(),
                lower_eigenvalue=lower_eigenvalue, eta_min=eta_min, energy_cap=energy_cap, momentum_cap=momentum_cap))
        evidence.report.update(fixed_source_position_and_density=True, nonzero_source_momentum_retained=True,
            constrained_mass_Hessian_not_full_moving_canonical_chart=True,
            no_uniform_third_source_momentum_variation_claim=True, no_forward_evolution=True,
            original_action_unchanged=True, old_force_gates_unchanged=True, subagents_used=False, github_action=False,
            analytic_lower_matrix=lower_matrix.tolist(), analytic_lower_eigenvalue=lower_eigenvalue)
        radius, measure = integration_nodes(loads.nodes, order=10)
        step = .0002
        for field_scale, momentum_scale in [(1., 0.), (0., 1.), (1., 1.)]:
            direction = CanonicalDirectionLoads(loads, field_scale, momentum_scale)
            solution = RadialResponse(direction, tangent=True, tight=True)
            data = solution.sample(radius)
            field_second_density = 2*loads.energy(radius)*direction.shape(radius)**2
            field_norm_squared = float(measure @ field_second_density)
            momentum_norm_squared = float(measure @ data['density'])*momentum_scale**2
            loading = data['loading']
            q_mm = -source**4/(radius**2*loading**3)
            q_mp = -data['metric']**2*data['momentum']*(3*source**2+2*data['metric']*data['momentum']**2)/(radius*loading**3)
            q_pp = data['metric']**3*source**2/loading**3
            field_term = float(measure @ (data['speed']*field_second_density))
            source_term = float(measure @ (data['eta']*data['density']*q_pp*momentum_scale**2))
            binding_term = float(measure @ (data['eta']*(-4*data['mass_first']*data['energy_direction']/radius
                +data['density']*(q_mm*data['mass_first']**2+2*q_mp*data['mass_first']*momentum_scale))))
            hessian = field_term+source_term+binding_term
            radial_hessian = solution.final[5]/coupling+field_term
            evidence.check(str((field_scale, momentum_scale))+'_second_variation_adjoint_identity',
                abs(hessian-radial_hessian) < 5e-9, dict(adjoint=hessian, radial=radial_hessian))
            norms = np.sqrt([field_norm_squared, momentum_norm_squared])
            lower = float(norms @ lower_matrix @ norms)
            evidence.check(str((field_scale, momentum_scale))+'_analytic_lower_bound', hessian >= lower-2e-10,
                dict(hessian=hessian, lower=lower, norm_squared=norms.tolist()))
            finite = {}
            for factor in [-2, -1, 1, 2]:
                perturbed = CanonicalDirectionLoads(loads, field_scale, momentum_scale, parameter=factor*step)
                finite[factor] = RadialResponse(perturbed, tight=True).hamiltonian
            difference = (-finite[2]+16*finite[1]-30*solution.hamiltonian+16*finite[-1]-finite[-2])/(12*step**2)
            row = dict(field_scale=field_scale, momentum_scale=momentum_scale, field_term=field_term,
                source_kinetic_term=source_term, gravitational_binding_term=binding_term, hessian=hessian,
                finite_difference=difference, error=abs(hessian-difference), lower_bound=lower)
            evidence.report['cases'].append(row)
            evidence.check(str((field_scale, momentum_scale))+'_finite_canonical_loading_second_difference', row['error'] < 3e-5, row)
            print(json.dumps(row), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
