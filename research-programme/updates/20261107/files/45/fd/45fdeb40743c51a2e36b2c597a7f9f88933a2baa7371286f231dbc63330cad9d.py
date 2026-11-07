from stage164_common import *


def main():
    modest()
    folder=ROOT/'results/validation-real'
    folder.mkdir(parents=True,exist_ok=False)
    packet=verify_packet(ROOT/'results/remaining-real-probe')
    checks=[]
    assert packet['all_checks_passed'] and packet['probes']==8 and not packet['source_adopted']
    rehashed={}
    for filename,sha in packet['input_hashes'].items():
        assert digest(filename)==sha,filename
        rehashed[filename]=sha
    checks.append(dict(name='Additional real-event probe packet and all consumed hashes',passed=True))
    improved=0
    for label,record in packet['records'].items():
        endpoint,order_tag,node_tag=label.split('-')
        path=moment_path(endpoint,int(order_tag[5:]),int(node_tag[4:]))
        source=read_npz(path)
        values=read_npz(ROOT/'results/remaining-real-probe'/(label+'.npz'))
        assert np.array_equal(values['old'],source['difference'])
        assert float(values['weight'])==float(source['weight'])
        old=abs(values['old'][0]+values['old'][-1])
        new=abs(values['new'][0]+values['new'][-1])
        assert np.array_equal(old,record['old_defect']) and np.array_equal(new,record['new_defect'])
        assert np.max(abs(values['new']-values['old']))/np.max(abs(values['old']))<=1e-10
        improved+=int(max(new)<max(old))
        assert not record['source_adopted']
        checks.append(dict(name='Independent saved real-source comparison:'+label,passed=True))
    assert improved==packet['improved_events']==7 and not packet['all_events_fixed']
    checks.append(dict(name='Residual event retained;no full-bank real-precision adoption',passed=True))
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    checks.append(dict(name='All current scripts compile without bytecode',passed=True))
    finish(folder,dict(checks=checks,additional_scientific_checks=packet['count'],improved_probe_events=improved,
        probe_events=8,full_bank_adoption=False,source_hashes=rehashed),__file__,[*rehashed,ROOT/'results/remaining-real-probe/status.json'])
    print(json.dumps(dict(checks=len(checks),passed=True,improved=improved,events=8)),flush=True)


if __name__=='__main__':
    main()
