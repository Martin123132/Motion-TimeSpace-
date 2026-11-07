from paired_redistribution import *


def main():
    modest()
    folder=ROOT/'results/weak-soft-structure'
    folder.mkdir(parents=True,exist_ok=False)
    metadata,saved,spectrum=snapshot()
    theta=metadata['reference_temperature']
    parameters=source.context(theta,.1,[.02,.005,-.01],theta)
    tree,tree_map,normalized=source.tree_map(parameters)
    hard_direction=parameters['hard_direction']
    soft_direction=np.array([0.,.8,.6])
    doppler=source.dot(parameters['bath'],np.r_[1.,soft_direction])
    hard_doppler=parameters['hard_doppler']
    energy=parameters['energy']
    hard=parameters['hard']
    recoil=np.array([0.,0.,energy])-hard*hard_direction
    final_energy=math.sqrt(1+recoil@recoil)
    born_frequency=hard*hard_doppler/theta
    born=np.r_[scalar_functions(born_frequency)-scalar_functions(1.),1-born_frequency]
    pole=source.ALPHA/(4*np.pi**2)*np.linalg.norm(np.cross(recoil,soft_direction))**2/(final_energy-recoil@soft_direction)**2
    rows=[]
    checks=[]
    for scaled in [1e-3,1e-4,1e-5,1e-6]:
        emitted=theta*scaled/doppler
        tensor_values,photons,final,hard_values,denominators=tensor_batch(energy,np.array([emitted,-emitted]),hard_direction,soft_direction)
        squared=np.sum(abs(tensor_values)**2,axis=(1,2,3,4,5))/4
        density=source.ALPHA/(4*np.pi**2)*hard_values*emitted/(energy*denominators*(hard/energy)**2*tree_map[0,0])*squared
        outgoing_frequency=hard_values*hard_doppler/theta
        sign=np.array([1.,-1.])
        jumps=scalar_functions(outgoing_frequency)+sign[:,None]*scalar_functions(scaled)-scalar_functions(1.)
        jumps=np.column_stack([jumps,-jumps[:,1]])
        hard_bose=(1+1/np.expm1(outgoing_frequency))/parameters['hard_bose']
        occupation=1/np.expm1(scaled)
        positive=(density[0]*hard_bose[0]*(1+occupation)*np.outer(jumps[0],jumps[0])
                  +density[1]*hard_bose[1]*occupation*np.outer(jumps[1],jumps[1]))/2
        expected=(1+2*occupation)*pole/(2*emitted)*np.outer(born,born)
        regular=[1,2,3,4]
        residual=np.linalg.norm((positive-expected)[np.ix_(regular,regular)])/np.linalg.norm(expected[np.ix_(regular,regular)])
        chemical_ratio=positive[0,0]/((1+2*occupation)*pole/(2*emitted))
        rows.append(dict(soft_over_bath_temperature=scaled,regular_relative_pole_remainder=float(residual),
                         chemical_pole_ratio=float(chemical_ratio),regular_subtracted_norm=float(np.linalg.norm((positive-expected)[np.ix_(regular,regular)]))))
    checks.append(check('Paired weak pole matches elastic virtual soft coefficient on IR-regular modes',rows[-1]['regular_relative_pole_remainder'],1e-8))
    checks.append(check('Photon chemical direction retains physical real pole',abs(rows[-1]['chemical_pole_ratio']-1),1e-8))
    checks.append(dict(name='Regular relative pole remainder decreases under soft refinement',
                       passed=rows[-1]['regular_relative_pole_remainder']<rows[0]['regular_relative_pole_remainder']*1e-3))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       leading_weak_soft_counterterm_derived=True,finite_virtual_projection_pending=True,
                       chemical_mode_cannot_be_removed_by_elastic_counterterm=True),__file__,
           [ROOT/'paired_redistribution.py',ROOT/'resolved_redistribution.py',ROOT/'batched_real.py',
            ROOT/'results/saved-state/status.json',ROOT/'results/saved-state/state.npz',PARENT/'polarized_source.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
