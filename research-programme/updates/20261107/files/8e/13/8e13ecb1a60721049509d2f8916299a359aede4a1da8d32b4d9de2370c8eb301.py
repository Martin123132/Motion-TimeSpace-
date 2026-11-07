import argparse
from types import SimpleNamespace
from emission_common import *
import compare_backgrounds as engine


def local_finish(folder, report, script, extra):
    report.update(console_serialization_successor=True, mathematical_comparison_unchanged=True)
    finish(folder, report, __file__, [Path(script), *extra])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fine', required=True)
    parser.add_argument('--coarse', required=True)
    parser.add_argument('--name', required=True)
    engine.json = SimpleNamespace(loads=json.loads, dumps=lambda value: json.dumps(value, default=lambda item: item.item()))
    engine.finish = local_finish
    engine.main(parser.parse_args())
