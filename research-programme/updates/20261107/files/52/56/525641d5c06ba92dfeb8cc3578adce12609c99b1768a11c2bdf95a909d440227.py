from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_physical_native_kernel_20260928 import NativeKernel,decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from decimal import Decimal,localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-Neumann-source-corner-profile-'+args.level+'-attempt01',__file__)
    deadline = perf_counter()+600
    try:
        parent_path = evidence.output.parent/'annular-constrained-state-search-integrity-20261001.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['hashes'])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
        relative_root = 'source-intake/navier-stokes/20260914/'
        builder = verify_report(evidence,relative_root+'annular-Neumann-kernel-family-attempt01/status.json')
        acceleration_report = verify_report(evidence,relative_root+'annular-Neumann-null-acceleration-'+args.level+'-attempt02/status.json')
        evidence.check('complete_input_calculations',builder['state']==acceleration_report['state']=='complete')
        case = next(row for row in builder['cases'] if row['level']==args.level)
        with np.load(evidence.root/case['initial_data_path'],allow_pickle=False) as archive:
            state = {name:archive[name].copy() for name in archive.files}
        with np.load(evidence.root/acceleration_report['results'][-1]['acceleration_path'],allow_pickle=False) as archive:
            acceleration = archive['acceleration'].copy()
        with localcontext() as context:
            context.prec = 64
            unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            packet = json.loads((evidence.root/sources['packet']).read_text())
            loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
            engine = NativeKernel(action.mesh,packet['gram_support'],True)
            data = physical_data(engine,loads,action,0.)
            radii = np.asarray(nodal_radii(engine,data['edges']),float)
            source = float(data['source'])
            lower,upper = float(data['edges'][0]),float(data['edges'][-1])
            amplitude = float(case['amplitude'])
            endpoint = np.where(radii<source,lower,upper)
            displacement = np.where(radii<source,(radii-lower)/(source-lower),(upper-radii)/(upper-source))
            section = 2*amplitude*((radii-endpoint)*displacement-(source-endpoint))
            field_acceleration = np.asarray(decimals(acceleration[:,:-1].T)@decimals(data['cardinal']),float)
            source_acceleration = float(data['cardinal']@acceleration[:,-1])
            normal = field_acceleration-section*source_acceleration
        values,derivatives = action.solver.values(action.solution,radii)
        metric = 1-2*values[0]/radii
        metric_radial = -2*derivatives[0]/radii+2*values[0]/radii**2
        speed_square = np.exp(2*values[1])*metric
        drift = speed_square*(2/radii+derivatives[1]+metric_radial/(2*metric))
        gradient = 2*amplitude*(radii-endpoint)
        interior_wave = 2*amplitude*speed_square+drift*gradient
        predicted_normal = interior_wave+2*amplitude*(source-endpoint)*source_acceleration
        error = normal-predicted_normal
        evidence.check('normal_chain_rule_independent_form',np.max(np.abs(normal-
            (field_acceleration-gradient*displacement*source_acceleration+
             2*amplitude*(source-endpoint)*source_acceleration)))<1e-15)
        corner = next(row for row in case['source_corner'] if row['label']==0.)
        limits = [2*amplitude*(source-lower)*(source_acceleration-corner['required_left']),
            2*amplitude*(source-upper)*(source_acceleration-corner['required_right'])]
        evidence.check('nonzero_one_sided_required_accelerations',min(abs(value) for value in limits)>1e-5)
        bands = []
        for margin in [.005,.01,.025,.05]:
            selected = (np.abs(radii-source)>margin)&(radii-lower>margin)&(upper-radii>margin)
            evidence.check('interior_band_populated_'+str(margin),np.count_nonzero(selected)>100)
            bands.append(dict(margin=margin,count=int(np.count_nonzero(selected)),
                maximum_error=float(np.max(np.abs(error[selected]))),
                rms_error=float(np.sqrt(np.mean(error[selected]**2)))))
        near = {}
        for side in ['left','right']:
            indices = np.flatnonzero(radii<source if side=='left' else radii>source)
            indices = indices[np.argsort(np.abs(radii[indices]-source))[:8]]
            near[side] = [dict(radius=float(radii[index]),distance=float(radii[index]-source),
                normal=float(normal[index]),interior_prediction=float(predicted_normal[index]),error=float(error[index]))
                for index in indices]
        path = evidence.output/'central-normal-acceleration-profile.npz'
        np.savez_compressed(path,radius=radii,normal=normal,interior_prediction=predicted_normal,error=error,
            source=np.array(source),source_acceleration=np.array(source_acceleration),source_trace_limits=np.array(limits))
        evidence.own(path,'outputs')
        evidence.report.update(level=args.level,profile_path=str(path.relative_to(evidence.root)),
            source_acceleration=source_acceleration,source_radius=source,lower=lower,upper=upper,
            amplitude=amplitude,source_trace_limits=limits,interior_bands=bands,nearest_source_nodes=near,
            continuum_trace_condition_met=False,finite_Galerkin_profile_not_continuum_trajectory=True,
            scope='Central material label; boundary/source-layer diagnostic only, no force modification.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

