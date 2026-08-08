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

DOC = ROOT / "2845-Y5-R2FR-CAB-source-current-identity-or-finite-amplitude-inputs-under-AX1090.md"

SRC_2844_DOC = ROOT / "2844-Y5-R2FR-CAB-one-over-r-amplitude-law-or-parent-cancellation-theorem-under-AX1090.md"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_NEXT = RESIDUALS / "P8_Y5_R2FR_2844_NEXT_TARGET.csv"
SRC_2844_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2844_VALIDATION.csv"
SRC_11 = ROOT / "11-cell-current-origin-attempt.md"
SRC_1884 = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_1063 = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_1008 = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
SRC_1268 = ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2845_SOURCE_REGISTER.csv",
    "identity_audit": RESIDUALS / "P8_Y5_R2FR_2845_SOURCE_CURRENT_IDENTITY_AUDIT.csv",
    "no_go": RESIDUALS / "P8_Y5_R2FR_2845_CONSERVATION_NO_GO_LEDGER.csv",
    "owner_contract": RESIDUALS / "P8_Y5_R2FR_2845_PARENT_CURRENT_OWNER_CONTRACT.csv",
    "finite_inputs": RESIDUALS / "P8_Y5_R2FR_2845_FINITE_AMPLITUDE_INPUT_ROWS.csv",
    "route_split": RESIDUALS / "P8_Y5_R2FR_2845_ROUTE_SPLIT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2845_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2845_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2845_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2845_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2845_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_inputs_copy": LOCAL_BOUNDS / "RAB_CAB_finite_amplitude_inputs_2845_NONCLAIM.csv",
    "identity_copy": SOURCE_WEIGHT / "RAB_CAB_source_current_identity_audit_2845_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2845_current_owner_or_finite_local_inputs_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_CAB_SOURCE_CURRENT_IDENTITY_2845_NONCLAIM.csv",
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
        ("SRC2845_0_2844_doc", SRC_2844_DOC, "Q_CAB = -sigma_R*q_R_eff;VAL2844_OVERALL", "2844 charge-balance target"),
        ("SRC2845_1_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "2844 flux identity table"),
        ("SRC2845_2_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;MISSING_SOURCE_CURRENT_IDENTITY", "2844 missing parent contract"),
        ("SRC2845_3_2844_next", SRC_2844_NEXT, "NEXT2844_0_2845", "2844 handoff to current identity"),
        ("SRC2845_4_2844_validation", SRC_2844_VALIDATION, "VAL2844_OVERALL", "2844 validation"),
        ("SRC2845_5_11", SRC_11, "Q_R = constant.;Q_R = 0.;But that theorem is not currently derived.", "cell-current no-charge obstruction"),
        ("SRC2845_6_1884", SRC_1884, "NBC1884_1_exact_zero_flux_lemma;NBC1884_4_no_boundary_charge_parent_signature;SDM1884_2_source_silence", "zero-flux lemma and missing source silence"),
        ("SRC2845_7_1063", SRC_1063, "THM1063_5_verdict;NO1063_2_Noether_current_owner", "Noether/current owner missing"),
        ("SRC2845_8_1078", SRC_1078, "CURRENT_OWNER_NOT_SIGNED;CEK1078_1_current_rescaling", "current rescaling counterexample"),
        ("SRC2845_9_1008", SRC_1008, "PVA1008_4_Noether_identity_limit;ownership_not_zero_theorem", "Noether identity does not prove zero residual current"),
        ("SRC2845_10_1268", SRC_1268, "VAR1268_1_E_R;need J_R=0, boundary zero, and readout-regeneration zero", "R_AB source silence requirement"),
    ]
    return [source_row(*spec) for spec in specs]


