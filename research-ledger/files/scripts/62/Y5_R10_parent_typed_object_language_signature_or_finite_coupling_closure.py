from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1220"
TITLE = "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SIGNATURE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_TYPED_SIGNATURE_ATTEMPT.csv"
CLAUSE_COVERAGE_PATH = OUT_DIR / f"{PACK_ID}_SIGNATURE_CLAUSE_COVERAGE.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_IF_SIGNED_THEOREM_PACK.csv"
DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_NO_HIDDEN_VISIBLE_ROUTE_DEMOTION.csv"
FINITE_CLOSURE_PATH = OUT_DIR / f"{PACK_ID}_FINITE_COUPLING_CLOSURE_REGISTER.csv"
COUNTEREXAMPLE_PATH = OUT_DIR / f"{PACK_ID}_COUNTEREXAMPLE_LOCK_UPDATE.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1220_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def is_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return value is False
    return str(value).strip().lower() == "false"


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1220_0_1219_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_NEXT_TARGET.csv",
            "needle": "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md",
            "purpose": "1219 handoff to parent typed object-language signature target",
        },
        {
            "source_id": "SRC1220_1_1219_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TVC1219_6_verdict",
            "purpose": "typed visible coefficient functor not derived",
        },
        {
            "source_id": "SRC1220_2_1219_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_1_alpha",
            "purpose": "active hidden scalar counterexamples",
        },
        {
            "source_id": "SRC1220_3_1219_debts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv",
            "needle": "FC1219_0_alpha",
            "purpose": "finite coupling closure debt rows",
        },
        {
            "source_id": "SRC1220_4_1065_grammar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "needle": "PGG1065_5_verdict",
            "purpose": "parent grammar candidate not signed",
        },
        {
            "source_id": "SRC1220_5_1065_allowed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv",
            "needle": "AAG1065_4_source_only_species_scalar",
            "purpose": "allowed/prohibited grammar rows",
        },
        {
            "source_id": "SRC1220_6_1065_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
            "needle": "WTZ1065_4_verdict",
            "purpose": "source-weight theorem-zero clauses not signed",
        },
        {
            "source_id": "SRC1220_7_1066_typing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
            "needle": "OLT1066_6_verdict",
            "purpose": "object-language typing audit",
        },
        {
            "source_id": "SRC1220_8_1066_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
            "needle": "ODR1066_4_verdict",
            "purpose": "operator-domain exclusion not derived",
        },
        {
            "source_id": "SRC1220_9_1066_exclusion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "purpose": "source-scalar exclusion conditional only",
        },
        {
            "source_id": "SRC1220_10_1066_normalization",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "needle": "FMQ1066_4_verdict",
            "purpose": "action-scale/measure owner missing",
        },
        {
            "source_id": "SRC1220_11_1055_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "purpose": "single parent action contract candidate",
        },
        {
            "source_id": "SRC1220_12_1055_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
            "needle": "ADG1055_0_derivation_not_minimality",
            "purpose": "no aesthetic minimality adoption gate",
        },
        {
            "source_id": "SRC1220_13_1055_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CE1055_1_hidden_invariant_scalar",
            "purpose": "counterexamples if contract unsigned",
        },
        {
            "source_id": "SRC1220_14_1045_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "needle": "MFS1045_6_verdict",
            "purpose": "matter functor not parent signed",
        },
        {
            "source_id": "SRC1220_15_1088_MOMS",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_7_verdict",
            "purpose": "MOMS signature not derived",
        },
        {
            "source_id": "SRC1220_16_1089_coverage",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv",
            "needle": "MOMS1088_7_all_in_one",
            "purpose": "no single source signs all clauses",
        },
        {
            "source_id": "SRC1220_17_1114_obstructions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1114_0_grammar",
            "purpose": "typed grammar and scalar obstruction ledger",
        },
        {
            "source_id": "SRC1220_18_1114_nohom",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "purpose": "no-hidden-visible theorem not derived",
        },
        {
            "source_id": "SRC1220_19_1092_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
            "needle": "GEN1092_0_finite_cell_spectrum",
            "purpose": "surviving invariant generators",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    debt_1219 = read_csv(OUT_DIR / "P8_Y5_R10_1219_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv")
    alpha_debt = find_row(debt_1219, "debt_id", "FC1219_0_alpha")
    surface_debt = find_row(debt_1219, "debt_id", "FC1219_1_surface")
    norm_debt = find_row(debt_1219, "debt_id", "FC1219_2_common_norm")
    tail_debt = find_row(debt_1219, "debt_id", "FC1219_3_tail")
    readout_debt = find_row(debt_1219, "debt_id", "FC1219_4_readout")

    signature_rows = [
        {
            "signature_id": "PTOL1220_0_parent_domain",
            "required_clause": "one parent object language is declared before readout/fitting",
            "candidate_source": "PAC1055_6_single_parent_action; PGG1065_0_parent_language",
            "test": "is the domain derived from MTS primitives rather than adopted as a discipline contract?",
            "current_status": "SCHEMA_WRITTEN_NOT_DERIVED",
            "effect_if_signed": "visible coefficient functors can be type-checked against one parent domain",
            "effect_if_unsigned": "hidden coefficient maps remain legal closure terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_1_visible_coefficient_domain",
            "required_clause": "Coeff(O_vis) may depend only on q_loc and fixed representation/topological data",
            "candidate_source": "ODR1066_0_allowed_coefficient_ring; PAC1055_3_no_mixed_coefficients",
            "test": "does the corpus derive Hom(C_hid,Coeff(O_vis))=empty rather than assume it?",
            "current_status": "POWERFUL_RULE_NOT_DERIVED",
            "effect_if_signed": "f(I_hid)F_Q^2, mass(I), binding(I), clock(I), and source_weight(I) become ill-typed",
            "effect_if_unsigned": "HSC1219 counterexamples stay active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_2_matter_bundle_constants",
            "required_clause": "ordinary matter constants are fixed representation/superselection data or explicit residuals",
            "candidate_source": "MFS1045_5_constants_split; MOMS1088_3_constant_superselection; PAC1055_2_matter_functor",
            "test": "are the matter bundle, vertical lift, and constants parent-constructed for all ordinary species?",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "effect_if_signed": "surface/binding/mass/clock coefficient drift can be theorem-zero",
            "effect_if_unsigned": "surface, mass, and clock residual rows remain mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_3_source_weight_exclusion",
            "required_clause": "source-only species weights are not objects in the parent matter grammar",
            "candidate_source": "PGG1065_5_verdict; SSE1066_5_verdict; WTZ1065_4_verdict",
            "test": "is w_A syntactically impossible, not merely absent from a chosen action?",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "effect_if_signed": "relative source-weight WEP branch can be theorem-zero after projection/readout closure",
            "effect_if_unsigned": "finite Delta_w/source-weight closure debt remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_4_action_scale_measure_owner",
            "required_clause": "one parent action scale/measure/hbar owner covers all ordinary matter sectors",
            "candidate_source": "FMQ1066_4_verdict; ADG1055_3_source_label_forgetting",
            "test": "can species-dependent action multipliers be shown gauge/quotient redundant in source and quantum measure?",
            "current_status": "NOT_PARENT_SIGNED",
            "effect_if_signed": "source-only normalization counterexample is removed",
            "effect_if_unsigned": "w_A S_A remains a live source-coupling counterexample",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_5_radiative_readout_closure",
            "required_clause": "effective/readout maps preserve the same typed coefficient domain",
            "candidate_source": "PAC1055_5_radiative_readout_closure; CE1055_4_readout_regeneration; OBS1114_3_radiative",
            "test": "does the type rule survive S_eff, loops, spectroscopy, and MICROSCOPE/readout projection?",
            "current_status": "UNSIGNED",
            "effect_if_signed": "bare action zero can transfer to observable clock/WEP/alpha rows",
            "effect_if_unsigned": "readout coefficient drift remains finite closure debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_6_no_extension_no_marker",
            "required_clause": "no co-moving marker, domain selector, boundary class, or hidden invariant extends coefficient domains",
            "candidate_source": "NMF980_7_verdict; OBS1114_2_no_extension; GEN1092_*",
            "test": "are all scalar/marker extensions removed or typed out?",
            "current_status": "NOT_DERIVED",
            "effect_if_signed": "continuous hidden scalar counterexample loses its argument source",
            "effect_if_unsigned": "HSC1219_0 generic scalar remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "signature_id": "PTOL1220_7_verdict",
            "required_clause": "parent typed object-language signature certificate",
            "candidate_source": "PTOL1220_0 through PTOL1220_6",
            "test": "do all clauses form one signed parent grammar/action-domain certificate?",
            "current_status": "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED",
            "effect_if_signed": "no-hidden-visible route can reopen as theorem-zero",
            "effect_if_unsigned": "demote no-hidden-visible route to finite-coupling closure debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coverage_rows = [
        {
            "clause_id": "COV1220_0_parent_domain",
            "coverage": "single-action schema exists",
            "best_source": "PAC1055_6; PGG1065_0",
            "source_status": "schema_written_not_derived",
            "claim_gap": "derive the parent action language from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "COV1220_1_visible_coefficients",
            "coverage": "typed coefficient rule exists as conditional theorem",
            "best_source": "ODR1066_0; TVC1219_1; NHV1114_1",
            "source_status": "conditional_rule_not_parent_signed",
            "claim_gap": "prove hidden objects are absent from coefficient argument domains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "COV1220_2_matter_functor",
            "coverage": "matter functor and constant-sector route named",
            "best_source": "MFS1045_6; MOMS1088_3; PAC1055_2",
            "source_status": "matter_bundle_and_constants_unsigned",
            "claim_gap": "construct the species-complete matter bundle and fixed constants",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "COV1220_3_source_weights",
            "coverage": "source-only scalar exclusion is exact conditionally",
            "best_source": "PGG1065_5; SSE1066_5",
            "source_status": "conditional_not_parent_signed",
            "claim_gap": "derive action-scale/measure/current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "COV1220_4_readout",
            "coverage": "readout regeneration obstruction is explicit",
            "best_source": "PAC1055_5; OBS1114_3",
            "source_status": "closure_missing",
            "claim_gap": "prove renormalized/readout functor preserves the typed grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "COV1220_5_all_in_one",
            "coverage": "no single source signs all clauses",
            "best_source": "MOMS1088_7_all_in_one; PTOL1220_7_verdict",
            "source_status": "NO_PARENT_SIGNATURE_CERTIFICATE",
            "claim_gap": "certificate absent; closure demotion required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_rows = [
        {
            "theorem_id": "IFSIG1220_0_no_hidden_coefficients",
            "if_signed": "PTOL1220_0 through PTOL1220_6 all hold in one parent action-domain certificate",
            "derivation": "visible coefficients are typed/factored through q_loc and fixed representation/topological data, so hidden/local scalar arguments cannot enter",
            "would_close": "HSC1219 hidden scalar counterexamples and no-hidden-visible coefficient morphism",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "IFSIG1220_1_alpha_surface",
            "if_signed": "no-hidden coefficients plus EM-F2/matter-functor/readout clauses",
            "derivation": "c_alpha and c_surface have no hidden/local scalar arguments; vertical derivative vanishes",
            "would_close": "FC1219_0_alpha and FC1219_1_surface",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "IFSIG1220_2_source_weight",
            "if_signed": "typed grammar plus action-scale/current owner",
            "derivation": "w_A is not an admissible parent object and source extraction happens before readout selectors",
            "would_close": "source-only WEP weight branch",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "IFSIG1220_3_observed_transfer",
            "if_signed": "radiative/readout closure preserves the typed domain",
            "derivation": "tree-level coefficient silence survives S_eff, clocks, spectroscopy, WEP readout, and R10 projection",
            "would_close": "readout regeneration counterexample",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "IFSIG1220_4_current_verdict",
            "if_signed": "current corpus is audited",
            "derivation": "not all clauses are signed; therefore theorem-zero cannot be promoted",
            "would_close": "nothing yet; this is a demotion checkpoint",
            "current_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    demotion_rows = [
        {
            "demotion_id": "DEM1220_0_route_status",
            "route": "no-hidden-visible typed coefficient route",
            "demotion": "demote from theorem route to explicit closure unless a new parent grammar certificate appears",
            "because": "PTOL1220_7 verdict says no signed parent typed object-language certificate exists",
            "effect": "finite coupling rows cannot be retired by absence/minimality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1220_1_contract_status",
            "route": "PAC1055/P1065 grammar contract",
            "demotion": "usable as private discipline contract only",
            "because": "contract rows are exact but repeatedly labelled not parent-derived",
            "effect": "may guide future action writing but cannot pass WEP/PPN/R10 gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1220_2_hidden_scalar",
            "route": "hidden scalar counterexample",
            "demotion": "promote counterexample to mandatory closure annotation on affected finite rows",
            "because": "continuous hidden scalar target remains allowed if grammar is unsigned",
            "effect": "alpha/surface/clock/source rows carry explicit HSC/CE blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_rows = [
        {
            "closure_id": "FCCR1220_0_alpha",
            "from_debt_row": "FC1219_0_alpha",
            "coefficient_or_debt": alpha_debt["coefficient_or_debt"],
            "retained_counterexample": alpha_debt["retained_counterexample"],
            "threshold_or_source": alpha_debt["threshold_or_source"],
            "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT",
            "required_to_promote": "new signed parent grammar certificate plus EM-F2/readout closure, or source-backed alpha prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "FCCR1220_1_surface",
            "from_debt_row": "FC1219_1_surface",
            "coefficient_or_debt": surface_debt["coefficient_or_debt"],
            "retained_counterexample": surface_debt["retained_counterexample"],
            "threshold_or_source": surface_debt["threshold_or_source"],
            "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT",
            "required_to_promote": "new signed parent grammar certificate plus matter-constant/readout closure, or source-backed surface prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "FCCR1220_2_common_norm",
            "from_debt_row": "FC1219_2_common_norm",
            "coefficient_or_debt": norm_debt["coefficient_or_debt"],
            "retained_counterexample": norm_debt["retained_counterexample"],
            "threshold_or_source": norm_debt["threshold_or_source"],
            "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT",
            "required_to_promote": "same-branch vector norm fixed before material/readout choice",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "FCCR1220_3_tail",
            "from_debt_row": "FC1219_3_tail",
            "coefficient_or_debt": tail_debt["coefficient_or_debt"],
            "retained_counterexample": tail_debt["retained_counterexample"],
            "threshold_or_source": tail_debt["threshold_or_source"],
            "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT",
            "required_to_promote": "basis completeness theorem or empirical all-material tail envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "FCCR1220_4_readout",
            "from_debt_row": "FC1219_4_readout",
            "coefficient_or_debt": readout_debt["coefficient_or_debt"],
            "retained_counterexample": readout_debt["retained_counterexample"],
            "threshold_or_source": readout_debt["threshold_or_source"],
            "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT",
            "required_to_promote": "renormalized/readout functor closure or sourced residual prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexample_rows = [
        {
            "counterexample_id": "CELOCK1220_0_hidden_scalar",
            "source_counterexample": "HSC1219_0_generic_scalar;CE1055_1_hidden_invariant_scalar",
            "still_active": True,
            "why": "typed object language and invariant algebra triviality are not parent-signed",
            "affected_rows": "FCCR1220_0_alpha;FCCR1220_1_surface;FCCR1220_2_common_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CELOCK1220_1_alpha_F2",
            "source_counterexample": "HSC1219_1_alpha;CE1055_0_gauge_kinetic_function",
            "still_active": True,
            "why": "scalar gauge kinetic functions are covariant and visible-gauge invariant unless the domain forbids them",
            "affected_rows": "FCCR1220_0_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CELOCK1220_2_source_weight",
            "source_counterexample": "HSC1219_4_source_weight;CE1055_3_relative_source_weight",
            "still_active": True,
            "why": "action-scale/current/source-label owner is not parent-derived",
            "affected_rows": "source-weight/WEP/local-GR source branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CELOCK1220_3_readout",
            "source_counterexample": "HSC1219_3_clock;CE1055_4_readout_regeneration",
            "still_active": True,
            "why": "radiative/readout closure is unsigned",
            "affected_rows": "FCCR1220_4_readout;clock;alpha_eff",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "FEED1220_0_to_TVC1219_6",
            "target_row": "TVC1219_6_verdict",
            "update": "signature certificate not built; typed-functor route demoted to closure debt",
            "source_rows": "PTOL1220_7_verdict;DEM1220_0_route_status",
            "current_status": "NO_PARENT_TYPED_SIGNATURE_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1220_1_to_FC1219",
            "target_row": "FC1219 finite coupling closure debts",
            "update": "all affected finite rows now explicitly registered as closure debts",
            "source_rows": "FCCR1220_0_alpha;FCCR1220_1_surface;FCCR1220_2_common_norm;FCCR1220_3_tail;FCCR1220_4_readout",
            "current_status": "FINITE_CLOSURE_REGISTER_CREATED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1220_2_to_local_GR",
            "target_row": "local GR/Newton source-side coupling branch",
            "update": "typed grammar would help but is not signed and cannot close EH/source Hamiltonian/PPN gates",
            "source_rows": "PTOL1220_7_verdict;FCCR1220_2_common_norm;CELOCK1220_2_source_weight",
            "current_status": "LOCAL_GR_SOURCE_SIDE_STILL_CLAIM_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1220_0_signature_or_closure_stub",
            "signature_certificate_valid": False,
            "finite_closure_rows": 5,
            "counterexample_locks": 4,
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject theorem promotion and accept explicit finite closure register",
            "reason": "parent typed signature certificate is absent; closure rows are nonclaim",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1220_0_no_certificate",
            "decision": "do not promote parent typed object language to theorem",
            "because": "all clauses are useful but at least one critical clause is unsigned in every route",
            "next_action": "treat no-hidden-visible route as closure unless a new primitive source appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1220_1_closure_register",
            "decision": "create explicit finite coupling closure register",
            "because": "the project needs trackable finite debts rather than repeated re-litigation of the same grammar gap",
            "next_action": "turn closure register into either source-acquisition rows or a parent-primitive source hunt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1220_2_derivation_boundary",
            "decision": "do not use absence in a proposed action as proof",
            "because": "1055 adoption gates explicitly forbid aesthetic minimality as claim evidence",
            "next_action": "future derivation must supply primitive grammar construction, not just a clean contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1220_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1220 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1220_1_signature_certificate",
            "gate": "parent typed object-language signature certificate",
            "status": "BLOCKED",
            "reason": "PTOL1220_7_verdict=PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1220_2_no_hidden_visible",
            "gate": "no-hidden-visible theorem promotion",
            "status": "BLOCKED",
            "reason": "route demoted to finite closure debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1220_3_counterexamples",
            "gate": "counterexample locks removed",
            "status": "BLOCKED",
            "reason": "CELOCK1220 rows remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1220_4_finite_closure",
            "gate": "finite closure rows score-ready",
            "status": "BLOCKED",
            "reason": "closure rows are explicit but not source-backed/scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1220_5_local_GR",
            "gate": "local GR/Newton derivation",
            "status": "BLOCKED",
            "reason": "typed signature gap is only one source-side issue; EH/source Hamiltonian/PPN gates remain independent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1220_0_1221",
            "target_file": "1221-Y5-R10-finite-coupling-closure-scorepack-or-parent-primitive-source.md",
            "target_script": "scripts/Y5_R10_finite_coupling_closure_scorepack_or_parent_primitive_source.py",
            "task": "turn the finite coupling closure register into source-acquisition/scorepack rows while keeping an escape hatch for a genuinely new parent grammar primitive source",
            "success_condition": "alpha/surface/readout/source-weight closure debts get source-acquisition schemas and runner-ready nonclaim rows, or a new primitive derivation source reopens the theorem route",
            "do_not_do": "do not re-argue the same unsigned grammar contract as a proof; do not claim WEP/local-GR/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    signature_fields = ["signature_id", "required_clause", "candidate_source", "test", "current_status", "effect_if_signed", "effect_if_unsigned", "valid_for_claim", "claim_allowed"]
    coverage_fields = ["clause_id", "coverage", "best_source", "source_status", "claim_gap", "valid_for_claim", "claim_allowed"]
    theorem_fields = ["theorem_id", "if_signed", "derivation", "would_close", "current_status", "valid_for_claim", "claim_allowed"]
    demotion_fields = ["demotion_id", "route", "demotion", "because", "effect", "valid_for_claim", "claim_allowed"]
    finite_fields = ["closure_id", "from_debt_row", "coefficient_or_debt", "retained_counterexample", "threshold_or_source", "closure_status", "required_to_promote", "valid_for_claim", "claim_allowed"]
    counterexample_fields = ["counterexample_id", "source_counterexample", "still_active", "why", "affected_rows", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "update", "source_rows", "current_status", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "signature_certificate_valid", "finite_closure_rows", "counterexample_locks", "valid_prediction_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(SIGNATURE_ATTEMPT_PATH, signature_rows, signature_fields)
    write_csv(CLAUSE_COVERAGE_PATH, coverage_rows, coverage_fields)
    write_csv(CONDITIONAL_THEOREM_PATH, theorem_rows, theorem_fields)
    write_csv(DEMOTION_PATH, demotion_rows, demotion_fields)
    write_csv(FINITE_CLOSURE_PATH, finite_rows, finite_fields)
    write_csv(COUNTEREXAMPLE_PATH, counterexample_rows, counterexample_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        SIGNATURE_ATTEMPT_PATH,
        CLAUSE_COVERAGE_PATH,
        CONDITIONAL_THEOREM_PATH,
        DEMOTION_PATH,
        FINITE_CLOSURE_PATH,
        COUNTEREXAMPLE_PATH,
        FEED_PATH,
        RUNNER_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = read_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    signature_not_derived = any(row["signature_id"] == "PTOL1220_7_verdict" and row["current_status"] == "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED" for row in signature_rows)
    no_all_in_one_certificate = any(row["clause_id"] == "COV1220_5_all_in_one" and row["source_status"] == "NO_PARENT_SIGNATURE_CERTIFICATE" for row in coverage_rows)
    conditionals_not_promoted = any(row["theorem_id"] == "IFSIG1220_4_current_verdict" and row["current_status"] == "NOT_PROMOTED" for row in theorem_rows)
    route_demoted = any(row["demotion_id"] == "DEM1220_0_route_status" and "demote" in row["demotion"].lower() for row in demotion_rows)
    finite_register_created = len(finite_rows) == 5 and all(row["closure_status"] == "FINITE_CLOSURE_DEBT_EXPLICIT" for row in finite_rows)
    counterexamples_active = all(row["still_active"] is True for row in counterexample_rows)
    numeric_thresholds_positive = all(float(row["threshold_or_source"]) > 0 for row in finite_rows[:3])
    missing_rows_nonclaim = all(not (has_missing(row) and not is_false(row, "valid_for_claim")) for row in finite_rows + feed_rows)
    runner_refuses = runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    claim_locks_blocked = all(
        any(row["gate_id"] == gate_id and row["status"] == "BLOCKED" for row in claim_gates)
        for gate_id in ["GATE1220_1_signature_certificate", "GATE1220_2_no_hidden_visible", "GATE1220_3_counterexamples", "GATE1220_4_finite_closure", "GATE1220_5_local_GR"]
    )
    no_claim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for row in signature_rows + coverage_rows + theorem_rows + demotion_rows + finite_rows + counterexample_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1221 = next_rows[0]["target_file"].startswith("1221-")

    validation_rows = [
        validation_row("VAL1220_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1220_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1220_2_signature_not_derived", "signature certificate is not overclaimed", signature_not_derived, "PTOL1220_7_verdict=PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"),
        validation_row("VAL1220_3_no_all_in_one", "no all-in-one parent certificate exists", no_all_in_one_certificate, "COV1220_5_all_in_one=NO_PARENT_SIGNATURE_CERTIFICATE"),
        validation_row("VAL1220_4_conditionals_not_promoted", "conditional theorems are not promoted", conditionals_not_promoted, "IFSIG1220_4_current_verdict=NOT_PROMOTED"),
        validation_row("VAL1220_5_route_demoted", "no-hidden-visible route demoted", route_demoted, "DEM1220_0_route_status records demotion"),
        validation_row("VAL1220_6_finite_register_created", "finite closure register created", finite_register_created, "; ".join(row["closure_id"] for row in finite_rows)),
        validation_row("VAL1220_7_counterexamples_active", "counterexamples remain active", counterexamples_active, "; ".join(row["counterexample_id"] for row in counterexample_rows)),
        validation_row("VAL1220_8_thresholds_positive", "carried numeric thresholds are positive", numeric_thresholds_positive, "; ".join(f"{row['closure_id']}={row['threshold_or_source']}" for row in finite_rows[:3])),
        validation_row("VAL1220_9_missing_rows_nonclaim", "no MISSING row is valid for claim", missing_rows_nonclaim, "tail/readout missing rows remain nonclaim"),
        validation_row("VAL1220_10_runner_refuses", "runner stub refuses missing product", runner_refuses, "valid_prediction_rows=0 and claim_allowed=false"),
        validation_row("VAL1220_11_claim_locks_blocked", "claim locks remain blocked", claim_locks_blocked, "signature, no-hidden-visible, counterexamples, finite closure, and local-GR gates blocked"),
        validation_row("VAL1220_12_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1220_13_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1220_14_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1220_15_next_target", "next target is staged", next_1221, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1220_16_overall",
            "overall 1220 validation",
            validation_pass,
            "1220 parent typed signature pack is reproducible, nonclaim, and finite-closure-demoted" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1220 Y5/R10 Parent Typed Object Language Signature Or Finite Coupling Closure

**Current verdict:** 1220 does **not** produce a signed parent typed object-language/action-domain certificate. The no-hidden-visible route is therefore demoted to explicit finite-coupling closure debt unless a genuinely new parent grammar primitive is supplied.

**Main progress:** the grammar route is now cleanly separated from evidence. The contract is powerful and mathematically exact if adopted, but every critical clause is still conditional: parent domain, visible coefficient domain, matter constants, source-weight exclusion, action-scale owner, no-extension/no-marker, and radiative/readout closure.

**Practical consequence:** absence of hidden couplings in a clean draft action is not enough. The affected alpha, surface/binding, common-norm, tail, and readout rows now sit in a finite closure register with their counterexamples attached.

## Source Register

{markdown_table(source_rows, source_fields)}

## Parent Typed Signature Attempt

{markdown_table(signature_rows, signature_fields)}

## Signature Clause Coverage

{markdown_table(coverage_rows, coverage_fields)}

## If-Signed Theorem Pack

{markdown_table(theorem_rows, theorem_fields)}

## No-Hidden-Visible Route Demotion

{markdown_table(demotion_rows, demotion_fields)}

## Finite Coupling Closure Register

{markdown_table(finite_rows, finite_fields)}

## Counterexample Lock Update

{markdown_table(counterexample_rows, counterexample_fields)}

## Feed Update

{markdown_table(feed_rows, feed_fields)}

## Product Runner Stub

{markdown_table(runner_rows, runner_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("parent_typed_signature_certificate_derived=false")
    print("finite_coupling_closure_register_created=true")
    print("valid_prediction_rows=0")


if __name__ == "__main__":
    main()
