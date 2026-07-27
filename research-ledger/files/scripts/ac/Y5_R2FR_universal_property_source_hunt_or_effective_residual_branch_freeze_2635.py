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
DOC_PATH = ROOT / "2635-Y5-R2FR-universal-property-source-hunt-or-effective-residual-branch-freeze.md"

PREFIX = "P8_Y5_UNIVERSAL_PROPERTY_HUNT_2635"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "candidate_review": RESIDUALS / f"{PREFIX}_CANDIDATE_REVIEW.csv",
    "source_hunt_verdict": RESIDUALS / f"{PREFIX}_SOURCE_HUNT_VERDICT.csv",
    "axiom_freeze": RESIDUALS / f"{PREFIX}_AXIOM_FREEZE_GATE.csv",
    "generator_queue": RESIDUALS / f"{PREFIX}_GENERATOR_ELIMINATION_QUEUE.csv",
    "effective_pack": RESIDUALS / f"{PREFIX}_EFFECTIVE_RESIDUAL_PACK_SEED.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2635_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2635_00_2634",
        "role": "immediate parent-action source-hunt handoff",
        "path": ROOT / "2634-Y5-R2FR-parent-action-generating-principle-or-effective-GR-residual-branch.md",
        "needles": ["GENERATING_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS", "2635-Y5-R2FR-universal-property-source-hunt", "VAL2634_OVERALL"],
    },
    {
        "source_id": "SRC2635_01_407",
        "role": "primitive relational quotient sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needles": ["primitive_relational_quotient_action_sketch_written_candidate_parent_origin_formalized", "no_marker_theorem_derived", "Decision"],
    },
    {
        "source_id": "SRC2635_02_423",
        "role": "minimality/no-extension theorem attempt",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": ["parent_universal_property_derived", "no_natural_marker_theorem_derived", "The current corpus does not yet prove the universal property"],
    },
    {
        "source_id": "SRC2635_03_573",
        "role": "early primitive-minimal no-natural-marker theorem attempt",
        "path": ROOT / "573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md",
        "needles": ["PM573_1_material_marker_no_extension", "I_loc(Q_MTS)", "primitive-minimal no-marker theorem"],
    },
    {
        "source_id": "SRC2635_04_965",
        "role": "primitive quotient/no-natural-marker theorem attempt",
        "path": ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
        "needles": ["THEOREM_NOT_PROVEN_CURRENT_CORPUS", "PQ965_0_theorem_target", "V965_2_theorem_not_overclaimed"],
    },
    {
        "source_id": "SRC2635_05_980",
        "role": "no-marker sector functor obstruction",
        "path": ROOT / "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md",
        "needles": ["NO_MARKER_FUNCTOR_REJECTED_CURRENT_CORPUS", "NMF980_2_scalar_obstruction_lemma", "V980_3_no_marker_verdict_nonclaim"],
    },
    {
        "source_id": "SRC2635_06_1237",
        "role": "MTS primitives to sorted parent action audit",
        "path": ROOT / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md",
        "needles": ["does **not** derive the sorted parent action grammar", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED", "PRIM1237_8_verdict"],
    },
    {
        "source_id": "SRC2635_07_1513",
        "role": "primitive minimality/no-higher-derivative theorem audit",
        "path": ROOT / "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md",
        "needles": ["primitive minimality/no-natural-marker theorem still does not close", "THEOREM_NOT_PROVEN_CURRENT_CORPUS", "VAL1513_12_overall"],
    },
    {
        "source_id": "SRC2635_08_1676",
        "role": "object-language/no-marker theorem attempt",
        "path": ROOT / "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md",
        "needles": ["NO_SOURCE_ONLY_SLOT_THEOREM_NOT_PROVED", "HIDDEN_MARKER_OBSTRUCTION_ACTIVE", "VAL1676_OVERALL"],
    },
    {
        "source_id": "SRC2635_09_1982",
        "role": "wider corpus parent-action signature scan",
        "path": ROOT / "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md",
        "needles": ["candidate_files_scanned=373", "scanner only creates review queue", "VAL1982_OVERALL"],
    },
    {
        "source_id": "SRC2635_10_1983",
        "role": "top parent-action candidate review",
        "path": ROOT / "1983-Y5-R2FR-top-parent-action-candidate-review.md",
        "needles": ["zero reviewed candidates promoted", "No reviewed wider-corpus hit signs", "VAL1983_OVERALL"],
    },
    {
        "source_id": "SRC2635_11_2458",
        "role": "parent action signature hunt and route demotion",
        "path": ROOT / "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
        "needles": ["Strong candidates exist, but they are partial", "no source-backed signature is promoted", "VAL2458_OVERALL"],
    },
    {
        "source_id": "SRC2635_12_2609",
        "role": "current primitive package gate",
        "path": ROOT / "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
        "needles": ["primitive minimality remains unproved", "local invariant algebra not trivialized", "VAL2609_OVERALL"],
    },
    {
        "source_id": "SRC2635_13_2623",
        "role": "primitive quotient/no-marker/no-tower current gate",
        "path": ROOT / "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md",
        "needles": ["PRIMITIVE_QUOTIENT_NO_MARKER_NO_TOWER_NOT_PROVEN", "PQT2623_3_no_extension_universal_property", "VAL2623_OVERALL"],
    },
    {
        "source_id": "SRC2635_14_2625",
        "role": "parent-domain certificate attempt",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": ["FIELD_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE", "READOUT_ZERO_DEMOTED_TO_CLOSURE", "VAL2625_OVERALL"],
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
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def candidate_review_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAN2635_0_primitive_sketch",
            "source_ids": "SRC2635_01_407",
            "candidate_claim": "primitive relational quotient/readout parent-action sketch",
            "review_result": "SKETCH_NOT_THEOREM",
            "why_not_claim_grade": "explicitly still needs quotient/basis-free parent configuration, no-marker theorem, matter functor and flux ownership proofs",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAN2635_1_no_extension",
            "source_ids": "SRC2635_02_423;SRC2635_04_965;SRC2635_13_2623",
            "candidate_claim": "Q_MTS is free/minimal/primitive and forbids Q_tilde=(Q,m)/G_rel",
            "review_result": "NOT_DERIVED_LIVE_COUNTERMODEL",
            "why_not_claim_grade": "all reviewed sources retain covariant material marker extensions and local invariant generators",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAN2635_2_no_marker_functor",
            "source_ids": "SRC2635_03_573;SRC2635_05_980;SRC2635_08_1676",
            "candidate_claim": "no nonconstant natural local marker/source functor exists",
            "review_result": "REJECTED_OR_REDUCED_TO_TRIVIALITY",
            "why_not_claim_grade": "980 proves one untrivialized invariant scalar can generate a forbidden continuous sector functor",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAN2635_3_sorted_grammar",
            "source_ids": "SRC2635_06_1237",
            "candidate_claim": "MTS primitives derive sorted parent action grammar",
            "review_result": "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED",
            "why_not_claim_grade": "motion-load/observer scaffolding is partial and does not derive hidden-visible coefficient exclusion",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAN2635_4_wider_scan",
            "source_ids": "SRC2635_09_1982;SRC2635_10_1983;SRC2635_11_2458",
            "candidate_claim": "wider corpus contains a claim-grade parent action signature",
            "review_result": "NO_PROMOTED_SOURCE",
            "why_not_claim_grade": "scans found partial/conditional hits only and explicitly promoted zero sources",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAN2635_5_parent_domain",
            "source_ids": "SRC2635_14_2625",
            "candidate_claim": "closed Conf_parent/Args(S_parent) certificate excluding readout/projector/marker inputs",
            "review_result": "CERTIFICATE_DOES_NOT_CLOSE",
            "why_not_claim_grade": "readout-zero is closure discipline only; field list and no-extension remain unsigned",
            "promote_to_theorem": "False",
            "valid_for_claim": "False",
        },
    ]


