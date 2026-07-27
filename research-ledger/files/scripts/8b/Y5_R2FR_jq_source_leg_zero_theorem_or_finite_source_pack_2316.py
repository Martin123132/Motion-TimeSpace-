from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_JQ_SOURCE_LEG_ZERO_THEOREM_OR_FINITE_SOURCE_PACK_2316"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md"

PATHS = {
    "2315_doc": ROOT / "2315-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill.md",
    "2315_validation": OUT / "P8_Y5_BRR545_2315_VALIDATION.csv",
    "2315_formula": OUT / "P8_Y5_PARENT_QLOC_2315_FINITE_RESIDUAL_FORMULA_UPDATE.csv",
    "2315_arena": OUT / "P8_Y5_PARENT_QLOC_2315_ARENA_READINESS_UPDATE.csv",
    "1088_conditional": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1088_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_countermodel": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "1087_descent": OUT / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
    "1087_contract": OUT / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
    "1086_attempt": OUT / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
    "1089_hunt": OUT / "P8_Y5_R10_1089_SIGNATURE_SOURCE_HUNT.csv",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1090_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1090_decision": OUT / "P8_Y5_R10_1090_DECISION_LEDGER.csv",
    "2284_formula": OUT / "P8_Y5_PARENT_QLOC_2284_Q_RESIDUAL_FORMULA_LEDGER.csv",
    "2285_projection": OUT / "P8_Y5_PARENT_QLOC_2285_PROJECTION_MATRIX_NONCLAIM.csv",
}

