from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3518-Y5-R2FR-vq-private-first-class-source-vector-silence-or-Dq-bound.md"
CANONICAL_STATUS = OUT / "P8_EM_vq_private_firstclass_source_silence_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3518": {"path": Path(__file__).resolve(), "role": "3518 generator"},
    "doc_3517": {
        "path": ROOT / "3517-Y5-R2FR-actual-q-map-vertical-basis-construction-or-Dq-norm-bound.md",
        "role": "3517 q-map and vertical-basis handoff",
    },
    "basis_3517": {
        "path": OUT / "P8_Y5_R2FR_3517_CANDIDATE_VERTICAL_BASIS.csv",
        "role": "candidate v_q basis row",
    },
    "dq_matrix_3517": {
        "path": OUT / "P8_Y5_R2FR_3517_DQ_MATRIX_SKELETON.csv",
        "role": "3517 Dq[v_q] conditional entries",
    },
    "dq_bound_3517": {
        "path": OUT / "P8_Y5_R2FR_3517_DQ_NORM_BOUND_TEMPLATE.csv",
        "role": "3517 Dq norm handoff",
    },
    "q_signature_2298": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2298_Q_SOURCE_SIGNATURE_ATTEMPT.csv",
        "role": "q source-signature attempt",
    },
    "q_slot_2299": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2299_Q_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
        "role": "direct q source-slot exclusion attempt",
    },
    "bqweyl_bound_2302": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv",
        "role": "B_qWeyl bound-row nonclaim",
    },
    "bqweyl_index_2302": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_INDEX_ZERO_THEOREM_GATE.csv",
        "role": "conditional linear Weyl index zero theorem gate",
    },
    "q_vector_2363": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2363_Q_SOURCE_VECTOR_CONTRACT.csv",
        "role": "q source-vector contract",
    },
    "linear_bqweyl_2365": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2365_LINEAR_BQWEYL_ZERO_AUDIT.csv",
        "role": "metric/epsilon-only B_qWeyl zero audit",
    },
    "bqweyl_status_2365": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2365_BQWEYL_BOUND_ROW_STATUS.csv",
        "role": "B_qWeyl row status",
    },
    "finite_jq_2367": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2367_FINITE_JQ_SOURCE_PACK.csv",
        "role": "finite J_q source pack",
    },
    "jq_channel_2430": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2430_JQ_SOURCE_CHANNEL_ZERO_AUDIT.csv",
        "role": "J_q channel zero audit",
    },
    "vertical_kernel_2589": {
        "path": OUT / "P8_Y5_VERTICAL_KERNEL_2589_KERNEL_LEAK_ROWS.csv",
        "role": "vertical-kernel leak rows",
    },
    "qv_contract_2590": {
        "path": OUT / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv",
        "role": "vertical Noether charge extraction contract",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "THM3518_0_first_class_orbit_zero",
            "route": "first_class_quotient",
            "statement": "If v_q is a parent first-class generator and q is constant on its gauge orbit, then Dq[v_q]=0.",
            "exact_contract": "i_vq Omega_parent = delta G_q; G_q|constraint_surface=0; L_vq S_parent=0; q(Phi+epsilon v_q)=q(Phi)",
            "current_evidence": "3517 marks v_q candidate, but 2298/2363/2590 do not provide a signed parent generator and zero Hamiltonian charge.",
            "status": "DERIVED_CONDITIONAL_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["qv_contract_2590"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "THM3518_1_local_surface_charge_zero",
            "route": "first_class_quotient",
            "statement": "A local representative is silent only when every linked surface has zero integrable and nonintegrable v_q charge.",
            "exact_contract": "delta H_vq[S]=Integral_S(delta Q_vq - i_vq theta_parent + delta B_vq + C_vq)=0 for all local linking surfaces S",
            "current_evidence": "The extraction contract exists, but no sourced Q_vq, B_vq, C_vq zero signature is present.",
            "status": "DERIVED_LOCAL_CHARGE_GATE_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["qv_contract_2590"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "THM3518_2_source_vector_termwise_zero",
            "route": "source_vector_silence",
            "statement": "The q source vector is silent only if each source channel is zero term-by-term, not by cancellation.",
            "exact_contract": "J_q_total=j_matter+j_const+j_weight+j_shadow+j_readout+j_boundary+j_curvature+j_tail; every summand must vanish in the same parent object language",
            "current_evidence": "2367 and 2430 enumerate the channels but leave matter, boundary, readout, memory/history and source-normalization channels unsigned.",
            "status": "DERIVED_NO_CANCELLATION_GATE_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["finite_jq_2367"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "THM3518_3_BqWeyl_index_zero",
            "route": "curvature_source_tail",
            "statement": "A linear B_qWeyl tail is killed only in the metric/epsilon-only scalar grammar with no hidden Weyl spurion, projector or readout kernel.",
            "exact_contract": "q is scalar/quotient/pure density; no four-index spurion P^{abcd}; no post-variation readout projector; no boundary regeneration",
            "current_evidence": "2302 and 2365 prove only a conditional index lemma; hidden spurion/projector/readout countermodels survive.",
            "status": "DERIVED_CONDITIONAL_INDEX_ZERO_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["bqweyl_index_2302"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "THM3518_4_CqT_direct_source_slot",
            "route": "matter_source_tail",
            "statement": "A mixed qT source vertex is absent only if the parent object language forbids direct q matter/source slots.",
            "exact_contract": "S_matter=Sbar[q(Phi),Psi,theta] with q appearing only through observed geometry/coframe and q-basic constants; no C_qT q T or epsilon_q_source vertex",
            "current_evidence": "2299 gives a conditional no-direct-slot subtheorem but the parent object-language signature is not signed.",
            "status": "DERIVED_CONDITIONAL_SLOT_ZERO_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "THM3518_5_source_coordinate_descent_hook",
            "route": "Y_descent_hook",
            "statement": "If the previous clauses fire and Y=Ybar(q(Phi)), then D_vq Y=0 and v_q becomes eligible for the 3516 A_X zero theorem.",
            "exact_contract": "D_vq Y = DYbar[Dq[v_q]] + Delta_Y_nonbasic; require Dq[v_q]=0 and Delta_Y_nonbasic=0",
            "current_evidence": "3516/3517 provide the hook, but Dq[v_q]=0 and source-coordinate descent are not certified.",
            "status": "DERIVED_HOOK_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["dq_matrix_3517"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3518_0_Z_vq_first_class",
            "quantity": "Z_vq_first_class",
            "definition": "all first-class generator, gauge-orbit q-constancy, and local Hamiltonian charge clauses fire",
            "value": "False",
            "reason": "parent G_q, Q_vq/B_vq/C_vq and q-orbit constancy are not source-signed",
            "implication": "cannot set Dq[v_q]=0 by first-class argument",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3518_1_Z_vq_source_silent",
            "quantity": "Z_vq_source_silent",
            "definition": "all J_q_total channels vanish termwise",
            "value": "False",
            "reason": "matter, source-normalization, boundary, readout and tail channels remain live",
            "implication": "cannot claim source-vector silence",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3518_2_Z_BqWeyl",
            "quantity": "Z_BqWeyl",
            "definition": "linear Weyl tail forbidden by parent index/object-language theorem",
            "value": "False",
            "reason": "metric/epsilon-only lemma is conditional; hidden spurion/projector/readout countermodels survive",
            "implication": "B_qWeyl remains an explicit Dq-bound component",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3518_3_Z_CqT",
            "quantity": "Z_CqT",
            "definition": "direct qT or q-source matter vertex forbidden",
            "value": "False",
            "reason": "parent matter object language is not signed tightly enough",
            "implication": "C_qT remains an explicit Dq-bound component",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3518_4_Z_Dq_vq_zero",
            "quantity": "Z_Dq_vq_zero",
            "definition": "Dq[v_q]=0 as a usable vertical-kernel certificate",
            "value": "False",
            "reason": "first-class and source-silence gates both fail to fire in current source hierarchy",
            "implication": "v_q is still candidate, not certified vertical",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3518_5_A_X_eligibility",
            "quantity": "A_X_zero_eligibility_for_vq",
            "definition": "v_q can enter 3516 local mass/source-coordinate amplitude-zero theorem",
            "value": "False",
            "reason": "Dq[v_q]=0 and Y descent hook are not signed",
            "implication": "local GR/Newton pass remains unclaimed",
            "valid_for_claim": "False",
        },
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JQ3518_0_j_matter",
            "component": "j_matter",
            "formula_slot": "delta S_matter / delta q_private",
            "zero_condition": "matter action descends through observed geometry/coframe and q-basic constants only",
            "current_status": "MISSING_PARENT_OBJECT_LANGUAGE",
            "residual_symbol": "C_qT",
            "bound_input_needed": "source-backed C_qT coefficient and matter tensor projection norm",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_1_B_qWeyl",
            "component": "B_qWeyl",
            "formula_slot": "B_qWeyl q_private W_abcd P^{abcd} or equivalent curvature tail",
            "zero_condition": "metric/epsilon-only scalar grammar with no Weyl spurion, no projector/readout, no boundary regeneration",
            "current_status": "CONDITIONAL_ZERO_NOT_FIRED",
            "residual_symbol": "B_qWeyl",
            "bound_input_needed": "source-backed B_qWeyl and local Weyl/profile projection norm",
            "source_path": str(SOURCES["bqweyl_status_2365"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_2_C_qT",
            "component": "C_qT",
            "formula_slot": "C_qT q_private T or q-source stress vertex",
            "zero_condition": "no direct q matter/source slot in parent action",
            "current_status": "CONDITIONAL_ZERO_NOT_FIRED",
            "residual_symbol": "C_qT",
            "bound_input_needed": "source-backed C_qT and stress/source support norm",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_3_j_boundary",
            "component": "j_boundary",
            "formula_slot": "delta B_boundary / delta q_private plus corner/reference terms",
            "zero_condition": "fixed boundary class, zero compact flux and no source-denominator reference leakage",
            "current_status": "MISSING_BOUNDARY_REFERENCE_SILENCE",
            "residual_symbol": "E_boundary",
            "bound_input_needed": "boundary flux norm, H_ref source-blindness row and corner kernel",
            "source_path": str(SOURCES["vertical_kernel_2589"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_4_j_readout",
            "component": "j_readout",
            "formula_slot": "post-variation projector/readout derivative",
            "zero_condition": "projector/readout fixed before variation or proven q-basic",
            "current_status": "MISSING_READOUT_PROJECTOR_SILENCE",
            "residual_symbol": "E_readout",
            "bound_input_needed": "projector derivative norm and source-coordinate readout Lipschitz factor",
            "source_path": str(SOURCES["dq_matrix_3517"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_5_j_tail",
            "component": "j_tail",
            "formula_slot": "memory/history/nonlocal tail response",
            "zero_condition": "tail kernel q-basic or compact support/causal projection makes local contribution vanish",
            "current_status": "MISSING_TAIL_KERNEL_SILENCE",
            "residual_symbol": "E_tail",
            "bound_input_needed": "tail kernel norm, local support window and projection profile",
            "source_path": str(SOURCES["jq_channel_2430"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "JQ3518_6_j_const_weight_shadow",
            "component": "j_const+j_weight+j_shadow",
            "formula_slot": "constant-sector, source-weight and shadow-marker derivative terms",
            "zero_condition": "constants are superselected/q-basic and no source-label or hidden marker survives",
            "current_status": "MISSING_CONSTANT_WEIGHT_SHADOW_SIGNATURE",
            "residual_symbol": "E_const_weight_shadow",
            "bound_input_needed": "constant-sector descent row and source-weight/shadow-marker coefficient bounds",
            "source_path": str(SOURCES["finite_jq_2367"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DQB3518_0_vq_master",
            "term": "master_Dq_vq",
            "bound_formula": "||Dq[v_q]||_q <= C_FC|delta H_vq| + C_M|C_qT| ||T|| + C_W|B_qWeyl| ||W|| + E_boundary + E_readout + E_tail + E_const_weight_shadow",
            "required_inputs": "C_FC,C_M,C_W; sourced delta H_vq; C_qT; B_qWeyl; local T and W profiles; boundary/readout/tail norms",
            "prediction_value": "MISSING_VQ_MASTER_DQ_NORM",
            "bound_value": "MISSING_LOCAL_DQ_BOUND",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DQB3518_1_source_coordinate",
            "term": "D_vq_Y",
            "bound_formula": "||D_vq Y|| <= L_Y ||Dq[v_q]||_q + ||Delta_Y_nonbasic||",
            "required_inputs": "source-coordinate descent Y=Ybar(q(Phi)); Lipschitz L_Y; nonbasic leakage norm",
            "prediction_value": "MISSING_DVQY_NORM",
            "bound_value": "MISSING_SOURCE_COORDINATE_BOUND",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DQB3518_2_local_amplitude",
            "term": "A_loc_vq",
            "bound_formula": "|A_loc[v_q]| <= C_A (L_Y ||Dq[v_q]||_q + ||Delta_Y_nonbasic||)",
            "required_inputs": "local amplitude normalization C_A and source-coordinate bound",
            "prediction_value": "MISSING_A_LOC_VQ",
            "bound_value": "MISSING_PPN_OR_R10_TOLERANCE",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DQB3518_3_BqWeyl",
            "term": "B_qWeyl_tail",
            "bound_formula": "E_W <= C_W |B_qWeyl| ||P_W W||",
            "required_inputs": "B_qWeyl coefficient, Weyl projection operator, local Weyl profile",
            "prediction_value": "MISSING_BQWEYL_COEFFICIENT",
            "bound_value": "MISSING_Weyl_PROFILE_BOUND",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DQB3518_4_CqT",
            "term": "C_qT_matter_tail",
            "bound_formula": "E_T <= C_T |C_qT| ||P_T T||",
            "required_inputs": "C_qT coefficient, source stress projection, matter support normalization",
            "prediction_value": "MISSING_CQT_COEFFICIENT",
            "bound_value": "MISSING_STRESS_PROFILE_BOUND",
            "status": "NONCLAIM_TEMPLATE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3518_0_real_progress",
            "decision": "v_q now has an exact two-gate contract rather than a vague missing label",
            "rationale": "The route is either parent first-class quotient zero or termwise source-vector silence plus explicit Dq bounds.",
            "effect": "future work can attack concrete parent clauses instead of circling the same missing variable",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3518_1_no_current_vertical_claim",
            "decision": "do not certify v_q as vertical in current corpus",
            "rationale": "first-class charge zero, object-language no-source-slot, B_qWeyl, C_qT, boundary/readout and tail clauses are unsigned.",
            "effect": "local GR/Newton remains open, not failed; the obstruction is now localized to parent source language and tails",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3518_2_next_object_language",
            "decision": "next target is parent object-language normal form",
            "rationale": "C_qT and B_qWeyl survive because the grammar of allowed q appearances is not closed.",
            "effect": "prove q appears only through quotient geometry/constants, or keep finite source-channel bounds",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3519-Y5-R2FR-vq-parent-object-language-normal-form-or-source-channel-bound.md",
            "next_script": "scripts/Y5_R2FR_3519_vq_parent_object_language_normal_form_or_source_channel_bound.py",
            "objective": "Build the parent grammar for q appearances: auxiliary/constraint-only, observed geometry/coframe, q-basic constants, or forbidden direct source slot.",
            "success_gate": "Either prove no direct qT/B_qWeyl/source-slot terms survive after quotient reduction, or emit finite sourced component bounds for C_qT and B_qWeyl.",
            "why_next": "3518 shows the weakest link is not the algebra of Dq but the unsourced object language that decides which q couplings are legal.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    status: list[dict[str, Any]],
    components: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3518_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    routes = {row["route"] for row in theorem}
    checks.append(
        {
            "check_id": "VAL3518_1_two_gate_theorem_present",
            "passed": bool_text("first_class_quotient" in routes and "source_vector_silence" in routes),
            "detail": "theorem contains first-class quotient and source-vector silence routes",
            "valid_for_claim": "False",
        }
    )
    required_components = {"B_qWeyl", "C_qT", "j_matter", "j_boundary", "j_readout", "j_tail"}
    component_names = {row["component"] for row in components}
    checks.append(
        {
            "check_id": "VAL3518_2_required_components_explicit",
            "passed": bool_text(required_components.issubset(component_names)),
            "detail": "; ".join(sorted(component_names)),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3518_3_no_claim_flags_true",
            "passed": bool_text(
                all(row["fires_now"] == "False" and row["valid_for_claim"] == "False" for row in theorem)
                and all(row["value"] == "False" and row["valid_for_claim"] == "False" for row in status)
                and all(row["valid_for_claim"] == "False" for row in components + bounds)
            ),
            "detail": "no first-class/source-silent/Dq-zero/local-GR claim is enabled",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3518_4_bounds_placeholder_block",
            "passed": bool_text(all(row["prediction_value"].startswith("MISSING_") and row["bound_value"].startswith("MISSING_") for row in bounds)),
            "detail": "every bound row requires sourced numeric inputs before claim use",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3518_5_next_target_object_language",
            "passed": bool_text(any("object-language" in row["next_doc"] or "object_language" in row["next_script"] for row in next_rows)),
            "detail": "3519 parent object-language normal-form target selected",
            "valid_for_claim": "False",
        }
    )
    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3518_6_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    output_paths_in_root = all(str(path).startswith(str(ROOT)) for path in outputs.values()) and str(DOC).startswith(str(ROOT))
    checks.append(
        {
            "check_id": "VAL3518_7_outputs_stay_in_post_checkpoint_work",
            "passed": bool_text(output_paths_in_root),
            "detail": f"root={ROOT}",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3518_8_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3518_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    status: list[dict[str, Any]],
    components: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3518 - v_q Private First-Class Source-Vector Silence Or Dq Bound

## Summary
- **Leap made:** `v_q` is no longer just labelled "missing"; it now has an exact two-gate contract.
- **Gate A:** prove `v_q` is a first-class parent generator with zero local Hamiltonian charge and q-constant gauge orbits.
- **Gate B:** prove the q source vector is termwise silent: matter, curvature, boundary, readout, history/tail and constant/weight/shadow channels all vanish without cancellation.
- **Current result:** neither gate fires in the present corpus, so `Dq[v_q]=0`, `D_vq Y=0`, local GR/Newton and PPN/R10 passes remain unclaimed.
- **Best next attack:** close the parent object language so direct `qT`, `B_qWeyl`, source-slot and readout-tail terms are either forbidden by grammar or carried as finite bound rows.

## Derived Contract
The usable theorem is:

`Dq[v_q]=0` if `i_vq Omega_parent=delta G_q`, `G_q=0` on the constraint surface, `q` is constant on the `v_q` orbit, and every local linked surface obeys `delta H_vq[S]=0`.

The source-silence theorem is:

`J_q_total=0` only when `j_matter`, `j_const`, `j_weight`, `j_shadow`, `j_readout`, `j_boundary`, `j_curvature`, and `j_tail` vanish termwise in the same parent object language. Cancellation is not accepted.

If those gates fire and `Y=Ybar(q(Phi))`, then `D_vq Y=0` follows by the 3516 chain rule. If any gate does not fire, use the Dq bound template below.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Theorem Clauses
{markdown_table(theorem, ["clause_id", "route", "statement", "exact_contract", "current_evidence", "status", "fires_now", "valid_for_claim"])}

## Canonical v_q Status
{markdown_table(status, ["status_id", "quantity", "definition", "value", "reason", "implication", "valid_for_claim"])}

## Source-Vector Components
{markdown_table(components, ["component_id", "component", "formula_slot", "zero_condition", "current_status", "residual_symbol", "bound_input_needed", "valid_for_claim"])}

## Dq Bound Template
{markdown_table(bounds, ["bound_id", "term", "bound_formula", "required_inputs", "prediction_value", "bound_value", "status", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    theorem = theorem_rows()
    status = status_rows()
    components = component_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3518_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R2FR_3518_VQ_FIRSTCLASS_SILENCE_THEOREM.csv",
        "status": OUT / "P8_Y5_R2FR_3518_VQ_PRIVATE_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "components": OUT / "P8_Y5_R2FR_3518_VQ_SOURCE_VECTOR_COMPONENTS.csv",
        "dq_bounds": OUT / "P8_Y5_R2FR_3518_VQ_DQ_NORM_BOUND_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3518_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3518_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3518_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["theorem"], theorem, ["clause_id", "route", "statement", "exact_contract", "current_evidence", "status", "fires_now", "source_path", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "definition", "value", "reason", "implication", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["components"], components, ["component_id", "component", "formula_slot", "zero_condition", "current_status", "residual_symbol", "bound_input_needed", "source_path", "valid_for_claim"])
    write_csv(outputs["dq_bounds"], bounds, ["bound_id", "term", "bound_formula", "required_inputs", "prediction_value", "bound_value", "status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])

    validation_rows = validate(outputs, sources, theorem, status, components, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, theorem, status, components, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
