import json
import numpy as np
from scipy.integrate import solve_ivp

from annular_common_source_history_20260913 import ExteriorModePreparation, exterior_modes
from annular_clock_reservoir_coupling_20260913 import ProperClockDrive
from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution, ChebyshevRule
from annular_finite_width_bulk_current_20260913 import shape_weight


OUTPUT_NAMES = ['inner_current', 'inner_mass', 'inner_U_over_N', 'inner_mass_rate', 'source_energy', 'source_power', 'total_mass']
PROBE_NAMES = ['exterior_momentum', 'adjacent_interior_momentum', 'existing_source_energy']


def load_prepared_system(root, branch, degree=16):
    intake = root/'source-intake/navier-stokes/20260913'
    old = {row['label']:row for row in json.loads((intake/'annular-clock-reservoir-coupling-attempt01/status.json').read_text())['cases']}
    row = next(row for row in json.loads((intake/'annular-common-source-history-attempt01/status.json').read_text())['cases'] if row['branch']==branch and row['case']==0)
    with np.load(root/'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03'/(branch+'_source_snapshot.npz'),allow_pickle=False) as archive:
        source = {key:archive[key].copy() for key in archive.files}
    with np.load(intake/'annular-finite-width-boundary-cut-attempt01'/(branch+'_0_prepared_collar.npz'),allow_pickle=False) as archive:
        prepared = {key:archive[key].copy() for key in archive.files}
    with np.load(root/'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'/('canonical_N16_'+branch+'_sample0.npz'),allow_pickle=False) as archive:
        clock = archive['affine_clock'].copy()
        acceleration = float(archive['endpoint_acceleration'][-1])
    preparation = ExteriorModePreparation(source,branch!='GR',prepared['kinetic_seed'],float(prepared['outer_clock']),prepared['drive'],row['width'],row['shape'],reservoir_energy=row['reservoir_energy'],base_coefficients=old[row['label']]['coefficients'])
    model = preparation.build(row['exterior_amplitudes'])
    driver = ProperClockDrive(model,float(clock[1]),acceleration,degree=64)
    return HorizontalEvolution(model,driver,clock,degree=degree), row


class TimeFit:
    def __init__(self, values, duration):
        self.duration = duration
        rule = ChebyshevRule(len(values)-1)
        self.coefficients = np.tensordot(rule.inverse, values, axes=(1,0))

    def __call__(self, time):
        return np.polynomial.chebyshev.chebval(2*time/self.duration-1, self.coefficients)


