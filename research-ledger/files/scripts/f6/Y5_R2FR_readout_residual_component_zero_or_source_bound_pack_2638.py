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
DOC_PATH = ROOT / "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md"

PREFIX = "P8_Y5_READOUT_COMPONENT_BOUND_2638"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "component_zero": RESIDUALS / f"{PREFIX}_COMPONENT_ZERO_ATTEMPTS.csv",
    "source_bound_pack": RESIDUALS / f"{PREFIX}_SOURCE_BOUND_PACK.csv",
    "envelope": RESIDUALS / f"{PREFIX}_NO_CANCELLATION_ENVELOPE.csv",
    "response_bridge": RESIDUALS / f"{PREFIX}_QLOC_RESPONSE_BRIDGE.csv",
    "arena_readiness": RESIDUALS / f"{PREFIX}_ARENA_READINESS.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2638_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2638_00_2637",
        "role": "immediate readout residual pack handoff",
        "path": ROOT / "2637-Y5-R2FR-readout-projector-Ereadout-source-pack-or-closed-domain-certificate.md",
        "needles": ["READOUT_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE_AS_DERIVATION", "ER2637_0_E_readout_total", "VAL2637_OVERALL"],
    },
    {
        "source_id": "SRC2638_01_2637_residual_csv",
        "role": "machine-readable readout residual pack",
        "path": RESIDUALS / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_EREADOUT_RESIDUAL_PACK.csv",
        "needles": ["E_readout_total", "Delta_readout_abs"],
    },
    {
        "source_id": "SRC2638_02_2625",
        "role": "readout residual template and certificate failure",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": ["RRT2625_0_E_readout_total", "READOUT_ZERO_DEMOTED_TO_EXPLICIT_CLOSURE", "VAL2625_OVERALL"],
    },
    {
        "source_id": "SRC2638_03_2407",
        "role": "projector commutator/stress zero attempt and bound rows",
        "path": ROOT / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md",
        "needles": ["PZ2407_1_fixed_chainmap_lemma", "PVS2407_4_current_verdict", "VAL2407_OVERALL"],
    },
    {
        "source_id": "SRC2638_04_2408",
        "role": "topological-Hilbert equality merge and R_eq finite rows",
        "path": ROOT / "2408-Y5-R2FR-topological-Hilbert-equality-R-eq-zero-or-epsilonM-bound-fill.md",
        "needles": ["THE2408_4_current_verdict", "REQ2408_0_R_eq", "VAL2408_OVERALL"],
    },
    {
        "source_id": "SRC2638_05_2409",
        "role": "Gamma_eff/Khat metric response and q_loc response operator frontier",
        "path": ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
        "needles": ["KHAT_IDENTITY_NOT_PARENT_SIGNED", "ROP2409_2_R10_yukawa_kernel_scaffold", "VAL2409_OVERALL"],
    },
    {
        "source_id": "SRC2638_06_2489",
        "role": "PPN readout/gauge tail and gamma-only guard",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["PPNV2489_6_readout_gauge", "GAMMA_ONLY_PASS_FORBIDDEN", "VAL2489_OVERALL"],
    },
    {
        "source_id": "SRC2638_07_2631",
        "role": "full PPN vector readout/GM tail",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": ["PPNV2631_6_readout_gauge", "FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE", "VAL2631_OVERALL"],
    },
    {
        "source_id": "SRC2638_08_2636",
        "role": "generator priority readout selection",
        "path": ROOT / "2636-Y5-R2FR-generator-elimination-priority-or-effective-GR-residual-vector-source-pack.md",
        "needles": ["READOUT_PROJECTOR_E_READOUT_SELECTED_FIRST", "E_readout_total", "VAL2636_OVERALL"],
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


def component_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "CZ2638_0_E_readout_total",
            "symbol": "E_readout_total",
            "zero_route": "P_read/R_read absent from Conf_parent and Args(S_parent); no varied S_red branch; variation strictly before readout",
            "current_evidence": "conditional readout theorem clean; parent domain certificate unsigned",
            "missing_inputs": "closed parent action domain; no reduced-action parent branch; section/readout provenance",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_0_E_readout_total",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CZ2638_1_projector_norm",
            "symbol": "projector_norm",
            "zero_route": "P_read/Pi_M fixed topological chain-map on the physical Hilbert current complex with dPi=Pi d",
            "current_evidence": "fixed chain-map lemma conditional-clean",
            "missing_inputs": "physical current domain lock; topological-Hilbert equality; boundary zero flux; M_H_ref/tau lock",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_1_projector_norm",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CZ2638_2_section_backreaction",
            "symbol": "section_backreaction",
            "zero_route": "representative section is gauge/readout-only and never varied as physical structure",
            "current_evidence": "section backreaction listed as retained countermodel",
            "missing_inputs": "section gauge theorem; section map; variation rule; source provenance",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_2_section_backreaction",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CZ2638_3_marker_readout",
            "symbol": "marker_readout",
            "zero_route": "no material marker, boundary class, domain selector or species label can enter before variation as readout data",
            "current_evidence": "hidden marker/readout return repeatedly identified",
            "missing_inputs": "primitive no-marker/no-extension theorem or finite marker coefficients",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_3_marker_readout",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CZ2638_4_projector_stress_beta_equiv",
            "symbol": "projector_stress_beta_equiv",
            "zero_route": "delta_g P_read=0 and delta_domain P_read=0 via fixed metric-independent topological data",
            "current_evidence": "topological no-stress route conditional; Hodge/domain projector stress retained",
            "missing_inputs": "metric independence; domain lock; physical Hilbert equality; PPN stress projection",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_4_projector_stress_beta_equiv",
            "valid_for_claim": "False",
        },
        {
            "component_id": "CZ2638_5_apparatus_backreaction",
            "symbol": "apparatus_backreaction",
            "zero_route": "measurement apparatus is ordinary matter in S_matter before variation or an ideal nonbackreacting post-solution probe",
            "current_evidence": "apparatus clause exists as classification, not a universal source theorem",
            "missing_inputs": "apparatus ideal-limit bound or inclusion in matter action/source map",
            "result": "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED",
            "zero_claimed": "False",
            "bound_row": "RB2638_5_apparatus_backreaction",
            "valid_for_claim": "False",
        },
    ]


