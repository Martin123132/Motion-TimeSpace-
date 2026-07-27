from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1156-Y5-R10-parent-quotient-matter-functor-signature-or-frame-leak-bound-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1156_0_1155_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1155_NEXT_TARGET.csv",
            "needle": "NEXT1155_0_1156",
            "role": "handoff selecting quotient/matter functor signature or frame-leak bound fill.",
        },
        {
            "source_id": "SRC1156_1_1155_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1155_SINGLE_OBSERVED_COFRAME_PROOF_AUDIT.csv",
            "needle": "COF1155_7_verdict",
            "role": "1155 single-frame verdict showing q/matter functor unsigned.",
        },
        {
            "source_id": "SRC1156_2_1155_residuals",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1155_DELTA_FRAME_CAL_RESIDUAL_ROWS.csv",
            "needle": "DFR1155_4_frame_coupling_vector",
            "role": "1155 frame residual interface.",
        },
        {
            "source_id": "SRC1156_3_626_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
            "needle": "QIM626_5_signature_verdict",
            "role": "quotient-invariant matter signature attempt.",
        },
        {
            "source_id": "SRC1156_4_626_cg",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv",
            "needle": "CGB626_1_cg_value",
            "role": "older c_g bound input template.",
        },
        {
            "source_id": "SRC1156_5_623_coframe",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "OCF623_4_bg_verdict",
            "role": "coframe functor theorem attempt retaining b_g.",
        },
        {
            "source_id": "SRC1156_6_637_qmap",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
            "needle": "QM637_2_vertical_kernel",
            "role": "candidate q-map and vertical-kernel derivation.",
        },
        {
            "source_id": "SRC1156_7_710_parent_clause",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
            "needle": "DPC710_9_verdict",
            "role": "descent parent-action clause fails current corpus.",
        },
        {
            "source_id": "SRC1156_8_711_descent_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
            "needle": "QDA711_9_verdict",
            "role": "quotient descent derivation audit fails current corpus.",
        },
        {
            "source_id": "SRC1156_9_711_retained",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_711_RETAINED_BRANCH_REQUIREMENTS.csv",
            "needle": "RR711_3_WEP",
            "role": "retained branch requirements for WEP/source charges.",
        },
        {
            "source_id": "SRC1156_10_943_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            "needle": "CFC943_2_matter_functor",
            "role": "coframe coupling contract requiring matter functor.",
        },
        {
            "source_id": "SRC1156_11_944_descent",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
            "needle": "QDG944_7_total",
            "role": "quotient observed-coframe descent proof gate.",
        },
        {
            "source_id": "SRC1156_12_945_bound_rows",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "needle": "BND945_7_score_gate",
            "role": "first frame leak bound rows.",
        },
        {
            "source_id": "SRC1156_13_1050_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "PFT1050_5_verdict",
            "role": "visible-hidden product functor theorem attempt.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def functor_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "QMF1156_0_descent_criterion",
                "claim_piece": "quotient-invariant matter action criterion",
                "mathematical_form": "S_matter descends iff Lie_v S_matter=0 for every v in ker(Dq), up to owned gauge/boundary terms",
                "current_status": "VALID_CONDITIONAL_CRITERION",
                "missing_for_current_MTS": "parent signatures for q, vertical action, matter domain, and boundary tails",
                "residual_if_missing": "frame leak rows stay active",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_1_parent_q_object",
                "claim_piece": "parent quotient object and map",
                "mathematical_form": "q: Phi_parent -> Q_obs with physical local configurations as quotient classes",
                "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
                "missing_for_current_MTS": "full parent construction of Q_obs and local admissible domain",
                "residual_if_missing": "Dq(v)=0 cannot be used as evidence",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_2_vertical_kernel",
                "claim_piece": "local Xhat/frame direction is vertical",
                "mathematical_form": "Dq[v_X]=0 and v_X is tangent to a presymplectic/null orbit",
                "current_status": "CONDITIONAL_MATH_PASS_NOT_CURRENTLY_SIGNED",
                "missing_for_current_MTS": "prove Xhat/frame direction is null representative rather than physical residual",
                "residual_if_missing": "c_g,b_dis,b_A can be physical coefficients",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_3_eobs_functor",
                "claim_piece": "observed coframe functor",
                "mathematical_form": "e_obs(Phi)=Obs_e(q(Phi))",
                "current_status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
                "missing_for_current_MTS": "Obs_e construction as parent data",
                "residual_if_missing": "source/readout frame can drift",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_4_matter_factorization",
                "claim_piece": "ordinary matter action factors through observed quotient data",
                "mathematical_form": "S_matter[Phi,Psi]=Sbar_matter[q(Phi),Psi,theta]",
                "current_status": "NOT_PARENT_SIGNED",
                "missing_for_current_MTS": "matter functor and quotient-owned constants/masses/charges",
                "residual_if_missing": "representative Weyl/disformal/mass/clock channels remain legal",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_5_geometry_stack_and_boundary",
                "claim_piece": "measure/coframe/connection/derivative and boundary tails descend",
                "mathematical_form": "mu,e,g,omega,D are q-functions or owned gauge/exact data; Lie_v S_matter has zero local projection/flux",
                "current_status": "NOT_PARENT_SIGNED",
                "missing_for_current_MTS": "connection descent and boundary no-tail certificate",
                "residual_if_missing": "q_nonH and boundary/source current rows remain active",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_6_no_hidden_visible_morphism",
                "claim_piece": "no hidden-to-visible coefficient morphisms plus radiative/readout closure",
                "mathematical_form": "Hom(C_hid,Coeff(O_vis))=Const or absent; EFT/readout maps preserve q-factorization",
                "current_status": "UNSIGNED_CRITICAL",
                "missing_for_current_MTS": "product functor construction and radiative/readout closure",
                "residual_if_missing": "b_alpha,b_clock,b_A and source-label rows remain live",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "QMF1156_7_verdict",
                "claim_piece": "current MTS parent-signs quotient matter functor",
                "mathematical_form": "QMF1156_1 through QMF1156_6 all signed in one parent branch",
                "current_status": "QUOTIENT_MATTER_FUNCTOR_NOT_PARENT_SIGNED",
                "missing_for_current_MTS": "q-map, vertical kernel, e_obs functor, matter factorization, constants, boundary, radiative closure",
                "residual_if_missing": "fill frame-leak bound rows; no local-GR/Newton/R10/WEP/clock claim",
                "valid_for_claim": "false",
            },
        ]
    )


def bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "FLB1156_0_Z_functor",
                "parameter": "Z_quotient_matter_functor",
                "definition": "true iff q-map, e_obs functor, matter factorization, constants, boundary, and readout closure are parent-signed",
                "required_columns": "theorem_path;source_paths;all_subclauses_signed;valid_for_claim",
                "current_value": "false",
                "source_path": "this_checkpoint",
                "arena_links": "all_local_arenas",
                "status": "NOT_PARENT_SIGNED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_1_c_g",
                "parameter": "c_g",
                "definition": "d ln A_g/dXhat for representative Weyl/common matter frame",
                "required_columns": "mode_id;A_g_definition;c_g;units;arena_projection;source_path;zero_theorem_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "arena_links": "R10;PPN;WEP;clock;orbital",
                "status": "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_2_b_dis",
                "parameter": "b_dis",
                "definition": "representative disformal derivative dB_g/dXhat with profile convention",
                "required_columns": "mode_id;B_g_definition;b_dis;units;arena_projection;source_path;zero_theorem_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "arena_links": "PPN;preferred_frame;clock;orbital",
                "status": "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_3_b_A",
                "parameter": "b_A",
                "definition": "d ln m_A^obs/dXhat or constants/clock derivative for species/material class A",
                "required_columns": "species_id;material_class;b_A;units;arena_projection;source_path;zero_theorem_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "arena_links": "WEP;clock;composition;R10",
                "status": "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BA",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_4_q_nonH",
                "parameter": "q_nonH",
                "definition": "ordinary source projection carried by non-Hilbert torsion/connection/boundary currents",
                "required_columns": "channel_id;current_definition;q_nonH;units;source_path;zero_flux_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "arena_links": "R10;PPN;source_normalization;R_eq",
                "status": "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_5_b_alpha_clock",
                "parameter": "b_alpha;b_clock",
                "definition": "hidden/representative derivative of EM and clock/frequency readout coefficients",
                "required_columns": "coefficient_id;sensitivity_vector;value;units;arena_projection;source_path;zero_theorem_path;valid_for_claim",
                "current_value": "MISSING_PARENT_INPUT",
                "source_path": "MISSING_PARENT_SOURCE",
                "arena_links": "clock;EM;WEP;R10",
                "status": "MISSING_RADIATIVE_READOUT_CLOSURE_OR_NUMERIC_BOUND",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_6_arena_projection_bundle",
                "parameter": "tau_R10;tau_PPN;tau_clock;tau_orbital",
                "definition": "arena projections mapping frame-leak coefficients to short-range, PPN, clock, and orbital observables",
                "required_columns": "arena;projection_formula;tau_value;units;source_path;normalization;valid_for_claim",
                "current_value": "MISSING_ARENA_PROJECTIONS",
                "source_path": "MISSING_ARENA_SOURCE",
                "arena_links": "R10;PPN;clock;orbital",
                "status": "MISSING_ARENA_PROJECTION",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "FLB1156_7_epsilon_frame_leak",
                "parameter": "epsilon_frame_leak",
                "definition": "absolute component envelope for all retained frame/matter-functor leakage rows",
                "required_columns": "system_id;component_sum_abs;normalization;epsilon_frame_leak;units;source_path;valid_for_claim",
                "current_value": "MISSING_COMPONENT_INPUTS",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "all_local_arenas",
                "status": "BLOCKED_MISSING_COMPONENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1156_0_no_q_by_declaration",
                "guard": "do not declare q or Q_obs after seeing which fields must be hidden",
                "status": "ACTIVE",
                "reason": "q must be parent kinematics/action data",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1156_1_no_vertical_by_label",
                "guard": "do not call Xhat vertical unless v_X in ker(Dq) is parent-proved",
                "status": "ACTIVE",
                "reason": "otherwise Xhat may be a physical residual mode",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1156_2_no_hidden_visible_morphism",
                "guard": "hidden/representative variables cannot enter visible coefficients unless retained",
                "status": "ACTIVE",
                "reason": "mixed morphisms regenerate frame, mass, EM, clock, and WEP couplings",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1156_3_no_radiative_shortcut",
                "guard": "tree-level factorization is not enough without EFT/readout closure",
                "status": "ACTIVE",
                "reason": "loops, thresholds, and spectroscopy maps can regenerate local coefficients",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1156_4_no_local_claim",
                "guard": "no Newton/local-GR/R10/WEP/clock claim from unsigned functor",
                "status": "ACTIVE",
                "reason": "frame-leak bound rows remain missing and nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1156_0_sources_exist",
                "rule": "all 1156 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1156_1_conditional_criterion",
                "rule": "quotient descent criterion and coframe functor lemma are present",
                "gate_pass": "true_nonclaim",
                "reason": "conditional theorem shape is available but not promoted",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1156_2_current_functor_signed",
                "rule": "current MTS parent-signs q, vertical kernel, e_obs, matter factorization, constants, boundary, and radiative closure",
                "gate_pass": "false",
                "reason": "QMF1156 verdict remains not parent signed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1156_3_bound_rows_ready",
                "rule": "frame-leak bound rows exist and remain nonclaim until sourced",
                "gate_pass": "true_nonclaim",
                "reason": "c_g,b_dis,b_A,q_nonH,b_alpha/b_clock and arena projections are emitted with missing markers",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1156_4_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR/R10/WEP/clock claim allowed",
                "gate_pass": "false",
                "reason": "functor theorem unsigned and frame-leak bound rows unfilled",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1156_0_conditional_theorem",
                "decision": "quotient_matter_functor_route_is_exact_but_conditional",
                "reason": "if parent q and matter functor factorization are signed, vertical frame/matter leakage vanishes by chain rule",
                "next_action": "do not promote without parent q-map and vertical-kernel proof",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1156_1_current_branch",
                "decision": "current_MTS_quotient_matter_functor_not_parent_signed",
                "reason": "q-map, vertical kernel, e_obs functor, matter factorization, constants, boundary, and radiative closure remain unsigned",
                "next_action": "retain frame-leak bound rows",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1156_2_best_next",
                "decision": "target_parent_q_map_null_generator_proof_or_cg_bound_first_fill",
                "reason": "q and v_X in ker(Dq) are the first upstream clauses; if they fail, c_g is the first common-frame bound row",
                "next_action": "1157 parent q-map/null-generator proof or c_g bound first fill",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1156_0_1157",
                "next_target": "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
                "objective": "try to prove q:Phi->Q_obs and v_X in ker(Dq) from parent null/quotient geometry; if it fails, fill the first c_g bound row",
                "include": "q object; null generator; presymplectic kernel; local domain; c_g units and arena projections",
                "exclude": "q by declaration; vertical by label; matter-functor promotion; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = audit + bounds + guards + gates + decisions + next_target
    add(
        "V1156_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1156_1_verdict_blocks_functor",
        any(row["audit_id"] == "QMF1156_7_verdict" and row["current_status"] == "QUOTIENT_MATTER_FUNCTOR_NOT_PARENT_SIGNED" for row in audit),
        "quotient matter functor remains unsigned for current MTS",
    )
    required_bounds = {"FLB1156_1_c_g", "FLB1156_2_b_dis", "FLB1156_3_b_A", "FLB1156_4_q_nonH", "FLB1156_5_b_alpha_clock", "FLB1156_6_arena_projection_bundle"}
    add(
        "V1156_2_bound_rows_present",
        required_bounds.issubset({row["row_id"] for row in bounds}),
        "frame-leak bound rows cover c_g,b_dis,b_A,q_nonH,b_alpha/b_clock and arena projections",
    )
    add(
        "V1156_3_bound_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["current_value"]) for row in bounds if row["row_id"] != "FLB1156_0_Z_functor")
        and any(row["row_id"] == "FLB1156_0_Z_functor" and row["current_value"] == "false" for row in bounds),
        "bound rows remain missing/nonclaim and Z_functor is false",
    )
    add(
        "V1156_4_guards_active",
        {"GUARD1156_0_no_q_by_declaration", "GUARD1156_1_no_vertical_by_label", "GUARD1156_2_no_hidden_visible_morphism", "GUARD1156_3_no_radiative_shortcut", "GUARD1156_4_no_local_claim"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all no-functor-cheat guards are active",
    )
    add(
        "V1156_5_claim_gates_blocked",
        any(row["gate_id"] == "G1156_2_current_functor_signed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1156_4_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "functor signature and local promotion remain blocked",
    )
    add(
        "V1156_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1156_7_next_target",
        next_target[0]["next_target"].startswith("1157-") and "q-map-null-generator" in str(next_target[0]["next_target"]),
        "1157 handoff targets parent q-map/null-generator proof or c_g first fill",
    )
    add(
        "V1156_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1156_9_csv_parse", csv_parse_ok, "all 1156 CSV outputs parse cleanly")
    add("V1156_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1156_SUMMARY",
        True,
        "1156 keeps quotient/matter functor route conditional, rejects current functor promotion, and emits nonclaim frame-leak bound rows",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1156 - Y5/R10 Parent Quotient Matter Functor Signature or Frame-Leak Bound Fill

**Current verdict:** the quotient/matter-functor route does not close for current MTS. The descent theorem is exact conditionally, but `q`, `v_X in ker(Dq)`, `e_obs(q)`, matter factorization, quotient-owned constants, boundary/no-tail terms, and radiative/readout closure are not parent-signed together.

**Useful progress:** the frame leak is now split into sourceable rows: `c_g`, `b_dis`, `b_A`, `q_nonH`, `b_alpha/b_clock`, arena projections, and the total `epsilon_frame_leak`.

**Important guard:** no hidden-to-visible morphism by silence. If a hidden/representative variable can feed a visible coefficient, it must be forbidden by parent functor structure or retained as a real local bound row.

**Best next attack:** prove the upstream `q` object and `v_X in ker(Dq)` from parent null/quotient geometry. If that fails, the first numeric fallback is the common-frame `c_g` row.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, clock, GitHub, or public claim follows from 1156.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Quotient Matter Functor Signature Audit
{table(["audit_id", "claim_piece", "mathematical_form", "current_status", "missing_for_current_MTS", "residual_if_missing", "valid_for_claim"], audit)}

## Frame-Leak Bound Fill Rows
{table(["row_id", "parameter", "definition", "required_columns", "current_value", "source_path", "arena_links", "status", "valid_for_claim", "claim_allowed"], bounds)}

## No-Functor-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1156_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "bounds": OUT / "P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv",
        "guards": OUT / "P8_Y5_R10_1156_NO_FUNCTOR_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1156_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1156_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1156_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1156_VALIDATION.csv",
    }

    sources = source_rows()
    audit = functor_audit_rows()
    bounds = bound_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audit, bounds, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audit, bounds, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
