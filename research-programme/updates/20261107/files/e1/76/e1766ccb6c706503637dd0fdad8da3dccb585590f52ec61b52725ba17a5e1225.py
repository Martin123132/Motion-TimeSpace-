from __future__ import annotations

from feedback_common import *
import urllib.request


def main():
    modest()
    folder=ROOT/'results/source-projection'
    folder.mkdir(parents=True,exist_ok=False)
    phase_rows=[]
    rng=np.random.default_rng(61)
    for index in range(12):
        mass=float(rng.uniform(.7,3.))
        scale=float(rng.uniform(.4,1.2))
        density=float(rng.uniform(.5,2.))
        gradient=rng.normal(size=3)*.03
        velocity=rng.normal(size=3)*.02
        expected=density*np.outer(velocity,velocity)+np.outer(gradient,gradient)/(4*mass**2*scale**2*density)
        expected-=np.eye(3)*np.trace(expected)/3
        for count in [64,128]:
            phase=2*math.pi*np.arange(count)/count
            derivatives=np.sqrt(2)/mass*(gradient[:,None]/(2*math.sqrt(density))*np.cos(phase)+
                math.sqrt(density)*mass*scale*velocity[:,None]*np.sin(phase))
            averaged=derivatives@derivatives.T/(count*scale**2)
            averaged-=np.eye(3)*np.trace(averaged)/3
            phase_rows.append(dict(case=index,count=count,max_absolute_error=float(np.max(abs(averaged-expected))),
                trace=float(np.trace(averaged))))
    feedback=json.loads((ROOT/'results/feedback/status.json').read_text())
    source_rows=[]
    for result in feedback['rows']:
        if result['branch']!='heavy':
            continue
        model=NativeSeed('heavy',result['k_Mpc_inverse'])
        endpoint=np.array(result['endpoint'])
        scale=math.exp(FINAL)
        hubble=math.exp(model.log_hubble(FINAL))
        density=endpoint[0,-1]
        velocity=endpoint[1,-1]
        velocity_part=(hubble/model.wave)**2*velocity**2
        gradient_part=model.wave**2*density**2/(4*model.mass**2*scale**2)
        source_rows.append(dict(k_Mpc_inverse=model.wave,
            canonical_hilbert_tracefree_xx_max_over_rho_per_amplitude_squared=2*(velocity_part+gradient_part)/3,
            velocity_part=velocity_part,gradient_part=gradient_part,
            phase_window_scope='Fixed slow envelope leading NR phase average, not all-order cosmological matching',
            metric_slip_inferred=False))
    sources=ROOT/'sources'
    sources.mkdir(exist_ok=False)
    records=[]
    urls=[
        ('nonrelativistic-real-field.html','https://arxiv.org/abs/1712.00445'),
        ('beyond-schrodinger-poisson.html','https://arxiv.org/html/2104.10128v1'),
        ('nonlinear-scalar-stress.html','https://arxiv.org/html/1707.08568v1')]
    for filename,url in urls:
        request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-research/1.0'})
        with urllib.request.urlopen(request,timeout=30) as response:
            content=response.read(8_000_001)
            assert len(content)<=8_000_000
            final_url=response.url
        path=sources/filename
        path.write_bytes(content)
        records.append(dict(url=url,final_url=final_url,path=str(path),bytes=len(content),sha256=digest(path),
            role='Primary methodological reference; no external code executed or theorem imported as MTS proof.'))
    finish(folder,dict(phase_rows=phase_rows,source_rows=source_rows,source_records=records,
        hilbert_momentum_flux_improvement_not_used_as_gravity_source=True),
        __file__,[ROOT/'results/feedback/status.json',*[Path(row['path']) for row in records]])
    print(json.dumps(dict(state='complete',phase_tests=len(phase_rows),max_phase_error=max(row['max_absolute_error'] for row in phase_rows),source_rows=source_rows)))


if __name__=='__main__':
    main()
