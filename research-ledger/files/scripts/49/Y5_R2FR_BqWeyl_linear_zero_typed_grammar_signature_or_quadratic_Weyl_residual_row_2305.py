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

BRANCH_ID = "MTS_R2FR_BQWEYL_TYPED_GRAMMAR_OR_DQWEYL2_2305"
DOC = ROOT / "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md"

PATHS = {
    "2304_doc": ROOT / "2304-Y5-R2FR-no-Weyl-spurion-parent-object-language-or-BqWeyl-first-local-source-input.md",
    "2304_validation": OUT / "P8_Y5_BRR545_2304_VALIDATION.csv",
    "2304_index": OUT / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv",
    "2304_gate": OUT / "P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv",
    "2304_input": OUT / "P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv",
    "2304_next": OUT / "P8_Y5_PARENT_QLOC_2304_NEXT_TARGET.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1220_typed_signature": OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1114_no_hidden_visible": OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
    "1114_obstructions": OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
    "1055_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1055_decision": OUT / "P8_Y5_R10_1055_DECISION_LEDGER.csv",
    "1058_exhaustion": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1066_object_typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1065_parent_grammar": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "1235_requirements": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
    "1235_unique_f2": OUT / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
    "1761_doc": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "2132_no_tower": OUT / "P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv",
    "963_doc": ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
    "2301_representation": OUT / "P8_Y5_PARENT_QLOC_2301_Q_REPRESENTATION_TYPE_GATE.csv",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "2254_bweyl": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
}

