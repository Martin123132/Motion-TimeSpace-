from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUT = OUT / "P8_Y5_R2FR_3134_QUOTIENT_MAP_INPUTS.csv"
ATTEMPT = OUT / "P8_Y5_R2FR_3134_QUOTIENT_MAP_ATTEMPT.csv"
REDUCTION = OUT / "P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv"
LEAKAGE = OUT / "P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"
GATE = OUT / "P8_Y5_R2FR_3134_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3134_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    candidate = ROOT / path_text
    if candidate.exists():
        return candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str, row_id_column: str) -> dict[str, str] | None:
    if not row_id:
        return None
    if row_id_column:
        for row in rows:
            if row.get(row_id_column, "") == row_id:
                return row
    for row in rows:
        if row_id in row.values():
            return row
    return None


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "pass", "passed", "yes", "1"}


def base_inputs() -> list[dict[str, Any]]:
    residual = "source-intake\\mts_residuals\\"
    parent = "source-intake\\parent-action\\"
    source_weight = "source-intake\\source-weight\\"
    wep = "source-intake\\wep-sources\\"
    beta = "source-intake\\beta-source\\docs\\"
    return [
        {
            "source_id": "SRC3134_0",
            "role": "3133_next",
            "source_file": residual + "P8_Y5_R2FR_3133_GATE.csv",
            "source_row_id": "AQPG3133_2",
            "row_id_column": "gate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "3133 handoff to parent quotient map or profile upgrade.",
        },
        {
            "source_id": "SRC3134_1",
            "role": "2970_parent_signature_verdict",
            "source_file": residual + "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
            "source_row_id": "SIG2970_8_verdict",
            "row_id_column": "signature_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "2970 parent signature verdict.",
        },
        {
            "source_id": "SRC3134_2",
            "role": "2970_q_object",
            "source_file": residual + "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
            "source_row_id": "SIG2970_1_q_object",
            "row_id_column": "signature_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "q object gate.",
        },
        {
            "source_id": "SRC3134_3",
            "role": "2970_vertical_kernel",
            "source_file": residual + "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
            "source_row_id": "SIG2970_2_vertical_kernel",
            "row_id_column": "signature_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "vertical generator in Dq kernel gate.",
        },
        {
            "source_id": "SRC3134_4",
            "role": "2970_q_basic_matter",
            "source_file": residual + "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
            "source_row_id": "SIG2970_6_basic_matter_action",
            "row_id_column": "signature_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "q-basic matter action gate.",
        },
        {
            "source_id": "SRC3134_5",
            "role": "2970_no_source_slot",
            "source_file": residual + "P8_Y5_R2FR_2970_PARENT_SIGNATURE_GATE.csv",
            "source_row_id": "SIG2970_7_no_source_slot",
            "row_id_column": "signature_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "no source-only slot gate.",
        },
        {
            "source_id": "SRC3134_6",
            "role": "2970_chain_rule",
            "source_file": residual + "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv",
            "source_row_id": "MAT2970_0_chain_rule",
            "row_id_column": "matter_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "conditional chain rule theorem.",
        },
        {
            "source_id": "SRC3134_7",
            "role": "2970_hilbert_current",
            "source_file": residual + "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv",
            "source_row_id": "MAT2970_4_Hilbert_current",
            "row_id_column": "matter_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "conditional Hilbert current uniqueness.",
        },
        {
            "source_id": "SRC3134_8",
            "role": "2970_matter_verdict",
            "source_file": residual + "P8_Y5_R2FR_2970_BASIC_MATTER_ACTION_AUDIT.csv",
            "source_row_id": "MAT2970_7_verdict",
            "row_id_column": "matter_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "q-basic matter action verdict.",
        },
        {
            "source_id": "SRC3134_9",
            "role": "2970_qmap_verdict",
            "source_file": residual + "P8_Y5_R2FR_2970_QMAP_KERNEL_AUDIT.csv",
            "source_row_id": "QMAP2970_6_verdict",
            "row_id_column": "qmap_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "Dq[v_Z]=0 branch verdict.",
        },
        {
            "source_id": "SRC3134_10",
            "role": "2970_leakage_total",
            "source_file": residual + "P8_Y5_R2FR_2970_FIRST_LEAKAGE_COEFFICIENT_ROWS_NONCLAIM.csv",
            "source_row_id": "COEF2970_9_total",
            "row_id_column": "coefficient_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "finite leakage coefficient total fallback.",
        },
        {
            "source_id": "SRC3134_11",
            "role": "2911_qmap",
            "source_file": parent + "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv",
            "source_row_id": "QMAP2911_7_verdict",
            "row_id_column": "qmap_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "q-map kernel attempt verdict.",
        },
        {
            "source_id": "SRC3134_12",
            "role": "2956_descent",
            "source_file": parent + "matter_pullback_descent_audit_2956_NOT_DERIVED.csv",
            "source_row_id": "DESC2956_7_verdict",
            "row_id_column": "descent_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "matter pullback descent verdict.",
        },
        {
            "source_id": "SRC3134_13",
            "role": "2986_certificate",
            "source_file": parent + "q_vX_action_descent_certificate_2986_NOT_SIGNED.csv",
            "source_row_id": "QVX2986_10_verdict",
            "row_id_column": "certificate_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "single q/v_X/action descent certificate verdict.",
        },
        {
            "source_id": "SRC3134_14",
            "role": "3101_conditional",
            "source_file": parent + "vertical_descent_cg_zero_theorem_3101_CONDITIONAL.csv",
            "source_row_id": "ZTH3101_2_variation_zero",
            "row_id_column": "step_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "conditional variation-zero theorem.",
        },
        {
            "source_id": "SRC3134_15",
            "role": "2711_closure",
            "source_file": source_weight + "AX1090_PARENT_OBJECT_EXPLICIT_CLOSURE_2711_NONCLAIM.csv",
            "source_row_id": "AX1090_0_LC_3",
            "row_id_column": "closure_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "explicit closure q/readout order.",
        },
        {
            "source_id": "SRC3134_16",
            "role": "2829_qbasic",
            "source_file": source_weight + "qbasic_no_source_prefactor_theorem_audit_2829_NONCLAIM.csv",
            "source_row_id": "THA2829_7_current_verdict",
            "row_id_column": "theorem_audit_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "q-basic/no-source-prefactor theorem verdict.",
        },
        {
            "source_id": "SRC3134_17",
            "role": "2676_measure",
            "source_file": wep + "action_scale_measure_owner_wip_nonclaim_2676.csv",
            "source_row_id": "OWN2676_4_verdict",
            "row_id_column": "audit_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "parent action-scale/measure/current owner verdict.",
        },
        {
            "source_id": "SRC3134_18",
            "role": "2677_grammar",
            "source_file": wep + "no_species_action_weight_object_language_wip_2677.csv",
            "source_row_id": "GRM2677_6_verdict",
            "row_id_column": "clause_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "no-species-action-weight grammar verdict.",
        },
        {
            "source_id": "SRC3134_19",
            "role": "2796_synthesis",
            "source_file": beta + "WEP_SIGNATURE_SYNTHESIS_OR_CLOSURE_2796_NONCLAIM.csv",
            "source_row_id": "SYN2796_8_verdict",
            "row_id_column": "synthesis_id",
            "required": "true",
            "valid_for_claim": "false",
            "notes": "MOMS synthesis verdict.",
        },
    ]


