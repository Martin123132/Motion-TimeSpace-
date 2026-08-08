from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3817"
BRANCH = "MTS_R2FR_Y5_QBLIND_MATTER_DESCENT_PRESERVES_HILBERT_STRESS_AND_BIANCHI_CURRENT_3817"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3817_qblind_matter_descent_preserves_Hilbert_stress_and_Bianchi_current.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3816 = PCW / "3816-Y5-R2FR-parent-qblind-matter-descent-action-template-or-finite-qmatter-source-row.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_1009 = PCW / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
P_1010 = PCW / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
P_1013 = PCW / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"

CSV_3816_NEXT = OUT / "P8_Y5_R2FR_3816_NEXT_TARGET.csv"
CSV_3816_THEOREM = OUT / "P8_Y5_R2FR_3816_CHAIN_RULE_ZERO_THEOREM.csv"
CSV_3816_IMPL = OUT / "P8_Y5_R2FR_3816_LOCAL_GR_IMPLICATION_MATRIX.csv"
CSV_3792_THEOREM = OUT / "P8_Y5_R2FR_3792_SAME_CURRENT_WARD_HILBERT_THEOREM.csv"
CSV_3792_GUARD = OUT / "P8_Y5_R2FR_3792_WARD_COUNTEREXAMPLE_GUARD.csv"
CSV_3792_COMPONENTS = OUT / "P8_Y5_R2FR_3792_EPSILON_JQ_COMPONENTS.csv"
CSV_1009_CONTRACT = OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv"
CSV_1009_CLAIM = OUT / "P8_Y5_R10_1009_CLAIM_GATE.csv"
CSV_1010_THEOREM = OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv"
CSV_1010_CLAIM = OUT / "P8_Y5_R10_1010_CLAIM_GATE.csv"
CSV_1013_FLUX = OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv"
CSV_1013_OBS = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
CSV_1016_SELECTOR = OUT / "P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv"
CSV_2446_PACK = OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3817_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv",
    "ward": OUT / "P8_Y5_R2FR_3817_BIANCHI_WARD_CURRENT_AUDIT.csv",
    "hilbert_residuals": OUT / "P8_Y5_R2FR_3817_HILBERT_OWNER_RESIDUAL_ROWS.csv",
    "bianchi_residuals": OUT / "P8_Y5_R2FR_3817_BIANCHI_RESIDUAL_ROWS.csv",
    "newton_gates": OUT / "P8_Y5_R2FR_3817_NEWTON_SOURCE_BRIDGE_GATES.csv",
    "gates": OUT / "P8_Y5_R2FR_3817_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3817_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3817_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3817_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3817_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3817_0_3816_doc", P_3816, "Key result", "3816 qblind matter handoff"),
    ("SRC3817_1_3816_next", CSV_3816_NEXT, "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md", "3816 machine next target"),
    ("SRC3817_2_3816_theorem", CSV_3816_THEOREM, "QMT3816_2_hilbert_stress_not_zeroed", "Hilbert stress preservation guard"),
    ("SRC3817_3_3816_impl", CSV_3816_IMPL, "IMP3816_0_local_GR", "local GR implication gate"),
    ("SRC3817_4_3792_doc", P_3792, "Stress Ward identity", "same-current stress Ward identity source"),
    ("SRC3817_5_3792_theorem", CSV_3792_THEOREM, "SCW3792_3_total_Hilbert_stress", "total Hilbert stress theorem"),
    ("SRC3817_6_3792_guard", CSV_3792_GUARD, "WCG3792_4_boundary_flux", "Ward counterexample/boundary guard"),
    ("SRC3817_7_3792_components", CSV_3792_COMPONENTS, "EJ3792_2_lorentz", "same-current residual components"),
    ("SRC3817_8_1009_contract", CSV_1009_CONTRACT, "PCS1009_2_universal_matter", "parent sector universal matter contract"),
    ("SRC3817_9_1009_claim", CSV_1009_CLAIM, "CG1009_5_Htau_MHref_local_GR", "total parent current-chain claim gate"),
    ("SRC3817_10_1010_theorem", CSV_1010_THEOREM, "GKT1010_3_Euler_closure", "Euler/Bianchi residual closure warning"),
    ("SRC3817_11_1010_claim", CSV_1010_CLAIM, "CG1010_5_Htau_MHref_local_GR", "q_loc/local GR guardrail"),
    ("SRC3817_12_1013_flux", CSV_1013_FLUX, "PFC1013_0_same_frame_JH", "PiM/JH flux closure theorem attempt"),
    ("SRC3817_13_1013_obs", CSV_1013_OBS, "OBS1013_7_calibration_PPN_tail", "measured-GM obstruction vector"),
    ("SRC3817_14_1016_doc", P_1016, "W_source = closure(supp J_H[tau])", "parent source-worldtube selector source"),
    ("SRC3817_15_1016_contract", CSV_1016_CONTRACT, "PSC1016_1_single_observed_coframe", "single observed coframe source contract"),
    ("SRC3817_16_1016_selector", CSV_1016_SELECTOR, "PST1016_0_selector_lemma", "source worldtube selector lemma"),
    ("SRC3817_17_2446_pack", CSV_2446_PACK, "RCS2446_5_readout_PPN_tail", "local PPN/readout residual pack"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "theorem_id": "HSP3817_0_derivative_split",
            "claim_piece": "q-current derivative differs from metric derivative",
            "statement": "J_q^ordinary=delta S_ord/delta q_src can vanish while T_H^{mu nu}=2/sqrt(-g_obs) delta S_ord/delta g_obs_mu_nu remains nonzero.",
            "proof_status": "EXACT_FUNCTIONAL_DERIVATIVE_SPLIT",
            "consequence": "qblind matter descent suppresses the hidden q-source leg without deleting the ordinary stress source of GR.",
            "missing_for_claim": "none for the split; parent signature still needed for applying it to MTS.",
        },
        {
            **base,
            "theorem_id": "HSP3817_1_Hilbert_stress_preserved",
            "claim_piece": "Hilbert stress survives qblind descent",
            "statement": "For OMAT3816, metric/coframe dependence remains in S_ord through g_obs,e_obs,D_obs even when no direct q_src slot exists.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "ordinary matter can remain a metric source after J_q^ordinary is theorem-zero.",
            "missing_for_claim": "OMAT3816 parent signature and same observed metric/coframe owner.",
        },
        {
            **base,
            "theorem_id": "HSP3817_2_diffeomorphism_Ward",
            "claim_piece": "ordinary Hilbert Ward identity",
            "statement": "Diffeomorphism invariance gives nabla_mu T_ord^{mu nu}=E_psi nabla^nu psi plus force-exchange, boundary and frame terms.",
            "proof_status": "EXACT_CONDITIONAL_WARD_IDENTITY",
            "consequence": "on shell and with all exchange/boundary terms included or bounded, the stress current is conserved.",
            "missing_for_claim": "matter EOM, boundary silence, same-frame coframe, and exchange-current accounting.",
        },
        {
            **base,
            "theorem_id": "HSP3817_3_same_current_total_stress",
            "claim_piece": "charged matter and EM exchange cancels internally",
            "statement": "If one q_obs-descended source action owns charged matter, EM, binding, apparatus and interactions, Lorentz force exchange cancels inside nabla_mu T_total^{mu nu}.",
            "proof_status": "EXACT_CONDITIONAL_IMPORT_FROM_3792",
            "consequence": "EM/Poynting stress can be admitted into the same Hilbert source rather than treated as missing mass hair.",
            "missing_for_claim": "same-current source action, total domain/tail closure, Z_EM/B_Q owner and boundary silence.",
        },
        {
            **base,
            "theorem_id": "HSP3817_4_Bianchi_compatibility",
            "claim_piece": "metric equation compatibility",
            "statement": "If the metric field equation is EH-like with E_g^{mu nu}=kappa T_total^{mu nu}/2 plus retained residual R_extra, Bianchi requires nabla_mu T_total^{mu nu}+kappa^{-1}nabla_mu R_extra^{mu nu}=0.",
            "proof_status": "EXACT_CONDITIONAL_COMPATIBILITY_EQUATION",
            "consequence": "local GR can reopen only when total stress conservation and extra-sector residuals are zero or bounded.",
            "missing_for_claim": "EH coefficient, extra-sector stress closure, projector/domain no-flux and source normalization.",
        },
        {
            **base,
            "theorem_id": "HSP3817_5_Newton_scope_guard",
            "claim_piece": "conserved Hilbert stress is not yet Newtonian GM",
            "statement": "A conserved T_H source is necessary for GR/Newton recovery but not sufficient for the Poisson equation, measured GM, inverse-square calibration or PPN tail.",
            "proof_status": "EXACT_SCOPE_GUARD",
            "consequence": "3817 can preserve the GR source without claiming the weak-field Newton limit.",
            "missing_for_claim": "EH weak-field equation, kappa/G owner, Pi_M J_H flux closure, M_H_ref and calibration/PPN rows.",
        },
    ]


