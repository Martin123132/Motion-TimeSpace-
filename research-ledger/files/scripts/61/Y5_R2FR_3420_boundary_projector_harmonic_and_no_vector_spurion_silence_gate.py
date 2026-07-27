from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3420-Y5-R2FR-boundary-projector-harmonic-and-no-vector-spurion-silence-gate-under-AX1090.md"

ALPHA3_PRODUCT_LIMIT = 5.381673706808059e-15

SOURCES = {
    "doc_3419": ROOT / "3419-Y5-R2FR-Khat-Gamma-eff-metric-response-lock-and-Helmholtz-audit-under-AX1090.md",
    "next_3419": OUT / "P8_Y5_R2FR_3419_NEXT_TARGET.csv",
    "helmholtz_3419": OUT / "P8_Y5_R2FR_3419_HELMHOLTZ_AUDIT.csv",
    "qloc_consequence_3419": OUT / "P8_Y5_R2FR_3419_QLOC_CONSEQUENCE.csv",
    "branch_split_3419": OUT / "P8_Y5_R2FR_3419_METRIC_RESPONSE_BRANCH_SPLIT.csv",
    "boundary_audit_3418": OUT / "P8_Y5_R2FR_3418_BOUNDARY_PROJECTOR_AUDIT.csv",
    "vector_zero_3418": OUT / "P8_Y5_R2FR_3418_VECTOR_ZERO_DERIVATION.csv",
    "alpha_rows_3418": OUT / "P8_Y5_R2FR_3418_ALPHA_VECTOR_BOUND_ROWS.csv",
    "ward_gates_3417": OUT / "P8_Y5_R2FR_3417_WARD_ZERO_RESCUE_GATES.csv",
    "hidden_stress_3416": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
    "em_poynting_3382": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "maxwell_route_3339": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
    "pim_projector_stress": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "pim_projector_algebra": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "frame_doc_1003": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
    "projector_doc_1014": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "hilbert_boundary_doc_1015": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3420_SOURCE_REGISTER.csv",
    "local_domain_rule": OUT / "P8_Y5_R2FR_3420_LOCAL_DOMAIN_RULE.csv",
    "hodge_silence_theorem": OUT / "P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv",
    "projector_owner_gate": OUT / "P8_Y5_R2FR_3420_PROJECTOR_OWNER_GATE.csv",
    "no_vector_spurion_audit": OUT / "P8_Y5_R2FR_3420_NO_VECTOR_SPURION_AUDIT.csv",
    "em_poynting_flux_gate": OUT / "P8_Y5_R2FR_3420_EM_POYNTING_VECTOR_FLUX_GATE.csv",
    "alpha_vector_residual_rows": OUT / "P8_Y5_R2FR_3420_ALPHA_VECTOR_RESIDUAL_ROWS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3420_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3420_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3420_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3420_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3420_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def cell(value: Any) -> str:
        return str(value).replace("|", "/").replace("\n", " ")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3419": "declares boundary/projector/spurion leakage as next alpha3 danger",
        "next_3419": "selects 3420 target",
        "helmholtz_3419": "bulk Helmholtz closed only in adopted parent-response branch; boundary/projector remains open",
        "qloc_consequence_3419": "q_loc consequence of Khat response branch and remaining boundary/projector dependencies",
        "branch_split_3419": "old Khat failure vs explicit parent-response branch",
        "boundary_audit_3418": "boundary, harmonic, projector and hidden-vector leak taxonomy",
        "vector_zero_3418": "conditional q_loc vector-zero theorem clauses",
        "alpha_rows_3418": "alpha-vector product bound fallback, including alpha3 limit",
        "ward_gates_3417": "Ward-zero rescue gate naming Euler/boundary/projector vector zero",
        "hidden_stress_3416": "safe-class gate for public Hilbert stress and q_loc T_GK",
        "em_poynting_3382": "public Maxwell/Poynting Hilbert stress chain",
        "maxwell_route_3339": "Maxwell/current/Hodge coupling route and hidden-current guard",
        "pim_projector_stress": "projector variation stress contract",
        "pim_projector_algebra": "projector algebra contract",
        "frame_doc_1003": "preferred-frame leakage and covariant-frame guard",
        "projector_doc_1014": "Pi_M/projector commutator and stress guard",
        "hilbert_boundary_doc_1015": "topological-Hilbert equality and boundary-zero flux guard",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def local_domain_rule() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "LDR3420_0_domain",
            "domain_clause": "Use a local vacuum test domain Omega that is a compact ball/collar fixed before readout.",
            "mathematical_content": "Omega subset Sigma_t, boundary dOmega smooth, closure(Omega) excludes matter support and external apparatus currents.",
            "why_needed": "prevents moving-domain or fitted-boundary choices from hiding alpha-vector charge",
            "current_status": "CONDITIONAL_LOCAL_TEST_RULE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "rule_id": "LDR3420_1_cohomology",
            "domain_clause": "H^1(Omega)=0 or all harmonic one-forms have zero physical flux/charge.",
            "mathematical_content": "ker Delta_Hodge on one-forms is trivial, so q_harmonic=0 after boundary conditions.",
            "why_needed": "kills harmonic q_loc vector residue instead of assuming it away",
            "current_status": "PASS_FOR_CONTRACTIBLE_LOCAL_BALL_ONLY",
            "valid_for_claim": False,
        },
        {
            "rule_id": "LDR3420_2_no_flux",
            "domain_clause": "The parent boundary term carries no transverse flux: P_V n_mu B_GK^{mu nu}=0.",
            "mathematical_content": "surface integral of vector boundary current through dOmega vanishes in the local rest frame",
            "why_needed": "kills q_T boundary source and alpha3 boundary charge",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "rule_id": "LDR3420_3_fixed_reference",
            "domain_clause": "Boundary reference/corner data are fixed once, source-blind and not varied after observing residuals.",
            "mathematical_content": "delta_g B_ref and corner shifts are exact or zero on dOmega",
            "why_needed": "prevents reference terms from acting as hidden preferred-frame knobs",
            "current_status": "OPEN_BOUNDARY_REFERENCE",
            "valid_for_claim": False,
        },
        {
            "rule_id": "LDR3420_4_stationary_rest_frame",
            "domain_clause": "Local rest frame has no net exchange-odd momentum flux through dOmega.",
            "mathematical_content": "P_V int_dOmega T^{i0} n_i dS = 0 for public matter/EM plus hidden safe classes",
            "why_needed": "prevents Poynting/matter/radiation flow from becoming f_qV",
            "current_status": "OPEN_FLUX_CONDITION",
            "valid_for_claim": False,
        },
        {
            "rule_id": "LDR3420_5_verdict",
            "domain_clause": "Boundary/harmonic silence is theorem-grade only on fixed, contractible, no-flux, source-blind local domains.",
            "mathematical_content": "LDR3420_0 through LDR3420_4 imply no boundary/harmonic q_loc vector charge",
            "why_needed": "makes the local vacuum plateau a domain theorem rather than an axiom",
            "current_status": "THEOREM_CONTRACT_BUILT_NOT_PROMOTED",
            "valid_for_claim": False,
        },
    ]


