from shape_common import *
from stable_spectral_readout import exact_readout


def interval_rule(lower,upper,count):
    nodes,weights=special.roots_legendre(count)
    low,high=math.log(lower),math.log(upper)
    frequency=np.exp((low+high)/2+(high-low)/2*nodes)
    occupation=1/np.expm1(frequency)
    measure=weights*(high-low)/2*frequency**3*occupation*(1+occupation)/I3
    return frequency,measure


def main():
    modest()
    folder=ROOT/'results/residual-readout'
    folder.mkdir(parents=True,exist_ok=False)
    source=ROOT/'results/decomposition/status.json'
    report=json.loads(source.read_text())
    raw_path=PARENT/'results/projection/status.json'
    metadata=json.loads(raw_path.read_text())
    basis=infrared_ladder.ConsistentBasis(**metadata['basis_specification'])
    shifts=np.array(report['readouts']['canonical700']['energy_shifts'])
    capacity=report['readouts']['canonical700']['capacity']
    edges=[1e-5,1e-3,1e-2,1e-1,1.,10.,60.]
    checks,inputs,models=[],[source,raw_path,ROOT/'RESIDUAL-READOUT.md'],{}
    for path,expected in report['input_hashes'].items():
        assert digest(path)==expected,path
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<limit)))
    for model in ['heavy','cold']:
        canonical_path=ROOT/'results/decomposition'/f'{model}-main-1024-canonical.npz'
        stable_path=PARENT/'results/stable-readout'/f'{model}-physical-band-spectrum.npz'
        inputs.extend([canonical_path,stable_path])
        with np.load(canonical_path) as saved:
            photon,energy,amplitudes=[saved[key].copy() for key in ['photon','energy','amplitudes']]
            norm_reference=saved['residual_norm'][:3].copy()
        physical=metadata['models'][model]['metadata']
        heat=physical['heat']
        eta=energy/capacity
        with np.load(stable_path) as saved:
            frequency=saved['x'].copy()
            window_occupation=saved['delta_occupation'].copy()
        baseline=exact_readout(basis,frequency,photon[:,:1],energy[:1],65)['potential']
        occupation=1/np.expm1(frequency)
        weight=occupation*(1+occupation)
        total=np.column_stack([heat*weight*baseline[:,0],window_occupation])
        standard=np.column_stack([frequency/BETA-1,frequency*(frequency/np.tanh(frequency/2)-4)])
        templates=standard-frequency[:,None]*shifts
        temp=heat*weight[:,None]*frequency[:,None]*eta
        mu=heat*weight[:,None]*templates[:,0,None]*amplitudes[0]
        comp_y=heat*weight[:,None]*templates[:,1,None]*amplitudes[1]
        residual=total-temp-mu-comp_y
        absolute_scale=abs(total)+abs(temp)+abs(mu)+abs(comp_y)+abs(residual)
        allowance=256*np.finfo(float).eps*np.maximum(absolute_scale,1e-300)
        test('Physical occupation reconstruction within explicit cancellation allowance:'+model,
            np.max(abs(total-temp-mu-comp_y-residual)/allowance),1.)
        frequency_hz=frequency*physical['k_B']*physical['reference_temperature_K']/physical['h_P']
        radiance=2*physical['h_P']*frequency_hz**3/physical['c']**2
        parts={name:radiance[:,None]*value for name,value in
            [('total',total),('temperature',temp),('mu',mu),('y',comp_y),('residual',residual)]}
        intensity_allowance=256*np.finfo(float).eps*np.maximum(sum(abs(value) for value in parts.values()),1e-300)
        error=parts['total']-parts['temperature']-parts['mu']-parts['y']-parts['residual']
        test('Specific intensity reconstruction within explicit cancellation allowance:'+model,np.max(abs(error)/intensity_allowance),1.)
        np.savez(folder/f'{model}-physical-residual-spectrum.npz',x=frequency,frequency_Hz=frequency_hz,
            delta_occupation_total=total,delta_occupation_temperature=temp,delta_occupation_mu=mu,
            delta_occupation_y=comp_y,delta_occupation_residual=residual,
            **{'delta_intensity_'+key+'_SI':value for key,value in parts.items()},
            fractional_residual_intensity=residual/occupation[:,None],
            signed_mu_y_physical=heat*amplitudes,
            temperature_energy_fraction=heat*eta,
            temperature_standard_fraction=heat*(eta-shifts@amplitudes))
        bin_sums={}
        for count in [300,600]:
            bins=[]
            for lower,upper in zip(edges[:-1],edges[1:]):
                sample,measure=interval_rule(lower,upper,count)
                potential=basis.evaluate(sample)@photon[:,:3]
                standards=np.column_stack([sample/BETA-1,sample*(sample/np.tanh(sample/2)-4)])
                matched=standards-sample[:,None]*shifts
                remainder=potential-sample[:,None]*eta[:3]-matched@amplitudes[:,:3]
                bins.append(np.sum(measure[:,None]*remainder**2,axis=0))
            bin_sums[count]=np.array(bins)
        test('Residual bins reconstruct canonical squared norm:'+model,
            np.max(abs(bin_sums[600].sum(axis=0)/norm_reference**2-1)),1e-8)
        test('Residual-bin300 to600 quadrature sensitivity:'+model,
            np.max(abs(bin_sums[300]-bin_sums[600])/norm_reference[None,:]**2),1e-8)
        fractions=bin_sums[600]/norm_reference[None,:]**2
        models[model]=dict(bin_edges=edges,column_order=['baseline','window-join1','window-join2'],
            fixed_primary_amplitudes_not_refitted=True,residual_squared_norm_fraction_by_bin=fractions.tolist(),
            residual_squared_norm_below_point1=fractions[:3].sum(axis=0).tolist(),
            residual_squared_norm_below_one=fractions[:4].sum(axis=0).tolist())
    finish(folder,dict(checks=checks,models=models,physical_units='W m^-2 Hz^-1 sr^-1',
        pointwise_roundoff_allowance_explicit=True,baseline_and_window_same_templates=True,
        source_evaluations=0,projection_amplitudes_refitted=False,
        analytic_template_tail_not_assumed_physical=True,final_saved_scale=1e-5),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],models=models)),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__=='__main__':
    main()

