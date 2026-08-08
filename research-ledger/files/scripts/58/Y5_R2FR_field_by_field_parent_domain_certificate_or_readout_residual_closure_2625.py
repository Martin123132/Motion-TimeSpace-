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
DOC_PATH = ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md"

PREFIX = "P8_Y5_PARENT_DOMAIN_CERT_2625"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "field_certificate": RESIDUALS / f"{PREFIX}_FIELD_BY_FIELD_CERTIFICATE_ATTEMPT.csv",
    "action_arguments": RESIDUALS / f"{PREFIX}_S_PARENT_ARGUMENT_AUDIT.csv",
    "readout_exclusion": RESIDUALS / f"{PREFIX}_READOUT_EXCLUSION_CERTIFICATE.csv",
    "closure_policy": RESIDUALS / f"{PREFIX}_READOUT_CLOSURE_POLICY.csv",
    "residual_template": RESIDUALS / f"{PREFIX}_READOUT_RESIDUAL_TEMPLATE.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2625_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2625_00_2624_handoff_doc",
        "description": "2624 selects field-by-field parent-domain certificate",
        "path": ROOT / "2624-Y5-R2FR-readout-after-variation-parent-schema-theorem-or-generator-residual-bound.md",
        "needles": ["NEXT2624_0_primary", "FIELD_BY_FIELD_PARENT_DOMAIN_CERTIFICATE_IS_NEXT", "PDS2624_6_current_verdict"],
    },
    {
        "source_id": "SRC2625_01_2624_validation",
        "description": "2624 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2624_VALIDATION.csv",
        "needles": ["VAL2624_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2625_02_2624_parent_domain",
        "description": "2624 parent-domain audit",
        "path": RESIDUALS / "P8_Y5_READOUT_SCHEMA_GATE_2624_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
        "needles": ["PDS2624_0_conf_parent_field_list", "PDS2624_6_current_verdict"],
    },
    {
        "source_id": "SRC2625_03_407_parent_sketch",
        "description": "primitive relational quotient/readout parent-action sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needles": ["configuration_space_sketch_written", "readout_projection", "S_readout_observables"],
    },
    {
        "source_id": "SRC2625_04_410_functor",
        "description": "quotient matter functor theorem attempt and reduced readout counterexample",
        "path": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": ["parent quotient object", "reduced_readout_EFT", "quotient_matter_functor_parent_derived"],
    },
    {
        "source_id": "SRC2625_05_422_no_cheat",
        "description": "matter/readout no-cheat theorem contract",
        "path": ROOT / "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "needles": ["readout_after_variation_contract_written", "parent_factorization_derived", "post_readout_EFT_action"],
    },
    {
        "source_id": "SRC2625_06_968_domain",
        "description": "historical parent-domain signature audit",
        "path": ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        "needles": ["PDS968_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS", "REC968_5_verdict"],
    },
    {
        "source_id": "SRC2625_07_967_readout",
        "description": "historical readout schema theorem",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": ["RAV967_5_verdict", "CONDITIONAL_SCHEMA_THEOREM_WRITTEN_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC2625_08_423_minimality",
        "description": "parent-action minimality/no-extension blocker",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": ["closed_parent_field_list", "parent_universal_property_derived", "post_readout_EFT"],
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
            "lineage_id": "LIN2625_0_current_handoff",
            "input_checkpoint": "2624",
            "what_it_gave": "clean readout theorem shape plus parent-domain blocker",
            "current_use": "source-check the actual parent field/action domain",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2625_1_parent_sketch",
            "input_checkpoint": "407",
            "what_it_gave": "candidate parent configuration/action sketch with readout listed as observable/readout only",
            "current_use": "candidate evidence for exclusion, not a closed certificate",
            "claim_status": "sketch_not_theorem",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2625_2_no_cheat",
            "input_checkpoint": "422/967/968",
            "what_it_gave": "readout-after-variation rule and exact exclusion clause",
            "current_use": "install closure discipline while theorem-zero stays blocked",
            "claim_status": "contract_ready_parent_unsigned",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2625_3_minimality_blocker",
            "input_checkpoint": "423/410",
            "what_it_gave": "reduced readout EFT and marker extensions remain legal without universal-property/minimality theorem",
            "current_use": "retain countermodels and variation-tax policy",
            "claim_status": "countermodels_retained",
            "valid_for_claim": False,
        },
    ]


