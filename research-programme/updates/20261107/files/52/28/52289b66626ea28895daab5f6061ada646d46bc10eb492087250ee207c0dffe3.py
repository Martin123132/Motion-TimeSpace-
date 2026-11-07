from __future__ import annotations

import numpy as np
from stage_common import *

sys.path.insert(0, str(PARENT))
import native_common as original


def main():
    modest()
    folder = ROOT/'runs/prior-native-controls'
    folder.mkdir(parents=True, exist_ok=False)
    rows = []
    for label in ['late-cold','late-lcdm']:
        data = np.load(ROOT/'runs'/label/'evolution.npz')
        params = original.params_for(PARENT/'runs/backgrounds/cold.npz', accuracy=2.5, initial_time_factor=.5)
        params.Accuracy.BackgroundTimeStepBoost=8
        if label=='late-lcdm':
            params.DarkEnergy=original.camb.dark_energy.DarkEnergyFluid()
        native = original.camb.get_background(params)
        times = native.conformal_time(1/data['requested_scale']-1,tol=1e-10)
        native.Params.Accuracy.IntTolBoost=6
        values = native.get_time_evolution(data['modes'],times,vars=original.camb.model.evolve_names,lAccuracyBoost=4)
        np.savez_compressed(folder/(label+'.npz'),values=values,names=original.camb.model.evolve_names)
        difference = abs(values-data['values'][:,:,:34])
        norm = np.maximum(np.max(abs(values),axis=1,keepdims=True),1e-25)
        rows.append(dict(label=label, maximum_column_normalized_error=float(np.max(difference/norm))))
    finish(folder,dict(controls=rows,source_library=original.camb.__file__),__file__,
        [PARENT/'native/camb/cambdll.dll',PARENT/'native_common.py',PARENT/'runs/backgrounds/cold.npz',
         ROOT/'runs/late-cold/evolution.npz',ROOT/'runs/late-lcdm/evolution.npz',*folder.glob('*.npz')])
    print(json.dumps(rows,indent=2))


if __name__ == '__main__':
    main()
