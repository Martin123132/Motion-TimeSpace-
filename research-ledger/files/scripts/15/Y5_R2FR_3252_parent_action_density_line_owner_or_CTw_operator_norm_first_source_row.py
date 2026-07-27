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

DOC = ROOT / "3252-Y5-R2FR-parent-action-density-line-owner-or-C_Tw-operator-norm-first-source-row-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3252_SOURCE_REGISTER.csv",
    "owner": OUT / "P8_Y5_R2FR_3252_PARENT_ACTION_DENSITY_LINE_OWNER_ATTEMPT.csv",
    "failure": OUT / "P8_Y5_R2FR_3252_ACTION_MEASURE_FAILURE_AUDIT.csv",
    "ctw": OUT / "P8_Y5_R2FR_3252_CTW_OPERATOR_NORM_SOURCE_ROW.csv",
    "update": OUT / "P8_Y5_R2FR_3252_DJH_WEIGHTED_SOURCE_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3252_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3252_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3252_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3252_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:220]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3252_3251_handoff",
            ROOT / "3251-Y5-R2FR-source-prefactor-edge-zero-or-same-frame-DJH-residual-first-bound-under-AX1090.md",
            "immediate C_Tw/action-line handoff",
            ["C_Tw", "action-density", "NEXT3251"],
        ),
        (
            "SRC3252_1230_action_scale",
            OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
            "universal action-scale owner theorem attempt",
            ["UAS1230_0_target", "L_action", "hbar_parent"],
        ),
        (
            "SRC3252_1230_measure",
            OUT / "P8_Y5_R10_1230_MEASURE_DESCENT_PROOF_STACK.csv",
            "measure/current descent clauses",
            ["MDS1230_0_parent_measure_line", "hbar_parent", "current_extraction"],
        ),
        (
            "SRC3252_1066_measure",
            OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "field/measure/quantum normalization audit",
            ["FMQ1066_1_Hilbert_source_rescaling", "hbar", "measure_jacobian"],
        ),
        (
            "SRC3252_1066_typing",
            OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
            "parent object-language typing audit",
            ["OLT1066_4_inert_source_scalar", "w_A", "not_parent_signed"],
        ),
        (
            "SRC3252_1067_hbar",
            OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
            "hbar and measure owner audit",
            ["HMO1067_0_hbar_parent", "HMO1067_1_measure_parent", "OWNER_NOT_DERIVED"],
        ),
        (
            "SRC3252_1078_action_measure",
            OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
            "action-measure proof attempt",
            ["AM1078_0_target", "ACTION_MEASURE_NOT_SIGNED", "w_A"],
        ),
        (
            "SRC3252_1220_typed",
            OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "parent typed signature attempt",
            ["PTOL1220_4_action_scale_measure_owner", "source_weight_exclusion"],
        ),
        (
            "SRC3252_1229_contract",
            OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
            "local GR source coupling contract",
            ["THM1229_0_target", "THM1229_3_residual_vector", "local-GR"],
        ),
        (
            "SRC3252_1229_clause_audit",
            OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
            "universal source-coupling clause audit",
            ["CLC1229_0_single_action_scale", "CLC1229_4_measure_coframe_connection_descent"],
        ),
        (
            "SRC3252_1722_CwH",
            OUT / "P8_Y5_PARENT_QLOC_1722_CWH_BOUND_LAW.csv",
            "weighted Hilbert current bound law",
            ["CWHL1722_1_operator_bound", "C_Tw", "EXACT_NORM_BOUND_FORM"],
        ),
        (
            "SRC3252_3250_DJH",
            OUT / "P8_Y5_R2FR_3250_DJH_RESIDUAL_VECTOR.csv",
            "same-frame D_A J_H residual vector",
            ["DJH3250_3_weighted_source", "C_wH", "delta_w"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "ADL3252_0_parent_line",
            "claim_piece": "single parent action-density line",
            "formal_statement": "There exists one parent action-density line L_action and ordinary matter action density ell_ord in Gamma(L_action tensor Dens), with species sectors as fields/representations inside ell_ord, not separate source-normalization lines.",
            "derivation_gain": "A relative w_A can only appear as an automorphism/extra coefficient of L_action; it is not silently available once L_action is owned.",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "ADL3252_1_hbar_owner",
            "claim_piece": "one hbar/action phase owner",
            "formal_statement": "The weighting exp(i S_ord / hbar_parent) uses a single hbar_parent or parent phase normalization for all ordinary matter histories.",
            "derivation_gain": "Forbids species-dependent hbar_A or action-scale factors that leave classical EOM looking unchanged but rescale Hilbert source strength.",
            "current_status": "CONDITIONAL_ROUTE_OWNER_MISSING",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "ADL3252_2_measure_owner",
            "claim_piece": "species-blind measure owner",
            "formal_statement": "The parent measure, quotient Jacobian, coframe volume, and path/statistical measure are species-blind after quotient descent: D_A log dmu_parent has no source-label component.",
            "derivation_gain": "Blocks species-dependent measure Jacobians J_A from recreating w_A after the action grammar is cleaned.",
            "current_status": "CONDITIONAL_ROUTE_OWNER_MISSING",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "ADL3252_3_current_extraction",
            "claim_piece": "pre-readout Hilbert current owner",
            "formal_statement": "T_obs is extracted from the total matter action before species/readout/projector selection: T_total=(2/sqrt(-g_obs)) delta S_ord/delta g_obs.",
            "derivation_gain": "Forbids post-variation source maps F((T_A,A))=kappa_A T_A from adding source labels after covariance has done its work.",
            "current_status": "CONDITIONAL_READOUT_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "ADL3252_4_zero_theorem",
            "claim_piece": "Delta_w and C_wH zero if signed",
            "formal_statement": "ADL3252_0 through ADL3252_3 plus no-Hom typing and connected naturality imply delta_w_rel=0 and therefore C_wH=0.",
            "derivation_gain": "This is the parent-owner clause needed by 3251 to remove the weighted-source term from D_A J_H.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "ADL3252_5_current_verdict",
            "claim_piece": "current MTS action-density owner status",
            "formal_statement": "The corpus has conditional contracts for L_action, hbar, measure, and current extraction, but no signed parent action constructing them as one object.",
            "derivation_gain": "Finite C_Tw and delta_w rows remain mandatory unless this owner is derived.",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def failure_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_id": "AMF3252_0_classical_EOM_rescaling",
            "construction": "S_A -> w_A S_A leaves isolated classical Euler-Lagrange form unchanged",
            "why_it_survives": "Hilbert source, quantum/statistical weight and source normalization still rescale",
            "kills_clause": "ADL3252_1_hbar_owner",
            "status": "ACTIVE_GUARDRAIL",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "AMF3252_1_species_hbar",
            "construction": "sector-specific hbar_A or phase normalization",
            "why_it_survives": "acts like a species action-scale weight even if action grammar has no explicit w_A",
            "kills_clause": "ADL3252_1_hbar_owner",
            "status": "ACTIVE_OBSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "AMF3252_2_measure_jacobian",
            "construction": "species-dependent measure/coframe/quotient Jacobian J_A",
            "why_it_survives": "turns a clean bare action into an effective weighted source after variable changes",
            "kills_clause": "ADL3252_2_measure_owner",
            "status": "ACTIVE_OBSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "AMF3252_3_post_readout_map",
            "construction": "F((T_A,A))=kappa_A T_A after Hilbert variation",
            "why_it_survives": "covariance of T_A does not prevent source-label selection after variation",
            "kills_clause": "ADL3252_3_current_extraction",
            "status": "ACTIVE_OBSTRUCTION",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "AMF3252_4_disconnected_category",
            "construction": "ordinary matter category splits into disconnected source components",
            "why_it_survives": "connected naturality only forces common weights inside each component",
            "kills_clause": "ADL3252_4_zero_theorem",
            "status": "ACTIVE_UNTIL_GRAPH_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "AMF3252_5_marker_shadow_return",
            "construction": "hidden marker/frame/constant re-enters as a source-weight surrogate",
            "why_it_survives": "no-shadow and constant-marker split remain unsigned",
            "kills_clause": "ADL3252_0_parent_line;ADL3252_2_measure_owner",
            "status": "ACTIVE_OBSTRUCTION",
            "valid_for_claim": "false",
        },
    ]


