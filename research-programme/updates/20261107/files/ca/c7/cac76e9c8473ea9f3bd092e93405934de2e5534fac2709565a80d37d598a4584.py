from coefficient_common import *


def main():
    checks,failed,rows,hashes=[],{},[],{}
    paths=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent.name!='validation')
    assert len(paths)==12
    for path in paths:
        packet=local_packet(path.parent)
        checks.extend(packet['checks'])
        names=[row['name'] for row in packet['checks'] if not row['passed']]
        if names:
            failed[path.parent.name]=names
        hashes[str(path)]=digest(path)
        copied={key:value for key,value in packet.items() if key not in ['checks','input_hashes']}
        if 'variants' in copied:
            copied['variants']={name:{key:value for key,value in variant.items() if key!='source_diagnostic'} for name,variant in copied['variants'].items()}
        rows.append(dict(packet=path.parent.name,**copied))
    categories={}
    for row in checks:
        if not row['passed']:
            category=row['name'].split(':')[0]
            categories[category]=categories.get(category,0)+1
    summary=dict(stage=129,checks=len(checks),passes=sum(row['passed'] for row in checks),
        retained_failed_checks=sum(not row['passed'] for row in checks),expected_failed_by_packet=failed,
        failure_categories=categories,rows=rows,source_packet_hashes=hashes,
        scope='Saved-event33-temperature Compton refinement and derived positive reciprocal-pair moment repair;paired640-step prefix replays and explicitly local139-knot source splice.',
        later_state_carried=False,new_temperature_integrals=0,new_inner_steps=3840,frequency_nodes=5265,response_steps=2048)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(checks=summary['checks'],passes=summary['passes'],failures=summary['retained_failed_checks'],categories=categories)),flush=True)
    for row in rows:
        if row['packet'].startswith('replay-'):
            print(json.dumps({key:row[key] for key in ['packet','endpoint_defect_relative','solve_errors']}),flush=True)
        if row['packet'].startswith('feedback-'):
            print(json.dumps(dict(packet=row['packet'],variants={name:dict(reference=value['reference'],
                endpoint=value['comparison']['gas_endpoint_relative'],peak=value['comparison']['gas_peak_relative'],
                radiation=value['comparison']['radiation_relative'],signed_endpoint=value['comparison']['gas_endpoint'],
                signs=value['comparison']['endpoint_sign_preserved']) for name,value in row['variants'].items()})),flush=True)


if __name__=='__main__':
    main()