def field_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "FDC2625_0_target",
            "certificate_piece": "field-by-field parent-domain certificate",
            "requirement": "every Conf_parent field and every S_parent argument is listed with source path; no P_read/R_read/fitted mask/section appears as a variational argument",
            "current_status": "CERTIFICATE_ATTEMPT_WRITTEN",
            "evidence_status": "source-backed inventory exists only as sketch/contract",
            "claim_effect": "no theorem-zero credit yet",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "FDC2625_1_conf_parent_closed",
            "certificate_piece": "closed Conf_parent field list",
            "requirement": "parent configuration object is closed and not extendable by marker/readout fields",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence_status": "407 sketches configuration objects; 423 says closed_parent_field_list is contract_only",
            "claim_effect": "readout exclusion cannot be corpus-wide theorem-zero",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "FDC2625_2_S_parent_arguments_closed",
            "certificate_piece": "closed S_parent argument list",
            "requirement": "S_parent arguments are exhausted before variation",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence_status": "407 lists action blocks but does not prove closure or no-extension",
            "claim_effect": "delta S/delta P_read absence remains conditional",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "FDC2625_3_readout_excluded",
            "certificate_piece": "P_read/R_read excluded from parent variation",
            "requirement": "readout exists only as R_read:Sol(S_parent)->Obs after variation",
            "current_status": "CLOSURE_CERTIFICATE_READY_NOT_DERIVATION",
            "evidence_status": "407 and 422 support the rule; 968 says certificate ready only as contract",
            "claim_effect": "discipline contract can be used privately, but generator remains conditional",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "FDC2625_4_reduced_actions_demoted",
            "certificate_piece": "readout/reduced EFT variation tax",
            "requirement": "any varied S_red[g,P_read] is a retained branch, not parent theorem-zero",
            "current_status": "POLICY_GUARDRAIL_SIGNED_FOR_THIS_WORKBENCH",
            "evidence_status": "422, 423, 967, and 968 all retain post-readout/reduced EFT countermodels",
            "claim_effect": "prevents fake pass but does not derive absence",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "FDC2625_5_current_verdict",
            "certificate_piece": "readout generator removal",
            "requirement": "field-domain certificate closes all rows FDC2625_1..4",
            "current_status": "READOUT_ZERO_DEMOTED_TO_EXPLICIT_CLOSURE",
            "evidence_status": "not enough evidence for theorem-zero; enough for explicit nonclaim closure and residual template",
            "claim_effect": "no readout projector theorem-zero or local-GR claim",
            "valid_for_claim": False,
        },
    ]


