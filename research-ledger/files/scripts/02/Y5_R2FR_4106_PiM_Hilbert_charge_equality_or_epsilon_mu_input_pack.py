from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_COUPLING_SPINE_4106"
CHECKPOINT_ID = "4106"
DECISION = (
    "SOURCE_COUPLING_SPINE_CONSOLIDATED_PIM_TO_GAUSS_ORBITAL_"
    "CONDITIONAL_NEWTON_ROUTE_ACTIVE_CONSTANT_GEFF_GATE_NEXT"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4106_00_4105_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4105_NEXT_TARGET.csv",
        "4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md",
        "4105 selects PiM-Hilbert charge equality/epsilon_mu as the current next target.",
    ),
    "SRC4106_01_3592_equality": (
        SOURCE_DIR / "P8_Y5_R2FR_3592_PIM_HILBERT_EQUALITY_ATTEMPT.csv",
        "PHE3592_7_verdict",
        "3592 attempts the central PiM/Hilbert charge equality.",
    ),
    "SRC4106_02_3592_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_3592_CHARGE_EQUALITY_RESIDUAL_IDENTITY.csv",
        "CEI3592_10_total_identity",
        "3592 decomposes the equality failure into Delta terms.",
    ),
    "SRC4106_03_3592_epsilon": (
        SOURCE_DIR / "P8_Y5_R2FR_3592_EPSILON_MU_INPUT_PACK.csv",
        "EMI3592_10_epsilon_mu",
        "3592 creates the epsilon_mu input pack.",
    ),
    "SRC4106_04_3593_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_3593_DELTAPIM_VARIATION_SPLIT.csv",
        "DPS3593_2_Gamma_zero",
        "3593 removes the independent-Gamma PiM variation piece in the private LC branch.",
    ),
    "SRC4106_05_3593_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3593_DELTAPIM_BOUND_INPUT_PACK.csv",
        "DPB3593_7_epsilon_PiM_total",
        "3593 gives the epsilon_PiM component bound pack.",
    ),
    "SRC4106_06_3594_topological": (
        SOURCE_DIR / "P8_Y5_R2FR_3594_FIXED_TOPOLOGICAL_PIM_THEOREM_ATTEMPT.csv",
        "FTP3594_7_verdict",
        "3594 conditionally zeroes metric/domain projector stress for fixed-topological or identity PiM.",
    ),
    "SRC4106_07_3595_glue": (
        SOURCE_DIR / "P8_Y5_R2FR_3595_HILBERT_TO_TOPOLOGICAL_GLUE_THEOREM.csv",
        "HGT3595_6_conditional_glue_theorem",
        "3595 derives the Hilbert-to-topological glue theorem and wrong-object guard.",
    ),
    "SRC4106_08_3596_worldtube": (
        SOURCE_DIR / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv",
        "WSL3596_6_conditional_lock_theorem",
        "3596 locks the non-cheat dressed worldtube source-measure definition.",
    ),
    "SRC4106_09_3597_em": (
        SOURCE_DIR / "P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv",
        "EMT3597_6_conditional_theorem",
        "3597 makes EM stress/Poynting/binding once-only accounting explicit.",
    ),
    "SRC4106_10_3598_gauss": (
        SOURCE_DIR / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_CALIBRATION_THEOREM.csv",
        "GOC3598_",
        "3598 derives the dressed-source to Gauss/orbital measured-GM bridge.",
    ),
    "SRC4106_11_3598_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3598_STATUS.csv",
        "GAUSS_ORBITAL_CALIBRATION_THEOREM_CONDITIONAL_DELTA_CAL_BOUND_ACTIVE",
        "3598 status identifies constant-G_eff/radial-time hair as the next gate.",
    ),
    "SRC4106_12_3598_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3598_NEXT_TARGET.csv",
        "3599-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md",
        "3598 selects constant G_eff and derivative-hair silence as the next target.",
    ),
    "SRC4106_13_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4106_PiM_Hilbert_charge_equality_or_epsilon_mu_input_pack.py",
        "Reproducible generator for this 4106 checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_type": "local_checkpoint_or_generator",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "contains_needle": bool_string(path.exists() and needle in read_text(path)),
                "valid_for_claim": "False",
            }
        )
    return rows


