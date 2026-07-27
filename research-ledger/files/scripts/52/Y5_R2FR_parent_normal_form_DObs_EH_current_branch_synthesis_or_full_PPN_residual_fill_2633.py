from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md"

PREFIX = "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "normal_form_gate": RESIDUALS / f"{PREFIX}_PARENT_NORMAL_FORM_GATE.csv",
    "conditional_theorem": RESIDUALS / f"{PREFIX}_CONDITIONAL_LOCAL_GR_THEOREM.csv",
    "blocker_matrix": RESIDUALS / f"{PREFIX}_BLOCKER_MATRIX.csv",
    "residual_vector": RESIDUALS / f"{PREFIX}_RESIDUAL_VECTOR_MAP.csv",
    "ppn_fill": RESIDUALS / f"{PREFIX}_PPN_COMPONENT_FILL_LEDGER.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2633_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2633_00_2483_EH_coupling",
        "role": "EH/kappa origin and coefficient residual",
        "path": ROOT / "2483-Y5-R2FR-parent-EH-coupling-origin-or-coupling-residual-row.md",
        "needles": ["BLOCKED_PARENT_ORIGIN", "KRES2483_0_e_kappaG", "VAL2483_OVERALL"],
    },
    {
        "source_id": "SRC2633_01_2484_EH_uniqueness",
        "role": "EH uniqueness hypothesis contract",
        "path": ROOT / "2484-Y5-R2FR-EH-uniqueness-hypotheses-or-parent-normal-form-blocker.md",
        "needles": ["EH uniqueness is a viable derivation route", "e_EH_hyp", "VAL2484_OVERALL"],
    },
    {
        "source_id": "SRC2633_02_2485_parent_normal_form",
        "role": "parent normal-form skeleton and coefficient slots",
        "path": ROOT / "2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md",
        "needles": [
            "SKELETON_WRITTEN_NOT_PARENT_DERIVED",
            "NF2485_0_parent_action_skeleton",
            "VAL2485_OVERALL",
        ],
    },
    {
        "source_id": "SRC2633_03_2486_quotient_DObs",
        "role": "quotient chain-rule and residual owner split",
        "path": ROOT / "2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md",
        "needles": ["`Dq[v]=0` is not enough", "Residual Owner Split", "VAL2486_OVERALL"],
    },
    {
        "source_id": "SRC2633_04_2487_observed_coframe",
        "role": "DObs_e kernel and terminal public coframe blocker",
        "path": ROOT / "2487-Y5-R2FR-observed-coframe-functor-and-vertical-generator-certificate-or-DObs-leak-row.md",
        "needles": [
            "DOBS_E_KERNEL_ZERO_NOT_SIGNED",
            "TERMINAL_PUBLIC_COFRAME_NOT_PARENT_DERIVED",
            "VAL2487_OVERALL",
        ],
    },
    {
        "source_id": "SRC2633_05_2488_no_shadow",
        "role": "no-shadow action-domain attempt and common-frame countermodels",
        "path": ROOT / "2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md",
        "needles": [
            "ACTION_DOMAIN_NO_SHADOW_NOT_DERIVED_CURRENT_CORPUS",
            "NO_SHADOW_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "VAL2488_OVERALL",
        ],
    },
    {
        "source_id": "SRC2633_06_2489_PPN_kernel",
        "role": "first common-frame PPN kernel and full-vector guard",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["GAMMA_ONLY_PASS_FORBIDDEN", "PPNV2489_7_total_abs", "VAL2489_OVERALL"],
    },
    {
        "source_id": "SRC2633_07_2631_current_vector",
        "role": "current-branch full PPN vector consolidation",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": [
            "FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE",
            "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP",
            "VAL2631_OVERALL",
        ],
    },
    {
        "source_id": "SRC2633_08_2632_rollforward",
        "role": "source-prefactor rollforward and local-GR frontier shift",
        "path": ROOT / "2632-Y5-R2FR-no-source-prefactor-parent-action-clause-or-PPN-component-basis-first-row.md",
        "needles": [
            "SOURCE_PREFACTOR_CHAIN_IMPORTED_DO_NOT_RESTART",
            "PARENT_NORMAL_FORM_AND_DOBS_ARE_NOW_THE_GR_FRONTIER",
            "VAL2632_OVERALL",
        ],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = read_text(path)
        exists = path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def normal_form_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PNFG2633_0_parent_action_inventory",
            "required_clause": "one signed parent action S_parent[Phi] with typed fields, public/coframe variables, auxiliary/private variables, matter, boundary and coefficient slots",
            "source_status": "2485 writes the skeleton only",
            "current_status": "BLOCKED_SKELETON_NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_PARENT_OBJECT_LANGUAGE;MISSING_FIELD_SORT_SIGNATURE;MISSING_COEFFICIENT_OWNER",
            "if_signed_effect": "all local-GR clauses have a single source of truth rather than separate closure axioms",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_1_EH_uniqueness_hypotheses",
            "required_clause": "public metric/coframe, local diffeomorphism symmetry, two-derivative leading grammar, no extra public rank-2 tensors, and boundary/falloff class",
            "source_status": "2484 says EH uniqueness is viable only under these hypotheses",
            "current_status": "BLOCKED_HYPOTHESES_UNSIGNED",
            "missing_for_claim": "MISSING_DIFF_GENERATOR;MISSING_DERIVATIVE_GRAMMAR;MISSING_RESIDUAL_SECTOR_SILENCE;MISSING_BOUNDARY_CLASS",
            "if_signed_effect": "EH leading operator is derived instead of imported",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_2_kappa_owner",
            "required_clause": "a1=1/(2*kappa_MTS) and measured G relation arise from parent normalization before fitting tests",
            "source_status": "2483 retains e_kappaG and e_EH_import",
            "current_status": "BLOCKED_COEFFICIENT_OWNER_UNSIGNED",
            "missing_for_claim": "MISSING_A1_OWNER;MISSING_KAPPA_MTS_TO_G_REF_TRANSFER;MISSING_SOURCE_NORMALIZATION",
            "if_signed_effect": "Newtonian coupling can be derived rather than calibrated by GM",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_3_matter_source_descent",
            "required_clause": "ordinary matter descends through the public coframe with no active source-only prefactors",
            "source_status": "2632 imports the old source-prefactor chain and keeps Hilbert matter side as conditionally useful",
            "current_status": "PASS_CONDITIONAL_NONCLAIM",
            "missing_for_claim": "MISSING_PARENT_ACTION_SIGNATURE;MISSING_NO_EXTRA_MATTER_ARGUMENT_GRAMMAR;MISSING_PRESERVATION_CLAUSES",
            "if_signed_effect": "right-hand side becomes a universal Hilbert source compatible with Ward/Bianchi conservation",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_4_quotient_DObs_no_shadow",
            "required_clause": "q_parent, vertical generators, and terminal public coframe force DObs_e[v_X]=0 for all private/residual directions",
            "source_status": "2486-2488 prove only exact conditional chain-rule/no-shadow theorems",
            "current_status": "BLOCKED_DOBS_E_AND_ACTION_DOMAIN_UNSIGNED",
            "missing_for_claim": "MISSING_Q_PARENT_SIGNATURE;MISSING_DOBS_E_KERNEL;MISSING_TERMINAL_PUBLIC_COFRAME;MISSING_NO_EXTRA_FRAME_GRAMMAR",
            "if_signed_effect": "private variables stop moving rods, clocks, photons, sources and PPN readout",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_5_residual_silence_or_bound",
            "required_clause": "all non-EH operator sectors are theorem-zero or finite with source-backed local bounds",
            "source_status": "2484/2485/2632 keep DeltaE_MTS, R11 and boundary/readout residuals live",
            "current_status": "BLOCKED_RESIDUAL_SECTOR_ZERO_OR_BOUNDS_MISSING",
            "missing_for_claim": "MISSING_R11_DIVERGENCE_LAW;MISSING_WEAK_FIELD_PROJECTION;MISSING_LOCAL_BOUND_INPUTS;MISSING_NO_CANCELLATION_ENVELOPE",
            "if_signed_effect": "field equation reduces to EH plus matter in local weak-field systems",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PNFG2633_6_full_PPN_vector_closure",
            "required_clause": "gamma, beta, preferred-frame, source, endpoint, readout and q_loc/Khat residuals are theorem-zero or bounded componentwise",
            "source_status": "2489/2631 say gamma-only is forbidden and values are missing",
            "current_status": "BLOCKED_FULL_VECTOR_VALUES_MISSING",
            "missing_for_claim": "MISSING_DELTA_P_QRHAT;MISSING_BETA_KERNEL;MISSING_DISFORMAL_KERNEL;MISSING_SOURCE_PREFACATOR_THEOREM;MISSING_ENDPOINT_READOUT;MISSING_TOTAL_ABS_VALUE",
            "if_signed_effect": "local-GR claim becomes PPN-vector safe instead of a single-test shortcut",
            "valid_for_claim": "False",
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM2633_0_parent_normal_form_to_public_equation",
            "statement": "If PNFG2633_0-5 are parent-signed, varying the reduced public branch gives a1*G_mn + a0*g_mn + DeltaE_res_mn = 1/2*T_H_mn with DeltaE_res_mn=0 or bounded.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "standard variation plus 2484 EH uniqueness route and 2485 normal-form equation shape",
            "missing_for_claim": "same unsigned PNFG clauses plus coefficient owner",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM2633_1_Bianchi_Ward_source_compatibility",
            "statement": "If matter descends through the same public coframe and source-only prefactors are absent, diffeomorphism invariance gives the Ward/Bianchi compatibility condition for the Hilbert source.",
            "proof_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "2632 rollforward keeps the source side conditionally useful rather than solved",
            "missing_for_claim": "parent action signature and preservation clauses",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM2633_2_Newtonian_Poisson_limit",
            "statement": "If a1/kappa is parent-owned, residual sectors vanish or are bounded, and source normalization is fixed before readout, the weak static branch yields nabla^2 U = 4*pi*G_parent*rho_H plus controlled residuals.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "2483/2485 already isolate e_kappaG, E_norm, and DeltaE_MTS as the missing pieces",
            "missing_for_claim": "G_parent owner; E_norm zero/bound; boundary class; no fitted-GM transfer",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM2633_3_no_shadow_to_PPN_vector",
            "statement": "If q_parent/DObs_e terminal public coframe no-shadow is signed, then b_R=d_R=w_R=epsilon_endpoint_R=0 and the full local PPN vector can be zeroed only after beta/delta_p/source/readout clauses also close.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "2487/2488 give the no-shadow conditional theorem; 2489/2631 keep the full-vector guard",
            "missing_for_claim": "DObs_e kernel; terminal action domain; beta and delta_p response closures",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM2633_4_local_GR_claim_gate",
            "statement": "Local GR is claimable only when the public equation, Newtonian limit, no-shadow PPN vector, source normalization and residual-sector silence all pass simultaneously.",
            "proof_status": "CLAIM_GATE_WRITTEN_NOT_PASSED",
            "reason": "single-clause victories can mask live residuals",
            "missing_for_claim": "all blocked PNFG rows",
            "valid_for_claim": "False",
        },
    ]


