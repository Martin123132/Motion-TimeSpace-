from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3464-Y5-R2FR-canonical-action-normalization-from-MTS-primitives-or-WEP-effective-source-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3464": Path(__file__).resolve(),
    "doc_3463": ROOT / "3463-Y5-R2FR-single-source-current-owner-from-Noether-Poynting-flow-or-WEP-tau-map-under-AX1090.md",
    "audit_3463": OUT / "P8_Y5_R2FR_3463_SINGLE_SOURCE_CURRENT_AUDIT.csv",
    "em_3463": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
    "obstruction_3463": OUT / "P8_Y5_R2FR_3463_ACTION_NORMALIZATION_OBSTRUCTION.csv",
    "tau_3463": OUT / "P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv",
    "chain_3463": OUT / "P8_Y5_R2FR_3463_BOUND_CHAIN_UPDATE.csv",
    "doc_3462": ROOT / "3462-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-WEP-sY5-row-under-AX1090.md",
    "counter_3462": OUT / "P8_Y5_R2FR_3462_NO_GO_COUNTERMODEL.csv",
    "wep_3462": OUT / "P8_Y5_R2FR_3462_WEP_SY5_PRODUCT_ROW.csv",
    "normalization_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "action_1937": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
    "hilbert_1937": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
    "alpha_owner_1811": OUT / "P8_Y5_PARENT_QLOC_1811_ALPHA_OWNER_AUDIT.csv",
    "alpha_level_1812": OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
    "alpha_path_1930": OUT / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_PATH_DECISION.csv",
    "charge_current": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "charge_residuals": OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
    "charge_dependency_2339": OUT / "P8_Y5_PARENT_QLOC_2339_CHARGE_NORMALIZATION_DEPENDENCY.csv",
    "charge_spine_2340": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
    "dd_map_2441": OUT / "P8_Y5_PARENT_QLOC_2441_MTS_TO_DD_CHARGE_MAP.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [
            str(row.get(field, ""))
            .replace("\n", "<br>")
            .replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3464": "generator for this checkpoint",
        "doc_3463": "live source-current/Poynting normalization predecessor",
        "audit_3463": "single source-current audit rows",
        "em_3463": "Maxwell/Poynting source-current ledger",
        "obstruction_3463": "weighted-action obstruction rows",
        "tau_3463": "WEP tau/effective contrast derivation",
        "chain_3463": "live bound-chain update from 3463",
        "doc_3462": "no-source-only-slot obstruction predecessor",
        "counter_3462": "weighted descended action countermodel",
        "wep_3462": "first WEP s_Y5 product row",
        "normalization_stack": "source-normalization theorem stack",
        "ward_universality": "source-current Ward universality contract",
        "action_1937": "minimal parent matter action signature",
        "hilbert_1937": "conditional Hilbert source theorem",
        "alpha_owner_1811": "alpha_EM parent owner audit",
        "alpha_level_1812": "alpha level/fibre norm owner audit",
        "alpha_path_1930": "alpha product path decision",
        "charge_current": "charge-current equality attempt",
        "charge_residuals": "charge-current residual decomposition",
        "charge_dependency_2339": "charge normalization dependency rows",
        "charge_spine_2340": "parent charge extraction spine",
        "dd_map_2441": "MTS to Damour-Donoghue charge map",
        "local_bounds": "source-backed local empirical bound ledger",
    }
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def canonical_normalization_theorem_audit() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CAN3464_0_target",
            "statement": "No independent sector action scale w_A or w_EM survives in the local matter/EM source action.",
            "proof_attempt": "Derive from one parent action unit, one observed coframe/Hodge star, one Hilbert source current, and fixed measured matter/EM constants.",
            "result": "TARGET_EXACT",
            "meaning": "This is the exact theorem needed to turn the 1937 conditional Hilbert-source route into source-coupling closure.",
            "source_path": str(SOURCES["doc_3463"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_1_single_action_unit",
            "statement": "A single parent action phase/symplectic normalization forbids arbitrary relative sector multipliers.",
            "proof_attempt": "If all fields enter one parent variational principle and the relative action scale is observable through quantum/statistical weights, canonical commutators, or symplectic form, then w_A is not a gauge convention.",
            "result": "STRONG_CONDITIONAL",
            "meaning": "This kills the classical EOM loophole only if the quantum/action-unit normalization is parent-owned.",
            "source_path": str(SOURCES["charge_spine_2340"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_2_matter_kinetic_readout",
            "statement": "Matter sector normalizations are fixed by measured masses, charges, kinetic terms, and representation labels.",
            "proof_attempt": "Canonical field redefinitions may move a factor into theta_A, but then it becomes a measured matter parameter rather than a hidden gravitational source weight.",
            "result": "CONDITIONAL_CLASSIFICATION",
            "meaning": "Good classification, but not yet a parent theorem forbidding an inert source-only multiplier.",
            "source_path": str(SOURCES["action_1937"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_3_EM_alpha_owner",
            "statement": "The EM sector action scale is fixed by one Maxwell curvature norm plus charge/current/fine-structure ownership.",
            "proof_attempt": "Under A -> lambda A, the Maxwell kinetic scale and current charge rescale together; once charge units and alpha_EM=e^2/(4*pi*hbar*c) are owned, w_EM has no independent source meaning.",
            "result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "meaning": "This is the clean EM route, but alpha level owner, unique F^2, Hom exclusion, and readout/radiative closure are all unsigned.",
            "source_path": str(SOURCES["alpha_level_1812"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_4_hidden_Hom_exclusion",
            "statement": "Hidden/local MTS variables cannot map into sector action scales or F^2 coefficients.",
            "proof_attempt": "Forbid Hom(C_hidden,Coeff(S_A)) and Hom(C_hidden,Coeff(F^2)) except measured visible constants.",
            "result": "NOT_PARENT_DERIVED",
            "meaning": "Without this typed coefficient-domain theorem, hidden scalars can reopen b_alpha or w_A channels.",
            "source_path": str(SOURCES["alpha_owner_1811"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_5_preservation",
            "statement": "Renormalization, readout, projection, and boundary reductions preserve the no-sector-scale rule.",
            "proof_attempt": "Show loops/clocks/material readout do not regenerate source weights, alpha markers, or species/projector source charges.",
            "result": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "meaning": "Even a clean bare action is not enough unless the maps into experiments preserve it.",
            "source_path": str(SOURCES["alpha_path_1930"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CAN3464_6_verdict",
            "statement": "Current MTS derives canonical action/source normalization.",
            "proof_attempt": "Close CAN3464_1 through CAN3464_5 together.",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "meaning": "A serious conditional theorem is now written, but the parent primitive proof is still missing; finite WEP/alpha/source residual rows remain active.",
            "source_path": str(SOURCES["obstruction_3463"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def em_alpha_charge_owner_audit() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EAC3464_0_gauge_rescaling",
            "object": "Maxwell kinetic/current normalization redundancy",
            "formula": "A -> lambda A, e -> e/lambda can move normalization between F^2 and J.A",
            "status": "CLASSIFICATION_EXACT",
            "closure_needed": "fix charge/current normalization and alpha_EM in one parent convention",
            "source_path": str(SOURCES["em_3463"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EAC3464_1_alpha_level",
            "object": "fine-structure owner",
            "formula": "alpha_EM = e^2/(4*pi*hbar*c) in a fixed visible convention",
            "status": "OWNER_NOT_DERIVED",
            "closure_needed": "alpha_EM=alpha_*(ell_EM,g_*) plus Lie_v ell_EM=0 or equivalent parent level theorem",
            "source_path": str(SOURCES["alpha_level_1812"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EAC3464_2_unique_F2",
            "object": "unique Maxwell curvature norm",
            "formula": "no independent lambda(X) F_Q^2 or w_EM F^2 coefficient",
            "status": "UNIQUE_F2_NOT_CLOSED",
            "closure_needed": "typed coefficient-domain certificate or one-parent-curvature-norm theorem",
            "source_path": str(SOURCES["alpha_level_1812"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EAC3464_3_charge_current",
            "object": "charge/current owner",
            "formula": "J^mu and A_mu normalization must be owned before EM stress and material charges can be scored",
            "status": "PARENT_CHARGE_SPINE_EXISTS_VALUES_MISSING",
            "closure_needed": "parent charge extraction, fixed reference, source denominator, and residual charge silence",
            "source_path": str(SOURCES["charge_spine_2340"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EAC3464_4_DD_map",
            "object": "alpha/material WEP map",
            "formula": "D_e_source = S_E^q * b_alpha if alpha_EM(q)=alpha_0 exp(b_alpha q)",
            "status": "PARTIAL_MAP_SOURCE_LEG_MISSING",
            "closure_needed": "q normalization, Earth/source leg, b_mhat/nuclear sector, and no readout reentry",
            "source_path": str(SOURCES["dd_map_2441"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EAC3464_5_verdict",
            "object": "EM action normalization proof",
            "formula": "w_EM=0 as an independent source coefficient",
            "status": "NOT_DERIVED_BUT_NOW_LOCALIZED",
            "closure_needed": "alpha owner + unique F2 + charge-current owner + readout/radiative closure",
            "source_path": str(SOURCES["alpha_owner_1811"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def wep_effective_source_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "WEB3464_0_observable_definition",
            "quantity": "effective WEP source contrast",
            "formula": "eta_AB=2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)",
            "value_or_status": "EXACT_SMALL_MODEL_FORMULA",
            "units": "dimensionless",
            "source_path": str(SOURCES["tau_3463"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "WEB3464_1_linear_effective_contrast",
            "quantity": "Delta_w_eff_TiPt",
            "formula": "Delta_w_eff_AB := epsilon_A-epsilon_B, so eta_AB=Delta_w_eff_AB+O(epsilon^2)",
            "value_or_status": "DEFINED_EFFECTIVE_NOT_RAW_PARENT",
            "units": "dimensionless",
            "source_path": str(SOURCES["tau_3463"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "WEB3464_2_MICROSCOPE_bound",
            "quantity": "abs(Delta_w_eff_TiPt)",
            "formula": "|Delta_w_eff_TiPt| <= eta_TiPt_bound in the direct effective model",
            "value_or_status": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]),
            "source_row": "R1_WEP_source_charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "WEB3464_3_raw_parent_map",
            "quantity": "Delta_w_eff_TiPt(raw MTS)",
            "formula": "Delta_w_eff = tau_w Delta_w_raw + S_E^q b_alpha Delta_Q_alpha + S_E^q b_mhat Delta_Q_mhat + Delta_shadow + Delta_readout + O(epsilon^2)",
            "value_or_status": "MISSING_RAW_TO_EFFECTIVE_MAP",
            "units": "dimensionless",
            "source_path": str(SOURCES["dd_map_2441"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "WEB3464_4_no_claim_status",
            "quantity": "WEP branch",
            "formula": "score only a sourced/theorem-zero raw-to-effective map; otherwise retain |Delta_w_eff_TiPt| bound as an empirical ceiling",
            "value_or_status": "NONCLAIM_BOUND_READY_PREDICTION_MISSING",
            "units": "dimensionless",
            "source_path": str(SOURCES["wep_3462"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def raw_to_effective_requirements() -> list[dict[str, Any]]:
    return [
        {
            "req_id": "RTE3464_0_tau_w",
            "raw_component": "Delta_w_raw_TiPt",
            "needed_map": "tau_w from parent source coefficient to Eotvos acceleration contrast",
            "current_status": "MISSING_PARENT_TO_EOTVOS_PROJECTION",
            "acceptance": "derived tau_w with units/convention or theorem-zero Delta_w_raw",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "req_id": "RTE3464_1_b_alpha",
            "raw_component": "b_alpha",
            "needed_map": "S_E^q b_alpha Delta_Q_alpha contribution",
            "current_status": "PARTIAL_DD_MAP_SOURCE_LEG_MISSING",
            "acceptance": "q normalization, Earth/source leg, material charge tensor, readout closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "req_id": "RTE3464_2_b_mhat",
            "raw_component": "b_mhat or nuclear-binding mass coefficient",
            "needed_map": "dominant nuclear/mass material response",
            "current_status": "MTS_COMPONENT_NOT_IN_CURRENT_BASIS",
            "acceptance": "parent mass/quark/nuclear-binding coefficient row or theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "req_id": "RTE3464_3_shadow_readout",
            "raw_component": "Delta_shadow + Delta_readout",
            "needed_map": "projection of hidden/source-shadow/readout currents into Ti/Pt/Earth material contrast",
            "current_status": "RETAINED_UNMAPPED",
            "acceptance": "source-shadow basis, material projection, no-cancellation envelope",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "req_id": "RTE3464_4_no_cancellation",
            "raw_component": "sum of retained source channels",
            "needed_map": "absolute envelope before any signed cancellation",
            "current_status": "REQUIRED_GUARD",
            "acceptance": "sum_abs_components <= 2.8e-15 or theorem-zero for every component",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_chain_update() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CHAIN3464_0_to_3463",
            "feeds": "SSC3463_3_action_normalization;ANO3463_2_EM_normalization",
            "update": "canonical action/source normalization is now the named theorem, not a vague coupling gap",
            "formula": "no independent w_A or w_EM once action unit, charge/current, alpha, and readout are parent-owned",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3464_1_to_3462_WEP",
            "feeds": "WEP3462_4_product",
            "update": "WEP product can be treated as effective contrast bound while raw MTS map is missing",
            "formula": "|Delta_w_eff_TiPt| <= 2.8e-15; Delta_w_eff = tau_w Delta_w_raw + alpha/mass/shadow/readout terms",
            "status": "NONCLAIM_EFFECTIVE_BOUND_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3464_2_to_3460",
            "feeds": "Y5B3460_0_source_work_norm",
            "update": "raw source-normalization terms remain in J_norm until canonical normalization or raw-to-effective WEP map closes",
            "formula": "J_norm <= C_Y5 ||s_Y5|| + C_w ||Delta_w_raw|| + Q_nonH + Q_boundary + Q_domain + Q_range + Q_time",
            "status": "BOUND_INPUT_STILL_RAW",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3464_3_to_EM",
            "feeds": "Maxwell/Poynting stress ledger",
            "update": "EM is now the best diagnostic for the no-sector-scale theorem because w_EM affects Poynting stress and alpha/charge normalization",
            "formula": "w_EM forbidden iff unique F2 + alpha owner + charge-current owner + readout closure",
            "status": "EM_OWNER_TARGET_SHARP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3464_0_conditional_theorem",
            "claim": "canonical normalization would forbid source-only w_A/w_EM",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "the theorem is exact if all owner clauses are parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3464_1_parent_derivation",
            "claim": "MTS currently derives the canonical normalization theorem",
            "status": "FAIL_BLOCKED",
            "reason": "alpha owner, unique F2, hidden Hom exclusion, charge-current owner, and readout/radiative closure are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3464_2_effective_WEP_bound",
            "claim": "effective WEP contrast bound is ready as a nonclaim ceiling",
            "status": "PASS_NONCLAIM_BOUND",
            "reason": "the Eotvos-normalized effective contrast has a source-backed 2.8e-15 ceiling",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3464_3_raw_MTS_prediction",
            "claim": "raw MTS coefficients predict Delta_w_eff_TiPt",
            "status": "FAIL_BLOCKED",
            "reason": "raw-to-effective map requires tau_w, b_alpha source leg, b_mhat, shadow/readout projection, and no-cancellation envelope",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3464_4_local_GR_source_coupling",
            "claim": "local GR/Newton calibrated source coupling is derived",
            "status": "FAIL_BLOCKED",
            "reason": "canonical normalization is only one source-side gate; residual silence, boundary/domain, observed-frame, and PPN gates remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3464_0_theorem_status",
            "decision": "Keep canonical action normalization as the primary derivation target.",
            "because": "It is the exact missing clause that defeats the weighted Hilbert-current countermodel.",
            "next_action": "Try to derive EM alpha/charge/current owner from MTS primitives first.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3464_1_EM_priority",
            "decision": "Use EM/Poynting/fine-structure as the cleanest probe.",
            "because": "The Maxwell action has an explicit kinetic/current normalization redundancy, so it exposes whether MTS owns action scales or merely assumes them.",
            "next_action": "Attack unique F2, alpha level owner, charge-current owner, and readout closure as one package.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3464_2_WEP_bound_status",
            "decision": "Retain |Delta_w_eff_TiPt| <= 2.8e-15 as a useful nonclaim empirical ceiling.",
            "because": "It is a clean bound on the effective contrast, but not a raw MTS prediction until the component map is derived.",
            "next_action": "Build raw-to-effective component rows or prove canonical normalization kills them.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3465-Y5-R2FR-EM-alpha-Hodge-charge-owner-or-WEP-raw-to-effective-map.md",
            "next_script": "scripts/Y5_R2FR_3465_EM_alpha_Hodge_charge_owner_or_WEP_raw_to_effective_map.py",
            "objective": "Try to derive the EM action-normalization owner as a package: observed Hodge/coframe, unique F2 norm, charge-current owner, alpha level/fine-structure owner, and readout/radiative closure; if not, build raw-to-effective WEP component rows.",
            "success_gate": "Either w_EM/b_alpha is theorem-zero from EM owner clauses, or Delta_w_eff_TiPt gets explicit raw component rows with source paths, units, and no-cancellation envelope.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; raw tau unity shortcut; alpha/fine-structure owner overclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(paths: dict[str, Path], datasets: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    stamp = now()

    sources = datasets["source_register"]
    missing_sources = [row["source_id"] for row in sources if not row["exists"]]
    checks.append(
        {
            "check_id": "VAL3464_0_sources_exist",
            "passed": not missing_sources,
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} source paths exist; missing={';'.join(missing_sources) or 'none'}",
            "timestamp_utc": stamp,
        }
    )

    theorem = datasets["canonical_normalization_theorem_audit"]
    result_map = {row["theorem_id"]: row["result"] for row in theorem}
    checks.append(
        {
            "check_id": "VAL3464_1_theorem_conditional_not_claimed",
            "passed": result_map.get("CAN3464_1_single_action_unit") == "STRONG_CONDITIONAL"
            and result_map.get("CAN3464_6_verdict") == "NOT_DERIVED_CURRENT_CORPUS",
            "detail": ";".join(f"{key}={value}" for key, value in result_map.items()),
            "timestamp_utc": stamp,
        }
    )

    em = datasets["em_alpha_charge_owner_audit"]
    checks.append(
        {
            "check_id": "VAL3464_2_EM_owner_gaps_present",
            "passed": any(row["row_id"] == "EAC3464_1_alpha_level" and row["status"] == "OWNER_NOT_DERIVED" for row in em)
            and any(row["row_id"] == "EAC3464_2_unique_F2" and row["status"] == "UNIQUE_F2_NOT_CLOSED" for row in em),
            "detail": ";".join(f"{row['row_id']}={row['status']}" for row in em),
            "timestamp_utc": stamp,
        }
    )

    wep = datasets["wep_effective_source_bound"]
    checks.append(
        {
            "check_id": "VAL3464_3_effective_bound_nonclaim",
            "passed": any(row["bound_id"] == "WEB3464_2_MICROSCOPE_bound" and row["value_or_status"] == "2.8e-15" for row in wep)
            and all(str(row["valid_for_claim"]).lower() == "false" for row in wep),
            "detail": ";".join(f"{row['bound_id']}={row['value_or_status']}" for row in wep),
            "timestamp_utc": stamp,
        }
    )

    raw = datasets["raw_to_effective_requirements"]
    checks.append(
        {
            "check_id": "VAL3464_4_raw_map_requirements",
            "passed": any("tau_w" in row["req_id"] for row in raw)
            and any("b_alpha" in row["req_id"] for row in raw)
            and any("b_mhat" in row["req_id"] for row in raw)
            and any("no_cancellation" in row["req_id"] for row in raw),
            "detail": ";".join(f"{row['req_id']}={row['current_status']}" for row in raw),
            "timestamp_utc": stamp,
        }
    )

    chain = datasets["bound_chain_update"]
    checks.append(
        {
            "check_id": "VAL3464_5_chain_updates",
            "passed": any("3463" in row["chain_id"] for row in chain)
            and any("3462" in row["chain_id"] for row in chain)
            and any("3460" in row["chain_id"] for row in chain)
            and any("EM" in row["chain_id"] for row in chain),
            "detail": ";".join(f"{row['chain_id']}->{row['feeds']}" for row in chain),
            "timestamp_utc": stamp,
        }
    )

    claim_rows = [
        row
        for rows in datasets.values()
        for row in rows
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    checks.append(
        {
            "check_id": "VAL3464_6_no_claim_rows",
            "passed": not claim_rows,
            "detail": f"claim_like_rows={len(claim_rows)}",
            "timestamp_utc": stamp,
        }
    )

    parse_ok = True
    parse_details: list[str] = []
    for name, path in paths.items():
        if path.suffix.lower() == ".csv":
            if name == "validation" and not path.exists():
                parse_details.append(f"{path.name}:pending_write")
                continue
            try:
                parse_details.append(f"{path.name}:{len(read_csv(path))}")
            except Exception as exc:  # pragma: no cover - validation output
                parse_ok = False
                parse_details.append(f"{path.name}:PARSE_FAIL:{exc}")
    checks.append(
        {
            "check_id": "VAL3464_7_csv_parse",
            "passed": parse_ok,
            "detail": ";".join(parse_details),
            "timestamp_utc": stamp,
        }
    )

    formalization_has_outputs = any(FORMALIZATION.rglob("*3464*")) if FORMALIZATION.exists() else False
    checks.append(
        {
            "check_id": "VAL3464_8_formalization_untouched_by_3464",
            "passed": not formalization_has_outputs,
            "detail": f"formalization_exists={FORMALIZATION.exists()}; 3464_outputs_in_formalization={formalization_has_outputs}",
            "timestamp_utc": stamp,
        }
    )

    next_rows = datasets["next_target"]
    checks.append(
        {
            "check_id": "VAL3464_9_next_target_3465",
            "passed": len(next_rows) == 1 and "EM-alpha-Hodge-charge-owner" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
            "timestamp_utc": stamp,
        }
    )

    overall = all(row["passed"] for row in checks)
    checks.append(
        {
            "check_id": "VAL3464_SUMMARY",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return checks


def write_doc(datasets: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3464 - Canonical Action Normalization From MTS Primitives Or WEP Effective Source Bound",
        "",
        "**Current verdict:** the no-sector-action-scale theorem is exact as a conditional theorem, but not yet parent-derived. If MTS supplies one action unit, one observed coframe/Hodge star, fixed charge/current/fine-structure ownership, and readout/radiative closure, then independent `w_A` and `w_EM` have nowhere to live. The current corpus has those as candidate owner clauses, not a closed derivation.",
        "",
        "**Concrete progress:** the WEP side now has a clean nonclaim ceiling: in the effective Eotvos-normalized model `|Delta_w_eff_TiPt| <= 2.8e-15`. Raw MTS coefficients still need a map into `Delta_w_eff_TiPt`; the map must include `tau_w`, alpha, nuclear/mass, shadow/readout, and a no-cancellation envelope.",
        "",
        "## Source Register",
        md_table(datasets["source_register"]),
        "",
        "## Canonical Normalization Theorem Audit",
        md_table(datasets["canonical_normalization_theorem_audit"]),
        "",
        "## EM Alpha/Charge Owner Audit",
        md_table(datasets["em_alpha_charge_owner_audit"]),
        "",
        "## WEP Effective Source Bound",
        md_table(datasets["wep_effective_source_bound"]),
        "",
        "## Raw-To-Effective Requirements",
        md_table(datasets["raw_to_effective_requirements"]),
        "",
        "## Bound Chain Update",
        md_table(datasets["bound_chain_update"]),
        "",
        "## Claim Gates",
        md_table(datasets["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(datasets["decision_ledger"]),
        "",
        "## Validation",
        md_table(datasets["validation"]),
        "",
        "## Next Target",
        md_table(datasets["next_target"]),
        "",
        "## Bottom Line",
        "",
        "- The coupling problem has sharpened again: not source-current existence, but canonical action normalization.",
        "- EM is the best probe because `F^2`, charge/current normalization, fine-structure, Hodge/coframe, and Poynting stress all meet in one place.",
        "- No WEP/local-GR/Newton claim is promoted.",
        "- The finite fallback is now cleaner: score raw MTS only after it maps into `Delta_w_eff_TiPt`, whose empirical ceiling is `2.8e-15`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_register": OUT / "P8_Y5_R2FR_3464_SOURCE_REGISTER.csv",
        "canonical_normalization_theorem_audit": OUT / "P8_Y5_R2FR_3464_CANONICAL_NORMALIZATION_THEOREM_AUDIT.csv",
        "em_alpha_charge_owner_audit": OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
        "wep_effective_source_bound": OUT / "P8_Y5_R2FR_3464_WEP_EFFECTIVE_SOURCE_BOUND.csv",
        "raw_to_effective_requirements": OUT / "P8_Y5_R2FR_3464_RAW_TO_EFFECTIVE_REQUIREMENTS.csv",
        "bound_chain_update": OUT / "P8_Y5_R2FR_3464_BOUND_CHAIN_UPDATE.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3464_CLAIM_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3464_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3464_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3464_VALIDATION.csv",
    }
    datasets = {
        "source_register": source_register(),
        "canonical_normalization_theorem_audit": canonical_normalization_theorem_audit(),
        "em_alpha_charge_owner_audit": em_alpha_charge_owner_audit(),
        "wep_effective_source_bound": wep_effective_source_bound(),
        "raw_to_effective_requirements": raw_to_effective_requirements(),
        "bound_chain_update": bound_chain_update(),
        "claim_gates": claim_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    for key, rows in datasets.items():
        write_csv(paths[key], rows)
    datasets["validation"] = validate(paths, datasets)
    write_csv(paths["validation"], datasets["validation"])
    write_doc(datasets)


if __name__ == "__main__":
    main()
