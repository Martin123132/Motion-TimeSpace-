import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()
import numpy as np
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_moving_collar_action_20260914 import MovingCollarAction
from annular_moving_collar_sparse_20260914 import sparse_factors,SparseMovingCollarAction


def main():
    evidence=EvidenceRun('annular-moving-collar-sparse-equivalence-attempt01',__file__)
    try:
        for count in [17,33,65,129]:
            for gram in [False,True]:
                old=full_spatial_factors(count,gram)
                new=sparse_factors(count,gram)
                errors=[float(np.max(abs(dense-sparse.toarray()))) for dense,sparse in zip(old,new)]
                evidence.check(str((count,gram))+'_every_factor_and_sampling_entry',max(errors)<2e-15,errors)
        generator=np.random.default_rng(141400)
        for gram in [False,True]:
            old=MovingCollarAction(33,gram,[-.3,.3],[.5,.5])
            new=SparseMovingCollarAction(33,gram,[-.3,.3],[.5,.5])
            evidence.check(str(gram)+'_identical_initial_state',np.array_equal(old.initial_state,new.initial_state))
            state=old.initial_state+.0002*generator.normal(size=len(old.initial_state))
            state[-2:]=[.11,-.09]
            before=old.rhs(0,state)
            after=new.rhs(0,state)
            error=float(np.max(abs(before-after)))
            evidence.check(str(gram)+'_same_exact_action_equations',error<2e-12,error)
            energy_error=abs(old.energy(state)['total']-new.energy(state)['total'])
            evidence.check(str(gram)+'_same_action_energy',energy_error<2e-14,float(energy_error))
        for gram in [False,True]:
            matrices=sparse_factors(8193,gram)
            stored=sum(array.nbytes for matrix in matrices for array in [matrix.data,matrix.indices,matrix.indptr])
            evidence.check(str(gram)+'_large_factory_storage_under_5MB',stored<5_000_000,stored)
        evidence.report.update(sparse_only_no_equations_changed=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

