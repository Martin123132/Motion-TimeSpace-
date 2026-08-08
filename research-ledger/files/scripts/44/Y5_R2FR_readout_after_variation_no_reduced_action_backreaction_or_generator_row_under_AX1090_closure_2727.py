from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2727-Y5-R2FR-readout-after-variation-no-reduced-action-backreaction-or-generator-row-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2727_SOURCE_REGISTER.csv",
    "schema_audit": RESIDUALS / "P8_Y5_R2FR_2727_READOUT_AFTER_VARIATION_SCHEMA_AUDIT.csv",
    "domain_signature": RESIDUALS / "P8_Y5_R2FR_2727_PARENT_DOMAIN_SIGNATURE_REQUIREMENTS.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2727_READOUT_REENTRY_COUNTERMODEL_LEDGER.csv",
    "residual_rows": RESIDUALS / "P8_Y5_R2FR_2727_READOUT_REENTRY_RESIDUAL_ROWS_NONCLAIM.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2727_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2727_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2727_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2727_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2727_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2727_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2727_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2727_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "readout_after_variation_generator_rows_2727_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "readout_after_variation_EJeff_update_2727_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2727_MEMORY_POSITIVE_OPERATOR_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2727_0_2726",
        "label": "2726 direct handoff",
        "path": ROOT / "2726-Y5-R2FR-parent-no-extension-minimality-and-LC-descent-or-Eoperator-bound-under-AX1090-closure.md",
        "needles": [
            "KS2726_0_readout_after_variation",
            "NER2726_2_E_readout_reentry",
            "NEXT2726_0_selected",
            "VAL2726_OVERALL",
        ],
        "use": "selects readout-after-variation as the next generator kill target",
    },
    {
        "source_id": "SRC2727_1_966",
        "label": "966 generator ranking",
        "path": ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md",
        "needles": [
            "GE966_0_readout_projector",
            "PTC966_0_readout_domain",
            "CGATE966_2_readout_projector",
            "DEC966_0_generator_audit",
        ],
        "use": "ranks readout projector as the smallest high-leverage generator lock",
    },
    {
        "source_id": "SRC2727_2_967",
        "label": "967 schema theorem",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": [
            "RAV967_0_domain_separation",
            "RAV967_1_no_variation_slot",
            "RAV967_5_verdict",
            "RCM967_0_reduced_EFT",
            "GTR967_0_readout_projector",
        ],
        "use": "proves the clean schema theorem conditionally and identifies reduced-EFT countermodel",
    },
    {
        "source_id": "SRC2727_3_968",
        "label": "968 parent-domain signature audit",
        "path": ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        "needles": [
            "PDS968_0_conf_parent_field_list",
            "PDS968_2_readout_exclusion",
            "PDS968_3_reduced_EFT_backreaction",
            "PDS968_6_verdict",
            "REC968_5_verdict",
            "DEC968_0_parent_domain",
        ],
        "use": "exact readout exclusion certificate is ready as a contract but not parent-derived",
    },
    {
        "source_id": "SRC2727_4_422",
        "label": "422 matter/readout no-cheat contract",
        "path": ROOT / "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "needles": [
            "readout_after_variation",
            "no_reduced_EFT_backreaction",
            "R_read is defined only on Sol(S_parent)",
            "readout_after_variation_contract_written",
        ],
        "use": "original variation-order contract and readout-on-solution-space theorem form",
    },
    {
        "source_id": "SRC2727_5_423",
        "label": "423 no-extension/readout countermodel",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": [
            "readout_not_parent_field",
            "post_readout_EFT",
            "post_readout_reduced_action",
            "extension_variation_tax_enforced",
        ],
        "use": "post-readout reduced action remains legal as retained EFT branch if parent does not forbid it",
    },
    {
        "source_id": "SRC2727_6_574_csv",
        "label": "574 generator elimination attempts",
        "path": RESIDUALS / "P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv",
        "needles": [
            "GE574_0_readout_projector",
            "R_read: Sol(S_parent)->Obs",
            "conditional_elimination_as_parent_source",
            "readout projector becomes R0/R11 reduced-action marker",
        ],
        "use": "machine-readable readout generator attempt row",
    },
    {
        "source_id": "SRC2727_7_968_csv",
        "label": "968 parent domain signature CSV",
        "path": RESIDUALS / "P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
        "needles": [
            "PDS968_0_conf_parent_field_list",
            "PDS968_1_S_parent_arguments",
            "PDS968_2_readout_exclusion",
            "PDS968_6_verdict",
        ],
        "use": "machine-readable parent-domain signature blockers",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def schema_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "RAV2727_0_domain_separation",
            "claim_piece": "readout is a map on solution space",
            "formal_statement": "R_read: Sol(S_parent)->Obs, with Conf_parent and Args(S_parent) defined before readout",
            "result": "SCHEMA_THEOREM_CLEAN",
            "why_not_promoted": "current corpus does not provide a closed field-by-field Conf_parent/Args(S_parent) certificate",
            "residual_if_failed": "E_parent_domain_signature",
            "claim_allowed": False,
        },
        {
            "audit_id": "RAV2727_1_no_variation_slot",
            "claim_piece": "no Euler-Lagrange variation with respect to P_read",
            "formal_statement": "If P_read notin Args(S_parent), delta S_parent/delta P_read is undefined and no readout source term exists",
            "result": "CONDITIONAL_THEOREM",
            "why_not_promoted": "the premise P_read notin Args(S_parent) is contract-ready but not parent-signed",
            "residual_if_failed": "E_Pread_variation_slot",
            "claim_allowed": False,
        },
        {
            "audit_id": "RAV2727_2_no_reduced_action_backreaction",
            "claim_piece": "readout-reduced functionals cannot earn parent theorem-zero credit",
            "formal_statement": "Any varied S_red[R_read(Phi)] defines a distinct retained EFT branch and pays a residual tax",
            "result": "GUARDRAIL_STRONG_NOT_ABSOLUTE_EXCLUSION",
            "why_not_promoted": "a reduced EFT is still mathematically legal unless the parent no-extension theorem forbids it",
            "residual_if_failed": "E_reduced_EFT_backreaction",
            "claim_allowed": False,
        },
        {
            "audit_id": "RAV2727_3_apparatus_distinction",
            "claim_piece": "measurement apparatus is ordinary matter before variation or ideal nonbackreacting readout after variation",
            "formal_statement": "Physical apparatus stress belongs in S_matter; ideal R_read carries no stress/current",
            "result": "CLASSIFICATION_READY_NOT_FULL_PARENT_CLAUSE",
            "why_not_promoted": "apparatus/source confusion remains possible without a parent-domain certificate",
            "residual_if_failed": "E_apparatus_backreaction",
            "claim_allowed": False,
        },
        {
            "audit_id": "RAV2727_4_hidden_marker_return",
            "claim_piece": "readout labels cannot hide a material marker that enters before variation",
            "formal_statement": "Domain separation kills only post-variation readout, not pre-variation marker data renamed as readout",
            "result": "BLOCKED_BY_NO_MARKER_THEOREM",
            "why_not_promoted": "primitive no-natural-marker/local invariant algebra triviality remains unproved",
            "residual_if_failed": "E_hidden_marker_as_readout",
            "claim_allowed": False,
        },
        {
            "audit_id": "RAV2727_5_verdict",
            "claim_piece": "readout projector generator eliminated",
            "formal_statement": "R_read notin Args(S_parent), no reduced-action backreaction, no source/coupling absorption, no hidden marker return",
            "result": "READOUT_GENERATOR_NOT_ELIMINATED_PARENT_SIGNATURE_MISSING",
            "why_not_promoted": "schema theorem is clean but parent-domain signature/no-extension premises remain unsigned",
            "residual_if_failed": "E_readout_reentry remains active",
            "claim_allowed": False,
        },
    ]


