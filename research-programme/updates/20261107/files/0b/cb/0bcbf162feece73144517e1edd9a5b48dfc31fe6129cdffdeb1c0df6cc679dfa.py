import argparse
from wave_common import *
import build_infrared_ladder as engine


def main(arguments):
    engine.ROOT = ROOT
    def local_finish(folder, report, script, extra):
        dependencies = [PARENT / 'infrared_ladder.py' if path == ROOT / 'infrared_ladder.py' else path for path in extra]
        finish(folder, report, __file__, [Path(script), *dependencies])
    engine.finish = local_finish
    engine.main(arguments)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--count', type=int, default=104)
    parser.add_argument('--quadrature', type=int, default=700)
    parser.add_argument('--event-order', type=int, default=6)
    parser.add_argument('--minimum', type=float, default=1e-5)
    parser.add_argument('--pivot', type=float, default=.1)
    main(parser.parse_args())
