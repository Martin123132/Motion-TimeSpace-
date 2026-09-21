from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_exponential_20260919 import FactoredAction,VelocityGenerator,propagate
from scipy.linalg import expm
from scipy.sparse import csr_matrix
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-action-exponential-algebra-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,synthetic_fixture_not_physical_evidence=True)
        random = np.random.default_rng(191848)
        for case in range(3):
            count = 7
            mass = np.diag(random.uniform(1.,3.,count))
            off = random.uniform(-.1,.1,count-1)
            mass += np.diag(off,1)+np.diag(off,-1)
            bands = np.zeros((5,count))
            bands[2] = np.diag(mass)
            bands[1,1:],bands[3,:-1] = off,off
            gradient,gram = csr_matrix(random.normal(size=(9,count))),csr_matrix(random.normal(size=(4,count)))
            weights,gram_weights = random.uniform(.5,2.,9),random.uniform(.1,1.,4)
            action = FactoredAction(bands,gradient,weights,gram,gram_weights)
            stiffness = (gradient.T @ gradient.multiply(weights[:,None])+gram.T @ gram.multiply(gram_weights[:,None])).toarray()
            dense = np.linalg.solve(mass,stiffness)
            slope = random.normal(size=count)
            scale,step = 3.2,.13
            generator = VelocityGenerator(action,slope,scale)
            matrix = np.zeros(generator.shape)
            matrix[:count,count:2*count] = scale*np.eye(count)
            matrix[count:2*count,:count] = -dense/scale
            matrix[count:2*count,-1] = slope
            tests = random.normal(size=(2*count+1,3))
            evidence.check(str(case)+'_factor_and_banded_mass_match_dense',np.max(abs(action.acceleration_operator(tests[:count])-dense @ tests[:count])) < 1e-12)
            evidence.check(str(case)+'_block_generator_and_adjoint',np.max(abs(generator @ tests-matrix @ tests)) < 1e-12
                and np.max(abs(generator.H @ tests-matrix.T @ tests)) < 1e-12)
            velocity,acceleration = random.normal(size=(2,count,2))
            constants = np.array([1.,0.])
            first = propagate(action,velocity,acceleration,slope,step,constants,scale)
            initial = np.vstack([scale*velocity,acceleration,constants[None,:]])
            expected = expm(step*matrix) @ initial
            error = max(float(np.max(abs(first['velocity']-expected[:count]/scale))),
                float(np.max(abs(first['acceleration']-expected[count:2*count]))))
            evidence.check(str(case)+'_independent_dense_exponential',error < 2e-12)
            half = propagate(action,velocity,acceleration,slope,step/2,constants,scale)
            halves = propagate(action,half['velocity'],half['acceleration'],slope,step/2,constants,scale)
            split_error = action.energy_norm(first['velocity'][:,0]-halves['velocity'][:,0],first['acceleration'][:,0]-halves['acceleration'][:,0])
            evidence.check(str(case)+'_constant_source_halfstep_control',split_error < 2e-12)
            initial_energy = action.energy(velocity[:,1],acceleration[:,1])
            final_energy = action.energy(first['velocity'][:,1],first['acceleration'][:,1])
            evidence.check(str(case)+'_homogeneous_action_energy_conservation',abs(final_energy-initial_energy) < 2e-12*initial_energy)
            rescaled = propagate(action,velocity,acceleration,slope,step,constants,.8)
            evidence.check(str(case)+'_scaling_is_not_a_physical_parameter',action.energy_norm(
                first['velocity'][:,0]-rescaled['velocity'][:,0],first['acceleration'][:,0]-rescaled['acceleration'][:,0]) < 3e-12)
            evidence.report['cases'].append(dict(case=case,dense_exponential_error=error,halfstep_energy_norm=split_error,
                energy_relative_drift=abs(final_energy-initial_energy)/initial_energy,valid_for_claim=False))
        zero = FactoredAction(np.vstack([np.zeros((2,2)),np.ones((1,2)),np.zeros((2,2))]),
            csr_matrix((1,2)),np.ones(1),csr_matrix((1,2)),np.zeros(1))
        velocity,acceleration,slope = np.array([[.2],[.3]]),np.array([[.1],[-.4]]),np.array([.7,-.2])
        result = propagate(zero,velocity,acceleration,slope,.2,np.ones(1),2.)
        evidence.check('zero_frequency_polynomial_limit',np.max(abs(result['velocity']-velocity-.2*acceleration-.02*slope[:,None])) < 1e-14
            and np.max(abs(result['acceleration']-acceleration-.2*slope[:,None])) < 1e-14)
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
