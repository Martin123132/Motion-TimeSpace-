from common227 import *
import time

def positive_controls(values,depth=0):
    if np.min(values)>0:
        return True,depth,float(np.min(values))
    if depth==12:
        return False,depth,float(np.min(values))
    first=(values[:-1]+values[1:])/2
    second=(first[:-1]+first[1:])/2
    center=(second[0]+second[1])/2
    left=np.array([values[0],first[0],second[0],center])
    right=np.array([center,second[1],first[2],values[3]])
    left_result=positive_controls(left,depth+1)
    right_result=positive_controls(right,depth+1)
    return left_result[0] and right_result[0],max(left_result[1],right_result[1]),min(left_result[2],right_result[2])

def bank_audit(reference,rows):
    emission=reference.emission
    rates=np.array([emission.br_rates(theta) for theta in emission.temperatures])
    spline=interpolate.CubicSpline(np.log(emission.temperatures),rates,axis=0,extrapolate=False)
    records=[]
    for index in range(len(reference.br_values)):
        controls=np.array(bernstein(spline,index))
        positive,depth,minimum=positive_controls(controls)
        check(rows,f'BR cell{index}:positive scalar Bernstein representation',int(not positive),0,'passivity')
        error=0.
        for control,values in enumerate(controls):
            gram=(emission.values.T*(emission.measure*values))@emission.values
            original=reference.br_values[index][control]
            error=max(error,float(np.linalg.norm(gram-original)/max(np.linalg.norm(original),1e-300)))
        check(rows,f'BR cell{index}:matrix/scalar spline linearity',error,1e-10,'representation')
        records.append(dict(index=index,positive=positive,subdivision_depth=depth,minimum_rate_control=minimum,relative_matrix_difference=error))
    return records

def integrate_bounds(cells,group=1):
    area=mp.mpf(0);moment=mp.mpf(0);pair=mp.mpf(0)
    endpoint=mp.mpf(LAST)
    for first_index in range(0,len(cells),group):
        portion=cells[first_index:first_index+group]
        first=mp.mpf(portion[0]['first']);last=mp.mpf(portion[-1]['last'])
        norm=max(mp.mpf(cell['norm']) for cell in portion)
        injection=max(mp.mpf(cell['pair']) for cell in portion)
        width=last-first
        area+=width*norm
        moment+=width*(endpoint-(first+last)/2)*norm
        pair+=width*injection
    return area,moment,pair

