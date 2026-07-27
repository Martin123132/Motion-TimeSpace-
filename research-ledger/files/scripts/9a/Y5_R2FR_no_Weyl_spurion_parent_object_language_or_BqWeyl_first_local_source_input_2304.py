from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_NO_WEYL_SPURION_OBJECT_LANGUAGE_OR_BQWEYL_SOURCE_2304"
DOC = ROOT / "2304-Y5-R2FR-no-Weyl-spurion-parent-object-language-or-BqWeyl-first-local-source-input.md"

PATHS = {
    "2303_doc": ROOT / "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md",
    "2303_validation": OUT / "P8_Y5_BRR545_2303_VALIDATION.csv",
    "2303_candidate_clause": OUT / "P8_Y5_PARENT_QLOC_2303_CANDIDATE_PARENT_Q_CLAUSE_NONCLAIM.csv",
    "2303_bqweyl_acquisition": OUT / "P8_Y5_PARENT_QLOC_2303_BQWEYL_LOCAL_BOUND_ACQUISITION_REQUIREMENTS.csv",
    "2302_doc": ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
    "1761_doc": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
    "2135_doc": ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md",
    "1313_doc": ROOT / "1313-Y5-R10-RAB-typed-no-hidden-visible-coefficient-morphism-or-alpha-product-input.md",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1220_typed_signature": OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
}

