from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1580"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1580-Y5-RAB-PPN-residual-vector-or-qRhat-source-row.md"

SOURCE_FILES = {
    "1579_doc": ROOT / "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md",
    "1579_validation": OUT / "P8_Y5_BRR545_1579_VALIDATION.csv",
    "1579_acquisition": OUT / "P8_Y5_PARENT_QLOC_1579_COMPONENT_SOURCE_ACQUISITION_LEDGER.csv",
    "1579_external": OUT / "P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv",
    "1579_dry_run": OUT / "P8_Y5_PARENT_QLOC_1579_COMPARATOR_DRY_RUN.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "1577_doc": ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1579_doc": ["NEXT_1580_RAB_PPN_RESIDUAL_VECTOR_OR_QRHAT_SOURCE_ROW", "gamma_minus_1=C_QR q_R_hat+tails"],
    "1579_validation": ["VAL1579_OVERALL", "PASS"],
    "1579_acquisition": ["ACQ1579_8_tau_PPN", "MISSING_PPN_PROJECTION"],
    "1579_external": ["EXT1579_1_PPN", "upper_bound=2.3e-05 dimensionless"],
    "1579_dry_run": ["DRY1579_1_PPN", "INTERNAL_PROJECTION_MISSING"],
    "05_reciprocity": ["R_AB = ln(A B) = ln(T^2 S).", "W R_AB' = Q_R."],
    "10_observer": ["R_AB = ln(T^2 S) = 2 ln(J_q).", "gamma - 1 = 0 after R_AB=0."],
    "1577_doc": ["W_R partial_r R_AB=Q_R", "FINITE_COMPONENT_BOUND_FILL_STARTED_NONCLAIM"],
    "local_bound_claims": ["Cassini_Shapiro_gamma_2003", "gamma_minus_1", "2.3e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1580_SOURCE_REGISTER.csv"
PPN_BRIDGE = OUT / "P8_Y5_PARENT_QLOC_1580_PPN_BRIDGE_DERIVATION.csv"
QRHAT_ROW = OUT / "P8_Y5_PARENT_QLOC_1580_QRHAT_SOURCE_ROW_NONCLAIM.csv"
CASSINI_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1580_CASSINI_BOUND_CONTRACT.csv"
PPN_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1580_PPN_DRY_RUN.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1580_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1580_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1580_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1580_VALIDATION.csv"

COPY_TARGETS = {
    PPN_BRIDGE: [
        QUARANTINE / "PPN_BRIDGE_DERIVATION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_PPN_bridge_derivation_nonclaim_1580.csv",
    ],
    QRHAT_ROW: [
        QUARANTINE / "QRHAT_SOURCE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "qRhat_source_row_nonclaim_1580.csv",
    ],
    CASSINI_CONTRACT: [
        QUARANTINE / "CASSINI_BOUND_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "Cassini_bound_contract_nonclaim_1580.csv",
    ],
    PPN_DRY_RUN: [
        QUARANTINE / "PPN_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "PPN_dry_run_nonclaim_1580.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "RAB_PPN_decision_nonclaim_1580.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def local_bound_by_dataset(dataset_id: str) -> dict[str, str]:
    for row in read_csv(SOURCE_FILES["local_bound_claims"]):
        if row.get("dataset_id") == dataset_id:
            return row
    return {}


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1580_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, NEEDLES[key]),
                "needles": "; ".join(NEEDLES[key]),
                "purpose": "derive PPN gamma residual vector from R_AB/q_R_hat or keep q_R_hat source row blocked",
                **flags(),
            }
        )
    return rows


def ppn_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PPNB1580_0_observer_identity",
            "observer reciprocal strain",
            "R_AB=ln(A B)=ln(T^2 S)",
            "sourced from 05 and 10",
            "FORMAL_INPUT",
            "requires PPN-compatible identification of A=T^2 and B=S in the same weak-field radial gauge",
        ),
        (
            "PPNB1580_1_ppn_expansion",
            "weak-field PPN metric",
            "A=1-2 U_N+O(U_N^2), B=1+2 gamma U_N+O(U_N^2)",
            "standard PPN expansion used as comparator grammar",
            "FORMAL_COMPARATOR_GRAMMAR",
            "does not import Einstein equations; it defines the observable gamma channel",
        ),
        (
            "PPNB1580_2_linear_bridge",
            "linearized reciprocal strain",
            "R_AB=ln[(1-2 U_N)(1+2 gamma U_N)]=2(gamma-1)U_N+O(U_N^2)",
            "Taylor expansion of PPN comparator grammar",
            "DERIVED_CONDITIONAL_BRIDGE",
            "valid only after gauge/source denominator and observer-map matching are fixed",
        ),
        (
            "PPNB1580_3_qRhat_definition",
            "dimensionless local hair",
            "q_R_hat:=R_AB^(1)/(2 U_N)",
            "definition from bridge row",
            "FORMAL_DEFINITION_VALUE_MISSING",
            "numeric q_R_hat remains missing because R_AB profile/source charge is not derived",
        ),
        (
            "PPNB1580_4_residual_vector",
            "PPN gamma residual",
            "gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+O(U_N)",
            "PPN residual vector contract",
            "FORMAL_NONCLAIM_VECTOR_READY",
            "tails must be zero-proved or absolutely bounded before Cassini scoring",
        ),
        (
            "PPNB1580_5_current_hair_projection",
            "exterior reciprocal hair if current branch is retained",
            "W~r^2 and W R_AB'=Q_R imply R_AB~sigma_Q Q_R/r, so q_R_hat~sigma_Q Q_R/(2 G M)",
            "combines 05 current obstruction with PPN bridge",
            "CONDITIONAL_BOUND_TARGET",
            "sign convention, W normalization, M/source denominator, and tails remain unsourced",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "object": obj,
            "equation": equation,
            "derivation_basis": derivation_basis,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for bridge_id, obj, equation, derivation_basis, status, blocking_gap in rows
    ]