def source_hunt_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "SHV2635_0_overall",
            "question": "Does the current reviewed corpus contain a source-backed universal-property/no-extension theorem for Q_MTS?",
            "answer": "NO_CLAIM_GRADE_SOURCE_FOUND",
            "evidence_basis": "407,423,573,965,980,1237,1513,1676,1982,1983,2458,2609,2623,2625,2634",
            "consequence": "universal-property route is frozen as axiom/closure unless genuinely new source evidence appears",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "SHV2635_1_partial_gain",
            "question": "Did the hunt find useful theorem pieces?",
            "answer": "YES_CONDITIONAL_PIECES_ONLY",
            "evidence_basis": "fixed spurion exclusion, readout-after-variation no-cheat, scalar obstruction lemma, generator list",
            "consequence": "these pieces guide generator eliminations but do not derive local GR",
            "valid_for_claim": "False",
        },
        {
            "verdict_id": "SHV2635_2_repetition_guard",
            "question": "Should the global universal-property proof be retried immediately?",
            "answer": "NO_WITHOUT_NEW_SOURCE",
            "evidence_basis": "same failure appears across early, historical, current and wider-corpus scans",
            "consequence": "next work must be generator-by-generator theorem-zero or source-backed residual rows",
            "valid_for_claim": "False",
        },
    ]


