from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System, PrimitiveP2Geometry
from annular_live_P2_current_20260918 import P2Material, P2Density
import hashlib
import json
import numpy as np


def main():
    evidence=EvidenceRun('annular-P2-readout-error-budget-attempt01',__file__)
    try:
        evidence.report.update(no_forward_evolution=True,github_action=False,subagents_used=False,
            same_saved_states_no_refitting=True,readout_refinement_not_continuum_force_comparison=True,
            canonical_source_force_not_proper_acceleration=True,full_live_P2_force_convergence_proven=False)
        probes=np.linspace(5.21,6.79,241)
        for branch in ['reference','MTS']:
            folder=evidence.root/'source-intake/navier-stokes/20260914'/('annular-P2-tight-budget-'+branch+'-attempt01')
            status=json.loads((folder/'status.json').read_text())
            evidence.own(folder/'status.json')
            evidence.check(branch+'_tight_evolution_complete',status['state']=='complete')
            records={}
            for mode,degree in [('principal',14),('half_step',14),('label_refined',18)]:
                path=folder/(mode+'.npz')
                evidence.check(branch+mode+'_saved_array_hash',hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
                evidence.own(path)
                with np.load(path) as data:
                    states,rates=data['states'],data['rates']
                system=PrimitiveP2System(17,branch=='MTS',layer_degree=degree,radial_degree=18,action_order=32,label_order=20)
                forces,loads,clocks,residuals=[],[],[],[]
                for state,velocity in zip(states,rates):
                    coordinates,momenta=state
                    material=P2Material(system,coordinates)
                    geometry=PrimitiveP2Geometry(system,material,velocity)
                    residuals.append(system.canonical_residual(coordinates,momenta,velocity,geometry))
                    forces.append(system.forces(coordinates,velocity,geometry))
                    density=P2Density(material,probes)
                    density.update(velocity)
                    mass,lapse,unused,unused2=geometry.values(probes)
                    mass_rhs,unused=density.rhs(mass,lapse)
                    loads.append(mass_rhs/(system.coupling*probes**2))
                    lapse,root=geometry.metric(coordinates[:,-1])
                    clocks.append(np.sqrt(lapse**2-velocity[:,-1]**2/root**2))
                records[mode]=(system,states,np.array(forces),np.array(loads),np.array(clocks))
                evidence.check(branch+mode+'_saved_rates_still_canonical',max(residuals)<2e-10,max(residuals))
            coarse,unused,base_force,base_load,base_clock=records['principal']
            for mode in ['half_step','label_refined']:
                fine,states,force,load,clock=records[mode]
                interpolation=P2Material(fine,states[-1,0]).interpolation(coarse.labels)
                force=np.einsum('ij,tjm->tim',interpolation,force)
                clock=np.einsum('ij,tj->ti',interpolation,clock)
                row=dict(branch=branch,mode=mode,
                    canonical_source_force_difference=float(max(abs(force[:,:,-1]-base_force[:,:,-1]).ravel())),
                    scalar_covector_difference=float(max(abs(force[:,:,:-1]-base_force[:,:,:-1]).ravel())),
                    total_radial_density_difference=float(max(abs(load-base_load).ravel())),
                    proper_clock_rate_difference=float(max(abs(clock-base_clock).ravel())))
                evidence.report['cases'].append(row)
                evidence.save()
                print(row,flush=True)
                evidence.check(branch+mode+'_source_force_refinement_budget',row['canonical_source_force_difference']<2e-8,row)
                evidence.check(branch+mode+'_density_and_clock_refinement_budget',max(row['total_radial_density_difference'],row['proper_clock_rate_difference'])<2e-8,row)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
