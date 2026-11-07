from __future__ import annotations

import argparse
from spectrum_common import *


def fields(label):
    data=load_evolution(label)
    folder=ROOT/'runs'/label
    status=json.loads((folder/'status.json').read_text())
    background=np.load(folder/'background.npz')
    value=data['values'];names=data['names']
    cold=background['cdm'];baryon=background['baryon'];neutrino=background['nu']
    cb=cold+baryon
    standard=cb+neutrino
    delta_cb=(cold*value[:,:,names.index('delta_cdm')]+baryon*value[:,:,names.index('delta_baryon')])/cb
    numerator=cb*delta_cb+neutrino*value[:,:,names.index('delta_nu')]
    if status['arguments']['branch']=='heavy':
        table=np.load(ROOT/'runs/projection'/(status['arguments']['projection']+'.npz'))
        density0=float(table['matching_density'])
        actual=value[0,:,names.index('a')]
        numerator=numerator+actual**2*value[:,:,names.index('mts_drho_h')]
        standard=standard+density0*actual
    delta_m=numerator/standard
    velocity_cdm=value[:,:,names.index('v_newtonian_cdm')]
    velocity_cb=(cold*velocity_cdm+baryon*value[:,:,names.index('v_newtonian_baryon')])/cb
    assert np.isfinite(delta_m).all()
    return data,dict(delta_m=delta_m,delta_cb=delta_cb,velocity_cdm=velocity_cdm,velocity_cb=velocity_cb)


def integrate_pair(grid,first,second,kmin=None,kmax=None,method='cubic'):
    lower=grid[0] if kmin is None else kmin
    upper=grid[-1] if kmax is None else kmax
    assert np.min(first)>0 and np.min(second)>0
    coordinate=np.linspace(math.log(lower),math.log(upper),8193)
    chosen=np.exp(coordinate)
    interpolator=interpolate.CubicSpline if method=='cubic' else interpolate.PchipInterpolator
    first_spline=interpolator(np.log(grid),np.log(first),axis=0)
    second_spline=interpolator(np.log(grid),np.log(second),axis=0)
    primordial=previous.AS*(chosen/.05)**(previous.NS-1)
    window=top_hat(chosen*8/(previous.H0/100))**2
    integrand=(primordial*window)[:,None]*np.exp(first_spline(coordinate)+second_spline(coordinate))
    return integrate.simpson(integrand,x=coordinate,axis=0)


