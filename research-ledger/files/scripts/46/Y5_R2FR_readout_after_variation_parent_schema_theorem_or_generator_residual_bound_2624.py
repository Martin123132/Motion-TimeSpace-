from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2624-Y5-R2FR-readout-after-variation-parent-schema-theorem-or-generator-residual-bound.md"

PREFIX = "P8_Y5_READOUT_SCHEMA_GATE_2624"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "readout_theorem": RESIDUALS / f"{PREFIX}_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
    "parent_domain": RESIDUALS / f"{PREFIX}_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
    "reduced_action": RESIDUALS / f"{PREFIX}_REDUCED_ACTION_DEMOTION_LEDGER.csv",
    "residual_bound": RESIDUALS / f"{PREFIX}_PROJECTOR_RESIDUAL_BOUND_TEMPLATE.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "generator_transition": RESIDUALS / f"{PREFIX}_GENERATOR_TRANSITION_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2624_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2624_00_2623_handoff_doc",
        "description": "2623 selects readout-after-variation as first tactical generator lock",
        "path": ROOT / "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md",
        "needles": ["NEXT2623_0_primary", "READOUT_AFTER_VARIATION_PARENT_SCHEMA_IS_NEXT", "GEN2623_0_readout_projector"],
    },
    {
        "source_id": "SRC2624_01_2623_validation",
        "description": "2623 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2623_VALIDATION.csv",
        "needles": ["VAL2623_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2624_02_2623_marker_audit",
        "description": "2623 readout projector marker audit",
        "path": RESIDUALS / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_NATURAL_MARKER_AUDIT.csv",
        "needles": ["MRK2623_0_readout_projector", "CONDITIONAL_SCHEMA_THEOREM_READY_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC2624_03_967_readout_doc",
        "description": "historical readout-after-variation theorem attempt",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED", "DEC967_0_readout"],
    },
    {
        "source_id": "SRC2624_04_967_readout_csv",
        "description": "historical readout schema theorem CSV",
        "path": RESIDUALS / "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
        "needles": ["RAV967_0_domain_separation", "RAV967_5_verdict"],
    },
    {
        "source_id": "SRC2624_05_968_domain_doc",
        "description": "historical parent domain signature audit",
        "path": ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        "needles": ["PDS968_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS", "REC968_5_verdict"],
    },
    {
        "source_id": "SRC2624_06_968_domain_csv",
        "description": "historical parent domain signature CSV",
        "path": RESIDUALS / "P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
        "needles": ["PDS968_0_conf_parent_field_list", "PDS968_6_verdict"],
    },
    {
        "source_id": "SRC2624_07_422_no_cheat",
        "description": "original matter/readout no-cheat contract",
        "path": ROOT / "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "needles": ["readout_after_variation", "conditional_no_cheat_rule", "post_readout_EFT_action"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": exists,
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": False,
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2624_0_current_handoff",
            "input_checkpoint": "2623",
            "what_it_gave": "readout projector ranked as first tactical generator lock",
            "current_use": "attempt to remove that generator by parent-domain logic",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2624_1_readout_theorem",
            "input_checkpoint": "967",
            "what_it_gave": "conditional schema theorem: a non-argument of S_parent cannot vary",
            "current_use": "promote the clean logic into the current 26xx spine while checking parent signature",
            "claim_status": "conditional_schema_ready",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2624_2_domain_audit",
            "input_checkpoint": "968",
            "what_it_gave": "parent-domain signature was not signed; readout clause ready as contract",
            "current_use": "keep theorem-zero blocked unless Conf_parent/S_parent field list is closed",
            "claim_status": "parent_signature_missing",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2624_3_original_no_cheat",
            "input_checkpoint": "422",
            "what_it_gave": "readout-after-variation no-cheat contract and post-readout EFT countermodel",
            "current_use": "forbid reduced-action projector tricks from earning theorem-zero credit",
            "claim_status": "guardrail_imported",
            "valid_for_claim": False,
        },
    ]


def readout_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "RAV2624_0_domain_separation",
            "theorem_piece": "separate parent configuration, solution space, and observables",
            "formal_statement": "Conf_parent --EL--> Sol(S_parent) --R_read--> Obs",
            "status": "FORMAL_SCHEMA_CLEAN",
            "conditional_gain": "readout maps report observables after solving; they are not parent fields",
            "remaining_gap": "corpus must sign that every readout/projector obeys this separation",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RAV2624_1_no_variation_slot",
            "theorem_piece": "readout has no Euler-Lagrange variation",
            "formal_statement": "if P_read not in Args(S_parent), then delta S_parent/delta P_read is undefined/not a field equation",
            "status": "CONDITIONAL_THEOREM",
            "conditional_gain": "a genuine post-solution readout cannot source E_LHS or T_H",
            "remaining_gap": "need closed S_parent argument list excluding P_read, R_read, fitted masks, and active readout blocks",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RAV2624_2_order_of_operations",
            "theorem_piece": "variation before readout",
            "formal_statement": "delta S_parent=0 is solved before R_read is applied",
            "status": "CONDITIONAL_PASS",
            "conditional_gain": "readout changes the reporting map, not the parent equations",
            "remaining_gap": "published/reduced derivations must not sneak R_read back into the varied functional",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RAV2624_3_reduced_action_tax",
            "theorem_piece": "readout-reduced action demotion",
            "formal_statement": "if S_red[g,P_read] is varied, S_red is a retained EFT branch, not S_parent",
            "status": "GUARDRAIL_PASS_NOT_ELIMINATION",
            "conditional_gain": "prevents closure-zero from being mislabelled theorem-zero",
            "remaining_gap": "does not forbid a new EFT branch; it only demotes it to explicit residual testing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RAV2624_4_chain_rule_scope",
            "theorem_piece": "readout silence does not prove matter/source blindness",
            "formal_statement": "readout exclusion removes P_read variation only; it does not prove S_matter factors through geometry and universal constants",
            "status": "SCOPE_GUARD_RETAINED",
            "conditional_gain": "prevents overclaiming WEP/source/fibre/species results from readout alone",
            "remaining_gap": "matter factorization, species universality, finite-fibre blindness, and same-frame EH/source remain separate gates",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RAV2624_5_current_verdict",
            "theorem_piece": "readout projector generator elimination",
            "formal_statement": "P_read removed from I_loc(Q_MTS) iff parent domain excludes it and all reduced backreaction is demoted",
            "status": "CONDITIONAL_SCHEMA_THEOREM_NOT_PARENT_SIGNED",
            "conditional_gain": "the logical theorem is clean and ready to become a certificate",
            "remaining_gap": "current corpus still has contract/sketch, not closed parent-domain certificate",
            "valid_for_claim": False,
        },
    ]