def hodge_silence_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "HST3420_0_decomposition",
            "claim": "The spatial q_loc vector splits as D chi_q + q_T + q_harmonic.",
            "derivation": "Hodge decomposition on Omega with boundary conditions fixed before readout.",
            "requires": "Omega, h_ij, boundary condition class and P_V stated",
            "current_status": "PASS_KINEMATIC",
            "valid_for_claim": False,
        },
        {
            "step_id": "HST3420_1_bulk_removed",
            "claim": "After 3419 parent-response adoption and future Euler closure, no bulk vector source remains.",
            "derivation": "bulk q_loc is a Ward/Euler residual; adopted Khat=Kmetric removes independent bulk Khat obstruction.",
            "requires": "3421 E_A=0/source-free local branch",
            "current_status": "CONDITIONAL_ON_3421",
            "valid_for_claim": False,
        },
        {
            "step_id": "HST3420_2_transverse_boundary_zero",
            "claim": "If P_V n_mu B_GK^{mu nu}=0, q_T has no boundary source.",
            "derivation": "transverse Hodge source is the solenoidal part of the boundary/flux current; zero flux kills it.",
            "requires": "no-flux boundary primitive and fixed reference/corner data",
            "current_status": "CONDITIONAL_BOUNDARY_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "HST3420_3_harmonic_zero",
            "claim": "If H^1(Omega)=0, q_harmonic=0.",
            "derivation": "contractible local ball admits no nonzero harmonic one-form with the imposed boundary silence.",
            "requires": "local ball or explicit zero charge for any topology",
            "current_status": "PASS_FOR_LOCAL_BALL_RULE",
            "valid_for_claim": False,
        },
        {
            "step_id": "HST3420_4_vector_spurion_zero",
            "claim": "If no exchange-odd vector spurion survives, f_qV=0.",
            "derivation": "scalar U^2/local isotropic data cannot generate alpha1/alpha2/alpha3 without a vector, axial vector, boundary normal, momentum, Poynting flux or hidden constitutive vector.",
            "requires": "no-vector-spurion audit rows NVS3420_0 through NVS3420_7 pass",
            "current_status": "CONDITIONAL_SPURION_AUDIT_OPEN",
            "valid_for_claim": False,
        },
        {
            "step_id": "HST3420_5_silence_theorem",
            "claim": "Under HST3420_1 through HST3420_4, P_V q_loc=0 and alpha3_q is theorem-zero in the adopted parent branch.",
            "derivation": "bulk Ward residual removed, transverse boundary source zero, harmonic sector trivial, and no vector spurion remains to couple scalar q_proxy into alpha-vector lanes.",
            "requires": "3421 Euler/Z-basis plus no-flux/projector/no-spurion parent signatures",
            "current_status": "THEOREM_CONTRACT_BUILT_NOT_CLOSED",
            "valid_for_claim": False,
        },
    ]


