from quadrature_common import *
from paired_adjoint import paired_difference
import mpmath as mp
import time


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/arithmetic-proof'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    physical=[]
    for label in [40,20]:
        path=PARENT/'results'/f'operator-m{label}/event-00020.npz'
        event=read_npz(path)
        inputs.append(path)
        physical.extend([float(event['ratios'].min()),float(event['ratios'].max()),
            float(event['ratios'][np.argmin(abs(event['ratios']-1))])])
    ratios=np.array(sorted(set(physical+[1.,1.-1e-12,1.+1e-12,1.-1e-8,1.+1e-8,1.-1e-4,1.+1e-4])))
    frequency=np.array([2.1e-5,.0003,.01,.039])
    paired=paired_difference(basis,frequency,ratios)
    base=basis.evaluate(frequency)
    legacy=basis.evaluate(ratios[:,None]*frequency)-base
    legacy+=(basis.evaluate(frequency/ratios[:,None])-base)/ratios[:,None,None]
    mp.mp.dps=80
    norms=[mp.mpf(float(value)) for value in basis.norms]
    pivot,mean=mp.mpf(float(basis.pivot)),mp.mpf(float(basis.mean))
    projections=[[[mp.mpf(float(value)) for value in basis.projections[degree,repeat,:degree]]
        for repeat in range(2)] for degree in range(basis.count)]
    def evaluate(argument):
        compact=(argument-pivot)/(argument+pivot)
        values=[1/norms[0],(argument-mean)/norms[1]]
        for degree in range(2,basis.count):
            value=compact*values[degree-1]
            for repeat in range(2):
                value-=mp.fsum(coefficient*entry for coefficient,entry in zip(projections[degree][repeat],values))
            values.append(value/norms[degree])
        return values
    rows,reference=[],np.zeros_like(paired)
    checks=[]
    for ratio_index,ratio in enumerate(ratios):
        multiplier=mp.mpf(float(ratio))
        for frequency_index,position in enumerate(frequency):
            argument=mp.mpf(float(position))
            base_mp=evaluate(argument)
            forward=evaluate(argument*multiplier)
            backward=evaluate(argument/multiplier)
            expected=[positive-centre+(negative-centre)/multiplier for positive,negative,centre in zip(forward,backward,base_mp)]
            denominator=max(max(abs(value) for value in expected),mp.mpf('1e-300'))
            paired_error=max(abs(mp.mpf(float(value))-exact) for value,exact in zip(paired[ratio_index,frequency_index],expected))/denominator
            legacy_error=max(abs(mp.mpf(float(value))-exact) for value,exact in zip(legacy[ratio_index,frequency_index],expected))/denominator
            reference[ratio_index,frequency_index]=[float(value) for value in expected]
            rows.append(dict(ratio=float(ratio),frequency=float(position),paired_relative_error=float(paired_error),
                legacy_relative_error=float(legacy_error),reference_max=float(max(abs(value) for value in expected))))
            checks.append(check(f'80digit paired recurrence:{ratio_index}:{frequency_index}',float(paired_error),1e-8))
    checks.append(dict(name='Unity shifts vanish exactly',passed=not np.count_nonzero(paired[ratios==1])))
    checks.append(dict(name='Constant increments vanish exactly',passed=not np.count_nonzero(paired[:,:,0])))
    np.savez_compressed(folder/'comparison.npz',frequency=frequency,ratios=ratios,paired=paired,legacy=legacy,reference=reference)
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,decimal_digits=80,stored_basis_coefficients_held_fixed=True,
        basis_reconstruction_uncertainty_certified=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        paired_max=max(row['paired_relative_error'] for row in rows),
        legacy_max=max(row['legacy_relative_error'] for row in rows),seconds=time.monotonic()-started)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
