from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2846-Y5-R2FR-parent-current-owner-or-finite-local-PPN-input-contract-under-AX1090.md"

SRC_2845_DOC = ROOT / "2845-Y5-R2FR-CAB-source-current-identity-or-finite-amplitude-inputs-under-AX1090.md"
SRC_2845_OWNER = RESIDUALS / "P8_Y5_R2FR_2845_PARENT_CURRENT_OWNER_CONTRACT.csv"
SRC_2845_FINITE = RESIDUALS / "P8_Y5_R2FR_2845_FINITE_AMPLITUDE_INPUT_ROWS.csv"
SRC_2845_NEXT = RESIDUALS / "P8_Y5_R2FR_2845_NEXT_TARGET.csv"
SRC_2845_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2845_VALIDATION.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_1063 = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_1884 = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_1268 = ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md"
SRC_1882 = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2846_SOURCE_REGISTER.csv",
    "owner_theorem": RESIDUALS / "P8_Y5_R2FR_2846_NARROW_PARENT_CURRENT_OWNER_THEOREM.csv",
    "counterexample": RESIDUALS / "P8_Y5_R2FR_2846_RESCALING_COUNTEREXAMPLE_AUDIT.csv",
    "ppn_contract": RESIDUALS / "P8_Y5_R2FR_2846_FINITE_LOCAL_PPN_INPUT_CONTRACT.csv",
    "formula_pack": RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv",
    "claim_matrix": RESIDUALS / "P8_Y5_R2FR_2846_CLAIM_READINESS_MATRIX.csv",
    "route_split": RESIDUALS / "P8_Y5_R2FR_2846_ROUTE_SPLIT.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2846_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2846_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2846_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2846_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ppn_contract_copy": LOCAL_BOUNDS / "RAB_CAB_finite_local_PPN_input_contract_2846_NONCLAIM.csv",
    "owner_theorem_copy": SOURCE_WEIGHT / "RAB_parent_current_owner_theorem_2846_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2846_finite_local_PPN_bound_map_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_PARENT_CURRENT_OWNER_OR_FINITE_PPN_2846_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2846_0_2845_doc", SRC_2845_DOC, "NEXT2845_0_2846;VAL2845_OVERALL", "2845 selected parent-current-owner or finite PPN contract"),
        ("SRC2846_1_2845_owner", SRC_2845_OWNER, "OWNER2845_1_current_owner;MISSING_CURRENT_OWNER", "2845 owner contract"),
        ("SRC2846_2_2845_finite", SRC_2845_FINITE, "FIN2845_0_Q_CAB;FIN2845_5_PPN_vector", "2845 finite amplitude inputs"),
        ("SRC2846_3_2845_next", SRC_2845_NEXT, "NEXT2845_0_2846", "2845 next-target row"),
        ("SRC2846_4_2845_validation", SRC_2845_VALIDATION, "VAL2845_OVERALL", "2845 validation"),
        ("SRC2846_5_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "2844 exact charge-balance condition"),
        ("SRC2846_6_1063", SRC_1063, "THM1063_5_verdict;NO1063_2_Noether_current_owner", "source-label/current owner remains conditional"),
        ("SRC2846_7_1078", SRC_1078, "CURRENT_OWNER_NOT_SIGNED;CEK1078_1_current_rescaling", "current-rescaling counterexample"),
        ("SRC2846_8_1884", SRC_1884, "NBC1884_1_exact_zero_flux_lemma;NBC1884_4_no_boundary_charge_parent_signature;SDM1884_2_source_silence", "zero-flux lemma and missing source silence"),
        ("SRC2846_9_1268", SRC_1268, "VAR1268_1_E_R;PASS_ONLY_IF_SOURCES_ZERO", "R_AB matter/boundary/readout source silence requirement"),
        ("SRC2846_10_1882", SRC_1882, "C_R = R_AB = ln(T^2 S);C_R = 2(p-1)u", "C_R to PPN residual identity"),
    ]
    return [source_row(*spec) for spec in specs]