def source_bound_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RB2638_0_E_readout_total",
            "symbol": "E_readout_total",
            "bound_parameter": "epsilon_Ereadout_A",
            "mathematical_form": "epsilon_Ereadout_A := ||Pi_A delta S_red[g,P_read]/delta g|| / ||E_GR,A||",
            "units": "arena-normalized dimensionless or field-equation operator units before projection",
            "required_source_path": "explicit S_red or parent proof that no S_red is allowed; P_read definition; variation path",
            "required_projection": "Pi_A for PPN, WEP, R10, clock and orbital arenas",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "variation-before-readout GR/EH local baseline",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_1_projector_norm",
            "symbol": "projector_norm",
            "bound_parameter": "epsilon_projector_comm_A",
            "mathematical_form": "epsilon_projector_comm_A := ||Pi_A([nabla,P_read]J or [d,Pi_M]J_H)|| / M_H_ref",
            "units": "operator norm, 1/length, GM-flux, or dimensionless after M_H_ref normalization",
            "required_source_path": "projector definition; current complex; derivative operator; M_H_ref/tau denominator",
            "required_projection": "WEP, clock, R10, source-normalization and PPN response",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "fixed topological chain-map on physical Hilbert source",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_2_section_backreaction",
            "symbol": "section_backreaction",
            "bound_parameter": "epsilon_section_A",
            "mathematical_form": "epsilon_section_A := ||Pi_A(delta S_section[s(Obs)]/delta g)|| / ||E_GR,A||",
            "units": "field-equation operator units or arena-normalized dimensionless amplitude",
            "required_source_path": "representative section map; gauge/readout classification; variation rule; source provenance",
            "required_projection": "PPN, orbital, clock and local-GR readout tail response",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "section is pure gauge or post-solution readout only",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_3_marker_readout",
            "symbol": "marker_readout",
            "bound_parameter": "epsilon_marker_read_A",
            "mathematical_form": "epsilon_marker_read_A := sum_i |K_i^read m_i| projected into arena A",
            "units": "coupling-specific dimensionless marker amplitude or operator coefficient",
            "required_source_path": "no-marker/no-extension theorem or finite marker coefficient component list",
            "required_projection": "WEP, PPN, clock and R10 marker/source response",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "readout contains no pre-variation marker/action-domain label",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_4_projector_stress_beta_equiv",
            "symbol": "projector_stress_beta_equiv",
            "bound_parameter": "epsilon_Pi_stress_A",
            "mathematical_form": "epsilon_Pi_stress_A := ||Pi_A(-2/sqrt(-g) delta S_Pi/delta g)||",
            "units": "PPN beta/gamma/preferred-frame equivalent or rank-2 operator units",
            "required_source_path": "delta_g P_read/Pi_M rule; metric-independence proof or stress coefficient source",
            "required_projection": "PPN beta/gamma/preferred-frame and local-GR response",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "metric-independent post-solution/topological projector",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_5_apparatus_backreaction",
            "symbol": "apparatus_backreaction",
            "bound_parameter": "epsilon_apparatus_A",
            "mathematical_form": "epsilon_apparatus_A := ||Pi_A(T_apparatus)|| / ||T_source|| or ideal-probe limit",
            "units": "ordinary stress-energy units or dimensionless source-normalized tail",
            "required_source_path": "apparatus matter action or ideal-probe approximation with bound",
            "required_projection": "WEP, clock, orbital and source-normalization response",
            "numeric_status": "MISSING_NUMERIC_VALUE",
            "source_status": "MISSING_SOURCE_PATH",
            "baseline": "apparatus included before variation or nonbackreacting after variation",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "RB2638_6_Delta_readout_abs",
            "symbol": "Delta_readout_abs",
            "bound_parameter": "Delta_readout_abs_A",
            "mathematical_form": "sum of absolute readout component amplitudes in arena A",
            "units": "arena-normalized dimensionless absolute envelope",
            "required_source_path": "all component rows RB2638_0..5 theorem-zero or source-backed numeric",
            "required_projection": "PPN/WEP/R10/clock/orbital response matrix",
            "numeric_status": "MISSING_COMPONENT_VALUES",
            "source_status": "MISSING_COMPONENT_SOURCE_PATHS",
            "baseline": "no fitted GM, no gamma-only, no cancellation-only scoring",
            "valid_for_claim": "False",
        },
    ]