def ward_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "audit_id": "BWA3817_0_total_identity",
            "object": "total Hilbert stress Ward current",
            "identity": "nabla_mu T_total^{mu nu}=C_EOM^nu+C_exchange^nu+C_boundary^nu+C_frame^nu+C_extra^nu",
            "current_status": "IDENTITY_WRITTEN_COMPONENTS_OPEN",
            "zero_condition": "all C components theorem-zero or source-bounded in the same observed frame",
            "residual_if_failed": "C_Bianchi_total",
        },
        {
            **base,
            "audit_id": "BWA3817_1_matter_EOM",
            "object": "ordinary matter equations of motion",
            "identity": "C_EOM^nu=sum_A E_A nabla^nu psi_A",
            "current_status": "CONDITIONAL_ON_SAME_PARENT_ACTION",
            "zero_condition": "ordinary matter EOM hold inside the parent variational problem",
            "residual_if_failed": "C_matter_EOM",
        },
        {
            **base,
            "audit_id": "BWA3817_2_EM_exchange",
            "object": "Lorentz/Poynting exchange",
            "identity": "nabla_mu T_EM^{mu nu}+nabla_mu T_charged^{mu nu}=0 up to parent exchange terms",
            "current_status": "CONDITIONAL_FROM_3792_NOT_SIGNED",
            "zero_condition": "same current J_Q and same Hilbert source owner",
            "residual_if_failed": "C_EM_exchange + epsilon_Poynting_domain",
        },
        {
            **base,
            "audit_id": "BWA3817_3_boundary_frame",
            "object": "boundary/frame terms",
            "identity": "boundary and coframe endpoint terms vanish or are included in total source",
            "current_status": "BOUNDARY_FRAME_UNSIGNED",
            "zero_condition": "fixed reference, no-flux boundary and one observed coframe",
            "residual_if_failed": "C_boundary_flux + C_frame_mismatch",
        },
        {
            **base,
            "audit_id": "BWA3817_4_projector_readout",
            "object": "Pi_M/P_loc/readout projections",
            "identity": "projection commutes with conserved current only after fixed chain-map/domain clauses",
            "current_status": "PROJECTOR_READOUT_OPEN",
            "zero_condition": "Pi_M J_H flux closure and fixed readout/domain maps",
            "residual_if_failed": "C_projector_readout + OBS1013 obstruction vector",
        },
        {
            **base,
            "audit_id": "BWA3817_5_verdict",
            "object": "Bianchi-compatible total stress",
            "identity": "BWA3817_1 through BWA3817_4 all close in one branch",
            "current_status": "CONDITIONAL_THEOREM_NOT_STRICT_CLAIM",
            "zero_condition": "same total action plus closed boundary/projector/source domain",
            "residual_if_failed": "C_Bianchi_total retained",
        },
    ]


