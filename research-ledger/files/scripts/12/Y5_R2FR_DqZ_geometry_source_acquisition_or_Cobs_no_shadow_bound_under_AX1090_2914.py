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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2914"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2914-Y5-R2FR-DqZ-geometry-source-acquisition-or-Cobs-no-shadow-bound-under-AX1090.md"

SRC_2913_DOC = ROOT / "2913-Y5-R2FR-parent-auxiliary-constraint-origin-or-DqZ-geometry-bound-fill-under-AX1090.md"
SRC_2913_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2913_DQZ_GEOMETRY_ACQUISITION_CONTRACT.csv"
SRC_2913_NEXT = RESIDUALS / "P8_Y5_R2FR_2913_NEXT_TARGET.csv"
SRC_2913_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2913_CLAIM_GATES.csv"
SRC_2911_DQZ = RESIDUALS / "P8_Y5_R2FR_2911_FINITE_DQZ_NORM_VECTOR.csv"
SRC_2911_QMAP = RESIDUALS / "P8_Y5_R2FR_2911_Q_MAP_DERIVATIVE_AUDIT.csv"
SRC_2885_FACTOR = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv"
SRC_2886_COMPONENT = RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv"
SRC_943_CONTRACT = RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
SRC_944_FRAME = RESIDUALS / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv"
SRC_945_OBS = RESIDUALS / "P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv"
SRC_945_QMAP = RESIDUALS / "P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv"
SRC_945_BOUNDS = RESIDUALS / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv"
SRC_946_INTERFACE = RESIDUALS / "P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv"
SRC_947_PROJECTION = RESIDUALS / "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv"
SRC_1029_THEOREM = RESIDUALS / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv"
SRC_1029_INTAKE = RESIDUALS / "P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv"
SRC_1029_TAU = RESIDUALS / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv"
SRC_1030_CONTRACT = RESIDUALS / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
SRC_1030_PROVENANCE = RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv"
SRC_1031_TERMINAL = RESIDUALS / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv"
SRC_1031_FALLBACK = RESIDUALS / "P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2914_SOURCE_REGISTER.csv",
    "cobs": RESIDUALS / "P8_Y5_R2FR_2914_COBS_FUNCTOR_NORMALIZATION_AUDIT.csv",
    "shadow": RESIDUALS / "P8_Y5_R2FR_2914_NO_SHADOW_COMPONENT_BOUND_AUDIT.csv",
    "heads": RESIDUALS / "P8_Y5_R2FR_2914_DQZ_GEOMETRY_HEAD_ACQUISITION_ROWS.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2914_ARENA_PROJECTION_REQUIREMENTS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2914_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2914_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2914_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2914_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2914_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2914_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "cobs_copy": PARENT_ACTION / "Cobs_no_shadow_head_audit_2914_NONCLAIM.csv",
    "heads_copy": LOCAL_BOUNDS / "DqZ_geometry_head_acquisition_2914_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2914_CSHADOW_COMPONENT_BOUND_OR_COBS_PROOF_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


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
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2914_00_2913_doc", SRC_2913_DOC, "NEXT2913_0_2914;C_Obs_e", "2913 handoff to DqZ geometry head acquisition"),
        ("SRC2914_01_2913_contract", SRC_2913_CONTRACT, "DGC2913_01_C_Obs_e;DGC2913_09_no_shadow", "2913 DqZ geometry acquisition contract"),
        ("SRC2914_02_2913_next", SRC_2913_NEXT, "NEXT2913_0_2914;C_Obs_e/C_shadow", "machine-readable 2914 target"),
        ("SRC2914_03_2913_claims", SRC_2913_CLAIMS, "CG2913_5_local_GR_Newton;BLOCKED_NONCLAIM", "2913 local claim ceiling"),
        ("SRC2914_04_2911_dqz", SRC_2911_DQZ, "DQZ2911_1_DqZ_geometry;DQZ2911_TOTAL", "upstream DqZ geometry vector"),
        ("SRC2914_05_2911_qmap", SRC_2911_QMAP, "QMAP2911_1_Dq_geometry;QMAP2911_7_verdict", "Dq geometry conditional zero and verdict"),
        ("SRC2914_06_2885_factor", SRC_2885_FACTOR, "DQZF2885_0_Dq_Z_norm;DQZF2885_2_C_Obs_e", "DqZ factor value/blocker ledger"),
        ("SRC2914_07_2886_component", SRC_2886_COMPONENT, "DQC2886_0_E_DqZ_coframe;MISSING_COMPONENT_VALUES", "first finite DqZ coframe component"),
        ("SRC2914_08_943_contract", SRC_943_CONTRACT, "CFC943_1_observed_coframe_descent;CFC943_6_no_shadow_frame_rule", "observed coframe/no-shadow contract"),
        ("SRC2914_09_944_frame", SRC_944_FRAME, "FLB944_0_cg_weyl;FLB944_7_epsilon_frame_leak", "frame leak bound pack"),
        ("SRC2914_10_945_obs", SRC_945_OBS, "OBS945_0_projection_functor;OBS945_6_verdict", "Obs_e functor audit"),
        ("SRC2914_11_945_qmap", SRC_945_QMAP, "QMAP945_2_observed_functor;QMAP945_6_verdict", "q candidate and observed functor construction"),
        ("SRC2914_12_945_bounds", SRC_945_BOUNDS, "BND945_0_cg_value;BND945_7_score_gate", "first frame leak bound rows"),
        ("SRC2914_13_946_interface", SRC_946_INTERFACE, "CGB946_0_cg_R10;CGB946_1_cg_PPN_gamma", "c_g arena interface"),
        ("SRC2914_14_947_projection", SRC_947_PROJECTION, "PFA947_0_R10_projection;PFA947_4_cg_parent_value", "projection fill attempt"),
        ("SRC2914_15_1029_theorem", SRC_1029_THEOREM, "NST1029_2_no_extra_frame_slot;NST1029_6_verdict", "no-shadow-frame theorem audit"),
        ("SRC2914_16_1029_intake", SRC_1029_INTAKE, "CGI1029_1_finite_cg_R10;MISSING_PARENT_INPUT", "c_g provenance template"),
        ("SRC2914_17_1029_tau", SRC_1029_TAU, "TAU1029_0_R10;TAU1029_1_PPN_gamma_beta", "tau projection requirements"),
        ("SRC2914_18_1030_contract", SRC_1030_CONTRACT, "SPM1030_0_public_metric_object;SPM1030_6_contract_verdict", "single-public-metric contract"),
        ("SRC2914_19_1030_provenance", SRC_1030_PROVENANCE, "CPG1030_0_zero_branch;CPG1030_4_no_cancellation", "c_g provenance gate binding"),
        ("SRC2914_20_1031_terminal", SRC_1031_TERMINAL, "TPM1031_3_vertical_chain_rule;TPM1031_6_verdict", "terminal public metric proof audit"),
        ("SRC2914_21_1031_fallback", SRC_1031_FALLBACK, "FCG1031_0_cg_value;FCG1031_3_no_cancellation", "finite c_g/tau fallback"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def cobs_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "COBS2914_0_definition",
            "C_Obs_e",
            "C_Obs_e := ||D Obs_e||_{q->e}, the operator norm from visible quotient perturbations to observed coframe/metric perturbations.",
            "DEFINITION_SHARP",
            "dimensionless after q/e norm declarations",
            "makes DqZ_geometry a bounded operator rather than a slogan",
            "none at definition level",
        ),
        (
            "COBS2914_1_projection_value",
            "candidate normalization C_Obs_e=1",
            "If q contains e_obs as a coordinate and the e-norm is the q-subnorm, Obs_e(q)=e_obs gives ||D Obs_e||=1.",
            "CONDITIONAL_NORMALIZATION_ONLY",
            "dimensionless",
            "would fix the first head without fitting",
            "q_candidate parent ownership and norm conventions are unsigned",
        ),
        (
            "COBS2914_2_chain_zero_against_Z",
            "D_Z Obs_e=0 condition",
            "If Z is absent from q or vertical with Dq[v_Z]=0, then D_Z Obs_e = D Obs_e[Dq(v_Z)] = 0.",
            "CONDITIONAL_CHAIN_RULE_VALID",
            "dimensionless",
            "would kill the coframe part of DqZ_geometry",
            "Dq_Z_norm is not zero/currently parent-signed",
        ),
        (
            "COBS2914_3_uniqueness",
            "unique ordinary observed coframe",
            "All rods, clocks, photons, source currents and orbit readouts use the same quotient-owned e_obs.",
            "NOT_PARENT_UNIQUE",
            "functor certificate",
            "would stop frame relabelling and source/readout drift",
            "terminal/single-public-metric proofs remain closure-only",
        ),
        (
            "COBS2914_4_matter_interface",
            "matter/readout functor through Obs_e",
            "S_matter and readout maps evaluate only on Obs_e(q), theta(q) and retained explicit residuals.",
            "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "functor certificate",
            "would align Hilbert source and geometry response",
            "matter-interface restriction is not derived from parent domain",
        ),
        (
            "COBS2914_5_verdict",
            "C_Obs_e/F_obs_e status for current MTS",
            "current corpus derives a parent-unique observed coframe functor with source/readout uniqueness and fixed norm.",
            "COBS_FUNCTOR_NOT_PARENT_UNIQUE",
            "nonclaim",
            "do not set DqZ_geometry to zero",
            "use conditional C_Obs_e=1 only inside a nonclaim candidate branch",
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "units": units,
                "would_do": would_do,
                "blocking_gap": gap,
                "parent_signed": False,
                "claim_value": "NONE",
            }
        )
        for audit_id, target, statement, status, units, would_do, gap in specs
    ]


