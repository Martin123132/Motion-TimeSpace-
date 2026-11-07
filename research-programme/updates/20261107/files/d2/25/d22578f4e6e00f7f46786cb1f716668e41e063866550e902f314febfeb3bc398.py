from ordered_real_kernel import *


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/separator-and-resolution'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    input_paths=[ROOT/'results'/name/'status.json' for name in ['ordered-real-a8-r24','ordered-real-a12-r40','ordered-real-a16-r56']]
    packets=[json.loads(path.read_text()) for path in input_paths]
    for index,high in enumerate(packets[-1]['rows']):
        for field in ['matched_ratio','finite_real_remainder','upper_log_term','integrated_pole']:
            for level in [0,1]:
                low=packets[level]['rows'][index]
                checks.append(check('Angular/radial refinement '+field+' E='+str(high['energy'])+' c='+str(high['cosine'])+' level='+str(level),
                    abs(low[field]-high[field])/max(abs(high[field]),1e-30),1e-8))
    for energy,cosine in [('0.00045962015785263325','.1'),('.1','-.8')]:
        reference=integrate_ordered(energy,cosine,10,32)
        coefficient=reference['analytic_pole']
        errors=[]
        for share in ['.01','.001','.0001']:
            lower=mp.mpf(energy)*mp.mpf(share)
            result=integrate_ordered(energy,cosine,10,32,lower)
            assembled=float(matched_soft_ratio(energy,cosine,lower))+result['resolved_real_above']
            checks.append(check('Subtracted and sliced assembly agree E='+energy+' share='+share,abs(assembled-result['matched_ratio'])/coefficient,1e-10))
            error=abs(result['matched_ratio']-reference['matched_ratio'])/coefficient
            errors.append(error)
            checks.append(check('Finite unmatched interval shrinks with separator E='+energy+' share='+share,error,4*float(share)))
            rows.append(dict(**result,cutoff_share=float(share),separator_error_in_cusp_units=error,reference_ratio=reference['matched_ratio']))
        checks.append(dict(name='Linear separator convergence E='+energy,passed=errors[1]<.15*errors[0] and errors[2]<.15*errors[1],errors=errors))
        checks.append(dict(name='Real-only number count retains soft logarithm E='+energy,passed=rows[-1]['resolved_real_above']>rows[-2]['resolved_real_above']>rows[-3]['resolved_real_above']))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
        numerical_gate_scope='Nine unpolarized vacuum differential hardest-photon samples, three refinements and two separator sequences; not all-energy proof or thermal accuracy certificate',
        photon_number_creation_not_cancelled=True),__file__,[ROOT/'ordered_real_kernel.py',ROOT/'vacuum_virtual.py',*input_paths])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