def axiom_freeze_rows() -> list[dict[str, Any]]:
    return [
        {
            "freeze_id": "AX2635_0_universal_property",
            "frozen_statement": "Q_MTS is primitive-minimal/free and forbids material marker extensions",
            "status": "AXIOM_ONLY_NOT_THEOREM",
            "allowed_use": "may be labelled as a private closure/axiom branch only",
            "forbidden_use": "may not zero residuals, claim local GR, or promote PPN/R10/WEP rows",
            "thaw_condition": "new source-backed proof of category, morphisms, initial/free object and no-natural-marker functor",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "AX2635_1_no_marker_functor",
            "frozen_statement": "all natural local marker/sector functors are constant",
            "status": "REJECTED_AS_GLOBAL_CURRENT_THEOREM",
            "allowed_use": "narrow discrete/connected branch may be tried separately",
            "forbidden_use": "may not suppress continuous constants, species weights or source coefficients globally",
            "thaw_condition": "local invariant algebra triviality or generator-specific theorem",
            "valid_for_claim": "False",
        },
        {
            "freeze_id": "AX2635_2_readout_domain",
            "frozen_statement": "readout/projector/fitted masks are absent from S_parent before variation",
            "status": "CLOSURE_DISCIPLINE_NOT_GLOBAL_CERTIFICATE",
            "allowed_use": "blocks reduced-action laundering in private ledgers",
            "forbidden_use": "may not count as projector theorem-zero without field-domain certificate",
            "thaw_condition": "closed Conf_parent/Args(S_parent) certificate",
            "valid_for_claim": "False",
        },
    ]


