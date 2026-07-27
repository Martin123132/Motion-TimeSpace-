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
DOC_PATH = ROOT / "2637-Y5-R2FR-readout-projector-Ereadout-source-pack-or-closed-domain-certificate.md"

PREFIX = "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / f"{PREFIX}_CLOSED_DOMAIN_CERTIFICATE_ATTEMPT.csv",
    "conditional_lemma": RESIDUALS / f"{PREFIX}_CONDITIONAL_READOUT_LEMMA.csv",
    "countermodels": RESIDUALS / f"{PREFIX}_COUNTERMODEL_RETENTION.csv",
    "residual_pack": RESIDUALS / f"{PREFIX}_EREADOUT_RESIDUAL_PACK.csv",
    "arena_projection": RESIDUALS / f"{PREFIX}_ARENA_PROJECTION_REQUIREMENTS.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2637_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2637_00_2636",
        "role": "immediate handoff selecting readout/projector first",
        "path": ROOT / "2636-Y5-R2FR-generator-elimination-priority-or-effective-GR-residual-vector-source-pack.md",
        "needles": ["READOUT_PROJECTOR_E_READOUT_SELECTED_FIRST", "EFF2636_3", "VAL2636_OVERALL"],
    },
    {
        "source_id": "SRC2637_01_2625",
        "role": "field-domain certificate and readout residual template",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": ["FDC2625_3_readout_excluded", "RRT2625_0_E_readout_total", "VAL2625_OVERALL"],
    },
    {
        "source_id": "SRC2637_02_967",
        "role": "readout-after-variation conditional schema theorem",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": ["RAV967_0_domain_separation", "RCM967_0_reduced_EFT", "V967_2_readout_verdict_not_overclaimed"],
    },
    {
        "source_id": "SRC2637_03_968",
        "role": "parent-domain signature attempt and readout clause",
        "path": ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        "needles": ["PDS968_2_readout_exclusion", "REC968_5_verdict", "V968_3_readout_clause_nonclaim_ready"],
    },
    {
        "source_id": "SRC2637_04_422",
        "role": "matter/readout no-cheat contract",
        "path": ROOT / "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "needles": ["readout_after_variation_contract_written", "parent_factorization_derived", "local_GR_promoted"],
    },
    {
        "source_id": "SRC2637_05_423",
        "role": "minimality/no-extension and post-readout EFT countermodel",
        "path": ROOT / "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "needles": ["closed_parent_field_list", "post_readout_EFT", "parent_universal_property_derived"],
    },
    {
        "source_id": "SRC2637_06_407",
        "role": "primitive relational quotient/readout parent sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needles": ["readout_projection", "S_readout_observables", "local_GR_promoted"],
    },
    {
        "source_id": "SRC2637_07_2407",
        "role": "projector commutator/variation obstruction and bound pack",
        "path": ROOT / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md",
        "needles": ["PZ2407_1_fixed_chainmap_lemma", "PVS2407_4_current_verdict", "VAL2407_OVERALL"],
    },
    {
        "source_id": "SRC2637_08_2489",
        "role": "PPN readout/gauge tail and no gamma-only guard",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["PPNV2489_6_readout_gauge", "GAMMA_ONLY_PASS_FORBIDDEN", "VAL2489_OVERALL"],
    },
    {
        "source_id": "SRC2637_09_2631",
        "role": "full PPN vector readout tail",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": ["PPNV2631_6_readout_gauge", "FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE", "VAL2631_OVERALL"],
    },
    {
        "source_id": "SRC2637_10_2633",
        "role": "effective residual vector and DObs/readout shadow",
        "path": ROOT / "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md",
        "needles": ["DObs_e_R", "Delta_PPN_abs", "VAL2633_OVERALL"],
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
    rows: list[dict[str, Any]] = []
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


def certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "RDC2637_0_parent_configuration_closed",
            "clause": "Conf_parent is closed and excludes P_read, R_read, fitted masks, post-solution sections, readout-selected active blocks and material marker labels",
            "source_basis": "407;423;968;2625",
            "current_evidence": "readout exclusion contract/sketch exists",
            "missing_signature": "closed parent field list and no-extension/universal-property theorem",
            "status": "NOT_PARENT_SIGNED",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_1_action_arguments_closed",
            "clause": "Args(S_parent) are exhausted before variation, so no variational derivative with respect to P_read can be formed",
            "source_basis": "422;967;968;2625",
            "current_evidence": "conditional readout-after-variation theorem shape is clean",
            "missing_signature": "field-by-field action-domain inventory with source path for every argument",
            "status": "CONDITIONAL_SCHEMA_ONLY",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_2_variation_before_readout",
            "clause": "vary S_parent on Conf_parent first, solve parent equations, then apply R_read:Sol(S_parent)->Obs",
            "source_basis": "422;967",
            "current_evidence": "mathematically sufficient no-cheat order is recorded",
            "missing_signature": "parent factorization and same-frame source/EH ownership still unsigned",
            "status": "RELATIVE_THEOREM_READY",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_3_no_reduced_action_theorem_credit",
            "clause": "any varied S_red[g,P_read] or readout-selected EFT is a retained branch, not parent theorem-zero",
            "source_basis": "423;967;968;2625",
            "current_evidence": "variation tax and no-cheat policy are repeatedly recorded",
            "missing_signature": "does not forbid all such branches; only demotes them",
            "status": "POLICY_GUARDRAIL_SIGNED_NOT_ELIMINATION",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_4_no_section_backreaction",
            "clause": "representative section s:Obs->Conf_parent is gauge/readout-only and cannot be varied as physical structure",
            "source_basis": "967;968;2407",
            "current_evidence": "section/backreaction countermodel retained",
            "missing_signature": "section gauge theorem or explicit bound for section_backreaction",
            "status": "LIVE_COUNTERMODEL_RETAINED",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_5_projector_metric_independence",
            "clause": "projector/readout map is fixed topological data or post-solution map, not a metric/domain/Hodge/Green operator contributing stress",
            "source_basis": "2407;2625;2636",
            "current_evidence": "fixed chain-map/topological no-stress route is conditional-clean",
            "missing_signature": "physical Hilbert current equality, domain lock, boundary flux zero and tau/MHref lock",
            "status": "PROJECTOR_STRESS_ZERO_NOT_PROVED",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_6_no_hidden_marker_as_readout",
            "clause": "no material marker, boundary class, domain selector or species label may be renamed as readout data before variation",
            "source_basis": "423;968;2635",
            "current_evidence": "hidden-marker return is identified as a live loophole",
            "missing_signature": "primitive no-natural-marker/no-extension theorem",
            "status": "BLOCKED_BY_NO_MARKER_THEOREM_MISSING",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "RDC2637_7_verdict",
            "clause": "readout/projector generator is removed from local invariant algebra",
            "source_basis": "all reviewed 2637 sources",
            "current_evidence": "conditional theorem is clean but parent domain certificate remains unsigned",
            "missing_signature": "RDC2637_0..6 all parent-signed",
            "status": "READOUT_THEOREM_ZERO_NOT_CLAIMED",
            "closes_as_derivation": "False",
            "valid_for_claim": "False",
        },
    ]


