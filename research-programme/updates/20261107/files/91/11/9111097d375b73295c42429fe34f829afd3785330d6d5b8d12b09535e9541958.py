from batched_real import *


def main():
    modest()
    folder=ROOT/'results/batched-real'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    for energy in [.000145,.00045962015785263325,.1]:
        hard_direction=np.array([math.sqrt(.99),0,.1])
        soft_direction=np.array([0.,.8,.6])
        shares=np.array([1e-9,1e-5,.01,.2,-.01,-2.])
        tensors,photons,final,hard,denominator=tensor_batch(energy,energy*shares,hard_direction,soft_direction)
        for index,share in enumerate(shares):
            reference=reduced.tensor(reduced.event(energy,energy*share,hard_direction,soft_direction))
            checks.append(check('Batched exact tensor E='+str(energy)+' share='+str(share),
                                np.linalg.norm(tensors[index]-reference)/np.linalg.norm(reference),2e-12))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks)),__file__,
           [ROOT/'batched_real.py',PARENT/'reduced_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
