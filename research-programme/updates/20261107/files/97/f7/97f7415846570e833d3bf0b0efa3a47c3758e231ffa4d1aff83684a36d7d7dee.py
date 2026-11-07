from __future__ import annotations

from precision_common import *


def fields(label):
    folder=ROOT/'runs'/label
    packets=[np.load(path) for path in sorted(folder.glob('chunk-*.npz'))]
    values=np.concatenate([packet['values'] for packet in packets])
    modes=np.concatenate([packet['modes'] for packet in packets])
    names=packets[0]['names'].tolist()
    scales=packets[0]['requested_scale']
    report=json.loads((folder/'status.json').read_text())
    background=np.load(folder/'background.npz')
    cold,baryon,neutrino=[background[key] for key in ['cdm','baryon','nu']]
    combined=cold+baryon
    total=combined+neutrino
    delta_cb=(cold*values[:,:,names.index('delta_cdm')]+baryon*values[:,:,names.index('delta_baryon')])/combined
    numerator=combined*delta_cb+neutrino*values[:,:,names.index('delta_nu')]
    if report['branch']=='heavy':
        table=np.load(ROOT/'runs/projection'/(report['projection']+'.npz'))
        actual=values[0,:,names.index('a')]
        numerator+=actual**2*values[:,:,names.index('mts_drho_h')]
        total+=float(table['matching_density'])*actual
    velocity_cdm=values[:,:,names.index('v_newtonian_cdm')]
    velocity_cb=(cold*velocity_cdm+baryon*values[:,:,names.index('v_newtonian_baryon')])/combined
    return modes,scales,dict(delta_m=numerator/total,delta_cb=delta_cb,velocity_cdm=velocity_cdm,velocity_cb=velocity_cb)


def main():
    modest()
    folder=ROOT/'results/spectrum'
    folder.mkdir(parents=True,exist_ok=False)
    reports=[]
    paths=[]
    old_report=json.loads((SPECTRUM/'results/spectrum/status.json').read_text())
    for label in ['heavy','cold','heavy-200','heavy-250','heavy-window4']:
        modes,scales,columns=fields(label)
        trusted=modes<=5
        central=spectrum_summary(modes[trusted],{key:value[trusted] for key,value in columns.items()},scales)
        old_path=SPECTRUM/'results/spectrum'/(label+'.npz')
        old=np.load(old_path)
        assert np.array_equal(modes,old['modes']) and np.array_equal(scales,old['scales'])
        late=scales>=.08
        band=(modes>=.007)&(modes<=.14)
        changes={key:float(max(abs(columns[key][band][:,late]/old[key][band][:,late]-1).ravel())) for key in columns}
        old_branch=next(row for row in old_report['branches'] if row['label']==label)
        statistic_changes={key:max(abs(row[key]/old_row[key]-1) for row,old_row in zip(central,old_branch['central']))
            for key in ['sigma8_m','sigma8_cb','fsigma8_cdm_m','fsigma8_cb_m','velocity_sigma8_cb','d_sigma8m_d_lna']}
        power=2*math.pi**2/modes[:,None]**3*previous.AS*(modes[:,None]/.05)**(previous.NS-1)*columns['delta_m']**2
        output=folder/(label+'.npz')
        np.savez_compressed(output,modes=modes,scales=scales,linear_power_Mpc3=power,pressure_qualified_band=trusted,**columns)
        reports.append(dict(label=label,central=central,maximum_survey_band_transfer_changes=changes,
            maximum_statistic_changes=statistic_changes,trusted_kmax_Mpc_inverse=5.,
            survey_refit_trigger=bool(max(changes.values())>.005 or max(statistic_changes.values())>.001)))
        paths.extend([old_path,output,ROOT/'runs'/label/'status.json',ROOT/'runs'/label/'background.npz',*sorted((ROOT/'runs'/label).glob('chunk-*.npz'))])
        print(json.dumps(reports[-1]),flush=True)
    main_branch=reports[0]
    matching=[]
    for branch in reports[2:]:
        matching.append(dict(label=branch['label'],changes={key:max(abs(row[key]/base[key]-1) for row,base in zip(branch['central'],main_branch['central']))
            for key in ['sigma8_m','fsigma8_cdm_m','velocity_sigma8_cb']}))
    finish(folder,dict(branches=reports,matching_sensitivity=matching,lcdm_unchanged_control=str(SPECTRUM/'results/spectrum/lcdm.npz'),
        unchanged_primordial_normalization=True,stock_dark_slot_sigma8_not_used=True),__file__,paths+[SPECTRUM/'results/spectrum/status.json',SPECTRUM/'analyze_spectrum.py',SPECTRUM/'results/spectrum/lcdm.npz'])


if __name__=='__main__':
    main()