def source_coupling_spine_rows() -> List[dict]:
    entries = [
        (
            "SCS4106_0_target_equality",
            "PiM/Hilbert charge equality",
            "B_xi/G_ref = M_H[Pi_M J_H]",
            "central source-coupling equality needed before fitted GM can become derived Newtonian GM",
            "TARGET_EXACT_NOT_PARENT_SIGNED",
            "SRC4106_01_3592_equality",
        ),
        (
            "SCS4106_1_residual_identity",
            "charge equality residual",
            "B_xi/G_ref - M_H[Pi_M J_H] = Delta_frame+Delta_nonEH+Delta_symp+Delta_PiM+Delta_extra+Delta_flux+Delta_G+Delta_cal+Delta_PPN+Delta_GK_source",
            "failure of the equality is now a real residual identity rather than a vague missing coupling",
            "RESIDUAL_IDENTITY_ACTIVE",
            "SRC4106_02_3592_residual",
        ),
        (
            "SCS4106_2_Gamma_PiM_piece",
            "independent-Gamma projector variation",
            "delta_Gamma_ind Pi_M=0 inside the q/e_obs/tau-natural LC branch",
            "one projector-variation component is removed in the private branch",
            "ZERO_DERIVED_PRIVATE_BRANCH",
            "SRC4106_04_3593_variation",
        ),
        (
            "SCS4106_3_fixed_topological_PiM",
            "metric/domain projector stress",
            "fixed-topological or identity Pi_M gives delta_g Pi_M=0 and homology-preserving D_D Pi_M exact/boundary-silent",
            "conditional route kills K_PiM_metric and K_PiM_domain only if parent selector is owned",
            "CONDITIONAL_STRESS_ZERO",
            "SRC4106_06_3594_topological",
        ),
        (
            "SCS4106_4_Hilbert_topological_glue",
            "wrong-object obstruction",
            "closed Hilbert mass current decomposes as ell_M(Pi_M J_H) omega_M_top + dB + R_perp",
            "topological charge works only when its scalar is defined from the same Hilbert/worldtube source",
            "CONDITIONAL_GLUE_THEOREM",
            "SRC4106_07_3595_glue",
        ),
        (
            "SCS4106_5_worldtube_source_measure",
            "dressed source measure",
            "Q_M := ell_M(Pi_M J_H_total) := M_source^dress[W;tau] before orbital readout",
            "only non-cheat definition of the source scalar; not an orbital-fit label",
            "CONDITIONAL_DEFINITION_LOCK",
            "SRC4106_08_3596_worldtube",
        ),
        (
            "SCS4106_6_EM_Poynting_once",
            "Hilbert source accounting",
            "J_H_total = J_matter + J_EM + J_Poynting + J_binding + exact improvements",
            "Poynting flux is a source/boundary term in the dressed balance, not optional bookkeeping",
            "CONDITIONAL_ONCE_ONLY_THEOREM",
            "SRC4106_09_3597_em",
        ),
        (
            "SCS4106_7_Gauss_orbital_bridge",
            "measured Newtonian GM",
            "M_source^dress -> Poisson -> Gauss flux -> inverse-square orbital readout -> mu_obs=G_eff M_H",
            "this is the explicit bridge from source charge to what orbits feel",
            "CONDITIONAL_NEWTON_BRIDGE",
            "SRC4106_10_3598_gauss",
        ),
        (
            "SCS4106_8_next_gate",
            "constant coupling and derivative hair",
            "G_eff superselection plus partial_r ln mu_obs=0, dln_Geff_dt=0, dln_Meff_dt=0, and PPN source stability",
            "without this, Newtonian GM can drift, vary radially, or hide fitted profile hair",
            "NEXT_GATE_SELECTED",
            "SRC4106_11_3598_status",
        ),
    ]
    return [
        {
            **row_base(),
            "spine_id": spine_id,
            "rung": rung,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for spine_id, rung, formula, meaning, status, source_key in entries
    ]


def epsilon_mu_status_rows() -> List[dict]:
    entries = [
        ("EMU4106_0_frame", "epsilon_frame", "Delta_frame/(G_ref M_H)", "MISSING_ZERO_OR_BOUND", "SRC4106_03_3592_epsilon"),
        ("EMU4106_1_operator", "epsilon_operator", "Delta_nonEH/(G_ref M_H)", "MISSING_EH_ONLY_OR_R11_BOUND", "SRC4106_03_3592_epsilon"),
        ("EMU4106_2_symplectic", "epsilon_symp", "Delta_symp/(G_ref M_H)", "MISSING_BOUNDARY_REFERENCE_INPUT", "SRC4106_03_3592_epsilon"),
        ("EMU4106_3_PiM", "epsilon_PiM", "epsilon_PiM_Gamma + epsilon_PiM_metric_domain + epsilon_PiM_parent + epsilon_PiM_flux + epsilon_PiM_EM_accounting + epsilon_PiM_readout", "PARTIAL_REDUCTION_GAMMA_ZERO_METRIC_DOMAIN_CONDITIONAL", "SRC4106_05_3593_bound"),
        ("EMU4106_4_wrong_object", "epsilon_PiM_parent_wrong_object", "epsilon_Qlabel+epsilon_Rperp+epsilon_Bzero+epsilon_worldtube+epsilon_extra_exchange+epsilon_frame_species+epsilon_EM_once", "BOUND_BRANCH_ACTIVE_VALUES_MISSING", "SRC4106_07_3595_glue"),
        ("EMU4106_5_worldtube", "epsilon_source_measure_total", "epsilon_Qlabel + epsilon_worldtube + epsilon_Htau + epsilon_ref + epsilon_W + epsilon_frame_tau + epsilon_EM_once + epsilon_Gref_units", "BOUND_BRANCH_ACTIVE_VALUES_MISSING", "SRC4106_08_3596_worldtube"),
        ("EMU4106_6_EM_once", "epsilon_EM_source_total", "epsilon_EM_once + epsilon_Hodge_EM + epsilon_w_EM + epsilon_XF2 + epsilon_CJQ + epsilon_Phi_EM_rad + epsilon_EM_readout + epsilon_Delta_J_total + epsilon_EM_double_count + epsilon_dB_impr", "POYNTING_EXPLICIT_BOUND_BRANCH_ACTIVE", "SRC4106_09_3597_em"),
        ("EMU4106_7_calibration", "Delta_cal", "M_source^dress[J_H_total] - M_Gauss_orbital plus Gauss/orbit/derivative-hair terms", "CONDITIONAL_THEOREM_BOUND_ACTIVE", "SRC4106_10_3598_gauss"),
        ("EMU4106_8_total", "epsilon_mu", "sum_abs(all source, projector, EM, calibration, GK and PPN residual components)", "TOTAL_INPUT_PACK_ACTIVE_NOT_SCORE_READY", "SRC4106_03_3592_epsilon"),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, definition, status, source_key in entries
    ]


def newton_theorem_condition_rows() -> List[dict]:
    entries = [
        (
            "NTC4106_0_same_frame",
            "same observed frame/coframe",
            "e_obs, source tau, EM Hodge, Pi_M and orbit readout use the same parent branch before readout",
            "OPEN_BOUND_REQUIRED",
            "SRC4106_08_3596_worldtube",
        ),
        (
            "NTC4106_1_source_charge",
            "parent-owned dressed Hilbert source",
            "Q_M = ell_M(Pi_M J_H_total) = M_source^dress[W;tau]",
            "CONDITIONAL_LOCK_NOT_FULLY_SIGNED",
            "SRC4106_08_3596_worldtube",
        ),
        (
            "NTC4106_2_EM_accounting",
            "EM/Poynting/binding once-only accounting",
            "visible EM stress, Poynting flux and binding energy are varied once in J_H_total, with no omission/double count",
            "CONDITIONAL_THEOREM_BOUND_ACTIVE",
            "SRC4106_09_3597_em",
        ),
        (
            "NTC4106_3_Gauss_bridge",
            "Poisson/Gauss/orbit readout",
            "same source charge passes Poisson equation, Gauss flux and inverse-square slow-orbit readout",
            "CONDITIONAL_THEOREM_BOUND_ACTIVE",
            "SRC4106_10_3598_gauss",
        ),
        (
            "NTC4106_4_constant_Geff",
            "constant universal coupling",
            "G_eff/kappa is source-independent, time-independent, radial-profile silent and range-independent",
            "NEXT_GATE_OPEN",
            "SRC4106_11_3598_status",
        ),
        (
            "NTC4106_5_PPN_stability",
            "second-order source stability",
            "same charge remains stable at beta/gamma/preferred-frame and conservation order",
            "OPEN_PPN_GATE",
            "SRC4106_10_3598_gauss",
        ),
        (
            "NTC4106_6_Newton_promotion",
            "conditional Newton promotion rule",
            "if all preceding gates close and residual rows are zero/bounded, mu_obs=G_eff M_H and a_r=-mu_obs/r^2 in the slow weak-field exterior",
            "THEOREM_ROUTE_EXACT_NOT_ACTIVATED",
            "SRC4106_10_3598_gauss",
        ),
    ]
    return [
        {
            **row_base(),
            "condition_id": condition_id,
            "condition": condition,
            "statement": statement,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for condition_id, condition, statement, status, source_key in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4106_0_consolidate",
            "consolidate the 3592-3598 source-coupling ladder into current 4106 chain",
            "the old trail is real progress and should not be orphaned",
            "current branch now has one spine from PiM/Hilbert equality to Gauss/orbital calibration",
            "LADDER_RESTORED",
            "SRC4106_12_3598_next",
        ),
        (
            "DEC4106_1_no_claim",
            "do not claim Newton/local-GR yet",
            "the bridge is conditional and constant-G_eff/derivative-hair gates remain open",
            "epsilon_mu and Delta_cal remain active",
            "PUBLIC_CLAIM_BLOCKED",
            "SRC4106_11_3598_status",
        ),
        (
            "DEC4106_2_poynting_role",
            "retain Poynting as source-balance flux",
            "EM/Poynting is owned by Hilbert source accounting, not bolted on after readout",
            "future source coupling cannot omit or double-count EM stress",
            "POYNTING_ROLE_FIXED",
            "SRC4106_09_3597_em",
        ),
        (
            "DEC4106_3_next",
            "attack constant G_eff and derivative hair next",
            "Gauss/orbital theorem collapses only if source/coupling profile hair is silent or bounded",
            "4107 targets constant Geff/radial-time hair zero or bounds",
            "NEXT_TARGET_SELECTED",
            "SRC4106_12_3598_next",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def claim_gate_rows() -> List[dict]:
    entries = [
        ("CLAIM4106_0_PiM_Hilbert", "PiM/Hilbert charge equality", "BLOCKED", "equality decomposed into residual identity but not parent-zero"),
        ("CLAIM4106_1_source_measure", "dressed worldtube source measure equals Hilbert scalar", "CONDITIONAL_ONLY", "H_tau, reference, support, frame/tau and extra-sector premises remain open"),
        ("CLAIM4106_2_EM_once", "EM/Poynting/binding once-only source accounting", "CONDITIONAL_ONLY", "Hodge/action/current/Poynting/readout/current-closure rows remain unsigned"),
        ("CLAIM4106_3_Gauss_orbital", "dressed source equals measured orbital GM", "CONDITIONAL_ONLY", "Poisson/Gauss/orbit and derivative-hair rows remain active"),
        ("CLAIM4106_4_Newton_GR", "Newton/local-GR/PPN promotion", "BLOCKED", "constant G_eff, radial/time hair and PPN source stability are not closed"),
    ]
    return [
        {
            **row_base(),
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for claim_id, claim, status, reason in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4106_0",
            "target_doc": "4107-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_4107_constant_Geff_radial_time_hair_zero_or_bound.py",
            "objective": "prove constant universal G_eff/kappa superselection and radial/time derivative silence for mu_obs, or fill dln_Geff_dt, dln_Meff_dt, partial_t_epsilon_mu and partial_r_ln_mu_obs bound rows",
            "success_gate": "Newtonian calibration may advance only if coupling/source derivative hair is parent-zero, or each drift/profile channel has sourced numeric bounds without cancellation by fit",
            "reason": "4106 connects the source-coupling ladder up to Gauss/orbital calibration; constant coupling and derivative-hair silence is now the sharpest Newton/GR gate",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4106_0",
            "decision": DECISION,
            "strongest_result": "4106 restores and consolidates the source-coupling ladder: PiM/Hilbert equality becomes an epsilon_mu residual identity; independent-Gamma PiM variation is zero in the private LC branch; fixed-topological/identity PiM conditionally kills metric/domain projector stress; Hilbert-to-topological glue and dressed worldtube source measure are written; EM/Poynting/binding once-only accounting is explicit; and Gauss/orbital calibration gives the conditional bridge to measured Newtonian GM.",
            "what_moved_forward": "the coupling problem is no longer one vague missing constant; it is a chain of theorem gates ending at constant G_eff and derivative-hair silence",
            "still_missing": "parent-signed PiM/Hilbert equality; H_tau integrability; same frame/tau; EM Hodge/action/current normalization; Poynting flux zero or bound; Gauss residual zero; constant universal G_eff; partial_r ln mu_obs silence; dln_Geff_dt/dln_Meff_dt silence; PPN source stability",
            "public_status": "no Newton_local_GR_PPN_R10 claim",
            "next_target": "4107 constant Geff radial-time hair zero or bound",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4106_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4106_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE": SOURCE_DIR / "P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE.csv",
        "P8_Y5_R2FR_4106_EPSILON_MU_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4106_EPSILON_MU_STATUS.csv",
        "P8_Y5_R2FR_4106_NEWTON_THEOREM_CONDITIONS": SOURCE_DIR / "P8_Y5_R2FR_4106_NEWTON_THEOREM_CONDITIONS.csv",
        "P8_Y5_R2FR_4106_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4106_DECISION_GATE.csv",
        "P8_Y5_R2FR_4106_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4106_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4106_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4106_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4106_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4106_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4106 - PiM/Hilbert charge equality or epsilon_mu input pack",
        "",
        "## Verdict",
        "4106 restores the source-coupling ladder into the current chain rather than leaving it buried in the older checkpoint run.",
        "",
        "The important progress is this: the coupling problem is no longer `where is G?` as a vague complaint. It is a theorem chain:",
        "",
        "`Pi_M/Hilbert equality -> epsilon_mu residual identity -> PiM variation reduction -> fixed/topological projector branch -> Hilbert/topological glue -> dressed worldtube source -> EM/Poynting once-only source accounting -> Gauss/orbital measured GM -> constant G_eff and derivative-hair gate`.",
        "",
        "This does not claim Newton/local GR. It gives the actual route and names the remaining failure modes without refitting them into `GM`.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Concrete Advances",
        "- `B_xi/G_ref - M_H[Pi_M J_H]` is decomposed into explicit `Delta_*` residuals.",
        "- `delta_Gamma_ind Pi_M=0` is carried inside the q/e_obs/tau-natural LC branch.",
        "- Fixed-topological or identity `Pi_M` conditionally removes metric/domain projector stress.",
        "- The topological charge is forced to be the same Hilbert/worldtube source scalar, not an independent label.",
        "- EM stress, Poynting flux, and binding energy must enter the Hilbert source exactly once before readout.",
        "- Dressed Hilbert source reaches Newtonian `GM` only through Poisson/Gauss/orbital calibration.",
        "",
        "## Still Not Claimed",
        "- Constant universal `G_eff` is not yet parent-signed.",
        "- Radial/time derivative hair in `mu_obs` is not yet silent.",
        "- Poynting/radiative flux has to be zero or explicitly bounded.",
        "- PPN source stability remains downstream.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4106_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE.csv`",
        "- `P8_Y5_R2FR_4106_EPSILON_MU_STATUS.csv`",
        "- `P8_Y5_R2FR_4106_NEWTON_THEOREM_CONDITIONS.csv`",
        "- `P8_Y5_R2FR_4106_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4106_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4106_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4106_STATUS.csv`",
        "- `P8_Y5_BRR545_4106_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4107-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md`",
        "- Objective: prove constant universal `G_eff/kappa` and radial/time derivative silence, or create sourced bound rows for `dln_Geff_dt`, `dln_Meff_dt`, `partial_t_epsilon_mu`, and `partial_r_ln_mu_obs`.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4106_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE"], source_coupling_spine_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_EPSILON_MU_STATUS"], epsilon_mu_status_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_NEWTON_THEOREM_CONDITIONS"], newton_theorem_condition_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4106_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4106_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4106_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4106_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    spine_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE"]))
    spine_tokens = ["PiM/Hilbert", "residual identity", "Poynting", "Gauss", "constant coupling"]
    missing_spine = [token for token in spine_tokens if token not in spine_text]
    add("VAL4106_3_spine_complete", "source-coupling spine reaches Gauss/orbital and constant coupling gate", not missing_spine, ";".join(missing_spine) or "spine tokens present")

    epsilon_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4106_EPSILON_MU_STATUS"]))
    epsilon_tokens = ["epsilon_mu", "epsilon_PiM", "epsilon_EM_source_total", "Delta_cal", "epsilon_source_measure_total"]
    missing_epsilon = [token for token in epsilon_tokens if token not in epsilon_text]
    add("VAL4106_4_epsilon_status", "epsilon_mu residual status includes source/projector/EM/calibration components", not missing_epsilon, ";".join(missing_epsilon) or "epsilon tokens present")

    condition_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4106_NEWTON_THEOREM_CONDITIONS"]))
    condition_tokens = ["same observed frame", "Q_M", "EM/Poynting", "Poisson", "G_eff", "PPN", "mu_obs"]
    missing_condition = [token for token in condition_tokens if token not in condition_text]
    add("VAL4106_5_newton_conditions", "Newton theorem conditions include source, EM, Gauss, Geff, and PPN gates", not missing_condition, ";".join(missing_condition) or "Newton conditions present")

    decisions = parse_csv(outputs["P8_Y5_R2FR_4106_DECISION_GATE"])
    poynting_decision = any(row.get("status") == "POYNTING_ROLE_FIXED" for row in decisions)
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" for row in decisions)
    add("VAL4106_6_decisions", "decision gate fixes Poynting role and selects next target", poynting_decision and next_decision, f"poynting={poynting_decision}; next={next_decision}")

    claims = parse_csv(outputs["P8_Y5_R2FR_4106_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    blocked_or_conditional = all(row.get("status") in {"BLOCKED", "CONDITIONAL_ONLY"} for row in claims)
    add("VAL4106_7_claim_guard", "all claim rows are blocked or conditional and nonpublic", no_public_claim and blocked_or_conditional, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4106_NEXT_TARGET"])
    next_ok = any("4107-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4106_8_next_target", "next target is constant Geff/radial-time hair gate", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4106_STATUS"])
    status_text = " ".join(" ".join(row.values()) for row in status_rows_local)
    status_ok = DECISION in status_text and "no Newton_local_GR_PPN_R10 claim" in status_text
    add("VAL4106_9_status", "status records decision and no-claim state", status_ok, "status row checked")

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4106*")) or any(
            FORMALIZATION.rglob("4106-Y5-R2FR*")
        )
    add("VAL4106_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4106_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4106_VALIDATION.csv"
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