def action_argument_rows() -> list[dict[str, Any]]:
    return [
        {
            "argument_id": "ARG2625_0_observed_geometry",
            "candidate_argument": "observed metric/coframe e_obs or g_munu",
            "source_evidence": "407 S_geom_same_frame conditional_not_derived",
            "domain_status": "PARENT_ARGUMENT_CANDIDATE",
            "readout_like": False,
            "open_issue": "same-frame EH/source still conditional",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_1_relational_MTS_state",
            "candidate_argument": "relational MTS state / quotient variables",
            "source_evidence": "407 relational_MTS_state true, G_rel not yet formalized",
            "domain_status": "PARENT_ARGUMENT_CANDIDATE_SKETCHED",
            "readout_like": False,
            "open_issue": "parent symmetry/object not fully formalized",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_2_boundary_domain_class",
            "candidate_argument": "boundary/domain class",
            "source_evidence": "407 boundary_domain_class true; 2623 domain class retained",
            "domain_status": "PARENT_OR_BOUNDARY_ARGUMENT_RETAINED",
            "readout_like": False,
            "open_issue": "relative/domain class can become selector if not closed",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_3_matter_fields",
            "candidate_argument": "ordinary matter fields Psi",
            "source_evidence": "407 S_matter_quotient_functor sufficient_axiom_not_derived; 410 matter factorization open",
            "domain_status": "PARENT_ARGUMENT_CANDIDATE",
            "readout_like": False,
            "open_issue": "matter quotient functor/factorization not parent-derived",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_4_finite_cell_fibre",
            "candidate_argument": "finite-cell fibre h or spectrum",
            "source_evidence": "407 finite_cell_fibre true; 422 finite_fibre_blindness not derived",
            "domain_status": "RETAINED_UNRESOLVED_GENERATOR",
            "readout_like": False,
            "open_issue": "can become matter-visible scalar/source dial",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_5_readout_projection",
            "candidate_argument": "R_read/P_read/P_active/fitted masks",
            "source_evidence": "407 readout_projection observable/readout only false; 968 readout certificate contract not derivation",
            "domain_status": "EXCLUDED_BY_CLOSURE_NOT_BY_PARENT_THEOREM",
            "readout_like": True,
            "open_issue": "must be excluded by closed Conf_parent/S_parent certificate to earn theorem-zero",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_6_marker_extension",
            "candidate_argument": "material marker extension m",
            "source_evidence": "423 material marker extension not blocked; 2623 marker countermodels retained",
            "domain_status": "LEGAL_COUNTERMODEL_UNLESS_NO_EXTENSION_SIGNED",
            "readout_like": True,
            "open_issue": "readout theorem cannot remove a marker that enters before variation",
            "valid_for_claim": False,
        },
        {
            "argument_id": "ARG2625_7_verdict",
            "candidate_argument": "S_parent argument closure",
            "source_evidence": "all sources",
            "domain_status": "NOT_CLOSED_CURRENT_CORPUS",
            "readout_like": True,
            "open_issue": "one readout-like class is closure-excluded, but marker/reduced-action loopholes remain",
            "valid_for_claim": False,
        },
    ]


def readout_exclusion_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "REC2625_0_parent_domain_clause",
            "clause": "Conf_parent excludes P_read, R_read, fitted masks, post-solution sections, and readout-selected active blocks",
            "current_status": "CANDIDATE_CLAUSE_READY",
            "scope": "private closure discipline unless parent universal-property theorem closes",
            "valid_for_claim": False,
        },
        {
            "clause_id": "REC2625_1_solution_space_readout",
            "clause": "R_read is a map Sol(S_parent)->Obs and has no Euler-Lagrange equation",
            "current_status": "CANDIDATE_CLAUSE_READY",
            "scope": "valid conditional theorem shape",
            "valid_for_claim": False,
        },
        {
            "clause_id": "REC2625_2_reduced_action_tax",
            "clause": "If a readout-reduced functional is varied, it defines a retained EFT branch",
            "current_status": "POLICY_GUARDRAIL_READY",
            "scope": "prevents reduced-action theorem-zero laundering",
            "valid_for_claim": False,
        },
        {
            "clause_id": "REC2625_3_apparatus_clause",
            "clause": "Physical measuring devices are ordinary matter sources before variation or nonbackreacting probes after variation",
            "current_status": "CANDIDATE_CLAUSE_READY",
            "scope": "classification guard",
            "valid_for_claim": False,
        },
        {
            "clause_id": "REC2625_4_hidden_marker_clause",
            "clause": "No material marker, boundary class, domain selector, or species label may be reintroduced by renaming it as readout data",
            "current_status": "BLOCKED_BY_NO_MARKER_THEOREM",
            "scope": "requires primitive/no-natural-marker lock",
            "valid_for_claim": False,
        },
        {
            "clause_id": "REC2625_5_verdict",
            "clause": "Readout exclusion certificate",
            "current_status": "INSTALLED_AS_EXPLICIT_CLOSURE_NOT_DERIVATION",
            "scope": "usable private discipline contract, not local-GR theorem",
            "valid_for_claim": False,
        },
    ]


def closure_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "POL2625_0_no_theorem_zero_credit",
            "policy": "readout-zero is closure-only until field-domain certificate closes",
            "reason": "source evidence is sketch/contract, not proof of closed parent domain",
            "effect": "all projector-zero rows remain valid_for_claim=false",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2625_1_reduced_action_retention",
            "policy": "varied S_red[g,P_read] is a retained branch",
            "reason": "reduced action can generate real Euler terms",
            "effect": "E_readout_total residual template stays live",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2625_2_readout_not_matter_probe",
            "policy": "real apparatus stress is ordinary matter before variation",
            "reason": "avoids confusing nonbackreacting observational readout with physical probe source",
            "effect": "apparatus/probe rows cannot be claimed silent by readout clause alone",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2625_3_marker_not_renamed_readout",
            "policy": "pre-variation markers cannot be hidden as readout labels",
            "reason": "readout theorem only removes post-solution maps",
            "effect": "primitive no-marker branch remains open",
            "valid_for_claim": False,
        },
    ]


