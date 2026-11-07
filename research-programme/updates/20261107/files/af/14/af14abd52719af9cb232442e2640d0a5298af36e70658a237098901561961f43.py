from spatial_defect_common import *


def falling_complex(value,count):
    product=np.ones_like(value,dtype=complex)
    for index in range(count):
        product*=value-index
    return product


def main():
    modest()
    folder=ROOT/'results/inner-symbols'
    folder.mkdir(parents=True,exist_ok=False)
    bank_path=PARENT/'results/balanced-coefficients/bank.npz'
    bank=read_npz(bank_path)
    spacing=float(bank['spacing'])
    waves=np.r_[np.linspace(0,.25/spacing,65),np.linspace(.25/spacing,np.pi/spacing,129)[1:]]
    powers=-1+1j*waves
    smooth=waves<=.25/spacing+1e-12
    checks,rows=[],[]
    archives={name:[] for name in ['physical','grid','second','third']}
    for index,path in enumerate(event_paths()):
        event=read_npz(path)
        inverse,variance,third,unused_upper,unused_lower=deposition_moments(event['ratios'],spacing)
        inv=inverse[:,None]
        logarithm=np.log(inv)
        exponent=powers[None,:]
        physical=np.sum(event['rates'][:,None]*(inv*np.expm1(-(exponent+1)*logarithm)+inv**2*np.expm1((exponent+1)*logarithm))/2,axis=0)
        defects=[]
        for order,moments in [(2,variance/2),(3,third/6)]:
            derivative=(falling_complex(-powers,order)*inv**(-exponent-order)
                +falling_complex(powers+3,order)*inv**(exponent+3-order)
                -falling_complex(np.ones_like(powers),order)*inv**(1-order)
                -falling_complex(2*np.ones_like(powers),order)*inv**(2-order))/2
            defects.append(np.sum((event['rates']*moments)[:,None]*derivative,axis=0))
        shift=bank['offsets']*spacing
        grid=np.sum((bank['low'][index]*np.exp(-shift))[:,None]*np.expm1(1j*shift[:,None]*waves),axis=0)
        second=grid/bank['normalization'][index]-defects[0]
        third_symbol=second-defects[1]
        values=dict(physical=physical,grid=grid,second=second,third=third_symbol)
        row=dict(index=index,variants={})
        for label,action in values.items():
            diagnostics={}
            for band,mask in [('smooth',smooth),('nyquist',np.ones(len(waves),dtype=bool))]:
                growth=max(0.,float(np.max(action[mask].real)))/bank['eigenvalue'][index]
                discrepancy=float(np.max(abs(action[mask]-physical[mask]))/max(np.max(abs(physical[mask])),1e-300))
                diagnostics[band]=dict(positive_growth_over_eigen=growth,relative_symbol_error=discrepancy)
                checks.append(check(f'Sampled dissipativity:{label}:{band}:{index}',growth,1e-9))
            row['variants'][label]=diagnostics
            archives[label].append(action)
        rows.append(row)
    np.savez_compressed(folder/'symbols.npz',waves=waves,smooth=smooth,**{key:np.array(value) for key,value in archives.items()})
    finish(folder,dict(checks=checks,rows=rows,sampled_only=True,finite_boundary_stability_proved=False,
        no_cutoff_selected=True),__file__,[bank_path,*event_paths(),ROOT/'INNER-SYMBOL-CHECK.md'])
    print(json.dumps(dict(checks=len(checks),failed=sum(not row['passed'] for row in checks),
        maximum_growth={label:max(row['variants'][label]['nyquist']['positive_growth_over_eigen'] for row in rows) for label in archives})),flush=True)


if __name__=='__main__':
    main()
