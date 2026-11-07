from common import ROOT,NORMAL,BACKGROUND,GATE,ALGEBRA,modest,guard,check_prior,require,read,write,digest,load
from harmonics import harmonics,verify
import numpy as np
from scipy.interpolate import CubicSpline


def norm(values):
    return max(float(np.max(abs(values))),1e-80)


def sup(values):
    return float(np.max(abs(values)))


def variation_bound(spline):
    widths=np.diff(spline.x)
    return float(np.sum(abs(spline.c[0])*widths**3+abs(spline.c[1])*widths**2+abs(spline.c[2])*widths))


def magnitude_bound(spline):
    widths=np.diff(spline.x)
    return float(np.max(abs(spline.c[0])*widths**3+abs(spline.c[1])*widths**2+abs(spline.c[2])*widths+abs(spline.c[3])))


def rapid_integral(efolds,phase,mu,coefficients,scale):
    frequency=CubicSpline(efolds,mu)
    widths=np.diff(efolds)
    minimum=float(np.min(frequency.c[3]-abs(frequency.c[2])*widths-abs(frequency.c[1])*widths**2-abs(frequency.c[0])*widths**3))
    require(minimum>0,"positive phase derivative polynomial lower bound")
    phase_function=frequency.antiderivative()
    reconstructed_phase=phase[0]+phase_function(efolds)-phase_function(efolds[0])
    phase_error=sup(reconstructed_phase-phase)
    contributions=[]
    primitive=np.zeros(len(efolds),complex)
    correction=np.zeros(len(efolds),complex)
    rapid=np.zeros(len(efolds),complex)
    interior_bound=0.
    for index,values in enumerate(coefficients,start=1):
        coefficient=CubicSpline(efolds,values)
        rotation=np.exp(2j*index*reconstructed_phase)
        term=rotation*values/(2j*index*mu)
        primitive+=term
        correction+=rotation*(coefficient(efolds,1)-frequency(efolds,1)*values/mu)/(2j*index*mu)
        rapid+=rotation*values
        variation=variation_bound(coefficient)
        maximum=magnitude_bound(coefficient)
        bound=variation/(2*index*minimum)+maximum*variation_bound(frequency)/(2*index*minimum**2)
        interior_bound+=bound
        contributions.append(dict(harmonic=index,coefficient_variation_bound=variation,coefficient_sup_bound=maximum,interior_integral_bound=bound))
    direct=[]
    reconstructed=[]
    for stride in (1,2,4):
        keep=np.unique(np.r_[np.arange(0,len(efolds),stride),len(efolds)-1])
        source_integral=CubicSpline(efolds[keep],rapid[keep]).antiderivative()
        defect_integral=CubicSpline(efolds[keep],correction[keep]).antiderivative()
        direct.append(source_integral(efolds)-source_integral(efolds[0]))
        reconstructed.append(primitive-primitive[0]-defect_integral(efolds)+defect_integral(efolds[0]))
    bound=sup(primitive-primitive[0])+interior_bound
    error=sup(direct[0]-reconstructed[0])/scale
    refinement=max(sup(item-direct[0])/scale for item in direct[1:])
    excess=max(0.,sup(direct[0])-bound)/scale
    return dict(passed=max(error,refinement)<GATE and excess<ALGEBRA and phase_error<ALGEBRA,
                integration_by_parts_error=error,source_refinement=refinement,phase_reconstruction_error=phase_error,
                direct_integral_normalized=sup(direct[0])/scale,interpolant_bound_normalized=bound/scale,bound_excess=excess,
                minimum_frequency_lower_bound=minimum,terms=contributions,
                scope="analytic bound for declared cubic coefficient/frequency interpolants, sampled endpoint term; not global coupled trajectory error or unsampled physical coefficient bound"),dict(rapid_integral=direct[0],ibp_integral=reconstructed[0],primitive=primitive,ibp_remainder=correction)


