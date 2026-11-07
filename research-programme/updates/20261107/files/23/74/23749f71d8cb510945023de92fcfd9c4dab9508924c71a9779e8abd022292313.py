from __future__ import annotations

from evolution_common import *


class CoupledSystem:
    def __init__(self,background,maximum=8):
        self.background=background
        self.angular=Angular(maximum)
        self.directions=self.angular.directions
        self.weights=self.angular.weights
        self.screen=self.angular.screen
        self.count=len(self.weights)
        self.size=26+10*self.count
        self.momenta=np.array([[.1,0.,0.],[0.,.1,0.],[.1,.1,0.],[.1,.1,0.]])
        self.cold_numbers=np.zeros(4,complex)
        self.mass2=background.masses**2

    def unpack(self,state):
        return dict(metric=state[:9].reshape(3,3),rate=state[9:18].reshape(3,3),field=state[18:20],
            prime=state[20:22],number=state[22],velocity=state[23:26],
            photon=state[26:26+9*self.count].reshape(self.count,3,3),neutrino=state[26+9*self.count:])

    def pack(self,metric,rate,field,prime,number,velocity,photon,neutrino):
        return np.r_[metric.ravel(),rate.ravel(),field,prime,number,velocity,photon.ravel(),neutrino]

    def moments(self,state):
        parts=self.unpack(state)
        return self.angular.moments(parts['photon']),self.angular.moments(parts['neutrino'])

    def stress(self,moment,states):
        background=self.background.at(moment)
        scale=background['scale']
        fields=background['fields']
        prime=background['prime']
        output=[]
        pieces=[self.unpack(state) for state in states]
        moments=[self.moments(state) for state in states]
        for index,parts in enumerate(pieces):
            photon,neutrino=moments[index]
            theta_metric=np.trace(parts['metric'])/2
            energy=(background['cold']*(self.cold_numbers[index]-theta_metric)+background['baryon']*(parts['number']-theta_metric)+
                background['photon']*photon[0]+background['neutrino']*neutrino[0]+
                np.sum(prime*parts['prime']/scale**2+self.mass2*fields*parts['field']))
            momentum=(scale*(background['baryon']*parts['velocity']+background['photon']*photon[1]+background['neutrino']*neutrino[1])-
                1j*self.momenta[index]*np.sum(prime*parts['field'])/scale)
            stress=(background['photon']*photon[2]+background['neutrino']*neutrino[2]+
                np.eye(3)*np.sum(prime*parts['prime']/scale**2-self.mass2*fields*parts['field']))
            if index==3:
                left,right=pieces[:2]
                hleft,hright=left['metric'],right['metric']
                volume_left,volume_right=np.trace(hleft)/2,np.trace(hright)/2
                volume_quadratic=-np.trace(hleft@hright)/4
                determinant_quadratic=volume_left*volume_right/2-volume_quadratic
                number_product=(volume_left*right['number']+volume_right*left['number'])/2
                velocity_product=left['velocity']@right['velocity']
                energy+=background['cold']*determinant_quadratic+background['baryon']*(determinant_quadratic-number_product+velocity_product/2)
                density_left=left['number']-volume_left
                density_right=right['number']-volume_right
                momentum+=scale*background['baryon']*(density_left*right['velocity']+density_right*left['velocity'])/2
                stress+=background['baryon']*(np.outer(left['velocity'],right['velocity'])+np.outer(right['velocity'],left['velocity']))/2
                for category,weight in [(0,background['photon']),(1,background['neutrino'])]:
                    flux_left,flux_right=moments[0][category][1],moments[1][category][1]
                    stress_left,stress_right=moments[0][category][2],moments[1][category][2]
                    momentum+=scale*weight*(hleft@flux_right+hright@flux_left)/4
                    stress+=weight*(stress_left@hright+stress_right@hleft-hleft@stress_right-hright@stress_left)/4
                dot=self.momenta[0]@self.momenta[1]
                product=left['field']*right['field']
                kinetic=left['prime']*right['prime']
                energy+=np.sum(kinetic+(scale**2*self.mass2-dot)*product)/(2*scale**2)
                pressure=np.sum(kinetic-(scale**2*self.mass2-dot/3)*product)/(2*scale**2)
                tensor=(np.outer(self.momenta[0],self.momenta[1])+np.outer(self.momenta[1],self.momenta[0]))/2-np.eye(3)*dot/3
                stress+=np.eye(3)*pressure-tensor*np.sum(product)/scale**2
                momentum-=1j*(self.momenta[1]*np.sum(left['prime']*right['field'])+self.momenta[0]*np.sum(right['prime']*left['field']))/(2*scale)
            output.append((energy,momentum,stress))
        return output

    def local_ray(self,metric,rate,momentum):
        first=1j*np.einsum('a,ij->aij',momentum,metric)
        rotation=np.empty((self.count,3,3),complex)
        for left in range(3):
            for right in range(3):
                rotation[:,left,right]=self.directions@(first[left,right,:]-first[right,left,:])/2
        projected=np.einsum('ni,ij,nj->n',self.directions,rate,self.directions)
        direction_rate=np.einsum('nij,nj->ni',rotation,self.directions)-self.directions@rate.T+projected[:,None]*self.directions
        generator=rotation+np.einsum('ni,nj,jk->nik',self.directions,self.directions,rate)
        coordinate_velocity=-self.directions@metric.T/2
        return coordinate_velocity,direction_rate,generator,projected

    def collision_quadratic(self,photon,velocity,density):
        screen=self.screen
        zeroth=screen/2
        projected=self.directions@velocity
        speed2=velocity@velocity
        rotation1=np.einsum('ni,j->nij',self.directions,velocity)@screen
        rotation2=(projected[:,None,None]*np.einsum('ni,j->nij',self.directions,velocity)-.5*np.outer(velocity,velocity))@screen
        trans1=np.swapaxes(rotation1,1,2)
        trans2=np.swapaxes(rotation2,1,2)
        mean0=collision.mean_matrix(self.weights,zeroth)
        moving1=photon+rotation1@zeroth+zeroth@trans1
        mean1=collision.mean_matrix(self.weights,moving1-2*projected[:,None,None]*zeroth)
        moving2=rotation1@photon+photon@trans1+rotation2@zeroth+zeroth@trans2+rotation1@zeroth@trans1
        mean2=collision.mean_matrix(self.weights,moving2-2*projected[:,None,None]*moving1+(projected**2+speed2)[:,None,None]*zeroth)
        gain0=1.5*screen@mean0@screen
        gain1=1.5*(screen@mean1@screen+trans1@mean0@screen+screen@mean0@rotation1)
        gain2=1.5*(screen@mean2@screen+trans1@mean1@screen+screen@mean1@rotation1+trans2@mean0@screen+screen@mean0@rotation2+trans1@mean0@rotation1)
        gain2+=3*projected[:,None,None]*gain1+(6*projected**2-1.5*speed2)[:,None,None]*gain0
        result=gain2+projected[:,None,None]*photon-.5*speed2*zeroth
        result+=density*(gain1+3*projected[:,None,None]*gain0-photon+projected[:,None,None]*zeroth)
        return result

    def slow_rhs(self,moment,states):
        background=self.background.at(moment)
        scale,hubble=background['scale'],background['hubble']
        stresses=self.stress(moment,states)
        pieces=[self.unpack(state) for state in states]
        output=np.empty_like(states)
        for index,parts in enumerate(pieces):
            momentum=self.momenta[index]
            energy,_,stress=stresses[index]
            trace_rate=np.trace(parts['rate'])
            metric_prime=2*parts['rate']
            ricci=inherited.linear_ricci(parts['metric'],momentum)
            rate_prime=-2*hubble*parts['rate']-ricci-hubble*trace_rate*np.eye(3)+scale**2*(stress+np.eye(3)*(energy-np.trace(stress))/2)
            field_prime=parts['prime']
            prime_prime=-2*hubble*parts['prime']-(momentum@momentum+scale**2*self.mass2)*parts['field']-trace_rate*background['prime']
            number_prime=-1j*momentum@parts['velocity']
            velocity_prime=-hubble*parts['velocity']
            photon_prime=-1j*(self.directions@momentum)[:,None,None]*parts['photon']-2*np.einsum('ni,ij,nj->n',self.directions,parts['rate'],self.directions)[:,None,None]*self.screen
            neutrino_prime=-1j*(self.directions@momentum)*parts['neutrino']-4*np.einsum('ni,ij,nj->n',self.directions,parts['rate'],self.directions)
            if index==3:
                left,right=pieces[:2]
                hleft,hright=left['metric'],right['metric']
                metric_prime=metric_prime+hleft@right['rate']+hright@left['rate']
                rate_prime-=inherited.quadratic_ricci(hleft,hright,self.momenta[0],self.momenta[1])
                rate_prime-=(np.trace(left['rate'])*right['rate']+np.trace(right['rate'])*left['rate'])/2
                dot=self.momenta[0]@self.momenta[1]
                prime_prime-=(np.trace(left['rate'])*right['prime']+np.trace(right['rate'])*left['prime'])/2
                prime_prime+=((momentum@hleft@self.momenta[1]-dot*np.trace(hleft)/2)*right['field']+
                    (momentum@hright@self.momenta[0]-dot*np.trace(hright)/2)*left['field'])/2
                number_prime-=1j*momentum@((left['number']*right['velocity']+right['number']*left['velocity']-hleft@right['velocity']-hright@left['velocity'])/2)
                velocity_prime-=1j*((self.momenta[1]@left['velocity'])*right['velocity']+(self.momenta[0]@right['velocity'])*left['velocity'])/2
                for own,partner,own_momentum,partner_momentum in [(left,right,self.momenta[0],self.momenta[1]),(right,left,self.momenta[1],self.momenta[0])]:
                    coordinate,direction,generator,redshift=self.local_ray(own['metric'],own['rate'],own_momentum)
                    photon_gradient=self.angular.gradient(partner['photon'])
                    neutrino_gradient=self.angular.gradient(partner['neutrino'])
                    photon_prime+=.5*(-1j*(coordinate@partner_momentum)[:,None,None]*partner['photon']-
                        np.einsum('ni,niab->nab',direction,photon_gradient)-4*redshift[:,None,None]*partner['photon']+
                        generator@partner['photon']+partner['photon']@np.swapaxes(generator,1,2))
                    neutrino_prime+=.5*(-1j*(coordinate@partner_momentum)*partner['neutrino']-
                        np.einsum('ni,ni->n',direction,neutrino_gradient)-4*redshift*partner['neutrino'])
                density_left=left['number']-np.trace(hleft)/2
                density_right=right['number']-np.trace(hright)/2
                collision_source=(self.collision_quadratic(left['photon']+right['photon'],left['velocity']+right['velocity'],density_left+density_right)-
                    self.collision_quadratic(left['photon'],left['velocity'],density_left)-self.collision_quadratic(right['photon'],right['velocity'],density_right))/2
                metric_velocity=-(hleft@right['velocity']+hright@left['velocity'])/4
                collision_source+=2*(self.directions@metric_velocity)[:,None,None]*self.screen
                photon_prime+=background['opacity']*collision_source
                photon_left=self.angular.moments(left['photon'])
                photon_right=self.angular.moments(right['photon'])
                acceleration=((hleft@photon_right[1]+hright@photon_left[1])/4-
                    ((photon_left[2]+np.eye(3)*photon_left[0])@right['velocity']+(photon_right[2]+np.eye(3)*photon_right[0])@left['velocity'])/2)
                velocity_prime+=background['opacity']*background['photon']/background['baryon']*acceleration
            output[index]=self.pack(metric_prime,rate_prime,field_prime,prime_prime,number_prime,velocity_prime,photon_prime,neutrino_prime)
        return output

    def collision_rhs(self,moment,states):
        background=self.background.at(moment)
        output=np.zeros_like(states)
        for index,state in enumerate(states):
            parts=self.unpack(state)
            mean=collision.mean_matrix(self.weights,parts['photon'])
            radiation=background['opacity']*(1.5*self.screen@mean@self.screen-parts['photon']+2*(self.directions@parts['velocity'])[:,None,None]*self.screen)
            flux=self.angular.moments(parts['photon'])[1]
            velocity=background['opacity']/background['ratio']*(.75*flux-parts['velocity'])
            output[index,23:26]=velocity
            output[index,26:26+9*self.count]=radiation.ravel()
        return output

    def propagate_collision(self,states,ratio,depth,kind='exp'):
        coefficient=1 if kind in ['exp','phi1'] else .5
        output=coefficient*states.copy()
        for index,state in enumerate(states):
            parts=self.unpack(state)
            radiation,velocity=self.angular.projectors.apply(parts['photon'],parts['velocity'],ratio,depth,kind)
            output[index,23:26]=velocity
            output[index,26:26+9*self.count]=radiation.ravel()
        return output

    def constraints(self,moment,states):
        background=self.background.at(moment)
        stresses=self.stress(moment,states)
        pieces=[self.unpack(state) for state in states]
        output=[]
        for index,parts in enumerate(pieces):
            momentum=self.momenta[index]
            energy,current,_=stresses[index]
            ricci=inherited.linear_ricci(parts['metric'],momentum)
            hamiltonian=np.trace(ricci)+4*background['hubble']*np.trace(parts['rate'])-2*background['scale']**2*energy
            vector=1j*momentum*np.trace(parts['rate'])-1j*momentum@parts['rate']-background['scale']*current
            if index==3:
                left,right=pieces[:2]
                hamiltonian+=np.trace(inherited.quadratic_ricci(left['metric'],right['metric'],self.momenta[0],self.momenta[1]))
                hamiltonian+=np.trace(left['rate'])*np.trace(right['rate'])-np.trace(left['rate']@right['rate'])
                for own,partner,own_momentum in [(left,right,self.momenta[0]),(right,left,self.momenta[1])]:
                    connection=geometry.christoffel_linear(1j*np.einsum('a,ij->aij',own_momentum,own['metric']))
                    for component in range(3):
                        vector[component]+=.5*sum(-connection[upper,upper,middle]*partner['rate'][middle,component]+connection[middle,upper,component]*partner['rate'][upper,middle] for upper in range(3) for middle in range(3))
            output.append(np.r_[hamiltonian,vector])
        return np.array(output)

    def project_constraints(self,moment,states):
        output=states.copy()
        changes=[]
        for index in range(4):
            if index==3:
                left,right=[self.unpack(state) for state in output[:2]]
                commutator=(left['metric']@right['rate']-right['rate']@left['metric']+
                    right['metric']@left['rate']-left['rate']@right['metric'])/2
                current=output[index,9:18].reshape(3,3)
                output[index,9:18]=((current+current.T)/2-commutator/2).ravel()
            residual=self.constraints(moment,output)[index]
            hubble=self.background.at(moment)['hubble']
            trace_change=-residual[0]/(4*hubble)
            momentum=self.momenta[index]
            magnitude=np.linalg.norm(momentum)
            axis=momentum/magnitude
            column=(momentum*trace_change-1j*residual[1:])/magnitude
            parallel=axis@column
            transverse=column-parallel*axis
            adjustment=parallel*np.outer(axis,axis)+np.outer(axis,transverse)+np.outer(transverse,axis)+(trace_change-parallel)*(np.eye(3)-np.outer(axis,axis))/2
            output[index,9:18]+=adjustment.ravel()
            changes.append(float(np.linalg.norm(adjustment))/max(float(np.linalg.norm(states[index,9:18])),1e-30))
        return output,changes
