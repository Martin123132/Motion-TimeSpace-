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
DOC_PATH = ROOT / "4121-Y5-R2FR-source-readout-descent-zero-or-JXZ-residual-row.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_READOUT_DESCENT_CURRENT_SPINE_4121"
CHECKPOINT_ID = "4121"
DECISION = "SOURCE_READOUT_DESCENT_THEOREM_DERIVED_JXZ_SYMBOLIC_ROWS_ACTIVE"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4121_00_4120_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_NEXT_TARGET.csv",
        "4121-Y5-R2FR-source-readout-descent-zero-or-JXZ-residual-row.md",
        "4120 selected source/readout descent as next coupling target.",
    ),
    "SRC4121_01_4120_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_STATUS.csv",
        "DQXZ_POSITIVE_COMPONENT_NORM_DERIVED_SOURCE_EM_READOUT_NEXT",
        "Current-chain DqX/DqZ component norm handoff.",
    ),
    "SRC4121_02_4120_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_DQXZ_COMPONENT_EVALUATION.csv",
        "CMP4120_2_source_Z",
        "4120 source/readout component pressure target.",
    ),
    "SRC4121_03_4120_filled": (
        SOURCE_DIR / "P8_Y5_R2FR_4120_FILLED_DQXZ_ROWS.csv",
        "DQL4120_1_Dq_X_filled_formula",
        "Filled DqX/DqZ formula rows.",
    ),
    "SRC4121_04_3635_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3635_STATUS.csv",
        "SOURCE_READOUT_THEOREM_DERIVED_JX_SYMBOLIC_ROW_ACTIVE",
        "Older source/readout descent checkpoint.",
    ),
    "SRC4121_05_3635_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3635_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "SDT3635_3_orbit_GM_calibration",
        "Older source/readout theorem and GM calibration guard.",
    ),
    "SRC4121_06_3635_law": (
        SOURCE_DIR / "P8_Y5_R2FR_3635_SOURCE_CURRENT_LAW.csv",
        "SCL3635_0_general_chain_rule",
        "Older chain-rule source current law.",
    ),
    "SRC4121_07_3635_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_3635_SOURCE_READOUT_COMPONENT_GATE.csv",
        "SRC3635_1_GM_calibration",
        "Older source/readout component gate.",
    ),
    "SRC4121_08_3635_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_3635_JX_SOURCE_RESIDUAL_ROW.csv",
        "JX3635_0_source_readout_residual",
        "Older symbolic J_X/J_Z source residual row.",
    ),
    "SRC4121_09_3629_coupling": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv",
        "EXACT_CONDITIONAL_COUPLING_LAW",
        "Response-doublet source-current obstruction.",
    ),
    "SRC4121_10_3629_coeffs": (
        SOURCE_DIR / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv",
        "JZC3629_3_Newton_source",
        "Existing J_Z coefficient row for Newton/R10/R11 source channel.",
    ),
    "SRC4121_11_3630_parent_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv",
        "S_source[Pi_M(q)J_H(q,Psi)]",
        "Parent action clause that would sign source-normalization descent.",
    ),
    "SRC4121_12_1667_retained": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
        "Dsource_readout_Dq_leak",
        "Retained source/readout Dq leak row.",
    ),
    "SRC4121_13_669_residual": (
        SOURCE_DIR / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
        "RV669_2_J_X",
        "Existing X-sector source current placeholder.",
    ),
    "SRC4121_14_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4121_source_readout_descent_zero_or_JXZ_residual_row.py",
        "Reproducible generator for this 4121 checkpoint.",
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