def shadow_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SHD2914_0_definition",
            "C_shadow",
            "absolute representative-frame leakage into observed geometry/source/readout not mediated by q",
            "C_shadow_abs := |tau_geom_cg c_g| + |tau_geom_dis b_dis| + |tau_geom_A b_A| + |tau_geom_alpha b_alpha| + |q_nonH| + |Delta_W_support|",
            "DEFINITION_SHARP_NONCANCELLATION",
            "dimensionless_or_arena_specific",
            "no cancellation between unknown frame/source tails",
        ),
        (
            "SHD2914_1_cg_weyl",
            "c_g common Weyl frame",
            "e_m=A_g(Xhat)e_obs gives C_shadow contribution through c_g := Lie_vX ln A_g",
            "C_shadow_cg := |tau_geom_cg c_g|",
            "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
            "dimensionless",
            "1029/1030/1031 prove only conditional no-shadow routes",
        ),
        (
            "SHD2914_2_disformal",
            "b_dis disformal frame",
            "g_m=A_g^2 g_obs+B_g(Xhat)U_mu U_nu survives even when c_g is zero unless excluded or bounded",
            "C_shadow_dis := |tau_geom_dis b_dis|",
            "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
            "model_dependent",
            "single-public-metric c_g-only closure is insufficient",
        ),
        (
            "SHD2914_3_constants",
            "b_A/b_alpha constants and material markers",
            "vertical dependence of masses, charges or clock constants can hide frame leakage after a field rename",
            "C_shadow_const := |tau_geom_A b_A| + |tau_geom_alpha b_alpha|",
            "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BOUND",
            "dimensionless",
            "terminal metric alone does not control constants/source normalization",
        ),
        (
            "SHD2914_4_nonHilbert_support",
            "q_nonH/Delta_W_support",
            "non-Hilbert current, boundary/source support or tau-normal mismatch can source geometry despite matter-frame silence",
            "C_shadow_support := |q_nonH| + |Delta_W_support| + |Delta_tau_n|",
            "MISSING_SOURCE_SUPPORT_ZERO_OR_NUMERIC_BOUND",
            "source_normalized",
            "local GR source side is not won by c_g=0 alone",
        ),
        (
            "SHD2914_5_verdict",
            "C_shadow zero/current bound",
            "current corpus derives C_shadow=0 or a numeric source-backed upper bound.",
            "C_shadow_abs=0 or C_shadow_abs<=source_backed_bound",
            "CSHADOW_ZERO_OR_BOUND_NOT_DERIVED",
            "nonclaim",
            "stage component rows; no DqZ_geometry claim",
        ),
    ]
    return [
        add_common(
            {
                "shadow_id": shadow_id,
                "symbol": symbol,
                "statement": statement,
                "formula_or_component": formula,
                "current_status": status,
                "units": units,
                "reason": reason,
                "absolute_no_cancellation": True,
                "claim_value": "MISSING",
            }
        )
        for shadow_id, symbol, statement, formula, status, units, reason in specs
    ]


