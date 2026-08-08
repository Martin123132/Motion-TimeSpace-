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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2977"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2977-Y5-R2FR-response-doublet-MAB-Zbasis-owner-and-no-linear-source-lock-or-DeltaK-deltaM-row-under-AX1090.md"

SRC_2976_DOC = ROOT / "2976-Y5-R2FR-Gamma-eff-scalar-density-owner-and-Kmetric-volume-component-or-DeltaK-first-bound-under-AX1090.md"
SRC_2976_NEXT = RESIDUALS / "P8_Y5_R2FR_2976_NEXT_TARGET.csv"
SRC_2976_GAMMA = RESIDUALS / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv"
SRC_2976_DELTAVOL = RESIDUALS / "P8_Y5_R2FR_2976_DELTAK_VOL_BOUND_ROW_NONCLAIM.csv"
SRC_2976_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2976_VALIDATION.csv"

SRC_2217_DENSITY = BETA_DOCS / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv"
SRC_2800_QLOC = BETA_DOCS / "RESPONSE_DOUBLET_QLOC_BOUND_2800_NONCLAIM.csv"
SRC_2817_DZ = BETA_DOCS / "STRICT_DOUBLE_ZERO_COEFFICIENT_KILL_2817_NONCLAIM.csv"
SRC_1712_CONJ = RAB_QUEUE / "JR1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv"
SRC_1712_ID = RAB_QUEUE / "JR1712_METRIC_RESPONSE_IDENTITY_AUDIT.csv"
SRC_1712_BLOCKERS = RAB_QUEUE / "JR1712_CONJUGACY_BLOCKER_AUDIT.csv"
SRC_2857_ACTION = LOCAL_BOUNDS / "RAB_MINIMAL_DOUBLET_ACTION_ANSATZ_2857_NONCLAIM.csv"
SRC_2858_GATE = LOCAL_BOUNDS / "RAB_MINIMAL_DOUBLET_CONSISTENCY_GATE_2858_NONCLAIM.csv"
SRC_2852_SYM = LOCAL_BOUNDS / "RAB_SOURCE_DOUBLET_SYMMETRY_CANDIDATES_2852_NONCLAIM.csv"
SRC_2857_OWNER = SOURCE_WEIGHT / "RAB_VERTICAL_GENERATOR_OWNERSHIP_GATE_2857_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2977_SOURCE_REGISTER.csv",
    "owner": RESIDUALS / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv",
    "no_linear": RESIDUALS / "P8_Y5_R2FR_2977_NO_LINEAR_SOURCE_JZ_BZ_AUDIT.csv",
    "deltak": RESIDUALS / "P8_Y5_R2FR_2977_DELTAK_DELTAM_DELTAZ_BOUND_ROWS_NONCLAIM.csv",
    "rollforward": RESIDUALS / "P8_Y5_R2FR_2977_GAMMA_EFF_OWNER_ROLLFORWARD_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2977_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2977_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2977_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2977_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2977_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": PARENT_ACTION / "response_doublet_MAB_Zbasis_owner_2977_NOT_DERIVED.csv",
    "deltak_copy": LOCAL_BOUNDS / "DeltaK_deltaM_deltaZ_bound_rows_2977_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2977_no_linear_source_JZ_BZ_or_component_bounds_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2977_00_2976_doc", SRC_2976_DOC, "NEXT2976_0_2977;M_AB", "2976 selected response-doublet owner target"),
        ("SRC2977_01_2976_next", SRC_2976_NEXT, "NEXT2976_0_2977", "machine next-target row"),
        ("SRC2977_02_2976_gamma", SRC_2976_GAMMA, "GAM2976_4_MAB;GAM2976_5_Zbasis", "M_AB/Z blockers"),
        ("SRC2977_03_2976_deltavol", SRC_2976_DELTAVOL, "DKV2976_0_definition;DKV2976_4_no_cancellation", "DeltaK_vol retained row"),
        ("SRC2977_04_2976_validation", SRC_2976_VALIDATION, "VAL2976_OVERALL", "2976 validation"),
        ("SRC2977_05_2217_density", SRC_2217_DENSITY, "RDP2217_0_parent_action_ansatz;RDP2217_4_density_verdict", "response-doublet density candidate"),
        ("SRC2977_06_2800_qloc", SRC_2800_QLOC, "RDT2800_0_parent_doublets;RDT2800_7_verdict", "response-doublet source/current blocker audit"),
        ("SRC2977_07_2817_dz", SRC_2817_DZ, "CK2817_1_exact_double_zero;CK2817_4_verdict", "strict double-zero coefficient kill"),
        ("SRC2977_08_1712_conj", SRC_1712_CONJ, "CJA1712_1_even_density;CJA1712_6_verdict", "conjugacy action attempt"),
        ("SRC2977_09_1712_identity", SRC_1712_ID, "MRI1712_0_Z_variation;MRI1712_4_verdict", "metric-response identity audit"),
        ("SRC2977_10_1712_blockers", SRC_1712_BLOCKERS, "BLK1712_0_component_lock;BLK1712_6_verdict", "conjugacy blocker audit"),
        ("SRC2977_11_2857_action", SRC_2857_ACTION, "ANS2857_0_doublet;ANS2857_7_claim_guard", "minimal doublet action ansatz"),
        ("SRC2977_12_2858_gate", SRC_2858_GATE, "GATE2858_0_algebra;GATE2858_7_full_vector", "minimal doublet consistency gate"),
        ("SRC2977_13_2852_sym", SRC_2852_SYM, "SYM2852_0_fixed_source_vector;SYM2852_4_auxiliary_constraint", "source-doublet symmetry candidates"),
        ("SRC2977_14_2857_owner", SRC_2857_OWNER, "OWN2857_0_sigma;OWN2857_6_full_vector", "vertical generator ownership gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        anchors_ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "exists": path.exists(),
                    "anchors_required": anchors,
                    "anchors_found": anchors_ok,
                    "missing_anchors": missing,
                    "role": role,
                }
            )
        )
    return rows


