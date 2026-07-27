from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NO_HIDDEN_VISIBLE_HOM_OR_FINITE_COUPLING_PRIOR_2317"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md"

PATHS = {
    "2316_doc": ROOT / "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
    "2316_validation": OUT / "P8_Y5_BRR545_2316_VALIDATION.csv",
    "2316_source_pack": OUT / "P8_Y5_PARENT_QLOC_2316_FINITE_JQ_SOURCE_PACK.csv",
    "1090_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1091_theorem": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "1091_obstructions": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_OBSTRUCTION_LEDGER.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1058_visible_domain": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
    "1049_classification": OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
    "1049_priors": OUT / "P8_Y5_R10_1049_RESIDUAL_PRIOR_SLOTS.csv",
    "1451_grammar_doc": ROOT / "1451-Y5-R10-RAB-no-source-only-slot-operator-grammar-theorem-or-epsilon-bound-inputs.md",
    "1467_visible_algebra": OUT / "P8_Y5_R10_1467_VISIBLE_COEFFICIENT_ALGEBRA_THEOREM_ATTEMPT.csv",
    "1467_no_hidden_f2": OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv",
    "1468_visible_triviality": OUT / "P8_Y5_R10_1468_PARENT_VISIBLE_COEFFICIENT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
    "1468_hidden_audit": OUT / "P8_Y5_R10_1468_HIDDEN_INVARIANT_ALGEBRA_AUDIT.csv",
    "1469_hidden_theorem": OUT / "P8_Y5_R10_1469_HIDDEN_INVARIANT_ALGEBRA_THEOREM_ATTEMPT.csv",
    "1473_residual_vector": OUT / "P8_Y5_R10_1473_EXECUTABLE_LOCAL_RESIDUAL_VECTOR.csv",
    "1473_double_zero": OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv",
    "1490_source_target": OUT / "P8_Y5_R10_1490_SOURCE_COEFFICIENT_TARGET_EXCLUSION_ATTEMPT.csv",
    "1490_hidden_triviality": OUT / "P8_Y5_R10_1490_HIDDEN_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
    "1490_delta_w": OUT / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv",
}