def conditional_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "CRL2637_0_domain",
            "statement": "If P_read and R_read are not elements of Conf_parent and are not arguments of S_parent, then delta S_parent/delta P_read is absent rather than zero-by-cancellation.",
            "proof_status": "VALID_RELATIVE_TO_DOMAIN_PREMISE",
            "proof_sketch": "Euler-Lagrange derivatives exist only for action arguments; a map defined on Sol(S_parent) is post-variation observable structure.",
            "parent_premise_status": "UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "CRL2637_1_no_source",
            "statement": "If R_read:Sol(S_parent)->Obs is applied only after solving, it cannot source parent field equations.",
            "proof_status": "VALID_RELATIVE_TO_ORDERING_PREMISE",
            "proof_sketch": "The variation is completed before readout is evaluated; readout changes reported observables, not the stationary-action equations.",
            "parent_premise_status": "UNSIGNED_PARENT_FACTORISATION",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "CRL2637_2_branch_tax",
            "statement": "If a readout-reduced functional S_red[g,P_read] is varied, it defines a different retained effective branch with E_readout_total rather than a theorem-zero parent row.",
            "proof_status": "POLICY_AND_VARIATION_RULE_CLEAN",
            "proof_sketch": "Projector dependence inside a varied functional contributes by ordinary product/chain-rule terms unless separately zeroed.",
            "parent_premise_status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "CRL2637_3_metric_independent_projector",
            "statement": "If a projector is fixed topological chain-map data on the physical current complex, commutator/stress terms can vanish.",
            "proof_status": "VALID_RELATIVE_TO_TOPOLOGICAL_CHAINMAP_PREMISE",
            "proof_sketch": "For d Pi=Pi d and delta_g Pi=0, the commutator and metric projector stress terms vanish on that complex.",
            "parent_premise_status": "PHYSICAL_HILBERT_EQUALITY_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "lemma_id": "CRL2637_4_verdict",
            "statement": "The exact readout theorem is mathematically real but not yet an MTS parent theorem.",
            "proof_status": "CONDITIONAL_CLEAN_NOT_PARENT_SIGNED",
            "proof_sketch": "The logic closes under premises, while the corpus still lacks closed Conf_parent/Args(S_parent), no-extension/no-marker, and projector physical-current signatures.",
            "parent_premise_status": "BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "RCM2637_0_reduced_action",
            "countermodel": "varied readout-reduced action S_red[g,P_read]",
            "why_live": "projector dependence can create Euler terms while looking like observation",
            "required_for_elimination": "prove no readout-reduced branch is parent action or carry E_readout_total",
            "retained_residual": "E_readout_total",
            "status": "LIVE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "RCM2637_1_section_backreaction",
            "countermodel": "representative section s:Obs->Conf_parent varied as physical",
            "why_live": "active representative labels can return through section dependence",
            "required_for_elimination": "section is gauge/readout-only with no variation slot or source-backed bound",
            "retained_residual": "section_backreaction",
            "status": "LIVE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "RCM2637_2_metric_domain_projector",
            "countermodel": "P_read or Pi_M depends on metric, Hodge operator, Green kernel, domain or worldtube",
            "why_live": "delta_g P_read and domain derivatives create projector stress/source-normalization tails",
            "required_for_elimination": "topological/metric-independent projector theorem on physical Hilbert current",
            "retained_residual": "projector_norm;projector_stress_beta_equiv;D_D_PiM",
            "status": "LIVE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "RCM2637_3_hidden_marker_readout",
            "countermodel": "material marker renamed as readout label before variation",
            "why_live": "domain separation only helps if the marker is not an action argument",
            "required_for_elimination": "primitive no-marker/no-extension theorem or finite marker coupling rows",
            "retained_residual": "marker_readout",
            "status": "LIVE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "RCM2637_4_apparatus_source",
            "countermodel": "measurement apparatus/probe treated as readout while carrying stress-energy",
            "why_live": "real apparatus belongs in ordinary matter before variation, not in pure post-solution readout",
            "required_for_elimination": "apparatus clause and ideal-probe limit or included matter source map",
            "retained_residual": "apparatus_backreaction",
            "status": "LIVE_RETAINED",
            "valid_for_claim": "False",
        },
    ]


