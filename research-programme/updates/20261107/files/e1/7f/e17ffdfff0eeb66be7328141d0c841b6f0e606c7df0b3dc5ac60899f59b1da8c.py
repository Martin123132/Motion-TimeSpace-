from reduced_amplitude import *
import ordered_real_kernel as scalar


def main():
    modest()
    exact.mp.mp.dps=70
    for energy in ['.00045962015785263325','.1']:
        for fraction in ['1e-7','.01','.3','-.3','-3']:
            sample=exact.event(energy,fraction,[.7,.2,-.3],[-.3,.5,.6])
            first=np.array(list(sample['directions'][1]),float)
            second=np.array(list(sample['directions'][2]),float)
            fast_sample=event(float(energy),float(energy)*float(fraction),first,second)
            fast=tensor(fast_sample)
            original=exact.tensor_for_event(sample)
            print(energy,fraction,'tensor',np.linalg.norm(fast-original)/np.linalg.norm(original),
                  'mueller',np.linalg.norm(mueller(fast)-mueller(original))/np.linalg.norm(mueller(original)),flush=True)
    tree,final=exact.single_tensor('.00045962015785263325',[.7,.2,-.3])
    hard=float(energy)/(1+float(energy)*(1-first[2]))
    print('tree expected factor2U',mueller(tree)[0,0],flush=True)


if __name__=='__main__':
    main()