def q_rhat_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "QRHAT1580_0_definition",
            "symbol": "q_R_hat",
            "definition": "q_R_hat:=R_AB^(1)/(2 U_N) in a PPN-compatible weak-field observer gauge",
            "units": "dimensionless",
            "value": "",
            "source_path": "05-reciprocity-theorem-attempt.md; 10-observer-map-symplectic-contract.md",
            "source_anchor": "R_AB=ln(A B); PPN gamma residual bridge",
            "current_status": "FORMAL_DEFINITION_DERIVED_VALUE_MISSING",
            "why_not_claim": "R_AB profile, Q_R/source denominator, gauge matching, and boundary/source tails are not sourced",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "QRHAT1580_1_current_hair_target",
            "symbol": "Q_R/(2GM)",
            "definition": "if W~r^2 and R_AB~sigma_Q Q_R/r, then q_R_hat~sigma_Q Q_R/(2GM)",
            "units": "dimensionless after source-mass normalization",
            "value": "",
            "source_path": "05-reciprocity-theorem-attempt.md; 1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            "source_anchor": "W R_AB'=Q_R; current route preserves reciprocal hair",
            "current_status": "CONDITIONAL_BOUND_TARGET_VALUE_MISSING",
            "why_not_claim": "Q_R, W normalization, source mass convention, and tail envelope are missing",
            **flags(),
        },
    ]


def cassini_contract_rows() -> list[dict[str, Any]]:
    cassini = local_bound_by_dataset("Cassini_Shapiro_gamma_2003")
    upper = cassini.get("upper_bound", "")
    units = cassini.get("units", "")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "CAS1580_0_gamma_bound",
            "external_dataset_id": "Cassini_Shapiro_gamma_2003",
            "observable": "gamma_minus_1",
            "external_upper_bound": upper,
            "external_units": units,
            "mts_bound_expression": "abs(q_R_hat+delta_gauge+delta_source+delta_boundary) <= external_upper_bound at leading PPN order",
            "conditional_QR_expression": "abs(sigma_Q Q_R/(2GM)+tails) <= external_upper_bound if W~r^2 and R_AB~sigma_Q Q_R/r",
            "current_status": "BOUND_CONTRACT_ONLY_NO_MTS_VALUE",
            "why_not_claim": "q_R_hat/Q_R and tail terms are not derived or source-backed",
            **flags(),
        }
    ]