def owner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OWN2977_0_parent_doublets",
            "R_+^A,R_-^A",
            "Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2",
            "CONDITIONAL_DOUBLETS_ONLY",
            "physical Y0-Y6/PPN/source channels are not parent-locked",
            SRC_1712_CONJ,
        ),
        (
            "OWN2977_1_MAB",
            "M_AB",
            "H_AB:=partial_A partial_B Gamma_eff|_{Z=0}=M_AB",
            "MISSING_MAB_OWNER_UNITS_POSITIVITY",
            "source, units, positivity, self-adjointness, gauge quotient and domain not signed",
            SRC_2217_DENSITY,
        ),
        (
            "OWN2977_2_Zbasis",
            "Z^A",
            "Z^A must be the actual quotient-vertical/local residual generator",
            "COMPONENT_LOCK_NOT_PROVED",
            "full physical residual vector lock remains open",
            SRC_1712_BLOCKERS,
        ),
        (
            "OWN2977_3_exchange",
            "exchange evenness",
            "E:Z^A->-Z^A forbids a linear Z source only if exact parent symmetry covers source/readout",
            "CONDITIONAL_TEMPLATE_ONLY",
            "source/readout/Y5/Y6 channels can remain even and visible",
            SRC_2800_QLOC,
        ),
        (
            "OWN2977_4_positive_operator",
            "L_AB/M_AB positive operator",
            "int Z^A L_AB Z^B >= c ||Z||^2 after constraints/gauge removal",
            "FORMAL_CANDIDATE_ONLY",
            "positive theorem cannot activate while J_Z/B_Z and domain are open",
            SRC_2800_QLOC,
        ),
        (
            "OWN2977_5_vertical_generator",
            "v_Z",
            "actual Omega-raised generator/quotient kernel, not chosen after desired cancellation",
            "NOT_PARENT_SIGNED",
            "parent Omega, DCdagger and q-map are missing",
            SRC_2857_OWNER,
        ),
        (
            "OWN2977_6_matter_descent",
            "matter/source/readout descent",
            "matter, clocks, source measures and readouts see quotient/even variables only",
            "FAIL_OPEN",
            "matter descent and source weights remain unsigned",
            SRC_2858_GATE,
        ),
        (
            "OWN2977_7_verdict",
            "response-doublet owner lock",
            "M_AB, Z^A, positivity, verticality, no-linear-source and boundary all parent-signed",
            "NOT_PARENT_SIGNED_DELTAM_DELTAZ_ROWS_REQUIRED",
            "formal double-zero remains useful but not claimable",
            SRC_1712_BLOCKERS,
        ),
    ]
    return [
        add_common(
            {
                "owner_id": owner_id,
                "object": obj,
                "required_statement": statement,
                "status": status,
                "blocking_gap": gap,
                "source_path": str(source),
                "parent_signed": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for owner_id, obj, statement, status, gap, source in rows
    ]


def no_linear_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NL2977_0_density_derivative",
            "delta_Z Gamma_eff",
            "delta Gamma_eff/delta Z^A = M_AB Z^B + O(Z^3), hence F1=0 at formal Z=0",
            "FORMAL_DOUBLE_ZERO_PASS",
            "Z=0 physical/local residual state is not proved",
            SRC_1712_ID,
        ),
        (
            "NL2977_1_source_current",
            "J_Z",
            "Euler: L_AB Z^B = J_A + boundary/source terms; need J_Z=0",
            "JZ_ZERO_NOT_PROVED",
            "matter/source/readout can inject odd or visible source terms",
            SRC_2800_QLOC,
        ),
        (
            "NL2977_2_boundary",
            "B_Z",
            "boundary/source work vanishes in compact local collar or is exact/included",
            "BZ_ZERO_NOT_PROVED",
            "boundary/domain clauses remain unsigned",
            SRC_2800_QLOC,
        ),
        (
            "NL2977_3_Y5Y6",
            "Y5/Y6 even debt",
            "source-normalization and extra-stress channels must be even/topological/bounded",
            "OPEN_HARD_BLOCK",
            "Y5 source-normalization and Y6 extra-stress may live outside the doublet zero",
            SRC_1712_BLOCKERS,
        ),
        (
            "NL2977_4_no_marker",
            "no independent source covector",
            "parent object language or representation theory forbids an independent source-doublet covector",
            "CANDIDATE_ONLY",
            "source symmetry candidates are not parent-adopted",
            SRC_2852_SYM,
        ),
        (
            "NL2977_5_verdict",
            "no-linear-source lock",
            "J_Z=B_Z=0 plus matter/source/readout descent and boundary silence",
            "NOT_PROVED_RETAIN_JZ_BZ",
            "retain explicit J_Z/B_Z rows and DeltaK_deltaM/Z bounds",
            SRC_1712_CONJ,
        ),
    ]
    return [
        add_common(
            {
                "no_linear_id": row_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "blocking_gap": gap,
                "source_path": str(source),
                "formal_pass": row_id == "NL2977_0_density_derivative",
                "parent_signed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, obj, statement, status, gap, source in rows
    ]


def deltak_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DK2977_0_DeltaM",
            "DeltaK_deltaM",
            "K_hat_deltaM - 1/2(delta M_AB/delta g_{mu nu}) Z^A Z^B",
            "stress",
            "MISSING_DELTA_MAB_VALUE",
            "M_AB metric dependence, units, domain and Khat component split",
            SRC_2976_GAMMA,
        ),
        (
            "DK2977_1_DeltaZ",
            "DeltaK_deltaZ",
            "K_hat_deltaZ - (M_AB Z^A delta_g Z^B + symmetric partner)",
            "stress",
            "MISSING_DELTA_Z_VALUE",
            "Z^A metric/coframe/readout dependence and physical lock",
            SRC_1712_BLOCKERS,
        ),
        (
            "DK2977_2_JZ",
            "eps_JZ",
            "||J_Z|| contribution to response-doublet Euler source",
            "source norm",
            "MISSING_JZ_ZERO_OR_BOUND",
            "source-current coefficient, matter descent and source weights",
            SRC_2800_QLOC,
        ),
        (
            "DK2977_3_BZ",
            "eps_BZ",
            "||B_Z|| boundary/source work contribution",
            "boundary/source norm",
            "MISSING_BZ_ZERO_OR_BOUND",
            "boundary no-flux/exactness or source-backed finite bound",
            SRC_2800_QLOC,
        ),
        (
            "DK2977_4_operator",
            "eps_MAB_domain",
            "operator-domain error from non-positive/non-self-adjoint/gauge-unreduced M_AB",
            "operator norm",
            "MISSING_OPERATOR_DOMAIN_CERTIFICATE",
            "inner product, gauge quotient, boundary domain and units",
            SRC_1712_BLOCKERS,
        ),
        (
            "DK2977_5_no_cancellation",
            "absolute envelope",
            "DeltaK_deltaM, DeltaK_deltaZ, J_Z, B_Z and operator-domain rows are summed in absolute value",
            "guardrail",
            "NO_CANCELLATION_GUARD_ACTIVE",
            "parent identity proving cancellation",
            SRC_2976_DELTAVOL,
        ),
    ]
    return [
        add_common(
            {
                "deltak_id": row_id,
                "symbol": symbol,
                "definition_or_bound": definition,
                "units": units,
                "status": status,
                "required_input": required,
                "source_path": str(source),
                "lower_bound": 0,
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "finite_value_present": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, status, required, source in rows
    ]


def rollforward_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RF2977_0_formal_win",
            "formal F1=0",
            "delta_Z Gamma_eff=M_AB Z+O(Z^3), so first variation vanishes at formal Z=0",
            "keeps the derivation route alive",
        ),
        (
            "RF2977_1_claim_gap",
            "parent owner gap",
            "formal Z=0 is not yet a physical local-GR residual state because Z-basis/full vector lock fails",
            "blocks local-GR promotion",
        ),
        (
            "RF2977_2_q_loc_envelope",
            "eps_q_loc_component",
            "add eps_JZ, eps_BZ, eps_MAB_domain, DeltaK_deltaM and DeltaK_deltaZ to the absolute q_loc envelope",
            "no hidden source-current cancellation",
        ),
        (
            "RF2977_3_next",
            "next fork",
            "attack J_Z/B_Z no-linear-source theorem first, because positivity cannot rescue nonzero source/boundary work",
            "select 2978",
        ),
    ]
    return [
        add_common(
            {
                "rollforward_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "meaning": meaning,
                "source_path": str(SRC_1712_ID if row_id == "RF2977_0_formal_win" else SRC_2800_QLOC),
                "accepted_for_scoring": False,
            }
        )
        for row_id, quantity, formula, meaning in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2977_0_formal_F1", "formal first variation zero at Z=0", True, "FORMAL_TEMPLATE_ONLY_NOT_PARENT_CLAIM"),
        ("CG2977_1_MAB", "M_AB owned, unit-normalized and positive", False, "MAB_OWNER_UNITS_POSITIVITY_MISSING"),
        ("CG2977_2_Zbasis", "Z^A is physical residual/vertical generator", False, "Z_BASIS_PHYSICAL_LOCK_MISSING"),
        ("CG2977_3_JZ", "J_Z=0 or bounded", False, "JZ_ZERO_OR_BOUND_MISSING"),
        ("CG2977_4_BZ", "B_Z=0 or bounded", False, "BZ_ZERO_OR_BOUND_MISSING"),
        ("CG2977_5_deltak", "DeltaK_deltaM/Z score-ready", False, "DELTAK_DELTAM_DELTAZ_MISSING_VALUES"),
        ("CG2977_6_local_GR", "local GR/Newton reduction", False, "LOCAL_GR_NOT_DERIVED"),
        ("CG2977_7_arena_claims", "R10/PPN/clock/orbital/WEP claims", False, "NO_ARENA_CLAIM_ALLOWED"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2977_0_formal_success",
            "The response-doublet density gives a real formal double-zero/F1=0 route.",
            "delta_Z Gamma_eff=M_AB Z+O(Z^3) is exactly the sort of local fixed-point mechanism wanted.",
            "keep this as the main derivation route",
        ),
        (
            "DEC2977_1_not_parent_signed",
            "The response-doublet owner lock is not closed.",
            "M_AB owner/units/positivity, Z physical lock, J_Z/B_Z silence, matter descent and boundary all remain open.",
            "do not claim q_loc zero or local GR",
        ),
        (
            "DEC2977_2_bounds",
            "DeltaK_deltaM/DeltaK_deltaZ plus J_Z/B_Z rows are the honest fallback.",
            "they expose exactly where the formal density leaks into observable local physics.",
            "carry rows into the q_loc envelope",
        ),
        (
            "DEC2977_3_next",
            "Next attack should target J_Z/B_Z no-linear-source/source-current silence.",
            "positivity cannot prove silence when source and boundary work are nonzero.",
            "run 2978 on source-functional evenness or explicit J_Z/B_Z bounds",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2977_0_2978",
                "priority": "selected_primary",
                "next_doc": "2978-Y5-R2FR-no-linear-source-JZ-BZ-theorem-or-source-bound-rows-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_no_linear_source_JZ_BZ_theorem_or_source_bound_rows_under_AX1090_2978.py",
                "objective": "Try to prove J_Z=B_Z=0 from exchange-even source/readout descent, no-marker object language, compact boundary silence and parent quotient verticality; if not, emit explicit J_Z/B_Z source-bound rows.",
                "include": "J_Z;B_Z;exchange evenness;source/readout descent;no marker;Y5;Y6;boundary;verticality;source-functional symmetry;finite J_Z/B_Z bounds",
                "exclude": "plateau axiom;bookkeeping stress claim;full K_metric certificate;full Z-basis scoring;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "copy_id": "COPY2977_0_owner",
                "source_output": str(OUTPUTS["owner"]),
                "branch_copy": str(BRANCH_OUTPUTS["owner_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2977_1_deltak",
                "source_output": str(OUTPUTS["deltak"]),
                "branch_copy": str(BRANCH_OUTPUTS["deltak_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2977_2_next",
                "source_output": str(OUTPUTS["next"]),
                "branch_copy": str(BRANCH_OUTPUTS["next_copy"]),
                "status": "copied",
            }
        ),
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources = all_rows["sources"]
    owner = all_rows["owner"]
    no_linear = all_rows["no_linear"]
    deltak = all_rows["deltak"]
    claims = all_rows["claims"]
    next_rows = all_rows["next"]

    checks = [
        ("VAL2977_0_sources_exist", all(row["exists"] for row in sources), "all cited local source paths exist", True),
        ("VAL2977_1_anchors_found", all(row["anchors_found"] for row in sources), "all cited source anchors found", True),
        (
            "VAL2977_2_formal_double_zero_present",
            any(row["no_linear_id"] == "NL2977_0_density_derivative" and row["status"] == "FORMAL_DOUBLE_ZERO_PASS" for row in no_linear),
            "formal F1=0 row is preserved",
            True,
        ),
        (
            "VAL2977_3_owner_not_signed",
            any(row["owner_id"] == "OWN2977_7_verdict" and row["status"] == "NOT_PARENT_SIGNED_DELTAM_DELTAZ_ROWS_REQUIRED" for row in owner),
            "response-doublet owner lock remains unproved",
            True,
        ),
        (
            "VAL2977_4_JZ_BZ_retained",
            any(row["no_linear_id"] == "NL2977_5_verdict" and row["status"] == "NOT_PROVED_RETAIN_JZ_BZ" for row in no_linear),
            "J_Z/B_Z retained instead of hidden",
            True,
        ),
        (
            "VAL2977_5_deltak_rows_nonclaim",
            any(row["deltak_id"] == "DK2977_0_DeltaM" for row in deltak)
            and any(row["deltak_id"] == "DK2977_1_DeltaZ" for row in deltak)
            and all(not row["accepted_for_scoring"] for row in deltak),
            "DeltaK_deltaM/Z rows exist and remain nonclaim",
            True,
        ),
        (
            "VAL2977_6_claims_blocked_except_formal",
            all((row["claim_gate_id"] == "CG2977_0_formal_F1" and row["condition_passed"]) or (not row["condition_passed"]) for row in claims),
            "all physics claim gates remain blocked except formal F1 template",
            True,
        ),
        (
            "VAL2977_7_next_target_written",
            bool(next_rows) and next_rows[0]["next_id"] == "NEXT2977_0_2978",
            "2978 J_Z/B_Z no-linear-source target selected",
            True,
        ),
        ("VAL2977_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        (
            "VAL2977_9_csvs_parse",
            all(csv_parses(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"]) and all(csv_parses(path) for path in BRANCH_OUTPUTS.values()),
            "all generated CSV files parse",
            True,
        ),
        (
            "VAL2977_10_outputs_under_post_checkpoint",
            all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL2977_11_formalization_clean",
            not any(FORMALIZATION.rglob("*2977*")) if FORMALIZATION.exists() else True,
            "no 2977 outputs were written to formalization-workbench",
            True,
        ),
        ("VAL2977_12_doc_written", DOC.exists(), "2977 markdown checkpoint exists", True),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2977_OVERALL", "passed": overall, "check": "2977 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2977 — Response-Doublet M_AB/Z-Basis Owner and No-Linear-Source Lock, or DeltaK_deltaM Row

Status: `Y5_R2FR_2977_formal_F1_zero_preserved_owner_lock_not_parent_signed_JZ_BZ_DeltaK_rows_written_nonclaim`

Claim ceiling: `no_parent_signed_response_doublet_no_JZ_zero_no_BZ_zero_no_DeltaK_deltaM_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The formal win is real: `delta_Z Gamma_eff = M_AB Z^B + O(Z^3)`, so the first variation vanishes at formal `Z=0`.
- The parent proof still fails: `M_AB`, `Z^A`, positivity/domain, vertical generator ownership, matter descent, `J_Z`, and `B_Z` are not signed.
- This means the response-doublet density remains the best derivation route, but it is not a local-GR/PPN/R10 claim.
- The honest fallback rows are now explicit: `DeltaK_deltaM`, `DeltaK_deltaZ`, `eps_JZ`, `eps_BZ`, and `eps_MAB_domain`.
- Next target is narrower and nastier: prove `J_Z=B_Z=0`, or source finite source/boundary rows.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## Response-Doublet Owner Lock

{md_table(all_rows["owner"], ["owner_id", "object", "required_statement", "status", "blocking_gap", "parent_signed"])}

## No-Linear-Source / J_Z / B_Z Audit

{md_table(all_rows["no_linear"], ["no_linear_id", "object", "statement", "status", "blocking_gap", "formal_pass", "parent_signed"])}

## DeltaK_deltaM / DeltaK_deltaZ Bound Rows

{md_table(all_rows["deltak"], ["deltak_id", "symbol", "definition_or_bound", "units", "status", "required_input", "upper_bound", "accepted_for_scoring"])}

## Rollforward

{md_table(all_rows["rollforward"], ["rollforward_id", "quantity", "formula", "meaning", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "owner": owner_rows(),
        "no_linear": no_linear_rows(),
        "deltak": deltak_rows(),
        "rollforward": rollforward_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["owner"], BRANCH_OUTPUTS["owner_copy"])
    shutil.copyfile(OUTPUTS["deltak"], BRANCH_OUTPUTS["deltak_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2977 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