def projector_owner_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "POG3420_0_qbasic_projection",
            "projector_risk": "P_loc/P_V depends on representative metric, domain normal or readout choice",
            "zero_route": "projectors are q-basic functionals fixed by the parent branch before readout",
            "bound_route": "retain Delta_P_projector_alpha_vector",
            "current_status": "OPEN_PROJECTOR_OWNER",
            "valid_for_claim": False,
        },
        {
            "gate_id": "POG3420_1_metric_variation",
            "projector_risk": "delta_g P_loc produces extra Hilbert/projector stress",
            "zero_route": "delta_g P_loc=0 on the adopted local branch or variation is exact/constraint",
            "bound_route": "projector_stress_beta_alpha_equiv",
            "current_status": "OPEN_PROJECTOR_STRESS",
            "valid_for_claim": False,
        },
        {
            "gate_id": "POG3420_2_hodge_operator",
            "projector_risk": "Hodge/Green operator variation produces transverse response",
            "zero_route": "fixed local ball with self-adjoint Green operator and no kernel",
            "bound_route": "Delta_Hodge_Green_commutator",
            "current_status": "OPEN_HODGE_VARIATION",
            "valid_for_claim": False,
        },
        {
            "gate_id": "POG3420_3_domain_normal",
            "projector_risk": "moving boundary normal n_i acts as preferred direction",
            "zero_route": "domain selected covariantly before readout; no moving normal response",
            "bound_route": "Delta_domain_normal_alpha",
            "current_status": "OPEN_DOMAIN_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "POG3420_4_verdict",
            "projector_risk": "projector words are not enough to claim vector silence",
            "zero_route": "POG3420_0 through POG3420_3 theorem-zero",
            "bound_route": "absolute projector residual envelope",
            "current_status": "PROJECTOR_SILENCE_NOT_CLOSED",
            "valid_for_claim": False,
        },
    ]


