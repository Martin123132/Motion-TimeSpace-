import numpy as np
from scipy.interpolate import CubicSpline
from common import ALGEBRA,GATE,guard,require,write,digest
from harmonics import harmonics


def coefficients(parent,efold,rotated):
    context=parent.context(efold)
    metric,observed,physical=parent.metric(context,rotated)
    terms,metadata=parent.stress(context["current"][11],parent.project(physical))
    amplitude=complex(*rotated[parent.slots])
    scale,hubble,omega,background=context["scale"],context["hubble"],context["omega"],context["A"]
    hminus=omega*background**2/(8*scale**2*hubble**2)
    phase=np.exp(2j*context["phase"])
    hzero=-(observed[0]+3*observed[1])/(6*hubble**2)-2*np.real(hminus/phase)
    zzero=-(observed[2]+3*np.sum(terms[:6,2]))/(2*parent.wave*hubble)-metric*observed[0]/(3*hubble**2)
    values=harmonics(scale,omega,hubble,parent.wave,context["mu"],background,amplitude,metric,hzero,zzero)
    primitive=phase*values[1]/(2j*context["mu"])+phase**2*values[2]/(4j*context["mu"])
    return primitive,values,context,metadata


class CoefficientTable:
    def __init__(self,efolds,values,support):
        self.support=np.array(support,dtype=int)
        self.fine=CubicSpline(efolds,values,axis=0)
        keep=np.unique(np.r_[np.arange(0,len(efolds),2),len(efolds)-1])
        self.coarse=CubicSpline(efolds[keep],values[keep],axis=0)

    def row(self,efold,order=0,coarse=False):
        return (self.coarse if coarse else self.fine)(efold,order)

    def apply(self,efold,vector,order=0,coarse=False):
        return np.dot(self.row(efold,order,coarse),vector[self.support])


def prepare_table(parent,efolds,units,core,mapping,signature,folder):
    if parent.model=="cold":
        write(folder/"micromotion-table-check.json",dict(passed=True,cold_identity=True,background_only=True))
        return None
    require(signature[16]==0 and signature[17]==0,"unhandled thermal-pressure perturbation state")
    native_columns=[1,2,3,int(signature[3]),int(signature[4])]+list(range(int(signature[2]),int(signature[2])+4))
    native_columns += [int(signature[50])+node*(int(signature[40])+1) for node in range(5)]
    core_native=mapping[core]
    support=np.array([int(np.flatnonzero(core_native==value)[0]) for value in native_columns],dtype=int)
    require(len(set(support))==14 and all(slot in support for slot in parent.slots),"pressure/density support")
    values=np.zeros((len(efolds),len(support)),complex)
    for index,efold in enumerate(efolds):
        if index%64==0:
            guard()
        for column,slot in enumerate(support):
            basis=np.zeros(len(units))
            basis[slot]=units[slot]
            values[index,column]=coefficients(parent,efold,basis)[0]/units[slot]
    table=CoefficientTable(efolds,values,support)
    seed=np.sin(np.arange(1,len(units)+1))*units
    probes=np.unique(np.linspace(2,len(efolds)-4,97,dtype=int))
    offgrid_errors=[]
    support_errors=[]
    derivative_changes=[]
    amplitude_unit=max(units[parent.slots])
    for index in probes:
        guard()
        current=float(efolds[index])
        direct=coefficients(parent,current,seed)[0]
        sparse=table.apply(current,seed)
        support_errors.append(float(abs(direct-sparse)/max(abs(direct),amplitude_unit)))
        midpoint=float((efolds[index]+efolds[index+1])/2)
        direct_midpoint=coefficients(parent,midpoint,seed)[0]
        interpolated=table.apply(midpoint,seed)
        weighted_size=float(np.sum(abs(table.row(midpoint))*units[support]))
        offgrid_errors.append(float(abs(direct_midpoint-interpolated)/max(weighted_size,1e-80)))
        derivative_changes.append(float(abs(table.apply(midpoint,seed,1)-table.apply(midpoint,seed,1,True))/amplitude_unit))
    require(max(support_errors)<ALGEBRA and max(offgrid_errors)<GATE and max(derivative_changes)<GATE,"sparse coefficient representation")
    path=folder/"micromotion-coefficients.npz"
    np.savez_compressed(path,efold=efolds,coefficients=values,support=support,native_support=np.array(native_columns),units=units)
    write(folder/"micromotion-table-check.json",dict(passed=True,background_only=True,no_future_perturbations=True,
          support_error=max(support_errors),midpoint_interpolation_error=max(offgrid_errors),
          coefficient_derivative_refinement_per_unit=max(derivative_changes),probes=len(probes),
          source_sha256=digest(__file__),output=path.name,output_sha256=digest(path),
          support_from="native stress density/pressure and eta; explicit five neutrino monopoles; no thermal perturbation state"))
    return table