SOURCES = [
    ("SRC2317_00_2316_doc", "2316_doc", PATHS["2316_doc"], ["NEXT2316_0", "no-hidden-visible-hom/operator-domain"], "2316 handoff: no-hidden-visible-Hom is the next coupling target"),
    ("SRC2317_01_2316_validation", "2316_validation", PATHS["2316_validation"], ["VAL2316_OVERALL", "PASS"], "2316 validation"),
    ("SRC2317_02_2316_source_pack", "2316_source_pack", PATHS["2316_source_pack"], ["JQPACK2316_4_shadow", "MISSING_NO_SHADOW_THEOREM_OR_VALUE"], "finite j_q source pack with hidden/shadow coupling leg"),
    ("SRC2317_03_1090_axioms", "1090_axioms", PATHS["1090_axioms"], ["AX1090_1_no_hidden_visible_hom", "MISSING_AXIOM_NOT_ADOPTED"], "missing no-hidden-visible-Hom axiom"),
    ("SRC2317_04_1091_theorem", "1091_theorem", PATHS["1091_theorem"], ["ODH1091_6_verdict", "THEOREM_NOT_DERIVED_CURRENT_CORPUS"], "operator-domain theorem attempt"),
    ("SRC2317_05_1091_obstructions", "1091_obstructions", PATHS["1091_obstructions"], ["OBS1091_0_invariant_scalar", "nonconstant hidden invariant scalar"], "operator-domain obstruction ledger"),
    ("SRC2317_06_1066_operator_domain", "1066_operator_domain", PATHS["1066_operator_domain"], ["ODR1066_4_verdict", "EXACT_RULE_NOT_DERIVED"], "source-scalar/operator-domain rule audit"),
    ("SRC2317_07_1058_visible_domain", "1058_visible_domain", PATHS["1058_visible_domain"], ["VOE1058_5_verdict", "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR"], "visible operator domain exhaustion failed"),
    ("SRC2317_08_1049_classification", "1049_classification", PATHS["1049_classification"], ["OCR1049_5_verdict", "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED"], "operator classification failed as claim"),
    ("SRC2317_09_1049_priors", "1049_priors", PATHS["1049_priors"], ["RP1049_0_b_alpha", "MISSING_PRIOR_WIDTH"], "retained alpha/mass/clock prior slots"),
    ("SRC2317_10_1451_grammar_doc", "1451_grammar_doc", PATHS["1451_grammar_doc"], ["OG1451_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"], "no-source-only-slot grammar attempt"),
    ("SRC2317_11_1467_visible_algebra", "1467_visible_algebra", PATHS["1467_visible_algebra"], ["VCA1467_4_verdict", "EXACT_EQUIVALENCE_NOT_PARENT_SIGNED"], "visible coefficient algebra theorem attempt"),
    ("SRC2317_12_1467_no_hidden_f2", "1467_no_hidden_f2", PATHS["1467_no_hidden_f2"], ["NHF1467_1_forbidden_if_algebra_signed", "false_generically"], "no-hidden-F2 operator classification"),
    ("SRC2317_13_1468_visible_triviality", "1468_visible_triviality", PATHS["1468_visible_triviality"], ["VAT1468_4_verdict", "NOT_PARENT_DERIVED_KEEP_RETAINED_ALPHA_BOUND_ROWS"], "parent visible coefficient algebra attempt"),
    ("SRC2317_14_1468_hidden_audit", "1468_hidden_audit", PATHS["1468_hidden_audit"], ["HIA1468_2_covariance_not_enough", "REJECTED_SHORTCUT"], "hidden invariant audit rejects covariance shortcut"),
    ("SRC2317_15_1469_hidden_theorem", "1469_hidden_theorem", PATHS["1469_hidden_theorem"], ["HIT1469_4_verdict", "NOT_PARENT_DERIVED_PRODUCT_RUNNER_REQUIRED"], "hidden invariant algebra theorem attempt"),
    ("SRC2317_16_1473_residual_vector", "1473_residual_vector", PATHS["1473_residual_vector"], ["ERV1473_0_alpha_EM_slope", "FILL_NUMERIC_OR_THEOREM_ZERO"], "executable residual vector"),
    ("SRC2317_17_1473_double_zero", "1473_double_zero", PATHS["1473_double_zero"], ["DZ1473_4_verdict", "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR"], "double-zero theorem attempt"),
    ("SRC2317_18_1490_source_target", "1490_source_target", PATHS["1490_source_target"], ["SCT1490_5_verdict", "NOT_DERIVED_BOUND_INPUT_ROUTE_SELECTED"], "source coefficient target exclusion failed"),
    ("SRC2317_19_1490_hidden_triviality", "1490_hidden_triviality", PATHS["1490_hidden_triviality"], ["HIA1490_6_verdict", "NOT_TRIVIALITY_PROVED"], "hidden invariant algebra triviality not proved"),
    ("SRC2317_20_1490_delta_w", "1490_delta_w", PATHS["1490_delta_w"], ["DWR1490_6_claim_gate", "MISSING_SOURCE_BACKED_VALUE"], "real delta_w input requirements"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2317_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2317_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT.csv",
    "clauses": OUT / "P8_Y5_PARENT_QLOC_2317_OPERATOR_DOMAIN_CLAUSE_LEDGER.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2317_HIDDEN_COUPLING_COUNTERMODEL_TO_JQ_MAP.csv",
    "priors": OUT / "P8_Y5_PARENT_QLOC_2317_FINITE_COUPLING_PRIOR_INTERFACE.csv",
    "arena": OUT / "P8_Y5_PARENT_QLOC_2317_LOCAL_GR_ARENA_IMPACT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2317_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2317_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2317_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2317_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2317_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2317_0_theorem", OUTPUTS["theorem"], RAB_QUEUE / "JR2317_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT_NONCLAIM.csv"),
    ("COPY2317_1_priors", OUTPUTS["priors"], RAB_QUEUE / "JR2317_FINITE_COUPLING_PRIOR_INTERFACE_NONCLAIM.csv"),
    ("COPY2317_2_arena_beta", OUTPUTS["arena"], BETA_DOCS / "NO_HIDDEN_VISIBLE_HOM_LOCAL_ARENA_IMPACT_2317_NONCLAIM.csv"),
    ("COPY2317_3_arena_wep", OUTPUTS["arena"], MICRO_RESIDUALS / "no_hidden_visible_hom_local_arena_impact_nonclaim_2317.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return False, "missing_needles=" + ";".join(missing_needles)
    return True, "all_needles_found"


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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        needles_found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(needles_found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_0_target",
            "claim_piece": "no hidden-visible coefficient homomorphism",
            "formal_statement": "For visible operators O_vis in EM, mass, clock, source, frame, and readout sectors, Hom(C_hid,Coeff(O_vis)) is absent or constant after quotient/constant projection.",
            "proof_status": "TARGET_SHARP",
            "exact_gain": "would kill j_const, j_shadow, j_hom, and part of j_weight/readout in the 2316 source pack",
            "current_gap": "target is a grammar theorem, not a consequence of covariance",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_1_descent_lemma",
            "claim_piece": "descended coefficients are vertically silent",
            "formal_statement": "If c_i = p^* cbar_i with p=(q_loc,pi_const) and v in ker(Dp), then L_v c_i=0, so the corresponding first-order hidden coupling source vanishes.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "exact_gain": "mathematics of the zero is clean once every coefficient is proved to descend",
            "current_gap": "the inclusion Coeff(O_vis) subset Image(p^*) is unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_2_obstruction_necessity",
            "claim_piece": "hidden coefficient map is exactly the obstruction",
            "formal_statement": "If c_i=c0+epsilon f(I_hid) and dI_hid is nonzero on an allowed hidden direction, then L_v c_i=epsilon f'(I_hid)L_v I_hid generically sources j_q.",
            "proof_status": "COUNTEREXAMPLE_PROVED_IF_I_SURVIVES",
            "exact_gain": "shows why local-GR cannot be won by rhetoric; the coupling has to be killed or bounded",
            "current_gap": "hidden invariant algebra triviality is not proved",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_3_target_exclusion_route",
            "claim_piece": "forbid source-only and visible coefficient targets by parent coefficient functor",
            "formal_statement": "R_+^source, f_X F_Q^2, m_A(X), clock_X, A_shadow(X), and readout_X are not target objects of the visible coefficient functor except fixed representation data.",
            "proof_status": "POWERFUL_CONDITIONAL_ROUTE",
            "exact_gain": "would close the central fork without listing every hidden scalar",
            "current_gap": "1490 says source-only target exclusion is not derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_4_radiative_readout_guard",
            "claim_piece": "tree-level sequester must survive effective action and readout",
            "formal_statement": "If S_bare has no hidden-visible Hom but S_eff or detector/readout maps regenerate coefficient dependence, the local source leg is finite rather than theorem-zero.",
            "proof_status": "REQUIRED_GUARD_UNSIGNED",
            "exact_gain": "prevents a fake zero produced only before reduction/calibration",
            "current_gap": "radiative/readout closure remains unsigned in 1058/1091/1468/1490",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHVH2317_5_verdict",
            "claim_piece": "current corpus derives no-hidden-visible-Hom",
            "formal_statement": "NHVH2317_1 plus parent coefficient-functor target exclusion plus hidden invariant triviality plus radiative/readout closure would sign AX1090_1.",
            "proof_status": "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED",
            "exact_gain": "conditional route is exact and valuable",
            "current_gap": "operator-domain theorem, hidden invariant triviality, target exclusion, and readout closure all remain unsigned",
            "valid_for_claim": "false",
        },
    ]


def build_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_0_parent_object",
            "needed_clause": "one parent action/coefficient functor exists before readout and fitting",
            "best_source": "AX1090_0;1447;1090",
            "current_status": "PARENT_OBJECT_NOT_PROVEN",
            "failure_if_missing": "visible coefficient grammar can be changed after the fact",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_1_visible_coefficient_algebra",
            "needed_clause": "Coeff(O_vis) lives only in quotient-plus-fixed-constant algebra",
            "best_source": "VCA1467;VAT1468;ODH1091",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "failure_if_missing": "hidden EM/mass/clock/readout maps remain legal",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_2_hidden_invariant_triviality",
            "needed_clause": "hidden invariant algebra has no nonconstant source-relevant scalars",
            "best_source": "HIT1469;HIA1490",
            "current_status": "NOT_TRIVIALITY_PROVED",
            "failure_if_missing": "f(I_hid) visible coefficients survive",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_3_source_target_exclusion",
            "needed_clause": "R_+ source-only/action-scale target is not in the admissible visible coefficient target category",
            "best_source": "ODR1066;SCT1490",
            "current_status": "EXACT_RULE_NOT_DERIVED",
            "failure_if_missing": "w_A and kappa_A source multipliers feed j_weight/j_readout",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_4_radiative_readout_closure",
            "needed_clause": "effective action, thresholds, calibration, and detector/readout maps preserve the no-Hom grammar",
            "best_source": "VOE1058;ODH1091;NHF1467",
            "current_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "failure_if_missing": "tree-level silence can be undone by S_eff or readout maps",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_5_common_measure",
            "needed_clause": "common action/current normalization prevents source-weight Hom through action scale",
            "best_source": "SSE1066;AX1090_2;1451",
            "current_status": "COMMON_MEASURE_UNSIGNED",
            "failure_if_missing": "classical EOM can look common while Hilbert/source current is weighted",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ODC2317_6_verdict",
            "needed_clause": "all operator-domain clauses signed together",
            "best_source": "2317 synthesis",
            "current_status": "FAIL_REDUCTION_KEEP_FINITE_PRIORS",
            "failure_if_missing": "j_q hidden-visible coupling terms remain theorem targets or source-backed priors",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCJ2317_0_alpha_F2",
            "live_countermodel": "Z_EM = Z0 + epsilon f(I_hid)",
            "j_q_channel": "j_const/j_hom via b_alpha = L_v ln Z_EM",
            "arena_pressure": "EM, clocks, WEP, R10, PPN alpha branch",
            "why_live": "gauge and diffeo covariance allow scalar EM kinetic coefficients unless coefficient algebra is signed",
            "needed_to_kill": "visible coefficient algebra plus radiative/readout closure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCJ2317_1_mass_clock",
            "live_countermodel": "m_A, mu, nuclear binding, or clock coefficients depend on I_hid",
            "j_q_channel": "j_const via b_mu, b_mA, b_nuc, b_clock_i",
            "arena_pressure": "WEP, clocks, orbital source calibration",
            "why_live": "ordinary matter spectrum/constants are not parent-owned as fixed representation data",
            "needed_to_kill": "fixed constant sector plus no-hidden-visible-Hom",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCJ2317_2_shadow_frame",
            "live_countermodel": "A_A(I_hid)^2 g_obs or disformal B_A(I_hid)",
            "j_q_channel": "j_shadow through matter-frame derivative",
            "arena_pressure": "PPN gamma, WEP, clocks, local force",
            "why_live": "no-shadow/domain clause is unsigned",
            "needed_to_kill": "operator-domain target exclusion for source-only frames",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCJ2317_3_source_weight",
            "live_countermodel": "w_A(I_hid) S_A or kappa_A(I_hid) T_A",
            "j_q_channel": "j_weight/j_readout through active source prefactor",
            "arena_pressure": "Newton source normalization, WEP, R10",
            "why_live": "source-only R_+ target exclusion and common measure are not parent-derived",
            "needed_to_kill": "no-source-only-slot grammar plus common measure/current owner",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HCJ2317_4_readout_regeneration",
            "live_countermodel": "calibration, threshold, detector, or source-worldtube map depends on hidden/readout state",
            "j_q_channel": "j_readout/tau residual",
            "arena_pressure": "PPN, clocks, orbital, R10 transfer",
            "why_live": "variation-before-readout and radiative/readout closure are unsigned",
            "needed_to_kill": "parent readout functor closure",
            "valid_for_claim": "false",
        },
    ]


