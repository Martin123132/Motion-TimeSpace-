from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
EXTERNAL_DIR = ROOT / "source-intake" / "external_papers"

DOC = ROOT / "640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_charge_topology_or_kappa_alpha_numeric_prior.py"

STATUS = "Y5_R10_charge_topology_ladder_blocks_kappa_alpha_zero_numeric_prior_template_staged_nonclaim"
CLAIM_CEILING = "charge_topology_attempt_and_kappa_alpha_prior_template_only_no_EM_R10_WEP_clock_PPN_or_local_GR_pass"
NEXT_TARGET = "641-Y5-R10-kappa-alpha-pressure-envelope-and-charge-topology-next-proof.md"

PRIOR_639_DOC = ROOT / "639-Y5-R10-finite-constant-beta-local-bound-matrix-runner.md"
PRIOR_639_VALIDATION = MTS_DIR / "P8_Y5_BRR545_639_VALIDATION.csv"
PRIOR_639_MATRIX = MTS_DIR / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv"
PRIOR_639_SYMBOLS = MTS_DIR / "P8_Y5_R10_639_CONSTANT_BETA_SYMBOL_TABLE.csv"
PRIOR_639_SLOTS = MTS_DIR / "P8_Y5_R10_639_NUMERIC_SLOT_LEDGER.csv"
PRIOR_287_DOC = ROOT / "287-boundary-current-charge-owner-attempt.md"
PRIOR_109_DOC = ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md"
PRIOR_110_DOC = ROOT / "110-endpoint-charge-equation-attempt.md"
ANDERSEN_CONTRACT = EXTERNAL_DIR / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv"
ANDERSEN_AUDIT = EXTERNAL_DIR / "Andersen_2026_HFGW_EM_charge_relevance_AUDIT.csv"
ANDERSEN_DECISION = EXTERNAL_DIR / "Andersen_2026_charge_phase_DECISION.csv"
P8_CHARGE_STATUS = MTS_DIR / "P8_charge_current_equality_STATUS.csv"
P8_PG_CONTRACT = MTS_DIR / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_640_SOURCE_REGISTER.csv"
CHARGE_TOPOLOGY_LADDER = MTS_DIR / "P8_Y5_R10_640_CHARGE_TOPOLOGY_LADDER.csv"
KAPPA_ALPHA_DERIVATION = MTS_DIR / "P8_Y5_R10_640_KAPPA_ALPHA_DERIVATION.csv"
MAXWELL_LIMIT_GATE = MTS_DIR / "P8_Y5_R10_640_MAXWELL_LIMIT_GATE.csv"
KAPPA_ALPHA_PRIOR_TEMPLATE = MTS_DIR / "P8_Y5_R10_640_KAPPA_ALPHA_PRIOR_TEMPLATE.csv"
MATRIX_UPDATE = MTS_DIR / "P8_Y5_R10_640_MATRIX_UPDATE.csv"
ADOPTION_GATE = MTS_DIR / "P8_Y5_R10_640_ADOPTION_GATE.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_640_DECISION.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_640_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_640_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_640_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_639_DOC, "immediate 639 checkpoint"),
        (PRIOR_639_VALIDATION, "639 validation gate"),
        (PRIOR_639_MATRIX, "639 local bound matrix"),
        (PRIOR_639_SYMBOLS, "639 constant beta symbol table"),
        (PRIOR_639_SLOTS, "639 numeric slot ledger"),
        (PRIOR_287_DOC, "boundary-current charge owner obstruction"),
        (PRIOR_109_DOC, "normalized boundary charge obstruction"),
        (PRIOR_110_DOC, "endpoint charge equation obstruction"),
        (ANDERSEN_CONTRACT, "external phase/current charge contract"),
        (ANDERSEN_AUDIT, "external HFGW/EM charge relevance audit"),
        (ANDERSEN_DECISION, "external charge phase decision ledger"),
        (P8_CHARGE_STATUS, "charge-current equality status"),
        (P8_PG_CONTRACT, "Poisson-Gauss/charge calibration contract"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC640_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def charge_topology_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "rung_id": "CTL640_0_compact_phase",
            "needed_statement": "theta_Q is a compact parent phase with theta_Q ~ theta_Q + 2pi and a real shift symmetry",
            "would_imply": "charge sign/polarity can be phase orientation rather than an inserted label",
            "current_evidence": "Andersen contract PC0 names the route; MTS charge files do not derive the phase variable",
            "rung_status": "open_not_derived",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_1_noether_current",
            "needed_statement": "J_Q^mu is the Noether/Ward/topological current of the compact phase and obeys nabla_mu J_Q^mu=0",
            "would_imply": "charge conservation is structural",
            "current_evidence": "287 supports relative current conservation conditionally, but not the EM charge current",
            "rung_status": "conditional_support_only",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_2_charge_unit",
            "needed_statement": "Q/e = n or Q/Q_star = n/k with e or Q_star fixed by winding, level, index, or boundary-current theorem",
            "would_imply": "charge unit is discrete/topological and locally vertical-silent",
            "current_evidence": "287/109/110 repeatedly identify Q_star or unit charge as missing",
            "rung_status": "fail_current_derivation",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_3_gauge_kinetic_normalization",
            "needed_statement": "the Maxwell/gauge kinetic coefficient is fixed by the same parent topological level/readout normalization",
            "would_imply": "alpha_EM is quotient/topological rather than a smooth scalar alpha_EM(Xhat)",
            "current_evidence": "no current file derives the gauge kinetic normalization or fine-structure value",
            "rung_status": "not_derived",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_4_Maxwell_limit",
            "needed_statement": "coarse-grained charge carrier equations reduce to Gauss, no-monopole, Faraday, and Ampere-Maxwell equations in one observed frame",
            "would_imply": "the charge branch is EM, not only a Coulomb analogy",
            "current_evidence": "Andersen audit says Maxwell/Lorentz limits remain missing",
            "rung_status": "not_derived",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_5_Lorentz_readout",
            "needed_statement": "ordinary matter sees q(E+v x B) from the same observed coframe without adding a material marker",
            "would_imply": "charge coupling does not reopen WEP/clock/source-marker channels",
            "current_evidence": "external audit leaves Lorentz-force/readout as a required derivation",
            "rung_status": "not_derived",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "CTL640_6_regular_source",
            "needed_statement": "carrier/source is finite, topological, or regularized without hidden singular source normalization",
            "would_imply": "charge source does not bypass measured-GM/source-normalization gates",
            "current_evidence": "Andersen contract PC6 and PC7 keep source regularity and GR-gate separation open",
            "rung_status": "not_derived",
            "blocks_kappa_alpha_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def kappa_alpha_derivation_rows(ladder_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = [row for row in ladder_rows if row.get("blocks_kappa_alpha_zero") == "true"]
    return [
        {
            "derivation_id": "KA640_0_if_topological",
            "claim": "If alpha_EM is fixed by a parent topological/representation level, then kappa_alpha=d ln alpha_EM/dXhat=0 for smooth local vertical Xhat.",
            "proof_status": "conditional_math_pass",
            "reason": "a locally smooth vertical variation cannot change an integer level or a quotient-owned fixed representation constant",
            "current_parent_status": "topological ownership not derived",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "KA640_1_current_corpus",
            "claim": "Current MTS corpus derives kappa_alpha=0.",
            "proof_status": "fail_current_claim",
            "reason": f"charge topology ladder has {len(blockers)} blocking rungs",
            "current_parent_status": "open",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "KA640_2_finite_branch",
            "claim": "If any ladder rung fails, kappa_alpha remains an explicit finite constant-sector input.",
            "proof_status": "required_fallback",
            "reason": "alpha_EM is dimensionless, so unit convention cannot hide d ln alpha_EM/dXhat",
            "current_parent_status": "kappa_alpha=MISSING_PARENT_NUMERIC",
            "valid_for_claim": "false",
        },
    ]


def maxwell_limit_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ML640_0_Gauss",
            "required_equation": "div E = rho/epsilon0 or quotient-normalized equivalent",
            "current_status": "not_derived",
            "why_it_matters": "Coulomb-like force alone does not define full EM",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ML640_1_no_monopole",
            "required_equation": "div B = 0 or topological magnetic-sector constraint",
            "current_status": "not_derived",
            "why_it_matters": "needed to identify a Maxwell field rather than arbitrary vector potential analogy",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ML640_2_Faraday",
            "required_equation": "curl E + partial_t B = 0",
            "current_status": "not_derived",
            "why_it_matters": "needed for gauge field dynamics and clock/spectroscopy consistency",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ML640_3_Ampere_Maxwell",
            "required_equation": "curl B - partial_t E = J",
            "current_status": "not_derived",
            "why_it_matters": "connects conserved charge current to propagating EM field",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ML640_4_Lorentz_force",
            "required_equation": "matter readout gives q(E+v x B)",
            "current_status": "not_derived",
            "why_it_matters": "without it, alpha_EM cannot be promoted into the matter-sector constants ledger",
            "valid_for_claim": "false",
        },
    ]