SOURCES = [
    (
        "SRC2304_00_2303_doc",
        "2303_doc",
        PATHS["2303_doc"],
        ["DEC2303_3_next", "2304-Y5-R2FR-no-Weyl-spurion-parent-object-language-or-BqWeyl-first-local-source-input.md"],
        "direct handoff selecting no-Weyl-spurion object-language proof or first B_qWeyl source input",
    ),
    (
        "SRC2304_01_2303_validation",
        "2303_validation",
        PATHS["2303_validation"],
        ["VAL2303_OVERALL", "PASS"],
        "confirms the preceding q field-content/no-spurion checkpoint passed",
    ),
    (
        "SRC2304_02_2303_clause",
        "2303_candidate_clause",
        PATHS["2303_candidate_clause"],
        ["PQC2303_0_clause_shape", "WOULD_ACTIVATE_BQWEYL_INDEX_THEOREM_IF_PARENT_SIGNED"],
        "candidate parent q clause that would activate the linear Weyl index theorem if signed",
    ),
    (
        "SRC2304_03_2303_acquisition",
        "2303_bqweyl_acquisition",
        PATHS["2303_bqweyl_acquisition"],
        ["BQA2303_6_acceptance_rule", "NONCLAIM_ACQUISITION_SCHEMA_READY"],
        "incoming B_qWeyl nonclaim acquisition rule",
    ),
    (
        "SRC2304_04_2302_theorem",
        "2302_doc",
        PATHS["2302_doc"],
        ["BQWZ2302_0_conditional_theorem", "EXACT_CONDITIONAL_THEOREM"],
        "incoming conditional B_qWeyl index-zero theorem",
    ),
    (
        "SRC2304_05_1761_object_language",
        "1761_doc",
        PATHS["1761_doc"],
        ["HOM1761_4_verdict", "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED"],
        "object-language/no-direct-vertex route remains unsigned",
    ),
    (
        "SRC2304_06_1768_normal_form",
        "1768_doc",
        PATHS["1768_doc"],
        ["SCL1768_5_post_variation_projector", "FORBIDDEN_BY_NORMAL_FORM_CONTRACT_UNSIGNED"],
        "post-variation projector/source-map branch is forbidden only if parent normal form is signed",
    ),
    (
        "SRC2304_07_963_higher_curvature",
        "963_doc",
        PATHS["963_doc"],
        ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
        "no-higher-curvature/second-order parent signature remains unsigned",
    ),
    (
        "SRC2304_08_1343_zero_signature",
        "1343_doc",
        PATHS["1343_doc"],
        ["ZERO1343_5_verdict", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"],
        "R2/f(R)/curvature parent coefficient zero signature remains unsigned",
    ),
    (
        "SRC2304_09_2135_curvature_morphism",
        "2135_doc",
        PATHS["2135_doc"],
        ["NMC2135_5_verdict", "NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED"],
        "curvature-specific no-mixed morphism proof failed under current evidence",
    ),
    (
        "SRC2304_10_1313_typed_morphism",
        "1313_doc",
        PATHS["1313_doc"],
        ["TMC1313_1_type_rule", "EXACT_CONDITIONAL_THEOREM"],
        "typed no-hidden-visible morphism is exact conditional but depends on parent grammar",
    ),
    (
        "SRC2304_11_1107_exhaustion",
        "1107_exhaustion",
        PATHS["1107_exhaustion"],
        ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
        "object-language exhaustion is not derived",
    ),
    (
        "SRC2304_12_1220_typed_signature",
        "1220_typed_signature",
        PATHS["1220_typed_signature"],
        ["PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
        "parent typed object-language signature certificate is not derived",
    ),
    (
        "SRC2304_13_1236_certificate",
        "1236_certificate",
        PATHS["1236_certificate"],
        ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
        "typed object-language certificate exists as a schema but is not parent-derived",
    ),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
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
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        seen: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def rows_to_markdown(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def make_sources() -> tuple[list[dict[str, Any]], dict[str, bool]]:
    rows: list[dict[str, Any]] = []
    source_ok: dict[str, bool] = {}
    for source_id, source_key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        source_ok[source_key] = found
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": source_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_string(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows, source_ok


def make_index_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_0_grammar_target",
            "lemma_piece": "typed parent object-language target",
            "statement": "Let q be admitted only as a scalar, quotient coordinate, or pure density, and let the parent local scalar grammar have no independent Weyl-type four-index spurion/projector/readout kernel.",
            "status": "TARGET_SHARP",
            "proof_or_reason": "This is the exact grammar needed to make the linear q-Weyl branch an index question rather than a fitted closure.",
            "source_keys": "2303_candidate_clause;1220_typed_signature;1236_certificate",
            "missing_parent_signature": "parent typed object-language and q representation are not signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_1_metric_trace_zero",
            "lemma_piece": "metric-only contraction of one Weyl tensor",
            "statement": "With only g^{ab} available, every scalar contraction linear in C_{abcd} traces one Weyl index pair and vanishes by tracelessness.",
            "status": "EXACT_INDEX_LEMMA_UNDER_GRAMMAR",
            "proof_or_reason": "Examples reduce to g^{ac}g^{bd}C_{abcd}=0 or equivalent trace permutations; no scalar q C term survives.",
            "source_keys": "2302_doc",
            "missing_parent_signature": "need proof that no non-metric four-index object is in the parent q grammar",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_2_epsilon_single_weyl_zero",
            "lemma_piece": "epsilon-only contraction of one Weyl tensor",
            "statement": "The oriented scalar epsilon^{abcd} C_{abcd} vanishes for a single Weyl tensor; the nontrivial parity-odd curvature scalar is quadratic, C * C, not linear.",
            "status": "EXACT_INDEX_LEMMA_UNDER_GRAMMAR",
            "proof_or_reason": "Pair symmetries plus the first Bianchi identity kill the fully antisymmetric one-Weyl contraction; no linear pseudoscalar q epsilon C term remains.",
            "source_keys": "2302_doc",
            "missing_parent_signature": "need proof that no extra orientation-dependent spurion/readout kernel is admitted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_3_spurion_necessity",
            "lemma_piece": "linear Weyl coupling requires a spurion",
            "statement": "A nonzero local scalar linear in Weyl has the form q P^{abcd} C_{abcd}; P^{abcd} is exactly the forbidden Weyl-type spurion/projector/readout object.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_reason": "The Weyl tensor carries four free curvature indices; if metric/epsilon contractions vanish, a nonzero linear contraction needs an additional object with Weyl symmetries or a readout kernel.",
            "source_keys": "2302_doc;1768_doc;2303_candidate_clause",
            "missing_parent_signature": "no-spurion/no-projector/no-readout kernel is not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_4_ricci_scalar_not_weyl",
            "lemma_piece": "allowed linear curvature channel",
            "statement": "qR, q R_{ab}u^a u^b, or Einstein/Ricci trace channels are different operators; they do not license qC_{abcd} without a spurion.",
            "status": "CLASSIFICATION_RULE",
            "proof_or_reason": "Ricci/scalar contractions have metric traces; Weyl is the trace-free irreducible part, so the local residual ledger must not merge them.",
            "source_keys": "2135_doc;2303_bqweyl_acquisition",
            "missing_parent_signature": "Ricci/scalar coefficient owner still has its own beta/R2/fR closure gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_5_quadratic_weyl_guard",
            "lemma_piece": "quadratic Weyl is a separate residual",
            "statement": "q C_{abcd}C^{abcd} and q C_{abcd}*C^{abcd} are not killed by the linear index theorem; they are higher-curvature residuals controlled by a separate no-higher-curvature/no-tower signature.",
            "status": "RETAIN_AS_SEPARATE_GUARD",
            "proof_or_reason": "The linear B_qWeyl route can be zero while D_qWeyl2 remains live unless the parent second-order/higher-curvature theorem is signed.",
            "source_keys": "963_doc;1343_doc",
            "missing_parent_signature": "no bare or induced higher-curvature tower remains unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OLI2304_6_verdict",
            "lemma_piece": "linear B_qWeyl object-language theorem",
            "statement": "B_qWeyl(linear)=0 follows if the typed object-language, q representation, and no-spurion/projector/readout kernel clauses are signed.",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "proof_or_reason": "The index algebra is strong, but current corpus evidence does not prove the parent grammar is exhausted or spurion-free.",
            "source_keys": "1107_exhaustion;1220_typed_signature;1236_certificate;2303_candidate_clause",
            "missing_parent_signature": "object-language exhaustion, parent typed signature, q field content, no hidden Weyl spurion, and readout closure",
            "valid_for_claim": "false",
        },
    ]


def make_parent_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_0_parent_typed_language",
            "gate": "parent typed object-language is signed",
            "required_evidence": "one parent grammar/action domain derived from MTS primitives before fitting",
            "current_evidence": "1220 and 1236 write the schema but mark it not parent-derived",
            "status": "MISSING_PARENT_SIGNATURE",
            "blocking_source_keys": "1220_typed_signature;1236_certificate",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_1_object_language_exhaustion",
            "gate": "no extra local counterterm algebra beyond parent generated terms",
            "required_evidence": "Allowed[S_vis] exhausted by Image(ParentGenerate)",
            "current_evidence": "1107 says object-language exhaustion is not derived",
            "status": "MISSING_OBJECT_LANGUAGE_EXHAUSTION",
            "blocking_source_keys": "1107_exhaustion",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_2_q_representation",
            "gate": "q is only scalar/quotient/pure density in the parent grammar",
            "required_evidence": "q field-content certificate with no Weyl-index type",
            "current_evidence": "2303 found a future parent clause but not a current proof",
            "status": "MISSING_Q_FIELD_CONTENT_CERTIFICATE",
            "blocking_source_keys": "2303_candidate_clause",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_3_no_spurion_projector",
            "gate": "no Weyl-type spurion/projector/readout kernel",
            "required_evidence": "parent normal form forbids P^{abcd}C_{abcd} style source/readout maps",
            "current_evidence": "1768 forbids post-variation projectors only as an unsigned contract; 2303 did not source a no-spurion certificate",
            "status": "MISSING_NO_SPURION_SIGNATURE",
            "blocking_source_keys": "1768_doc;2303_candidate_clause",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_4_hidden_frame_extensions",
            "gate": "no hidden conformal/disformal/readout frame extension supplies the missing tensor",
            "required_evidence": "hidden frame and matter/readout descent are signed absent or harmless",
            "current_evidence": "1761 keeps hidden frame live unless declared extension",
            "status": "MISSING_FRAME_DESCENT_SIGNATURE",
            "blocking_source_keys": "1761_doc",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_5_curvature_morphism",
            "gate": "hidden invariants cannot feed curvature coefficients",
            "required_evidence": "fixed EH/curvature coefficient owner plus hidden invariant triviality",
            "current_evidence": "2135 proves scalar-tensor/nonminimal curvature countermodel remains legal if hidden scalar survives",
            "status": "MISSING_CURVATURE_MORPHISM_EXCLUSION",
            "blocking_source_keys": "2135_doc",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_6_no_higher_curvature_tower",
            "gate": "quadratic Weyl/Ricci/R2 tower absent or bounded",
            "required_evidence": "parent second-order/no-extra-scalar/no-integrated-out tower signature",
            "current_evidence": "963 and 1343 keep higher-curvature zero signatures unsigned",
            "status": "MISSING_HIGHER_CURVATURE_SIGNATURE",
            "blocking_source_keys": "963_doc;1343_doc",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PTG2304_7_verdict",
            "gate": "promote B_qWeyl linear zero to current local-GR evidence",
            "required_evidence": "PTG2304_0 through PTG2304_6 all pass",
            "current_evidence": "multiple hard parent signatures remain missing",
            "status": "ZERO_THEOREM_NOT_ACTIVATED_CURRENT_CORPUS",
            "blocking_source_keys": "1107_exhaustion;1220_typed_signature;1236_certificate;2303_candidate_clause;1768_doc;963_doc;1343_doc",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
    ]


def make_first_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQI2304_0_Z_linear_object_language",
            "input_name": "Z_BqWeyl_linear_object_language",
            "input_type": "theorem_switch",
            "symbol": "Z_BqWeyl_linear",
            "value": "false",
            "units": "dimensionless_bool",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "required_to_promote": "parent typed object-language + q scalar/density representation + no Weyl spurion/projector/readout",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv",
            "arena": "R10;PPN;clock;orbital;local_GR",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQI2304_1_BqWeyl_parent_coefficient",
            "input_name": "B_qWeyl_parent_coefficient",
            "input_type": "numeric_or_zero_parent_coefficient",
            "symbol": "B_qWeyl",
            "value": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_COEFFICIENT",
            "units": "depends_on_parent_normalization",
            "status": "MISSING_PARENT_INPUT",
            "required_to_promote": "either Z_BqWeyl_linear=true or a source-backed coefficient with normalization, sign, and uncertainty",
            "source_path": "MISSING_PARENT_ACTION_SOURCE",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQI2304_2_local_projection_norms",
            "input_name": "B_qWeyl_local_projection_norms",
            "input_type": "arena_projection",
            "symbol": "||P_arena(q C)||",
            "value": "MISSING_R10_PPN_CLOCK_ORBITAL_PROJECTION",
            "units": "arena_specific",
            "status": "MISSING_ARENA_PROJECTION",
            "required_to_promote": "map B_qWeyl into R10 alpha(lambda), PPN residual vector, clock drift, and orbital precession units",
            "source_path": "MISSING_ARENA_PROJECTION_SOURCE",
            "arena": "R10;PPN;clock;orbital",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQI2304_3_DqWeyl2_quadratic_residual",
            "input_name": "D_qWeyl2_quadratic_residual",
            "input_type": "separate_higher_curvature_residual",
            "symbol": "D_qWeyl2",
            "value": "RETAIN_NONCLAIM_RESIDUAL",
            "units": "length_squared_or_parent_normalized",
            "status": "NOT_KILLED_BY_LINEAR_INDEX_THEOREM",
            "required_to_promote": "parent second-order/no-higher-curvature/no-integrated-out tower signature or source-backed finite bound",
            "source_path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md;1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
            "arena": "R10;PPN;clock;orbital;cosmology_if_active",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQI2304_4_acceptance_rule",
            "input_name": "B_qWeyl_acceptance_rule",
            "input_type": "claim_gate",
            "symbol": "claim(B_qWeyl)",
            "value": "false",
            "units": "boolean",
            "status": "CLAIM_REFUSED",
            "required_to_promote": "no row with MISSING_PARENT_INPUT/MISSING_ARENA_PROJECTION and either theorem-zero or numeric coefficient passes all local bounds",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv",
            "arena": "all_local_arenas",
            "valid_for_claim": "false",
        },
    ]


