from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1029_0_1028_next", "source-intake/mts_residuals/P8_Y5_R10_1028_NEXT_TARGET.csv", "1029-Y5-R10-cg-no-shadow", "1028 handoff to c_g/no-shadow frame target."),
        ("SRC1029_1_1028_theorem", "source-intake/mts_residuals/P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv", "NM1028_4_no_shadow_frame", "1028 identifies no-shadow-frame as a missing theorem."),
        ("SRC1029_2_1028_bound_pack", "source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv", "FMB1028_0_cg", "1028 c_g row and projection requirements."),
        ("SRC1029_3_1028_links", "source-intake/mts_residuals/P8_Y5_R10_1028_OBSERVABLE_LINK_MAP.csv", "OL1028_0_R10_alpha", "1028 observable map for c_g."),
        ("SRC1029_4_943_contract", "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv", "CFC943_6_no_shadow_frame_rule", "943 no-shadow-frame rule as contract."),
        ("SRC1029_5_944_frame_pack", "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv", "FLB944_0_cg_weyl", "944 c_g frame-leak bound row."),
        ("SRC1029_6_945_obs_audit", "source-intake/mts_residuals/P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv", "OBS945_3_representative_weyl", "945 representative Weyl counterexample."),
        ("SRC1029_7_945_kernel", "source-intake/mts_residuals/P8_Y5_R10_945_KERNEL_TEST.csv", "KT945_4_representative_weyl", "945 kernel test for representative Weyl variation."),
        ("SRC1029_8_946_interface", "source-intake/mts_residuals/P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv", "CGB946_0_cg_R10", "946 empirical c_g interface."),
        ("SRC1029_9_947_projection", "source-intake/mts_residuals/P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv", "PFA947_4_cg_parent_value", "947 c_g parent value/projection gap."),
        ("SRC1029_10_951_provenance", "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv", "PGS951_0_numeric_value", "951 finite coefficient provenance gate."),
        ("SRC1029_11_952_intake", "source-intake/mts_residuals/P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv", "CIT952_4_zero_theorem_switch", "952 coefficient intake template."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def no_shadow_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "NST1029_0_define_shadow_frame",
            "claim": "A shadow frame is an ordinary matter/readout frame not uniquely equal to the quotient-owned observed coframe.",
            "mathematical_form": "e_m = A_g(Xhat) e_obs or g_m = A_g(Xhat)^2 g_obs, with c_g := Lie_vX ln A_g",
            "derivation_step": "definition",
            "current_status": "DEFINITION_SHARP",
            "missing_for_claim": "none at definition level",
            "if_missing": "cannot name the retained frame coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_1_chain_rule_zero",
            "claim": "If A_g factors only through q, vertical X cannot change it.",
            "mathematical_form": "A_g(Phi)=Abar(q(Phi)) and Dq[v_X]=0 => Lie_vX ln A_g = D ln Abar[Dq(v_X)] = 0",
            "derivation_step": "valid conditional proof",
            "current_status": "CONDITIONAL_THEOREM_VALID",
            "missing_for_claim": "parent-signed q-kernel and factorization of A_g through q",
            "if_missing": "c_g must be retained as finite",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_2_no_extra_frame_slot",
            "claim": "The parent matter action contains no independent A_g(Xhat) frame slot.",
            "mathematical_form": "Allowed[S_matter] = Sbar[Psi,e_obs(q(Phi)),omega[e_obs],theta(q)] and excludes Sbar[Psi,A_g(Xhat)e_obs,...]",
            "derivation_step": "action-domain exclusion",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "missing_for_claim": "single-public-metric/no-extra-frame parent action clause",
            "if_missing": "universal scalar-tensor-like c_g remains legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_3_observability_rule",
            "claim": "Any frame that changes rods, clocks, masses, charges, free fall, or source readout is observable and must be in q or retained.",
            "mathematical_form": "A_g affects experiment => A_g in Q_obs or coefficient row c_g retained",
            "derivation_step": "no-shadow-frame rule",
            "current_status": "CONTRACT_AVAILABLE_NOT_THEOREM",
            "missing_for_claim": "parent proof that observable frame data cannot be hidden in representative variables",
            "if_missing": "field-renaming can hide the same coupling in masses, G_eff, or source normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_4_common_mode_limit",
            "claim": "A constant common conformal normalization can be calibrated, but an X-dependent derivative is physical unless theorem-zero.",
            "mathematical_form": "A_g=A_0 is unit/G calibration; Lie_vX ln A_g=c_g produces trace/source coupling when X varies",
            "derivation_step": "calibration separation",
            "current_status": "CONDITIONAL_PHYSICS_GUARD",
            "missing_for_claim": "source-measure and local weak-field projection that separates calibration from finite coupling",
            "if_missing": "do not treat common WEP silence as c_g=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_5_matter_variation_trace",
            "claim": "Finite c_g is the first-order matter-frame source coupling.",
            "mathematical_form": "delta_X S_matter contains (1/2) sqrt(-g) T^{mu nu} delta_X g_m,mu nu ~ sqrt(-g) T c_g delta Xhat",
            "derivation_step": "local variation shape",
            "current_status": "FORMULA_SHAPE_VALID_SIGN_CONVENTION_TO_BE_FIXED",
            "missing_for_claim": "normalization of Xhat, sign convention, trace/source support, and arena projection",
            "if_missing": "only absolute-bound envelope may be used",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NST1029_6_verdict",
            "claim": "c_g=0 no-shadow-frame theorem is derived in the current corpus.",
            "mathematical_form": "NST1029_1 plus NST1029_2 plus NST1029_3 with parent signatures => c_g=0",
            "derivation_step": "attempt verdict",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "parent-signed single-public-metric/no-extra-frame clause and q-kernel ownership",
            "if_missing": "stage c_g intake/provenance and tau projection rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE1029_0_scalar_tensor_common_frame",
            "weak_premise": "universal matter coupling or WEP compliance",
            "construction": "e_m=A_g(Xhat)e_obs with the same A_g for every ordinary species",
            "failure": "composition WEP can be quiet while a common trace coupling/fifth-force remains",
            "required_repair": "parent no-extra-frame theorem or numeric c_g/tau projections",
            "blocks_cg_zero": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1029_1_einstein_jordan_relabel",
            "weak_premise": "choose e_obs as the matter frame by notation",
            "construction": "move A_g(Xhat) into masses, G_eff, or source normalization by a frame rename",
            "failure": "c_g disappears from one ledger and reappears as b_A, b_alpha, or source-normalization residual",
            "required_repair": "same-frame/source-measure ledger across matter, clocks, and active source",
            "blocks_cg_zero": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1029_2_constant_unit_absorption",
            "weak_premise": "common conformal factor is just units",
            "construction": "A_g=A_0 is absorbable, but A_g(Xhat)=A_0 exp(c_g Xhat) is not if Xhat varies locally",
            "failure": "calibration removes only the constant mode, not the derivative coupling",
            "required_repair": "prove Lie_vX A_g=0 or bound c_g with profile/arena projection",
            "blocks_cg_zero": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1029_3_disformal_partner",
            "weak_premise": "killing the Weyl coefficient kills all frame leakage",
            "construction": "g_m=A_g^2 g_obs+B_g(Xhat)U_muU_nu with c_g=0 but b_dis nonzero",
            "failure": "preferred-frame/PPN/clock leakage survives the c_g branch",
            "required_repair": "also close b_dis or retain it in the total qbarXT envelope",
            "blocks_cg_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1029_4_boundary_source_support",
            "weak_premise": "matter-frame c_g=0 is enough for local GR",
            "construction": "ordinary matter frame is clean but non-Hilbert current or support shift carries source coupling",
            "failure": "local source normalization can remain non-GR even with c_g=0",
            "required_repair": "q_nonH and Delta_W_support theorem-zero or numeric bound rows",
            "blocks_cg_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def cg_intake_template_rows() -> list[dict[str, str]]:
    return [
        {
            "intake_id": "CGI1029_0_zero_theorem_branch",
            "coefficient_symbol": "c_g",
            "branch_type": "parent_zero_theorem",
            "candidate_value": "PARENT_SIGNED_TRUE_REQUIRED",
            "units": "dimensionless",
            "candidate_source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_PARENT_SIGNED_NO_SHADOW_FRAME_THEOREM",
            "comparison_bound": "zero theorem must close before bypassing finite bounds",
            "comparison_bound_source": "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
            "claim_policy": "NONCLAIM_UNTIL_FULL_LOCAL_STACK_CLOSES",
            "ready_for_provenance_gate": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "intake_id": "CGI1029_1_finite_cg_R10",
            "coefficient_symbol": "c_g",
            "branch_type": "finite_value",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "candidate_source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_DERIVATION_STATUS",
            "comparison_bound": "alpha_bound(lambda) / |K_X(lambda) Qbar_XH tau_R10|",
            "comparison_bound_source": "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv;P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv",
            "claim_policy": "NONCLAIM_UNTIL_CG_AND_TAU_R10_ARE_SOURCED",
            "ready_for_provenance_gate": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "intake_id": "CGI1029_2_finite_cg_PPN_gamma",
            "coefficient_symbol": "c_g",
            "branch_type": "finite_value",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "candidate_source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_DERIVATION_STATUS",
            "comparison_bound": "2.3e-05 / |M_gamma tau_PPN|",
            "comparison_bound_source": "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
            "claim_policy": "NONCLAIM_UNTIL_RESPONSE_MATRIX_AND_GAUGE_ARE_SOURCED",
            "ready_for_provenance_gate": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "intake_id": "CGI1029_3_finite_cg_PPN_beta",
            "coefficient_symbol": "c_g",
            "branch_type": "finite_value",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "candidate_source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_DERIVATION_STATUS",
            "comparison_bound": "7.8e-05 / |M_beta tau_beta|",
            "comparison_bound_source": "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv",
            "claim_policy": "NONCLAIM_UNTIL_RESPONSE_MATRIX_AND_GAUGE_ARE_SOURCED",
            "ready_for_provenance_gate": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "intake_id": "CGI1029_4_finite_cg_clock_common",
            "coefficient_symbol": "c_g",
            "branch_type": "finite_value_or_parent_zero",
            "candidate_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "candidate_source_path": "MISSING_PARENT_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "derivation_status": "MISSING_DERIVATION_STATUS",
            "comparison_bound": "requires clock projection and separation from b_A/b_alpha",
            "comparison_bound_source": "P8_Y5_R10_1028_OBSERVABLE_LINK_MAP.csv",
            "claim_policy": "NONCLAIM_COMMON_MODE_NOT_WEP_ONLY",
            "ready_for_provenance_gate": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_projection_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "TAU1029_0_R10",
            "projection_symbol": "tau_R10",
            "arena": "R10 short-range inverse-square/fifth-force",
            "required_formula": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g plus retained marker/source tails",
            "required_inputs": "K_X(lambda);Qbar_XH;tau_R10;c_g;source/test material convention;lambda profile",
            "current_status": "MISSING_TAU_R10_AND_PARENT_CG",
            "source_hint": "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv:PFA947_0_R10_projection",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "TAU1029_1_PPN_gamma_beta",
            "projection_symbol": "tau_PPN",
            "arena": "PPN gamma/beta",
            "required_formula": "gamma_minus_1,beta_minus_1 = response_operator(profile,gauge) * tau_PPN * c_g",
            "required_inputs": "M_gamma;M_beta;tau_PPN;gauge;weak-field order;disformal separation",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "source_hint": "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv:PFA947_1_PPN_projection",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "TAU1029_2_clock_common",
            "projection_symbol": "tau_clock",
            "arena": "atomic clocks/readout",
            "required_formula": "delta ln nu = tau_clock c_g + S_A b_A + S_alpha b_alpha after calibration separation",
            "required_inputs": "clock sensitivities;calibration convention;standalone c_g versus b_A/b_alpha split",
            "current_status": "MISSING_CLOCK_COMMON_MODE_PROJECTION",
            "source_hint": "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv:FMB1028_3_tau_clock",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "TAU1029_3_WEP_limit",
            "projection_symbol": "tau_WEP_common_mode",
            "arena": "WEP/composition",
            "required_formula": "common c_g alone is not a differential WEP signal; WEP constrains differences or marker coefficients",
            "required_inputs": "material sensitivities and b_A/b_alpha rows if composition signal is used",
            "current_status": "WEP_ONLY_ZERO_FORBIDDEN",
            "source_hint": "P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv:BI947_2_bA_WEP_alpha",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "TAU1029_4_orbital_source",
            "projection_symbol": "tau_orbital",
            "arena": "orbital/source support/local GR",
            "required_formula": "source residual = tau_orbital c_g + q_nonH + Delta_W_support terms",
            "required_inputs": "source-measure selector;worldtube support;hidden-current silence;profile convention",
            "current_status": "MISSING_SOURCE_SUPPORT_PROJECTION",
            "source_hint": "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv:FMB1028_4_tau_orbital",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def provenance_dryrun_rows() -> list[dict[str, str]]:
    rows = []
    for index, row in enumerate(cg_intake_template_rows()):
        missing = []
        if row["candidate_value"].startswith("MISSING") or row["candidate_value"].endswith("REQUIRED"):
            missing.append("candidate_value_or_parent_signed_true")
        if row["candidate_source_path"].startswith("MISSING"):
            missing.append("candidate_source_path")
        if row["source_row_id"].startswith("MISSING"):
            missing.append("source_row_id")
        if row["derivation_status"].startswith("MISSING"):
            missing.append("derivation_status")
        rows.append(
            {
                "dryrun_id": f"CGD1029_{index}_{row['intake_id'].split('_', 1)[1]}",
                "coefficient_symbol": row["coefficient_symbol"],
                "arena_or_branch": row["branch_type"],
                "candidate_value": row["candidate_value"],
                "provenance_status": "rejected_missing_provenance",
                "failure_reasons": ";".join(missing),
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1029_0_sources",
            "claim": "all 1029 cited sources exist",
            "gate_pass": "true",
            "reason": "validated by source register",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1029_1_cg_zero",
            "claim": "c_g=0 by parent no-shadow-frame theorem",
            "gate_pass": "false",
            "reason": "NST1029_6 fails current claim because no-extra-frame parent clause is unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1029_2_finite_cg_score",
            "claim": "finite c_g row can be scored",
            "gate_pass": "false",
            "reason": "candidate value, source path, derivation status, and tau projections are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1029_3_WEP_shortcut",
            "claim": "WEP silence proves c_g=0",
            "gate_pass": "false",
            "reason": "a common Weyl coupling can be composition-blind while still producing fifth-force/PPN effects",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1029_4_no_cancellation",
            "claim": "unknown marker/source tails may cancel c_g",
            "gate_pass": "true",
            "reason": "cancellation is forbidden; each component must be theorem-zero or separately bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1029_5_local_GR",
            "claim": "local GR/Newton or R10/PPN pass is established",
            "gate_pass": "false",
            "reason": "1029 is theorem audit plus provenance intake only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1029_0_derivation",
            "decision": "The c_g zero theorem is mathematically clean under a single-public-metric/no-extra-frame parent clause.",
            "because": "if A_g is absent as an independent argument or factors through q, then verticality gives Lie_vX ln A_g=0 by chain rule.",
            "next_action": "try to derive the no-extra-frame parent clause from the action domain rather than assert it",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1029_1_current_status",
            "decision": "Current MTS does not yet prove c_g=0.",
            "because": "representative Weyl frame, scalar-tensor common-frame, and frame-relabel counterexamples remain legal unless the parent action excludes them.",
            "next_action": "retain c_g as a nonclaim coefficient row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1029_2_intake",
            "decision": "The first c_g intake/provenance template is staged.",
            "because": "finite or zero-theorem branches now require candidate value, source path, source row id, derivation status, units, bound link, and tau projections.",
            "next_action": "do not score c_g until the intake and tau projection rows are real",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1029_3_next_target",
            "decision": "Next target is single-public-metric parent action derivation or c_g provenance gate.",
            "because": "this is the exact parent clause needed to turn no-shadow frame from a closure into a theorem; failing that, c_g must enter a strict provenance gate.",
            "next_action": "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "objective": "derive the parent action clause that ordinary matter has only one public metric/coframe argument and no A_g(Xhat) shadow-frame slot; if this fails, route c_g through the 1029/951 provenance gate with sourced tau_R10 and tau_PPN projections",
            "include": "matter action domain, observed coframe uniqueness, quotient functor, no extra frame argument, no field-rename hiding, c_g source path, tau_R10, tau_PPN, provenance gate",
            "exclude": "WEP-only proof, notation-only matter-frame choice, placeholder c_g values, cancellation with b_A/b_alpha/q_nonH/support, local-GR/R10/PPN claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    intake: list[dict[str, str]],
    tau: list[dict[str, str]],
    dryrun: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    theorem_required = {f"NST1029_{idx}_{name}" for idx, name in [
        (0, "define_shadow_frame"),
        (1, "chain_rule_zero"),
        (2, "no_extra_frame_slot"),
        (3, "observability_rule"),
        (4, "common_mode_limit"),
        (5, "matter_variation_trace"),
        (6, "verdict"),
    ]}
    counter_required = {f"CE1029_{idx}_{name}" for idx, name in [
        (0, "scalar_tensor_common_frame"),
        (1, "einstein_jordan_relabel"),
        (2, "constant_unit_absorption"),
        (3, "disformal_partner"),
        (4, "boundary_source_support"),
    ]}
    intake_required = {f"CGI1029_{idx}_{name}" for idx, name in [
        (0, "zero_theorem_branch"),
        (1, "finite_cg_R10"),
        (2, "finite_cg_PPN_gamma"),
        (3, "finite_cg_PPN_beta"),
        (4, "finite_cg_clock_common"),
    ]}
    tau_required = {f"TAU1029_{idx}_{name}" for idx, name in [
        (0, "R10"),
        (1, "PPN_gamma_beta"),
        (2, "clock_common"),
        (3, "WEP_limit"),
        (4, "orbital_source"),
    ]}
    checks = [
        ("V1029_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1029_1_theorem_rows_complete", theorem_required.issubset({row["theorem_id"] for row in theorem}), "no-shadow theorem audit covers definition, chain rule, no-extra-frame, observability, calibration, trace variation, and verdict"),
        ("V1029_2_cg_zero_not_claimed", any(row["theorem_id"] == "NST1029_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem), "c_g=0 remains nonclaim"),
        ("V1029_3_counterexamples_complete", counter_required.issubset({row["counterexample_id"] for row in counterexamples}), "counterexamples cover common frame, relabel, calibration, disformal partner, and source support"),
        ("V1029_4_counterexamples_block", all(row["valid_for_claim"] == "false" for row in counterexamples) and any(row["counterexample_id"] == "CE1029_0_scalar_tensor_common_frame" and flag(row["blocks_cg_zero"]) for row in counterexamples), "common-frame counterexample blocks WEP-only c_g zero"),
        ("V1029_5_intake_complete", intake_required.issubset({row["intake_id"] for row in intake}), "c_g intake rows cover zero theorem, R10, PPN gamma/beta, and clock common-mode branches"),
        ("V1029_6_intake_nonclaim", all(row["ready_for_provenance_gate"] == "false" and row["valid_for_claim"] == "false" for row in intake), "intake rows refuse placeholder promotion"),
        ("V1029_7_tau_requirements_complete", tau_required.issubset({row["projection_id"] for row in tau}), "tau requirements cover R10, PPN, clocks, WEP limit, and orbital/source support"),
        ("V1029_8_dryrun_rejects_placeholders", all(row["score_eligible"] == "false" and row["claim_allowed"] == "false" for row in dryrun), "provenance dry run rejects every placeholder c_g row"),
        ("V1029_9_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1029_10_no_cancellation_guard", any(row["gate_id"] == "CGATE1029_4_no_cancellation" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1029_11_decision_next", any(row["decision_id"] == "DEC1029_3_next_target" for row in decisions), "decision ledger selects the 1030 target"),
        ("V1029_12_next_target_written", len(next_target) == 1 and "1030-Y5-R10-single-public-metric" in next_target[0]["next_target"], "1030 next target row is present"),
        ("V1029_13_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, theorem, counterexamples, intake, tau, dryrun, gates, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1029_14_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1029_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1029 c_g no-shadow theorem/provenance validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    intake: list[dict[str, str]],
    tau: list[dict[str, str]],
    dryrun: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1029 Y5 R10 c_g no-shadow-frame theorem or first numeric coupling row",
            "",
            "**Status:** The no-shadow-frame theorem now has an exact conditional derivation: if the matter/readout frame either is not an independent parent argument, or factors only through the parent quotient `q`, then `c_g = Lie_vX ln A_g = 0` follows by chain rule. Current MTS still cannot claim this because the single-public-metric/no-extra-frame parent action clause and q-kernel ownership are not signed.",
            "",
            "**Claim ceiling:** no `c_g=0`, finite-`c_g`, R10, WEP, clock, EM, PPN, orbital, local-GR/Newton, or source-zero pass is allowed from 1029.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## No-shadow-frame theorem audit",
            md_table(theorem, ["theorem_id", "claim", "mathematical_form", "derivation_step", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "## Counterexample ledger",
            md_table(counterexamples, ["counterexample_id", "weak_premise", "construction", "failure", "required_repair", "blocks_cg_zero", "valid_for_claim"]),
            "## c_g intake template",
            md_table(intake, ["intake_id", "coefficient_symbol", "branch_type", "candidate_value", "units", "candidate_source_path", "source_row_id", "derivation_status", "comparison_bound", "comparison_bound_source", "claim_policy", "ready_for_provenance_gate", "valid_for_claim"]),
            "## Tau projection requirements",
            md_table(tau, ["projection_id", "projection_symbol", "arena", "required_formula", "required_inputs", "current_status", "source_hint", "score_ready", "valid_for_claim"]),
            "## Provenance dry run",
            md_table(dryrun, ["dryrun_id", "coefficient_symbol", "arena_or_branch", "candidate_value", "provenance_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = no_shadow_theorem_rows()
    counterexamples = counterexample_rows()
    intake = cg_intake_template_rows()
    tau = tau_projection_rows()
    dryrun = provenance_dryrun_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, counterexamples, intake, tau, dryrun, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1029_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1029_COUNTEREXAMPLE_LEDGER.csv", counterexamples)
    write_csv(OUT / "P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv", intake)
    write_csv(OUT / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", tau)
    write_csv(OUT / "P8_Y5_R10_1029_CG_PROVENANCE_DRYRUN.csv", dryrun)
    write_csv(OUT / "P8_Y5_R10_1029_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1029_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1029_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1029_VALIDATION.csv", validations)
    write_doc(sources, theorem, counterexamples, intake, tau, dryrun, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