def head_rows() -> list[dict[str, Any]]:
    specs = [
        ("HEAD2914_0_DqZ_geometry_total", "DqZ_geometry_abs", "abs(E_DqZ_geometry) <= Pi_geom_abs*C_Obs_e_abs*Dq_Z_norm_abs*N_Z_abs + C_shadow_abs + E_boundary_geom_abs + E_readout_geom_abs", "dimensionless_frame_or_metric_response", "all heads below", "MISSING_COMPONENT_INPUTS"),
        ("HEAD2914_1_C_Obs_e_abs", "C_Obs_e_abs", "operator norm ||D Obs_e||_{q->e}; conditional candidate value 1 only if q contains e_obs with matching norm", "dimensionless", "parent q/e norm and Obs_e uniqueness certificate", "CONDITIONAL_1_NOT_PARENT_SIGNED"),
        ("HEAD2914_2_Dq_Z_norm_abs", "Dq_Z_norm_abs", "operator norm ||Dq[v_Z]||_q/||v_Z||_Z", "dimensionless_after_norms", "parent q map, Dq matrix, Z basis, q/Z norms", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("HEAD2914_3_N_Z_abs", "N_Z_abs", "allowed amplitude/norm of Z-basis perturbation in local compact branch", "declared_Z_norm_units", "rank/eigenbasis and branch normalization", "MISSING_Z_DIRECTION_NORM"),
        ("HEAD2914_4_Pi_geom_abs", "Pi_geom_abs", "projection norm from coframe/metric response to PPN, clock, orbital and R10 geometry observables", "arena_projection_norm", "gauge-fixed weak-field/readout maps", "MISSING_ARENA_PROJECTION"),
        ("HEAD2914_5_C_shadow_abs", "C_shadow_abs", "sum_abs of Weyl/disformal/constants/non-Hilbert/support frame leakage components", "dimensionless_or_arena_specific", "c_g, b_dis, b_A, b_alpha, q_nonH, Delta_W_support source rows", "MISSING_COMPONENT_VALUES"),
        ("HEAD2914_6_E_boundary_geom_abs", "E_boundary_geom_abs", "boundary/projector/source-support geometry tail", "arena_geometry_units", "proper collar, boundary primitive, projector commutator", "MISSING_BOUNDARY_TAIL_BOUND"),
        ("HEAD2914_7_E_readout_geom_abs", "E_readout_geom_abs", "clock/EM/orbit/PPN readout regeneration of geometry leakage", "arena_geometry_units", "readout functor and marker silence", "MISSING_READOUT_TAIL_BOUND"),
        ("HEAD2914_8_promotion_rule", "promotion_rule", "valid_for_claim true only after all heads are numeric or theorem-zero, sourced, unit-locked and no MISSING markers remain", "boolean_gate", "validation plus no-cancellation guard", "PROMOTION_BLOCKED_NOW"),
    ]
    return [
        add_common(
            {
                "head_id": head_id,
                "symbol": symbol,
                "definition_or_bound": definition,
                "units": units,
                "required_source_or_input": required,
                "current_status": status,
                "candidate_value": "MISSING" if "CONDITIONAL_1" not in status else "1_CONDITIONAL_NONCLAIM",
                "source_paths": ";".join(str(p) for p in [SRC_2913_CONTRACT, SRC_2885_FACTOR, SRC_945_OBS, SRC_944_FRAME, SRC_1029_INTAKE]),
                "promotion_allowed_now": False,
            }
        )
        for head_id, symbol, definition, units, required, status in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("APR2914_0_PPN", "PPN gamma/beta/preferred-frame", "Pi_geom must map coframe response into gamma, beta, alpha1/alpha2/alpha3 with gauge/profile and disformal separation", "MISSING_PPN_RESPONSE_MATRIX", "no PPN pass"),
        ("APR2914_1_clock", "clock/EM", "readout tail must separate c_g common-frame clock drift from b_A/b_alpha sensitivity", "MISSING_CLOCK_COMMON_MODE_SPLIT", "no clock/EM pass"),
        ("APR2914_2_orbital", "orbital/source support", "geometry/source support must use same observed coframe and measured-GM convention", "MISSING_SOURCE_SUPPORT_PROJECTION", "no orbital/Newton pass"),
        ("APR2914_3_R10", "R10 alpha(lambda)", "C_shadow/c_g branch needs K_X(lambda), Qbar_XH, tau_R10 and real bound curve before score", "MISSING_R10_PROJECTION_AND_VALUES", "no R10 pass"),
        ("APR2914_4_local_GR", "local GR/Newton", "all DqZ_geometry heads must be theorem-zero or bounded below tolerance plus source/EH/PPN gates", "BLOCKED_NONCLAIM", "no local GR claim"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "requirement": requirement,
                "current_status": status,
                "claim_effect": effect,
            }
        )
        for arena_id, arena, requirement, status, effect in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2914_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked"),
        ("RUN2914_1_Cobs", "COBS_CONDITIONAL_NORMALIZATION_NOT_PARENT_SIGNED", "C_Obs_e/F_obs_e", False, "candidate C_Obs_e=1 is only a norm convention inside an unsigned q branch"),
        ("RUN2914_2_no_shadow", "CSHADOW_ZERO_NOT_DERIVED_COMPONENTS_RETAINED", "C_shadow", False, "c_g/disformal/constants/non-Hilbert/support components remain missing"),
        ("RUN2914_3_heads", "DQZ_GEOMETRY_HEAD_ROWS_STAGED_NONCLAIM", "DqZ_geometry acquisition heads", False, "contract is complete but no row is score-ready"),
        ("RUN2914_4_next", "2915_CSHADOW_COMPONENT_BOUND_SELECTED", "next target", False, "componentize C_shadow/c_g/disformal or prove stronger no-shadow branch"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2914_0_Cobs_definition", "C_Obs_e/F_obs_e contract is defined", "PASS_CONDITIONAL_ONLY", "definition and candidate normalization exist, but not a parent theorem", True),
        ("CG2914_1_Cobs_value", "C_Obs_e=1 can be used as claim input", "BLOCKED_NONCLAIM", "q/e norm and parent-unique observed coframe are unsigned", False),
        ("CG2914_2_Cshadow_zero", "C_shadow=0 by no-shadow theorem", "BLOCKED_NONCLAIM", "single-public-metric/no-extra-frame and field-rename guards remain unsigned", False),
        ("CG2914_3_DqZ_geometry_bound", "DqZ_geometry finite row is score-ready", "BLOCKED_NONCLAIM", "head values/projections/source paths are missing", False),
        ("CG2914_4_R10_PPN_clock_orbit", "R10/PPN/clock/orbital tests can be run from 2914", "BLOCKED_NONCLAIM", "2914 only stages input contracts", False),
        ("CG2914_5_local_GR_Newton", "local GR/Newton follows after 2914", "BLOCKED_NONCLAIM", "DqZ geometry/source/readout and EH/source gates remain open", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2914_0_result", "Cobs_head_sharpened_not_claimed", "C_Obs_e can be normalized to 1 only inside the unsigned candidate q branch; this is useful bookkeeping, not theorem evidence.", "keep C_Obs_e as conditional nonclaim input"),
        ("DEC2914_1_shadow", "Cshadow_is_now_the_main_geometry_leak", "Once C_Obs_e is treated as a candidate norm, the dangerous piece is representative frame leakage: c_g, b_dis, constants, non-Hilbert/source support.", "componentize C_shadow next"),
        ("DEC2914_2_local_GR", "local_GR_still_blocked_but_less_vague", "The blocker is no longer a generic plateau issue; it is a finite geometry response ledger with named heads and arenas.", "do not claim GR; fill/prove heads"),
        ("DEC2914_3_next", "go_to_2915_Cshadow_component_pack", "The fastest non-loop progress is to build the C_shadow component envelope and decide whether any component can be theorem-zero.", "try c_g/disformal/constants/support component proof or source rows"),
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
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2914_0_2915",
                "selection_status": "selected_primary",
                "target_file": "2915-Y5-R2FR-Cshadow-component-bound-pack-or-Cobs-parent-normalization-proof-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Cshadow_component_bound_pack_or_Cobs_parent_normalization_proof_under_AX1090_2915.py",
                "task": "componentize C_shadow into c_g, b_dis, b_A, b_alpha, q_nonH and Delta_W_support, while checking whether C_Obs_e=1 can be parent-normalized rather than declared",
                "success_condition": "at least one C_shadow component is parent theorem-zero or every component gets source-ready numeric/provenance requirements with arena projections and no MISSING promotion",
                "fallback_condition": "keep C_shadow_abs as a strict nonclaim absolute envelope and select the first missing component for real source acquisition",
                "guardrails": "no local GR/Newton/R10/PPN claim; no Weyl/disformal field rename shortcut; no cancellation among unknowns; no source-less numeric values; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("cobs_copy", OUTPUTS["cobs"], BRANCH_OUTPUTS["cobs_copy"]),
        ("heads_copy", OUTPUTS["heads"], BRANCH_OUTPUTS["heads_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    cobs_rows_: list[dict[str, Any]],
    shadow_rows_: list[dict[str, Any]],
    head_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    cobs_verdict = next(row for row in cobs_rows_ if row["audit_id"] == "COBS2914_5_verdict")
    shadow_verdict = next(row for row in shadow_rows_ if row["shadow_id"] == "SHD2914_5_verdict")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2914_5_local_GR_Newton")
    required_heads = {
        "DqZ_geometry_abs",
        "C_Obs_e_abs",
        "Dq_Z_norm_abs",
        "N_Z_abs",
        "Pi_geom_abs",
        "C_shadow_abs",
        "E_boundary_geom_abs",
        "E_readout_geom_abs",
        "promotion_rule",
    }
    head_symbols = {str(row["symbol"]) for row in head_rows_}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2914_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2914_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2914_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2914_3_Cobs_not_promoted", cobs_verdict["current_status"] == "COBS_FUNCTOR_NOT_PARENT_UNIQUE" and not bool(cobs_verdict["parent_signed"]), "C_Obs_e/F_obs_e remains conditional nonclaim"),
        ("VAL2914_4_Cshadow_not_promoted", shadow_verdict["current_status"] == "CSHADOW_ZERO_OR_BOUND_NOT_DERIVED", "C_shadow has no theorem-zero or numeric bound"),
        ("VAL2914_5_heads_complete", required_heads.issubset(head_symbols), "DqZ_geometry head acquisition rows complete"),
        (
            "VAL2914_6_heads_nonclaim",
            all(not bool(row["promotion_allowed_now"]) and not bool(row["valid_for_claim"]) for row in head_rows_),
            "all head rows remain nonclaim",
        ),
        (
            "VAL2914_7_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2914_8_next_target_selected", next_rows_[0]["route_id"] == "NEXT2914_0_2915" and bool(next_rows_[0]["selected"]), "2915 Cshadow component target selected"),
        ("VAL2914_9_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2914_10_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2914_11_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2914_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2914 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    cobs_rows_: list[dict[str, Any]],
    shadow_rows_: list[dict[str, Any]],
    head_rows_: list[dict[str, Any]],
    arena_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2914_OVERALL")
    text = f"""# 2914 - Y5/R2FR DqZ Geometry Source Acquisition Or Cobs No-Shadow Bound Under AX1090

Status: `Y5_R2FR_2914_Cobs_conditional_normalization_Cshadow_not_derived_DqZ_geometry_heads_staged_2915_next`

Claim ceiling: `DqZ_geometry_head_acquisition_nonclaim_only_no_DqZ_zero_no_Cshadow_zero_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2914 attacks the first concrete head of the `DqZ_geometry` residual instead of circling the same GR-blocker language.

The useful result is that `C_Obs_e` is now separated from the dangerous frame leakage. If the candidate quotient `q` contains `e_obs` as a public coordinate and the q/e norms are matched, then `C_Obs_e=1` is a clean conditional normalization. But it is still not a claim input, because the parent-unique observed coframe and matter/readout functor are not signed.

The dangerous term is now named: `C_shadow_abs`. It is the absolute no-cancellation envelope over representative Weyl/disformal frame leakage, constants/material markers, non-Hilbert currents and support shifts. Current MTS does not derive `C_shadow=0`, and no numeric source-backed bound is present.

So the local-GR problem is narrower again:

`DqZ_geometry_abs <= Pi_geom_abs*C_Obs_e_abs*Dq_Z_norm_abs*N_Z_abs + C_shadow_abs + E_boundary_geom_abs + E_readout_geom_abs`

This is still nonclaim, but it is now a proper acquisition formula rather than a vague plateau debt.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Cobs Functor Normalization Audit

{md_table(cobs_rows_, ["audit_id", "target", "current_status", "statement", "units", "would_do", "blocking_gap", "parent_signed", "valid_for_claim"])}

## No-Shadow Component Bound Audit

{md_table(shadow_rows_, ["shadow_id", "symbol", "current_status", "statement", "formula_or_component", "units", "reason", "absolute_no_cancellation", "valid_for_claim"])}

## DqZ Geometry Head Acquisition Rows

{md_table(head_rows_, ["head_id", "symbol", "definition_or_bound", "units", "required_source_or_input", "current_status", "candidate_value", "promotion_allowed_now", "valid_for_claim"])}

## Arena Projection Requirements

{md_table(arena_rows_, ["arena_id", "arena", "requirement", "current_status", "claim_effect", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is not a proof of local GR, but it is a real narrowing of the battlefield. `C_Obs_e` is probably not where the beast lives if the public-coframe branch is eventually signed; it can be normalized cleanly inside that branch. The beast is `C_shadow_abs`: common Weyl frame, disformal frame, constants, non-Hilbert current and support shift.

That makes 2915 the sensible next punch: componentize `C_shadow` and try to kill or source its pieces one by one.

## Not Claimed

- `C_Obs_e=1` is not claim-valid; it is conditional on the unsigned parent q/coframe branch.
- `C_shadow=0` is not derived.
- `Dq_Z_norm=0`, `DqZ_geometry=0`, source/readout descent and boundary silence are not proved.
- Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    cobs_rows_ = cobs_rows()
    shadow_rows_ = shadow_rows()
    head_rows_ = head_rows()
    arena_rows_ = arena_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["cobs"], cobs_rows_)
    write_csv(OUTPUTS["shadow"], shadow_rows_)
    write_csv(OUTPUTS["heads"], head_rows_)
    write_csv(OUTPUTS["arenas"], arena_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        cobs_rows_,
        shadow_rows_,
        head_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        cobs_rows_,
        shadow_rows_,
        head_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        cobs_rows_,
        shadow_rows_,
        head_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        cobs_rows_,
        shadow_rows_,
        head_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2914_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