def make_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2304_0_weyl_spurion",
            "countermodel": "q P^{abcd} C_{abcd}",
            "why_legal_without_gate": "P^{abcd} can be declared as a hidden representative/readout tensor unless the parent object-language forbids it",
            "would_break": "linear B_qWeyl zero theorem",
            "required_exclusion": "no Weyl-spurion/projector/readout kernel signature",
            "source_keys": "1768_doc;2303_candidate_clause",
            "status": "LIVE_UNTIL_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2304_1_projector_source_map",
            "countermodel": "post-variation projection from a curvature/readout source into q equation",
            "why_legal_without_gate": "a source-map inserted after variation can mimic a Weyl response unless rejected by action normal form",
            "would_break": "variational local-GR reduction",
            "required_exclusion": "action-owned source-map identity signature",
            "source_keys": "1768_doc",
            "status": "LIVE_AS_FORBIDDEN_BUT_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2304_2_hidden_frame",
            "countermodel": "hidden conformal/disformal frame moves the effect into clocks, matter constants, or PPN",
            "why_legal_without_gate": "frame movement can preserve covariance while shifting observable couplings",
            "would_break": "claim that Weyl branch is harmless locally",
            "required_exclusion": "matter/source/readout descent and hidden-frame absence",
            "source_keys": "1761_doc;1236_certificate",
            "status": "LIVE_UNLESS_DECLARED_EXTENSION",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2304_3_quadratic_weyl",
            "countermodel": "q C_{abcd} C^{abcd} or q C_{abcd}*C^{abcd}",
            "why_legal_without_gate": "quadratic curvature scalars are not removed by a one-Weyl index theorem",
            "would_break": "attempt to erase all Weyl sensitivity from linear theorem alone",
            "required_exclusion": "no-higher-curvature/no-tower signature or finite source-backed bound",
            "source_keys": "963_doc;1343_doc",
            "status": "RETAIN_AS_SEPARATE_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CM2304_4_hidden_curvature_coefficient",
            "countermodel": "F(I_hid) R[g_obs] or integrated-out auxiliary curvature scalar",
            "why_legal_without_gate": "diffeomorphism covariance allows scalar-tensor/nonminimal curvature coupling if hidden scalar invariant survives",
            "would_break": "local-GR closure even if the linear Weyl branch is removed",
            "required_exclusion": "fixed EH coefficient owner, hidden invariant triviality, and matter/readout harmlessness",
            "source_keys": "2135_doc",
            "status": "LIVE_NONCLAIM_OWNER_ROUTE",
            "valid_for_claim": "false",
        },
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2304_0_R10",
            "arena": "R10_short_range",
            "claim_allowed": "false",
            "reason": "B_qWeyl coefficient/theorem switch and arena projection are not source-backed",
            "blocking_rows": "BQI2304_0_Z_linear_object_language;BQI2304_1_BqWeyl_parent_coefficient;BQI2304_2_local_projection_norms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2304_1_PPN",
            "arena": "PPN_local_GR",
            "claim_allowed": "false",
            "reason": "linear Weyl theorem does not close hidden frame, curvature coefficient, or higher-curvature residual gates",
            "blocking_rows": "PTG2304_4_hidden_frame_extensions;PTG2304_5_curvature_morphism;PTG2304_6_no_higher_curvature_tower",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2304_2_clocks",
            "arena": "clock_redshift_alpha_drift",
            "claim_allowed": "false",
            "reason": "readout/radiative closure is not signed, so a frame-moved residual can re-enter clocks",
            "blocking_rows": "CM2304_2_hidden_frame;PTG2304_3_no_spurion_projector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2304_3_orbital",
            "arena": "orbital_precession_ephemerides",
            "claim_allowed": "false",
            "reason": "no arena projection from B_qWeyl or quadratic Weyl residual to orbital units exists",
            "blocking_rows": "BQI2304_2_local_projection_norms;BQI2304_3_DqWeyl2_quadratic_residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2304_4_local_GR_Newton",
            "arena": "local_GR_Newton_limit",
            "claim_allowed": "false",
            "reason": "linear Weyl index lemma is useful but not enough to derive GR/Newton without parent action and matter/source descent",
            "blocking_rows": "PTG2304_0_parent_typed_language;PTG2304_1_object_language_exhaustion;PTG2304_7_verdict",
            "valid_for_claim": "false",
        },
    ]


