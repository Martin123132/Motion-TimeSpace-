import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
PARENTS = {
    'precise': ('check_precise_compensated_source.py', '5b3932e9ad077bcdf78535255fa88a40f0d4c0b8397111941575b857c4669a2f'),
    'native': ('check_native_compensated_pairs.py', 'c42294cf440616e2b8becfacda9ece47d7d75bc5474dd757edddbac3072ff829'),
}
sys.dont_write_bytecode = True


def endpoint_guard():
    if datetime.now(timezone.utc) >= datetime(2026, 11, 2, 23, 40, tzinfo=timezone.utc):
        raise TimeoutError('Current turn safe-save deadline; no automatic retry')
    if 3 <= datetime.now(timezone.utc).astimezone(ZoneInfo('Europe/London')).hour < 14:
        raise RuntimeError('Music priority window; await release')
    if (ROOT.parent / 'execution-v3/STOP-REQUEST.json').exists():
        raise RuntimeError('Owner stop preserved')


def replace_once(source, previous, replacement):
    if source.count(previous) != 1:
        raise RuntimeError('Qualified source boundary changed: ' + previous)
    return source.replace(previous, replacement)


def source_text(mode):
    filename, expected = PARENTS[mode]
    content = (ROOT / filename).read_bytes()
    if hashlib.sha256(content).hexdigest() != expected:
        raise RuntimeError('Qualified parent changed: ' + filename)
    source = content.decode('utf-8').replace('\r\n', '\n')
    source = replace_once(source, "CONSUMER = ROOT / 'saved-epoch-cell424'",
                          "CONSUMER = ROOT / 'saved-epoch-cell450'")
    source = replace_once(source, 'def guard():\n', 'def guard():\n    endpoint_guard()\n')
    if mode == 'precise':
        source = replace_once(source, "DESTINATION = ROOT / 'compensated-epoch-source-001'",
                              "DESTINATION = ROOT / 'compensated-epoch-source-final450-001'")
        source = replace_once(source,
                              "load_verified_cell(ROOT.parent, 424, ROOT.parent / 'supervisor-cells417-424.json')",
                              "load_verified_cell(ROOT.parent, 450, ROOT.parent / 'supervisor-cells449-450.json')")
        if source.count('actual_history_cell=424') != 2:
            raise RuntimeError('History provenance fields changed')
        source = source.replace('actual_history_cell=424', 'actual_history_cell=450')
        source = replace_once(source, "    inputs.update(restart['inputs'])",
            "    inputs.update(restart['inputs'])\n"
            "    for final_input in (CONSUMER / 'manifest.json', CONSUMER / 'columns.npz', ROOT / 'run_final_epoch_qualification.py'):\n"
            "        inputs[str(final_input)] = digest(final_input)")
        source = replace_once(source,
            "previous_goal_turn='progress: event coupling derived, saved source verified, bounded cache qualified'",
            "previous_goal_turn='progress: full history450 completed and actual final source histories bound'")
    else:
        source = replace_once(source, "PARENT = ROOT / 'compensated-epoch-source-001'",
                              "PARENT = ROOT / 'compensated-epoch-source-final450-001'")
        source = replace_once(source, 'ast.parse(source.read_text()).body',
                              'ast.parse(endpoint_source_text()).body')
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=tuple(PARENTS))
    arguments = parser.parse_args()
    endpoint_guard()
    program = source_text(arguments.mode)
    compile(program, str(ROOT / PARENTS[arguments.mode][0]), 'exec')
    if arguments.mode == 'native':
        compile(source_text('precise'), str(ROOT / PARENTS['precise'][0]), 'exec')
    context = dict(__file__=str(ROOT / PARENTS[arguments.mode][0]), __name__='final_epoch_qualification',
                   endpoint_guard=endpoint_guard, endpoint_source_text=lambda: source_text('precise'))
    exec(compile(program, str(ROOT / PARENTS[arguments.mode][0]), 'exec'), context)
