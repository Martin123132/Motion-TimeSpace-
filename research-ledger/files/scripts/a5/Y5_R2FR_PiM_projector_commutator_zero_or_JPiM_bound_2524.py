from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_PIM_PROJECTOR_COMMUTATOR_2524"
CHECKPOINT_ID = "2524"
DOC = ROOT / "2524-Y5-R2FR-PiM-projector-commutator-zero-or-JPiM-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_SOURCE_REGISTER.csv",
    "pim_zero_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_PIM_ZERO_AUDIT.csv",
    "pim_commutator_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_PIM_COMMUTATOR_GATE.csv",
    "jpim_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2524_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2524_VALIDATION.csv",
}

BRANCH_COPIES = {
    "pim_zero_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "PiM_projector_commutator_zero_audit_2524_NONCLAIM.csv",
    "jpim_bound_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "JPiM_bound_rows_2524_NONCLAIM.csv",
    "pim_commutator_gate": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2524_PIM_COMMUTATOR_GATE_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2524_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2524_0_2523_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2523_NEXT_TARGET.csv",
        "needles": ["NEXT2523_0_selected", "J_PiM_comm"],
        "role": "authoritative 2523 handoff to Pi_M projector commutator gate",
    },
    {
        "source_id": "SRC2524_1_2523_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2523_VALIDATION.csv",
        "needles": ["VAL2523_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2524_2_2523_jreadout",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv",
        "needles": ["JRO2523_1_PiM_comm", "MISSING_PIM_COMMUTATOR_ZERO_OR_BOUND"],
        "role": "J_readout already exposes Pi_M as the highest-leverage subcomponent",
    },
    {
        "source_id": "SRC2524_3_2407_zero_audit",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2407_PIM_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["PZ2407_1_fixed_chainmap_lemma", "CONDITIONAL_THEOREM_CLEAN"],
        "role": "prior Pi_M audit: fixed chain-map theorem is conditionally clean",
    },
    {
        "source_id": "SRC2524_4_2407_bound_pack",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2407_PIM_COEFFICIENT_BOUND_PACK.csv",
        "needles": ["PCB2407_0_I_commutator", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"],
        "role": "prior finite Pi_M coefficient rows remain unfilled and nonclaim",
    },
    {
        "source_id": "SRC2524_5_2408_equality",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2408_TOPOLOGICAL_HILBERT_EQUALITY_STATUS.csv",
        "needles": ["THE2408_4_current_verdict", "NOT_PARENT_SIGNED_NONCLAIM"],
        "role": "topological-Hilbert equality remains conditional rather than parent-signed",
    },
    {
        "source_id": "SRC2524_6_2408_finite_rows",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2408_FINITE_ROWS.csv",
        "needles": ["REQ2408_0_R_eq", "REQ2408_2_I_commutator"],
        "role": "R_eq/I_commutator/B_zero finite rows exist but lack values",
    },
    {
        "source_id": "SRC2524_7_2419_chainmap_gate",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv",
        "needles": ["CMG2419_3_chainmap", "ZERO_NOT_DERIVED_BOUND_PACK_REQUIRED"],
        "role": "source-worldtube/projector chain-map zero remains unsigned",
    },
    {
        "source_id": "SRC2524_8_2419_bound_pack",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2419_CHAINMAP_READOUT_BOUND_PACK.csv",
        "needles": ["CBP2419_0_total", "MISSING_CHAINMAP_ZERO_OR_SOURCE_ROW"],
        "role": "absolute source-worldtube/projector readout bound pack",
    },
    {
        "source_id": "SRC2524_9_2481_source_norm",
        "path": "2481-Y5-R2FR-Hilbert-worldtube-source-normalization-zero-certificate-or-Enorm-row.md",
        "needles": ["THM2481_5_zero_certificate_verdict", "ZERO_NOT_PROMOTED_RETAIN_E_NORM"],
        "role": "stationary Hilbert/worldtube source normalization exists only as control branch",
    },
    {
        "source_id": "SRC2524_10_2482_worldtube",
        "path": "2482-Y5-R2FR-kappaG-parent-calibration-or-dynamic-worldtube-closure.md",
        "needles": ["KAP2482_4_verdict", "DYN2482_4_verdict"],
        "role": "kappa/G origin and dynamic worldtube closure remain retained residuals",
    },
    {
        "source_id": "SRC2524_11_2503_selector",
        "path": "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["WHS2503_6_current_verdict", "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS"],
        "role": "worldtube-Hilbert source selector is conditional and not claimable",
    },
    {
        "source_id": "SRC2524_12_2205_frontier",
        "path": "2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md",
        "needles": ["BLK2205_1_PiM_Hamiltonian_lock", "CG2205_5_local_GR_newton"],
        "role": "local-GR frontier names Pi_M lock/source measure as a blocker",
    },
]


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
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found_needles = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found_needles),
                role=spec["role"],
                source_pass=path.exists() and len(found_needles) == len(spec["needles"]),
            )
        )
    return rows


