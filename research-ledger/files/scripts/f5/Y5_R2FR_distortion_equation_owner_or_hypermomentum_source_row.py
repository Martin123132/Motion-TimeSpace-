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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1833"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1833-Y5-R2FR-distortion-equation-owner-or-hypermomentum-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1833_0_1832_next",
        "source_key": "1832_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_NEXT_TARGET.csv",
        "needles": ["NEXT1832_0_primary", "selected"],
        "role": "1832 selects distortion equation owner or hypermomentum source row.",
    },
    {
        "source_id": "SRC1833_1_1832_validation",
        "source_key": "1832_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1832_VALIDATION.csv",
        "needles": ["VAL1832_OVERALL", "PASS"],
        "role": "confirms 1832 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1833_2_1832_distortion_contract",
        "source_key": "1832_distortion_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_DISTORTION_EQUATION_CONTRACT.csv",
        "needles": ["DC1832_1_equation", "MISSING_EQUATION"],
        "role": "distortion equation contract requiring M_C, Delta_Gamma, boundary and projective pieces.",
    },
    {
        "source_id": "SRC1833_3_1832_TQ_attempt",
        "source_key": "1832_TQ_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_TQ_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["TQ1832_6_verdict", "TQ_ZERO_THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "torsion/nonmetricity zero theorem did not close.",
    },
    {
        "source_id": "SRC1833_4_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["independent_connection_hypermomentum", "not_forbidden"],
        "role": "hypermomentum/source connection channel is retained as legal.",
    },
    {
        "source_id": "SRC1833_5_P4_templates",
        "source_key": "P4_templates",
        "source_path": P4_RUN / "P4_R11_template_rows.csv",
        "needles": ["independent_connection_hypermomentum", "fill_numeric_or_zero"],
        "role": "template schema for hypermomentum/source row if theorem fails.",
    },
    {
        "source_id": "SRC1833_6_1045_matter",
        "source_key": "1045_matter_connection_stack",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["QG1045_2_connection_stack", "CONDITIONAL_CONNECTION_CAVEAT"],
        "role": "matter connection descent is conditional and keeps independent connection caveat.",
    },
    {
        "source_id": "SRC1833_7_537_parent_action_contract",
        "source_key": "537_parent_action_contract",
        "source_path": ROOT / "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
        "needles": ["PAC537_0_covariant_parent_action", "PAC537_7_extra_sector_mass_charge_silence"],
        "role": "parent-action contract supplies the needed variational scaffold but not this C-equation.",
    },
    {
        "source_id": "SRC1833_8_538_Euler_Ward",
        "source_key": "538_Euler_Ward",
        "source_path": ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "needles": ["EW538_0_variation", "DAT537_4_PiM_Hilbert_identification"],
        "role": "Euler/Ward chain is conditional and source-charge identification remains open.",
    },
    {
        "source_id": "SRC1833_9_1010_Gamma_Khat",
        "source_key": "1010_Gamma_Khat",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_3_Euler_closure", "QRES1010_3_source_boundary_gap"],
        "role": "Gamma/Khat action route keeps source-current and boundary gaps explicit.",
    },
    {
        "source_id": "SRC1833_10_1561_ansatz",
        "source_key": "1561_minimal_ansatz",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["ANS1561_A_EH_lambdaR_silent", "NOT_ADOPTED_CURRENT_MTS_DERIVATION"],
        "role": "EH-style repair ansatz is not accepted as current MTS derivation.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_SOURCE_REGISTER.csv",
    "distortion_owner": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DISTORTION_EQUATION_OWNER_AUDIT.csv",
    "operator_decomposition": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_OPERATOR_DECOMPOSITION_CONTRACT.csv",
    "hypermomentum_source": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv",
    "boundary_projective": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_BOUNDARY_PROJECTIVE_LEDGER.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1833_VALIDATION.csv",
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


def distortion_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_0_target",
            "equation_piece": "parent distortion equation",
            "required_form": "delta_C S_parent = M_C C - Delta_Gamma + B_C + P_projective = 0",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "equation is not present as an MTS parent variation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_1_C_variable_owner",
            "equation_piece": "distortion variable C",
            "required_form": "C is either absent, auxiliary, dynamical, projective/gauge, or retained residual before readout",
            "current_status": "NOT_PARENT_OWNED",
            "blocker": "1831 did not certify the field inventory and 1832 retained C as unresolved",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_2_M_C_operator",
            "equation_piece": "bulk connection operator M_C",
            "required_form": "M_C is explicit, covariant, symmetric/integrable, positive or invertible on nonprojective C modes",
            "current_status": "MISSING_PARENT_OPERATOR",
            "blocker": "no action row supplies c_T, c_Q, c_TQ or the operator basis with signs and units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_3_Delta_Gamma_source",
            "equation_piece": "hypermomentum/source current",
            "required_form": "Delta_Gamma := delta(S_matter + S_source + S_readout)/delta Gamma in the same branch",
            "current_status": "NOT_ZEROED_OR_SOURCED",
            "blocker": "ordinary matter/source/readout independence from independent Gamma is only conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_4_boundary_term",
            "equation_piece": "connection boundary work B_C",
            "required_form": "all integration-by-parts, symplectic and support-boundary C terms vanish or are retained as rows",
            "current_status": "BOUNDARY_GAP_RETAINED",
            "blocker": "Gamma/Khat and worldtube files retain source-boundary gaps",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_5_projective_kernel",
            "equation_piece": "projective kernel",
            "required_form": "projective trace is fixed, gauge, or invisible to all matter/light/clock/source sectors",
            "current_status": "PROJECTIVE_KERNEL_OPEN",
            "blocker": "projective invariance is not proved sector-by-sector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "DEO1833_6_verdict",
            "equation_piece": "distortion equation owner",
            "required_form": "DEO1833_1 through DEO1833_5 close in one parent action",
            "current_status": "DISTORTION_EQUATION_OWNER_NOT_PROVEN",
            "blocker": "M_C, Delta_Gamma, boundary and projective pieces remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def operator_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "operator_id": "OPD1833_0_torsion_irreducible",
            "operator_block": "torsion irreducible blocks",
            "needed_fields": "c_vector_T;c_axial_T;c_tensor_T;units;sign;normalization",
            "current_status": "MISSING_OPERATOR_VALUES",
            "zero_condition": "positive/invertible torsion block and no spin/hypermomentum source",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "OPD1833_1_nonmetricity_trace",
            "operator_block": "Weyl/nonmetricity trace block",
            "needed_fields": "c_Qtrace;clock_rod_normalization;units;sign",
            "current_status": "MISSING_OPERATOR_VALUES",
            "zero_condition": "positive/invertible Q trace block and no clock/rod/source current",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "OPD1833_2_nonmetricity_shear",
            "operator_block": "trace-free nonmetricity/lightcone block",
            "needed_fields": "c_Qshear;lightcone_normalization;units;sign",
            "current_status": "MISSING_OPERATOR_VALUES",
            "zero_condition": "positive/invertible shear block and no lightcone source current",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "OPD1833_3_mixed_TQ",
            "operator_block": "torsion/nonmetricity mixed block",
            "needed_fields": "c_TQ;operator_basis;diagonalization;positivity",
            "current_status": "MISSING_OPERATOR_BASIS",
            "zero_condition": "full M_C matrix is positive after mixed block diagonalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "OPD1833_4_projective",
            "operator_block": "projective trace block",
            "needed_fields": "gauge_fix_or_invariance;source_visibility;boundary_condition",
            "current_status": "MISSING_PROJECTIVE_PROOF",
            "zero_condition": "projective mode is fixed or invisible to every retained sector",
            "valid_for_claim": False,
        },
    ]


