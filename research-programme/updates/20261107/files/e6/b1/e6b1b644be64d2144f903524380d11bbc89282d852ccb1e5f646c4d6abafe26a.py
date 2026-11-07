from __future__ import annotations

from matching_common import *
from prepare_matching import project


def evolve(source, requested, modes=MODES):
    params = params_for(source)
    native = camb.get_background(params)
    times = native.conformal_time(1/requested-1,tol=1e-10)
    native.Params.Accuracy.IntTolBoost=6
    values = native.get_time_evolution(modes,times,vars=camb.model.evolve_names,lAccuracyBoost=4)
    return native, times, values


def main():
    modest()
    folder = ROOT/'runs/independent-probes'
    folder.mkdir(parents=True, exist_ok=False)
    source = ROOT/'runs/matching-inputs/a225-w6-d8.npz'
    names = camb.model.evolve_names
    original = np.load(REFERENCE)
    requested = original['requested_scale']
    native,times,values = evolve(source,requested)
    overlap = dict(values=values,names=np.array(names),modes=MODES)
    table = np.load(BACKGROUND)
    density0 = float(np.load(source)['matching_density'])
    native_rows, _ = project(overlap,table,.00025,density0,6,8)
    exact_rows, _ = project(original,table,.00025,density0,6,8)
    overlap_rows = []
    for actual, expected in zip(native_rows,exact_rows):
        overlap_rows.append(dict(k=actual['k'], delta_difference_over_mode_norm=
            abs(actual['delta']-expected['delta'])/expected['mode_norm'],
            momentum_difference_over_mode_norm=abs(actual['momentum']-expected['momentum'])/expected['mode_norm'],
            averaged=actual, exact_projected=expected))
    np.savez_compressed(folder/'overlap.npz',**overlap,requested_scale=requested,conformal_time=times)
    before = requested < .00018
    early = []
    for index,mode in enumerate(MODES):
        for column in ['delta_cdm','delta_baryon','delta_photon','delta_neutrino','etak']:
            new = values[index,before,names.index(column)]
            old = original['values'][index,before,original['names'].tolist().index(column)]
            early.append(dict(k=float(mode),column=column,normalized_change=float(np.max(abs(new-old))/max(np.max(abs(old)),1e-25))))
    residual_reports = []
    for count in [2001,4001]:
        requested = np.geomspace(.0003,1.,count)
        native,times,values = evolve(source,requested)
        scales = np.ascontiguousarray(values[0,:,names.index('a')])
        densities = native.get_background_densities(scales,vars=['cdm','baryon','photon','neutrino','nu'])
        densities = {key:value/scales**2 for key,value in densities.items()}
        efolds = np.log(scales)
        combined = densities['cdm']+densities['baryon']+densities['nu']
        per_mode = []
        for index,mode in enumerate(MODES):
            data = values[index]
            hubble = data[:,names.index('H')]
            density = data[:,names.index('mts_drho_h')]
            momentum = data[:,names.index('mts_q_h')]
            pressure = data[:,names.index('mts_dp_h')]
            cold = data[:,names.index('delta_cdm')]
            eta = data[:,names.index('etak')]
            pieces = [densities[key]*data[:,names.index(column)] for key,column in
                [('cdm','delta_cdm'),('baryon','delta_baryon'),('photon','delta_photon'),
                 ('neutrino','delta_neutrino'),('nu','delta_nu')]]
            pieces += [density,data[:,names.index('mts_drho_s')]]
            total = sum(pieces)
            reported = combined*data[:,names.index('delta_tot_de')]
            assembly = float(np.max(abs(total-reported)/np.maximum(np.sum(np.abs(pieces),axis=0),1e-30)))
            residuals = []
            for center in range(6,count-6,8):
                stencil = np.arange(center-5,center+6)
                coordinate = efolds[stencil]-efolds[center]
                span = max(abs(coordinate))

                def derivative(series):
                    return np.polynomial.polynomial.polyfit(coordinate/span,series[stencil],7)[1]/span

                d_density,d_momentum,d_cold = [derivative(series) for series in [density,momentum,cold]]
                background = density0/scales[center]
                energy_terms = np.array([d_density,density[center],3*pressure[center],
                    mode*momentum[center]/hubble[center],-background*d_cold])
                momentum_terms = np.array([d_momentum,2*momentum[center],-mode*pressure[center]/hubble[center]])
                constraint_terms = np.array([-hubble[center]**2*d_cold/mode,-total[center]/(2*mode),-eta[center]])
                residuals.append([float(abs(sum(terms))/max(sum(abs(terms)),1e-30))
                    for terms in [energy_terms,momentum_terms,constraint_terms]])
            per_mode.append(dict(k=float(mode),density_assembly_error=assembly,
                maximum_normalized_residuals=dict(zip(['heavy_energy','heavy_momentum','Hamiltonian'],
                    np.max(residuals,axis=0).tolist()))))
        np.savez_compressed(folder/f'dense-{count}.npz',values=values,names=names,modes=MODES,
            requested_scale=requested,conformal_time=times)
        residual_reports.append(dict(samples=count,rows=per_mode))
    requested = np.array([.0001,.0003,.001,.01,.1,1.])
    _,_,forward = evolve(source,requested)
    _,_,reverse = evolve(source,requested,MODES[::-1])
    order_error = float(np.max(abs(forward-reverse[::-1])/np.maximum(abs(forward),1e-20)))
    finish(folder,dict(overlap=overlap_rows,early_comparisons=early,residuals=residual_reports,
        reversed_mode_order_error=order_error,finite=True),__file__,
        [REFERENCE,BACKGROUND,source,ROOT/'prepare_matching.py',*native_hashes(),*folder.glob('*.npz')])
    print(json.dumps(dict(overlap=overlap_rows,maximum_early_error=max(row['normalized_change'] for row in early),
        residuals=residual_reports,mode_order_error=order_error),indent=2))


if __name__ == '__main__':
    main()
