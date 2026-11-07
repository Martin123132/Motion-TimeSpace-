from response217 import *


def main():
    protocol()
    rows=[];records=[];paths={}
    with mp.workdps(100):
        for model in ('heavy','cold'):
            values=packet(ROOT/f'frozen/{model}.npz')
            mass=as_mp(values['mass'])
            temperature=as_mp(values['temperature'][:,None])
            energy=as_mp(values['energy'][None,:])
            defect=energy-temperature.T*mass
            defect_norm=mp.sqrt(mp.fsum(value**2 for value in defect))
            check(rows,model+':stored energy/mass row roundoff',defect_norm/mp.sqrt(mp.fsum(value**2 for value in energy)),1e-10,'identity')
            for count in (2048,4096):
                folder=ROOT/f'cases/{model}-{count}'
                reference_packet=packet(folder/'reference80.npz')['state']
                original_packet=packet(folder/'direct.npz')['state']
                reference=as_mp(reference_packet[:,:36])+as_mp(reference_packet[:,36:])
                direct=as_mp(original_packet[:,:36])+as_mp(original_packet[:,36:])
                photon=mp.matrix(96,36)
                for row,index in enumerate(values['others'],start=1):
                    photon[int(index),:]=reference[row,:]
                for column in range(36):
                    photon[1,column]=(reference[0,column]-mp.fsum(energy[0,int(index)]*photon[int(index),column] for index in values['others']))/energy[0,1]
                contracted=temperature.T*mass*photon
                encoded=energy*photon
                correction=defect*photon
                heat=mp.mpf(float(values['heat']))
                alpha=mp.mpf(float(1.5/(.25*float(values['span'])/count)))
                balance=-heat*(alpha+1)/alpha*reference[96,:]
                for column in range(36):
                    scale=max(abs(contracted[column]),mp.mpf('1e-300'))
                    identity=abs(encoded[column]-contracted[column]-correction[column])/scale
                    residual=abs(direct[0,column]-contracted[column])/scale
                    balance_error=abs(balance[column]-contracted[column])/scale
                    check(rows,f'{model}:{count}:readout defect identity:{column}',identity,1e-10,'identity')
                    check(rows,f'{model}:{count}:contracted energy replay:{column}',residual,1e-10,'identity')
                    check(rows,f'{model}:{count}:reference energy balance:{column}',balance_error,1e-10,'identity')
                    records.append(dict(model=model,count=count,column=column,raw_error=float(abs(direct[0,column]-encoded[column])/scale),
                        readout_defect=float(abs(correction[column])/scale),remaining=float(residual),balance_error=float(balance_error)))
                for name in ('reference80.npz','direct.npz','result.json'):
                    paths[str(folder/name)]=digest(folder/name)
        failed=[row for row in rows if not row['passed']]
        write(ROOT/'results/energy-readout-diagnosis.json',dict(checks=rows,failed_checks=failed,records=records,
            input_hashes=paths,scope='diagnosis of stored spectral row versus mass-contracted protected energy',precision=100,
            hypothesis='binary-rounded e equals t*M at float precision but not after lifting all operands independently to 100digits'))
        print(json.dumps(dict(checks=len(rows),failed=len(failed),raw_max=max(row['raw_error'] for row in records),
            defect_max=max(row['readout_defect'] for row in records),remaining_max=max(row['remaining'] for row in records),
            balance_max=max(row['balance_error'] for row in records))),flush=True)


if __name__=='__main__':
    inherited.source.modest()
    main()
