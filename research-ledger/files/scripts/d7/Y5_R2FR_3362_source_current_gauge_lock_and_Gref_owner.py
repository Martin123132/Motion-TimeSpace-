from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3362-Y5-R2FR-source-current-gauge-lock-and-Gref-owner-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3362_0_3361_doc", ROOT / "3361-Y5-R2FR-odd-residual-parentization-and-physical-lock-under-AX1090.md", "3361 handoff"),
    ("LSRC3362_1_3361_next", OUT / "P8_Y5_R2FR_3361_NEXT_TARGET.csv", "3361 next target"),
    ("LSRC3362_2_3361_y5_obstruction", OUT / "P8_Y5_R2FR_3361_Y5_ZERO_MODE_OBSTRUCTION.csv", "Y5 zero-mode obstruction"),
    ("LSRC3362_3_current_gauge_lock", OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv", "current normalization gauge lock lemma"),
    ("LSRC3362_4_compensator_trichotomy", OUT / "P8_Y5_R2FR_3275_COMPENSATOR_CURRENT_TRICHOTOMY.csv", "compensator current trichotomy"),
    ("LSRC3362_5_rep_current", OUT / "P8_Y5_R2FR_3277_REPRESENTATION_CURRENT_THEOREM.csv", "representation current theorem"),
    ("LSRC3362_6_source_universality", OUT / "P8_Y5_R2FR_3290_SOURCE_CURRENT_UNIVERSALITY_THEOREM.csv", "source-current universality theorem"),
    ("LSRC3362_7_weight_class", OUT / "P8_Y5_R2FR_3291_CURRENT_WEIGHT_CLASSIFICATION.csv", "current weight classification"),
    ("LSRC3362_8_coupling_decomp", OUT / "P8_Y5_R2FR_3339_COUPLING_DECOMPOSITION_THEOREM.csv", "coupling decomposition theorem"),
    ("LSRC3362_9_current_verdict", OUT / "P8_Y5_R2FR_3342_CURRENT_CORPUS_VERDICT.csv", "current corpus verdict"),
    ("LSRC3362_10_source_owner", OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv", "Y5 source normalization owner theorem"),
    ("LSRC3362_11_source_stack", OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "source normalization theorem stack"),
    ("LSRC3362_12_min_source_readout", OUT / "P8_Y5_R2FR_3037_MINIMUM_SOURCE_READOUT_LOCK_PARENT_CLAUSE.csv", "minimum source-readout parent clause"),
    ("LSRC3362_13_gref_lock", OUT / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv", "G_ref lock and A_W normalization audit"),
    ("LSRC3362_14_wphi_lock", OUT / "P8_Y5_R2FR_3052_GREF_WPHI_SOURCE_READOUT_LOCK_CANDIDATE.csv", "G_ref/W/Phi source-readout candidate"),
    ("LSRC3362_15_source_mass", OUT / "P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv", "source mass lock and DeltaGM rows"),
    ("LSRC3362_16_r11_source_norm", OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11 source normalization operator rows"),
    ("LSRC3362_17_ppn_vector", OUT / "P8_Y5_R2FR_3110_LOCAL_PPN_RESIDUAL_VECTOR.csv", "local PPN residual vector"),
    ("LSRC3362_18_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "AX1090 source-side theorem scope"),
    ("LSRC3362_19_3358_surface", OUT / "P8_Y5_R2FR_3358_EPSILON_SURFACE_SOURCE_UPDATE.csv", "surface/source residual update"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3362_LOCAL_SOURCE_REGISTER.csv",
    "theorem_packet": OUT / "P8_Y5_R2FR_3362_CURRENT_GAUGE_THEOREM_PACKET.csv",
    "grav_lock": OUT / "P8_Y5_R2FR_3362_GRAVITATIONAL_SOURCE_COUPLING_LOCK.csv",
    "gref_owner": OUT / "P8_Y5_R2FR_3362_GREF_OWNER_AND_NEWTON_LIMIT.csv",
    "compensator_audit": OUT / "P8_Y5_R2FR_3362_COMPENSATOR_AND_UNIVERSALITY_AUDIT.csv",
    "y5_result": OUT / "P8_Y5_R2FR_3362_Y5_RESULT_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3362_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3362_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3362_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3362_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def current_gauge_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CG3362_0_Maxwell_current_lock",
            "statement": "For an exact gauge current, a spacetime-dependent current normalization is forbidden unless the ordinary current is tangent to its level sets or a compensating current carries the mismatch.",
            "math_form": "nabla_mu(kappa_J J_Q^mu)=0 and nabla_mu J_Q^mu=0 imply J_Q^mu nabla_mu ln(kappa_J)=0",
            "proof_status": "EXACT_CONDITIONAL_CURRENT_LOCK",
            "proof_sketch": "Take the divergence of the Maxwell source equation. Antisymmetry/gauge identity kills the left side. Subtract the Noether conservation law for the parent-owned current.",
            "what_it_derives": "no local time/range/material variation in kappa_J if current richness and no compensator are parent-signed",
            "what_it_does_not_derive": "the absolute numerical value of the coupling constant",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CG3362_1_gravitational_Bianchi_lock",
            "statement": "The same logic applies to the gravitational Hilbert source coupling: Bianchi plus matter Ward conservation kills variable gravitational coupling if no extra source current remains.",
            "math_form": "E^{mu nu}=kappa_g(x) T_H^{mu nu}+Delta J^{mu nu}; nabla_mu E^{mu nu}=0; nabla_mu T_H^{mu nu}=0; Delta J=0 => T_H^{mu nu} nabla_mu kappa_g=0",
            "proof_status": "EXACT_CONDITIONAL_GRAVITATIONAL_LOCK",
            "proof_sketch": "Use diffeomorphism invariance of the left-hand side and the matter Ward identity of the same observed metric/coframe. If allowed local stress tensors are rich enough, the only branch-safe solution is nabla_mu kappa_g=0.",
            "what_it_derives": "constant local G_eff / kappa_g under source-richness, same-frame Hilbert source, and no extra source projection",
            "what_it_does_not_derive": "one universal value across all source classes unless source-only prefactors are grammatically excluded",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CG3362_2_universality_requires_no_prefactor_grammar",
            "statement": "Bianchi/current conservation can force each allowed coupling weight to be constant, but equality of constants requires a separate no-source-prefactor or common-representation theorem.",
            "math_form": "E=sum_A kappa_A T_A; independent Ward identities give T_A^{mu nu} partial_mu kappa_A=0, not automatically kappa_A=kappa_B",
            "proof_status": "EXACT_LIMIT_OF_CURRENT_LOCK",
            "proof_sketch": "A theory with two constant species weights is still conserved and covariant. Therefore universality is not implied by conservation alone; it comes from the parent grammar having only one Hilbert source slot.",
            "what_it_derives": "the precise extra premise needed for WEP/source universality",
            "what_it_does_not_derive": "species-blind source coupling in current MTS without adopting the parent no-prefactor clause",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CG3362_3_Gref_parameter_distinction",
            "statement": "Local GR/Newton needs one universal constant G_ref; deriving the numerical value of G_ref is a stronger parent-theory problem, not something GR itself supplies.",
            "math_form": "G_ref = kappa_g c^4/(8*pi), with partial G_ref=0 and no source/range/frame dependence",
            "proof_status": "EXACT_SCOPE_DISTINCTION",
            "proof_sketch": "Once kappa_g is a universal constant, the weak-field limit gives the Newtonian coefficient. The number can be measured or fixed by a deeper topological/superselection sector; it is not derived by the local Bianchi argument.",
            "what_it_derives": "why a universal constant is acceptable for local-GR reduction while variable/source-dependent coupling is not",
            "what_it_does_not_derive": "the observed SI value of Newton's constant",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "CG3362_4_Y5_closure_condition",
            "statement": "Y5 closes only if current/Bianchi lock, one Hilbert source slot, no compensator/source-shadow, same observed frame, G_ref owner, and no extra mass projection all hold in one branch.",
            "math_form": "epsilon_mu = DeltaG_derivative + DeltaG_species + DeltaG_frame + DeltaM_extra + DeltaG_absolute; all but allowed G_ref constant must vanish or be bounded",
            "proof_status": "CLOSURE_CONTRACT_DERIVED_NOT_SATISFIED",
            "proof_sketch": "Collect the necessary consequences of CG3362_0 through CG3362_3 and the 3361 Gauss-flux obstruction. A single missing clause leaves a source-normalization residual.",
            "what_it_derives": "a non-circular pass/fail contract for calibrated source coupling",
            "what_it_does_not_derive": "current MTS satisfaction of every clause",
            "valid_for_claim": "false",
        },
    ]


def gravitational_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "GLOCK3362_0_same_Hilbert_source",
            "condition": "The source current in the field equation is the Hilbert stress of the same observed matter action.",
            "math_form": "T_H^{mu nu}=2/sqrt(-g_obs) delta S_matter[g_obs,Psi]/delta g_obs_{mu nu}",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_true": "Bianchi can act on the same object measured by clocks/orbits/source readout",
            "if_false": "source-only selectors and non-Hilbert currents survive as Y5 residuals",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "GLOCK3362_1_no_extra_source_projection",
            "condition": "No boundary/domain/non-EH/projector/memory/source-shadow current contributes an independent mass projection.",
            "math_form": "Delta J^{mu nu}=0 or Pi_M Delta J=0/topological/bounded",
            "current_status": "NOT_PROVED",
            "if_true": "Bianchi lock applies to the complete source side",
            "if_false": "a conserved extra source can shift GM without violating Bianchi",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "GLOCK3362_2_stress_richness",
            "condition": "Allowed compact matter configurations span enough local stress/current directions.",
            "math_form": "T_H^{mu nu} partial_mu kappa_g=0 for all allowed T_H => partial_mu kappa_g=0",
            "current_status": "PHYSICAL_PLAUSIBLE_NOT_PARENT_SIGNED",
            "if_true": "local time/radial/frame drift of G_eff is killed",
            "if_false": "coupling gradients can hide in untested current-orthogonal directions",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "GLOCK3362_3_no_source_prefactor_grammar",
            "condition": "The parent action has one ordinary matter source slot, not species/source/readout prefactors.",
            "math_form": "S_ord=sum_A S_A[Psi_A,g_obs,theta_A] and field equation sees T_total, not sum_A w_A T_A",
            "current_status": "CONDITIONAL_CLAUSE_EXISTS_NOT_ADOPTED",
            "if_true": "constant species/source coupling weights are structurally absent",
            "if_false": "WEP/source-composition residual rows remain live",
            "passed": "false",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "GLOCK3362_4_same_branch_readout",
            "condition": "Field equation, source charge, clocks, photons, and orbital readout use the same observed coframe and time.",
            "math_form": "g_field=g_matter=g_source=g_clock=g_orbit and tau_source=tau_clock=tau_orbit",
            "current_status": "NOT_SIGNED",
            "if_true": "G_ref cannot be hidden in a frame/readout conversion",
            "if_false": "DeltaGM can re-enter through source time, clock time, or orbital denominator",
            "passed": "false",
            "valid_for_claim": "false",
        },
    ]


def gref_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "GREF3362_0_universal_constant_allowed",
            "statement": "A single universal constant G_ref is allowed as the local GR/Newton reduction constant.",
            "math_form": "G_ref=kappa_g c^4/(8*pi), partial_t G_ref=partial_r G_ref=partial_A G_ref=0",
            "result": "SCOPE_CLARIFIED",
            "claim_impact": "MTS does not need to derive the numerical value of G to reduce to GR; it must prevent hidden dependence and extra source projection",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "GREF3362_1_Newton_limit_if_same_frame",
            "statement": "With EH left-hand side, same observed frame, and Hilbert source, the weak-field coefficient becomes the Newtonian inverse-square coefficient.",
            "math_form": "G_00^(1)=kappa_g T_00 => nabla^2 Phi=4*pi G_ref rho when W=Phi and T_00=rho c^2",
            "result": "EXACT_CONDITIONAL_NEWTON_COEFFICIENT_MAP",
            "claim_impact": "turns calibrated Newtonian mechanics into a derived limit once G_ref and source mass are owned",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "GREF3362_2_absolute_value_not_derived",
            "statement": "The local current/Bianchi route does not compute the observed numerical value of G_ref.",
            "math_form": "partial_mu G_ref=0 does not imply G_ref=6.674...e-11 SI",
            "result": "ABSOLUTE_G_REMAINS_PARENT_PARAMETER_OR_TOPOLOGICAL_TARGET",
            "claim_impact": "prevents a false demand: GR does not derive G either, but MTS may later try to own it topologically",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "GREF3362_3_extra_mass_projection_survives",
            "statement": "Even with universal G_ref, measured GM can shift if the source mass charge has extra boundary/non-EH/projector pieces.",
            "math_form": "mu_obs=G_ref(M_H+R_nonEH+R_symp+R_extra+R_boundary+R_time_frame)",
            "result": "DELTA_MASS_ROWS_RETAINED",
            "claim_impact": "Y5 is not closed until source mass lock rows zero or bound the extra charge pieces",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "GREF3362_4_topological_superselection_future",
            "statement": "A deeper MTS parent action could in principle derive/fix G_ref as a zero-form/topological/superselection datum.",
            "math_form": "d kappa=0 plus boundary/topological quantization or fixed parent normalization",
            "result": "FUTURE_STRONGER_ROUTE_NOT_CURRENT_PROOF",
            "claim_impact": "separates competitive local-GR reduction from the harder numerical-constant derivation programme",
            "valid_for_claim": "false",
        },
    ]


