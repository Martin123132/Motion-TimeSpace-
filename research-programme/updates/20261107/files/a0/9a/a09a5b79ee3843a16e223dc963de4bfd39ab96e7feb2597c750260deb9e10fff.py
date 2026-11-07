from __future__ import annotations

from spectrum_common import *


def main():
    modest()
    folder=ROOT/'runs/native-control-integrals'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    for label in ['cold','lcdm']:
        params=inherited.params_for(EARLY/'runs/backgrounds/cold.npz')
        if label=='lcdm':
            params.DarkEnergy=camb.dark_energy.DarkEnergyFluid()
        params.set_matter_power(redshifts=TARGET_REDSHIFTS.tolist(),kmax=10,nonlinear=False,silent=True)
        params.Transfer.accurate_massive_neutrinos=True
        result=camb.get_results(params)
        row=dict(branch=label,redshifts=TARGET_REDSHIFTS.tolist(),sigma8=result.get_sigma8().tolist(),
            fsigma8_velocity_cdm_total=result.get_fsigma8().tolist())
        rows.append(row)
        transfer=result.get_matter_transfer_data()
        np.savez_compressed(folder/(label+'.npz'),redshifts=TARGET_REDSHIFTS,sigma8=result.get_sigma8(),
            fsigma8=result.get_fsigma8(),transfer=transfer.transfer_data)
        print(row,flush=True)
    finish(folder,dict(controls=rows,scope='Independent native k sampling and integrator; valid only for the two no-heavy controls.'),
        __file__,[EARLY/'runs/backgrounds/cold.npz',*folder.glob('*.npz')])


if __name__=='__main__':
    main()