def load_sources(inputs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for input_row in inputs:
        path = source_path(str(input_row["source_file"]))
        row = find_row(read_csv(path), str(input_row["source_row_id"]), str(input_row["row_id_column"]))
        sources[str(input_row["role"])] = {
            "input": input_row,
            "path": path,
            "row": row,
            "exists": path.exists(),
            "found": row is not None,
        }
    return sources


def source_paths(sources: dict[str, dict[str, Any]], *roles: str) -> str:
    return ";".join(str(sources[role]["path"]) for role in roles)


def status_of(sources: dict[str, dict[str, Any]], role: str) -> str:
    row = sources.get(role, {}).get("row") or {}
    for key in ("current_status", "status", "current_result", "signature_status", "result"):
        if row.get(key):
            return str(row[key])
    return ""


def quotient_attempt_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "row_id": "QMP3134_0",
            "object": "candidate_parent_chart",
            "candidate_definition": "Conf_parent contains observed coframe/metric/connection, ordinary matter bundles Psi_A, representation constants theta_A, MTS vertical variables Z/Xhat/domain-memory-boundary data, and admissible source/worldtube/boundary classes.",
            "derived_statement": "This is the minimal chart needed to state the quotient theorem without hiding source/readout/boundary channels.",
            "status": "explicit_candidate_chart_written",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "AX1090_PARENT_OBJECT_REMAINS_CLOSURE;FIELD_CHART_NOT_DERIVED_FROM_PRIMITIVES",
            "next_action": "derive Conf_parent from primitive MTS action grammar or retain AX1090_0_LC label",
            "source_paths": source_paths(sources, "2711_closure", "2970_parent_signature_verdict"),
            "generated_utc": now,
        },
        {
            "row_id": "QMP3134_1",
            "object": "candidate_quotient_map_q",
            "candidate_definition": "q: Conf_parent -> Q_obs maps Phi to (e_obs,g_obs,omega_obs,A_obs,mu_obs,tau_obs,theta_rep,boundary_class_obs) and forgets only representative vertical data.",
            "derived_statement": "Observed geometry/readout must be q-basic before variation; q cannot be chosen after fitting to erase a residual.",
            "status": "formal_map_declared_not_parent_owned",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "Q_OBJECT_NOT_PARENT_SIGNED;Q_BY_DECLARATION_REFUSED",
            "next_action": "construct q from parent equations/domain equivalence relation, not from post-readout projection",
            "source_paths": source_paths(sources, "2970_q_object", "2911_qmap", "2711_closure"),
            "generated_utc": now,
        },
        {
            "row_id": "QMP3134_2",
            "object": "vertical_generator_kernel",
            "candidate_definition": "v_X is vertical iff Dq[v_X]=0 for every observed geometry, source-current, boundary/support, and readout component on an open local branch.",
            "derived_statement": "Pointwise or after-solve verticality is not enough; the open-branch kernel and q/v norms must be owned.",
            "status": "kernel_condition_exact_but_not_signed",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "OPEN_BRANCH_DQ_KERNEL_UNSIGNED;DQ_NORM_MISSING;SOURCE_AND_BOUNDARY_COMPONENTS_NOT_ZERO",
            "next_action": "prove Dq[v_X]=0 componentwise or carry finite Dq leakage coefficients",
            "source_paths": source_paths(sources, "2970_vertical_kernel", "2970_qmap_verdict", "2986_certificate"),
            "generated_utc": now,
        },
        {
            "row_id": "QMP3134_3",
            "object": "q_basic_matter_pullback",
            "candidate_definition": "S_matter[Phi,Psi;theta]=Sbar[q(Phi),Psi,theta] with theta representation data fixed or q-pulled back.",
            "derived_statement": "delta_v S_matter = (delta Sbar/delta q)Dq[v] + (partial Sbar/partial theta)Lie_v(theta); this vanishes if Dq[v]=0 and Lie_v(theta)=0.",
            "status": "chain_rule_proved_conditionally",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "MATTER_FUNCTOR_DOMAIN_UNSIGNED;CONSTANT_MARKER_SILENCE_UNSIGNED",
            "next_action": "turn the chain-rule theorem into a parent-owned matter functor, not a closure assumption",
            "source_paths": source_paths(sources, "2970_chain_rule", "2956_descent", "3101_conditional"),
            "generated_utc": now,
        },
        {
            "row_id": "QMP3134_4",
            "object": "no_source_only_slot",
            "candidate_definition": "ordinary matter grammar excludes independent source-only weights w_A(Z), source prefactors, hidden current bypasses, and post-quotient spurions.",
            "derived_statement": "Without this grammar, S_matter=sum_A w_A S_A is a legal pre-variation countermodel and the quotient zero does not prove WEP/source silence.",
            "status": "countermodel_guard_live",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "NO_SOURCE_ONLY_SLOT_NOT_PARENT_SIGNED;ACTION_MEASURE_OWNER_UNSIGNED;SPECIES_WEIGHT_COUNTERMODEL_LIVE",
            "next_action": "derive action-scale/measure/current owner or keep J_spurion/J_direct finite rows",
            "source_paths": source_paths(sources, "2970_no_source_slot", "2829_qbasic", "2676_measure", "2677_grammar"),
            "generated_utc": now,
        },
        {
            "row_id": "QMP3134_5",
            "object": "3134_quotient_map_verdict",
            "candidate_definition": "The quotient theorem is now explicit enough to be audited: the algebra closes, but parent ownership does not.",
            "derived_statement": "qbar_XT/source-current zero is conditional only; finite Dq/J leakage heads remain mandatory until the parent signature closes.",
            "status": "conditional_theorem_sharp_finite_leakage_active",
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PARENT_SIGNATURE_NOT_DERIVED;FINITE_LEAKAGE_CARRY_FORWARD_REQUIRED",
            "next_action": "3135 should attack no-source-only-slot/action-measure owner or fill first finite leakage bound row",
            "source_paths": source_paths(sources, "2970_parent_signature_verdict", "2970_matter_verdict", "2796_synthesis", "3133_next"),
            "generated_utc": now,
        },
    ]