def domain_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "req_id": "RDOM2727_0_conf_parent",
            "requirement": "closed typed Conf_parent field list",
            "acceptance": "every varied parent field is listed; readout/projector/fitted masks are excluded",
            "current_status": "SKETCH_EXISTS_NOT_CLOSED_SIGNATURE",
            "source": str(ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"),
            "claim_allowed": False,
        },
        {
            "req_id": "RDOM2727_1_S_parent_args",
            "requirement": "closed Args(S_parent)",
            "acceptance": "S_parent depends only on parent fields, matter fields, owned geometry construction and constants",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "source": str(RESIDUALS / "P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv"),
            "claim_allowed": False,
        },
        {
            "req_id": "RDOM2727_2_readout_exclusion",
            "requirement": "P_read, R_read and P_active are excluded from S_parent",
            "acceptance": "readout maps are functions on Sol(S_parent) only and no Euler equation exists for them",
            "current_status": "RELATIVE_SCHEMA_THEOREM_AVAILABLE_PARENT_SIGNATURE_MISSING",
            "source": str(ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md"),
            "claim_allowed": False,
        },
        {
            "req_id": "RDOM2727_3_reduced_EFT_tax",
            "requirement": "any varied readout-reduced action is a new retained EFT branch",
            "acceptance": "S_red cannot be used as theorem-zero evidence for S_parent",
            "current_status": "GUARDRAIL_PASS_NOT_FORBIDDEN_THEOREM",
            "source": str(ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md"),
            "claim_allowed": False,
        },
        {
            "req_id": "RDOM2727_4_no_absorption",
            "requirement": "readout cannot absorb source/coupling/operator residuals after scoring",
            "acceptance": "no fitted masks, posthoc branch selectors, or projection choices alter parent equations",
            "current_status": "POLICY_ACTIVE_PARENT_PROOF_MISSING",
            "source": str(ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "claim_allowed": False,
        },
        {
            "req_id": "RDOM2727_5_verdict",
            "requirement": "parent-domain signature closes",
            "acceptance": "RDOM2727_0 through RDOM2727_4 all pass as parent-signed facts",
            "current_status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "source": str(ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"),
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "RCM2727_0_reduced_EFT",
            "form": "S_red[R_read(Phi)] is varied after observational projection",
            "survives_because": "legal as a new EFT branch unless no-extension theorem forbids it",
            "damage": "projector-dependent Euler terms can mimic parent sources",
            "required_block": "RDOM2727_3_reduced_EFT_tax plus parent no-extension theorem",
            "currently_killed": False,
        },
        {
            "countermodel_id": "RCM2727_1_posthoc_mask",
            "form": "P_active or Pi_read is chosen after seeing observables and inserted into a derivation",
            "survives_because": "guardrail forbids claim credit but parent-domain theorem is not signed",
            "damage": "can hide residuals or create source/coupling absorption",
            "required_block": "RDOM2727_2_readout_exclusion and RDOM2727_4_no_absorption",
            "currently_killed": False,
        },
        {
            "countermodel_id": "RCM2727_2_apparatus_source",
            "form": "measuring apparatus/probe stress is confused with ideal readout",
            "survives_because": "apparatus clause is classification-ready but not a full parent-domain clause",
            "damage": "readout silence can fake missing matter/source terms",
            "required_block": "ordinary apparatus in S_matter before variation or ideal nonbackreacting probe limit",
            "currently_killed": False,
        },
        {
            "countermodel_id": "RCM2727_3_marker_renamed_readout",
            "form": "material marker, domain class or species label is renamed as readout data",
            "survives_because": "no-marker/local invariant algebra theorem is not proved",
            "damage": "readout theorem cannot eliminate pre-variation marker data",
            "required_block": "primitive no-natural-marker theorem or retained marker residual rows",
            "currently_killed": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RDR2727_0_E_parent_domain_signature",
            "quantity": "E_parent_domain_signature",
            "definition": "residual from missing closed Conf_parent and Args(S_parent) certificate excluding readout/projector variables",
            "feeds": "E_readout_reentry;E_local_invariant_algebra",
            "source_path": str(ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"),
            "units_need": "zero theorem or binary parent-domain certificate",
            "missing": "field-by-field parent domain and action-argument ledger",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RDR2727_1_E_Pread_variation_slot",
            "quantity": "E_Pread_variation_slot",
            "definition": "residual if P_read/R_read/P_active appears as an action argument or variational variable",
            "feeds": "E_readout_reentry;source/operator residuals",
            "source_path": str(ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md"),
            "units_need": "dimensionless readout-source leakage or zero-domain proof",
            "missing": "parent-signed P_read notin Args(S_parent)",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RDR2727_2_E_reduced_EFT_backreaction",
            "quantity": "E_reduced_EFT_backreaction",
            "definition": "residual from varying a readout-reduced functional as if it were parent action",
            "feeds": "E_readout_reentry;E_auxiliary_reentry;R11",
            "source_path": str(ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md"),
            "units_need": "dimensionless reduced-action Euler contribution",
            "missing": "no reduced-EFT backreaction theorem or retained branch coefficient map",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RDR2727_3_E_apparatus_backreaction",
            "quantity": "E_apparatus_backreaction",
            "definition": "residual from confusing physical measuring apparatus stress with ideal nonbackreacting readout",
            "feeds": "source/readout gates;WEP/clocks/orbits",
            "source_path": str(ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md"),
            "units_need": "probe stress/source norm or ideal-probe limiting proof",
            "missing": "apparatus-as-matter before variation or nonbackreacting readout limit",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RDR2727_4_E_hidden_marker_as_readout",
            "quantity": "E_hidden_marker_as_readout",
            "definition": "residual from material marker/domain/species data entering before variation and later being described as readout",
            "feeds": "E_readout_reentry;E_visible_coefficient_morphism;WEP/R10",
            "source_path": str(ROOT / "414-local-quotient-invariant-algebra-triviality-gate.md"),
            "units_need": "marker coupling coefficient or no-marker theorem",
            "missing": "primitive no-natural-marker/local invariant algebra triviality",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RDR2727_5_E_source_coupling_absorption",
            "quantity": "E_source_coupling_absorption",
            "definition": "residual from using post-readout projection/mask choices to absorb source, coupling, or operator errors",
            "feeds": "E_readout_reentry;E_reference_absorption;E_operator_core",
            "source_path": str(ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "units_need": "dimensionless absorption/no-cancellation guard",
            "missing": "fixed-before-readout projection ownership and no fitted-mask certificate",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2727_0_readout_reentry",
            "formula": "E_readout_reentry := E_parent_domain_signature + E_Pread_variation_slot + E_reduced_EFT_backreaction + E_apparatus_backreaction + E_hidden_marker_as_readout + E_source_coupling_absorption",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2727_1_no_extension_dependency",
            "formula": "E_no_extension_minimality keeps E_readout_reentry active until the parent-domain signature and no-hidden-marker theorem are signed",
            "status": "DEPENDENCY_LEDGER_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2727_0_readout_schema",
            "claim": "readout-after-variation schema theorem",
            "status": "CONDITIONAL_CLEAN",
            "required_before_claim": "closed parent-domain signature proving R_read/P_read not in S_parent arguments",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2727_1_generator_removed",
            "claim": "readout projector removed from I_loc(Q_MTS)",
            "status": "BLOCKED",
            "required_before_claim": "parent-domain signature, no reduced-EFT backreaction, no hidden marker return, no absorption",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2727_2_EH_GR",
            "claim": "EH/local-GR route improves to claim level",
            "status": "BLOCKED",
            "required_before_claim": "all no-extension generators and LC/source/operator gates closed",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2727_0_conf_parent",
            "missing_item": "closed Conf_parent/Args(S_parent) field list",
            "effect": "readout exclusion remains a contract, not parent theorem",
            "best_next_attack": "make a parent-domain certificate only if accepting explicit closure; otherwise move to next generator",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2727_1_reduced_EFT",
            "missing_item": "absolute no reduced-action backreaction theorem",
            "effect": "post-readout EFT remains legal as retained branch",
            "best_next_attack": "keep variation tax and do not count S_red as parent proof",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2727_2_hidden_marker",
            "missing_item": "no hidden marker return",
            "effect": "readout theorem cannot kill pre-variation marker data",
            "best_next_attack": "continue generator elimination, next memory/class scalar positive operator",
            "claim_blocked": True,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2727_0_schema",
            "decision": "Accept readout-after-variation as a clean conditional schema theorem.",
            "rationale": "If readout is only Sol(S_parent)->Obs, it has no variational slot.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2727_1_no_promotion",
            "decision": "Do not remove readout projector from I_loc at theorem-zero level.",
            "rationale": "Parent-domain signature and no reduced-action backreaction remain unsigned.",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2727_2_next",
            "decision": "Move to memory/class scalar positive-operator route next.",
            "rationale": "Readout is sharpened but not parent-signed; the next ranked generator has a concrete derivation route rather than repeating the same closure clause.",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2727_0_selected",
            "status": "selected_primary",
            "target_doc": "2728-Y5-R2FR-memory-positive-operator-local-silence-or-residual-row-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_memory_positive_operator_local_silence_or_residual_row_under_AX1090_closure_2728.py",
            "mission": "try to prove the memory/class scalar obeys a positive source-free local operator with zero boundary flux, so X=0 locally; if not, retain a source-ready memory scalar residual row",
            "acceptance": "parent L_X form, positivity, J_X=0, boundary/zero-mode silence, and matter/readout no-source clauses close; or E_memory_scalar_generator remains nonclaim with missing inputs explicit",
            "forbidden": "plateau axiom, invented coefficients, local-GR claim, formalization-workbench edits, GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2727_0_readout",
            "sector": "readout generator",
            "state": "conditional schema theorem clean; parent signature missing",
            "confidence": "high on schema, high on nonclaim status",
            "next_need": "either explicit parent-domain closure or move to next generator",
        },
        {
            "snapshot_id": "SNAP2727_1_no_extension",
            "sector": "no-extension/minimality",
            "state": "one generator sharply residualized, not eliminated",
            "confidence": "high blocker clarity",
            "next_need": "memory positive-operator proof attempt",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2727_0_local_bounds",
            "source_table": str(OUTPUTS["residual_rows"]),
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "local/R10/PPN branches can ingest readout re-entry residual components without claim credit",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2727_1_source_weight",
            "source_table": str(OUTPUTS["ejeff_update"]),
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "source-weight branch receives refined E_readout_reentry vector",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2727_2_next_queue",
            "source_table": str(OUTPUTS["next_target"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues memory positive-operator generator target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False, 0, "empty"
        return True, len(rows), "ok"
    except Exception as exc:
        return False, 0, repr(exc)


def recent_formalization_changes() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(
        1 for path in FORMALIZATION.rglob("*")
        if path.is_file() and path.stat().st_mtime >= start
    )


def validation_rows(
    source_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    domain_rows: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_parent_domain_signature",
        "E_Pread_variation_slot",
        "E_reduced_EFT_backreaction",
        "E_apparatus_backreaction",
        "E_hidden_marker_as_readout",
        "E_source_coupling_absorption",
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    parse_results = [(*parse_csv(path), path) for path in csv_paths]
    parse_detail = "; ".join(
        f"{path.name}:{row_count}:{detail}" if passed else f"{path.name}:{detail}"
        for passed, row_count, detail, path in parse_results
    )
    source_ok = all(row["exists"] is True and row["required_needles_found"] is True for row in source_rows)
    schema_nonclaim = all(row["claim_allowed"] is False for row in schema_rows)
    domain_nonclaim = all(row["claim_allowed"] is False for row in domain_rows)
    countermodels_live = all(row["currently_killed"] is False for row in countermodels)
    residual_nonclaim = (
        {row["quantity"] for row in residuals} == required_quantities
        and all(row["valid_for_claim"] is False for row in residuals)
    )
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    branch_paths_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_recent_changed_count = recent_formalization_changes()
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {"validation_id": "VAL2727_0_sources", "passed": source_ok, "detail": "all source paths exist and required needles found", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_1_doc_written", "passed": DOC.exists(), "detail": str(DOC), "timestamp_utc": ts()},
        {"validation_id": "VAL2727_2_csv_parse", "passed": all(result[0] for result in parse_results), "detail": parse_detail, "timestamp_utc": ts()},
        {"validation_id": "VAL2727_3_schema_nonclaim", "passed": schema_nonclaim, "detail": "readout schema theorem remains conditional/nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_4_domain_nonclaim", "passed": domain_nonclaim, "detail": "parent-domain requirements remain unsigned", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_5_countermodels_live", "passed": countermodels_live, "detail": "readout re-entry countermodels remain live unless parent signature closes", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_6_residual_rows_complete_nonclaim", "passed": residual_nonclaim, "detail": "readout residual components complete and valid_for_claim=false", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_7_ejeff_update_nonclaim", "passed": ejeff_nonclaim, "detail": "E_readout_reentry update remains formal/nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_8_claim_gates_false", "passed": gates_false, "detail": "no readout theorem-zero, EH, local-GR or public claim opened", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_9_branch_copies", "passed": branch_paths_ok, "detail": "branch copies exist and remain nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_10_no_formalization_recent_changes", "passed": formalization_recent_changed_count == 0, "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}", "timestamp_utc": ts()},
        {"validation_id": "VAL2727_11_no_github_outputs", "passed": no_github_outputs, "detail": "no GitHub/public-output path was written", "timestamp_utc": ts()},
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2727_OVERALL",
            "passed": overall,
            "detail": "2727 keeps readout-after-variation as a clean conditional schema theorem, retains E_readout_reentry, and selects memory positive-operator next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2727 - Y5/R2FR Readout-After-Variation No Reduced-Action Backreaction Or Generator Row Under AX1090 Closure

## Private Verdict

2727 takes the first generator-kill shot selected by 2726: the readout projector.

The mathematical schema is clean:

`R_read: Sol(S_parent) -> Obs`

If readout is only a map on the solution space, then `P_read` is not an argument of `S_parent`, so there is no parent Euler-Lagrange source `delta S_parent/delta P_read`.

But the generator is **not eliminated at theorem-zero level**. The current corpus still lacks the closed parent-domain signature: a field-by-field `Conf_parent`, a closed `Args(S_parent)`, a parent-signed exclusion of `P_read/R_read/P_active`, no varied reduced-EFT backreaction, and no hidden marker renamed as readout.

So the win is narrower but real: readout-after-variation is now a precise conditional theorem and anti-smuggling contract. `E_readout_reentry` remains active and decomposed.

## Claim Ceiling

- No readout theorem-zero, no local invariant algebra triviality, no EH/Newton/local-GR/PPN/R10/WEP/clock/orbital/public claim is opened.
- Readout is accepted only as a conditional schema theorem until the parent-domain signature is signed.
- All new residual rows are `valid_for_claim=false`.
- No `formalization-workbench` edits, GitHub action, or public-output path is allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## Readout Schema Audit

{markdown_table(rows["schema_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "why_not_promoted", "residual_if_failed", "claim_allowed"])}

## Parent-Domain Signature Requirements

{markdown_table(rows["domain_signature"], ["req_id", "requirement", "acceptance", "current_status", "source", "claim_allowed"])}

## Readout Re-Entry Countermodels

{markdown_table(rows["countermodels"], ["countermodel_id", "form", "survives_because", "damage", "required_block", "currently_killed"])}

## Readout Residual Rows

{markdown_table(rows["residual_rows"], ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"])}

## E_Jeff Update

{markdown_table(rows["ejeff_update"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"])}

## Current Blocker Stack

{markdown_table(rows["blocker_stack"], ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"])}

## Decision Ledger

{markdown_table(rows["decision_ledger"], ["decision_id", "decision", "rationale", "allowed", "claim_credit"])}

## Next Target

{markdown_table(rows["next_target"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"])}

## Project Status Snapshot

{markdown_table(rows["project_snapshot"], ["snapshot_id", "sector", "state", "confidence", "next_need"])}

## Branch Copies

{markdown_table(rows["branch_copies"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is not a fake win, but it is a useful one. The readout trick cannot be used to sneak a source into the parent action if readout really happens after variation. However, we still need the parent field-domain certificate before calling the generator dead. So we keep the readout residual alive, and move to the next possible generator kill: the memory/class scalar positive-operator route.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    schema = schema_audit_rows()
    domain = domain_signature_rows()
    countermodels = countermodel_rows()
    residuals = residual_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "schema_audit": schema,
        "domain_signature": domain,
        "countermodels": countermodels,
        "residual_rows": residuals,
        "ejeff_update": ejeff,
        "claim_gates": gates,
        "blocker_stack": blockers,
        "decision_ledger": decisions,
        "next_target": next_rows,
        "project_snapshot": snapshot,
    }

    for key, table_rows in data.items():
        write_csv(OUTPUTS[key], table_rows)

    write_csv(BRANCH_OUTPUTS["local_bounds"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    copies = branch_copy_rows()
    data["branch_copies"] = copies
    write_csv(OUTPUTS["branch_copies"], copies)

    data["validation"] = [
        {"validation_id": "VAL2727_PRE_DOC", "passed": False, "detail": "pre-document placeholder", "timestamp_utc": ts()}
    ]
    write_doc(data)

    validation = validation_rows(source_rows, schema, domain, countermodels, residuals, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2727 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