class LiveExteriorResponse:
    def __init__(self, system, duration=.004):
        self.system, self.duration = system, duration
        self.state_size = len(system.initial_state)
        self.free = len(system.radii)-1
        indices = np.arange(self.state_size-1).reshape(len(system.grid.offsets), 2*len(system.radii))
        negative = system.grid.offsets < 0
        self.exterior = np.concatenate([indices[negative,0], indices[negative,self.free]])
        self.retained = np.ones(self.state_size,dtype=bool)
        self.retained[self.exterior] = False
        self.exterior_size = len(self.exterior)
        directions = []
        values = np.zeros_like(indices,dtype=float)
        values[:,self.free] = exterior_modes(system.grid.offsets)[:,0]
        directions.append(system.pack(values,0.))
        values = np.zeros_like(values)
        values[:,self.free+1] = 1-4*system.grid.offsets**2
        directions.append(system.pack(values,0.))
        values = np.zeros_like(values)
        values[:,-1] = .001
        directions.append(system.pack(values,0.))
        self.directions = np.column_stack(directions)
        points, weights = np.polynomial.legendre.leggauss(24)
        self.offsets = np.concatenate([-.25+.25*points, .25+.25*points])
        self.weights = np.concatenate([.25*weights,.25*weights])*shape_weight(self.offsets,system.shape)

    def outputs(self, evaluation):
        inner = evaluation['geometry'].metric(np.array([self.system.radii[0]]))
        current = evaluation['current'].evaluate(np.array([self.system.radii[0]]))[0]
        ratio = inner['U'][0]/inner['N'][0]
        source, force = self.system.source_at(evaluation,self.offsets)
        energy = self.weights @ source['energy']
        power = self.weights @ (-force*source['source_velocity'])
        total_mass = evaluation['geometry'].metric(np.array([self.system.radii[-1]+self.system.width/2]))['mu'][0]
        return np.array([current,inner['mu'][0],ratio,-self.system.coupling*ratio*current,energy,power,total_mass])

    def differential(self, time, state, direction, step=1e-20):
        evaluation = self.system.evaluate(time,state+1j*step*direction)
        return evaluation['rhs'].imag/step, self.outputs(evaluation).imag/step

    def integrate(self, initial=None, divisor=4):
        initial = self.system.initial_state if initial is None else initial
        solution = solve_ivp(self.system.rhs,(0.,self.duration),initial,method='DOP853',rtol=2e-11,atol=2e-13,max_step=self.duration/divisor,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def integrate_tangents(self, reference):
        def equation(time, flattened):
            directions = flattened.reshape(self.directions.shape)
            return np.column_stack([self.differential(time,reference.sol(time),direction)[0] for direction in directions.T]).ravel()

        solution = solve_ivp(equation,(0.,self.duration),self.directions.ravel(),method='DOP853',rtol=2e-11,atol=2e-13,max_step=self.duration/4,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def reduced_replay(self, reference, times):
        def equation(time, exterior):
            state = reference.sol(time)
            state[self.exterior] = exterior
            return self.system.rhs(time,state)[self.exterior]

        solution = solve_ivp(equation,(0.,self.duration),reference.sol(0.)[self.exterior],method='DOP853',rtol=2e-11,atol=2e-13,max_step=self.duration/4,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        errors, reconstructed_outputs = [], []
        for time in times:
            full = reference.sol(time)
            reconstructed = full.copy()
            reconstructed[self.exterior] = solution.sol(time)
            original = self.system.evaluate(time,full)
            rebuilt = self.system.evaluate(time,reconstructed)
            observed = self.outputs(rebuilt)
            reconstructed_outputs.append(observed)
            errors.append({'time':float(time),'exterior_error':float(abs(full[self.exterior]-reconstructed[self.exterior]).max()),
                           'output_error':float(abs(observed-self.outputs(original)).max()),
                           'retained_equation_discrepancy':float(abs(original['rhs'][self.retained]-rebuilt['rhs'][self.retained]).max())})
        return errors,np.stack(reconstructed_outputs)

    def sample_operator(self, reference, tangents, degree=16, progress=None):
        times=self.duration*(ChebyshevRule(degree).points+1)/2
        matrices, output_blocks, drives, direct, full, baseline, tangent_states = [], [], [], [], [], [], []
        for index,time in enumerate(times):
            state=reference.sol(time)
            tangent=tangents.sol(time).reshape(self.directions.shape)
            matrix=np.empty((self.exterior_size,self.exterior_size))
            output_block=np.empty((len(OUTPUT_NAMES),self.exterior_size))
            for column,entry in enumerate(self.exterior):
                direction=np.zeros(self.state_size)
                direction[entry]=1.
                differential,observation=self.differential(time,state,direction)
                matrix[:,column]=differential[self.exterior]
                output_block[:,column]=observation
            driving,instant,complete=[],[],[]
            for direction in tangent.T:
                retained=direction.copy()
                retained[self.exterior]=0.
                differential,observation=self.differential(time,state,retained)
                driving.append(differential[self.exterior])
                instant.append(observation)
                complete.append(self.differential(time,state,direction)[1])
            matrices.append(matrix)
            output_blocks.append(output_block)
            drives.append(np.column_stack(driving))
            direct.append(np.column_stack(instant))
            full.append(np.column_stack(complete))
            baseline.append(self.outputs(self.system.evaluate(time,state)))
            tangent_states.append(tangent)
            if progress:
                progress(index+1,len(times))
        return {'times':times,'Aee':np.stack(matrices),'output_e':np.stack(output_blocks),'retained_drive':np.stack(drives),
                'retained_direct':np.stack(direct),'full_output_tangent':np.stack(full),'baseline_outputs':np.stack(baseline),
                'full_tangent_states':np.stack(tangent_states)}

    def memory_replay(self, samples, stride=1, frozen=False):
        fits={key:TimeFit(samples[key][::stride],self.duration) for key in ['Aee','output_e','retained_drive','retained_direct']}
        columns=self.exterior_size+self.directions.shape[1]
        initial=np.column_stack([np.eye(self.exterior_size),np.zeros((self.exterior_size,self.directions.shape[1]))])

        def equation(time,flattened):
            matrix=fits['Aee'](0. if frozen else time)
            values=flattened.reshape(self.exterior_size,columns)
            derivative=matrix @ values
            derivative[:,self.exterior_size:] += fits['retained_drive'](time)
            return derivative.ravel()

        solution=solve_ivp(equation,(0.,self.duration),initial.ravel(),method='DOP853',rtol=2e-12,atol=2e-14,max_step=self.duration/8,dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        predicted,homogeneous,driven,exteriors,propagators=[],[],[],[],[]
        for time in samples['times']:
            values=solution.sol(time).reshape(self.exterior_size,columns)
            propagator=values[:,:self.exterior_size]
            initial_part=propagator @ self.directions[self.exterior]
            driven_part=values[:,self.exterior_size:]
            output=fits['output_e'](0. if frozen else time)
            direct=fits['retained_direct'](time)
            predicted.append(direct+output @ (initial_part+driven_part))
            homogeneous.append(output @ initial_part)
            driven.append(output @ driven_part)
            exteriors.append(initial_part+driven_part)
            propagators.append(propagator)
        return {'predicted':np.stack(predicted),'initial_contribution':np.stack(homogeneous),'memory_contribution':np.stack(driven),
                'exterior_tangents':np.stack(exteriors),'propagators':np.stack(propagators),'fits':fits,'solution':solution}

    def terminal_duhamel(self, memory, order=12):
        points,weights=np.polynomial.legendre.leggauss(order)
        result=np.zeros((self.exterior_size,self.directions.shape[1]))
        transitions=[]
        for time,weight in zip(self.duration*(points+1)/2,self.duration*weights/2):
            def equation(current,flattened):
                return (memory['fits']['Aee'](current) @ flattened.reshape(self.exterior_size,self.exterior_size)).ravel()

            solution=solve_ivp(equation,(time,self.duration),np.eye(self.exterior_size).ravel(),method='DOP853',rtol=2e-12,atol=2e-14,max_step=self.duration/8)
            if not solution.success:
                raise RuntimeError(solution.message)
            transition=solution.y[:,-1].reshape(self.exterior_size,self.exterior_size)
            result += weight*(transition @ memory['fits']['retained_drive'](time))
            transitions.append(transition)
        return result,np.stack(transitions)

    def balances(self, reference, tangents=None, order=12):
        points,weights=np.polynomial.legendre.leggauss(order)
        integral=np.zeros(2)
        tangent_integral=np.zeros((2,self.directions.shape[1]))
        missing_metric=np.zeros(self.directions.shape[1])
        for time,weight in zip(self.duration*(points+1)/2,self.duration*weights/2):
            state=reference.sol(time)
            output=self.outputs(self.system.evaluate(time,state))
            integral += weight*np.array([-self.system.coupling*output[2]*output[0],output[5]])
            if tangents is not None:
                directions=tangents.sol(time).reshape(self.directions.shape)
                for index,direction in enumerate(directions.T):
                    variation=self.differential(time,state,direction)[1]
                    tangent_integral[:,index] += weight*np.array([-self.system.coupling*(output[2]*variation[0]+output[0]*variation[2]),variation[5]])
                    missing_metric[index] += -weight*self.system.coupling*output[0]*variation[2]
        first=self.outputs(self.system.evaluate(0.,reference.sol(0.)))
        last=self.outputs(self.system.evaluate(self.duration,reference.sol(self.duration)))
        result={'mass_balance_error':float(abs(last[1]-first[1]-integral[0])),
                'source_energy_balance_error':float(abs(last[4]-first[4]-integral[1])),
                'inner_mass_change':float(last[1]-first[1]),'source_energy_change':float(last[4]-first[4]),
                'total_mass_change':float(last[6]-first[6])}
        if tangents is not None:
            endpoint=[]
            for time in [0.,self.duration]:
                variations=tangents.sol(time).reshape(self.directions.shape)
                endpoint.append(np.column_stack([self.differential(time,reference.sol(time),direction)[1][[1,4]] for direction in variations.T]))
            errors=endpoint[1]-endpoint[0]-tangent_integral
            result.update({'tangent_balance_errors':errors.tolist(),'omitted_metric_weight_contributions':missing_metric.tolist()})
        return result