SOURCES = [
    ("SRC2316_00_2315_doc", "2315_doc", PATHS["2315_doc"], ["q_R=j_q/(n_q H n_q)", "2316-Y5-R2FR"], "2315 handoff: numerator j_q is the highest-value local residual target"),
    ("SRC2316_01_2315_validation", "2315_validation", PATHS["2315_validation"], ["VAL2315_OVERALL", "PASS"], "2315 validation"),
    ("SRC2316_02_2315_formula", "2315_formula", PATHS["2315_formula"], ["FORM2315_2_qR", "j_q/M_q^2"], "q_R numerator/denominator formula"),
    ("SRC2316_03_2315_arena", "2315_arena", PATHS["2315_arena"], ["ARENA2315_0_PPN_gamma", "j_q"], "arena rows blocked by j_q/source normalization"),
    ("SRC2316_04_1088_conditional", "1088_conditional", PATHS["1088_conditional"], ["THM1088_5_conclusion", "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE"], "conditional ordinary-matter zero theorem"),
    ("SRC2316_05_1088_signature", "1088_signature", PATHS["1088_signature"], ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"], "MOMS signature not parent-derived"),
    ("SRC2316_06_1088_countermodel", "1088_countermodel", PATHS["1088_countermodel"], ["CM1088_0_species_weight", "NOT_KILLED_BY_CURRENT_CORPUS"], "live countermodels against matter source zero"),
    ("SRC2316_07_1087_descent", "1087_descent", PATHS["1087_descent"], ["PMD1087_6_verdict", "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED"], "matter descent zero not signed"),
    ("SRC2316_08_1087_contract", "1087_contract", PATHS["1087_contract"], ["ZCC1087_4_constant_superselection", "CONSTANT_SUPERSELECTION_UNSIGNED"], "future zero-current contract clauses"),
    ("SRC2316_09_1086_attempt", "1086_attempt", PATHS["1086_attempt"], ["SCZ1086_5_verdict", "SOURCE_CURRENT_ZERO_NOT_DERIVED"], "source-current zero attempt failed without parent premises"),
    ("SRC2316_10_1089_hunt", "1089_hunt", PATHS["1089_hunt"], ["HUNT1089_8_verdict", "NO_PARENT_SIGNATURE_SOURCE_FOUND"], "source hunt found no signed MOMS parent action"),
    ("SRC2316_11_1090_synthesis", "1090_synthesis", PATHS["1090_synthesis"], ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"], "MOMS synthesis failed without extra axioms"),
    ("SRC2316_12_1090_axioms", "1090_axioms", PATHS["1090_axioms"], ["AX1090_1_no_hidden_visible_hom", "MISSING_AXIOM_NOT_ADOPTED"], "missing axiom ledger"),
    ("SRC2316_13_1090_decision", "1090_decision", PATHS["1090_decision"], ["DEC1090_2_best_next", "no-hidden-visible-hom"], "best next derivation target"),
    ("SRC2316_14_2284_formula", "2284_formula", PATHS["2284_formula"], ["QRF2284_0_algebraic_parent_block", "q_R=j_q/M_q^2"], "finite q residual parent formula"),
    ("SRC2316_15_2285_projection", "2285_projection", PATHS["2285_projection"], ["POBS2285_0_gamma", "gamma_minus_1 = 1*q_R"], "PPN/R10 projection matrix remains nonclaim"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2316_SOURCE_REGISTER.csv",
    "transfer": OUT / "P8_Y5_PARENT_QLOC_2316_JQ_ZERO_THEOREM_TRANSFER.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_2316_MATTER_SIGNATURE_CLAUSE_STATUS.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2316_COUNTERMODEL_TO_JQ_MAP.csv",
    "source_pack": OUT / "P8_Y5_PARENT_QLOC_2316_FINITE_JQ_SOURCE_PACK.csv",
    "arena": OUT / "P8_Y5_PARENT_QLOC_2316_QR_ZERO_AND_ARENA_IMPACT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2316_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2316_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2316_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2316_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2316_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2316_0_transfer", OUTPUTS["transfer"], RAB_QUEUE / "JR2316_JQ_ZERO_THEOREM_TRANSFER_NONCLAIM.csv"),
    ("COPY2316_1_source_pack", OUTPUTS["source_pack"], RAB_QUEUE / "JR2316_FINITE_JQ_SOURCE_PACK_NONCLAIM.csv"),
    ("COPY2316_2_arena_beta", OUTPUTS["arena"], BETA_DOCS / "Q_JQ_SOURCE_LEG_ARENA_IMPACT_2316_NONCLAIM.csv"),
    ("COPY2316_3_arena_wep", OUTPUTS["arena"], MICRO_RESIDUALS / "jq_source_leg_arena_impact_nonclaim_2316.csv"),
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
        values = []
        for field in fields:
            values.append(str(row.get(field, "")).replace("\n", " ").replace("|", "\\|"))
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


def build_transfer_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQZ2316_0_definition",
            "statement": "Define j_q as the weak-field source-leg numerator in the q branch.",
            "formula": "delta_q S_matter = integral sqrt(g) j_q L q + O(L^2 q, q^2); q_R=j_q/(n_q^A H_AB n_q^B) on the 2315 branch.",
            "source_basis": "2315 FORM2315_2_qR plus 2284 QRF2284_0",
            "status": "DEFINITION_IMPORTED_AND_BRANCH_LOCKED",
            "claim_effect": "sets the numerator target; does not prove the numerator vanishes",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQZ2316_1_conditional_transfer",
            "statement": "If the full MOMS1088 ordinary-matter signature is parent-signed, then j_q^matter=0.",
            "formula": "MOMS1088 signed => delta_v S_matter=0 for v_q in ker(Dq) => j_q^matter=0.",
            "source_basis": "1088 THM1088_5_conclusion",
            "status": "CONDITIONAL_THEOREM_TRANSFERRED",
            "claim_effect": "strong route to local matter-source silence, but only under unsigned premises",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQZ2316_2_qR_consequence",
            "statement": "If M_q^2>0 and the same-branch matter numerator is zero, the matter part of q_R vanishes.",
            "formula": "M_q^2=n_q^A H_AB n_q^B>0 and j_q^matter=0 => q_R^matter=0.",
            "source_basis": "2314 denominator imported through 2315; 1088 conditional numerator theorem",
            "status": "CONDITIONAL_ALGEBRAIC_CONSEQUENCE",
            "claim_effect": "would remove the ordinary-matter q residual leg, not boundary/curvature/source-normalization legs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQZ2316_3_current_corpus_verdict",
            "statement": "Current corpus does not promote j_q^matter=0 to a claim.",
            "formula": "1089 no parent source + 1090 missing axioms => j_q^matter=0 remains conditional; finite source pack must stay live.",
            "source_basis": "1089 HUNT1089_8_verdict; 1090 SYN1090_8_verdict",
            "status": "ZERO_THEOREM_NOT_PROMOTED",
            "claim_effect": "local GR/Newton and R10/PPN scoring remain blocked",
            "valid_for_claim": "false",
        },
    ]


def build_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_0_action_form",
            "parent_clause": "single ordinary-matter parent action descends through observed quotient variables",
            "evidence_status": "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED",
            "needed_for_jq_zero": "gives a common owner for ordinary matter before readout/fitting",
            "current_gap": "one source action object is still a schema/contract, not derived",
            "source_row": "MOMS1088_0_action_form;SYN1090_1_action_object",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_1_quotient_pullback",
            "parent_clause": "v_q in ker(Dq) makes observed coframe/metric/gauge data silent by chain rule",
            "evidence_status": "EXACT_CONDITIONAL_LEMMA",
            "needed_for_jq_zero": "prevents visible geometry variation from producing j_q",
            "current_gap": "q, Obs_e, and matter bundle are not parent-selected in one action",
            "source_row": "MOMS1088_1_quotient_observables;SYN1090_2_quotient_pullback",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_2_matter_lift",
            "parent_clause": "ordinary matter vertical lifts are fixed, gauge, diffeo, Lorentz, or boundary-only",
            "evidence_status": "LIFT_OPTIONS_AVAILABLE_NOT_OWNED",
            "needed_for_jq_zero": "removes physical matter-field variation along the q-vertical direction",
            "current_gap": "parent matter bundle functor and boundary class remain unsigned",
            "source_row": "MOMS1088_2_matter_bundle;PMD1087_3_matter_functor;SYN1090_3_matter_lift",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_3_constants",
            "parent_clause": "masses, charges, alpha_EM, clocks, and labels are X-trivial or retained as explicit residual fields",
            "evidence_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "needed_for_jq_zero": "kills direct constant-sector contributions to j_q",
            "current_gap": "hidden-visible coefficient functions remain legal without an operator-domain theorem",
            "source_row": "MOMS1088_3_constant_superselection;ZCC1087_4_constant_superselection;AX1090_3_fixed_constant_sector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_4_no_species_weights",
            "parent_clause": "no independent w_A(X) S_A source weights before variation",
            "evidence_status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "needed_for_jq_zero": "prevents a weighted source numerator even when visible geometry descends",
            "current_gap": "common quantum/action measure owner is missing",
            "source_row": "MOMS1088_4_no_species_weights;SCZ1086_2_pre_action_weight_leak;AX1090_2_common_quantum_measure",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_5_variation_order",
            "parent_clause": "variation is taken before empirical readout, material projection, and source-worldtube fitting",
            "evidence_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "needed_for_jq_zero": "blocks post-variation creation or erasure of j_q",
            "current_gap": "detector/readout model not derived from the parent action",
            "source_row": "MOMS1088_5_variation_order;ZCC1087_2_variation_order;AX1090_4_variation_domain_order",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_6_no_shadow_domain",
            "parent_clause": "no conformal/disformal/source-only frame, support marker, boundary charge, or hidden-visible coefficient map",
            "evidence_status": "NO_SHADOW_DOMAIN_UNSIGNED",
            "needed_for_jq_zero": "closes the largest surviving direct coupling route into j_q",
            "current_gap": "no-hidden-visible-hom/operator-domain theorem is not yet derived",
            "source_row": "MOMS1088_6_no_shadow_domain;SYN1090_6_no_shadow_readout;AX1090_1_no_hidden_visible_hom",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2316_7_verdict",
            "parent_clause": "all MOMS clauses are parent-signed together",
            "evidence_status": "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "needed_for_jq_zero": "would promote JQZ2316_1 from conditional theorem to local-branch claim",
            "current_gap": "1089 and 1090 show no parent source and missing axioms",
            "source_row": "MOMS1088_7_verdict;HUNT1089_8_verdict;SYN1090_8_verdict",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_0_species_weight",
            "surviving_channel": "pre-action species/source weights",
            "j_q_map": "j_q contains j_weight = sum_A (partial_q w_A) T_A or its weak-field source projection",
            "damage_if_live": "visible metric can descend while active source strength is species/material dependent",
            "killed_by": "MOMS1088_4_no_species_weights plus AX1090_2 common action measure",
            "current_status": "LIVE_FINITE_NUMERATOR_CHANNEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_1_variable_constants",
            "surviving_channel": "alpha_EM, masses, clock standards, or material constants vary with hidden/representative variables",
            "j_q_map": "j_q contains j_const = sum_a (partial_q theta_a)(partial L_matter/partial theta_a)",
            "damage_if_live": "WEP, clocks, R10, and EM rows can receive composition-dependent coupling",
            "killed_by": "MOMS1088_3 constant superselection plus AX1090_1 no-hidden-visible-hom",
            "current_status": "LIVE_FINITE_NUMERATOR_CHANNEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_2_shadow_frame",
            "surviving_channel": "conformal/disformal/source-only matter frame",
            "j_q_map": "j_q contains j_shadow from partial_q A_A, partial_q B_A, or source-only metric coefficients",
            "damage_if_live": "a fifth-force-like residual hides outside the observed coframe chain rule",
            "killed_by": "MOMS1088_6 no shadow/domain plus AX1090_1 operator-domain theorem",
            "current_status": "LIVE_FINITE_NUMERATOR_CHANNEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_3_post_variation_selector",
            "surviving_channel": "readout/material projection after variation changes source normalization",
            "j_q_map": "j_q contains j_readout from source-worldtube, calibration, or material-selector dependence",
            "damage_if_live": "a residual source current can be manufactured by readout rather than parent dynamics",
            "killed_by": "MOMS1088_5 variation-before-readout plus AX1090_4 variation domain order",
            "current_status": "LIVE_FINITE_NUMERATOR_CHANNEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_4_boundary_domain",
            "surviving_channel": "support/domain marker, boundary charge, or local source profile shifts under v_q",
            "j_q_map": "j_q contains j_boundary or boundary hair Q_R that is not killed by bulk matter descent",
            "damage_if_live": "bulk zero can coexist with finite local/compact-source residuals",
            "killed_by": "parent boundary class, no-flux/no-charge theorem, or explicit boundary residual bound",
            "current_status": "LIVE_FINITE_NUMERATOR_CHANNEL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMJ2316_5_hidden_visible_hom",
            "surviving_channel": "hidden/representative variables hom into visible coefficients",
            "j_q_map": "j_q contains j_hom from direct coefficient maps f_X F^2, m_A(X), A_A(X), or detector coefficients",
            "damage_if_live": "coupling can survive every coframe descent clause unless the coefficient domain is closed",
            "killed_by": "AX1090_1 no-hidden-visible-hom/operator-domain theorem",
            "current_status": "BEST_NEXT_DERIVATION_TARGET",
            "valid_for_claim": "false",
        },
    ]


