from ordered_real_kernel import *
import argparse


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--order',type=int,required=True)
    arguments=parser.parse_args()
    order=arguments.order
    mp.mp.dps=65
    folder=ROOT/'results'/('total-cross-section-'+str(order))
    folder.mkdir(parents=True,exist_ok=False)
    nodes,weights=np.polynomial.legendre.leggauss(order)
    checks,rows=[],[]
    for energy in ['0.00045962015785263325','.01','.1']:
        correction,born=mp.mpf(0),mp.mpf(0)
        for cosine,weight in zip(nodes,weights):
            output=integrate_ordered(energy,str(cosine),order,3*order)
            incoming,outgoing,rapidity=kinematics(energy,str(cosine))
            differential=mp.pi*(outgoing/mp.mpf(energy))**2*compton(incoming,outgoing)
            born+=mp.mpf(float(weight))*differential
            correction+=mp.mpf(float(weight))*differential*mp.mpf(str(output['matched_ratio']))/mp.mpf(str(ALPHA))
        row=dict(energy=float(energy),born_over_alpha2=float(born),nlo_over_alpha3=float(correction),
                 relative_nlo=float(mp.mpf(str(ALPHA))*correction/born),hard_angular_order=order,soft_angular_order=order,radial_order=3*order)
        checks.append(dict(name='Finite positive inclusive total E='+energy,passed=correction>0 and born>0))
        rows.append(row)
        write_json(folder/'progress.json',dict(state='running',completed=len(rows),expected=3,rows=rows))
        print(json.dumps(row),flush=True)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
        external_comparison_pending=True),__file__,[ROOT/'vacuum_virtual.py',ROOT/'ordered_real_kernel.py'])


if __name__=='__main__':
    main()
