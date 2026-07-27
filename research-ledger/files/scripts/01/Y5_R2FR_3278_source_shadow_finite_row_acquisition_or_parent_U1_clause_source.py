from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3278-Y5-R2FR-source-shadow-finite-row-acquisition-or-parent-U1-clause-source-under-AX1090.md"

SRC_3276_DOC = ROOT / "3276-Y5-R2FR-minimal-covariant-derivative-domain-or-first-source-shadow-coefficient-under-AX1090.md"
SRC_3276_SPLIT = OUT / "P8_Y5_R2FR_3276_AQ_DOMAIN_SPLIT_THEOREM.csv"
SRC_3276_MAG = OUT / "P8_Y5_R2FR_3276_F_ONLY_MAGNETIZATION_CURRENT_LEMMA.csv"
SRC_3276_GAUGE = OUT / "P8_Y5_R2FR_3276_NONCONSERVED_COMPENSATOR_GAUGE_REJECTION.csv"
SRC_3276_SHADOW = OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_3277_DOC = ROOT / "3277-Y5-R2FR-parent-exact-U1-representation-signature-or-source-shadow-data-intake-under-AX1090.md"
SRC_3277_SIG = OUT / "P8_Y5_R2FR_3277_EXACT_U1_PARENT_SIGNATURE_AUDIT.csv"
SRC_3277_THEOREM = OUT / "P8_Y5_R2FR_3277_REPRESENTATION_CURRENT_THEOREM.csv"
SRC_3277_INTAKE = OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_INTAKE_ROWS_NONCLAIM.csv"
SRC_3277_RUNNER = OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_BOUND_RUNNER_NONCLAIM.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_1815_NO_RESCALE = OUT / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"
SRC_2508_PROOF = OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
SRC_2616_SHADOW = OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3278_SOURCE_REGISTER.csv",
    "target": OUT / "P8_Y5_R2FR_3278_TARGET_SELECTION.csv",
    "clauses": OUT / "P8_Y5_R2FR_3278_EXACT_U1_CLAUSE_SOURCE_ROWS.csv",
    "scan": OUT / "P8_Y5_R2FR_3278_FINITE_COEFFICIENT_SOURCE_SCAN.csv",
    "acquisition": OUT / "P8_Y5_R2FR_3278_SOURCE_SHADOW_ACQUISITION_AUDIT.csv",
    "intake": OUT / "P8_Y5_R2FR_3278_SOURCE_SHADOW_INTAKE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3278_BOUND_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3278_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3278_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3278_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3278_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: str, limit: int = 300) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


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
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 220)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3276_DOC, "3276 local theorem handoff", ["nonconserved", "magnetization", "source-shadow"]),
        (SRC_3276_SPLIT, "A_Q domain split theorem", ["ADS3276_3", "nonconserved_AJ_compensator"]),
        (SRC_3276_MAG, "F-only magnetization identity", ["MAG3276_1", "identically conserved"]),
        (SRC_3276_GAUGE, "nonconserved compensator gauge rejection", ["GJR3276_2", "REJECT_SILENT_COMPENSATOR"]),
        (SRC_3276_SHADOW, "3276 finite shadow coefficient rows", ["SSR3276_1", "MISSING_SOURCE_BACKED_SHADOW_BLOCK"]),
        (SRC_3277_DOC, "3277 parent exact-U1 handoff", ["nonconserved source-shadow exclusion", "finite data intake"]),
        (SRC_3277_SIG, "3277 exact U1 parent signature audit", ["U1SIG3277_3", "MATHEMATICALLY_DERIVED_PARENT_ACTION_UNSIGNED"]),
        (SRC_3277_THEOREM, "3277 representation current theorem", ["REP3277_1", "nonconserved source-shadow exclusion"]),
        (SRC_3277_INTAKE, "3277 source-shadow intake rows", ["SSI3277_1", "MISSING_SOURCE_BACKED_CONSERVED_SHADOW"]),
        (SRC_3277_RUNNER, "3277 bound runner", ["SSI3277_7_twice_bound_smoke", "FAIL_BOUND"]),
        (SRC_765_CEX, "current/generator rescale counterexamples", ["rescale", "counter"]),
        (SRC_1815_NO_RESCALE, "conditional no-current-rescale theorem", ["rescale", "pre-action"]),
        (SRC_2508_PROOF, "no-source-only slot attempt", ["source", "slot"]),
        (SRC_2616_SHADOW, "source-shadow ban attempt", ["source-shadow", "ban"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3278_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "source_class": "local_checkpoint_or_corpus_extract",
                "valid_for_claim": "false",
            }
        )
    return rows