def generator_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": "1",
            "generator_id": "GEN2635_0_readout_projector",
            "current_status": "CLOSURE_DISCIPLINED_NOT_THEOREM_ZERO",
            "best_next_attack": "source E_readout_total residual or prove closed parent-domain certificate",
            "test_arenas": "PPN;WEP;R10;clocks;orbital",
            "valid_for_claim": "False",
        },
        {
            "priority": "2",
            "generator_id": "GEN2635_1_continuous_marker_scalar",
            "current_status": "OBSTRUCTION_PROVED_IF_INVARIANT_SCALAR_SURVIVES",
            "best_next_attack": "identify each surviving scalar and either theorem-zero it or give coefficient/source-bound row",
            "test_arenas": "PPN;R10;clocks;WEP",
            "valid_for_claim": "False",
        },
        {
            "priority": "3",
            "generator_id": "GEN2635_2_species_constants_source_weights",
            "current_status": "UNIVERSALITY_NOT_PARENT_DERIVED",
            "best_next_attack": "derive one shared matter/source functional or source finite species-weight priors",
            "test_arenas": "WEP;clock;source_normalization;PPN",
            "valid_for_claim": "False",
        },
        {
            "priority": "4",
            "generator_id": "GEN2635_3_integrated_out_tower",
            "current_status": "NO_TOWER_THEOREM_NOT_DERIVED",
            "best_next_attack": "sector Hessian/source-independent solution audit or operator coefficient bounds",
            "test_arenas": "PPN;R10;orbital;local_GR",
            "valid_for_claim": "False",
        },
        {
            "priority": "5",
            "generator_id": "GEN2635_4_domain_boundary_topology",
            "current_status": "CONDITIONALLY_SAFE_NOT_DERIVED",
            "best_next_attack": "prove stress-free/no-flux/topological silence or source class-leak residuals",
            "test_arenas": "orbital;R10;PPN;cosmology_local_split",
            "valid_for_claim": "False",
        },
    ]


def effective_pack_rows() -> list[dict[str, Any]]:
    symbols = [
        ("EFFP2635_0", "e_EH_import", "EH import residual", "operator/local_GR"),
        ("EFFP2635_1", "e_kappaG", "parent-to-measured-G coupling residual", "Newton/orbital"),
        ("EFFP2635_2", "DeltaE_MTS", "non-EH local operator residual", "PPN/R10/orbital"),
        ("EFFP2635_3", "E_readout_total", "readout/reduced-action backreaction residual", "PPN/WEP/R10"),
        ("EFFP2635_4", "DObs_e_R", "observed coframe/readout leak", "PPN/clocks/orbital"),
        ("EFFP2635_5", "b_R;d_R;w_R;epsilon_endpoint_R", "common-frame/no-shadow residuals", "PPN/clocks/WEP"),
        ("EFFP2635_6", "Delta_PPN_abs", "componentwise no-cancellation local PPN envelope", "PPN"),
    ]
    return [
        {
            "pack_id": pack_id,
            "symbol": symbol,
            "role": role,
            "arena": arena,
            "required_before_scoring": "theorem-zero or numeric value with units, source path, projection kernel, baseline and no-cancellation rule",
            "valid_for_claim": "False",
        }
        for pack_id, symbol, role, arena in symbols
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2635_0_internal", "claim": "2635 may guide private route selection", "status": "ALLOW_INTERNAL_NONCLAIM", "passed": "True", "claim_allowed": "False", "valid_for_claim": "False"},
        {"gate_id": "CG2635_1_universal_property", "claim": "Q_MTS universal-property/no-extension theorem is source-backed", "status": "BLOCKED", "passed": "False", "claim_allowed": "False", "valid_for_claim": "False"},
        {"gate_id": "CG2635_2_axiom_counts_as_derivation", "claim": "axiom/closure route counts as derived local GR", "status": "FORBIDDEN", "passed": "False", "claim_allowed": "False", "valid_for_claim": "False"},
        {"gate_id": "CG2635_3_effective_tests_ready", "claim": "effective residual branch is ready to score", "status": "BLOCKED_RESIDUAL_INPUTS_MISSING", "passed": "False", "claim_allowed": "False", "valid_for_claim": "False"},
        {"gate_id": "CG2635_4_local_GR", "claim": "MTS derives local GR/Newton/PPN", "status": "BLOCKED", "passed": "False", "claim_allowed": "False", "valid_for_claim": "False"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2635_0_source_hunt",
            "decision": "NO_CLAIM_GRADE_UNIVERSAL_PROPERTY_SOURCE_FOUND",
            "reason": "all reviewed candidates are sketches, conditional contracts, explicit failures, obstruction lemmas, or partial signature hits",
            "consequence": "do not repeat the global proof hunt without new evidence",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2635_1_freeze",
            "decision": "UNIVERSAL_PROPERTY_ROUTE_FROZEN_AS_AXIOM_ONLY",
            "reason": "using it as a theorem would falsely erase live marker/tower/readout countermodels",
            "consequence": "if used, label as axiom/closure branch only",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2635_2_next",
            "decision": "MOVE_TO_GENERATOR_ELIMINATION_OR_EFFECTIVE_RESIDUAL_PACK",
            "reason": "the remaining work is now finite: eliminate named generators or source explicit residual rows",
            "consequence": "2636 should build the generator/residual priority runner rather than circle minimality language",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2636-Y5-R2FR-generator-elimination-priority-or-effective-GR-residual-vector-source-pack.md",
            "script": "scripts/Y5_R2FR_generator_elimination_priority_or_effective_GR_residual_vector_source_pack_2636.py",
            "objective": "turn the frozen universal-property gap into action: rank the surviving generators, attempt theorem-zero only where a source-backed route exists, and otherwise seed the effective GR residual vector with source-required rows before local testing",
            "include": "2635 generator queue; 2623 generator list; 2625 readout residual template; 2633/2634 residual vectors; 2489/2631 full PPN vector",
            "exclude": "global universal-property retry without new source, axiom counted as derivation, gamma-only pass, fitted GM, public claim",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2635_verdict", OUTPUTS["source_hunt_verdict"], LOCAL_BOUNDS / "Universal_property_source_hunt_verdict_2635_NONCLAIM.csv"),
        ("COPY2635_axiom", OUTPUTS["axiom_freeze"], LOCAL_BOUNDS / "Universal_property_axiom_freeze_2635_NONCLAIM.csv"),
        ("COPY2635_queue", OUTPUTS["generator_queue"], LOCAL_BOUNDS / "Generator_elimination_queue_2635_NONCLAIM.csv"),
        ("COPY2635_effective", OUTPUTS["effective_pack"], LOCAL_BOUNDS / "Effective_residual_pack_seed_2635_NONCLAIM.csv"),
        ("COPY2635_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2635_GENERATOR_ELIMINATION_OR_EFFECTIVE_PACK_NEXT.csv"),
    ]
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in pairs
    ]