def blocker_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2633_0_e_EH_import",
            "owned_by": "EH operator origin",
            "current_residual": "e_EH_import",
            "source_anchor": "2483/2484",
            "why_it_matters": "using EH because GR works is not deriving EH from MTS",
            "closure_route": "parent normal-form hypotheses force EH as unique leading operator",
            "status": "BLOCKED_PARENT_ORIGIN",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_1_e_kappaG",
            "owned_by": "coefficient/coupling owner",
            "current_residual": "e_kappaG",
            "source_anchor": "2483/2485",
            "why_it_matters": "Newtonian G must not be a fitted transfer after the fact",
            "closure_route": "derive a1 and kappa_MTS from parent normalization and source worldtube convention",
            "status": "BLOCKED_COEFFICIENT_OWNER",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_2_e_EH_hyp",
            "owned_by": "EH uniqueness hypotheses",
            "current_residual": "e_EH_hyp",
            "source_anchor": "2484",
            "why_it_matters": "Lovelock/EH uniqueness only works if MTS signs the hypotheses",
            "closure_route": "field list, symmetry generator, derivative grammar, boundary class, no-extra-tensor clauses",
            "status": "BLOCKED_HYPOTHESIS_SIGNATURES",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_3_DeltaE_MTS",
            "owned_by": "non-EH operator sector",
            "current_residual": "DeltaE_MTS;R11_residual_operator;DeltaE_boundary",
            "source_anchor": "2484/2485/2632",
            "why_it_matters": "extra rank-2 local operators shift Newton/PPN even if EH is present",
            "closure_route": "derive sector zeros or retain source-backed local bounds",
            "status": "BLOCKED_RESIDUAL_SECTOR_SILENCE",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_4_DObs_e_R",
            "owned_by": "quotient/readout no-shadow",
            "current_residual": "DObs_e_R;epsilon_R_cell;epsilon_common_frame_abs",
            "source_anchor": "2486/2487/2488",
            "why_it_matters": "Dq[v]=0 does not stop hidden variables moving rods/clocks unless readout is q-basic",
            "closure_route": "derive terminal public coframe and DObs_e[v_X]=0 for retained directions",
            "status": "BLOCKED_DOBS_E_KERNEL",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_5_common_frame_coefficients",
            "owned_by": "no-shadow action-domain clause",
            "current_residual": "b_R;d_R;w_R;epsilon_endpoint_R",
            "source_anchor": "2488/2489/2631",
            "why_it_matters": "a universal same frame can still be physically wrong if it depends on hidden C_R/J_q",
            "closure_route": "parent action-domain exclusion or source-backed PPN/clock/orbital response kernels",
            "status": "BLOCKED_NO_SHADOW_ZERO",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK2633_6_Delta_PPN_abs",
            "owned_by": "full local PPN vector",
            "current_residual": "Delta_PPN_abs",
            "source_anchor": "2489/2631",
            "why_it_matters": "gamma-only success cannot claim local GR while beta/source/preferred-frame/readout tails survive",
            "closure_route": "componentwise theorem-zero or numeric bounds with no pair-cancellation shortcut",
            "status": "BLOCKED_VECTOR_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RV2633_0_public_equation",
            "equation_slot": "a1*G_mn + a0*g_mn + DeltaE_MTS_mn + DeltaE_boundary_mn = 1/2*T_H_mn + J_shadow_mn",
            "zero_or_bound_needed": "DeltaE_MTS=0/bound; DeltaE_boundary=0/bound; J_shadow=0/bound",
            "source_anchors": "2485;2486;2632",
            "test_arenas": "Newton;PPN;orbital;R10",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV2633_1_source_normalization",
            "equation_slot": "G_parent*rho_H transfer into nabla^2 U",
            "zero_or_bound_needed": "e_kappaG=0/bound; E_norm=0/bound; no fitted GM",
            "source_anchors": "2483;2485;2486",
            "test_arenas": "Newton;orbital;local_GR",
            "status": "PARENT_COUPLING_OWNER_MISSING",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV2633_2_readout_shadow",
            "equation_slot": "DObs_e[v_X] and common-frame transfer into metric/clock/source readouts",
            "zero_or_bound_needed": "DObs_e_R=0/bound; epsilon_common_frame_abs=0/bound",
            "source_anchors": "2486;2487;2488",
            "test_arenas": "PPN;clocks;WEP;orbital",
            "status": "DOBS_E_KERNEL_NOT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV2633_3_PPN_abs",
            "equation_slot": "Delta_PPN_abs = |delta_p|+|b_R|+|delta_beta|+|d_R|+|w_R|+|endpoint|+|readout|+...",
            "zero_or_bound_needed": "all components theorem-zero or source-backed finite rows; no cancellations",
            "source_anchors": "2489;2631",
            "test_arenas": "Cassini;Mercury;LLR;pulsar;preferred_frame",
            "status": "FULL_VECTOR_OPEN",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV2633_4_effective_GR_branch",
            "equation_slot": "effective leading GR plus explicit residual vector",
            "zero_or_bound_needed": "declare effective status if parent action generator fails; source every residual row before tests",
            "source_anchors": "2484;2632",
            "test_arenas": "same tests as local GR, but as residual-bounded EFT branch",
            "status": "BACKUP_ROUTE_ONLY",
            "valid_for_claim": "False",
        },
    ]


