from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1987-Y5-R2FR-first-residual-component-fill-selector.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1987_VALIDATION.csv"

SOURCES = {
    "1986_doc": {
        "path": ROOT / "1986-Y5-R2FR-memory-route-finite-residual-vector-pack.md",
        "needles": ["DEC1986_2_best_next", "RC1986_3_action_weight"],
    },
    "1986_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1986_VALIDATION.csv",
        "needles": ["VAL1986_OVERALL", "PASS"],
    },
    "1986_catalog": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1986_RESIDUAL_COMPONENT_CATALOG.csv",
        "needles": ["RC1986_3_action_weight", "FIRST_FILL_READY_VALUES_MISSING"],
    },
    "1387_action_weight": {
        "path": ROOT / "1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md",
        "needles": ["AWE1387_7_verdict", "DWB1387_4_beta_product_guard"],
    },
    "1027_qbar": {
        "path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["BQT1027_3_total_abs_guard", "DEC1027_2_coupling_status"],
    },
    "1685_connectedness": {
        "path": ROOT / "1685-Y5-R2FR-qbar-source-weight-intake-runner-or-matter-category-connectedness-proof.md",
        "needles": ["MCC1685_5_verdict", "PROOF_NOT_CLOSED"],
    },
    "1687_bound_contract": {
        "path": ROOT / "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md",
        "needles": ["BND1687_5_verdict", "BOUND_CONTRACT_READY_INPUTS_MISSING_NONCLAIM"],
    },
    "1920_delta_rows": {
        "path": ROOT / "1920-Y5-R2FR-source-weight-parent-current-owner-or-delta-w-first-rows.md",
        "needles": ["SWP1920_5_verdict", "DWA1920_0_WEP_TiPt"],
    },
    "1934_wep_bound": {
        "path": ROOT / "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md",
        "needles": ["WEP1934_0_MICROSCOPE_TiPt_eta", "REQ1934_0_projection_map"],
    },
    "1936_universality": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_4_verdict", "HIL1936_2_no_species_weight"],
    },
    "1936_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1936_VALIDATION.csv",
        "needles": ["VAL1936_OVERALL", "PASS"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_SOURCE_REGISTER.csv",
    "selector": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_COMPONENT_SELECTOR.csv",
    "selected_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_SELECTED_COMPONENT_CONTRACT.csv",
    "theorem_route": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_DERIVATION_ATTACK_PLAN.csv",
    "fallback": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_FINITE_BOUND_FALLBACK.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1987_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "FIRST_RESIDUAL_COMPONENT_SELECTOR_1987_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1987_ACTION_WEIGHT_SOURCE_BETA_FIRST_FILL_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "1987 first residual component selector",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    selector = [
        row(
            {
                "selector_id": "SEL1987_0_action_weight",
                "component_id": "RC1986_3_action_weight",
                "component": "Delta_w_abs;beta_w_source_abs;beta_w_test_abs",
                "selection_status": "SELECTED_FIRST_FILL",
                "physics_leverage": "highest: source universality, WEP, Newton measured-G, R10 scalar exchange, PPN and local-GR all touch this seam",
                "derivation_readiness": "conditional Hilbert/universal-source theorem already sharp in 1936; action-weight counterexample explicit in 1387",
                "finite_bound_readiness": "DWB1387 and DWA1920 rows already define source-beta and Delta_w first-fill schemas",
                "closure_risk": "medium: still needs parent signature, but the finite fallback is narrow and nonclaim",
                "score_100": "94",
                "reason": "best first target because it converts the coupling gap into either a theorem-zero source signature or a finite source-beta row",
            }
        ),
        row(
            {
                "selector_id": "SEL1987_1_qbar_XT",
                "component_id": "RC1986_1_beta",
                "component": "qbar_XT_abs source/test coupling envelope",
                "selection_status": "RESERVE_SECOND",
                "physics_leverage": "very high: direct source/test coupling and common fifth-force leakage",
                "derivation_readiness": "conditional chain-rule theorem exists, but q-kernel, observed coframe, markers, and hidden tails remain unsigned together",
                "finite_bound_readiness": "BQT1027 total absolute guard exists, but component values are still mostly placeholders",
                "closure_risk": "high: too many parent clauses can hide closure if attacked first",
                "score_100": "88",
                "reason": "keep as second target after action-weight/source-beta because it needs more parent machinery before a clean fill",
            }
        ),
        row(
            {
                "selector_id": "SEL1987_2_boundary",
                "component_id": "RC1986_2_boundary",
                "component": "Phi_boundary_abs",
                "selection_status": "RESERVE",
                "physics_leverage": "high for local projection and source silence",
                "derivation_readiness": "boundary-zero rows exist, but edge/domain/projector ownership remains scattered",
                "finite_bound_readiness": "not yet: needs local projection kernel and source support convention",
                "closure_risk": "high: easy to bury residuals as boundary conditions",
                "score_100": "72",
                "reason": "important, but not the cleanest first strike",
            }
        ),
        row(
            {
                "selector_id": "SEL1987_3_measured_GM",
                "component_id": "RC1986_5_measured_GM",
                "component": "GM_source_norm_abs",
                "selection_status": "RESERVE",
                "physics_leverage": "high for Newton/orbital reduction",
                "derivation_readiness": "1012 has the residual row, but source-normalization owner remains open",
                "finite_bound_readiness": "requires measured-G convention and calibration body map",
                "closure_risk": "medium-high: measured calibration can hide nonuniversal source weights",
                "score_100": "67",
                "reason": "do after action-weight, because GM absorption is only legal once source weights are known universal",
            }
        ),
        row(
            {
                "selector_id": "SEL1987_4_kernel_projection",
                "component_id": "RC1986_7_kernel_projection",
                "component": "K_alpha_abs;K_PPN_abs;K_clock_abs;K_orbital_abs",
                "selection_status": "RESERVE",
                "physics_leverage": "needed for tests, but not the root coupling derivation",
                "derivation_readiness": "1033/1034 expose missing kernel normalizations",
                "finite_bound_readiness": "blocked until selected residual has real coefficient rows",
                "closure_risk": "medium: can become pure data plumbing without theory ownership",
                "score_100": "61",
                "reason": "use once the selected coupling residual has a theorem-zero or finite value",
            }
        ),
        row(
            {
                "selector_id": "SEL1987_5_Jc",
                "component_id": "RC1986_0_Jc",
                "component": "J_c_abs canonical memory source",
                "selection_status": "RESERVE_LATER",
                "physics_leverage": "maximal but too broad",
                "derivation_readiness": "requires all source channels, boundary silence, and parent current ownership at once",
                "finite_bound_readiness": "none: source decomposition still needs channel-by-channel owner rows",
                "closure_risk": "very high: attacking the top source first risks restating the whole programme",
                "score_100": "52",
                "reason": "not a good first fill because it is the whole beast, not one exposed rib",
            }
        ),
    ]

    selected_contract = [
        row(
            {
                "contract_id": "CON1987_0_selected_component",
                "selected_component": "RC1986_3_action_weight",
                "symbol_block": "Delta_w_A; beta_w_source; beta_w_test; beta_w_source*beta_w_test",
                "definition": "pre-variation matter/source action weights and their canonical field-dependence after source/test split",
                "theorem_zero_condition": "single parent-signed Hilbert source action with no independent species/material/source multiplier and no readout re-entry",
                "finite_bound_condition": "if theorem-zero fails, every source/test/material weight gets units, source path, normalization, and absolute no-cancellation envelope",
                "observable_links": "WEP/MICROSCOPE;R10;Newton measured-G;PPN;clock;orbital;local_GR",
                "claim_status": "NONCLAIM_SELECTED_FOR_FILL",
            }
        ),
        row(
            {
                "contract_id": "CON1987_1_zero_formula",
                "selected_component": "RC1986_3_action_weight",
                "symbol_block": "Delta_w_A=0; beta_w_source=0; beta_w_test=0",
                "definition": "universal Hilbert coupling removes relative action/source weights and derivative source charges",
                "theorem_zero_condition": "S_matter=sum_A S_A[Psi_A,e_obs,theta_A] with one measure/current owner, no w_A slot, Lie_X e_obs=0, Lie_X theta_A=0",
                "finite_bound_condition": "not applicable if parent signature is actually proved",
                "observable_links": "would remove action-weight contribution to WEP/R10/Newton/PPN/local residual vector",
                "claim_status": "CONDITIONAL_ONLY_NOT_PARENT_SIGNED",
            }
        ),
        row(
            {
                "contract_id": "CON1987_2_finite_formula",
                "selected_component": "RC1986_3_action_weight",
                "symbol_block": "alpha_w(lambda); eta_w; DeltaGM_w",
                "definition": "finite source-weight effect if relative or field-dependent weights survive",
                "theorem_zero_condition": "failed or unsigned parent no-source-weight theorem",
                "finite_bound_condition": "alpha_w(lambda)=K_w(lambda)*abs(beta_w_source*beta_w_test)+epsilon_tail_abs; eta_w=abs(P_WEP*Delta_w_AB)+tail_abs",
                "observable_links": "R10 alpha(lambda); MICROSCOPE eta; Newton GM; PPN source residual",
                "claim_status": "FORMULA_READY_VALUES_MISSING",
            }
        ),
    ]

    theorem_route = [
        row(
            {
                "route_id": "THM1987_0_single_observed_frame",
                "required_clause": "all ordinary matter sees the same observed metric/coframe e_obs",
                "why_needed": "prevents frame-dependent source weights from re-entering as a common Weyl/disformal coupling",
                "current_status": "MISSING_PARENT_SIGNATURE",
                "if_signed": "supports Delta_w_A=0 for ordinary matter",
                "if_unsigned": "retain qbar_geom/source-weight residual",
            }
        ),
        row(
            {
                "route_id": "THM1987_1_single_hilbert_source_owner",
                "required_clause": "the gravitational source is the Hilbert variation of the same matter action used for inertial dynamics",
                "why_needed": "blocks a second source current that can carry hidden weights",
                "current_status": "MISSING_COMMON_CURRENT_OWNER",
                "if_signed": "one source normalization for all ordinary sectors",
                "if_unsigned": "Delta_w_A remains a live finite residual",
            }
        ),
        row(
            {
                "route_id": "THM1987_2_no_species_weight_slot",
                "required_clause": "parent object language contains no independent w_A or kappa_A species/source multiplier",
                "why_needed": "kills the exact 1387 counterexample rather than assuming it away",
                "current_status": "MISSING_NO_SOURCE_WEIGHT_THEOREM",
                "if_signed": "relative source weights vanish before arena projection",
                "if_unsigned": "finite material/source coefficient ledger required",
            }
        ),
        row(
            {
                "route_id": "THM1987_3_derivative_silence",
                "required_clause": "vertical/memory generator does not act on e_obs, theta_A, masses, EM constants, or material markers",
                "why_needed": "beta_w_source and beta_w_test must be zero, not merely common",
                "current_status": "MISSING_MARKER_AND_READOUT_SILENCE",
                "if_signed": "beta_w_source=beta_w_test=0",
                "if_unsigned": "R10/clock/WEP source-beta rows remain live",
            }
        ),
        row(
            {
                "route_id": "THM1987_4_boundary_readout_preservation",
                "required_clause": "projection, boundary, and readout maps preserve the no-weight/no-marker clauses",
                "why_needed": "prevents a zero in the parent bulk from reappearing at the local readout",
                "current_status": "MISSING_PRESERVATION_THEOREM",
                "if_signed": "selected action-weight residual can be promoted toward theorem-zero",
                "if_unsigned": "retain Phi_boundary and arena transfer tails",
            }
        ),
        row(
            {
                "route_id": "THM1987_5_current_verdict",
                "required_clause": "all THM1987_0 through THM1987_4 are parent-signed together",
                "why_needed": "local GR/Newton require source universality, not isolated conditional lemmas",
                "current_status": "THEOREM_TARGET_NOT_CLOSED",
                "if_signed": "RC1986_3 can move from finite residual to theorem-zero candidate",
                "if_unsigned": "1988 must fill finite action-weight/source-beta rows",
            }
        ),
    ]

    fallback = [
        row(
            {
                "fallback_id": "FB1987_0_common_factor",
                "quantity": "w_*",
                "required_input": "common action/source normalization and derivative silence",
                "units": "dimensionless",
                "formula": "T_eff=w_* sum_A T_A; absorbable into measured G only if common and derivative-silent",
                "status": "MISSING_COMMON_ACTION_NORMALIZATION",
            }
        ),
        row(
            {
                "fallback_id": "FB1987_1_relative_weight",
                "quantity": "Delta_w_A",
                "required_input": "source/material class A, reference class, uncertainty, source path, no-calibration-hiding rule",
                "units": "dimensionless",
                "formula": "Delta_w_A := w_A/w_* - 1",
                "status": "SOURCE_READY_SCHEMA_VALUES_MISSING",
            }
        ),
        row(
            {
                "fallback_id": "FB1987_2_source_beta",
                "quantity": "beta_w_source",
                "required_input": "canonical field normalization and source weight function w_source(phi)",
                "units": "canonical inverse-field or declared dimensionless convention",
                "formula": "beta_w,S := partial_phi ln w_S(phi)",
                "status": "MISSING_SOURCE_BETA_WEIGHT_FUNCTION",
            }
        ),
        row(
            {
                "fallback_id": "FB1987_3_test_beta",
                "quantity": "beta_w_test",
                "required_input": "test material action map and canonical field convention",
                "units": "same beta convention as source",
                "formula": "beta_w,T := partial_phi ln w_T(phi)",
                "status": "MISSING_TEST_BETA_WEIGHT_FUNCTION",
            }
        ),
        row(
            {
                "fallback_id": "FB1987_4_product_guard",
                "quantity": "alpha_w(lambda)",
                "required_input": "K_w(lambda), beta_w_source, beta_w_test, epsilon_tail_abs, alpha_bound(lambda)",
                "units": "dimensionless alpha",
                "formula": "alpha_w(lambda)=K_w(lambda)*abs(beta_w,S*beta_w,T)+epsilon_tail_abs",
                "status": "PRODUCT_FORMULA_READY_VALUES_MISSING",
            }
        ),
        row(
            {
                "fallback_id": "FB1987_5_wep_transfer",
                "quantity": "eta_w_AB",
                "required_input": "P_WEP, Delta_w_AB, material charges, tau_WEP, Earth/source environment",
                "units": "dimensionless eta",
                "formula": "eta_w_AB <= abs(P_WEP*Delta_w_AB)+tail_abs",
                "status": "REAL_MICROSCOPE_BOUND_EXISTS_MTS_PROJECTION_MISSING",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1987_0_component_selected",
                "claim": "first residual component selected",
                "status": "PASS_NONCLAIM",
                "reason": "RC1986_3_action_weight is selected as the first fill target",
            }
        ),
        row(
            {
                "gate_id": "CG1987_1_theorem_zero",
                "claim": "Delta_w and beta_w are theorem-zero",
                "status": "FAIL_BLOCKED",
                "reason": "parent single-metric Hilbert source, no species weight, derivative silence, and readout preservation are unsigned together",
            }
        ),
        row(
            {
                "gate_id": "CG1987_2_finite_bound",
                "claim": "finite source-beta/action-weight row can be scored",
                "status": "FAIL_BLOCKED",
                "reason": "Delta_w_A, beta_w_source, beta_w_test, K_w, tau_WEP, and arena projection values remain missing",
            }
        ),
        row(
            {
                "gate_id": "CG1987_3_local_GR_Newton",
                "claim": "local GR/Newton source coupling is derived",
                "status": "FAIL_BLOCKED",
                "reason": "source universality remains conditional and cannot be absorbed into measured G unless relative weights vanish",
            }
        ),
        row(
            {
                "gate_id": "CG1987_4_empirical_pass",
                "claim": "R10/WEP/PPN/clock/orbital comparison can pass",
                "status": "FAIL_BLOCKED",
                "reason": "selector has no numeric MTS prediction rows and no claim-grade bound comparison",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1987_0_selection",
                "decision": "SELECT_RC1986_3_ACTION_WEIGHT",
                "because": "it is the narrowest high-leverage coupling gap with both a theorem route and a finite-row fallback already staged",
                "next_action": "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
            }
        ),
        row(
            {
                "decision_id": "DEC1987_1_no_circling",
                "decision": "DO_NOT_WIDEN_SCHEMA_AGAIN",
                "because": "1986 already made the residual vector; progress now means filling or killing one component",
                "next_action": "attempt parent Hilbert/no-source-weight proof first; if it fails, fill the finite Delta_w/beta_w row",
            }
        ),
        row(
            {
                "decision_id": "DEC1987_2_claim_status",
                "decision": "NO_LOCAL_GR_OR_TEST_CLAIM",
                "because": "selecting the coupling component is a work-order, not evidence that it is zero or bounded",
                "next_action": "keep all claim flags false until theorem-zero or source-backed finite rows exist",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1987_0_primary",
                "selection_status": "selected",
                "target_doc": "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
                "target_script": "scripts/Y5_R2FR_action_weight_source_beta_theorem_or_finite_row_fill_1988.py",
                "task": "try to prove the parent Hilbert/no-source-weight/derivative-silence theorem for RC1986_3; if it cannot be signed, create the first finite Delta_w/beta_w source row with units and source paths",
                "success_condition": "one selected component becomes theorem-zero candidate or nonclaim finite-bound row; no local-GR/Newton/R10/WEP claim is made",
                "do_not": "do not widen the residual vector, invent coefficients, set tau=1 by choice, absorb nonuniversal weights into measured G, or modify formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1987_0_selector_record",
                "artifact_type": "source_weight_component_selection",
                "selected_component": "RC1986_3_action_weight",
                "status": "NONCLAIM_WORK_ORDER",
                "source_path": str(DOC_PATH),
                "next_target": "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1987_0_action_weight_source_beta",
                "priority": "1",
                "component": "RC1986_3_action_weight",
                "needed_rows": "Delta_w_A;beta_w_source;beta_w_test;K_w(lambda);tau_WEP;P_WEP;epsilon_tail_abs",
                "first_action": "attempt theorem-zero from parent Hilbert source coupling and no species/source-weight slot",
                "fallback_action": "fill finite source-beta row with source paths and units",
                "blocked_claims": "local_GR;Newton;R10;WEP;PPN;clock;orbital",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "selector": selector,
        "selected_contract": selected_contract,
        "theorem_route": theorem_route,
        "fallback": fallback,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val(
        "VAL1987_00_sources",
        "PASS" if not source_failures else "FAIL",
        "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures),
    )

    selected = [row for row in tables["selector"] if row["selection_status"] == "SELECTED_FIRST_FILL"]
    val(
        "VAL1987_01_exactly_one_selected",
        "PASS" if len(selected) == 1 and selected[0]["component_id"] == "RC1986_3_action_weight" else "FAIL",
        "RC1986_3_action_weight selected as first fill component",
    )

    contract_text = "\n".join(str(row) for row in tables["selected_contract"])
    has_theorem = "theorem_zero_condition" in contract_text and "Delta_w_A=0" in contract_text
    has_fallback = "alpha_w(lambda)=K_w(lambda)*abs(beta_w_source*beta_w_test)+epsilon_tail_abs" in contract_text
    val(
        "VAL1987_02_contract_routes",
        "PASS" if has_theorem and has_fallback else "FAIL",
        "selected contract has theorem-zero route and finite-bound fallback",
    )

    theorem_verdict = tables["theorem_route"][-1]["current_status"] == "THEOREM_TARGET_NOT_CLOSED"
    val(
        "VAL1987_03_theorem_not_promoted",
        "PASS" if theorem_verdict else "FAIL",
        "theorem route remains target only, not a derived claim",
    )

    fallback_ready = any(row["fallback_id"] == "FB1987_4_product_guard" and "VALUES_MISSING" in row["status"] for row in tables["fallback"])
    val(
        "VAL1987_04_fallback_nonclaim",
        "PASS" if fallback_ready else "FAIL",
        "finite source-beta fallback is formula-ready but values missing",
    )

    gates_safe = all(row["status"] in {"PASS_NONCLAIM", "FAIL_BLOCKED"} for row in tables["claim_gate"])
    no_claim_gate_pass = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"])
    val(
        "VAL1987_05_claim_gates",
        "PASS" if gates_safe and no_claim_gate_pass else "FAIL",
        "all claim gates blocked except nonclaim component selection",
    )

    next_ok = tables["next"][0]["target_doc"] == "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md"
    val("VAL1987_06_next_target", "PASS" if next_ok else "FAIL", "1988 action-weight/source-beta fill target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1987_07_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1987_08_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1987_09_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1987*")]
    val(
        "VAL1987_10_formalization_untouched",
        "PASS" if not formalization_artifacts else "FAIL",
        f"formalization_1987_artifact_count={len(formalization_artifacts)}",
    )

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1987_OVERALL", overall, "1987 first residual component fill selector")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Component Selector", tables["selector"]),
        ("Selected Component Contract", tables["selected_contract"]),
        ("Derivation Attack Plan", tables["theorem_route"]),
        ("Finite Bound Fallback", tables["fallback"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1987 Y5 R2FR: First Residual Component Fill Selector",
        "",
        "Private checkpoint. This is the anti-circling step after 1986: choose one residual component to attack rather than widening the local-GR residual vector again.",
        "",
        "Verdict: select `RC1986_3_action_weight` as the first fill target. This is the clean coupling seam: either a parent Hilbert/no-source-weight/derivative-silence theorem kills `Delta_w_A`, `beta_w_source`, and `beta_w_test`, or those quantities become explicit finite source-beta rows with units, source paths, and no-cancellation guards.",
        "",
        "No local-GR, Newton, R10, WEP, PPN, clock, orbital, or public claim follows from 1987. The result is a work-order: attack the coupling/source-weight component first.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1987_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