def envelope_rows() -> list[dict[str, Any]]:
    components = "epsilon_Ereadout_A;epsilon_projector_comm_A;epsilon_section_A;epsilon_marker_read_A;epsilon_Pi_stress_A;epsilon_apparatus_A"
    return [
        {
            "envelope_id": "ENV2638_0_definition",
            "arena": "generic_A",
            "formula": "Delta_readout_abs_A = |epsilon_Ereadout_A| + |epsilon_projector_comm_A| + |epsilon_section_A| + |epsilon_marker_read_A| + |epsilon_Pi_stress_A| + |epsilon_apparatus_A|",
            "components": components,
            "rule": "componentwise absolute no-cancellation envelope",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "ENV2638_1_PPN",
            "arena": "PPN",
            "formula": "Delta_PPN_abs includes Delta_readout_abs_PPN as an additive tail",
            "components": "E_readout_total;section_backreaction;projector_stress_beta_equiv;readout_gauge",
            "rule": "no gamma-only pass and no beta/source/readout cancellation",
            "score_status": "BLOCKED_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "ENV2638_2_R10",
            "arena": "R10",
            "formula": "alpha_readout_R10(lambda) bounded only after q_loc/Yukawa source map and readout coefficients exist",
            "components": "E_readout_total;projector_norm;marker_readout",
            "rule": "real alpha(lambda) bound curve plus sourced lambda/tau/K/Qbar normalization required",
            "score_status": "BLOCKED_SOURCE_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "envelope_id": "ENV2638_3_Newton_orbital",
            "arena": "Newton_orbital",
            "formula": "Delta_GM_readout_abs <= |epsilon_section_orb| + |epsilon_apparatus_orb| + |epsilon_projector_comm_orb| + |delta_GM_readout|",
            "components": "section_backreaction;apparatus_backreaction;projector_norm;readout_gauge",
            "rule": "no fitted-GM shortcut",
            "score_status": "BLOCKED_GM_TRANSFER_MISSING",
            "valid_for_claim": "False",
        },
    ]