def pim_zero_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "PIM2524_0_definition",
            "claim_piece": "Pi_M projector commutator contribution",
            "formal_statement": "J_PiM_comm := ||(delta_m Pi_M)J_H|| + ||[d,Pi_M]J_H|| on the parent local source complex, with common M_H_ref or source-current normalization.",
            "result": "DEFINITION_LOCKED",
            "blocking_gap": "definition alone supplies neither a zero theorem nor a numeric/source-backed bound",
            "effect": "isolates the Newton-facing readout/source-normalization artery inside J_readout",
        },
        {
            "audit_id": "PIM2524_1_product_rule",
            "claim_piece": "projected-current product rule",
            "formal_statement": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H and delta_m(Pi_M J_H)=Pi_M delta_m J_H + (delta_m Pi_M)J_H.",
            "result": "EXACT_OBSTRUCTION_IDENTITY",
            "blocking_gap": "the commutator and projector-variation terms are real unless Pi_M is fixed/chain-map on the physical current complex",
            "effect": "prevents dropping the dangerous term by notation",
        },
        {
            "audit_id": "PIM2524_2_fixed_chainmap_lemma",
            "claim_piece": "fixed parent chain-map zero",
            "formal_statement": "If Pi_M is parent-selected before readout, delta_m Pi_M=0, and d Pi_M=Pi_M d on C_H(A_ext), then [d,Pi_M]J_H=0 for J_H in that complex.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "blocking_gap": "current corpus has not signed physical J_H in the same complex, fixed domain/worldtube, and parent-selected Pi_M together",
            "effect": "the zero route is mathematically clean but only after ownership clauses close",
        },
        {
            "audit_id": "PIM2524_3_topological_no_stress",
            "claim_piece": "topological metric-independence route",
            "formal_statement": "If Pi_M is an absolute/topological representative fixed by the parent rather than a Hodge/Green/domain/readout functional, then delta_g Pi_M=delta_m Pi_M=0.",
            "result": "EXACT_CONDITIONAL_NO_STRESS_ROUTE",
            "blocking_gap": "the same topological object must still equal the observed Hilbert/worldtube source object",
            "effect": "topological Pi_M can avoid projector stress only if it is not a closed wrong charge",
        },
        {
            "audit_id": "PIM2524_4_hodge_domain_counterroute",
            "claim_piece": "Hodge/domain/readout Pi_M",
            "formal_statement": "If Pi_M=Pi_M[g,n_mu,G_B,chi_W,A_ext,S_link,R_A], then delta_m Pi_M, delta_g Pi_M, and domain derivatives generate finite projector/source stress.",
            "result": "COUNTERMODEL_ACTIVE",
            "blocking_gap": "no parent theorem forbids this dependence for the observed source map",
            "effect": "finite operator rows are mandatory if the projector is not topological/fixed",
        },
        {
            "audit_id": "PIM2524_5_physical_current_lock",
            "claim_piece": "Hilbert current in same complex",
            "formal_statement": "J_H[e_obs,tau] must be the observed matter Hilbert source, include or zero all extra channels, and live on the same exterior annulus/source complex used by Pi_M.",
            "result": "NOT_PARENT_SIGNED",
            "blocking_gap": "source-current descent, extra-channel silence, stationary/dynamic worldtube closure and denominator lock are incomplete",
            "effect": "the chain-map lemma may otherwise project a surrogate current",
        },
        {
            "audit_id": "PIM2524_6_same_object_equality",
            "claim_piece": "topological-Hilbert equality",
            "formal_statement": "Pi_M J_H = J_M_top + dB_zero + R_eq with R_eq=0 and compact boundary flux of dB_zero equal to zero.",
            "result": "KEY_BLOCKER_NOT_DERIVED",
            "blocking_gap": "R_eq, B_zero_flux, fixed reference, M_H_ref, worldtube selector and no-extra-channel clauses remain unsigned/unfilled",
            "effect": "closed topological charge is not Newton/source-normalization evidence by itself",
        },
        {
            "audit_id": "PIM2524_7_calibration_guard",
            "claim_piece": "no fitted-GM/readout laundering",
            "formal_statement": "Pi_M, M_H_ref, source worldtube and calibration must be fixed before orbital/PPN/readout fitting; observed GM cannot be used to prove the mass map.",
            "result": "PASS_GUARDRAIL",
            "blocking_gap": "guardrail passes as a prohibition, not as a zero theorem",
            "effect": "keeps the route non-circular",
        },
        {
            "audit_id": "PIM2524_8_verdict",
            "claim_piece": "J_PiM_comm=0 theorem",
            "formal_statement": "J_PiM_comm=0 requires fixed parent Pi_M, chain-map property, fixed source worldtube/domain, physical Hilbert current domain, same-object equality, zero boundary flux, and same denominator.",
            "result": "JPIM_ZERO_THEOREM_NOT_DERIVED_STAGE_BOUND_ROWS",
            "blocking_gap": "current evidence proves the conditional route, not the antecedents",
            "effect": "retain finite nonclaim J_PiM_comm rows and attack fixed source-worldtube/current descent next",
        },
    ]
    return [base_row(**entry) for entry in entries]