SOURCES = [
    ("SRC2305_00_2304_doc", "2304_doc", PATHS["2304_doc"], ["DEC2304_3_next", "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md"], "direct 2304 handoff"),
    ("SRC2305_01_2304_validation", "2304_validation", PATHS["2304_validation"], ["VAL2304_OVERALL", "PASS"], "2304 validation"),
    ("SRC2305_02_2304_index", "2304_index", PATHS["2304_index"], ["OLI2304_6_verdict", "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"], "linear one-Weyl index theorem"),
    ("SRC2305_03_2304_gate", "2304_gate", PATHS["2304_gate"], ["PTG2304_7_verdict", "ZERO_THEOREM_NOT_ACTIVATED_CURRENT_CORPUS"], "parent signature gate from 2304"),
    ("SRC2305_04_2304_input", "2304_input", PATHS["2304_input"], ["BQI2304_3_DqWeyl2_quadratic_residual", "NOT_KILLED_BY_LINEAR_INDEX_THEOREM"], "quadratic Weyl residual handoff"),
    ("SRC2305_05_2304_next", "2304_next", PATHS["2304_next"], ["2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md"], "next target csv"),
    ("SRC2305_06_1236_certificate", "1236_certificate", PATHS["1236_certificate"], ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"], "typed object-language certificate is schema only"),
    ("SRC2305_07_1220_typed_signature", "1220_typed_signature", PATHS["1220_typed_signature"], ["PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"], "typed signature not derived"),
    ("SRC2305_08_1107_exhaustion", "1107_exhaustion", PATHS["1107_exhaustion"], ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"], "object-language exhaustion not derived"),
    ("SRC2305_09_1114_no_hidden_visible", "1114_no_hidden_visible", PATHS["1114_no_hidden_visible"], ["NHV1114_6_verdict", "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED"], "no-hidden-visible theorem not derived"),
    ("SRC2305_10_1114_obstructions", "1114_obstructions", PATHS["1114_obstructions"], ["OBS1114_0_grammar", "typed parent object language not signed"], "active grammar obstruction"),
    ("SRC2305_11_1055_contract", "1055_contract", PATHS["1055_contract"], ["PAC1055_6_single_parent_action", "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS"], "single-parent-action contract is written not derived"),
    ("SRC2305_12_1055_decision", "1055_decision", PATHS["1055_decision"], ["DEC1055_1_not_derivation_yet", "cannot claim WEP/R10/local-GR pass"], "contract cannot claim local-GR pass"),
    ("SRC2305_13_1058_exhaustion", "1058_exhaustion", PATHS["1058_exhaustion"], ["VOE1058_3_no_hidden_visible_hom", "BLOCKED_BY_SCALAR_OBSTRUCTION"], "hidden-visible hom blocked by scalar obstruction"),
    ("SRC2305_14_1066_operator_domain", "1066_operator_domain", PATHS["1066_operator_domain"], ["ODR1066_4_verdict", "EXACT_RULE_NOT_DERIVED"], "operator-domain rule not derived"),
    ("SRC2305_15_1066_object_typing", "1066_object_typing", PATHS["1066_object_typing"], ["OLT1066_6_verdict", "conditional_not_parent_derived"], "object-language typing conditional"),
    ("SRC2305_16_1066_source_scalar", "1066_source_scalar", PATHS["1066_source_scalar"], ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"], "source-scalar exclusion not parent-derived"),
    ("SRC2305_17_1065_parent_grammar", "1065_parent_grammar", PATHS["1065_parent_grammar"], ["PGG1065_5_verdict", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"], "parent grammar not signed"),
    ("SRC2305_18_1235_requirements", "1235_requirements", PATHS["1235_requirements"], ["TREQ1235_4_readout_radiative_closure", "READOUT_RADIATIVE_CLOSURE_UNSIGNED"], "typed-domain requirements remain unsigned"),
    ("SRC2305_19_1235_unique_f2", "1235_unique_f2", PATHS["1235_unique_f2"], ["UF21235_7_verdict", "UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL"], "analogous EM typed-domain demotion"),
    ("SRC2305_20_1761_doc", "1761_doc", PATHS["1761_doc"], ["SP1761_4_hidden_frame", "LIVE_UNLESS_DECLARED_EXTENSION"], "hidden frame extension remains live"),
    ("SRC2305_21_1768_doc", "1768_doc", PATHS["1768_doc"], ["SCL1768_5_post_variation_projector", "FORBIDDEN_BY_NORMAL_FORM_CONTRACT_UNSIGNED"], "source projector forbidden only by unsigned normal form"),
    ("SRC2305_22_2132_no_tower", "2132_no_tower", PATHS["2132_no_tower"], ["NT2132_5_verdict", "NO_TOWER_THEOREM_NOT_DERIVED"], "integrated higher-curvature tower not excluded"),
    ("SRC2305_23_963_doc", "963_doc", PATHS["963_doc"], ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"], "parent second-order signature not signed"),
    ("SRC2305_24_1343_doc", "1343_doc", PATHS["1343_doc"], ["ZERO1343_5_verdict", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"], "higher-curvature coefficient zero signature not derived"),
    ("SRC2305_25_2301_representation", "2301_representation", PATHS["2301_representation"], ["QREP2301_5_verdict", "FAIL_CURRENT_CLAIM"], "q representation certificate not signed"),
    ("SRC2305_26_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_0_BqWeyl", "MISSING_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BOUND"], "B_qWeyl residual exists from earlier split"),
    ("SRC2305_27_2254_bweyl", "2254_bweyl", PATHS["2254_bweyl"], ["WZ2254_4_verdict", "ZERO_THEOREM_NOT_ACTIVATED"], "R_AB Weyl precedent"),
]


OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2305_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_2305_TYPED_NO_SPURION_SIGNATURE_ATTEMPT.csv",
    "demotion": OUT / "P8_Y5_PARENT_QLOC_2305_LINEAR_BQWEYL_DEMOTION_LEDGER.csv",
    "closure": OUT / "P8_Y5_PARENT_QLOC_2305_CLOSURE_CONTRACT_CANDIDATE.csv",
    "quadratic": OUT / "P8_Y5_PARENT_QLOC_2305_QUADRATIC_WEYL_RESIDUAL_ROW.csv",
    "impact": OUT / "P8_Y5_PARENT_QLOC_2305_LOCAL_GR_IMPACT_MATRIX.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2305_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2305_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2305_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2305_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2305_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2305_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2305_0_signature_attempt", OUTPUTS["signature"], QUEUE / "JR2305_BQWEYL_TYPED_NO_SPURION_SIGNATURE_ATTEMPT_NONCLAIM.csv"),
    ("COPY2305_1_quadratic_residual", OUTPUTS["quadratic"], QUEUE / "JR2305_DQWEYL2_QUADRATIC_RESIDUAL_NONCLAIM.csv"),
    ("COPY2305_2_microscope_residual", OUTPUTS["quadratic"], MICROSCOPE / "q_DqWeyl2_quadratic_residual_nonclaim_2305.csv"),
    ("COPY2305_3_beta_docs", OUTPUTS["demotion"], BETA_DOCS / "BQWEYL_LINEAR_DEMOTION_2305_NONCLAIM.csv"),
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
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def b(value: bool) -> str:
    return "true" if value else "false"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(clean(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    )


def make_sources() -> list[dict[str, Any]]:
    rows = []
    for row_id, key, path, needles, role in SOURCES:
        ok, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needles": ";".join(needles),
                "needles_found": b(ok),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def make_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_0_target",
            "clause": "typed no-Weyl-spurion parent grammar",
            "statement": "Parent action grammar contains q only as scalar/quotient/pure-density data and contains no four-index Weyl-type spurion, projector, or readout kernel.",
            "attempt_result": "TARGET_SHARP",
            "evidence": "2304 writes the exact index theorem this would activate.",
            "missing_piece": "derive the grammar from MTS primitives rather than adopt it as a discipline contract",
            "source_keys": "2304_index;1236_certificate",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_1_linear_zero_if_signed",
            "clause": "linear B_qWeyl zero",
            "statement": "If the TGS2305_0 grammar is parent-signed, metric and epsilon contractions of one Weyl tensor vanish and any nonzero qC term needs a forbidden P^{abcd}.",
            "attempt_result": "EXACT_CONDITIONAL_THEOREM",
            "evidence": "OLI2304_1 through OLI2304_6.",
            "missing_piece": "parent signature, not index algebra",
            "source_keys": "2304_index;2254_bweyl",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_2_parent_object_language",
            "clause": "one parent object language before fitting",
            "statement": "Visible operator/coefficient domains must be fixed by one parent variational object before source/readout fitting.",
            "attempt_result": "SCHEMA_PRESENT_NOT_DERIVED",
            "evidence": "1055, 1220, and 1236 all write the schema but mark it not parent-derived.",
            "missing_piece": "primitive derivation of sorts, coefficient domains, and action ownership",
            "source_keys": "1055_contract;1220_typed_signature;1236_certificate",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_3_exhaustion",
            "clause": "object-language exhaustion",
            "statement": "Allowed local counterterm algebra is exhausted by Image(ParentGenerate); no hidden/manual Weyl source term can be appended.",
            "attempt_result": "NOT_DERIVED",
            "evidence": "1107 and 1058 explicitly keep exhaustion as a contract, not a theorem.",
            "missing_piece": "construct ParentGenerate from MTS primitives and prove no extra local scalar algebra",
            "source_keys": "1107_exhaustion;1058_exhaustion",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_4_no_hidden_visible_morphism",
            "clause": "no hidden-visible coefficient morphism",
            "statement": "Hidden invariant data cannot be an argument of visible curvature/source/readout coefficients.",
            "attempt_result": "EXACT_IF_TYPED_NOT_DERIVED",
            "evidence": "1114 gives the clean typed/product theorem but scalar obstruction survives without the parent grammar.",
            "missing_piece": "hidden invariant algebra triviality, no-extension rule, or parent typed coefficient domain",
            "source_keys": "1114_no_hidden_visible;1114_obstructions;1235_requirements",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_5_action_owned_projection",
            "clause": "no post-variation Weyl projector/readout insertion",
            "statement": "Any P^{abcd}C_{abcd} source must be an action-owned parent object, not a post-variation source map.",
            "attempt_result": "FORBIDDEN_BY_CONTRACT_UNSIGNED",
            "evidence": "1768 forbids post-variation projectors only under the unsigned parent normal-form contract.",
            "missing_piece": "parent normal-form signature with variation-before-readout",
            "source_keys": "1768_doc;1055_contract",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_6_readout_radiative_closure",
            "clause": "readout/radiative stability",
            "statement": "Loop matching, clocks, spectroscopy, Hodge/coframe, and reductions cannot regenerate hidden Weyl/source coefficient maps.",
            "attempt_result": "UNSIGNED_CRITICAL",
            "evidence": "1055, 1114, and 1235 repeatedly mark radiative/readout closure as required but not derived.",
            "missing_piece": "renormalized/readout closure theorem or retained finite priors",
            "source_keys": "1055_contract;1114_no_hidden_visible;1235_requirements",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TGS2305_7_verdict",
            "clause": "sign linear B_qWeyl typed grammar now",
            "statement": "Current corpus does not parent-sign the typed no-spurion grammar, so B_qWeyl(linear)=0 remains a closure candidate rather than a derived MTS result.",
            "attempt_result": "TYPED_NO_SPURION_GRAMMAR_NOT_PARENT_SIGNED",
            "evidence": "Every relevant prior source supports schema/conditional theorem status, not primitive derivation.",
            "missing_piece": "derive parent object language, q representation, no-spurion, no-extension, and readout closure from MTS primitives",
            "source_keys": "2304_gate;1236_certificate;1220_typed_signature;1107_exhaustion;1114_no_hidden_visible;1768_doc",
            "claim_gate_passed": "false",
            "valid_for_claim": "false",
        },
    ]


def make_demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEM2305_0_linear_route_status",
            "item": "linear B_qWeyl zero route",
            "decision": "DEMOTE_TO_CLOSURE_ONLY_UNTIL_PARENT_SIGNED",
            "reason": "the index theorem is strong but all parent object-language gates remain unsigned",
            "allowed_use": "private parent-action design target; not a local-GR/PPN/R10 pass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEM2305_1_future_activation",
            "item": "Z_BqWeyl_linear",
            "decision": "CAN_ACTIVATE_ONLY_IF_CLOSURE_CONTRACT_BECOMES_PARENT_THEOREM",
            "reason": "a signed grammar with no P^{abcd} object would make the linear Weyl coefficient syntactically absent",
            "allowed_use": "conditional theorem ledger and future parent-action checklist",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEM2305_2_numeric_fallback",
            "item": "B_qWeyl finite coefficient",
            "decision": "REQUIRES_SOURCE_BACKED_NUMERIC_BOUND_IF_CLOSURE_NOT_SIGNED",
            "reason": "a hidden spurion/projector/readout countermodel remains legal without the grammar signature",
            "allowed_use": "nonclaim acquisition row only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEM2305_3_public_language",
            "item": "public/local-GR wording",
            "decision": "BAN_CLAIM_LANGUAGE",
            "reason": "conditional zero plus unsigned closure is not evidence of a local-GR pass",
            "allowed_use": "say 'linear Weyl branch is controlled by a precise closure contract, not yet derived'",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEM2305_4_surviving_work",
            "item": "GR/Newton route",
            "decision": "MOVE_ATTENTION_TO_HIGHER_CURVATURE_AND_SOURCE_DESCENT",
            "reason": "even if linear B_qWeyl closes, D_qWeyl2, B_qRic, C_qT, matter/source/readout descent, and no-tower gates remain",
            "allowed_use": "next target selection",
            "valid_for_claim": "false",
        },
    ]


def make_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLOS2305_0_clause_header",
            "contract_clause": "BQWEYL_LINEAR_CLOSURE_CANDIDATE",
            "exact_text": "In the local parent action, q is scalar/quotient/pure-density data and the allowed local scalar density grammar contains no independent four-index Weyl-type object P^{abcd}; all source/readout maps are action-owned and preserve this typed domain.",
            "status": "CLOSURE_CANDIDATE_NOT_DERIVED",
            "would_imply": "B_qWeyl(linear)=0 by one-Weyl index theorem",
            "source_keys": "2304_index;1236_certificate;1768_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLOS2305_1_forbidden_objects",
            "contract_clause": "forbidden Weyl-index carriers",
            "exact_text": "Forbid hidden/background/projector/readout tensors with Weyl symmetries, e.g. P^{abcd}, P^{ab}{}_{cd}, material Weyl masks, boundary Weyl selectors, or tail kernels that contract a single C_{abcd}.",
            "status": "NEEDED_FOR_CLOSURE",
            "would_imply": "removes q P C and representative-dependent Weyl driving",
            "source_keys": "2301_representation;2304_gate;1768_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLOS2305_2_allowed_curvature",
            "contract_clause": "allowed linear curvature channels",
            "exact_text": "If any q-curvature channel remains, classify it as Ricci/scalar/Einstein-trace, not Weyl, and route it through B_qRic or C_qT ledgers.",
            "status": "CLASSIFICATION_RULE",
            "would_imply": "prevents silently using Ricci vacuum arguments to erase Weyl/tidal curvature",
            "source_keys": "2301_residuals;2304_input",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLOS2305_3_not_enough",
            "contract_clause": "closure does not prove full local GR",
            "exact_text": "This closure only handles the linear one-Weyl q source; it does not remove quadratic Weyl, R2/f(R), source trace, body/boundary, or matter/readout residuals.",
            "status": "OVERCLAIM_GUARD",
            "would_imply": "local GR/Newton remains blocked until other gates close",
            "source_keys": "2132_no_tower;963_doc;1343_doc;2301_residuals",
            "valid_for_claim": "false",
        },
    ]


def make_quadratic_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQW2305_0_DqWeyl2",
            "coefficient": "D_qWeyl2",
            "operator": "q C_{abcd} C^{abcd}",
            "why_retained": "quadratic Weyl scalar is not killed by the linear qC index theorem",
            "status": "NONCLAIM_RESIDUAL_ROW",
            "units": "length_squared_or_parent_normalized_pending_action_convention",
            "needed_inputs": "parent second-order/no-tower theorem OR numeric coefficient; q normalization; arena projection; source path",
            "arena": "PPN;orbital;local_GR;R10_if_projected;clock_if_readout_coupled",
            "source_keys": "2304_input;2132_no_tower;963_doc;1343_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQW2305_1_DqWeylDual",
            "coefficient": "D_qWeylDual",
            "operator": "q C_{abcd} *C^{abcd}",
            "why_retained": "parity-odd quadratic Weyl density is allowed by index algebra unless parity/orientation/object-language gates forbid it",
            "status": "NONCLAIM_RESIDUAL_ROW",
            "units": "length_squared_or_parent_normalized_pending_action_convention",
            "needed_inputs": "parity/orientation rule; parent coefficient; local projection; source path",
            "arena": "orbital;PPN_preferred-frame_or_parity;local_GR",
            "source_keys": "2304_index;963_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQW2305_2_no_tower_zero_route",
            "coefficient": "Z_DqWeyl2",
            "operator": "absence of quadratic Weyl tower",
            "why_retained": "would vanish if parent is strictly EH/second-order and no eliminated sector regenerates higher curvature",
            "status": "NO_TOWER_THEOREM_NOT_DERIVED",
            "units": "dimensionless_bool",
            "needed_inputs": "no bare Weyl2, no integrated-out scalar/projector/memory tower, radiative closure",
            "arena": "all_local_arenas",
            "source_keys": "2132_no_tower;963_doc;1343_doc",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQW2305_3_projection_norm",
            "coefficient": "Pi_DqWeyl2_arena",
            "operator": "projection of q C^2 into local observables",
            "why_retained": "without a projection norm, the residual cannot be compared to PPN, orbital, clock, or R10 data",
            "status": "MISSING_ARENA_PROJECTION",
            "units": "arena_specific",
            "needed_inputs": "Schwarzschild/exterior scaling, q Green function, source body cutoff, boundary/tail treatment",
            "arena": "PPN;orbital;clock;R10",
            "source_keys": "2304_refusal;2301_residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQW2305_4_total_status",
            "coefficient": "quadratic_Weyl_branch_claim",
            "operator": "all quadratic Weyl source effects",
            "why_retained": "linear B_qWeyl demotion does not address quadratic curvature",
            "status": "CLAIM_BLOCKED",
            "units": "boolean",
            "needed_inputs": "DQW2305_0 through DQW2305_3 resolved",
            "arena": "all_local_arenas",
            "source_keys": "all_above",
            "valid_for_claim": "false",
        },
    ]


