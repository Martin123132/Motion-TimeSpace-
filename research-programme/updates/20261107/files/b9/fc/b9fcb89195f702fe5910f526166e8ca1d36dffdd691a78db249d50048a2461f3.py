from stage165_common import *


class PreciseSoftShifts(PreciseBornCorrelated):
    def __init__(self,spectra,digits=80):
        super().__init__(spectra)
        self.digits=digits
        self.maximum_precise_pair=0.
        self.maximum_direction_repair=0.

    def difference_product(self,parameters,soft,direction,born_left,born_right):
        density,products,left=self.event_products(parameters,soft,direction)
        right=self.last_right
        with mp.workdps(self.digits):
            energy=mp.mpf(float(parameters['energy']))
            cosine=mp.mpf(float(parameters['cosine']))
            temperature=mp.mpf(float(parameters['temperature']))
            hard_direction=[mp.sqrt(1-cosine*cosine),mp.mpf(0),cosine]
            soft_direction=[mp.mpf(float(value)) for value in direction]
            horizontal=mp.sqrt((1-soft_direction[2]**2)/(soft_direction[0]**2+soft_direction[1]**2))
            soft_direction[0]*=horizontal
            soft_direction[1]*=horizontal
            self.maximum_direction_repair=max(self.maximum_direction_repair,max(float(abs(soft_direction[index]-mp.mpf(float(direction[index])))) for index in range(3)))
            angular=1-cosine
            mixed=1-sum(hard_direction[index]*soft_direction[index] for index in range(3))
            incident_soft=1-soft_direction[2]
            initial_denominator=1+energy*angular
            hard=energy/initial_denominator
            recoil0=[-hard*hard_direction[0],mp.mpf(0),energy-hard*hard_direction[2]]
            initial_recoil_energy=mp.sqrt(1+sum(value*value for value in recoil0))
            transform=[mp.mpf(float(value)) for value in parameters['transform'][0]]
            delta=[]
            for signed in soft:
                signed=mp.mpf(float(signed))
                denominator=initial_denominator-signed*mixed
                hard_shift=-signed*((1+energy*incident_soft)*initial_denominator-energy*mixed)/(initial_denominator*denominator)
                energy_shift=signed*(energy*(initial_denominator*(angular-incident_soft)+mixed)-signed*mixed*initial_denominator)/(initial_denominator*denominator)
                recoil_shift=[-hard_shift*hard_direction[index]-signed*soft_direction[index] for index in range(3)]
                recoil=[recoil0[index]+recoil_shift[index] for index in range(3)]
                numerator=2*sum(recoil0[index]*recoil_shift[index] for index in range(3))+sum(value*value for value in recoil_shift)
                rest_shift=numerator/(mp.sqrt(1+sum(value*value for value in recoil))+initial_recoil_energy)
                boost=sum(transform[index+1]*recoil_shift[index] for index in range(3))
                photon=(transform[0]*energy_shift-boost)/temperature
                electron=(transform[0]*rest_shift+boost)/temperature
                self.maximum_precise_pair=max(self.maximum_precise_pair,float(abs(photon+electron)/max(abs(photon),abs(electron),mp.mpf('1e-300'))))
                delta.append([float(photon),float(mp.sign(signed)),float(electron)])
            delta=np.array(delta)
        difference=np.einsum('ni,nj->nij',delta,right)+np.einsum('i,nj->nij',born_left,right-born_right)
        return density,difference,left,delta