def residual_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "ER2637_0_E_readout_total",
            "symbol": "E_readout_total",
            "definition": "delta S_red[g,P_read]/delta g or any equivalent readout-backreaction operator retained when closure fails",
            "units_required": "field-equation operator density or normalized dimensionless projected amplitude",
            "source_status": "MISSING_S_RED_AND_P_READ_FORM",
            "source_path_required": "explicit S_red or proof no S_red is parent action; P_read definition; variation path",
            "projection_required": "PPN/WEP/R10/clock/orbital readout response kernel",
            "baseline_required": "variation-before-readout parent baseline",
            "arena_links": "PPN;WEP;R10;clocks;orbital",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_1_projector_norm",
            "symbol": "projector_norm",
            "definition": "||[nabla,P_read]|| or ||[d,Pi_M]J_H|| normalized on the physical source/readout complex",
            "units_required": "1/length, operator norm, or dimensionless after source/worldtube normalization",
            "source_status": "MISSING_PROJECTOR_NORM_AND_DOMAIN",
            "source_path_required": "projector definition; derivative operator; local domain; current complex; normalization denominator",
            "projection_required": "WEP/clock/R10/source-normalization/PPN response",
            "baseline_required": "fixed topological chain-map or absent parent readout projector",
            "arena_links": "WEP;clocks;R10;PPN;source_normalization",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_2_section_backreaction",
            "symbol": "section_backreaction",
            "definition": "Euler/source term produced if a representative section s:Obs->Conf_parent or fitted mask is varied as physical",
            "units_required": "field-equation operator units or dimensionless projected amplitude",
            "source_status": "MISSING_SECTION_GAUGE_THEOREM_OR_VALUE",
            "source_path_required": "section map, gauge/readout classification, variation rule, source provenance",
            "projection_required": "PPN/readout/orbital/clock tail response",
            "baseline_required": "section is pure gauge or post-solution readout only",
            "arena_links": "PPN;orbital;clocks;local_GR",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_3_marker_readout",
            "symbol": "marker_readout",
            "definition": "pre-variation material marker, boundary class, domain selector or species label hidden as readout data",
            "units_required": "coupling-specific dimensionless marker amplitude or operator coefficient",
            "source_status": "BLOCKED_BY_NO_MARKER_THEOREM_MISSING",
            "source_path_required": "no-marker/no-extension theorem or finite marker coefficient rows",
            "projection_required": "WEP/PPN/clock/R10 marker/source response",
            "baseline_required": "readout data contains no action-domain marker",
            "arena_links": "WEP;PPN;clocks;R10",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_4_projector_stress_beta_equiv",
            "symbol": "projector_stress_beta_equiv",
            "definition": "PPN-equivalent stress generated by metric/domain dependence of a projector/readout map",
            "units_required": "dimensionless PPN beta/gamma/preferred-frame equivalent or operator units before projection",
            "source_status": "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE",
            "source_path_required": "delta_g P_read/Pi_M rule; topological metric-independence proof or coefficient bound",
            "projection_required": "beta/gamma/preferred-frame/local-GR response",
            "baseline_required": "metric-independent post-solution readout",
            "arena_links": "PPN;preferred_frame;local_GR",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_5_apparatus_backreaction",
            "symbol": "apparatus_backreaction",
            "definition": "stress/source tail if measurement apparatus is not idealized as nonbackreacting readout",
            "units_required": "ordinary matter stress-energy units or dimensionless source-normalized tail",
            "source_status": "MISSING_APPARATUS_IDEAL_LIMIT",
            "source_path_required": "apparatus included in matter action or ideal-probe approximation with bound",
            "projection_required": "WEP/clock/orbital/source-normalization projection",
            "baseline_required": "apparatus is ordinary matter before variation or nonbackreacting after variation",
            "arena_links": "WEP;clocks;orbital;source_normalization",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "ER2637_6_readout_abs_envelope",
            "symbol": "Delta_readout_abs",
            "definition": "absolute no-cancellation envelope over E_readout_total, projector_norm, section_backreaction, marker_readout, projector_stress and apparatus tails",
            "units_required": "arena-normalized absolute dimensionless vector",
            "source_status": "SCHEMA_READY_VALUES_MISSING",
            "source_path_required": "all component theorem-zero proofs or sourced numeric rows",
            "projection_required": "full PPN/WEP/R10/clock/orbital response matrix",
            "baseline_required": "variation-before-readout, no fitted GM, no gamma-only scoring",
            "arena_links": "PPN;WEP;R10;clocks;orbital;local_GR",
            "valid_for_claim": "False",
        },
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "APR2637_0_PPN",
            "arena": "PPN/local_GR",
            "readout_components": "E_readout_total;section_backreaction;projector_stress_beta_equiv;Delta_readout_abs",
            "needed_before_test": "beta/gamma/preferred-frame response kernels and no-cancellation envelope",
            "current_status": "BLOCKED_COMPONENT_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "APR2637_1_WEP",
            "arena": "WEP/source universality",
            "readout_components": "projector_norm;marker_readout;apparatus_backreaction",
            "needed_before_test": "source species/material marker basis and same matter functional owner",
            "current_status": "BLOCKED_MARKER_SOURCE_ROWS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "APR2637_2_R10",
            "arena": "short-range/R10",
            "readout_components": "E_readout_total;projector_norm;marker_readout",
            "needed_before_test": "lambda/tau/K/Qbar projection and real bound rows",
            "current_status": "BLOCKED_COEFFICIENT_PROJECTIONS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "APR2637_3_clocks",
            "arena": "clock/time readout",
            "readout_components": "projector_norm;section_backreaction;apparatus_backreaction;DObs_e_R",
            "needed_before_test": "clock map and coframe/readout response normalization",
            "current_status": "BLOCKED_CLOCK_KERNEL_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "APR2637_4_orbital",
            "arena": "Newton/orbital/GM",
            "readout_components": "E_readout_total;section_backreaction;delta_GM;apparatus_backreaction",
            "needed_before_test": "measured-GM transfer fixed before readout and endpoint/domain tail bound",
            "current_status": "BLOCKED_FITTED_GM_GUARD_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2637_0_no_readout_axiom_promotion",
            "forbidden_move": "count readout-after-variation as a parent theorem without closed Conf_parent/Args(S_parent)",
            "reason": "current sources only sign a conditional schema/closure contract",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2637_1_no_reduced_action_laundering",
            "forbidden_move": "vary S_red[g,P_read] and call resulting zero a parent zero",
            "reason": "varied reduced action is a retained branch with E_readout_total",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2637_2_no_hidden_marker_readout",
            "forbidden_move": "rename material/domain/species marker as readout data before variation",
            "reason": "domain separation does not remove pre-variation action arguments",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2637_3_no_projector_free_lunch",
            "forbidden_move": "assume projector commutator or stress vanishes for metric/domain/Hodge projectors",
            "reason": "2407 retains projector stress unless topological physical-current equality is parent-signed",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2637_4_no_local_claim",
            "forbidden_move": "claim GR/Newton/PPN/WEP/R10 pass from 2637",
            "reason": "2637 writes the readout theorem contract and residual pack only",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2637_0_internal_contract",
            "claim": "2637 may guide private readout/projector work",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2637_1_closed_domain_certificate",
            "claim": "closed readout/projector domain certificate is parent-signed",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2637_2_Ereadout_zero",
            "claim": "E_readout_total=0 as an MTS theorem",
            "status": "BLOCKED_CONDITIONAL_ONLY",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2637_3_residual_pack_ready",
            "claim": "readout residual pack has numeric/source-backed rows ready for scoring",
            "status": "BLOCKED_VALUES_MISSING",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2637_4_local_GR",
            "claim": "readout/projector seam no longer blocks derived GR/Newton",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2637_0_result",
            "decision": "READOUT_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE_AS_DERIVATION",
            "reason": "the conditional theorem is clean, but closed Conf_parent/Args(S_parent), no-extension/no-marker, and projector physical-current signatures remain unsigned",
            "consequence": "do not claim E_readout_total=0; carry explicit readout residual rows",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2637_1_gain",
            "decision": "READOUT_THEOREM_CONTRACT_IS_NOW_EXACT",
            "reason": "the work now distinguishes absent action argument, post-solution readout, varied reduced branch, section backreaction and metric/domain projector stress",
            "consequence": "future testing can isolate readout residuals rather than letting them hide inside GM/gauge choices",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2637_2_next",
            "decision": "MOVE_TO_COMPONENT_ZERO_OR_BOUND_PACK",
            "reason": "the parent certificate route is not signed, so the honest next move is componentwise zero attempts or source-ready bound rows",
            "consequence": "2638 should attack E_readout_total/projector_norm/section_backreaction/marker_readout components directly",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md",
            "script": "scripts/Y5_R2FR_readout_residual_component_zero_or_source_bound_pack_2638.py",
            "objective": "attempt componentwise theorem-zero for E_readout_total, projector_norm, section_backreaction and marker_readout; if any component remains unsigned, write source-ready nonclaim bound rows with units, source paths, projection kernels, baselines and no-cancellation envelope",
            "include": "2637 readout residual pack; 2407 Pi_M commutator/stress rows; 2489/2631 readout PPN tails; 2625 RRT template; 2636 generator priority",
            "exclude": "global universal-property retry, closure axiom as theorem, reduced-action laundering, fitted GM, gamma-only/local-GR claim",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_pairs() -> list[tuple[str, Path, Path]]:
    return [
        ("COPY2637_certificate", OUTPUTS["certificate"], LOCAL_BOUNDS / "Readout_closed_domain_certificate_2637_NONCLAIM.csv"),
        ("COPY2637_lemma", OUTPUTS["conditional_lemma"], LOCAL_BOUNDS / "Conditional_readout_lemma_2637_NONCLAIM.csv"),
        ("COPY2637_countermodels", OUTPUTS["countermodels"], LOCAL_BOUNDS / "Readout_countermodel_retention_2637_NONCLAIM.csv"),
        ("COPY2637_residual_pack", OUTPUTS["residual_pack"], LOCAL_BOUNDS / "Ereadout_residual_pack_2637_NONCLAIM.csv"),
        ("COPY2637_projection", OUTPUTS["arena_projection"], LOCAL_BOUNDS / "Readout_arena_projection_2637_NONCLAIM.csv"),
        ("COPY2637_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2637_READOUT_RESIDUAL_COMPONENT_ZERO_OR_BOUND_NEXT.csv"),
    ]