def ppn_fill_rows() -> list[dict[str, Any]]:
    components = [
        ("PPNF2633_0_delta_p", "delta_p_or_q_R_hat", "gamma,beta", "derive reciprocal lock/no-boundary charge or source normalized delta_p row"),
        ("PPNF2633_1_bR", "b_R", "gamma/common Weyl", "derive no-shadow b_R=0 or source same-frame coefficient"),
        ("PPNF2633_2_beta", "delta_beta_total", "beta", "derive second-order field equation/source/readout closure"),
        ("PPNF2633_3_dR", "d_R", "alpha1,alpha2,preferred-frame", "derive no disformal/current slot or source response matrix"),
        ("PPNF2633_4_wR", "w_R/Delta_w_eff", "source normalization,beta,gamma", "use 2632 imported source chain; do not restart it unless parent action evidence appears"),
        ("PPNF2633_5_endpoint", "epsilon_endpoint_R", "xi,alpha3,light-time tails", "derive boundary endpoint silence or source orbital/PPN projection"),
        ("PPNF2633_6_readout", "alpha_readout_or_delta_GM", "gamma,beta,measured-GM transfer", "fix readout gauge before testing; no fitted-GM shortcut"),
        ("PPNF2633_7_total_abs", "Delta_PPN_abs", "all local PPN components", "sum componentwise absolute envelope with no cancellation"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "ppn_observables": observables,
            "required_next_input": required,
            "source_anchor": "2489;2631;2632",
            "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE",
            "route_policy": "derive first; otherwise source-backed nonclaim residual row",
            "valid_for_claim": "False",
        }
        for component_id, symbol, observables, required in components
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2633_0_no_EH_import_as_proof",
            "forbidden_route": "treating standard EH/GR success as a derivation of MTS",
            "reason": "2483/2484 keep EH origin and hypotheses unsigned",
            "status": "FORBIDDEN",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2633_1_no_gamma_only",
            "forbidden_route": "claiming local GR from Cassini gamma or any one PPN component",
            "reason": "2489/2631 require full componentwise PPN vector closure",
            "status": "FORBIDDEN",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2633_2_no_source_prefactor_rerun",
            "forbidden_route": "redoing the w_A/source-prefactor hunt as if 1890-1940/2632 did not exist",
            "reason": "source side is conditionally useful; current frontier is parent operator/readout",
            "status": "FORBIDDEN_UNLESS_NEW_PARENT_ACTION_EVIDENCE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2633_3_no_fitted_GM_shortcut",
            "forbidden_route": "absorbing kappa/source/readout residuals into measured GM",
            "reason": "Newtonian reduction must derive the transfer before comparing tests",
            "status": "FORBIDDEN",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2633_4_no_q_shape_shortcut",
            "forbidden_route": "declaring a variable invisible because q_shape forgets it",
            "reason": "2486/2487 show DObs_e and readout inheritance are the physical gate",
            "status": "FORBIDDEN",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2633_0_internal_checkpoint",
            "claim": "2633 may be used as a private local-GR synthesis gate",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "why": "all rows are guarded and no local test is promoted",
            "passed": "True",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CG2633_1_EH_derived",
            "claim": "MTS derives the EH/kappa local operator",
            "status": "BLOCKED",
            "why": "parent normal-form hypotheses and coefficient owner are unsigned",
            "passed": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CG2633_2_Newton_limit",
            "claim": "MTS derives Newtonian gravity",
            "status": "BLOCKED",
            "why": "needs EH/kappa owner, source normalization, residual silence and boundary class",
            "passed": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CG2633_3_no_shadow",
            "claim": "private/residual variables are locally invisible to rods, clocks, photons and sources",
            "status": "BLOCKED",
            "why": "DObs_e kernel and terminal public coframe/action-domain clause are not parent-signed",
            "passed": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CG2633_4_full_PPN",
            "claim": "MTS passes local PPN as GR",
            "status": "BLOCKED",
            "why": "full PPN vector values/theorem-zeros are missing",
            "passed": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "CG2633_5_effective_residual_branch",
            "claim": "MTS can be tested as an effective GR-plus-residual framework",
            "status": "POSSIBLE_ONLY_AFTER_SOURCE_BACKED_RESIDUAL_ROWS",
            "why": "effective fallback needs numeric/theorem-zero residual rows and baselines",
            "passed": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2633_0_result",
            "decision": "PARENT_NORMAL_FORM_GATE_WRITTEN_NOT_PASSED",
            "reason": "the current corpus has enough pieces to state the exact local-GR contract, but not enough parent signatures to claim it",
            "consequence": "local GR remains alive and sharply localized, not solved",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2633_1_best_route",
            "decision": "DERIVE_PARENT_ACTION_GENERATING_PRINCIPLE_NEXT",
            "reason": "separate residual attacks keep circling unless a parent principle signs field list, symmetry, derivative grammar, coefficient owner and no-extra-frame domain together",
            "consequence": "2634 should try to generate the normal form from MTS primitives, or explicitly demote to an effective residual branch",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2633_2_testing",
            "decision": "TESTING_AFTER_GATE_OR_EFFECTIVE_DECLARATION",
            "reason": "PPN/R10/WEP data are useful only after theorem-zero values or source-backed residual rows exist",
            "consequence": "no local-GR/PPN public claim from this checkpoint",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2633_3_gain",
            "decision": "THE_PROJECT_MOVED_FROM_GAP_LIST_TO_ONE_LOCAL_GR_CONTRACT",
            "reason": "EH, kappa, source, DObs, no-shadow and PPN are now clauses of one gate",
            "consequence": "next work can attack the parent action rather than repeatedly discovering the same blockers",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2634-Y5-R2FR-parent-action-generating-principle-or-effective-GR-residual-branch.md",
            "script": "scripts/Y5_R2FR_parent_action_generating_principle_or_effective_GR_residual_branch_2634.py",
            "objective": "try to derive a parent action generating principle strong enough to sign the 2633 local-GR gate: field/sort list, diffeomorphism generator, two-derivative public grammar, coefficient owner, terminal public coframe/no-extra-frame action domain and residual-sector silence; if it fails, demote the local branch to effective GR plus explicit residual rows",
            "include": "2484 EH hypothesis contract; 2485 parent skeleton; 2486 q/DObs chain rule; 2487/2488 no-shadow blockers; 2489/2631 full PPN vector; 2632 source rollforward; 2633 local-GR gate",
            "exclude": "EH import as proof, fitted G/GM, gamma-only pass, q_shape shortcut, source-prefactor rerun without new parent evidence, public claim",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2634b-Y5-R2FR-effective-GR-residual-test-pack.md",
            "script": "scripts/Y5_R2FR_effective_GR_residual_test_pack_2634b.py",
            "objective": "held fallback: if derivation-first fails again, build source-backed residual rows for the effective GR-plus-residual branch before any PPN/R10/WEP scoring",
            "include": "DeltaE_MTS, e_kappaG, DObs_e_R, b_R, d_R, w_R, endpoint/readout tails, accepted local bounds",
            "exclude": "using effective success as fundamental derivation",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2633_gate",
            "artifact": "parent_normal_form_gate",
            "source_path": str(OUTPUTS["normal_form_gate"]),
            "copy_path": str(LOCAL_BOUNDS / "Parent_normal_form_gate_2633_NONCLAIM.csv"),
            "source_exists": bool_text(OUTPUTS["normal_form_gate"].exists()),
            "copy_exists": bool_text((LOCAL_BOUNDS / "Parent_normal_form_gate_2633_NONCLAIM.csv").exists()),
            "valid_for_claim": "False",
        },
        {
            "copy_id": "COPY2633_theorem",
            "artifact": "conditional_local_gr_theorem",
            "source_path": str(OUTPUTS["conditional_theorem"]),
            "copy_path": str(LOCAL_BOUNDS / "Conditional_local_GR_theorem_2633_NONCLAIM.csv"),
            "source_exists": bool_text(OUTPUTS["conditional_theorem"].exists()),
            "copy_exists": bool_text((LOCAL_BOUNDS / "Conditional_local_GR_theorem_2633_NONCLAIM.csv").exists()),
            "valid_for_claim": "False",
        },
        {
            "copy_id": "COPY2633_residual_vector",
            "artifact": "residual_vector_map",
            "source_path": str(OUTPUTS["residual_vector"]),
            "copy_path": str(LOCAL_BOUNDS / "Residual_vector_map_2633_NONCLAIM.csv"),
            "source_exists": bool_text(OUTPUTS["residual_vector"].exists()),
            "copy_exists": bool_text((LOCAL_BOUNDS / "Residual_vector_map_2633_NONCLAIM.csv").exists()),
            "valid_for_claim": "False",
        },
        {
            "copy_id": "COPY2633_ppn_fill",
            "artifact": "ppn_component_fill_ledger",
            "source_path": str(OUTPUTS["ppn_fill"]),
            "copy_path": str(LOCAL_BOUNDS / "PPN_component_fill_ledger_2633_NONCLAIM.csv"),
            "source_exists": bool_text(OUTPUTS["ppn_fill"].exists()),
            "copy_exists": bool_text((LOCAL_BOUNDS / "PPN_component_fill_ledger_2633_NONCLAIM.csv").exists()),
            "valid_for_claim": "False",
        },
        {
            "copy_id": "COPY2633_next",
            "artifact": "next_target",
            "source_path": str(OUTPUTS["next_target"]),
            "copy_path": str(RAB_QUEUE / "JR2633_PARENT_ACTION_GENERATING_PRINCIPLE_NEXT.csv"),
            "source_exists": bool_text(OUTPUTS["next_target"].exists()),
            "copy_exists": bool_text((RAB_QUEUE / "JR2633_PARENT_ACTION_GENERATING_PRINCIPLE_NEXT.csv").exists()),
            "valid_for_claim": "False",
        },
    ]