def residual_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RRT2625_0_E_readout_total",
            "symbol": "E_readout_total",
            "definition": "delta S_red[g,P_read]/delta g or any equivalent readout-backreaction operator",
            "status": "RETAINED_IF_CLOSURE_FAILS",
            "needed_inputs": "S_red form, P_read definition, variation path, source/readout provenance",
            "observable_links": "PPN; R10; WEP/source; clocks; orbital mass readout",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RRT2625_1_projector_norm",
            "symbol": "||[nabla,P_read]||",
            "definition": "local projection/commutator leakage if projector is promoted to branch operator",
            "status": "MISSING_PROJECTOR_NORM",
            "needed_inputs": "projector definition, local domain, derivative operator, norm",
            "observable_links": "WEP; clocks; R10; source normalization",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RRT2625_2_marker_readout",
            "symbol": "E_marker_readout",
            "definition": "pre-variation marker hidden as readout label",
            "status": "BLOCKED_BY_NO_MARKER_THEOREM_MISSING",
            "needed_inputs": "primitive no-marker theorem or marker coupling coefficients",
            "observable_links": "WEP; PPN; clocks; R10",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RRT2625_3_nonclaim_lock",
            "symbol": "claim_allowed",
            "definition": "readout generator removal requires closed parent-domain certificate",
            "status": "NONCLAIM_LOCK",
            "needed_inputs": "FDC2625_1..4 all parent-signed",
            "observable_links": "all local arenas",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2625_0_sketch_not_closed_domain",
            "failure_mode": "parent sketch omits readout but does not prove the list is closed",
            "mathematical_form": "Conf_parent listed by sketch, but extension Conf_parent x P_read not theorem-forbidden",
            "retained": True,
            "why_survives": "407 is a sketch and 968 says parent-domain signature is not signed",
            "what_kills_it": "source-backed closed field-domain certificate",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2625_1_reduced_action_branch",
            "failure_mode": "readout-reduced functional is varied as a new EFT",
            "mathematical_form": "delta S_red[g,P_read]/delta g != 0",
            "retained": True,
            "why_survives": "policy demotes it but does not forbid its existence",
            "what_kills_it": "explicitly exclude from parent theorem-zero and carry residual",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2625_2_hidden_marker_as_readout",
            "failure_mode": "pre-variation material marker is renamed readout",
            "mathematical_form": "S_parent[g,m] followed by R_read(m)",
            "retained": True,
            "why_survives": "readout theorem cannot remove variables already in S_parent",
            "what_kills_it": "primitive no-natural-marker theorem",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2625_3_verdict",
            "failure_mode": "readout generator remains closure-only",
            "mathematical_form": "P_read excluded by discipline contract, not parent theorem",
            "retained": True,
            "why_survives": "field-by-field certificate does not close from current evidence",
            "what_kills_it": "future parent universal-property/domain theorem or explicit residual-bound branch",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2625_0_closed_parent_domain",
            "claim": "Conf_parent and S_parent field/action domain is closed",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_SKETCH_NOT_CLOSED_CERTIFICATE",
        },
        {
            "gate_id": "GATE2625_1_readout_generator_removed",
            "claim": "readout projector removed from local invariant algebra",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_READOUT_ZERO_DEMOTED_TO_CLOSURE",
        },
        {
            "gate_id": "GATE2625_2_projector_residual_bound",
            "claim": "projector residual numerically bounded",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PROJECTOR_NORM_AND_SRED_INPUTS_MISSING",
        },
        {
            "gate_id": "GATE2625_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_READOUT_AND_REMAINING_GENERATOR_GATES_OPEN",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2625_0_certificate_result",
            "decision": "FIELD_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE",
            "reason": "the corpus has a strong readout contract and parent sketch, but not a closed source-backed Conf_parent/S_parent argument theorem",
            "next_action": "use readout exclusion only as explicit nonclaim closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2625_1_readout_policy",
            "decision": "READOUT_ZERO_DEMOTED_TO_CLOSURE",
            "reason": "this blocks cheating while avoiding false theorem-zero credit",
            "next_action": "carry E_readout_total residual template for any varied reduced/readout branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2625_2_best_next",
            "decision": "PARENT_MEMORY_OPERATOR_OWNER_HUNT_IS_NEXT",
            "reason": "readout is now disciplined as closure; the next derivable generator route is the memory positive-operator lemma, which needs actual parent L_X and J_X owner rows",
            "next_action": "build 2626 parent memory operator owner hunt or demote memory to retained residual",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2625_0_primary",
            "selection_status": "selected",
            "target_doc": "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md",
            "target_script": "scripts/Y5_R2FR_parent_memory_operator_owner_hunt_or_memory_residual_template_2626.py",
            "objective": "hunt for an actual parent owner of the memory/class scalar operator L_X and source J_X; if no owner exists, demote memory scalar silence to retained residual inputs",
            "acceptance_gate": "parent X, selected local domain D, L_X form/sign, J_X source map, boundary/zero-mode data, and observable couplings are sourced or retained nonclaim",
            "claim_policy": "no memory zero, R10, PPN, clock, or local-GR claim without sourced operator inputs",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2625_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2626b-Y5-R2FR-readout-projector-residual-source-pack.md",
            "target_script": "scripts/Y5_R2FR_readout_projector_residual_source_pack_2626b.py",
            "objective": "source projector/readout residual rows if a concrete varied readout-reduced branch is kept",
            "acceptance_gate": "S_red, P_read, commutator norm, and observable maps have source paths and valid_for_claim=false until complete",
            "claim_policy": "fallback only; no invented projector coefficients",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "certificate": field_certificate_rows(),
        "arguments": action_argument_rows(),
        "readout": readout_exclusion_rows(),
        "policy": closure_policy_rows(),
        "residual": residual_template_rows(),
        "countermodel": countermodel_rows(),
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
        ("COPY2625_certificate", "field_certificate", OUTPUTS["field_certificate"], LOCAL_BOUNDS / "Field_by_field_parent_domain_certificate_2625_NONCLAIM.csv"),
        ("COPY2625_arguments", "action_arguments", OUTPUTS["action_arguments"], LOCAL_BOUNDS / "S_parent_argument_audit_2625_NONCLAIM.csv"),
        ("COPY2625_readout", "readout_exclusion", OUTPUTS["readout_exclusion"], LOCAL_BOUNDS / "Readout_exclusion_certificate_2625_NONCLAIM.csv"),
        ("COPY2625_residual", "residual_template", OUTPUTS["residual_template"], LOCAL_BOUNDS / "Readout_residual_template_2625_NONCLAIM.csv"),
        ("COPY2625_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2625_PARENT_MEMORY_OPERATOR_NEXT.csv"),
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


def certificate_attempt_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["certificate_id"] == "FDC2625_0_target" for row in rows_map["certificate"])