def hilbert_residual_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    items = [
        ("RHO3817_0_same_action", "R_H_same_action", "ordinary/EM/binding/apparatus not in one source action", "norm of stress/source mismatch between separately varied action blocks", "stress_or_source_current_units", "MISSING_TOTAL_SOURCE_ACTION_OWNER"),
        ("RHO3817_1_same_frame", "R_H_frame", "matter/clocks/orbits use different metric or coframe", "||T_H[g1]-T_H[g_obs]|| in local arena", "stress_units_or_dimensionless_after_source_norm", "MISSING_SINGLE_OBSERVED_FRAME"),
        ("RHO3817_2_metric_derivative", "R_H_metric_owner", "Hilbert stress not owned by metric variation", "||T_declared - 2/sqrt(-g) delta S/delta g||", "stress_units", "MISSING_HILBERT_VARIATION_CERTIFICATE"),
        ("RHO3817_3_nonHilbert_bypass", "R_nonHilbert_source", "non-Hilbert source current bypasses T_H", "||J_NH||/||J_H|| or arena-normalized source term", "dimensionless_or_source_current_units", "MISSING_NO_NONHILBERT_BYPASS"),
        ("RHO3817_4_EM_binding_tail", "R_EM_binding_tail", "EM, binding, apparatus or Poynting stress excluded from total source domain", "epsilon_EM_Hilbert+epsilon_binding_source+epsilon_Poynting_domain", "dimensionless_after_source_norm", "MISSING_TOTAL_DOMAIN_TAIL_CLOSURE"),
        ("RHO3817_5_total", "R_Hilbert_owner_total", "total Hilbert-owner residual", "sum_abs(R_H_same_action,R_H_frame,R_H_metric_owner,R_nonHilbert_source,R_EM_binding_tail)", "dimensionless_or_declared_stress_norm", "COMPONENTS_MISSING_OR_CONDITIONAL"),
    ]
    return [
        {
            **base,
            "residual_id": residual_id,
            "symbol": symbol,
            "failure_route": failure_route,
            "bound_formula": formula,
            "units": units,
            "current_status": status,
            "exit_requirement": "theorem-zero in the same parent branch or source-backed numeric bound",
        }
        for residual_id, symbol, failure_route, formula, units, status in items
    ]


