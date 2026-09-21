from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_schur_force_20260919 import FullSchurForce, schur_difference
from annular_position_action_response_20260919 import PositionGenerator, propagate_position
from scipy.sparse import csr_matrix
from scipy.linalg import expm
import contextlib
import json
import numpy as np
import sympy as symbolic


class DenseAction:
    def __init__(self, mass, stiffness):
        self.mass, self.stiffness = mass, stiffness
        self.count = mass.shape[0]
        self.operator = np.linalg.solve(mass, stiffness)

    def acceleration_operator(self, values):
        return self.operator @ values

    def acceleration_transpose(self, values):
        return self.operator.T @ values


def main():
    evidence = EvidenceRun('annular-full-force-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, synthetic_controls_only=True)
        first_drive, last_drive, first_ratio, last_ratio, first_gravity, last_gravity = symbolic.symbols('Jc Jf qc qf Gc Gf')
        first_force = (first_drive-first_ratio*first_gravity)/(1+first_ratio)
        last_force = (last_drive-last_ratio*last_gravity)/(1+last_ratio)
        budget = ((last_drive-first_drive)-last_ratio*(last_gravity-first_gravity)
            -(last_ratio-first_ratio)*(first_gravity+first_force))/(1+last_ratio)
        evidence.check('exact_schur_signed_difference', symbolic.factor(last_force-first_force-budget) == 0)
        random = np.random.default_rng(719432)
        for fixture in range(12):
            count, quadrature = 5, 13
            model = object.__new__(FullSchurForce)
            model.shape = csr_matrix(random.normal(size=(quadrature,count)))
            model.material = csr_matrix(random.normal(size=(quadrature,count)))
            model.material_partial = csr_matrix(random.normal(size=(quadrature,count)))
            model.material_rate = csr_matrix(random.normal(size=(quadrature,count)))
            model.gradient = csr_matrix(random.normal(size=(quadrature,count)))
            model.gram = csr_matrix(random.normal(size=(4,count)))
            model.weight = np.exp(random.normal(size=quadrature)*.2)
            model.weight_partial, model.weight_rate = random.normal(size=(2,quadrature))
            model.gradient_weight = np.exp(random.normal(size=quadrature)*.2)
            model.gradient_partial = random.normal(size=quadrature)
            model.gram_weight = np.exp(random.normal(size=4)*.2)
            model.gram_partial = random.normal(size=4)
            model.source_velocity, model.inertia, model.dust_drive = .03, .7, -.11
            shape, material = model.shape.toarray(), model.material.toarray()
            partial, rate = model.material_partial.toarray(), model.material_rate.toarray()
            mass = shape.T @ (model.weight[:,None]*shape)
            model.solve = lambda values: np.linalg.solve(mass, values)
            cross = shape.T @ (model.weight[:,None]*material)
            inertia = material.T @ (model.weight[:,None]*material)
            cross_rate = shape.T @ (model.weight_rate[:,None]*material+model.weight[:,None]*rate)
            mass_rate = shape.T @ (model.weight_rate[:,None]*shape)
            inertia_rate = rate.T @ (model.weight[:,None]*material)+material.T @ (
                model.weight_rate[:,None]*material+model.weight[:,None]*rate)
            mass_partial = shape.T @ (model.weight_partial[:,None]*shape)
            cross_partial = shape.T @ (model.weight_partial[:,None]*material+model.weight[:,None]*partial)
            inertia_partial = partial.T @ (model.weight[:,None]*material)+material.T @ (
                model.weight_partial[:,None]*material+model.weight[:,None]*partial)
            first, last = random.normal(size=(2,2,count))*.1
            scalar, velocity = last
            speed = model.source_velocity
            raw = (.5*velocity @ mass_partial @ velocity+speed*velocity @ cross_partial @ scalar
                +.5*speed**2*scalar @ inertia_partial @ scalar-.5*scalar @ model.stiffness(scalar, partial=True))
            transport = (velocity @ cross @ velocity+velocity @ cross_rate @ scalar
                +speed*scalar @ inertia_rate @ scalar+2*speed*velocity @ inertia @ scalar)
            right = speed*cross.T @ velocity+speed**2*inertia @ scalar-model.stiffness(scalar)
            right -= mass_rate @ velocity+speed*cross_rate @ scalar+speed*cross @ velocity
            independent_drive = raw-transport-scalar @ cross.T @ model.solve(right)
            result = model.evaluate(*last, with_gradient=True)
            evidence.check('fixture'+str(fixture)+'_independent_dense_drive', abs(result['free_wave_drive']-independent_drive) < 2e-12)
            direction = random.normal(size=last.shape)
            plus, minus = model.evaluate(*(last+.07*direction)), model.evaluate(*(last-.07*direction))
            for name, gradient in [('free_wave_drive','gradient_drive'),('inertia_ratio','gradient_ratio')]:
                analytic = float(np.sum(result[gradient]*direction))
                difference = (plus[name]-minus[name])/.14
                evidence.check('fixture'+str(fixture)+'_'+name+'_quadratic_directional_derivative',
                    abs(analytic-difference) < 3e-11*max(1.,abs(analytic)), dict(analytic=analytic, difference=difference))
            covector, before, after = model.secant(first,last)
            pairing = float(np.sum(covector*(last-first)))
            evidence.check('fixture'+str(fixture)+'_exact_rational_secant', abs(pairing-after['force']+before['force']) < 2e-12)
            after['dust_drive'] += .2
            after['force'] = (after['free_wave_drive']-after['inertia_ratio']*after['dust_drive'])/(1+after['inertia_ratio'])
            full = schur_difference(before,after)
            evidence.check('fixture'+str(fixture)+'_nonzero_dust_and_inertia', abs(full['total']-full['direct']) < 2e-12)
            evidence.report['cases'].append(dict(kind='quadratic_full_force',fixture=fixture,
                independent_drive_error=abs(result['free_wave_drive']-independent_drive),
                secant_error=abs(pairing-result['force']+before['force']),valid_for_claim=False))
        for frequency in [0.,3.,70.]:
            mass = np.diag([.8,1.2,1.5])
            stiffness = np.diag([.5,1.,2.])*frequency**2
            action = DenseAction(mass,stiffness)
            count = action.count
            position,velocity = random.normal(size=(2,count,2))
            first_force,last_force = random.normal(size=(2,count))
            step = .003
            slope = (last_force-first_force)/step
            generator = PositionGenerator(action,first_force,slope,scale=10.)
            dense = np.zeros((2*count+2,2*count+2))
            dense[:count,count:2*count] = 10*np.eye(count)
            dense[count:2*count,:count] = -action.operator/10
            dense[count:2*count,-2],dense[count:2*count,-1] = slope,first_force
            dense[-2,-1] = 1
            test = random.normal(size=(2*count+2,2))
            evidence.check('frequency'+str(frequency)+'_generator_adjoint', np.max(abs(generator @ test-dense @ test)) < 1e-12
                and np.max(abs(generator.T @ test-dense.T @ test)) < 1e-12)
            moved = propagate_position(action,position,velocity,first_force,last_force,step,[1.,0.],scale=10.)
            initial = np.vstack([10*position,velocity,np.zeros((1,2)),np.array([[1.,0.]])])
            exact = expm(step*dense) @ initial
            error = max(np.max(abs(moved['position']-exact[:count]/10)),np.max(abs(moved['velocity']-exact[count:2*count])))
            evidence.check('frequency'+str(frequency)+'_independent_dense_exponential', error < 2e-12)
            half = propagate_position(action,position,velocity,first_force,(first_force+last_force)/2,step/2,[1.,0.],scale=10.)
            halves = propagate_position(action,half['position'],half['velocity'],(first_force+last_force)/2,last_force,step/2,[1.,0.],scale=10.)
            evidence.check('frequency'+str(frequency)+'_affine_halfstep', np.max(abs(moved['position']-halves['position'])) < 2e-12
                and np.max(abs(moved['velocity']-halves['velocity'])) < 2e-12)
            evidence.report['cases'].append(dict(kind='affine_position_response',frequency=frequency,
                independent_exponential_error=float(error),valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
