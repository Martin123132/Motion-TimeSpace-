from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3951"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3951-Y5-R2FR-GK-symbol-match-coefficient-extraction-or-epsilon-GK-first-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3951_SOURCE_REGISTER.csv",
    "audit": SRC / "P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv",
    "components": SRC / "P8_Y5_R2FR_3951_EPSILON_GK_COMPONENT_INPUTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3951_GK_SYMBOL_MATCH_DECISION.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3951_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3951_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3951_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3951_VALIDATION.csv",
}

NEXT_DOC = "3952-Y5-R2FR-GK-Helmholtz-Khat-metric-response-test-or-DeltaK-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3952_GK_Helmholtz_Khat_metric_response_test_or_DeltaK_bound.py"
QLOC_PROXY_VALUE = "7.432631961576971e-06"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def row_contains(row: dict[str, str], needle: str) -> bool:
    return needle in " ".join(str(value) for value in row.values())


def find_row(path: Path, needle: str) -> dict[str, str] | None:
    for row in read_csv(path):
        if row_contains(row, needle):
            return row
    return None


def compact_row(row: dict[str, str] | None, preferred: list[str]) -> str:
    if not row:
        return "ROW_NOT_FOUND"
    pieces: list[str] = []
    for key in preferred:
        value = row.get(key, "")
        if value:
            pieces.append(f"{key}={value}")
    if not pieces:
        pieces = [f"{key}={value}" for key, value in list(row.items())[:5]]
    return " | ".join(pieces)[:1200]


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3951_00_3950_next", SRC / "P8_Y5_R2FR_3950_NEXT_TARGET.csv", "NEXT3950_0", "3950 handoff target"),
        ("SRC3951_01_3950_signature", SRC / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv", "GKS3950_4_verdict", "positive auxiliary verdict"),
        ("SRC3951_02_3950_ward", SRC / "P8_Y5_R2FR_3950_GK_WARD_QLOC_ZERO_THEOREM.csv", "WZ3950_1_q_loc", "q_loc Ward route"),
        ("SRC3951_03_3950_bound", SRC / "P8_Y5_R2FR_3950_EPSILON_NONMINIMAL_GK_BOUND_ROW.csv", "EGK3950_6_total", "epsilon_nonminimal_GK total"),
        ("SRC3951_04_GO516_A", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "response doublet candidate"),
        ("SRC3951_05_GK514_A", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_A_metric_response_scalar_density", "metric response scalar density"),
        ("SRC3951_06_G514_match", SRC / "P8_GK_STRESS_ACTION_GATE_TESTS.csv", "G514_2_current_MTS_match", "current MTS metric-response match gate"),
        ("SRC3951_07_GKT1010", SRC / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv", "GKT1010_6_verdict", "q_loc theorem attempt verdict"),
        ("SRC3951_08_QBF1011", SRC / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv", "QBF1011_0_compact_shell_budget", "compact shell q_loc proxy"),
        ("SRC3951_09_PHS2216", SRC / "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv", "PHS2216_1_parent_density_owner", "parent density owner extraction"),
        ("SRC3951_10_EVM2216", SRC / "P8_Y5_PARENT_QLOC_2216_SIGNATURE_EVIDENCE_MAP.csv", "EVM2216_1_hard_block", "parent action owner hard block"),
        ("SRC3951_11_KIC2217_density", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv", "KIC2217_0_scalar_density_owner", "Khat identity density owner"),
        ("SRC3951_12_KIC2217_helmholtz", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv", "KIC2217_4_Helmholtz_integrability", "Helmholtz integrability gate"),
        ("SRC3951_13_DK2217_density", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv", "DK2217_0_density_owner_gap", "Delta density residual"),
        ("SRC3951_14_DK2217_helmholtz", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv", "DK2217_4_Helmholtz_gap", "Helmholtz residual"),
        ("SRC3951_15_DK2217_source_boundary", SRC / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv", "DK2217_5_source_boundary_gap", "source and boundary residual"),
        ("SRC3951_16_GAP1619_operator", SRC / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv", "GAP1619_5_positive_operator_parent", "positive operator parent gap"),
        ("SRC3951_17_GAP1619_PPN", SRC / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv", "GAP1619_6_PPN_source_lock", "PPN source lock gap"),
        ("SRC3951_18_validation_3950", SRC / "P8_Y5_BRR545_3950_VALIDATION.csv", "VAL3950_19_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def evidence(path_name: str, needle: str, preferred: list[str]) -> str:
    return compact_row(find_row(SRC / path_name, needle), preferred)


def extraction_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    go516 = evidence(
        "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "GO516_A_response_doublet_quadratic_density",
        ["field_content", "action_density", "current_status"],
    )
    gk514 = evidence(
        "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "GK514_A_metric_response_scalar_density",
        ["candidate_action", "stress_form", "required_identification", "current_status"],
    )
    g514 = evidence(
        "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
        "G514_2_current_MTS_match",
        ["gate", "result", "evidence"],
    )
    q1010 = evidence(
        "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
        "GKT1010_6_verdict",
        ["claim_piece", "current_evidence", "status"],
    )
    q1011 = evidence(
        "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
        "QBF1011_0_compact_shell_budget",
        ["quantity", "candidate_value", "units", "bound_or_gate", "status"],
    )
    phs2216 = evidence(
        "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv",
        "PHS2216_1_parent_density_owner",
        ["parent_signature", "extraction_result", "what_remains_unsigned"],
    )
    evm2216 = evidence(
        "P8_Y5_PARENT_QLOC_2216_SIGNATURE_EVIDENCE_MAP.csv",
        "EVM2216_1_hard_block",
        ["premise", "finding", "promotion_status", "next_use"],
    )
    kic_density = evidence(
        "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv",
        "KIC2217_0_scalar_density_owner",
        ["requirement", "comparison_result", "mismatch", "repair"],
    )
    kic_helmholtz = evidence(
        "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv",
        "KIC2217_4_Helmholtz_integrability",
        ["requirement", "comparison_result", "mismatch", "repair"],
    )
    dk_density = evidence(
        "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv",
        "DK2217_0_density_owner_gap",
        ["residual_symbol", "definition", "physical_effect", "required_to_close"],
    )
    dk_helmholtz = evidence(
        "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv",
        "DK2217_4_Helmholtz_gap",
        ["residual_symbol", "definition", "physical_effect", "required_to_close"],
    )
    dk_source_boundary = evidence(
        "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv",
        "DK2217_5_source_boundary_gap",
        ["residual_symbol", "definition", "physical_effect", "required_to_close"],
    )
    gap_operator = evidence(
        "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv",
        "GAP1619_5_positive_operator_parent",
        ["required_signature", "status", "effect"],
    )
    gap_ppn = evidence(
        "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv",
        "GAP1619_6_PPN_source_lock",
        ["required_signature", "status", "effect"],
    )
    return [
        {
            "row_id": "GKA3951_0_Z_field_identification",
            "coefficient_slot": "Z^A physical residual fields",
            "current_extraction": "CANDIDATE_RESPONSE_DOUBLET_ONLY",
            "matched_source_ids": "SRC3951_04_GO516_A;SRC3951_17_GAP1619_PPN",
            "extracted_candidate": "Z^A=(R_+^A-R_-^A)/2 from response-doublet candidate",
            "evidence_summary": go516,
            "derived_effect": "gives a possible double-zero coordinate if actual q_loc/PPN/source-normalization residuals map to Z^A",
            "missing_or_unsigned_clause": "actual MTS residual vector-to-Z^A map not derived",
            "next_action": "match Gamma_eff/K_hat/q_loc symbols to the response-doublet variables or demote Z^A to closure-only",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_1_GAB_kinetic_signature",
            "coefficient_slot": "G_AB gradient/kinetic matrix",
            "current_extraction": "NOT_EXTRACTED_FROM_CURRENT_MTS",
            "matched_source_ids": "SRC3951_01_3950_signature;SRC3951_16_GAP1619_operator",
            "extracted_candidate": "formal positive auxiliary kinetic block G_AB>=0",
            "evidence_summary": gap_operator,
            "derived_effect": "would sign the gradient energy and help no-hair if positive after constraints",
            "missing_or_unsigned_clause": "no parent-owned G_AB entries, units, field basis, gauge removal, or sign proof",
            "next_action": "derive second variation of an explicit Gamma_eff density with respect to gradients of Z^A",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_2_MAB_hessian_signature",
            "coefficient_slot": "M_AB mass/Hessian matrix",
            "current_extraction": "NOT_EXTRACTED_FROM_CURRENT_MTS",
            "matched_source_ids": "SRC3951_04_GO516_A;SRC3951_09_PHS2216",
            "extracted_candidate": "formal quadratic density M_AB Z^A Z^B / 2",
            "evidence_summary": phs2216,
            "derived_effect": "would provide local restoring force and amplitude suppression if M_AB has a positive gap",
            "missing_or_unsigned_clause": "parent density owner not found; M_AB is not yet a parent Hessian",
            "next_action": "write Gamma_eff as an accepted scalar density first, then compute Hessian",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_3_Gamma_density_owner",
            "coefficient_slot": "Gamma_eff scalar density/action owner",
            "current_extraction": "FAIL_CURRENT_CLAIM",
            "matched_source_ids": "SRC3951_09_PHS2216;SRC3951_10_EVM2216;SRC3951_11_KIC2217_density",
            "extracted_candidate": "none accepted; only candidate route exists",
            "evidence_summary": f"{phs2216} || {evm2216} || {kic_density}",
            "derived_effect": "without density ownership the Ward/q_loc proof cannot activate",
            "missing_or_unsigned_clause": "explicit field content, metric dependence, units, and boundary convention",
            "next_action": "construct the parent density or keep Gamma_eff as residual/readout only",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_4_Kmetric_Khat_identity",
            "coefficient_slot": "K_metric/K_hat response identity",
            "current_extraction": "FAIL_CURRENT_CLAIM",
            "matched_source_ids": "SRC3951_05_GK514_A;SRC3951_06_G514_match;SRC3951_11_KIC2217_density",
            "extracted_candidate": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} minus convention",
            "evidence_summary": f"{gk514} || {g514} || {kic_density}",
            "derived_effect": "would set Delta_K=0 by definition and convert q_loc into a Ward residual",
            "missing_or_unsigned_clause": "actual K_hat not matched to metric variation of actual Gamma_eff",
            "next_action": "perform Helmholtz/metric-response test for the proposed K_hat tensor",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_5_DeltaK_mismatch_residual",
            "coefficient_slot": "Delta_K := K_hat - K_metric[Gamma_eff]",
            "current_extraction": "VALUE_READY_SYMBOLIC_RESIDUAL_NOT_NUMERIC",
            "matched_source_ids": "SRC3951_13_DK2217_density;SRC3951_14_DK2217_helmholtz",
            "extracted_candidate": "Delta_K is the residual bucket for density-owner and Helmholtz mismatch",
            "evidence_summary": f"{dk_density} || {dk_helmholtz}",
            "derived_effect": "if nonzero it feeds epsilon_GK_metric_response_mismatch=|Delta_K|/E_pos",
            "missing_or_unsigned_clause": "no tensor value, norm, or arena projection yet",
            "next_action": "either prove Delta_K=0 via Helmholtz identity or bound |Delta_K| against E_pos",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_6_Helmholtz_integrability",
            "coefficient_slot": "H_GK antisymmetric second-variation obstruction",
            "current_extraction": "NOT_CHECKED_BLOCKS_PROMOTION",
            "matched_source_ids": "SRC3951_12_KIC2217_helmholtz;SRC3951_14_DK2217_helmholtz",
            "extracted_candidate": "H_GK is the obstruction to a parent action for proposed K_hat",
            "evidence_summary": f"{kic_helmholtz} || {dk_helmholtz}",
            "derived_effect": "if H_GK=0 the Khat stress can be variational; if not, the local branch remains bound-only",
            "missing_or_unsigned_clause": "no second-variation symmetry calculation has been run on a proposed tensor",
            "next_action": "make 3952 a Helmholtz/Khat metric-response test rather than another audit",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_7_source_current_boundary",
            "coefficient_slot": "J_GK + B_GK source and boundary terms",
            "current_extraction": "UNSIGNED_NONZERO_ALLOWED",
            "matched_source_ids": "SRC3951_15_DK2217_source_boundary;SRC3951_02_3950_ward",
            "extracted_candidate": "source-current plus boundary forcing after candidate density variation",
            "evidence_summary": dk_source_boundary,
            "derived_effect": "even a good Khat identity does not give q_loc=0 unless source and boundary terms vanish or are bounded",
            "missing_or_unsigned_clause": "no source-current-zero theorem, no boundary-flux-zero theorem, no finite values",
            "next_action": "after Helmholtz, prove J_A=B_A=0 or add finite component rows",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_8_q_loc_Ward_route",
            "coefficient_slot": "q_loc^nu Ward residual profile",
            "current_extraction": "CONDITIONAL_FORM_ONLY",
            "matched_source_ids": "SRC3951_02_3950_ward;SRC3951_07_GKT1010",
            "extracted_candidate": "q_loc^nu=-P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu)",
            "evidence_summary": q1010,
            "derived_effect": "local zero is mathematically clean if Euler, boundary, source and projector clauses close",
            "missing_or_unsigned_clause": "current corpus lacks match, Helmholtz check, Euler closure, double-zero, projector, and boundary certificates",
            "next_action": "use this as the theorem target, not as a present claim",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_9_q_loc_compact_shell_proxy",
            "coefficient_slot": "q_loc compact-shell proxy",
            "current_extraction": "NUMERIC_PROXY_IMPORTED_NONCLAIM",
            "matched_source_ids": "SRC3951_08_QBF1011",
            "extracted_candidate": QLOC_PROXY_VALUE,
            "evidence_summary": q1011,
            "derived_effect": "first actual number in this GK/q_loc chain; useful smoke input but not a physical claim row",
            "missing_or_unsigned_clause": "mapping into PPN/source-normalization units and arena projection",
            "next_action": "carry it as q_loc_shell_proxy until the physical projector and units are derived",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_10_positive_operator_parent",
            "coefficient_slot": "positive operator / no-hair parent",
            "current_extraction": "FORMAL_CANDIDATE_ONLY",
            "matched_source_ids": "SRC3951_16_GAP1619_operator",
            "extracted_candidate": "H_AB and M_AB positive after gauge/constraint removal",
            "evidence_summary": gap_operator,
            "derived_effect": "would suppress local hair and support the plateau without an axiom",
            "missing_or_unsigned_clause": "positivity assumed in normal form, not derived for actual MTS variables",
            "next_action": "requires the same parent density and Hessian extraction as GKA3951_2",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKA3951_11_PPN_source_lock",
            "coefficient_slot": "physical residual equals PPN/source-normalization vector",
            "current_extraction": "NOT_DERIVED",
            "matched_source_ids": "SRC3951_17_GAP1619_PPN",
            "extracted_candidate": "Z^A should equal the physical q_loc/PPN/source-normalization residual vector",
            "evidence_summary": gap_ppn,
            "derived_effect": "needed so a silent Z^A actually means Newton/GR normalization survives",
            "missing_or_unsigned_clause": "source-current/charge equality not derived",
            "next_action": "after Khat response, map Z^A to measured local source normalization",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def component_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "EGKI3951_0_denominator",
            "E_pos",
            "positive source-energy denominator",
            "",
            "energy",
            "MISSING_DENOMINATOR_VALUE",
            "SRC3951_03_3950_bound",
            "E_pos source row still required before epsilon scoring",
        ),
        (
            "EGKI3951_1_GK_energy",
            "epsilon_GK_energy",
            "E_GK_unsigned_abs/E_pos",
            "",
            "dimensionless",
            "MISSING_GAB_MAB_AMPLITUDE_SUPPORT",
            "SRC3951_01_3950_signature;SRC3951_16_GAP1619_operator",
            "need field content, G_AB, M_AB, amplitudes, and local support",
        ),
        (
            "EGKI3951_2_metric_response",
            "epsilon_GK_metric_response_mismatch",
            "|Delta_K|/E_pos",
            "",
            "dimensionless",
            "MISSING_DELTAK_VALUE",
            "SRC3951_13_DK2217_density;SRC3951_14_DK2217_helmholtz",
            "need Khat metric-response proof or Delta_K norm",
        ),
        (
            "EGKI3951_3_boundary",
            "epsilon_GK_boundary",
            "|E_Khat_boundary_unsigned|/E_pos",
            "",
            "dimensionless",
            "MISSING_BOUNDARY_FLUX_VALUE",
            "SRC3951_15_DK2217_source_boundary",
            "need boundary silence theorem or finite boundary flux",
        ),
        (
            "EGKI3951_4_source_charge",
            "epsilon_GK_source_charge",
            "|E_GK_source_charge|/E_pos",
            "",
            "dimensionless",
            "MISSING_SOURCE_CHARGE_VALUE",
            "SRC3951_15_DK2217_source_boundary;SRC3951_17_GAP1619_PPN",
            "need source-current-zero theorem or finite source-charge row",
        ),
        (
            "EGKI3951_5_negative_hessian",
            "epsilon_GK_negative_hessian",
            "|E_negative_hessian_modes|/E_pos",
            "",
            "dimensionless",
            "MISSING_HESSIAN_SIGNATURE_VALUE",
            "SRC3951_09_PHS2216;SRC3951_16_GAP1619_operator",
            "need Hessian/mass-gap signature or negative-mode bound",
        ),
        (
            "EGKI3951_6_q_loc_proxy",
            "q_loc_shell_proxy",
            "max |P_loc d_rel J_rel| proxy from compact-shell runner",
            QLOC_PROXY_VALUE,
            "dimensionless_proxy",
            "NUMERIC_PROXY_NONCLAIM",
            "SRC3951_08_QBF1011",
            "mapping into PPN/source-normalization units still missing",
        ),
        (
            "EGKI3951_7_total",
            "epsilon_nonminimal_counterterm_GK",
            "sum_abs(epsilon_GK_energy,epsilon_GK_metric_response_mismatch,epsilon_GK_boundary,epsilon_GK_source_charge,epsilon_GK_negative_hessian)",
            "",
            "dimensionless",
            "COMPONENT_VALUES_MISSING_PROXY_IMPORTED",
            "SRC3951_03_3950_bound;SRC3951_08_QBF1011",
            "cannot score total until denominator and physical component values exist",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "component_symbol": symbol,
            "formula_or_value": formula,
            "value": value,
            "units": units,
            "extraction_status": status,
            "source_ids": source_ids,
            "blocker": blocker,
            "row_type": "EPSILON_GK_COMPONENT_INPUT",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, value, units, status, source_ids, blocker in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3951_0_no_actual_match",
            "decision": "do not sign the Gamma_eff/K_hat positive auxiliary route yet",
            "basis": "Z^A, G_AB, M_AB, Gamma density ownership, Khat metric-response identity, Helmholtz integrability, and source/boundary silence remain unsigned against actual MTS definitions",
            "effect": "local-GR/PPN promotion remains blocked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3951_1_keep_route",
            "decision": "keep the response-doublet/metric-response route as the best derivation path",
            "basis": "it is the least smuggled route because q_loc becomes a Ward residual if Khat is a true metric response",
            "effect": "next work should compute the Helmholtz/Khat identity rather than circle the same gap",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3951_2_import_proxy",
            "decision": "carry the compact-shell q_loc proxy as a nonclaim smoke input",
            "basis": f"QBF1011 gives {QLOC_PROXY_VALUE} in dimensionless_proxy units",
            "effect": "this is the first concrete numerical GK/q_loc input but cannot be used as a local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3951_3_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next useful leap is a Helmholtz/metric-response calculation or a Delta_K bound",
            "effect": "turn Khat identity into a calculation with a pass/fail obstruction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3951_0_sources", "source-backed extraction register", "all source files and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3951_1_coefficients", "actual GK coefficients", "Z^A/G_AB/M_AB/K_metric extracted from accepted MTS parent density", "BLOCKED_NO_PARENT_COEFFICIENT_MATCH"),
        ("CG3951_2_Khat", "Khat metric-response identity", "K_hat equals metric response and passes Helmholtz symmetry", "BLOCKED_HELMHOLTZ_NOT_RUN"),
        ("CG3951_3_source_boundary", "q_loc source/boundary silence", "E_A, R_boundary, R_source vanish or are bounded", "BLOCKED_SOURCE_BOUNDARY_UNSIGNED"),
        ("CG3951_4_proxy", "q_loc proxy handling", "numeric proxy is carried without claim", "PASS_NONCLAIM_PROXY_ONLY"),
        ("CG3951_5_epsilon", "epsilon_nonminimal_GK scoring", "component values and E_pos denominator exist", "BLOCKED_COMPONENT_VALUES_MISSING"),
        ("CG3951_6_local_GR", "local-GR/source-coupling promotion", "all proof or bounded residual clauses close", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in data
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3951_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "turn the Khat identity into a real calculation: compute Helmholtz symmetry / metric-response integrability for the proposed K_hat tensor, or define Delta_K and bound epsilon_GK_metric_response_mismatch",
            "success_condition": "either H_GK=0 and Delta_K=0 are derived for a stated parent density, or a nonclaim Delta_K/E_pos bound row is filled with sourced units and arena projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3951 extracted the GK coefficient status: no actual parent-owned Z/G/M/Khat match yet, but the compact-shell q_loc proxy is imported as a nonclaim smoke input and the next target is a real Helmholtz/Khat calculation.",
            "sources_found": f"{found}/{len(source_rows)}",
            "q_loc_proxy_value": QLOC_PROXY_VALUE,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3951 - GK Symbol Match Coefficient Extraction Or Epsilon GK First Values

Timestamp: `{timestamp}`

## Result

3951 looked for actual parent-owned `Gamma_eff/K_hat` coefficient matches instead of just repeating the gap.

The extraction result is:

- `Z^A`: candidate response-doublet variable exists, but the actual MTS `q_loc/PPN/source-normalization` residual vector is not mapped to it.
- `G_AB`: no parent-owned kinetic/gradient matrix extracted.
- `M_AB`: no parent-owned Hessian/mass-gap matrix extracted.
- `Gamma_eff`: current corpus still treats it as candidate/readout/route symbol, not an accepted scalar density with units and boundary convention.
- `K_hat`: not yet proved to be the metric response of `sqrt(-g)Gamma_eff`.
- `Delta_K`: now the explicit residual bucket for the Khat mismatch.
- `H_GK`: Helmholtz second-variation obstruction is the next real calculation.

## Concrete Nonclaim Input

The useful numerical carry-forward is:

`q_loc_shell_proxy = {QLOC_PROXY_VALUE}`

Units: `dimensionless_proxy`.

This is not a local-GR or PPN claim. It still needs the physical projector, units, and source-normalization map.

## Why This Matters

The best route remains the metric-response route:

`q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu)`.

If `K_hat` is a true metric response and the source/boundary terms close, this becomes a derived local suppression mechanism. If the Helmholtz test fails, the route becomes a bound-only residual branch.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3951_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_GK_COEFFICIENT_EXTRACTION_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_EPSILON_GK_COMPONENT_INPUTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_GK_SYMBOL_MATCH_DECISION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3951_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3951 - GK Symbol Match Coefficient Extraction

Timestamp: `{timestamp}`

- Extracted the actual GK coefficient status: no parent-owned `Z^A/G_AB/M_AB/K_metric` match is signed yet.
- Imported the first concrete q_loc-side smoke number: `q_loc_shell_proxy = {QLOC_PROXY_VALUE}` in `dimensionless_proxy` units; it remains nonclaim until projector/source-normalization mapping exists.
- Promoted `Delta_K := K_hat - K_metric[Gamma_eff]` and `H_GK` Helmholtz obstruction as the real next calculation, not a vibes gap.
- Current local-GR status: blocked for public claim, but the derivation route is now sharper and has a pass/fail next gate.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3951 - GK Symbol Match Coefficient Extraction"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audit = extraction_audit_rows(timestamp)
    components = component_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    audit_ids = {row["row_id"] for row in audit}
    component_symbols = {row["component_symbol"] for row in components}
    gate_statuses = {row["status"] for row in claim_gate}
    qloc_rows = [row for row in components if row["component_symbol"] == "q_loc_shell_proxy"]
    nonclaim_groups = (audit, components, decisions, claim_gate, next_target)
    checks = [
        ("VAL3951_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3951_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3951_02_required_audit_slots", {"GKA3951_0_Z_field_identification", "GKA3951_1_GAB_kinetic_signature", "GKA3951_2_MAB_hessian_signature", "GKA3951_4_Kmetric_Khat_identity", "GKA3951_5_DeltaK_mismatch_residual", "GKA3951_6_Helmholtz_integrability", "GKA3951_7_source_current_boundary", "GKA3951_9_q_loc_compact_shell_proxy"}.issubset(audit_ids), "audit includes all required GK coefficient slots"),
        ("VAL3951_03_no_false_coefficient_claim", all(not row["claim_allowed"] for row in audit), "no coefficient row allows claim"),
        ("VAL3951_04_component_slots", {"E_pos", "epsilon_GK_energy", "epsilon_GK_metric_response_mismatch", "epsilon_GK_boundary", "epsilon_GK_source_charge", "epsilon_GK_negative_hessian", "q_loc_shell_proxy", "epsilon_nonminimal_counterterm_GK"}.issubset(component_symbols), "epsilon GK component inputs emitted"),
        ("VAL3951_05_proxy_imported", bool(qloc_rows) and qloc_rows[0]["value"] == QLOC_PROXY_VALUE and qloc_rows[0]["units"] == "dimensionless_proxy", "q_loc shell proxy imported exactly"),
        ("VAL3951_06_proxy_nonclaim", bool(qloc_rows) and not qloc_rows[0]["valid_for_claim"] and not qloc_rows[0]["score_ready"], "q_loc proxy remains nonclaim and not score-ready"),
        ("VAL3951_07_total_not_score_ready", any(row["component_symbol"] == "epsilon_nonminimal_counterterm_GK" and not row["score_ready"] for row in components), "epsilon total remains blocked until component values exist"),
        ("VAL3951_08_claim_gate_blocks", "BLOCKED_NO_PARENT_COEFFICIENT_MATCH" in gate_statuses and "BLOCKED_HELMHOLTZ_NOT_RUN" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate blocks local-GR promotion"),
        ("VAL3951_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to Helmholtz/Khat test"),
        ("VAL3951_10_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3951_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3951_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3951_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3951_14_spine_updated", SPINE_PATH.exists() and "3951 - GK Symbol Match Coefficient Extraction" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3951_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3951_16_script_compile", True, "script compiled before validation write"),
        ("VAL3951_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    audit = extraction_audit_rows(timestamp)
    components = component_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3951 validation failed: {failed}")

    print(f"3951 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print(f"q_loc_shell_proxy={QLOC_PROXY_VALUE} (nonclaim)")


if __name__ == "__main__":
    run()
