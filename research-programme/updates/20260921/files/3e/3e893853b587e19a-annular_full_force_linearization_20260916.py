import numpy as np
from scipy.linalg import solve_banded
from annular_boundary_response_20260916 import field_matrices
from annular_moving_spectral_curvature_20260916 import analytic_matrix_derivatives
from annular_anchored_projector_chart_20260916 import material_terms


class FullForceLinearization:
    def __init__(self, system):
        self.system = system
        self.count = system.count
        self.last_position = None
        self.last_matrices = None

    def matrices(self, position):
        if self.last_position == position:
            return self.last_matrices
        sparse = field_matrices(self.system,position)
        matrices = {key:sparse[key].toarray() for key in ['mass','transport','transport_square','stiffness']}
        first,second = analytic_matrix_derivatives(self.system,position)
        mass = matrices['mass']
        bands = np.zeros((5,self.count),dtype=mass.dtype)
        for offset in range(-2,3):
            columns = np.arange(max(0,-offset),min(self.count,self.count-offset))
            bands[2+offset,columns] = mass[columns+offset,columns]
        self.last_position = position
        self.last_matrices = matrices,first,second,bands
        return self.last_matrices

    def evaluate(self, state, linearize=False):
        coordinates,rates = np.split(state[:-1],2)
        field,position,velocity,speed = coordinates[:-1],coordinates[-1],rates[:-1],rates[-1]
        matrices,first,second,bands = self.matrices(position)
        mass,transport,square,stiffness = [matrices[key] for key in ['mass','transport','transport_square','stiffness']]
        material = material_terms(self.system,position,speed)
        drift = first['mass']+transport-transport.T
        correction = first['transport']-square
        field_rhs = -speed*drift @ velocity-stiffness @ field-speed**2*correction @ field
        source_rhs = velocity @ (first['mass']/2-transport) @ velocity-2*speed*velocity @ square @ field
        source_rhs -= speed**2*(field @ first['transport_square'] @ field)/2+field @ first['stiffness'] @ field/2
        source_rhs += material['covector']-speed*material['momentum_b']
        cross = transport @ field
        inertia = material['inertia']+field @ square @ field
        solved = solve_banded((2,2),bands,np.column_stack([field_rhs,cross]))
        schur = inertia-cross @ solved[:,1]
        if np.real(schur)<=0:
            raise ValueError('Nonpositive original kinetic Schur complement.')
        source_acceleration = (source_rhs-cross @ solved[:,0])/schur
        field_acceleration = solved[:,0]-solved[:,1]*source_acceleration
        acceleration = np.append(field_acceleration,source_acceleration)
        flow = np.concatenate([rates,acceleration,[material['clock']]])
        force = material['inertia']*source_acceleration+material['momentum_b']*speed
        result = dict(flow=flow,force=force,acceleration=acceleration,schur=schur)
        if not linearize:
            return result
        if np.iscomplexobj(state):
            raise ValueError('Analytic Jacobian qualification uses a real base state.')
        material_b = {key:np.imag(value)/1e-24 for key,value in material_terms(self.system,position+1e-24j,speed).items()}
        material_v = {key:np.imag(value)/1e-24 for key,value in material_terms(self.system,position,speed+1e-24j).items()}
        count,dimension = self.count,len(state)
        source_column,speed_column = count,2*count+1
        right_derivative = np.zeros((count+1,dimension))
        right_derivative[:-1,:count] = -stiffness-speed**2*correction-source_acceleration*transport
        right_derivative[-1,:count] = -2*speed*square @ velocity-speed**2*first['transport_square'] @ field-first['stiffness'] @ field
        right_derivative[-1,:count] -= transport.T @ field_acceleration+2*source_acceleration*square @ field
        right_derivative[:-1,count+1:speed_column] = -speed*drift
        right_derivative[-1,count+1:speed_column] = (first['mass']-transport-transport.T) @ velocity-2*speed*square @ field
        drift_b = second['mass']+first['transport']-first['transport'].T
        correction_b = second['transport']-first['transport_square']
        field_b = -speed*drift_b @ velocity-first['stiffness'] @ field-speed**2*correction_b @ field
        field_b -= first['mass'] @ field_acceleration+first['transport'] @ field*source_acceleration
        source_b = velocity @ (second['mass']/2-first['transport']) @ velocity-2*speed*velocity @ first['transport_square'] @ field
        source_b -= speed**2*(field @ second['transport_square'] @ field)/2+field @ second['stiffness'] @ field/2
        source_b += material_b['covector']-speed*material_b['momentum_b']
        source_b -= (first['transport'] @ field) @ field_acceleration
        source_b -= (material_b['inertia']+field @ first['transport_square'] @ field)*source_acceleration
        right_derivative[:,source_column] = np.append(field_b,source_b)
        field_speed = -drift @ velocity-2*speed*correction @ field
        source_speed = -2*velocity @ square @ field-speed*field @ first['transport_square'] @ field
        source_speed += material_v['covector']-material['momentum_b']-speed*material_v['momentum_b']
        source_speed -= material_v['inertia']*source_acceleration
        right_derivative[:,speed_column] = np.append(field_speed,source_speed)
        field_solved = solve_banded((2,2),bands,right_derivative[:-1])
        source_derivative = (right_derivative[-1]-cross @ field_solved)/schur
        acceleration_derivative = np.vstack([field_solved-solved[:,1,None]*source_derivative[None,:],source_derivative])
        jacobian = np.zeros((dimension,dimension))
        jacobian[:count+1,count+1:2*(count+1)] = np.eye(count+1)
        jacobian[count+1:2*(count+1)] = acceleration_derivative
        jacobian[-1,source_column],jacobian[-1,speed_column] = material_b['clock'],material_v['clock']
        force_gradient = material['inertia']*source_derivative
        force_gradient[source_column] += material_b['inertia']*source_acceleration+speed*material_b['momentum_b']
        force_gradient[speed_column] += material_v['inertia']*source_acceleration+material['momentum_b']+speed*material_v['momentum_b']
        result.update(jacobian=jacobian,force_gradient=force_gradient)
        return result

    def rhs(self, instant, state):
        return self.evaluate(state)['flow']
