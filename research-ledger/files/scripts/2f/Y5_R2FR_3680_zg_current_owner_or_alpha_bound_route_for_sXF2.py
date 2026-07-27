from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3680"
BRANCH_ID = "MTS_R2FR_Y5_ZG_CURRENT_OWNER_OR_ALPHA_BOUND_ROUTE_FOR_SXF2_3680"
DOC = ROOT / "3680-Y5-R2FR-zg-current-owner-or-alpha-bound-route-for-sXF2.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def parse_float(value: object) -> float:
    return float(str(value).strip())


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3679", RESIDUALS / "P8_Y5_R2FR_3679_NEXT_TARGET.csv", "z_g=0", "3679 selected z_g current owner or alpha bound route"),
        ("map_3679", RESIDUALS / "P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv", "z_g = D_Xhat ln g_J", "canonical identity between z_g, s_XF2 and b_alpha_X"),
        ("bounds_3679", RESIDUALS / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv", "SXF23679_2_alpha_clock_route", "3679 alpha route remained blocked by z_g owner"),
        ("gate_3507", RESIDUALS / "P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv", "GATE3507_0_same_parent_owner", "same parent owner gate for kinetic/current normalization"),
        ("source_theorem_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv", "SCT3650_2_beta_zero_law", "conditional beta/source-current zero law"),
        ("source_audit_3650", RESIDUALS / "P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv", "SCA3650_6_total", "charge-current closure remains unsigned"),
        ("current_theorem_1814", RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv", "VCC1814_2_current_variation", "visible connection/current owner theorem"),
        ("current_audit_1814", RESIDUALS / "P8_Y5_PARENT_QLOC_1814_CURRENT_OWNER_AUDIT.csv", "COA1814_2_no_current_rescale", "current rescaling countermodel survives"),
        ("no_rescale_1815", RESIDUALS / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv", "NCR1815_0_target", "post-current rescale theorem contract"),
        ("post_pre_1815", RESIDUALS / "P8_Y5_PARENT_QLOC_1815_POST_PRE_RESCALE_SPLIT_AUDIT.csv", "PPR1815_2_pre_action_weight", "pre-action weights survive current owner"),
        ("readout_order_1816", RESIDUALS / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv", "VBR1816_0_target", "variation-before-readout theorem contract"),
        ("selector_order_1816", RESIDUALS / "P8_Y5_PARENT_QLOC_1816_SOURCE_SELECTOR_ORDER_AUDIT.csv", "SSO1816_6_verdict", "readout/source selector order still fails current zero proof"),
        ("tq_1100", RESIDUALS / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv", "TQT1100_1_compact_U1_limit", "compact U(1) fixes labels but not coupling normalization"),
        ("ward_1101", RESIDUALS / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv", "GFT1101_2_Ward_limit", "Ward current owner limit"),
        ("alpha_clock_1052", RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "source-backed clock product bound, not standalone b_alpha"),
        ("alpha_wep_1052", RESIDUALS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha projection product target"),
        ("alpha_req_1098", RESIDUALS / "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv", "REQ1098_0_c_alpha", "DD alpha coefficient threshold"),
        ("alpha_source_runner_3508", RESIDUALS / "P8_EM_alpha_source_bound_runner_results.csv", "ASRUN3508_0_z_g_alpha", "old alpha-source runner explicitly blocks z_g without sourced rows"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def prior_values() -> dict[str, float]:
    bound_rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv")
    by_id = {row["bound_id"]: row for row in bound_rows}
    clock_rows = load_csv(RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv")
    clock = {row["bound_id"]: row for row in clock_rows}
    wep_rows = load_csv(RESIDUALS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv")
    wep = {row["projection_id"]: row for row in wep_rows}
    req_rows = load_csv(RESIDUALS / "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv")
    req = {row["requirement_id"]: row for row in req_rows}
    return {
        "sxf2_o1_budget": parse_float(by_id["SXF23679_0_equal_budget_O1"]["bound_or_value"]),
        "sxf2_4pi_budget": parse_float(by_id["SXF23679_1_equal_budget_4pi"]["bound_or_value"]),
        "clock_best_product_1sigma": parse_float(clock["ACB1052_2"]["product_bound_1sigma_yr_inv"]),
        "clock_best_product_2sigma": parse_float(clock["ACB1052_2"]["product_bound_2sigma_yr_inv"]),
        "clock_h0_normalized": parse_float(clock["ACB1052_2"]["H0_normalized_diagnostic"]),
        "wep_alpha_product_target": parse_float(wep["AWP1052_0_alpha_Coulomb"]["required_abs_beta_source_max"]),
        "wep_eta_bound": parse_float(wep["AWP1052_0_alpha_Coulomb"]["eta_bound"]),
        "dd_alpha_threshold": parse_float(req["REQ1098_0_c_alpha"]["threshold_abs"]),
    }


def zero_theorem_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZG3680_0_target",
            "z_g=0 current-normalization theorem",
            "z_g = D_Xhat ln g_J vanishes for the measured current/source normalization used in alpha_eff",
            "TARGET_NOT_PROVED",
            "would make s_XF2=-b_alpha_X and let alpha/clock/WEP routes hit the Maxwell kinetic residual directly",
            "continue through owner clauses",
        ),
        (
            "ZG3680_1_compact_lattice",
            "fixed representation charge labels",
            "D_Xhat ln n_A=0 for integer/representation weights once the T_Q lattice is parent-owned",
            "PARTIAL_SUPPORT_ONLY",
            "compact U(1) helps with relative labels but not the continuous current unit or Maxwell kinetic normalization",
            "retain base-unit and current-owner terms",
        ),
        (
            "ZG3680_2_noether_current_owner",
            "same Noether current owner",
            "J_Q := delta S_matter/delta A_Q^vis with A_Q^vis and charge labels supplied by the same parent connection/generator",
            "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "Ward/Noether conservation can define the current form, but not the calibration amplitude unless owner/readout clauses sign",
            "retain z_Noether/current normalization component",
        ),
        (
            "ZG3680_3_post_current_rescale",
            "post-variation c_A current rescale",
            "after source extraction, J_A -> c_A J_A is harmless only if readout is strictly downstream and no source-current slot exists",
            "KILLED_CONDITIONALLY_NOT_PARENT_SIGNED",
            "1815/1816 narrow this loophole but do not close it for the current corpus",
            "retain z_cA_post component",
        ),
        (
            "ZG3680_4_pre_action_weight",
            "pre-variation action/source weight",
            "S_matter=sum_A w_A S_A before variation is inherited by Hilbert/Noether currents",
            "SURVIVES_CURRENT_OWNER",
            "this is mostly a source/WEP/Newton coupling leg, not a direct alpha spectroscopy leg, but it blocks source-calibration claims",
            "retain z_Delta_w/source-weight component",
        ),
        (
            "ZG3680_5_readout_worldtube_transfer",
            "source/readout/worldtube transfer",
            "K_arena[J_Q] must be fixed downstream with no support, boundary, normalization or effective-action reentry",
            "MISSING_ARENA_TRANSFER_KERNEL",
            "arena data can otherwise see a different current than the parent variation current",
            "retain transfer component and source-backed row requirement",
        ),
        (
            "ZG3680_6_ward_limit",
            "Ward identity alone",
            "nabla_mu J_Q^mu=0",
            "CONSERVATION_NOT_CALIBRATION",
            "conservation survives current rescaling and does not fix alpha/current normalization by itself",
            "do not use Ward identity as z_g zero proof",
        ),
        (
            "ZG3680_7_verdict",
            "current corpus proves z_g=0",
            "ZG3680_1 through ZG3680_6 all close with common parent normalization and readout order",
            "THEOREM_NOT_PROVED_RETAIN_TWO_KNOB_ROUTE",
            "z_g=0 is not claimed; b_alpha_X=2 z_g-s_XF2 must remain a two-knob identity",
            "build bound rows for both z_g and s_XF2",
        ),
    ]
    return [
        {
            **base(ts),
            "zero_id": zero_id,
            "clause": clause,
            "required_signature": required_signature,
            "current_status": current_status,
            "consequence": consequence,
            "next_action": next_action,
            "source_signed": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for zero_id, clause, required_signature, current_status, consequence, next_action in specs
    ]


def zg_decomposition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZGD3680_0_definition",
            "z_g",
            "z_g = D_Xhat ln g_J",
            "canonical current/source normalization derivative entering b_alpha_X",
            "MISSING_ZERO_OR_NUMERIC_BOUND",
            "dimensionless canonical derivative",
        ),
        (
            "ZGD3680_1_core_decomposition",
            "z_g_core,A",
            "z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A",
            "direct alpha/current normalization leg before WEP/source extras",
            "NO_CANCELLATION_COMPONENTS_UNFILLED",
            "dimensionless canonical derivative",
        ),
        (
            "ZGD3680_2_lattice_term",
            "z_lattice,A",
            "z_lattice,A = D_Xhat ln n_A",
            "integer charge/representation labels; conditionally zero if fixed parent T_Q lattice is signed",
            "PARTIAL_ZERO_ONLY_IF_TQ_LATTICE_SIGNED",
            "dimensionless canonical derivative",
        ),
        (
            "ZGD3680_3_noether_term",
            "z_Noether,A",
            "z_Noether,A = D_Xhat ln Z_JA",
            "Noether current normalization and matter-field/source measure normalization",
            "MISSING_PARENT_CURRENT_OWNER_OR_BOUND",
            "dimensionless canonical derivative",
        ),
        (
            "ZGD3680_4_post_current_term",
            "z_cA_post,A",
            "z_cA_post,A = D_Xhat ln c_A",
            "post-variation current/source-test transfer if readout order is unsigned",
            "MISSING_READOUT_ORDER_THEOREM_OR_C_A_BOUND",
            "dimensionless current fraction",
        ),
        (
            "ZGD3680_5_readout_term",
            "z_readout,A",
            "z_readout,A = D_Xhat ln R_A",
            "spectroscopy/source readout normalization; zero only if pure downstream fixed readout",
            "MISSING_READOUT_TRANSFER_KERNEL_OR_BOUND",
            "dimensionless transfer fraction",
        ),
        (
            "ZGD3680_6_source_arena_extension",
            "z_source,A",
            "z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A",
            "WEP/R10/Newton source arenas see extra pre-action/source-worldtube/non-Hilbert pieces beyond direct alpha current normalization",
            "SOURCE_ARENA_EXTENSION_LIVE",
            "dimensionless projected source coupling",
        ),
        (
            "ZGD3680_7_two_knob_identity",
            "b_alpha_X",
            "b_alpha_X = 2 z_g - s_XF2",
            "fine-structure residual constrains a difference, not s_XF2 alone",
            "DERIVED_IDENTITY_RETAINED",
            "dimensionless canonical derivative",
        ),
    ]
    return [
        {
            **base(ts),
            "component_id": component_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "current_status": current_status,
            "units": units,
            "numeric_value": "MISSING_COMPONENT_VALUE",
            "source_path_or_row": "see source register",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for component_id, symbol, formula, meaning, current_status, units in specs
    ]


def two_knob_bound_rows(ts: str) -> list[dict[str, object]]:
    values = prior_values()
    specs = [
        (
            "TKB3680_0_identity",
            "b_alpha_X",
            "b_alpha_X = 2 z_g - s_XF2",
            "identity",
            "alpha evidence hits a two-knob vector unless z_g=0 is proved",
            "DERIVED_IDENTITY_NONCLAIM",
            "none",
            "not a bound",
        ),
        (
            "TKB3680_1_sXF2_budget_O1",
            "abs(s_XF2)",
            f"{values['sxf2_o1_budget']:.12e}",
            "dimensionless canonical transfer",
            "3679/3678 equal-component target under |g_FXR|<=1",
            "PRIVATE_TARGET_NOT_EVIDENCE",
            str(RESIDUALS / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv"),
            "target budget only",
        ),
        (
            "TKB3680_2_sXF2_budget_4pi",
            "abs(s_XF2)",
            f"{values['sxf2_4pi_budget']:.12e}",
            "dimensionless canonical transfer",
            "3679/3678 equal-component target under |g_FXR|<=4pi",
            "PRIVATE_TARGET_NOT_EVIDENCE",
            str(RESIDUALS / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv"),
            "target budget only",
        ),
        (
            "TKB3680_3_clock_product",
            "abs((2 z_g - s_XF2) * tau_clock)",
            f"{values['clock_best_product_1sigma']:.12e}",
            "yr^-1",
            "best local clock product row ACB1052_2",
            "SOURCE_BACKED_PRODUCT_NOT_STANDALONE_COEFFICIENT",
            str(RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"),
            "requires tau_clock and shared Xhat normalization before scoring z_g/s_XF2",
        ),
        (
            "TKB3680_4_clock_if_tau_known",
            "abs(2 z_g - s_XF2)",
            "B_clock/abs(tau_clock)",
            "dimensionless canonical derivative",
            "algebraic conversion of clock product if tau_clock is derived",
            "FORMULA_READY_INPUTS_MISSING",
            "MISSING_TAU_CLOCK_XHAT_SOURCE_PATH",
            "not score-ready until tau_clock is sourced",
        ),
        (
            "TKB3680_5_direct_if_zg_zero",
            "abs(s_XF2)",
            "B_clock/abs(tau_clock)",
            "dimensionless canonical transfer",
            "direct alpha-clock route if parent proves z_g=0",
            "CONDITIONAL_ON_ZG_ZERO_AND_TAU_CLOCK",
            "MISSING_ZG_ZERO_THEOREM_AND_TAU_CLOCK",
            "this is the clean win route, but both inputs are missing",
        ),
        (
            "TKB3680_6_if_zg_bounded",
            "abs(s_XF2)",
            "B_alpha + 2*B_zg",
            "dimensionless canonical transfer",
            "two-knob triangle bound if alpha and z_g bounds are both sourced",
            "FORMULA_READY_INPUTS_MISSING",
            "MISSING_B_ALPHA_AND_B_ZG_SOURCE_ROWS",
            "keeps the current-normalization ambiguity explicit",
        ),
        (
            "TKB3680_7_wep_alpha_projection",
            "abs(P_WEP_alpha)",
            f"{values['wep_alpha_product_target']:.12e}",
            "dimensionless",
            "MICROSCOPE alpha/Coulomb projection target AWP1052_0",
            "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION",
            str(RESIDUALS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"),
            "requires beta_source_alpha, tau_WEP and material/source map",
        ),
        (
            "TKB3680_8_dd_alpha_threshold",
            "abs(c_alpha_DD or b_alpha)",
            f"{values['dd_alpha_threshold']:.12e}",
            "dimensionless",
            "DD alpha coefficient threshold REQ1098_0",
            "SOURCE_BACKED_THRESHOLD_NO_MTS_COEFFICIENT",
            str(RESIDUALS / "P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv"),
            "requires a parent-owned c_alpha or theorem-zero",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "route": route,
            "status": status,
            "source_path_or_missing": source_path_or_missing,
            "interpretation": interpretation,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, route, status, source_path_or_missing, interpretation in specs
    ]


def source_arena_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "SAR3680_0_clock",
            "clock/spectroscopy",
            "b_alpha_X = 2 z_g - s_XF2",
            "tau_clock",
            "clock product bound exists, but tau_clock/Xhat map is not derived",
            "MISSING_TAU_CLOCK_XHAT",
        ),
        (
            "SAR3680_1_wep",
            "MICROSCOPE/WEP",
            "beta_source_alpha,A*(2 z_g - s_XF2) plus z_source,A tails",
            "tau_WEP/material tensor/source map",
            "projection target exists, but beta/source/material map is missing",
            "MISSING_BETA_SOURCE_ALPHA_AND_MATERIAL_MAP",
        ),
        (
            "SAR3680_2_r10",
            "R10/short-range",
            "K_X Qbar_XH qbar_XT with alpha/source component rows",
            "tau_R10/lambda_X/source profile",
            "cannot reuse clock alpha bound without arena projection",
            "MISSING_R10_ALPHA_SOURCE_PROJECTION",
        ),
        (
            "SAR3680_3_ppn_newton",
            "PPN/Newton/source calibration",
            "z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A",
            "source-worldtube/GM calibration/PPN source vector",
            "pre-action weights and non-Hilbert bypass block GR/Newton source claims",
            "MISSING_SOURCE_UNIVERSALITY_VECTOR",
        ),
    ]
    return [
        {
            **base(ts),
            "arena_id": arena_id,
            "arena": arena,
            "observed_combination": observed_combination,
            "required_projection": required_projection,
            "current_result": current_result,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for arena_id, arena, observed_combination, required_projection, current_result, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3680_0_zg_zero",
            "z_g=0 is not derived",
            "THEOREM_NOT_PROVED",
            "Noether/Ward support exists, but compact charge labels and conservation do not fix the continuous current normalization or readout/source transfer.",
            "keep z_g live in b_alpha_X=2 z_g-s_XF2",
        ),
        (
            "DEC3680_1_real_progress",
            "z_g is no longer vague",
            "PROMOTED_TO_COMPONENT_VECTOR",
            "the current-normalization ambiguity is now split into lattice, Noether/current, post-current c_A, readout, pre-action weight, worldtube and non-Hilbert components.",
            "target components rather than restating the coupling problem",
        ),
        (
            "DEC3680_2_best_derivation_route",
            "variation-before-readout/order is the nearest derivation lever",
            "DERIVATION_FIRST",
            "1815/1816 show post-current c_A can be demoted if source extraction precedes readout and no source-current slot exists.",
            "attack post-current c_A/readout order or import a bound row",
        ),
        (
            "DEC3680_3_best_empirical_route",
            "alpha data must be used as a two-knob bound",
            "BOUND_ROUTE_READY_NOT_SCORE_READY",
            "clock and WEP product rows exist, but they require tau/projector/source maps and cannot be treated as standalone s_XF2 evidence.",
            "build two-knob runner only after tau_clock/tau_WEP or z_g bound exists",
        ),
        (
            "DEC3680_4_claim_discipline",
            "no local-GR/Maxwell/WEP/R10 claim",
            "PRIVATE_NONCLAIM",
            "3680 is a coupling-identity bridge, not a pass of any local arena.",
            "continue privately",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3680_0_zg_zero", "claim z_g=0", "BLOCKED_NONCLAIM", "current owner, readout order, no source slot and source transfer are not parent-signed"),
        ("CG3680_1_direct_sXF2_alpha", "treat alpha/clock as direct s_XF2 bound", "BLOCKED_ZG_LIVE", "b_alpha_X=2 z_g-s_XF2 remains two-knob"),
        ("CG3680_2_score_two_knob", "score z_g/s_XF2 two-knob runner", "BLOCKED_PROJECTIONS_MISSING", "tau_clock, tau_WEP, beta_source_alpha and arena source maps are missing"),
        ("CG3680_3_source_universality", "claim source-current universality/Newton source calibration", "BLOCKED_SOURCE_WEIGHTS", "pre-action weights, worldtube transfer and non-Hilbert bypass remain open"),
        ("CG3680_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    values = prior_values()
    return [
        {
            **base(ts),
            "status": "ZG_ZERO_NOT_PROVED_TWO_KNOB_ALPHA_SOURCE_ROUTE_FORMALIZED_NONCLAIM",
            "summary": "3680 bridges the older current-owner work into the 3679 s_XF2 throat. It does not prove z_g=0, but it decomposes z_g into explicit current/readout/source components and turns b_alpha_X=2 z_g-s_XF2 into an executable two-knob route.",
            "claim_ceiling": "no z_g zero, direct s_XF2 alpha bound, WEP/R10/source calibration, Maxwell/local-GR/Newton/PPN, or public claim is made",
            "useful_result": f"source-backed product targets exist: clock |(2 z_g-s_XF2) tau_clock| <= {values['clock_best_product_1sigma']:.12e} yr^-1 and WEP alpha target {values['wep_alpha_product_target']:.12e}; both remain nonclaim until tau/projection/source maps are derived",
            "next_missing_piece": "derive variation-before-readout/no-source-slot enough to kill z_cA_post, or source a finite z_g component bound before attempting the two-knob runner",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3680_0",
            "target_doc": "3681-Y5-R2FR-post-current-cA-readout-order-zero-or-zg-component-bound.md",
            "target_script": "scripts/Y5_R2FR_3681_post_current_cA_readout_order_zero_or_zg_component_bound.py",
            "objective": "derive enough variation-before-readout/no-source-slot structure to set the post-current z_cA_post component to zero, or source a finite post-current/readout-transfer z_g component bound",
            "success_gate": "z_cA_post is theorem-zero from parent readout order, or a source-backed nonclaim z_g component row exists with units, normalizer, source path and no-cancellation placement",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3680 - z_g current owner or alpha bound route for s_XF2",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint bridges the older current-owner work into the new `s_XF2` throat. The result is not `z_g=0`; the result is a sharper object: `z_g` is now a component vector, and alpha data is a two-knob constraint.",
        "",
        "## Main result",
        "",
        "`z_g = D_Xhat ln g_J` is **not proven zero**.",
        "",
        "The exact identity remains:",
        "",
        "`b_alpha_X = 2 z_g - s_XF2`.",
        "",
        "So clock/WEP/R10 alpha evidence cannot be used as direct `s_XF2` evidence until either `z_g=0` is parent-signed or `z_g` is separately bounded.",
        "",
        "The direct current leg is decomposed as:",
        "",
        "`z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A`.",
        "",
        "For source arenas the extension is:",
        "",
        "`z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A`.",
        "",
        "## z_g zero audit",
    ]
    for row in zero_rows:
        lines.append(f"- `{row['zero_id']}`: {row['current_status']} - {row['clause']} -> {row['consequence']}")
    lines.extend(["", "## Component decomposition"])
    for row in components:
        lines.append(f"- `{row['component_id']}`: {row['current_status']} - `{row['formula']}`")
    lines.extend(["", "## Two-knob bound route"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Source arena transfer"])
    for row in arenas:
        lines.append(f"- `{row['arena_id']}`: {row['status']} - {row['arena']} sees `{row['observed_combination']}` and needs {row['required_projection']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + zero_rows + components + bounds + arenas + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3680*", "3680-Y5-R2FR-*", "P8_Y5*3680*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    zero_statuses = {str(row["current_status"]) for row in zero_rows}
    component_formulas = " ".join(str(row["formula"]) for row in components)
    bound_by_id = {str(row["bound_id"]): row for row in bounds}

    add("VAL3680_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3680_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3680_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3680 outputs written")
    add("VAL3680_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3680_4_zg_not_zero", "THEOREM_NOT_PROVED_RETAIN_TWO_KNOB_ROUTE" in zero_statuses, "z_g zero theorem is not promoted")
    add("VAL3680_5_decomposition", "z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A" in component_formulas, "direct z_g component decomposition present")
    add("VAL3680_6_source_extension", "z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A" in component_formulas, "source arena extension present")
    add("VAL3680_7_two_knob_identity", any(row["bound_id"] == "TKB3680_0_identity" and "2 z_g - s_XF2" in row["bound_or_formula"] for row in bounds), "two-knob alpha identity retained")
    add("VAL3680_8_clock_bound_product", "TKB3680_3_clock_product" in bound_by_id and parse_float(bound_by_id["TKB3680_3_clock_product"]["bound_or_formula"]) > 0 and bound_by_id["TKB3680_3_clock_product"]["status"] == "SOURCE_BACKED_PRODUCT_NOT_STANDALONE_COEFFICIENT", "clock product bound imported as non-standalone coefficient")
    add("VAL3680_9_wep_bound_product", "TKB3680_7_wep_alpha_projection" in bound_by_id and parse_float(bound_by_id["TKB3680_7_wep_alpha_projection"]["bound_or_formula"]) > 0, "WEP alpha projection target imported")
    add("VAL3680_10_no_direct_alpha", any(row["claim_gate_id"] == "CG3680_1_direct_sXF2_alpha" and row["status"] == "BLOCKED_ZG_LIVE" for row in gates), "direct s_XF2 alpha interpretation blocked while z_g lives")
    add("VAL3680_11_arena_rows", {row["arena_id"] for row in arenas} == {"SAR3680_0_clock", "SAR3680_1_wep", "SAR3680_2_r10", "SAR3680_3_ppn_newton"}, "clock/WEP/R10/PPN arena transfer rows present")
    add("VAL3680_12_next_target", next_target[0]["target_doc"].startswith("3681-") and "z_cA_post" in next_target[0]["objective"], "3681 targets post-current cA/readout-order component")
    add("VAL3680_13_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3680_14_doc_written", "z_g_core,A" in doc_text and "b_alpha_X = 2 z_g - s_XF2" in doc_text and "not proven zero" in doc_text, "doc records z_g decomposition and two-knob route")
    add("VAL3680_15_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3680_16_no_formalization_leak", not leaks, "no 3680 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    zero_rows = zero_theorem_rows(ts)
    components = zg_decomposition_rows(ts)
    bounds = two_knob_bound_rows(ts)
    arenas = source_arena_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3680_SOURCE_REGISTER.csv",
        "zero": RESIDUALS / "P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv",
        "components": RESIDUALS / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3680_TWO_KNOB_ALPHA_BOUND_ROUTE_ROWS.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3680_SOURCE_ARENA_TRANSFER_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3680_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3680_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3680_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3680_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3680_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["zero"], zero_rows)
    write_csv(outputs["components"], components)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["arenas"], arenas)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, zero_rows, components, bounds, arenas, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, zero_rows, components, bounds, arenas, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3680 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3680 checkpoint: z_g zero not proved; two-knob alpha/source route formalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