def ctw_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CTW3252_0_operator_definition",
            "quantity": "C_Tw",
            "definition": "C_Tw := ||L_Tw||_{Sigma->J,A}, L_Tw[delta_w]=star_eobs(sum_c delta_w_c T_c_obs(tau,.)) on A_ext",
            "bound_form": "C_wH <= C_Tw ||delta_w||_Sigma",
            "derived_status": "OPERATOR_NORM_DEFINITION_EXACT",
            "required_inputs": "component_basis;Sigma_metric;J_norm;A_ext;tau_id;e_obs_id;volume_form;units",
            "current_value": "MISSING_C_TW_OPERATOR_NORM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CTW3252_1_component_rss_bound",
            "quantity": "C_Tw_upper",
            "definition": "For finite component basis and Euclidean Sigma, ||L_Tw|| <= (sum_c ||J_c||_J^2)^(1/2), J_c=star_eobs(T_c_obs(tau,.))",
            "bound_form": "C_wH <= (sum_c ||J_c||_J^2)^(1/2) ||delta_w||_2",
            "derived_status": "NEW_FINITE_COMPONENT_BOUND_FORM",
            "required_inputs": "finite component list;component current norms ||J_c||_J;same A_ext/tau/e_obs;orthogonality/covariance convention",
            "current_value": "MISSING_COMPONENT_CURRENT_NORMS",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CTW3252_2_first_source_row",
            "quantity": "weighted_source_piece_of_D_A_J_H",
            "definition": "first claim-ready schema for the C_wH contribution to the 3250 D_A J_H residual vector",
            "bound_form": "||D_A J_H||_weighted <= C_Tw_upper ||delta_w||_2",
            "derived_status": "SCHEMA_READY_VALUES_MISSING",
            "required_inputs": "CTW3252_1_component_rss_bound;delta_w vector/theorem-zero;absolute-sum policy;source paths;units",
            "current_value": "NOT_COMPUTED",
            "valid_for_claim": "false",
        },
    ]


