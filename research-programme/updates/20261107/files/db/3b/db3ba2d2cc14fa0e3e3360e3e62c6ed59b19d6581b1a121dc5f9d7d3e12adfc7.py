from spatial_defect_common import *
import mpmath as mp


def main():
    modest()
    folder=ROOT/'results/preflight'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    points=np.array([2e-5,.0001,.001,.01,.02,.04,.05])
    jets=basis_jets(basis,points)
    checks=[check('Values match saved basis',np.max(abs(jets[0]-basis.evaluate(points)))/np.max(abs(jets[0])),1e-10),
        check('First derivatives match saved recurrence',np.max(abs(jets[1]-basis.derivative(points)))/np.max(abs(jets[1])),1e-10)]
    mp.mp.dps=80
    def reference(frequency,degree):
        values=[mp.mpf(1)/float(basis.norms[0]),(frequency-float(basis.mean))/float(basis.norms[1])]
        compact=(frequency-basis.pivot)/(frequency+basis.pivot)
        for column in range(2,degree+1):
            value=compact*values[-1]
            for repeat in range(2):
                value-=sum(mp.mpf(float(basis.projections[column,repeat,index]))*values[index] for index in range(column))
            values.append(value/float(basis.norms[column]))
        return values[degree]
    reference_rows=[]
    for point_index in [1,5]:
        point=float(points[point_index])
        for degree in [0,1,2,15,47,95]:
            for order in range(4):
                exact=float(mp.diff(lambda frequency:reference(frequency,degree),mp.mpf(point),order))
                scale=max(abs(exact),float(np.max(abs(jets[order,point_index])))*1e-12,1e-300)
                error=abs(jets[order,point_index,degree]-exact)/scale
                checks.append(check(f'80digit derivative:{point_index}:{degree}:{order}',error,1e-9))
                reference_rows.append(dict(point=point,degree=degree,order=order,reference=exact,relative=error))
    for inverse in [mp.mpf('0.93'),mp.mpf('1.02'),mp.mpf('1.11')]:
        first,second=inverse+mp.mpf('.0007'),inverse-mp.mpf('.0003')
        variance=(first-inverse)*(inverse-second)
        third=variance*(first+second-2*inverse)
        fraction=(inverse-second)/(first-second)
        for power in [0,1,2]:
            function=lambda value:(value**(1-power)-value+value**(2+power)-value**2)/2
            full=fraction*function(first)+(1-fraction)*function(second)-function(inverse)
            approximation=variance*mp.diff(function,inverse,2)/2+third*mp.diff(function,inverse,3)/6
            if power<=1:
                checks.append(check(f'Exact moment polynomial:{inverse}:{power}',float(abs(full-approximation)),1e-70))
            else:
                fourth_bound=max(abs(mp.diff(function,value,4)) for value in [first,second])
                fourth=(fraction*(first-inverse)**4+(1-fraction)*(second-inverse)**4)*fourth_bound/24
                checks.append(dict(name='Scalar fourth remainder bound:'+str(inverse),passed=bool(abs(full-approximation)<=fourth)))
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,reference_rows=reference_rows,precision_digits=80,
        full_basis_count=96),__file__,ladder.inputs)
    print(json.dumps(dict(checks=len(checks),max_derivative_error=max(row['relative'] for row in reference_rows))),flush=True)


if __name__=='__main__':
    main()
