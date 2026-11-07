from polarized_source import *


def main():
    modest()
    energy=.00045962015785263325
    parameters=context(energy,.1,[0,0,0],energy)
    source=WARD/'results/thermal-angular-8/amplitude.npz'
    with np.load(source) as saved:
        correction=saved['tensor'].copy()
    tree,tree_mueller,normalized=tree_map(parameters)
    virtual=interference(tree,correction)/tree_mueller[0,0]
    started=time.perf_counter()
    rest,lab,pieces=matched_moments(parameters,virtual,4,24)
    print('seconds',time.perf_counter()-started,flush=True)
    print('intensity',lab[:,0,0].tolist(),flush=True)
    print('mueller',lab[0].tolist(),flush=True)
    print('energy closure',np.linalg.norm(lab[1:5]+lab[5:9]),flush=True)
    expected=json.loads((PARENT/'results/thermal-a4-r24/status.json').read_text())['thermal_correction_vector']
    print('relative nonzero',[(lab[index,0,0]/expected[index]-1) for index in [0,1,2,4]],flush=True)


if __name__=='__main__':
    main()
