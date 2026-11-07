from refine222 import *
from fractions import Fraction as Rational

def bdf_scalar(current,older,step,decay,force):
    return (2*current-older/2+step*force)/(Rational(3,2)+step*decay)

def toy_run():
    path=ROOT/'boundary-contract.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),script_sha256=digest(__file__),derivation_sha256=digest(ROOT/'BOUNDARY-MATCHING-DERIVATION.md'),
        counts=[32,64],decays=[0,1,2],identity_tolerance=1e-10,source_support=[0,1],final_time=2))
    rows=[];records=[]
    for count in (32,64):
        step=Rational(1,count)
        current=step;older=Rational(0)
        for ordinal in range(2,count+1):
            older,current=current,bdf_scalar(current,older,step,Rational(0),Rational(1))
        check(rows,f'N{count}:causal interior exact area',float(current-1),1e-10,'identity')
        old_tail_limit=(3*current-older)/2
        check(rows,f'N{count}:naive tail exact excess',float(old_tail_limit-1-step/2),1e-10,'identity')
        correct_next=current
        correct_limit=(3*correct_next-current)/2
        check(rows,f'N{count}:right restart exact area',float(correct_limit-1),1e-10,'identity')
        check(rows,f'N{count}:naive stop is detected',int(abs(float(old_tail_limit-1))<=1e-10),0,'negative_control')

    def add(first,second):
        return [first[index]+second[index] for index in range(2)]
    def scale(value,vector):
        return [value*entry for entry in vector]
    def action(operator,vector):
        return [sum(operator[row][column]*vector[column] for column in range(2)) for row in range(2)]
    def shifted(alpha,operator,sign=-1):
        return [[(alpha if row==column else 0)+sign*operator[row][column] for column in range(2)] for row in range(2)]
    def solve(operator,rhs):
        determinant=operator[0][0]*operator[1][1]-operator[0][1]*operator[1][0]
        return [(operator[1][1]*rhs[0]-operator[0][1]*rhs[1])/determinant,
                (operator[0][0]*rhs[1]-operator[1][0]*rhs[0])/determinant]
    operator=[[Rational(-2),Rational(1)],[Rational(2),Rational(-1)]]
    step=Rational(1,32);alpha_b=Rational(3,2)/step;alpha_t=2/step
    forcing=[Rational(1),Rational(-1)]
    homogeneous=[Rational(2),Rational(3)];homogeneous_old=[Rational(7,3),Rational(8,3)]
    joint=list(homogeneous);joint_old=list(homogeneous_old)
    increment=[Rational(0),Rational(0)];increment_old=list(increment)
    for ordinal in range(1,65):
        history_h=scale(1/step,add(scale(2,homogeneous),scale(Rational(-1,2),homogeneous_old)))
        new_h=solve(shifted(alpha_b,operator),history_h)
        if ordinal==1:
            new_i=solve(shifted(alpha_t,operator),scale(2,forcing))
            rhs=add(add(history_h,scale(alpha_t-alpha_b,new_h)),scale(2,forcing))
            new_j=solve(shifted(alpha_t,operator),rhs)
        elif ordinal==33:
            right_operator=shifted(alpha_t,operator,1)
            new_i=solve(shifted(alpha_t,operator),action(right_operator,increment))
            rhs=add(action(shifted(alpha_t,operator),new_h),action(right_operator,add(joint,scale(-1,homogeneous))))
            new_j=solve(shifted(alpha_t,operator),rhs)
        else:
            source=forcing if ordinal<=32 else [Rational(0),Rational(0)]
            history_i=scale(1/step,add(scale(2,increment),scale(Rational(-1,2),increment_old)))
            history_j=scale(1/step,add(scale(2,joint),scale(Rational(-1,2),joint_old)))
            new_i=solve(shifted(alpha_b,operator),add(history_i,source))
            new_j=solve(shifted(alpha_b,operator),add(history_j,source))
        check(rows,f'2x2 step{ordinal}:independent joint matching',max(abs(float(value)) for value in add(new_j,scale(-1,add(new_h,new_i)))),1e-10,'identity')
        check(rows,f'2x2 step{ordinal}:balance',float(sum(new_j)-5),1e-10,'identity')
        homogeneous_old,homogeneous=homogeneous,new_h
        joint_old,joint=joint,new_j
        increment_old,increment=increment,new_i
    with mp.workdps(80):
        for decay in (1,2):
            errors={}
            for count in (32,64):
                step=mp.mpf(1)/count
                current=step/(1+step*decay/2);older=mp.mpf(0)
                for ordinal in range(2,count+1):
                    older,current=current,(2*current-older/2+step)/(mp.mpf('1.5')+step*decay)
                older,current=current,(1-step*decay/2)*current/(1+step*decay/2)
                for ordinal in range(count+2,2*count+1):
                    older,current=current,(2*current-older/2)/(mp.mpf('1.5')+step*decay)
                expected=(1-mp.exp(-decay))*mp.exp(-decay)/decay
                errors[count]=abs(current-expected)/abs(expected)
                check(rows,f'decay{decay}:N{count}:relative error',errors[count],.01,'comparison')
                records.append(dict(decay=decay,count=count,relative_error=float(errors[count])))
            check(rows,f'decay{decay}:refinement shrinks error',int(errors[64]>=errors[32]),0,'comparison')
            records.append(dict(decay=decay,refinement_ratio=float(errors[64]/errors[32]),continuum_bound=False))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/boundary-algebra.json',dict(checks=rows,failed_checks=failed,records=records,
        scope='exact rational matching and scalar numerical controls; full physical application is next'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),records=records)),flush=True)

if __name__=='__main__':
    toy_run()