def ppn_dry_run_rows() -> list[dict[str, Any]]:
    cassini = local_bound_by_dataset("Cassini_Shapiro_gamma_2003")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "PPNDRY1580_0_Cassini",
            "arena": "PPN/Cassini gamma",
            "external_bound": cassini.get("upper_bound", ""),
            "external_units": cassini.get("units", ""),
            "mts_prediction": "",
            "required_missing_inputs": "q_R_hat numeric or Q_R/(2GM); delta_gauge; delta_source; delta_boundary; PPN gauge/source denominator",
            "dry_run_status": "NOT_RUN_BLOCKED",
            "blocker": "FORMAL_BRIDGE_READY_BUT_QRHAT_VALUE_MISSING",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dry_run_id": "PPNDRY1580_1_GR_limit",
            "arena": "local GR reduction",
            "external_bound": "gamma_minus_1=0 target",
            "external_units": "dimensionless",
            "mts_prediction": "",
            "required_missing_inputs": "Q_R=0 theorem or q_R_hat=0 theorem; beta-1=0; conservation/Bianchi identity; common matter coframe",
            "dry_run_status": "NOT_RUN_BLOCKED",
            "blocker": "GAMMA_BRIDGE_ALONE_NOT_FULL_GR_REDUCTION",
            "can_score": False,
            "passes_for_claim": False,
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1580_0_bridge", "R_AB to gamma_minus_1 formal bridge exists", "PASS_FORMAL_NONCLAIM", "linear PPN expansion gives R_AB=2(gamma-1)U_N conditionally"),
        ("GATE1580_1_qRhat_value", "q_R_hat numeric/theorem-zero row exists", "BLOCKED_NO_CLAIM", "q_R_hat and Q_R/(2GM) remain value-missing"),
        ("GATE1580_2_Cassini_score", "Cassini PPN comparison can be scored", "BLOCKED_NO_CLAIM", "tails, gauge/source denominator and q_R_hat are missing"),
        ("GATE1580_3_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "gamma bridge does not prove Q_R=0, beta=1, conservation or common matter coupling"),
        ("GATE1580_4_finite_branch", "finite R_AB branch passes local tests", "BLOCKED_NO_CLAIM", "only a bound contract exists; no prediction is made"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1580_0_progress",
            "PPN_BRIDGE_DERIVED_CONDITIONALLY",
            "R_AB=ln(AB) gives gamma_minus_1=R_AB/(2U_N)+tails at leading PPN order",
            "the PPN/local-GR test now has a real MTS-facing residual variable q_R_hat",
        ),
        (
            "DEC1580_1_claim_ceiling",
            "NO_CASSINI_OR_GR_CLAIM",
            "q_R_hat/Q_R, gauge/source denominator, and boundary/source tails are missing",
            "Cassini becomes a bound contract, not a pass/fail result",
        ),
        (
            "DEC1580_2_next",
            "NEXT_1581_RAB_QRHAT_PROFILE_AND_CASSINI_BOUND_ROW_OR_NO_CHARGE_RETURN",
            "the next step is to use W R_AB'=Q_R and W~r^2 to either bound Q_R/(2GM) or return to a parent no-charge theorem",
            "derive/source the radial hair amplitude before scoring Cassini",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md",
            "script": "scripts/Y5_RAB_qRhat_profile_and_Cassini_bound_row_or_no_charge_return.py",
            "objective": "derive the radial q_R_hat profile from W R_AB'=Q_R and W~r^2, then write a Cassini bound row for Q_R/(2GM) or return to the no-charge theorem route",
            "do_not": "do not claim Cassini pass or local GR unless Q_R=0/q_R_hat=0 and all PPN tails/gauge/source denominators are parent-signed",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "parent_signed",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "can_score",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    generated_paths = [Path(__file__).resolve(), DOC, *generated_csvs]
    generated_paths.extend(target for targets in COPY_TARGETS.values() for target in targets)
    if any(is_within(path, FORMALIZATION) for path in generated_paths):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1580_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1580" in path.name for path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    bridge = read_csv(PPN_BRIDGE)
    qrows = read_csv(QRHAT_ROW)
    cassini = read_csv(CASSINI_CONTRACT)
    dry = read_csv(PPN_DRY_RUN)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1580_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL1580_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL1580_2_bridge_formula",
            any(row["bridge_id"] == "PPNB1580_2_linear_bridge" and "2(gamma-1)U_N" in row["equation"] for row in bridge),
            "linear PPN bridge R_AB=2(gamma-1)U_N is recorded",
        ),
        (
            "VAL1580_3_qrhat_definition_nonclaim",
            any(row["symbol"] == "q_R_hat" and row["current_status"] == "FORMAL_DEFINITION_DERIVED_VALUE_MISSING" for row in qrows),
            "q_R_hat formal definition exists but remains value-missing",
        ),
        (
            "VAL1580_4_cassini_contract_only",
            any(row["external_upper_bound"] == "2.3e-05" and row["current_status"] == "BOUND_CONTRACT_ONLY_NO_MTS_VALUE" for row in cassini),
            "Cassini row is a bound contract only",
        ),
        (
            "VAL1580_5_ppn_dry_run_blocked",
            all(row["dry_run_status"] == "NOT_RUN_BLOCKED" and row["can_score"] == "False" for row in dry),
            "PPN dry-run rows block scoring",
        ),
        (
            "VAL1580_6_claim_gates_closed",
            all(row["claim_allowed"] == "False" for row in gates),
            "claim gates remain nonclaim even when formal bridge passes",
        ),
        (
            "VAL1580_7_decision_next",
            any(row["decision"] == "NEXT_1581_RAB_QRHAT_PROFILE_AND_CASSINI_BOUND_ROW_OR_NO_CHARGE_RETURN" for row in decisions),
            "decision selects q_R_hat profile and Cassini bound target",
        ),
        ("VAL1580_8_csv_parse", all(len(read_csv(path)) > 0 for path in generated_csvs), "all generated 1580 CSVs parse cleanly"),
        ("VAL1580_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1580_10_no_raw_accepted", not has_1580_rows(RAB_RAW) and not has_1580_rows(RAB_ACCEPTED), "no 1580 rows written to raw/accepted finite directories"),
        ("VAL1580_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets), "branch/quarantine nonclaim copies written"),
        ("VAL1580_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1580_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1580 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1580_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1580 PPN residual vector/q_Rhat source-row validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    qrows: list[dict[str, Any]],
    cassini: list[dict[str, Any]],
    dry: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1580 - R_AB PPN Residual Vector Or qRhat Source Row",
                "## Verdict\n"
                "- A conditional PPN bridge is now derived: with `R_AB=ln(A B)` and PPN-compatible weak-field variables, `R_AB=2(gamma-1)U_N+O(U_N^2)`.\n"
                "- This defines the useful local hair variable `q_R_hat:=R_AB^(1)/(2U_N)`, so `gamma_minus_1=q_R_hat+tails` at leading order.\n"
                "- If the exterior current-hair branch is retained, `W R_AB'=Q_R` with `W~r^2` gives the bound target `q_R_hat~sigma_Q Q_R/(2GM)`.\n"
                "- Cassini therefore becomes a real bound contract on `q_R_hat` or `Q_R/(2GM)`, not a pass, because the value, gauge/source denominator, and tails are missing.\n"
                "- No Cassini, PPN, local GR/Newton, no-charge, beta, conservation, R10, WEP, clock, or orbital claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## PPN Bridge Derivation",
                md_table(bridge, ["bridge_id", "object", "equation", "status", "blocking_gap"]),
                "## q_R_hat Source Row",
                md_table(qrows, ["row_id", "symbol", "definition", "units", "value", "current_status", "why_not_claim"]),
                "## Cassini Bound Contract",
                md_table(cassini, ["contract_id", "observable", "external_upper_bound", "mts_bound_expression", "conditional_QR_expression", "current_status"]),
                "## PPN Dry Run",
                md_table(dry, ["dry_run_id", "arena", "external_bound", "required_missing_inputs", "dry_run_status", "blocker"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    bridge = ppn_bridge_rows()
    qrows = q_rhat_rows()
    cassini = cassini_contract_rows()
    dry = ppn_dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        PPN_BRIDGE,
        QRHAT_ROW,
        CASSINI_CONTRACT,
        PPN_DRY_RUN,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PPN_BRIDGE, bridge)
    write_csv(QRHAT_ROW, qrows)
    write_csv(CASSINI_CONTRACT, cassini)
    write_csv(PPN_DRY_RUN, dry)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, bridge, qrows, cassini, dry, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