def certificate_not_closed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["certificate_id"] == "FDC2625_5_current_verdict"
        and row["current_status"] == "READOUT_ZERO_DEMOTED_TO_EXPLICIT_CLOSURE"
        for row in rows_map["certificate"]
    )


def readout_argument_audited(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["argument_id"] == "ARG2625_5_readout_projection"
        and row["domain_status"] == "EXCLUDED_BY_CLOSURE_NOT_BY_PARENT_THEOREM"
        for row in rows_map["arguments"]
    )


def marker_loophole_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["argument_id"] == "ARG2625_6_marker_extension"
        and row["domain_status"] == "LEGAL_COUNTERMODEL_UNLESS_NO_EXTENSION_SIGNED"
        for row in rows_map["arguments"]
    )


def closure_policy_installed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["clause_id"] == "REC2625_5_verdict"
        and row["current_status"] == "INSTALLED_AS_EXPLICIT_CLOSURE_NOT_DERIVATION"
        for row in rows_map["readout"]
    )


def residual_template_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return len(rows_map["residual"]) >= 4 and all(not bool(row["valid_for_claim"]) for row in rows_map["residual"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["countermodel_id"] == "CM2625_3_verdict" and bool(row["retained"]) for row in rows_map["countermodel"])


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
        row["decision_id"] == "DEC2625_2_best_next"
        and row["decision"] == "PARENT_MEMORY_OPERATOR_OWNER_HUNT_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["route_id"] == "NEXT2625_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"])


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2625*"))


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
        check_row("VAL2625_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2625_01_certificate_attempt", certificate_attempt_recorded(rows_map), "field-domain certificate attempt recorded", "certificate attempt missing"),
        check_row("VAL2625_02_certificate_not_closed", certificate_not_closed(rows_map), "certificate does not close; readout demoted to closure", "certificate incorrectly closed or verdict missing"),
        check_row("VAL2625_03_readout_argument_audited", readout_argument_audited(rows_map), "readout argument audited as closure-excluded", "readout argument row missing"),
        check_row("VAL2625_04_marker_loophole_retained", marker_loophole_retained(rows_map), "hidden marker loophole retained", "marker loophole missing or promoted"),
        check_row("VAL2625_05_closure_policy_installed", closure_policy_installed(rows_map), "readout closure policy installed as nonclaim", "closure policy missing"),
        check_row("VAL2625_06_residual_template_nonclaim", residual_template_nonclaim(rows_map), "readout residual template remains nonclaim", "residual template missing or promoted"),
        check_row("VAL2625_07_countermodel_retained", countermodel_retained(rows_map), "readout/domain countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2625_08_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2625_09_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2625_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2625_11_formalization_untouched", no_formalization_artifacts(), "no 2625 outputs found under formalization-workbench", "2625 outputs found under formalization-workbench"),
        check_row("VAL2625_12_decision_next", decision_next(rows_map), "decision selects parent memory operator owner hunt", "decision route missing"),
        check_row("VAL2625_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2625_14_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2625_15_csv_parse", csv_parse_all(), "all generated 2625 CSVs parse", "one or more generated 2625 CSVs fail to parse"),
        check_row("VAL2625_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2625_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2625 field-by-field parent-domain certificate or readout residual closure",
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
        "# 2625 - Field By Field Parent Domain Certificate Or Readout Residual Closure",
        "## Summary\n"
        "- 2625 source-checks the actual `Conf_parent` / `S_parent` domain needed to turn the readout theorem into a generator removal.\n"
        "- The certificate does not close from current evidence: sources show a strong sketch/contract, not a closed parent field/action theorem.\n"
        "- Readout-zero is therefore installed only as explicit private closure discipline; any varied readout/reduced action remains a nonclaim residual branch.\n"
        "- No local-GR, Newton, PPN, WEP, R10, readout-projector theorem-zero, or public claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Field By Field Certificate Attempt\n" + markdown_table(rows_map["certificate"], ["certificate_id", "certificate_piece", "requirement", "current_status", "evidence_status", "claim_effect"]),
        "## S Parent Argument Audit\n" + markdown_table(rows_map["arguments"], ["argument_id", "candidate_argument", "source_evidence", "domain_status", "readout_like", "open_issue"]),
        "## Readout Exclusion Certificate\n" + markdown_table(rows_map["readout"], ["clause_id", "clause", "current_status", "scope"]),
        "## Readout Closure Policy\n" + markdown_table(rows_map["policy"], ["policy_id", "policy", "reason", "effect"]),
        "## Readout Residual Template\n" + markdown_table(rows_map["residual"], ["residual_id", "symbol", "definition", "status", "needed_inputs", "observable_links"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is useful discipline, not theorem closure. The readout projector cannot be allowed to cheat through reduced actions anymore, but the parent-domain theorem still needs a stronger universal-property/field-list proof. Since readout is now closure-disciplined, the next derivation route is the memory positive-operator owner hunt.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["field_certificate"], rows_map["certificate"])
    write_csv(OUTPUTS["action_arguments"], rows_map["arguments"])
    write_csv(OUTPUTS["readout_exclusion"], rows_map["readout"])
    write_csv(OUTPUTS["closure_policy"], rows_map["policy"])
    write_csv(OUTPUTS["residual_template"], rows_map["residual"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2625 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
