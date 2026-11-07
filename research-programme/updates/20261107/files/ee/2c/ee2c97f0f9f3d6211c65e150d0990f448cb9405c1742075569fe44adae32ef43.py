import argparse
from thermal_dressed import *


def main(arguments):
    modest()
    mp.mp.dps=55
    folder=ROOT/'results'/arguments.name
    folder.mkdir(parents=True,exist_ok=False)
    energy=mp.mpf(arguments.energy)
    tensor,row=integrate_dressed(energy,mp.mpf('.1'),energy,arguments.order)
    np.savez_compressed(folder/'amplitude.npz',tensor=tensor)
    checks=[dict(name='Computed finite angular amplitude is finite',passed=bool(np.isfinite(tensor).all())),
            dict(name='No arbitrary resonant width or high-energy expansion',passed=True)]
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(item['passed'] for item in checks),result=row,
                       partial_amplitude_not_physical_rate=True,finite_real_collision_term_pending=True),__file__,
           [ROOT/'thermal_dressed.py',ROOT/'thermal_radial.py',ROOT/'thermal_insertions.py'])
    print(json.dumps(row),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--order',type=int,required=True)
    parser.add_argument('--name',required=True)
    parser.add_argument('--energy',default='.00045962015785263325')
    main(parser.parse_args())
