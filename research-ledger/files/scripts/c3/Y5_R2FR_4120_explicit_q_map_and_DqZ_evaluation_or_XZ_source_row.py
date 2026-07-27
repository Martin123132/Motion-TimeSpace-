from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4120-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-XZ-source-row.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_DQXZ_COMPONENT_NORM_CURRENT_SPINE_4120"
CHECKPOINT_ID = "4120"
DECISION = "DQXZ_POSITIVE_COMPONENT_NORM_DERIVED_SOURCE_EM_READOUT_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4120_00_4119_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4119_NEXT_TARGET.csv",
        "4120-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-XZ-source-row.md",
        "4119 selected explicit q-map and DqZ/DqX evaluation.",
    ),
    "SRC4120_01_4119_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4119_STATUS.csv",
        "STRICT_QUOTIENT_ABSENT_POLE_THEOREM_CONSTRUCTED_DQZ_EVALUATION_NEXT",
        "Current-chain strict quotient theorem handoff.",
    ),
    "SRC4120_02_4119_targets": (
        SOURCE_DIR / "P8_Y5_R2FR_4119_DQZ_COMPONENT_TARGETS.csv",
        "DQZ4119_5_EM_stress",
        "4119 component target list including EM/Poynting separation.",
    ),
    "SRC4120_03_3634_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3634_STATUS.csv",
        "DQZ_COMPONENT_NORM_DERIVED_SOURCE_READOUT_NEXT",
        "Older DqZ component norm checkpoint.",
    ),
    "SRC4120_04_3634_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_3634_QMAP_COMPONENT_NORM.csv",
        "NORM3634_0_full_definition",
        "Older positive component norm definition for Dq_Z.",
    ),
    "SRC4120_05_3634_lemma": (
        SOURCE_DIR / "P8_Y5_R2FR_3634_DQZ_NO_CANCELLATION_LEMMA.csv",
        "LEM3634_0_positive_norm",
        "Older no-cancellation lemma.",
    ),
    "SRC4120_06_3634_components": (
        SOURCE_DIR / "P8_Y5_R2FR_3634_DQZ_COMPONENT_EVALUATION.csv",
        "DQZ3634_1_source_readout",
        "Older source/readout high-pressure component.",
    ),
    "SRC4120_07_1667_dq_tests": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "Dq",
        "Prior Dq-on-Z/phi tests.",
    ),
    "SRC4120_08_1667_retained": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
        "Dsource_readout",
        "Retained Dq leak rows for source/readout and boundary/projector.",
    ),
    "SRC4120_09_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4120_explicit_q_map_and_DqZ_evaluation_or_XZ_source_row.py",
        "Reproducible generator for this 4120 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def norm_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "NORM4120_0_DqZ_full",
            "Dq_Z_norm",
            "||Dq[partial_Z]||_Q^2=w_G||partial_Z G_obs||^2+w_M||partial_Z M_obs||^2+w_T||partial_Z Theta_obs||^2+w_B||partial_Z B_obs||^2+w_EM||partial_Z EM_obs||^2",
            "all weights positive and all component norms dimensionless after arena normalization",
            "Dq_Z_norm=0 iff every listed partial_Z component is zero",
            "EXACT_POSITIVE_COMPONENT_NORM",
        ),
        (
            "NORM4120_1_DqX_full",
            "Dq_X_norm",
            "||Dq[partial_X]||_Q^2=w_G||partial_X G_obs||^2+w_M||partial_X M_obs||^2+w_T||partial_X Theta_obs||^2+w_B||partial_X B_obs||^2+w_EM||partial_X EM_obs||^2",
            "same norm structure for the parallel X residual family",
            "Dq_X_norm=0 iff every listed partial_X component is zero",
            "EXACT_POSITIVE_COMPONENT_NORM",
        ),
        (
            "NORM4120_2_geometry",
            "G_obs=(e_obs,g_obs,nabla_obs)",
            "||partial_A G_obs||_G^2 for A in {X,Z}",
            "observed local frame/coframe/metric/connection norm",
            "partial_A e_obs=partial_A g_obs=partial_A nabla_obs=0",
            "COMPONENT_DEFINED_NOT_EVALUATED",
        ),
        (
            "NORM4120_3_source_readout",
            "M_obs=(mu_obs,GM_readout,Hamiltonian_source_mass,orbit_normalization)",
            "||partial_A M_obs||_M^2 for A in {X,Z}",
            "source/readout norm after reference mass/Hamiltonian normalization",
            "partial_A mu_obs=partial_A GM_readout=partial_A source_charge=0",
            "HIGHEST_PRESSURE_COMPONENT_NOT_EVALUATED",
        ),
        (
            "NORM4120_4_clock_marker",
            "Theta_obs=(clock_map,constants_marker,material_marker)",
            "||partial_A Theta_obs||_T^2 for A in {X,Z}",
            "clock/material marker norm",
            "partial_A clock and marker maps vanish",
            "COMPONENT_DEFINED_NOT_EVALUATED",
        ),
        (
            "NORM4120_5_boundary_projector",
            "B_obs=(boundary_projector,collar_charge,Pi_M)",
            "||partial_A B_obs||_B^2 plus Q_boundary[partial_A] proper/zero",
            "boundary/projector norm plus edge-charge gate",
            "partial_A boundary projector vanishes and Q_boundary is zero/exact/proper",
            "BOUNDARY_COMPONENT_DEFINED_NOT_EVALUATED",
        ),
        (
            "NORM4120_6_EM_Poynting",
            "EM_obs=(Maxwell_F,T_EM,Poynting_flux)",
            "||partial_A EM_obs||_EM^2 for A in {X,Z}",
            "Maxwell stress/Poynting flux norm, or separate physical coefficient if not q-owned",
            "partial_A EM stress/readout vanishes or EM flux is scored separately",
            "EM_COMPONENT_DEFINED_NOT_EVALUATED",
        ),
    ]
    for norm_id, symbol, formula, units, zero_condition, status in data:
        row = row_base()
        row.update(
            {
                "norm_id": norm_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "zero_condition": zero_condition,
                "current_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def lemma_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "LEM4120_0_positive_norm",
            "For positive weights and positive-definite component norms, Dq_A_norm=0 is equivalent to componentwise zero for A in {X,Z}.",
            "sum_i w_i||partial_A q_i||^2=0 with w_i>0 implies partial_A q_i=0 for every i.",
            "This forbids cancelling a source/readout leak against geometry or EM by signs.",
            "PROVED_CONDITIONAL_ON_NORM_CHOICE",
        ),
        (
            "LEM4120_1_component_zero_contract",
            "Strict quotient absence requires five separate zeros: geometry, source/readout, clock/marker, boundary/projector, and EM/Poynting.",
            "Dq[partial_A]=(partial_A G_obs,partial_A M_obs,partial_A Theta_obs,partial_A B_obs,partial_A EM_obs).",
            "Geometry-only verticality is insufficient for coupling/local-GR claims.",
            "PROVED_AS_DEFINITIONAL_SPLIT",
        ),
        (
            "LEM4120_2_failure_mode",
            "If any component derivative is nonzero or unsigned, A in {X,Z} cannot be promoted to an absent quotient fibre for local tests.",
            "nonzero partial_A q_i implies Dq[partial_A] != 0.",
            "The branch moves to J_A/Dq leak coefficient rows instead of another theorem-zero pass.",
            "PROVED_DECISION_RULE",
        ),
    ]
    for lemma_id, statement, proof, consequence, status in data:
        row = row_base()
        row.update(
            {
                "lemma_id": lemma_id,
                "statement": statement,
                "proof": proof,
                "consequence": consequence,
                "current_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def component_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("CMP4120_0_geometry_Z", "partial_Z G_obs", "zero if observed geometry is defined wholly from quotient q and Z is only representative fibre", "UNSIGNED_ZERO_CANDIDATE", "explicit e_obs(Phi), g_obs(Phi), nabla_obs(Phi) with no Z dependence", "R0 geometry; PPN metric residuals"),
        ("CMP4120_1_geometry_X", "partial_X G_obs", "parallel X geometry test", "UNSIGNED_ZERO_CANDIDATE", "explicit observed geometry map with no X dependence", "R0/R3/R4 geometry"),
        ("CMP4120_2_source_Z", "partial_Z M_obs", "zero only if source mass, GM calibration, Hamiltonian normalization, and orbit/readout maps descend through q", "OPEN_HIGHEST_PRESSURE_COMPONENT", "derive source/readout descent or compute nonzero Z source leakage", "J_Z; WEP; R10/R11 source normalization; orbital/clock leakage"),
        ("CMP4120_3_source_X", "partial_X M_obs", "parallel X source/readout leakage test", "OPEN_HIGHEST_PRESSURE_COMPONENT", "derive X source/readout descent or compute nonzero X source leakage", "J_X; R10/R11 fifth-force/source charge"),
        ("CMP4120_4_clock_marker", "partial_A Theta_obs", "zero if clocks/constants/material markers are fixed standards or q-owned", "OPEN", "explicit clock and marker map independent of X/Z", "clock redshift; material constants; EM/fine-structure style channels"),
        ("CMP4120_5_boundary_projector", "partial_A B_obs and Q_boundary[partial_A]", "zero/exact/proper if boundary class and Pi_M are q-owned", "OPEN_BOUNDARY_RISK", "boundary charge and projector silence on local collar", "alpha3; xi; memory flux; source normalization edge rows"),
        ("CMP4120_6_EM_Poynting", "partial_A EM_obs", "zero only if Maxwell stress/Poynting flux is q-owned or absent; otherwise score it as physical stress/flux", "OPEN_EM_RISK", "derive EM stress descent or retain an EM/Poynting coefficient", "Maxwell limit; EM stress; source coupling; boundary flux"),
        ("CMP4120_7_verdict", "Dq_XZ_norms", "exact positive component norm exists and prevents cancellations", "FORMULA_FILLED_NOT_THEOREM_ZERO", "prove all components zero or score the first nonzero component", "source/readout descent is next because it directly owns coupling"),
    ]
    for component_id, derivative, zero_condition, status, next_input, affected in data:
        row = row_base()
        row.update(
            {
                "component_id": component_id,
                "derivative": derivative,
                "zero_condition": zero_condition,
                "current_status": status,
                "needed_input": next_input,
                "affected_arena": affected,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def filled_rows() -> List[dict]:
    rows: List[dict] = []
    formulas = [
        (
            "DQL4120_0_Dq_Z_filled_formula",
            "Dq_Z_norm",
            "sqrt(w_G||partial_Z G_obs||^2+w_M||partial_Z M_obs||^2+w_T||partial_Z Theta_obs||^2+w_B||partial_Z B_obs||^2+w_EM||partial_Z EM_obs||^2)",
            "partial_Z G_obs=partial_Z M_obs=partial_Z Theta_obs=partial_Z B_obs=partial_Z EM_obs=0 plus Q_boundary[partial_Z] proper/zero",
            "source/readout component partial_Z M_obs is highest pressure",
        ),
        (
            "DQL4120_1_Dq_X_filled_formula",
            "Dq_X_norm",
            "sqrt(w_G||partial_X G_obs||^2+w_M||partial_X M_obs||^2+w_T||partial_X Theta_obs||^2+w_B||partial_X B_obs||^2+w_EM||partial_X EM_obs||^2)",
            "partial_X G_obs=partial_X M_obs=partial_X Theta_obs=partial_X B_obs=partial_X EM_obs=0 plus Q_boundary[partial_X] proper/zero",
            "source/readout component partial_X M_obs is highest pressure",
        ),
    ]
    for row_id, symbol, value_or_formula, zero_condition, next_measurement in formulas:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "value_or_formula": value_or_formula,
                "units": "dimensionless after component normalization",
                "zero_condition": zero_condition,
                "fill_level": "symbolic_formula_filled_not_numeric_not_claim",
                "score_status": "not_scoreable_until_component_zeros_or_bounds",
                "next_measurement": next_measurement,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def branch_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("BR4120_A_strict_absent", "all X/Z component derivatives and boundary charges vanish", "strict quotient absent-pole route survives for X/Z source/pole channel", "NOT_CLAIMED", "prove component zeros from explicit q map"),
        ("BR4120_B_source_leak", "geometry may vanish but source/readout component is nonzero/unsigned", "coupling is physical or closure-assumed; open J_X/J_Z and source-charge residual rows", "MOST_LIKELY_LIVE_BOTTLENECK", "derive source/readout descent or fill J_X/J_Z with units/projection"),
        ("BR4120_C_boundary_leak", "bulk components vanish but boundary/projector survives", "bulk no-pole theorem is insufficient; edge channels remain", "BOUNDARY_RISK_OPEN", "prove Q_boundary=0/exact/proper or score boundary_flux_XZ"),
        ("BR4120_D_EM_leak", "EM/Poynting component depends on X/Z or leaks through boundary", "Maxwell/EM stress is physical and cannot be hidden in q_loc", "EM_RISK_OPEN", "derive EM descent or score EM/Poynting coefficient"),
    ]
    for branch_id_local, condition, result, status, next_test in data:
        row = row_base()
        row.update(
            {
                "branch_id_local": branch_id_local,
                "condition": condition,
                "result": result,
                "current_status": status,
                "next_test": next_test,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4120_0_formula_filled",
            "Dq_Z_norm and Dq_X_norm are no longer placeholders; both have exact positive component norms with no-cancellation lemmas.",
            "SYMBOLIC_ROWS_FILLED",
            "evaluate component derivatives instead of repeating broad q-owner audits.",
        ),
        (
            "DEC4120_1_coupling_focus",
            "Source/readout components partial_Z M_obs and partial_X M_obs are the highest-pressure coupling targets.",
            "SOURCE_READOUT_NEXT",
            "attempt source/readout descent theorem or open J_X/J_Z rows.",
        ),
        (
            "DEC4120_2_EM_accounting",
            "EM/Poynting is now a named component of the quotient norm, so Maxwell stress is either q-owned or separately scored.",
            "EM_NOT_HIDDEN",
            "carry EM descent/flux into the source-readout or boundary pass.",
        ),
        (
            "DEC4120_3_claim",
            "No DqX/DqZ theorem-zero, local-GR, PPN, R10/R11, WEP, clock, Newton, or EM claim is allowed from this checkpoint.",
            "NO_CLAIM",
            "component formulas are progress, not evidence of silence.",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4120_0",
            "target_doc": "4121-Y5-R2FR-source-readout-descent-zero-or-JXZ-residual-row.md",
            "target_script": "scripts/Y5_R2FR_4121_source_readout_descent_zero_or_JXZ_residual_row.py",
            "objective": "try to prove partial_Z M_obs=partial_X M_obs=0 for source mass, GM calibration, Hamiltonian normalization, orbit/readout maps, and source charge; if not, create the first executable nonclaim J_X/J_Z/source-charge residual rows",
            "success_gate": "source/readout descent is theorem-zero from q, or J_X/J_Z and Dsource_readout rows contain formula, units, projection, source path, comparator target, and no-cancellation guard",
            "reason": "4120 reduces the coupling problem to source/readout component derivatives after proving no component cancellation is allowed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4120_0",
            "result": DECISION,
            "summary": (
                "4120 converts Dq_Z_norm and Dq_X_norm into exact positive component norms over geometry, source/readout, "
                "clock/marker, boundary/projector, and EM/Poynting components. The no-cancellation lemma says verticality "
                "requires componentwise zeros, not a tuned sum. The sharpest coupling target is now partial_Z M_obs and "
                "partial_X M_obs, because source/readout leakage reopens J_Z/J_X even if geometry looks vertical."
            ),
            "dqz_formula_filled": "True",
            "dqx_formula_filled": "True",
            "no_cancellation_lemma_proved": "True",
            "component_zeros_signed": "False",
            "score_ready": "False",
            "claim_state": "no DqX/DqZ theorem-zero, local_GR, Newton, PPN, R10, R11, WEP, clock, Gdot, or EM_source claim",
            "next_target": "4121 source-readout descent zero or JX/JZ residual row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4120_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4120_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4120_QMAP_COMPONENT_NORM": SOURCE_DIR / "P8_Y5_R2FR_4120_QMAP_COMPONENT_NORM.csv",
        "P8_Y5_R2FR_4120_DQXZ_NO_CANCELLATION_LEMMA": SOURCE_DIR / "P8_Y5_R2FR_4120_DQXZ_NO_CANCELLATION_LEMMA.csv",
        "P8_Y5_R2FR_4120_DQXZ_COMPONENT_EVALUATION": SOURCE_DIR / "P8_Y5_R2FR_4120_DQXZ_COMPONENT_EVALUATION.csv",
        "P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS.csv",
        "P8_Y5_R2FR_4120_STRICT_VS_RESIDUAL_BRANCH_SPLIT": SOURCE_DIR / "P8_Y5_R2FR_4120_STRICT_VS_RESIDUAL_BRANCH_SPLIT.csv",
        "P8_Y5_R2FR_4120_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4120_DECISION_GATES.csv",
        "P8_Y5_R2FR_4120_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4120_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4120_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4120_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4120 - Explicit q-map and DqZ/DqX Evaluation or XZ Source Row",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- `Dq_Z_norm` and `Dq_X_norm` are now exact positive component norms, not missing placeholders.",
        "- No-cancellation result: local verticality needs componentwise zeros in geometry, source/readout, clock/marker, boundary/projector, and EM/Poynting channels.",
        "- The highest-pressure coupling target is `partial_Z M_obs` / `partial_X M_obs`; if it survives, `J_Z/J_X` is physical and must be scored.",
        "- No local-GR or fifth-force claim is made from this checkpoint.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Component Norm", "", "| norm_id | symbol | formula | current_status |", "|---|---|---|---|"])
    for row in norm_rows():
        sections.append(f"| {row['norm_id']} | {row['symbol']} | `{row['formula']}` | {row['current_status']} |")
    sections.extend(["", "## No-Cancellation Lemma", "", "| lemma_id | statement | current_status |", "|---|---|---|"])
    for row in lemma_rows():
        sections.append(f"| {row['lemma_id']} | {row['statement']} | {row['current_status']} |")
    sections.extend(["", "## Component Evaluation", "", "| component_id | derivative | current_status | affected_arena |", "|---|---|---|---|"])
    for row in component_rows():
        sections.append(f"| {row['component_id']} | `{row['derivative']}` | {row['current_status']} | {row['affected_arena']} |")
    sections.extend(["", "## Decisions", "", "| decision_id | status | next_action |", "|---|---|---|"])
    for row in decision_rows():
        sections.append(f"| {row['decision_id']} | {row['status']} | {row['next_action']} |")
    sections.extend(
        [
            "",
            "## Next Target",
            "",
            "- `4121-Y5-R2FR-source-readout-descent-zero-or-JXZ-residual-row.md`",
            "- Try to prove source/readout descent for mass, GM calibration, Hamiltonian normalization, orbit/readout maps, and source charge. If it fails, create executable `J_X/J_Z` rows.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4120_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4120_QMAP_COMPONENT_NORM": norm_rows,
        "P8_Y5_R2FR_4120_DQXZ_NO_CANCELLATION_LEMMA": lemma_rows,
        "P8_Y5_R2FR_4120_DQXZ_COMPONENT_EVALUATION": component_rows,
        "P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS": filled_rows,
        "P8_Y5_R2FR_4120_STRICT_VS_RESIDUAL_BRANCH_SPLIT": branch_rows,
        "P8_Y5_R2FR_4120_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4120_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4120_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4120_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4120_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4120_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    norm_text = flatten_rows([outputs["P8_Y5_R2FR_4120_QMAP_COMPONENT_NORM"]])
    norm_ok = all(token in norm_text for token in ["Dq_Z_norm", "Dq_X_norm", "w_EM", "partial_Z M_obs", "partial_X M_obs"])
    add("VAL4120_3_norm", "component norm covers DqZ, DqX, source, and EM/Poynting weights", norm_ok, "norm tokens checked")

    lemma_text = flatten_rows([outputs["P8_Y5_R2FR_4120_DQXZ_NO_CANCELLATION_LEMMA"]])
    lemma_ok = all(token in lemma_text for token in ["positive weights", "componentwise zero", "source/readout", "EM/Poynting"])
    add("VAL4120_4_lemma", "no-cancellation lemma requires componentwise zeros", lemma_ok, "lemma tokens checked")

    component_text = flatten_rows([outputs["P8_Y5_R2FR_4120_DQXZ_COMPONENT_EVALUATION"]])
    component_ok = all(token in component_text for token in ["partial_Z M_obs", "partial_X M_obs", "Q_boundary", "EM/Poynting", "OPEN_HIGHEST_PRESSURE_COMPONENT"])
    add("VAL4120_5_components", "component evaluation identifies source and EM/boundary risks", component_ok, "component tokens checked")

    filled_text = flatten_rows([outputs["P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS"]])
    filled_ok = all(token in filled_text for token in ["Dq_Z_norm", "Dq_X_norm", "not_scoreable_until_component_zeros_or_bounds"])
    add("VAL4120_6_filled_rows", "filled DqXZ rows are symbolic formulas but not score-ready", filled_ok, "filled-row tokens checked")

    branch_text = flatten_rows([outputs["P8_Y5_R2FR_4120_STRICT_VS_RESIDUAL_BRANCH_SPLIT"]])
    branch_ok = all(token in branch_text for token in ["BR4120_A_strict_absent", "BR4120_B_source_leak", "BR4120_D_EM_leak"])
    add("VAL4120_7_branches", "branch split includes strict, source leak, boundary leak, and EM leak outcomes", branch_ok, "branch tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4120_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4121-Y5-R2FR-source-readout-descent-zero-or-JXZ-residual-row.md"
    add("VAL4120_8_next_target", "next target is 4121 source-readout descent", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4120_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no DqX/DqZ" in status_rows_local[0].get("claim_state", "")
    add("VAL4120_9_status", "status records formula fill and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4120_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4120*")) or any(FORMALIZATION.rglob("4120-Y5-R2FR*"))
    add("VAL4120_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4120_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4120_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
