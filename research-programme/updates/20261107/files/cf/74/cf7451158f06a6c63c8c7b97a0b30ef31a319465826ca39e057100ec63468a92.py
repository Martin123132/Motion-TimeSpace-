from ordered_real_kernel import *
import argparse


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--angular',type=int,required=True)
    parser.add_argument('--radial',type=int,required=True)
    parser.add_argument('--name',required=True)
    arguments=parser.parse_args()
    mp.mp.dps=65
    folder=ROOT/'results'/arguments.name
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    started=time.perf_counter()
    for energy in ['0.00045962015785263325','.01','.1']:
        for cosine in ['-.8','.1','.7']:
            row=integrate_ordered(energy,cosine,arguments.angular,arguments.radial)
            checks.append(check('Soft angular integral E='+energy+' c='+cosine,abs(row['integrated_pole']/row['analytic_pole']-1),1e-5))
            rows.append(row)
            write_json(folder/'progress.json',dict(state='running',completed=len(rows),expected=9,elapsed_seconds=time.perf_counter()-started,last=row))
            print(json.dumps(row),flush=True)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        rows=rows,elapsed_seconds=time.perf_counter()-started,observable='Inclusive hardest-photon differential cross section at fixed direction divided by its Born differential cross section',
        vacuum_unpolarized_rest_electron=True,relative_correction_only=True,finite_temperature=False,
        angular_order=arguments.angular,radial_order=arguments.radial,arithmetic_decimal_places=65),__file__,
        [ROOT/'vacuum_virtual.py',ROOT/'ordered_real_kernel.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