def parent_domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "domain_id": "PDS2624_0_conf_parent_field_list",
            "signature_piece": "closed Conf_parent field list",
            "current_status": "SKETCH_EXISTS_NOT_CLOSED_SIGNATURE",
            "blocks": "readout exclusion cannot be corpus-wide theorem-zero",
            "next_action": "write a field-by-field parent-domain certificate or keep readout closure policy",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_1_S_parent_arguments",
            "signature_piece": "S_parent argument list",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "blocks": "delta S/delta P_read absence remains conditional",
            "next_action": "explicitly list every action argument and forbid P_read/R_read/masks/sections",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_2_readout_exclusion",
            "signature_piece": "P_read/R_read/P_active excluded from S_parent",
            "current_status": "RELATIVE_SCHEMA_THEOREM_AVAILABLE_PARENT_SIGNATURE_MISSING",
            "blocks": "post-readout projector generator not eliminated",
            "next_action": "promote as explicit parent-domain clause only if no contradictory source exists",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_3_no_reduced_EFT_backreaction",
            "signature_piece": "no reduced action theorem-zero credit",
            "current_status": "POLICY_GUARDRAIL_READY_NOT_DERIVATION",
            "blocks": "S_red can return projector terms as a new branch",
            "next_action": "demote every varied reduced/readout functional to retained residual rows",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_4_material_probe",
            "signature_piece": "measurement/probe apparatus distinction",
            "current_status": "CLASSIFICATION_WRITTEN_NOT_FULL_PARENT_CLAUSE",
            "blocks": "apparatus/source confusion can fake readout silence",
            "next_action": "include real apparatus stress in S_matter before variation or idealize after variation",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_5_hidden_marker_return",
            "signature_piece": "no hidden marker renamed as readout",
            "current_status": "NOT_SIGNED",
            "blocks": "domain separation does not remove a marker that enters before readout",
            "next_action": "needs primitive no-natural-marker theorem or retained residual",
            "valid_for_claim": False,
        },
        {
            "domain_id": "PDS2624_6_current_verdict",
            "signature_piece": "parent domain signature",
            "current_status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "blocks": "readout projector generator remains conditional closure, not theorem-zero",
            "next_action": "build a source-backed parent-domain certificate or carry projector residuals",
            "valid_for_claim": False,
        },
    ]


