from thermal_event_source import *
from thermal_dressed import integrate_dressed


def main():
    modest()
    mp.mp.dps=60
    folder=ROOT/'results/cold-bath-limit'
    folder.mkdir(parents=True,exist_ok=False)
    energy=mp.mpf('.00045962015785263325')
    cosine=mp.mpf('.1')
    reference=json.loads((ROOT/'results/thermal-a8-r56/status.json').read_text())
    checks,rows=[],[]
    for ratio in ['.1','.02']:
        temperature=energy*mp.mpf(ratio)
        tensor,virtual=integrate_dressed(energy,cosine,temperature,4)
        result=matched_event_source(energy,cosine,temperature,4,40,mp.mpf(str(virtual['amplitude_interference_over_bare'])))
        values=[float(value) for value in result['total']]
        checks.append(dict(name='Computed finite thermal rate tends toward vacuum T/E='+ratio,
                           passed=abs(values[0])<abs(reference['thermal_correction_vector'][0])*float(ratio)))
        checks.append(check('Cold-bath photon/electron four-force T/E='+ratio,
                            max(abs(values[index+1]+values[index+5]) for index in range(4)),1e-40))
        rows.append(dict(temperature_over_incoming_energy=float(ratio),thermal_correction_vector=values,
                         finite_virtual_interference=virtual['amplitude_interference_over_bare']))
    checks.append(dict(name='Second cooling step further suppresses the thermal rate correction',
                       passed=abs(rows[-1]['thermal_correction_vector'][0])<abs(rows[0]['thermal_correction_vector'][0])*.1))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       finite_virtual_recomputed_not_rescaled=True,sampled_zero_temperature_approach=True,
                       exact_zero_temperature_order_from_analytic_small_T_expansion=True),__file__,
           [ROOT/'thermal_event_source.py',PARENT/'thermal_dressed.py',ROOT/'results/thermal-a8-r56/status.json'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