def copy_branch_artifacts() -> None:
    for _, source, target in branch_copy_pairs():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in branch_copy_pairs()
    ]


def formalization_has_2637_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*2637*"):
        if path.is_file():
            return True
    for path in FORMALIZATION.rglob("*READOUT_EREADOUT_CERTIFICATE_2637*"):
        if path.is_file():
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [target for _, _, target in branch_copy_pairs()]
    checks = [
        (
            "VAL2637_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2637_01_certificate_nonclaim",
            all(row["closes_as_derivation"] == "False" for row in generated["certificate"]) and any(row["status"] == "READOUT_THEOREM_ZERO_NOT_CLAIMED" for row in generated["certificate"]),
            "closed-domain certificate does not promote theorem-zero",
        ),
        (
            "VAL2637_02_conditional_lemma",
            any(row["proof_status"] == "CONDITIONAL_CLEAN_NOT_PARENT_SIGNED" for row in generated["conditional_lemma"]),
            "conditional readout theorem is recorded without parent-signature promotion",
        ),
        (
            "VAL2637_03_countermodels_retained",
            all(row["status"] == "LIVE_RETAINED" for row in generated["countermodels"]),
            "readout/reduced-action/projector countermodels remain retained",
        ),
        (
            "VAL2637_04_residual_pack",
            any(row["symbol"] == "E_readout_total" for row in generated["residual_pack"]) and any(row["symbol"] == "Delta_readout_abs" for row in generated["residual_pack"]),
            "readout residual pack contains E_readout_total and no-cancellation envelope",
        ),
        (
            "VAL2637_05_residual_nonclaim",
            all(row["valid_for_claim"] == "False" and row["source_status"].startswith(("MISSING", "BLOCKED", "SCHEMA")) for row in generated["residual_pack"]),
            "all readout residual rows remain source-required nonclaim rows",
        ),
        (
            "VAL2637_06_arenas_blocked",
            all(row["claim_allowed"] == "False" and row["current_status"].startswith("BLOCKED") for row in generated["arena_projection"]),
            "all readout-linked arenas remain blocked",
        ),
        (
            "VAL2637_07_route_guards",
            any(row["guard_id"] == "RG2637_1_no_reduced_action_laundering" for row in generated["route_guards"]) and any(row["guard_id"] == "RG2637_3_no_projector_free_lunch" for row in generated["route_guards"]),
            "reduced-action laundering and projector-free-lunch shortcuts are guarded",
        ),
        (
            "VAL2637_08_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate allows local GR or empirical pass",
        ),
        (
            "VAL2637_09_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2638-Y5-R2FR-readout-residual") for row in generated["next_target"]),
            "2638 component zero/source-bound target selected",
        ),
        (
            "VAL2637_10_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim local_bounds copies and acquisition queue exist and parse",
        ),
        (
            "VAL2637_11_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2637 CSVs parse",
        ),
        (
            "VAL2637_12_formalization_untouched",
            not formalization_has_2637_outputs(),
            "no 2637 outputs are written under formalization-workbench",
        ),
        (
            "VAL2637_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2637_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2637 readout/projector closed-domain certificate attempt and E_readout residual source pack",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2637 - Y5 R2/f(R) Readout Projector E_readout Source Pack Or Closed-Domain Certificate",
        "",
        "Status: `Y5_R2FR_2637_readout_conditional_theorem_clean_parent_domain_unsigned_Ereadout_residual_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no readout/projector theorem-zero, no `E_readout_total=0` theorem, no local-GR/Newton proof, no PPN/WEP/R10/clock/orbital pass, no fitted-GM or reduced-action shortcut, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2637 takes the clean readout idea as far as the current corpus allows. The mathematical lemma is real: if readout is only a map `R_read: Sol(S_parent)->Obs`, and if `P_read/R_read` are not parent action arguments, then readout cannot source the parent Euler-Lagrange equations.",
        "",
        "But that is still a conditional theorem, not a parent-signed MTS theorem. The current sources do not close the parent configuration/action domain, no-extension/no-marker clause, representative-section gauge clause, or physical projector/current equality. So `E_readout_total=0` is not claimed. The honest output is a component residual pack.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Closed-Domain Certificate Attempt",
        md_table(generated["certificate"]),
        "",
        "## Conditional Readout Lemma",
        md_table(generated["conditional_lemma"]),
        "",
        "## Countermodel Retention",
        md_table(generated["countermodels"]),
        "",
        "## E_readout Residual Pack",
        md_table(generated["residual_pack"]),
        "",
        "## Arena Projection Requirements",
        md_table(generated["arena_projection"]),
        "",
        "## Route Guards",
        md_table(generated["route_guards"]),
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
        "Good news: this is not a foggy gap anymore. The readout rule is mathematically sharp, and we know exactly when it works.",
        "",
        "Hard news: MTS does not yet get to cash it as a derived GR step, because the parent action domain is not signed tightly enough. The right next move is component-by-component: try to zero `E_readout_total`, `projector_norm`, `section_backreaction`, and `marker_readout`; anything not zeroed becomes a sourced nonclaim bound row before testing.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "certificate": certificate_rows(),
        "conditional_lemma": conditional_lemma_rows(),
        "countermodels": countermodel_rows(),
        "residual_pack": residual_pack_rows(),
        "arena_projection": arena_projection_rows(),
        "route_guards": route_guard_rows(),
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
