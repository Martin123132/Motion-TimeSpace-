import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import lu_factor, lu_solve
from scipy.sparse.linalg import LinearOperator, gmres

from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution, PolarGeometry, LayerCurrent, ChebyshevRule
from annular_live_exterior_response_20260913 import LiveExteriorResponse, TimeFit


class ProtocolGeometry(PolarGeometry):
    def __init__(self, system, time, state, parameter):
        self.parameter = parameter
        super().__init__(system, time, np.asarray(state, dtype=np.result_type(state, parameter)))

    def scalar(self, offsets):
        data = super().scalar(offsets)
        theta = data['theta']
        data['source_velocity'] = data['source_velocity']+self.parameter*theta**2/2
        data['chi'][:, -1] += self.parameter*theta**3/6
        data['A'] = data['chi'] @ self.system.factors.T
        data['potential'] = data['R']**2*(data['A']**2 @ self.system.sampling)/(2*self.system.spacing)
        return data


class ProtocolEvolution(HorizontalEvolution):
    def __init__(self, base):
        self.__dict__.update(base.__dict__.copy())
        self.initial_state = base.initial_state.copy()

    def evaluate(self, time, state):
        return self.evaluate_protocol(time, state, 0.)

    def evaluate_protocol(self, time, state, parameter):
        geometry = ProtocolGeometry(self, time, state, parameter)
        current = LayerCurrent(self, lambda offsets:geometry.layer(offsets)['pair_current'])
        data = geometry.layer(self.grid.offsets)
        mass_rate = -self.coupling*data['U'][:, -1]*current.evaluate(data['R'][:, -1])/data['N'][:, -1]
        acceleration = self.proper_acceleration+parameter*data['theta']
        momentum_rate = data['R'][:, -1]**2*acceleration*data['N'][:, -1]/data['U'][:, -1]
        momentum_rate += data['R'][:, -1]*data['source_velocity']*mass_rate/data['U'][:, -1]**3
        force = self.node_weights[-1]*momentum_rate-data['Gchi'][:, -1]
        energy_rate = -force*data['source_velocity']
        values = np.column_stack([data['q'][:, :-1], data['Gchi'][:, :-1]/self.node_weights[:-1], data['N'][:, -1], energy_rate])
        inner_rate = geometry.metric(np.array([self.radii[0]]))['N'][0]
        return {'geometry':geometry, 'current':current, 'data':data, 'source_p_rate':momentum_rate,
                'source_force':force, 'energy_rate':energy_rate, 'rhs':self.pack(values, inner_rate), 'parameter':parameter}

    def source_at(self, evaluation, offsets):
        data = evaluation['geometry'].layer(offsets)
        mass_rate = self.mass_flux(evaluation, data['R'][:, -1])
        acceleration = self.proper_acceleration+evaluation['parameter']*data['theta']
        momentum_rate = data['R'][:, -1]**2*acceleration*data['N'][:, -1]/data['U'][:, -1]
        momentum_rate += data['R'][:, -1]*data['source_velocity']*mass_rate/data['U'][:, -1]**3
        return data, self.node_weights[-1]*momentum_rate-data['Gchi'][:, -1]

    def integrate_protocol(self, parameter, duration=.004, divisor=8):
        solution = solve_ivp(lambda time,state:self.evaluate_protocol(time,state,parameter)['rhs'],
                             (0.,duration), self.initial_state, method='DOP853', rtol=2e-12, atol=2e-14,
                             max_step=duration/divisor, dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution


class JointSchurResponse:
    def __init__(self, system, samples, duration=.004, stride=1, full_exterior_columns=None, progress=None):
        self.system = system
        self.response = LiveExteriorResponse(system, duration)
        self.duration = duration
        self.times = samples['times'][::stride]
        self.states = samples['reference_states'].T[::stride]
        self.exterior = self.response.exterior
        self.retained = self.response.retained
        self.count = len(self.times)
        self.size = len(system.initial_state)
        self.exterior_size = len(self.exterior)
        self.retained_size = int(self.retained.sum())
        self.integration = ChebyshevRule(self.count-1).integration*duration/2
        columns = []
        forcing = []
        for index, (time, state) in enumerate(zip(self.times, self.states)):
            if full_exterior_columns is None:
                block = np.empty((self.size,self.exterior_size))
                for column, entry in enumerate(self.exterior):
                    direction = np.zeros(self.size)
                    direction[entry] = 1.
                    block[:,column] = self.jvp(time,state,direction)
                columns.append(block)
            forcing.append(system.evaluate_protocol(time,state,1j*1e-20)['rhs'].imag/1e-20)
            if progress:
                progress(index+1,self.count)
        self.columns = np.stack(columns) if full_exterior_columns is None else full_exterior_columns[::stride].copy()
        self.forcing = np.stack(forcing)
        self.Aee = self.columns[:,self.exterior,:]
        self.Axe = self.columns[:,self.retained,:]
        matrix = np.eye(self.count*self.exterior_size)-np.einsum('jk,kab->jakb',self.integration,self.Aee).reshape(self.count*self.exterior_size,-1)
        self.exterior_matrix = matrix
        self.exterior_lu = lu_factor(matrix)
        self.linear_solves = []

    def jvp(self, time, state, direction):
        return self.system.evaluate(time,state+1j*1e-20*direction)['rhs'].imag/1e-20

    def exterior_solve(self, values):
        return lu_solve(self.exterior_lu,values.ravel()).reshape(self.count,self.exterior_size)

    def retained_action(self, retained):
        values = np.zeros((self.count,self.size))
        values[:,self.retained] = retained
        return np.stack([self.jvp(time,state,direction) for time,state,direction in zip(self.times,self.states,values)])

    def solve(self, right, coupled=True):
        exterior_constant = self.exterior_solve(right[:,self.exterior])
        rhs = right[:,self.retained].copy()
        if coupled:
            rhs += self.integration @ np.einsum('tia,ta->ti',self.Axe,exterior_constant)
        history = []

        def action(flattened):
            retained = flattened.reshape(self.count,self.retained_size)
            differential = self.retained_action(retained)
            rate = differential[:,self.retained]
            if coupled:
                exterior = self.exterior_solve(self.integration @ differential[:,self.exterior])
                rate = rate+np.einsum('tia,ta->ti',self.Axe,exterior)
            return (retained-self.integration @ rate).ravel()

        operator = LinearOperator((rhs.size,rhs.size),matvec=action,dtype=np.float64)
        retained,info = gmres(operator,rhs.ravel(),rtol=2e-11,atol=2e-15,restart=30,maxiter=5,
                             callback=lambda residual:history.append(float(residual)),callback_type='pr_norm')
        if info != 0:
            raise RuntimeError('Retained Schur solve failed: '+str(info))
        retained = retained.reshape(self.count,self.retained_size)
        differential = self.retained_action(retained)
        exterior = self.exterior_solve(right[:,self.exterior]+self.integration @ differential[:,self.exterior])
        result = np.empty((self.count,self.size))
        result[:,self.retained] = retained
        result[:,self.exterior] = exterior
        residual = float(abs(action(retained.ravel())-rhs.ravel()).max())
        record = {'coupled':coupled,'iterations':len(history),'schur_residual':residual,'gmres_history':history}
        self.linear_solves.append(record)
        return result,record

    def linear_response(self, coupled=True):
        result,record = self.solve(self.integration @ self.forcing,coupled=coupled)
        if coupled:
            rates = np.stack([self.jvp(time,state,direction) for time,state,direction in zip(self.times,self.states,result)])+self.forcing
            record['full_collocation_residual'] = float(abs(result-self.integration @ rates).max())
        return result,record

    def nonlinear_response(self, parameter, tangent, max_iterations=5):
        states = self.states+parameter*tangent
        history = []
        for iteration in range(max_iterations):
            rates = np.stack([self.system.evaluate_protocol(time,state,parameter)['rhs'] for time,state in zip(self.times,states)])
            residual = states-self.system.initial_state-self.integration @ rates
            error = float(abs(residual).max())
            history.append({'iteration':iteration,'nonlinear_collocation_residual':error})
            if error<5e-13 and iteration>0:
                return states,history
            correction,record = self.solve(-residual)
            history[-1]['correction_max'] = float(abs(correction).max())
            history[-1]['linear_iterations'] = record['iterations']
            states += correction
        raise RuntimeError('Nonlinear joint closure did not converge: '+repr(history))

    def output_tangent(self, tangent):
        return np.stack([self.response.outputs(self.system.evaluate_protocol(time,state+1j*1e-20*direction,1j*1e-20)).imag/1e-20
                         for time,state,direction in zip(self.times,self.states,tangent)])

