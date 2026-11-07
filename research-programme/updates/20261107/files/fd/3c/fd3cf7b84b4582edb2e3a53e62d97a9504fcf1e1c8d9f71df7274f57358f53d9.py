from polarized_source import *


def main():
    modest()
    datasets={}
    for name in ['rest-a4-r24','rest-a6-r40','moving-a4-r24-v6','moving-a6-r40-v8']:
        with np.load(ROOT/'results'/name/'source.npz') as saved:
            datasets[name]={key:saved[key].copy() for key in saved.files}
    for first,second in [('rest-a4-r24','rest-a6-r40'),('moving-a4-r24-v6','moving-a6-r40-v8')]:
        coarse,fine=datasets[first],datasets[second]
        for key in ['virtual','lab_fixed_momentum']:
            print(first,key,'relative',np.linalg.norm(fine[key]-coarse[key])/np.linalg.norm(fine[key]),flush=True)
        print('canonical correction',fine['canonical_correction'][:,0,0].tolist(),flush=True)
        print('matrix',fine['lab_fixed_momentum'][0].tolist(),flush=True)
        mueller_total=fine['born'][0]+fine['lab_fixed_momentum'][0]
        choi=sum(mueller_total[first_index,second_index]*np.kron(PAULI[first_index],PAULI[second_index].T)/2
                 for first_index,second_index in itertools.product(range(4),repeat=2))
        print('Choi eigenvalues',np.linalg.eigvalsh(choi).tolist(),flush=True)


if __name__=='__main__':
    main()