def reduced_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "RED2624_0_reduced_EFT",
            "branch": "varied readout-reduced action S_red[g,P_read]",
            "admissibility": "LEGAL_AS_NEW_EFT",
            "demotion_rule": "must not be counted as parent theorem-zero; retain projector-dependent Euler terms",
            "residual": "c_projector_or_E_readout",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RED2624_1_section_choice",
            "branch": "representative section s:Obs->Conf_parent varied as physical",
            "admissibility": "LIVE_IF_SECTION_BACKREACTS",
            "demotion_rule": "prove section is gauge/readout-only or pay variation tax",
            "residual": "section_backreaction_residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RED2624_2_material_probe",
            "branch": "probe/readout apparatus treated as source",
            "admissibility": "ORDINARY_MATTER_IF_REAL_APPARATUS",
            "demotion_rule": "include apparatus in S_matter before variation or idealize as nonbackreacting after variation",
            "residual": "apparatus_stress_residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RED2624_3_hidden_marker",
            "branch": "material marker renamed as readout label",
            "admissibility": "LIVE_WITHOUT_NO_MARKER_THEOREM",
            "demotion_rule": "domain separation cannot remove markers that enter S_parent before readout",
            "residual": "marker_readout_residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RED2624_4_verdict",
            "branch": "all reduced-action/readout-backreaction branches",
            "admissibility": "RETAINED_NONCLAIM_IF_VARIED",
            "demotion_rule": "every such branch is explicit modified-operator/source residual, never theorem-zero",
            "residual": "E_readout_total",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "PRB2624_0_E_readout_total",
            "symbol": "E_readout_total",
            "definition": "E_readout_total = delta S_red[g,P_read]/delta g or equivalent readout-backreaction operator",
            "units": "operator_dependent",
            "needed_inputs": "S_red form, P_read definition, variation path, source/readout provenance",
            "observable_links": "PPN, R10, WEP/source, orbital mass readout, clocks",
            "status": "NONCLAIM_BOUND_REQUIRED_IF_PARENT_DOMAIN_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "residual_id": "PRB2624_1_projector_commutator",
            "symbol": "||[nabla,P_read]||",
            "definition": "local commutator/projection leakage norm",
            "units": "inverse_length_or_operator_dependent",
            "needed_inputs": "projector definition, local domain, derivative operator, norm",
            "observable_links": "WEP, clocks, R10, source normalization",
            "status": "MISSING_PROJECTOR_NORM",
            "valid_for_claim": False,
        },
        {
            "residual_id": "PRB2624_2_section_backreaction",
            "symbol": "E_section",
            "definition": "Euler term induced by treating representative/readout section as physical",
            "units": "operator_dependent",
            "needed_inputs": "section map, gauge proof or variation tax",
            "observable_links": "PPN preferred-frame, source frame, boundary/domain tests",
            "status": "MISSING_SECTION_GAUGE_PROOF_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "residual_id": "PRB2624_3_claim_policy",
            "symbol": "claim_allowed",
            "definition": "readout/projector theorem-zero is false unless parent domain certificate closes",
            "units": "status",
            "needed_inputs": "PDS2624_0..6 all pass",
            "observable_links": "all local arenas",
            "status": "NONCLAIM_LOCK",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2624_0_reduced_EFT",
            "failure_mode": "readout projector returns via varied reduced action",
            "mathematical_form": "S_red[g,P_read] with delta S_red/delta g != 0",
            "retained": True,
            "why_survives": "parent-domain exclusion is not signed corpus-wide",
            "what_kills_it": "closed Conf_parent/S_parent domain certificate or retained residual branch",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2624_1_section_backreaction",
            "failure_mode": "representative section is varied as physical",
            "mathematical_form": "s:Obs->Conf_parent contributes delta s/delta g terms",
            "retained": True,
            "why_survives": "section gauge/readout-only proof is absent",
            "what_kills_it": "section is pure gauge/readout-only or explicit variation tax",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2624_2_hidden_marker",
            "failure_mode": "material marker is renamed readout but enters before variation",
            "mathematical_form": "S_parent[g,m] then R_read reports m as label",
            "retained": True,
            "why_survives": "readout theorem cannot remove pre-variation marker fields",
            "what_kills_it": "primitive no-natural-marker theorem",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2624_3_matter_probe",
            "failure_mode": "real apparatus/probe stress is mistaken for pure readout",
            "mathematical_form": "S_matter includes apparatus degrees of freedom",
            "retained": True,
            "why_survives": "apparatus classification is not a full parent clause",
            "what_kills_it": "include apparatus before variation or explicitly idealize nonbackreacting readout",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2624_4_verdict",
            "failure_mode": "readout generator not theorem-zero",
            "mathematical_form": "P_read excluded only by contract, not parent-domain proof",
            "retained": True,
            "why_survives": "2624 records conditional theorem but no closed parent action domain",
            "what_kills_it": "2625 field-by-field parent-domain certificate",
            "valid_for_claim": False,
        },
    ]


