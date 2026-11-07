import argparse
from polarized_source import *


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--velocity',nargs=3,type=float,default=[0,0,0])
    parser.add_argument('--angular',type=int,default=4)
    parser.add_argument('--radial',type=int,default=24)
    parser.add_argument('--virtual-order',type=int,default=6)
    parser.add_argument('--reuse-virtual')
    parser.add_argument('--profile',type=float)
    arguments=parser.parse_args()
    folder=ROOT/'results'/arguments.name
    folder.mkdir(parents=True,exist_ok=False)
    energy=.00045962015785263325
    parameters=context(energy,.1,arguments.velocity,energy)
    write_json(folder/'RUNNING.json',dict(started_utc=datetime.now(timezone.utc).isoformat(),arguments=vars(arguments)))
    started=time.perf_counter()
    dependencies=[ROOT/'polarized_source.py',ROOT/'moving_frame.py',ROOT/'reduced_amplitude.py',WARD/'thermal_dressed.py']
    if arguments.reuse_virtual:
        source=Path(arguments.reuse_virtual)
        with np.load(source) as saved:
            correction=saved['tensor'].copy()
        dependencies.append(source)
        tree,tree_mueller,normalized=tree_map(parameters)
        virtual=interference(tree,correction)/tree_mueller[0,0]
    else:
        correction,virtual=virtual_map(parameters,arguments.virtual_order)
    print(arguments.name+' virtual ready '+str(round(time.perf_counter()-started,2))+'s',flush=True)
    rest,lab,pieces=matched_moments(parameters,virtual,arguments.angular,arguments.radial,arguments.profile)
    canonical=canonical_momentum_correction(parameters)
    fixed_momentum=lab+canonical
    born=lab_moments(pieces['born'][:,None,None]*pieces['normalized_tree'],parameters)
    checks=[dict(name='All moving polarized source components finite',passed=bool(np.isfinite(fixed_momentum).all())),
            check('Every polarized energy/momentum exchange cancels',
                  np.linalg.norm(fixed_momentum[1:5]+fixed_momentum[5:9])/max(np.linalg.norm(fixed_momentum[1:5]),1e-30),1e-9)]
    total=born[0]+fixed_momentum[0]
    cone_violation=0.
    for component in [1,2,3]:
        for sign in [-1,1]:
            stokes=np.eye(4)[0]+sign*np.eye(4)[component]
            output=total@stokes
            cone_violation=max(cone_violation,np.linalg.norm(output[1:])-output[0])
    checks.append(check('Born plus thermal correction respects six Stokes-cone probes',cone_violation,2e-12))
    np.savez_compressed(folder/'source.npz',tensor=correction,virtual=virtual,rest=rest,lab_fixed_velocity=lab,
                        canonical_correction=canonical,lab_fixed_momentum=fixed_momentum,born=born,
                        real=pieces['real'],profile_conversion=pieces['profile_conversion'])
    report=dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                arguments=vars(arguments),elapsed_seconds=time.perf_counter()-started,
                lab_energy=energy,lab_temperature=energy,lab_cosine=.1,
                rest_energy=parameters['energy'],rest_cosine=parameters['cosine'],
                born_differential_over_thomson=parameters['born_differential_over_thomson'],
                relative_flux=parameters['relative_flux'],angular_jacobian=parameters['angular_jacobian'],
                event_mueller_thermal=fixed_momentum[0].tolist(),intensity_moments=fixed_momentum[:,0,0].tolist(),
                conditional_hard_photon_map=True,full_electron_distribution_integrated=False)
    finish(folder,report,__file__,[*dependencies,folder/'source.npz',folder/'RUNNING.json'])
    print(json.dumps(dict(name=arguments.name,elapsed=report['elapsed_seconds'],failed=[row for row in checks if not row['passed']],
                          intensity=report['intensity_moments'])),flush=True)


if __name__=='__main__':
    main()