def copy_branch_artifacts() -> None:
    copies = [
        (OUTPUTS["normal_form_gate"], LOCAL_BOUNDS / "Parent_normal_form_gate_2633_NONCLAIM.csv"),
        (OUTPUTS["conditional_theorem"], LOCAL_BOUNDS / "Conditional_local_GR_theorem_2633_NONCLAIM.csv"),
        (OUTPUTS["residual_vector"], LOCAL_BOUNDS / "Residual_vector_map_2633_NONCLAIM.csv"),
        (OUTPUTS["ppn_fill"], LOCAL_BOUNDS / "PPN_component_fill_ledger_2633_NONCLAIM.csv"),
        (OUTPUTS["next_target"], RAB_QUEUE / "JR2633_PARENT_ACTION_GENERATING_PRINCIPLE_NEXT.csv"),
    ]
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def formalization_has_2633_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and ("2633" in path.name or "PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633" in path.name):
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [
        LOCAL_BOUNDS / "Parent_normal_form_gate_2633_NONCLAIM.csv",
        LOCAL_BOUNDS / "Conditional_local_GR_theorem_2633_NONCLAIM.csv",
        LOCAL_BOUNDS / "Residual_vector_map_2633_NONCLAIM.csv",
        LOCAL_BOUNDS / "PPN_component_fill_ledger_2633_NONCLAIM.csv",
        RAB_QUEUE / "JR2633_PARENT_ACTION_GENERATING_PRINCIPLE_NEXT.csv",
    ]

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL2633_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2633_01_gate_written",
            len(generated["normal_form_gate"]) >= 7
            and any(row["clause_id"] == "PNFG2633_4_quotient_DObs_no_shadow" for row in generated["normal_form_gate"]),
            "parent normal-form/DObs/EH gate is written with all major clauses",
        ),
        (
            "VAL2633_02_EH_not_promoted",
            any(row["status"] == "BLOCKED_PARENT_ORIGIN" for row in generated["blocker_matrix"])
            and all(row["valid_for_claim"] == "False" for row in generated["blocker_matrix"]),
            "EH/kappa remains blocked rather than imported as proof",
        ),
        (
            "VAL2633_03_conditional_theorem",
            any(row["theorem_id"] == "THM2633_4_local_GR_claim_gate" for row in generated["conditional_theorem"])
            and all(row["valid_for_claim"] == "False" for row in generated["conditional_theorem"]),
            "local-GR theorem is conditional and nonclaim",
        ),
        (
            "VAL2633_04_DObs_no_shadow_blocked",
            any("DOBS_E" in row["current_status"] for row in generated["normal_form_gate"])
            and any("NO_SHADOW" in row["status"] for row in generated["blocker_matrix"]),
            "DObs/no-shadow is explicit and blocked",
        ),
        (
            "VAL2633_05_full_PPN_vector",
            len(generated["ppn_fill"]) == 8
            and any(row["component_id"] == "PPNF2633_7_total_abs" for row in generated["ppn_fill"]),
            "full PPN vector ledger includes total absolute no-cancellation component",
        ),
        (
            "VAL2633_06_route_guards",
            all(row["status"].startswith("FORBIDDEN") for row in generated["route_guards"]),
            "EH import, gamma-only, source-prefactor rerun, fitted-GM, and q_shape shortcuts are forbidden",
        ),
        (
            "VAL2633_07_claim_gates_safe",
            all(row["claim_allowed"] == "False" for row in generated["claim_gates"])
            and all(row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate promotes local GR/Newton/PPN",
        ),
        (
            "VAL2633_08_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2634-Y5-R2FR-parent-action") for row in generated["next_target"]),
            "2634 parent action generating-principle target selected",
        ),
        (
            "VAL2633_09_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim branch copies and acquisition queue exist and parse",
        ),
        (
            "VAL2633_10_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2633 CSVs parse",
        ),
        (
            "VAL2633_11_formalization_untouched",
            not formalization_has_2633_outputs(),
            "no 2633 outputs are written under formalization-workbench",
        ),
        (
            "VAL2633_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2633_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2633 parent-normal-form/DObs/EH synthesis and local-GR conditional gate",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2633 - Y5 R2/f(R) Parent Normal Form DObs EH Current-Branch Synthesis Or Full PPN Residual Fill",
        "",
        "Status: `Y5_R2FR_2633_parent_normal_form_DObs_EH_local_GR_gate_written_not_passed_nonclaim`",
        "",
        "Claim ceiling: no local-GR/Newton proof, no PPN/WEP/R10 pass, no EH import-as-proof, no fitted `G/GM`, no gamma-only pass, no source-prefactor rerun, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2633 compresses the current local-GR frontier into one gate. The good news is that the route is now precise: if the parent action signs the EH normal form, the coefficient owner, the Hilbert source descent, `q_parent/DObs_e` no-shadow, residual-sector silence and the full PPN vector, then local GR/Newton follows as a conditional theorem.",
        "",
        "The bad-but-useful news is that the current corpus does not sign those clauses yet. So this checkpoint does not claim GR. It turns the remaining problem into a parent-action generating-principle target instead of another loop around coupling, Cassini gamma, or fitted `GM`.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Parent Normal-Form Gate",
        md_table(generated["normal_form_gate"]),
        "",
        "## Conditional Local-GR Theorem",
        md_table(generated["conditional_theorem"]),
        "",
        "## Blocker Matrix",
        md_table(generated["blocker_matrix"]),
        "",
        "## Residual Vector Map",
        md_table(generated["residual_vector"]),
        "",
        "## PPN Component Fill Ledger",
        md_table(generated["ppn_fill"]),
        "",
        "## Route Guards",
        md_table(generated["route_guards"]),
        "",
        "## Claim Gates",
        md_table(generated["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(generated["decision"]),
        "",
        "## Next Target",
        md_table(generated["next_target"]),
        "",
        "## Branch Copies",
        md_table(generated["branch_copies"]),
        "",
        "## Validation",
        md_table(validation),
        "",
        "## Plain-English Verdict",
        "",
        "This is progress, but not the victory lap. We have a clean theorem-shaped bridge to GR now: parent action -> EH/kappa -> Hilbert source -> no-shadow readout -> full PPN vector. The bridge is conditional; the missing keystone is the parent action generating principle that signs those clauses together.",
        "",
        "So the next best route is 2634: try to derive that generating principle. If it works, local GR becomes genuinely serious. If it fails, we stop calling the local branch fundamental and build the honest effective-GR-plus-residual test pack instead.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "normal_form_gate": normal_form_gate_rows(),
        "conditional_theorem": conditional_theorem_rows(),
        "blocker_matrix": blocker_matrix_rows(),
        "residual_vector": residual_vector_rows(),
        "ppn_fill": ppn_fill_rows(),
        "route_guards": route_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], generated["source_register"])
    write_csv(OUTPUTS["normal_form_gate"], generated["normal_form_gate"])
    write_csv(OUTPUTS["conditional_theorem"], generated["conditional_theorem"])
    write_csv(OUTPUTS["blocker_matrix"], generated["blocker_matrix"])
    write_csv(OUTPUTS["residual_vector"], generated["residual_vector"])
    write_csv(OUTPUTS["ppn_fill"], generated["ppn_fill"])
    write_csv(OUTPUTS["route_guards"], generated["route_guards"])
    write_csv(OUTPUTS["claim_gates"], generated["claim_gates"])
    write_csv(OUTPUTS["decision"], generated["decision"])
    write_csv(OUTPUTS["next_target"], generated["next_target"])
    copy_branch_artifacts()
    generated["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], generated["branch_copies"])

    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(generated, validation)

    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