def compensator_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "COMP3362_0_exact_improvement",
            "survivor": "antisymmetric improvement / magnetization current",
            "can_hide_variable_coupling": "false_if_no_boundary_flux",
            "reason": "its divergence vanishes identically, so it cannot cancel J dot grad(kappa); it can still affect boundary/Poynting bookkeeping",
            "status": "PARTIAL_ZERO_FOR_COUPLING_DRIFT",
            "next_action": "route boundary flux to EM stress/boundary residual rows",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3362_1_separately_conserved_shadow",
            "survivor": "separately conserved shadow/source current",
            "can_hide_variable_coupling": "false_for_gradient_true_for_source_normalization",
            "reason": "it cannot cancel variable kappa divergence but can add an independent source charge block",
            "status": "FINITE_RESIDUAL_RETAINED",
            "next_action": "needs no-shadow theorem or source-backed WEP/R10/PPN bound",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3362_2_nonconserved_compensator",
            "survivor": "nonconserved compensator current",
            "can_hide_variable_coupling": "true",
            "reason": "it can be chosen so nabla J_comp = -J dot grad(kappa)",
            "status": "DANGEROUS_ESCAPE_RETAINED_UNLESS_GAUGE_REJECTED",
            "next_action": "exclude by exact parent gauge representation or keep explicit residual",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "COMP3362_3_constant_species_weight",
            "survivor": "constant source/species prefactor",
            "can_hide_variable_coupling": "not_variable_but_breaks_universality",
            "reason": "Bianchi permits constant w_A unless the parent grammar has only one Hilbert source slot",
            "status": "UNIVERSALITY_GAP_RETAINED",
            "next_action": "prove no-source-prefactor grammar or use WEP/source-composition bounds",
            "valid_for_claim": "false",
        },
    ]


