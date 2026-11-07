from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_wave_resume_20260930 import restore_totals
import numpy as np


def main():
    evidence = EvidenceRun('annular-C0-wave-resume-validation-attempt01',__file__)
    try:
        sizes = dict(base=4,volume=4,atoms=4,force=1)

        def empty():
            return {name:np.zeros(size) for name,size in sizes.items()}

        def accumulate(totals,corrections,blocks):
            for block in blocks:
                for name,size in sizes.items():
                    value = block[:size]
                    updated = totals[name]+value
                    corrections[name] += np.where(abs(totals[name])>=abs(value),(totals[name]-updated)+value,(value-updated)+totals[name])
                    totals[name] = updated

        blocks = np.random.default_rng(92837).normal(size=(48,4))*np.tile([1e12,1.,1e-12],16)[:,None]
        total,correction = empty(),empty()
        accumulate(total,correction,blocks)
        saved_total,saved_correction = empty(),empty()
        accumulate(saved_total,saved_correction,blocks[:17])
        base = dict(**{'total_'+name:value for name,value in saved_total.items()},
            **{'correction_'+name:value for name,value in saved_correction.items()},
            phase='volume',next_index=17*16,order=32,complete=False)
        path = evidence.output/'manufactured-partial.npz'
        np.savez_compressed(path,**base)
        evidence.own(path,'outputs')
        loaded,loaded_correction = empty(),empty()
        phase,index = restore_totals(path,32,loaded,loaded_correction)
        evidence.check('restored_block_boundary',phase=='volume' and index==17*16)
        accumulate(loaded,loaded_correction,blocks[17:])
        evidence.check('bitwise_compensated_resume',all(np.array_equal(loaded[name],total[name])
            and np.array_equal(loaded_correction[name],correction[name]) for name in sizes))
        for label,change in [('wrong-order',dict(order=24)),('completed',dict(complete=True)),
                ('bad-phase',dict(phase='unknown')),('misaligned',dict(next_index=3)),
                ('negative',dict(next_index=-16)),('nonfinite',dict(total_force=np.array([np.nan])))]:
            path = evidence.output/(label+'.npz')
            np.savez_compressed(path,**dict(base,**change))
            evidence.own(path,'outputs')
            rejected = False
            try:
                restore_totals(path,32,empty(),empty())
            except ValueError:
                rejected = True
            evidence.check(label+'_rejected',rejected)
        for phase in ['traces','radial-cuts']:
            path = evidence.output/(phase+'.npz')
            np.savez_compressed(path,**dict(base,phase=phase))
            evidence.own(path,'outputs')
            loaded,loaded_correction = empty(),empty()
            restore_totals(path,32,loaded,loaded_correction)
            evidence.check(phase+':preserve_volume_restart_atoms',np.array_equal(loaded['volume'],saved_total['volume'])
                and np.array_equal(loaded_correction['volume'],saved_correction['volume'])
                and np.all(loaded['atoms']==0) and np.all(loaded_correction['atoms']==0))
        evidence.report.update(manufactured_only=True,actual_wave_resumed=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