def source_row_by_id(path: Path, key: str, row_id: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == row_id:
            return row
    raise KeyError(f"{row_id} not found in {path}")


def cj_bound() -> float:
    for row in read_csv(SRC_3277_INTAKE):
        if row.get("row_id") == "SSI3277_0_exact_U1_zero_conditional":
            return float(row["bound_value"])
    return float(read_csv(SRC_3276_SHADOW)[0]["bound_value"])


def target_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "TARGET3278_0_exact_clause_first",
            "selected_target": "source the exact U1 nonconserved-compensator rejection clause",
            "why_this_target": "it is a real mathematical clause already derived in 3276/3277 and does not require pretending a finite coefficient exists.",
            "finite_row_attempted": "true",
            "finite_row_result": "no source-backed numeric conserved-shadow/current-rescale/pre-action-weight/readout coefficient found in the searched local evidence set.",
            "parent_action_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "target_id": "TARGET3278_1_finite_row_guard",
            "selected_target": "do not promote C_J=0 from absence of a finite row",
            "why_this_target": "missing finite data is evidence of a gap, not evidence for the zero theorem; the exact clause only kills nonconserved silent compensation.",
            "finite_row_attempted": "true",
            "finite_row_result": "finite branch remains explicit and nonclaim.",
            "parent_action_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def exact_u1_clause_rows() -> list[dict[str, Any]]:
    gauge = source_row_by_id(SRC_3276_GAUGE, "test_id", "GJR3276_2_nonconserved_shadow")
    split = source_row_by_id(SRC_3276_SPLIT, "split_id", "ADS3276_3_nonconserved_AJ_compensator")
    rep = source_row_by_id(SRC_3277_THEOREM, "theorem_id", "REP3277_1_nonconserved_shadow")
    sig = source_row_by_id(SRC_3277_SIG, "sig_id", "U1SIG3277_3_exact_gauge_invariance")
    return [
        {
            "clause_id": "CLAUSE3278_0_nonconserved_silent_compensator_forbidden",
            "mathematical_clause": "For S_shadow=int mu A_Q_mu J_comp^mu, exact local U1 with delta A_Q_mu=nabla_mu lambda gives delta S=-int mu lambda nabla_mu J_comp^mu plus boundary; compact-support arbitrary lambda requires nabla_mu J_comp^mu=0 or a real charged-sector Ward identity.",
            "source_paths": ";".join(str(path) for path in [SRC_3276_GAUGE, SRC_3276_SPLIT, SRC_3277_THEOREM, SRC_3277_SIG]),
            "source_rows": "GJR3276_2_nonconserved_shadow;ADS3276_3_nonconserved_AJ_compensator;REP3277_1_nonconserved_shadow;U1SIG3277_3_exact_gauge_invariance",
            "source_evidence": compact(" | ".join([gauge["result"], split["divergence_status"], rep["formal_statement"], sig["current_evidence"]]), 900),
            "source_backed": "true",
            "parent_action_signed": "false",
            "claim_status": "CLAUSE_SOURCE_BACKED_PARENT_ACTION_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLAUSE3278_1_F_only_wave_response_not_CJ_compensator",
            "mathematical_clause": "F_Q-only wave/Pauli/polarization/Poynting response changes H^{mu nu}, T_EM^{mu nu}, boundary flux and constitutive stress, but its current is J_mag^nu=-nabla_mu H^{mu nu} and is identically conserved.",
            "source_paths": ";".join(str(path) for path in [SRC_3276_SPLIT, SRC_3276_MAG]),
            "source_rows": "ADS3276_1_F_only_magnetization;MAG3276_1_identity;MAG3276_3_stress_consequence",
            "source_evidence": compact(" | ".join([
                source_row_by_id(SRC_3276_SPLIT, "split_id", "ADS3276_1_F_only_magnetization")["C_J_effect"],
                source_row_by_id(SRC_3276_MAG, "lemma_id", "MAG3276_1_identity")["formula"],
                source_row_by_id(SRC_3276_MAG, "lemma_id", "MAG3276_3_stress_consequence")["claim"],
            ]), 900),
            "source_backed": "true",
            "parent_action_signed": "false",
            "claim_status": "CLAUSE_SOURCE_BACKED_SIDE_CONDITIONS_REMAIN",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CLAUSE3278_2_parent_exact_U1_signature_not_signed",
            "mathematical_clause": "The nonconserved-compensator rejection can be used only inside a branch where exact U1 is parent action data; 3277 records that the parent action signature is still unsigned.",
            "source_paths": str(SRC_3277_SIG),
            "source_rows": "U1SIG3277_5_verdict",
            "source_evidence": source_row_by_id(SRC_3277_SIG, "sig_id", "U1SIG3277_5_verdict")["status"],
            "source_backed": "true",
            "parent_action_signed": "false",
            "claim_status": "BLOCKS_LOCAL_GR_OR_MAXWELL_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def is_real_finite_numeric(value: str, row: dict[str, str]) -> bool:
    text = str(value).strip()
    if not text or "MISSING" in text.upper() or "FORBIDDEN" in text.upper():
        return False
    try:
        numeric = float(text)
    except ValueError:
        return False
    if not math.isfinite(numeric):
        return False
    if numeric == 0.0:
        return False
    status_text = " ".join(str(v).upper() for v in row.values())
    if any(marker in status_text for marker in ["SMOKE", "CONDITIONAL", "THEOREM", "NO_FLUX", "PASS_IF"]):
        return False
    return True


def finite_coefficient_source_scan_rows() -> list[dict[str, Any]]:
    scan_sources = [SRC_3276_SHADOW, SRC_3277_INTAKE]
    rows: list[dict[str, Any]] = []
    for path in scan_sources:
        for index, row in enumerate(read_csv(path)):
            row_id = row.get("row_id", f"row_{index}")
            value = row.get("numeric_value", row.get("prediction_value", ""))
            quantity = row.get("coefficient", row.get("quantity", ""))
            status = row.get("status", row.get("result_status", ""))
            finite_numeric = is_real_finite_numeric(value, row)
            rows.append(
                {
                    "scan_id": f"SCAN3278_{len(rows)}",
                    "source_path": str(path),
                    "source_row": row_id,
                    "quantity": quantity,
                    "value_field": value,
                    "status_field": status,
                    "real_finite_numeric_candidate": bool_str(finite_numeric),
                    "reason": "candidate" if finite_numeric else "missing, forbidden, theorem-zero, conditional, or smoke row",
                    "valid_for_claim": "false",
                }
            )
    if not any(row["real_finite_numeric_candidate"] == "true" for row in rows):
        rows.append(
            {
                "scan_id": "SCAN3278_SUMMARY",
                "source_path": ";".join(str(path) for path in scan_sources),
                "source_row": "summary",
                "quantity": "epsilon_shadow/c_A_or_kappa_A/w_A/readout_reentry",
                "value_field": "NO_REAL_FINITE_SOURCE_BACKED_NUMERIC_ROW_FOUND",
                "status_field": "BLOCKED_FOR_CJ_CLAIM",
                "real_finite_numeric_candidate": "false",
                "reason": "the searched rows contain only missing, forbidden, theorem-zero, conditional no-flux, or smoke values.",
                "valid_for_claim": "false",
            }
        )
    return rows


def acquisition_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ACQ3278_0_nonconserved_clause",
            "route": "exact U1 clause source",
            "target_quantity": "J_comp_nonconserved",
            "result": "SOURCE_BACKED_AS_FORBIDDEN_SILENT_ROUTE",
            "source_paths": ";".join(str(path) for path in [SRC_3276_GAUGE, SRC_3277_THEOREM]),
            "next_action": "do not put this into numeric runner as a finite residual; route real sectors to conserved-shadow branch.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACQ3278_1_conserved_shadow",
            "route": "finite source-shadow coefficient",
            "target_quantity": "epsilon_shadow",
            "result": "BLOCKED_NO_SOURCE_BACKED_NUMERIC_ROW",
            "source_paths": ";".join(str(path) for path in [SRC_3276_SHADOW, SRC_3277_INTAKE]),
            "next_action": "hunt for a real parent/source row or demote C_J finite branch to closure-only.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACQ3278_2_current_rescale",
            "route": "current normalization/readout rescale",
            "target_quantity": "c_A_or_kappa_A",
            "result": "BLOCKED_BY_RESCALING_COUNTEREXAMPLE_AND_MISSING_COEFFICIENT",
            "source_paths": ";".join(str(path) for path in [SRC_765_CEX, SRC_1815_NO_RESCALE, SRC_3277_INTAKE]),
            "next_action": "source an actual current map or treat as explicit residual coefficient.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACQ3278_3_pre_action_weight",
            "route": "pre-action source weight",
            "target_quantity": "w_A",
            "result": "BLOCKED_NO_PARENT_WEIGHT_MAP",
            "source_paths": ";".join(str(path) for path in [SRC_1815_NO_RESCALE, SRC_3277_INTAKE]),
            "next_action": "source a parent variational weight map before using it in C_J.",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "ACQ3278_4_magnetization_boundary",
            "route": "F-only wave/Poynting/magnetization response",
            "target_quantity": "epsilon_mag_boundary",
            "result": "EXACT_ZERO_ONLY_WITH_NO_FLUX_SIDE_CONDITION",
            "source_paths": ";".join(str(path) for path in [SRC_3276_SPLIT, SRC_3276_MAG, SRC_3277_INTAKE]),
            "next_action": "move wave/Poynting effects into EM stress and boundary residuals, not current-normalization C_J.",
            "valid_for_claim": "false",
        },
    ]


def intake_rows() -> list[dict[str, Any]]:
    bound = cj_bound()
    return [
        {
            "row_id": "SSI3278_0_exact_U1_clause_nonconserved_forbidden",
            "current_type": "nonconserved_forbidden_clause",
            "coefficient": "J_comp_nonconserved",
            "numeric_value": "FORBIDDEN_BY_SOURCE_BACKED_EXACT_U1_CLAUSE_IF_PARENT_U1_HOLDS",
            "units": "not numeric",
            "conservation_certificate": "source-backed local clause requires nabla_mu J_comp^mu=0 or real charged-sector Ward identity",
            "projection_to_CJ": "not a finite residual; route real sector to conserved shadow intake",
            "bound_value": fmt(bound),
            "status": "CLAUSE_SOURCE_BACKED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_1_conserved_shadow_missing",
            "current_type": "conserved_shadow",
            "coefficient": "epsilon_shadow",
            "numeric_value": "MISSING_SOURCE_BACKED_CONSERVED_SHADOW",
            "units": "dimensionless relative source-current coefficient",
            "conservation_certificate": "MISSING",
            "projection_to_CJ": "MISSING_SHADOW_TO_CJ_PROJECTION",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_2_current_rescale_missing",
            "current_type": "current_rescale",
            "coefficient": "c_A_or_kappa_A",
            "numeric_value": "MISSING_CURRENT_RESCALE_COEFFICIENT",
            "units": "dimensionless relative current normalization",
            "conservation_certificate": "normalization may be conserved but is independent unless parent map is signed",
            "projection_to_CJ": "MISSING_C_A_TO_CJ_MAP",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_3_pre_action_weight_missing",
            "current_type": "pre_action_weight",
            "coefficient": "w_A",
            "numeric_value": "MISSING_PRE_ACTION_WEIGHT",
            "units": "dimensionless action/source weight",
            "conservation_certificate": "weighted current can conserve but source ownership remains parent-domain debt",
            "projection_to_CJ": "MISSING_WA_TO_CJ_MAP",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_4_magnetization_no_flux_zero",
            "current_type": "magnetization_boundary",
            "coefficient": "epsilon_mag_boundary",
            "numeric_value": "0",
            "units": "dimensionless current-normalization leakage",
            "conservation_certificate": "F-only current identically conserved; zero requires compact no-flux/source support",
            "projection_to_CJ": "zero under no-flux side condition",
            "bound_value": fmt(bound),
            "status": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_5_half_bound_smoke",
            "current_type": "smoke",
            "coefficient": "C_J_effective",
            "numeric_value": fmt(bound / 2.0),
            "units": "dimensionless local logarithmic coefficient",
            "conservation_certificate": "SMOKE_NUMERIC_NONCLAIM",
            "projection_to_CJ": "identity",
            "bound_value": fmt(bound),
            "status": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3278_6_twice_bound_smoke",
            "current_type": "smoke",
            "coefficient": "C_J_effective",
            "numeric_value": fmt(bound * 2.0),
            "units": "dimensionless local logarithmic coefficient",
            "conservation_certificate": "SMOKE_NUMERIC_NONCLAIM",
            "projection_to_CJ": "identity",
            "bound_value": fmt(bound),
            "status": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def runner_result(row: dict[str, Any]) -> tuple[str, str, str, str]:
    value = str(row["numeric_value"])
    bound = float(row["bound_value"])
    if "FORBIDDEN_BY_SOURCE_BACKED_EXACT_U1_CLAUSE" in value:
        return ("N/A", "N/A", "CLAUSE_PASS_NONNUMERIC_NONCLAIM", "CLAUSE_PASS_NONNUMERIC_NONCLAIM")
    if "MISSING" in value or "FORBIDDEN" in value:
        return ("MISSING", "false", "REFUSE_OR_FAIL", "REFUSE_OR_FAIL")
    numeric = float(value)
    ratio = abs(numeric) / bound if bound != 0 else math.inf
    result = "PASS_NUMERIC_NONCLAIM" if abs(numeric) <= bound else "FAIL_BOUND"
    expected = {
        "SSI3278_4_magnetization_no_flux_zero": "PASS_NUMERIC_NONCLAIM",
        "SSI3278_5_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "SSI3278_6_twice_bound_smoke": "FAIL_BOUND",
    }.get(str(row["row_id"]), result)
    return (fmt(ratio), bool_str(abs(numeric) <= bound), result, expected)


def bound_runner_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in intake_rows():
        ratio, pass_bound, result, expected = runner_result(row)
        rows.append(
            {
                "row_id": row["row_id"],
                "current_type": row["current_type"],
                "numeric_value": row["numeric_value"],
                "bound_value": row["bound_value"],
                "prediction_over_bound": ratio,
                "pass_bound": pass_bound,
                "result": result,
                "expected": expected,
                "expectation_met": bool_str(result == expected),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    clauses = exact_u1_clause_rows()
    scan = finite_coefficient_source_scan_rows()
    runner = bound_runner_rows()
    return [
        {
            "gate_id": "GATE3278_0_exact_clause_sourced",
            "gate": "nonconserved silent compensator exact-U1 rejection is source-backed",
            "passed": bool_str(any(row["clause_id"] == "CLAUSE3278_0_nonconserved_silent_compensator_forbidden" and row["source_backed"] == "true" for row in clauses)),
            "claim_allowed": "false",
            "detail": "mathematical clause promoted; parent action exact-U1 remains unsigned.",
        },
        {
            "gate_id": "GATE3278_1_parent_action_signature",
            "gate": "parent exact-U1 action signature is signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "3277 verdict remains EXACT_U1_REPRESENTATION_SIGNATURE_NOT_PARENT_SIGNED.",
        },
        {
            "gate_id": "GATE3278_2_finite_coefficient_found",
            "gate": "real finite source-shadow/current-rescale/pre-action/readout coefficient found",
            "passed": bool_str(any(row["real_finite_numeric_candidate"] == "true" for row in scan)),
            "claim_allowed": "false",
            "detail": "scan found no live finite source-backed numeric row; only missing/theorem-zero/smoke rows.",
        },
        {
            "gate_id": "GATE3278_3_runner_behaviour",
            "gate": "bound runner routes nonnumeric clause, missing rows, zero row, and smoke rows correctly",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "claim_allowed": "false",
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "gate_id": "GATE3278_4_no_local_claim",
            "gate": "no R10, WEP, PPN, clock, orbital, local-GR, or Maxwell claim promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3278 is a clause-source and finite-row acquisition checkpoint only.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3278_0_real_progress",
            "decision": "Promote the nonconserved silent-compensator rejection from a target to a source-backed local mathematical clause.",
            "why_it_moves_forward": "one branch is now closed cleanly: no hidden nonconserved current can be inserted to cancel variable kappa_J without either breaking exact U1 or becoming a real charged sector.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3278_1_wave_poynting_route",
            "decision": "Keep wave/Poynting/F-only response in EM stress and boundary residuals rather than C_J current normalization.",
            "why_it_moves_forward": "this preserves the user's background-field intuition while keeping the math honest: F-only terms are real physics, but their current is identically conserved.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3278_2_finite_branch",
            "decision": "Finite C_J rows are not found; they remain explicit source-acquisition debt.",
            "why_it_moves_forward": "the next step cannot be another abstract theorem loop; it must either find a real coefficient/source map or demote the C_J finite branch to closure-only.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3278_0_3279",
            "target_doc": "3279-Y5-R2FR-first-finite-source-shadow-row-source-hunt-or-CJ-closure-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3279_first_finite_source_shadow_row_source_hunt_or_CJ_closure_demotion.py",
            "objective": "Make one aggressive finite-row source hunt for epsilon_shadow, c_A/kappa_A, w_A, or readout reentry across the local corpus; if no real numeric/source map exists, demote the finite C_J branch to explicit closure-only and move to the next coupling component.",
            "guardrail": "Do not write another theorem-only target unless it names a new source path and a real coefficient map; finite rows must be numeric, unit-labelled, source-backed, and valid_for_claim=false until bounds pass.",
            "valid_for_claim": "false",
        }
    ]


def output_csvs_parse() -> bool:
    return all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register_rows()
    clauses = exact_u1_clause_rows()
    scan = finite_coefficient_source_scan_rows()
    intake = intake_rows()
    runner = bound_runner_rows()
    gates = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3278_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3278_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3278_2_outputs_parse",
            "check": "all 3278 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3278_3_clause_promoted_not_claimed",
            "check": "at least one exact U1 clause is source-backed but no clause is valid_for_claim",
            "passed": bool_str(any(row["source_backed"] == "true" for row in clauses) and all(row["valid_for_claim"] == "false" for row in clauses)),
            "detail": ";".join(f"{row['clause_id']}={row['claim_status']}" for row in clauses),
        },
        {
            "check_id": "VAL3278_4_no_finite_candidate_fabricated",
            "check": "finite source-shadow scan does not fabricate a numeric row",
            "passed": bool_str(not any(row["real_finite_numeric_candidate"] == "true" for row in scan)),
            "detail": "no real finite numeric source-backed candidate in 3276/3277 intake rows",
        },
        {
            "check_id": "VAL3278_5_intake_rows_nonclaim",
            "check": "all 3278 intake rows remain nonclaim",
            "passed": bool_str(all(row["valid_for_claim"] == "false" for row in intake)),
            "detail": "",
        },
        {
            "check_id": "VAL3278_6_runner_expectations",
            "check": "bound runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3278_7_claim_gates_false",
            "check": "no 3278 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3278_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3278_9_overall",
            "check": "3278 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3278_9_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(compact(str(row.get(col, "")), 180).replace("|", "\\|") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc() -> None:
    target = read_csv(OUTPUTS["target"])
    clauses = read_csv(OUTPUTS["clauses"])
    scan = read_csv(OUTPUTS["scan"])
    acquisition = read_csv(OUTPUTS["acquisition"])
    intake = read_csv(OUTPUTS["intake"])
    runner = read_csv(OUTPUTS["runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3278 - Source-shadow finite row acquisition or parent U1 clause source under AX1090

## Summary

3278 does **not** claim local GR, Maxwell closure, WEP, R10, PPN, clock, or orbital success. It takes one real step forward: the nonconserved silent-compensator route is now promoted to a source-backed local mathematical clause, using the 3276/3277 gauge-variation rows.

The finite `C_J` branch is also forced through an acquisition gate. No real source-backed finite coefficient row is found in the current 3276/3277 intake evidence, so `epsilon_shadow`, `c_A/kappa_A`, `w_A`, and readout reentry remain explicit nonclaim debt rather than hidden assumptions.

## Exact Clause

For a silent source term

`S_shadow = int mu A_Q_mu J_comp^mu`,

with `delta_lambda A_Q_mu = nabla_mu lambda`,

`delta_lambda S_shadow = int mu J_comp^mu nabla_mu lambda = - int mu lambda nabla_mu J_comp^mu + boundary`.

For arbitrary compact-support `lambda`, exact U(1) requires `nabla_mu J_comp^mu=0`, unless `J_comp` is the Noether current of a real charged sector whose Ward identity supplies the conservation law. Therefore a nonconserved silent compensator cannot be used as a hidden cancellation mechanism for variable `kappa_J`.

## Target Selection
{md_table(target, ["target_id", "selected_target", "why_this_target", "finite_row_result"])}

## Exact U1 Clause Source Rows
{md_table(clauses, ["clause_id", "source_backed", "parent_action_signed", "claim_status", "valid_for_claim"])}

## Finite Coefficient Source Scan
{md_table(scan, ["scan_id", "source_row", "quantity", "value_field", "real_finite_numeric_candidate", "reason"])}

## Source-Shadow Acquisition Audit
{md_table(acquisition, ["audit_id", "route", "target_quantity", "result", "next_action"])}

## Intake Rows
{md_table(intake, ["row_id", "current_type", "coefficient", "numeric_value", "status", "valid_for_claim"])}

## Bound Runner
{md_table(runner, ["row_id", "numeric_value", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decisions, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_rows, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register_rows(),
        "target": target_selection_rows(),
        "clauses": exact_u1_clause_rows(),
        "scan": finite_coefficient_source_scan_rows(),
        "acquisition": acquisition_audit_rows(),
        "intake": intake_rows(),
        "runner": bound_runner_rows(),
        "promotion": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
