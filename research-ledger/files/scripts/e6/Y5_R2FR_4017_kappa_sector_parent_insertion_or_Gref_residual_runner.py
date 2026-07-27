from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4017"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4017-Y5-R2FR-kappa-sector-parent-insertion-or-Gref-residual-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4017_SOURCE_REGISTER.csv",
    "packet": SRC / "P8_Y5_R2FR_4017_KAPPA_SECTOR_INSERTION_PACKET.csv",
    "theorem": SRC / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4017_KAPPA_INSERTION_AUDIT.csv",
    "runner": SRC / "P8_Y5_R2FR_4017_GREF_RESIDUAL_RUNNER_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4017_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4017_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4017_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4017_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4017_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4017_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4017_VALIDATION.csv",
}

NEXT_DOC = "4018-Y5-R2FR-second-order-PPN-source-stability-or-gamma-beta-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4018_second_order_PPN_source_stability_or_gamma_beta_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4017_00_handoff", SRC / "P8_Y5_R2FR_4016_NEXT_TARGET.csv", "NEXT4016_0", "4016 handoff"),
        ("SRC4017_01_4016_sector", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_0_global_sector_factorization", "global sector theorem"),
        ("SRC4017_02_4016_noHom", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_1_no_Hom_to_coupling", "no-Hom theorem"),
        ("SRC4017_03_4016_calibration", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_2_same_branch_calibration", "same branch calibration"),
        ("SRC4017_04_4016_derivative", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_3_derivative_silence", "derivative silence"),
        ("SRC4017_05_4016_Bianchi", SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "GSS4016_4_Bianchi_guard", "Bianchi guard"),
        ("SRC4017_06_4016_finite", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_0_master", "4016 finite vector"),
        ("SRC4017_07_4016_Csector", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_1_C_sector", "sector residual"),
        ("SRC4017_08_4016_Cscalar", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_2_C_local_scalar", "local scalar residual"),
        ("SRC4017_09_4016_CnoHom", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_3_C_noHom", "no-Hom residual"),
        ("SRC4017_10_4016_Gdot", SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv", "GREF4016_5_Gdot", "Gdot residual"),
        ("SRC4017_11_4015_Newton", SRC / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv", "GPN4015_5_G_constant_policy", "Newton constant policy"),
        ("SRC4017_12_4015_vector", SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv", "NBR4015_4_C_Gref_kappa", "Newton bridge Gref/kappa row"),
        ("SRC4017_13_CU0", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU0_same_frame_EH_source", "same-frame EH source"),
        ("SRC4017_14_CU1", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "global coupling contract"),
        ("SRC4017_15_CU2", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU2_no_MTS_invariant_dependence", "no invariant dependence"),
        ("SRC4017_16_CU3", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU3_species_source_blindness", "source blindness"),
        ("SRC4017_17_CU4", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU4_no_range_radial_running", "range/radial contract"),
        ("SRC4017_18_CU5", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU5_Bianchi_exchange_zero", "Bianchi exchange contract"),
        ("SRC4017_19_CU6", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU6_constant_only_calibration_policy", "constant calibration policy"),
        ("SRC4017_20_GS0", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS0_configuration_factorization", "global coupling factorization"),
        ("SRC4017_21_GS1", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS1_kappa_not_local_field", "kappa not local field"),
        ("SRC4017_22_GS2", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS2_trivial_MTS_action_on_kappa", "trivial MTS action"),
        ("SRC4017_23_GS3", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS3_no_species_marker_source_label", "no source marker"),
        ("SRC4017_24_GS4", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS4_no_range_radial_time_dependence", "no range/radial/time"),
        ("SRC4017_25_GS5", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS5_Bianchi_arbitrary_source_consistency", "Bianchi consistency"),
        ("SRC4017_26_GS6", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS6_constant_offset_policy", "constant offset"),
        ("SRC4017_27_KGL0", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_0_delta_kappa", "delta kappa"),
        ("SRC4017_28_KGL4", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_4_Geff_product", "G product"),
        ("SRC4017_29_bounds_Gdot", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_Geff_time_drift", "Gdot bound"),
        ("SRC4017_30_bounds_range", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_range_dependence", "range bound"),
        ("SRC4017_31_bounds_beta", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_nonlinear_beta_source_residue", "PPN beta bound"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def packet_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "KSP4017_0_config",
            "configuration object",
            "Q_parent := Q_dyn x K_G with kappa_* in K_G",
            "K_G is a branch/global coupling object, not a local field bundle",
            "T_local K_G=0; no compact-support delta kappa",
        ),
        (
            "KSP4017_1_action",
            "minimal action insertion",
            "S_parent[Phi,psi;kappa_*]=S_MTS_dyn[Phi]+(1/(2*kappa_*)) int R[e_obs(q(Phi))] dmu_obs + S_matter[psi,e_obs(q(Phi)),theta]+S_EM",
            "kappa_* appears only as the coefficient of the reduced EH source-coupling line on a fixed branch",
            "does not add a new local degree of freedom",
        ),
        (
            "KSP4017_2_calibration",
            "same-branch calibration",
            "G_ref := c^4*kappa_*/(8*pi)",
            "one kappa_* feeds EH, Hamiltonian, Poisson, Gauss, orbital and later PPN maps",
            "calibration of a universal constant, not a numerical prediction",
        ),
        (
            "KSP4017_3_noHom",
            "coupling no-Hom grammar",
            "Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range,K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0",
            "source/range/domain/memory labels cannot modulate the global coupling",
            "needed to silence WEP/R10/Gdot source drift",
        ),
        (
            "KSP4017_4_variation",
            "local variation rule",
            "delta_local S_parent has delta kappa_*=0 and therefore no E_kappa, Theta_kappa, Q_kappa local current",
            "local field equations vary only Q_dyn variables at fixed kappa_*",
            "prevents scalar-tensor/fifth-force kappa leakage",
        ),
        (
            "KSP4017_5_status",
            "adoption status",
            "packet is mathematically coherent but not yet declared the final parent action",
            "use as conditional branch for Newton/local-GR derivation tests",
            "claims remain false until integrated with source/PPN gates",
        ),
    ]
    return [
        {
            "packet_id": packet_id,
            "component": component,
            "mathematical_form": form,
            "meaning": meaning,
            "guard": guard,
            "status": "CANDIDATE_PARENT_PACKET_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for packet_id, component, form, meaning, guard in rows
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "KVT4017_0_local_variation_zero",
            "local kappa variation is absent",
            "For vertical/local variation v in TQ_dyn x {0}, v(kappa_*)=0, delta_v(1/kappa_*)=0 and no local E_kappa equation is produced",
            "C_local_scalar=0 and no scalar-kappa fifth force if K_G is genuinely global",
            "EXACT_CONDITIONAL_VARIATION_THEOREM",
        ),
        (
            "KVT4017_1_EH_coefficient_lock",
            "one EH source-coupling coefficient",
            "delta_g [(1/(2*kappa_*)) int R dmu] gives the same kappa_* multiplying the reduced stress source after same-frame matter descent",
            "C_Gref_kappa=0 for the EH/Poisson map when matter stress is on the same branch",
            "EXACT_CONDITIONAL_COEFFICIENT_THEOREM",
        ),
        (
            "KVT4017_2_noHom_derivative_zero",
            "source/range/domain derivatives vanish",
            "If Hom(label,K_G)=0 for all source, material, range, domain and memory labels, then partial_label kappa_*=0 and D_X lnG_ref=0 for those labels",
            "C_noHom=0, partial_A_lnG=0, partial_lambda_lnG=0 and domain/range drift zero conditionally",
            "EXACT_CONDITIONAL_NOHOM_COROLLARY",
        ),
        (
            "KVT4017_3_branch_constant_not_absolute_prediction",
            "global constant is calibration",
            "Different branches may carry different constant kappa_* values; within a branch derivatives vanish, but the numerical value is not predicted without a K_G normalization theorem",
            "keeps GR-like stance: universal coupling can be calibrated without pretending to derive its dimensionful value",
            "CALIBRATION_POLICY_THEOREM",
        ),
        (
            "KVT4017_4_not_enough_for_local_GR",
            "coupling lock is not full local GR",
            "K_G insertion closes the G_ref drift channel only; Pi_M/H_tau source equality, mu_extra, EM once-only and gamma/beta PPN stability remain separate",
            "prevents promotion from constant coupling to local-GR recovery",
            "ANTI_OVERCLAIM_GUARD",
        ),
        (
            "KVT4017_5_residual_runner_fallback",
            "fallback if packet is not adopted",
            "failed packet clause -> residual row among C_sector, C_local_scalar, C_noHom, C_Gref_kappa, Gdot, radial, source, range, frame, exchange",
            "turns unsigned insertion into executable nonclaim residual inputs",
            "FINITE_RUNNER_INTERFACE_NONCLAIM",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": form,
            "derived_result": result,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, claim_piece, form, result, status in rows
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("KIA4017_0_packet_coherence", "action packet is internally coherent", "PASS_CONDITIONAL", "none if treated as branch packet", "test against source and PPN gates"),
        ("KIA4017_1_parent_adoption", "packet is adopted as the actual parent action sector", "NOT_ADOPTED_FINAL", "cannot claim constant G from the full corpus", "future spine/action synthesis must choose or reject it explicitly"),
        ("KIA4017_2_matter_same_branch", "matter stress descends on same branch as EH coefficient", "CONDITIONAL_4008_4015", "different G in geometry/source maps", "bind to source-current and PPN rows"),
        ("KIA4017_3_noHom_signed", "no source/range/domain Hom into K_G", "CONDITIONAL_UNSIGNED", "WEP/R10/range/source drift", "retain no-Hom residuals if not adopted"),
        ("KIA4017_4_Bianchi_exchange", "no hidden Bianchi exchange is used to prove constancy", "GUARD_LOCKED", "fake constant-G derivation", "exchange row stays live unless separately zeroed"),
        ("KIA4017_5_numeric_G", "absolute numerical G is predicted", "REJECTED", "dimensionful overclaim", "keep numerical G as calibrated constant"),
        ("KIA4017_6_local_GR", "local GR follows from packet alone", "REJECTED", "PPN/local source overclaim", "move to gamma/beta/source-stability target"),
    ]
    return [
        {
            "audit_id": audit_id,
            "clause": clause,
            "current_status": status,
            "risk_if_open": risk,
            "next_action": action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, clause, status, risk, action in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GRR4017_0_C_sector", "C_sector", "0 if K_G parent sector is adopted; else 1 or sourced residual", "dimensionless", "blocks constant G if nonzero", "parent action sector source", "false"),
        ("GRR4017_1_C_local_scalar", "C_local_scalar", "0 if kappa_* notin Gamma(E_local); else scalar coupling coefficient", "dimensionless", "activates Gdot/fifth-force", "local scalar field source or theorem zero", "false"),
        ("GRR4017_2_C_noHom", "C_noHom", "0 if Hom(labels,K_G)=0; else max label-to-coupling map norm", "dimensionless", "activates source/range/domain drift", "object-language no-Hom source", "false"),
        ("GRR4017_3_C_Gref_kappa", "C_Gref_kappa", "ln(kappa_eff*c^4/(8*pi*G_ref))", "dimensionless", "EH/Poisson/Newton amplitude mismatch", "same branch calibration source", "false"),
        ("GRR4017_4_Gdot", "D_t_lnG", "D_t ln G_ref; compare with 9.6e-15 yr^-1 if nonzero", "yr^-1", "Gdot empirical pressure", "numeric derivative or theorem zero", "false"),
        ("GRR4017_5_range", "alpha_lambda", "finite-range alpha(lambda) projection from partial_lambda lnG or scalar branch", "dimensionless", "R10/fifth-force pressure", "alpha(lambda) curve and prediction source", "false"),
        ("GRR4017_6_source", "partial_A_lnG", "source/material derivative of lnG_ref", "dimensionless", "WEP/source-charge pressure", "source/material coefficient map", "false"),
        ("GRR4017_7_exchange", "delta_kappa_exchange", "kappa^-1 P_loc[T_obs nabla kappa]", "dimensionless projection", "Bianchi/exchange pressure", "exchange owner theorem or coefficient", "false"),
        ("GRR4017_8_PPN_handoff", "epsilon_PPN_2nd", "|gamma-1|+|beta-1|+|delta_beta_source| after K_G packet", "dimensionless", "local GR promotion gate", "4018 PPN source-stability rows", "false"),
    ]
    return [
        {
            "runner_id": runner_id,
            "quantity": quantity,
            "formula": formula,
            "units": units,
            "if_nonzero": if_nonzero,
            "required_source": required_source,
            "scoreable_now": scoreable,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for runner_id, quantity, formula, units, if_nonzero, required_source, scoreable in rows
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    cases = [
        ("CASE4017_0_packet_adopted_clean", True, True, True, True, False, False, "candidate K_G packet adopted with same branch and no-Hom"),
        ("CASE4017_1_packet_coherent_not_adopted", False, True, True, True, False, False, "packet is coherent but not selected as final parent action"),
        ("CASE4017_2_local_scalar_reentry", True, False, True, True, False, False, "kappa re-enters as local field"),
        ("CASE4017_3_noHom_fails", True, True, False, True, False, False, "labels/range/domain map into K_G"),
        ("CASE4017_4_same_branch_fails", True, True, True, False, False, False, "EH/Poisson/PPN maps use different coupling normalizations"),
        ("CASE4017_5_absolute_G_overclaim", True, True, True, True, True, False, "claims numerical G from calibration"),
        ("CASE4017_6_local_GR_overclaim", True, True, True, True, False, True, "claims full local GR from constant coupling alone"),
        ("CASE4017_7_runner_only", False, False, False, False, False, False, "use residual runner because packet clauses are unsigned"),
    ]
    return [
        {
            "case_id": case_id,
            "packet_adopted": adopted,
            "no_local_kappa": no_local,
            "no_Hom": no_hom,
            "same_branch": same_branch,
            "absolute_G_claim": absolute_g,
            "local_GR_claim": local_gr,
            "description": description,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for case_id, adopted, no_local, no_hom, same_branch, absolute_g, local_gr, description in cases
    ]


def truthy(row: dict[str, Any], key: str) -> bool:
    return str(row[key]).lower() == "true" if isinstance(row[key], str) else bool(row[key])


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cases:
        if truthy(row, "absolute_G_claim"):
            owner = "ABSOLUTE_G_OVERCLAIM_REJECTED"
            residual = "C_absolute_G_claim"
            claim = "NO_NUMERICAL_G_PREDICTION"
            action = "keep G_ref as calibrated unless a parent normalization theorem exists"
        elif truthy(row, "local_GR_claim"):
            owner = "LOCAL_GR_OVERCLAIM_REJECTED"
            residual = "epsilon_PPN_2nd"
            claim = "NO_LOCAL_GR_PROMOTION"
            action = "move to second-order PPN source-stability"
        elif not truthy(row, "packet_adopted"):
            owner = "KAPPA_PACKET_NOT_ADOPTED"
            residual = "C_sector+C_local_scalar+C_noHom+C_Gref_kappa"
            claim = "NO_CONSTANT_G_CLAIM"
            action = "use residual runner or explicitly adopt/reject packet in parent action synthesis"
        elif not truthy(row, "no_local_kappa"):
            owner = "LOCAL_KAPPA_REENTRY_BLOCKED"
            residual = "C_local_scalar+D_t_lnG+alpha_lambda"
            claim = "NO_GDOT_RANGE_SILENCE_CLAIM"
            action = "forbid kappa as local field or source scalar residuals"
        elif not truthy(row, "no_Hom"):
            owner = "NOHOM_GATE_BLOCKED"
            residual = "C_noHom+partial_A_lnG+partial_lambda_lnG"
            claim = "NO_SOURCE_RANGE_SILENCE_CLAIM"
            action = "prove no-Hom object grammar or run WEP/R10 residual rows"
        elif not truthy(row, "same_branch"):
            owner = "SAME_BRANCH_CALIBRATION_BLOCKED"
            residual = "C_Gref_kappa"
            claim = "NO_NEWTON_PPN_COUPLING_MATCH"
            action = "bind EH/Hamiltonian/Poisson/PPN maps to same kappa_*"
        elif row["case_id"] == "CASE4017_0_packet_adopted_clean":
            owner = "CONDITIONAL_KAPPA_SECTOR_INSERTION_LOCK"
            residual = "C_sector_C_local_scalar_C_noHom_C_Gref_kappa_ZERO_IF_PACKET_ADOPTED"
            claim = "CONSTANT_UNIVERSAL_GREF_CONDITIONAL_ONLY"
            action = "feed packet into 4018 PPN gamma/beta source-stability gate"
        else:
            owner = "GREF_RUNNER_NONCLAIM"
            residual = "FULL_RUNNER_VECTOR_REQUIRED"
            claim = "NO_CLAIM"
            action = "source numeric/theorem rows before scoring"
        rows.append(
            {
                "case_id": row["case_id"],
                "owner_status": owner,
                "residual_result": residual,
                "claim_result": claim,
                "next_action": action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4017_0_insert_packet", "write minimal K_G parent sector packet", "this is the first actual constructive coupling insertion rather than a missing-row statement", "conditional branch available"),
        ("DEC4017_1_not_final_action", "do not declare packet final parent action yet", "corpus-level adoption must also close source charge, EM once-only and PPN gates", "claims remain false"),
        ("DEC4017_2_runner", "emit residual runner rows for every unsigned packet clause", "if K_G is not adopted, drift/range/source terms stay executable", "no hidden measured-GM laundering"),
        ("DEC4017_3_next", f"move to {NEXT_DOC}", "with a candidate coupling sector in hand, the next local-GR bottleneck is gamma/beta/source-stability", "pushes beyond Newton to local-GR tests"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, rationale, effect in rows
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CLAIM4017_0_packet", "K_G packet is final parent action", False, "packet is candidate/conditional, not final corpus adoption"),
        ("CLAIM4017_1_constant_G", "constant universal G_ref", False, "conditional on packet adoption and source/branch locks"),
        ("CLAIM4017_2_absolute_G", "numerical G prediction", False, "calibration is not a normalization theorem"),
        ("CLAIM4017_3_Newton", "Newton source coupling pass", False, "requires 4015/4012/source equality plus packet adoption"),
        ("CLAIM4017_4_local_GR", "local GR pass", False, "requires 4018 PPN gamma/beta/source-stability"),
    ]
    return [
        {
            "claim_id": claim_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for claim_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4017_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "derive the second-order PPN source-stability gate for local GR: whether the MTS reduced metric gives gamma=1, beta=1, and zero source-normalized beta residual after the K_G packet and Newton bridge",
            "success_condition": "gamma-1, beta-1 and delta_beta_source are zero by parent reduction, or converted into explicit nonclaim PPN residual rows with observable bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Minimal parent K_G/kappa sector insertion packet constructed; local variation/no-Hom theorem derived conditionally; residual runner emitted for unsigned drift/range/source clauses.",
            "claim_allowed": False,
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["needle_found"])
    lines = [
        "# 4017 - Kappa Sector Parent Insertion Or G_ref Residual Runner",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint takes the coupling leap constructively.",
        "",
        "Candidate parent-sector packet:",
        "",
        "`Q_parent := Q_dyn x K_G`, with `kappa_* in K_G`.",
        "",
        "`S_parent[Phi,psi;kappa_*]=S_MTS_dyn[Phi]+(1/(2*kappa_*)) int R[e_obs(q(Phi))] dmu_obs + S_matter[psi,e_obs(q(Phi)),theta]+S_EM`.",
        "",
        "`G_ref := c^4*kappa_*/(8*pi)`.",
        "",
        "Local variations are taken along `TQ_dyn x {0}`, so `delta_local kappa_*=0`. Therefore the packet does not create a local scalar-kappa field, local `E_kappa`, or local kappa Noether current.",
        "",
        "## No-Hom Lock",
        "",
        "The packet only kills source/range/domain drift if the object language also signs",
        "",
        "`Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range,K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0`.",
        "",
        "Under that grammar, the coupling cannot depend on source labels, material labels, finite range, domain, memory, or projector data.",
        "",
        "## What This Does And Does Not Do",
        "",
        "It can conditionally close `C_sector`, `C_local_scalar`, `C_noHom`, and `C_Gref_kappa`.",
        "",
        "It does **not** claim the numerical value of `G`, does **not** by itself prove `Pi_M/H_tau` source equality, and does **not** give local GR until the second-order PPN source-stability gate is closed.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: owner=`{row['owner_status']}`, residual=`{row['residual_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a constructive route, not a closure axiom: a minimal global coupling sector has been written in parent-action language and its local variation/no-Hom consequences are explicit. It is still conditional because the whole corpus has not yet adopted this packet as the final parent action.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4017 - Kappa Sector Parent Insertion"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: a candidate parent coupling packet is now explicit: `Q_parent := Q_dyn x K_G`, `kappa_* in K_G`, and `S_parent=S_MTS_dyn+(1/(2*kappa_*)) int R[e_obs(q(Phi))] dmu_obs+S_matter+S_EM`.
- Local variation route: variations are along `TQ_dyn x {{0}}`, so `delta_local kappa_*=0`; no local `E_kappa`, `Theta_kappa`, or scalar-kappa fifth force is generated by this packet.
- No-Hom route: if `Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range,K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0`, then source/range/domain/memory derivatives of `G_ref` vanish conditionally.
- Calibration: `G_ref=c^4*kappa_*/(8*pi)` is a same-branch universal constant calibration, not a numerical prediction of `G`.
- Residual fallback: unsigned clauses feed `C_sector`, `C_local_scalar`, `C_noHom`, `C_Gref_kappa`, `D_t lnG`, `alpha(lambda)`, source derivative and exchange rows.
- No claim: packet is coherent and constructive but not yet the final parent action; local GR still needs second-order PPN source stability.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4017 - Kappa Sector Parent Insertion" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    packet: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4017_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4017_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, packet_id in enumerate(
        ["KSP4017_0_config", "KSP4017_1_action", "KSP4017_2_calibration", "KSP4017_3_noHom", "KSP4017_4_variation", "KSP4017_5_status"],
        start=2,
    ):
        add(f"VAL4017_{idx:02d}_packet", any(row["packet_id"] == packet_id for row in packet), f"{packet_id} present")
    for idx, theorem_id in enumerate(
        [
            "KVT4017_0_local_variation_zero",
            "KVT4017_1_EH_coefficient_lock",
            "KVT4017_2_noHom_derivative_zero",
            "KVT4017_3_branch_constant_not_absolute_prediction",
            "KVT4017_4_not_enough_for_local_GR",
            "KVT4017_5_residual_runner_fallback",
        ],
        start=8,
    ):
        add(f"VAL4017_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, audit_id in enumerate(
        ["KIA4017_0_packet_coherence", "KIA4017_1_parent_adoption", "KIA4017_3_noHom_signed", "KIA4017_5_numeric_G", "KIA4017_6_local_GR"],
        start=14,
    ):
        add(f"VAL4017_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    for idx, runner_id in enumerate(
        ["GRR4017_0_C_sector", "GRR4017_1_C_local_scalar", "GRR4017_2_C_noHom", "GRR4017_3_C_Gref_kappa", "GRR4017_4_Gdot", "GRR4017_5_range", "GRR4017_8_PPN_handoff"],
        start=19,
    ):
        add(f"VAL4017_{idx:02d}_runner", any(row["runner_id"] == runner_id for row in runner), f"{runner_id} present")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4017_26_clean_case", result_lookup["CASE4017_0_packet_adopted_clean"]["owner_status"] == "CONDITIONAL_KAPPA_SECTOR_INSERTION_LOCK", "clean packet case locks conditionally")
    add("VAL4017_27_not_adopted_case", result_lookup["CASE4017_1_packet_coherent_not_adopted"]["owner_status"] == "KAPPA_PACKET_NOT_ADOPTED", "not-adopted case remains blocked")
    add("VAL4017_28_scalar_case", "D_t_lnG" in result_lookup["CASE4017_2_local_scalar_reentry"]["residual_result"], "local scalar case activates Gdot")
    add("VAL4017_29_noHom_case", "partial_lambda_lnG" in result_lookup["CASE4017_3_noHom_fails"]["residual_result"], "no-Hom failure activates range/source rows")
    add("VAL4017_30_absolute_G_guard", result_lookup["CASE4017_5_absolute_G_overclaim"]["owner_status"] == "ABSOLUTE_G_OVERCLAIM_REJECTED", "absolute G overclaim rejected")
    add("VAL4017_31_local_GR_guard", result_lookup["CASE4017_6_local_GR_overclaim"]["owner_status"] == "LOCAL_GR_OVERCLAIM_REJECTED", "local GR overclaim rejected")
    add("VAL4017_32_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4017_33_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4017_34_doc_exists", DOC_PATH.exists() and "Candidate parent-sector packet" in read_text(DOC_PATH), "document written with insertion packet")
    add("VAL4017_35_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4017_36_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4017_37_compile", compile_ok, "script compiles")
    add("VAL4017_38_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        packet,
        theorem,
        audit,
        runner,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4017_39_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4017_40_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4017_41_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4017_42_calibration_not_prediction", "does **not** claim the numerical value of `G`" in read_text(DOC_PATH), "numerical G not claimed")
    add("VAL4017_43_ppn_handoff", "second-order PPN source-stability" in read_text(OUTPUTS["next"]), "PPN handoff recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    packet = packet_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    runner = runner_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["packet"], packet)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, packet, theorem, audit, runner, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4017 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