def summary(grid,columns,scales,method='cubic',kmin=None,kmax=None):
    late=scales>=.08
    columns={key:value[:,late] for key,value in columns.items()}
    scales=scales[late]
    options=dict(kmin=kmin,kmax=kmax,method=method)
    sigma_m=np.sqrt(integrate_pair(grid,columns['delta_m'],columns['delta_m'],**options))
    sigma_cb=np.sqrt(integrate_pair(grid,columns['delta_cb'],columns['delta_cb'],**options))
    fs_cdm_m=integrate_pair(grid,columns['velocity_cdm'],columns['delta_m'],**options)/sigma_m
    fs_cb_m=integrate_pair(grid,columns['velocity_cb'],columns['delta_m'],**options)/sigma_m
    fs_cb_cb=integrate_pair(grid,columns['velocity_cb'],columns['delta_cb'],**options)/sigma_cb
    sigma_vcb=np.sqrt(integrate_pair(grid,columns['velocity_cb'],columns['velocity_cb'],**options))
    rows=[]
    for redshift in TARGET_REDSHIFTS:
        center=-math.log1p(redshift)
        index=int(np.argmin(abs(np.log(scales)-center)))
        assert abs(math.log(scales[index])-center)<1e-12
        derivatives=[]
        for step in [.002,.001]:
            offsets=np.arange(-4,1) if redshift==0 else np.arange(-2,3)
            indices=[int(np.argmin(abs(np.log(scales)-(center+offset*step)))) for offset in offsets]
            coefficients=np.polynomial.polynomial.polyfit(offsets.astype(float),sigma_m[indices],4)
            derivatives.append(float(coefficients[1]/step))
        rows.append(dict(z=float(redshift),sigma8_m=float(sigma_m[index]),sigma8_cb=float(sigma_cb[index]),
            fsigma8_cdm_m=float(fs_cdm_m[index]),fsigma8_cb_m=float(fs_cb_m[index]),
            fsigma8_cb_cb=float(fs_cb_cb[index]),velocity_sigma8_cb=float(sigma_vcb[index]),
            d_sigma8m_d_lna=derivatives[-1],derivative_step_change=abs(derivatives[-1]-derivatives[0])))
    return rows


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('labels',nargs='+')
    parser.add_argument('--output',default='spectrum')
    args=parser.parse_args()
    folder=ROOT/'results'/args.output
    if folder.exists():
        assert not any(folder.iterdir()), 'Refusing to overwrite existing spectrum products'
    else:
        folder.mkdir(parents=True,exist_ok=False)
    reports=[]
    paths=[]
    for label in args.labels:
        data,columns=fields(label)
        grid=data['modes']
        coarse=np.isin(grid,modes(1))
        assert np.array_equal(grid[coarse],modes(1))
        trusted=grid<=5
        admitted=trusted&coarse
        central=summary(grid[trusted],{key:value[trusted] for key,value in columns.items()},data['scales'])
        variants=dict(coarse=summary(grid[admitted],{key:value[admitted] for key,value in columns.items()},data['scales']),
            pchip=summary(grid[trusted],{key:value[trusted] for key,value in columns.items()},data['scales'],method='pchip'),
            exploratory_kmax10=summary(grid,columns,data['scales']),
            kmax3=summary(grid[trusted],{key:value[trusted] for key,value in columns.items()},data['scales'],kmax=3),
            kmin1e4=summary(grid[trusted],{key:value[trusted] for key,value in columns.items()},data['scales'],kmin=1e-4))
        diagnostics=[]
        band=(grid>=.01*.7)&(grid<=.2*.7)
        for row in central:
            index=int(np.argmin(abs(data['scales']-1/(1+row['z']))))
            growth=columns['velocity_cb'][band,index]/columns['delta_cb'][band,index]
            diagnostics.append(dict(z=row['z'],RSD_like_band_Mpc_inverse=[.007,.14],
                effective_growth_min=float(min(growth)),effective_growth_max=float(max(growth)),
                fractional_growth_spread=float((max(growth)-min(growth))/np.mean(growth))))
        power=2*math.pi**2/grid[:,None]**3*previous.AS*(grid[:,None]/.05)**(previous.NS-1)*columns['delta_m']**2
        np.savez_compressed(folder/(label+'.npz'),modes=grid,scales=data['scales'],linear_power_Mpc3=power,
            pressure_qualified_band=trusted,**columns)
        changes={name:{key:max(abs(other[key]/base[key]-1) for base,other in zip(central,values))
            for key in ['sigma8_m','fsigma8_cdm_m','velocity_sigma8_cb']} for name,values in variants.items()}
        reports.append(dict(label=label,central=central,variants=variants,maximum_fractional_changes=changes,
            integral_cutoff_Mpc_inverse=5.,qualified_grid_count=int(trusted.sum()),
            growth_shape_diagnostics=diagnostics,k_count=len(grid),coarse_count=int(coarse.sum())))
        paths += [ROOT/'runs'/label/'status.json',ROOT/'runs'/label/'background.npz',
            *sorted((ROOT/'runs'/label).glob('chunk-*.npz'))]
        print(label,central[-1],changes,flush=True)
    finish(folder,dict(branches=reports,units=dict(k='Mpc^-1',power='Mpc^3',radius='8/h Mpc'),
        benchmark_only=True,stock_dark_slot_sigma8_not_used=True),__file__,[*paths,*folder.glob('*.npz')])


if __name__=='__main__':
    main()
