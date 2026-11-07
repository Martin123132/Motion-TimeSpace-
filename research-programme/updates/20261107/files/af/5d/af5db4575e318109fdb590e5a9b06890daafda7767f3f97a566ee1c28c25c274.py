from ordered_real_kernel import *
import argparse


def four_transfers(energy, companion, emitted, hard_cosine, soft_cosine, azimuth):
    hard_sine,soft_sine=mp.sqrt(1-hard_cosine**2),mp.sqrt(1-soft_cosine**2)
    soft=mp.matrix([emitted,emitted*soft_sine*mp.cos(azimuth),emitted*soft_sine*mp.sin(azimuth),emitted*soft_cosine])
    hard=mp.matrix([companion-energy,companion*hard_sine,0,companion*hard_cosine-energy])
    photons=hard+soft
    electron_spatial=[-photons[index] for index in range(1,4)]
    electron_energy=mp.sqrt(1+sum(value**2 for value in electron_spatial))-1
    return photons,mp.matrix([electron_energy,*electron_spatial]),soft,hard


def integrate_source(energy,hard_cosine,angular_order,radial_order):
    energy,hard_cosine=mp.mpf(str(energy)),mp.mpf(str(hard_cosine))
    born_energy=energy/(1+energy*(1-hard_cosine))
    born_photons,born_electron,ignored,born_hard=four_transfers(energy,born_energy,mp.mpf(0),hard_cosine,mp.mpf(0),mp.mpf(0))
    nodes,weights=np.polynomial.legendre.leggauss(radial_order)
    photon_remainder,electron_remainder,soft_moment=mp.zeros(4,1),mp.zeros(4,1),mp.zeros(4,1)
    hard_remainder=mp.zeros(4,1)
    pole_log=mp.mpf(0)
    worst_shell=mp.mpf(0)
    for soft_cosine,azimuth,angular_weight in angular_nodes(angular_order):
        values=geometry(energy,hard_cosine,soft_cosine,azimuth)
        upper=ordered_upper(*values)
        pole=pole_density(*values)
        pole_log+=angular_weight*pole*mp.log(2*upper)
        for node,weight in zip(nodes,weights):
            emitted=upper*(mp.mpf(float(node))+1)/2
            measure=upper*mp.mpf(float(weight))*angular_weight/2
            squared,companion,denominator=amplitude_squared(energy,emitted,*values[1:])
            ratio=born_energy/energy
            density=mp.mpf(str(ALPHA))/(8*mp.pi**2)*squared*companion*emitted/(energy*denominator*ratio**2*compton(-energy,born_energy))
            photons,electron,soft,hard=four_transfers(energy,companion,emitted,hard_cosine,soft_cosine,azimuth)
            worst_shell=max(worst_shell,abs(photons[0]+electron[0]))
            photon_remainder+=measure*(density*photons-pole/emitted*born_photons)
            electron_remainder+=measure*(density*electron-pole/emitted*born_electron)
            hard_remainder+=measure*(density*hard-pole/emitted*born_hard)
            soft_moment+=measure*density*soft
    common=finite_virtual_ratio(energy,hard_cosine)+soft_constant(energy,hard_cosine)+pole_log
    photons=common*born_photons+photon_remainder
    electron=common*born_electron+electron_remainder
    hard=common*born_hard+hard_remainder
    return dict(energy=float(energy),cosine=float(hard_cosine),
        photon_source=[float(value) for value in photons],electron_source=[float(value) for value in electron],
        soft_photon_source=[float(value) for value in soft_moment],hard_photon_source=[float(value) for value in hard],
        born_photon_source=[float(value) for value in born_photons],
        born_electron_source=[float(value) for value in born_electron],
        worst_event_energy_defect=float(worst_shell),
        integrated_four_force_defect=float(max(abs(value) for value in photons+electron)),
        resolved_plus_soft_defect=float(max(abs(value) for value in hard+soft_moment-photons)))


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--angular',type=int,required=True)
    parser.add_argument('--radial',type=int,required=True)
    parser.add_argument('--name',required=True)
    args=parser.parse_args()
    mp.mp.dps=65
    folder=ROOT/'results'/args.name
    folder.mkdir(parents=True,exist_ok=False)
    rows,checks=[],[]
    for energy,cosine in [('0.00045962015785263325','.1'),('.01','-.8'),('.1','.7')]:
        row=integrate_source(energy,cosine,args.angular,args.radial)
        checks.append(check('Independent on-shell electron energy at every event E='+energy,row['worst_event_energy_defect'],1e-55))
        checks.append(check('Matched photon plus electron four-force E='+energy,row['integrated_four_force_defect'],1e-50))
        checks.append(check('Hard plus created photons reproduce full source E='+energy,row['resolved_plus_soft_defect'],1e-50))
        checks.append(check('Azimuth-reflection transverse mean E='+energy,abs(row['photon_source'][2]),1e-50))
        checks.append(dict(name='Created photons carry positive finite energy E='+energy,passed=row['soft_photon_source'][0]>0))
        checks.append(dict(name='Omitting emitted photon energy breaks balance E='+energy,passed=abs(row['hard_photon_source'][0]+row['electron_source'][0])>.99*row['soft_photon_source'][0]))
        rows.append(row)
        print(json.dumps(row),flush=True)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
        normalization='NLO four-momentum change per incoming photon per Born differential cross section; energies/momenta in electron rest units',
        vacuum_unpolarized_rest_electron=True,thermal_average_not_taken=True,
        opposite_force_computed_from_independent_electron_mass_shell=True,angular_order=args.angular,radial_order=args.radial),__file__,
        [ROOT/'ordered_real_kernel.py',ROOT/'vacuum_virtual.py'])


if __name__=='__main__':
    main()
