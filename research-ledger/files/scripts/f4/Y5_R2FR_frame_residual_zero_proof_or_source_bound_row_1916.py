from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1916"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1916-Y5-R2FR-frame-residual-zero-proof-or-source-bound-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1915_doc": ROOT / "1915-Y5-R2FR-finite-residual-priority-and-first-fill-row.md",
    "1915_validation": OUT / "P8_Y5_BRR545_1915_VALIDATION.csv",
    "1915_first_fill": OUT / "P8_Y5_PARENT_QLOC_1915_FIRST_FILL_FRAME_RESIDUAL_ATTEMPT.csv",
    "1915_blockers": OUT / "P8_Y5_PARENT_QLOC_1915_FIRST_FILL_BLOCKER_LEDGER_NONCLAIM.csv",
    "1915_next": OUT / "P8_Y5_PARENT_QLOC_1915_NEXT_TARGET.csv",
    "944_doc": ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
    "944_validation": OUT / "P8_Y5_BRR545_944_VALIDATION.csv",
    "944_proof_attempt": OUT / "P8_Y5_R10_944_PROOF_ATTEMPT.csv",
    "944_descent_gate": OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
    "944_frame_leak_pack": OUT / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
    "945_doc": ROOT / "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
    "945_validation": OUT / "P8_Y5_BRR545_945_VALIDATION.csv",
    "945_q_map": OUT / "P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv",
    "945_obs_e": OUT / "P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv",
    "945_bound_rows": OUT / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
    "946_validation": OUT / "P8_Y5_BRR545_946_VALIDATION.csv",
    "946_kernel": OUT / "P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv",
    "946_cg_interface": OUT / "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
    "946_decision": OUT / "P8_Y5_R10_946_DECISION_LEDGER.csv",
    "1045_qbar_geom": OUT / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
    "1045_vertical_lift": OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
    "1046_doc": ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
    "1046_validation": OUT / "P8_Y5_BRR545_1046_VALIDATION.csv",
    "1046_no_shadow": OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv",
    "1046_marker_rows": OUT / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv",
    "1046_claim_gates": OUT / "P8_Y5_R10_1046_CLAIM_GATES.csv",
}