def owner_theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "THEO2846_0_conditional_statement",
            "If one parent current J_* owns both Q_CAB and q_R_eff, and the projections obey Q_CAB=-sigma_R*q_R_eff with common Green normalization and zero boundary flux, then the local 1/r gamma residual vanishes.",
            "EXACT_CONDITIONAL_THEOREM",
            "formal theorem statement is valid but premises are not parent-signed",
            True,
            False,
        ),
        (
            "THEO2846_1_single_parent_action",
            "same parent action varied in one convention produces both target-map and delta_R source equations",
            "MISSING",
            "no source path currently supplies this combined variation",
            False,
            False,
        ),
        (
            "THEO2846_2_single_current_owner",
            "one Noether/Hilbert/source current owner fixes the charge unit",
            "MISSING",
            "1063 and 1078 leave the current owner candidate-missing/not signed",
            False,
            False,
        ),
        (
            "THEO2846_3_opposite_projection",
            "P_CAB[J_*] = -sigma_R P_delta[J_*]",
            "MISSING",
            "this is the actual source-current identity required for Q_CAB+sigma_R*q_R_eff=0",
            False,
            False,
        ),
        (
            "THEO2846_4_no_rescaling_slot",
            "no legal J_* -> c J_* or independent source-only coefficient survives",
            "FAILED_CURRENT_CORPUS",
            "1078 records a current rescaling counterexample unless the owner theorem is signed",
            False,
            False,
        ),
        (
            "THEO2846_5_boundary_source_readout",
            "boundary, ordinary-source and readout regeneration terms vanish or are included in the same owned charge",
            "MISSING",
            "1884 and 1268 leave these clauses unsigned",
            False,
            False,
        ),
        (
            "THEO2846_6_verdict",
            "narrow parent current-owner theorem for local GR gamma suppression",
            "NOT_DERIVED",
            "the theorem is now exact as a contract, but the current corpus does not prove its premises",
            True,
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "theorem_id": theorem_id,
                "statement_or_clause": statement,
                "status": status,
                "reason": reason,
                "conditional_theorem_recorded": conditional,
                "parent_theorem_closed": closed,
                "control_only": True,
            }
        )
        for theorem_id, statement, status, reason, conditional, closed in specs
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CE2846_0_current_rescaling",
            "J_* -> c J_*",
            "Both charge definitions rescale unless one current owner and measurement convention are fixed.",
            "SURVIVES",
            "breaks a claimed amplitude identity without breaking conservation",
        ),
        (
            "CE2846_1_independent_source_slots",
            "Q_CAB and q_R_eff come from distinct parent source slots",
            "Each can be conserved and source-backed while their sum is nonzero.",
            "SURVIVES",
            "prevents treating Q_CAB+sigma_R*q_R_eff=0 as automatic",
        ),
        (
            "CE2846_2_boundary_hair",
            "boundary/corner flux contributes to Q_CAB or R_AB charge",
            "The exterior 1/r amplitude shifts even with a clean bulk current.",
            "SURVIVES",
            "requires boundary theorem or finite boundary row",
        ),
        (
            "CE2846_3_readout_regeneration",
            "readout/EFT map regenerates representative dependence",
            "A parent-level current cancellation can leak back into local observables.",
            "SURVIVES",
            "requires readout stability and full-vector PPN map",
        ),
    ]
    return [
        nonclaim(
            {
                "counterexample_id": counter_id,
                "counterexample": counterexample,
                "effect": effect,
                "status": status,
                "claim_impact": impact,
                "counterexample_survives": True,
                "control_only": True,
            }
        )
        for counter_id, counterexample, effect, status, impact in specs
    ]


