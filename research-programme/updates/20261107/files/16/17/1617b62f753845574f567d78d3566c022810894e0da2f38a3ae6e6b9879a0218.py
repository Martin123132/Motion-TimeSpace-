from thermal_vertex_common import *


def main():
    modest()
    folder=ROOT/'results/angular-refinement'
    folder.mkdir(parents=True,exist_ok=False)
    checks,inputs,packets,arrays=[],[],[],[]
    for order in [4,6,8]:
        source=ROOT/'results'/('thermal-angular-'+str(order))
        packet=json.loads((source/'status.json').read_text())
        assert packet['all_checks_passed']
        with np.load(source/'amplitude.npz') as saved:
            arrays.append(saved['tensor'].copy())
        packets.append(packet)
        inputs.extend([source/'status.json',source/'amplitude.npz'])
    for index in [0,1]:
        error=float(np.linalg.norm(arrays[index]-arrays[-1])/np.linalg.norm(arrays[-1]))
        checks.append(check('Complex polarization amplitude angular refinement '+str([4,6][index])+' versus 8',error,1e-9))
        first=packets[index]['result']['amplitude_interference_over_bare']
        final=packets[-1]['result']['amplitude_interference_over_bare']
        checks.append(check('Finite amplitude interference angular refinement '+str([4,6][index])+' versus 8',abs(first/final-1),1e-9))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                       accepted_angular_order=8,result=packets[-1]['result'],
                       fixed_kinematic_point_not_global_thermal_operator=True),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],result=packets[-1]['result'])),flush=True)


if __name__=='__main__':
    main()
