from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4018"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4018-Y5-R2FR-second-order-PPN-source-stability-or-gamma-beta-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4018_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4018_SECOND_ORDER_PPN_STABILITY_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4018_PPN_SOURCE_STABILITY_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4018_GAMMA_BETA_SOURCE_RESIDUAL_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4018_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4018_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4018_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4018_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4018_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4018_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4018_VALIDATION.csv",
}

NEXT_DOC = "4019-Y5-R2FR-EH-only-R11-no-extra-operator-adoption-or-PPN-residual-scorer.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4019_EH_only_R11_no_extra_operator_adoption_or_PPN_residual_scorer.py"


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
        ("SRC4018_00_handoff", SRC / "P8_Y5_R2FR_4017_NEXT_TARGET.csv", "NEXT4017_0", "4017 handoff"),
        ("SRC4018_01_4017_not_full_GR", SRC / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv", "KVT4017_4_not_enough_for_local_GR", "coupling lock not local GR"),
        ("SRC4018_02_4017_ppn_runner", SRC / "P8_Y5_R2FR_4017_GREF_RESIDUAL_RUNNER_ROWS.csv", "GRR4017_8_PPN_handoff", "PPN handoff row"),
        ("SRC4018_03_3624_contract", SRC / "P8_Y5_R2FR_3624_MINIMAL_LOCAL_GR_CONTRACT.csv", "LGC3624_4_ppn_completion", "minimal PPN/local-GR completion contract"),
        ("SRC4018_04_3624_gate_gamma", SRC / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv", "NPG3624_3_gamma", "gamma completion gate"),
        ("SRC4018_05_3624_gate_beta", SRC / "P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv", "NPG3624_4_beta", "beta completion gate"),
        ("SRC4018_06_3625_gamma", SRC / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv", "ENV3625_0_gamma", "gamma envelope"),
        ("SRC4018_07_3625_beta", SRC / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv", "ENV3625_1_beta", "beta envelope"),
        ("SRC4018_08_3625_total", SRC / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv", "ENV3625_6_total", "total PPN envelope"),
        ("SRC4018_09_3626_gamma", SRC / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv", "PCF3626_0_gamma", "gamma component row"),
        ("SRC4018_10_3626_beta", SRC / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv", "PCF3626_1_beta", "beta component row"),
        ("SRC4018_11_3626_total", SRC / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv", "PCF3626_6_total", "total component row"),
        ("SRC4018_12_3885_target", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_0_target", "conditional GR PPN target"),
        ("SRC4018_13_3885_gamma", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_1_gamma", "gamma condition"),
        ("SRC4018_14_3885_beta", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_2_beta", "beta condition"),
        ("SRC4018_15_3885_pref", SRC / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv", "PPT3885_3_preferred_frame", "preferred-frame condition"),
        ("SRC4018_16_3915_zero_gamma", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_0_gamma", "conditional gamma zero"),
        ("SRC4018_17_3915_zero_beta", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_1_beta", "conditional beta zero"),
        ("SRC4018_18_3915_zero_total", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_8_total", "conditional full PPN zero"),
        ("SRC4018_19_3915_res_gamma", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_0_gamma", "executable gamma residual"),
        ("SRC4018_20_3915_res_beta", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_1_beta", "executable beta residual"),
        ("SRC4018_21_3915_res_total", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "executable total residual"),
        ("SRC4018_22_3988_source_formula", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv", "JPPN3988_0_Hilbert_formula", "Hilbert source formula"),
        ("SRC4018_23_3988_ppn_env", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv", "JPPN3988_3_PPN_envelope", "PPN source stability envelope"),
        ("SRC4018_24_3988_ppn_bound", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv", "JPPNB3988_2_PPN_total", "PPN total source bound"),
        ("SRC4018_25_3988_beta_bound", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv", "JPPNB3988_12_Delta_beta_total_abs", "beta bound component"),
        ("SRC4018_26_3991_direct_beta", SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_SCHEMA.csv", "BSE3991_0_direct_beta", "direct source beta evaluator"),
        ("SRC4018_27_3991_envelope", SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_SCHEMA.csv", "BSE3991_1_3990_envelope", "no-Hom beta envelope"),
        ("SRC4018_28_3991_results", SRC / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_RESULTS.csv", "CASE3991_0_parent_theorem_zero", "parent theorem-zero beta case"),
        ("SRC4018_29_3954_source_norm", SRC / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv", "PPN3954_8_total_source_norm", "source normalization residual map"),
        ("SRC4018_30_template_gamma", SRC / "MTS_local_residual_predictions_TEMPLATE.csv", "R3_gamma", "gamma prediction template"),
        ("SRC4018_31_template_beta", SRC / "MTS_local_residual_predictions_TEMPLATE.csv", "R4_beta", "beta prediction template"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "PPN4018_0_metric_expansion_lock",
            "standard PPN expansion fixed",
            "g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6); g_ij=delta_ij(1+2 gamma U/c^2)+O(c^-4); first-order source normalization fixes A_source before beta is read",
            "prevents moving second-order errors into the first-order Newton calibration",
            "EXACT_DEFINITION_LOCK",
        ),
        (
            "PPN4018_1_gamma_EH_zero",
            "gamma zero condition",
            "If the local reduced metric operator is EH-only through O(U), the observed coframe/readout is the same for g_00 and g_ij, and no R11/q_loc/projector spatial stress survives, then Psi=Phi and gamma-1=0",
            "gamma can be zeroed only by same-branch EH/readout/no-extra-stress, not by Poisson alone",
            "EXACT_CONDITIONAL_GAMMA_THEOREM",
        ),
        (
            "PPN4018_2_beta_square_law",
            "source-normalized beta law",
            "Let A_source be the coefficient of U in g_00 after Hilbert-source normalization and B_source the coefficient of U^2; beta_eff=B_source/A_source^2 and delta_beta_source=B_source/A_source^2-1",
            "local GR requires B_source=A_source^2; first-order GM calibration cannot absorb a second-order beta error",
            "EXACT_SOURCE_NORMALIZED_BETA_LAW",
        ),
        (
            "PPN4018_3_beta_EH_zero",
            "beta zero condition",
            "If EH nonlinear completion is the only O(U^2) operator, the K_G coupling packet is same-branch, Pi_M/H_tau source equality holds, source prefactors are absent, and readout/boundary/R11 terms vanish, then beta-1=0",
            "the beta route is constructive but depends on source-current origin and no-extra-operator gates",
            "EXACT_CONDITIONAL_BETA_THEOREM",
        ),
        (
            "PPN4018_4_preferred_frame_conservation",
            "remaining local-GR PPN vector",
            "No independent local vector/domain/coframe/memory marker through O(U^2) gives alpha1=alpha2=alpha3=xi=0; total Hilbert stress plus Bianchi closure gives zeta_i=0",
            "gamma and beta are necessary but not the whole PPN claim",
            "EXACT_CONDITIONAL_FULL_PPN_VECTOR_THEOREM",
        ),
        (
            "PPN4018_5_no_cancellation_firewall",
            "PPN no-cancellation rule",
            "Delta_PPN_abs is an absolute-sum vector; no component may be hidden by an opposite-sign component or absorbed into measured GM after the first-order source normalization",
            "keeps the Mayweather route fair: close each round, do not win by bookkeeping tricks",
            "ANTI_TUNING_GUARD",
        ),
        (
            "PPN4018_6_finite_residual_vector",
            "finite fallback if theorem is unsigned",
            "epsilon_PPN_2nd_4018 <= |delta_gamma_EH|+|delta_gamma_R11|+|delta_gamma_readout|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|",
            "unsigned PPN clauses become executable residual rows rather than local-GR claims",
            "FINITE_PPN_SOURCE_STABILITY_VECTOR_NONCLAIM",
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
        ("PPA4018_0_first_order_normalization", "A_source fixed by 4015 Newton/Gauss/Hilbert source before beta readout", "CONDITIONAL_4015_4012", "beta can be backfilled by measured GM", "retain delta_beta_source if source equality is not signed"),
        ("PPA4018_1_EH_only_second_order", "no extra O(U^2) operator beyond EH nonlinear completion", "CONDITIONAL_NOT_FINAL", "beta/gamma shifted by R11/q_loc/operator tails", "prove EH-only/R11 no-extra operator or retain residuals"),
        ("PPA4018_2_same_readout_frame", "same observed coframe/frame/gauge used for temporal and spatial potentials", "CONDITIONAL", "gamma/readout mismatch", "retain gamma_readout/frame rows"),
        ("PPA4018_3_source_current_origin", "Hilbert source current comes from descended matter+EM action with no source prefactors", "CONDITIONAL_3988", "source-normalized beta and WEP/source charge leak", "retain source-current origin vector"),
        ("PPA4018_4_boundary_domain", "boundary/domain/projector/preferred-frame sectors vanish or are bounded", "OPEN", "alpha_i, xi, zeta_i and beta boundary residuals survive", "keep full PPN vector live"),
        ("PPA4018_5_KG_packet", "4017 K_G packet is same-branch and does not re-enter at O(U^2)", "CANDIDATE_PACKET_ONLY", "constant coupling not enough for local GR", "feed C_Gref_kappa/Gdot rows into PPN vector if unsigned"),
        ("PPA4018_6_claim_firewall", "Newton/gamma/beta partial success is not local-GR promotion", "LOCKED", "public/local-GR overclaim", "require all PPN vector components zero/bounded independently"),
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


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PPR4018_0_master", "epsilon_PPN_2nd_4018", "|delta_gamma_EH|+|delta_gamma_R11|+|delta_gamma_readout|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|", "MISSING_PARENT_SIGNATURES_OR_COMPONENT_VALUES", "dimensionless envelope", "full second-order PPN/source-stability vector", "local_GR; PPN"),
        ("PPR4018_1_gamma", "gamma_minus_1", "delta_gamma_EH+delta_gamma_R11+delta_gamma_readout+delta_gamma_frame+delta_gamma_source", "ZERO_IF_EH_ONLY_SAME_READOUT_NO_EXTRA_SPATIAL_STRESS_ELSE_RETAIN", "dimensionless", "spatial curvature per unit Newtonian potential", "Cassini/gamma; local_GR"),
        ("PPR4018_2_A_source", "A_source", "first-order coefficient of U in g_00 after Hilbert-source normalization", "FIXED_BY_4015_NEWTON_SOURCE_LOCK_ELSE_NO_BETA_SCORE", "dimensionless", "first-order source normalization", "Newton; PPN"),
        ("PPR4018_3_B_source", "B_source", "second-order coefficient paired with U^2 in g_00", "EH_COMPLETION_REQUIRES_B_SOURCE_EQUALS_A_SOURCE_SQUARED", "dimensionless", "second-order source response", "beta; local_GR"),
        ("PPR4018_4_delta_beta_source", "delta_beta_source", "B_source/A_source^2 - 1 plus source-normalization residue epsilon_SN", "ZERO_IF_B_SOURCE_EQUALS_A_SOURCE_SQUARED_AND_EPSILON_SN_ZERO_ELSE_RETAIN", "dimensionless", "source-normalized nonlinear residue", "beta; LLR/perihelion"),
        ("PPR4018_5_beta_total", "beta_minus_1", "delta_beta_source+delta_beta_R11+delta_beta_q_loc+delta_beta_boundary_domain+delta_beta_readout+delta_beta_gauge", "ZERO_IF_ALL_SECOND_ORDER_COMPONENTS_ZERO_ELSE_BOUND_AGAINST_7.8e-05", "dimensionless", "PPN beta total", "beta; local_GR"),
        ("PPR4018_6_preferred_frame", "alpha1_alpha2_alpha3_xi", "|alpha1|+|alpha2|+|alpha3|+|xi| from vector/domain/coframe/memory selectors", "ZERO_IF_NO_VECTOR_DOMAIN_MEMORY_MARKER_ELSE_RETAIN", "dimensionless vector", "preferred-frame/location vector", "PPN; local_GR"),
        ("PPR4018_7_conservation", "zeta_i", "stress nonconservation/non-Hilbert leakage projection", "ZERO_IF_TOTAL_HILBERT_STRESS_AND_BIANCHI_CLOSURE_ELSE_RETAIN", "dimensionless vector", "PPN conservation vector", "PPN; local_GR"),
        ("PPR4018_8_Gdot", "Gdot_over_G", "D_t ln G_ref in local branch after K_G packet", "ZERO_IF_4017_PACKET_ADOPTED_ELSE_RETAIN", "yr^-1", "local coupling drift contribution", "Gdot; PPN"),
        ("PPR4018_9_claim_gate", "Delta_PPN_abs", "absolute sum of all PPN components with no cancellation", "PASS_ONLY_IF_EACH_COMPONENT_THEOREM_ZERO_OR_NUMERIC_BOUND_PASS", "dimensionless envelope", "local-GR promotion firewall", "local_GR"),
    ]
    return [
        {
            "row_id": row_id,
            "coefficient": coefficient,
            "formula": formula,
            "value": value,
            "units": units,
            "role": role,
            "observable_links": links,
            "status": "FINITE_NONCLAIM_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, coefficient, formula, value, units, role, links in rows
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    cases = [
        ("CASE4018_0_full_EH_source_PPN_signed", True, True, True, True, True, True, True, False, False, "all second-order EH/source/readout/preferred-frame clauses signed"),
        ("CASE4018_1_gamma_only", True, True, False, True, False, False, True, False, False, "gamma locks but beta/full vector do not"),
        ("CASE4018_2_beta_square_law_open", True, True, False, True, False, False, True, False, False, "A_source/B_source square law not signed"),
        ("CASE4018_3_R11_operator_tail", False, False, False, True, False, False, True, False, False, "extra R11/q_loc/operator tail survives"),
        ("CASE4018_4_source_prefactor_open", True, True, True, False, False, False, True, False, False, "source current origin or source-prefactor gate open"),
        ("CASE4018_5_preferred_frame_open", True, True, True, True, False, False, True, False, False, "gamma/beta close but alpha_i/xi/zeta vector remains open"),
        ("CASE4018_6_Newton_overclaim", True, False, False, True, False, False, True, True, False, "tries to promote Newton/Gauss to local GR"),
        ("CASE4018_7_cancellation_attempt", True, True, False, True, True, True, True, False, True, "tries to cancel beta/gamma/vector components"),
        ("CASE4018_8_numeric_runner_pack", False, False, False, False, False, False, False, False, False, "residual rows exist but no sourced numeric/theorem inputs"),
    ]
    return [
        {
            "case_id": case_id,
            "EH_only": eh_only,
            "gamma_zero": gamma_zero,
            "beta_square": beta_square,
            "source_origin": source_origin,
            "preferred_frame_closed": preferred,
            "conservation_closed": conservation,
            "KG_packet": kg_packet,
            "newton_overclaim": newton_overclaim,
            "cancellation_attempt": cancellation_attempt,
            "description": description,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for case_id, eh_only, gamma_zero, beta_square, source_origin, preferred, conservation, kg_packet, newton_overclaim, cancellation_attempt, description in cases
    ]


def truthy(row: dict[str, Any], key: str) -> bool:
    return str(row[key]).lower() == "true" if isinstance(row[key], str) else bool(row[key])


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cases:
        if truthy(row, "newton_overclaim"):
            owner = "NEWTON_TO_LOCAL_GR_OVERCLAIM_REJECTED"
            residual = "gamma_beta_full_PPN_vector_required"
            claim = "NO_LOCAL_GR_PROMOTION"
            action = "keep Newton/Gauss as first-order only until full PPN vector closes"
        elif truthy(row, "cancellation_attempt"):
            owner = "PPN_CANCELLATION_REJECTED"
            residual = "Delta_PPN_abs_no_cancellation"
            claim = "NO_PPN_PASS"
            action = "absolute-sum each component; no opposite-sign cancellation"
        elif not truthy(row, "EH_only"):
            owner = "PPN_EH_ONLY_BLOCKED"
            residual = "delta_gamma_R11+delta_beta_R11+delta_beta_q_loc"
            claim = "NO_GAMMA_BETA_CLAIM"
            action = "derive EH-only/no-extra-operator branch or retain R11/q_loc PPN residuals"
        elif not truthy(row, "gamma_zero"):
            owner = "GAMMA_GATE_BLOCKED"
            residual = "gamma_minus_1"
            claim = "NO_LOCAL_GR_CLAIM"
            action = "close same-readout spatial curvature theorem or score gamma bound"
        elif not truthy(row, "beta_square"):
            owner = "BETA_SOURCE_STABILITY_BLOCKED"
            residual = "delta_beta_source+beta_minus_1"
            claim = "NO_BETA_OR_LOCAL_GR_CLAIM"
            action = "prove B_source=A_source^2 after source normalization or fill beta residuals"
        elif not truthy(row, "source_origin"):
            owner = "SOURCE_CURRENT_ORIGIN_BLOCKED"
            residual = "epsilon_parent_JH_origin+delta_beta_source"
            claim = "NO_SOURCE_NORMALIZED_PPN_CLAIM"
            action = "close Hilbert source-current origin/no-source-prefactor gate"
        elif not truthy(row, "preferred_frame_closed") or not truthy(row, "conservation_closed"):
            owner = "FULL_PPN_VECTOR_BLOCKED"
            residual = "alpha_i+xi+zeta_i"
            claim = "NO_LOCAL_GR_PROMOTION"
            action = "close preferred-frame/conservation rows after gamma/beta"
        elif row["case_id"] == "CASE4018_0_full_EH_source_PPN_signed":
            owner = "CONDITIONAL_LOCAL_GR_PPN_LOCK"
            residual = "GAMMA_BETA_ALPHA_XI_ZETA_ZERO_IF_ALL_PARENT_GATES_SIGNED"
            claim = "LOCAL_GR_CONDITIONAL_ONLY_NOT_PUBLIC_CLAIM"
            action = "next adopt/check EH-only R11 no-extra operator branch against residual scorer"
        else:
            owner = "PPN_RUNNER_NONCLAIM"
            residual = "FULL_PPN_SOURCE_STABILITY_VECTOR_REQUIRED"
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
        ("DEC4018_0_square_law", "make beta a source-normalized square-law test", "B_source=A_source^2 is the non-smuggled bridge from Newton to beta", "prevents measured-GM absorption of O(U^2) errors"),
        ("DEC4018_1_gamma_not_enough", "reject gamma-only or Newton-only promotion", "local GR needs beta and the full PPN vector, not just Poisson or gamma", "claim firewall remains active"),
        ("DEC4018_2_conditional_route", "retain exact conditional EH PPN theorem", "EH-only through O(U^2) plus same source/readout gives gamma=beta=1 and zero preferred-frame/conservation rows", "constructive route exists"),
        ("DEC4018_3_runner", "emit full residual runner rows", "current corpus has packet/source/R11 clauses still conditional, so every PPN component remains explicit", "no hidden closure assumption"),
        ("DEC4018_4_next", f"move to {NEXT_DOC}", "the next hard gate is adopting/proving EH-only R11/no-extra operator or running the PPN residual scorer", "pushes theorem branch toward testability"),
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
        ("CLAIM4018_0_gamma", "gamma=1 claimed", False, "conditional unless EH-only/readout/no-extra spatial stress is parent-signed"),
        ("CLAIM4018_1_beta", "beta=1 claimed", False, "conditional unless B_source=A_source^2 and all second-order residuals close"),
        ("CLAIM4018_2_full_PPN", "full PPN vector pass", False, "preferred-frame/conservation/source rows remain conditional/nonclaim"),
        ("CLAIM4018_3_local_GR", "local GR recovery", False, "requires 4019 EH-only/R11 operator adoption or residual scorer pass"),
        ("CLAIM4018_4_public", "public claim", False, "private theorem/runner checkpoint only"),
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
            "row_id": "NEXT4018_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "attempt to adopt/prove the EH-only R11/no-extra-operator branch through O(U^2), or run the PPN residual scorer with explicit gamma/beta/source rows",
            "success_condition": "R11/q_loc/operator/readout/source residuals are zero by theorem or mapped into executable gamma/beta/preferred-frame/conservation bound rows with no cancellation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Second-order PPN source-stability gate derived: gamma route, beta square-law B_source=A_source^2, full PPN residual vector and no-cancellation firewall recorded.",
            "claim_allowed": False,
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["needle_found"])
    lines = [
        "# 4018 - Second-Order PPN Source Stability Or Gamma/Beta Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint makes the local-GR gate explicit: Newton/Gauss is first order; local GR needs the second-order PPN vector.",
        "",
        "PPN frame:",
        "",
        "`g_00=-1+2U/c^2-2 beta U^2/c^4+O(c^-6)`",
        "",
        "`g_ij=delta_ij(1+2 gamma U/c^2)+O(c^-4)`.",
        "",
        "The non-smuggled beta test is:",
        "",
        "`beta_eff = B_source/A_source^2`",
        "",
        "`delta_beta_source = B_source/A_source^2 - 1`.",
        "",
        "So once `A_source` is fixed by the Newton/Gauss/Hilbert source bridge, the second-order coefficient must obey `B_source=A_source^2`. Otherwise beta fails even if the Newtonian limit looked fine.",
        "",
        "## Conditional Local-GR Route",
        "",
        "If the local reduced action is EH-only through `O(U^2)`, the 4017 `K_G` packet is same-branch, `Pi_M/H_tau` source equality holds, source prefactors are absent, and R11/q_loc/readout/boundary/projector tails vanish, then the GR PPN vector follows conditionally:",
        "",
        "`gamma=1`, `beta=1`, `alpha1=alpha2=alpha3=xi=zeta_i=0`.",
        "",
        "## Finite PPN Vector",
        "",
        "`epsilon_PPN_2nd_4018 <= |delta_gamma_EH|+|delta_gamma_R11|+|delta_gamma_readout|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|`.",
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
            "This is a necessary tightening. We now have a real conditional local-GR route, but also the exact firewall: gamma-only or Newton-only is not enough, and beta cannot be repaired by fitted GM. Current status remains nonclaim until the EH-only/R11/no-extra-operator branch is adopted or all residuals are scored.",
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
    marker = "## 4018 - Second-Order PPN Source Stability"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: local-GR recovery is now guarded by the second-order PPN frame `g_00=-1+2U/c^2-2 beta U^2/c^4`, `g_ij=delta_ij(1+2 gamma U/c^2)`.
- Gamma route: EH-only same-readout spatial/temporal potentials plus no R11/q_loc/projector spatial stress gives `gamma-1=0` conditionally.
- Beta route: after first-order Newton source normalization, `beta_eff=B_source/A_source^2`; local GR requires `B_source=A_source^2`, so beta cannot be fixed by measured-GM absorption.
- Full PPN route: no independent vector/domain/coframe/memory marker gives `alpha1=alpha2=alpha3=xi=0`; total Hilbert stress plus Bianchi closure gives `zeta_i=0`.
- Finite fallback: `epsilon_PPN_2nd_4018 <= |delta_gamma_EH|+|delta_gamma_R11|+|delta_gamma_readout|+|delta_beta_source|+|delta_beta_R11|+|delta_beta_q_loc|+|delta_beta_boundary|+|delta_beta_readout|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|Gdot/G|`.
- No claim: Newton/gamma/beta partial wins do not promote local GR; all components need theorem-zero or independent numeric bounds.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4018 - Second-Order PPN Source Stability" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4018_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4018_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "PPN4018_0_metric_expansion_lock",
            "PPN4018_1_gamma_EH_zero",
            "PPN4018_2_beta_square_law",
            "PPN4018_3_beta_EH_zero",
            "PPN4018_4_preferred_frame_conservation",
            "PPN4018_5_no_cancellation_firewall",
            "PPN4018_6_finite_residual_vector",
        ],
        start=2,
    ):
        add(f"VAL4018_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, audit_id in enumerate(
        [
            "PPA4018_0_first_order_normalization",
            "PPA4018_1_EH_only_second_order",
            "PPA4018_3_source_current_origin",
            "PPA4018_5_KG_packet",
            "PPA4018_6_claim_firewall",
        ],
        start=9,
    ):
        add(f"VAL4018_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    master = next(row for row in finite if row["row_id"] == "PPR4018_0_master")
    add("VAL4018_14_master_vector", "delta_beta_source" in master["formula"] and "alpha3" in master["formula"], "master vector contains beta and full PPN guards")
    for idx, row_id in enumerate(
        [
            "PPR4018_1_gamma",
            "PPR4018_2_A_source",
            "PPR4018_3_B_source",
            "PPR4018_4_delta_beta_source",
            "PPR4018_5_beta_total",
            "PPR4018_6_preferred_frame",
            "PPR4018_7_conservation",
            "PPR4018_8_Gdot",
            "PPR4018_9_claim_gate",
        ],
        start=15,
    ):
        add(f"VAL4018_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    lookup = {row["case_id"]: row for row in results}
    add("VAL4018_24_full_case", lookup["CASE4018_0_full_EH_source_PPN_signed"]["owner_status"] == "CONDITIONAL_LOCAL_GR_PPN_LOCK", "full conditional local-GR PPN case locks")
    add("VAL4018_25_gamma_only", lookup["CASE4018_1_gamma_only"]["owner_status"] == "BETA_SOURCE_STABILITY_BLOCKED", "gamma-only blocked by beta")
    add("VAL4018_26_beta_square", "delta_beta_source" in lookup["CASE4018_2_beta_square_law_open"]["residual_result"], "beta square-law failure routed")
    add("VAL4018_27_R11_tail", "delta_gamma_R11" in lookup["CASE4018_3_R11_operator_tail"]["residual_result"], "R11/operator tail routed")
    add("VAL4018_28_source_prefactor", "epsilon_parent_JH_origin" in lookup["CASE4018_4_source_prefactor_open"]["residual_result"], "source-current origin failure routed")
    add("VAL4018_29_preferred_frame", "alpha_i" in lookup["CASE4018_5_preferred_frame_open"]["residual_result"], "preferred-frame vector failure routed")
    add("VAL4018_30_newton_overclaim", lookup["CASE4018_6_Newton_overclaim"]["owner_status"] == "NEWTON_TO_LOCAL_GR_OVERCLAIM_REJECTED", "Newton overclaim rejected")
    add("VAL4018_31_cancellation", lookup["CASE4018_7_cancellation_attempt"]["owner_status"] == "PPN_CANCELLATION_REJECTED", "PPN cancellation rejected")
    add("VAL4018_32_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4018_33_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4018_34_doc_exists", DOC_PATH.exists() and "B_source=A_source^2" in read_text(DOC_PATH), "document written with beta square law")
    add("VAL4018_35_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4018_36_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4018_37_compile", compile_ok, "script compiles")
    add("VAL4018_38_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        theorem,
        audit,
        finite,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4018_39_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4018_40_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4018_41_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4018_42_gamma_not_enough", "gamma-only or Newton-only is not enough" in read_text(DOC_PATH), "gamma/Newton overclaim firewall recorded")
    add("VAL4018_43_ppn_next", "EH-only R11/no-extra-operator" in read_text(OUTPUTS["next"]), "EH-only/R11 next target recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
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

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4018 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
