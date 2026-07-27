from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2188"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2188_SOURCE_REGISTER.csv",
    "double_zero_contract": OUT / "P8_Y5_PARENT_QLOC_2188_DOUBLE_ZERO_THEOREM_CONTRACT.csv",
    "extra_leakage": OUT / "P8_Y5_PARENT_QLOC_2188_EXTRA_SECTOR_LEAKAGE_LEDGER.csv",
    "pim_lock": OUT / "P8_Y5_PARENT_QLOC_2188_PIM_LOCK_CONTRACT.csv",
    "local_envelope": OUT / "P8_Y5_PARENT_QLOC_2188_LOCAL_GR_ENVELOPE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2188_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2188_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2188_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2188_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2188_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2188_EXTRA_DOUBLE_ZERO_PIM_LOCK_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2188_EXTRA_PIM_LOCK_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_EXTRA_DOUBLE_ZERO_PIM_LOCK_2188_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2188_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2188-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2188*",
        "*P8_Y5_BRR545_2188*",
        "*Y5_R2FR_extra_sector_double_zero_and_PiM_lock_signature_or_residual_fill_2188*",
        "*JR2188*",
        "*PARENT_EXTRA_DOUBLE_ZERO_PIM_LOCK_2188*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2187_handoff",
            ROOT / "2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md",
            ["NEXT2187_0_2188", "EXTRA_DOUBLE_ZERO_AND_PIM_LOCK_SIGNATURE_NEXT", "VAL2187_OVERALL"],
            "2187 selects extra-sector double-zero and PiM lock signatures as the next local-GR descent gate.",
        ),
        (
            "min_action_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_3_extra_field_silence", "A511_6_metric_readout", "A511_2_universal_matter"],
            "minimum local-GR action blocks define extra-field silence, metric readout protection, and universal matter.",
        ),
        (
            "fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_2_positive_mass_gap"],
            "fixed-point conditions give the exact double-zero, PiM lock, and positive gap tests.",
        ),
        (
            "2185_conditional_EH",
            ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            ["extra-sector double zeros", "Pi_M(Phi0)=Pi_EH", "CONDITIONAL_INHERITANCE_WIN_CURRENT_MTS_CLAIM_BLOCKED"],
            "2185 proves coefficients inside EH but blocks MTS ownership until double-zero/PiM clauses close.",
        ),
        (
            "2187_signature_matrix",
            OUT / "P8_Y5_PARENT_QLOC_2187_EH_DESCENT_SIGNATURE_MATRIX.csv",
            ["EDS2187_1_extra_double_zero", "EDS2187_3_PiM_lock", "REQUIRED_NOT_PROVED"],
            "2187 signature matrix names extra double zero and PiM lock as live missing signatures.",
        ),
        (
            "2181_PiM_product_rule",
            ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
            ["d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H", "M_source[W]=integral_S Pi_M J_H=M_eff"],
            "2181 supplies the PiM product-rule obstruction and measured source equality target.",
        ),
        (
            "2182_topological_equality",
            ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            ["Pi_M J_H = J_M_top + dB_zero + R_eq", "R_eq=0"],
            "2182 defines the topological-Hilbert equality residual needed by the PiM lock path.",
        ),
        (
            "1009_parent_current_chain",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["S_GK[g,Phi]", "double-zero local residual", "PIM_PARENT_ORIGIN_AND_VARIATION_NOT_PROVED"],
            "1009 shows the Gamma/Khat/q_loc and PiM pieces still need parent variation and double-zero proof.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def double_zero_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DZ2188_0_split",
            "parent local action split",
            "S_parent = S_EH[e_obs,kappa0] + S_matter[psi,e_obs] + sum_i int sqrt(-g) C_i(Phi) O_i[g,psi,Pi_M,boundary] + S_gap[Phi] + S_boundary.",
            "CONTRACT_WRITTEN_NOT_PARENT_ACTION",
            "the theorem is meaningful only after every local non-EH operator O_i is listed.",
        ),
        (
            "DZ2188_1_fixed_point",
            "local fixed point",
            "Phi=Phi0, E_A(Phi0)=0, L_tau Phi0=0, exterior source current J_A=0.",
            "FIXED_POINT_REQUIRED_NOT_PROVED",
            "there is no plateau axiom; the fixed point must solve parent Euler equations.",
        ),
        (
            "DZ2188_2_amplitude_zero",
            "zeroth-order extra silence",
            "For every metric/source/readout/projector coupling, C_i(Phi0)=0 unless it is already part of EH or universal matter.",
            "C0_ZERO_REQUIRED_NOT_PROVED",
            "otherwise local GR inherits a finite fifth-force/source/readout term.",
        ),
        (
            "DZ2188_3_derivative_zero",
            "first-variation extra silence",
            "For every such coupling, partial_A C_i(Phi0)=0, so the linear leakage F_1 vanishes.",
            "DC_ZERO_REQUIRED_NOT_PROVED",
            "this is the exact double-zero condition rather than a fitted suppression.",
        ),
        (
            "DZ2188_4_F1_law",
            "derived local leakage law",
            "Expanding C_i=C_i0+C_i,A phi^A+O(phi^2) gives F_1=sum_i(C_i0 delta O_i + C_i,A phi^A O_i0); double zero implies F_1=0.",
            "CONDITIONAL_THEOREM_DERIVED",
            "this closes the algebraic first-order leakage route if parent-signed.",
        ),
        (
            "DZ2188_5_mass_gap",
            "positive compact exterior operator",
            "int <phi,L phi> >= m_min^2 ||phi||^2 with zero source and boundary flux, giving phi=0 or an explicit exponential/energy bound.",
            "POSITIVE_GAP_REQUIRED_NOT_PROVED",
            "double zero alone is not enough if compact exterior hair is unsuppressed.",
        ),
        (
            "DZ2188_6_boundary",
            "extra boundary silence",
            "theta_extra, Q_tau_extra, exact/topological boundary improvements have zero compact local flux or fixed reference subtraction.",
            "BOUNDARY_SILENCE_REQUIRED_NOT_PROVED",
            "bulk silence can still fail through Hamiltonian/boundary charge leakage.",
        ),
        (
            "DZ2188_7_verdict",
            "current double-zero status",
            "The exact theorem route is written and useful, but current MTS sources do not yet parent-sign the C_i list, C_i(Phi0)=0, partial_A C_i(Phi0)=0, gap, and boundary clauses.",
            "THEOREM_CONTRACT_PASS_CURRENT_CLAIM_FAILS",
            "retain residual rows and attack the parent operator inventory next.",
        ),
    ]
    return [
        base_row(contract_id=contract_id, clause=clause, statement=statement, status=status, implication=implication)
        for contract_id, clause, statement, status, implication in specs
    ]