def bianchi_residual_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    items = [
        ("CBI3817_0_matter_EOM", "C_matter_EOM", "sum_A E_A nabla^nu psi_A", "stress_divergence_units", "MISSING_PARENT_EOM_CLOSE"),
        ("CBI3817_1_EM_exchange", "C_EM_exchange", "leftover Lorentz/Poynting exchange after same-current cancellation", "stress_divergence_units", "MISSING_SAME_CURRENT_EXCHANGE_CLOSURE"),
        ("CBI3817_2_boundary_flux", "C_boundary_flux", "boundary, tail, endpoint or reference flux in stress Ward identity", "stress_flux_units", "MISSING_BOUNDARY_NO_FLUX_OR_BOUND"),
        ("CBI3817_3_extra_sector", "C_extra_sector", "non-EH/Gamma/Khat/domain/memory stress divergence not included in T_total", "stress_divergence_units", "MISSING_EXTRA_SECTOR_STRESS_CLOSURE"),
        ("CBI3817_4_projector_readout", "C_projector_readout", "[d,Pi_M]J_H, delta Pi_M stress, readout/domain commutator", "GM_flux_or_stress_units", "MISSING_PIM_CHAINMAP_READOUT_CLOSURE"),
        ("CBI3817_5_metric_equation", "C_metric_equation", "Bianchi mismatch in metric equation residual R_extra", "stress_divergence_units", "MISSING_EH_METRIC_EQUATION_OWNER"),
        ("CBI3817_6_total", "C_Bianchi_total", "sum_abs(C_matter_EOM,C_EM_exchange,C_boundary_flux,C_extra_sector,C_projector_readout,C_metric_equation)", "stress_divergence_or_dimensionless_after_norm", "COMPONENTS_MISSING_OR_CONDITIONAL"),
    ]
    return [
        {
            **base,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_status": status,
            "exit_requirement": "zero theorem or finite source-backed row with arena normalization",
        }
        for residual_id, symbol, definition, units, status in items
    ]