def reduction_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "row_id": "RED3134_0",
            "clause": "chain_rule_variation",
            "proof_status": "formal_pass_conditional",
            "mathematical_result": "delta_v Sbar[q(Phi),Psi,theta] = S_,q Dq[v] + S_,theta Lie_v(theta)",
            "what_is_proven_now": "If Dq[v]=0 and theta is vertical-silent, the matter variation vanishes.",
            "what_is_not_proven": "That current MTS owns q, v, theta silence, and the matter functor.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2970_chain_rule", "2956_descent", "3101_conditional"),
            "generated_utc": now,
        },
        {
            "row_id": "RED3134_1",
            "clause": "Hilbert_current_uniqueness",
            "proof_status": "subtheorem_pass_conditional",
            "mathematical_result": "For one fixed common S_matter varied before readout, T_H is unique and post-variation material rescaling is illegal.",
            "what_is_proven_now": "Post-variation source-selector tricks are blocked.",
            "what_is_not_proven": "Pre-action species/source weights and species measure Jacobians are excluded.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2970_hilbert_current", "2676_measure"),
            "generated_utc": now,
        },
        {
            "row_id": "RED3134_2",
            "clause": "q_object_and_kernel",
            "proof_status": "fail_current_claim",
            "mathematical_result": "Dq[v_X]=0 is the exact condition needed for quotient silence.",
            "what_is_proven_now": "The necessary kernel condition is sharp and componentized.",
            "what_is_not_proven": "q object, open-branch verticality, q/v norms, source current, and boundary support components.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2970_q_object", "2970_vertical_kernel", "2911_qmap"),
            "generated_utc": now,
        },
        {
            "row_id": "RED3134_3",
            "clause": "q_basic_matter_functor",
            "proof_status": "fail_current_claim",
            "mathematical_result": "Ordinary matter must be a functor over Q_obs with no direct Z/source argument.",
            "what_is_proven_now": "The exact functor target is known.",
            "what_is_not_proven": "Parent matter bundle domain, constant/marker silence, no-shadow frame, boundary/worldtube owner.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2970_q_basic_matter", "2956_descent", "2986_certificate"),
            "generated_utc": now,
        },
        {
            "row_id": "RED3134_4",
            "clause": "no_source_only_slot",
            "proof_status": "fail_current_claim",
            "mathematical_result": "A connected parent ordinary-matter grammar would forbid independent w_A(Z)S_A source weights.",
            "what_is_proven_now": "The countermodel and the needed grammar are explicit.",
            "what_is_not_proven": "Action measure/current owner, species-blind measure, source-label forgetting, boundary/domain no-reentry.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2970_no_source_slot", "2829_qbasic", "2677_grammar"),
            "generated_utc": now,
        },
        {
            "row_id": "RED3134_5",
            "clause": "local_GR_implication",
            "proof_status": "not_reached",
            "mathematical_result": "If all quotient/matter/no-source clauses closed, this would remove a WEP/source coupling branch; it would still not prove full GR/Newton by itself.",
            "what_is_proven_now": "A coupling branch can be structurally isolated.",
            "what_is_not_proven": "EH fixed point, Newtonian source normalization, PPN stability, boundary flux silence, and empirical arena projections.",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_paths(sources, "2711_closure", "2970_parent_signature_verdict"),
            "generated_utc": now,
        },
    ]