def generator_transition_rows() -> list[dict[str, Any]]:
    return [
        {
            "transition_id": "GTR2624_0_readout_projector",
            "generator": "post-readout projector",
            "before_status": "FIRST_TACTICAL_LOCK",
            "after_status": "CONDITIONAL_SCHEMA_READY_NOT_ELIMINATED",
            "reason": "logical theorem is clean but parent domain is not signed",
            "next_action": "field-by-field parent-domain certificate",
            "valid_for_claim": False,
        },
        {
            "transition_id": "GTR2624_1_species_constants",
            "generator": "species/source constants",
            "before_status": "retained",
            "after_status": "retained",
            "reason": "readout silence does not prove single matter functional or universality",
            "next_action": "matter/source schema later",
            "valid_for_claim": False,
        },
        {
            "transition_id": "GTR2624_2_memory_scalar",
            "generator": "memory/class scalar",
            "before_status": "retained",
            "after_status": "retained_with_positive_operator_route",
            "reason": "readout schema helps J_X no-readout-source premise, but parent L_X/J_X/boundary still missing",
            "next_action": "memory operator audit after domain certificate",
            "valid_for_claim": False,
        },
        {
            "transition_id": "GTR2624_3_local_invariant_algebra",
            "generator": "I_loc(Q_MTS)",
            "before_status": "not eliminated",
            "after_status": "not eliminated",
            "reason": "no generator is theorem-zero yet",
            "next_action": "remove or bound generators one by one",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2624_0_parent_domain",
            "claim": "parent action domain excludes readout variables",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_CLOSED_CONF_PARENT_S_PARENT_FIELD_LIST_MISSING",
        },
        {
            "gate_id": "GATE2624_1_readout_removed",
            "claim": "readout projector generator removed from I_loc",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_DOMAIN_SIGNATURE_NOT_SIGNED",
        },
        {
            "gate_id": "GATE2624_2_reduced_action_zero",
            "claim": "reduced action projector terms are theorem-zero",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_REDUCED_ACTIONS_DEMOTED_TO_RETAINED_BRANCHES",
        },
        {
            "gate_id": "GATE2624_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_READOUT_AND_OTHER_GENERATOR_GATES_OPEN",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2624_0_schema_result",
            "decision": "READOUT_THEOREM_CONDITIONAL_CLEAN",
            "reason": "a readout map on solution space cannot enter parent variation if it is not an action argument",
            "next_action": "use this as the exact theorem shape",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2624_1_parent_signature",
            "decision": "READOUT_PROJECTOR_NOT_THEOREM_ZERO_YET",
            "reason": "current evidence shows a parent-action sketch and no-extension guardrails, not a closed Conf_parent/S_parent certificate",
            "next_action": "do not remove the generator until the field-domain certificate is written and source-checked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2624_2_residual_policy",
            "decision": "REDUCED_ACTIONS_ARE_RETAINED_BRANCHES",
            "reason": "if a reduced/readout functional is varied, it defines a modified branch and must be bounded, not counted as proof",
            "next_action": "keep projector residual template active",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2624_3_best_next",
            "decision": "FIELD_BY_FIELD_PARENT_DOMAIN_CERTIFICATE_IS_NEXT",
            "reason": "this is the missing parent signature needed to turn the clean readout theorem into an actual generator removal",
            "next_action": "build 2625 parent-domain field-list certificate or keep readout as closure/residual",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2624_0_primary",
            "selection_status": "selected",
            "target_doc": "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
            "target_script": "scripts/Y5_R2FR_field_by_field_parent_domain_certificate_or_readout_residual_closure_2625.py",
            "objective": "write/source-check a field-by-field Conf_parent and S_parent argument certificate excluding P_read/R_read/fitted masks/sections from the parent variational domain, or demote readout-zero to explicit closure with residual rows",
            "acceptance_gate": "every parent action argument is listed with source path and no P_read-like argument appears; all reduced/readout functionals are explicitly retained nonclaim branches",
            "claim_policy": "no readout generator removal or local-GR claim unless the certificate closes",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2624_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2625b-Y5-R2FR-memory-positive-operator-input-audit-or-scalar-bound.md",
            "target_script": "scripts/Y5_R2FR_memory_positive_operator_input_audit_or_scalar_bound_2625b.py",
            "objective": "audit memory positive-operator inputs after readout/domain handling",
            "acceptance_gate": "L_X positivity, J_X=0, boundary/zero-mode data, and observable projections are source-backed or retained nonclaim",
            "claim_policy": "fallback only; no numeric memory bounds without sources",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "readout": readout_theorem_rows(),
        "domain": parent_domain_rows(),
        "reduced": reduced_action_rows(),
        "residual": residual_bound_rows(),
        "countermodel": countermodel_rows(),
        "transitions": generator_transition_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
        "branch_copies": [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_parse(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return True, sum(1 for _ in csv.DictReader(handle))
    except Exception:
        return False, 0


def copy_outputs() -> list[dict[str, Any]]:
    specs = [
        ("COPY2624_readout_theorem", "readout_theorem", OUTPUTS["readout_theorem"], LOCAL_BOUNDS / "Readout_schema_theorem_2624_NONCLAIM.csv"),
        ("COPY2624_parent_domain", "parent_domain", OUTPUTS["parent_domain"], LOCAL_BOUNDS / "Parent_domain_signature_audit_2624_NONCLAIM.csv"),
        ("COPY2624_reduced_action", "reduced_action", OUTPUTS["reduced_action"], LOCAL_BOUNDS / "Reduced_action_demotion_2624_NONCLAIM.csv"),
        ("COPY2624_projector_residual", "projector_residual", OUTPUTS["residual_bound"], LOCAL_BOUNDS / "Projector_residual_bound_template_2624_NONCLAIM.csv"),
        ("COPY2624_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2624_FIELD_BY_FIELD_PARENT_DOMAIN_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_key, source, target in specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        parsed, row_count = csv_parse(target)
        rows.append(
            {
                "copy_id": copy_id,
                "source_key": source_key,
                "copy_path": str(target),
                "copy_exists": target.exists(),
                "csv_parse": parsed,
                "row_count": row_count,
                "valid_for_claim": False,
            }
        )
    return rows


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["exists"] and row["needles_present"] for row in rows_map["sources"])


def readout_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "RAV2624_1_no_variation_slot"
        and row["status"] == "CONDITIONAL_THEOREM"
        for row in rows_map["readout"]
    )


def readout_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "RAV2624_5_current_verdict"
        and row["status"] == "CONDITIONAL_SCHEMA_THEOREM_NOT_PARENT_SIGNED"
        and not bool(row["valid_for_claim"])
        for row in rows_map["readout"]
    )


def parent_domain_not_signed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["domain_id"] == "PDS2624_6_current_verdict"
        and row["current_status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS"
        for row in rows_map["domain"]
    )


def reduced_actions_demoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["branch_id"] == "RED2624_4_verdict"
        and row["admissibility"] == "RETAINED_NONCLAIM_IF_VARIED"
        for row in rows_map["reduced"]
    )


def residual_template_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return len(rows_map["residual"]) >= 4 and all(not bool(row["valid_for_claim"]) for row in rows_map["residual"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["countermodel_id"] == "CM2624_4_verdict" and bool(row["retained"]) for row in rows_map["countermodel"])


def transitions_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["transition_id"] == "GTR2624_0_readout_projector"
        and row["after_status"] == "CONDITIONAL_SCHEMA_READY_NOT_ELIMINATED"
        for row in rows_map["transitions"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] == "BLOCKED" for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for field, value in row.items():
                if field in claim_like_keys and bool(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and bool(row.get("valid_for_claim", False)):
                return False
            if "MISSING_" in joined and str(row.get("current_status", "")).upper() == "READY":
                return False
    return True


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["decision_id"] == "DEC2624_3_best_next"
        and row["decision"] == "FIELD_BY_FIELD_PARENT_DOMAIN_CERTIFICATE_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["route_id"] == "NEXT2624_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"])


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2624*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def csv_parse_all() -> bool:
    return all(csv_parse(path)[0] for key, path in OUTPUTS.items() if key != "validation" and path.exists())


def branch_copies_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return bool(rows_map["branch_copies"]) and all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"])


def check_row(check_id: str, passed: bool, detail: str, blocker: str = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "PASS" if passed else "FAIL",
        "detail": detail if passed else blocker,
        "valid_for_claim": False,
    }


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        check_row("VAL2624_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2624_01_readout_theorem_recorded", readout_theorem_recorded(rows_map), "readout no-variation theorem recorded", "readout theorem row missing"),
        check_row("VAL2624_02_readout_not_promoted", readout_not_promoted(rows_map), "readout generator remains conditional/nonclaim", "readout generator was promoted"),
        check_row("VAL2624_03_parent_domain_not_signed", parent_domain_not_signed(rows_map), "parent domain signature remains unsigned", "parent domain incorrectly signed"),
        check_row("VAL2624_04_reduced_actions_demoted", reduced_actions_demoted(rows_map), "reduced actions demoted to retained branches", "reduced action demotion missing"),
        check_row("VAL2624_05_residual_template_nonclaim", residual_template_nonclaim(rows_map), "projector residual template remains nonclaim", "projector residual template missing or promoted"),
        check_row("VAL2624_06_countermodel_retained", countermodel_retained(rows_map), "readout countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2624_07_transitions_nonclaim", transitions_nonclaim(rows_map), "generator transition remains nonclaim", "generator transition missing or promoted"),
        check_row("VAL2624_08_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2624_09_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2624_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2624_11_formalization_untouched", no_formalization_artifacts(), "no 2624 outputs found under formalization-workbench", "2624 outputs found under formalization-workbench"),
        check_row("VAL2624_12_decision_next", decision_next(rows_map), "decision selects field-by-field parent-domain certificate", "decision route missing"),
        check_row("VAL2624_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2624_14_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2624_15_csv_parse", csv_parse_all(), "all generated 2624 CSVs parse", "one or more generated 2624 CSVs fail to parse"),
        check_row("VAL2624_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2624_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2624 readout after variation parent schema theorem or generator residual bound",
            "valid_for_claim": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    sections = [
        "# 2624 - Readout After Variation Parent Schema Theorem Or Generator Residual Bound",
        "## Summary\n"
        "- 2624 attacks the first ranked generator: the post-readout projector.\n"
        "- The theorem is mathematically clean: if `R_read: Sol(S_parent)->Obs` is only post-solution readout, it is not an argument of `S_parent` and cannot produce an Euler-Lagrange source.\n"
        "- Current evidence does not parent-sign the closed `Conf_parent` / `S_parent` domain certificate, so the generator is not theorem-zero yet.\n"
        "- Any varied readout-reduced action is demoted to a retained EFT/residual branch. No local-GR, Newton, PPN, WEP, R10, projector-zero, or public claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Readout Schema Theorem Attempt\n" + markdown_table(rows_map["readout"], ["theorem_id", "theorem_piece", "formal_statement", "status", "conditional_gain", "remaining_gap"]),
        "## Parent Domain Signature Audit\n" + markdown_table(rows_map["domain"], ["domain_id", "signature_piece", "current_status", "blocks", "next_action"]),
        "## Reduced Action Demotion Ledger\n" + markdown_table(rows_map["reduced"], ["branch_id", "branch", "admissibility", "demotion_rule", "residual"]),
        "## Projector Residual Bound Template\n" + markdown_table(rows_map["residual"], ["residual_id", "symbol", "definition", "units", "needed_inputs", "observable_links", "status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## Generator Transition Ledger\n" + markdown_table(rows_map["transitions"], ["transition_id", "generator", "before_status", "after_status", "reason", "next_action"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is a clean tactical gain, not a final removal. The readout projector now has a rigorous theorem shape and a strict no-cheat policy for reduced actions. But the parent field-domain certificate is still missing, so the generator remains conditional. The next step is field-by-field certification of `Conf_parent` and `S_parent` arguments.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["readout_theorem"], rows_map["readout"])
    write_csv(OUTPUTS["parent_domain"], rows_map["domain"])
    write_csv(OUTPUTS["reduced_action"], rows_map["reduced"])
    write_csv(OUTPUTS["residual_bound"], rows_map["residual"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["generator_transition"], rows_map["transitions"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2624 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