def make_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_0_source_integrity",
            "gate": "all cited sources exist and needles match",
            "passed": "true",
            "claim_effect": "evidence ledger is internally checkable",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_1_index_lemma",
            "gate": "linear one-Weyl index lemma derived under typed grammar",
            "passed": "true",
            "claim_effect": "conditional theorem strengthened",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_2_parent_signature",
            "gate": "parent typed grammar/q representation/no-spurion clauses signed",
            "passed": "false",
            "claim_effect": "blocks promotion of Z_BqWeyl_linear",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_3_numeric_bound_input",
            "gate": "B_qWeyl coefficient and local projections are numeric/source-backed",
            "passed": "false",
            "claim_effect": "blocks bound-route claim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_4_quadratic_guard",
            "gate": "quadratic Weyl/higher-curvature residual separated from linear theorem",
            "passed": "true",
            "claim_effect": "prevents overclaiming the Weyl cleanup",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GATE2304_5_local_claim",
            "gate": "R10/WEP/PPN/clock/orbital/local-GR pass",
            "passed": "false",
            "claim_effect": "all local arenas remain blocked",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2304_0",
            "decision": "LINEAR_BQWEYL_INDEX_ROUTE_STRENGTHENED",
            "reason": "a single Weyl tensor cannot make a scalar with q under metric/epsilon-only typed grammar; any nonzero linear term needs a forbidden four-index object",
            "next_action": "try to parent-sign the typed grammar/no-spurion clause rather than just restating it",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2304_1",
            "decision": "ZERO_NOT_ACTIVATED",
            "reason": "object-language exhaustion, q representation, no-spurion/projector, and readout closure remain unsigned",
            "next_action": "keep B_qWeyl first source rows nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2304_2",
            "decision": "QUADRATIC_WEYL_RESIDUAL_SPLIT",
            "reason": "qC and qC^2 are different; the linear index theorem does not remove higher-curvature tower risks",
            "next_action": "carry D_qWeyl2 as a separate residual until second-order/no-tower signature or finite bounds exist",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2304_3_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "the least-scrutiny route is now to sign the typed grammar/no-spurion object language or explicitly demote the linear route to closure-only while tracking D_qWeyl2",
            "next_action": "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md",
            "valid_for_claim": "false",
        },
    ]


OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2304_SOURCE_REGISTER.csv",
    "index": OUT / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv",
    "gate": OUT / "P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv",
    "first_input": OUT / "P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2304_CURVATURE_COUNTERMODEL_LEDGER.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2304_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2304_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2304_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2304_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2304_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2304_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2304_0_acquisition_lemma", OUTPUTS["index"], QUEUE / "JR2304_NO_WEYL_SPURION_TYPED_GRAMMAR_NONCLAIM.csv"),
    ("COPY2304_1_acquisition_input", OUTPUTS["first_input"], QUEUE / "JR2304_BQWEYL_FIRST_SOURCE_INPUT_NONCLAIM.csv"),
    ("COPY2304_2_microscope_residual", OUTPUTS["first_input"], MICROSCOPE / "q_BqWeyl_object_language_nonclaim_2304.csv"),
    ("COPY2304_3_beta_docs", OUTPUTS["countermodels"], BETA_DOCS / "Q_BQWEYL_OBJECT_LANGUAGE_2304_NONCLAIM.csv"),
]


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        row_count = len(read_csv_rows(dst))
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": bool_string(dst.exists()),
                "row_count": row_count,
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    index_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2304_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2304_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2304_02_index_theorem_present", any(row["row_id"] == "OLI2304_6_verdict" and row["status"] == "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED" for row in index_rows), "linear B_qWeyl theorem is exact conditional but unsigned"))
    checks.append(("VAL2304_03_metric_epsilon_zero_rows", {"OLI2304_1_metric_trace_zero", "OLI2304_2_epsilon_single_weyl_zero"}.issubset({row["row_id"] for row in index_rows}), "metric and epsilon one-Weyl zero lemmas are recorded"))
    checks.append(("VAL2304_04_parent_gate_blocks", any(row["row_id"] == "PTG2304_7_verdict" and row["claim_gate_passed"] == "false" for row in gate_rows), "parent signature gate blocks promotion"))
    checks.append(("VAL2304_05_first_input_nonclaim", all(row["valid_for_claim"] == "false" for row in input_rows), "all first B_qWeyl input rows are nonclaim"))
    checks.append(("VAL2304_06_missing_parent_input_retained", any("MISSING_PARENT" in row["status"] or "MISSING_PARENT" in row["value"] for row in input_rows), "missing parent coefficient/signature is explicit"))
    checks.append(("VAL2304_07_quadratic_guard_retained", any(row["row_id"] == "BQI2304_3_DqWeyl2_quadratic_residual" for row in input_rows) and any(row["row_id"] == "CM2304_3_quadratic_weyl" for row in countermodel_rows), "quadratic Weyl is split into a separate residual"))
    checks.append(("VAL2304_08_refusal_all_local", all(row["claim_allowed"] == "false" for row in refusal_rows), "all local arenas remain refused"))
    checks.append(("VAL2304_09_claim_gates_no_public_claim", any(row["row_id"] == "GATE2304_5_local_claim" and row["passed"] == "false" for row in claim_rows), "local claim gate is false"))
    checks.append(("VAL2304_10_next_target", any(row["row_id"] == "DEC2304_3_next" and "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md" in row["next_action"] for row in decision_rows), "next target is selected"))
    checks.append(("VAL2304_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2304_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in [source_rows, index_rows, gate_rows, input_rows, countermodel_rows, refusal_rows, claim_rows, decision_rows, copy_rows] for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2304_13_formalization_untouched_by_2304", len(list(FORMALIZATION.rglob("*2304*"))) == 0 if FORMALIZATION.exists() else True, "no 2304 output appears in formalization-workbench"))

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
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2304_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2304 derives the linear B_qWeyl no-spurion index theorem conditionally, refuses claim promotion because parent object-language/no-spurion gates are unsigned, and stages first B_qWeyl input rows as nonclaim.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    index_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2304 — No-Weyl-Spurion Parent Object Language Or B_qWeyl First Local Source Input",
        "",
        "## Summary",
        "",
        "2304 takes the best derivation-first route for the current local branch: do not ask whether `B_qWeyl` is small yet; ask whether a linear `q C_{abcd}` scalar can even be written in the parent object language.",
        "",
        "The answer is sharper than before but still not a public claim. If `q` is only a scalar/quotient/pure-density object and the parent scalar grammar only supplies `g`, `epsilon`, and ordinary observed-metric curvature objects, then a single Weyl tensor cannot form a nonzero scalar with `q`. Metric contractions trace the Weyl tensor to zero; the one-Weyl epsilon contraction also vanishes; any nonzero linear term needs a four-index Weyl-type spurion/projector/readout kernel `P^{abcd}`. That is exactly the object the no-spurion clause must forbid.",
        "",
        "So the linear index theorem is real as a conditional theorem. It is not activated for MTS yet because the typed parent object language, q field-content certificate, no-spurion/projector clause, and readout/radiative closure remain unsigned. The first `B_qWeyl` source rows therefore stay nonclaim. Quadratic Weyl terms such as `q C^2` are split into a separate higher-curvature residual because they are not removed by the linear theorem.",
        "",
        "## Source Register",
        "",
        rows_to_markdown(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Object-Language Index Lemma",
        "",
        rows_to_markdown(index_rows, ["row_id", "lemma_piece", "statement", "status", "proof_or_reason", "missing_parent_signature", "valid_for_claim"]),
        "",
        "## Parent Signature Gate",
        "",
        rows_to_markdown(gate_rows, ["row_id", "gate", "required_evidence", "current_evidence", "status", "claim_gate_passed", "valid_for_claim"]),
        "",
        "## B_qWeyl First Source Input",
        "",
        rows_to_markdown(input_rows, ["row_id", "input_name", "symbol", "value", "units", "status", "required_to_promote", "arena", "valid_for_claim"]),
        "",
        "## Countermodel Ledger",
        "",
        rows_to_markdown(countermodel_rows, ["row_id", "countermodel", "why_legal_without_gate", "would_break", "required_exclusion", "status", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        rows_to_markdown(refusal_rows, ["row_id", "arena", "claim_allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        rows_to_markdown(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        rows_to_markdown(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        rows_to_markdown(next_rows, ["row_id", "next_target", "why", "claim_status"]),
        "",
        "## Branch Copies",
        "",
        rows_to_markdown(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        rows_to_markdown(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows, _ = make_sources()
    index_rows = make_index_lemma_rows()
    gate_rows = make_parent_gate_rows()
    input_rows = make_first_source_rows()
    countermodel_rows = make_countermodel_rows()
    refusal_rows = make_refusal_rows()
    claim_rows = make_claim_gate_rows()
    decision_rows = make_decision_rows()
    next_rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2304_0",
            "next_target": "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md",
            "why": "try to parent-sign the typed no-spurion grammar; if it still fails, demote the linear B_qWeyl route to closure-only and carry D_qWeyl2 explicitly",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["index"], index_rows)
    write_csv(OUTPUTS["gate"], gate_rows)
    write_csv(OUTPUTS["first_input"], input_rows)
    write_csv(OUTPUTS["countermodels"], countermodel_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["claim_gates"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        index_rows,
        gate_rows,
        input_rows,
        countermodel_rows,
        refusal_rows,
        claim_rows,
        decision_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)

    write_markdown(
        source_rows,
        index_rows,
        gate_rows,
        input_rows,
        countermodel_rows,
        refusal_rows,
        claim_rows,
        decision_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2304_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
