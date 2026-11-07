from matched_feedback_common import *


class SourceQuadrature:
    def __init__(self,basis,frequency,offsets,upper,order):
        self.basis=basis
        self.upper=upper
        self.frequency,self.weights=log_rule([2e-5,4e-5,.0003,.001,.003,.01,upper],order)
        self.values=basis.evaluate(self.frequency)
        occupation=1/np.expm1(self.frequency)
        self.measure=self.weights*self.frequency**2*occupation*(1+occupation)/I3
        self.projection=self.values.T*self.measure
        spacing=math.log(frequency[1]/frequency[0])
        self.ratios=np.exp(offsets*spacing)
        self.adjoint=[]
        for ratio in self.ratios:
            shifted=basis.evaluate(self.frequency*ratio)-self.values
            inverse=(basis.evaluate(self.frequency/ratio)-self.values)/ratio
            adjoint=(shifted+inverse).T*self.weights/(2*I3)
            adjoint[0]=0
            adjoint[1]=self.frequency*(ratio-1+(1/ratio-1)/ratio)*self.weights/(2*I3*basis.norms[1])
            self.adjoint.append(adjoint)
        self.adjoint=np.array(self.adjoint)
        soft,soft_measure=log_rule([basis.minimum,2e-5,4e-5,.0003,.001,.003,.01,upper],order)
        self.soft=soft
        seeds,hard,soft_indices,weights=[],[],[],[]
        for index,(point,measure) in enumerate(zip(soft,soft_measure)):
            breaks=[2*point,2*upper,60.]
            breaks.extend(boundary for boundary in [2e-5,4e-5,.0003,.001,.003,.01,upper,.2,1.,5.,15.] if 2*point<boundary<60.)
            breaks.extend(boundary+point for boundary in [2e-5,4e-5,.0003,.001,.003,.01,upper] if 2*point<boundary+point<2*upper)
            seed,seed_measure=log_rule(sorted(set(breaks)),order)
            partner=seed-point
            density=seed**4*gould(point/seed)*np.exp(-seed)
            density/=(-np.expm1(-seed))*(-np.expm1(-partner))*(-np.expm1(-point))*point*I3*I4
            seeds.append(seed)
            hard.append(partner)
            weights.append(measure*seed_measure*density)
            soft_indices.append(np.full(len(seed),index,dtype=int))
        self.seed=np.concatenate(seeds)
        self.hard=np.concatenate(hard)
        self.soft_indices=np.concatenate(soft_indices)
        weights=np.concatenate(weights)
        delta=self.basis.evaluate(self.soft)[self.soft_indices]+self.basis.evaluate(self.hard)-self.basis.evaluate(self.seed)
        delta[:,0]=1/basis.norms[0]
        delta[:,1]=-basis.mean/basis.norms[1]
        self.dc_matrix=-(delta.T*weights)
        self.event_energy_defect=float(np.max(abs(delta@basis.temperature)))
        self.correction=CompactCorrection(basis,frequency,upper)
        for label,points in [('projection',self.frequency),('soft',self.soft),('hard',self.hard),('seed',self.seed)]:
            self.correction.register(label,points)
        self.correction.register('canonical',basis.nodes)


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--variant',choices=['fine','time','space'],default='fine')
    parser.add_argument('--order',type=int,default=24)
    parser.add_argument('--upper',type=float,default=.04)
    args=parser.parse_args()
    assert args.order in [16,24,32,48]
    assert args.upper in [.02,.04]
    modest()
    label=f'{args.variant}-q{args.order}-m{int(args.upper*1000)}'
    folder=ROOT/'results'/('sources-'+label)
    if folder.exists():
        assert not any(folder.iterdir()),folder
    folder.mkdir(parents=True,exist_ok=True)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs]
    checks,summaries=[],{}
    chain=ancestors()
    quadrature=None
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit)))
    for model in ['heavy','cold']:
        prediction,profiles,gas,dependencies=read_prediction(model,args.variant)
        inputs.extend(dependencies)
        if quadrature is None:
            quadrature=SourceQuadrature(basis,prediction['frequency'],prediction['offsets'],args.upper,args.order)
            test('Analytic DC event energy cancellation',quadrature.event_energy_defect,1e-12)
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        free_free=FreeFree(background,quadrature.frequency)
        inputs.extend([*emission.inputs,*free_free.inputs,background.parent.source,background.native_constants])
        for path in inputs:
            verify_source(path,chain)
        count=len(prediction['offsets'])
        bank_at=interpolate.interp1d(prediction['coefficient_knots'],prediction['coefficient_bank'],axis=0,bounds_error=True)
        raw,represented,projections,moments,replacement_norm,unresolved_norm=[],[],[],[],[],[]
        source_number,source_energy,projection_rule_changes=[],[],[]
        errors={key:0. for key in ['mass_projection','dc_energy','compton_number','dc_overlap_energy','compton_overlap_number','projected_control']}
        for epoch,position in enumerate(prediction['coordinate']):
            local=background.at(float(position))
            theta=local['thermal_parameter']
            bank=bank_at(position)
            spline=interpolate.CubicSpline(np.log(prediction['frequency']),prediction['slope'][epoch],axis=0,extrapolate=False)
            values={label:quadrature.correction.at(label,spline,profiles[epoch]) for label in ['projection','soft','hard','seed','canonical']}
            if epoch==0:
                values={key:np.zeros_like(value) for key,value in values.items()}
            moment=(basis.values.T*basis.measure)@values['canonical']
            projected=linalg.solve(basis.mass,moment,assume_a='pos')
            refined_moment=quadrature.projection@values['projection']
            projection_rule_changes.append(linalg.solve(basis.mass,refined_moment-moment,assume_a='pos'))
            projection_scale=np.maximum(np.linalg.norm(moment,axis=0),1e-300)
            errors['mass_projection']=max(errors['mass_projection'],float(np.max(np.linalg.norm(basis.mass@projected-moment,axis=0)/projection_scale)))
            stencil=bank[:count]
            kernel=stencil/quadrature.ratios
            adjoint=np.einsum('j,jif->if',kernel,quadrature.adjoint)
            scattering=adjoint@values['projection']
            jump=values['soft'][quadrature.soft_indices]+values['hard']-values['seed']
            dc=bank[count+1]*(quadrature.dc_matrix@jump)
            br=-quadrature.projection@(free_free.br_rates(theta)[:,None]*values['projection'])
            source=np.stack([scattering,dc,br])
            operators=np.stack([ladder.at(theta,0)[:96,:96],-emission.at(theta,'dc'),-emission.interpolator(math.log(theta))])
            old=np.einsum('tij,jk->tik',operators,projected)
            for name,vector,row in [('dc_energy',dc,basis.temperature),('compton_number',scattering,basis.chemical),
                    ('dc_overlap_energy',old[1],basis.temperature),('compton_overlap_number',old[0],basis.chemical)]:
                scale=np.maximum(abs(row)@abs(vector),1e-300)
                errors[name]=max(errors[name],float(np.max(abs(row@vector)/scale)))
            errors['projected_control']=max(errors['projected_control'],float(np.max(abs(old-old))))
            norm2=np.sum(basis.measure[:,None]*values['canonical']**2,axis=0)
            projected2=np.sum(projected*moment,axis=0)
            assert np.all(projected2<=norm2+1e-10*np.maximum(norm2,1e-300)),(model,epoch,projected2,norm2)
            raw.append(source)
            represented.append(old)
            projections.append(projected)
            moments.append(moment)
            replacement_norm.append(np.sqrt(norm2))
            unresolved_norm.append(np.sqrt(np.sum(basis.measure[:,None]*(values['canonical']-basis.values@projected)**2,axis=0)))
            source_number.append(np.einsum('i,tik->tk',basis.chemical,source-old))
            source_energy.append(np.einsum('i,tik->tk',basis.temperature,source-old))
        raw,represented=np.array(raw),np.array(represented)
        for name,value in errors.items():
            test(name+':'+model,value,1e-10)
        source=raw-represented
        assert np.all(np.isfinite(source))
        np.savez_compressed(folder/(model+'.npz'),coordinate=prediction['coordinate'],source=source,
            raw_source=raw,overlap_source=represented,projected_replacement=np.array(projections),
            replacement_moments=np.array(moments),replacement_norm=np.array(replacement_norm),
            unresolved_norm=np.array(unresolved_norm),number_source=np.array(source_number),
            energy_source=np.array(source_energy),source_variant=args.variant,quadrature_order=args.order,
            match_upper=args.upper,profiles=profiles,gas=gas,
            projection_quadrature_difference=np.array(projection_rule_changes))
        norms=np.sqrt(np.einsum('ntik,ij,ntjk->ntk',source,linalg.inv(basis.mass),source))
        scale=np.maximum(np.sqrt(np.einsum('ntik,ij,ntjk->ntk',raw,linalg.inv(basis.mass),raw)).sum(axis=1).max(axis=0),1e-300)
        summaries[model]=dict(errors=errors,maximum_source_dual_norm=norms.max(axis=0).tolist(),
            raw_source_norm_scale=scale.tolist(),endpoint_unresolved_fraction=(np.array(unresolved_norm)[-1]/np.maximum(np.array(replacement_norm)[-1],1e-300)).tolist(),
            maximum_replacement_norm=np.max(replacement_norm,axis=0).tolist())
        print(json.dumps(dict(model=model,case=label,errors=errors,summary=summaries[model])),flush=True)
    finish(folder,dict(checks=checks,models=summaries,variant=args.variant,quadrature_order=args.order,
        match_upper=args.upper,columns=['baseline','join1','join2'],new_parent_history=False,
        overlap_subtracted=True,stored_moment_derivative_accounted=True,
        soft_compton_extension=True,full_finite_frequency_compton_extension=False,
        matched_dc_all_legs=True,compact_event_count=len(quadrature.seed),fitted_cutoff=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