def ppn_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPN2846_0_branch_selector", "branch_selector", "one of parent_owner_theorem or finite_input_branch", "enum", "MISSING_BRANCH_CLOSURE", "must choose theorem evidence or finite numeric/source rows"),
        ("PPN2846_1_Q_CAB", "Q_CAB", "target-map monopole charge in shared Green convention", "charge", "MISSING_NUMERIC_OR_THEOREM", "source path plus units or parent owner theorem"),
        ("PPN2846_2_q_R_eff", "q_R_eff", "delta_R Green charge in same convention", "charge", "MISSING_NUMERIC_OR_THEOREM", "source path plus units or parent owner theorem"),
        ("PPN2846_3_sigma_R", "sigma_R", "parent Green sign convention", "dimensionless sign", "MISSING_SIGN", "derive from action or cite source row"),
        ("PPN2846_4_A_total", "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)", "net 1/r reciprocal amplitude", "charge", "MISSING_COMPUTABLE_INPUTS", "computed only after Q_CAB/q_R_eff/sigma_R are real"),
        ("PPN2846_5_delta_p", "delta_p_const=c^2*A_total/(2*G*M_source)", "first PPN spatial-curvature residual", "dimensionless", "MISSING_GM_CONVENTION", "requires measured GM/source convention"),
        ("PPN2846_6_q_R_hat", "q_R_hat_const=-c^2*A_total/(G*M_source)", "R-channel dimensionless PPN bridge variable", "dimensionless", "MISSING_GM_CONVENTION", "must match delta_p=-q_R_hat/2"),
        ("PPN2846_7_tail", "C_AB_reg,H_R,finite_range", "regular/tail/range corrections across local arenas", "profile functions", "MISSING_PROFILE_BOUNDS", "prove PPN-silent or include in residual vector"),
        ("PPN2846_8_full_vector", "full_PPN_residual_vector", "beta, gamma, preferred-frame, clock, endpoint, source normalization", "dimensionless vector", "MISSING_ARENA_PROJECTION", "gamma-only pass forbidden"),
        ("PPN2846_9_source_paths", "source_paths", "local file/source anchor for every nonzero/theorem value", "path+anchor", "MISSING_SOURCE_PATHS", "no placeholder or comparator-only rows"),
    ]
    return [
        nonclaim(
            {
                "input_id": input_id,
                "quantity": quantity,
                "role": role,
                "units_or_type": units,
                "current_status": status,
                "acceptance_gate": gate,
                "accepted_ready": False,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for input_id, quantity, role, units, status, gate in specs
    ]


def formula_pack_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FORM2846_0_A_total",
            "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
            "net local 1/r amplitude after target-map plus finite Green contribution",
            "DERIVED_SYMBOLIC_NONCLAIM",
        ),
        (
            "FORM2846_1_delta_p",
            "delta_p_const=c^2*A_total/(2*G*M_source)",
            "constant-limit gamma/spatial-curvature PPN residual",
            "DERIVED_CONDITIONAL_NONCLAIM",
        ),
        (
            "FORM2846_2_qRhat",
            "q_R_hat_const=-c^2*A_total/(G*M_source)",
            "dimensionless q_R_hat bridge with target-map correction",
            "DERIVED_CONDITIONAL_NONCLAIM",
        ),
        (
            "FORM2846_3_theorem_zero",
            "if Q_CAB=-sigma_R*q_R_eff and tails/full-vector channels close, then A_total=delta_p=q_R_hat=0",
            "local gamma branch theorem-zero condition",
            "EXACT_CONDITIONAL_NONCLAIM",
        ),
        (
            "FORM2846_4_finite_score_rule",
            "finite rows can be tested only after A_total, tail terms, GM convention and full vector are source-backed",
            "future empirical gate",
            "RULE_NONCLAIM",
        ),
    ]
    return [
        nonclaim(
            {
                "formula_id": formula_id,
                "formula": formula,
                "role": role,
                "status": status,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for formula_id, formula, role, status in specs
    ]


def claim_matrix_rows() -> list[dict[str, Any]]:
    specs = [
        ("CLAIM2846_0_parent_owner", "parent current-owner theorem", "BLOCKED", "owner, opposite projection, boundary/source/readout and normalization clauses are unsigned"),
        ("CLAIM2846_1_gamma_zero", "gamma/local 1/r residual zero", "BLOCKED", "A_total zero condition is known but not parent-signed or numerically sourced"),
        ("CLAIM2846_2_local_GR", "local GR / Newton limit", "BLOCKED", "full PPN vector, measured-GM convention, and non-gamma channels remain open"),
        ("CLAIM2846_3_finite_testing", "finite local PPN testing", "NOT_READY", "contract exists but rows are missing numeric/source-backed inputs"),
        ("CLAIM2846_4_private_progress", "private derivation progress", "PASS_NONCLAIM", "missing theorem is narrowed to a current-owner/opposite-projection contract"),
    ]
    return [
        nonclaim(
            {
                "claim_id": claim_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_check_passed": status == "PASS_NONCLAIM",
                "control_only": True,
            }
        )
        for claim_id, claim, status, reason in specs
    ]


def route_split_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE2846_0_owner_theorem",
            "prove the parent current owner plus opposite projection identity",
            "BEST_THEOREM_ROUTE_BUT_BLOCKED",
            "would derive local suppression without finite tuning, but present corpus does not sign it",
            False,
        ),
        (
            "ROUTE2846_1_finite_ppn_contract",
            "fill finite local PPN input contract and dry-run bound map",
            "SELECTED_NEXT",
            "moves toward testing while preserving the theorem route as a possible future closure",
            True,
        ),
        (
            "ROUTE2846_2_zero_flux_route",
            "prove Q_R=0 no-boundary/source-silence theorem",
            "PARALLEL_OPEN_ROUTE",
            "exact conditional lemma exists in 1884, but parent theorem is unsigned",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "route": route,
                "status": status,
                "reason": reason,
                "selected_for_next_work": selected,
                "selected_for_claim": False,
            }
        )
        for route_id, route, status, reason, selected in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2846_0_theorem_result",
            "Do not claim the parent-current-owner theorem.",
            "BLOCKED_NOT_SIGNED",
            "the exact theorem contract is written, but the current owner and opposite projection identity are missing",
            "keep as derivation target, not evidence",
        ),
        (
            "DEC2846_1_finite_contract",
            "Promote finite local PPN input contract to next work item.",
            "SELECTED",
            "this gets us closer to testing without pretending the derivation has closed",
            "build bound-map/dry-run checkpoint",
        ),
        (
            "DEC2846_2_rescaling_guard",
            "Keep the current-rescaling counterexample active.",
            "LOCKED",
            "otherwise the cancellation could be a convention artifact rather than physics",
            "require source owner or explicit unit map",
        ),
        (
            "DEC2846_3_no_claim",
            "No local-GR/Newton/PPN/R10/WEP/clock/orbital claim.",
            "LOCKED",
            "the branch is now disciplined but not closed",
            "private work only",
        ),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": action,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2846_0_2847",
                "status": "selected_primary",
                "target_doc": "2847-Y5-R2FR-finite-local-PPN-bound-map-dry-run-or-current-owner-retry-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_local_PPN_bound_map_dry_run_or_current_owner_retry_under_AX1090_2847.py",
                "mission": "turn the finite local PPN input contract into a dry-run bound map for A_total, delta_p, q_R_hat and full-vector gates, while keeping parent-owner theorem rows nonclaim unless sourced",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2846_0_ppn_contract", OUTPUTS["ppn_contract"], BRANCH_OUTPUTS["ppn_contract_copy"], "portable finite local PPN input contract"),
        ("COPY2846_1_owner_theorem", OUTPUTS["owner_theorem"], BRANCH_OUTPUTS["owner_theorem_copy"], "portable parent current-owner theorem audit"),
        ("COPY2846_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2846_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(src),
                    "copy_path": str(dst),
                    "purpose": purpose,
                    "exists": dst.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_ready",
        "parent_theorem_closed",
        "source_backed",
        "selected_for_claim",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "numeric_prediction", "alpha_predicted", "predicted_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2846_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2846_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2846_2_conditional_theorem_recorded", any(row["theorem_id"] == "THEO2846_0_conditional_statement" and row["conditional_theorem_recorded"] for row in rows_by_name["owner_theorem"]), "conditional owner theorem statement recorded"),
        ("VAL2846_3_parent_theorem_not_closed", not any(row["parent_theorem_closed"] for row in rows_by_name["owner_theorem"]), "parent-current-owner theorem remains unclaimed"),
        ("VAL2846_4_counterexamples_survive", all(row["counterexample_survives"] for row in rows_by_name["counterexample"]), "rescaling/boundary/readout counterexamples remain active"),
        ("VAL2846_5_ppn_contract_blocked", not any(row["accepted_ready"] for row in rows_by_name["ppn_contract"]), "finite local PPN contract remains unaccepted"),
        ("VAL2846_6_next_target_2847", any(row["next_id"] == "NEXT2846_0_2847" and row["selected"] for row in rows_by_name["next"]), "2847 finite local PPN dry-run target selected"),
        ("VAL2846_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2846_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2846_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2846_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2846_11_no_claim_flags", no_claim_flags(rows_by_name), "no source/claim flags are true"),
        ("VAL2846_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2846_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2846_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2846_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2846_OVERALL",
            "passed": overall,
            "detail": "2846 writes the exact parent-current-owner theorem contract, keeps it unclaimed because owner/opposite-projection/boundary/source/readout clauses are unsigned, and selects a finite local PPN bound-map dry run next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2846 - Y5 R2FR Parent Current Owner Or Finite Local PPN Input Contract Under AX1090

Status: `Y5_R2FR_2846_parent_owner_theorem_contract_written_not_signed_finite_PPN_contract_selected_nonclaim`

## Private Verdict

2846 narrows the derivation route as far as the current evidence allows.

The exact conditional theorem is:

```text
If one parent current J_* owns both Q_CAB and q_R_eff,
and the source projections obey Q_CAB = -sigma_R*q_R_eff,
with common Green normalization, zero boundary flux, source silence,
and readout stability,
then A_total=delta_p=q_R_hat=0 in the local 1/r gamma branch.
```

That is a real theorem contract. It is not yet a theorem of MTS, because the corpus still does not sign the parent current owner, the opposite projection identity, the no-rescaling rule, boundary/source silence, or the full local readout map.

So the next honest move is a finite local PPN input dry run. Not because we are giving up on derivation, but because this lets the theory face the local-GR gate with explicit inputs while the owner theorem remains an open derivation target.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Narrow Parent Current Owner Theorem

{markdown_table(rows["owner_theorem"], ["theorem_id", "statement_or_clause", "status", "reason", "conditional_theorem_recorded", "parent_theorem_closed", "valid_for_claim"])}

## Rescaling Counterexample Audit

{markdown_table(rows["counterexample"], ["counterexample_id", "counterexample", "status", "claim_impact", "counterexample_survives", "valid_for_claim"])}

## Finite Local PPN Input Contract

{markdown_table(rows["ppn_contract"], ["input_id", "quantity", "units_or_type", "current_status", "acceptance_gate", "accepted_ready", "valid_for_claim"])}

## Local PPN Formula Pack

{markdown_table(rows["formula_pack"], ["formula_id", "formula", "status", "role", "valid_for_claim"])}

## Claim Readiness Matrix

{markdown_table(rows["claim_matrix"], ["claim_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Route Split

{markdown_table(rows["route_split"], ["route_id", "route", "status", "reason", "selected_for_next_work", "selected_for_claim", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["owner_theorem"] = owner_theorem_rows()
    rows["counterexample"] = counterexample_rows()
    rows["ppn_contract"] = ppn_contract_rows()
    rows["formula_pack"] = formula_pack_rows()
    rows["claim_matrix"] = claim_matrix_rows()
    rows["route_split"] = route_split_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "owner_theorem", "counterexample", "ppn_contract", "formula_pack", "claim_matrix", "route_split", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2846_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2846_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
