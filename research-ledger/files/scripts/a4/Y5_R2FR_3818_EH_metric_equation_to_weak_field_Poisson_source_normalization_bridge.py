from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3818"
BRANCH = "MTS_R2FR_Y5_EH_METRIC_EQUATION_TO_WEAK_FIELD_POISSON_SOURCE_NORMALIZATION_BRIDGE_3818"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3818_EH_metric_equation_to_weak_field_Poisson_source_normalization_bridge.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3817 = PCW / "3817-Y5-R2FR-qblind-matter-descent-preserves-Hilbert-stress-and-Bianchi-current.md"
P_1006 = PCW / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"
P_1013 = PCW / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
P_1016 = PCW / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"

CSV_3817_NEXT = OUT / "P8_Y5_R2FR_3817_NEXT_TARGET.csv"
CSV_3817_THEOREM = OUT / "P8_Y5_R2FR_3817_HILBERT_STRESS_PRESERVATION_THEOREM.csv"
CSV_3817_NEWTON = OUT / "P8_Y5_R2FR_3817_NEWTON_SOURCE_BRIDGE_GATES.csv"
CSV_3377_THEOREM = OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv"
CSV_3434_POISSON = OUT / "P8_Y5_R2FR_3434_SOURCE_NORMALIZED_POISSON_LIMIT_THEOREM.csv"
CSV_3499_CHAIN = OUT / "P8_Y5_R2FR_3499_POISSON_NEWTON_THEOREM_CHAIN.csv"
CSV_3530_PNG = OUT / "P8_Y5_R2FR_3530_POISSON_PPN_GATES.csv"
CSV_3530_KG = OUT / "P8_Y5_R2FR_3530_KAPPA_G_CONTRACT.csv"
CSV_3755_KAPPA = OUT / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv"
CSV_3758_KAPPA = OUT / "P8_Y5_R2FR_3758_KAPPA_SUPERSELECTION_ACTION_CONTRACT.csv"
CSV_3768_KAPPA = OUT / "P8_Y5_R2FR_3768_KAPPA_EH_COEFFICIENT_THEOREM.csv"
CSV_3772_NEWTON = OUT / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv"
CSV_3772_ATTEMPT = OUT / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_ZERO_ATTEMPT.csv"
CSV_1006_CLAIM = OUT / "P8_Y5_R10_1006_CLAIM_GATE.csv"
CSV_1006_SCHEMA = OUT / "P8_Y5_R10_1006_DENOMINATOR_SOURCE_SCHEMA.csv"
CSV_1013_FLUX = OUT / "P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv"
CSV_1013_OBS = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
CSV_1016_CONTRACT = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
CSV_2446_PACK = OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3818_SOURCE_REGISTER.csv",
    "eh_template": OUT / "P8_Y5_R2FR_3818_EH_METRIC_EQUATION_TEMPLATE.csv",
    "poisson": OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv",
    "kappa": OUT / "P8_Y5_R2FR_3818_KAPPA_GREF_POLICY_AND_RESIDUALS.csv",
    "source_norm": OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv",
    "residuals": OUT / "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3818_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3818_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3818_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3818_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3818_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3818_0_3817_doc", P_3817, "EH-like metric equation", "3817 handoff to EH/Poisson bridge"),
    ("SRC3818_1_3817_next", CSV_3817_NEXT, "3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md", "3817 machine next target"),
    ("SRC3818_2_3817_theorem", CSV_3817_THEOREM, "HSP3817_5_Newton_scope_guard", "Newton scope guard"),
    ("SRC3818_3_3817_newton", CSV_3817_NEWTON, "NBG3817_0_metric_equation", "3817 bridge gates"),
    ("SRC3818_4_3377_theorem", CSV_3377_THEOREM, "WFS3377_2_EH_to_Poisson", "EH to Poisson coefficient theorem"),
    ("SRC3818_5_3434_poisson", CSV_3434_POISSON, "PL3434_0_field_equation", "source-normalized Poisson theorem"),
    ("SRC3818_6_3499_chain", CSV_3499_CHAIN, "PNC3499_2_EH_00_to_Poisson", "Poisson/Newton theorem chain"),
    ("SRC3818_7_3530_png", CSV_3530_PNG, "PNG3530_3_no_GM_smuggling", "Poisson/PPN anti-circular gate"),
    ("SRC3818_8_3530_kappa", CSV_3530_KG, "KG3530_2_calibrated_GN", "kappa/G calibrated constant contract"),
    ("SRC3818_9_3755_kappa", CSV_3755_KAPPA, "KT3755_6_constant_offset", "absolute G overclaim policy"),
    ("SRC3818_10_3758_kappa", CSV_3758_KAPPA, "KS3758_5_absolute_G_policy", "kappa superselection contract"),
    ("SRC3818_11_3768_kappa", CSV_3768_KAPPA, "KET3768_6_Newton_calibration_meaning", "EH coefficient leak Newton interface"),
    ("SRC3818_12_3772_newton", CSV_3772_NEWTON, "NSH3772_4_three_mass_identity", "three-mass Newton theorem"),
    ("SRC3818_13_3772_attempt", CSV_3772_ATTEMPT, "NZA3772_8_verdict", "Newton zero attempt verdict"),
    ("SRC3818_14_1006_doc", P_1006, "orbital GM substitution is explicitly rejected", "M_H_ref anti-circularity source"),
    ("SRC3818_15_1006_claim", CSV_1006_CLAIM, "CG1006_1_orbital_GM_substitution", "M_H_ref claim gate"),
    ("SRC3818_16_1006_schema", CSV_1006_SCHEMA, "MHS1006_2_anti_circularity", "M_H_ref anti-circularity schema"),
    ("SRC3818_17_1013_doc", P_1013, "compact-exterior closure", "PiM/JH flux closure source"),
    ("SRC3818_18_1013_flux", CSV_1013_FLUX, "PFC1013_8_verdict", "PiM/JH flux verdict"),
    ("SRC3818_19_1013_obs", CSV_1013_OBS, "OBS1013_7_calibration_PPN_tail", "measured-GM obstruction vector"),
    ("SRC3818_20_1016_contract", CSV_1016_CONTRACT, "PSC1016_5_dressed_source_charge", "dressed source charge contract"),
    ("SRC3818_21_2446_pack", CSV_2446_PACK, "RCS2446_5_readout_PPN_tail", "PPN/readout source residual"),
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