def kappa_alpha_prior_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "prior_id": "KAP640_0_theorem_zero",
            "prior_type": "theorem_zero_target",
            "kappa_alpha_value": "0",
            "units": "per_Xhat_unit",
            "allowed_only_if": "all charge topology ladder rungs close and Maxwell/Lorentz readout is parent-derived",
            "current_status": "not_allowed_for_claim",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KAP640_1_symbolic_free",
            "prior_type": "symbolic_free_parameter",
            "kappa_alpha_value": "MISSING_PARENT_NUMERIC",
            "units": "per_Xhat_unit",
            "allowed_only_if": "private pressure run needs sensitivity scan before derivation closes",
            "current_status": "default_after_640",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KAP640_2_log_scan_placeholder",
            "prior_type": "private_log_scan_template",
            "kappa_alpha_value": "SCAN_GRID_NOT_SET",
            "units": "per_Xhat_unit",
            "allowed_only_if": "641 defines Xhat units, kappa normalization, and cross-arena tau mapping",
            "current_status": "template_only",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KAP640_3_bound_saturating_diagnostic",
            "prior_type": "private_bound_saturating_diagnostic",
            "kappa_alpha_value": "DERIVE_FROM_BOUND_AFTER_MATRIX_NORMALIZATION",
            "units": "per_Xhat_unit",
            "allowed_only_if": "used only to learn which arena dominates; not a prediction",
            "current_status": "diagnostic_only",
            "valid_for_claim": "false",
        },
    ]