class Micromotion:
    def __init__(self,parent,table,reduced,coarse=False):
        self.parent,self.table,self.reduced,self.coarse=parent,table,reduced,coarse
        self.model,self.slots=parent.model,parent.slots

    def forward(self,efold,rotated):
        normal=self.parent.forward(efold,rotated)
        if self.model=="heavy":
            primitive=self.table.apply(efold,rotated,coarse=self.coarse)
            normal[self.slots]-=[primitive.real,primitive.imag]
        return normal

    def inverse(self,efold,normal):
        if self.model=="cold":
            return normal.copy(),None,None
        context=self.parent.context(efold)
        spectator=normal.copy()
        spectator[self.slots]=0.
        metric,_,_=self.parent.metric(context,spectator)
        forcing=context["primitive"]*context["coupling"]*metric*np.conjugate(context["A"])
        other=self.table.apply(efold,spectator,coarse=self.coarse)
        row=self.table.row(efold,coarse=self.coarse)
        columns=[row[int(np.flatnonzero(self.table.support==slot)[0])] for slot in self.slots]
        matrix=context["matrix"]-np.array([[value.real for value in columns],[value.imag for value in columns]])
        size=float(np.max(np.sum(abs(np.eye(2)-matrix),axis=1)))
        require(size<1,"second inverse bound")
        amplitude=np.linalg.solve(matrix,normal[self.slots]+[forcing.real+other.real,forcing.imag+other.imag])
        result=normal.copy()
        result[self.slots]=amplitude
        return result,context,dict(matrix=matrix,correction_size=size)

    def rates(self,efold,normal,exact=False):
        if self.model=="cold":
            rate,diagnostics=self.parent.rates(efold,normal,exact=True)
            for key in ("retained_mean","represented_defect","second_remainder","second_full_rate","second_desired_rate","map_primitive","direct_primitive","map_chain_rate","first_amplitude"):
                diagnostics[key]=np.zeros(2)
            return rate,diagnostics
        rotated,_,inverse=self.inverse(efold,normal)
        first=self.parent.forward(efold,rotated)
        first_rate,first_diagnostics=self.parent.rates(efold,first,exact=True)
        native_rate=self.parent.rotate_rhs(efold,rotated)
        direct,values,context,metadata=coefficients(self.parent,efold,rotated)
        primitive=self.table.apply(efold,rotated,coarse=self.coarse)
        primitive_rate=(self.table.apply(efold,rotated,1,self.coarse)+
                        self.table.apply(efold,native_rate,coarse=self.coarse))
        first_remainder=complex(*first_diagnostics["remainder"])
        phase=np.exp(2j*context["phase"])
        represented=first_remainder-values[0]-phase*values[1]-phase**2*values[2]
        slow=complex(*first_rate[self.slots])-first_remainder
        full=complex(*first_rate[self.slots])-primitive_rate
        retained=slow+values[0]+represented
        drop=self.reduced and not exact
        desired=retained if drop else full
        difference=desired-full
        defect_rotated=np.linalg.solve(inverse["matrix"],[difference.real,difference.imag])
        defect_state=np.zeros_like(normal)
        defect_state[self.slots]=defect_rotated
        defect_physical=self.parent.rotate_decode(efold,defect_state)[self.slots]
        hubble,omega=context["hubble"],context["omega"]
        density_correction=hubble*(metadata[15]*defect_physical[1]+omega**2*metadata[14]*defect_physical[0])
        momentum_correction=hubble*self.parent.wave*metadata[15]*defect_physical[0]
        bound=float(max(abs(difference.real),abs(difference.imag))/(1-inverse["correction_size"]))
        require(np.max(abs(defect_rotated))<=bound*(1+ALGEBRA)+1e-80,"second derivative defect bound")
        rate=first_rate.copy()
        rate[self.slots]=[desired.real,desired.imag]
        pair=lambda value:np.array([value.real,value.imag])
        diagnostics=dict(remainder=first_diagnostics["remainder"],retained_mean=pair(values[0]),represented_defect=pair(represented),
                         derivative_defect=defect_physical,stress_correction=np.array([density_correction,momentum_correction]),
                         correction_size=inverse["correction_size"],inverse_bound=1/(1-inverse["correction_size"]),defect_bound=bound,
                         hlog_difference=first_diagnostics["hlog_difference"],second_remainder=pair(full-retained),
                         second_full_rate=pair(full),second_desired_rate=pair(desired),map_primitive=pair(primitive),
                         direct_primitive=pair(direct),map_chain_rate=pair(primitive_rate),first_amplitude=first[self.slots])
        return rate,diagnostics

    def rhs(self,efold,normal):
        return self.rates(efold,normal)[0]

    def preflight(self,efold,rotated,units):
        normal=self.forward(efold,rotated)
        inverted,_,_=self.inverse(efold,normal)
        inverse_error=float(np.max(abs(inverted-rotated)/units))
        rate=self.parent.rotate_rhs(efold,rotated)
        mapped=self.forward(efold,rate)
        approximations=[]
        for step in (1e-6,5e-7):
            partial=(self.forward(efold-2*step,rotated)-8*self.forward(efold-step,rotated)+
                     8*self.forward(efold+step,rotated)-self.forward(efold+2*step,rotated))/(12*step)
            approximations.append(partial+mapped)
        full,_=self.rates(efold,normal,exact=True)
        scale=np.maximum(abs(full),units)
        chain=float(np.max(abs(full-approximations[-1])/scale))
        refinement=float(np.max(abs(approximations[-1]-approximations[0])/scale))
        zero=bool(np.count_nonzero(self.rhs(efold,np.zeros_like(normal)))==0)
        parity=float(np.max(abs(self.rhs(efold,normal)+self.rhs(efold,-normal))/scale))
        require(inverse_error<ALGEBRA and max(chain,refinement,parity)<GATE and zero,"second map preflight")
        return dict(inverse_error=inverse_error,chain_error=chain,derivative_refinement=refinement,parity=parity,
                    zero_exact=zero,finite_difference_steps=[1e-6,5e-7],coarse_coefficients=self.coarse,
                    derivative_rule="analytic derivative of background-only cubic row plus row times current native RHS")