def eh_template_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "template_id": "EHP3818_0_public_metric_equation",
            "piece": "EH-like public metric equation",
            "mathematical_form": "G_mu_nu[g_obs]+Lambda g_mu_nu+DeltaE_res_mu_nu = kappa_0 T_total_mu_nu",
            "derivation_status": "EXACT_CONDITIONAL_TEMPLATE",
            "meaning": "conserved Hilbert stress can source the observed metric only inside this public metric equation branch",
            "missing_for_claim": "parent normal form, EH leading operator, residual DeltaE closure",
        },
        {
            **base,
            "template_id": "EHP3818_1_kappa_owner",
            "piece": "single kappa/G owner",
            "mathematical_form": "kappa_0 = 8*pi*G_ref/c^4, fixed before source/readout selection",
            "derivation_status": "CALIBRATED_OR_SUPERSELECTED_CONSTANT_ALLOWED",
            "meaning": "the absolute measured value of G_ref may be empirical; the required theorem is universality and no post-readout drift/refit",
            "missing_for_claim": "parent-signed kappa owner or accepted calibrated-constant branch plus product-lock residuals",
        },
        {
            **base,
            "template_id": "EHP3818_2_total_source",
            "piece": "total Hilbert source",
            "mathematical_form": "T_total = T_matter + T_EM + T_binding + T_apparatus + T_boundary/included tails",
            "derivation_status": "CONDITIONAL_FROM_3792_3817",
            "meaning": "the source is total stress in the same observed frame, not a matter-only mask",
            "missing_for_claim": "same-current total source action, domain/tail closure",
        },
        {
            **base,
            "template_id": "EHP3818_3_residual_branch",
            "piece": "finite metric-equation residual",
            "mathematical_form": "R_EH_owner := ||DeltaE_res|| plus coefficient/operator/source-frame defects",
            "derivation_status": "FINITE_FALLBACK_REQUIRED_IF_UNSIGNED",
            "meaning": "if the EH equation is not parent-signed, the failure is scored as a residual operator, not hidden in G or M",
            "missing_for_claim": "component zero theorems or numeric source-backed bounds",
        },
    ]


