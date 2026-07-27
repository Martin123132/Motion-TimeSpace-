from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1637"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md"

SOURCE_FILES = {
    "1636_doc": ROOT / "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
    "1636_validation": OUT / "P8_Y5_BRR545_1636_VALIDATION.csv",
    "1636_next": OUT / "P8_Y5_PARENT_QLOC_1636_NEXT_TARGET.csv",
    "1636_bound_pack": OUT / "P8_Y5_PARENT_QLOC_1636_PIR_BOUND_INPUT_PACK.csv",
    "1629_doc": ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md",
    "1629_validation": OUT / "P8_Y5_BRR545_1629_VALIDATION.csv",
    "1629_slot_attempt": OUT / "P8_Y5_PARENT_QLOC_1629_RAB_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "1629_prior_widths": OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv",
    "1065_no_source_slot": ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
    "1065_grammar_csv": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "1066_source_scalar": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
    "955_minimal_matter": ROOT / "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md",
    "954_parent_clause": ROOT / "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md",
}

NEEDLES = {
    "1636_doc": [
        "NEXT_1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR_OR_FIRST_PIR_BOUND_ROW",
        "derive no independent R_AB slot",
    ],
    "1636_validation": ["VAL1636_OVERALL", "PASS"],
    "1636_next": [
        "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
        "do not adopt object-language as proof",
    ],
    "1636_bound_pack": ["PIRBP1636_4_boundary", "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL"],
    "1629_doc": ["RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS", "finite J_R/Pi_R/Q_R prior widths"],
    "1629_validation": ["VAL1629_OVERALL", "PASS"],
    "1629_slot_attempt": ["RSE1629_0_target", "RSE1629_7_verdict", "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS"],
    "1629_prior_widths": ["PW1629_2_PiR", "MISSING_PIR_PRIOR_WIDTH"],
    "1065_no_source_slot": ["CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED", "WTZ1065_0_strict_no_slot"],
    "1065_grammar_csv": ["PGG1065_1_no_inert_species_scalar", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
    "1066_source_scalar": ["CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED", "action-scale/measure ownership"],
    "955_minimal_matter": ["MMA955_3_relative_prefactor", "counterexample_survives"],
    "954_parent_clause": ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1637_SOURCE_REGISTER.csv"
NO_SLOT_GRAMMAR = OUT / "P8_Y5_PARENT_QLOC_1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR.csv"
OBSTRUCTION = OUT / "P8_Y5_PARENT_QLOC_1637_NO_SLOT_OBSTRUCTION_LEDGER.csv"
FIRST_PIR_BOUND = OUT / "P8_Y5_PARENT_QLOC_1637_FIRST_PIR_BOUND_ROW_SCHEMA.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1637_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1637_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1637_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1637_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    NO_SLOT_GRAMMAR,
    OBSTRUCTION,
    FIRST_PIR_BOUND,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    NO_SLOT_GRAMMAR,
    OBSTRUCTION,
    FIRST_PIR_BOUND,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(NO_SLOT_GRAMMAR, QUEUE / "JR1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR_NONCLAIM.csv")
    shutil.copy2(FIRST_PIR_BOUND, QUEUE / "JR1637_FIRST_PIR_BOUND_ROW_SCHEMA_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1637_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": key,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1637 no-independent-RAB-slot grammar / first Pi_R bound input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_slot_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_0_target",
            "grammar_clause": "ordinary matter/source/boundary actions contain no independent R_AB argument or source-only reciprocal scalar",
            "status": "TARGET_SHARPENED",
            "would_prove": "delta S_matter/delta R_AB=0 and removes the direct J_R/Pi_R source slot",
            "gap": "target statement is not a parent derivation",
            "source_basis": str(SOURCE_FILES["1629_slot_attempt"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_1_typed_arguments",
            "grammar_clause": "Arg(S_parent) is restricted to geometry, matter fields, gauge/current data, representation constants, and universal constants",
            "status": "CONDITIONAL_TYPING_LEMMA",
            "would_prove": "R_AB source-only scalars are not legal objects unless observed/typed",
            "gap": "typing principle remains adopted syntax, not derived from MTS primitives",
            "source_basis": str(SOURCE_FILES["1066_source_scalar"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_2_no_inert_RAB_scalar",
            "grammar_clause": "epsilon_RAB_source is forbidden if it changes active source strength but no nongravitational observable",
            "status": "EXACT_IF_PARENT_SYNTAX_ACCEPTED",
            "would_prove": "pre-action reciprocal source scalar cannot generate Pi_R/J_R",
            "gap": "parent syntax/action-scale owner remains unsigned",
            "source_basis": str(SOURCE_FILES["1629_slot_attempt"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_3_variation_order",
            "grammar_clause": "variation occurs before readout/source selectors and before local projection",
            "status": "CLEAN_IF_PARENT_VARIATION_ORDER_SIGNED",
            "would_prove": "post-variation selectors cannot create the primary R_AB source",
            "gap": "does not kill coefficients already inserted before variation",
            "source_basis": str(SOURCE_FILES["1629_slot_attempt"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_4_action_scale",
            "grammar_clause": "universal action-scale/measure owner forbids species/source-local multipliers of S_A",
            "status": "ACTION_SCALE_OWNER_NOT_PARENT_SIGNED",
            "would_prove": "source-only weights cannot hide as harmless classical normalizations",
            "gap": "quantum/path-integral/Hilbert-source action-scale obstruction survives",
            "source_basis": str(SOURCE_FILES["1066_source_scalar"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_5_boundary_slot",
            "grammar_clause": "boundary/worldtube/readout functional has no independent R_AB or Pi_R slot unless explicitly bounded",
            "status": "BOUNDARY_SLOT_NOT_PARENT_SIGNED",
            "would_prove": "Q_R=-Pi_R can close through Pi_R=0 after bulk source silence",
            "gap": "boundary object language is still missing",
            "source_basis": str(SOURCE_FILES["1629_slot_attempt"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_6_hidden_tail",
            "grammar_clause": "hidden non-Hilbert/source-support/domain/readout R_AB tails are absent or bounded",
            "status": "HIDDEN_TAIL_NOT_CLOSED",
            "would_prove": "visible no-slot theorem is stable under local projection and readout",
            "gap": "hidden tail/source-support terms remain legal until parent-banned or bounded",
            "source_basis": str(SOURCE_FILES["1629_slot_attempt"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIR1637_7_verdict",
            "grammar_clause": "no independent R_AB slot theorem",
            "status": "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS",
            "would_prove": "would unlock Pi_R=0 route if all grammar clauses were parent-signed",
            "gap": "current evidence repeats 1629/1065/1066: exact clause, unsigned parent derivation",
            "source_basis": "1637 synthesis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def obstruction_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1637_0_parent_object_language",
            "obstruction": "typed parent object language is not derived from MTS primitives",
            "status": "ACTIVE_OBSTRUCTION",
            "effect": "R_AB slot exclusion cannot be promoted from contract to theorem",
            "required_to_close": "parent field/category grammar proof or explicit residual bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1637_1_action_scale",
            "obstruction": "species/source action-scale or measure multiplier can change Hilbert source",
            "status": "ACTIVE_OBSTRUCTION",
            "effect": "source-only scalar cannot be dismissed as classical normalization",
            "required_to_close": "universal action-scale/measure owner or finite source-weight/Pi_R bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1637_2_pre_action_weight",
            "obstruction": "pre-action R_AB weights survive current-owner and variation-before-readout proofs",
            "status": "ACTIVE_OBSTRUCTION",
            "effect": "J_R/Pi_R can be generated before readout",
            "required_to_close": "no pre-action weight grammar or source-backed prior width",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1637_3_boundary_PiR",
            "obstruction": "boundary reciprocal momentum Pi_R is not syntactically excluded",
            "status": "ACTIVE_OBSTRUCTION",
            "effect": "Q_R=-Pi_R leaves massless reciprocal hair open",
            "required_to_close": "boundary no-slot theorem or Pi_R_boundary_abs bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1637_4_hidden_tail",
            "obstruction": "non-Hilbert/source-support/domain/readout tails can bypass visible no-slot grammar",
            "status": "ACTIVE_OBSTRUCTION",
            "effect": "local-GR proof would be unstable under readout/projection",
            "required_to_close": "hidden-tail theorem or retained residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def first_pir_bound_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRB1637_0_boundary_first_row",
            "coefficient_id": "Pi_R_boundary_abs",
            "arena": "local_GR;PPN;orbital",
            "projection": "MISSING_WORLDTUBE_BOUNDARY_TO_QR_QR_TO_QRLOCAL_PROJECTION",
            "bound_or_value": "MISSING_BOUND_VALUE",
            "units": "boundary reciprocal momentum units; requires normalization to Q_R and q_R",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_SOURCE_PATH",
            "equation_ref": "Q_R=-Pi_R; R_AB=q_R L_N; Delta gamma ~= q_R",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRB1637_1_verticality_support_row",
            "coefficient_id": "Pi_R_vertical_abs",
            "arena": "local_GR;PPN;clock;WEP",
            "projection": "MISSING_DQVR_TO_OBSERVED_COFAME_PROJECTION",
            "bound_or_value": "MISSING_BOUND_VALUE",
            "units": "dimensionless or declared coframe response units",
            "source_path": "MISSING_PARENT_VERTICALITY_SOURCE_PATH",
            "equation_ref": "Dq[v_R]=0 or retained observed coframe response",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PIRB1637_2_source_weight_support_row",
            "coefficient_id": "Pi_R_source_weight_abs",
            "arena": "Newton_GM;WEP;PPN;orbital",
            "projection": "MISSING_DELTA_W_OR_EPSILON_RAB_TO_SOURCE_CURRENT_PROJECTION",
            "bound_or_value": "MISSING_BOUND_VALUE",
            "units": "dimensionless source-weight response",
            "source_path": "MISSING_NO_SLOT_THEOREM_OR_NUMERIC_PRIOR_SOURCE_PATH",
            "equation_ref": "epsilon_RAB_source or w_A(R_AB) source-weight branch",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1637_0_no_slot",
            "decision": "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "1629, 1065, and 1066 all give exact conditional syntax but not a parent derivation",
            "next_action": "stop spending claim-credit on no-slot wording; either derive action-scale/boundary grammar or fill Pi_R bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1637_1_first_bound",
            "decision": "FIRST_PIR_BOUND_ROW_SCHEMA_STAGED_NOT_SOURCE_BACKED",
            "reason": "boundary Pi_R is the live hair route, but no projection/source/value exists yet",
            "next_action": "acquire/derive worldtube boundary projection and q_R normalization before any scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1637_2_next",
            "decision": "NEXT_1638_PIR_BOUND_SOURCE_ACQUISITION_AND_QR_NORMALIZATION",
            "reason": "the theorem route has repeated as conditional; the fallback now needs real source/projection inputs",
            "next_action": "source or derive Pi_R_boundary_abs projection to Q_R/q_R/Delta gamma, or write blocker ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1637_0_no_slot",
            "claim": "no independent R_AB slot theorem",
            "status": "BLOCKED",
            "blocker": "parent object language, action-scale owner, boundary slot, and hidden tail remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1637_1_PiR_bound",
            "claim": "first Pi_R boundary bound row scoreable",
            "status": "BLOCKED",
            "blocker": "projection, source path, units normalization, and bound/value are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1637_2_QR_zero",
            "claim": "Q_R=0/local reciprocal hair removed",
            "status": "BLOCKED",
            "blocker": "Pi_R neither theorem-zero nor bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1637_3_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "status": "BLOCKED",
            "blocker": "q_R amplitude/projection remains missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1638-Y5-R2FR-PiR-bound-source-acquisition-and-qR-normalization.md",
            "script": "scripts/Y5_R2FR_PiR_bound_source_acquisition_and_qR_normalization.py",
            "objective": "source or derive the first Pi_R_boundary_abs projection into Q_R, q_R, and Delta gamma; if no source exists, write a blocker ledger with exact missing inputs",
            "success_condition": "either Pi_R_boundary_abs has source/projection/units/bound metadata ready as nonclaim input, or the blocker ledger proves which parent/empirical source is missing",
            "guardrails": "do not score missing placeholders, do not set tau/projection to one, do not claim local GR, do not use R10 for massless Q_R/r",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: Iterable[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for field in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if field in row and row[field] != "False":
                    return False
    return True


def validation_rows() -> list[dict[str, object]]:
    source_rows = source_register_rows()
    grammar_ids = {row["grammar_id"] for row in no_slot_rows()}
    obstruction_ids = {row["obstruction_id"] for row in obstruction_rows()}
    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1637_0_sources_exist",
            all(row["path_exists"] for row in source_rows),
            "all cited 1637 source paths exist",
        ),
        (
            "VAL1637_1_needles_found",
            all(row["needles_found"] for row in source_rows),
            "all required 1637 source needles found",
        ),
        (
            "VAL1637_2_no_slot_verdict",
            any(row["status"] == "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS" for row in no_slot_rows()),
            "no independent R_AB slot theorem remains unpromoted",
        ),
        (
            "VAL1637_3_grammar_coverage",
            grammar_ids
            == {
                "NIR1637_0_target",
                "NIR1637_1_typed_arguments",
                "NIR1637_2_no_inert_RAB_scalar",
                "NIR1637_3_variation_order",
                "NIR1637_4_action_scale",
                "NIR1637_5_boundary_slot",
                "NIR1637_6_hidden_tail",
                "NIR1637_7_verdict",
            },
            "grammar audit covers typing, pre-action scalar, variation, action-scale, boundary, hidden tail",
        ),
        (
            "VAL1637_4_obstruction_coverage",
            obstruction_ids
            == {
                "OBS1637_0_parent_object_language",
                "OBS1637_1_action_scale",
                "OBS1637_2_pre_action_weight",
                "OBS1637_3_boundary_PiR",
                "OBS1637_4_hidden_tail",
            },
            "obstruction ledger covers parent syntax, action-scale, pre-action, boundary, hidden tail",
        ),
        (
            "VAL1637_5_first_bound_schema",
            any(row["row_id"] == "PIRB1637_0_boundary_first_row" for row in first_pir_bound_rows()),
            "first Pi_R boundary bound schema is staged",
        ),
        (
            "VAL1637_6_first_bound_nonclaim",
            all(row["source_backed"] is False and row["valid_for_claim"] is False for row in first_pir_bound_rows()),
            "first Pi_R bound rows remain explicitly not source-backed/nonclaim",
        ),
        (
            "VAL1637_7_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gate_rows()),
            "all 1637 claim gates remain blocked",
        ),
        (
            "VAL1637_8_next_target_selected",
            next_target_rows()[0]["next_target"] == "1638-Y5-R2FR-PiR-bound-source-acquisition-and-qR-normalization.md",
            "next target selects Pi_R bound source acquisition and q_R normalization",
        ),
        (
            "VAL1637_9_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1637 CSVs parse",
        ),
        (
            "VAL1637_10_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1637 generated decision rows remain nonclaim",
        ),
        (
            "VAL1637_11_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1637_12_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR_NONCLAIM.csv",
                    QUEUE / "JR1637_FIRST_PIR_BOUND_ROW_SCHEMA_NONCLAIM.csv",
                    QUEUE / "JR1637_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1637_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1637_14_formalization_untouched",
            not any(FORMALIZATION.rglob("*1637*")) if FORMALIZATION.exists() else True,
            "no 1637 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1637_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1637 no independent RAB slot grammar or first Pi_R bound row validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    grammar_rows = csv_rows(NO_SLOT_GRAMMAR)
    obstructions = csv_rows(OBSTRUCTION)
    first_rows = csv_rows(FIRST_PIR_BOUND)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_rows = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1637 — No Independent R_AB Slot Grammar Or First Pi_R Bound Row

**Private status:** nonclaim checkpoint. No `R_AB` source-slot exclusion theorem, `Pi_R=0`, `Q_R=0`, local-GR, Newton, PPN, WEP, clock, orbital, EM, or R10 pass is claimed.

## Verdict

The no-independent-`R_AB` slot theorem remains exact as a conditional grammar but is **not** parent-derived in the current corpus. This is not a new failure: 1629 already specialized the slot-exclusion route to `R_AB`, and 1065/1066 showed the same source-scalar obstruction in the ordinary-matter source language.

The useful result is that the loop is now closed:

```text
no-slot theorem not derived -> first Pi_R bound row must be sourced
```

The first fallback row is therefore `Pi_R_boundary_abs`, because boundary `Pi_R` is the direct route from bulk silence failure to massless `Q_R/r` hair.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## No Independent R_AB Slot Grammar

{markdown_table(grammar_rows, ["grammar_id", "grammar_clause", "status", "would_prove", "gap"])}

## Obstruction Ledger

{markdown_table(obstructions, ["obstruction_id", "obstruction", "status", "effect", "required_to_close"])}

## First Pi_R Bound Row Schema

{markdown_table(first_rows, ["row_id", "coefficient_id", "arena", "projection", "bound_or_value", "units", "source_path", "source_backed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        NO_SLOT_GRAMMAR: no_slot_rows(),
        OBSTRUCTION: obstruction_rows(),
        FIRST_PIR_BOUND: first_pir_bound_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