def copy_branch_artifacts() -> None:
    copies = [
        (OUTPUTS["source_hunt_verdict"], LOCAL_BOUNDS / "Universal_property_source_hunt_verdict_2635_NONCLAIM.csv"),
        (OUTPUTS["axiom_freeze"], LOCAL_BOUNDS / "Universal_property_axiom_freeze_2635_NONCLAIM.csv"),
        (OUTPUTS["generator_queue"], LOCAL_BOUNDS / "Generator_elimination_queue_2635_NONCLAIM.csv"),
        (OUTPUTS["effective_pack"], LOCAL_BOUNDS / "Effective_residual_pack_seed_2635_NONCLAIM.csv"),
        (OUTPUTS["next_target"], RAB_QUEUE / "JR2635_GENERATOR_ELIMINATION_OR_EFFECTIVE_PACK_NEXT.csv"),
    ]
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def formalization_has_2635_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and ("2635" in path.name or "UNIVERSAL_PROPERTY_HUNT_2635" in path.name):
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [
        LOCAL_BOUNDS / "Universal_property_source_hunt_verdict_2635_NONCLAIM.csv",
        LOCAL_BOUNDS / "Universal_property_axiom_freeze_2635_NONCLAIM.csv",
        LOCAL_BOUNDS / "Generator_elimination_queue_2635_NONCLAIM.csv",
        LOCAL_BOUNDS / "Effective_residual_pack_seed_2635_NONCLAIM.csv",
        RAB_QUEUE / "JR2635_GENERATOR_ELIMINATION_OR_EFFECTIVE_PACK_NEXT.csv",
    ]
    checks = [
        ("VAL2635_00_sources", all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]), "all cited source paths exist and required needles are present"),
        ("VAL2635_01_no_promotion", all(row["promote_to_theorem"] == "False" for row in generated["candidate_review"]), "no candidate source is promoted to theorem"),
        ("VAL2635_02_verdict", any(row["answer"] == "NO_CLAIM_GRADE_SOURCE_FOUND" for row in generated["source_hunt_verdict"]), "source hunt records no claim-grade universal-property source"),
        ("VAL2635_03_axiom_freeze", any(row["status"] == "AXIOM_ONLY_NOT_THEOREM" for row in generated["axiom_freeze"]), "universal-property route frozen as axiom-only"),
        ("VAL2635_04_generator_queue", len(generated["generator_queue"]) >= 5, "generator elimination queue is written"),
        ("VAL2635_05_effective_pack", any(row["symbol"] == "Delta_PPN_abs" for row in generated["effective_pack"]), "effective residual pack includes full PPN absolute envelope"),
        ("VAL2635_06_claim_gates", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]), "no claim gate promotes local GR or effective tests"),
        ("VAL2635_07_next_target", any(row["selected"] == "True" and row["next_target"].startswith("2636-Y5-R2FR-generator") for row in generated["next_target"]), "2636 generator/effective residual target selected"),
        ("VAL2635_08_branch_copies", all(path.exists() and csv_parses(path) for path in copy_paths), "nonclaim branch copies and acquisition queue exist and parse"),
        ("VAL2635_09_csv_parse", all(path.exists() and csv_parses(path) for path in output_csvs), "all generated 2635 CSVs parse"),
        ("VAL2635_10_formalization_untouched", not formalization_has_2635_outputs(), "no 2635 outputs are written under formalization-workbench"),
        ("VAL2635_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append({"check_id": "VAL2635_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "2635 universal-property source hunt and axiom/effective route freeze", "valid_for_claim": "False"})
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2635 - Y5 R2/f(R) Universal-Property Source Hunt Or Effective Residual Branch Freeze",
        "",
        "Status: `Y5_R2FR_2635_no_claim_grade_universal_property_source_found_axiom_only_freeze_effective_residual_route_selected_nonclaim`",
        "",
        "Claim ceiling: no universal-property theorem, no no-extension theorem, no no-marker theorem, no local-GR/Newton proof, no PPN/WEP/R10 pass, no effective-residual scoring, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2635 performs the promised focused source hunt. The result is hard but useful: the reviewed corpus does not contain a claim-grade proof that `Q_MTS` is primitive-minimal/free/initial or that material marker extensions are forbidden. Every strong source is either a sketch, a conditional contract, an explicit failure, an obstruction lemma, or a partial signature hit.",
        "",
        "That freezes the global universal-property route as axiom-only unless genuinely new source evidence appears. The theory work now has to move by generator elimination or by an honest effective GR-plus-residual vector.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Candidate Review",
        md_table(generated["candidate_review"]),
        "",
        "## Source-Hunt Verdict",
        md_table(generated["source_hunt_verdict"]),
        "",
        "## Axiom Freeze Gate",
        md_table(generated["axiom_freeze"]),
        "",
        "## Generator Elimination Queue",
        md_table(generated["generator_queue"]),
        "",
        "## Effective Residual Pack Seed",
        md_table(generated["effective_pack"]),
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
        "This stops the loop. We looked for the missing keystone and did not find a derivation-grade source. So the universal-property route is not dead, but it is frozen as axiom-only until new evidence appears.",
        "",
        "The best next move is practical and still derivation-first: attack the named generators one by one, and wherever a theorem-zero cannot be sourced, seed the effective residual vector with units, source paths, arena projections, baselines and no-cancellation guards. That gets us closer to real testing without lying about GR being derived yet.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "candidate_review": candidate_review_rows(),
        "source_hunt_verdict": source_hunt_verdict_rows(),
        "axiom_freeze": axiom_freeze_rows(),
        "generator_queue": generator_queue_rows(),
        "effective_pack": effective_pack_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in generated.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
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
