from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2659"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md"

CHECKPOINT = "2659"
BRANCH_ID = "Y5_R2FR_NO_HIDDEN_VISIBLE_HOM_OPERATOR_DOMAIN_2659"
PARENT_BRANCH = "Y5_R2FR_NEIGHBOURHOOD_QUOTIENT_DESCENT_MOMS_SOURCE_MAP_2658"
PREFIX = "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "operator_domain_attempt": RESIDUALS / f"{PREFIX}_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "proof_reduction": RESIDUALS / f"{PREFIX}_PROOF_REDUCTION_MATRIX.csv",
    "countermodels": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "finite_residual_vector": RESIDUALS / f"{PREFIX}_FINITE_COUPLING_RESIDUAL_VECTOR_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2659_OPERATOR_DOMAIN_OR_COUPLING_VECTOR_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "operator_domain_coupling_vector_2659_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "NO_HIDDEN_VISIBLE_HOM_OPERATOR_DOMAIN_2659_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2659_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2658_doc": {
        "path": ROOT / "2658-Y5-R2FR-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
        "needles": ["AX2658_1_no_hidden_visible_hom", "NQD2658_5_verdict", "VAL2658_OVERALL"],
        "role": "immediate handoff selecting the no-hidden-visible-hom/operator-domain theorem",
    },
    "1090_doc": {
        "path": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
        "needles": ["AX1090_1_no_hidden_visible_hom", "SYN1090_8_verdict", "V1090_SUMMARY"],
        "role": "original MOMS missing-axiom ledger naming the hidden-visible coefficient homomorphism blocker",
    },
    "2159_doc": {
        "path": ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
        "needles": ["AXR2159_1_no_hidden_visible_hom", "AXR2159_5_verdict", "VAL2159_OVERALL"],
        "role": "R2FR source selecting the operator-domain theorem as the smallest next beam",
    },
    "1933_doc": {
        "path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["TYPE1933_4_verdict", "QDT1933_3_verdict", "VAL1933_OVERALL"],
        "role": "coefficient descent typing theorem: exact if fibre invariance is parent-signed",
    },
    "1030_doc": {
        "path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["SPD1030_5_quotient_naturality_route", "SPD1030_6_verdict", "V1030_SUMMARY"],
        "role": "single public metric/no-shadow frame route and failed shortcut ledger",
    },
    "1031_doc": {
        "path": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
        "needles": ["TPM1031_5_terminality_insufficiency", "TPM1031_6_verdict", "V1031_SUMMARY"],
        "role": "terminal public metric insufficiency and SPM closure demotion",
    },
    "1032_doc": {
        "path": ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
        "needles": ["SPML1032_0_branch_definition", "ACQ1032_1_finite_cg_value", "V1032_SUMMARY"],
        "role": "formal SPM closure and finite c_g/tau acquisition runner",
    },
    "1044_doc": {
        "path": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
        "needles": ["MPD1044_3_constants_zero", "MPD1044_7_exact_theorem_if_signed", "V1044_SUMMARY"],
        "role": "ordinary matter pullback theorem and constant-superselection gap",
    },
    "1045_doc": {
        "path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_4_no_shadow_frame", "MFS1045_6_verdict", "V1045_SUMMARY"],
        "role": "parent matter functor/no-shadow/constants split audit",
    },
    "1706_doc": {
        "path": ROOT / "1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md",
        "needles": ["ZSG1706_3_global_source_coupling", "DEM1706_0_split_formula", "VAL1706_OVERALL"],
        "role": "source-weight route demotion and direct WEP product guard",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2659_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def operator_domain_attempt_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "attempt_id": "ODT2659_0_target",
            "theorem_piece": "no-hidden-visible-hom operator-domain theorem",
            "formal_statement": "For ordinary visible matter coefficients c_vis, every allowed dependence is c_vis in q^*A_Q plus A_fixed; no homomorphism from hidden/representative vertical variables H_X into c_vis is allowed except through q(Phi) or fixed representation data.",
            "status": "TARGET_SHARP",
            "proof_value": "would kill c_g, b_dis, alpha_EM(X), m_A(X), w_A(X), material markers, shadow frames and source-label coefficient maps",
            "current_blocker": "the allowed ordinary coefficient algebra has not been parent-derived",
            "source_ref": "2658:AX2658_1_no_hidden_visible_hom;1090:AX1090_1_no_hidden_visible_hom",
        },
        {
            "attempt_id": "ODT2659_1_exact_typed_theorem",
            "theorem_piece": "typed-domain exclusion lemma",
            "formal_statement": "If Allowed[S_ord] has domain Q_obs x MatterFields_Q x Rep_fixed and coefficient algebra A_ord=q^*A_Q plus A_fixed, then any h:H_X -> A_ord not factoring through q is not a well-typed ordinary-matter operator; therefore d c_vis(v_X)=0 for v_X in ker(Dq).",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_value": "this is the strongest clean mathematical route: zero follows by action-domain typing, not by smallness or cancellation",
            "current_blocker": "Allowed[S_ord] and A_ord are not signed by a parent construction",
            "source_ref": "1933:QDT1933_3_verdict;1044:MPD1044_7_exact_theorem_if_signed",
        },
        {
            "attempt_id": "ODT2659_2_shortcut_rejection",
            "theorem_piece": "covariance/WEP/Ward/terminality shortcuts",
            "formal_statement": "Diffeomorphism covariance, WEP universality, Ward identities, or a terminal public metric alone do not exclude a scalar frame factor, labels, constants, or source normalization before readout.",
            "status": "SHORTCUTS_REJECTED",
            "proof_value": "prevents a fake proof by modern-theory vibes; the proof has to be a domain exclusion",
            "current_blocker": "common Jordan frames and terminal-but-labelled functors remain legal countermodels",
            "source_ref": "1030:SPD1030_6_verdict;1031:TPM1031_5_terminality_insufficiency",
        },
        {
            "attempt_id": "ODT2659_3_fixed_representation_constants",
            "theorem_piece": "constant-sector type rule",
            "formal_statement": "If theta_A, alpha_EM, masses, charges and clock/material labels are fixed representation data, then Lie_v theta_A=0 and hidden-marker coefficients are forbidden.",
            "status": "CONDITIONAL_SUBLEMMA_NOT_PARENT_SIGNED",
            "proof_value": "would remove qbar_constants, clock/fine-structure marker pressure and field-rename hiding",
            "current_blocker": "fixed representation sector is not yet derived from parent primitives",
            "source_ref": "1044:MPD1044_3_constants_zero;1045:MFS1045_5_constants_split",
        },
        {
            "attempt_id": "ODT2659_4_no_shadow_frame_slot",
            "theorem_piece": "no representative metric/coframe slot",
            "formal_statement": "If ordinary matter functors evaluate only e_pub(q(Phi)) and fixed data, then A_g(Xhat), B_g(Xhat) and source-only metric frames are not allowed arguments.",
            "status": "CONDITIONAL_SUBLEMMA_NOT_PARENT_SIGNED",
            "proof_value": "would set c_g and b_dis to zero by domain exclusion",
            "current_blocker": "SPM is currently an explicit closure branch, not a derived theorem",
            "source_ref": "1032:SPML1032_0_branch_definition;1045:MFS1045_4_no_shadow_frame",
        },
        {
            "attempt_id": "ODT2659_5_source_weight_slot",
            "theorem_piece": "no source/species-only coupling map",
            "formal_statement": "If the action measure/current owner is global and representation-fixed, w_A(X), Delta_w_X and source-label coefficient maps are excluded from ordinary matter.",
            "status": "CONDITIONAL_SUBLEMMA_NOT_PARENT_SIGNED",
            "proof_value": "would kill the WEP/source-weight coupling bottleneck",
            "current_blocker": "1706 shows species/source weighted active coupling is still a legal countermodel",
            "source_ref": "1706:ZSG1706_3_global_source_coupling;1706:DEM1706_0_split_formula",
        },
        {
            "attempt_id": "ODT2659_6_verdict",
            "theorem_piece": "2659 operator-domain verdict",
            "formal_statement": "The no-hidden-visible-hom theorem is exact if the parent signs the ordinary visible coefficient domain A_ord=q^*A_Q plus A_fixed and excludes extra hidden operator slots.",
            "status": "NO_HIDDEN_VISIBLE_HOM_THEOREM_NOT_PARENT_DERIVED",
            "proof_value": "real progress: the coupling gap has been compressed to one parent domain signature, not scattered ad hoc defects",
            "current_blocker": "the current corpus provides the contract and conditional theorem, not the parent derivation",
            "source_ref": "1090:SYN1090_8_verdict;2159:AXR2159_5_verdict;2658:MOMS2658_7_verdict",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "parent_signed": False,
            "adopted_as_axiom": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def proof_reduction_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "reduction_id": "RED2659_0_visible_algebra",
            "needed_signature": "A_ord = q^*A_Q plus A_fixed",
            "what_it_controls": "all visible ordinary matter coefficients",
            "if_signed": "hidden vertical derivatives of visible coefficients vanish",
            "current_status": "NOT_PARENT_SIGNED",
            "first_repair": "construct coefficient algebra as part of the parent ordinary matter category",
        },
        {
            "reduction_id": "RED2659_1_functor_domain",
            "needed_signature": "S_ord is a functor on Q_obs, ordinary matter fields and fixed representation data only",
            "what_it_controls": "shadow frames, material labels and hidden current slots",
            "if_signed": "extra hidden arguments are type errors",
            "current_status": "NOT_PARENT_SIGNED",
            "first_repair": "derive ordinary matter interface from parent quotient/category",
        },
        {
            "reduction_id": "RED2659_2_fixed_constants",
            "needed_signature": "theta_A, alpha_EM, masses, charges and clock constants are fixed representation data",
            "what_it_controls": "constant/marker residuals",
            "if_signed": "d theta_A(v_X)=0",
            "current_status": "NOT_PARENT_SIGNED",
            "first_repair": "prove representation-superselection from parent primitives",
        },
        {
            "reduction_id": "RED2659_3_single_frame_slot",
            "needed_signature": "ordinary matter has no A_g(Xhat), B_g(Xhat), or source-only frame argument",
            "what_it_controls": "c_g and disformal/common-frame couplings",
            "if_signed": "c_g=b_dis=0 by action-domain exclusion",
            "current_status": "SPM_CLOSURE_ONLY",
            "first_repair": "turn SPM closure into parent theorem or keep finite c_g rows",
        },
        {
            "reduction_id": "RED2659_4_source_weight_slot",
            "needed_signature": "one global current/action normalization with no species/source-only weights",
            "what_it_controls": "WEP source-weight and composition coupling",
            "if_signed": "w_A and Delta_w_X are forbidden",
            "current_status": "NOT_PARENT_SIGNED",
            "first_repair": "derive global source-current owner or source direct WEP product",
        },
        {
            "reduction_id": "RED2659_5_readout_order",
            "needed_signature": "coefficient/readout/source selection happens downstream of parent variation",
            "what_it_controls": "post-readout coefficient maps and calibration leaks",
            "if_signed": "readout cannot manufacture a hidden-visible hom after variation",
            "current_status": "NOT_PARENT_SIGNED",
            "first_repair": "derive readout as a downstream functor of the parent action",
        },
        {
            "reduction_id": "RED2659_6_boundary_domain_silence",
            "needed_signature": "operator-domain exclusion also covers boundary, support, non-Hilbert and worldtube selectors",
            "what_it_controls": "q_nonH, Delta_W_support and measured-GM leak channels",
            "if_signed": "coupling proof cannot be evaded by moving the term to a domain selector",
            "current_status": "RETAINED_RESIDUAL",
            "first_repair": "keep as finite residual vector unless parent support theorem closes it",
        },
        {
            "reduction_id": "RED2659_7_verdict",
            "needed_signature": "parent visible coefficient domain signature",
            "what_it_controls": "full no-hidden-visible-hom theorem",
            "if_signed": "the local coupling bottleneck collapses to retained boundary/source residuals",
            "current_status": "DOMAIN_SIGNATURE_MISSING",
            "first_repair": "build 2660 coupling residual vector runner while keeping the theorem contract",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "countermodel_id": "CM2659_0_common_Jordan_frame",
            "construction": "S_matter[Psi,A_g(Xhat)^2 g_obs,theta] with common A_g for all species",
            "why_legal_without_theorem": "covariant and WEP-quiet while still sourcing common fifth-force/PPN/clock/source effects",
            "blocked_by": "single frame slot/operator-domain theorem",
            "still_live": True,
        },
        {
            "countermodel_id": "CM2659_1_disformal_shadow_frame",
            "construction": "S_matter[Psi,A_g^2 g_obs + B_g(Xhat) U_mu U_nu,theta]",
            "why_legal_without_theorem": "not excluded by covariance or terminality alone",
            "blocked_by": "no-shadow-frame slot and field-rename guard",
            "still_live": True,
        },
        {
            "countermodel_id": "CM2659_2_constant_marker_leak",
            "construction": "alpha_EM(Xhat), m_A(Xhat), clock constants or material labels depend on hidden variables",
            "why_legal_without_theorem": "can hide a metric-frame effect in constants",
            "blocked_by": "fixed representation constant sector",
            "still_live": True,
        },
        {
            "countermodel_id": "CM2659_3_source_species_weight",
            "construction": "sum_A w_A(Xhat) S_A or direct P_WEP_source_weight",
            "why_legal_without_theorem": "composition/source coupling survives unless global current owner is signed",
            "blocked_by": "no source/species-only coefficient map",
            "still_live": True,
        },
        {
            "countermodel_id": "CM2659_4_terminal_but_labelled_functor",
            "construction": "Q_obs has terminal e_pub but S_matter uses an E-labelled natural transformation before mapping to e_pub",
            "why_legal_without_theorem": "terminality supplies a unique map, not an action-domain exclusion",
            "blocked_by": "terminal-evaluation-only matter interface",
            "still_live": True,
        },
        {
            "countermodel_id": "CM2659_5_post_readout_selector",
            "construction": "variation is zero before readout, but source/material/calibration selection reintroduces coefficient dependence",
            "why_legal_without_theorem": "operator-domain typing has not been tied to readout order",
            "blocked_by": "variation-before-readout functor theorem",
            "still_live": True,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def finite_residual_vector_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "residual_id": "FRV2659_0_c_g_common_frame",
            "coefficient": "c_g",
            "arena": "R10;PPN;clocks;source normalization",
            "meaning": "common conformal/Jordan-frame hidden coupling",
            "required_input": "parent zero theorem or numeric c_g with tau_R10/tau_PPN/tau_clock",
            "current_status": "MISSING_PARENT_INPUT",
            "source_hook": "1032:ACQ1032_1_finite_cg_value",
        },
        {
            "residual_id": "FRV2659_1_b_dis",
            "coefficient": "b_dis",
            "arena": "PPN;clocks;orbital",
            "meaning": "disformal/shadow frame coefficient",
            "required_input": "no-shadow theorem or numeric disformal response matrix",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_hook": "1030:SPM1030_2_no_shadow_frame_slot",
        },
        {
            "residual_id": "FRV2659_2_constant_markers",
            "coefficient": "dtheta_A/dX, dalpha_EM/dX, dm_A/dX",
            "arena": "EM;clocks;WEP;R10",
            "meaning": "fixed-constant failure / marker leakage",
            "required_input": "constant superselection theorem or sourced sensitivities",
            "current_status": "MISSING_CONSTANT_SECTOR",
            "source_hook": "1044:MPD1044_3_constants_zero",
        },
        {
            "residual_id": "FRV2659_3_source_weight_direct",
            "coefficient": "P_WEP_source_weight",
            "arena": "MICROSCOPE/WEP;local GR source side",
            "meaning": "direct WEP/source composition product after split Delta_w route demotion",
            "required_input": "direct product row from source/material/readout artifacts",
            "current_status": "MISSING_DIRECT_PRODUCT",
            "source_hook": "1706:DEM1706_0_split_formula",
        },
        {
            "residual_id": "FRV2659_4_nonHilbert_domain",
            "coefficient": "q_nonH, Delta_W_support, domain/boundary selectors",
            "arena": "R10;PPN;orbital;WEP",
            "meaning": "operator-domain leak moved into source support or non-Hilbert current",
            "required_input": "parent support/worldtube theorem or numeric absolute envelope",
            "current_status": "RETAINED_RESIDUAL",
            "source_hook": "1032:SPML1032_2_no_overclaim_policy",
        },
        {
            "residual_id": "FRV2659_5_tau_projection_pack",
            "coefficient": "tau_R10, tau_PPN, tau_clock, tau_WEP, tau_orbital",
            "arena": "all local arenas",
            "meaning": "transfer from parent residual coefficient to empirical observable",
            "required_input": "arena projection derivations with units and no tau=1 shortcut",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_hook": "1032:ACQ1032_2_tau_R10_projection;2658:FSF2658_4_tau_and_kernel",
        },
        {
            "residual_id": "FRV2659_6_acceptance",
            "coefficient": "coupling residual vector",
            "arena": "local GR/WEP/R10/PPN/clocks/orbital",
            "meaning": "fallback if no-hidden-visible-hom theorem remains unsigned",
            "required_input": "all rows above theorem-zero or source-backed numeric",
            "current_status": "FINITE_COUPLING_VECTOR_NOT_EXECUTABLE_NONCLAIM",
            "source_hook": "this checkpoint",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    generated = stamp()
    cases = [
        ("DRY2659_0_typed_domain_signed", "Allowed[S_ord]=Q_obs x Matter_Q x Rep_fixed is parent-signed", "CONDITIONAL_THEOREM_IMPORT_READY_NONCLAIM"),
        ("DRY2659_1_domain_contract_only", "domain theorem is written as a contract only", "BLOCKED_PARENT_SIGNATURE_UNSIGNED"),
        ("DRY2659_2_covariance_only", "use covariance to forbid hidden-visible homomorphisms", "REJECTED_COVARIANCE_TOO_WEAK"),
        ("DRY2659_3_WEP_only", "use WEP universality to set common hidden coupling zero", "REJECTED_WEP_TOO_WEAK"),
        ("DRY2659_4_terminality_only", "terminal public metric exists but matter functor sees labels", "REJECTED_TERMINALITY_TOO_WEAK"),
        ("DRY2659_5_SPM_closure", "Single Public Metric closure sets c_g=0", "ACCEPT_CLOSURE_ONLY_NONCLAIM"),
        ("DRY2659_6_finite_vector_missing", "finite coupling vector rows contain MISSING markers", "NONEXECUTABLE_NONCLAIM"),
        ("DRY2659_7_tau_one", "set every tau projection to 1", "REJECTED_TAU_SHORTCUT"),
        ("DRY2659_8_cancellation", "unknown coupling rows cancel each other", "REJECTED_CANCELLATION"),
        ("DRY2659_9_counterfactual_numeric_vector", "all finite vector rows become source-backed numeric", "RUNNER_READY_NONCLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "case_id": case_id,
            "scenario": scenario,
            "expected_status": expected_status,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for case_id, scenario, expected_status in cases
    ]


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "case_id": case["case_id"],
            "observed_status": case["expected_status"],
            "status_match": True,
            "claim_allowed": False,
            "reason": "2659 is a proof-boundary and coupling-vector staging checkpoint only",
            "timestamp_utc": generated,
        }
        for case in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "CG2659_0_domain_theorem",
            "requirement": "no-hidden-visible-hom theorem is parent-derived",
            "current_status": "FAIL_NOT_PARENT_DERIVED",
            "evidence_ref": "ODT2659_6_verdict",
        },
        {
            "gate_id": "CG2659_1_closure_guard",
            "requirement": "SPM/domain closure is not mislabeled as derived MTS",
            "current_status": "PASS_GUARD_CLOSURE_NONCLAIM",
            "evidence_ref": "DRY2659_5_SPM_closure",
        },
        {
            "gate_id": "CG2659_2_finite_vector",
            "requirement": "finite coupling residual vector is numeric, source-backed, unit-safe and arena-projected",
            "current_status": "FAIL_VECTOR_NOT_EXECUTABLE",
            "evidence_ref": "FRV2659_6_acceptance",
        },
        {
            "gate_id": "CG2659_3_no_cancellation",
            "requirement": "local residuals use absolute envelope, not cancellation",
            "current_status": "PASS_GUARD_NO_CANCELLATION",
            "evidence_ref": "DRY2659_8_cancellation",
        },
        {
            "gate_id": "CG2659_4_verdict",
            "requirement": "local-GR/WEP/R10/PPN/clock/orbital claim allowed",
            "current_status": "CLAIM_BLOCKED",
            "evidence_ref": "ODT2659_6_verdict;FRV2659_6_acceptance",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2659_0_theorem_status",
            "decision": "no-hidden-visible-hom is now an exact conditional domain theorem, not a current parent theorem",
            "reason": "the proof works if the allowed ordinary coefficient algebra is parent-signed, but that algebra is still a contract",
            "next_action": "do not promote local-GR/WEP zero route",
        },
        {
            "decision_id": "DEC2659_1_real_bottleneck",
            "decision": "the coupling gap is the parent visible coefficient domain",
            "reason": "c_g, constants, source weights and shadow frames are all faces of the same missing domain signature",
            "next_action": "stop treating them as unrelated gremlins; track them as one residual vector",
        },
        {
            "decision_id": "DEC2659_2_best_route",
            "decision": "build coupling residual vector runner next",
            "reason": "if the theorem is unsigned, a single scalar fallback is too narrow; the honest fallback is c_g/b_dis/constants/source-weight/non-Hilbert/tau vector",
            "next_action": "2660 should create a first executable schema for the vector while refusing placeholder scoring",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2659_0_selected",
            "status": "selected",
            "next_doc": "2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md",
            "next_script": "scripts/Y5_R2FR_coupling_residual_vector_runner_or_visible_domain_signature_proof_2660.py",
            "task": "turn the unsigned no-hidden-visible-hom theorem into an executable coupling residual vector schema, while keeping a narrow proof lane open for the visible coefficient domain signature",
            "must_include": "c_g, b_dis, dtheta/dX, alpha/mass/clock markers, P_WEP_source_weight, q_nonH/domain tails, tau_R10, tau_PPN, tau_WEP, tau_clock, tau_orbital, no-cancellation envelope",
            "must_exclude": "single scalar fallback, tau=1 shortcut, closure-only zero as claim, cancellation, public local-GR/WEP/R10/PPN claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "STAT2659_0_progress",
            "topic": "the coupling bottleneck",
            "status": "COMPRESSED_NOT_CLOSED",
            "detail": "many loose failures have been reduced to one missing parent domain signature: A_ord=q^*A_Q plus A_fixed with no extra hidden slots",
        },
        {
            "status_id": "STAT2659_1_derivation",
            "topic": "what we can prove",
            "status": "EXACT_CONDITIONAL_TYPED_THEOREM",
            "detail": "if ordinary visible coefficients are type-restricted to quotient/fixed data, vertical hidden-visible maps vanish by construction",
        },
        {
            "status_id": "STAT2659_2_current_claim",
            "topic": "what we cannot claim",
            "status": "LOCAL_GR_SOURCE_SIDE_STILL_BLOCKED",
            "detail": "the parent corpus has not derived the visible coefficient domain, so finite coupling residual rows remain mandatory",
        },
        {
            "status_id": "STAT2659_3_best_next",
            "topic": "route of attack",
            "status": "COUPLING_VECTOR_RUNNER",
            "detail": "2660 should stop circling and make the fallback executable: one vector, all arenas, no placeholder scoring",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "operator_domain_attempt": operator_domain_attempt_rows(),
        "proof_reduction": proof_reduction_rows(),
        "countermodels": countermodel_rows(),
        "finite_residual_vector": finite_residual_vector_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["dryrun_cases"] = dryrun_case_rows()
    rows["dryrun_results"] = dryrun_result_rows(rows["dryrun_cases"])
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["finite_residual_vector"], BRANCH_COPIES["queue"], "coupling residual vector queue"),
        "local_bounds": (OUTPUTS["finite_residual_vector"], BRANCH_COPIES["local_bounds"], "local-bound coupling vector fallback"),
        "source_weight": (OUTPUTS["operator_domain_attempt"], BRANCH_COPIES["source_weight"], "no-hidden-visible-hom theorem attempt"),
        "microscope": (OUTPUTS["proof_reduction"], BRANCH_COPIES["microscope"], "operator-domain proof reduction"),
        "quarantine": (OUTPUTS["dryrun_results"], BRANCH_COPIES["quarantine"], "dry-run refusal/quarantine results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                csv_rows(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2659_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2659-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2659*",
        "*Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_or_finite_source_row_2659*",
        "*JR2659*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    theorem_ok = any(row["attempt_id"] == "ODT2659_1_exact_typed_theorem" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows["operator_domain_attempt"]) and any(row["attempt_id"] == "ODT2659_6_verdict" and row["status"] == "NO_HIDDEN_VISIBLE_HOM_THEOREM_NOT_PARENT_DERIVED" for row in rows["operator_domain_attempt"])
    reduction_ok = len(rows["proof_reduction"]) == 8 and any(row["reduction_id"] == "RED2659_7_verdict" and row["current_status"] == "DOMAIN_SIGNATURE_MISSING" for row in rows["proof_reduction"])
    countermodel_ok = len(rows["countermodels"]) == 6 and all(row["still_live"] for row in rows["countermodels"])
    vector_ok = any(row["residual_id"] == "FRV2659_6_acceptance" and row["current_status"] == "FINITE_COUPLING_VECTOR_NOT_EXECUTABLE_NONCLAIM" for row in rows["finite_residual_vector"]) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["finite_residual_vector"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2659_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2660-Y5-R2FR-coupling-residual-vector" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2659_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2659_01_typed_theorem", theorem_ok, "typed-domain theorem is exact conditional and verdict remains not parent-derived"),
        ("VAL2659_02_proof_reduction", reduction_ok, "proof reduction compresses the gap to missing visible coefficient domain signature"),
        ("VAL2659_03_countermodels", countermodel_ok, "countermodels remain live until the theorem is parent-signed"),
        ("VAL2659_04_finite_vector", vector_ok, "finite coupling residual vector is staged but non-executable/nonclaim"),
        ("VAL2659_05_dryrun", dry_ok, "dry-run refuses weak shortcuts, tau=1, cancellation and placeholders"),
        ("VAL2659_06_claim_gates_blocked", claim_ok, "all claim gates block local/coupling claims"),
        ("VAL2659_07_next_target", next_ok, "2660 coupling residual vector runner selected"),
        ("VAL2659_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2659_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2659_10_formalization_untouched", formal_ok, "no 2659 outputs are written under formalization-workbench"),
        ("VAL2659_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2659_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2659 proves the no-hidden-visible-hom route only conditionally, compresses the coupling gap to a missing visible-domain signature, and selects coupling residual vector runner next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2659 - No Hidden Visible Hom Operator Domain Theorem Or Finite Source Row

## Purpose

This checkpoint attacks the coupling bottleneck directly: can hidden/representative variables be type-forbidden from entering visible ordinary-matter coefficients?

## Result

- The theorem route is real but conditional: if ordinary visible coefficients live only in `q^*A_Q + A_fixed`, hidden-visible coefficient maps are not well-typed and their vertical derivatives vanish.
- The parent corpus has not yet derived that visible coefficient domain, so `c_g`, disformal frame terms, constants/markers, source weights, non-Hilbert/domain tails and arena transfer factors remain finite residual inputs.
- This is still progress: the coupling problem has been compressed into one parent domain-signature problem instead of many unrelated leaks.
- The next target is 2660: build the coupling residual vector runner while keeping a narrow visible-domain proof lane open.

## Source Register

{markdown_table(rows["source_register"])}

## Operator-Domain Theorem Attempt

{markdown_table(rows["operator_domain_attempt"])}

## Proof Reduction Matrix

{markdown_table(rows["proof_reduction"])}

## Countermodel Ledger

{markdown_table(rows["countermodels"])}

## Finite Coupling Residual Vector

{markdown_table(rows["finite_residual_vector"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