def build_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of EM/gauge kinetic or fine-structure coefficient",
            "units": "dimensionless vertical derivative",
            "zero_condition": "no-hidden-F2 plus alpha owner plus radiative/readout closure",
            "source_status": "MISSING_THEOREM_OR_NUMERIC_PRIOR",
            "observable_links": "clocks;WEP;R10;EM spectra;PPN alpha branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_1_b_mu",
            "symbol": "b_mu",
            "definition": "vertical derivative of mass-ratio/spectrum coefficient",
            "units": "dimensionless vertical derivative",
            "zero_condition": "fixed matter spectrum/constant sector",
            "source_status": "MISSING_THEOREM_OR_NUMERIC_PRIOR",
            "observable_links": "clocks;WEP;composition",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_2_b_mA_b_nuc",
            "symbol": "b_mA;b_nuc",
            "definition": "vertical derivative of material mass and nuclear/electromagnetic binding response",
            "units": "dimensionless material response",
            "zero_condition": "constant-sector/no-Hom theorem plus composition matrix ownership",
            "source_status": "MISSING_THEOREM_OR_NUMERIC_PRIOR",
            "observable_links": "WEP;R10;clock nuclear sensitivities;Newton GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_3_delta_w",
            "symbol": "delta_w_A",
            "definition": "relative active-source/action-scale weight after common mode removed",
            "units": "dimensionless source multiplier",
            "zero_condition": "source-only target exclusion plus common measure/current theorem",
            "source_status": "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT",
            "observable_links": "WEP;Newton source normalization;R10 source leg",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_4_shadow_frame",
            "symbol": "a_shadow;b_disformal",
            "definition": "hidden derivative of conformal/disformal/source-only matter frame",
            "units": "dimensionless frame derivative",
            "zero_condition": "no-shadow/domain plus no-hidden-visible-Hom target exclusion",
            "source_status": "MISSING_THEOREM_OR_NUMERIC_PRIOR",
            "observable_links": "PPN gamma;WEP;clock;local force",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_5_tau_readout",
            "symbol": "Delta_tau_readout",
            "definition": "arena-specific readout/calibration/source-worldtube transfer residual",
            "units": "arena-dependent declared tau units",
            "zero_condition": "variation-before-readout plus readout functor closure",
            "source_status": "MISSING_THEOREM_OR_REAL_SOURCE_BACKED_INPUT",
            "observable_links": "clocks;WEP;R10;PPN;orbital",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCP2317_6_claim_gate",
            "symbol": "finite_coupling_prior_claim_gate",
            "definition": "no finite coupling row can be used for scoring until theorem-zero or numeric source-backed priors exist with units and projection",
            "units": "guard",
            "zero_condition": "all components theorem-zero or source-backed",
            "source_status": "NONCLAIM_REQUIREMENTS_ONLY",
            "observable_links": "all local arenas",
            "valid_for_claim": "false",
        },
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2317_0_jq",
            "arena": "q_R numerator",
            "impact": "no-Hom would remove j_const, j_shadow, j_hom, and some source-weight/readout channels from j_q",
            "current_status": "CONDITIONAL_ONLY",
            "still_blocked_by": "hidden invariant triviality, target exclusion, radiative/readout closure, common measure",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2317_1_local_GR",
            "arena": "local GR/Newton reduction",
            "impact": "local residual vector is cleaner but still contains q_R priors, q_loc, beta, source normalization, and boundary/curvature channels",
            "current_status": "NOT_CLOSED",
            "still_blocked_by": "finite coupling priors are not theorem-zero or numeric/source-backed",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2317_2_R10",
            "arena": "R10 short-range",
            "impact": "hidden EM/source/matter-frame maps feed alpha(lambda) unless killed or bounded",
            "current_status": "BOUND_INPUT_ROUTE_ONLY",
            "still_blocked_by": "real alpha(lambda) bound curve plus finite coupling prediction/projection",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2317_3_clocks_WEP",
            "arena": "clocks/WEP/composition",
            "impact": "b_alpha, b_mu, b_mA, b_nuc, delta_w_A, and readout tau remain explicit nonclaim inputs",
            "current_status": "FINITE_PRIOR_INTERFACE",
            "still_blocked_by": "source-backed sensitivity matrices, material vectors, and parent zero theorems",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2317_4_orbital_source",
            "arena": "Newton/orbital source normalization",
            "impact": "source-only target exclusion failure keeps active source calibration residuals live",
            "current_status": "SOURCE_NORMALIZATION_OPEN",
            "still_blocked_by": "common measure/current theorem and observed GM/source-worldtube map",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_1_descent_lemma",
            "gate": "descended coefficients are vertically silent",
            "passed": "true",
            "claim_effect": "conditional theorem available",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_2_no_hidden_visible_hom",
            "gate": "no-hidden-visible-Hom parent theorem signed",
            "passed": "false",
            "claim_effect": "hidden coupling source legs remain live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_3_hidden_invariant_triviality",
            "gate": "hidden invariant algebra trivial or source target excluded",
            "passed": "false",
            "claim_effect": "finite coupling priors cannot be set to zero",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_4_finite_prior_ready",
            "gate": "finite coupling priors numeric/source-backed",
            "passed": "false",
            "claim_effect": "PPN/R10/WEP/clock/orbital scoring blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2317_5_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2317_0_claim_noHom",
            "claim": "no-hidden-visible-Hom is derived by 2317",
            "allowed": "false",
            "reason": "2317 proves only the conditional descent lemma; parent coefficient functor, hidden invariant triviality, target exclusion, and readout closure are unsigned",
            "blocking_rows": "NHVH2317_5_verdict;ODC2317_6_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2317_1_set_priors_zero",
            "claim": "finite coupling priors can be set to zero",
            "allowed": "false",
            "reason": "b_alpha, b_mu, delta_w, shadow-frame, and readout terms are theorem targets or missing numeric priors",
            "blocking_rows": "FCP2317_0_b_alpha;FCP2317_6_claim_gate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2317_2_local_GR",
            "claim": "MTS derives local GR/Newton after 2317",
            "allowed": "false",
            "reason": "hidden coupling branch remains open, and non-coupling local residual channels remain too",
            "blocking_rows": "ARENA2317_1_local_GR;CG2317_5_local_GR_Newton",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2317_3_score_tests",
            "claim": "R10/PPN/WEP/clock tests can be scored from 2317",
            "allowed": "false",
            "reason": "prior interface is symbolic and explicitly nonclaim until source-backed values/projections exist",
            "blocking_rows": "CG2317_4_finite_prior_ready",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2317_0",
            "next_target": "2318-Y5-R2FR-parent-coefficient-functor-construction-or-finite-coupling-prior-runner.md",
            "why": "2317 shows the exact theorem is available only if a parent coefficient functor/target category is derived; if that cannot be constructed, the honest route is a source-backed finite coupling prior runner",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_path, destination_path in BRANCH_COPY_SPECS:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source_path),
                "branch_copy_path": str(destination_path),
                "copy_exists": bool_text(destination_path.exists()),
                "row_count": len(read_csv_rows(destination_path)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, theorem_rows, clause_rows, countermodel_rows, prior_rows, arena_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2317-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2317",
        "P8_Y5_BRR545_2317",
        "JR2317_",
        "NO_HIDDEN_VISIBLE_HOM_LOCAL_ARENA_IMPACT_2317",
        "no_hidden_visible_hom_local_arena_impact_nonclaim_2317",
        "Y5_R2FR_no_hidden_visible_hom_jq_zero_or_finite_coefficient_prior_2317",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    theorem_ids = {row["row_id"] for row in theorem_rows}
    clause_ids = {row["row_id"] for row in clause_rows}
    prior_ids = {row["row_id"] for row in prior_rows}
    countermodel_ids = {row["row_id"] for row in countermodel_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2317_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2317_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2317_02_descent_lemma", any(row["row_id"] == "NHVH2317_1_descent_lemma" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "descent lemma recorded as exact conditional theorem"))
    checks.append(("VAL2317_03_noHom_not_promoted", any(row["row_id"] == "NHVH2317_5_verdict" and row["proof_status"] == "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED" for row in theorem_rows), "no-hidden-visible-Hom promotion refused"))
    checks.append(("VAL2317_04_clause_ledger_complete", {"ODC2317_1_visible_coefficient_algebra", "ODC2317_2_hidden_invariant_triviality", "ODC2317_3_source_target_exclusion", "ODC2317_4_radiative_readout_closure", "ODC2317_5_common_measure"}.issubset(clause_ids), "operator-domain clause ledger includes major blockers"))
    checks.append(("VAL2317_05_countermodels_mapped", {"HCJ2317_0_alpha_F2", "HCJ2317_1_mass_clock", "HCJ2317_2_shadow_frame", "HCJ2317_3_source_weight", "HCJ2317_4_readout_regeneration"}.issubset(countermodel_ids), "hidden coupling countermodels mapped to j_q channels"))
    checks.append(("VAL2317_06_prior_interface_complete", {"FCP2317_0_b_alpha", "FCP2317_1_b_mu", "FCP2317_2_b_mA_b_nuc", "FCP2317_3_delta_w", "FCP2317_4_shadow_frame", "FCP2317_5_tau_readout", "FCP2317_6_claim_gate"}.issubset(prior_ids), "finite coupling prior interface is explicit"))
    checks.append(("VAL2317_07_arena_blocks_preserved", all(row["score_ready"] == "false" for row in arena_rows), "all arena rows remain blocked/nonclaim"))
    checks.append(("VAL2317_08_claim_gates_block", any(row["row_id"] == "CG2317_5_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2317_09_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2317_10_next_target", any(row["row_id"] == "NEXT2317_0" and "parent-coefficient-functor" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2317_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2317_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2317_13_formalization_untouched_by_2317", len(formalization_hits) == 0, "no 2317 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2317_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2317 proves the exact conditional descent lemma for hidden-visible coefficient silence, refuses to promote no-hidden-visible-Hom because the parent coefficient functor, hidden invariant triviality, source target exclusion, common measure, and radiative/readout closure remain unsigned, maps the surviving countermodels into j_q channels, writes a finite coupling prior interface, keeps all local/PPN/R10/WEP/clock/orbital scores blocked, and selects parent coefficient functor construction or a finite coupling prior runner as the next target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2317 - No Hidden-Visible Hom j_q Zero Or Finite Coefficient Prior",
        "",
        "## Summary",
        "",
        "2317 goes at the coupling throat. The good news is that the exact mathematical lemma is solid: if every visible coefficient descends through quotient-plus-fixed-constant data, then hidden vertical motion cannot change that coefficient, and the corresponding first-order `j_q` source leg vanishes.",
        "",
        "The bad news is also clean: the current corpus does not derive the parent no-hidden-visible-Hom theorem. Hidden invariant scalar maps, source-only `R_+` targets, common-measure/action-scale gaps, and radiative/readout regeneration remain live. So this checkpoint does not claim local GR, PPN, WEP, R10, or clock success.",
        "",
        "The payoff is discipline. The coupling problem is now expressed as a finite prior/theorem-zero interface: `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `delta_w_A`, shadow-frame derivatives, and readout `Delta_tau` must each be either theorem-zero from a parent coefficient functor or numeric/source-backed before any local scoring.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## No Hidden-Visible Hom Theorem Attempt",
        "",
        markdown_table(theorem_rows, ["row_id", "claim_piece", "formal_statement", "proof_status", "exact_gain", "current_gap", "valid_for_claim"]),
        "",
        "## Operator-Domain Clause Ledger",
        "",
        markdown_table(clause_rows, ["row_id", "needed_clause", "best_source", "current_status", "failure_if_missing", "parent_signed", "valid_for_claim"]),
        "",
        "## Hidden Coupling Countermodel To j_q Map",
        "",
        markdown_table(countermodel_rows, ["row_id", "live_countermodel", "j_q_channel", "arena_pressure", "why_live", "needed_to_kill", "valid_for_claim"]),
        "",
        "## Finite Coupling Prior Interface",
        "",
        markdown_table(prior_rows, ["row_id", "symbol", "definition", "units", "zero_condition", "source_status", "observable_links", "valid_for_claim"]),
        "",
        "## Local GR Arena Impact",
        "",
        markdown_table(arena_rows, ["row_id", "arena", "impact", "current_status", "still_blocked_by", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    theorem_rows = build_theorem_rows()
    clause_rows = build_clause_rows()
    countermodel_rows = build_countermodel_rows()
    prior_rows = build_prior_rows()
    arena_rows = build_arena_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem_rows)
    write_csv(OUTPUTS["clauses"], clause_rows)
    write_csv(OUTPUTS["countermodels"], countermodel_rows)
    write_csv(OUTPUTS["priors"], prior_rows)
    write_csv(OUTPUTS["arena"], arena_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        theorem_rows,
        clause_rows,
        countermodel_rows,
        prior_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        theorem_rows,
        clause_rows,
        countermodel_rows,
        prior_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2317_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
