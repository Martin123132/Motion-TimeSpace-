from stage164_common import *


def main():
    modest()
    folder=ROOT/'results/baseline-check'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,records=[],list(ladder.inputs),{}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    path=READOUT_OWNER/'results/comparison'/(label+'.npz')
                    prior=read_npz(path)
                    inputs.append(path)
                    split=reader.split_values(prior['potential'],prior['energy'])
                    for quantity in ['amplitudes','residual','distortion']:
                        close(checks,'Saved paired readout re-evaluation:'+label+':'+quantity,split[quantity],prior[quantity],1e-10)
                    precise=precise_readout(prior,reader)
                    test(checks,'Saved paired baseline/MTS60digit cancellation:'+label,precise['same_baseline_cancellation'],1e-8)
                    close(checks,'Saved60digit increment amplitude:'+label,precise['amplitudes'][:,3:5],prior['amplitudes'][:,9:11],1e-8)
                    np.savez_compressed(folder/(label+'.npz'),baseline_potential=prior['potential'][:,:1],saved_mts_potential=prior['potential'][:,3:5],
                        baseline_amplitudes=prior['amplitudes'][:,:1],saved_mts_amplitudes=prior['amplitudes'][:,3:5],
                        baseline_energy=prior['energy'][:1],saved_mts_energy=prior['energy'][3:5])
                    records[label]=dict(path=str(path),sha256=digest(path),baseline_preserved=True,mts_preserved=True,
                        precision_cancellation=precise['same_baseline_cancellation'])
    finish(folder,dict(checks=checks,records=records,baseline_and_mts_reused=True,
        inner_histories_rerun=False,source_repair_does_not_replace_saved_readouts=True),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