def run(model,deadline):
    protocol()
    inputs=read(ROOT/'inputs.json')
    folder=ROOT/f'envelopes/{model}'
    if (folder/'complete.json').exists():
        print(json.dumps(dict(model=model,already_complete=True)),flush=True)
        return
    began=time.monotonic()
    with mp.workdps(80):
        reference=Reference(model,inputs)
        points=reference.pieces()
        if (folder/'restart.json').exists():
            restart=read(folder/'restart.json')
            assert restart['script_sha256']==digest(__file__)
            assert restart['points']==points
            rows=restart['checks'];cells=restart['cells'];audit=restart['bank_audit']
        else:
            rows=[];cells=[];audit=bank_audit(reference,rows)
        for index in range(len(cells),len(points)-1):
            first,last=points[index:index+2]
            bounds=reference.cell_bound(first,last)
            middle=(first+last)/2
            actual=reference.actual(middle)
            check(rows,f'cell{index}:actual force within continuous envelope',
                actual['norm']/max(bounds['norm'],mp.mpf('1e-300')),1+1e-10,'bound')
            check(rows,f'cell{index}:pair defect within continuous envelope',
                actual['pair']/max(bounds['pair'],mp.mpf('1e-300')),1+1e-10,'bound')
            check(rows,f'cell{index}:actual rate below radiation-only bound',
                actual['rate']/bounds['rate_bound'],1+1e-10,'bound')
            exact_compton=parent.matrix(reference.ladder.at(actual['theta'],0)[:96,:96])
            exact_br=parent.matrix(reference.emission.interpolator(math.log(actual['theta'])))
            decomposition=exact_compton-reference.dc_constant*mp.mpf(float(actual['theta']))**2*reference.dc-exact_br
            error=parent.norm(decomposition-actual['stiffness'])/max(parent.norm(actual['stiffness']),mp.mpf('1e-300'))
            check(rows,f'cell{index}:unchanged operator decomposition',error,1e-10,'identity')
            cells.append(dict(first=first,last=last,norm=mp.nstr(bounds['norm'],85),pair=mp.nstr(bounds['pair'],85),
                rate_bound=mp.nstr(bounds['rate_bound'],85),compton_nodes=bounds['compton_nodes'],br_index=bounds['br_index'],
                actual_midpoint_norm=float(actual['norm']),actual_midpoint_pair=float(actual['pair'])))
            if len(cells)%16==0 or index==len(points)-2:
                write(folder/'restart.json',dict(script_sha256=digest(__file__),points=points,cells=cells,checks=rows,bank_audit=audit))
                print(json.dumps(dict(model=model,cells=len(cells),total=len(points)-1,seconds=time.monotonic()-began,
                    failed=sum(not row['passed'] for row in rows))),flush=True)
                if index<len(points)-2 and datetime.now(timezone.utc)>=deadline:
                    return
        fine=integrate_bounds(cells)
        coarse=integrate_bounds(cells,2)
        metric=inherited.analytic_bound(reference.background,FIRST,LAST)
        gain=mp.mpf(float(metric['source_gain']))
        exponents=[]
        for group,values in ((1,fine),(2,coarse)):
            area,moment,pair=values
            exponent=gain*(reference.heat*pair+reference.heat**mp.mpf('1.5')*moment+reference.heat*reference.defect*area)
            exponents.append(exponent)
        check(rows,'nested envelope decreases causal exponent',exponents[0]/max(exponents[1],mp.mpf('1e-300')),1+1e-10,'bound')
        check(rows,'nested envelope refinement',abs(exponents[1]-exponents[0])/max(exponents[0],mp.mpf('1e-300')),.01,'refinement')
        for key,number in zip(('norm_area','norm_first_moment','pair_area'),fine):
            assert number>=0,key
        increase=mp.expm1(exponents[0])
        original=read(register(inputs,PREVIOUS/f'results/{model}.json'))
        combined=[]
        for record in original['records']:
            original_bound=mp.mpf(float(record['H_whole_attributed_bound']))
            combined.append(dict(**{key:record[key] for key in ('model','count','profile','grid','component','join')},
                prescribed_source_bound=float(original_bound),return_amplification_excess=float(increase),
                return_bound_addition=float(original_bound*increase),closed_rate_channel_bound=float(original_bound*(1+increase))))
        result=dict(model=model,checks=rows,failed_checks=[row for row in rows if not row['passed']],
            reference_path=str(reference.history_path),interval=[FIRST,LAST],cells=len(cells),bank_audit=audit,
            force_norm_integral=float(fine[0]),force_norm_first_moment=float(fine[1]),pair_defect_integral=float(fine[2]),
            heat=float(reference.heat),energy_moment_defect=float(reference.defect),uniform_gravity_gain=float(gain),
            fine_causal_exponent=float(exponents[0]),coarse_causal_exponent=float(exponents[1]),
            amplification_excess=float(increase),records=combined,finished_at=now(),seconds=time.monotonic()-began,
            scope='Continuous envelope of retained linearly interpolated original history and original matrix bank; metric-rate return channel',
            microscopic_continuum_accuracy_certified=False,all_higher_order_thermal_terms_closed=False)
        result['qualified']=not result['failed_checks']
        write(folder/'complete.json',result)
        write(ROOT/f'inputs-{model}.json',inputs)
        print(json.dumps(dict(model=model,complete=True,checks=len(rows),failed=len(result['failed_checks']),
            exponent=float(exponents[0]),increase=float(increase),seconds=time.monotonic()-began)),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=parent.MODELS,required=True)
    parser.add_argument('--stop-at',default='2026-10-26T20:00:00+00:00')
    args=parser.parse_args()
    run(args.model,datetime.fromisoformat(args.stop_at))