def extra_leakage_rows() -> list[dict[str, Any]]:
    rows = [
        ("EL2188_0_C0_GK", "epsilon_C0_GammaKhat", "zeroth-order metric/source coupling from Gamma_eff/K_hat/q_loc sector at Phi0", "MISSING_C0_VALUE", "MISSING_GK_C0_ZERO_PROOF", "dimensionless_or_declared", "PPN;R10;local_GR", "MISSING_SOURCE_PATH"),
        ("EL2188_1_dC_GK", "epsilon_dC_GammaKhat", "first derivative of Gamma_eff/K_hat/q_loc coupling at Phi0", "MISSING_DC_VALUE", "MISSING_GK_DC_ZERO_PROOF", "dimensionless_operator_norm", "PPN;R10;local_GR", "MISSING_SOURCE_PATH"),
        ("EL2188_2_C0_memory", "epsilon_C0_memory_response", "zeroth-order memory/response coupling that can source compact local hair", "MISSING_C0_VALUE", "MISSING_MEMORY_C0_ZERO_PROOF", "dimensionless_or_declared", "clocks;PPN;orbital", "MISSING_SOURCE_PATH"),
        ("EL2188_3_dC_memory", "epsilon_dC_memory_response", "first derivative of memory/response coupling at Phi0", "MISSING_DC_VALUE", "MISSING_MEMORY_DC_ZERO_PROOF", "dimensionless_operator_norm", "clocks;PPN;orbital", "MISSING_SOURCE_PATH"),
        ("EL2188_4_domain", "epsilon_domain_projector_stress", "domain/projector selector stress or preferred-frame leakage at local fixed point", "MISSING_PROJECTOR_STRESS_VALUE", "MISSING_DOMAIN_PROJECTOR_ZERO_PROOF", "dimensionless_or_stress_norm", "PPN_alpha_i;WEP;local_GR", "MISSING_SOURCE_PATH"),
        ("EL2188_5_species", "epsilon_species_coupling", "species-dependent matter coupling slope partial_A ln m_species(Phi0)", "MISSING_SPECIES_SLOPE", "MISSING_UNIVERSAL_MATTER_SLOPE_ZERO", "dimensionless", "WEP;clocks;source_mass", "MISSING_SOURCE_PATH"),
        ("EL2188_6_gap", "epsilon_extra_gap_hair", "failure of positive source-free compact exterior operator to force phi=0 or bound hair", "MISSING_MASS_GAP_BOUND", "MISSING_POSITIVE_GAP_CERTIFICATE", "dimensionless_or_length_scale", "PPN;orbital;R10", "MISSING_SOURCE_PATH"),
        ("EL2188_7_boundary", "epsilon_extra_boundary_flux", "extra-sector theta/Q/boundary flux through local linking surfaces", "MISSING_BOUNDARY_FLUX_VALUE", "MISSING_EXTRA_BOUNDARY_ZERO_PROOF", "GM_flux_or_dimensionless", "Newton;PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("EL2188_8_F1_total", "F1_extra_linear_leakage_norm", "absolute first-order leakage envelope sum |C_i0 delta O_i|+|C_i,A phi^A O_i0| across retained extra sectors", "MISSING_COMPONENT_INPUTS", "MISSING_DOUBLE_ZERO_COMPONENTS", "dimensionless_or_declared", "local_GR;PPN;WEP", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            value=value,
            status=status,
            units=units,
            observable_link=observable_link,
            source_path=source_path,
            score_ready=False,
        )
        for row_id, symbol, definition, value, status, units, observable_link, source_path in rows
    ]