def response_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_id": "QBR2638_0_readout_to_qmetric",
            "source_component": "E_readout_total;projector_stress_beta_equiv",
            "target_residual": "q_metric_response_defect",
            "bridge_statement": "readout/projector metric-response terms must either be absent from S_parent or enter the same K_hat/Gamma_eff response convention",
            "current_status": "KHAT_IDENTITY_NOT_PARENT_SIGNED",
            "next_input_needed": "source path proving K_hat equals metric response of live Gamma_eff or finite stress response row",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "QBR2638_1_projector_to_q_loc",
            "source_component": "projector_norm;R_eq_integral;I_commutator;D_D_PiM",
            "target_residual": "q_loc_response_operator",
            "bridge_statement": "projector/source mismatch becomes a q_loc or source-normalization residual only after physical current/domain/M_H_ref normalization is fixed",
            "current_status": "R_EQ_AND_MHREF_ROWS_UNFILLED",
            "next_input_needed": "R_eq/M_H_ref/B_zero or q_loc-to-Yukawa source map",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "QBR2638_2_readout_to_PPN",
            "source_component": "Delta_readout_abs",
            "target_residual": "Delta_PPN_abs",
            "bridge_statement": "readout tail is additive in the full PPN no-cancellation vector",
            "current_status": "FULL_VECTOR_SCHEMA_READY_VALUES_MISSING",
            "next_input_needed": "PPN Green/operator response or narrower R10 lane first",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "QBR2638_3_readout_to_R10",
            "source_component": "E_readout_total;projector_norm;marker_readout",
            "target_residual": "alpha_readout_R10(lambda)",
            "bridge_statement": "R10 is the narrowest empirical lane if a finite-range readout/q_loc source map can be defined",
            "current_status": "SCAFFOLD_READY_NOT_SCORE_READY",
            "next_input_needed": "lambda_X, source/test charge normalization, q_loc-to-Yukawa source map and real alpha_bound(lambda)",
            "valid_for_claim": "False",
        },
    ]