def pim_commutator_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "PMG2524_0_parent_PiM",
            "required_clause": "parent-selected Pi_M",
            "formal_condition": "Pi_M is selected by S_parent or its boundary/charge contract before readout, not by the fitted arena",
            "current_status": "BLOCKED_PARENT_SELECTOR_UNSIGNED",
            "if_fail": "Pi_M can be chosen to match observed GM rather than derived",
        },
        {
            "gate_id": "PMG2524_1_delta_m_fixed",
            "required_clause": "memory variation fixedness",
            "formal_condition": "delta_m Pi_M=0 on the local branch or ||(delta_m Pi_M)J_H|| has a source-backed bound",
            "current_status": "BLOCKED_DELTA_PIM_ZERO_UNSIGNED",
            "if_fail": "J_PiM_comm remains a source-normalization residual",
        },
        {
            "gate_id": "PMG2524_2_chainmap",
            "required_clause": "chain-map property",
            "formal_condition": "d Pi_M=Pi_M d on the physical Hilbert-current complex C_H(A_ext)",
            "current_status": "CONDITIONAL_MATH_NOT_PARENT_SIGNED",
            "if_fail": "I_commutator_abs survives",
        },
        {
            "gate_id": "PMG2524_3_fixed_domain",
            "required_clause": "fixed exterior annulus and linking surface",
            "formal_condition": "delta_m W_source=delta_m A_ext=delta_m S_link=0 before readout",
            "current_status": "BLOCKED_WORLDTUBE_DOMAIN_OWNER_UNSIGNED",
            "if_fail": "domain derivative and side-flux terms survive",
        },
        {
            "gate_id": "PMG2524_4_current_domain",
            "required_clause": "physical Hilbert current in same complex",
            "formal_condition": "J_H[e_obs,tau] includes all ordinary source channels and every extra source channel is zeroed or bounded",
            "current_status": "BLOCKED_PHYSICAL_CURRENT_DOMAIN_UNSIGNED",
            "if_fail": "Pi_M can project the wrong current",
        },
        {
            "gate_id": "PMG2524_5_same_object",
            "required_clause": "topological-Hilbert same-object equality",
            "formal_condition": "Pi_M J_H=J_M_top+dB_zero with R_eq=0 in the same compact source class",
            "current_status": "BLOCKED_REQ_ZERO_UNSIGNED",
            "if_fail": "closed wrong-charge countermodel remains active",
        },
        {
            "gate_id": "PMG2524_6_boundary_flux",
            "required_clause": "zero compact boundary/reference flux",
            "formal_condition": "integral_boundary dB_zero=0 with one parent-fixed reference and no moving excision/asymptotic leak",
            "current_status": "BLOCKED_BZERO_FLUX_UNSIGNED",
            "if_fail": "boundary/reference mass shift survives",
        },
        {
            "gate_id": "PMG2524_7_MHref_tau",
            "required_clause": "same positive source denominator and time generator",
            "formal_condition": "M_H_ref, tau_source, tau_charge, tau_clock and tau_readout are parent-owned in one frame",
            "current_status": "BLOCKED_MHREF_TAU_LOCK_UNSIGNED",
            "if_fail": "dimensionless commutator and R_eq rows are not score-ready",
        },
        {
            "gate_id": "PMG2524_8_projector_stress",
            "required_clause": "no Hodge/domain projector stress",
            "formal_condition": "delta_g Pi_M=0 or projector_stress_beta_equiv has a source-backed weak-field bound",
            "current_status": "BLOCKED_PROJECTOR_STRESS_UNSIGNED",
            "if_fail": "PPN/local-GR stress residual remains",
        },
        {
            "gate_id": "PMG2524_9_theorem",
            "required_clause": "J_PiM_comm zero theorem",
            "formal_condition": "PMG2524_0 through PMG2524_8 all pass with source paths",
            "current_status": "CLAIM_BLOCKED_STAGE_JPIM_ROWS",
            "if_fail": "retain nonclaim finite J_PiM rows",
        },
    ]
    return [base_row(**entry, gate_pass=False) for entry in entries]


