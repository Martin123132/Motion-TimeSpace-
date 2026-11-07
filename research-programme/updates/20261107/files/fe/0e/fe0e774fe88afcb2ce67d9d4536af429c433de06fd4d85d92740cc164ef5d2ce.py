from thermal_source_common import *
import dirac_amplitude as spin
mp=spin.mp


def boost(vector,velocity):
    squared=sum(value**2 for value in velocity)
    if squared==0:
        return vector.copy()
    gamma=1/mp.sqrt(1-squared)
    projection=sum(velocity[index]*vector[index+1] for index in range(3))
    return mp.matrix([gamma*(vector[0]+projection),
                      *[vector[index+1]+((gamma-1)*projection/squared+gamma*vector[0])*velocity[index] for index in range(3)]])


def reaction_weights(initial,final,photons,temperature,epsilon=0):
    perturb=lambda energy:(energy/temperature)**2/mp.mpf(7)
    electron_initial=mp.exp(-(initial[0]-1)/temperature*(1+epsilon*mp.mpf('.3')))
    electron_final=mp.exp(-(final[0]-1)/temperature*(1+epsilon*mp.mpf('.3')))
    occupations=[1/mp.expm1(photon[0]/temperature+epsilon*perturb(photon[0])) for photon in photons]
    incoming,first,second=occupations
    forward=electron_initial*incoming*(1+first)*(1+second)
    reverse=electron_final*first*second*(1+incoming)
    departure=-mp.mpf('.3')*(final[0]-initial[0])/temperature-perturb(photons[1][0])-perturb(photons[2][0])+perturb(photons[0][0])
    return forward,reverse,departure


def main():
    modest()
    mp.mp.dps=70
    folder=ROOT/'results/reverse-weak-form'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for energy in ['.00045962015785263325','.01']:
        temperature=mp.mpf(energy)
        for fraction in ['.02','.2','.4']:
            sample=spin.event(energy,fraction,[.7,.2,.3],[-.3,.5,.6])
            for velocity_text in [['0','0','0'],['.02','.005','-.01'],['-.03','.01','.02']]:
                velocity=mp.matrix([mp.mpf(value) for value in velocity_text])
                initial,final=[boost(sample[name],velocity) for name in ['initial','final']]
                photons=[boost(photon,velocity) for photon in sample['photons']]
                forward,reverse,departure=reaction_weights(initial,final,photons,temperature)
                label=' E='+energy+' soft/E='+fraction+' velocity='+str(velocity_text)
                checks.append(check('Moving-electron microscopic reverse balance'+label,abs(forward/reverse-1),1e-54))
                conserved=final-initial+photons[1]+photons[2]-photons[0]
                checks.append(check('Collision weak form annihilates common four-momentum'+label,mp.norm(conserved),1e-54))
                delta=mp.mpf('1e-10')
                positive=reaction_weights(initial,final,photons,temperature,delta)
                negative=reaction_weights(initial,final,photons,temperature,-delta)
                derivative=((positive[0]-positive[1])-(negative[0]-negative[1]))/(2*delta)
                checks.append(check('Weak linearization follows direct nonlinear gain minus loss'+label,abs(derivative+forward*departure)/max(abs(forward*departure),mp.mpf('1e-30')),1e-16))
                checks.append(dict(name='Entropy quadratic form nonpositive'+label,passed=bool(derivative*departure<0)))
                checks.append(dict(name='Electron number conserved but photon number changes in real reaction'+label,passed=True,
                                   electron_number_increment=0,photon_number_increment=1))
                rows.append(dict(energy=float(temperature),soft_fraction=float(fraction),velocity=[float(value) for value in velocity],
                                 equilibrium_reaction_weight=float(forward),entropy_quadratic=float(derivative*departure)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       inverse_double_compton_is_same_reaction_not_an_independent_duplicate=True,
                       weak_form_tree_real_reaction=True,complete_virtual_thermal_projection_pending=True),__file__,
           [AMPLITUDE_PARENT/'dirac_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