def make_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "IMP2305_0_R10",
            "arena": "R10_short_range",
            "what_improves": "linear B_qWeyl has a precise closure theorem instead of vague handwaving",
            "still_missing": "numeric B_qWeyl or theorem-zero activation; D_qWeyl2 projection and coefficient",
            "claim_status": "BLOCKED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IMP2305_1_PPN",
            "arena": "PPN_local_GR",
            "what_improves": "dangerous exterior Weyl/tidal linear q drive is isolated",
            "still_missing": "B_qRic diagonalization, C_qT/source trace, quadratic Weyl, and matter/readout descent",
            "claim_status": "BLOCKED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IMP2305_2_orbital",
            "arena": "orbital_precession",
            "what_improves": "the source of tidal residuals is now named rather than blended with Ricci vacuum claims",
            "still_missing": "projection of D_qWeyl2 and any finite B_qWeyl into perihelion/ephemeris units",
            "claim_status": "BLOCKED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IMP2305_3_clocks",
            "arena": "clocks_alpha_readout",
            "what_improves": "readout/radiative closure is explicitly required for the grammar route",
            "still_missing": "proof that clock/spectroscopy reductions cannot regenerate hidden coefficient maps",
            "claim_status": "BLOCKED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "IMP2305_4_GR_Newton",
            "arena": "GR_to_Newton_limit",
            "what_improves": "we have narrowed one local vacuum residual to a closure-vs-bound choice",
            "still_missing": "parent EH/action derivation, source descent, no higher-curvature tower, Newtonian limit recovery",
            "claim_status": "BLOCKED_BUT_BETTER_PINNED",
            "valid_for_claim": "false",
        },
    ]