def jpim_bound_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "JPIM2524_0_total",
            "quantity": "J_PiM_comm",
            "row_role": "total Pi_M projector/source-normalization readout contribution",
            "formula_or_bound": "J_PiM_comm <= I_commutator_abs + DmPiM_JH + Ddomain_PiM + projector_stress_beta_equiv + R_eq_integral + B_zero_flux + E_worldtube + E_extra_current + E_MHref_guard + E_calibration",
            "units": "memory_source_units_or_dimensionless_after_MHref",
            "required_inputs": "component zero certificates or values; units; source paths; M_H_ref; norm convention; no-cancellation ledger",
            "current_status": "MISSING_JPIM_ZERO_OR_COMPONENT_VALUES",
            "observable_links": "J_readout;J_mem;Q_mem;Newton;PPN;R10;WEP;clock;orbit",
        },
        {
            "row_id": "JPIM2524_1_Icommutator",
            "quantity": "I_commutator_abs",
            "row_role": "finite exterior-annulus chain-map commutator",
            "formula_or_bound": "I_commutator_abs := M_H_ref^-1 abs(int_A [d,Pi_M]J_H)",
            "units": "dimensionless_after_MHref_or_GM_flux_units",
            "required_inputs": "A_ext;Pi_M;J_H profile;M_H_ref;orientation;source path",
            "current_status": "MISSING_CHAINMAP_ZERO_OR_SOURCE_ROW",
            "observable_links": "Newton;PPN;R10;R11;orbital",
        },
        {
            "row_id": "JPIM2524_2_DmPiM",
            "quantity": "DmPiM_JH",
            "row_role": "memory variation of the mass projector",
            "formula_or_bound": "DmPiM_JH := ||(delta_m Pi_M)J_H||",
            "units": "memory_source_units",
            "required_inputs": "Pi_M parent functional; memory generator; J_H norm; fixedness theorem or operator derivative",
            "current_status": "MISSING_DELTA_M_PIM_ZERO_OR_BOUND",
            "observable_links": "J_readout;Q_mem;PPN",
        },
        {
            "row_id": "JPIM2524_3_Ddomain",
            "quantity": "Ddomain_PiM",
            "row_role": "worldtube/domain/linking-surface derivative",
            "formula_or_bound": "Ddomain_PiM <= ||D_D Pi_M|| (||delta W_source||+||delta A_ext||+||delta S_link||)",
            "units": "declared_operator_norm_times_domain_variation",
            "required_inputs": "domain variation amplitude; operator norm; support theorem; source path",
            "current_status": "MISSING_FIXED_DOMAIN_OR_OPERATOR_BOUND",
            "observable_links": "Newton;R10;orbit;source_normalization",
        },
        {
            "row_id": "JPIM2524_4_projector_stress",
            "quantity": "projector_stress_beta_equiv",
            "row_role": "weak-field stress from metric-dependent Pi_M",
            "formula_or_bound": "projector_stress_beta_equiv := PPN-projected norm of delta_g Pi_M contribution",
            "units": "PPN_or_operator_units",
            "required_inputs": "metric derivative of Pi_M; weak-field map; PPN projection kernel",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE",
            "observable_links": "PPN_beta;PPN_gamma;local_GR",
        },
        {
            "row_id": "JPIM2524_5_Req",
            "quantity": "R_eq_integral",
            "row_role": "same-object topological-Hilbert equality residual",
            "formula_or_bound": "R_eq_integral := M_H_ref^-1 int_S(Pi_M J_H - J_M_top - dB_zero)",
            "units": "dimensionless_after_MHref",
            "required_inputs": "Pi_M J_H profile;J_M_top profile;B_zero;M_H_ref;source path",
            "current_status": "MISSING_REQ_ZERO_OR_SOURCE_ROW",
            "observable_links": "Newton;local_GR;source_normalization",
        },
        {
            "row_id": "JPIM2524_6_Bzero",
            "quantity": "B_zero_flux",
            "row_role": "boundary/reference exact-flux leakage",
            "formula_or_bound": "B_zero_flux := M_H_ref^-1 int_boundary dB_zero",
            "units": "dimensionless_or_GM_flux_units",
            "required_inputs": "boundary class;reference;B_zero definition;flux value/theorem;source path",
            "current_status": "MISSING_BZERO_FLUX_ZERO_OR_VALUE",
            "observable_links": "PPN;Gdot;orbit;R10",
        },
        {
            "row_id": "JPIM2524_7_worldtube",
            "quantity": "E_worldtube",
            "row_role": "source-worldtube/support mismatch",
            "formula_or_bound": "E_worldtube <= abs(delta W_source)+abs(delta support profile)+abs(linking surface drift)",
            "units": "dimensionless_or_memory_source_units",
            "required_inputs": "parent worldtube selector; support profile; jump theorem; side-flux bound",
            "current_status": "MISSING_WORLDTUBE_FIXEDNESS_OR_BOUND",
            "observable_links": "Newton;WEP;clock;orbit",
        },
        {
            "row_id": "JPIM2524_8_extra_current",
            "quantity": "E_extra_current",
            "row_role": "extra source-current/anomaly leakage in projected mass closure",
            "formula_or_bound": "E_extra_current <= normalized ||Pi_M dJ_extra|| + anomaly/source-channel terms",
            "units": "dimensionless_or_GM_flux_units",
            "required_inputs": "extra-current zero theorem or finite source-channel rows",
            "current_status": "MISSING_EXTRA_CHANNEL_ZERO_OR_BOUND",
            "observable_links": "Newton;PPN;R11;species_coupling",
        },
        {
            "row_id": "JPIM2524_9_MHref_guard",
            "quantity": "E_MHref_guard",
            "row_role": "missing same-frame denominator/time generator guard",
            "formula_or_bound": "E_MHref_guard := I_not_sourced(M_H_ref,H_tau,H_ref,Q_tau,tau_source=tau_readout)",
            "units": "guard_or_dimensionless_denominator_residual",
            "required_inputs": "positive M_H_ref;H_tau;H_ref;Q_tau;tau lock;source path",
            "current_status": "MISSING_MHREF_TAU_LOCK",
            "observable_links": "all_local_arenas",
        },
        {
            "row_id": "JPIM2524_10_calibration",
            "quantity": "E_calibration",
            "row_role": "absolute source calibration/fitted-GM guard",
            "formula_or_bound": "E_calibration <= abs(surface charge calibration - parent v-source mass calibration)",
            "units": "dimensionless",
            "required_inputs": "parent fixed calibration; no fitted GM feedback; source normalization convention",
            "current_status": "MISSING_PARENT_FIXED_CALIBRATION_OR_VALUE",
            "observable_links": "Newton;Gdot;PPN;orbit",
        },
        {
            "row_id": "JPIM2524_11_Jreadout_insertion",
            "quantity": "J_PiM contribution to J_readout",
            "row_role": "Pi_M component in total readout re-entry",
            "formula_or_bound": "J_readout <= J_PiM_comm + J_Ploc_comm + J_worldtube_comm + J_material_comm + J_coframe_DObs + J_EFT_pre + J_calibration + J_boundary_endpoint",
            "units": "memory_source_units",
            "required_inputs": "J_PiM_comm value/theorem-zero plus remaining J_readout components",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "J_readout;J_mem;Q_mem",
        },
        {
            "row_id": "JPIM2524_12_Qmem_insertion",
            "quantity": "N_src J_PiM_comm",
            "row_role": "Pi_M readout-source drive insertion into Q_mem",
            "formula_or_bound": "Q_mem_PiM <= A_ref^-1 N_src J_PiM_comm",
            "units": "dimensionless_after_Aref",
            "required_inputs": "A_ref;N_src;J_PiM_comm value/theorem-zero;source path",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "Q_norm;PPN_gamma;local_GR",
        },
    ]
    return [
        base_row(
            **entry,
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
        )
        for entry in entries
    ]


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "POG2524_0_readout",
            "arena": "J_readout/J_mem/Q_mem",
            "map_formula": "J_PiM_comm -> J_readout -> J_mem -> A_ref^-1 N_src J_mem",
            "required_bundle": "J_PiM zero/value; A_ref; N_src; no double counting with worldtube and boundary rows",
            "status": "BLOCKED_MISSING_JPIM_VALUE_OR_THEOREM",
        },
        {
            "gate_id": "POG2524_1_Newton",
            "arena": "Newton/source normalization",
            "map_formula": "epsilon_M includes I_commutator,R_eq,B_zero,E_worldtube,E_calibration and maps to Delta_Newton",
            "required_bundle": "same source object; M_H_ref; kappa/G origin; no fitted GM; source-worldtube closure",
            "status": "BLOCKED_MISSING_SOURCE_NORMALIZATION_ZERO",
        },
        {
            "gate_id": "POG2524_2_PPN",
            "arena": "PPN/local GR",
            "map_formula": "projector_stress_beta_equiv and epsilon_M feed gamma/beta/preferred-frame residuals",
            "required_bundle": "PPN projection kernel; projector stress map; source normalization envelope",
            "status": "BLOCKED_MISSING_PPN_PROJECTOR_KERNEL",
        },
        {
            "gate_id": "POG2524_3_R10",
            "arena": "R10/short range",
            "map_formula": "R_eq/I_commutator/worldtube/source-charge mismatch can act as source/test charge normalization residual",
            "required_bundle": "range map; source/test charges; real alpha(lambda) bound; component values",
            "status": "BLOCKED_MISSING_R10_SOURCE_PROJECTION",
        },
        {
            "gate_id": "POG2524_4_WEP_clock_orbit",
            "arena": "WEP/clock/orbital",
            "map_formula": "worldtube, tau, material and calibration pieces project into eta, clock and orbit residuals",
            "required_bundle": "material tensor; tau lock; orbit kernels; fixed calibration protocol",
            "status": "BLOCKED_MISSING_WEP_CLOCK_ORBIT_BUNDLE",
        },
        {
            "gate_id": "POG2524_5_local_GR",
            "arena": "local GR/Newton claim",
            "map_formula": "local GR requires Pi_M/source normalization plus EH descent plus extra-sector double zeros plus readout gates",
            "required_bundle": "all upstream zero certificates or finite residuals under bounds",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2524_0_chainmap_without_current",
            "case_description": "claim J_PiM=0 from fixed chain-map algebra without proving J_H is the observed current in the same complex",
            "missing_requirements": "physical Hilbert current domain; extra-channel silence; source worldtube; M_H_ref",
            "result_status": "REJECT",
            "blocking_markers": "WRONG_CURRENT_COMPLEX",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2524_1_closed_wrong_charge",
            "case_description": "use closed J_M_top as measured mass without R_eq=0 and zero boundary flux",
            "missing_requirements": "topological-Hilbert equality; B_zero flux zero; fixed reference",
            "result_status": "REJECT",
            "blocking_markers": "CLOSED_WRONG_OBJECT",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2524_2_hodge_projector_free_lunch",
            "case_description": "treat a Hodge/Green/domain Pi_M as stress-free topological data",
            "missing_requirements": "metric/domain independence theorem or projector-stress bound",
            "result_status": "REJECT",
            "blocking_markers": "PROJECTOR_STRESS_RETAINED",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2524_3_fitted_GM_normalization",
            "case_description": "use observed orbital GM to calibrate Pi_M, M_H_ref or source mass",
            "missing_requirements": "parent fixed calibration; external source normalization; no-feedback proof",
            "result_status": "REJECT",
            "blocking_markers": "ORBITAL_GM_LAUNDERING",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2524_4_numeric_JPiM_without_denominator",
            "case_description": "score numeric J_PiM row without M_H_ref, tau lock, units and source path",
            "missing_requirements": "M_H_ref;tau;units;source_path;arena projection;component allocation",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_DENOMINATOR_AND_SOURCE",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2524_5_future_complete_JPiM",
            "case_description": "future J_PiM row with parent-zero theorem or real source-backed finite component values",
            "missing_requirements": "none in schema; evidence remains future",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST",
            "blocking_markers": "FUTURE_EVIDENCE_ONLY",
            "pass_fail": "TEMPLATE_NONCLAIM",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2524_0_conditional_win",
            "decision": "accept the fixed-chainmap zero as conditional theorem",
            "rationale": "the product-rule obstruction is exact and the chain-map lemma really kills it when the parent antecedents are true",
            "next_action": "do not rederive this algebra again unless new parent evidence appears",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2524_1_no_promotion",
            "decision": "do not claim Pi_M commutator silence",
            "rationale": "physical current/domain, same-object equality, zero boundary flux, M_H_ref and fixed-worldtube clauses are unsigned",
            "next_action": "retain finite J_PiM_comm component rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2524_2_next",
            "decision": "attack fixed source-worldtube/current descent next",
            "rationale": "repeating topological-Hilbert equality is low-value; the missing upstream object is the parent-owned current/domain on which Pi_M acts",
            "next_action": "try to sign W_source/A_ext/S_link and J_H descent or stage domain-motion bound rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2524_3_claim_guard",
            "decision": "keep Newton/local-GR/PPN/R10/WEP claims blocked",
            "rationale": "J_PiM_comm still feeds J_readout, J_mem, Q_mem and source normalization",
            "next_action": "promote only after theorem-zero or source-backed finite rows with arena kernels",
            "status": "ACTIVE",
        },
    ]
    return [base_row(**entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2524_0_selected",
            "selection_status": "selected",
            "target_file": "2525-Y5-R2FR-source-worldtube-fixed-domain-and-Hilbert-current-descent-or-Jdomain-bound.md",
            "target_script": "scripts/Y5_R2FR_source_worldtube_fixed_domain_and_Hilbert_current_descent_or_Jdomain_bound_2525.py",
            "objective": "prove W_source, A_ext, S_link, J_H and tau are parent-owned/fixed before readout and live on the same Hilbert-current complex, or stage finite domain-motion/current-escape rows",
            "success_condition": "source-worldtube/domain/current descent is theorem-zero for Pi_M chain-map use, or retained as finite nonclaim E_worldtube/E_domain_motion/E_current_escape rows",
            "do_not_do": "do not define the worldtube after fitting; do not use observed GM; do not count Noether conservation alone as source equality; do not claim Newton/local GR",
        },
        {
            "route_id": "NEXT2524_1_fibre_queue",
            "selection_status": "queued_after_source_worldtube",
            "target_file": "2526-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2526.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after the source-worldtube/projector lane is narrowed",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let memory/readout/source-worldtube closure erase independent fibre residuals",
        },
    ]
    return [base_row(**entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_map = {
        "pim_zero_audit": OUTPUTS["pim_zero_audit"],
        "jpim_bound_rows": OUTPUTS["jpim_bound_rows"],
        "pim_commutator_gate": OUTPUTS["pim_commutator_gate"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, destination in BRANCH_COPIES.items():
        source = source_map[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        parse_ok, row_count, parse_message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=f"COPY2524_{key}",
                source_path=str(source.relative_to(ROOT)),
                destination_path=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_message=parse_message,
                status="NONCLAIM_BRANCH_COPY",
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
                "gate_pass",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    audit_rows = rows_by_name["pim_zero_audit"]
    gate_rows = rows_by_name["pim_commutator_gate"]
    bound_rows = rows_by_name["jpim_bound_rows"]

    add("VAL2524_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2524_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2524_02_chainmap_theorem_written",
        any(
            row["audit_id"] == "PIM2524_2_fixed_chainmap_lemma"
            and row["result"] == "EXACT_CONDITIONAL_THEOREM"
            for row in audit_rows
        ),
        "fixed parent chain-map zero is recorded as conditional theorem",
    )
    add(
        "VAL2524_03_general_zero_not_promoted",
        any(
            row["audit_id"] == "PIM2524_8_verdict"
            and row["result"] == "JPIM_ZERO_THEOREM_NOT_DERIVED_STAGE_BOUND_ROWS"
            for row in audit_rows
        ),
        "current Pi_M zero remains unclaimed",
    )
    add(
        "VAL2524_04_gates_blocked",
        len(gate_rows) == 10 and all(str(row["gate_pass"]) == "False" for row in gate_rows),
        "parent Pi_M/current/domain/equality/boundary gates all block promotion",
    )
    add(
        "VAL2524_05_bound_rows_complete",
        all(
            any(row["row_id"] == required for row in bound_rows)
            for required in [
                "JPIM2524_0_total",
                "JPIM2524_1_Icommutator",
                "JPIM2524_2_DmPiM",
                "JPIM2524_5_Req",
                "JPIM2524_6_Bzero",
                "JPIM2524_11_Jreadout_insertion",
                "JPIM2524_12_Qmem_insertion",
            ]
        ),
        "J_PiM rows include total, commutator, variation, equality, boundary, readout and Qmem insertion",
    )
    add(
        "VAL2524_06_bound_rows_nonclaim",
        all(
            str(row["accepted_for_scoring"]) == "False"
            and str(row["claim_pass"]) == "False"
            and str(row["score_ready"]) == "False"
            for row in bound_rows
        ),
        "all J_PiM bound rows are blocked for scoring",
    )
    add(
        "VAL2524_07_observable_gates_blocked",
        all(
            str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED")
            for row in rows_by_name["observable_gate"]
        ),
        "readout/Qmem/Newton/PPN/R10/WEP/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2524_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(
            str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"}
            for row in rows_by_name["dryrun_results"]
        ),
        "chainmap-without-current, closed-wrong-charge, Hodge free-lunch, fitted GM and incomplete numeric rows do not score",
    )
    add(
        "VAL2524_09_next_target_worldtube",
        any(
            row["route_id"] == "NEXT2524_0_selected"
            and "source-worldtube-fixed-domain" in row["target_file"]
            for row in rows_by_name["next_target"]
        ),
        "source-worldtube/fixed-domain owner selected next",
    )
    add("VAL2524_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2524_11_branch_copies",
        all(
            str(row["copied"]) == "True" and str(row["parse_ok"]) == "True"
            for row in rows_by_name["branch_copies"]
        ),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2524*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2524_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2524_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2524_CSV_{path.stem}", parse_ok, f"{parse_message}; rows={row_count}")
    for key, path in BRANCH_COPIES.items():
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2524_COPY_CSV_{key}", parse_ok, f"{parse_message}; rows={row_count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2524_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2524 preserves the fixed-chainmap Pi_M zero theorem as conditional, refuses to promote current Pi_M silence, stages J_PiM rows, and selects fixed source-worldtube/current descent next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2524 - Pi_M Projector Commutator Zero or JPiM Bound",
                "",
                "**Current verdict:** the `Pi_M` algebra is not the enemy. A parent-fixed chain-map kills the commutator exactly. Current MTS still does not parent-sign the physical Hilbert-current complex, fixed source worldtube/domain, topological-Hilbert same-object equality, zero boundary flux, same denominator, and no fitted-GM calibration together.",
                "",
                "**Main gain:** `J_PiM_comm` is now split into named nonclaim rows: `I_commutator_abs`, `(delta_m Pi_M)J_H`, domain motion, projector stress, `R_eq`, `B_zero_flux`, worldtube mismatch, extra-current escape, denominator guard, and calibration guard.",
                "",
                "**Claim discipline:** no Newton, local-GR, PPN, WEP, R10, clock, orbit, `J_readout`, `J_mem`, `Q_mem`, or GitHub/public claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Pi_M Zero Audit",
                md_table(rows_by_name["pim_zero_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect"]),
                "",
                "## Pi_M Commutator Gate",
                md_table(rows_by_name["pim_commutator_gate"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_fail", "gate_pass"]),
                "",
                "## JPiM Bound Rows",
                md_table(rows_by_name["jpim_bound_rows"], ["row_id", "quantity", "row_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
                "",
                "## Observable Gate",
                md_table(rows_by_name["observable_gate"], ["gate_id", "arena", "map_formula", "required_bundle", "status", "claim_pass"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "missing_requirements", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "next_action", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "pim_zero_audit": pim_zero_audit_rows(),
        "pim_commutator_gate": pim_commutator_gate_rows(),
        "jpim_bound_rows": jpim_bound_rows(),
        "observable_gate": observable_gate_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
