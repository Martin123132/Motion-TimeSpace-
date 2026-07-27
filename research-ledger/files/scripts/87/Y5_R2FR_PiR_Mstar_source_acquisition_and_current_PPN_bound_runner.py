from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1643"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1643-Y5-R2FR-PiR-Mstar-source-acquisition-and-current-PPN-bound-runner.md"

SOURCE_FILES = {
    "1642_doc": ROOT / "1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md",
    "1642_validation": OUT / "P8_Y5_BRR545_1642_VALIDATION.csv",
    "1642_next": OUT / "P8_Y5_PARENT_QLOC_1642_NEXT_TARGET.csv",
    "1642_fill": OUT / "P8_Y5_PARENT_QLOC_1642_PIR_MSTAR_SOURCE_FILL_ROWS.csv",
    "1642_rule": OUT / "P8_Y5_PARENT_QLOC_1642_NORMALIZED_PPN_SCORE_RULE.csv",
    "1639_law": OUT / "P8_Y5_PARENT_QLOC_1639_NR_LAW_CONDITIONAL.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "1006_denominator": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
    "1016_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
}

NEEDLES = {
    "1642_doc": ["1643-Y5-R2FR-PiR-Mstar-source-acquisition-and-current-PPN-bound-runner.md", "Exactness is therefore useful mathematics, not evidence by itself"],
    "1642_validation": ["VAL1642_OVERALL", "PASS"],
    "1642_next": ["current PPN gamma bound", "do not use orbital GM as M_star"],
    "1642_fill": ["Pi_R_boundary_abs", "M_star_same_frame", "MISSING_CURRENT_EXTERNAL_PPN_GAMMA_BOUND"],
    "1642_rule": ["|q_R| = k_W |Pi_R| c^2/(2 G M_*)", "BLOCKED_BY_MISSING_SOURCE_ROWS"],
    "1639_law": ["N_R = c^2/(2 G M_*)", "no orbital-GM backfill"],
    "05_reciprocity": ["R_AB ~ Q_R/r", "W R_AB' = Q_R"],
    "1006_denominator": ["orbital GM substitution is explicitly rejected", "M_H_ref denominator"],
    "1016_selector": ["MISSING_BOUNDARY_REFERENCE_INPUT", "MISSING_PARENT_WORLDTUBE_SELECTOR"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1643_SOURCE_REGISTER.csv"
EXTERNAL_SOURCES = OUT / "P8_Y5_PARENT_QLOC_1643_EXTERNAL_PPN_SOURCE_REGISTER.csv"
INPUT_STATUS = OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_INPUT_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_BOUND_RUNNER.csv"
BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1643_SOURCE_ACQUISITION_BLOCKERS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1643_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1643_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1643_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1643_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    EXTERNAL_SOURCES,
    INPUT_STATUS,
    RUNNER,
    BLOCKERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    INPUT_STATUS,
    RUNNER,
    BLOCKERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def source_paths_exist(value: str) -> bool:
    if value.startswith("MISSING_") or value == "":
        return False
    paths = [Path(part.strip()) for part in value.split(";") if part.strip() and not part.strip().startswith("MISSING_")]
    return bool(paths) and all(path.exists() for path in paths)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1643 normalized finite Pi_R/PPN source acquisition runner",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def external_source_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "external_id": "EXT1643_0_Cassini_gamma",
            "observable": "PPN_gamma",
            "source_label": "Bertotti, Iess, Tortora 2003 Cassini radio link test",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "doi": "10.1038/nature01997",
            "reported_result": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "gamma_minus_one_central": "2.1e-5",
            "gamma_minus_one_sigma": "2.3e-5",
            "abs_delta_gamma_envelope_1sigma": "4.4e-5",
            "abs_delta_gamma_envelope_2sigma": "6.7e-5",
            "units": "dimensionless",
            "extraction_method": "source abstract/search-result numeric statement; 2sigma envelope computed as abs(central)+2*sigma",
            "source_backed": True,
            "valid_bound_source": True,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "external_id": "EXT1643_1_ephemerides_consistency_review",
            "observable": "PPN_framework_consistency",
            "source_label": "Fienga and Minazzoli 2023 Living Reviews in Relativity",
            "source_url": "https://link.springer.com/article/10.1007/s41114-023-00047-0",
            "doi": "10.1007/s41114-023-00047-0",
            "reported_result": "planetary ephemeris tests require consistent framework/refit treatment; correlated parameters need caution",
            "gamma_minus_one_central": "",
            "gamma_minus_one_sigma": "",
            "abs_delta_gamma_envelope_1sigma": "",
            "abs_delta_gamma_envelope_2sigma": "",
            "units": "review/caution",
            "extraction_method": "used as framework-consistency caution, not as numeric gamma bound",
            "source_backed": True,
            "valid_bound_source": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def input_status_rows() -> list[dict[str, object]]:
    cassini_url = "https://pubmed.ncbi.nlm.nih.gov/14508481/"
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_0_PiR_boundary_abs",
            "quantity": "Pi_R_boundary_abs",
            "required_for_formula": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "current_value": "MISSING_BOUND_VALUE",
            "units": "reciprocal-tail length units after worldtube projection",
            "source_path_or_url": "MISSING_PARENT_OR_EMPIRICAL_SOURCE_PATH",
            "source_backed": False,
            "input_status": "MISSING_SOURCE_ROW",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_1_Bzero_flux",
            "quantity": "B_zero_flux",
            "required_for_formula": "linked-boundary flux of dC_R/exact improvement contributing to Pi_R",
            "current_value": "MISSING_B_ZERO_FLUX",
            "units": "GM-flux or reciprocal-boundary units before normalization",
            "source_path_or_url": "MISSING_BOUNDARY_REFERENCE_SOURCE_PATH",
            "source_backed": False,
            "input_status": "MISSING_SOURCE_ROW",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_2_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "required_for_formula": "N_R = c^2/(2 G M_*)",
            "current_value": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS",
            "units": "mass",
            "source_path_or_url": "MISSING_PARENT_SOURCE_MASS_PATH",
            "source_backed": False,
            "input_status": "MISSING_SOURCE_ROW",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_3_kW_tail",
            "quantity": "k_W_tail",
            "required_for_formula": "R_AB = k_W Q_R/r",
            "current_value": "CONDITIONAL_k_W_EQUALS_1_FROM_CORPUS_NOT_PARENT_SIGNED",
            "units": "dimensionless",
            "source_path_or_url": str(SOURCE_FILES["05_reciprocity"]),
            "source_backed": True,
            "input_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_4_Delta_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "required_for_formula": "|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max",
            "current_value": "6.7e-5",
            "units": "dimensionless; conservative 2sigma envelope from Cassini gamma result",
            "source_path_or_url": cassini_url,
            "source_backed": True,
            "input_status": "SOURCE_BACKED_BOUND_AVAILABLE_NONCLAIM",
            "valid_for_runner": True,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1643_5_absolute_vector",
            "quantity": "absolute_local_residual_vector",
            "required_for_formula": "no cancellation credit across Pi_R, boundary, source-mass, readout, and q_loc residuals",
            "current_value": "MISSING_ABSOLUTE_VECTOR_GUARD",
            "units": "dimensionless residual budget",
            "source_path_or_url": "MISSING_RESIDUAL_VECTOR_SOURCE_PATH",
            "source_backed": False,
            "input_status": "MISSING_SOURCE_ROW",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1643_0_input_gate",
            "formula": "all inputs must be source-backed or parent-signed before scoring",
            "available_inputs": "Delta_gamma_abs_max source-backed; k_W_tail corpus-conditional only",
            "missing_inputs": "Pi_R_boundary_abs;B_zero_flux;M_star_same_frame;absolute_local_residual_vector;parent-signed k_W_tail",
            "runner_status": "NOT_SCORED_MISSING_INPUTS",
            "numeric_result": "NOT_COMPUTED",
            "result": "BLOCKED",
            "reason": "only the external PPN gamma bound is source-backed; MTS numerator/denominator rows remain missing",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1643_1_finite_qR_bound",
            "formula": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "available_inputs": "none claim-valid for Pi_R/Mstar/kW product",
            "missing_inputs": "Pi_R_boundary_abs;M_star_same_frame;parent-signed k_W_tail",
            "runner_status": "NOT_SCORED_MISSING_INPUTS",
            "numeric_result": "NOT_COMPUTED",
            "result": "BLOCKED",
            "reason": "finite q_R amplitude cannot be computed without Pi_R and noncircular M_star",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1643_2_gamma_bound_inversion",
            "formula": "|Pi_R| <= (2 G M_*/(k_W c^2)) * 6.7e-5",
            "available_inputs": "Delta_gamma_abs_max=6.7e-5 from Cassini 2sigma envelope",
            "missing_inputs": "M_star_same_frame;parent-signed k_W_tail;Pi_R projection convention",
            "runner_status": "FORMULA_READY_NOT_SCORED",
            "numeric_result": "SYMBOLIC_BOUND_ONLY",
            "result": "BLOCKED",
            "reason": "gamma bound is real, but the allowed Pi_R bound still scales with missing M_star/kW",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1643_3_R10_guard",
            "formula": "massless Q_R/r is not alpha(lambda)",
            "available_inputs": "none",
            "missing_inputs": "finite carrier/range if R10 is ever reopened",
            "runner_status": "R10_ROUTE_REFUSED",
            "numeric_result": "NOT_APPLICABLE",
            "result": "BLOCKED",
            "reason": "this reciprocal branch remains local/PPN/orbital, not finite-range R10",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1643_0_PiR",
            "missing_input": "Pi_R_boundary_abs",
            "blocker_type": "MISSING_NUMERATOR",
            "why_needed": "sets the physical reciprocal hair amplitude",
            "repair": "derive Pi_R=0 or source absolute boundary-tail coefficient with units",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1643_1_Bzero",
            "missing_input": "B_zero_flux",
            "blocker_type": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "why_needed": "exact boundary bookkeeping can shift Pi_R/source mass",
            "repair": "source theorem-zero or finite linked-boundary flux row",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1643_2_Mstar",
            "missing_input": "M_star_same_frame",
            "blocker_type": "MISSING_NONCIRCULAR_DENOMINATOR",
            "why_needed": "normalizes Q_R/Pi_R into dimensionless q_R without borrowing orbital GM",
            "repair": "derive same-frame Hilbert/Noether source mass or M_H_ref",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1643_3_kW",
            "missing_input": "parent-signed k_W_tail",
            "blocker_type": "CONDITIONAL_TAIL_NORMALIZATION",
            "why_needed": "converts Q_R into the 1/r coefficient of R_AB",
            "repair": "derive W(r) radial equation/integration convention from parent action",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1643_4_no_cancellation",
            "missing_input": "absolute_local_residual_vector",
            "blocker_type": "MISSING_NO_CANCELLATION_GUARD",
            "why_needed": "prevents Pi_R from being hidden by unrelated residual cancellations",
            "repair": "assemble absolute local residual vector across Pi_R, q_loc, frame, readout, source-mass channels",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1643_0_gamma",
            "decision": "PPN_GAMMA_BOUND_SOURCE_BACKED_CASSINI_ANCHOR",
            "reason": "Cassini supplies gamma=1+(2.1+/-2.3)e-5; 2sigma envelope 6.7e-5 is staged as a nonclaim bound input",
            "next_action": "keep gamma bound available but do not score until MTS numerator/denominator inputs exist",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1643_1_runner",
            "decision": "NORMALIZED_PPN_RUNNER_REFUSES_MISSING_MTS_INPUTS",
            "reason": "Pi_R, B_zero, Mstar, parent kW, and no-cancellation vector are missing or conditional",
            "next_action": "attack same-frame Mstar denominator first because it blocks every finite bound",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1643_2_ephemerides",
            "decision": "EPHEMERIDES_USED_AS_CONSISTENCY_CAUTION_NOT_BOUND",
            "reason": "current reviews emphasize framework consistency and correlations; no ephemeris gamma row is imported as a simple standalone bound",
            "next_action": "only use ephemeris constraints after a same-framework MTS refit path exists",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1643_0_gamma_bound",
            "claim": "external PPN gamma bound acquired",
            "status": "PASS_AS_BOUND_INPUT_ONLY",
            "blocker": "not an MTS pass; only one external bound row is source-backed",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1643_1_PPN_score",
            "claim": "MTS finite Pi_R branch passes PPN gamma",
            "status": "BLOCKED",
            "blocker": "Pi_R, Mstar, parent kW, and no-cancellation inputs are missing",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1643_2_local_GR",
            "claim": "local GR recovered through reciprocal-hair branch",
            "status": "BLOCKED",
            "blocker": "Pi_R zero theorem remains unsigned and finite residual runner is not score-ready",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1643_3_R10",
            "claim": "massless reciprocal tail is finite-range R10 evidence",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r remains local/PPN/orbital",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md",
            "script": "scripts/Y5_R2FR_Mstar_same_frame_source_mass_owner_or_noncircular_denominator_blocker.py",
            "objective": "derive or source M_star_same_frame/M_H_ref as a parent Hilbert/Noether source mass denominator before orbital fitting; if it fails, keep a noncircular-denominator blocker ledger",
            "success_condition": "either M_star is parent-signed/source-backed in the same frame as Pi_R/q_R/PPN, or every finite Pi_R bound remains blocked by a noncircular denominator failure",
            "guardrails": "do not use orbital GM as M_star, do not claim local GR or PPN pass, do not score placeholders, keep Cassini gamma as bound input only",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for column_name in ["valid_for_mts_claim", "claim_allowed", "score_allowed"]:
                if column_name in row and bool_string(row[column_name]) == "true":
                    return False
    return True


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(EXTERNAL_SOURCES, QUEUE / "JR1643_EXTERNAL_PPN_SOURCE_REGISTER_NONCLAIM.csv")
    shutil.copy2(INPUT_STATUS, QUEUE / "JR1643_NORMALIZED_PPN_INPUT_STATUS_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1643_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    external = csv_rows(EXTERNAL_SOURCES)
    inputs = csv_rows(INPUT_STATUS)
    runner = csv_rows(RUNNER)
    blockers = csv_rows(BLOCKERS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    gamma_rows = [row for row in external if row["external_id"] == "EXT1643_0_Cassini_gamma"]
    gamma_input = [row for row in inputs if row["quantity"] == "Delta_gamma_abs_max"]

    checks = [
        (
            "VAL1643_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1643 local source paths exist",
        ),
        (
            "VAL1643_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1643 local source needles found",
        ),
        (
            "VAL1643_2_external_gamma_source",
            bool(gamma_rows)
            and gamma_rows[0]["source_url"].startswith("https://")
            and gamma_rows[0]["doi"] == "10.1038/nature01997"
            and float(gamma_rows[0]["abs_delta_gamma_envelope_2sigma"]) > 0,
            "Cassini gamma external source and 2sigma envelope are recorded",
        ),
        (
            "VAL1643_3_gamma_input_filled",
            bool(gamma_input)
            and gamma_input[0]["current_value"] == "6.7e-5"
            and bool_string(gamma_input[0]["source_backed"]) == "true"
            and bool_string(gamma_input[0]["valid_for_runner"]) == "true",
            "Delta gamma input is source-backed as a bound row",
        ),
        (
            "VAL1643_4_mts_inputs_missing",
            all(
                row["input_status"] in {"MISSING_SOURCE_ROW", "CONDITIONAL_NOT_PARENT_SIGNED"}
                for row in inputs
                if row["quantity"] != "Delta_gamma_abs_max"
            ),
            "all MTS numerator/denominator/no-cancellation inputs remain missing or conditional",
        ),
        (
            "VAL1643_5_runner_refuses_scoring",
            all(bool_string(row["score_allowed"]) == "false" and row["result"] == "BLOCKED" for row in runner),
            "normalized PPN runner refuses scoring",
        ),
        (
            "VAL1643_6_blockers_complete",
            all(
                required in {row["missing_input"] for row in blockers}
                for required in [
                    "Pi_R_boundary_abs",
                    "B_zero_flux",
                    "M_star_same_frame",
                    "parent-signed k_W_tail",
                    "absolute_local_residual_vector",
                ]
            ),
            "source acquisition blockers cover PiR, Bzero, Mstar, kW, and no-cancellation",
        ),
        (
            "VAL1643_7_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "PPN_GAMMA_BOUND_SOURCE_BACKED_CASSINI_ANCHOR",
                    "NORMALIZED_PPN_RUNNER_REFUSES_MISSING_MTS_INPUTS",
                    "EPHEMERIDES_USED_AS_CONSISTENCY_CAUTION_NOT_BOUND",
                ]
            ),
            "required 1643 decisions are recorded",
        ),
        (
            "VAL1643_8_claim_gates_safe",
            any(row["status"] == "PASS_AS_BOUND_INPUT_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "gamma bound gate is input-only and all MTS claims remain forbidden",
        ),
        (
            "VAL1643_9_next_target_selected",
            next_targets[0]["next_target"] == "1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md",
            "next target selects Mstar same-frame denominator ownership",
        ),
        (
            "VAL1643_10_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1643 CSVs parse",
        ),
        (
            "VAL1643_11_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1643 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1643_12_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1643_13_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1643_EXTERNAL_PPN_SOURCE_REGISTER_NONCLAIM.csv",
                    QUEUE / "JR1643_NORMALIZED_PPN_INPUT_STATUS_NONCLAIM.csv",
                    QUEUE / "JR1643_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1643_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1643_15_formalization_untouched",
            not any(FORMALIZATION.rglob("*1643*")) if FORMALIZATION.exists() else True,
            "no 1643 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1643_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1643 PiR/Mstar source acquisition and current PPN bound runner validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows_data = csv_rows(SOURCE_REGISTER)
    external = csv_rows(EXTERNAL_SOURCES)
    inputs = csv_rows(INPUT_STATUS)
    runner = csv_rows(RUNNER)
    blockers = csv_rows(BLOCKERS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1643 - Pi_R Mstar Source Acquisition And Current PPN Bound Runner

**Private status:** nonclaim checkpoint. No PPN pass, local-GR pass, Newton pass, orbital pass, WEP pass, clock pass, EM pass, or R10 pass is claimed.

## Verdict

The current external PPN gamma bound is now source-backed for the finite residual branch. The conservative internal envelope staged here is:

```text
Cassini: gamma - 1 = (2.1 +/- 2.3) x 10^-5
|Delta gamma|max,2sigma = |2.1|e-5 + 2*2.3e-5 = 6.7e-5
```

That is useful, but it does **not** score MTS. The normalized runner still refuses to run because the MTS-side numerator and denominator are missing:

```text
|q_R| = k_W |Pi_R| c^2/(2 G M_*)
|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|max
```

`Pi_R_boundary_abs`, `B_zero_flux`, same-frame `M_*`, parent-signed `k_W`, and the absolute no-cancellation vector are still missing or conditional. Cassini gives the external wall; MTS still has to supply the thing being thrown at the wall.

## Local Source Register

{markdown_table(source_rows_data, ["source_id", "path", "path_exists", "needles_found", "role"])}

## External Source Register

{markdown_table(external, ["external_id", "observable", "source_label", "source_url", "doi", "reported_result", "abs_delta_gamma_envelope_2sigma", "valid_bound_source"])}

## Normalized PPN Input Status

{markdown_table(inputs, ["input_id", "quantity", "current_value", "source_backed", "input_status", "valid_for_runner"])}

## Normalized PPN Runner

{markdown_table(runner, ["run_id", "formula", "available_inputs", "missing_inputs", "runner_status", "result"])}

## Source Acquisition Blockers

{markdown_table(blockers, ["blocker_id", "missing_input", "blocker_type", "why_needed", "repair"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        EXTERNAL_SOURCES: external_source_rows(),
        INPUT_STATUS: input_status_rows(),
        RUNNER: runner_rows(),
        BLOCKERS: blocker_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