def poisson_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "derivation_id": "POI3818_0_linearized_00",
            "claim_piece": "EH 00 equation to Poisson",
            "formula": "g_00=-(1+2 Phi/c^2), G_00^(1)=2 nabla^2 Phi/c^2, T_00=rho_H c^2, kappa_0=8*pi*G_ref/c^4 => nabla^2 Phi=4*pi*G_ref rho_H",
            "status": "EXACT_CONDITIONAL_WEAK_FIELD_ALGEBRA",
            "missing_for_claim": "EH-only operator, sign/gauge convention, same-frame nonrelativistic Hilbert source",
            "scope": "first-order Newton/Poisson only",
        },
        {
            **base,
            "derivation_id": "POI3818_1_source_integral",
            "claim_piece": "Poisson source mass",
            "formula": "M_H_ref = int_D rho_H d^3x = c^-2(H_tau[S_outer]-H_ref)",
            "status": "CONDITIONAL_SOURCE_NORMALIZATION",
            "missing_for_claim": "positive same-frame M_H_ref, H_tau integrability, fixed H_ref, Pi_M J_H equality",
            "scope": "source normalization, not orbital fitting",
        },
        {
            **base,
            "derivation_id": "POI3818_2_residual_poisson",
            "claim_piece": "Poisson residual equation",
            "formula": "nabla^2 Phi = 4*pi*G_ref rho_H + S_EH + S_source + S_boundary + S_domain + S_nonEH + S_readout",
            "status": "FINITE_RESIDUAL_FORM",
            "missing_for_claim": "all residual source profiles zero or bounded",
            "scope": "fallback when clean Poisson bridge fails",
        },
        {
            **base,
            "derivation_id": "POI3818_3_gauss_inverse_square",
            "claim_piece": "Gauss exterior to inverse-square potential",
            "formula": "oint grad Phi.dS = 4*pi*G_ref M_H_ref + residual_flux; exterior Phi=-G_ref M_H_ref/r + deltaPhi_res",
            "status": "EXACT_CONDITIONAL_GAUSS_TEMPLATE",
            "missing_for_claim": "source-free exterior annulus, no residual monopole, no range/radial/boundary hair",
            "scope": "first-order inverse-square only",
        },
        {
            **base,
            "derivation_id": "POI3818_4_scope_guard",
            "claim_piece": "Poisson is not full local GR",
            "formula": "Poisson success does not imply gamma=1, beta=1, alpha_i=0, xi=0",
            "status": "NO_OVERCLAIM_RULE",
            "missing_for_claim": "second-order PPN/source/operator gates",
            "scope": "prevents Newton pass becoming local-GR pass",
        },
    ]


def kappa_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "kappa_id": "KGP3818_0_constant_policy",
            "piece": "Newton constant policy",
            "statement": "Do not try to derive the numerical value of G_ref here; require one fixed parent/calibrated coupling used everywhere.",
            "status": "POLICY_AND_DIMENSIONAL_GUARD",
            "residual_if_missing": "epsilon_Gref_match",
        },
        {
            **base,
            "kappa_id": "KGP3818_1_local_constancy",
            "piece": "local kappa/G drift",
            "statement": "If kappa is q_obs-owned or global/superselected, local hidden/source/time/range derivatives vanish by chain rule or signature.",
            "status": "EXACT_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "residual_if_missing": "delta_kappa + beta_kappa,A zeta^A",
        },
        {
            **base,
            "kappa_id": "KGP3818_2_product_lock",
            "piece": "G_eff product lock",
            "statement": "D_X ln G_eff = D_X ln G_ref + D_X ln w_common + D_X ln ell_J + D_X ln R_frame + retained source terms.",
            "status": "EXACT_BOOKKEEPING_IDENTITY",
            "residual_if_missing": "Delta_coupling_baseline_abs",
        },
        {
            **base,
            "kappa_id": "KGP3818_3_no_cancellation",
            "piece": "no cancellation between coupling and source mass",
            "statement": "G drift, source-mass drift, frame normalization, Poisson normalization and readout residuals must be absolute-summed unless a parent identity signs their cancellation.",
            "status": "NO_CANCELLATION_GUARD",
            "residual_if_missing": "R_GM_calibration",
        },
    ]


