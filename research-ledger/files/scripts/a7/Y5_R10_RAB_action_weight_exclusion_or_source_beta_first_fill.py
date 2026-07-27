from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1387_SOURCE_REGISTER.csv"
ACTION_WEIGHT_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv"
FIRST_FILL_PATH = SRC_DIR / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv"
ARENA_IMPACT_PATH = SRC_DIR / "P8_Y5_R10_1387_ARENA_IMPACT_MAP.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1387_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1387_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1387_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1387_VALIDATION.csv"

STATUS = (
    "action_weight_exclusion_attempt_failed_current_corpus_"
    "delta_w_source_beta_first_fill_written_nonclaim"
)
CLAIM_CEILING = (
    "action_weight_counterexample_audit_and_first_fill_rows_only_no_parent_signed_exclusion_"
    "no_beta_score_no_R10_no_PPN_no_WEP_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1387_0_1386_doc",
        "source_path": "1386-Y5-R10-RAB-canonical-coupling-zero-theorem-or-beta-acquisition-runner.md",
        "required_anchor": "NEXT1386_0_1387",
        "purpose": "handoff to action-weight exclusion or finite source-beta first fill",
    },
    {
        "source_id": "SRC1387_1_1386_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1386_NEXT_TARGET.csv",
        "required_anchor": "NEXT1386_0_1387",
        "purpose": "machine-readable 1387 target",
    },
    {
        "source_id": "SRC1387_2_1386_clause_matrix",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv",
        "required_anchor": "PCM1386_4_action_weight_exclusion",
        "purpose": "1386 identifies action-weight exclusion as active counterexample",
    },
    {
        "source_id": "SRC1387_3_1386_beta_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1386_BETA_ACQUISITION_RUNNER_ROWS.csv",
        "required_anchor": "BAR1386_2_beta_source",
        "purpose": "finite beta/source acquisition schema",
    },
    {
        "source_id": "SRC1387_4_1066_source_scalar",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
        "required_anchor": "SSE1066_5_verdict",
        "purpose": "conditional source-scalar exclusion lemma and surviving obstruction",
    },
    {
        "source_id": "SRC1387_5_1066_measure",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
        "required_anchor": "FMQ1066_4_verdict",
        "purpose": "action-scale/measure normalization audit",
    },
    {
        "source_id": "SRC1387_6_1078_object_language",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
        "required_anchor": "OL1078_4_verdict",
        "purpose": "object-language proof attempt",
    },
    {
        "source_id": "SRC1387_7_1078_action_measure",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
        "required_anchor": "AM1078_4_verdict",
        "purpose": "action-measure proof attempt",
    },
    {
        "source_id": "SRC1387_8_1078_counterexamples",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv",
        "required_anchor": "CEK1078_0_species_action_weight",
        "purpose": "counterexample kill matrix",
    },
    {
        "source_id": "SRC1387_9_1079_current_owner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "required_anchor": "NCO1079_5_species_action_weight",
        "purpose": "current-owner proof cannot kill pre-variation weights",
    },
    {
        "source_id": "SRC1387_10_1079_counterexamples",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
        "required_anchor": "CER1079_0_species_action_weight",
        "purpose": "species action weight survives current-owner proof",
    },
    {
        "source_id": "SRC1387_11_1229_counterexamples",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "CEX1229_0_action_multiplier",
        "purpose": "active source-coupling countermodel",
    },
    {
        "source_id": "SRC1387_12_1229_clauses",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
        "required_anchor": "CLC1229_0_single_action_scale",
        "purpose": "universal source coupling clauses",
    },
    {
        "source_id": "SRC1387_13_1036_beta",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "required_anchor": "BETA1036_2_R10_alpha_match",
        "purpose": "finite beta source/test product law",
    },
    {
        "source_id": "SRC1387_14_this_script",
        "source_path": "scripts/Y5_R10_RAB_action_weight_exclusion_or_source_beta_first_fill.py",
        "required_anchor": "STATUS",
        "purpose": "1387 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    fieldnames = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(column, "")) for column in fieldnames) + " |")
    return "\n".join(lines)


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_ROWS:
        source_path = ROOT / row["source_path"]
        rows.append(
            {
                **row,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, row["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def action_weight_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "AWE1387_0_definition",
            "target": "pre-variation action weight",
            "formal_statement": "S_matter = sum_A w_A S_A[Psi_A,e_obs,theta_A] with w_A independent of the isolated Euler-Lagrange equations",
            "attempt_result": "counterexample is well-defined and must be killed by parent syntax/measure, not by local EOM",
            "current_status": "COUNTEREXAMPLE_VALID",
            "remaining_gap": "derive that w_A is inadmissible, common, quotient-equivalent, or null-projected",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_1_classical_eom",
            "target": "classical equation shortcut",
            "formal_statement": "multiplying one disconnected matter-sector action by constant w_A leaves its isolated classical EOM form unchanged",
            "attempt_result": "classical dynamics cannot exclude source weights",
            "current_status": "SHORTCUT_REJECTED",
            "remaining_gap": "need Hilbert-source, quantum/measure, or object-language owner",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_2_object_language",
            "target": "forbid source-only scalar slot",
            "formal_statement": "Arg(S_parent) contains geometry, matter fields, gauge/current data, representation constants, and universal constants, but no inert source-only w_A",
            "attempt_result": "conditional typing lemma exists",
            "current_status": "OBJECT_LANGUAGE_NOT_PARENT_SIGNED",
            "remaining_gap": "parent MTS primitives do not yet derive the object-language grammar",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_3_action_measure",
            "target": "single hbar/action-measure owner",
            "formal_statement": "one parent action scale and measure for all ordinary matter sectors would make relative w_A physically inadmissible unless carried by a real field/current",
            "attempt_result": "clean conditional route exists",
            "current_status": "ACTION_MEASURE_NOT_SIGNED",
            "remaining_gap": "no parent statistical/measure axiom is signed strongly enough",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_4_current_owner",
            "target": "Hilbert/current owner",
            "formal_statement": "variation-before-readout fixes the source tensor after a common action is chosen",
            "attempt_result": "kills post-variation rescaling conditionally, but w_A inserted before variation is inherited by T_eff",
            "current_status": "CURRENT_OWNER_PARTIAL_NOT_ENOUGH",
            "remaining_gap": "pre-action weights need object-language/action-measure closure",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_5_naturality_connectedness",
            "target": "connected ordinary matter category",
            "formal_statement": "a natural positive scalar over a connected matter category is common",
            "attempt_result": "helpful only if the ordinary matter category is parent-connected and label-only constants are forbidden",
            "current_status": "CONNECTEDNESS_NOT_DERIVED",
            "remaining_gap": "direct-sum/disconnected species components can carry independent constants",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_6_common_factor_policy",
            "target": "common w_*",
            "formal_statement": "if w_A=w_* for all species and w_* has no time/range/radius/frame/domain dependence, it can be absorbed into measured G_N as calibration",
            "attempt_result": "common constant is harmless only as calibration; species/range/phi dependence is not harmless",
            "current_status": "COMMON_FACTOR_POLICY_ONLY",
            "remaining_gap": "prove w_A=w_* and derivative silence before any absorption",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AWE1387_7_verdict",
            "target": "action-weight exclusion",
            "formal_statement": "current corpus does not kill S_matter=sum_A w_A S_A",
            "attempt_result": "proof route is precise but unsigned; finite Delta_w/beta_w acquisition is mandatory",
            "current_status": "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED",
            "remaining_gap": "fill Delta_w_A and beta_w_A rows or derive parent object-language/action-measure owner",
            "valid_for_claim": "False",
        },
    ]


def first_fill_rows() -> list[dict[str, str]]:
    return [
        {
            "fill_id": "DWB1387_0_w_common",
            "quantity": "w_* common action factor",
            "definition": "w_A=w_* for all ordinary matter sectors",
            "formula_or_mapping": "T_eff = w_* sum_A T_A; w_* may be absorbed into G_N only if derivative/source/range/frame silent",
            "units": "dimensionless",
            "required_source": "single parent hbar/action-measure owner or common-action normalization theorem",
            "blocks_if_missing": "clean Newton/source normalization; proof that species weights are absent",
            "current_status": "MISSING_COMMON_ACTION_NORMALIZATION",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_1_Delta_w_A",
            "quantity": "Delta_w_A",
            "definition": "relative pre-variation source/action multiplier for material/source class A",
            "formula_or_mapping": "Delta_w_A := w_A/w_* - 1; contributes to partial_A ln mu_obs and source-charge residuals",
            "units": "dimensionless",
            "required_source": "parent exclusion theorem, material/source coefficient value, or upper bound by species/source class",
            "blocks_if_missing": "WEP/source-charge; Newton measured-GM universality; finite beta_source convention",
            "current_status": "FIRST_FILL_ROW_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_2_beta_w_source",
            "quantity": "beta_w_source",
            "definition": "canonical phi-dependence of source action weight if w_source depends on phi",
            "formula_or_mapping": "beta_w,S := partial_phi ln w_S(phi); if w_A is constant but species-dependent, beta_w=0 but Delta_w_A still affects source normalization",
            "units": "canonical inverse-field or dimensionless by convention",
            "required_source": "canonical phi normalization and source weight function w_S(phi)",
            "blocks_if_missing": "R10 source leg; finite fifth-force source coupling; clock/orbital source response",
            "current_status": "MISSING_SOURCE_BETA_WEIGHT_FUNCTION",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_3_beta_w_test",
            "quantity": "beta_w_test",
            "definition": "canonical phi-dependence of test-body action weight/material response",
            "formula_or_mapping": "beta_w,T := partial_phi ln w_T(phi); finite exchange uses beta_source*beta_test",
            "units": "same beta convention as beta_w_source",
            "required_source": "test material action and composition map",
            "blocks_if_missing": "R10 test leg; WEP/material comparison; clocks",
            "current_status": "MISSING_TEST_BETA_WEIGHT_FUNCTION",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_4_beta_product_guard",
            "quantity": "beta_w_source*beta_w_test",
            "definition": "action-weight contribution to finite scalar exchange",
            "formula_or_mapping": "alpha_w(lambda)=K_w(lambda) beta_w,S beta_w,T + epsilon_tail(lambda); no linear beta shortcut",
            "units": "dimensionless alpha after convention lock",
            "required_source": "beta convention, K_w/profile factor, source/test rows, tail envelope, R10 bound curve",
            "blocks_if_missing": "R10 alpha(lambda); local finite-force score",
            "current_status": "PRODUCT_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_5_no_absorption_guard",
            "quantity": "measured-G absorption guard",
            "definition": "only a universal constant common factor may be absorbed into measured G_N",
            "formula_or_mapping": "partial_t,r,A,lambda,frame ln w_A = 0 and Delta_w_A=0 are required before absorption",
            "units": "dimensionless derivative checks",
            "required_source": "derivative silence theorem or finite residual bounds",
            "blocks_if_missing": "Newton inverse-square/source normalization and local GR promotion",
            "current_status": "GUARD_READY_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "DWB1387_6_first_fill_verdict",
            "quantity": "Delta_w/beta_source first-fill pack",
            "definition": "action-weight counterexample is converted into explicit nonclaim source beta/source-normalization rows",
            "formula_or_mapping": "runner must refuse claims until DWB1387_0 through DWB1387_5 are theorem-zero or source-backed",
            "units": "not claim-grade",
            "required_source": "complete action-weight exclusion theorem or finite coefficient pack",
            "blocks_if_missing": "local GR, Newton, PPN, R10, WEP",
            "current_status": "NONCLAIM_FIRST_FILL_READY",
            "valid_for_claim": "False",
        },
    ]


def arena_impact_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "AIM1387_0_Newton",
            "arena": "Newton/source normalization",
            "impact_if_Delta_w_survives": "measured source strength becomes composition/source weighted instead of universal",
            "required_to_score": "Delta_w_A values or theorem-zero; no measured-G absorption cheat",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "AIM1387_1_WEP",
            "arena": "WEP/source charge",
            "impact_if_Delta_w_survives": "relative source/test material weights contribute to eta_source_AB or tau_WEP product",
            "required_to_score": "material/source classes, Delta_w_AB or beta_A matrix, source worldtube/readout kernel",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "AIM1387_2_R10",
            "arena": "R10 alpha(lambda)",
            "impact_if_Delta_w_survives": "phi-dependent weights contribute beta_w,S beta_w,T to finite exchange",
            "required_to_score": "mu_m^2, beta_w,S, beta_w,T, K_w(lambda), bound curve, tail envelope",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "AIM1387_3_PPN",
            "arena": "PPN/local residual vector",
            "impact_if_Delta_w_survives": "source-normalization weights can alter gamma/beta/source terms after measured-G calibration",
            "required_to_score": "weak-field source vector including second-order beta_source residue",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "AIM1387_4_clocks",
            "arena": "clocks/constants",
            "impact_if_Delta_w_survives": "species/action measure dependence can track material standards or effective constants",
            "required_to_score": "constant-sector superselection or finite clock/material beta rows",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
        {
            "arena_id": "AIM1387_5_local_GR",
            "arena": "local GR reduction",
            "impact_if_Delta_w_survives": "local matter coupling/source side is not GR-universal",
            "required_to_score": "action-weight theorem-zero or complete finite residual vector below all local bounds",
            "status": "BLOCKED",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1387_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1387_1_exclusion_attempt",
            "gate": "action-weight exclusion is attempted",
            "status": "PASS_ATTEMPTED",
            "reason": "object-language, action-measure, current-owner, and connectedness routes are audited",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1387_2_counterexample",
            "gate": "w_A counterexample is killed",
            "status": "BLOCKED_COUNTEREXAMPLE_SURVIVES",
            "reason": "object-language and action-measure owners remain unsigned; current owner cannot kill pre-variation weights",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1387_3_first_fill",
            "gate": "Delta_w/beta_source first-fill rows exist",
            "status": "PASS_NONCLAIM_FIRST_FILL",
            "reason": "DWB1387 rows convert the counterexample into explicit source-beta/source-normalization inputs",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1387_4_numeric",
            "gate": "finite source beta/action-weight rows can score",
            "status": "BLOCKED_VALUES_MISSING",
            "reason": "Delta_w_A, beta_w,S, beta_w,T, convention, material map, and arena kernels are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1387_5_local_claim",
            "gate": "local GR / Newton / PPN / R10 / WEP pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1387 is an exclusion audit and nonclaim first-fill pack, not a derived GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1387_0_exclusion_status",
            "decision": "action-weight exclusion is not parent-signed",
            "because": "object-language typing and action-measure ownership remain conditional contracts, not derived MTS theorems",
            "next_action": "do not claim g_c=0 from matter descent",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1387_1_first_fill",
            "decision": "convert w_A into finite Delta_w/beta_w rows",
            "because": "pre-variation source weights survive current-owner proof and affect source normalization/fifth-force products",
            "next_action": "build a strict validator for DWB1387 rows before any numeric runner",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1387_2_physics_priority",
            "decision": "common factor is calibration; relative or phi-dependent weights are physics",
            "because": "only w_A=w_* with derivative silence may be absorbed into measured G_N",
            "next_action": "separate common calibration from species/range/phi-dependent source residuals",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1387_0_1388",
            "next_doc": "1388-Y5-R10-RAB-Delta-w-source-beta-validator-or-action-measure-owner-return.md",
            "next_script": "scripts/Y5_R10_RAB_Delta_w_source_beta_validator_or_action_measure_owner_return.py",
            "task": "build a strict validator for the Delta_w/beta_w first-fill rows, while preserving the option to return to a parent action-measure owner theorem if new evidence appears",
            "success_condition": "validator refuses scoring unless common calibration, Delta_w_A, beta_w_source, beta_w_test, convention, material/source map, and arena kernels are source-backed; local claims remain blocked",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    audit: list[dict[str, str]],
    first_fill: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    exclusion_failed = any(
        row["audit_id"] == "AWE1387_7_verdict"
        and row["current_status"] == "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED"
        for row in audit
    )
    first_fill_ready = any(
        row["fill_id"] == "DWB1387_6_first_fill_verdict"
        and row["current_status"] == "NONCLAIM_FIRST_FILL_READY"
        for row in first_fill
    )
    nonclaim = all(row.get("valid_for_claim", "False") == "False" for row in audit + first_fill)
    arenas_blocked = all(row["status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in arenas)
    local_blocked = any(row["gate_id"] == "GATE1387_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        ACTION_WEIGHT_AUDIT_PATH,
        FIRST_FILL_PATH,
        ARENA_IMPACT_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_action_weight_exclusion_or_source_beta_first_fill.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, exclusion_failed, first_fill_ready, nonclaim, arenas_blocked, local_blocked, outside_formalization])
    return [
        {
            "validation_id": "VAL1387_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1387_1_exclusion_refusal",
            "check": "action-weight exclusion is not falsely claimed",
            "status": "PASS" if exclusion_failed else "FAIL",
            "details": "AWE1387_7 keeps the counterexample alive and routes to first-fill rows.",
        },
        {
            "validation_id": "VAL1387_2_first_fill",
            "check": "Delta_w/beta_source first-fill rows are written",
            "status": "PASS" if first_fill_ready else "FAIL",
            "details": "DWB1387_6 records nonclaim first-fill readiness.",
        },
        {
            "validation_id": "VAL1387_3_nonclaim",
            "check": "audit and fill rows remain nonclaim",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "All AWE1387 and DWB1387 rows keep valid_for_claim=False.",
        },
        {
            "validation_id": "VAL1387_4_arena_refusal",
            "check": "arena routing remains blocked",
            "status": "PASS" if arenas_blocked and local_blocked else "FAIL",
            "details": "AIM1387 rows and GATE1387_5 block local/R10/PPN/WEP/Newton claims.",
        },
        {
            "validation_id": "VAL1387_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1387_6_overall",
            "check": "overall 1387 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1387 rejects a false action-weight exclusion and writes nonclaim Delta_w/source-beta first-fill rows.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    audit: list[dict[str, str]],
    first_fill: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1387 - Y5 R10 RAB Action-Weight Exclusion Or Source-Beta First Fill

**Generated:** {generated}

**Current verdict:** the independent action-weight counterexample is not killed by the current corpus. `S_matter=sum_A w_A S_A` can preserve isolated classical equations while changing Hilbert source normalization. Object-language and action-measure routes are good conditional theorem targets, but they are not parent-signed.

**Discipline move:** turn `w_A` into explicit nonclaim rows. A common constant `w_*` is calibration only if it is universal and derivative-silent. Relative `Delta_w_A` or phi-dependent `beta_w,A` is physics and must be theorem-zero or source-backed before any Newton, WEP, R10, PPN, or local-GR score.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Action-Weight Exclusion Audit

{md_table(audit)}

## `Delta_w` / Source-Beta First-Fill Rows

{md_table(first_fill)}

## Arena Impact Map

{md_table(arenas)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    audit = action_weight_audit_rows()
    first_fill = first_fill_rows()
    arenas = arena_impact_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, audit, first_fill, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ACTION_WEIGHT_AUDIT_PATH, audit)
    write_csv(FIRST_FILL_PATH, first_fill)
    write_csv(ARENA_IMPACT_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, audit, first_fill, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1387 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
