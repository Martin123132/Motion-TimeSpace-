from continue199 import *

def main():
    config=checked_protocol();inputs=read(ROOT/'inputs.json');rows=[];records=[]
    for model in ('heavy','cold'):
        equation=ContinuedEquation(model,'candidate')
        basis=equation.basis;local=equation.operator.background.at(config['target_fraction']*config['expansion_span'])
        damping=equation.operator.emission.at(local['thermal_parameter'],'dcbr')
        factor=linear.cholesky(basis.mass,lower=True)
        check(rows,model+':mass symmetry',np.linalg.norm(basis.mass-basis.mass.T)/np.linalg.norm(basis.mass),1e-10)
        check(rows,model+':e=MT',np.linalg.norm(basis.energy-basis.mass@basis.temperature)/np.linalg.norm(basis.energy),1e-10)
        check(rows,model+':emission symmetry',np.linalg.norm(damping-damping.T)/np.linalg.norm(damping),1e-10)
        eigenvalues=linear.eigvalsh(smooth.whiten(damping,factor))
        check(rows,model+':emission PSD',max(0.,-float(eigenvalues[0]))/max(abs(eigenvalues).max(),1e-300),1e-10)
        stiffness=local['coefficient']/local['thermal_parameter']*(smooth.candidate(OFFSET,equation.frozen)-damping)
        eigenvalues=linear.eigvalsh(smooth.whiten(stiffness,factor))
        check(rows,model+':K negative semidefinite',max(0.,float(eigenvalues[-1]))/max(abs(eigenvalues).max(),1e-300),1e-10)
        for grid in ('half','quarter'):
            status=read(ROOT/'histories'/model/grid/'complete.json');step=status['step'];alpha=1.5/step
            response=linear.solve(alpha*basis.mass-stiffness,-stiffness@basis.temperature,assume_a='gen')
            projected=float(basis.energy@response);lower=float(equation.heat)*(alpha+1)
            denominator=lower+alpha*projected
            check(rows,model+':'+grid+':positive capacity',int(denominator<=0 or lower<=0 or projected<0),0)
            records.append(dict(model=model,grid=grid,alpha=alpha,projected=projected,lower_bound=lower,denominator=denominator))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/capacity-lemma.json',dict(checks=rows,failed_checks=failed,records=records,scope='target matrix evidence for conditional lemma'))
    print(json.dumps(dict(checks=len(rows),failed=failed,records=records)),flush=True)

if __name__=='__main__':main()
