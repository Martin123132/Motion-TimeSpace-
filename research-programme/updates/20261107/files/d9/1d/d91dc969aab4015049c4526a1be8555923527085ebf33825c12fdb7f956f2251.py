import numpy as np
from common import ALGEBRA, GATE, require


class NearIdentity:
    def __init__(self, model, reduced, slots, mass, wave, anchor, point, carrier, carrier_rate, hubble_log,
                 rotate_decode, rotate_rhs, project, observe, stress):
        self.model,self.reduced,self.slots=model,reduced,slots
        self.mass,self.wave,self.anchor=mass,wave,anchor
        self.point,self.carrier,self.carrier_rate,self.hubble_log=point,carrier,carrier_rate,hubble_log
        self.rotate_decode,self.rotate_rhs,self.project=rotate_decode,rotate_rhs,project
        self.observe,self.stress=observe,stress

    def context(self,efold):
        current=self.point(efold)
        scale,hubble=current[10],current[12]
        omega=scale*self.mass
        phase,mu=self.carrier(efold)
        mu_rate=float(self.carrier_rate(efold,1))
        hlog=float(self.hubble_log(efold,1))
        rotation=np.exp(1j*phase)
        field=self.anchor+current[2]
        velocity=current[3]
        amplitude=scale*(np.sqrt(omega)*field+1j*velocity/np.sqrt(omega))*rotation
        amplitude_rate=(rotation*(scale*np.sqrt(omega)*(1.5*field+current[7])+
                                   1j*scale/np.sqrt(omega)*(.5*velocity+current[8]))+
                        1j*mu*amplitude)
        gamma=self.wave**2/(2*omega*hubble)
        coupling=self.wave/(2*hubble)
        primitive=rotation**2/(2j*mu)
        density_row=omega/(2*self.wave*hubble*scale**2)*np.array([amplitude.real,amplitude.imag])
        columns=[primitive*((1.5-1j*gamma)*value.conjugate()+coupling*density_row[index]*amplitude.conjugate())
                 for index,value in enumerate((1+0j,1j))]
        correction=np.array([[value.real for value in columns],[value.imag for value in columns]])
        matrix=np.eye(2)-correction
        size=float(np.max(np.sum(abs(correction),axis=1)))
        require(size<1,"near-identity inverse not bounded")
        return dict(current=current,scale=scale,hubble=hubble,omega=omega,phase=phase,mu=mu,mu_rate=mu_rate,
                    hlog=hlog,rotation=rotation,A=amplitude,A_rate=amplitude_rate,gamma=gamma,coupling=coupling,
                    primitive=primitive,density_row=density_row,matrix=matrix,correction_size=size)

    def metric(self,context,rotated):
        physical=self.rotate_decode(float(np.log(context["scale"])),rotated)
        observed=self.observe(context["current"][11],self.project(physical))
        metric=(observed[2]/(2*self.wave)+self.wave*observed[7])/context["hubble"]
        return metric,observed,physical

    def forward(self,efold,rotated):
        if self.model=="cold":
            return rotated.copy()
        context=self.context(efold)
        metric,_,_=self.metric(context,rotated)
        amplitude=complex(*rotated[self.slots])
        coefficient=(1.5-1j*context["gamma"])*amplitude.conjugate()+context["coupling"]*metric*context["A"].conjugate()
        normal=amplitude-context["primitive"]*coefficient
        result=rotated.copy()
        result[self.slots]=[normal.real,normal.imag]
        return result

    def inverse(self,efold,normal):
        if self.model=="cold":
            return normal.copy(),None
        context=self.context(efold)
        spectator=normal.copy()
        spectator[self.slots]=0.
        metric,_,_=self.metric(context,spectator)
        forcing=context["primitive"]*context["coupling"]*metric*context["A"].conjugate()
        amplitude=np.linalg.solve(context["matrix"],normal[self.slots]+[forcing.real,forcing.imag])
        result=normal.copy()
        result[self.slots]=amplitude
        return result,context

    def rates(self,efold,normal,exact=False):
        rotated,context=self.inverse(efold,normal)
        native_rate=self.rotate_rhs(efold,rotated)
        if self.model=="cold":
            return native_rate,dict(remainder=np.zeros(2),derivative_defect=np.zeros(2),stress_correction=np.zeros(2),
                                    correction_size=0.,inverse_bound=1.,defect_bound=0.,hlog_difference=0.)
        context=self.context(efold)
        metric,observed,physical=self.metric(context,rotated)
        terms,metadata=self.stress(context["current"][11],self.project(physical))
        amplitude=complex(*rotated[self.slots])
        amplitude_rate=complex(*native_rate[self.slots])
        hubble=context["hubble"]
        metric_rate=(np.sum(terms[:,3])/(2*self.wave)+self.wave*observed[8])/hubble**2-context["hlog"]*metric
        gamma_rate=-context["gamma"]*(1+context["hlog"])
        coupling_rate=-context["coupling"]*context["hlog"]
        coefficient=(1.5-1j*context["gamma"])*amplitude.conjugate()+context["coupling"]*metric*context["A"].conjugate()
        coefficient_rate=(-1j*gamma_rate*amplitude.conjugate()+
                          (1.5-1j*context["gamma"])*amplitude_rate.conjugate()+
                          coupling_rate*metric*context["A"].conjugate()+
                          context["coupling"]*metric_rate*context["A"].conjugate()+
                          context["coupling"]*metric*context["A_rate"].conjugate())
        remainder=-context["primitive"]*(coefficient_rate-context["mu_rate"]/context["mu"]*coefficient)
        slow=(-1j*context["gamma"]*amplitude-context["coupling"]*metric*context["A"]+
              1j*(context["mu"]-context["omega"]/hubble)*amplitude)
        drop=self.reduced and not exact
        desired=slow if drop else slow+remainder
        rate=native_rate.copy()
        rate[self.slots]=[desired.real,desired.imag]
        defect_rotated=np.linalg.solve(context["matrix"],-[remainder.real,remainder.imag]) if drop else np.zeros(2)
        defect_state=np.zeros_like(normal)
        defect_state[self.slots]=defect_rotated
        defect_physical=self.rotate_decode(efold,defect_state)[self.slots]
        field,velocity=context["A"],metadata[15]
        actual_field=metadata[14]
        density_correction=hubble*(velocity*defect_physical[1]+context["omega"]**2*actual_field*defect_physical[0])
        momentum_correction=hubble*self.wave*velocity*defect_physical[0]
        background_defect=0.
        for offset in (4,14):
            background_field,background_velocity,field_rate,velocity_rate,mass=metadata[offset:offset+5]
            field_defect=field_rate-background_velocity
            velocity_defect=velocity_rate+2*hubble*background_velocity+(context["scale"]*mass)**2*background_field
            background_defect+=background_velocity*velocity_defect+(context["scale"]*mass)**2*background_field*field_defect
        hlog_from_sources=-(observed[0]+3*observed[1])/(6*hubble**2)+background_defect/(6*hubble**3)
        local_bound=float(max(abs(remainder.real),abs(remainder.imag))/(1-context["correction_size"]))
        require(np.max(abs(defect_rotated))<=local_bound*(1+ALGEBRA)+1e-80,"Neumann defect bound")
        diagnostics=dict(remainder=np.array([remainder.real,remainder.imag]),derivative_defect=defect_physical,
                         stress_correction=np.array([density_correction,momentum_correction]),
                         correction_size=context["correction_size"],inverse_bound=1/(1-context["correction_size"]),
                         defect_bound=local_bound,hlog_difference=float(context["hlog"]-hlog_from_sources))
        return rate,diagnostics

    def rhs(self,efold,normal):
        return self.rates(efold,normal)[0]

    def preflight(self,efold,rotated,units):
        normal=self.forward(efold,rotated)
        inverted,_=self.inverse(efold,normal)
        inverse_error=float(np.max(abs(inverted-rotated)/units))
        rate=self.rotate_rhs(efold,rotated)
        mapped_rate=self.forward(efold,rate)
        derivatives=[]
        for step in (1e-6,5e-7):
            partial=(self.forward(efold-2*step,rotated)-8*self.forward(efold-step,rotated)+
                     8*self.forward(efold+step,rotated)-self.forward(efold+2*step,rotated))/(12*step)
            derivatives.append(partial+mapped_rate)
        exact,_=self.rates(efold,normal,exact=True)
        denominator=np.maximum(abs(exact),units)
        chain_error=float(np.max(abs(exact-derivatives[-1])/denominator))
        refinement=float(np.max(abs(derivatives[0]-derivatives[1])/denominator))
        zero_error=np.count_nonzero(self.rhs(efold,np.zeros_like(normal)))
        parity=float(np.max(abs(self.rhs(efold,normal)+self.rhs(efold,-normal))/np.maximum(abs(exact),units)))
        require(inverse_error<ALGEBRA and max(chain_error,refinement,parity)<GATE and zero_error==0,"normal-form preflight")
        return dict(inverse_error=inverse_error,chain_error=chain_error,derivative_refinement=refinement,parity=parity,
                    zero_exact=zero_error==0,finite_difference_steps=[1e-6,5e-7])
