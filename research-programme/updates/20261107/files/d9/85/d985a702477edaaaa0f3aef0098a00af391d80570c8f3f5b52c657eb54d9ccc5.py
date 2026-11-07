import sys
from datetime import datetime, timezone
from pathlib import Path

from prepare_stable_real_pair_021_022 import EXPECTED, read, digest, require, require_music_handover, verify


ROOT = Path(__file__).resolve().parent
PARENT = ROOT / 'run_stable_absorption_pair.py'
PREFLIGHT = ROOT / 'real-pair021-022-preflight.json'


def open_campaign(folder):
    if EARLY:
        folder.mkdir()
    else:
        require(folder.is_dir() and all((folder/name).is_file() for name in ('pre-music-end.json','pre-music-integrity.json'))
                and not any((folder/name).exists() for name in ('post-music-supervisor.json','end.json')),
                'Only the verified, intentionally sealed first half may be continued once')


def session_protocol(folder, writer, proposed):
    if EARLY:
        writer(folder/'protocol.json', dict(proposed, phase_layout='21 before music, 22 after handover'))
        return
    from verify_stable_real_pair_021_022 import adapted_check
    earlier = read(folder/'protocol.json')
    require(all(proposed[key] == earlier[key] for key in proposed if key not in ('started','stop_utc','process')),
            'Frozen pair controls changed across handover')
    sealed = read(folder/'pre-music-integrity.json')
    check = adapted_check(partial=True)
    require(sealed['passed'] and check['passed'] and all(sealed[key]==check[key] for key in ('campaign_end_sha256','rays','verified_files','actual_child_exits')),
            'Pre-music acceptance changed')
    writer(folder/'post-music-supervisor.json', dict(process=proposed['process'],started=proposed['started'],stop_utc=proposed['stop_utc'],
           first_end_sha256=digest(folder/'pre-music-end.json'),first_integrity_sha256=digest(folder/'pre-music-integrity.json')))


def initial_receipts(folder):
    if EARLY:
        return [], []
    sealed = read(folder/'pre-music-end.json')
    require(sealed['state']=='sealed-before-music' and sealed['failure'] is None and sealed['completed_rays']==[21], 'Not a clean handover')
    return list(sealed['runs']), [21]


def adapted_source():
    require(digest(PARENT) == EXPECTED[PARENT.name], 'Changed retained supervisor')
    record = read(PREFLIGHT)
    require(record['passed'] and record['rays'] == [21,22] and len(record['compiled']) == 12, 'Preflight required')
    verify(record['inputs'])
    source = PARENT.read_text()
    replacements = [
        ("guard(); campaign.mkdir()", "guard(); open_campaign(campaign)"),
        ("write(campaign/'protocol.json',dict(started=now()", "session_protocol(campaign,write,dict(started=now()"),
        ("runs=[]; completed=[]; failure=None", "runs,completed=initial_receipts(campaign); failure=None"),
        ("        for ray in rays:\n            qualified=", "        for ray in ((21,) if EARLY else (22,)):\n            qualified="),
        ("write(campaign/'end.json',dict(state='complete' if failure is None else 'stopped'",
         "write(campaign/('pre-music-end.json' if EARLY else 'end.json'),dict(state=('sealed-before-music' if EARLY else 'complete') if failure is None else 'stopped'"),
        ("read,digest,verify=original.read,original.digest,original.verify",
         "read,digest,verify=original.read,original.digest,original.verify\n"
         "FROZEN.update(pair_extra_frozen)"),
        ("    protected=dict(original_protocol['preserved_inputs'])",
         "    protected=dict(original_protocol['preserved_inputs'])\n"
         "    protected.update(read(ROOT/'real-pair021-022-preflight.json')['preserved_inputs'])"),
        ("    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]",
         "    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]\n"
         "    require(arguments.first==21,'This adapter is frozen for rays 21 and 22')"),
    ]
    for before,after in replacements:
        require(source.count(before)==1,'Changed adaptation boundary')
        source=source.replace(before,after)
    return source


if __name__ == '__main__':
    require_music_handover()
    EARLY=datetime.now(timezone.utc) < datetime(2026,11,6,14,tzinfo=timezone.utc)
    continuation='--resume-after-music' in sys.argv
    if continuation:
        sys.argv.remove('--resume-after-music')
    if sys.argv[1]=='batch':
        require(continuation != EARLY, 'Use ordinary batch before music; explicit --resume-after-music after handover')
    if EARLY:
        deadline=datetime.fromisoformat(sys.argv[sys.argv.index('--stop-utc')+1].replace('Z','+00:00'))
        require(deadline.tzinfo is not None and datetime.now(timezone.utc)<deadline<=datetime(2026,11,6,2,50,tzinfo=timezone.utc), 'Pre-music deadline exceeded')
        require('--ray' not in sys.argv or int(sys.argv[sys.argv.index('--ray')+1])==21, 'Only ray 21 is authorized before music')
    extras={PARENT.name:EXPECTED[PARENT.name],PREFLIGHT.name:digest(PREFLIGHT)}
    context=dict(__file__=str(Path(__file__)),__name__='__main__',pair_extra_frozen=extras,EARLY=EARLY,
                 open_campaign=open_campaign,session_protocol=session_protocol,initial_receipts=initial_receipts)
    exec(compile(adapted_source(),str(PARENT),'exec'),context)