def arena_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "AR2638_0_PPN",
            "arena": "PPN/local_GR",
            "required_rows": "RB2638_0;RB2638_2;RB2638_4;RB2638_6 plus readout_gauge",
            "current_status": "BLOCKED_READOUT_COMPONENT_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "AR2638_1_R10",
            "arena": "R10 short range",
            "required_rows": "RB2638_0;RB2638_1;RB2638_3 plus q_loc/Yukawa source map and alpha_bound(lambda)",
            "current_status": "BLOCKED_SOURCE_MAP_AND_BOUND_CURVE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "AR2638_2_WEP",
            "arena": "WEP/source universality",
            "required_rows": "RB2638_1;RB2638_3;RB2638_5 plus species/source matter functional owner",
            "current_status": "BLOCKED_MARKER_SOURCE_COMPONENTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "AR2638_3_clocks",
            "arena": "clock/time readout",
            "required_rows": "RB2638_1;RB2638_2;RB2638_5 plus DObs_e_R clock response",
            "current_status": "BLOCKED_CLOCK_RESPONSE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "arena_id": "AR2638_4_orbital",
            "arena": "Newton/orbital/GM",
            "required_rows": "RB2638_1;RB2638_2;RB2638_5 plus delta_GM/source transfer",
            "current_status": "BLOCKED_FITTED_GM_GUARD_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2638_0_no_component_zero_without_source",
            "forbidden_move": "set any readout component to zero from closure preference alone",
            "reason": "each component now has an explicit missing source/theorem input",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2638_1_no_duplicate_topological_equality_loop",
            "forbidden_move": "repeat the Pi_M topological-Hilbert equality proof without new evidence",
            "reason": "2408 already merged that route and kept R_eq/B_zero/I_commutator rows unfilled",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2638_2_no_placeholder_scoring",
            "forbidden_move": "score MISSING_NUMERIC_VALUE or MISSING_SOURCE_PATH rows",
            "reason": "source-bound pack is schema-ready only",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2638_3_no_fitted_GM_or_gamma_only",
            "forbidden_move": "hide readout tails in fitted GM or a gamma-only comparison",
            "reason": "readout tails feed beta, source normalization, clocks, WEP and orbital channels",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2638_0_internal",
            "claim": "2638 may guide private component sourcing",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2638_1_component_zero",
            "claim": "all readout residual components are theorem-zero",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2638_2_source_bound_pack",
            "claim": "readout source-bound rows are ready to score",
            "status": "BLOCKED_NUMERIC_AND_SOURCE_INPUTS_MISSING",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2638_3_R10_lane",
            "claim": "readout/q_loc R10 comparison is allowed",
            "status": "BLOCKED_QLOC_YUKAWA_MAP_AND_BOUND_CURVE_MISSING",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2638_4_local_GR",
            "claim": "readout/projector no longer blocks derived GR/Newton",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2638_0_result",
            "decision": "READOUT_COMPONENT_ZERO_ATTEMPTS_DO_NOT_CLOSE",
            "reason": "every component has a clean zero route but at least one missing parent/source input",
            "consequence": "carry component source-bound rows; no E_readout_total or projector zero claim",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2638_1_gain",
            "decision": "READOUT_RESIDUAL_VECTOR_NOW_SOURCE_READY",
            "reason": "components, units, source requirements, projection kernels and no-cancellation envelope are explicit",
            "consequence": "testing can later use rows without hiding readout tails in GM/gauge choices",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2638_2_route_merge",
            "decision": "MERGE_WITH_QLOC_RESPONSE_FRONTIER_NOT_DUPLICATE_PIM_EQUALITY",
            "reason": "2408 already handled topological-Hilbert equality; 2409 says the narrower next empirical lane is q_loc-to-Yukawa/R10",
            "consequence": "next target should map readout residuals into q_loc response/R10 source row rather than repeat equality proof",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2639-Y5-R2FR-readout-residual-to-q-loc-response-map-or-R10-Yukawa-source-row.md",
            "script": "scripts/Y5_R2FR_readout_residual_to_q_loc_response_map_or_R10_Yukawa_source_row_2639.py",
            "objective": "map Delta_readout_abs components into the existing q_loc/Khat response-operator frontier; if the parent bridge does not close, emit the first source-ready readout-to-R10 Yukawa row with lambda, tau, source/test normalization, alpha_readout(lambda), source path placeholders and valid_for_claim=false",
            "include": "2638 source-bound pack; 2409 q_loc response rows; 2408 R_eq finite rows; 2489/2631 PPN readout tails; R10 alpha-bound acquisition contracts",
            "exclude": "duplicate Pi_M equality proof, closure axiom as theorem, placeholder scoring, fitted GM, gamma-only/local-GR claim",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_pairs() -> list[tuple[str, Path, Path]]:
    return [
        ("COPY2638_component_zero", OUTPUTS["component_zero"], LOCAL_BOUNDS / "Readout_component_zero_attempts_2638_NONCLAIM.csv"),
        ("COPY2638_source_bound", OUTPUTS["source_bound_pack"], LOCAL_BOUNDS / "Readout_source_bound_pack_2638_NONCLAIM.csv"),
        ("COPY2638_envelope", OUTPUTS["envelope"], LOCAL_BOUNDS / "Readout_no_cancellation_envelope_2638_NONCLAIM.csv"),
        ("COPY2638_bridge", OUTPUTS["response_bridge"], LOCAL_BOUNDS / "Readout_q_loc_response_bridge_2638_NONCLAIM.csv"),
        ("COPY2638_arena", OUTPUTS["arena_readiness"], LOCAL_BOUNDS / "Readout_arena_readiness_2638_NONCLAIM.csv"),
        ("COPY2638_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2638_READOUT_QLOC_R10_SOURCE_ROW_NEXT.csv"),
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


def formalization_has_2638_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*2638*"):
        if path.is_file():
            return True
    for path in FORMALIZATION.rglob("*READOUT_COMPONENT_BOUND_2638*"):
        if path.is_file():
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [target for _, _, target in branch_copy_pairs()]
    checks = [
        (
            "VAL2638_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2638_01_component_zeros_nonclaim",
            all(row["zero_claimed"] == "False" and row["result"] == "ZERO_NOT_PROVED_SOURCE_BOUND_ROW_REQUIRED" for row in generated["component_zero"]),
            "all component zero attempts remain nonclaim and source-bound",
        ),
        (
            "VAL2638_02_bound_pack_contains_core",
            any(row["symbol"] == "E_readout_total" for row in generated["source_bound_pack"]) and any(row["symbol"] == "Delta_readout_abs" for row in generated["source_bound_pack"]),
            "source-bound pack contains E_readout_total and Delta_readout_abs",
        ),
        (
            "VAL2638_03_bound_pack_unscored",
            all(row["valid_for_claim"] == "False" and row["numeric_status"].startswith("MISSING") and row["source_status"].startswith("MISSING") for row in generated["source_bound_pack"]),
            "all source-bound rows remain unscored placeholders",
        ),
        (
            "VAL2638_04_envelope",
            any(row["envelope_id"] == "ENV2638_0_definition" and "no-cancellation" in row["rule"] for row in generated["envelope"]),
            "readout no-cancellation envelope is written",
        ),
        (
            "VAL2638_05_response_bridge",
            any(row["target_residual"] == "alpha_readout_R10(lambda)" for row in generated["response_bridge"]) and all(row["valid_for_claim"] == "False" for row in generated["response_bridge"]),
            "q_loc/R10 response bridge is staged as nonclaim",
        ),
        (
            "VAL2638_06_arenas_blocked",
            all(row["claim_allowed"] == "False" and row["current_status"].startswith("BLOCKED") for row in generated["arena_readiness"]),
            "all readout-linked arenas remain blocked",
        ),
        (
            "VAL2638_07_route_guards",
            any(row["guard_id"] == "RG2638_1_no_duplicate_topological_equality_loop" for row in generated["route_guards"]) and any(row["guard_id"] == "RG2638_2_no_placeholder_scoring" for row in generated["route_guards"]),
            "duplicate-proof and placeholder-scoring guards are active",
        ),
        (
            "VAL2638_08_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate allows local GR or empirical pass",
        ),
        (
            "VAL2638_09_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2639-Y5-R2FR-readout-residual-to-q-loc") for row in generated["next_target"]),
            "2639 readout-to-q_loc/R10 target selected",
        ),
        (
            "VAL2638_10_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim local_bounds copies and acquisition queue exist and parse",
        ),
        (
            "VAL2638_11_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2638 CSVs parse",
        ),
        (
            "VAL2638_12_formalization_untouched",
            not formalization_has_2638_outputs(),
            "no 2638 outputs are written under formalization-workbench",
        ),
        (
            "VAL2638_13_pycache_absent",
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
            "check_id": "VAL2638_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2638 readout component zero attempts and source-bound residual pack",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2638 - Y5 R2/f(R) Readout Residual Component Zero Or Source-Bound Pack",
        "",
        "Status: `Y5_R2FR_2638_readout_component_zero_attempts_do_not_close_source_bound_pack_written_nonclaim`",
        "",
        "Claim ceiling: no readout component theorem-zero, no `E_readout_total=0`, no projector stress/commutator zero, no local-GR/Newton proof, no PPN/WEP/R10/clock/orbital pass, no placeholder scoring, no fitted-GM or gamma-only shortcut, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2638 takes the 2637 residual pack and does the unglamorous but necessary surgery. Each readout component gets one theorem-zero attempt. None closes as a parent-signed result in the current corpus, so each component is converted into a source-ready bound row rather than left as fog.",
        "",
        "This is the right kind of annoying progress: the readout seam can no longer be waved away, but it also can no longer sprawl. It is now a finite vector with units, missing source paths, response projections, baselines, and a no-cancellation envelope.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Component-Zero Attempts",
        md_table(generated["component_zero"]),
        "",
        "## Source-Bound Pack",
        md_table(generated["source_bound_pack"]),
        "",
        "## No-Cancellation Envelope",
        md_table(generated["envelope"]),
        "",
        "## q_loc Response Bridge",
        md_table(generated["response_bridge"]),
        "",
        "## Arena Readiness",
        md_table(generated["arena_readiness"]),
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
        "We did not get the readout kill-shot. But we did get the boxing-footwork version of progress: the residual is now cornered into named components instead of floating around as a vague objection.",
        "",
        "The best next attack is not another projector equality loop. That has already been merged. The sharper route is to map this readout residual vector into the existing `q_loc/Khat` response frontier, preferably the narrower R10/Yukawa lane first, because full PPN is too many doors at once.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "component_zero": component_zero_rows(),
        "source_bound_pack": source_bound_pack_rows(),
        "envelope": envelope_rows(),
        "response_bridge": response_bridge_rows(),
        "arena_readiness": arena_readiness_rows(),
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