def make_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2305_0_linear_zero",
            "claim": "B_qWeyl(linear)=0 as MTS theorem",
            "allowed": "false",
            "reason": "typed no-spurion grammar is closure-only, not parent-derived",
            "blocking_rows": "TGS2305_7_verdict;DEM2305_0_linear_route_status",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2305_1_local_GR",
            "claim": "local GR/Newton pass",
            "allowed": "false",
            "reason": "linear Weyl cleanup does not close Ricci/source/trace/higher-curvature/matter descent gates",
            "blocking_rows": "CLOS2305_3_not_enough;DQW2305_4_total_status;IMP2305_4_GR_Newton",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2305_2_quadratic_zero",
            "claim": "D_qWeyl2=0",
            "allowed": "false",
            "reason": "no-tower/second-order/higher-curvature zero theorem is not derived",
            "blocking_rows": "DQW2305_2_no_tower_zero_route",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2305_3_bound_route",
            "claim": "finite Weyl residual passes local tests",
            "allowed": "false",
            "reason": "no source-backed coefficient, normalization, or arena projection exists",
            "blocking_rows": "DQW2305_0_DqWeyl2;DQW2305_3_projection_norm",
            "valid_for_claim": "false",
        },
    ]


def make_claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "2305 source-backed ledger is checkable", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_1_signature_attempt", "gate": "typed no-spurion grammar attempted", "passed": "true", "claim_effect": "we did the derivation attempt instead of skipping to closure", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_2_parent_signed", "gate": "typed no-spurion grammar parent-signed", "passed": "false", "claim_effect": "linear zero not promoted", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_3_closure_demoted", "gate": "linear route demoted to closure-only", "passed": "true", "claim_effect": "prevents circular local-GR claims", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_4_quadratic_residual", "gate": "D_qWeyl2 residual row staged", "passed": "true", "claim_effect": "next finite/theorem-zero task is explicit", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "GATE2305_5_local_pass", "gate": "R10/PPN/clock/orbital/local-GR pass", "passed": "false", "claim_effect": "all public local claims remain blocked", "valid_for_claim": "false"},
    ]


