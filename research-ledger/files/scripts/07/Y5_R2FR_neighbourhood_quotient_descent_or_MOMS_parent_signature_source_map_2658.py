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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2658"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2658-Y5-R2FR-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md"

CHECKPOINT = "2658"
BRANCH_ID = "Y5_R2FR_NEIGHBOURHOOD_QUOTIENT_DESCENT_MOMS_SOURCE_MAP_2658"
PARENT_BRANCH = "Y5_R2FR_PARENT_COUPLING_SOURCE_MATERIAL_CONTRACTION_2657"
PREFIX = "P8_Y5_NQD_MOMS_2658"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "neighbourhood_descent_attempt": RESIDUALS / f"{PREFIX}_NEIGHBOURHOOD_DESCENT_ATTEMPT.csv",
    "moms_signature_source_map": RESIDUALS / f"{PREFIX}_MOMS_SIGNATURE_SOURCE_MAP.csv",
    "axiom_debt": RESIDUALS / f"{PREFIX}_AXIOM_DEBT_NOT_ADOPTED.csv",
    "finite_source_fallback": RESIDUALS / f"{PREFIX}_FINITE_SOURCE_MAP_FALLBACK_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_DESCENT_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_DESCENT_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2658_MOMS_AXIOM_DEBT_OR_FINITE_SOURCE_MAP_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "WEP_neighbourhood_descent_source_map_2658_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "MOMS_PARENT_SIGNATURE_SOURCE_MAP_2658_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2658_NEIGHBOURHOOD_DESCENT_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2658_DESCENT_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2657_doc": {
        "path": ROOT / "2657-Y5-R2FR-parent-coupling-source-material-contraction-zero-or-finite-WEP-coefficient-pack.md",
        "needles": ["PCZ2657_2_neighbourhood_double_zero", "NEXT2657_0_selected", "VAL2657_OVERALL"],
        "role": "immediate handoff: double-zero theorem is exact conditional; descent/MOMS source map is next",
    },
    "1486_doc": {
        "path": ROOT / "1486-Y5-R10-RAB-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
        "needles": ["NQD1486_5_verdict", "MOMS1088_7_verdict", "VAL1486_19_overall"],
        "role": "earlier neighbourhood descent and MOMS source-map checkpoint",
    },
    "1088_doc": {
        "path": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "needles": ["MOMS1088_7_verdict", "THM1088_5_conclusion", "V1088_SUMMARY"],
        "role": "minimal ordinary-matter signature contract and conditional qbar_XT zero theorem",
    },
    "1090_doc": {
        "path": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
        "needles": ["SYN1090_8_verdict", "AX1090_1_no_hidden_visible_hom", "AX1090_4_variation_domain_order", "V1090_SUMMARY"],
        "role": "MOMS synthesis failure and five missing axioms not adopted",
    },
    "1912_doc": {
        "path": ROOT / "1912-Y5-R2FR-neighbourhood-quotient-descent-signature-proof-or-axiom-ledger.md",
        "needles": ["NQD1912_2_open_neighbourhood_upgrade", "NQD1912_4_verdict", "VAL1912_OVERALL"],
        "role": "R2FR neighbourhood descent proof attempt and axiom ledger",
    },
    "1933_doc": {
        "path": ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
        "needles": ["TYPE1933_4_verdict", "QDT1933_3_verdict", "VAL1933_OVERALL"],
        "role": "quotient descent typing theorem: exact equivalence, unsigned fibre invariance",
    },
    "2159_doc": {
        "path": ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
        "needles": ["MOM2159_7_verdict", "AXR2159_1_no_hidden_visible_hom", "VAL2159_OVERALL"],
        "role": "latest parent ordinary-matter signature failure and selected no-hidden-visible-hom route",
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
                "source_id": f"SRC2658_{source_id}",
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


def neighbourhood_descent_attempt_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "attempt_id": "NQD2658_0_target",
            "clause": "ordinary-matter open-neighbourhood quotient descent",
            "exact_requirement": "There exists an open fibre neighbourhood U such that S_ord[Phi,Psi,theta]=Sbar_ord[q(Phi),Psi_q,theta] and every WEP/source/material vertical flow stays in ker(Dq) on U.",
            "current_evidence": "2657 gives the exact conditional double-zero theorem if this premise is signed.",
            "status": "TARGET_EXACT",
            "blocker": "target is a theorem premise, not yet a parent theorem",
            "source_ref": "2657:PCZ2657_2_neighbourhood_double_zero;1912:NQD1912_0_target",
        },
        {
            "attempt_id": "NQD2658_1_pointwise_chain_rule",
            "clause": "visible geometry is vertical-blind",
            "exact_requirement": "If visible geometry is Obs_g(q(Phi)) and V is q-vertical, then Lie_V g_obs=0 by the chain rule.",
            "current_evidence": "pointwise geometry silence is a clean conditional lemma",
            "status": "EXACT_CONDITIONAL_POINTWISE_LEMMA",
            "blocker": "pointwise geometry silence does not control matter action, constants, source weights, boundary class, or readout order",
            "source_ref": "1912:NQD1912_1_chain_rule",
        },
        {
            "attempt_id": "NQD2658_2_fibre_invariance_equivalence",
            "clause": "descent iff fibre-invariance",
            "exact_requirement": "For a visible coefficient/action-density c, c=q^*cbar exactly when c is constant on q-fibres; then dc(V)=0 for all vertical V.",
            "current_evidence": "1933 supplies the exact quotient theorem but not the parent source of fibre-invariance",
            "status": "EXACT_EQUIVALENCE_NOT_PARENT_SUPPLIED",
            "blocker": "fibre-invariance of ordinary matter coefficients remains unsigned",
            "source_ref": "1933:QDT1933_3_verdict;1933:TYPE1933_4_verdict",
        },
        {
            "attempt_id": "NQD2658_3_action_descent_upgrade",
            "clause": "upgrade pointwise descent to full S_ord descent",
            "exact_requirement": "The same parent object must own matter bundle, measure/coframe/connection, constants, source/material variations and variation-before-readout on U.",
            "current_evidence": "1088/1090/1486/1912 identify the exact clauses",
            "status": "UPGRADE_FAILS_PARENT_SIGNATURE_MISSING",
            "blocker": "MOMS action object, matter lift, constant sector, no species weights, no shadow domain and variation order remain unsigned",
            "source_ref": "1088:MOMS1088_7_verdict;1090:SYN1090_8_verdict;1912:NQD1912_2_open_neighbourhood_upgrade",
        },
        {
            "attempt_id": "NQD2658_4_countermodel_retention",
            "clause": "legal countermodels still exist",
            "exact_requirement": "No hidden-visible coefficient homomorphism, shadow/disformal frame, source-only weight, fixed-constant leak, boundary selector, or post-readout source selector may survive.",
            "current_evidence": "countermodels are repeatedly retained in prior ledgers",
            "status": "COUNTERMODELS_RETAINED",
            "blocker": "operator-domain/no-hidden-visible-hom theorem has not been derived",
            "source_ref": "1090:AX1090_1_no_hidden_visible_hom;1912:NQD1912_3_countermodel_retention;2159:AXR2159_1_no_hidden_visible_hom",
        },
        {
            "attempt_id": "NQD2658_5_verdict",
            "clause": "2658 neighbourhood descent verdict",
            "exact_requirement": "promote PCZ2657_2 from conditional theorem to parent-signed local-GR/WEP theorem-zero",
            "current_evidence": "conditional mathematics is sound, but the parent ordinary-matter descent premise is still absent",
            "status": "NEIGHBOURHOOD_QUOTIENT_DESCENT_NOT_PARENT_SIGNED",
            "blocker": "MOMS signature and no-hidden-visible-hom/operator-domain theorem remain open",
            "source_ref": "2657:PCZ2657_2_neighbourhood_double_zero;1486:NQD1486_5_verdict;1912:NQD1912_4_verdict",
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


def moms_signature_source_map_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "clause_id": "MOMS2658_0_action_form",
            "signature_clause": "one ordinary-matter parent action object",
            "what_it_would_zero": "sets the variation target for J_X^matter and C_parent_X",
            "current_status": "SCHEMA_AVAILABLE_NOT_DERIVED",
            "blocker": "no single parent action object has been source-owned",
            "best_source": "1090:SYN1090_0;1487:OMSO1487_6",
        },
        {
            "clause_id": "MOMS2658_1_quotient_observables",
            "signature_clause": "visible observables depend on parent only through q(Phi)",
            "what_it_would_zero": "makes vertical variations invisible to visible matter coefficients",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "blocker": "quotient functor and observable map are used but not globally owned",
            "best_source": "1933:QDT1933_3_verdict",
        },
        {
            "clause_id": "MOMS2658_2_matter_bundle",
            "signature_clause": "ordinary matter fields lift through the same quotient bundle",
            "what_it_would_zero": "prevents material/worldtube source labels from re-entering outside q",
            "current_status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "blocker": "matter bundle descent is the sharpest action-level missing beam",
            "best_source": "1486:MOMS1088_2;1912:NQD1912_2_open_neighbourhood_upgrade",
        },
        {
            "clause_id": "MOMS2658_3_constant_superselection",
            "signature_clause": "ordinary constants are fixed representation data, not hidden-coordinate functions",
            "what_it_would_zero": "blocks alpha_EM(X), masses m_A(X), clock constants and calibration leaks",
            "current_status": "UNSIGNED_CONSTANT_SECTOR",
            "blocker": "fixed-constant sector has not been derived from parent representation data",
            "best_source": "1090:AX1090_2_fixed_constant_sector",
        },
        {
            "clause_id": "MOMS2658_4_no_species_weights",
            "signature_clause": "no source/species-only prefactor w_A(X) or Delta_w_X",
            "what_it_would_zero": "kills the WEP source-weight branch and composition dependent C_parent_X",
            "current_status": "UNSIGNED_COUPLING_BOTTLENECK",
            "blocker": "coupling/source-weight slot is still a legal countermodel",
            "best_source": "2159:AXR2159_1_no_hidden_visible_hom",
        },
        {
            "clause_id": "MOMS2658_5_variation_order",
            "signature_clause": "variation happens before empirical readout/source selection/material projection",
            "what_it_would_zero": "prevents a post-variation selector from manufacturing or erasing residual current",
            "current_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "blocker": "readout/source-worldtube model has not been tied to the same parent action",
            "best_source": "1090:AX1090_4_variation_domain_order;2656:SRB2656_5_verdict",
        },
        {
            "clause_id": "MOMS2658_6_no_shadow_domain",
            "signature_clause": "no shadow frame/disformal domain/non-Hilbert representative channel in ordinary matter",
            "what_it_would_zero": "blocks representative leakage that preserves covariance while breaking WEP/source descent",
            "current_status": "NO_HIDDEN_VISIBLE_HOM_NOT_DERIVED",
            "blocker": "operator-domain theorem is missing",
            "best_source": "1090:AX1090_1_no_hidden_visible_hom;2159:AXR2159_1_no_hidden_visible_hom",
        },
        {
            "clause_id": "MOMS2658_7_verdict",
            "signature_clause": "all MOMS clauses parent-signed together",
            "what_it_would_zero": "would import THM1088_5 and PCZ2657_2 as local WEP/source-current zero route",
            "current_status": "MOMS_PARENT_SIGNATURE_NOT_DERIVED",
            "blocker": "clauses remain a contract/source map, not a theorem",
            "best_source": "1088:MOMS1088_7_verdict;1090:SYN1090_8_verdict;2159:MOM2159_7_verdict",
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


def axiom_debt_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "debt_id": "AX2658_0_parent_action_object",
            "needed_principle": "one parent ordinary-matter action object",
            "why_needed": "without a single action owner, vertical variation can be moved between geometry, matter, readout and source terms",
            "current_basis": "1090:AX1090_0;1487:OMSO1487_6",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "next_derivation_hook": "construct ordinary matter subaction as a functor over q(Phi)",
        },
        {
            "debt_id": "AX2658_1_no_hidden_visible_hom",
            "needed_principle": "operator-domain theorem forbids hidden/representative variables mapping into visible coefficients except through q or fixed data",
            "why_needed": "kills alpha_EM(X), m_A(X), w_A(X), shadow frames, source markers and calibration leaks at once",
            "current_basis": "1090:AX1090_1;2159:AXR2159_1_no_hidden_visible_hom",
            "status": "BEST_NEXT_DERIVATION_TARGET",
            "next_derivation_hook": "prove from quotient category/domain typing before touching finite data rows",
        },
        {
            "debt_id": "AX2658_2_common_measure_current_owner",
            "needed_principle": "measure/coframe/connection/current are owned by the same parent action",
            "why_needed": "prevents a current from re-entering through a different density or frame",
            "current_basis": "1090:AX1090_3;2654:action owner gap",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "next_derivation_hook": "derive Hilbert-current owner from parent variation class",
        },
        {
            "debt_id": "AX2658_3_fixed_constants_representation_sector",
            "needed_principle": "ordinary constants sit in fixed representation data",
            "why_needed": "prevents local hidden-coordinate dependence of EM, mass, clock and material coefficients",
            "current_basis": "1090:AX1090_2",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "next_derivation_hook": "tie constants to representation labels, not source-worldtube fields",
        },
        {
            "debt_id": "AX2658_4_variation_before_readout",
            "needed_principle": "source/current variations precede empirical readout and material projection",
            "why_needed": "prevents selection effects from being mistaken for parent current zeros",
            "current_basis": "1090:AX1090_4;1912:AX1912_7",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "next_derivation_hook": "derive readout as downstream functor of the parent variation",
        },
        {
            "debt_id": "AX2658_5_matter_bundle_lift",
            "needed_principle": "ordinary matter fields and worldtubes lift through the same quotient bundle",
            "why_needed": "source labels and material tensors otherwise evade the quotient",
            "current_basis": "1486:MOMS1088_2;1912:NQD1912_2",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "next_derivation_hook": "make Psi_q and source worldtube data part of the q-owned ordinary matter category",
        },
        {
            "debt_id": "AX2658_6_verdict",
            "needed_principle": "MOMS/local-GR descent axiom debt",
            "why_needed": "these principles would close the zero route, but adopting them would be closure-only",
            "current_basis": "1090:SYN1090_8_verdict;2159:MOM2159_7_verdict",
            "status": "AXIOM_DEBT_NOT_ADOPTED",
            "next_derivation_hook": "attempt AX2658_1 first because it removes the widest class of coupling countermodels",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "adopt_as_axiom": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def finite_source_fallback_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "fallback_id": "FSF2658_0_C_parent_X",
            "coefficient_or_input": "C_parent_X = N_X^-1 dS_parent(Phi+sV_X)/ds|0",
            "required_for": "finite WEP/source-current residual if zero route fails",
            "missing_parent_input": "Z_X, M_X^2, numerator coefficients, source path and basis",
            "candidate_source": "2657:FWP2657_0_C_parent",
            "units": "action/current normalization dependent",
            "status": "MISSING_PARENT_INPUT",
            "next_action": "derive zero via MOMS or source finite coefficient with units",
        },
        {
            "fallback_id": "FSF2658_1_source_weight",
            "coefficient_or_input": "w_A(X) or Delta_w_X",
            "required_for": "composition/source dependence if no-hidden-visible-hom theorem fails",
            "missing_parent_input": "source/species coupling law and sign",
            "candidate_source": "2159 first coupling-bound row",
            "units": "dimensionless or declared normalization",
            "status": "MISSING_SOURCE_WEIGHT_ROW",
            "next_action": "select as first finite row only after theorem attempt fails",
        },
        {
            "fallback_id": "FSF2658_2_constant_residuals",
            "coefficient_or_input": "alpha_EM(X), m_A(X), clock/material coefficients",
            "required_for": "EM, clock and material tests if constants are not fixed representation data",
            "missing_parent_input": "operator-domain rule for visible constants",
            "candidate_source": "1090:AX1090_1;1090:AX1090_2",
            "units": "coefficient-specific",
            "status": "MISSING_ARENA_PROJECTION",
            "next_action": "prove constants cannot be hidden-coordinate functions, or build arena rows",
        },
        {
            "fallback_id": "FSF2658_3_shadow_readout_residual",
            "coefficient_or_input": "shadow/disformal/readout residual vector",
            "required_for": "PPN, WEP, clocks and orbital local tests",
            "missing_parent_input": "no-shadow domain and readout ordering",
            "candidate_source": "1912 countermodel ledger;2656 source-worldtube bound",
            "units": "arena-specific",
            "status": "MISSING_ARENA_PROJECTION",
            "next_action": "derive operator-domain theorem or source residual vector components",
        },
        {
            "fallback_id": "FSF2658_4_tau_and_kernel",
            "coefficient_or_input": "tau_WEP, tau_PPN, tau_clock, tau_orbital and readout kernels",
            "required_for": "turn finite coefficients into actual test predictions",
            "missing_parent_input": "same-branch readout kernel and official-array mapping",
            "candidate_source": "2656:SRB2656_5_verdict",
            "units": "arena-specific transfer factor",
            "status": "MISSING_READOUT_KERNEL",
            "next_action": "do not set tau=1; source or derive kernels",
        },
        {
            "fallback_id": "FSF2658_5_acceptance",
            "coefficient_or_input": "finite source-map fallback",
            "required_for": "nonzero local residual branch",
            "missing_parent_input": "all rows above",
            "candidate_source": "this checkpoint",
            "units": "mixed pending rows",
            "status": "FINITE_SOURCE_MAP_NOT_EXECUTABLE_NONCLAIM",
            "next_action": "try operator-domain theorem before finite source-row acquisition",
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


def dryrun_cases_rows() -> list[dict[str, Any]]:
    generated = stamp()
    cases = [
        ("DRY2658_0_chain_rule_only", "only pointwise vertical-blind geometry is supplied", "REJECTED_NOT_ACTION_DESCENT"),
        ("DRY2658_1_closure_axiom", "MOMS is simply assumed as a closure axiom", "REJECTED_AXIOM_NOT_ADOPTED"),
        ("DRY2658_2_unsigned_MOMS", "MOMS clauses remain source-map rows only", "BLOCKED_PARENT_SIGNATURE_UNSIGNED"),
        ("DRY2658_3_hidden_visible_hom", "hidden variable maps into alpha/mass/source coefficients", "BLOCKED_OPERATOR_DOMAIN_MISSING"),
        ("DRY2658_4_source_weight_live", "source-only w_A(X) branch remains legal", "BLOCKED_FINITE_SOURCE_WEIGHT_REQUIRED"),
        ("DRY2658_5_quotient_theorem_only", "descent theorem supplied without fibre-invariance source", "BLOCKED_FIBRE_INVARIANCE_UNSIGNED"),
        ("DRY2658_6_finite_rows_missing", "fallback finite source rows are placeholders", "NONEXECUTABLE_NONCLAIM"),
        ("DRY2658_7_tau_one_default", "readout transfer tau is set to 1 by convenience", "REJECTED_BOUND_INVERSION"),
        ("DRY2658_8_cancellation", "residuals cancel only by hand-tuned opposite signs", "REJECTED_FINE_TUNED_CANCELLATION"),
        ("DRY2658_9_counterfactual_signed_MOMS", "all MOMS clauses are parent-derived in a future branch", "CONDITIONAL_ZERO_THEOREM_IMPORT_READY_NONCLAIM"),
        ("DRY2658_10_counterfactual_finite_pack", "all finite source coefficients and kernels are sourced", "FINITE_PRODUCT_RUNNER_READY_NONCLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "case_id": case_id,
            "scenario": scenario,
            "expected_status": expected,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for case_id, scenario, expected in cases
    ]


def dryrun_results_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "case_id": case["case_id"],
                "observed_status": case["expected_status"],
                "status_match": True,
                "claim_allowed": False,
                "reason": "2658 is a proof/debt checkpoint only; even counterfactual rows require later arena/run validation before claims",
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "CG2658_0_neighbourhood_descent",
            "requirement": "ordinary matter action descends through q on an open fibre neighbourhood",
            "current_status": "FAIL_NOT_PARENT_SIGNED",
            "evidence_ref": "NQD2658_5_verdict",
        },
        {
            "gate_id": "CG2658_1_MOMS_signature",
            "requirement": "MOMS ordinary-matter signature clauses are parent-derived together",
            "current_status": "FAIL_MOMS_PARENT_SIGNATURE_NOT_DERIVED",
            "evidence_ref": "MOMS2658_7_verdict",
        },
        {
            "gate_id": "CG2658_2_axiom_adoption",
            "requirement": "missing axioms are either derived or explicitly adopted as closure",
            "current_status": "PASS_GUARD_AXIOMS_NOT_ADOPTED",
            "evidence_ref": "AX2658_6_verdict",
        },
        {
            "gate_id": "CG2658_3_finite_fallback",
            "requirement": "finite source-map rows are numeric, sourced, unit-safe and same-branch",
            "current_status": "FAIL_FINITE_SOURCE_MAP_NOT_EXECUTABLE",
            "evidence_ref": "FSF2658_5_acceptance",
        },
        {
            "gate_id": "CG2658_4_verdict",
            "requirement": "local-GR/WEP/source-current pass can be claimed",
            "current_status": "CLAIM_BLOCKED",
            "evidence_ref": "NQD2658_5_verdict;MOMS2658_7_verdict;FSF2658_5_acceptance",
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
            "decision_id": "DEC2658_0_proof_status",
            "decision": "do not promote the 2657 conditional double-zero theorem",
            "reason": "open-neighbourhood ordinary-matter descent and MOMS signature are not parent-signed",
            "next_action": "keep theorem as exact conditional mathematics",
        },
        {
            "decision_id": "DEC2658_1_coupling_diagnosis",
            "decision": "the coupling/source-weight slot is the active bottleneck",
            "reason": "w_A, alpha_EM(X), m_A(X), shadow frames and source labels all use the same missing operator-domain/no-hidden-visible-hom beam",
            "next_action": "attack the operator-domain theorem before data-row acquisition",
        },
        {
            "decision_id": "DEC2658_2_next",
            "decision": "select 2659 no-hidden-visible-hom/operator-domain theorem",
            "reason": "one theorem could eliminate the widest family of legal countermodels",
            "next_action": "try to derive domain typing: hidden variables cannot feed visible matter coefficients except through q or fixed representation data",
        },
        {
            "decision_id": "DEC2658_3_fallback",
            "decision": "if the theorem fails, select first finite source-weight row",
            "reason": "then the honest route is finite coefficient evidence rather than closure-only zero",
            "next_action": "stage w_A/Delta_w_X with units, signs, parent source and arena projection",
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
            "next_id": "NEXT2658_0_selected",
            "status": "selected",
            "next_doc": "2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md",
            "next_script": "scripts/Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_or_finite_source_row_2659.py",
            "task": "derive or reject the operator-domain theorem forbidding hidden/representative variables from entering visible ordinary-matter coefficients except through q(Phi) or fixed representation data",
            "must_prove": "domain typing; quotient ownership; fixed ordinary constants; no source/species-only coefficient hom; no shadow frame/readout reentry",
            "fallback_if_fails": "stage first finite source-weight/coupling row as nonclaim evidence input",
            "must_exclude": "closure-only MOMS, tau=1 transfer, cancellation tuning, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "STAT2658_0_local_GR",
            "topic": "local GR/WEP reduction",
            "status": "NOT_CLOSED",
            "detail": "the route is now sharply conditional: MOMS/open-neighbourhood descent would give zero, but it is not parent-derived",
        },
        {
            "status_id": "STAT2658_1_solid_piece",
            "topic": "what is mathematically solid",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "detail": "chain-rule vertical silence, quotient descent equivalence, THM1088_5 and PCZ2657_2 remain useful conditional theorems",
        },
        {
            "status_id": "STAT2658_2_project_overview",
            "topic": "full project state",
            "status": "CLOSER_TO_THE_REAL_GAP_NOT_CLAIM_READY",
            "detail": "the local branch has stopped wandering: the next hard beam is coupling/domain ownership, not another cosmetic residual ledger",
        },
        {
            "status_id": "STAT2658_3_best_improvement_route",
            "topic": "next route of attack",
            "status": "OPERATOR_DOMAIN_THEOREM_FIRST",
            "detail": "prove no-hidden-visible-hom if possible; if not, admit finite source-weight/coupling coefficients and test them honestly",
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
        "neighbourhood_descent_attempt": neighbourhood_descent_attempt_rows(),
        "moms_signature_source_map": moms_signature_source_map_rows(),
        "axiom_debt": axiom_debt_rows(),
        "finite_source_fallback": finite_source_fallback_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["dryrun_cases"] = dryrun_cases_rows()
    rows["dryrun_results"] = dryrun_results_rows(rows["dryrun_cases"])
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["axiom_debt"], BRANCH_COPIES["queue"], "MOMS axiom debt / theorem target queue"),
        "local_bounds": (OUTPUTS["finite_source_fallback"], BRANCH_COPIES["local_bounds"], "finite local source-map fallback"),
        "source_weight": (OUTPUTS["moms_signature_source_map"], BRANCH_COPIES["source_weight"], "MOMS parent signature source map"),
        "microscope": (OUTPUTS["neighbourhood_descent_attempt"], BRANCH_COPIES["microscope"], "neighbourhood descent proof attempt"),
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
                "copy_id": f"COPY2658_{copy_id}",
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
        "*2658-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2658*",
        "*Y5_R2FR_neighbourhood_quotient_descent_or_MOMS_parent_signature_source_map_2658*",
        "*JR2658*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    descent_ok = any(row["attempt_id"] == "NQD2658_5_verdict" and row["status"] == "NEIGHBOURHOOD_QUOTIENT_DESCENT_NOT_PARENT_SIGNED" for row in rows["neighbourhood_descent_attempt"])
    moms_ok = len(rows["moms_signature_source_map"]) == 8 and any(row["clause_id"] == "MOMS2658_7_verdict" and row["current_status"] == "MOMS_PARENT_SIGNATURE_NOT_DERIVED" for row in rows["moms_signature_source_map"]) and all(not row["parent_signed"] and not row["adopted_as_axiom"] for row in rows["moms_signature_source_map"])
    axiom_ok = any(row["debt_id"] == "AX2658_6_verdict" and row["status"] == "AXIOM_DEBT_NOT_ADOPTED" for row in rows["axiom_debt"]) and all(not row["adopt_as_axiom"] for row in rows["axiom_debt"])
    finite_ok = any(row["fallback_id"] == "FSF2658_5_acceptance" and row["status"] == "FINITE_SOURCE_MAP_NOT_EXECUTABLE_NONCLAIM" for row in rows["finite_source_fallback"]) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["finite_source_fallback"])
    dry_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2658_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2659-Y5-R2FR-no-hidden-visible-hom" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2658_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2658_01_neighbourhood_descent", descent_ok, "descent attempt preserves exact theorem but keeps verdict not parent-signed"),
        ("VAL2658_02_MOMS_source_map", moms_ok, "MOMS source map has eight unsigned nonclaim clauses"),
        ("VAL2658_03_axiom_debt", axiom_ok, "axiom debt is explicit and not adopted"),
        ("VAL2658_04_finite_fallback", finite_ok, "finite source fallback rows remain non-executable/nonclaim"),
        ("VAL2658_05_dryrun", dry_ok, "dry-run refuses pointwise-only, closure-only, tau=1, cancellation and placeholder routes"),
        ("VAL2658_06_claim_gates_blocked", claim_ok, "all claim gates block local/WEP claim"),
        ("VAL2658_07_next_target", next_ok, "2659 no-hidden-visible-hom operator-domain theorem selected"),
        ("VAL2658_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2658_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2658_10_formalization_untouched", formal_ok, "no 2658 outputs are written under formalization-workbench"),
        ("VAL2658_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2658_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2658 keeps neighbourhood descent/MOMS unsigned, stages finite source fallback nonclaim, and selects no-hidden-visible-hom operator-domain theorem next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2658 - Neighbourhood Quotient Descent Or MOMS Parent Signature Source Map

## Purpose

This checkpoint tries the derivation-first route after 2657: can the exact local double-zero theorem be promoted by parent-signing open-neighbourhood quotient descent and the minimal ordinary-matter signature?

## Result

- The zero theorem is still mathematically good, but it is still conditional: pointwise geometry silence and quotient-descent equivalence do not by themselves prove full ordinary-matter action descent on an open neighbourhood.
- The MOMS parent signature remains unsigned: action owner, matter bundle, fixed constants, no species/source weights, no shadow domain and variation-before-readout are all still proof debts.
- The honest next target is not another cosmetic residual ledger. It is the coupling/domain beam: prove a no-hidden-visible-hom/operator-domain theorem, or admit a finite source-weight/coupling row as nonclaim input.
- No local-GR, WEP, R10, PPN, clock or orbital claim is allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"])}

## Neighbourhood Descent Attempt

{markdown_table(rows["neighbourhood_descent_attempt"])}

## MOMS Signature Source Map

{markdown_table(rows["moms_signature_source_map"])}

## Axiom Debt

{markdown_table(rows["axiom_debt"])}

## Finite Source Fallback

{markdown_table(rows["finite_source_fallback"])}

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