def descent_theorem_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "SDT4121_0_source_quotient_setup",
            "Let M_obs be measured source/readout data: rest mass, GM calibration, Hamiltonian/source charge, orbit/readout maps, and source-coupled EM calibration.",
            "M_obs=M_bar(q(Phi)) is the source-readout descent condition",
            "For any fibre direction v_A in ker(Dq), A in {X,Z}, partial_A M_obs=DM_bar[Dq(v_A)]=0.",
            "CONDITIONAL_THEOREM",
            "if M_obs uses X/Z directly, source current J_X/J_Z is physical or must be bounded",
        ),
        (
            "SDT4121_1_source_action_zero",
            "If geometry, source/readout, boundary/projector, and EM source readouts descend through q, the source action has no linear X/Z current.",
            "delta_A S_source=(delta S_source/delta G_obs)partial_A G_obs+(delta S_source/delta M_obs)partial_A M_obs+(delta S_source/delta B_obs)partial_A B_obs+(delta S_source/delta EM_obs)partial_A EM_obs=0",
            "4120 supplies the component split; all source-visible components must vanish componentwise.",
            "CONDITIONAL_THEOREM",
            "geometry-only descent is insufficient because M_obs or EM_obs can source X/Z",
        ),
        (
            "SDT4121_2_point_particle_source",
            "For a compact source represented by point-particle/readout action, the X/Z source splits into geometry, mass-readout, boundary, and EM calibration pieces.",
            "delta_A S_pp=-int c ds_obs partial_A mu_obs - 1/2 int mu_obs u^mu u^nu partial_A g_obs_mn d tau + readout/projector/EM terms",
            "If partial_A g_obs=0, the leading source current is controlled by partial_A mu_obs plus readout/projector/EM derivatives.",
            "DERIVED_SOURCE_CURRENT_FORM",
            "source mass/readout derivative remains the live coupling row",
        ),
        (
            "SDT4121_3_orbit_GM_calibration",
            "Newtonian/orbital observables see GM_obs; hiding X/Z-dependence in measured GM is not GR reduction.",
            "partial_A(GM_obs)=G_obs partial_A M_obs + M_obs partial_A G_obs + calibration/projector terms",
            "With geometry/G fixed, nonzero partial_A M_obs feeds WEP/source charge, R10/R11, and orbital residuals.",
            "DERIVED_GM_READOUT_GUARD",
            "GM calibration can absorb a fifth-force-looking coupling unless reported as a residual",
        ),
        (
            "SDT4121_4_verdict",
            "The theorem is exact, but the live corpus does not parent-sign M_obs=M_bar(q(Phi)).",
            "partial_X M_obs=partial_Z M_obs=0 is sufficient for source silence, not currently proven",
            "The coupling gap is now a theorem-or-coefficient branch: prove source descent or score J_X/J_Z.",
            "THEOREM_SOUND_NOT_PARENT_SIGNED",
            "open J_X/J_Z source residual rows with normalization requirements",
        ),
    ]
    for theorem_id, statement, identity, derivation, status, blocks in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "identity": identity,
                "derivation": derivation,
                "status": status,
                "blocks_if_missing": blocks,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def current_law_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "SCL4121_0_general_chain_rule",
            "J_A_source for A in {X,Z}",
            "J_A_source=Pi_M^*[(delta L_source/delta G_obs)partial_A G_obs+(delta L_source/delta M_obs)partial_A M_obs+(delta L_source/delta B_obs)partial_A B_obs+(delta L_source/delta EM_obs)partial_A EM_obs]",
            "source current is the chain-rule image of every A-visible readout component",
            "partial_A G_obs=partial_A M_obs=partial_A B_obs=partial_A EM_obs=0",
            "EXACT_CHAIN_RULE_FORM",
        ),
        (
            "SCL4121_1_geometry_zero_limit",
            "J_A_source|geometry_zero",
            "J_A_source=Pi_M^*[(delta L_source/delta M_obs)partial_A M_obs+(delta L_source/delta B_obs)partial_A B_obs+(delta L_source/delta EM_obs)partial_A EM_obs]",
            "even perfect metric/coframe quotient leaves source current if measured mass/readout or EM source calibration depends on X/Z",
            "partial_A M_obs=0 plus boundary and EM silence",
            "COUPLING_BOTTLENECK_EXPOSED",
        ),
        (
            "SCL4121_2_profile",
            "A_profile_from_source",
            "A^I(x)=-(L^{-1})^{IJ}J_J_source + boundary Green terms + O(J^2), A in {X,Z}",
            "if source descent fails, the local branch produces a residual profile that must be bounded",
            "J_A_source=0 and boundary source=0",
            "PROFILE_ROUTE_FROM_3629_RETAINED",
        ),
        (
            "SCL4121_3_projection",
            "R_source residual",
            "R_source~P_R[L^{-1}Pi_M^*((delta L_source/delta M_obs)partial_A M_obs + EM/boundary terms)]",
            "bridge from source-readout leakage to WEP/R10/R11/orbital/EM residual rows",
            "partial_A M_obs=0 or projection P_R kills the source theoremically",
            "EXECUTABLE_SYMBOLIC_BRIDGE",
        ),
    ]
    for law_id, quantity, formula, meaning, zero_condition, status in data:
        row = row_base()
        row.update(
            {
                "law_id": law_id,
                "quantity": quantity,
                "formula": formula,
                "meaning": meaning,
                "zero_condition": zero_condition,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def component_gate_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("SRC4121_0_rest_mass_Z", "partial_Z mu_obs", "measured rest/source mass is q-owned or fixed external label", "OPEN", "species/source charge row opens; WEP/source charge and R10/R11 affected"),
        ("SRC4121_1_rest_mass_X", "partial_X mu_obs", "parallel X source mass is q-owned or fixed external label", "OPEN", "X-sector source charge and R10/R11 fifth-force affected"),
        ("SRC4121_2_GM_calibration", "partial_A(GM_obs)", "Newtonian calibration uses only EH/source quotient variables or reports residual separately", "OPEN", "delta_Newton_MTS and alpha(lambda) rows become live"),
        ("SRC4121_3_Hamiltonian_source", "partial_A H_source or Pi_M J_H", "Hamiltonian/source projector Pi_M is q-owned and orthogonal to extra charge", "OPEN", "source normalization and hidden Hamiltonian charge drive J_X/J_Z"),
        ("SRC4121_4_orbit_readout", "partial_A orbit/readout map", "orbit and ephemeris readouts are functions of observed metric/source quotient only", "OPEN", "orbital residuals and PPN/source projection rows must be scored"),
        ("SRC4121_5_EM_source_calibration", "partial_A EM_obs/source_EM_readout", "EM/Poynting source readout is q-owned or kept as separate physical stress/flux", "OPEN_EM_RISK", "Maxwell/EM stress and source coupling rows remain live"),
        ("SRC4121_6_verdict", "partial_A M_obs for A in {X,Z}", "all source/readout subcomponents vanish componentwise", "SOURCE_DESCENT_NOT_CLAIMED", "use J_X/J_Z source residual rows"),
    ]
    for component_id, component, required_zero, status, if_nonzero in data:
        row = row_base()
        row.update(
            {
                "component_id": component_id,
                "component": component,
                "required_zero": required_zero,
                "current_evidence": "parent-signature missing in current corpus",
                "status": status,
                "if_nonzero": if_nonzero,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def residual_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "JXZ4121_0_source_readout_residual",
            "RV669_2_J_X;JZC3629_3_Newton_source;DQL1667_4_Dsource_readout",
            "J_X_source_or_J_Z_source",
            "Pi_M^*[(delta L_source/delta M_obs)partial_A M_obs+(delta L_source/delta G_obs)partial_A G_obs+(delta L_source/delta B_obs)partial_A B_obs+(delta L_source/delta EM_obs)partial_A EM_obs]",
            "Pi_M^*[(delta L_source/delta M_obs)partial_A M_obs + boundary/projector/EM terms]",
            "source action density per normalized X/Z field",
            "R1_WEP_source_charge;R10_fifth_force;R11_EH_operator_ledger;orbital_source_projection;EM_source_flux",
            "M_obs=M_bar(q), G_obs=G_bar(q), EM_obs=EM_bar(q), and boundary/projector silence",
            "symbolic_executable_law_not_numeric",
            "not_scoreable_until_field_normalization_projection_units_and_comparator",
        ),
        (
            "JXZ4121_1_GM_residual",
            "JZC3629_3_Newton_source;R10_fifth_force",
            "delta_GM_XZ",
            "partial_A(GM_obs)=G_obs partial_A M_obs + M_obs partial_A G_obs + calibration/projector terms",
            "G_obs partial_A M_obs when geometry is quotient-silent",
            "GM readout derivative per normalized X/Z field",
            "Newtonian_orbital;R10_alpha_lambda;source_normalization",
            "GM_obs=GM_bar(q) and calibration projector silence",
            "symbolic_GM_guard_not_numeric",
            "not_scoreable_until_GM_units_projection_and_bound",
        ),
        (
            "JXZ4121_2_EM_source_residual",
            "CMP4120_6_EM_Poynting;ENV3625_5_EM_source",
            "J_XZ_EM_source",
            "Pi_EM^*[(delta L_source/delta EM_obs)partial_A EM_obs + Q_boundary_EM[partial_A]]",
            "EM/Poynting source term if Maxwell stress is not quotient-owned",
            "EM stress or Poynting flux derivative per normalized X/Z field",
            "Maxwell_limit;EM_stress;boundary_flux;source_coupling",
            "EM_obs=EM_bar(q) or EM flux coefficient is independently bounded",
            "symbolic_EM_law_not_numeric",
            "not_scoreable_until_EM_normalization_projection_and_bound",
        ),
    ]
    for row_id, prior_rows, symbol, value_or_formula, geometry_zero_reduction, units, feeds, zero_condition, fill_level, score_status in data:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "prior_rows": prior_rows,
                "symbol": symbol,
                "value_or_formula": value_or_formula,
                "geometry_zero_reduction": geometry_zero_reduction,
                "units": units,
                "feeds": feeds,
                "zero_condition": zero_condition,
                "fill_level": fill_level,
                "score_status": score_status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def normalization_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("NRM4121_0_field_basis", "normalized X/Z field basis", "A_norm^I = sqrt(Z_A) A^I or quotient-absent theorem-zero", "needed before J_A has units and comparator meaning", "MISSING_FIELD_NORMALIZATION"),
        ("NRM4121_1_source_action_density", "delta L_source/delta M_obs", "source action derivative convention and density measure", "sets units of source current", "MISSING_SOURCE_DENSITY_CONVENTION"),
        ("NRM4121_2_projection", "Pi_M^* and P_R", "project source current into WEP/R10/R11/orbital/EM arenas", "turns symbolic J_A into residual vector", "MISSING_ARENA_PROJECTION"),
        ("NRM4121_3_green_profile", "L^{-1}J_A", "positive operator inverse/profile and boundary Green terms", "connects source current to observable amplitude/range", "MISSING_L_INV_PROFILE"),
        ("NRM4121_4_units_bounds", "units/source/comparator", "units, source path, comparator bound, no-cancellation guard", "minimum for a scoreable row", "MISSING_UNITS_AND_BOUNDS"),
    ]
    for req_id, item, formula, why_needed, status in data:
        row = row_base()
        row.update(
            {
                "requirement_id": req_id,
                "item": item,
                "formula_or_requirement": formula,
                "why_needed": why_needed,
                "current_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4121_0_theorem",
            "Source/readout descent is sufficient: M_obs=M_bar(q) implies partial_X M_obs=partial_Z M_obs=0 and kills the source part of J_X/J_Z when geometry/boundary/EM also descend.",
            "CONDITIONAL_SOURCE_ZERO_THEOREM",
            "try to parent-sign measured source mass/GM/Hamiltonian/orbit/EM readout as quotient data.",
        ),
        (
            "DEC4121_1_live_gap",
            "The live corpus does not sign source/readout descent; rest mass, GM calibration, Hamiltonian source, orbit readout, and EM source calibration remain open componentwise.",
            "SOURCE_DESCENT_NOT_CLAIMED",
            "keep J_X/J_Z source residual rows active.",
        ),
        (
            "DEC4121_2_progress",
            "The coupling gap is now an explicit chain-rule current, not a vague missing coupling.",
            "JXZ_SYMBOLIC_ROWS_FILLED",
            "next checkpoint should either parent-sign source mass as q-data or normalize J_X/J_Z for scoring.",
        ),
        (
            "DEC4121_3_claim",
            "No source-zero, local-GR, R10/R11, WEP, Newton, PPN, clock, Gdot, or EM-source claim is allowed from this checkpoint.",
            "NO_CLAIM",
            "use these rows as theorem/coefficient machinery only.",
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
            "next_id": "NEXT4121_0",
            "target_doc": "4122-Y5-R2FR-source-mass-quotient-signature-or-JXZ-normalization.md",
            "target_script": "scripts/Y5_R2FR_4122_source_mass_quotient_signature_or_JXZ_normalization.py",
            "objective": "attempt to parent-sign measured source mass, GM calibration, Hamiltonian/source charge, orbit/readout maps, and EM source calibration as q-data; if that fails, define field normalization, units, projections, and first comparator channels for J_X/J_Z source residuals",
            "success_gate": "M_obs=M_bar(q) is parent-signed for all source/readout subcomponents, or J_X/J_Z rows gain explicit normalization, units, source paths, projections, comparator targets, and no-cancellation guards",
            "reason": "4121 derived the exact chain-rule current; the unresolved fork is source-mass quotient signature versus scoreable coupling normalization.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4121_0",
            "result": DECISION,
            "summary": (
                "4121 derives the source/readout coupling law in current-chain form. If measured source data M_obs "
                "descends through q, then partial_X M_obs=partial_Z M_obs=0 and the source parts of J_X/J_Z die. "
                "If not, J_X/J_Z are exactly the chain-rule pullback of source/readout, boundary/projector, and "
                "EM/Poynting readout derivatives into the source action. The coupling fork is now concrete: "
                "parent-sign source descent or normalize the source residuals for scoring."
            ),
            "source_descent_theorem_derived": "True",
            "jxjz_symbolic_rows_written": "True",
            "source_descent_parent_signed": "False",
            "score_ready": "False",
            "claim_state": "no source_zero, local_GR, Newton, PPN, R10, R11, WEP, clock, Gdot, or EM_source claim",
            "next_target": "4122 source-mass quotient signature or JX/JZ normalization",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4121_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "P8_Y5_R2FR_4121_SOURCE_CURRENT_LAW": SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_CURRENT_LAW.csv",
        "P8_Y5_R2FR_4121_SOURCE_READOUT_COMPONENT_GATE": SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_READOUT_COMPONENT_GATE.csv",
        "P8_Y5_R2FR_4121_JXZ_SOURCE_RESIDUAL_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4121_JXZ_SOURCE_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_4121_JXZ_NORMALIZATION_REQUIREMENTS": SOURCE_DIR / "P8_Y5_R2FR_4121_JXZ_NORMALIZATION_REQUIREMENTS.csv",
        "P8_Y5_R2FR_4121_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4121_DECISION_GATES.csv",
        "P8_Y5_R2FR_4121_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4121_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4121_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4121_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4121 - Source-Readout Descent Zero or JX/JZ Residual Row",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- This checkpoint derives the coupling fork: source silence is equivalent to quotient descent of measured source/readout data, not a vibe.",
        "- If `M_obs=M_bar(q)` and geometry/boundary/EM readouts also descend, then `partial_X M_obs=partial_Z M_obs=0` and source `J_X/J_Z` dies.",
        "- If source/readout descends fails, `J_X/J_Z` is the chain-rule pullback of `partial_A M_obs`, boundary/projector, and EM/Poynting derivatives.",
        "- No source-zero or local-GR claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Source-Readout Descent Theorem", "", "| theorem_id | identity | status |", "|---|---|---|"])
    for row in descent_theorem_rows():
        sections.append(f"| {row['theorem_id']} | `{row['identity']}` | {row['status']} |")
    sections.extend(["", "## Source Current Law", "", "| law_id | quantity | formula | status |", "|---|---|---|---|"])
    for row in current_law_rows():
        sections.append(f"| {row['law_id']} | {row['quantity']} | `{row['formula']}` | {row['status']} |")
    sections.extend(["", "## Component Gate", "", "| component_id | component | status | if_nonzero |", "|---|---|---|---|"])
    for row in component_gate_rows():
        sections.append(f"| {row['component_id']} | `{row['component']}` | {row['status']} | {row['if_nonzero']} |")
    sections.extend(["", "## Residual Rows", "", "| row_id | symbol | score_status |", "|---|---|---|"])
    for row in residual_rows():
        sections.append(f"| {row['row_id']} | {row['symbol']} | {row['score_status']} |")
    sections.extend(["", "## Next Target", "", "- `4122-Y5-R2FR-source-mass-quotient-signature-or-JXZ-normalization.md`", "- Parent-sign the source/readout map or normalize `J_X/J_Z` enough to score it.", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4121_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM": descent_theorem_rows,
        "P8_Y5_R2FR_4121_SOURCE_CURRENT_LAW": current_law_rows,
        "P8_Y5_R2FR_4121_SOURCE_READOUT_COMPONENT_GATE": component_gate_rows,
        "P8_Y5_R2FR_4121_JXZ_SOURCE_RESIDUAL_ROWS": residual_rows,
        "P8_Y5_R2FR_4121_JXZ_NORMALIZATION_REQUIREMENTS": normalization_rows,
        "P8_Y5_R2FR_4121_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4121_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4121_STATUS": status_rows,
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
        "VAL4121_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4121_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

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
    add("VAL4121_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM"]])
    theorem_ok = all(token in theorem_text for token in ["M_obs=M_bar(q(Phi))", "partial_X M_obs", "partial_Z M_obs", "GM_obs", "EM"])
    add("VAL4121_3_theorem", "source-readout theorem covers M_obs, X/Z, GM, and EM readout", theorem_ok, "theorem tokens checked")

    law_text = flatten_rows([outputs["P8_Y5_R2FR_4121_SOURCE_CURRENT_LAW"]])
    law_ok = all(token in law_text for token in ["J_A_source", "partial_A M_obs", "partial_A EM_obs", "L^{-1}", "R10"])
    add("VAL4121_4_current_law", "source-current law includes chain rule, EM, profile, and R10 projection", law_ok, "law tokens checked")

    component_text = flatten_rows([outputs["P8_Y5_R2FR_4121_SOURCE_READOUT_COMPONENT_GATE"]])
    component_ok = all(token in component_text for token in ["partial_Z mu_obs", "partial_X mu_obs", "partial_A(GM_obs)", "partial_A H_source", "EM"])
    add("VAL4121_5_component_gate", "component gate covers mass, GM, Hamiltonian, orbit, and EM source calibration", component_ok, "component tokens checked")

    residual_text = flatten_rows([outputs["P8_Y5_R2FR_4121_JXZ_SOURCE_RESIDUAL_ROWS"]])
    residual_ok = all(token in residual_text for token in ["J_X_source_or_J_Z_source", "delta_GM_XZ", "J_XZ_EM_source", "not_scoreable"])
    add("VAL4121_6_residual_rows", "residual rows include JX/JZ, GM, and EM source residuals", residual_ok, "residual tokens checked")

    norm_text = flatten_rows([outputs["P8_Y5_R2FR_4121_JXZ_NORMALIZATION_REQUIREMENTS"]])
    norm_ok = all(token in norm_text for token in ["normalized X/Z field basis", "delta L_source/delta M_obs", "Pi_M^*", "L^{-1}J_A", "MISSING_UNITS_AND_BOUNDS"])
    add("VAL4121_7_normalization", "normalization requirements cover field basis, source density, projection, profile, and bounds", norm_ok, "normalization tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4121_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4122-Y5-R2FR-source-mass-quotient-signature-or-JXZ-normalization.md"
    add("VAL4121_8_next_target", "next target is 4122 source-mass signature or JXZ normalization", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4121_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no source_zero" in status_rows_local[0].get("claim_state", "")
    add("VAL4121_9_status", "status records theorem and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4121_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4121*")) or any(FORMALIZATION.rglob("4121-Y5-R2FR*"))
    add("VAL4121_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4121_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4121_VALIDATION.csv"
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