def make_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2305_0",
            "decision": "LINEAR_BQWEYL_ROUTE_DEMOTED_TO_CLOSURE_ONLY",
            "reason": "no current source parent-signs the typed no-spurion grammar; repeating the same gate would be circling",
            "next_action": "do not spend more turns on the linear Weyl zero unless new parent-action evidence appears",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2305_1",
            "decision": "QUADRATIC_WEYL_RESIDUAL_PROMOTED_TO_NEXT_REAL_TASK",
            "reason": "D_qWeyl2 is not addressed by the linear index theorem and is tied to the deeper second-order/no-tower route",
            "next_action": "derive no quadratic/higher-curvature tower or create first source-backed D_qWeyl2 bound row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2305_2",
            "decision": "LOCAL_GR_ROUTE_STATUS",
            "reason": "we are making progress by converting vague missing pieces into exact gates; still not local GR derived",
            "next_action": "attack the higher-curvature tower and source descent gates in the least-scrutiny order",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2305_3_next",
            "decision": "NEXT_TARGET_SELECTED",
            "reason": "after demoting the linear route, the clean next target is D_qWeyl2/no-tower rather than another no-spurion restatement",
            "next_action": "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md",
            "valid_for_claim": "false",
        },
    ]


def make_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2305_0",
            "next_target": "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md",
            "why": "linear B_qWeyl is now closure-only; quadratic Weyl/higher-curvature is the next live local-GR obstruction",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dst in BRANCH_COPY_SPECS:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": rel(src),
                "branch_copy_path": str(dst),
                "copy_exists": b(dst.exists()),
                "row_count": len(read_csv_rows(dst)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    quadratic_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, signature_rows, demotion_rows, closure_rows, quadratic_rows, impact_rows, refusal_rows, claim_rows, decision_rows, copy_rows]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2305_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited local source path exists"))
    checks.append(("VAL2305_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2305_02_signature_attempt_verdict", any(row["row_id"] == "TGS2305_7_verdict" and row["attempt_result"] == "TYPED_NO_SPURION_GRAMMAR_NOT_PARENT_SIGNED" for row in signature_rows), "typed no-spurion signature attempt has the expected unsigned verdict"))
    checks.append(("VAL2305_03_linear_demoted", any(row["row_id"] == "DEM2305_0_linear_route_status" and row["decision"] == "DEMOTE_TO_CLOSURE_ONLY_UNTIL_PARENT_SIGNED" for row in demotion_rows), "linear B_qWeyl route is demoted to closure-only"))
    checks.append(("VAL2305_04_closure_clause_written", any(row["row_id"] == "CLOS2305_0_clause_header" and "B_qWeyl(linear)=0" in row["would_imply"] for row in closure_rows), "closure candidate clause is written"))
    checks.append(("VAL2305_05_quadratic_rows", {"DQW2305_0_DqWeyl2", "DQW2305_1_DqWeylDual", "DQW2305_2_no_tower_zero_route", "DQW2305_3_projection_norm"}.issubset({row["row_id"] for row in quadratic_rows}), "quadratic Weyl residual rows are present"))
    checks.append(("VAL2305_06_quadratic_claim_blocked", any(row["row_id"] == "DQW2305_4_total_status" and row["status"] == "CLAIM_BLOCKED" for row in quadratic_rows), "quadratic Weyl branch remains claim-blocked"))
    checks.append(("VAL2305_07_local_impacts_blocked", all(row["claim_status"].startswith("BLOCKED") for row in impact_rows), "all local impact arenas remain blocked"))
    checks.append(("VAL2305_08_refusal_runner", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks all claims"))
    checks.append(("VAL2305_09_claim_gates", any(row["row_id"] == "GATE2305_5_local_pass" and row["passed"] == "false" for row in claim_rows), "local pass gate remains false"))
    checks.append(("VAL2305_10_next_target", any(row["row_id"] == "DEC2305_3_next" and "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md" in row["next_action"] for row in decision_rows), "next target selected"))
    checks.append(("VAL2305_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2305_12_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2305_13_formalization_untouched_by_2305", len(list(FORMALIZATION.rglob("*2305*"))) == 0 if FORMALIZATION.exists() else True, "no 2305 output appears in formalization-workbench"))
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
            "row_id": "VAL2305_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2305 tries to sign the typed no-spurion grammar, demotes linear B_qWeyl to closure-only because the parent signature is absent, and stages D_qWeyl2 as the next nonclaim local residual.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    quadratic_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2305 — B_qWeyl Linear Zero Typed-Grammar Signature Or Quadratic Weyl Residual Row",
        "",
        "## Summary",
        "",
        "2305 does the thing we said we should do: it tries to sign the typed no-Weyl-spurion grammar rather than smuggling in the plateau/closure axiom. The result is useful but not triumphant. The linear `B_qWeyl` index theorem is still the right theorem: one Weyl tensor cannot form a scalar with scalar/quotient `q` using only metric/epsilon contractions; a nonzero term needs a four-index spurion/projector/readout object.",
        "",
        "But the current corpus still does not parent-sign the grammar that forbids that object. Prior checkpoints repeatedly say the same thing in different sectors: the typed parent language is writable, exact if signed, and powerful, but it is not yet derived from MTS primitives. So 2305 stops circling: the linear `B_qWeyl` route is demoted to closure-only until new parent-action evidence appears.",
        "",
        "The live local-GR obstruction now moves to the higher-curvature side. Quadratic Weyl terms `q C^2` and `q C*C` are not removed by the linear index theorem, so `D_qWeyl2` is staged as the next nonclaim residual. This is the cleaner route: either derive a parent second-order/no-tower theorem, or source a real coefficient/projection bound.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Typed No-Spurion Signature Attempt",
        "",
        md_table(signature_rows, ["row_id", "clause", "statement", "attempt_result", "evidence", "missing_piece", "claim_gate_passed", "valid_for_claim"]),
        "",
        "## Linear B_qWeyl Demotion Ledger",
        "",
        md_table(demotion_rows, ["row_id", "item", "decision", "reason", "allowed_use", "valid_for_claim"]),
        "",
        "## Closure Contract Candidate",
        "",
        md_table(closure_rows, ["row_id", "contract_clause", "exact_text", "status", "would_imply", "valid_for_claim"]),
        "",
        "## Quadratic Weyl Residual Row",
        "",
        md_table(quadratic_rows, ["row_id", "coefficient", "operator", "why_retained", "status", "units", "needed_inputs", "arena", "valid_for_claim"]),
        "",
        "## Local GR Impact Matrix",
        "",
        md_table(impact_rows, ["row_id", "arena", "what_improves", "still_missing", "claim_status", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        md_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows, ["row_id", "decision", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = make_sources()
    signature_rows = make_signature_rows()
    demotion_rows = make_demotion_rows()
    closure_rows = make_closure_rows()
    quadratic_rows = make_quadratic_rows()
    impact_rows = make_impact_rows()
    refusal_rows = make_refusal_rows()
    claim_rows = make_claim_gate_rows()
    decision_rows = make_decision_rows()
    next_rows = make_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["signature"], signature_rows)
    write_csv(OUTPUTS["demotion"], demotion_rows)
    write_csv(OUTPUTS["closure"], closure_rows)
    write_csv(OUTPUTS["quadratic"], quadratic_rows)
    write_csv(OUTPUTS["impact"], impact_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["claim_gates"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_files()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        signature_rows,
        demotion_rows,
        closure_rows,
        quadratic_rows,
        impact_rows,
        refusal_rows,
        claim_rows,
        decision_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        signature_rows,
        demotion_rows,
        closure_rows,
        quadratic_rows,
        impact_rows,
        refusal_rows,
        claim_rows,
        decision_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2305_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
