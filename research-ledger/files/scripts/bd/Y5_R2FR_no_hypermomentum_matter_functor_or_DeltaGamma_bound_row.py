from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1834"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1834-Y5-R2FR-no-hypermomentum-matter-functor-or-DeltaGamma-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1834_0_1833_next",
        "source_key": "1833_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_NEXT_TARGET.csv",
        "needles": ["NEXT1833_0_primary", "selected"],
        "role": "1833 selects no-hypermomentum matter functor or DeltaGamma bound row.",
    },
    {
        "source_id": "SRC1834_1_1833_validation",
        "source_key": "1833_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1833_VALIDATION.csv",
        "needles": ["VAL1833_OVERALL", "PASS"],
        "role": "confirms 1833 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1834_2_1833_hyper",
        "source_key": "1833_hypermomentum_source",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv",
        "needles": ["HYP1833_0_Delta_Gamma_total", "SOURCE_ROW_STAGED_NONCLAIM"],
        "role": "DeltaGamma total row was staged as the source-side obstruction.",
    },
    {
        "source_id": "SRC1834_3_1830_nohyper",
        "source_key": "1830_no_hypermomentum",
        "source_path": ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md",
        "needles": ["NIC1830_3_no_hypermomentum", "NOT_PARENT_SIGNED"],
        "role": "prior no-hypermomentum clause is explicitly not parent-signed.",
    },
    {
        "source_id": "SRC1834_4_1045_matter_functor",
        "source_key": "1045_matter_functor",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_2_matter_bundle_functor", "QG1045_2_connection_stack"],
        "role": "matter functor and connection descent are conditional.",
    },
    {
        "source_id": "SRC1834_5_1155_geometry_stack",
        "source_key": "1155_geometry_stack",
        "source_path": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
        "needles": ["COF1155_3_geometry_stack", "SINGLE_OBSERVED_COFRAME_NOT_DERIVED"],
        "role": "single geometry/source/readout coframe remains unproved.",
    },
    {
        "source_id": "SRC1834_6_P4_gate",
        "source_key": "P4_gate_tests",
        "source_path": P4_RUN / "P4_gate_tests.csv",
        "needles": ["hypermomentum_spin_gate", "fail_open"],
        "role": "P4 gate records hypermomentum/spin as fail-open.",
    },
    {
        "source_id": "SRC1834_7_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["independent_connection_hypermomentum", "not_forbidden"],
        "role": "independent connection hypermomentum remains a legal demotion row.",
    },
    {
        "source_id": "SRC1834_8_537_source_frame",
        "source_key": "537_source_frame",
        "source_path": ROOT / "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
        "needles": ["PAC537_1_single_observed_source_frame", "PAC537_7_extra_sector_mass_charge_silence"],
        "role": "source frame and extra-sector charge silence are contract-only.",
    },
    {
        "source_id": "SRC1834_9_1561_matter",
        "source_key": "1561_matter_descent",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["EUL1561_4_matter", "OPEN_MATTER_DESCENT"],
        "role": "minimal ansatz leaves matter descent open.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_SOURCE_REGISTER.csv",
    "no_hypermomentum": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "DeltaGamma_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_BOUND_ROW.csv",
    "component_basis": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DELTAGAMMA_COMPONENT_BASIS.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1834_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1834_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def no_hypermomentum_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_0_target",
            "clause": "no hypermomentum theorem",
            "required_statement": "Delta_Gamma = delta(S_matter + S_source + S_readout)/delta Gamma = 0 because all sectors use only e_obs and omega[e_obs]",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "matter/source/readout functor is not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_1_matter_bundle",
            "clause": "ordinary matter bundle over observed coframe",
            "required_statement": "Psi_A in E_A[e_obs] and S_A[Psi_A,e_obs,omega[e_obs],theta_A] for every ordinary matter species",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "blocker": "1045 leaves matter category and vertical lift unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_2_connection_descent",
            "clause": "connection is derivative-only",
            "required_statement": "all Gamma/omega appearances are omega[e_obs], not independent variables varied by matter/source/readout",
            "current_status": "CONDITIONAL_CONNECTION_CAVEAT",
            "blocker": "independent connection requires its own descent row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_3_spin_torsion",
            "clause": "spin does not source independent torsion",
            "required_statement": "spinor matter uses coframe-owned spin connection or spin-torsion current is theorem-zero/bounded",
            "current_status": "SPIN_TORSION_SOURCE_NOT_EXCLUDED",
            "blocker": "P4 hypermomentum/spin gate is fail-open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_4_source_readout",
            "clause": "source/readout actions carry no independent Gamma charge",
            "required_statement": "source support, clocks, photons, rods, orbital readout and boundary markers use the same observed metric/coframe branch",
            "current_status": "SOURCE_READOUT_NOT_PARENT_SIGNED",
            "blocker": "single source/readout frame and extra-sector charge silence remain contract-only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_5_projective",
            "clause": "projective trace invisible or fixed",
            "required_statement": "all sectors are projectively invariant, or a parent constraint/gauge fixes the trace",
            "current_status": "PROJECTIVE_INVARIANCE_NOT_PROVEN",
            "blocker": "projective residue gate is only conditional-open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHM1834_6_verdict",
            "clause": "current MTS proves Delta_Gamma=0",
            "required_statement": "NHM1834_1 through NHM1834_5 all close in one parent branch",
            "current_status": "NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN",
            "blocker": "matter functor, connection descent, spin torsion, source/readout and projective clauses remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def DeltaGamma_bound_rows() -> list[dict[str, Any]]:
    source_path = RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DGB1834_0_total",
            "quantity": "||Delta_Gamma_total||",
            "bound_formula": "||Delta_spin|| + ||Delta_source|| + ||Delta_readout|| + ||Delta_projective|| + ||Delta_boundary||",
            "bound_value": "MISSING_COMPONENT_VALUES",
            "units": "MISSING_COMMON_DUAL_CONNECTION_UNITS",
            "normalization": "MISSING_CONNECTION_VARIATION_NORMALIZATION",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "observable_map": "MISSING_DELTAGAMMA_TO_P4_WEP_PPN_CLOCK_MAP",
            "status": "BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DGB1834_1_spin",
            "quantity": "||Delta_spin||",
            "bound_formula": "spin/torsion source norm in same dual connection basis",
            "bound_value": "MISSING_SPIN_BOUND",
            "units": "MISSING_SPIN_CURRENT_UNITS",
            "normalization": "MISSING_SPIN_CONNECTION_NORMALIZATION",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "observable_map": "MISSING_SPIN_TO_CLOCK_LIGHTCONE_MAP",
            "status": "BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DGB1834_2_source_readout",
            "quantity": "||Delta_source_readout||",
            "bound_formula": "source support plus readout connection-current norm",
            "bound_value": "MISSING_SOURCE_READOUT_BOUND",
            "units": "MISSING_SOURCE_READOUT_UNITS",
            "normalization": "MISSING_SOURCE_BRANCH_NORMALIZATION",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "observable_map": "MISSING_R10_PPN_ORBITAL_MAP",
            "status": "BOUND_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def component_basis_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_0_spin", "component": "spin_hypermomentum", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_1_material", "component": "material_marker_connection_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_2_source_support", "component": "source_support_connection_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_3_clock_rods", "component": "clock_rod_nonmetric_connection_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_4_photon_lightcone", "component": "photon_lightcone_connection_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_5_orbital_readout", "component": "orbital_readout_connection_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "component_id": "DGC1834_6_projective", "component": "projective_trace_current", "included_in_total": True, "status": "MISSING_ZERO_OR_BOUND", "valid_for_claim": False},
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1834_0_theorem_result",
            "decision": "NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN",
            "reason": "omega[e_obs] matter language exists, but matter functor, source/readout frame, spin torsion, and projective invariance are not parent-signed",
            "next_action": "do not set Delta_Gamma to zero",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1834_1_bound_result",
            "decision": "DELTAGAMMA_BOUND_ROW_STAGED_NONCLAIM",
            "reason": "Delta_Gamma is now split into components, but no component has a numeric value, zero theorem, units, or observable map",
            "next_action": "build component-to-observable map before any numeric scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1834_2_best_next",
            "decision": "DELTAGAMMA_COMPONENT_MAP_NEXT",
            "reason": "the next useful step is not another broad proof attempt; it is mapping each retained source current to WEP/PPN/clock/orbital residual channels",
            "next_action": "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1834_0_primary",
            "next_target": "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md",
            "script": "scripts/Y5_R2FR_DeltaGamma_component_map_to_P4_observables.py",
            "objective": "map each retained Delta_Gamma component into P4/WEP/PPN/clock/lightcone/orbital observables without inserting placeholder coefficients",
            "selection_status": "selected",
            "success_condition": "observable map skeleton is complete and nonclaim, or a parent zero theorem removes a component with source evidence",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1834_1_parallel",
            "next_target": "1835b-Y5-R2FR-matter-category-parent-construction.md",
            "script": "scripts/Y5_R2FR_matter_category_parent_construction.py",
            "objective": "attempt the deeper parent construction of the matter category over e_obs and omega[e_obs]",
            "selection_status": "held_parallel",
            "success_condition": "matter category clauses are parent-signed or retained as component residuals",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_hypermomentum": no_hypermomentum_rows(),
        "DeltaGamma_bound": DeltaGamma_bound_rows(),
        "component_basis": component_basis_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def missing_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        if any("MISSING_" in str(value) for value in row.values()) and str(row["valid_for_claim"]).lower() == "true":
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1834-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1834") or name.startswith("P8_Y5_BRR545_1834"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1834_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1834_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1834_2_theorem_attempt_written",
            any(row["theorem_id"] == "NHM1834_0_target" for row in rows_map["no_hypermomentum"]),
            "no-hypermomentum theorem attempt is written",
        ),
        (
            "VAL1834_3_theorem_not_promoted",
            any(row["theorem_id"] == "NHM1834_6_verdict" and row["current_status"] == "NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN" for row in rows_map["no_hypermomentum"]),
            "no-hypermomentum theorem is not promoted",
        ),
        (
            "VAL1834_4_bound_rows_staged",
            all(row["status"] == "BOUND_ROW_STAGED_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["DeltaGamma_bound"]),
            "DeltaGamma bound rows are staged and nonclaim",
        ),
        (
            "VAL1834_5_component_basis_complete",
            len(rows_map["component_basis"]) >= 7 and all(row["valid_for_claim"] is False for row in rows_map["component_basis"]),
            "DeltaGamma component basis is present and nonclaim",
        ),
        (
            "VAL1834_6_missing_rows_nonclaim",
            missing_rows_nonclaim(rows_map["DeltaGamma_bound"]) and missing_rows_nonclaim(rows_map["component_basis"]),
            "rows with missing markers remain valid_for_claim=false",
        ),
        (
            "VAL1834_7_decision_next",
            any(row["decision_id"] == "DEC1834_2_best_next" and row["decision"] == "DELTAGAMMA_COMPONENT_MAP_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects DeltaGamma component map next",
        ),
        (
            "VAL1834_8_next_selected",
            any(row["route_id"] == "NEXT1834_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1834_9_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1834_10_csv_parse", csv_parse_ok(output_paths), "all generated 1834 CSVs parse"),
        ("VAL1834_11_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1834_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1834_13_formalization_untouched", no_formalization_outputs(), "no 1834 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1834_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1834 no-hypermomentum matter functor or DeltaGamma bound row checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1834 Y5 R2FR no-hypermomentum matter functor or DeltaGamma bound row",
            "",
            "**Progress:** 1834 tests the source side of the distortion equation. If ordinary matter, source support, clocks, photons, rods, orbital readout and boundary markers all couple only through `e_obs` and `omega[e_obs]`, then `Delta_Gamma=0` and the `C=0` route can reopen. Current MTS does not yet prove that functor.",
            "",
            "**Current verdict:** no no-hypermomentum theorem yet. The clean matter-functor route is real, but the matter category, connection descent, spin-torsion silence, source/readout frame, and projective invariance are all unsigned. `Delta_Gamma` is retained as a component-wise nonclaim bound row.",
            "",
            "**Claim ceiling:** no `Delta_Gamma=0`, no `C=0`, no `T=Q=0`, no P4 pass, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1834.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## No-Hypermomentum Theorem Attempt",
            markdown_table(rows_map["no_hypermomentum"], ["theorem_id", "clause", "required_statement", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## DeltaGamma Bound Row",
            markdown_table(rows_map["DeltaGamma_bound"], ["bound_id", "quantity", "bound_formula", "bound_value", "units", "normalization", "source_path", "source_exists", "observable_map", "status", "valid_for_claim"]),
            "",
            "## DeltaGamma Component Basis",
            markdown_table(rows_map["component_basis"], ["component_id", "component", "included_in_total", "status", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a strong sharpening, not a retreat. The obstruction is no longer a foggy 'coupling problem'; it is a finite source-current vector. The next move is to map every retained `Delta_Gamma` component into observables. Then the branch can either theorem-zero components one by one, or test them without pretending the coupling disappeared.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1834 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
