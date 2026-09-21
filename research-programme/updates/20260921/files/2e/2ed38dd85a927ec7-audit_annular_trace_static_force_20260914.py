from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from scipy.linalg import cho_factor, cho_solve
import numpy as np
import sympy as sp


def equilibrium(count,gram,phase,cut=False):
    spacing=1/(count-1)
    position=(int(.6/spacing)+phase)*spacing
    cell=int(position/spacing)
    fractions=np.zeros(count)
    fractions[cell]=1-phase
    fractions[cell+1]=phase
    factors,unused=full_spatial_factors(count,gram)
    stiffness=factors.T @ factors/spacing
    factorization=cho_factor(stiffness[1:-1,1:-1])
    free=cho_solve(factorization,-stiffness[1:-1,0])
    response=cho_solve(factorization,fractions[1:-1])
    profile=np.concatenate([[1.],free,[0.]])
    value=fractions @ profile
    compliance=fractions[1:-1] @ response
    if cut:
        penalty=1/(spacing*phase*(1-phase))
        profile[1:-1]-=response*(penalty*value)/(1+penalty*compliance)
        energy=np.sum((factors @ profile)**2)/(2*spacing)+penalty*(fractions @ profile)**2/2
        force=profile[cell]**2/(2*(spacing*phase)**2)-profile[cell+1]**2/(2*(spacing*(1-phase))**2)
        trace=0.
    else:
        multiplier=-value/compliance
        profile[1:-1]+=multiplier*response
        energy=np.sum((factors @ profile)**2)/(2*spacing)
        force=multiplier*(profile[cell+1]-profile[cell])/spacing
        trace=fractions @ profile
    target=1/(2*position**2)
    return dict(count=count,branch='MTS' if gram else 'reference',phase=phase,
                method='cut_cell_reference_correction' if cut else 'interpolated_trace',
                radius=position,energy=float(energy),force=float(force),
                exact_continuum_energy=1/(2*position),exact_continuum_force=target,
                force_ratio=float(force/target),trace_error=float(abs(trace)))


def main():
    evidence=EvidenceRun('annular-trace-static-force-phase-audit-attempt01',__file__)
    try:
        position,spacing,phase=sp.symbols('b h theta',positive=True)
        baseline=1-position
        green=position*(1-position)-spacing*phase*(1-phase)
        energy=sp.Rational(1,2)+baseline**2/(2*green)
        force=-sp.diff(energy,position)-sp.diff(energy,phase)/spacing
        limit=sp.simplify(sp.limit(2*position**2*force,spacing,0))
        evidence.check('interpolated_static_force_limit_is_twice_cell_fraction',sp.simplify(limit-2*phase)==0,str(limit))
        left,right=sp.symbols('q_l q_r',real=True)
        original=(right-left)**2/(2*spacing)
        split=left**2/(2*spacing*phase)+right**2/(2*spacing*(1-phase))
        correction=((1-phase)*left+phase*right)**2/(2*spacing*phase*(1-phase))
        evidence.check('exact_cut_cell_energy_enrichment',sp.simplify(split-original-correction)==0)
        for count in [33,65,129,257]:
            for gram in [False,True]:
                for fraction in [.2,.5,.8]:
                    for cut in [False,True]:
                        row=equilibrium(count,gram,fraction,cut)
                        evidence.report['cases'].append(row)
                        if not gram and cut:
                            evidence.check(str(count)+str(fraction)+'_reference_cut_cell_exact_pressure',
                                           abs(row['force_ratio']-1)<2e-9 and
                                           abs(row['energy']-row['exact_continuum_energy'])<2e-10,row)
                        if not cut:
                            evidence.check(row['branch']+str(count)+str(fraction)+'_constraint_solved',
                                           row['trace_error']<2e-10)
        verdict={}
        for branch in ['reference','MTS']:
            for method in ['interpolated_trace','cut_cell_reference_correction']:
                fine=[row for row in evidence.report['cases'] if row['branch']==branch and row['method']==method and row['count']==257]
                error=max(abs(row['force_ratio']-1) for row in fine)
                verdict[branch+'_'+method]=dict(max_finest_relative_force_error=error,
                                               passes_half_percent_pressure_gate=error<.005,
                                               finest_force_ratios=[row['force_ratio'] for row in fine])
        evidence.report.update(verdict=verdict,
                               phase_test_uses_known_planar_static_continuum_control=True,
                               complete_old_Gram_factors_retained=True,
                               cut_cell_dynamic_mass_action_derived=False,
                               covariant_cut_cell_current_derived=False,
                               exact_full_MTS_boundary_completion_derived=False,
                               coupled_pilot_local_conservation_not_equal_to_force_accuracy=True,
                               full_GR_limit_proven=False,valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

