from vacuum_virtual import *


def main():
    modest()
    mp.mp.dps = 80
    for energy in ['0.00045962015785263325', '.1', '1', '9']:
        for cosine in ['-.9', '.1', '.6']:
            direct = brown_finite(energy, cosine)
            recast = recast_finite(energy, cosine)
            printed = recast_finite(energy, cosine, argument_scale=1)
            print(json.dumps(dict(energy=energy, cosine=cosine, brown=float(direct), recast=float(recast),
                printed_argument=float(printed), difference=float(recast-direct),
                finite_ratio=float(finite_virtual_ratio(energy, cosine)))), flush=True)


if __name__ == '__main__':
    main()
