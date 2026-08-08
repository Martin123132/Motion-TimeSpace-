from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2711"
BRANCH_ID = "Y5_R2FR_AX1090_PARENT_OBJECT_DERIVATION_FROM_MTS_PRIMITIVES_OR_EXPLICIT_CLOSURE_2711"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2711_SOURCE_REGISTER.csv",
    "primitive_source_hunt": RESIDUALS / "P8_Y5_R2FR_2711_PRIMITIVE_SOURCE_HUNT.csv",
    "ax1090_derivation_attempt": RESIDUALS / "P8_Y5_R2FR_2711_AX1090_DERIVATION_ATTEMPT.csv",
    "parent_object_clause_audit": RESIDUALS / "P8_Y5_R2FR_2711_PARENT_OBJECT_CLAUSE_AUDIT.csv",
    "explicit_closure_axiom_ledger": RESIDUALS / "P8_Y5_R2FR_2711_EXPLICIT_CLOSURE_AXIOM_LEDGER.csv",
    "branch_route_rules": RESIDUALS / "P8_Y5_R2FR_2711_BRANCH_ROUTE_RULES.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2711_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2711_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2711_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2711_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2711_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_parent_object_gate": LOCAL_BOUNDS / "AX1090_parent_object_gate_2711_NONCLAIM.csv",
    "source_weight_parent_closure": SOURCE_WEIGHT / "AX1090_PARENT_OBJECT_EXPLICIT_CLOSURE_2711_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2711_PARENT_OBJECT_CLOSURE_OR_A511_FIXED_POINT_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2711_2710_HANDOFF",
        "relative_path": "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md",
        "required_needles": [
            "AX1090_0_PARENT_OBJECT_MISSING",
            "F2710_0_first_gate",
            "NEXT2710_0_selected",
        ],
        "purpose": "imports first irreducible parent-object gate from 2710",
    },
    {
        "source_id": "SRC2711_1090_MISSING_AXIOM_LEDGER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
        "required_needles": [
            "AX1090_0_parent_object",
            "MISSING_AXIOM_NOT_ADOPTED",
            "AX1090_4_variation_domain_order",
        ],
        "purpose": "imports the exact AX1090 parent-object axiom that earlier work refused to adopt",
    },
    {
        "source_id": "SRC2711_2710_PARENT_OBJECT_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2710_PARENT_OBJECT_NORMAL_FORM.csv",
        "required_needles": [
            "PO2710_0_parent_object",
            "S_parent[Phi,Psi;theta]=int_M L_parent",
            "AX1090_0_PARENT_OBJECT_MISSING",
        ],
        "purpose": "imports the normal form that any primitive derivation must own",
    },
    {
        "source_id": "SRC2711_2710_FIRST_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2710_IRREDUCIBLE_FALSIFIER_GATE.csv",
        "required_needles": [
            "F2710_0_first_gate",
            "FIRST_IRREDUCIBLE_GATE",
            "derive AX1090_0 from MTS primitives",
        ],
        "purpose": "imports the falsifier that blocks local promotion without AX1090_0",
    },
    {
        "source_id": "SRC2711_01_MOTION_LOAD_CONTRACT",
        "relative_path": "01-motion-load-route-contract.md",
        "required_needles": [
            "more primitive than the earlier motion-field formulation?",
            "independent primitives.",
            "p=1 or gamma=1 is derived from motion-load/routing structure;",
        ],
        "purpose": "tests whether the motion-load primitive route already defines a parent object",
    },
    {
        "source_id": "SRC2711_02_LOCAL_GR_CONDITIONAL",
        "relative_path": "02-motion-load-local-GR-reduction.md",
        "required_needles": [
            "If `p=1` is treated as the exact Schwarzschild-form reciprocal completion",
            "motion-load local GR reduction = conditional success;",
            "But no main-workbench promotion is allowed yet.",
        ],
        "purpose": "keeps local-GR inheritance conditional rather than claimed",
    },
    {
        "source_id": "SRC2711_03_PARENT_ORIGIN",
        "relative_path": "03-reciprocal-routing-parent-origin.md",
        "required_needles": [
            "the MTS/motion-load action must imply the vacuum radial stress balance",
            "p=1 is conditionally derived from reciprocity;",
            "without smuggling in Einstein's exterior equations.",
        ],
        "purpose": "imports the no-GR-smuggling action-origin contract",
    },
    {
        "source_id": "SRC2711_04_ACTION_CONTRACT",
        "relative_path": "04-vacuum-reciprocity-action-contract.md",
        "required_needles": [
            "What exact theorem must a motion-load parent action satisfy",
            "action theorem proved;",
            "motion-load route unpromoted.",
        ],
        "purpose": "imports the reciprocal parent-action theorem target and failure state",
    },
    {
        "source_id": "SRC2711_07_NONPROP_CONSTRAINT",
        "relative_path": "07-nonpropagating-reciprocity-constraint.md",
        "required_needles": [
            "S_constraint = integral lambda_R R_AB.",
            "why does the parent motion-load action contain lambda_R ln(T^2 S)?",
            "p=1 recovered.",
        ],
        "purpose": "tests whether the lambda_R constraint is parent-derived rather than inserted",
    },
    {
        "source_id": "SRC2711_10_OBSERVER_MAP",
        "relative_path": "10-observer-map-symplectic-contract.md",
        "required_needles": [
            "The local motion-load route now has a precise no-smuggling contract:",
            "derive R_AB=0 from the parent theory",
            "contract not satisfied;",
        ],
        "purpose": "imports the local observer-map no-smuggling contract",
    },
    {
        "source_id": "SRC2711_407_PRIMITIVE_QUOTIENT",
        "relative_path": "407-primitive-relational-quotient-action-sketch.md",
        "required_needles": [
            "Primitive Relational Quotient Action Sketch",
            "S_matter_quotient_functor",
            "matter quotient functor/no-marker selector proof",
            "Practical read: this is a good theorem target. It is not a theorem.",
        ],
        "purpose": "imports the best primitive quotient/action sketch and its missing proofs",
    },
    {
        "source_id": "SRC2711_1157_QMAP",
        "relative_path": "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
        "required_needles": [
            "the parent `q`/null-generator proof does not close",
            "QMAP1157_1_parent_q_object",
            "NOT_CONSTRUCTED_FOR_CURRENT_MTS",
        ],
        "purpose": "imports the unresolved parent quotient-map object",
    },
    {
        "source_id": "SRC2711_1276_EH_FIXED_POINT",
        "relative_path": "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
        "required_needles": [
            "least-ad-hoc path",
            "ESC1276_1_local_EH_fixed_point",
            "CANDIDATE_NOT_DERIVED",
            "PG1276_0_EH_fixed_point",
        ],
        "purpose": "imports the local EH fixed-point scaffold and its non-derived status",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def primitive_source_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "HUNT2711_0_motion_load_primitives",
            "candidate": "motion-load independent primitives",
            "source_path": "01-motion-load-route-contract.md",
            "positive_content": "the route asks whether motion/time/space can be more primitive than the earlier motion-field formulation and demands p=1 or gamma=1 be derived from routing structure",
            "missing_for_AX1090_0": "does not define Conf_parent, full L_parent, matter domain, boundary class, q, readout maps, and variation order as one parent object",
            "derivation_status": "PRIMITIVE_MOTIVATION_NOT_PARENT_OBJECT",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2711_1_motion_load_reciprocity",
            "candidate": "reciprocal routing and R_AB constraint route",
            "source_path": "03-reciprocal-routing-parent-origin.md;04-vacuum-reciprocity-action-contract.md;07-nonpropagating-reciprocity-constraint.md",
            "positive_content": "identifies the theorem needed to derive AB=1/p=1 from a motion-load action without importing Schwarzschild or Einstein vacuum equations",
            "missing_for_AX1090_0": "lambda_R/R_AB is an action theorem target, not a parent-derived term with a signed variation domain",
            "derivation_status": "LOCAL_ACTION_CONTRACT_NOT_PARENT_OBJECT",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2711_2_primitive_relational_quotient",
            "candidate": "primitive relational quotient action sketch",
            "source_path": "407-primitive-relational-quotient-action-sketch.md",
            "positive_content": "best current candidate for quotient/readout discipline, selector-blind matter, no marker extension, and total flux ownership",
            "missing_for_AX1090_0": "configuration quotient, no-marker theorem, matter quotient functor, and Ward flux owner remain sketches rather than parent-derived proofs",
            "derivation_status": "GOOD_THEOREM_TARGET_NOT_THEOREM",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2711_3_parent_q_map",
            "candidate": "parent q map/null-generator proof",
            "source_path": "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
            "positive_content": "states the needed Conf_parent -> Q_obs quotient object and prevents q by declaration",
            "missing_for_AX1090_0": "the parent quotient object is explicitly not constructed for current MTS",
            "derivation_status": "PARENT_Q_OBJECT_NOT_CONSTRUCTED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2711_4_local_EH_fixed_point",
            "candidate": "A511/local EH fixed-point scaffold",
            "source_path": "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            "positive_content": "least-ad-hoc route for GR reduction: parent-signed local EH fixed point plus silent/topological extras and matter in the observed frame",
            "missing_for_AX1090_0": "the scaffold is candidate-not-derived and presupposes the parent object rather than deriving it",
            "derivation_status": "EH_FIXED_POINT_SCAFFOLD_NOT_PARENT_SOURCE",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "HUNT2711_5_verdict",
            "candidate": "AX1090_0 from current primitive corpus",
            "source_path": "all 2711 registered sources",
            "positive_content": "the corpus strongly constrains what the parent object must be and has several promising theorem targets",
            "missing_for_AX1090_0": "no single primitive source constructs the parent action object before readout/projection/fitting",
            "derivation_status": "DERIVATION_NOT_CLOSED_EXPLICIT_CLOSURE_REQUIRED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def ax1090_derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "DER2711_0_configuration_space",
            "required_clause": "construct Conf_parent and its admissible local/boundary domain before readout",
            "best_source": "407 configuration-space sketch plus 2710 normal form",
            "attempted_derivation": "identify observed geometry, relational MTS state, finite-cell fibre, readout projection, active-marker exclusion, and boundary-domain class as one configuration object",
            "failure_or_gap": "G_rel, finite-cell fibre status, exact readout role, and boundary class are not formalized as one variational domain",
            "result": "NOT_DERIVED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_1_parent_lagrangian",
            "required_clause": "construct L_parent(Phi,dPhi,Psi,dPsi,theta) plus boundary term before sector projection",
            "best_source": "04 action contract and 07 nonpropagating reciprocity constraint",
            "attempted_derivation": "use reciprocal-strain constraint as local route to p=1/gamma=1 and try to read it as a parent action block",
            "failure_or_gap": "the corpus asks why the parent motion-load action contains the constraint; it does not answer that question",
            "result": "NOT_DERIVED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_2_quotient_map",
            "required_clause": "define q: Conf_parent -> Q_obs as a parent/reduced phase-space quotient, not a post-fit class",
            "best_source": "1157 parent q-map gate and 407 quotient sketch",
            "attempted_derivation": "promote the relational quotient sketch into an owned q-map",
            "failure_or_gap": "1157 explicitly records the parent quotient object as not constructed for current MTS",
            "result": "NOT_DERIVED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_3_matter_descent",
            "required_clause": "derive ordinary matter action as a quotient functor of one observed coframe/frame",
            "best_source": "407 matter quotient functor row and 1276 local EH fixed-point scaffold",
            "attempted_derivation": "treat matter as living only on the observed frame inherited from the local EH fixed point",
            "failure_or_gap": "matter quotient functor/no-marker selector proof is named as missing, and EH fixed point is candidate-not-derived",
            "result": "NOT_DERIVED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_4_variation_order",
            "required_clause": "prove all variations occur before empirical readout, material projection, source selection, or calibration",
            "best_source": "1090 AX1090_4 plus 2710 parent-object normal form",
            "attempted_derivation": "use the 2710 normal form to force readout maps to be declared before variation",
            "failure_or_gap": "this is a clean contract, not a derivation from MTS primitives",
            "result": "CONTRACT_ONLY",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_5_local_EH_inheritance",
            "required_clause": "show MTS local branch reduces to EH plus silent/topological extras before deriving Newton/PPN",
            "best_source": "1276 A511/local EH fixed-point scaffold",
            "attempted_derivation": "inherit GR radial equations only after parent-signed A511 blocks and vanishing extra variations",
            "failure_or_gap": "the A511 blocks are a scaffold whose parent signatures are not yet derived",
            "result": "CANDIDATE_NOT_DERIVED",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "DER2711_6_verdict",
            "required_clause": "derive AX1090_0 parent object from current MTS primitive corpus",
            "best_source": "all registered 2711 primitive and gate sources",
            "attempted_derivation": "combine motion-load primitives, reciprocal action theorem, primitive quotient sketch, parent q-map gate, and EH fixed-point scaffold",
            "failure_or_gap": "the combination is coherent but circular: every route needs the parent object or a signed parent action before it can prove the parent object",
            "result": "DERIVATION_NOT_CLOSED_EXPLICIT_CLOSURE",
            "derived": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def parent_object_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "POA2711_0_parent_configuration",
            "clause": "Conf_parent exists as one admissible parent configuration space",
            "best_current_status": "SKETCHED_NOT_CONSTRUCTED",
            "source_path": "407-primitive-relational-quotient-action-sketch.md",
            "missing_input": "formal G_rel/equivalence relation, finite-cell fibre theorem, domain/boundary class",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_1_parent_action",
            "clause": "S_parent is defined before all projections and readouts",
            "best_current_status": "NORMAL_FORM_ONLY",
            "source_path": "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md",
            "missing_input": "parent Lagrangian owner and sector variation signatures",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_2_quotient_readout",
            "clause": "q and readout maps are declared before variation and not fitted after the fact",
            "best_current_status": "REQUIRED_NOT_BUILT",
            "source_path": "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
            "missing_input": "parent quotient object Conf_parent -> Q_obs",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_3_matter_action",
            "clause": "ordinary matter descends through q/common observed coframe with no hidden material marker",
            "best_current_status": "SUFFICIENT_AXIOM_NOT_DERIVED",
            "source_path": "407-primitive-relational-quotient-action-sketch.md",
            "missing_input": "matter quotient functor/no-marker selector theorem",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_4_local_reciprocity",
            "clause": "R_AB=0 or equivalent reciprocal constraint is produced by parent Euler equations",
            "best_current_status": "THEOREM_TARGET",
            "source_path": "04-vacuum-reciprocity-action-contract.md;07-nonpropagating-reciprocity-constraint.md",
            "missing_input": "parent origin of lambda_R/R_AB and vacuum source silence proof",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_5_local_EH_fixed_point",
            "clause": "local branch is EH plus matter plus silent/topological extras",
            "best_current_status": "CANDIDATE_NOT_DERIVED",
            "source_path": "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            "missing_input": "parent-derived A511 action blocks and vanishing first variations",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_6_variation_order",
            "clause": "variation precedes readout/projection/fitting/source-worldtube selection",
            "best_current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
            "missing_input": "derived detector/source model that fixes the ordering",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "clause_id": "POA2711_7_verdict",
            "clause": "AX1090_0 parent object can be used in local branch",
            "best_current_status": "EXPLICIT_CLOSURE_REQUIRED_NOT_CLAIM",
            "source_path": "this checkpoint",
            "missing_input": "primitive derivation of the parent object",
            "claim_pass": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def explicit_closure_axiom_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "AX1090_0_LC",
            "closure_name": "local parent object closure",
            "statement": "For the local transition branch only, assume there exists one parent action object S_parent[Phi,Psi;theta] with Conf_parent, admissible boundary/domain class, quotient/readout maps, matter domain, and variation order declared before any empirical readout/projection/fitting.",
            "why_needed": "all local GR/Newton/PPN/R10/WEP routes require a common owner for q, matter, source charge, boundary terms, and variation order",
            "source_status": "EXPLICIT_CLOSURE_NOT_DERIVED",
            "allowed_use": "theorem target bookkeeping and conditional local branch construction",
            "forbidden_use": "claiming local-GR/Newton/PPN/R10/WEP pass or treating closure as proof",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_1",
            "closure_name": "configuration owner",
            "statement": "Conf_parent is the owner of observed geometry, relational MTS variables, finite-cell fibre data, readout maps, matter variables, and boundary/domain class.",
            "why_needed": "prevents separate contracts from deriving each other circularly",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "audit every later local theorem for a declared owner",
            "forbidden_use": "declaring a new sector owner after a failed variation",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_2",
            "closure_name": "action owner",
            "statement": "S_parent is varied on Conf_parent before local readout; all sector action blocks, constraints, and boundary terms must appear inside S_parent or be retained as residuals.",
            "why_needed": "blocks hidden insertion of lambda_R, EH, matter couplings, or source charges after the fact",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "route non-owned blocks into residual ledgers",
            "forbidden_use": "using a fitted local equation as if it were a parent Euler equation",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_3",
            "closure_name": "quotient/readout order",
            "statement": "q, readout maps, and observer-frame maps are declared before variation and cannot be chosen to erase a local residual after fitting.",
            "why_needed": "prevents q by declaration and no-shadow smuggling",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "test local readout maps against pre-variation ownership",
            "forbidden_use": "post-hoc frame choice to set c_g, PPN residuals, or R10 coefficients to zero",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_4",
            "closure_name": "matter descent",
            "statement": "ordinary matter couples through the same observed frame/coframe unless a nonzero residual current is explicitly retained and bounded.",
            "why_needed": "keeps WEP, clocks, R10, and charge tests honest",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "conditional same-frame bookkeeping",
            "forbidden_use": "asserting WEP/source universality without a quotient matter functor proof",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_5",
            "closure_name": "local EH fixed-point target",
            "statement": "local-GR work may attempt to prove an EH fixed point only after all non-EH action blocks are parent-owned, silent, topological, boundary-only, or source-bounded.",
            "why_needed": "keeps GR reduction derivable instead of imported",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "next A511 fixed-point derivation attempt",
            "forbidden_use": "jumping from gamma=1 or AB=1 to full GR/Newton/PPN pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "closure_id": "AX1090_0_LC_6",
            "closure_name": "residual retention",
            "statement": "any coefficient or current not parent-derived under AX1090_0_LC remains an explicit residual with valid_for_claim=false until source-owned or bounded.",
            "why_needed": "preserves falsifiability and prevents theory-by-omission",
            "source_status": "CLOSURE_SUBCLAUSE",
            "allowed_use": "build clean residual/bound ledgers",
            "forbidden_use": "dropping awkward couplings because the local branch would look nicer without them",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_route_rules_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ROUTE2711_0_if_parent_object_derived",
            "condition": "AX1090_0 is later derived from primitive MTS action grammar",
            "next_action": "promote AX1090_0_LC from closure to theorem and rerun A511/EH fixed-point proof without closure language",
            "claim_status": "future_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "route_id": "ROUTE2711_1_current_route",
            "condition": "AX1090_0 not derived in 2711",
            "next_action": "carry AX1090_0_LC explicitly and attempt A511 local EH fixed-point proof or route every non-EH term to residual/bound ledgers",
            "claim_status": "closure_only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "route_id": "ROUTE2711_2_if_A511_closes_under_closure",
            "condition": "A511 blocks are parent-signed under explicit AX1090_0_LC and extra variations vanish or are bounded",
            "next_action": "derive Newton/PPN residual equations conditionally, with closure label retained",
            "claim_status": "conditional_private_theorem_target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "route_id": "ROUTE2711_3_if_A511_fails",
            "condition": "A511 cannot be signed even with AX1090_0_LC",
            "next_action": "demote local transition route to residual-only and focus on primitive parent-action construction",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gates_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2711_0_AX1090_parent_object", "AX1090_0 parent object derived from MTS primitives", "false", "closure only"),
        ("CG2711_1_local_GR", "local GR reduction claimed", "false", "blocked until AX1090/A511 and residual silence close"),
        ("CG2711_2_Newton_PPN", "Newtonian and PPN branch claimed", "false", "blocked until EH fixed point plus beta/gamma/conservation"),
        ("CG2711_3_R10_WEP_clock_orbital", "local empirical arenas claimed", "false", "blocked until parent coefficients are sourced and valid_for_claim=true"),
        ("CG2711_4_public_or_github", "public/GitHub action allowed", "false", "private checkpoint only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, claim_allowed, reason in gates
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2711_0_derivation_result",
            "decision": "AX1090_0 is not derived from current primitive corpus",
            "rationale": "motion-load, reciprocity, quotient, q-map, and EH fixed-point sources all require the parent object or parent action they would need to prove",
            "consequence": "do not claim local GR/Newton/PPN/local-bound pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2711_1_closure_policy",
            "decision": "write AX1090_0_LC as an explicit local-transition closure axiom",
            "rationale": "closure language is cleaner than pretending the parent object is already proven",
            "consequence": "future local work can proceed conditionally without smuggling",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2711_2_next_route",
            "decision": "attack A511 local EH fixed point under explicit AX1090_0_LC",
            "rationale": "this is the least-ad-hoc route to GR/Newton reduction while keeping closure debt visible",
            "consequence": "next checkpoint must either sign A511 action blocks or route non-EH pieces to finite residuals",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2711_0_selected",
            "status": "selected_primary",
            "target_doc": "2712-Y5-R2FR-A511-local-EH-fixed-point-under-AX1090-closure-or-residual-routing.md",
            "target_script": "scripts/Y5_R2FR_A511_local_EH_fixed_point_under_AX1090_closure_or_residual_routing_2712.py",
            "purpose": "try to parent-sign the A511/local EH fixed-point action blocks under explicit AX1090_0_LC; if any non-EH term is not silent/topological/boundary/source-bounded, route it to a residual ledger and keep local-GR unclaimed",
            "acceptance_condition": "A511 blocks are either parent-signed with zero/bounded first variation or explicitly retained as residuals; no Newton/PPN/local test claim is made from closure alone",
            "forbidden_shortcuts": "treat AX1090_0_LC as proof; import Einstein equations; assume lambda_R/R_AB; erase residual couplings; run public/GitHub action; edit formalization-workbench",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT2711_0_project_meaning",
            "area": "overall",
            "status": "first missing parent-action axiom is now explicit",
            "meaning": "the project is not looping; it has located the root gate that local GR/Newton reduction must pass",
            "risk": "closure can become a crutch if not attacked again",
            "next_action": "use AX1090_0_LC only as a labeled bridge while trying to derive or residual-route A511",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STAT2711_1_good_news",
            "area": "theory spine",
            "status": "coherent theorem target",
            "meaning": "motion-load, quotient/readout, and EH fixed-point routes are mutually compatible as a possible parent-action programme",
            "risk": "compatibility is not derivation",
            "next_action": "convert candidate action blocks into signed parent variations or bounded residuals",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STAT2711_2_bad_news",
            "area": "claim ceiling",
            "status": "no local-GR claim yet",
            "meaning": "AX1090_0, A511, matter descent, q-map, and variation order remain unproved",
            "risk": "without these, MTS is a promising framework rather than a derived GR replacement",
            "next_action": "make the next checkpoint an action-block proof attempt, not another broad survey",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    threshold = START_UTC.timestamp() - 2.0
    changed_count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                changed_count += 1
        except OSError:
            continue
    return changed_count


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2711_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2711_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    hunt = rows_by_name["primitive_source_hunt"]
    add("VAL2711_2_hunt_attempted", len(hunt) >= 6 and any(row["hunt_id"] == "HUNT2711_5_verdict" for row in hunt), "primitive source hunt completed")
    add("VAL2711_3_no_primitive_derivation_claim", all(row["derived"] == "false" and row["valid_for_claim"] == "false" for row in hunt), "no primitive source-hunt row claims AX1090 derivation")

    derivation = rows_by_name["ax1090_derivation_attempt"]
    add("VAL2711_4_derivation_attempted", any(row["attempt_id"] == "DER2711_6_verdict" and row["result"] == "DERIVATION_NOT_CLOSED_EXPLICIT_CLOSURE" for row in derivation), "AX1090 derivation attempt reaches explicit closure verdict")
    add("VAL2711_5_derivation_rows_nonclaim", all(row["derived"] == "false" and row["valid_for_claim"] == "false" for row in derivation), "all derivation rows remain nonclaim")

    audit = rows_by_name["parent_object_clause_audit"]
    add("VAL2711_6_clause_audit_complete", len(audit) >= 8 and any(row["clause_id"] == "POA2711_7_verdict" for row in audit), "parent-object clause audit complete")
    add("VAL2711_7_no_clause_claims", all(row["claim_pass"] == "false" and row["valid_for_claim"] == "false" for row in audit), "no parent-object clause claims pass")

    closures = rows_by_name["explicit_closure_axiom_ledger"]
    add("VAL2711_8_closure_axiom_written", any(row["closure_id"] == "AX1090_0_LC" and row["source_status"] == "EXPLICIT_CLOSURE_NOT_DERIVED" for row in closures), "explicit AX1090_0_LC closure axiom written")
    add("VAL2711_9_closure_nonclaim", all(row["valid_for_claim"] == "false" for row in closures), "closure rows are nonclaim")

    add("VAL2711_10_route_2712_selected", any(row["next_id"] == "NEXT2711_0_selected" and "2712" in row["target_doc"] for row in rows_by_name["next_target"]), "2712 A511/EH route selected")
    add("VAL2711_11_claims_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates remain blocked")
    add("VAL2711_12_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2711_13_no_formalization_recent_changes", formalization_recent_change_count() == 0, f"formalization_recent_changed_count={formalization_recent_change_count()}")
    add("VAL2711_14_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2711_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2711_PARSE_validation")]
    add(
        "VAL2711_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2711 tries to derive AX1090_0 from MTS primitives, finds the current corpus coherent but unsigned, writes explicit AX1090_0_LC closure language, blocks all claims, and selects A511/local EH fixed-point routing for 2712",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Primitive Source Hunt", rows_by_name["primitive_source_hunt"]),
        ("AX1090 Derivation Attempt", rows_by_name["ax1090_derivation_attempt"]),
        ("Parent Object Clause Audit", rows_by_name["parent_object_clause_audit"]),
        ("Explicit Closure Axiom Ledger", rows_by_name["explicit_closure_axiom_ledger"]),
        ("Branch Route Rules", rows_by_name["branch_route_rules"]),
        ("Decision Ledger", rows_by_name["decision_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2711: AX1090 Parent Object Derivation From MTS Primitives Or Explicit Closure",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2711 tries the derivation route first. The current corpus has real structure: motion-load primitives, reciprocal-routing contracts, a primitive quotient/action sketch, a parent q-map gate, and an A511/local EH fixed-point scaffold. But none of those sources constructs the one parent action object before readout/projection/fitting. They all either require that object, require a parent action, or state a good theorem target rather than a proof.",
        "",
        "So the honest result is not `AX1090_0 derived`. The honest result is: `AX1090_0_LC` is now an explicit local-transition closure axiom, not a hidden assumption. That keeps the branch alive while making the debt visible.",
        "",
        "## Bottom Line",
        "",
        "- Good news: the pieces are not random; they point at the same missing owner.",
        "- Hard news: the owner is still not derived from MTS primitives.",
        "- Discipline move: local GR/Newton/PPN/local-bound claims stay blocked.",
        "- Next route: try to parent-sign A511/local EH fixed-point action blocks under explicit closure, or route every non-EH term to residual/bound ledgers.",
        "",
        "## Closure Contract",
        "",
        "`AX1090_0_LC` is allowed only as a private local-transition bridge. It may organize the next derivation attempt, but it cannot be used as evidence that MTS has reduced to GR/Newton. Any coupling, current, source charge, boundary term, q-map, or readout coefficient not parent-derived remains an explicit residual.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "primitive_source_hunt": primitive_source_hunt_rows(),
        "ax1090_derivation_attempt": ax1090_derivation_attempt_rows(),
        "parent_object_clause_audit": parent_object_clause_audit_rows(),
        "explicit_closure_axiom_ledger": explicit_closure_axiom_ledger_rows(),
        "branch_route_rules": branch_route_rules_rows(),
        "claim_gates": claim_gates_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def main() -> None:
    rows_by_name = build_rows()
    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_parent_object_gate"], rows_by_name["parent_object_clause_audit"])
    write_csv(BRANCH_OUTPUTS["source_weight_parent_closure"], rows_by_name["explicit_closure_axiom_ledger"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"overall={validation[-1]['passed']}")


if __name__ == "__main__":
    main()