SOURCE_NEEDLES = {
    "1915_doc": ["FIRST_FILL_BLOCKED_CONDITIONAL_ZERO_ONLY", "NEXT1915_0_primary"],
    "1915_validation": ["VAL1915_OVERALL,PASS"],
    "1915_first_fill": ["FF1915_6_result", "FIRST_FILL_BLOCKED_CONDITIONAL_ZERO_ONLY"],
    "1915_blockers": ["BL1915_0_parent_q_owner", "BL1915_7_arena_projection_kernels"],
    "1915_next": ["NEXT1915_0_primary", "1916-Y5-R2FR-frame-residual-zero-proof-or-source-bound-row.md"],
    "944_doc": ["descent theorem is real", "c_g/b_g"],
    "944_validation": ["V944_12_validation_rows_ready", "pass"],
    "944_proof_attempt": ["P944_7_verdict", "proof_not_closed"],
    "944_descent_gate": ["QDG944_7_total", "not_proved_current_corpus"],
    "944_frame_leak_pack": ["FLB944_0_cg_weyl", "FLB944_7_epsilon_frame_leak"],
    "945_doc": ["q_candidate(Phi)", "ker(Dq_candidate)"],
    "945_validation": ["V945_12_validation_rows_ready", "pass"],
    "945_q_map": ["QMAP945_6_verdict", "candidate_construction_only_no_descent_claim"],
    "945_obs_e": ["OBS945_6_verdict", "formal_only"],
    "945_bound_rows": ["BND945_0_cg_value", "BND945_7_score_gate"],
    "946_validation": ["V946_12_validation_rows_ready", "pass"],
    "946_kernel": ["KCERT946_3_matter_invisibility", "conditional_not_parent_signed"],
    "946_cg_interface": ["CGB946_0_cg_R10", "MISSING_PARENT_CG_AND_TAU_R10"],
    "946_decision": ["DEC946_0_kernel_certificate", "q_kernel_certificate_failed_current_corpus"],
    "1045_qbar_geom": ["QG1045_4_current_verdict", "FAIL_CURRENT_CLAIM_QBAR_GEOM_ZERO_NOT_SIGNED"],
    "1045_vertical_lift": ["VLG1045_4_verdict", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"],
    "1046_doc": ["Current verdict", "not yet a parent-signed MTS theorem"],
    "1046_validation": ["V1046_13_formalization_untouched", "pass"],
    "1046_no_shadow": ["NSF1046_5_verdict", "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED"],
    "1046_marker_rows": ["QMC1046_0_b_conf", "MISSING_B_CONF_OR_THEOREM_ZERO"],
    "1046_claim_gates": ["CG1046_0_no_shadow_frame", "false"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1916_SOURCE_REGISTER.csv",
    "zero_proof_gate": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_ZERO_PROOF_GATE.csv",
    "parent_signature_contract": OUT / "P8_Y5_PARENT_QLOC_1916_PARENT_SIGNATURE_CONTRACT.csv",
    "source_bound_rows": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_SOURCE_BOUND_ROWS_NONCLAIM.csv",
    "arena_requirements": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_ARENA_PROJECTION_REQUIREMENTS.csv",
    "score_gate": OUT / "P8_Y5_PARENT_QLOC_1916_FRAME_NO_CANCELLATION_SCORE_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1916_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1916_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1916_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1916_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1916_VALIDATION.csv",
}


BRANCH_COPIES = {
    "zero_proof_gate": SOURCE_WEIGHT_DOCS / "FRAME_RESIDUAL_ZERO_PROOF_GATE_1916_NONCLAIM.csv",
    "source_bound_rows": MICROSCOPE_RESIDUALS / OUTPUTS["source_bound_rows"].name,
    "parent_signature_contract": QUEUE / "JR1916_FRAME_PARENT_SIGNATURE_CONTRACT.csv",
    "score_gate": QUARANTINE / OUTPUTS["score_gate"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
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
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    rows = []
    for key, path in INPUTS.items():
        needles = SOURCE_NEEDLES[key]
        exists = path.exists()
        text = source_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        status = "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_OR_NEEDLE_FAILED"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1916 frame residual zero proof or finite source-bound row",
                "needles": ";".join(needles),
                "status": status,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def build_zero_proof_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_0_parent_q_candidate",
            "claim_piece": "parent quotient q_loc exists as parent-owned action object",
            "mathematical_form": "q_loc: Phi_parent -> Q_loc and v_X in ker(Dq_loc)",
            "best_current_evidence": "QMAP945_1 writes q_candidate and QMAP945_3 writes ker(Dq_candidate)",
            "current_status": "CANDIDATE_WRITTEN_NOT_PARENT_SIGNED",
            "missing_for_claim": "variational parent action proves q_loc and identifies its kernel before matter/readout",
            "if_missing": "Dq_loc[v_X]=0 remains notation, not a physical invisibility theorem",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_1_chain_rule_core",
            "claim_piece": "observed coframe vertical derivative vanishes if q and Obs_e are owned",
            "mathematical_form": "e_obs=Obs_e(q_loc(Phi)); Dq_loc[v_X]=0 => Lie_v e_obs=DObs_e[Dq_loc(v_X)]=0",
            "best_current_evidence": "DER943_0, P944_1, QG1045_1",
            "current_status": "EXACT_CONDITIONAL_SUBLEMMA",
            "missing_for_claim": "parent ownership of q_loc and Obs_e",
            "if_missing": "cannot import Z_frame from the sublemma alone",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_2_kernel_null_certificate",
            "claim_piece": "ker(Dq_candidate) is physical gauge/presymplectic-null and matter-invisible",
            "mathematical_form": "i_v Omega_parent=0 and Lie_v S_matter=0 for all ordinary matter/readout standards",
            "best_current_evidence": "KCERT946_0..KCERT946_3",
            "current_status": "FAILED_CURRENT_CORPUS",
            "missing_for_claim": "bulk null, boundary primitive zero, no-marker, and matter-invisibility certificates in one parent branch",
            "if_missing": "candidate quotient is useful notation but not a zero theorem",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_3_observed_frame_uniqueness",
            "claim_piece": "ordinary matter sees only the quotient-owned observed coframe",
            "mathematical_form": "Allowed[S_A]=S_A[Psi_A,e_obs(q),omega[e_obs],theta_A]",
            "best_current_evidence": "OBS945_6, CFC943_2, MFS1045_2",
            "current_status": "FORMAL_FUNCTOR_ONLY_NOT_UNIQUE_PARENT_FRAME",
            "missing_for_claim": "single-public-frame parent clause plus species/readout equivalence",
            "if_missing": "a second frame can re-enter rods, clocks, source support, or free fall",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_4_no_shadow_frame",
            "claim_piece": "hidden conformal/disformal/source-only matter frame is absent",
            "mathematical_form": "exclude e_A=A_A(Xhat)e_obs and g_A=A_A(Xhat)^2 g_obs + D_A(Xhat)U_mu U_nu + ... unless A_A,D_A factor through q",
            "best_current_evidence": "NSF1046_1 exact conditional theorem; NSF1046_5 verdict fail",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "missing_for_claim": "no-extra-frame action-domain exclusion and observable-completeness theorem",
            "if_missing": "c_g/b_conf/b_dis remain finite retained coefficients",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_5_connection_stack",
            "claim_piece": "connection/measure/derivative stack descends with e_obs",
            "mathematical_form": "omega_m=omega[e_obs] or independent non-Hilbert current is retained as q_nonH",
            "best_current_evidence": "QG1045_2, QDG944_4, CFC943_4",
            "current_status": "CONDITIONAL_CONNECTION_CAVEAT_OPEN",
            "missing_for_claim": "Levi-Civita/coframe-owned matter connection or explicit retained current row",
            "if_missing": "torsion, nonmetricity, boundary, or non-Hilbert currents can source local forces",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_6_matter_lift_boundary",
            "claim_piece": "matter lift and local boundary/source support are silent",
            "mathematical_form": "delta_v Psi_A fixed/gauge with delta_v S_A boundary-only and Pi_local dB=0",
            "best_current_evidence": "VLG1045_4, QDG944_6",
            "current_status": "VERTICAL_LIFT_AND_BOUNDARY_SILENCE_NOT_SIGNED",
            "missing_for_claim": "parent matter-bundle lift and compact/exact boundary no-tail certificate",
            "if_missing": "support-shift and boundary tail rows remain live",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ZFG1916_7_total",
            "claim_piece": "Z_frame theorem-zero for frame_or_coframe_residual",
            "mathematical_form": "Z_frame=true iff ZFG1916_0 through ZFG1916_6 are parent-signed in one branch",
            "best_current_evidence": "1915 first-fill plus 944/945/946/1046 audits",
            "current_status": "FRAME_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "missing_for_claim": "multiple parent signatures and no-shadow/kernel certificates",
            "if_missing": "keep finite nonclaim b_g/b_dis/q_nonH/tau/support rows",
            "z_frame_clause_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_parent_signature_contract() -> list[dict[str, Any]]:
    clauses = [
        (
            "PSC1916_0_q_owner",
            "q_loc is primitive or derived from the parent action before matter/readout",
            "q_loc: Phi_parent -> Q_loc, not a post-fit equivalence relation",
            "prevents projection-by-declaration",
            "QDG944_0_parent_q_map;QMAP945_1_candidate_projection",
        ),
        (
            "PSC1916_1_kernel_null",
            "every v_X in ker(Dq_loc) is gauge/presymplectic-null or retained",
            "i_v Omega_parent=0 and i_v Theta_parent=dB_v with zero compact local flux",
            "turns representative motion into non-physical redundancy",
            "KCERT946_0_bulk_presymplectic_null;KCERT946_1_boundary_primitive_zero",
        ),
        (
            "PSC1916_2_obs_e_owner",
            "observed coframe is a quotient functor",
            "e_obs(Phi)=Obs_e(q_loc(Phi))",
            "makes Lie_v e_obs vanish by chain rule",
            "QDG944_2_observed_coframe_functor;OBS945_6_verdict",
        ),
        (
            "PSC1916_3_single_public_frame",
            "ordinary matter/readout has no second conformal/disformal/source-only frame",
            "Allowed[S_A] excludes A_A(Xhat)e_obs and D_A(Xhat) slots unless quotient-owned",
            "kills c_g/b_conf/b_dis instead of fitting them",
            "NSF1046_2_no_extra_frame_slot;NSF1046_5_verdict",
        ),
        (
            "PSC1916_4_connection_lock",
            "matter connection and derivative operator descend with e_obs or are explicit residuals",
            "omega_m=omega[e_obs] or q_nonH retained",
            "prevents torsion/nonmetricity/boundary currents hiding inside frame zero",
            "QDG944_4_geometry_stack_descent;QG1045_2_connection_stack",
        ),
        (
            "PSC1916_5_matter_lift",
            "vertical lift of ordinary matter is fixed/gauge/owned for every species",
            "delta_v Psi_A=0 or owned gauge lift with no physical source work",
            "prevents a convention from masquerading as theorem",
            "VLG1045_0_fixed_lift;VLG1045_4_verdict",
        ),
        (
            "PSC1916_6_boundary_support",
            "local boundary/source support has no projected tail",
            "Pi_local dB_v=0 and source support is fixed by quotient-owned Hilbert current",
            "prevents Delta_W_support and tau/frame readout leakage",
            "QDG944_6_boundary_no_tail;FLB944_5_tau_normal_shift;FLB944_6_support_shift",
        ),
        (
            "PSC1916_7_acceptance",
            "all clauses signed in one branch with source paths",
            "Z_frame=true only if PSC1916_0..PSC1916_6 pass together",
            "prevents cherry-picking old conditional lemmas",
            "ZFG1916_7_total",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "source_ids": source_ids,
            "current_status": "UNSIGNED_CONTRACT_ROW",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for contract_id, required_clause, mathematical_form, why_needed, source_ids in clauses
    ]


def build_source_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FSB1916_0_cg_weyl",
            "c_g/b_g",
            "common conformal/Weyl matter-frame derivative",
            "c_g := Lie_v ln A_g or d ln A_g/dXhat for a representative common matter/source frame",
            "alpha_R10(lambda)=K_X Qbar_XH tau_R10 c_g; gamma-1 ~ M_gamma tau_PPN c_g; WEP/clock projections require arena kernels",
            "Xhat normalization; A_g definition; c_g value or zero theorem; source path; tau_R10/tau_PPN/tau_WEP/tau_clock",
            "dimensionless",
            "R10;PPN;WEP;clock;source_normalization",
            "FLB944_0_cg_weyl;BND945_0_cg_value;CGB946_0_cg_R10;QMC1046_0_b_conf",
            "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
        ),
        (
            "FSB1916_1_b_dis",
            "b_dis",
            "disformal/profile-normalized matter-frame derivative",
            "b_dis := Lie_v B_g or dB_g/dXhat for g_m=A_g^2 g_obs + B_g U_mu U_nu",
            "preferred-frame/PPN/orbital/clock residual ~ tau_dis M_dis b_dis",
            "disformal tensor profile; normalization; b_dis value or absence theorem; arena projections",
            "model_dependent_declared",
            "PPN;preferred_frame;clock;orbital;R10",
            "FLB944_1_disformal;BND945_4_disformal_value;QMC1046_1_b_dis",
            "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
        ),
        (
            "FSB1916_2_q_nonH",
            "q_nonH",
            "non-Hilbert current/source projection from connection, torsion, nonmetricity, or boundary tail",
            "q_nonH := Pi_local J_nonHilbert / M_ref with branch-declared units",
            "local residual envelope includes |Pi_local q_nonH|/M_ref",
            "current definition; projection operator; source worldtube; zero-flux theorem or numeric source row",
            "source_current_units_or_declared_dimensionless_ratio",
            "R10;PPN;WEP;source_normalization",
            "FLB944_4_nonHilbert_current;FRS943_6_nonHilbert_current_projection;QDG944_4_geometry_stack_descent",
            "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
        ),
        (
            "FSB1916_3_delta_tau_n",
            "Delta_tau_n",
            "mismatch between source tau/normal frame and readout tau/normal frame",
            "Delta_tau_n := tau_source*n_source - tau_readout*n_readout in declared local normalization",
            "mass/readout/source envelope includes |Delta_tau_n| plus frame/source support shifts",
            "source/readout tau convention; normal definition; system profile; source path",
            "dimensionless_or_declared_frame_units",
            "clock;orbital;source_support;WEP",
            "FLB944_5_tau_normal_shift;FRS943_4_tau_normal_frame_shift",
            "MISSING_TAU_NORMAL_LOCK_OR_NUMERIC_BOUND",
        ),
        (
            "FSB1916_4_delta_W_support",
            "Delta_W_support",
            "source worldtube/support shift under allowed observed-frame choices",
            "Delta_W_support := change in closure supp T_obs(n,tau) under frame/support rule variation",
            "orbital/local-GR residual envelope includes |Delta Q_H/M_ref| induced by support shift",
            "support selector; Hilbert current positivity/support theorem; system-level source bound",
            "dimensionless_or_declared_support_measure_units",
            "orbital;local_GR;source_support",
            "FLB944_6_support_shift;FRS943_5_worldtube_support_shift",
            "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND",
        ),
        (
            "FSB1916_5_epsilon_frame_abs",
            "epsilon_frame_leak",
            "absolute no-cancellation frame residual envelope",
            "epsilon_frame_leak = |c_g terms| + |b_dis terms| + |q_nonH terms| + |Delta_tau_n terms| + |Delta_W_support terms|",
            "score only by forward projection into each arena; never infer components from bounds",
            "all component values theorem-zero or numeric/source-backed; branch-locked arena kernels",
            "dimensionless_after_declared_normalization",
            "all_local_arenas",
            "FLB944_7_epsilon_frame_leak;NCP1914_0_absolute_sum;DFF1915_2_cancellation_fit",
            "MISSING_COMPONENT_VALUES_AND_ARENA_KERNELS",
        ),
        (
            "FSB1916_6_constant_marker_delegation",
            "b_A/b_alpha/b_clock",
            "constant/material marker leak belongs primarily to constant_sector_residual but can masquerade as frame leakage",
            "delegate to constant-sector row unless parent action puts it inside the frame slot",
            "not scored inside frame residual without explicit branch assignment",
            "constant superselection theorem or finite constant-sector coefficient rows",
            "dimensionless",
            "WEP;clock;R10;composition",
            "FLB944_2_species_mass;FLB944_3_charge_clock_constants;QMC1046_2_b_marker",
            "DELEGATED_TO_CONSTANT_SECTOR_NONCLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "score_formula": score_formula,
            "required_inputs": required_inputs,
            "units": units,
            "observable_links": observable_links,
            "source_ids": source_ids,
            "current_status": current_status,
            "source_path": "MISSING_PARENT_SOURCE",
            "numeric_value": "MISSING_PARENT_INPUT",
            "uncertainty_or_prior": "MISSING_UNCERTAINTY",
            "arena_projection": "MISSING_ARENA_PROJECTION",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for row_id, symbol, definition, formula, score_formula, required_inputs, units, observable_links, source_ids, current_status in rows
    ]


def build_arena_requirements() -> list[dict[str, Any]]:
    arenas = [
        (
            "APR1916_0_WEP_MICROSCOPE_TiPt",
            "WEP_MICROSCOPE_TiPt",
            "eta_AB_frame <= sum_j |K_WEP_j tau_WEP_j R_material/source_j FSB1916_j|",
            "Ti/Pt material response tensor; official source/readout arrays; tau_WEP; frame coefficient values",
            "BLOCKED_PARENT_VALUES_MATERIAL_SOURCE_READOUT_MISSING",
        ),
        (
            "APR1916_1_R10_short_range",
            "R10_short_range",
            "alpha_frame(lambda) <= sum_j |K_R10_j(lambda) Qbar_j(lambda) tau_R10_j(lambda) FSB1916_j|",
            "range kernels; source/test composition; alpha(lambda) bound curve; c_g/q_nonH/source profile",
            "BLOCKED_RANGE_KERNEL_PARENT_VALUES_BOUND_CURVE_MISSING",
        ),
        (
            "APR1916_2_PPN_beta_gamma",
            "PPN_beta_gamma_source",
            "PPN_frame <= |M_gamma c_g| + |M_beta c_g| + |M_dis b_dis| + |M_nonH q_nonH|",
            "weak-field operator matrix; gauge/source calibration; measured-G guard; PPN residual rows",
            "BLOCKED_OPERATOR_MATRIX_GR_LIMIT_SOURCE_CALIBRATION_MISSING",
        ),
        (
            "APR1916_3_clock_drift",
            "clock_and_constant_drift",
            "clock_frame <= |K_clock,c c_g| + |K_clock,dis b_dis| + |K_clock,tau Delta_tau_n| plus constant-sector split",
            "clock sensitivity vector; tau/readout lock; constant-sector split",
            "BLOCKED_CLOCK_SENSITIVITY_CONSTANT_SPLIT_MISSING",
        ),
        (
            "APR1916_4_orbital_GM",
            "orbital_GM_inverse_square",
            "orbital_frame <= |K_orb c_g| + |K_orb,dis b_dis| + |K_orb,support Delta_W_support|",
            "source body composition; orbital GM convention; inverse-square kernel; measured-G guard",
            "BLOCKED_ORBITAL_SOURCE_MAP_AND_GM_GUARD_MISSING",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "arena": arena,
            "projection_formula": projection_formula,
            "needed_inputs": needed_inputs,
            "current_status": current_status,
            "no_cancellation_policy": "ABSOLUTE_SUM_UNLESS_PARENT_IDENTITY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for requirement_id, arena, projection_formula, needed_inputs, current_status in arenas
    ]


def build_score_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NSG1916_0_absolute_envelope",
            "rule": "Frame residual scores use absolute component envelopes until a parent identity proves cancellation.",
            "forbidden_move": "fit c_g against q_nonH or tau/support shifts to cancel a bound",
            "acceptable_replacement": "theorem-zero each row, or source finite rows with covariance/envelope and branch-locked kernels",
            "enforced": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NSG1916_1_no_bound_inversion",
            "rule": "Empirical WEP/R10/PPN/clock/orbital bounds compare against forward projections only.",
            "forbidden_move": "define c_g or b_dis by saturating a local bound",
            "acceptable_replacement": "derive/source c_g first, then compare",
            "enforced": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NSG1916_2_no_GM_absorption",
            "rule": "Measured GM/readout calibration can absorb only branch-declared common-mode terms.",
            "forbidden_move": "hide frame residual in measured GM, tau, or source normalization",
            "acceptable_replacement": "measured-G/common-mode guard plus explicit residual row",
            "enforced": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NSG1916_3_branch_lock",
            "rule": "Source value, arena kernel, material tensor, and readout convention must belong to the same branch.",
            "forbidden_move": "mix a c_g coefficient from one convention with a tau/kernel from another",
            "acceptable_replacement": "branch-locked product row with source anchors",
            "enforced": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NSG1916_4_score_status",
            "rule": "No frame/coframe local score is allowed from 1916.",
            "forbidden_move": "claim local-GR, WEP, PPN, R10, clock, or orbital pass from schema rows",
            "acceptable_replacement": "next proof/source pass",
            "enforced": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1916_0_Z_frame",
            "requirement": "Z_frame=true with parent-signed q/Obs_e/kernel/no-shadow/connection/matter-lift/boundary clauses",
            "current_status": "FALSE_FRAME_ZERO_NOT_PROVED",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1916_1_finite_rows",
            "requirement": "if Z_frame=false, finite c_g/b_dis/q_nonH/Delta_tau/Delta_W rows have numeric values, units, uncertainties, and source paths",
            "current_status": "FALSE_SOURCE_ROWS_SCHEMA_ONLY",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1916_2_arena_kernels",
            "requirement": "at least one arena projection kernel is branch-locked and source-backed",
            "current_status": "FALSE_ARENA_KERNELS_MISSING",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1916_3_no_cancellation",
            "requirement": "absolute envelope/no-bound-inversion/no-GM-hiding policy enforced",
            "current_status": "TRUE_GUARD_ACTIVE_NONCLAIM",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1916_4_claim",
            "requirement": "1916 supports local-GR/WEP/PPN/R10/clock/orbital claim-grade scoring",
            "current_status": "CLAIM_BLOCKED",
            "blocks_claim_if_failed": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1916_0_zero_attempt",
            "decision": "DO_NOT_PROMOTE_FRAME_ZERO",
            "reason": "The chain-rule core is exact, but the parent q-kernel, observed-frame uniqueness, no-shadow action slot, connection lock, matter lift, and boundary silence are not signed in one parent branch.",
            "consequence": "frame_or_coframe_residual remains a live finite residual row, not a local-GR pass.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1916_1_source_bound_rows",
            "decision": "STAGE_FRAME_SOURCE_BOUND_ROWS_NONCLAIM",
            "reason": "If the zero route stays unsigned, the honest fallback is c_g/b_g, b_dis, q_nonH, Delta_tau_n, and Delta_W_support with no-cancellation projection rows.",
            "consequence": "future testing can become data-facing only after real parent values or theorem-zero sources are supplied.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1916_2_next_route",
            "decision": "NEXT_ATTACK_SINGLE_PUBLIC_METRIC_AND_Q_KERNEL",
            "reason": "The least hand-wavy derivation route is to prove the parent has one matter-visible metric/coframe and that ker(Dq) is a true null/gauge kernel.",
            "consequence": "1917 should try to sign that route; if it fails, fill the first c_g source/projection row rather than broad scoring.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1916_0_primary",
            "selection_status": "selected",
            "target_doc": "1917-Y5-R2FR-single-public-metric-q-kernel-null-certificate-or-first-cg-row.md",
            "target_script": "scripts/Y5_R2FR_single_public_metric_q_kernel_null_certificate_or_first_cg_row_1917.py",
            "objective": "try to prove the single-public-metric/no-shadow-frame clause together with a q-kernel null certificate; if not, fill the first finite c_g/b_g source-projection row as nonclaim",
            "success_condition": "either Z_frame first two hard clauses become parent-signed, or FSB1916_0_cg_weyl receives a real source/projection row with units and no claim flags",
            "do_not": "do not import frame zero from the chain-rule lemma alone, do not use local bounds as coefficients, and do not broaden into WEP/PPN scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def build_project_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1916_0_gain",
            "area": "frame/coframe residual",
            "summary": "1916 converts the selected residual into an explicit zero-proof gate plus finite source-bound rows.",
            "risk_level": "STRUCTURE_GAINED_NONCLAIM",
            "project_meaning": "we now know exactly what would make the local-GR frame residual disappear, and what must be sourced if it does not",
            "next_action": "attack single-public-metric/q-kernel certificate or fill c_g row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1916_1_truth",
            "area": "zero theorem",
            "summary": "Z_frame is not proved in the current corpus; chain-rule blindness remains conditional.",
            "risk_level": "PROMISING_BUT_UNSIGNED",
            "project_meaning": "this is a derivation bottleneck, not a data failure",
            "next_action": "sign parent q/Obs_e/no-shadow/kernel clauses in one branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "STAT1916_2_guard",
            "area": "empirical discipline",
            "summary": "source-bound rows are schema-only and all claim flags remain false.",
            "risk_level": "CLAIM_DISCIPLINE_MAINTAINED",
            "project_meaning": "we have not turned missing theory into fake evidence",
            "next_action": "source one row or prove it zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": build_source_register(),
        "zero_proof_gate": build_zero_proof_gate(),
        "parent_signature_contract": build_parent_signature_contract(),
        "source_bound_rows": build_source_bound_rows(),
        "arena_requirements": build_arena_requirements(),
        "score_gate": build_score_gate(),
        "claim_gate": build_claim_gate(),
        "decision": build_decision(),
        "next_target": build_next_target(),
        "project_status": build_project_status(),
    }


def copy_branch_artifacts() -> None:
    for key, destination in BRANCH_COPIES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], destination)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    unsafe: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            if "valid_for_claim" in row and bool_string(row["valid_for_claim"]) != "false":
                unsafe.append(f"{path.name}:valid_for_claim")
            if "claim_allowed" in row and bool_string(row["claim_allowed"]) != "false":
                unsafe.append(f"{path.name}:claim_allowed")
    return not unsafe, "claim flags all false" if not unsafe else ";".join(unsafe)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    failures: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:
            failures.append(f"{path.name}:{exc}")
            continue
        if not rows:
            failures.append(f"{path.name}:no_rows")
    return not failures, "all generated CSVs parse with rows" if not failures else ";".join(failures)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1916_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    zero_rows = csv_rows(OUTPUTS["zero_proof_gate"])
    checks.append(
        {
            "validation_id": "VAL1916_01_zero_gate",
            "status": "PASS"
            if any(row["gate_id"] == "ZFG1916_7_total" and row["current_status"] == "FRAME_ZERO_NOT_PROVED_CURRENT_CORPUS" for row in zero_rows)
            and all(bool_string(row["z_frame_clause_pass"]) == "false" for row in zero_rows)
            else "FAIL",
            "detail": "Z_frame remains false/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    contract_rows = csv_rows(OUTPUTS["parent_signature_contract"])
    checks.append(
        {
            "validation_id": "VAL1916_02_parent_contract",
            "status": "PASS" if len(contract_rows) >= 7 and all(bool_string(row["parent_signed"]) == "false" for row in contract_rows) else "FAIL",
            "detail": "parent signature contract rows are staged unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    source_rows_loaded = csv_rows(OUTPUTS["source_bound_rows"])
    checks.append(
        {
            "validation_id": "VAL1916_03_source_bound_rows",
            "status": "PASS"
            if len(source_rows_loaded) >= 6
            and all(bool_string(row["score_ready"]) == "false" for row in source_rows_loaded)
            and any(row["row_id"] == "FSB1916_0_cg_weyl" and row["current_status"] == "MISSING_PARENT_ZERO_OR_NUMERIC_CG" for row in source_rows_loaded)
            else "FAIL",
            "detail": "finite frame source rows are schema-only nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    arena_rows = csv_rows(OUTPUTS["arena_requirements"])
    checks.append(
        {
            "validation_id": "VAL1916_04_arena_requirements",
            "status": "PASS" if len(arena_rows) == 5 and all(bool_string(row["score_ready"]) == "false" for row in arena_rows) else "FAIL",
            "detail": "five arena requirements remain blocked until kernels/source rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    score_rows = csv_rows(OUTPUTS["score_gate"])
    checks.append(
        {
            "validation_id": "VAL1916_05_score_gate",
            "status": "PASS" if len(score_rows) >= 5 and all(bool_string(row["enforced"]) == "true" for row in score_rows) else "FAIL",
            "detail": "no-cancellation/no-bound-inversion/no-GM-hiding gates enforced",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1916_06_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1916_4_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1916_07_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1916_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1917 single-public-metric/q-kernel route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1916_08_claim_flags_safe",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1916_09_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1916_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1916_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1916-Y5-R2FR-frame-residual",
            "P8_Y5_PARENT_QLOC_1916",
            "Y5_R2FR_frame_residual_zero_proof_or_source_bound_row_1916",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append(
        {
            "validation_id": "VAL1916_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1916_artifact_count={len(formalization_hits)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1916_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1916 frame residual zero proof or source-bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1916 - Frame Residual Zero Proof Or Source-Bound Row

## Purpose

This checkpoint attacks the first residual chosen in 1915: `frame_or_coframe_residual`. It tries the derivation route first. If the zero theorem is not parent-signed, it stages the finite source-bound rows needed for honest future testing.

## Result

- The chain-rule core remains mathematically good: quotient-owned observed coframes are vertically blind.
- `Z_frame=true` is **not** proved in the current corpus.
- The blockers are now exact: parent `q_loc`, kernel nullness, observed-frame uniqueness, no-shadow action slot, connection lock, matter lift, and boundary/source support.
- The finite fallback is explicit: `c_g/b_g`, `b_dis`, `q_nonH`, `Delta_tau_n`, `Delta_W_support`, plus the absolute envelope `epsilon_frame_leak`.
- Every finite row is nonclaim/schema-only until a real source path, numeric value/theorem-zero, uncertainty, units, and arena projection exist.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Frame Zero Proof Gate

{markdown_table(rows_by_name["zero_proof_gate"])}

## Parent Signature Contract

{markdown_table(rows_by_name["parent_signature_contract"])}

## Frame Source-Bound Rows

{markdown_table(rows_by_name["source_bound_rows"])}

## Arena Projection Requirements

{markdown_table(rows_by_name["arena_requirements"])}

## No-Cancellation Score Gate

{markdown_table(rows_by_name["score_gate"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