def main():
    modest()
    check_prior()
    symbolic=verify()
    write(ROOT/"harmonic-identities.json",dict(**symbolic,source_sha256=digest(ROOT/"harmonics.py")))
    parent=read(NORMAL/"prediction-owned-result.json")
    require(parent["state"]=="complete","closed full histories")
    destination=ROOT/"decomposition"
    destination.mkdir(exist_ok=False)
    reports=[]
    for family in parent["reports"]:
        guard()
        model,label,wave=family["model"],family["label"],family["wave"]
        stem=model+"-"+label
        case=next(row for row in family["cases"] if row["tag"]=="G192-full-fine")
        path=NORMAL/"runs-owned"/stem/case["file"]
        require(digest(path)==case["sha256"],"source packet")
        packet=load(path)
        if model=="cold":
            zero=all(np.count_nonzero(packet[key])==0 for key in ("normal_remainder","derivative_defect","stress_rate_correction"))
            require(zero,"cold no added scalar")
            report=dict(model=model,label=label,wave=wave,passed=True,cold_exact_zero=zero,input_sha256=case["sha256"],input=str(path))
            reports.append(report)
            write(destination/(stem+".json"),report)
            continue
        meta=packet["metadata"]
        efolds,scale,hubble,phase,mu=packet["efold"],packet["a"],packet["H"],packet["carrier_phase"],packet["carrier_derivative"]
        omega=scale*float(packet["mass"])
        background=scale*(np.sqrt(omega)*meta[:,14]+1j*meta[:,15]/np.sqrt(omega))*np.exp(1j*phase)
        amplitude=packet["envelope"][:,0]+1j*packet["envelope"][:,1]
        metric=meta[:,2]
        rotation=np.exp(2j*phase)
        gamma=wave**2/(2*omega*hubble)
        coupling=wave/(2*hubble)
        observer=packet["observer"]
        hcanonical=-(observer[:,0]+3*observer[:,1])/(6*hubble**2)
        zcanonical=-(observer[:,2]+3*packet["terms"][:,:,2].sum(axis=1))/(2*wave*hubble)-metric*observer[:,0]/(3*hubble**2)
        hminus=omega*background**2/(8*scale**2*hubble**2)
        zminus=3*omega*background*amplitude/(4*wave*hubble*scale**2)
        hzero=hcanonical-2*np.real(hminus/rotation)
        zzero=zcanonical-2*np.real(zminus/rotation)
        coefficients=harmonics(scale,omega,hubble,wave,mu,background,amplitude,metric,hzero,zzero)
        canonical=sum(value*rotation**index for index,value in enumerate(coefficients))
        background_packet=load(BACKGROUND/"runs"/model/"dop-half-cap.npz")
        hlog=CubicSpline(efolds,np.log(background_packet["H"]))(efolds,1)
        mu_rate=CubicSpline(efolds,background_packet["a"]*float(packet["mass"])/background_packet["H"])(efolds,1)
        zactual=(packet["terms"][:,:,3].sum(axis=1)/(2*wave)+wave*observer[:,8])/hubble**2-hlog*metric
        coefficient=(1.5-1j*gamma)*np.conjugate(amplitude)+coupling*metric*np.conjugate(background)
        actual_background_rate=(np.exp(1j*phase)*(scale*np.sqrt(omega)*(1.5*meta[:,14]+meta[:,16]/hubble)+
                               1j*scale/np.sqrt(omega)*(.5*meta[:,15]+meta[:,17]/hubble))+1j*mu*background)
        background_defect=actual_background_rate-1.5*rotation*np.conjugate(background)
        carrier_defect=1j*(mu-omega/hubble)*amplitude
        inside=(1j*gamma*(hlog-hcanonical)*np.conjugate(amplitude)+(1.5-1j*gamma)*np.conjugate(carrier_defect)-
                coupling*(hlog-hcanonical)*metric*np.conjugate(background)+coupling*(zactual-zcanonical)*np.conjugate(background)+
                coupling*metric*np.conjugate(background_defect)-(mu_rate/mu-(1-hcanonical))*coefficient)
        defects=-rotation*inside/(2j*mu)
        actual=packet["normal_remainder"][:,0]+1j*packet["normal_remainder"][:,1]
        reconstruction=sup(actual-canonical-defects)/norm(amplitude)
        decomposition_error=sup(actual-canonical-defects)/norm(actual)
        primitive_report,primitive_arrays=rapid_integral(efolds,phase,mu,coefficients[1:],norm(amplitude))
        mean_integral=CubicSpline(efolds,coefficients[0]).antiderivative()
        mean_path=mean_integral(efolds)-mean_integral(efolds[0])
        defect_integral=CubicSpline(efolds,defects).antiderivative()
        defect_path=defect_integral(efolds)-defect_integral(efolds[0])
        arrays=dict(efold=efolds,mean=coefficients[0],harmonic1=coefficients[1],harmonic2=coefficients[2],
                    canonical=canonical,represented_defect=defects,actual=actual,mean_integral=mean_path,defect_integral=defect_path,**primitive_arrays)
        output=destination/(stem+".npz")
        np.savez_compressed(output,**arrays)
        report=dict(model=model,label=label,wave=wave,passed=bool(reconstruction<ALGEBRA and decomposition_error<ALGEBRA and primitive_report["passed"]),
                    reconstruction_per_amplitude=reconstruction,reconstruction_per_remainder=decomposition_error,
                    instantaneous_mean_per_amplitude=sup(coefficients[0])/norm(amplitude),
                    instantaneous_rapid_per_amplitude=sup(canonical-coefficients[0])/norm(amplitude),
                    instantaneous_represented_defect_per_amplitude=sup(defects)/norm(amplitude),
                    mean_integral_per_amplitude=sup(mean_path)/norm(amplitude),defect_integral_per_amplitude=sup(defect_path)/norm(amplitude),
                    rapid_integral=primitive_report,input=str(path),input_sha256=case["sha256"],output=output.name,output_sha256=digest(output))
        reports.append(report)
        write(destination/(stem+".json"),report)
        print({key:value for key,value in report.items() if key not in ("rapid_integral","input","output_sha256","input_sha256")},flush=True)
    result=dict(passed=all(row["passed"] for row in reports),reports=reports,source_sha256=digest(__file__),harmonics_sha256=digest(ROOT/"harmonics.py"),
                previous_closeout_sha256=digest(NORMAL/"closeout.json"),protocol_sha256=digest(ROOT/"PROTOCOL.md"),
                no_new_evolution=True,coefficients_not_fitted=True)
    write(ROOT/"decomposition-result.json",result)
    require(result["passed"],"decomposition failed; inspect without automatic evolution")


if __name__=="__main__":
    main()