def hypermomentum_source_rows() -> list[dict[str, Any]]:
    source_path = P4_RUN / "P4_R11_template_rows.csv"
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HYP1833_0_Delta_Gamma_total",
            "source_current": "Delta_Gamma_total",
            "definition": "delta(S_matter + S_source + S_readout)/delta Gamma",
            "components": "spin_hypermomentum;source_support_current;readout_connection_current;projective_trace_current",
            "value": "MISSING_PARENT_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "units": "MISSING_HYPERMOMENTUM_UNITS",
            "normalization": "MISSING_CONNECTION_VARIATION_NORMALIZATION",
            "weak_field_map": "MISSING_DELTA_GAMMA_TO_PPN_WEP_CLOCK_MAP",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "status": "SOURCE_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HYP1833_1_spin",
            "source_current": "spin_hypermomentum",
            "definition": "spinor/tetrad matter connection charge beyond omega[e_obs]",
            "components": "axial_torsion_spin_coupling",
            "value": "MISSING_NO_SPIN_TORSION_THEOREM_OR_BOUND",
            "units": "MISSING_SPIN_CURRENT_UNITS",
            "normalization": "MISSING_SPIN_CONNECTION_NORMALIZATION",
            "weak_field_map": "MISSING_SPIN_CLOCK_LIGHTCONE_MAP",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "status": "SOURCE_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HYP1833_2_source_readout",
            "source_current": "source_readout_connection_current",
            "definition": "non-Hilbert source, support and readout dependence on independent Gamma",
            "components": "source_support;clock_readout;orbital_readout;boundary_marker",
            "value": "MISSING_SOURCE_READOUT_ZERO_OR_BOUND",
            "units": "MISSING_SOURCE_CURRENT_UNITS",
            "normalization": "MISSING_READOUT_BRANCH_NORMALIZATION",
            "weak_field_map": "MISSING_SOURCE_TO_R10_PPN_ORBITAL_MAP",
            "source_path": str(source_path),
            "source_exists": source_path.exists(),
            "status": "SOURCE_ROW_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def boundary_projective_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "BPL1833_0_boundary_C",
            "residual": "B_C",
            "definition": "boundary/symplectic/support work from varying C or Gamma",
            "required_zero": "compact-support no-flux theorem or explicit boundary row",
            "current_status": "MISSING_BOUNDARY_NO_FLUX",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "BPL1833_1_projective_trace",
            "residual": "P_projective",
            "definition": "projective trace kernel of connection variation",
            "required_zero": "fixed gauge, algebraic constraint, or universal projective invariance",
            "current_status": "MISSING_PROJECTIVE_INVARIANCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ledger_id": "BPL1833_2_metric_response_overlap",
            "residual": "Delta_K_boundary",
            "definition": "mismatch between K_hat and metric/connection response after derivative boundary terms",
            "required_zero": "Gamma/Khat action-existence and boundary-matching certificate",
            "current_status": "MISSING_METRIC_RESPONSE_BOUNDARY_MATCH",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1833_0_equation_owner_result",
            "decision": "DISTORTION_EQUATION_OWNER_NOT_PROVEN",
            "reason": "the current corpus has variational contracts but no parent C/Gamma variation supplying M_C, Delta_Gamma, boundary and projective terms",
            "next_action": "do not claim C=0, T=Q=0, Levi-Civita compatibility, or local GR",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1833_1_source_row_result",
            "decision": "HYPERMOMENTUM_SOURCE_ROW_STAGED_NONCLAIM",
            "reason": "matter/source/readout Gamma-current is the first concrete source-side object to theorem-zero or bound",
            "next_action": "derive no-hypermomentum matter functor or fill Delta_Gamma bound row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1833_2_best_next",
            "decision": "NO_HYPERMOMENTUM_THEOREM_OR_DELTAGAMMA_BOUND_NEXT",
            "reason": "M_C cannot prove C=0 until the right-hand source current is either zero by parent functor or quantitatively bounded",
            "next_action": "1834-Y5-R2FR-no-hypermomentum-matter-functor-or-DeltaGamma-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1833_0_primary",
            "next_target": "1834-Y5-R2FR-no-hypermomentum-matter-functor-or-DeltaGamma-bound-row.md",
            "script": "scripts/Y5_R2FR_no_hypermomentum_matter_functor_or_DeltaGamma_bound_row.py",
            "objective": "prove ordinary matter, source and readout actions are independent of independent Gamma beyond omega[e_obs]; if not, fill a nonclaim Delta_Gamma bound row",
            "selection_status": "selected",
            "success_condition": "no-hypermomentum theorem is parent-signed, or Delta_Gamma residual row has source-ready units and maps but remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1833_1_secondary",
            "next_target": "1834b-Y5-R2FR-projective-boundary-kernel-gate.md",
            "script": "scripts/Y5_R2FR_projective_boundary_kernel_gate.py",
            "objective": "separately fix or map projective trace and boundary C residuals",
            "selection_status": "held_secondary",
            "success_condition": "projective and boundary kernels become theorem-zero or explicit residual rows",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "distortion_owner": distortion_owner_rows(),
        "operator_decomposition": operator_decomposition_rows(),
        "hypermomentum_source": hypermomentum_source_rows(),
        "boundary_projective": boundary_projective_rows(),
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
        if "1833-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1833") or name.startswith("P8_Y5_BRR545_1833"):
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
        ("VAL1833_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1833_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL1833_2_owner_audit_written",
            any(row["owner_id"] == "DEO1833_0_target" for row in rows_map["distortion_owner"]),
            "distortion equation owner audit is written",
        ),
        (
            "VAL1833_3_owner_not_promoted",
            any(row["owner_id"] == "DEO1833_6_verdict" and row["current_status"] == "DISTORTION_EQUATION_OWNER_NOT_PROVEN" for row in rows_map["distortion_owner"]),
            "distortion equation owner is not promoted",
        ),
        (
            "VAL1833_4_operator_contract_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["operator_decomposition"]),
            "operator decomposition contract remains nonclaim",
        ),
        (
            "VAL1833_5_hypermomentum_rows_staged",
            all(row["status"] == "SOURCE_ROW_STAGED_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["hypermomentum_source"]),
            "hypermomentum/source rows are staged and nonclaim",
        ),
        (
            "VAL1833_6_missing_rows_nonclaim",
            missing_rows_nonclaim(rows_map["operator_decomposition"]) and missing_rows_nonclaim(rows_map["hypermomentum_source"]) and missing_rows_nonclaim(rows_map["boundary_projective"]),
            "rows with missing markers remain valid_for_claim=false",
        ),
        (
            "VAL1833_7_boundary_projective_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["boundary_projective"]),
            "boundary/projective ledger remains nonclaim",
        ),
        (
            "VAL1833_8_decision_next",
            any(row["decision_id"] == "DEC1833_2_best_next" and row["decision"] == "NO_HYPERMOMENTUM_THEOREM_OR_DELTAGAMMA_BOUND_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects no-hypermomentum theorem or DeltaGamma bound next",
        ),
        (
            "VAL1833_9_next_selected",
            any(row["route_id"] == "NEXT1833_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1833_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1833_11_csv_parse", csv_parse_ok(output_paths), "all generated 1833 CSVs parse"),
        ("VAL1833_12_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1833_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1833_14_formalization_untouched", no_formalization_outputs(), "no 1833 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1833_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1833 distortion equation owner or hypermomentum source row checkpoint",
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
            "# 1833 Y5 R2FR distortion equation owner or hypermomentum source row",
            "",
            "**Progress:** 1833 turns the distortion question into a parent-action ownership test. The exact desired equation is `delta_C S_parent = M_C C - Delta_Gamma + B_C + P_projective = 0`. If `M_C` is positive/invertible and the right-hand residuals vanish, the local Levi-Civita route becomes clean. Current MTS does not yet own that equation.",
            "",
            "**Current verdict:** no distortion-equation theorem yet. The corpus has variational scaffolds and P4 templates, but no parent variation that supplies `M_C`, no parent-signed `Delta_Gamma=0`, no boundary no-flux theorem for `C`, and no all-sector projective-invariance proof. The hypermomentum/source row is therefore staged as the next nonclaim object.",
            "",
            "**Claim ceiling:** no `C=0`, no `T=Q=0`, no Levi-Civita compatibility, no P4 pass, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1833.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Distortion Equation Owner Audit",
            markdown_table(rows_map["distortion_owner"], ["owner_id", "equation_piece", "required_form", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## Operator Decomposition Contract",
            markdown_table(rows_map["operator_decomposition"], ["operator_id", "operator_block", "needed_fields", "current_status", "zero_condition", "valid_for_claim"]),
            "",
            "## Hypermomentum / Source Row",
            markdown_table(rows_map["hypermomentum_source"], ["row_id", "source_current", "definition", "components", "value", "units", "normalization", "weak_field_map", "source_path", "source_exists", "status", "valid_for_claim"]),
            "",
            "## Boundary / Projective Ledger",
            markdown_table(rows_map["boundary_projective"], ["ledger_id", "residual", "definition", "required_zero", "current_status", "valid_for_claim"]),
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
            "This is the coupling problem in its sharpest local-GR form. The theory does not need to beat GR by decorative complexity here; it needs to show the right-hand side of the distortion equation is zero, or small. The next best shot is the no-hypermomentum theorem: prove matter/source/readout never couple to an independent connection beyond `omega[e_obs]`. If that fails, `Delta_Gamma` becomes an explicit bounded residual.",
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
    print(f"1833 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