def y5_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_id": "Y5R3362_0_derivative_coupling",
            "quantity": "partial_mu G_eff / G_eff",
            "result": "DERIVED_ZERO_IF_BIANCHI_WARD_RICHNESS_NO_EXTRA_SOURCE",
            "current_value": "CONDITIONAL_NOT_PARENT_SIGNED",
            "remaining_inputs": "same Hilbert source, no DeltaJ, stress richness, same observed branch",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "result_id": "Y5R3362_1_species_source_weight",
            "quantity": "kappa_A/kappa_B - 1",
            "result": "NOT_DERIVED_BY_CURRENT_LOCK_ALONE",
            "current_value": "RETAIN_WEP_SOURCE_COMPOSITION_RESIDUAL",
            "remaining_inputs": "no-source-prefactor parent grammar or source-backed WEP/composition bound",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "result_id": "Y5R3362_2_absolute_Gref",
            "quantity": "G_ref numerical value",
            "result": "NOT_REQUIRED_FOR_LOCAL_GR_REDUCTION_BUT_NOT_NUMERICALLY_DERIVED",
            "current_value": "UNIVERSAL_CONSTANT_OR_TOPOLOGICAL_TARGET",
            "remaining_inputs": "parent superselection/topological normalization if the stronger programme wants to compute G",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "result_id": "Y5R3362_3_DeltaGM_total",
            "quantity": "extra measured-GM/source mass projection",
            "result": "NOT_ZEROED",
            "current_value": "RETAIN_R_NON_EH_R_SYMP_R_EXTRA_R_BOUNDARY_R_TIME_FRAME",
            "remaining_inputs": "source mass lock, boundary/symplectic/reference integrability, no extra mass projection",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "result_id": "Y5R3362_4_Y5_status",
            "quantity": "Y5_source_normalization",
            "result": "PARTIALLY_ADVANCED_NOT_CLOSED",
            "current_value": "variable coupling route is theorem-reduced; absolute/source-mass/universality rows remain",
            "remaining_inputs": "3363 should fill a first quantitative bound row if no parent proof closes the remaining rows",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3362_0_current_lock_theorem",
            "claim": "current/Bianchi lock theorem for variable coupling is mathematically derived conditionally",
            "passed": "true",
            "reason": "divergence identity gives J dot grad(kappa)=0 or T dot grad(kappa)=0 under Noether/Ward conservation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3362_1_parent_assumptions_signed",
            "claim": "same Hilbert source, stress richness, no compensator, and same branch are signed in current MTS",
            "passed": "false",
            "reason": "source owner/readout/gref files remain conditional contracts",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3362_2_universal_species_blind_source",
            "claim": "species/source prefactors are excluded",
            "passed": "false",
            "reason": "current lock alone permits constant source weights unless no-prefactor grammar is adopted",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3362_3_absolute_Gref_derived",
            "claim": "numerical Newton constant is derived",
            "passed": "false",
            "reason": "3362 only separates universal constant ownership from hidden local/source dependence",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3362_4_DeltaGM_extra_mass_zero",
            "claim": "extra source mass projections are zero",
            "passed": "false",
            "reason": "R_nonEH/R_symp/R_extra/R_boundary/R_time_frame rows remain retained",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3362_5_local_GR_Newton_claim",
            "claim": "source-normalized local GR/Newton is claim-ready",
            "passed": "false",
            "reason": "the variable-coupling theorem is useful but the parent assumptions and extra source-mass rows are not closed",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3362_0",
            "question": "Did 3362 close the coupling?",
            "answer": "not fully",
            "reason": "it conditionally derives zero local variation of the coupling, but does not prove parent assumptions, species universality, absolute G_ref, or extra mass projection zero",
            "next_action": "either prove no-prefactor/source-mass lock clauses or move to first quantitative source-normalization bound row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3362_1",
            "question": "What actual progress happened?",
            "answer": "the coupling gap split into derivative drift, species/source weights, absolute G_ref, and extra mass projection",
            "reason": "Bianchi/current locks attack derivative drift; no-prefactor grammar attacks weights; source mass lock attacks DeltaGM; topological/superselection may attack absolute G",
            "next_action": "do not conflate those rows again",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3362_2",
            "question": "Is deriving the numerical value of G mandatory for local GR recovery?",
            "answer": "no",
            "reason": "GR itself uses a universal constant; local recovery needs one source-blind constant and no hidden residuals, while numerical derivation of G is a stronger later theory target",
            "next_action": "treat G_ref as allowed parent constant unless the stronger topological route is explicitly pursued",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3363-Y5-R2FR-first-source-normalization-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3363_first_source_normalization_bound_row.py",
            "objective": "turn the remaining Y5 source-normalization pieces into the first quantitative nonclaim bound row: species/source weight, DeltaGM extra mass projection, or Gdot/range coupling, with units, weak-field map, and arena source path",
            "why_next": "3362 gives a theorem route for derivative coupling but leaves unproved parent assumptions; the fallback must become numeric/source-backed rather than another qualitative ledger",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3364-Y5-R2FR-no-source-prefactor-grammar-or-WEP-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3364_no_source_prefactor_grammar_or_WEP_bound.py",
            "objective": "prove the parent action has no species/source prefactor grammar; if not, bind the constant source-weight residual to WEP/source-composition data",
            "why_next": "current/Bianchi lock cannot force kappa_A=kappa_B; this row is the universality gap",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = local_source_rows()
    theorem_rows = current_gauge_theorem_rows()
    grav_rows = gravitational_lock_rows()
    gref_rows = gref_owner_rows()
    comp_rows = compensator_audit_rows()
    y5_rows = y5_result_rows()
    gate_rows = promotion_gate_rows()
    next_rows = next_target_rows()
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": detail,
            }
        )

    add("VAL3362_0_local_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3362_1_local_sources_parse", "all cited local source paths parse", all(row["parseable"] == "true" for row in sources))
    add("VAL3362_2_outputs_parse", "all 3362 non-validation outputs parse", all(path.exists() and parseable(path) for path in output_paths))
    add(
        "VAL3362_3_theorem_packet_contains_locks",
        "the theorem packet contains Maxwell lock, gravitational Bianchi lock, universality limit, and Gref distinction",
        all(
            required in {row["proof_status"] for row in theorem_rows}
            for required in [
                "EXACT_CONDITIONAL_CURRENT_LOCK",
                "EXACT_CONDITIONAL_GRAVITATIONAL_LOCK",
                "EXACT_LIMIT_OF_CURRENT_LOCK",
                "EXACT_SCOPE_DISTINCTION",
            ]
        ),
    )
    add(
        "VAL3362_4_grav_lock_not_overpromoted",
        "gravitational lock rows keep parent assumptions unsigned",
        all(row["passed"] == "false" for row in grav_rows),
    )
    add(
        "VAL3362_5_Gref_scope_separated",
        "Gref rows distinguish universal constant from numerical derivation and extra mass projection",
        any(row["result"] == "ABSOLUTE_G_REMAINS_PARENT_PARAMETER_OR_TOPOLOGICAL_TARGET" for row in gref_rows)
        and any(row["result"] == "DELTA_MASS_ROWS_RETAINED" for row in gref_rows),
    )
    add(
        "VAL3362_6_compensators_classified",
        "compensator audit classifies exact improvements, shadows, nonconserved compensators, and constant species weights",
        {row["audit_id"] for row in comp_rows}
        == {"COMP3362_0_exact_improvement", "COMP3362_1_separately_conserved_shadow", "COMP3362_2_nonconserved_compensator", "COMP3362_3_constant_species_weight"},
    )
    add(
        "VAL3362_7_Y5_split",
        "Y5 result splits derivative coupling, species weight, absolute Gref, and extra mass projection",
        {row["quantity"] for row in y5_rows}
        >= {"partial_mu G_eff / G_eff", "kappa_A/kappa_B - 1", "G_ref numerical value", "extra measured-GM/source mass projection"},
    )
    add(
        "VAL3362_8_no_overclaim",
        "local GR/Newton, parent assumptions, universality, absolute G, and DeltaGM zero remain unpromoted",
        all(
            row["passed"] == "false"
            for row in gate_rows
            if row["gate_id"]
            in {
                "GATE3362_1_parent_assumptions_signed",
                "GATE3362_2_universal_species_blind_source",
                "GATE3362_3_absolute_Gref_derived",
                "GATE3362_4_DeltaGM_extra_mass_zero",
                "GATE3362_5_local_GR_Newton_claim",
            }
        ),
    )
    add(
        "VAL3362_9_next_target_quantitative",
        "next target moves to first quantitative source-normalization bound row",
        any("first-source-normalization-bound-row" in row["target_id"] for row in next_rows),
    )
    add(
        "VAL3362_10_write_scope_outside_formalization",
        "all 3362 write targets are outside formalization-workbench",
        all(FW not in path.parents and path != FW for path in [DOC, *output_paths, OUTPUTS["validation"]]),
        "write_targets=" + str(len([DOC, *output_paths, OUTPUTS["validation"]])),
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3362_11_overall",
        "3362 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    grav_rows: list[dict[str, Any]],
    gref_rows: list[dict[str, Any]],
    comp_rows: list[dict[str, Any]],
    y5_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 3362 - Source-Current Gauge Lock And Gref Owner Under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "## Summary",
        "- This checkpoint takes the coupling seriously instead of circling the old Yloc parity route.",
        "- Real derivation: Bianchi/Noether identities conditionally force variable source coupling to be constant: `T_H^{mu nu} partial_mu kappa_g=0` or `J^mu partial_mu kappa_J=0`, and current/stress richness then gives `partial kappa=0`.",
        "- Important correction: that does not derive the numerical value of Newton's constant. GR does not derive that either. Local GR recovery needs one universal source-blind `G_ref`, not a computed SI number.",
        "- Remaining live pieces are now split cleanly: species/source prefactors, extra mass projection, compensator/source-shadow currents, same-frame readout, and optional topological `G_ref` ownership.",
        "- No local GR/Newton claim is promoted; the next step should be quantitative if the no-prefactor/source-mass theorem does not close.",
        "",
        "## Local Source Register",
        table(sources),
        "## Current Gauge Theorem Packet",
        table(theorem_rows),
        "## Gravitational Source Coupling Lock",
        table(grav_rows),
        "## Gref Owner And Newton Limit",
        table(gref_rows),
        "## Compensator And Universality Audit",
        table(comp_rows),
        "## Y5 Result Rows",
        table(y5_rows),
        "## Promotion Gates",
        table(gate_rows),
        "## Decision Ledger",
        table(decisions),
        "## Next Target",
        table(next_rows),
        "## Validation",
        table(validations),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "local_sources": local_source_rows(),
        "theorem_packet": current_gauge_theorem_rows(),
        "grav_lock": gravitational_lock_rows(),
        "gref_owner": gref_owner_rows(),
        "compensator_audit": compensator_audit_rows(),
        "y5_result": y5_result_rows(),
        "gates": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    validations = validation_rows()
    write_csv(OUTPUTS["validation"], validations)
    write_doc(
        rows_by_output["local_sources"],
        rows_by_output["theorem_packet"],
        rows_by_output["grav_lock"],
        rows_by_output["gref_owner"],
        rows_by_output["compensator_audit"],
        rows_by_output["y5_result"],
        rows_by_output["gates"],
        rows_by_output["decision"],
        rows_by_output["next"],
        validations,
    )
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