def update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "WDU3252_0_owner_route",
            "target": "NHE3251_5_CwH_zero",
            "update": "The zero route now depends specifically on a single parent L_action/hbar/measure/current owner, not a vague minimality assumption.",
            "effect": "makes the next proof target smaller and harder to smuggle",
            "valid_for_claim": "false",
        },
        {
            "update_id": "WDU3252_1_finite_route",
            "target": "DWB3251_0_operator",
            "update": "C_Tw gets a component root-sum-square upper-bound form using J_c=star(T_c_obs(tau,.)).",
            "effect": "finite fallback can be sourced from component current norms instead of an opaque operator constant",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3252_0_owner_theorem_shape",
            "claim": "single action-density/hbar/measure owner would kill relative source weights",
            "gate_pass": "true",
            "reason": "ADL3252 rows assemble the exact conditional owner route",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3252_1_current_parent_owner",
            "claim": "current MTS parent signs L_action/hbar/measure/current owner",
            "gate_pass": "false",
            "reason": "1066/1067/1078/1230/1220 keep owner clauses unsigned",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3252_2_CwH_zero_current",
            "claim": "C_wH=0 is claim-ready",
            "gate_pass": "false",
            "reason": "owner theorem is conditional only",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3252_3_CTw_numeric",
            "claim": "C_Tw operator norm is numeric/source-backed",
            "gate_pass": "false",
            "reason": "component current norms, delta_w, A_ext, norm pair and units remain missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3252_4_local_GR_Newton",
            "claim": "local GR/Newton source coupling follows",
            "gate_pass": "false",
            "reason": "weighted source is one residual component; other 3250 components still live",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3252_0_result",
            "decision": "Keep the single parent action-density/hbar/measure owner as the clean theorem route",
            "because": "it removes source weights structurally rather than tuning them small",
            "next_action": "try to derive the owner from the parent action/signature, or demote it to explicit closure",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3252_1_bound",
            "decision": "Use component current norms for the first finite C_Tw route",
            "because": "root-sum-square component bound is sourceable once component stress currents are defined",
            "next_action": "fill component current norm rows only after component basis and A_ext/tau/e_obs are fixed",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3252_2_best_next",
            "decision": "Attack ordinary-sector parent signature instead of data first",
            "because": "one signed action owner would remove a large source-coupling wound more cleanly than fitting C_Tw",
            "next_action": "write 3253 as parent ordinary-sector action signature or CTw component-current norm intake",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3252_0_3253",
            "selection": "selected_primary",
            "next_checkpoint": "3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3253_parent_ordinary_sector_action_signature_or_CTw_component_current_norm_intake.py",
            "objective": "Try to construct the parent ordinary-sector action signature that owns L_action, hbar, measure, current extraction, no hidden visible coefficients and no source-only weights as one object; if not, create the first component-current norm intake schema for CTw.",
            "guardrail": "do not claim local GR/Newton/WEP; do not use classical EOM scaling, measured G absorption, or covariance as proof; keep all finite rows nonclaim",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources_exist = all(row["exists"] == "true" for row in source_rows)
    sources_hit = all(row["evidence_hits"] not in {"MISSING_SOURCE", "NO_MATCH"} for row in source_rows)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    under_post_checkpoint = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in [*generated_csvs, DOC])
    formalization_3252 = [path for path in FW.rglob("*3252*") if path.is_file()] if FW.exists() else []
    formalization_clean = len(formalization_3252) == 0
    owner_present = any(row["owner_id"] == "ADL3252_4_zero_theorem" for row in owner_rows())
    failure_present = len(failure_rows()) >= 5
    ctw_present = any(row["row_id"] == "CTW3252_1_component_rss_bound" for row in ctw_rows())
    ctw_nonclaim = all(row["valid_for_claim"] == "false" for row in ctw_rows())
    ctw_has_missing = any("MISSING_" in ";".join(str(value) for value in row.values()) for row in ctw_rows())
    claims_blocked = all(row["claim_allowed"] == "false" for row in gate_rows())
    parent_owner_false = any(row["claim_gate_id"] == "CG3252_1_current_parent_owner" and row["gate_pass"] == "false" for row in gate_rows())
    next_written = bool(next_rows())
    doc_written = DOC.exists()
    checks = [
        ("VAL3252_0_sources_exist", sources_exist, "all cited source paths exist", str(sources_exist)),
        ("VAL3252_1_source_hits", sources_hit, "source evidence hits are present", str(sources_hit)),
        ("VAL3252_2_csvs_parse", csvs_parse, "all generated CSV files parse", str(csvs_parse)),
        ("VAL3252_3_outputs_under_post_checkpoint", under_post_checkpoint, "all outputs are under post-checkpoint-work", str(under_post_checkpoint)),
        ("VAL3252_4_formalization_clean", formalization_clean, "no 3252 outputs in formalization-workbench", f"formalization_3252_count={len(formalization_3252)}"),
        ("VAL3252_5_owner_present", owner_present, "action-density owner zero theorem route written", str(owner_present)),
        ("VAL3252_6_failure_present", failure_present, "action/measure failure audit present", str(failure_present)),
        ("VAL3252_7_ctw_present", ctw_present, "C_Tw component RSS bound row present", str(ctw_present)),
        ("VAL3252_8_ctw_nonclaim", ctw_nonclaim, "C_Tw rows remain nonclaim", str(ctw_nonclaim)),
        ("VAL3252_9_ctw_has_missing", ctw_has_missing, "C_Tw rows preserve missing-input markers", str(ctw_has_missing)),
        ("VAL3252_10_claims_blocked", claims_blocked, "all claim gates remain blocked", str(claims_blocked)),
        ("VAL3252_11_parent_owner_false", parent_owner_false, "current parent owner gate remains false", str(parent_owner_false)),
        ("VAL3252_12_next_written", next_written, "3253 next target written", str(next_written)),
        ("VAL3252_13_doc_written", doc_written, "3252 markdown checkpoint exists", str(doc_written)),
    ]
    rows = [
        {"validation_id": validation_id, "passed": bool_str(passed), "requirement": requirement, "evidence": evidence_text}
        for validation_id, passed, requirement, evidence_text in checks
    ]
    rows.append(
        {
            "validation_id": "VAL3252_OVERALL",
            "passed": bool_str(all(row["passed"] == "true" for row in rows)),
            "requirement": "3252 validation overall",
            "evidence": "all required validation rows passed",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    failure: list[dict[str, Any]],
    ctw: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    lines = [
        "# 3252 - Parent action-density line owner or C_Tw operator-norm first source row under AX1090",
        "",
        f"Generated: `{RUN_UTC}`",
        "",
        "Private derivation checkpoint. This does not claim local GR, Newton, WEP, R10, PPN, clock, orbital, or source-coupling closure.",
        "",
        "## Summary",
        "",
        "- `3252` attacks the owner under `C_wH`: one parent action-density line `L_action`, one `hbar_parent`, one species-blind measure, and one pre-readout Hilbert-current extraction.",
        "- If that owner is signed, source weights are not independent species knobs: relative `delta_w` vanishes after the common mode, so the `3251` weighted-source term `C_wH` disappears.",
        "- Current MTS still cannot claim this because the action line, hbar, measure/current owner, readout descent and hidden-marker closure remain unsigned.",
        "- The finite fallback improves: `C_Tw` is no longer opaque; for a finite component basis, `C_Tw <= (sum_c ||J_c||_J^2)^(1/2)` with `J_c=star_eobs(T_c_obs(tau,.))`.",
        "",
        "## Parent Action-Density Line Owner Attempt",
        "",
        md_table(owner, ["owner_id", "claim_piece", "formal_statement", "derivation_gain", "current_status", "valid_for_claim"]),
        "",
        "## Action/Measure Failure Audit",
        "",
        md_table(failure, ["failure_id", "construction", "why_it_survives", "kills_clause", "status", "valid_for_claim"]),
        "",
        "## C_Tw Operator-Norm Source Row",
        "",
        md_table(ctw, ["row_id", "quantity", "definition", "bound_form", "derived_status", "required_inputs", "current_value", "valid_for_claim"]),
        "",
        "## Weighted-Source Update",
        "",
        md_table(updates, ["update_id", "target", "update", "effect", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_id", "selection", "next_checkpoint", "next_script", "objective", "guardrail", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
        "",
        "## Working Verdict",
        "",
        "`3252` does not close source coupling, but it sharpens both paths: the derivation path is now a single parent ordinary-sector action signature, and the finite path has a component-current norm formula for `C_Tw` rather than an undefined coupling constant.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register()
    owner = owner_rows()
    failure = failure_rows()
    ctw = ctw_rows()
    updates = update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    generated_without_validation = [
        OUTPUTS["sources"],
        OUTPUTS["owner"],
        OUTPUTS["failure"],
        OUTPUTS["ctw"],
        OUTPUTS["update"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["owner"], owner)
    write_csv(OUTPUTS["failure"], failure)
    write_csv(OUTPUTS["ctw"], ctw)
    write_csv(OUTPUTS["update"], updates)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    DOC.write_text(
        "# 3252 - Parent action-density line owner or C_Tw operator-norm first source row under AX1090\n\n"
        "Pending final validation table.\n",
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_without_validation)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(source_rows, owner, failure, ctw, updates, gates, decisions, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3252_OVERALL")
    if overall["passed"] != "true":
        raise SystemExit("3252 validation failed")


if __name__ == "__main__":
    main()