def source_norm_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "guard_id": "SNG3818_0_MHref",
            "guard": "positive same-frame M_H_ref",
            "required_form": "M_H_ref=H_tau[S_link]-H_ref>0 with tau/coframe/reference/source paths",
            "current_status": "BLOCKED_FROM_1006",
            "why": "H_tau/H_ref values, integrability, tau/coframe lock and source path are missing",
        },
        {
            **base,
            "guard_id": "SNG3818_1_PiM_JH",
            "guard": "Pi_M J_H compact-exterior closure",
            "required_form": "d(Pi_M J_H)=0 and [d,Pi_M]J_H=0 or finite obstruction vector",
            "current_status": "BLOCKED_FROM_1013",
            "why": "Pi_M origin, commutator, extra projection, worldtube glue and calibration are unsigned",
        },
        {
            **base,
            "guard_id": "SNG3818_2_worldtube_selector",
            "guard": "pre-readout source worldtube",
            "required_form": "W_source=closure(supp J_H[tau]) with fixed linking surfaces before orbital fitting",
            "current_status": "CONDITIONAL_FROM_1016_NOT_SIGNED",
            "why": "parent action, same-frame source current, compactness and fixed reference remain open",
        },
        {
            **base,
            "guard_id": "SNG3818_3_no_orbital_GM_import",
            "guard": "anti-circular measured-GM policy",
            "required_form": "GM_orbit/G_ref cannot fill M_H_ref unless Poisson/Gauss/orbital bridge is already derived",
            "current_status": "GUARDRAIL_PASS_NONCLAIM",
            "why": "orbital agreement measures product GM and cannot separately prove G or M",
        },
        {
            **base,
            "guard_id": "SNG3818_4_PPN_tail",
            "guard": "PPN/readout stability",
            "required_form": "Delta_cal, Delta_PPN, gamma, beta and preferred-frame/source tails zero or bounded",
            "current_status": "OPEN_FROM_1013_2446_3530",
            "why": "first-order Poisson does not close second-order/local-GR residuals",
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    items = [
        ("R3818_0_EH_owner", "R_EH_owner", "EH metric equation owner/operator residual", "||DeltaE_res|| + |delta kappa| operator contribution", "stress_operator_or_dimensionless_after_norm", "MISSING_PARENT_EH_NORMAL_FORM"),
        ("R3818_1_Poisson_norm", "R_Poisson_norm", "weak-field Poisson coefficient/source residual", "|nabla^2 Phi - 4*pi*G_ref*rho_H| in arena norm", "potential_laplacian_or_dimensionless_after_norm", "MISSING_EH_POISSON_SOURCE_LOCK"),
        ("R3818_2_GM_calibration", "R_GM_calibration", "measured-GM anti-circular residual", "|delta ln mu_obs - delta ln G_ref - delta ln M_H_ref| plus frame/range/readout terms", "dimensionless_or_rate_units", "MISSING_GM_SPLIT_SOURCE_NORMALIZATION"),
        ("R3818_3_PiM_flux", "R_PiM_JH_flux", "projected Hilbert current flux obstruction", "abs(-Pi_M dJ_extra)+abs([d,Pi_M]J_H)+abs(A_parent)+abs(R_eq)+abs(B_zero_flux)", "GM_flux_or_dimensionless_after_MHref", "MISSING_PIM_JH_FLUX_CLOSURE"),
        ("R3818_4_PPN_readout", "R_PPN_readout_tail", "PPN/readout tail after Poisson", "Delta_cal + Delta_PPN + gamma/beta/preferred-frame residual vector", "dimensionless_vector", "MISSING_PPN_READOUT_STABILITY"),
        ("R3818_5_total", "R_EH_Poisson_GM_total", "total EH-to-Newton bridge residual", "sum_abs(R_EH_owner,R_Poisson_norm,R_GM_calibration,R_PiM_JH_flux,R_PPN_readout_tail)", "declared_mixed_norm_or_componentwise", "COMPONENTS_MISSING_OR_CONDITIONAL"),
    ]
    return [
        {
            **base,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "units": units,
            "current_status": status,
            "exit_requirement": "theorem-zero in one branch or source-backed numeric/component bound",
        }
        for residual_id, symbol, definition, formula, units, status in items
    ]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    return [
        {
            **base,
            "gate_id": "GATE3818_0_sources",
            "claim": "all cited source paths exist and needles are found",
            "gate_status": "PASS_NONCLAIM" if all_sources else "FAIL",
            "reason": "source-backed EH/Poisson runner is reproducible" if all_sources else "source path or needle missing",
            "gate_pass": bool_text(all_sources),
        },
        {
            **base,
            "gate_id": "GATE3818_1_EH_to_Poisson_algebra",
            "claim": "EH 00 weak-field algebra gives Poisson coefficient conditionally",
            "gate_status": "PASS_NONCLAIM",
            "reason": "linearized EH-to-Poisson formula is written as an exact conditional theorem",
            "gate_pass": "true",
        },
        {
            **base,
            "gate_id": "GATE3818_2_kappa_G_policy",
            "claim": "absolute G value is derived",
            "gate_status": "BLOCKED_SCOPE",
            "reason": "GR does not derive G; MTS needs a universal fixed/calibrated owner, not a numeric prediction here",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3818_3_source_normalization",
            "claim": "M_H_ref/Pi_M J_H source normalization is owned",
            "gate_status": "BLOCKED",
            "reason": "M_H_ref, Pi_M J_H flux closure, source selector and calibration remain unsigned",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3818_4_Newton_claim",
            "claim": "Newtonian GM recovery is claimed",
            "gate_status": "BLOCKED",
            "reason": "Poisson algebra is conditional and source normalization/calibration gates are open",
            "gate_pass": "false",
        },
        {
            **base,
            "gate_id": "GATE3818_5_local_GR_claim",
            "claim": "full local GR/PPN is claimed",
            "gate_status": "BLOCKED",
            "reason": "first-order Poisson is not full PPN/local GR",
            "gate_pass": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {"timestamp_utc": timestamp, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT, "valid_for_claim": "false", "claim_allowed": "false"}
    return [
        {
            **base,
            "decision_id": "DEC3818_0_EH_Poisson_theorem",
            "decision": "keep the EH-to-Poisson theorem as an exact conditional bridge",
            "because": "the coefficient map from kappa to 4*pi*G is clean once EH normal form and Hilbert source are owned",
            "next_action": "attack source normalization rather than re-derive linearized GR again",
        },
        {
            **base,
            "decision_id": "DEC3818_1_G_policy",
            "decision": "do not waste effort deriving the measured number G from GR",
            "because": "the serious requirement is one parent-fixed/calibrated coupling with no arena-by-arena refit",
            "next_action": "carry kappa/G product-lock residuals into source-normalization scoring",
        },
        {
            **base,
            "decision_id": "DEC3818_2_next_MHref_PiM",
            "decision": "make M_H_ref and Pi_M J_H source selector the next hard target",
            "because": "without a source mass owner, Poisson algebra can still be just fitted GM in disguise",
            "next_action": "derive or fill source selector/MHref/GM calibration rows in 3819",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md",
            "target_script": "scripts/Y5_R2FR_3819_MHref_PiM_JH_source_selector_and_GM_anti_circularity_bridge.py",
            "objective": "Derive or bound the source normalization gate exposed by 3818: positive same-frame M_H_ref, parent-owned Pi_M J_H flux closure, source worldtube selector, and measured-GM anti-circularity; if not closed, emit finite M_H_ref/PiM/GM residual rows ready for empirical scoring.",
            "success_gate": "Either M_H_ref and Pi_M J_H are parent-owned enough to feed Poisson/Gauss without orbital-GM laundering, or every failure is converted to finite residual rows with units and no-cancellation guards.",
            "avoid": "do not claim Newton/local GR; do not import orbital GM as source mass; do not hide boundary/projector tails; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_EH_TO_POISSON_THEOREM_AND_SOURCE_NORMALIZATION_GATES_BUILT",
            "summary": "3818 derives the exact conditional EH 00-to-Poisson coefficient bridge, states the honest G policy that the numeric Newton constant can be calibrated but must be one parent-fixed coupling, separates kappa/G product-lock residuals from source mass, and keeps Newton/local-GR claims blocked until M_H_ref, Pi_M J_H flux closure, source selector and measured-GM anti-circularity close.",
            "valid_for_claim": "false",
        }
    ]


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    status = grouped["status"][0]
    validation = grouped.get("validation", [])
    validation_pass = all(row.get("result") == "PASS" for row in validation) if validation else False
    text = f"""# 3818 - EH Metric Equation To Weak-Field Poisson Source-Normalization Bridge

## Status

- Status: `{status["status"]}`
- Claim level: private, nonclaim theorem bridge.
- Validation pass: `{bool_text(validation_pass)}`
- Main result: the EH-to-Poisson algebra is clean conditionally; the live blocker is source normalization, not the linearized GR calculation.

## EH To Poisson

The conditional weak-field bridge is:

```text
G_mu_nu + Lambda g_mu_nu + DeltaE_res_mu_nu = kappa_0 T_total_mu_nu
kappa_0 = 8*pi*G_ref/c^4
g_00 = -(1 + 2 Phi/c^2)
G_00^(1) = 2 nabla^2 Phi/c^2
T_00 = rho_H c^2

=> nabla^2 Phi = 4*pi*G_ref rho_H
```

This is exact conditional algebra, not a local-GR claim. It requires the EH operator, sign/gauge convention, same-frame Hilbert source, and residual operator silence or finite bounds.

## G Policy

We do **not** need to derive the numerical value of Newton's constant to reduce to GR. GR itself calibrates `G`. The MTS requirement is stricter in a different way:

```text
one fixed parent/calibrated G_ref
one Hilbert/Hamiltonian source mass
no arena-by-arena fitted GM absorption
```

If `kappa/G` is not parent-owned or superselected, its leakage enters finite product-lock residuals rather than being hidden in `GM`.

## Source Normalization Gate

The Poisson source must be:

```text
M_H_ref = int_D rho_H d^3x
        = c^-2 (H_tau[S_outer] - H_ref)
```

and the exterior source selector must satisfy:

```text
d(Pi_M J_H)=0
W_source = closure(supp J_H[tau])
```

Current status: this is still blocked by `M_H_ref`, `Pi_M` origin, commutator, worldtube glue, boundary/reference and measured-GM calibration.

## Finite Fallbacks

3818 emits:

```text
R_EH_Poisson_GM_total =
  R_EH_owner + R_Poisson_norm + R_GM_calibration
  + R_PiM_JH_flux + R_PPN_readout_tail
```

These rows keep the bridge scoreable without claiming Newton or local GR early.

## Next Target

`3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md`

Next we attack the actual remaining throat: `M_H_ref`, `Pi_M J_H`, worldtube selector, and anti-circular measured-GM calibration.

## Machine Outputs

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_SOURCE_REGISTER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_EH_METRIC_EQUATION_TEMPLATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_KAPPA_GREF_POLICY_AND_RESIDUALS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_CLAIM_GATES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_DECISION_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_NEXT_TARGET.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3818_STATUS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3818_VALIDATION.csv`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("# Local GR Coupling Spine - Current State After 3817", "# Local GR Coupling Spine - Current State After 3818")
    new_para = (
        "`3818` derives the exact conditional EH-to-Poisson coefficient bridge: with `G_00^(1)=2 nabla^2 Phi/c^2`, `T_00=rho_H c^2`, and `kappa_0=8*pi*G_ref/c^4`, the public EH branch gives `nabla^2 Phi=4*pi*G_ref rho_H`. It also locks the honest policy: MTS does not need to derive the numerical value of `G_ref` here, but it must own one fixed/calibrated coupling that cannot absorb source-mass errors. Newton/local GR remains blocked by `M_H_ref`, `Pi_M J_H` flux closure, source worldtube selection, measured-GM anti-circularity, and PPN/readout tails.\n"
    )
    if "`3818` derives the exact conditional EH-to-Poisson coefficient bridge" not in text:
        anchor = (
            "`3817` proves the necessary compatibility bridge after qblind matter descent: `J_q^ordinary=0` is a derivative with respect to the hidden q-source slot and does not set the metric Hilbert stress `T_H` to zero. It writes the Ward/Bianchi total-stress audit, imports the same-current EM/Poynting exchange cancellation from 3792, and emits finite `R_Hilbert_owner_total` and `C_Bianchi_total` residual rows when same-action/frame/boundary/projector clauses are unsigned. Newton/local GR remains blocked until the EH metric equation, Poisson weak-field limit, Pi_M J_H source selector, and measured-GM calibration are derived or bounded.\n"
        )
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + new_para)
        else:
            text += "\n" + new_para

    history_entry = (
        "- `3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md`: derives the conditional EH 00-to-Poisson coefficient map, states the fixed/calibrated `G_ref` policy, emits `R_EH_Poisson_GM_total`, and selects `M_H_ref`/`Pi_M J_H`/GM anti-circularity as the next source-normalization target."
    )
    if history_entry not in text:
        marker = "## Next Target"
        if marker in text:
            text = text.replace(marker, history_entry + "\n\n" + marker, 1)
        else:
            text += "\n" + history_entry + "\n"

    old_target = (
        "`3818-Y5-R2FR-EH-metric-equation-to-weak-field-Poisson-source-normalization-bridge.md`\n\n"
        "Target: derive or bound the next necessary bridge from conserved Hilbert stress to Newton/local GR: EH-like metric equation, `kappa/G` owner, weak-field Poisson limit, `Pi_M J_H` source selector, and no fitted-GM circularity. If any clause fails, emit finite `R_EH_owner`, `R_Poisson_norm`, and `R_GM_calibration` rows.\n\n"
        "This is the best next move because 3817 preserves the source stress, but the theory still has to prove that this stress sources the observed metric with the correct Newtonian normalization."
    )
    new_target = (
        "`3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md`\n\n"
        "Target: derive or bound the source-normalization gate exposed by 3818: positive same-frame `M_H_ref`, parent-owned `Pi_M J_H` flux closure, source worldtube selector, and measured-GM anti-circularity. If not closed, emit finite `M_H_ref`/`PiM`/`GM` residual rows ready for empirical scoring.\n\n"
        "This is the best next move because the EH-to-Poisson algebra is now clean conditionally; the remaining danger is laundering source normalization through fitted orbital `GM`."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3818_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3818_EH_METRIC_EQUATION_TEMPLATE.csv",
        "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv",
        "P8_Y5_R2FR_3818_KAPPA_GREF_POLICY_AND_RESIDUALS.csv",
        "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv",
        "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_3818_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3818_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3818_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3818_STATUS.csv",
        "P8_Y5_BRR545_3818_VALIDATION.csv",
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
    fwb_hits = list(FWB.rglob("*3818*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3818 markdown document written"),
        ("EH_template_written", any(row["template_id"] == "EHP3818_0_public_metric_equation" for row in grouped["eh_template"]), "EH metric equation template emitted"),
        ("poisson_derivation_written", any(row["derivation_id"] == "POI3818_0_linearized_00" and row["status"] == "EXACT_CONDITIONAL_WEAK_FIELD_ALGEBRA" for row in grouped["poisson"]), "weak-field Poisson derivation emitted"),
        ("G_policy_guard", any(row["kappa_id"] == "KGP3818_0_constant_policy" for row in grouped["kappa"]), "G policy guard emitted"),
        ("source_norm_blocked", any(row["guard_id"] == "SNG3818_3_no_orbital_GM_import" for row in grouped["source_norm"]), "anti-circular source normalization guard emitted"),
        ("residual_total_row", any(row["residual_id"] == "R3818_5_total" for row in grouped["residuals"]), "total EH/Poisson/GM residual row emitted"),
        ("claim_gates_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("newton_claim_blocked", any(row["gate_id"] == "GATE3818_4_Newton_claim" and row["gate_pass"] == "false" for row in grouped["gates"]), "Newton claim remains blocked"),
        ("next_target_selected", grouped["next_target"][0]["target_doc"].startswith("3819-Y5-R2FR-MHref-PiM-JH"), "3819 MHref/PiM/GM target selected"),
        ("spine_updated", "Current State After 3818" in spine_text and "3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md" in spine_text, "live spine updated to 3818 and 3819 target"),
        ("formalization_clean", not fwb_hits, "no 3818 files written under formalization-workbench"),
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
        "eh_template": eh_template_rows(timestamp),
        "poisson": poisson_rows(timestamp),
        "kappa": kappa_rows(timestamp),
        "source_norm": source_norm_rows(timestamp),
        "residuals": residual_rows(timestamp),
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
