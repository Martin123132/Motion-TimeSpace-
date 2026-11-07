from pathlib import Path

from prepare_stable_real_pair_005_006 import EXPECTED, read, digest, require, verify


ROOT = Path(__file__).resolve().parent
PARENT = ROOT / 'run_stable_absorption_pair.py'
PREFLIGHT = ROOT / 'real-pair005-006-preflight.json'


def adapted_source():
    require(digest(PARENT) == EXPECTED[PARENT.name], 'Changed retained supervisor')
    record = read(PREFLIGHT)
    require(record['passed'] and record['rays'] == [5,6] and len(record['compiled']) == 12, 'Preflight required')
    verify(record['inputs'])
    source = PARENT.read_text()
    replacements = [
        ("read,digest,verify=original.read,original.digest,original.verify",
         "read,digest,verify=original.read,original.digest,original.verify\n"
         "FROZEN.update(pair_extra_frozen)"),
        ("    protected=dict(original_protocol['preserved_inputs'])",
         "    protected=dict(original_protocol['preserved_inputs'])\n"
         "    protected.update(read(ROOT/'real-pair005-006-preflight.json')['preserved_inputs'])"),
        ("    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]",
         "    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]\n"
         "    require(arguments.first==5,'This adapter is frozen for rays 5 and 6')"),
    ]
    for before,after in replacements:
        require(source.count(before)==1,'Changed adaptation boundary')
        source=source.replace(before,after)
    return source


if __name__ == '__main__':
    extras={PARENT.name:EXPECTED[PARENT.name],PREFLIGHT.name:digest(PREFLIGHT)}
    context=dict(__file__=str(Path(__file__)),__name__='__main__',pair_extra_frozen=extras)
    exec(compile(adapted_source(),str(PARENT),'exec'),context)