def leakage_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    leakage_path = sources["2970_leakage_total"]["path"]
    source_rows = read_csv(leakage_path)
    now = stamp()
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        rows.append(
            {
                "row_id": "QLEAK3134_" + row.get("coefficient_id", ""),
                "source_coefficient_id": row.get("coefficient_id", ""),
                "symbol": row.get("symbol", ""),
                "definition": row.get("definition", ""),
                "units": row.get("units", ""),
                "bound_interface": row.get("bound_interface", ""),
                "candidate_value": row.get("candidate_value", ""),
                "current_status": "carried_forward_nonclaim",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "reason": "3134 quotient proof did not parent-sign this leakage head",
                "next_action": "theorem-zero this head or provide a source-backed upper bound",
                "source_paths": str(leakage_path),
                "generated_utc": now,
            }
        )
    return rows


def gate_rows(attempts: list[dict[str, Any]], reductions: list[dict[str, Any]], leaks: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    failed_reductions = [row["clause"] for row in reductions if row["proof_status"] in {"fail_current_claim", "not_reached"}]
    leakage_symbols = [row["symbol"] for row in leaks if row["symbol"]]
    return [
        {
            "gate_id": "QMG3134_0",
            "gate": "quotient_map_parent_signature",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "q and v_X in ker(Dq) are exactly specified but not parent-signed on an open local branch.",
            "failed_or_open_clauses": ";".join(failed_reductions),
            "leakage_heads": ";".join(leakage_symbols),
            "next_action": "derive q object/open-branch kernel or fill eps_q_parent/Dq leakage heads",
            "source_paths": source_paths(sources, "2970_parent_signature_verdict", "2970_qmap_verdict"),
        },
        {
            "gate_id": "QMG3134_1",
            "gate": "matter_pullback_chain_rule",
            "status": "formal_pass_but_parent_unsigned",
            "claim_allowed": "false",
            "reason": "The chain-rule theorem is valid, but parent-owned matter functor/no-source-slot clauses are not signed.",
            "failed_or_open_clauses": "q_basic_matter_functor;no_source_only_slot",
            "leakage_heads": "J_direct;J_spurion;J_nonH",
            "next_action": "attack action-measure/current owner or finite J leakage rows",
            "source_paths": source_paths(sources, "2970_chain_rule", "2970_matter_verdict", "2829_qbasic"),
        },
        {
            "gate_id": "QMG3134_2",
            "gate": "finite_leakage_fallback",
            "status": "active_nonclaim",
            "claim_allowed": "false",
            "reason": "First leakage coefficient heads from 2970 remain the executable fallback.",
            "failed_or_open_clauses": ";".join(failed_reductions),
            "leakage_heads": ";".join(leakage_symbols),
            "next_action": "3135 should either prove no-source-only-slot/action-measure owner or fill first finite leakage bound row",
            "source_paths": source_paths(sources, "2970_leakage_total"),
        },
    ]


def validate(
    inputs: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    attempts: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_columns = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    input_columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required_columns if column not in input_columns]
    unresolved = [role for role, payload in sources.items() if not payload["exists"] or not payload["found"]]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    parent_signed_leaks = [row.get("row_id", "") for row in attempts if str(row.get("parent_signed", "")).lower() == "true"]
    claim_leaks = [
        row.get("row_id", "")
        for row in [*attempts, *reductions, *leaks]
        if str(row.get("claim_allowed", "")).lower() != "false"
        or str(row.get("valid_for_claim", "")).lower() != "false"
    ]
    formal_passes = [row for row in reductions if row["proof_status"].startswith("formal_pass") or row["proof_status"].startswith("subtheorem_pass")]
    failures = [row for row in reductions if row["proof_status"] in {"fail_current_claim", "not_reached"}]
    return [
        {
            "check_id": "VAL3134_0_input_schema",
            "status": "pass" if not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3134_1_source_rows_resolve",
            "status": "pass" if not unresolved else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3134_2_no_parent_signature_promotion",
            "status": "pass" if not parent_signed_leaks else "fail",
            "details": ";".join(parent_signed_leaks),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3134_3_formal_and_failed_clauses_both_present",
            "status": "pass" if formal_passes and failures else "fail",
            "details": json.dumps({"formal_passes": len(formal_passes), "failures": len(failures)}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3134_4_leakage_heads_carried_forward",
            "status": "pass" if len(leaks) >= 10 else "fail",
            "details": str(len(leaks)),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3134_5_no_claim_leak",
            "status": "pass" if not claim_leaks else "fail",
            "details": ";".join(claim_leaks),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def main() -> None:
    inputs = base_inputs()
    write_csv(INPUT, inputs)
    sources = load_sources(inputs)
    attempts = quotient_attempt_rows(sources)
    reductions = reduction_rows(sources)
    leaks = leakage_rows(sources)
    gates = gate_rows(attempts, reductions, leaks, sources)
    validations = validate(inputs, sources, attempts, reductions, leaks)
    write_csv(ATTEMPT, attempts)
    write_csv(REDUCTION, reductions)
    write_csv(LEAKAGE, leaks)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)
    pycache = Path(__file__).with_name("__pycache__")
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