def identity_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ID2845_0_target_identity",
            "Q_CAB+sigma_R*q_R_eff=0",
            "needed to cancel the one-over-r local gamma residual",
            "TARGET_EXACT_FROM_2844",
            "mathematically exact as a condition; not proven by parent action",
            True,
            False,
        ),
        (
            "ID2845_1_current_conservation",
            "dJ=0 or partial_r(W partial_r C)=0 outside sources",
            "conserves the exterior charge",
            "INSUFFICIENT",
            "conservation gives Q=constant, not Q=0 or Q_CAB=-sigma_R*q_R_eff",
            True,
            False,
        ),
        (
            "ID2845_2_noether_ward",
            "dJ=-E_A delta Phi^A + boundary terms",
            "assigns ownership of charge flow on shell",
            "INSUFFICIENT",
            "Noether/Ward identities do not kill retained source, boundary, projector or readout pieces",
            True,
            False,
        ),
        (
            "ID2845_3_current_owner",
            "one parent current owner fixes Q_CAB and q_R_eff normalization",
            "would make the charge-balance identity meaningful and non-tunable",
            "MISSING",
            "1063/1078 mark the current owner as candidate-missing/not signed",
            False,
            False,
        ),
        (
            "ID2845_4_boundary_source_silence",
            "ordinary sources and boundary terms carry no independent reciprocal charge",
            "would prevent exterior hair from surviving",
            "MISSING",
            "1884 keeps Q_R=0 as a missing parent theorem",
            False,
            False,
        ),
        (
            "ID2845_5_verdict",
            "derive Q_CAB+sigma_R*q_R_eff=0 from existing corpus",
            "direct derivation attempt",
            "NOT_DERIVED",
            "existing current machinery gives a contract/no-go, not the needed identity",
            False,
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "identity_id": identity_id,
                "object": obj,
                "role": role,
                "status": status,
                "reason": reason,
                "formal_condition_known": condition_known,
                "parent_identity_closed": closed,
                "control_only": True,
            }
        )
        for identity_id, obj, role, status, reason, condition_known, closed in specs
    ]


def no_go_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NOGO2845_0_constant_not_zero",
            "J conserved",
            "Q is constant in the exterior",
            "Q value remains an integration/source/boundary datum",
            "cannot infer local GR suppression",
        ),
        (
            "NOGO2845_1_noether_not_zero",
            "Noether/Ward identity",
            "charge is owned by a symmetry/current",
            "retained C-terms, boundary terms and source pieces can be nonzero",
            "cannot infer Q_CAB=-sigma_R*q_R_eff",
        ),
        (
            "NOGO2845_2_rescaling_counterexample",
            "J_A -> c_A J_A",
            "conserved currents remain conserved after allowed normalization changes",
            "relative source weights survive unless one current/source owner fixes normalization",
            "cancellation can be spoiled without violating conservation",
        ),
        (
            "NOGO2845_3_independent_charge_counterexample",
            "Q_CAB and q_R_eff sourced by different parent slots",
            "each charge can be conserved",
            "their sum is not forced to vanish",
            "finite amplitude rows are mandatory if owner theorem fails",
        ),
    ]
    return [
        nonclaim(
            {
                "nogo_id": nogo_id,
                "assumption": assumption,
                "what_it_proves": proves,
                "what_it_does_not_prove": not_prove,
                "impact": impact,
                "counterexample_survives": True,
                "control_only": True,
            }
        )
        for nogo_id, assumption, proves, not_prove, impact in specs
    ]


