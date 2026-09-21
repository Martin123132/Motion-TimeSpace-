from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_GR_projection_20260916 import GRProjection
from run_annular_source_fitted_crossing_20260915 import initial
import argparse
import hashlib
import json
import numpy as np


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        path=intake/'annular-dense-GR-references-attempt01/status.json'
        status=json.loads(path.read_text())
        evidence.own(path)
        path=path.parent/'oracle-768.npz'
        evidence.own(path)
        evidence.check('reference_hash',status['state']=='complete' and hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path,allow_pickle=False) as saved:
            times,states,forces=saved['times'].copy(),saved['states'].copy(),saved['forces'].copy()
        oracle=TwoSidedGRCharacteristics(768,mass=0.,source=.03)
        system=LocallyRefinedSourceAction(33,True,background_mass=0.,source_splits=8)
        projection=GRProjection(oracle,system)
        reconstructed=[projection.reconstruct(state,oracle.rhs(instant,state)) for instant,state in zip(times,states)]
        projected,derivatives=np.array([row[0] for row in reconstructed]),np.array([row[1] for row in reconstructed])
        seed=initial(system)
        evidence.check('finite_small_projection',projected.shape==derivatives.shape==(81,len(seed))
            and np.isfinite(projected).all() and np.isfinite(derivatives).all())
        evidence.report.update(original_action_unchanged=True,finite_future_trajectories_read=False,
            fresh_small_reference_not_old_forward_data=True,count=33,source_splits=8,degree=768)
        destination=evidence.output/'GR-only-768-33.npz'
        np.savez_compressed(destination,times=times,states=projected,derivatives=derivatives,
            original_initial=seed,oracle_forces=forces)
        evidence.own(destination,'outputs')
        evidence.report['cases'].append(dict(count=33,scalar_dofs=system.count,degree=768,source_splits=8))
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