def matrix_update_rows() -> list[dict[str, Any]]:
    matrix_rows = read_csv(PRIOR_639_MATRIX)
    relevant = []
    for row in matrix_rows:
        required = row.get("required_mts_inputs", "")
        row_id = row.get("row_id", "")
        if "kappa_i" in required or row_id in {"R0_identity_coframe_direct", "R1_WEP_source_charge", "R2_clock_redshift"}:
            relevant.append(
                {
                    "update_id": f"MU640_{len(relevant)}",
                    "row_id": row_id,
                    "observable": row.get("observable", ""),
                    "kappa_alpha_role": "direct_or_indirect_constant_sensitivity",
                    "after_640_status": "blocked_until_kappa_alpha_zero_or_numeric_prior",
                    "prediction_numeric_ready": "false",
                    "valid_for_claim": "false",
                }
            )
    relevant.append(
        {
            "update_id": f"MU640_{len(relevant)}",
            "row_id": "EM_spectra",
            "observable": "alpha_EM_spectral_sensitivity",
            "kappa_alpha_role": "direct_EM_constant_variation",
            "after_640_status": "new_private_matrix_row_candidate_not_bound_scored",
            "prediction_numeric_ready": "false",
            "valid_for_claim": "false",
        }
    )
    return relevant


def adoption_gate_rows(
    ladder_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    maxwell_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ladder_blockers = [row for row in ladder_rows if row.get("blocks_kappa_alpha_zero") == "true"]
    maxwell_open = [row for row in maxwell_rows if row.get("current_status") != "derived"]
    claim_rows = [
        row
        for group in (ladder_rows, derivation_rows, maxwell_rows, prior_rows)
        for row in group
        if row.get("valid_for_claim") == "true"
    ]
    return [
        {
            "gate_id": "AG640_0_charge_ladder_audited",
            "requirement": "compact phase/current/unit/Maxwell/readout/source ladder audited",
            "result": "pass" if len(ladder_rows) == 7 else "fail",
            "detail": f"ladder_rows={len(ladder_rows)}",
            "kappa_alpha_zero_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG640_1_kappa_alpha_zero",
            "requirement": "all charge topology rungs close before kappa_alpha=0",
            "result": "blocked",
            "detail": f"ladder_blockers={len(ladder_blockers)};maxwell_open={len(maxwell_open)}",
            "kappa_alpha_zero_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG640_2_prior_template",
            "requirement": "numeric kappa_alpha prior is explicitly template-only until units/tau map are defined",
            "result": "pass" if len(prior_rows) == 4 else "fail",
            "detail": f"prior_rows={len(prior_rows)}",
            "kappa_alpha_zero_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG640_3_claim_leak",
            "requirement": "no EM/R10/WEP/clock/PPN/local-GR claim",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
            "kappa_alpha_zero_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D640_0_main_verdict",
            "decision": STATUS,
            "meaning": "the topological route would kill kappa_alpha if it closed, but the current corpus does not derive charge unit, Maxwell limit, or gauge normalization",
            "status": "derivation_attempt_blocks_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D640_1_best_news",
            "decision": "conditional_kappa_alpha_zero_theorem_shape_written",
            "meaning": "if alpha_EM is a fixed topological/representation level, smooth local Xhat variation cannot change it",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D640_2_blocker",
            "decision": "charge_unit_and_Maxwell_normalization_missing",
            "meaning": "current relative-current machinery supports conservation language but not the normalized EM coupling",
            "status": "core_blocker",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D640_3_fallback",
            "decision": "kappa_alpha_prior_template_staged_nonclaim",
            "meaning": "private pressure scans may be prepared only after Xhat units and arena tau maps are fixed",
            "status": "template_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC640_0_charge_unit_proof",
            "required_output": "derive or reject Q/e=n from compact phase/winding/level/index/current theorem",
            "success_condition": "charge unit is fixed without empirical amplitude or source normalization cheat",
            "if_success": "kappa_alpha zero route improves",
            "if_fail": "kappa_alpha remains finite input",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC640_1_Maxwell_gauge_normalization",
            "required_output": "derive Maxwell equations plus gauge kinetic normalization from the parent carrier/current action",
            "success_condition": "alpha_EM is a quotient/topological coefficient, not a smooth scalar marker",
            "if_success": "EM/clock/WEP constant rows may close conditionally",
            "if_fail": "numeric kappa_alpha pressure envelope is mandatory",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC640_2_kappa_alpha_pressure",
            "required_output": "if topology fails, define Xhat units, tau maps, and a private kappa_alpha scan envelope",
            "success_condition": "639 matrix can react to kappa_alpha without public claim",
            "if_success": "run 641 pressure envelope",
            "if_fail": "constant branch remains symbolic only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(
    ladder_rows: list[dict[str, Any]],
    maxwell_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    blockers = [row for row in ladder_rows if row.get("blocks_kappa_alpha_zero") == "true"]
    maxwell_open = [row for row in maxwell_rows if row.get("current_status") != "derived"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "charge_ladder_rows": len(ladder_rows),
            "charge_ladder_blockers": len(blockers),
            "maxwell_open_rows": len(maxwell_open),
            "kappa_alpha_zero_derived": "false",
            "kappa_alpha_numeric_ready": "false",
            "prior_template_rows": len(prior_rows),
            "matrix_update_rows": len(matrix_rows),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    ladder_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    maxwell_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row.get("exists") != "true"]
    prior_validation_rows = read_csv(PRIOR_639_VALIDATION)
    prior_fails = [row for row in prior_validation_rows if row.get("result") != "pass"]
    ladder_blockers = [row for row in ladder_rows if row.get("blocks_kappa_alpha_zero") == "true"]
    maxwell_open = [row for row in maxwell_rows if row.get("current_status") != "derived"]
    zero_allowed = any(row.get("kappa_alpha_zero_allowed") == "true" for row in gate_rows)
    claim_rows = [
        row
        for group in (ladder_rows, derivation_rows, maxwell_rows, prior_rows, matrix_rows, gate_rows)
        for row in group
        if row.get("valid_for_claim") == "true"
    ]
    return [
        {
            "check_id": "V640_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V640_1_prior_639_clean",
            "result": "pass" if prior_validation_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_validation_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V640_2_charge_ladder_complete_blocked",
            "result": "pass" if len(ladder_rows) == 7 and len(ladder_blockers) >= 5 else "fail",
            "detail": f"ladder_rows={len(ladder_rows)};blockers={len(ladder_blockers)}",
        },
        {
            "check_id": "V640_3_kappa_alpha_derivation_status",
            "result": "pass" if len(derivation_rows) == 3 and any(row.get("proof_status") == "fail_current_claim" for row in derivation_rows) else "fail",
            "detail": f"derivation_rows={len(derivation_rows)}",
        },
        {
            "check_id": "V640_4_maxwell_limit_open",
            "result": "pass" if len(maxwell_rows) == 5 and len(maxwell_open) == 5 else "fail",
            "detail": f"maxwell_rows={len(maxwell_rows)};open={len(maxwell_open)}",
        },
        {
            "check_id": "V640_5_prior_template_nonclaim",
            "result": "pass" if len(prior_rows) == 4 and all(row.get("valid_for_claim") == "false" for row in prior_rows) else "fail",
            "detail": f"prior_rows={len(prior_rows)}",
        },
        {
            "check_id": "V640_6_matrix_update_written",
            "result": "pass" if len(matrix_rows) >= 4 else "fail",
            "detail": f"matrix_update_rows={len(matrix_rows)}",
        },
        {
            "check_id": "V640_7_kappa_alpha_zero_blocked",
            "result": "pass" if len(gate_rows) == 4 and not zero_allowed else "fail",
            "detail": f"gate_rows={len(gate_rows)};zero_allowed={bool_text(zero_allowed)}",
        },
        {
            "check_id": "V640_8_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V640_9_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V640_10_no_local_claim",
            "result": "pass",
            "detail": "kappa_alpha_zero=false;kappa_alpha_numeric=false;EM=false;R10=false;WEP=false;clock=false;PPN=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_doc(
    source_rows: list[dict[str, Any]],
    ladder_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    maxwell_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = "\n".join(
        [
            "# 640 Y5 R10 charge topology or kappa alpha numeric prior",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Next target: `{NEXT_TARGET}`",
            "",
            "## Verdict",
            "- The good theorem shape is real: if `alpha_EM` is fixed by a parent topological/representation level, then smooth local `Xhat` variation gives `kappa_alpha = 0`.",
            "- The current corpus does not derive that ownership. The charge unit, gauge kinetic normalization, Maxwell limit, Lorentz readout, and regular source are still open.",
            "- Therefore `kappa_alpha=0` is **not** claimed.",
            "- A private `kappa_alpha` prior template is staged, but no numeric scan is allowed until `Xhat` units and arena `tau` maps are defined.",
            "",
            "## Derivation Core",
            "The attempted proof is:",
            "",
            "`theta_Q compact + Noether current + quantized charge unit + Maxwell/gauge normalization`",
            "",
            "`=> alpha_EM is quotient/topological`",
            "",
            "`=> delta_Xhat alpha_EM = 0`",
            "",
            "`=> kappa_alpha = d ln alpha_EM / dXhat = 0`.",
            "",
            "The proof is mathematically fine as a conditional theorem. It fails as a current MTS derivation because the parent action has not supplied the compact phase/current/unit/Maxwell normalization stack.",
            "",
            "## Source Register",
            markdown_table(source_rows),
            "## Charge Topology Ladder",
            markdown_table(ladder_rows),
            "## Kappa Alpha Derivation",
            markdown_table(derivation_rows),
            "## Maxwell Limit Gate",
            markdown_table(maxwell_rows),
            "## Kappa Alpha Prior Template",
            markdown_table(prior_rows),
            "## Matrix Update",
            markdown_table(matrix_rows),
            "## Adoption Gate",
            markdown_table(gate_rows),
            "## Decision",
            markdown_table(decision),
            "## Next Contract",
            markdown_table(contract_rows),
            "## Nonclaim Summary",
            markdown_table(summary),
            "## Validation",
            markdown_table(validation),
            "## Interpretation",
            "This is a clean fork, not a dead end. The elegant route is charge as compact topology: then `kappa_alpha` dies locally. But the current MTS files only have conservation/support clues, not the charge unit and Maxwell normalization. So the honest next move is either one more targeted charge-unit/Maxwell proof, or a private pressure envelope where `kappa_alpha` is treated as explicit and cross-checked against the 639 matrix.",
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    ladder_rows = charge_topology_ladder_rows()
    derivation_rows = kappa_alpha_derivation_rows(ladder_rows)
    maxwell_rows = maxwell_limit_gate_rows()
    prior_rows = kappa_alpha_prior_template_rows()
    matrix_rows = matrix_update_rows()
    gate_rows = adoption_gate_rows(ladder_rows, derivation_rows, maxwell_rows, prior_rows)
    decision = decision_rows()
    contract_rows = next_contract_rows()
    summary = nonclaim_summary_rows(ladder_rows, maxwell_rows, prior_rows, matrix_rows)
    validation = validation_rows(
        source_rows,
        ladder_rows,
        derivation_rows,
        maxwell_rows,
        prior_rows,
        matrix_rows,
        gate_rows,
        contract_rows,
    )

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(CHARGE_TOPOLOGY_LADDER, ladder_rows)
    write_csv(KAPPA_ALPHA_DERIVATION, derivation_rows)
    write_csv(MAXWELL_LIMIT_GATE, maxwell_rows)
    write_csv(KAPPA_ALPHA_PRIOR_TEMPLATE, prior_rows)
    write_csv(MATRIX_UPDATE, matrix_rows)
    write_csv(ADOPTION_GATE, gate_rows)
    write_csv(DECISION, decision)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validation)
    write_doc(
        source_rows,
        ladder_rows,
        derivation_rows,
        maxwell_rows,
        prior_rows,
        matrix_rows,
        gate_rows,
        decision,
        contract_rows,
        summary,
        validation,
    )

    failed = [row for row in validation if row["result"] != "pass"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "doc": str(DOC),
                "failed_checks": failed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