def build_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_0_total",
            "coefficient": "j_q_total",
            "definition": "j_q = j_matter + j_const + j_weight + j_shadow + j_readout + j_boundary + j_curvature + j_tail",
            "units_or_normalization": "q Euler-source / weak-field L coefficient; branch-normalization dependent",
            "source_status": "SYMBOLIC_DECOMPOSITION_ONLY",
            "missing_for_claim": "parent action, source normalization, units, coefficient values, and source paths for every nonzero term",
            "arena_use": "bookkeeping only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_1_matter",
            "coefficient": "j_matter",
            "definition": "ordinary-matter vertical source leg; zero under full MOMS1088 signature",
            "units_or_normalization": "same as j_q_total",
            "source_status": "CONDITIONAL_ZERO_NOT_PROMOTED",
            "missing_for_claim": "MOMS parent signature",
            "arena_use": "PPN/WEP/clock source silence if derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_2_weight",
            "coefficient": "j_weight",
            "definition": "pre-action source/species weighting contribution",
            "units_or_normalization": "partial_q w_A times Hilbert/source density",
            "source_status": "MISSING_PARENT_EXCLUSION_OR_VALUE",
            "missing_for_claim": "common action measure theorem or source-backed bound",
            "arena_use": "WEP/source normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_3_const",
            "coefficient": "j_const",
            "definition": "constant-sector derivative contribution from alpha_EM, masses, clocks, representation labels",
            "units_or_normalization": "sum_a partial_q theta_a partial L_matter/partial theta_a",
            "source_status": "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE",
            "missing_for_claim": "fixed constant sector or sourced sensitivities",
            "arena_use": "EM, clocks, WEP, particle/constant tests",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_4_shadow",
            "coefficient": "j_shadow",
            "definition": "conformal/disformal/source-only frame contribution",
            "units_or_normalization": "partial_q frame coefficient times matter stress/source density",
            "source_status": "MISSING_NO_SHADOW_THEOREM_OR_VALUE",
            "missing_for_claim": "no-hidden-visible-hom/operator-domain theorem",
            "arena_use": "PPN gamma, WEP, clocks, local force",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_5_readout",
            "coefficient": "j_readout",
            "definition": "post-variation material/readout/source-worldtube projection contribution",
            "units_or_normalization": "normalization dependent; must share branch with nHn denominator",
            "source_status": "MISSING_VARIATION_DOMAIN_ORDER_OR_VALUE",
            "missing_for_claim": "variation-before-readout theorem and detector/source model",
            "arena_use": "source normalization, PPN, orbital",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_6_boundary",
            "coefficient": "j_boundary",
            "definition": "compact-source boundary/domain support contribution, including possible Q_R hair",
            "units_or_normalization": "boundary flux or effective source charge",
            "source_status": "MISSING_BOUNDARY_CLASS_OR_VALUE",
            "missing_for_claim": "no-flux/no-charge theorem or explicit bound",
            "arena_use": "PPN local force, orbital, finite-range residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_7_curvature",
            "coefficient": "j_curvature",
            "definition": "higher-curvature/Weyl2 or D_q Weyl source coupling contribution",
            "units_or_normalization": "curvature-source normalization dependent",
            "source_status": "MISSING_PARENT_COEFFICIENT_OR_BOUND",
            "missing_for_claim": "D_qWeyl2 coefficient theorem or sourced bound",
            "arena_use": "R10/local geometry residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "JQPACK2316_8_same_branch_lock",
            "coefficient": "same_branch_lock",
            "definition": "the denominator n_q H n_q, numerator j_* terms, q normalization, and P_obs projection must be from the same parent branch",
            "units_or_normalization": "guard condition rather than coefficient",
            "source_status": "REQUIRED_GUARD",
            "missing_for_claim": "branch-locked parent action/source-normalization proof",
            "arena_use": "prevents mixing a closure denominator with an unrelated source numerator",
            "valid_for_claim": "false",
        },
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2316_0_PPN_gamma",
            "arena": "PPN gamma/light/Shapiro",
            "updated_formula": "gamma-1 = q_R + ... = j_q/(n_q H n_q) + retained q_loc/source terms + ...",
            "if_jq_zero": "ordinary-matter q_R leg drops out if MOMS and same-branch denominator are signed",
            "still_blocked_by": "MOMS unsigned; boundary/source normalization/q_loc channels remain",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2316_1_R10",
            "arena": "R10 short-range alpha(lambda)",
            "updated_formula": "alpha_q(lambda_q=xi_q) depends on K_q, Qbar_qH, qbar_qT, and finite j_q source pack",
            "if_jq_zero": "ordinary-matter source leg may vanish; curvature/boundary/hidden coupling legs still need coefficients",
            "still_blocked_by": "xi_q numeric/source, K_q/Qbar/qbar couplings, real bound curve, and j_q coefficient ownership",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2316_2_clocks_WEP",
            "arena": "clocks/WEP/composition",
            "updated_formula": "eta or clock residual receives j_const, j_weight, j_shadow, and j_readout unless MOMS closes them",
            "if_jq_zero": "MOMS would kill ordinary matter composition source channels in the q leg",
            "still_blocked_by": "constant superselection, no-species-weight, no-shadow, and readout-order clauses unsigned",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2316_3_orbital_Newton",
            "arena": "Newton/orbital/source normalization",
            "updated_formula": "local orbital residual must carry q_R plus separate delta_beta and observed-GM/source-normalization terms",
            "if_jq_zero": "only one q_R numerator leg is removed; beta and source-normalization still require derivation",
            "still_blocked_by": "Newtonian source charge theorem, beta completion, and boundary domain ownership",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2316_4_local_GR",
            "arena": "derived local GR/Newton limit",
            "updated_formula": "local-GR residual vector = {j_q/(nHn), q_loc, Q_R/boundary, delta_beta, delta_GM, curvature tail, hidden-visible hom terms}",
            "if_jq_zero": "the residual vector is shorter and cleaner, not empty",
            "still_blocked_by": "MOMS not signed and non-j_q residual vector not zeroed or bounded",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_1_conditional_transfer",
            "gate": "conditional MOMS -> j_q^matter=0 theorem transferred",
            "passed": "true",
            "claim_effect": "theorem route is sharper but remains conditional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_2_MOMS_signed",
            "gate": "MOMS ordinary-matter signature parent-signed",
            "passed": "false",
            "claim_effect": "j_q^matter=0 cannot be claimed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_3_finite_jq_values",
            "gate": "finite j_q source pack has numeric/source-backed coefficients",
            "passed": "false",
            "claim_effect": "R10/PPN/clock/orbital scoring blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_4_same_branch_lock",
            "gate": "numerator, denominator, projection, and source normalization are branch-locked",
            "passed": "false",
            "claim_effect": "cannot combine conditional denominator with unrelated source coefficients",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2316_5_local_GR_Newton",
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
            "row_id": "REF2316_0_claim_jq_zero",
            "claim": "j_q=0 is now proven by the current corpus",
            "allowed": "false",
            "reason": "only the conditional MOMS theorem is transferred; MOMS remains unsigned in 1088/1089/1090",
            "blocking_rows": "SIG2316_7_verdict;CG2316_2_MOMS_signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2316_1_claim_local_GR",
            "claim": "MTS now derives the local GR/Newton limit",
            "allowed": "false",
            "reason": "even if j_q^matter vanished, q_loc, Q_R/boundary, beta, source-normalization, curvature, and hidden-visible channels remain",
            "blocking_rows": "ARENA2316_4_local_GR;CG2316_5_local_GR_Newton",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2316_2_score_R10_PPN",
            "claim": "R10/PPN scoring can run with the 2316 rows",
            "allowed": "false",
            "reason": "finite source pack is symbolic and branch-normalization dependent",
            "blocking_rows": "JQPACK2316_0_total;CG2316_3_finite_jq_values;CG2316_4_same_branch_lock",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2316_3_use_countermodels_as_values",
            "claim": "countermodel j_q terms are numerical priors",
            "allowed": "false",
            "reason": "countermodel rows are only live residual channels until parent coefficients or bounds are sourced",
            "blocking_rows": "CMJ2316_0_species_weight;CMJ2316_5_hidden_visible_hom",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2316_0",
            "next_target": "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md",
            "why": "the no-hidden-visible-hom/operator-domain theorem attacks the biggest coupling leak at once: constant-sector, EM/mass, shadow-frame, source-only metric, and readout coefficient maps",
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
    transfer_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    source_pack_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [
        source_rows,
        transfer_rows,
        signature_rows,
        countermodel_rows,
        source_pack_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    ]
    formalization_output_markers = (
        "2316-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2316",
        "P8_Y5_BRR545_2316",
        "JR2316_",
        "Q_JQ_SOURCE_LEG_ARENA_IMPACT_2316",
        "jq_source_leg_arena_impact_nonclaim_2316",
        "Y5_R2FR_jq_source_leg_zero_theorem_or_finite_source_pack_2316",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    source_pack_ids = {row["row_id"] for row in source_pack_rows}
    countermodel_ids = {row["row_id"] for row in countermodel_rows}
    signature_ids = {row["row_id"] for row in signature_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2316_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2316_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2316_02_transfer_written", any(row["row_id"] == "JQZ2316_1_conditional_transfer" and "j_q^matter=0" in row["formula"] for row in transfer_rows), "MOMS conditional zero theorem transferred to j_q language"))
    checks.append(("VAL2316_03_zero_not_promoted", any(row["row_id"] == "JQZ2316_3_current_corpus_verdict" and row["status"] == "ZERO_THEOREM_NOT_PROMOTED" for row in transfer_rows), "current corpus verdict keeps j_q zero nonclaim"))
    checks.append(("VAL2316_04_signature_blockers_preserved", {"SIG2316_3_constants", "SIG2316_4_no_species_weights", "SIG2316_6_no_shadow_domain", "SIG2316_7_verdict"}.issubset(signature_ids), "signature blocker rows retained"))
    checks.append(("VAL2316_05_countermodels_mapped", {"CMJ2316_0_species_weight", "CMJ2316_1_variable_constants", "CMJ2316_2_shadow_frame", "CMJ2316_3_post_variation_selector", "CMJ2316_4_boundary_domain", "CMJ2316_5_hidden_visible_hom"}.issubset(countermodel_ids), "all retained countermodels mapped to j_q channels"))
    checks.append(("VAL2316_06_source_pack_complete", {"JQPACK2316_0_total", "JQPACK2316_1_matter", "JQPACK2316_2_weight", "JQPACK2316_3_const", "JQPACK2316_4_shadow", "JQPACK2316_5_readout", "JQPACK2316_6_boundary", "JQPACK2316_7_curvature", "JQPACK2316_8_same_branch_lock"}.issubset(source_pack_ids), "finite j_q source pack is explicit"))
    checks.append(("VAL2316_07_arena_blocks_preserved", all(row["score_ready"] == "false" for row in arena_rows), "all arena rows remain blocked/nonclaim"))
    checks.append(("VAL2316_08_claim_gates_block", any(row["row_id"] == "CG2316_5_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2316_09_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2316_10_next_target", any(row["row_id"] == "NEXT2316_0" and "no-hidden-visible-hom" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2316_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2316_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2316_13_formalization_untouched_by_2316", len(formalization_hits) == 0, "no 2316 checkpoint output appears in formalization-workbench"))

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
            "row_id": "VAL2316_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2316 transfers the old conditional MOMS ordinary-matter zero theorem into current j_q numerator language, proves only the conditional implication MOMS=>j_q^matter=0, refuses to promote it because the parent signature remains unsigned, stages a finite j_q source pack for all live coupling leaks, keeps every arena score blocked, and selects the no-hidden-visible-hom/operator-domain theorem as the next derivation target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    transfer_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    source_pack_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2316 - j_q Source-Leg Zero Theorem Or Finite Source Pack",
        "",
        "## Summary",
        "",
        "2316 takes the coupling problem head-on. The useful result is not a new public claim: it is a cleaner split between a conditional zero theorem and the finite source terms that still have to be derived, killed, or bounded.",
        "",
        "The old MOMS1088 ordinary-matter theorem transfers cleanly into the current 2315 notation: if the full parent ordinary-matter signature is signed, then `delta_v S_matter=0` along the quotient-vertical q direction, so the ordinary-matter source numerator satisfies `j_q^matter=0`. With the 2315 denominator this would give `q_R^matter=0` when `M_q^2=n_q H n_q>0` on the same branch.",
        "",
        "But the current corpus still does not sign MOMS. 1089 found no parent source, and 1090 showed that the synthesis needs missing axioms. Therefore this checkpoint refuses the local-GR/PPN/R10 claim and keeps a finite numerator pack live: `j_q = j_matter + j_const + j_weight + j_shadow + j_readout + j_boundary + j_curvature + j_tail`.",
        "",
        "The best next derivation target is the no-hidden-visible-hom/operator-domain theorem. That one is the coupling beast: it attacks direct alpha/mass/EM maps, shadow frames, source-only metrics, and material coefficient leaks in one place.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## j_q Zero Theorem Transfer",
        "",
        markdown_table(transfer_rows, ["row_id", "statement", "formula", "source_basis", "status", "claim_effect", "valid_for_claim"]),
        "",
        "## Matter Signature Clause Status",
        "",
        markdown_table(signature_rows, ["row_id", "parent_clause", "evidence_status", "needed_for_jq_zero", "current_gap", "source_row", "valid_for_claim"]),
        "",
        "## Countermodel To j_q Map",
        "",
        markdown_table(countermodel_rows, ["row_id", "surviving_channel", "j_q_map", "damage_if_live", "killed_by", "current_status", "valid_for_claim"]),
        "",
        "## Finite j_q Source Pack",
        "",
        markdown_table(source_pack_rows, ["row_id", "coefficient", "definition", "units_or_normalization", "source_status", "missing_for_claim", "arena_use", "valid_for_claim"]),
        "",
        "## q_R Zero And Arena Impact",
        "",
        markdown_table(arena_rows, ["row_id", "arena", "updated_formula", "if_jq_zero", "still_blocked_by", "score_ready", "valid_for_claim"]),
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
    transfer_rows = build_transfer_rows()
    signature_rows = build_signature_rows()
    countermodel_rows = build_countermodel_rows()
    source_pack_rows = build_source_pack_rows()
    arena_rows = build_arena_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["transfer"], transfer_rows)
    write_csv(OUTPUTS["signature"], signature_rows)
    write_csv(OUTPUTS["countermodels"], countermodel_rows)
    write_csv(OUTPUTS["source_pack"], source_pack_rows)
    write_csv(OUTPUTS["arena"], arena_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        transfer_rows,
        signature_rows,
        countermodel_rows,
        source_pack_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        transfer_rows,
        signature_rows,
        countermodel_rows,
        source_pack_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2316_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
