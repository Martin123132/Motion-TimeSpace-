import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, quad

from annular_compatible_h_evolution_20260914 import CompatibleEvolution
from annular_finite_width_bulk_current_20260913 import shape_weight


class EvidenceRun:
    def __init__(self, label, source):
        self.root = Path(__file__).resolve().parents[1]
        self.output = self.root/'source-intake/navier-stokes/20260914'/label
        self.output.mkdir(exist_ok=False)
        self.report = dict(state='running',checks=[],cases=[],inputs={},outputs={},
                           conditional_spherical_bulk_equations_identified=True,
                           evolving_reference_continuum_convergence_proven=False,
                           complete_parent_source_action_derived=False,
                           full_GR_limit_proven=False,valid_for_physics_claim=False)
        self.own(Path(source))
        snapshot = self.output/('executed-'+Path(source).name)
        snapshot.write_bytes(Path(source).read_bytes())
        self.own(snapshot,'outputs')
        self.save()

    def own(self,path,table='inputs'):
        self.report[table][str(path.relative_to(self.root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save(self):
        (self.output/'status.json').write_text(json.dumps(self.report,indent=2)+'\n',encoding='utf-8')

    def check(self,name,passed,detail=None):
        self.report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        self.save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def complete(self):
        for module in list(sys.modules.values()):
            filename = getattr(module,'__file__',None)
            if filename:
                path = Path(filename).resolve()
                if path.parent==self.root/'scripts' and path.suffix=='.py':
                    self.own(path)
        self.report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat())
        self.save()
        print(json.dumps(dict(state='complete',checks=len(self.report['checks']),cases=self.report['cases'])),flush=True)

    def fail(self,error):
        self.report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        self.save()


def bump_and_gradient(radius):
    radius = np.asarray(radius)
    coordinate = (radius-5.5)/.3
    selected = abs(coordinate)<1
    bump,gradient = np.zeros_like(radius),np.zeros_like(radius)
    denominator = 1-coordinate[selected]**2
    bump[selected] = np.exp(1-1/denominator)
    gradient[selected] = -2*coordinate[selected]*bump[selected]/(.3*denominator**2)
    return bump,gradient


def continuum_density(radius):
    bump,gradient = bump_and_gradient(radius)
    return .5*np.asarray(radius)**2*((.02*gradient)**2+(.004*bump)**2)


def thin_shell(mass_minus,radius=6.,coupling=.1,reservoir=.003):
    root_minus = np.sqrt(1-2*mass_minus/radius)
    geometric_proper_mass = coupling*reservoir
    root_plus = root_minus-geometric_proper_mass/radius
    mass_plus = mass_minus+geometric_proper_mass*root_minus-geometric_proper_mass**2/(2*radius)
    shell_lapse = (root_minus+root_plus)/2
    surface_density = reservoir/radius**2
    surface_pressure = surface_density*(1/(root_minus*root_plus)-1)/4
    return dict(U_minus=float(root_minus),U_plus=float(root_plus),m_plus=float(mass_plus),
                N_shell=float(shell_lapse),g_plus=float(shell_lapse/root_plus),
                Sigma=float(surface_density),P=float(surface_pressure))


def continuum_initial(tolerance=2e-12,max_step=.002):
    def rhs(radius,state):
        mass = state[0]
        lapse_density = float(continuum_density(radius))
        geometry = 1-2*mass/radius
        return [.1*geometry*lapse_density,mass/(radius**2*geometry)+.1*lapse_density/radius]
    solution = solve_ivp(rhs,(5.,6.),[.8,0.],method='DOP853',rtol=tolerance,
                         atol=tolerance/20,max_step=max_step,dense_output=True)
    if not solution.success:
        raise RuntimeError(solution.message)
    shell = thin_shell(solution.y[0,-1])
    shift = np.log(shell['N_shell'])-solution.y[1,-1]
    moments = [quad(lambda radius:float(continuum_density(radius))*((radius-5.5)/.5)**power,
                    5.2,5.8,epsabs=2e-13,epsrel=2e-12,limit=150)[0] for power in [0,1,2]]
    return solution,shift,shell,np.array(moments)


def collar_moments(system,geometry,order=24):
    points,weights = np.polynomial.legendre.leggauss(order)
    offsets = np.concatenate([-.25+.25*points,.25+.25*points])
    weights = np.concatenate([.25*weights,.25*weights])*shape_weight(offsets,system.shape)
    data = geometry.scalar(offsets)
    density_per_layer = data['potential']+system.node_weights[None,:]*data['p']**2/(2*data['R']**2)
    moments = [float(weights @ np.sum(density_per_layer*((data['R']-5.5)/.5)**power,axis=1))
               for power in [0,1,2]]
    source_radius = data['R'][:,-1]
    source_fields = geometry.metric(source_radius)
    surface_density = float(weights @ (data['energy']/source_radius**2))
    pressure = float(weights @ (data['energy']*source_fields['mu']/
                                (2*source_radius**3*source_fields['U']**2)))
    return np.array(moments),surface_density,pressure


def initial_case(count,degree,continuum):
    system = CompatibleEvolution(count,False,degree=degree)
    geometry = system.geometry(0.,system.initial_state)
    solution,shift,shell,exact_moments = continuum
    probes = np.linspace(5.,5.95,193)
    metric = geometry.metric(probes)
    exact = solution.sol(probes)
    endpoint_radii = np.array([6-system.width/2,6.,6+system.width/2])
    boundary = geometry.metric(endpoint_radii)
    matched = thin_shell(boundary['mu'][0])
    moments,surface_density,pressure = collar_moments(system,geometry)
    shell_difference = boundary['U'][-1]-boundary['U'][0]
    half_difference = boundary['U'][1]-boundary['U'][0]
    sigma_rule = -system.coupling*.003/6
    shell_error = abs(shell_difference-sigma_rule)
    mass_jump = boundary['mu'][-1]-boundary['mu'][0]
    predicted_jump = matched['m_plus']-boundary['mu'][0]
    result = dict(count=count,degree=degree,h=system.spacing,
                  bulk_mass_error=float(abs(metric['mu']-exact[0]).max()),
                  bulk_log_lapse_error=float(abs(metric['log_N']-exact[1]-shift).max()),
                  weak_energy_moment_error=float(abs(moments-exact_moments).max()),
                  weak_moments=moments.tolist(),
                  shell_U_jump_error=float(shell_error),
                  shell_half_U_jump_error=float(abs(half_difference-sigma_rule/2)),
                  shell_mass_jump=float(mass_jump),
                  shell_mass_jump_error=float(abs(mass_jump-predicted_jump)),
                  shell_lapse_jump=float(abs(boundary['N'][-1]-boundary['N'][0])),
                  midpoint_clock_error=float(abs(boundary['N'][1]-boundary['U'][1])),
                  shell_lapse_prediction_error=float(abs(boundary['N'][1]-matched['N_shell'])),
                  outer_clock=float(boundary['N'][-1]/boundary['U'][-1]),
                  outer_clock_prediction_error=float(abs(boundary['N'][-1]/boundary['U'][-1]-matched['g_plus'])),
                  surface_density=float(surface_density),
                  surface_density_error=float(abs(surface_density-matched['Sigma'])),
                  required_surface_pressure=float(pressure),
                  surface_pressure_error=float(abs(pressure-matched['P'])),
                  no_source_mass_error=float(abs(mass_jump)),
                  midpoint_as_exterior_mass_error=float(abs(boundary['mu'][-1]-boundary['mu'][1])),
                  forced_unit_outer_clock_error=float(abs(boundary['N'][-1]/boundary['U'][-1]-1)),
                  source_scalar_potential=float(abs(geometry.scalar(np.array([0.]))['potential'][0,-1])),
                  collocation_defect=float(geometry.collocation_defect),
                  minimum_F=float(geometry.minimum_F),
                  finite_width_boundary={name:values.tolist() for name,values in boundary.items()},
                  matched_thin_shell=matched)
    return result


def independent_radial_collars(count,degree=16):
    system = CompatibleEvolution(count,False,degree=degree)
    data_geometry = system.geometry(0.,system.initial_state)
    seed = np.array([.8,0.])
    pieces = []
    for piece in data_geometry.pieces:
        lower,upper = piece['lower'],piece['upper']
        if piece['gap']:
            old_mass,old_log = seed
            seed = np.array([old_mass,old_log+.5*np.log((1-2*old_mass/upper)/(1-2*old_mass/lower))])
            continue
        node = int(np.argmin(abs(system.radii-(lower+upper)/2)))
        def rhs(radius,state):
            offset = (radius-system.radii[node])/system.width
            data = data_geometry.scalar(np.array([offset]))
            measure = float(shape_weight(np.array([offset]),system.shape)[0]/system.width)
            density = float(data['potential'][0,node]+system.node_weights[node]*
                            data['p'][0,node]**2/(2*radius**2))*measure
            reservoir = float(data['energy'][0])*measure if node==count-1 else 0.
            geometry = 1-2*state[0]/radius
            return [.1*(geometry*density+np.sqrt(geometry)*reservoir),
                    state[0]/(radius**2*geometry)+.1*density/radius]
        solution = solve_ivp(rhs,(lower,upper),seed,method='DOP853',rtol=2e-12,atol=1e-14,
                             max_step=(upper-lower)/4,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        pieces.append((lower,upper,solution))
        seed = solution.y[:,-1]
    def probe(radius):
        for lower,upper,solution in pieces:
            if lower-1e-13<=radius<=upper+1e-13:
                return solution.sol(radius)
        raise ValueError(radius)
    center = probe(6.)
    normalization = .5*np.log(1-2*center[0]/6)-center[1]
    endpoint_radii = [6-system.width/2,6.,6+system.width/2]
    actual = data_geometry.metric(np.array(endpoint_radii))
    independent = np.array([probe(radius) for radius in endpoint_radii]).T
    return dict(count=count,mass_error=float(abs(actual['mu']-independent[0]).max()),
                log_lapse_error=float(abs(actual['log_N']-independent[1]-normalization).max()))
