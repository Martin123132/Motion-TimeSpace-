from source_pair_common import *
import time


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/balanced-coefficients'
    folder.mkdir(parents=True,exist_ok=False)
    raw_path=PARENT/'results/coefficients/bank.npz'
    total_path=PARENT/'results/balanced-coefficients/bank.npz'
    bank,total=map(read_npz,[raw_path,total_path])
    offsets,spacing=bank['offsets'],float(bank['spacing'])
    center=int(np.flatnonzero(offsets==0)[0])
    active=offsets!=0
    shift=offsets[active]*spacing
    waves=np.r_[np.linspace(0,.25/spacing,65),np.linspace(.25/spacing,np.pi/spacing,129)[1:]]
    powers=np.r_[1j*waves,1+1j*waves]
    smooth=np.tile(waves<=.25/spacing+1e-12,2)
    rows,checks,candidates,scales=[],[],[],[]
    symbol_physical,symbol_candidate,symbol_total=[],[],[]
    paths=event_paths()
    for index,(values,path) in enumerate(zip(bank['low'],paths)):
        event=read_npz(path)
        eigen=float(bank['eigenvalue'][index])
        candidate,scale,unscaled=physical_pairing(values,offsets,spacing,eigen)
        ratios=np.exp(shift)
        expected=scale*source_symbol(shift,values[active],powers)
        actual=symbol(shift,candidate[active],-powers-2,eigen)
        total_action=symbol(shift,total['low'][index,active],-powers-2,eigen)
        physical=source_symbol(np.log(event['ratios']),event['rates'],powers)
        residual=float(np.max(abs(actual-expected))/eigen)
        moments=symbol(shift,candidate[active],np.array([-1.,-2.,-3.]),eigen)
        moment_error=float(np.max(abs(moments-np.array([0.,0.,eigen])))/eigen)
        reciprocity=float(np.max(abs(candidate[:center][::-1]-candidate[center+1:]/np.exp(offsets[center+1:]*spacing)**3))/np.max(candidate[center+1:]))
        checks.extend([dict(name=f'Positive source pairing:{index}',passed=bool(np.all(candidate[active]>=0) and scale>0)),
            check(f'Full adjoint symbol identity:{index}',residual,1e-9),
            check(f'Bulk moments:{index}',moment_error,1e-9),
            check(f'Reciprocity:{index}',reciprocity,1e-14),
            check(f'Saved lambda=m/2:{index}',abs(eigen-float(bank['moment'][index])/2)/eigen,1e-8)])
        comparison={}
        for label,action in [('source',actual),('total',total_action)]:
            for band,mask in [('smooth',smooth),('nyquist',np.ones(len(powers),dtype=bool))]:
                value=float(np.max(abs(action[mask]-physical[mask]))/max(np.max(abs(physical[mask])),1e-300))
                comparison[label+'_'+band]=value
                if band=='smooth':
                    checks.append(check(f'Sensitivity1percent:symbol:{label}:{index}',value,.01))
        comparison['total_source_identity_defect_over_lambda']=float(np.max(abs(total_action-expected))/eigen)
        rows.append(dict(index=index,scale=scale,unscaled_eigenvalue=unscaled,eigenvalue=eigen,
            adjoint_identity_residual=residual,moment_error=moment_error,comparison=comparison,
            rate_change_from_total_relative=float(np.sum(abs(candidate-total['low'][index]))/np.sum(abs(total['low'][index])))))
        candidates.append(candidate)
        scales.append(scale)
        symbol_physical.append(physical)
        symbol_candidate.append(actual)
        symbol_total.append(total_action)
    assert all(row['passed'] for row in checks if not row['name'].startswith('Sensitivity1percent:'))
    np.savez_compressed(folder/'bank.npz',**{key:value for key,value in bank.items() if key!='low'},
        low=np.array(candidates),unrepaired_low=bank['low'],normalization=np.array(scales))
    np.savez_compressed(folder/'symbols.npz',powers=powers,smooth=smooth,physical=np.array(symbol_physical),
        source=np.array(symbol_candidate),total=np.array(symbol_total))
    inputs=[raw_path,total_path,raw_path.parent/'status.json',total_path.parent/'status.json',*paths]
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,bulk_moment_contracts_pass=True,
        pairing='source-adjoint',physical_eigenvalues_unchanged=True,new_empirical_fit=False,
        new_temperature_integrals=0,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failures=sum(not row['passed'] for row in checks),
        identity_max=max(row['adjoint_identity_residual'] for row in rows),
        symbol_errors={key:max(row['comparison'][key] for row in rows) for key in rows[0]['comparison']},
        rate_change_from_total_max=max(row['rate_change_from_total_relative'] for row in rows))),flush=True)


if __name__=='__main__':
    main()
