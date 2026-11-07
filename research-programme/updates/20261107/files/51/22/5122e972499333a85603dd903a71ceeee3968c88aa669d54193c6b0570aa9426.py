from direct_common import *


def integrate_panels(function,edges,order=32):
    nodes,weights=special.roots_legendre(order)
    total=0.
    for lower,upper in zip(edges[:-1],edges[1:]):
        frequency=(upper+lower)/2+(upper-lower)/2*nodes
        total+=(upper-lower)/2*np.sum(weights*function(frequency))
    return float(total)


def main():
    modest()
    folder=ROOT/'results/identities'
    folder.mkdir(parents=True,exist_ok=False)
    lower,upper=2e-5,.04
    def compact(frequency):
        coordinate=(frequency-lower)/(upper-lower)
        return np.where((coordinate>0)&(coordinate<1),coordinate**3*(1-coordinate)**3,0.)
    checks,rows=[],[]
    for ratio in [.91,1.,1.07]:
        edges=sorted(set([lower,upper,lower/ratio,upper/ratio]))
        for degree in [0,1,2,3]:
            potential=lambda frequency:frequency**degree
            weak=-integrate_panels(lambda frequency:(potential(ratio*frequency)-potential(frequency))*(compact(ratio*frequency)-compact(frequency)),edges)/(2*I3*ratio)
            adjoint=integrate_panels(lambda frequency:compact(frequency)*(potential(ratio*frequency)-potential(frequency)+(potential(frequency/ratio)-potential(frequency))/ratio),[lower,upper])/(2*I3*ratio)
            error=abs(weak-adjoint)/max(abs(weak)+abs(adjoint),1e-300)
            checks.append(check(f'Independent weak/adjoint equivalence r{ratio}degree{degree}',error,1e-8))
            rows.append(dict(ratio=ratio,degree=degree,weak=weak,adjoint=adjoint,relative_error=error))
        quadratic=-integrate_panels(lambda frequency:(compact(ratio*frequency)-compact(frequency))**2,edges)/(2*I3*ratio)
        checks.append(dict(name=f'Nonpositive compact quadratic form r{ratio}',value=quadratic,passed=quadratic<=0))
    finish(folder,dict(checks=checks,rows=rows,physical_fit_parameters=0),__file__)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