def newton_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "bridge_id": "NBG3817_0_metric_equation",
            "needed_bridge": "EH-like metric equation",
            "required_form": "G_mu_nu+Lambda g_mu_nu+R_extra_mu_nu = kappa T_total_mu_nu",
            "current_status": "DOWNSTREAM_NOT_DERIVED",
            "why_not_closed_by_3817": "3817 preserves T_total but does not derive the metric equation or kappa",
        },
        {
            **base,
            "bridge_id": "NBG3817_1_weak_field",
            "needed_bridge": "Poisson weak-field limit",
            "required_form": "nabla^2 Phi = 4 pi G_ref rho_H with correct sign and gauge",
            "current_status": "DOWNSTREAM_NOT_DERIVED",
            "why_not_closed_by_3817": "requires EH coefficient, weak-field gauge and source normalization",
        },
        {
            **base,
            "bridge_id": "NBG3817_2_source_charge",
            "needed_bridge": "Pi_M J_H flux/source selector",
            "required_form": "d(Pi_M J_H)=0 and W_source=closure(supp J_H[tau]) before orbital fitting",
            "current_status": "OPEN_FROM_1013_1016",
            "why_not_closed_by_3817": "projector commutator, worldtube glue and M_H_ref remain unsigned",
        },
        {
            **base,
            "bridge_id": "NBG3817_3_calibration",
            "needed_bridge": "measured GM and PPN tail",
            "required_form": "M_eff maps to observed GM without fitted circularity and PPN residuals are zero/bounded",
            "current_status": "OPEN_OBSTRUCTION_VECTOR",
            "why_not_closed_by_3817": "OBS1013 calibration/PPN tail and 2446 readout tail remain live",
        },
        {
            **base,
            "bridge_id": "NBG3817_4_verdict",
            "needed_bridge": "Newton/local-GR recovery",
            "required_form": "all NBG3817_0 through NBG3817_3 close",
            "current_status": "NOT_CLAIMED",
            "why_not_closed_by_3817": "conserved Hilbert stress is necessary but not sufficient",
        },
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    return [
        {
            **base,
            "gate_id": "GATE3817_0_sources",
            "claim": "all cited source paths exist and needles are found",
            "gate_status": "PASS_NONCLAIM" if all_sources else "FAIL",
            "reason": "source-backed Hilbert/Bianchi runner is reproducible" if all_sources else "source path or needle missing",
            "gate_pass": bool_text(all_sources),
        },
        {
            **base,
            "gate_id": "GATE3817_1_hilbert_stress_preservation",
            "claim": "qblind descent preserves possible nonzero Hilbert stress",
            "gate_status": "PASS_NONCLAIM",
            "reason": "functional derivative split and conditional theorem are explicit",
            "gate_pass": "true",
        },
        {
            **base,
            "gate_id": "GATE3817_2_bianchi_total_conservation",
            "claim": "total stress is conserved in the current corpus",
            "gate_status": "BLOCKED",
            "reason": "same-current action, boundary silence, extra-sector stress and projector/readout closure are unsigned",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3817_3_newton_poisson_bridge",
            "claim": "Newton/Poisson weak-field source bridge is derived",
            "gate_status": "BLOCKED",
            "reason": "EH coefficient, Pi_M J_H flux closure, M_H_ref and calibration/PPN tail remain open",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3817_4_local_GR_claim",
            "claim": "local GR is claimed",
            "gate_status": "BLOCKED",
            "reason": "3817 proves a necessary compatibility theorem only",
            "gate_pass": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "decision_id": "DEC3817_0_preserve_stress_route",
            "decision": "keep qblind ordinary matter descent because it silences hidden q-current without deleting Hilbert stress",
            "because": "this is the cleanest way to reduce to GR locally without adding a tuned fifth-force coupling",
            "next_action": "derive the EH metric equation and weak-field Poisson bridge",
        },
        {
            **base,
            "decision_id": "DEC3817_1_total_stress_needed",
            "decision": "require total Hilbert stress, not matter-only stress",
            "because": "EM, binding, apparatus and Poynting sectors can be real gravitational sources",
            "next_action": "carry same-current/total-domain clauses into the next EH bridge",
        },
        {
            **base,
            "decision_id": "DEC3817_2_no_Newton_shortcut",
            "decision": "do not promote conserved T_H into measured Newtonian GM",
            "because": "source selector, Pi_M flux closure, M_H_ref and calibration remain separate gates",
            "next_action": "build 3818 Poisson/source-normalization bridge or finite residual rows",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md",
            "target_script": "scripts/Y5_R2FR_3818_EH_metric_equation_to_weak_field_Poisson_source_normalization_bridge.py",
            "objective": "Derive or bound the next necessary bridge from conserved Hilbert stress to Newton/local GR: EH-like metric equation, kappa/G owner, weak-field Poisson limit, Pi_M J_H source selector, and no fitted-GM circularity; if any clause fails, emit finite R_EH_owner, R_Poisson_norm and R_GM_calibration rows.",
            "success_gate": "A theorem chain shows conserved T_H sources an EH metric equation with the correct Poisson limit and source normalization, or every missing clause becomes a finite residual row with units.",
            "avoid": "do not claim local GR; do not use orbital GM to prove source normalization; do not hide projector/readout tails; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_QBLIND_MATTER_PRESERVES_HILBERT_STRESS_BIANCHI_ROWS_BUILT",
            "summary": "3817 proves the exact functional-derivative split that qblind ordinary matter can have J_q^ordinary=0 while retaining nonzero Hilbert stress, writes the conditional Ward/Bianchi conservation audit for total stress, installs R_Hilbert_owner and C_Bianchi residual rows, and keeps Newton/local-GR claims blocked until EH metric equation, Poisson limit, Pi_M J_H source normalization and calibration gates close.",
            "valid_for_claim": "false",
        }
    ]


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    status = grouped["status"][0]
    validation = grouped.get("validation", [])
    validation_pass = all(row.get("result") == "PASS" for row in validation) if validation else False
    text = f"""# 3817 - Q-Blind Matter Descent Preserves Hilbert Stress And Bianchi Current

## Status

- Status: `{status["status"]}`
- Claim level: private, nonclaim theorem bridge.
- Validation pass: `{bool_text(validation_pass)}`
- Key result: q-blind ordinary matter can silence `J_q^ordinary` without deleting `T_H`.

## Core Theorem

3816 proved the hidden source-current branch:

```text
J_q^ordinary[v_q] = delta_vq S_ord = 0
```

3817 adds the necessary guard:

```text
J_q^ordinary = delta S_ord / delta q_src
T_H^{{mu nu}} = (2/sqrt(-g_obs)) delta S_ord / delta g_obs_mu_nu

J_q^ordinary = 0 does not imply T_H^{{mu nu}} = 0.
```

So the local q-fifth-force source can vanish while ordinary matter still gravitates through the observed metric.

## Ward/Bianchi Bridge

The conditional conservation identity is:

```text
nabla_mu T_total^{{mu nu}}
  = C_matter_EOM^nu
  + C_EM_exchange^nu
  + C_boundary_flux^nu
  + C_frame_mismatch^nu
  + C_extra_sector^nu
  + C_projector_readout^nu
```

If the same parent source action owns charged matter, EM, binding, apparatus and boundaries, the Lorentz/Poynting exchange cancels internally as in 3792. If boundary, frame, extra-sector and projector/readout terms are zero or bounded, the total Hilbert stress is Bianchi-compatible.

## What Is Not Claimed

This is not yet Newtonian gravity. Conserved Hilbert stress is necessary, but it does not by itself prove:

- the EH-like metric equation;
- the value or universality of `kappa/G`;
- the weak-field Poisson equation;
- `Pi_M J_H` compact-exterior flux closure;
- `M_H_ref`, measured-GM calibration, or PPN readout stability.

## Finite Fallbacks

3817 emits two nonclaim residual packs:

```text
R_Hilbert_owner_total =
  R_H_same_action + R_H_frame + R_H_metric_owner
  + R_nonHilbert_source + R_EM_binding_tail

C_Bianchi_total =
  C_matter_EOM + C_EM_exchange + C_boundary_flux
  + C_extra_sector + C_projector_readout + C_metric_equation
```

These are the honest fallback rows if the theorem clauses remain unsigned.

## Next Target

`3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md`

Next we attack the real GR/Newton bridge: conserved `T_H` must source an EH-like metric equation with the correct weak-field Poisson limit, source normalization and no fitted-GM circularity.

## Machine Outputs

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_SOURCE_REGISTER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_BIANCHI_WARD_CURRENT_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_HILBERT_OWNER_RESIDUAL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_BIANCHI_RESIDUAL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_NEWTON_SOURCE_BRIDGE_GATES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_CLAIM_GATES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_DECISION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_NEXT_TARGET.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3817_STATUS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3817_VALIDATION.csv`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("# Local GR Coupling Spine - Current State After 3816", "# Local GR Coupling Spine - Current State After 3817")
    new_para = (
        "`3817` proves the necessary compatibility bridge after qblind matter descent: `J_q^ordinary=0` is a derivative with respect to the hidden q-source slot and does not set the metric Hilbert stress `T_H` to zero. It writes the Ward/Bianchi total-stress audit, imports the same-current EM/Poynting exchange cancellation from 3792, and emits finite `R_Hilbert_owner_total` and `C_Bianchi_total` residual rows when same-action/frame/boundary/projector clauses are unsigned. Newton/local GR remains blocked until the EH metric equation, Poisson weak-field limit, Pi_M J_H source selector, and measured-GM calibration are derived or bounded.\n"
    )
    if "`3817` proves the necessary compatibility bridge" not in text:
        anchor = (
            "`3816` writes the parent qblind ordinary-matter action template `OMAT3816` and proves the exact chain-rule theorem: if ordinary matter descends through observed matter representation data and the hidden q-source variation leaves that data fixed, then `J_q^ordinary=0`. The key guardrail is that this does not delete matter: `T_H^{mu nu}=2/sqrt(-g_obs) delta S_ord/delta g_obs` can remain nonzero and source GR/Newton. If the template is unsigned, the failure is now a finite `C_qmatter_total` residual decomposition rather than a vague coupling hole.\n"
        )
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + new_para)
        else:
            text += "\n" + new_para

    history_entry = (
        "- `3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md`: proves qblind matter descent can silence hidden `J_q` without deleting Hilbert stress, writes the Ward/Bianchi total-stress audit, emits `R_Hilbert_owner_total` and `C_Bianchi_total`, and selects the EH-to-Poisson source-normalization bridge next."
    )
    if history_entry not in text:
        marker = "## Next Target"
        if marker in text:
            text = text.replace(marker, history_entry + "\n\n" + marker, 1)
        else:
            text += "\n" + history_entry + "\n"

    old_target = (
        "`3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md`\n\n"
        "Target: prove or bound the next GR bridge. Show that qblind ordinary matter descent sets the hidden q-current to zero while preserving nonzero Hilbert stress, Ward/Bianchi conservation, and the weak-field source needed for GR/Newton; if it fails, emit finite `R_Hilbert_owner` and `C_Bianchi` rows.\n\n"
        "This is the best next move because 3816 only wins if q-source silence does not accidentally delete the ordinary stress source of GR."
    )
    new_target = (
        "`3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md`\n\n"
        "Target: derive or bound the next necessary bridge from conserved Hilbert stress to Newton/local GR: EH-like metric equation, `kappa/G` owner, weak-field Poisson limit, `Pi_M J_H` source selector, and no fitted-GM circularity. If any clause fails, emit finite `R_EH_owner`, `R_Poisson_norm`, and `R_GM_calibration` rows.\n\n"
        "This is the best next move because 3817 preserves the source stress, but the theory still has to prove that this stress sources the observed metric with the correct Newtonian normalization."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3817_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv",
        "P8_Y5_R2FR_3817_BIANCHI_WARD_CURRENT_AUDIT.csv",
        "P8_Y5_R2FR_3817_HILBERT_OWNER_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_3817_BIANCHI_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_3817_NEWTON_SOURCE_BRIDGE_GATES.csv",
        "P8_Y5_R2FR_3817_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3817_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3817_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3817_STATUS.csv",
        "P8_Y5_BRR545_3817_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3817*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3817 markdown document written"),
        ("hilbert_preserved_theorem", any(row["theorem_id"] == "HSP3817_1_Hilbert_stress_preserved" for row in grouped["theorem"]), "Hilbert stress preservation theorem emitted"),
        ("scope_guard_newton", any(row["theorem_id"] == "HSP3817_5_Newton_scope_guard" for row in grouped["theorem"]), "Newton scope guard emitted"),
        ("bianchi_total_row", any(row["residual_id"] == "CBI3817_6_total" for row in grouped["bianchi_residuals"]), "C_Bianchi total row emitted"),
        ("hilbert_owner_total_row", any(row["residual_id"] == "RHO3817_5_total" for row in grouped["hilbert_residuals"]), "R_Hilbert owner total row emitted"),
        ("newton_gate_blocked", any(row["bridge_id"] == "NBG3817_4_verdict" and row["current_status"] == "NOT_CLAIMED" for row in grouped["newton_gates"]), "Newton/local GR bridge not claimed"),
        ("claim_gates_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("next_target_selected", grouped["next_target"][0]["target_doc"].startswith("3818-Y5-R2FR-EH-metric-equation"), "3818 EH-to-Poisson bridge selected"),
        ("spine_updated", "Current State After 3817" in spine_text and "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md" in spine_text, "live spine updated to 3817 and 3818 target"),
        ("formalization_clean", not fwb_hits, "no 3817 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "ward": ward_rows(timestamp),
        "hilbert_residuals": hilbert_residual_rows(timestamp),
        "bianchi_residuals": bianchi_residual_rows(timestamp),
        "newton_gates": newton_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