def no_vector_spurion_audit() -> list[dict[str, Any]]:
    return [
        {
            "spurion_id": "NVS3420_0_matter_momentum",
            "possible_vector": "ordinary matter momentum density T^{0i}",
            "safe_if": "local vacuum/rest frame has no net matter momentum through dOmega",
            "residual_if_not": "epsilon_matter_momentum_alpha",
            "current_status": "CONDITIONAL_LOCAL_REST_FRAME",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_1_EM_Poynting",
            "possible_vector": "public EM Poynting vector S_EM^i=(E x B)^i/mu0",
            "safe_if": "Maxwell/EM is included as public Hilbert stress and net transverse Poynting flux through dOmega is zero",
            "residual_if_not": "epsilon_EM_Poynting_alpha",
            "current_status": "IMPORTANT_OPEN_FLUX_CHECK",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_2_radiation_wave_flux",
            "possible_vector": "gravitational/EM/radiative wave momentum flux",
            "safe_if": "stationary local branch or time-averaged flux has no preferred-frame projection",
            "residual_if_not": "epsilon_wave_flux_alpha",
            "current_status": "OPEN_IF_WAVES_PRESENT",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_3_boundary_normal",
            "possible_vector": "domain normal/corner orientation",
            "safe_if": "fixed spherical/local geodesic ball or covariant domain with no anisotropic normal response",
            "residual_if_not": "epsilon_domain_normal_alpha",
            "current_status": "OPEN_DOMAIN_RULE",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_4_hidden_constitutive_vector",
            "possible_vector": "hidden/projector/constitutive stress vector",
            "safe_if": "hidden sector is pure gauge, topological exact, gapped no-hair, or explicitly bounded",
            "residual_if_not": "epsilon_hidden_vector_alpha",
            "current_status": "RETAINED_FROM_3416",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_5_frame_shadow",
            "possible_vector": "Weyl/disformal/frame shadow direction",
            "safe_if": "one public metric/coframe with quotient-invariant matter readout",
            "residual_if_not": "epsilon_frame_shadow_alpha",
            "current_status": "OPEN_FRAME_DESCENT",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_6_rotation_axial",
            "possible_vector": "spin/rotation/axial vector",
            "safe_if": "local non-rotating Fermi frame or axial coupling coefficient zero/bounded",
            "residual_if_not": "epsilon_rotation_alpha",
            "current_status": "OPEN_IF_ROTATING_SOURCE",
            "valid_for_claim": False,
        },
        {
            "spurion_id": "NVS3420_7_verdict",
            "possible_vector": "all exchange-odd vector spurions",
            "safe_if": "NVS3420_0 through NVS3420_6 theorem-zero or bounded",
            "residual_if_not": "epsilon_V_total",
            "current_status": "NO_VECTOR_SPURION_THEOREM_NOT_CLOSED",
            "valid_for_claim": False,
        },
    ]


def em_poynting_flux_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "EPF3420_0_public_Hilbert",
            "statement": "Public Maxwell/EM/Poynting stress is allowed on the ordinary Hilbert source side.",
            "condition": "same g_obs/coframe action and same kappa_MTS; no hidden current/source weighting",
            "effect_on_q_loc": "not hidden stress by itself",
            "current_status": "SAFE_CLASS_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "gate_id": "EPF3420_1_vector_flux",
            "statement": "A nonzero net Poynting vector is still a vector spurion for alpha_i/alpha3.",
            "condition": "int_dOmega P_V S_EM^i n_i dS = 0 or source-backed bound",
            "effect_on_q_loc": "otherwise contributes epsilon_EM_Poynting_alpha",
            "current_status": "FLUX_ZERO_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "EPF3420_2_wave_average",
            "statement": "High-frequency or wave EM/gravitational flux must be averaged or bounded, not ignored.",
            "condition": "time average has zero preferred-frame projection or residual bound enters alpha-vector envelope",
            "effect_on_q_loc": "prevents waves/Poynting from being silently dropped",
            "current_status": "BOUND_IF_WAVE_BRANCH_USED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "EPF3420_3_verdict",
            "statement": "Poynting vector is a useful place to look, but it is a gate not a free rescue.",
            "condition": "public Hilbert ownership plus zero net transverse flux",
            "effect_on_q_loc": "if passed, EM does not spoil q_loc vector silence",
            "current_status": "NONCLAIM_GATE_WRITTEN",
            "valid_for_claim": False,
        },
    ]


