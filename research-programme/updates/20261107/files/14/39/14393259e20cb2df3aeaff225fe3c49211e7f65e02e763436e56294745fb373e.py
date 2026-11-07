import argparse
import project_rectangular as runner
from log_rectangular import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--name', required=True)
    parser.add_argument('--radial', required=True, type=int)
    parser.add_argument('--source-run', required=True)
    arguments, unused = parser.parse_known_args()
    parent_packet = json.loads((PARENT / 'runs' / arguments.source_run / 'status.json').read_text())
    if arguments.radial == parent_packet['configuration']['soft_order']:
        raise ValueError('Use an explicitly distinct radial order for this changed quadrature control')
    folder = ROOT / 'runs' / arguments.name
    folder.mkdir(parents=True, exist_ok=True)
    method_path = folder / 'projection-method.json'
    method = dict(quadrature='logarithmic positive soft-energy panels',
                  fingerprints={str(path): digest(path) for path in [Path(__file__).resolve(), ROOT / 'log_rectangular.py']})
    if method_path.exists():
        assert json.loads(method_path.read_text()) == method
    else:
        write_json(method_path, method)
    original_finish = runner.finish
    def local_finish(folder, report, script, extra=()):
        report.update(quadrature_scheme=method['quadrature'],
                      energy_comparison_scope='Sensitivity relative to saved linear-soft-quadrature Stage91 energy, not identical quadrature.',
                      linear_source_superseded_only_after_vector_validation=True)
        original_finish(folder, report, script, [method_path, *extra])
    runner.Rectangular = LogRectangular
    runner.finish = local_finish
    runner.main()