def pim_lock_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PIM2188_0_fixed_point_value",
            "Pi_M(Phi0)=Pi_EH",
            "Projector value lock at the EH fixed point.",
            "PIM_VALUE_LOCK_REQUIRED_NOT_PROVED",
            "epsilon_PiM_value := ||Pi_M(Phi0)-Pi_EH|| remains live.",
        ),
        (
            "PIM2188_1_derivative_silence",
            "partial_A Pi_M(Phi0)=0",
            "Projector derivative silence prevents first-order mass calibration drift.",
            "PIM_DERIVATIVE_LOCK_REQUIRED_NOT_PROVED",
            "epsilon_DPiM := ||partial_A Pi_M(Phi0)|| remains live.",
        ),
        (
            "PIM2188_2_same_Hilbert_current",
            "Pi_M acts on the same J_H as the EH Hamiltonian source",
            "The current domain, coframe, tau, reference, and worldtube must match before readout.",
            "SAME_SOURCE_DOMAIN_REQUIRED_NOT_PROVED",
            "otherwise the projector can conserve the wrong mass current.",
        ),
        (
            "PIM2188_3_product_rule",
            "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "The commutator term vanishes only if Pi_M is fixed/covariantly constant on the same source-current domain.",
            "COMMUTATOR_ZERO_REQUIRED_NOT_PROVED",
            "I_commutator remains a nonclaim residual.",
        ),
        (
            "PIM2188_4_projector_stress",
            "no projector stress",
            "Metric/source variation of Pi_M contributes no hidden stress or boundary charge at Phi0.",
            "PROJECTOR_STRESS_ZERO_REQUIRED_NOT_PROVED",
            "PPN/source normalization can fail even if the algebraic value lock holds.",
        ),
        (
            "PIM2188_5_topological_equality",
            "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "The topological current must be the same Hilbert current with R_eq=0 and zero boundary flux.",
            "TOPOLOGICAL_HILBERT_EQUALITY_REQUIRED_NOT_PROVED",
            "R_eq/B_zero rows from 2182 remain active.",
        ),
        (
            "PIM2188_6_verdict",
            "current PiM lock status",
            "The exact PiM lock conditions are now gathered in one gate, but no current source parent-signs value lock, derivative silence, commutator zero, projector stress silence, and topological-Hilbert equality together.",
            "PIM_LOCK_CONTRACT_PASS_CURRENT_CLAIM_FAILS",
            "do not absorb PiM residuals into measured G.",
        ),
    ]
    return [
        base_row(lock_id=lock_id, lock_clause=lock_clause, statement=statement, status=status, implication=implication)
        for lock_id, lock_clause, statement, status, implication in specs
    ]