def alpha_vector_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "AVR3420_0_total_vector_envelope",
            "quantity": "epsilon_V_total",
            "formula": "|epsilon_boundary|+|epsilon_projector|+|epsilon_harmonic|+|epsilon_momentum|+|epsilon_EM_Poynting|+|epsilon_hidden|+|epsilon_frame|+|epsilon_rotation|",
            "required_for_alpha3": f"epsilon_V_total <= {ALPHA3_PRODUCT_LIMIT}",
            "source_path": str(DOC),
            "status": "ENVELOPE_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "AVR3420_1_boundary_flux",
            "quantity": "epsilon_boundary",
            "formula": "norm(P_V n_mu B_GK^{mu nu}) / q_proxy_normalization",
            "required_for_alpha3": "zero by no-flux theorem or included in epsilon_V_total",
            "source_path": str(SOURCES["boundary_audit_3418"]),
            "status": "MISSING_BOUNDARY_FLUX_VALUE_OR_THEOREM",
            "valid_for_claim": False,
        },
        {
            "row_id": "AVR3420_2_projector_commutator",
            "quantity": "epsilon_projector",
            "formula": "norm([delta_g,P_loc/P_V] T_GK) / q_proxy_normalization",
            "required_for_alpha3": "zero by q-basic projector theorem or included in epsilon_V_total",
            "source_path": str(SOURCES["pim_projector_stress"]),
            "status": "MISSING_PROJECTOR_STRESS_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "AVR3420_3_harmonic_charge",
            "quantity": "epsilon_harmonic",
            "formula": "norm(q_harmonic)/q_proxy_normalization",
            "required_for_alpha3": "zero if H^1(Omega)=0 or harmonic physical charge vanishes",
            "source_path": str(SOURCES["vector_zero_3418"]),
            "status": "ZERO_FOR_LOCAL_BALL_ONLY",
            "valid_for_claim": False,
        },
        {
            "row_id": "AVR3420_4_EM_Poynting",
            "quantity": "epsilon_EM_Poynting",
            "formula": "norm(P_V int_dOmega S_EM^i n_i dS)/q_proxy_normalization",
            "required_for_alpha3": "zero net flux or explicit source-backed bound",
            "source_path": str(SOURCES["em_poynting_3382"]),
            "status": "MISSING_POYNTING_FLUX_BOUND_OR_ZERO",
            "valid_for_claim": False,
        },
        {
            "row_id": "AVR3420_5_hidden_frame_rotation",
            "quantity": "epsilon_hidden+epsilon_frame+epsilon_rotation",
            "formula": "absolute vector-spurion sum from hidden stress, frame shadow, and spin/rotation",
            "required_for_alpha3": "all zero or included in epsilon_V_total",
            "source_path": str(SOURCES["hidden_stress_3416"]),
            "status": "MISSING_SAFE_CLASS_OR_BOUND_ROWS",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3420_0_local_domain",
            "gate": "fixed contractible local vacuum domain exists",
            "current_result": "PASS_FOR_LOCAL_BALL_CONDITIONAL",
            "promotes_if": "domain fixed before readout and source support excluded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_1_boundary_no_flux",
            "gate": "P_V boundary/improvement flux vanishes",
            "current_result": "BLOCKED_NOT_PARENT_SIGNED",
            "promotes_if": "no-flux/Stokes/corner certificate or bound rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_2_projector_owner",
            "gate": "P_loc/P_V projector variation produces no vector stress",
            "current_result": "BLOCKED_PROJECTOR_OWNER",
            "promotes_if": "q-basic projector theorem or finite commutator bound",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_3_no_vector_spurion",
            "gate": "matter/EM/Poynting/wave/hidden/frame/rotation vectors are zero or bounded",
            "current_result": "BLOCKED_SPURION_AUDIT_OPEN",
            "promotes_if": "NVS3420_0 through NVS3420_6 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_4_alpha3",
            "gate": "alpha3 q_loc lane is safe",
            "current_result": "NOT_PROMOTED",
            "promotes_if": "f_qV=0 by full silence theorem or epsilon_V_total <= 5.381673706808059e-15",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_5_q_loc_vector_zero",
            "gate": "P_V q_loc=0 in adopted parent-response branch",
            "current_result": "BLOCKED_PENDING_3421_AND_FLUX_PROJECTOR_GATES",
            "promotes_if": "bulk Euler/Z-basis plus 3420 boundary/projector/spurion gates pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3420_6_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "q_loc vector-zero plus retained beta/source/stress/nonEH envelopes close",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3420_0_theorem_shape",
            "finding": "Boundary/harmonic silence has a real theorem shape: fixed local ball, H^1=0, no transverse flux.",
            "evidence": "Hodge decomposition plus no-flux boundary condition kills q_T and q_harmonic.",
            "action": "Keep the silence route alive, but only as a conditional theorem contract.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3420_1_projector_not_free",
            "finding": "Projectors are not harmless notation.",
            "evidence": "metric/domain/readout variation can create projector stress or a preferred direction.",
            "action": "Require q-basic projector owner or finite commutator residual rows.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3420_2_poynting_gate",
            "finding": "The Poynting vector is exactly the sort of thing that could re-open the alpha-vector lane.",
            "evidence": "public EM/Poynting Hilbert stress is safe as a source class, but net flux is still a vector spurion.",
            "action": "Track EM/Poynting flux as zero-by-domain or residual-bound; do not ignore waves.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3420_3_next",
            "finding": "After 3420, the next load-bearing gap is Z-basis physical lock plus Euler source-free branch.",
            "evidence": "boundary silence cannot finish q_loc if bulk E_A source terms remain.",
            "action": "Build 3421 Z-basis/Euler local branch proof or residual rows.",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3421_Z_basis_physical_lock_and_Euler_source_free_local_branch.py",
            "objective": "prove Z=0 is the physical local branch covering q_loc/source/stress residuals and that all Gamma_eff fields obey E_A=0 through O(U^2); otherwise emit source-current residual rows",
            "why_next": "3420 handles boundary/projector/vector-spurion silence conditionally, but q_loc vector-zero still needs bulk Euler/source-free closure",
            "valid_for_claim": False,
        },
        {
            "target_id": "3422-Y5-R2FR-EM-Poynting-flux-zero-or-alpha-vector-bound-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3422_EM_Poynting_flux_zero_or_alpha_vector_bound_row.py",
            "objective": "if the EM/wave branch is retained, prove zero net transverse Poynting flux in local vacuum tests or stage epsilon_EM_Poynting_alpha rows",
            "why_next": "Poynting is now identified as a specific vector-spurion gate rather than an ignored background detail",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3420_0",
            "script": str(Path(__file__).resolve()),
            "mode": "BOUNDARY_PROJECTOR_HARMONIC_NO_VECTOR_SPURION_SILENCE_GATE",
            "result": "local-ball/Hodge/no-flux theorem contract built; projector and Poynting/vector-spurion residual rows staged; local GR remains blocked pending 3421 Euler/Z-basis closure",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    all_sources_exist = all(row["exists"] for row in source_rows)
    scope_ok = all(str(path).startswith(str(ROOT)) and "formalization-workbench" not in str(path) for path in OUTPUTS.values())
    nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for key, rows in generated.items()
        if key != "validation"
        for row in rows
    )
    hodge_theorem = any(row["step_id"] == "HST3420_5_silence_theorem" for row in generated["hodge_silence_theorem"])
    poynting_gate = any(row["spurion_id"] == "NVS3420_1_EM_Poynting" for row in generated["no_vector_spurion_audit"])
    alpha_envelope = any(row["row_id"] == "AVR3420_0_total_vector_envelope" and str(ALPHA3_PRODUCT_LIMIT) in row["required_for_alpha3"] for row in generated["alpha_vector_residual_rows"])
    projector_block = any(row["gate_id"] == "PG3420_2_projector_owner" and row["current_result"].startswith("BLOCKED") for row in generated["promotion_gates"])
    local_gr_blocked = any(row["gate_id"] == "PG3420_6_local_GR" and row["current_result"] == "BLOCKED" for row in generated["promotion_gates"])
    next_3421 = generated["next_target"][0]["target_id"].startswith("3421-Y5-R2FR-Z-basis")

    rows = [
        {
            "check_id": "VAL3420_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all_sources_exist,
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3420_1_scope",
            "check": "all outputs stay under post-checkpoint-work",
            "passed": scope_ok,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3420_2_all_nonclaim",
            "check": "3420 does not claim local GR or alpha3 pass",
            "passed": nonclaim,
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3420_3_hodge_theorem",
            "check": "Hodge/boundary silence theorem contract exists",
            "passed": hodge_theorem,
            "detail": "HST3420_5 present",
        },
        {
            "check_id": "VAL3420_4_poynting_included",
            "check": "Poynting vector is explicitly audited",
            "passed": poynting_gate,
            "detail": "NVS3420_1_EM_Poynting present",
        },
        {
            "check_id": "VAL3420_5_alpha_envelope",
            "check": "alpha-vector fallback envelope keeps alpha3 product limit",
            "passed": alpha_envelope,
            "detail": f"epsilon_V_total limit {ALPHA3_PRODUCT_LIMIT}",
        },
        {
            "check_id": "VAL3420_6_projector_block",
            "check": "projector owner remains a blocker",
            "passed": projector_block,
            "detail": "projector variation stress not silently dropped",
        },
        {
            "check_id": "VAL3420_7_local_GR_blocked",
            "check": "local GR remains blocked",
            "passed": local_gr_blocked,
            "detail": "Euler/Z-basis and flux/projector gates remain open",
        },
        {
            "check_id": "VAL3420_8_next_target",
            "check": "next target attacks bulk Euler/Z-basis closure",
            "passed": next_3421,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3420_9_overall",
            "check": "3420 boundary/projector/spurion silence gate is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3420 - Boundary/Projector/Harmonic and No-Vector-Spurion Silence Gate",
            "## Summary\n"
            "- This checkpoint builds the local boundary theorem route instead of assuming a vacuum plateau.\n"
            "- On a fixed contractible local vacuum ball, `H^1(Omega)=0` kills harmonic one-form charge, and `P_V n_mu B_GK^{mu nu}=0` kills transverse boundary flux.\n"
            "- Projectors are treated as live physics: if `P_loc/P_V` varies with the metric, domain, frame or readout, it creates a retained projector-stress/vector residual.\n"
            "- The Poynting vector is now explicitly included. Public Maxwell/Poynting Hilbert stress is a safe class only if it is varied from the same public action, but net transverse Poynting flux is still a vector spurion unless zero or bounded.\n"
            "- The alpha3 fallback is now an absolute vector-spurion envelope: `epsilon_V_total <= 5.381673706808059e-15` or theorem-zero.\n"
            "- Local GR is still not claimed: 3421 must prove the bulk `Z=0`/Euler source-free local branch.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Local Domain Rule\n" + md_table(generated["local_domain_rule"]),
            "## Hodge Boundary Silence Theorem\n" + md_table(generated["hodge_silence_theorem"]),
            "## Projector Owner Gate\n" + md_table(generated["projector_owner_gate"]),
            "## No-Vector-Spurion Audit\n" + md_table(generated["no_vector_spurion_audit"]),
            "## EM/Poynting Flux Gate\n" + md_table(generated["em_poynting_flux_gate"]),
            "## Alpha-Vector Residual Rows\n" + md_table(generated["alpha_vector_residual_rows"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "The boundary/projector side is now a theorem-shaped gate, not a handwave. "
            "The best path remains theorem-zero, but the fallback is concrete: every surviving vector spurion, including EM/Poynting flux, must fit inside an alpha3 product budget of about 5.38e-15.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "local_domain_rule": local_domain_rule(),
        "hodge_silence_theorem": hodge_silence_theorem(),
        "projector_owner_gate": projector_owner_gate(),
        "no_vector_spurion_audit": no_vector_spurion_audit(),
        "em_poynting_flux_gate": em_poynting_flux_gate(),
        "alpha_vector_residual_rows": alpha_vector_residual_rows(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3420 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
