import psutil
from mixed_nodes import *


def main():
    modest()
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            if Path(process.cwd()).resolve()==ROOT and any('project_mixed.py' in word for word in (process.info['cmdline'] or [])):
                raise RuntimeError('A source worker is still active; wait for its atomic saved-node exit.')
        except (psutil.AccessDenied,psutil.NoSuchProcess):
            continue
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    proof_path=ROOT/'results/mixed-proof/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    for filename,expected in proof['input_hashes'].items():
        assert digest(filename)==expected,filename
    rows,hashes,loop_hashes=[],{},{}
    for part in ['seed3']:
        for shard in [0,1]:
            folder=ROOT/'runs'/f'{part}-shard{shard}'
            config_path=folder/'configuration.json'
            if not config_path.exists():
                rows.append(dict(part=part,shard=shard,state='not_started',saved_nodes=0,total_nodes=2363-shard))
                continue
            config=json.loads(config_path.read_text())
            for filename,expected in config['fingerprints'].items():
                assert digest(filename)==expected,filename
            nodes=[identity for identity in physical_nodes(config['temperature'],3) if identity['index']%2==shard]
            paths=sorted((folder/'nodes').rglob('*.npz'))
            expected_paths=[folder/'nodes'/f"{identity['index']//500:03d}"/f"{identity['index']:05d}.npz" for identity in nodes[:len(paths)]]
            assert paths==expected_paths
            keys=['difference','virtual','state']
            for path,identity in zip(paths,nodes):
                saved=dict(np.load(path))
                assert json.loads(str(saved['identity']))==identity
                parameters,weight=parameters_and_weight(config['temperature'],identity)
                assert float(saved['weight'])>0 and np.isfinite(float(saved['weight']))
                assert abs(float(saved['weight'])/weight-1)<1e-13
                assert float(saved['event_energy_null'])<1e-10
                for key in keys:
                    assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
                hashes[path.relative_to(ROOT).as_posix()]=digest(path)
                if part=='seed3':
                    loop_path=Path(str(saved['loop_path']))
                    assert loop_path.is_relative_to(ROOT/'virtual-cache')
                    loop=json.loads(loop_path.read_text())
                    assert loop['identity']==virtual_identity(parameters) and loop['scalar']==float(saved['loop_scalar'])
                    assert loop['finite'] and np.isfinite(loop['scalar'])
                    loop_hashes[loop_path.relative_to(ROOT).as_posix()]=digest(loop_path)
            complete=(folder/'COMPLETE').exists()
            if complete:
                status_path=folder/'status.json'
                report=json.loads(status_path.read_text())
                assert report['all_checks_passed'] and len(paths)==report['nodes']==len(nodes)
                for filename,expected in report['input_hashes'].items():
                    assert digest(filename)==expected,filename
                hashes[status_path.relative_to(ROOT).as_posix()]=digest(status_path)
                hashes[(folder/'source.npz').relative_to(ROOT).as_posix()]=digest(folder/'source.npz')
                state='complete'
            else:
                progress=json.loads((folder/'progress.json').read_text())
                assert progress['state']=='paused_at_saved_node' and progress['completed_nodes']==len(paths)
                state='saved_partial'
            hashes[config_path.relative_to(ROOT).as_posix()]=digest(config_path)
            rows.append(dict(part=part,shard=shard,state=state,saved_nodes=len(paths),total_nodes=len(nodes),
                remaining_nodes=len(nodes)-len(paths)))
    assert not list(ROOT.rglob('*.tmp')) and not list(ROOT.rglob('__pycache__'))
    scripts={path.name:digest(path) for path in ROOT.glob('*.py')}
    for name in scripts:
        compile((ROOT/name).read_bytes(),str(ROOT/name),'exec')
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not changed,changed
    folder=ROOT/'results'/('partial-handoff-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    folder.mkdir(parents=True,exist_ok=False)
    report=dict(state='saved_partial_stage',saved_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SEAL,parent_payloads_reverified=len(parent['file_hashes']),rows=rows,
        node_and_packet_hashes=hashes,loop_hashes=loop_hashes,script_hashes=scripts,
        proof_sha256=digest(proof_path),derived_mixed_identity_checks=proof['count'],derived_mixed_identity_checks_passed=True,
        saved_node_shape_identity_weight_and_loop_checks_passed=True,current_workers_active=0,
        full_source_assembled=False,full_refined_frequency_response_compared=False,new_physical_history=False,new_empirical_fit=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='mtime scan since09:51:09UTC11October2026,not full content baseline.',
        next_action='Resume ONLY incomplete packets with unchanged project_mixed.py and configurations; do not rerun completed parts. Then audit/assemble/assess the missing coarse-frequency corner against the unchanged fine source,document actual outcomes,validate and seal.')
    write_json(folder/'handoff.json',report)
    (folder/'SAVED').write_text('safe partial handoff;not a completed source comparison\n',encoding='utf-8')
    print(json.dumps(dict(handoff_path=str(folder/'handoff.json'),handoff_sha256=digest(folder/'handoff.json'),
        **{key:report[key] for key in ['state','saved_utc','rows','derived_mixed_identity_checks','current_workers_active',
            'full_source_assembled','protected_workbench_recent_modified_file_count']})),flush=True)


if __name__=='__main__':
    main()
