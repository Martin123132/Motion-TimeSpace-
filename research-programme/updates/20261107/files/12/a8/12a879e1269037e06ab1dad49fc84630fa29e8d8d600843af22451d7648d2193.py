import mpmath as mp
from shape_common import *


def band_moments(lower,upper,precision):
    with mp.workdps(precision):
        lower,upper=mp.mpf(str(lower)),mp.mpf(str(upper))
        beta=3*mp.zeta(3)/mp.zeta(2)
        normalization=mp.pi**4/15
        def occupation(value):
            return 1/mp.expm1(value)
        def weight(value):
            result=occupation(value)
            return result*(1+result)
        def tail(order,value):
            return sum(mp.factorial(order)/mp.factorial(degree)*value**degree*
                mp.polylog(order-degree+1,mp.exp(-value)) for degree in range(order+1))
        def moment(order):
            return lower**order*occupation(lower)-upper**order*occupation(upper)+order*(tail(order-1,lower)-tail(order-1,upper))
        number_mu=(moment(3)/beta-moment(2))/normalization
        number_y=(lower**4*weight(lower)-upper**4*weight(upper))/normalization
        energy_mu=(moment(4)/beta-moment(3))/normalization
        energy_y=(lower**5*weight(lower)-upper**5*weight(upper)+
            lower**4*occupation(lower)-upper**4*occupation(upper)+4*(tail(3,lower)-tail(3,upper)))/normalization
        capacity=moment(4)/normalization
        return np.array([float(value) for value in [number_mu,number_y,energy_mu,energy_y,capacity]])


def main():
    modest()
    folder=ROOT/'results/finite-band-controls'
    folder.mkdir(parents=True,exist_ok=False)
    source=ROOT/'results/decomposition/status.json'
    report=json.loads(source.read_text())
    for path,expected in report['input_hashes'].items():
        assert digest(path)==expected,path
    failures=[row for row in report['checks'] if not row['passed']]
    assert {row['name'] for row in failures}=={
        'Standard mu and y number-preserving Planck moments:'+name for name in ['canonical700','full1400','full2100']}
    checks,rows,inputs=[],{},[source,ROOT/'FINITE-BAND-MOMENTS.md']
    for name,metadata in report['readouts'].items():
        path=ROOT/'results/decomposition'/f'{name}-definition.npz'
        inputs.append(path)
        with np.load(path) as saved:
            frequency,measure,standard=saved['frequency'],saved['measure'],saved['standard']
            actual=np.r_[measure@standard,(measure*frequency)@standard,np.sum(measure*frequency**2)]
        expected55=band_moments(metadata['minimum'],metadata['maximum'],55)
        expected75=band_moments(metadata['minimum'],metadata['maximum'],75)
        agreement=float(np.max(abs(expected55-expected75)))
        checks.append(dict(name='55 versus75 digit analytic boundary expressions:'+name,
            value=agreement,limit=1e-14,passed=agreement<1e-14))
        defect=abs(actual-expected75)
        checks.append(dict(name='Correct finite-band number identity at unchanged1e-8 gate:'+name,
            value=float(defect[:2].max()),limit=1e-8,passed=bool(defect[:2].max()<1e-8)))
        checks.append(dict(name='All five finite-band moments at stronger1e-10 gate:'+name,
            value=float(defect.max()),limit=1e-10,passed=bool(defect.max()<1e-10)))
        shifts=expected75[2:4]/expected75[4]
        error=float(np.max(abs(shifts-np.array(metadata['energy_shifts']))))
        checks.append(dict(name='Independent analytic energy matching agrees:'+name,
            value=error,limit=1e-10,passed=error<1e-10))
        rows[name]=dict(actual=actual.tolist(),analytic=expected75.tolist(),absolute_defects=defect.tolist(),
            energy_shifts=shifts.tolist(),mu_number_leading_boundary=metadata['minimum']/I3)
    finish(folder,dict(checks=checks,moments=rows,
        moment_order=['N_mu','N_y','E_mu','E_y','C_T'],retained_raw_failures=failures,
        decomposition_recomputed=False,templates_changed=False,thresholds_relaxed=False,
        failed_initial_zero_moment_assumption_corrected=True,source_evaluations=0,
        actual_increment_tail_derived=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        largest_moment_error=max(max(row['absolute_defects']) for row in rows.values()),
        canonical=rows['canonical700'])),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__=='__main__':
    main()