def owner_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("OWNER2845_0_parent_action", "single parent action varied in one convention", "must define both target-map source and delta_R source", "MISSING_PARENT_ACTION_OWNER"),
        ("OWNER2845_1_current_owner", "one Noether/Hilbert/source current owner", "prevents independent rescaling of Q_CAB and q_R_eff", "MISSING_CURRENT_OWNER"),
        ("OWNER2845_2_charge_balance", "parent identity Q_CAB+sigma_R*q_R_eff=0", "actual amplitude cancellation theorem", "MISSING_CHARGE_BALANCE_IDENTITY"),
        ("OWNER2845_3_boundary", "boundary/corner flux either zero or part of Q_CAB", "prevents hidden exterior hair", "MISSING_BOUNDARY_CHARGE_THEOREM"),
        ("OWNER2845_4_source_silence", "ordinary compact sources carry no independent reciprocal charge beyond the owned source", "prevents matter-source leakage", "MISSING_SOURCE_SILENCE"),
        ("OWNER2845_5_readout", "readout/projection does not regenerate representative dependence", "prevents local observable leakage after current identity", "MISSING_READOUT_STABILITY"),
        ("OWNER2845_6_normalization", "same measured-GM/source convention for Q_CAB and q_R_eff", "prevents a formal cancellation in wrong units", "MISSING_NORMALIZATION"),
    ]
    return [
        nonclaim(
            {
                "owner_id": owner_id,
                "required_clause": clause,
                "why_needed": why,
                "current_status": status,
                "closed": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for owner_id, clause, why, status in specs
    ]


def finite_input_rows() -> list[dict[str, Any]]:
    specs = [
        ("FIN2845_0_Q_CAB", "Q_CAB", "target-map monopole charge", "charge", "MISSING_NUMERIC_OR_THEOREM", "derive owner identity or fill finite value with source path"),
        ("FIN2845_1_q_R_eff", "q_R_eff", "delta_R Green charge", "charge", "MISSING_NUMERIC_OR_THEOREM", "derive source normalization or fill finite value"),
        ("FIN2845_2_sigma_R", "sigma_R", "Green sign convention", "dimensionless sign", "MISSING_SIGN", "source from parent action"),
        ("FIN2845_3_boundary_flux", "B_CAB/B_R", "boundary/corner charge contribution", "charge", "MISSING_BOUNDARY_INPUT", "prove zero or include in amplitude"),
        ("FIN2845_4_units", "shared charge units", "common convention for Q_CAB and q_R_eff", "unit map", "MISSING_UNIT_MAP", "write common Green/GM normalization"),
        ("FIN2845_5_PPN_vector", "full local residual vector", "gamma, beta, preferred-frame, clock, endpoint and source channels", "dimensionless vector", "MISSING_ARENA_PROJECTION", "do not claim gamma-only cancellation"),
    ]
    return [
        nonclaim(
            {
                "finite_id": finite_id,
                "quantity": quantity,
                "description": desc,
                "units_or_type": units,
                "current_status": status,
                "next_action": action,
                "accepted_ready": False,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for finite_id, quantity, desc, units, status, action in specs
    ]


def route_split_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE2845_0_owner_theorem",
            "derive one parent current/source owner and charge-balance identity",
            "BEST_DERIVATION_ROUTE_BUT_OPEN",
            "this is the only non-tuning way to turn the amplitude cancellation into a theorem",
            True,
        ),
        (
            "ROUTE2845_1_zero_flux",
            "prove Q_R=0 via no-boundary-charge/source descent",
            "PARALLEL_ZERO_ROUTE_OPEN",
            "1884 gives an exact lemma but the parent zero theorem is unsigned",
            False,
        ),
        (
            "ROUTE2845_2_finite_local_inputs",
            "fill finite Q_CAB, q_R_eff, boundary and full PPN rows",
            "FALLBACK_REQUIRED_IF_OWNER_FAILS",
            "needed for actual testing if no theorem closes",
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


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    specs = [
        ("GATE2845_0_sources", "source-anchor control", all(row["path_exists"] and row["anchors_found"] for row in rows["sources"]), "source anchors for this checkpoint exist"),
        ("GATE2845_1_identity_condition", "formal charge-balance condition", True, "condition is known from 2844 but not parent-derived"),
        ("GATE2845_2_parent_identity", "parent source-current identity", False, "Q_CAB+sigma_R*q_R_eff=0 not derived"),
        ("GATE2845_3_finite_inputs", "finite local amplitude inputs", False, "finite source rows remain missing/nonclaim"),
        ("GATE2845_4_local_claim", "local GR/Newton/PPN claim", False, "no owner theorem, no finite rows, no full-vector closure"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": False,
                "status": "CONTROL_OR_FORMAL_PASS_NONCLAIM" if control_passed and gate_id in {"GATE2845_0_sources", "GATE2845_1_identity_condition"} else "BLOCKED",
                "reason": reason,
                "control_check_passed": control_passed,
            }
        )
        for gate_id, claim, control_passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2845_0_main_result",
            "Current conservation does not derive the needed cancellation identity.",
            "NO_GO_RECORDED",
            "it fixes constancy of charge, not the value or relative normalization of two charges",
            "do not claim local suppression from conservation alone",
        ),
        (
            "DEC2845_1_best_route",
            "The missing object is a single parent current/source owner.",
            "SELECTED",
            "without it, Q_CAB and q_R_eff can be independently normalized or sourced",
            "target owner theorem or finite inputs next",
        ),
        (
            "DEC2845_2_fallback",
            "Finite local inputs are now explicitly defined.",
            "READY_AS_NONCLAIM_FALLBACK",
            "if the owner theorem fails, the framework has a concrete data/source pack to fill",
            "fill Q_CAB/q_R_eff/boundary/full-vector rows only with real sources",
        ),
        (
            "DEC2845_3_no_claim",
            "No local-GR/Newton/PPN/R10/WEP/clock/orbital claim.",
            "LOCKED",
            "all proof-critical owner/source rows remain missing",
            "keep private",
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
                "next_id": "NEXT2845_0_2846",
                "status": "selected_primary",
                "target_doc": "2846-Y5-R2FR-parent-current-owner-or-finite-local-PPN-input-contract-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_current_owner_or_finite_local_PPN_input_contract_under_AX1090_2846.py",
                "mission": "attempt the narrow parent current-owner theorem for Q_CAB and q_R_eff; if it fails, stage the finite local PPN input contract without treating conservation as local-GR evidence",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2845_0_finite_inputs", OUTPUTS["finite_inputs"], BRANCH_OUTPUTS["finite_inputs_copy"], "portable nonclaim finite amplitude input rows"),
        ("COPY2845_1_identity_audit", OUTPUTS["identity_audit"], BRANCH_OUTPUTS["identity_copy"], "portable source-current identity audit"),
        ("COPY2845_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2845_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
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
        "parent_identity_closed",
        "closed",
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
        ("VAL2845_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2845_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2845_2_identity_not_closed", not any(row["parent_identity_closed"] for row in rows_by_name["identity_audit"]), "parent source-current identity remains unclaimed"),
        ("VAL2845_3_no_go_recorded", any(row["nogo_id"] == "NOGO2845_0_constant_not_zero" and row["counterexample_survives"] for row in rows_by_name["no_go"]), "conservation-not-zero no-go recorded"),
        ("VAL2845_4_owner_contract_blocked", not any(row["closed"] for row in rows_by_name["owner_contract"]), "parent current-owner contract clauses remain open"),
        ("VAL2845_5_finite_inputs_blocked", not any(row["accepted_ready"] for row in rows_by_name["finite_inputs"]), "finite amplitude rows remain unaccepted"),
        ("VAL2845_6_next_target_2846", any(row["next_id"] == "NEXT2845_0_2846" and row["selected"] for row in rows_by_name["next"]), "2846 current-owner/finite-input target selected"),
        ("VAL2845_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2845_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2845_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2845_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2845_11_no_claim_flags", no_claim_flags(rows_by_name), "no source/claim/closed flags are true"),
        ("VAL2845_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2845_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2845_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2845_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2845_OVERALL",
            "passed": overall,
            "detail": "2845 confirms current conservation/Noether ownership is not enough to derive Q_CAB+sigma_R*q_R_eff=0, records the current-owner contract, and stages finite local amplitude rows as nonclaim fallback.",
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
    content = f"""# 2845 - Y5 R2FR C_AB Source-Current Identity Or Finite Amplitude Inputs Under AX1090

Status: `Y5_R2FR_2845_current_conservation_no_go_parent_owner_missing_finite_inputs_staged_nonclaim`

## Private Verdict

2845 tests the hoped-for parent identity:

```text
Q_CAB + sigma_R*q_R_eff = 0
```

This would close the 2844 one-over-r cancellation condition. Current evidence does **not** derive it.

The core no-go is simple and important:

```text
current conservation -> Q is constant
current conservation -/-> Q has the required value
```

Noether/Ward structure helps assign ownership, but the existing corpus still leaves source, boundary, projector, readout, and normalization pieces unsigned. The source-current owner problem from 1063/1078 survives here in sharper form: without one parent owner, `Q_CAB` and `q_R_eff` can be independently normalized or independently sourced.

So this is not grim, but it is strict: local GR suppression is now reduced to one missing structural theorem or to finite local amplitude inputs. That is progress; the target stopped being foggy.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Source-Current Identity Audit

{markdown_table(rows["identity_audit"], ["identity_id", "object", "status", "reason", "formal_condition_known", "parent_identity_closed", "valid_for_claim"])}

## Conservation No-Go Ledger

{markdown_table(rows["no_go"], ["nogo_id", "assumption", "what_it_proves", "what_it_does_not_prove", "impact", "counterexample_survives", "valid_for_claim"])}

## Parent Current Owner Contract

{markdown_table(rows["owner_contract"], ["owner_id", "required_clause", "current_status", "why_needed", "closed", "valid_for_claim"])}

## Finite Amplitude Input Rows

{markdown_table(rows["finite_inputs"], ["finite_id", "quantity", "units_or_type", "current_status", "next_action", "accepted_ready", "valid_for_claim"])}

## Route Split

{markdown_table(rows["route_split"], ["route_id", "route", "status", "reason", "selected_for_next_work", "selected_for_claim", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

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
    rows["identity_audit"] = identity_audit_rows()
    rows["no_go"] = no_go_rows()
    rows["owner_contract"] = owner_contract_rows()
    rows["finite_inputs"] = finite_input_rows()
    rows["route_split"] = route_split_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "identity_audit", "no_go", "owner_contract", "finite_inputs", "route_split", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2845_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2845_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
