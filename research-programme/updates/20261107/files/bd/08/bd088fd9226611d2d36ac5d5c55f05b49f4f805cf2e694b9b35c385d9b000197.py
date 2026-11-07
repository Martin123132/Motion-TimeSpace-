from stage146_precision_common import *
from decimal import Decimal,localcontext
import argparse


def compensated_leading(spectra,theta,folder):
    leading=event_owner.leading
    tests=event_owner.TestFunctions(spectra.basis)
    panels,scalar_terms=[],[]
    prefactor=4*weak.source.ALPHA*theta**2/(3*np.pi*event_owner.I3)
    rule=PanelRule(.5)
    constants=np.array([1/spectra.basis.norms[0],-spectra.basis.mean/spectra.basis.norms[1]])
    def integrate_piece(anchor,anchor_weight,lower,upper,inverse,spontaneous):
        if upper<=lower:
            return
        soft,weights=rule(18,lower,upper)
        hard=np.full_like(soft,anchor) if inverse else anchor-soft
        seed=hard+soft if inverse else np.full_like(soft,anchor)
        left=tests.evaluate(soft)+tests.evaluate(hard)-tests.evaluate(seed)
        left[:,0]=0.
        left[:,1]=constants[0]
        left[:,2]=constants[1]
        right=spectra.functions(soft)[:,1:]+spectra.functions(hard)[:,1:]-spectra.functions(seed)[:,1:]
        density=.5*prefactor*anchor_weight*weights*seed**4*leading.gould(soft/seed)
        density/=np.expm1(seed)*(-np.expm1(-hard))*soft
        if inverse:
            density/=-np.expm1(-soft)
        elif not spontaneous:
            density/=np.expm1(soft)
        panels.append(-(left.T*density)@right)
        scalar_terms.append(density[:,None]*right)
    floor=1e-6
    for anchor,anchor_weight in event_owner.compact_rule(128,1e-5,24.):
        integrate_piece(anchor,anchor_weight,floor,anchor/2,False,True)
        boundaries=sorted({floor,anchor/2,anchor,60.,
                           *[scale for scale in [.1,.5,1.,2.,5.,10.,20.,40.] if floor<scale<60.]})
        for lower,upper in zip(boundaries[:-1],boundaries[1:]):
            if upper<=anchor/2*(1+1e-14):
                integrate_piece(anchor,anchor_weight,lower,upper,False,False)
            if upper<=anchor*(1+1e-14):
                integrate_piece(anchor,anchor_weight,lower,upper,True,False)
    panels=np.asarray(panels)
    scalar_terms=np.concatenate(scalar_terms)
    output=np.zeros((98,4))
    flat=panels.reshape(len(panels),-1)
    output[:-1]=np.array([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(97,4)
    scalar=np.array([math.fsum(scalar_terms[:,column]) for column in range(4)])
    with localcontext() as context:
        context.prec=60
        exact=[sum((Decimal.from_float(float(value)) for value in scalar_terms[:,column]),Decimal(0)) for column in range(4)]
        for index in range(2):
            coefficient=Decimal.from_float(float(constants[index]))
            output[index+1]=[float(-coefficient*value) for value in exact]
    np.savez_compressed(folder/'leading-terms.npz',panels=panels,scalar_terms=scalar_terms,
                        scalar=scalar,constants=constants)
    return output,dict(panels=len(panels),scalar_nodes=len(scalar_terms),
                       scalar_exact=[str(value) for value in exact])


def run(case,chain):
    folder=ROOT/'results/reaggregation'/case
    if (folder/'COMPLETE').exists():
        report=verify_packet(folder)
        assert report['all_checks_passed']
        return
    folder.mkdir(parents=True,exist_ok=False)
    spec=CASES[case]
    raw=raw_components(case)
    bundle=EpochBundle(FRACTIONS[case])
    theta=epoch_context(bundle)[0][0]['theta']
    mass=bundle.basis.mass
    checks,inputs,refined,diagnostics=[],[spec['raw'],ROOT/'results/preflight/status.json',*bundle.inputs],{},{}
    moment_rows=np.array([0,1,2,97])
    for part,keys in [('control',['control']),('expensive',['difference','virtual','state'])]:
        location=spec[part]
        paths=sorted((location/'nodes').rglob('*.npz'))
        assert len(paths)==spec[part+'_nodes']
        reference={key:np.zeros((98,4)) for key in keys}
        terms={key:[] for key in keys}
        with localcontext() as context:
            context.prec=60
            exact={key:[[Decimal(0) for column in range(4)] for index in moment_rows] for key in keys}
            for ordinal,path in enumerate(paths):
                inherited.inherited.verify_source(path,chain)
                saved=read_npz(path)
                identity=json.loads(str(saved['identity']))
                assert identity['index']==ordinal
                weight=float(saved['weight'])
                assert np.isfinite(weight) and weight>0
                weight_exact=Decimal.from_float(-weight)
                for key in keys:
                    value=saved[key]
                    assert value.shape==(98,4) and np.isfinite(value).all()
                    contribution=-weight*value
                    reference[key]+=contribution
                    terms[key].append(contribution)
                    for index,row in enumerate(moment_rows):
                        for column in range(4):
                            exact[key][index][column]+=weight_exact*Decimal.from_float(float(value[row,column]))
                inputs.append(path)
            for key in keys:
                assert np.array_equal(reference[key],raw[key]),(case,key)
                values=np.asarray(terms[key]).reshape(len(paths),-1)
                stable=np.array([math.fsum(values[:,column]) for column in range(values.shape[1])]).reshape(98,4)
                fsum_only=stable.copy()
                stable[moment_rows]=[[float(value) for value in row] for row in exact[key]]
                refined[key]=stable
                diagnostics[key]=dict(exact_moment_rows=[[str(value) for value in row] for row in exact[key]],
                    sequential_reproduced_exactly=True,node_count=len(paths),
                    full_source_change=(dual_norm((stable-raw[key])[1:-1],mass)/
                                        np.maximum(dual_norm(raw[key][1:-1],mass),1e-300)).tolist())
                np.savez_compressed(folder/(key+'-sums.npz'),sequential=reference[key],
                                    fsum=fsum_only,refined=stable,moment_rows=moment_rows)
                checks.append(dict(name='Exact saved sequential aggregate:'+case+':'+key,passed=True))
    refined['sampled_leading'],leading_metadata=compensated_leading(bundle.epochs[0],theta,folder)
    leading_change=dual_norm((refined['sampled_leading']-raw['sampled_leading'])[1:-1],mass)/dual_norm(raw['sampled_leading'][1:-1],mass)
    test(checks,'Leading same quadrature arithmetic change:'+case,np.max(leading_change),1e-10)
    assert np.array_equal(refined['sampled_leading'][[0,-1]],raw['sampled_leading'][[0,-1]])
    refined['kinematic_remainder']=refined['control']-refined['sampled_leading']
    with localcontext() as context:
        context.prec=60
        names=['control','sampled_leading','difference','virtual','state']
        signs=[1,-1,1,1,1]
        refined['remainder']=np.array([float(sum(
            (sign*Decimal.from_float(float(refined[name].flat[index])) for name,sign in zip(names,signs)),
            Decimal(0))) for index in range(98*4)]).reshape(98,4)
    source_change=dual_norm((refined['remainder']-raw['remainder'])[1:-1],mass)/dual_norm(raw['remainder'][1:-1],mass)
    test(checks,'Only small source arithmetic change:'+case,np.max(source_change),1e-10)
    np.savez_compressed(folder/'source.npz',**refined,mass=mass,temperature=bundle.basis.temperature,
                        chemical=bundle.basis.chemical)
    finish(folder,dict(checks=checks,case=case,fraction=FRACTIONS[case],theta=theta,
        diagnostics=diagnostics,leading_metadata=leading_metadata,
        leading_relative_change=leading_change.tolist(),source_relative_change=source_change.tolist(),
        no_projection_used=True,new_event_evaluations=0,new_loop_evaluations=0,
        reused_event_nodes=spec['control_nodes']+spec['expensive_nodes']),
        __file__,[*inputs,folder/'source.npz',folder/'leading-terms.npz'])
    print(json.dumps(dict(case=case,source_change=source_change.tolist(),
                         leading_change=leading_change.tolist(),checks=len(checks))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--cases',nargs='+',choices=list(CASES),default=list(CASES))
    args=parser.parse_args()
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    chain=ancestors()
    for case in args.cases:
        run(case,chain)