def local_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2188_0_EH_core", "epsilon_EH_core_signature", "failure to parent-sign EH operator core with constant local kappa0", "MISSING_EH_CORE_PARENT_SIGNATURE", "MISSING_PARENT_SIGNATURE", "dimensionless_or_declared", "local_GR", "MISSING_SOURCE_PATH"),
        ("ENV2188_1_F1", "F1_extra_linear_leakage_norm", "absolute first-order extra-sector leakage envelope", "MISSING_COMPONENT_INPUTS", "MISSING_DOUBLE_ZERO_COMPONENTS", "dimensionless_or_declared", "PPN;WEP;local_GR", "MISSING_SOURCE_PATH"),
        ("ENV2188_2_gap", "epsilon_extra_gap_hair", "remaining compact exterior hair after double-zero algebra", "MISSING_MASS_GAP_BOUND", "MISSING_POSITIVE_GAP_CERTIFICATE", "dimensionless_or_declared", "PPN;orbital", "MISSING_SOURCE_PATH"),
        ("ENV2188_3_PiM_value", "epsilon_PiM_value", "projector value mismatch ||Pi_M(Phi0)-Pi_EH||", "MISSING_PIM_VALUE_LOCK", "MISSING_PARENT_PIM_LOCK", "dimensionless_or_GM_flux", "Newton;R10;PPN", "MISSING_SOURCE_PATH"),
        ("ENV2188_4_PiM_derivative", "epsilon_DPiM", "projector first derivative norm at Phi0", "MISSING_PIM_DERIVATIVE_LOCK", "MISSING_PARENT_PIM_LOCK", "dimensionless_operator_norm", "Newton;R10;PPN", "MISSING_SOURCE_PATH"),
        ("ENV2188_5_commutator", "I_commutator", "finite annulus/source integral of [d,Pi_M]J_H", "MISSING_I_COMMUTATOR_VALUE", "MISSING_COMMUTATOR_ZERO_OR_BOUND", "GM_flux_or_dimensionless", "Newton;R10;R11", "MISSING_SOURCE_PATH"),
        ("ENV2188_6_projector_stress", "epsilon_projector_stress", "metric/source stress from Pi_M variation", "MISSING_PROJECTOR_STRESS_VALUE", "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND", "dimensionless_or_stress_norm", "PPN;WEP;local_GR", "MISSING_SOURCE_PATH"),
        ("ENV2188_7_R_eq", "R_eq_integral", "topological-Hilbert equality residual Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_VALUE", "MISSING_R_EQ_ZERO_OR_BOUND", "GM_flux_or_dimensionless", "Newton;R10;R11", "MISSING_SOURCE_PATH"),
        ("ENV2188_8_boundary", "epsilon_boundary_reference_zero", "extra/reference/boundary flux through compact local linking surfaces", "MISSING_BOUNDARY_ZERO_PROOF", "MISSING_BOUNDARY_ZERO_OR_BOUND", "GM_flux_or_dimensionless", "Newton;PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("ENV2188_9_readout", "epsilon_readout_gauge_owner", "radial/angle readout owner from 2187 remains parent-unsigned", "MISSING_PARENT_RADIAL_GAUGE_OWNER", "MISSING_READOUT_OWNER", "dimensionless_or_declared", "2PN;PPN", "MISSING_SOURCE_PATH"),
        ("ENV2188_10_total", "Delta_local_GR_EH_descent_abs", "absolute no-cancellation sum of EH, F1, gap, PiM, commutator, projector, R_eq, boundary and readout residuals", "MISSING_COMPONENT_INPUTS", "MISSING_COMPONENT_INPUTS", "dimensionless_or_declared", "local_GR;Newton;PPN;WEP", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            value=value,
            status=status,
            units=units,
            observable_link=observable_link,
            source_path=source_path,
            score_ready=False,
        )
        for row_id, symbol, definition, value, status, units, observable_link, source_path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2188_0_F1_law", "F1=0 follows from double-zero algebra", "CONDITIONAL_PASS_GUARDRAIL", "the derivation law is written but depends on parent-signed C_i list and zeros"),
        ("CG2188_1_C0_zero", "all non-EH C_i(Phi0)=0 are parent-signed", "BLOCKED_NONCLAIM", "no current source supplies the full operator/coupling inventory and C0 zero proof"),
        ("CG2188_2_dC_zero", "all partial_A C_i(Phi0)=0 are parent-signed", "BLOCKED_NONCLAIM", "first-order silence remains open sector by sector"),
        ("CG2188_3_gap", "positive source-free compact exterior operator is parent-signed", "BLOCKED_NONCLAIM", "compact hair suppression cannot be claimed"),
        ("CG2188_4_PiM_lock", "Pi_M value, derivative, current-domain, commutator, and stress locks are parent-signed", "BLOCKED_NONCLAIM", "mass projector residuals remain live"),
        ("CG2188_5_envelope", "Delta_local_GR_EH_descent_abs is zero or source-bounded", "BLOCKED_NONCLAIM", "component rows are placeholders/missing source paths"),
        ("CG2188_6_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "2188 improves the theorem contract but does not close parent signatures"),
        ("CG2188_7_GitHub", "public/github update is triggered", "BLOCKED_NONCLAIM", "private goal work only; no GitHub action"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2188_0_gain",
            "F1_ZERO_LAW_DERIVED_CONDITIONALLY",
            "The exact first-order leakage expression is now explicit: double zeros of every non-EH coupling force F1=0.",
            "selected",
        ),
        (
            "DEC2188_1_gain",
            "PIM_LOCK_CONTRACT_UNIFIED",
            "Pi_M value lock, derivative silence, same-Hilbert-current domain, commutator zero, projector stress silence, and R_eq equality are gathered into one gate.",
            "selected",
        ),
        (
            "DEC2188_2_limit",
            "CURRENT_MTS_PARENT_SIGNATURES_STILL_MISSING",
            "The work has a clean theorem target, but no current source lists all C_i or signs C_i(Phi0)=0, partial_A C_i(Phi0)=0, positive gap, or full PiM lock.",
            "selected",
        ),
        (
            "DEC2188_3_next",
            "PARENT_EXTRA_SECTOR_INVENTORY_AND_COUPLING_MAP_NEXT",
            "The next best route is to build the actual parent operator inventory C_i/O_i and mark which double-zero clauses are derivable, bounded, or closure-only.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2188_0_2189",
            selection_status="selected",
            target_file="2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md",
            target_script="scripts/Y5_R2FR_parent_extra_sector_inventory_and_coupling_map_or_leakage_bounds_2189.py",
            objective="inventory every local non-EH parent operator C_i O_i that could affect metric/source/readout/PiM sectors, then test C_i(Phi0)=0, partial_A C_i(Phi0)=0, positive gap, and boundary silence sector by sector",
            success_condition="each retained extra sector is classified as parent-derived double-zero, source-bounded, or closure-only residual, with no unlabelled coupling left in the local-GR descent envelope",
            do_not_do="do not claim local GR from a generic double-zero theorem without the actual C_i inventory, do not hide PiM leakage inside measured G, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2188_1_parallel_source",
            selection_status="held_parallel",
            target_file="2189b-Y5-R2FR-PiM-commutator-and-projector-stress-bound-source-pack.md",
            target_script="scripts/Y5_R2FR_PiM_commutator_and_projector_stress_bound_source_pack_2189b.py",
            objective="if derivation stalls, acquire source-backed nonclaim bounds/normalizations for I_commutator, epsilon_projector_stress, R_eq_integral, and boundary flux",
            success_condition="at least one PiM residual row has source path, units, same-frame normalization, arena projection, and valid_for_claim=false",
            do_not_do="do not use reference-zero rows as MTS evidence or cancellation-only envelopes",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["local_envelope"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["extra_leakage"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["pim_lock"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def no_numeric_claim_rows(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        source_path = str(row.get("source_path", ""))
        value = str(row.get("value", ""))
        if "MISSING_" not in source_path and source_path != str(DOC):
            return False
        if value in {"0", "1", "1/2", "-2"} and str(row.get("score_ready", "")).lower() == "true":
            return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2188_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2188_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    dz_statuses = {row["status"] for row in rows_by_name["double_zero_contract"]}
    dz_pass = {"CONDITIONAL_THEOREM_DERIVED", "C0_ZERO_REQUIRED_NOT_PROVED", "DC_ZERO_REQUIRED_NOT_PROVED", "THEOREM_CONTRACT_PASS_CURRENT_CLAIM_FAILS"}.issubset(dz_statuses)
    validations.append(base_row(validation_id="VAL2188_02_double_zero_contract", status="PASS" if dz_pass else "FAIL", detail="F1 law and missing parent-zero clauses are explicit"))

    extra_symbols = {row["symbol"] for row in rows_by_name["extra_leakage"]}
    extra_required = {"epsilon_C0_GammaKhat", "epsilon_dC_GammaKhat", "epsilon_species_coupling", "F1_extra_linear_leakage_norm"}
    validations.append(base_row(validation_id="VAL2188_03_extra_leakage_rows", status="PASS" if extra_required.issubset(extra_symbols) and no_numeric_claim_rows(rows_by_name["extra_leakage"]) else "FAIL", detail=f"extra leakage rows={len(rows_by_name['extra_leakage'])} remain nonclaim/placeholders"))

    pim_statuses = {row["status"] for row in rows_by_name["pim_lock"]}
    pim_pass = {"PIM_VALUE_LOCK_REQUIRED_NOT_PROVED", "PIM_DERIVATIVE_LOCK_REQUIRED_NOT_PROVED", "COMMUTATOR_ZERO_REQUIRED_NOT_PROVED", "PIM_LOCK_CONTRACT_PASS_CURRENT_CLAIM_FAILS"}.issubset(pim_statuses)
    validations.append(base_row(validation_id="VAL2188_04_PiM_lock_contract", status="PASS" if pim_pass else "FAIL", detail="PiM value, derivative, commutator, stress and equality clauses are explicit"))

    envelope_symbols = {row["symbol"] for row in rows_by_name["local_envelope"]}
    envelope_required = {"Delta_local_GR_EH_descent_abs", "epsilon_PiM_value", "epsilon_DPiM", "I_commutator", "R_eq_integral"}
    envelope_pass = envelope_required.issubset(envelope_symbols) and no_numeric_claim_rows(rows_by_name["local_envelope"])
    validations.append(base_row(validation_id="VAL2188_05_local_envelope", status="PASS" if envelope_pass else "FAIL", detail=f"local-GR descent envelope rows={len(rows_by_name['local_envelope'])} remain missing/source-free/nonclaim"))

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2188_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in gate_statuses and "CONDITIONAL_PASS_GUARDRAIL" in gate_statuses else "FAIL", detail="claim gate separates theorem guardrail from blocked local-GR claim"))

    selected_decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2188_07_decision", status="PASS" if "PARENT_EXTRA_SECTOR_INVENTORY_AND_COUPLING_MAP_NEXT" in selected_decisions else "FAIL", detail="decision selects parent extra-sector inventory next"))

    next_routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2188_08_next_target", status="PASS" if "NEXT2188_0_2189" in next_routes else "FAIL", detail="2189 parent coupling map target selected"))

    validations.append(base_row(validation_id="VAL2188_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2188_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2188_11_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2188_12_formalization_clean", status="PASS" if not formalization_has_2188_artifacts() else "FAIL", detail="formalization-workbench has no 2188 artifacts"))

    remove_pycache()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2188_13_pycache_absent", status="PASS" if pycache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2188_OVERALL", status=overall, detail="2188 derives the conditional F1 double-zero law and PiM lock contract while keeping local-GR claim blocked/nonclaim"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2188 - Y5/R2FR Extra-Sector Double-Zero And PiM Lock Signature Or Residual Fill",
        "",
        "## Current Verdict",
        "",
        "2188 is a useful step forward, but not a local-GR claim.",
        "",
        "The real gain is that the local silence condition is now exact rather than vibes-based. If the parent local action contains non-EH terms",
        "",
        "`S_extra = sum_i int sqrt(-g) C_i(Phi) O_i[g,psi,Pi_M,boundary]`,",
        "",
        "then expanding around the compact local fixed point `Phi=Phi0+phi` gives the first-order leakage",
        "",
        "`F_1 = sum_i( C_i(Phi0) delta O_i + partial_A C_i(Phi0) phi^A O_i(Phi0) )`.",
        "",
        "So the clean local-GR route is:",
        "",
        "1. `C_i(Phi0)=0` for every non-EH metric/source/readout/projector coupling.",
        "2. `partial_A C_i(Phi0)=0` for every such coupling.",
        "3. the compact exterior extra-field operator has a positive source-free gap and zero boundary flux.",
        "4. `Pi_M(Phi0)=Pi_EH` and `partial_A Pi_M(Phi0)=0`, on the same Hilbert source-current domain.",
        "",
        "Under those clauses, `F_1=0` and the EH fixed-point coefficient extraction from 2185 is protected at first order. But current MTS sources still do **not** list and parent-sign every `C_i`, the positive gap, or the full PiM lock. Therefore all rows stay nonclaim.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Double-Zero Theorem Contract",
        "",
        md_table(rows_by_name["double_zero_contract"], ["contract_id", "clause", "statement", "status", "implication", "valid_for_claim"]),
        "",
        "## Extra-Sector Leakage Ledger",
        "",
        md_table(rows_by_name["extra_leakage"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## PiM Lock Contract",
        "",
        md_table(rows_by_name["pim_lock"], ["lock_id", "lock_clause", "statement", "status", "implication", "valid_for_claim"]),
        "",
        "## Local-GR Descent Envelope",
        "",
        md_table(rows_by_name["local_envelope"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "The route has improved from `maybe the extra sectors are quiet` to an exact contract:",
        "",
        "`MTS parent action -> EH fixed point -> actual C_i/O_i inventory -> C_i(Phi0)=0 -> partial_A C_i(Phi0)=0 -> positive compact gap -> PiM lock -> boundary/source/readout silence`.",
        "",
        "The next target should not repeat the generic theorem. It should inventory the actual parent non-EH operators and decide, sector by sector, whether the double-zero is derivable, source-bounded, or only a closure assumption.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "double_zero_contract": double_zero_contract_rows(),
        "extra_leakage": extra_leakage_rows(),
        "pim_lock": pim_lock_rows(),
        "local_envelope": local_envelope_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
