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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1829"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1829_0_1828_next",
        "source_key": "1828_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_NEXT_TARGET.csv",
        "needles": ["NEXT1828_0_primary", "selected"],
        "role": "1828 selects metric-only connection theorem or P4/hinge source pack.",
    },
    {
        "source_id": "SRC1829_1_1828_validation",
        "source_key": "1828_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1828_VALIDATION.csv",
        "needles": ["VAL1828_OVERALL", "PASS"],
        "role": "confirms 1828 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1829_2_1828_connection",
        "source_key": "1828_connection_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv",
        "needles": ["CCA1828_1_metric_only", "CONDITIONAL_NOT_PARENT_DERIVED"],
        "role": "metric-only route is identified as clean but unsigned.",
    },
    {
        "source_id": "SRC1829_3_1828_hinge",
        "source_key": "1828_hinge_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1828_HINGE_BIVECTOR_OWNER_AUDIT.csv",
        "needles": ["HBA1828_5_verdict", "HINGE_OWNER_FAILS_CURRENT_CORPUS"],
        "role": "hinge/bivector owner remains unsigned.",
    },
    {
        "source_id": "SRC1829_4_P4_routes",
        "source_key": "P4_compatibility_routes",
        "source_path": P4_RUN / "compatibility_theorem_routes.csv",
        "needles": ["P4_R0_metric_formalism_if_parent_selects_only_g", "P4_R5_empirical_R11_connection_vector"],
        "role": "P4 route ledger provides theorem branch and empirical vector fallback.",
    },
    {
        "source_id": "SRC1829_5_P4_demotions",
        "source_key": "P4_connection_operator_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["torsion_nonmetricity_combined", "independent_connection_hypermomentum"],
        "role": "P4 demotion ledger lists connection residual families.",
    },
    {
        "source_id": "SRC1829_6_P4_status",
        "source_key": "P4_theorem_attempt_status",
        "source_path": P4_RUN / "theorem_attempt_status.csv",
        "needles": ["Levi-Civita compatibility parent-derived", "fail"],
        "role": "prior theorem attempt fails current Levi-Civita compatibility claim.",
    },
    {
        "source_id": "SRC1829_7_P4_gate_tests",
        "source_key": "P4_gate_tests",
        "source_path": P4_RUN / "P4_gate_tests.csv",
        "needles": ["independent_connection_absence_gate", "fail_open"],
        "role": "independent-connection absence gate remains open.",
    },
    {
        "source_id": "SRC1829_8_1045_functor",
        "source_key": "1045_matter_connection_stack",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["QG1045_2_connection_stack", "CONDITIONAL_CONNECTION_CAVEAT"],
        "role": "matter-functor theorem has a conditional connection caveat.",
    },
    {
        "source_id": "SRC1829_9_1155_coframe",
        "source_key": "1155_single_observed_coframe",
        "source_path": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
        "needles": ["COF1155_3_geometry_stack", "NOT_PARENT_SIGNED"],
        "role": "single observed coframe/source frame proof remains unsigned.",
    },
    {
        "source_id": "SRC1829_10_1542_qdef",
        "source_key": "1542_visible_quotient",
        "source_path": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
        "needles": ["QDEF1542_1_minimal_visible_candidate", "CANDIDATE_ONLY"],
        "role": "visible quotient candidate includes omega_obs but remains candidate-only.",
    },
    {
        "source_id": "SRC1829_11_1010_Gamma",
        "source_key": "1010_Gamma_Khat",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["QRES1010_1_Gamma_metric_response_gap", "retained_symbolic_gap"],
        "role": "Gamma/Khat metric-response gap remains retained.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_SOURCE_REGISTER.csv",
    "metric_only_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
    "P4_source_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_P4_CONNECTION_SOURCE_PACK.csv",
    "hinge_source_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_HINGE_SOURCE_PACK.csv",
    "c2_interlock": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_C2_P4_HINGE_INTERLOCK.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1829_VALIDATION.csv",
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


def metric_only_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_0_target",
            "claim_piece": "metric-only connection theorem",
            "statement": "If the parent configuration contains only the observed metric/coframe and ordinary matter universally uses omega[e_obs], then Gamma is definitionally Levi-Civita/spin connection and P4 closes kinematically.",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "current corpus has candidate use of omega[e_obs] but does not prove absence of independent connection variables",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_1_exact_lemma",
            "claim_piece": "kinematic Levi-Civita lemma",
            "statement": "On a metric/coframe-only configuration space, compatibility is not a dynamical assumption: omega is constructed from e_obs and torsion/nonmetricity are not independent fields.",
            "current_status": "EXACT_CONDITIONAL_LEMMA",
            "blocker": "premise is not parent-signed for MTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_2_field_inventory",
            "claim_piece": "parent field inventory excludes independent connection",
            "statement": "Parent field list must exclude Gamma/omega as an independent physical variable or show it is pure shorthand for omega[e_obs].",
            "current_status": "NOT_DERIVED",
            "blocker": "q_loc candidate lists omega_obs but does not prove it is derivative-only rather than independent data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_3_matter_no_hypermomentum",
            "claim_piece": "no independent connection charge",
            "statement": "Matter, light, spin, source and readout actions must have no hypermomentum or connection charge beyond omega[e_obs].",
            "current_status": "NOT_DERIVED",
            "blocker": "spinor torsion, projective source charge, and non-Hilbert connection currents remain legal escape routes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_4_no_shadow_connection",
            "claim_piece": "single geometry stack",
            "statement": "measure, coframe, connection and derivative operators must descend together through one observed q/e functor.",
            "current_status": "CONDITIONAL_ONLY",
            "blocker": "single observed coframe/source frame and matter functor remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_5_Gamma_Khat_reconciliation",
            "claim_piece": "Gamma_eff/K_hat compatibility",
            "statement": "Current Gamma_eff/K_hat symbols must either reduce to omega[e_obs]/metric response or be carried as explicit q_loc/P4 residuals.",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "blocker": "K_hat metric response identity remains unmatched to current symbols",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MOC1829_6_verdict",
            "claim_piece": "1829 proves metric-only connection theorem",
            "statement": "MOC1829_1 is exact, but MOC1829_2 through MOC1829_5 do not close in the current corpus.",
            "current_status": "METRIC_ONLY_THEOREM_NOT_PARENT_SIGNED",
            "blocker": "no-independent-connection parent grammar is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def P4_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_0_combined_TQ",
            "operator_family": "torsion_nonmetricity_combined",
            "needed_input": "c_T, c_Q, units, normalization, weak-field map",
            "observable_links": "R0;R1;R2;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_1_axial_spin",
            "operator_family": "axial_torsion_spin_coupling",
            "needed_input": "spin-torsion coefficient, spinor matter assumptions, clock/light/spin map",
            "observable_links": "R0;R2;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_2_projective",
            "operator_family": "torsion_trace_projective_mode",
            "needed_input": "projective proof or source/WEP coefficient and units",
            "observable_links": "R0;R1;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_3_weyl_nonmetricity",
            "operator_family": "nonmetricity_weyl_trace",
            "needed_input": "Q_mu coefficient, clock/rod calibration map, WEP/clock bound source",
            "observable_links": "R0;R2;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_4_shear_nonmetricity",
            "operator_family": "nonmetricity_shear_lightcone",
            "needed_input": "trace-free Q coefficient, lightcone/clock/WEP map",
            "observable_links": "R0;R2;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_5_hypermomentum",
            "operator_family": "independent_connection_hypermomentum",
            "needed_input": "matter/source/readout Gamma-dependence theorem or hypermomentum residual coefficient",
            "observable_links": "R0;R1;R2;R11",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4SP1829_6_total",
            "operator_family": "P4_connection_vector",
            "needed_input": "all P4SP1829_0 through P4SP1829_5 source-backed or theorem-zero",
            "observable_links": "WEP;clock;spin;lightcone;operator_ledger",
            "status": "P4_VECTOR_READY_SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def hinge_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HSP1829_0_cell_complex",
            "quantity": "local_cell_hinge_complex",
            "needed_input": "parent-selected cells, hinges/faces, adjacency, refinement law",
            "status": "MISSING_CELL_COMPLEX_SOURCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HSP1829_1_area_bivector",
            "quantity": "B_h_or_A_h",
            "needed_input": "B_h = integral_h e wedge e, area units, source path, orientation convention",
            "status": "MISSING_AREA_BIVECTOR_SOURCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HSP1829_2_orientation",
            "quantity": "physical_hinge_orientation",
            "needed_input": "relative-chain/boundary theorem proving sign is physical not gauge",
            "status": "MISSING_ORIENTATION_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HSP1829_3_scale_shape",
            "quantity": "ell_cell_and_shape_factor",
            "needed_input": "cell scale, shape factor, uncertainty, continuum convention",
            "status": "MISSING_SCALE_SHAPE_SOURCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HSP1829_4_total",
            "quantity": "hinge_source_pack",
            "needed_input": "HSP1829_0 through HSP1829_3 all source-backed or parent-derived",
            "status": "HINGE_SOURCE_PACK_READY_SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def c2_interlock_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interlock_id": "INT1829_0_zero_route",
            "condition": "metric-only connection plus Palatini/Regge hinge action closes",
            "effect": "visible c2 zero route becomes much more credible but still needs action/variation/source gates",
            "current_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interlock_id": "INT1829_1_P4_interlock",
            "condition": "P4 connection residues survive",
            "effect": "finite c2/R2-fR scalaron map cannot be scored as local-GR-safe without P4 rows",
            "current_status": "P4_ROWS_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interlock_id": "INT1829_2_hinge_interlock",
            "condition": "hinge scale/shape missing",
            "effect": "c_R2_eff normalization remains undefined even if c2_visible is known",
            "current_status": "HINGE_SOURCE_PACK_REQUIRED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interlock_id": "INT1829_3_total",
            "condition": "current 1829 status",
            "effect": "no c2 zero and no finite c2 score; carry theorem-or-vector fork forward",
            "current_status": "NO_CLAIM_KEEP_DERIVING",
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1829_0_theorem_attempt",
            "gate": "metric-only theorem attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "exact kinematic lemma plus missing parent premises are recorded",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1829_1_parent_signed",
            "gate": "metric-only connection theorem parent-signed",
            "current_status": "BLOCKED",
            "reason": "no-independent-connection grammar is missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1829_2_P4_pack",
            "gate": "P4 connection source pack claim-ready",
            "current_status": "BLOCKED",
            "reason": "all P4 rows are source-pack schemas only",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1829_3_hinge_pack",
            "gate": "hinge source pack claim-ready",
            "current_status": "BLOCKED",
            "reason": "cell complex, area, orientation and scale are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1829_0_metric_only",
            "claim": "metric-only connection theorem derived",
            "status": "BLOCKED",
            "reason": "MTS does not yet prove absence of independent connection/hypermomentum",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1829_1_P4_vector",
            "claim": "P4 connection vector score-ready",
            "status": "BLOCKED",
            "reason": "P4 rows have no coefficients, units, maps, or source paths",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1829_2_c2",
            "claim": "c2 zero or finite c2 score-ready",
            "status": "BLOCKED",
            "reason": "connection and hinge interlocks are open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1829_3_local_GR",
            "claim": "local GR/Newton follows",
            "status": "REFUSED",
            "reason": "connection theorem/source pack only; source, q_loc, PPN, matter descent and operator gates remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1829_0_theorem_result",
            "decision": "METRIC_ONLY_CONNECTION_THEOREM_NOT_SIGNED",
            "reason": "the kinematic lemma is exact, but the parent grammar does not exclude independent connection or hypermomentum",
            "next_action": "do not promote Levi-Civita compatibility",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1829_1_vector_result",
            "decision": "P4_HINGE_SOURCE_PACK_STAGED_NONCLAIM",
            "reason": "torsion/nonmetricity/hypermomentum rows and hinge cell-scale rows are now explicit fallback debts",
            "next_action": "fill only with real coefficients or theorem-zero certificates",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1829_2_best_next",
            "decision": "NO_INDEPENDENT_CONNECTION_GRAMMAR_OR_P4_ROW_FILL_NEXT",
            "reason": "the least-cheaty derivation route is now field-inventory grammar: prove no independent connection slot exists",
            "next_action": "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1829_0_primary",
            "next_target": "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md",
            "script": "scripts/Y5_R2FR_no_independent_connection_parent_grammar_or_P4_row_fill.py",
            "objective": "prove the parent field grammar has no independent connection/hypermomentum slot; if not, start filling executable P4 connection rows with coefficients, units, source paths, and weak-field maps",
            "selection_status": "selected",
            "success_condition": "no-independent-connection theorem parent-signed, or P4 rows remain valid_for_claim=false with explicit missing inputs",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1829_1_parallel",
            "next_target": "1830b-Y5-R2FR-hinge-cell-scale-source-pack-fill.md",
            "script": "scripts/Y5_R2FR_hinge_cell_scale_source_pack_fill.py",
            "objective": "source or derive cell complex, B_h/A_h, orientation, ell_cell and shape_factor needed for Regge/c2 normalization",
            "selection_status": "held_parallel",
            "success_condition": "hinge rows become parent-derived or source-backed nonclaim inputs",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "metric_only_attempt": metric_only_attempt_rows(),
        "P4_source_pack": P4_source_pack_rows(),
        "hinge_source_pack": hinge_source_pack_rows(),
        "c2_interlock": c2_interlock_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
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
    guarded_keys = {"valid_for_claim", "claim_allowed", "gate_pass"}
    for key, rows in rows_map.items():
        if key == "acceptance_gate":
            continue
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1829-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1829") or name.startswith("P8_Y5_BRR545_1829"):
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
        ("VAL1829_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1829_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        ("VAL1829_2_theorem_attempt_written", any(row["attempt_id"] == "MOC1829_0_target" for row in rows_map["metric_only_attempt"]), "metric-only theorem attempt is written"),
        (
            "VAL1829_3_exact_lemma_nonclaim",
            any(row["attempt_id"] == "MOC1829_1_exact_lemma" and row["current_status"] == "EXACT_CONDITIONAL_LEMMA" and row["valid_for_claim"] is False for row in rows_map["metric_only_attempt"]),
            "exact metric-only lemma is recorded as conditional nonclaim",
        ),
        (
            "VAL1829_4_theorem_not_promoted",
            any(row["attempt_id"] == "MOC1829_6_verdict" and row["current_status"] == "METRIC_ONLY_THEOREM_NOT_PARENT_SIGNED" for row in rows_map["metric_only_attempt"]),
            "metric-only theorem is not promoted",
        ),
        (
            "VAL1829_5_P4_pack_nonclaim",
            any(row["row_id"] == "P4SP1829_6_total" and row["status"] == "P4_VECTOR_READY_SCHEMA_ONLY_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["P4_source_pack"]),
            "P4 source pack is schema-only nonclaim",
        ),
        (
            "VAL1829_6_hinge_pack_nonclaim",
            any(row["row_id"] == "HSP1829_4_total" and row["status"] == "HINGE_SOURCE_PACK_READY_SCHEMA_ONLY_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["hinge_source_pack"]),
            "hinge source pack is schema-only nonclaim",
        ),
        (
            "VAL1829_7_c2_interlock_blocks",
            any(row["interlock_id"] == "INT1829_3_total" and row["current_status"] == "NO_CLAIM_KEEP_DERIVING" for row in rows_map["c2_interlock"]),
            "c2/P4/hinge interlock blocks claims",
        ),
        (
            "VAL1829_8_acceptance_blocks",
            any(row["gate_id"] == "AC1829_0_theorem_attempt" and row["gate_pass"] is True and row["claim_allowed"] is False for row in rows_map["acceptance_gate"])
            and all(row["claim_allowed"] is False for row in rows_map["acceptance_gate"]),
            "acceptance gate allows contract-only progress and blocks claims",
        ),
        (
            "VAL1829_9_claim_gates_blocked",
            all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in rows_map["claim_gate"]),
            "all metric/P4/c2/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1829_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true outside contract-only acceptance"),
        (
            "VAL1829_11_decision_next",
            any(row["decision_id"] == "DEC1829_2_best_next" and row["decision"] == "NO_INDEPENDENT_CONNECTION_GRAMMAR_OR_P4_ROW_FILL_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects no-independent-connection grammar or P4 row fill next",
        ),
        (
            "VAL1829_12_next_selected",
            any(row["route_id"] == "NEXT1829_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1829_13_csv_parse", csv_parse_ok(output_paths), "all generated 1829 CSVs parse"),
        ("VAL1829_14_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1829_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1829_16_formalization_untouched", no_formalization_outputs(), "no 1829 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1829_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1829 metric-only connection theorem or P4 hinge source pack checkpoint",
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
            "# 1829 Y5 R2FR metric-only connection theorem or P4 hinge source pack",
            "",
            "**Progress:** 1829 writes the cleanest possible connection theorem as an exact conditional lemma: if the parent has only the observed metric/coframe and all sectors use `omega[e_obs]`, Levi-Civita compatibility is kinematic. The current corpus does not yet sign that parent field grammar, so the theorem is not promoted.",
            "",
            "**Current verdict:** no connection claim yet. The next derivation target is now even narrower: prove there is no independent connection/hypermomentum slot in the parent grammar. If that fails, the P4 torsion/nonmetricity/hypermomentum rows and hinge source-pack rows must be filled as explicit nonclaim residual inputs.",
            "",
            "**Claim ceiling:** no Levi-Civita compatibility claim, no P4 pass, no `c2` zero/score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1829.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Metric Only Connection Theorem Attempt",
            markdown_table(rows_map["metric_only_attempt"], ["attempt_id", "claim_piece", "statement", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## P4 Connection Source Pack",
            markdown_table(rows_map["P4_source_pack"], ["row_id", "operator_family", "needed_input", "observable_links", "status", "valid_for_claim"]),
            "",
            "## Hinge Source Pack",
            markdown_table(rows_map["hinge_source_pack"], ["row_id", "quantity", "needed_input", "status", "valid_for_claim"]),
            "",
            "## C2 P4 Hinge Interlock",
            markdown_table(rows_map["c2_interlock"], ["interlock_id", "condition", "effect", "current_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This is not grim; it is the right narrowing. GR does not need us to separately kill torsion and nonmetricity if MTS can prove the parent never had those independent slots. But if MTS cannot prove that field grammar, then connection residues must be treated like real modified-gravity channels and tested, not wished away.",
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
    print(f"1829 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
