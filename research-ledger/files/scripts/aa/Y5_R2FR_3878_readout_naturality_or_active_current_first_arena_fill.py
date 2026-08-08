from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3878"
BRANCH = "MTS_R2FR_Y5_READOUT_NATURALITY_OR_ACTIVE_CURRENT_FIRST_ARENA_FILL_3878"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3878-Y5-R2FR-readout-naturality-or-active-current-first-arena-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3877_NEXT = OUT / "P8_Y5_R2FR_3877_NEXT_TARGET.csv"
CSV_3877_THEOREM = OUT / "P8_Y5_R2FR_3877_TAIL_DECOMPOSITION_THEOREM.csv"
CSV_3877_CLAUSES = OUT / "P8_Y5_R2FR_3877_TAIL_OWNER_CLAUSE_AUDIT.csv"
CSV_3877_CONTRACT = OUT / "P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv"
CSV_3877_RUNNER = OUT / "P8_Y5_R2FR_3877_ACTIVE_RUNNER_FILL_ROWS.csv"
CSV_3868_INPUTS = OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv"
CSV_3867_SCHEMA = OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_INPUT_SCHEMA.csv"
CSV_3867_CANDIDATE = OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv"
CSV_3509_SOURCE = OUT / "P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv"
CSV_3510_COMMON = OUT / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv"
CSV_1230_ACTION = OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv"
CSV_1231_CONNECTED = OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv"
CSV_1231_ARENA = OUT / "P8_Y5_R10_1231_ARENA_RESIDUAL_LAWS.csv"
CSV_3871_ACTION_MEASURE = OUT / "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv"
CSV_3872_CANDIDATE = OUT / "P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv"
CSV_3873_POYNTING = OUT / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv"
CSV_3502_FLUX = OUT / "P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv"
CSV_3503_HODGE = OUT / "P8_Y5_R2FR_3503_EM_HODGE_CURRENT_BOUND_VECTOR.csv"
CSV_1223_PROOF = OUT / "P8_Y5_R10_1223_MINIMAL_PROOF_CONTRACTS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3878_SOURCE_REGISTER.csv",
    "common_theorem": OUT / "P8_Y5_R2FR_3878_COMMON_MODE_CALIBRATED_TAIL_THEOREM.csv",
    "domain_clauses": OUT / "P8_Y5_R2FR_3878_READOUT_DOMAIN_LOCK_CLAUSE_AUDIT.csv",
    "relative_contract": OUT / "P8_Y5_R2FR_3878_RELATIVE_TAIL_CONTRACT.csv",
    "arena_readiness": OUT / "P8_Y5_R2FR_3878_FIRST_ARENA_FILL_READINESS.csv",
    "runner_update": OUT / "P8_Y5_R2FR_3878_ACTIVE_RUNNER_CALIBRATED_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3878_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3878_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3878_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3878_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3878_00_3877_next", CSV_3877_NEXT, "NEXT3877_0", "3877 selected readout naturality or first arena fill"),
    ("SRC3878_01_3877_theorem", CSV_3877_THEOREM, "TT3877_2_conditional_zero", "tail zero theorem"),
    ("SRC3878_02_3877_common_gap", CSV_3877_CLAUSES, "TOC3877_0_readout_naturality", "readout naturality clause"),
    ("SRC3878_03_3877_arena_lock", CSV_3877_CLAUSES, "TOC3877_6_arena_lock", "arena domain lock clause"),
    ("SRC3878_04_3877_tail_contract", CSV_3877_CONTRACT, "RTC3877_0_total_tail", "b_tail contract"),
    ("SRC3878_05_3877_runner", CSV_3877_RUNNER, "RUNF3877_3_updated_runner", "b_tail active runner"),
    ("SRC3878_06_3868_readout", CSV_3868_INPUTS, "BIR3868_2_z_readout", "readout kernel missing"),
    ("SRC3878_07_3868_delta_w", CSV_3868_INPUTS, "BIR3868_3_z_Delta_w", "source weight missing"),
    ("SRC3878_08_3868_kernel", CSV_3868_INPUTS, "BIR3868_4_z_Karena", "arena kernel missing"),
    ("SRC3878_09_3867_projection", CSV_3867_SCHEMA, "SCHEMA3867_5", "projection consistency schema"),
    ("SRC3878_10_3867_zg", CSV_3867_CANDIDATE, "CAND3867_3_zg_decomposition", "z_g decomposition runner candidate"),
    ("SRC3878_11_3509_source_domain", CSV_3509_SOURCE, "NSF3509_0_typed_domain_target", "typed source-domain theorem"),
    ("SRC3878_12_3509_connected", CSV_3509_SOURCE, "NSF3509_1_connected_density_line_collapse", "connected source weights collapse"),
    ("SRC3878_13_3509_common", CSV_3509_SOURCE, "NSF3509_2_common_scalar_not_composition_source", "common scalar reclassification"),
    ("SRC3878_14_3510_common_identity", CSV_3510_COMMON, "UAS3510_1_common_scale_identity", "common scale identity"),
    ("SRC3878_15_3510_common_guard", CSV_3510_COMMON, "UAS3510_2_common_mode_not_harmless", "common scale guard"),
    ("SRC3878_16_3510_Newton", CSV_3510_COMMON, "UAS3510_4_Newton_Poisson_payoff", "Newton-Poisson calibrated source chain"),
    ("SRC3878_17_1230_naturality", CSV_1230_ACTION, "UAS1230_1_connected_naturality_lemma", "connected naturality lemma"),
    ("SRC3878_18_1230_absorb", CSV_1230_ACTION, "UAS1230_2_common_factor_absorption", "common factor absorption"),
    ("SRC3878_19_1230_measure", CSV_1230_ACTION, "UAS1230_3_measure_owner_extension", "measure owner extension"),
    ("SRC3878_20_1231_graph", CSV_1231_CONNECTED, "CMC1231_1_interaction_graph_lemma", "interaction graph collapse"),
    ("SRC3878_21_1231_forgetting", CSV_1231_CONNECTED, "CMC1231_2_source_forgetting_lemma", "source label forgetting"),
    ("SRC3878_22_1231_arena_wep", CSV_1231_ARENA, "ARENA1231_0_WEP_MICROSCOPE", "first arena residual law"),
    ("SRC3878_23_3871_measure", CSV_3871_ACTION_MEASURE, "AMT3871_4_measure_jacobian", "measure Jacobian reentry"),
    ("SRC3878_24_3872_total_bj", CSV_3872_CANDIDATE, "CAND3872_9_total_bJ", "executable b_J envelope"),
    ("SRC3878_25_3873_poynting_zero", CSV_3873_POYNTING, "PZT3873_2_stationary_zero", "stationary Poynting boundary zero"),
    ("SRC3878_26_3502_readout_rad", CSV_3502_FLUX, "EMF3502_6_readout_radiative_regeneration", "readout/radiative EM regeneration"),
    ("SRC3878_27_3503_cem_readout", CSV_3503_HODGE, "EMB3503_5_C_EM_readout", "C_EM_readout retained"),
    ("SRC3878_28_1223_readout", CSV_1223_PROOF, "PROOF1223_3_readout", "effective/readout proof contract"),
]

COMMON_MODE_THEOREM = (
    "For every tail coefficient X_A in {R_A,c_A_pre,w_A,kappa_A,J_A_measure,K_arena,R_rad,A}, "
    "write X_A=X_* x_A with X_* common across ordinary matter and x_A relative. "
    "Then D_Xhat ln X_A = D_Xhat ln X_* + D_Xhat ln x_A. "
    "If x_A is q-basic/natural on a connected ordinary-matter/source category, the relative term vanishes; "
    "the common term is not a WEP/material source charge and may be absorbed into one calibrated G/source normalization only if it is derivative-silent in time, range, frame, arena and readout domain."
)

RELATIVE_TAIL = (
    "b_tail_rel,A := b_readout_rel,A + b_source_slot_rel,A + b_rad_rel,A"
)

COMMON_TAIL = (
    "z_tail_common := D_Xhat ln R_* + D_Xhat ln c_* + D_Xhat ln w_* + D_Xhat ln kappa_* + D_Xhat ln J_* + D_Xhat ln K_* + D_Xhat ln R_rad,*"
)

RELATIVE_SOURCE_SLOT = (
    "b_source_slot_rel,A := |D_Xhat ln(c_A_pre/c_*)| + |D_Xhat ln(w_A/w_*)| + |D_Xhat ln(kappa_A/kappa_*)| + |D_Xhat ln(J_A_measure/J_*)| + |D_Xhat ln(K_arena,A/K_*)|"
)

CALIBRATED_RUNNER = (
    "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_common_drift"
)

COMMON_DRIFT = (
    "b_common_drift := |D_t ln C_*| + |D_r ln C_*| + |D_frame ln C_*| + |D_lambda ln C_*| + |Delta_domain(C_*)|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_common_mode_relative_tail_split",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def common_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CMT3878_0_split", "common-relative tail split", COMMON_MODE_THEOREM, "EXACT_ALGEBRAIC_SPLIT", "none"),
        ("CMT3878_1_relative_zero", "relative naturality route", "If the relative factors x_A form a natural automorphism over a connected ordinary-matter/source category and source labels are quotient-forgotten before readout, D_Xhat ln x_A=0.", "EXACT_CONDITIONAL_RELATIVE_ZERO", "connectedness/source-label forgetting/readout naturality not parent-signed"),
        ("CMT3878_2_common_reclassification", "common scale is not species poison", "A common tail scale C_* cannot create WEP composition charge by itself; it renormalizes calibrated source coupling instead.", "EXACT_RECLASSIFICATION", "absolute Newton/G/source calibration still needs derivative silence"),
        ("CMT3878_3_common_guard", "common scale is not free magic", "C_* is harmless only after one calibration if it is derivative-silent in time, range, frame, arena, and readout domain.", "ANTI_BACKFILL_GUARD", "retain b_common_drift"),
        ("CMT3878_4_Newton_payoff", "Newton/GR connection", "With fixed kappa_ref, fixed common source scale, and the same Hilbert source in the weak-field 00 equation, the Poisson coefficient is recovered as one calibrated coupling rather than a material-dependent patch.", "EXACT_CONDITIONAL_NEWTON_CHAIN", "kappa/G_ref/source projector owners still separate gates"),
        ("CMT3878_5_verdict", "3878 status", "The current branch cannot claim b_tail=0, but it has converted the active tail problem into relative material/source tails plus one common calibrated drift channel.", "RUNNER_NARROWED_NONCLAIM", "next target is common G/source calibration or parent domain signature"),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def domain_clause_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DLC3878_0_readout_common_factor", "readout factors admit common-relative split", "R_A=R_* r_A and D_X ln r_A=0 if r_A is q-basic/natural", "EXACT_IF_READOUT_FUNCTOR_SIGNED", "b_readout_rel"),
        ("DLC3878_1_source_weight_connectedness", "source weights collapse by connected naturality", "w_A=w_* on connected ordinary matter action-density line", "EXACT_CONDITIONAL_FROM_1230_1231", "D_X ln(w_A/w_*)"),
        ("DLC3878_2_current_coefficient", "pre-current coefficients share the same owner", "c_A_pre=c_* if same-current owner has no species source slot", "CONDITIONAL_NOT_PARENT_SIGNED", "D_X ln(c_A_pre/c_*)"),
        ("DLC3878_3_selector", "source selector has no material label", "kappa_A=kappa_* or explicit real field/current residual", "CONDITIONAL_NOT_PARENT_SIGNED", "D_X ln(kappa_A/kappa_*)"),
        ("DLC3878_4_measure", "measure Jacobian species-blind", "J_A_measure=J_* if the parent measure descends before source/readout split", "MISSING_MEASURE_DESCENT", "D_X ln(J_A_measure/J_*)"),
        ("DLC3878_5_arena_kernel", "arena kernel common convention", "K_arena,A=K_* k_A with k_A fixed by source/test material profile rather than hidden tail", "MISSING_ARENA_DOMAIN_LOCK", "D_X ln(K_arena,A/K_*)"),
        ("DLC3878_6_radiative", "radiative/readout closure common", "R_rad,A=R_rad,* if S_eff/readout preserves the same typed coefficient domain", "UNSIGNED_READOUT_RAD_CLOSURE", "D_X ln(R_rad,A/R_rad,*)"),
        ("DLC3878_7_common_calibration", "common scale derivative silence", "C_* calibrated once; require D_t,D_r,D_frame,D_lambda and domain drift zero", "NOT_DERIVED_RETAIN_COMMON_DRIFT", "b_common_drift"),
    ]
    return [
        {
            "clause_id": row_id,
            "owner_clause": clause,
            "mathematical_form": form,
            "current_status": status,
            "residual_if_missing": residual,
            "passes_current_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, form, status, residual in rows
    ]


def relative_contract_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RTC3878_0_relative_tail", "b_tail_rel,A", RELATIVE_TAIL, "relative/material/source part of the tail after common calibration is separated", "RUNNER_FILL_NONCLAIM"),
        ("RTC3878_1_common_tail", "z_tail_common", COMMON_TAIL, "universal tail scale that can only be calibrated away if derivative-silent", "COMMON_CALIBRATION_CHANNEL_RETAINED"),
        ("RTC3878_2_common_drift", "b_common_drift", COMMON_DRIFT, "absolute Newton/G/source-calibration drift left after one calibration", "MISSING_COMMON_SCALE_DERIVATIVE_SILENCE"),
        ("RTC3878_3_readout_rel", "b_readout_rel,A", "b_readout_rel,A := |D_Xhat ln(R_A/R_*)| + |delta_readout_domain,A-delta_readout_domain,*|", "relative readout transfer drift", "MISSING_READOUT_NATURALITY_OR_BOUND"),
        ("RTC3878_4_source_slot_rel", "b_source_slot_rel,A", RELATIVE_SOURCE_SLOT, "relative prevariation source/current/measure/kernel drift", "MISSING_RELATIVE_SOURCE_SLOT_ZERO_OR_BOUND"),
        ("RTC3878_5_rad_rel", "b_rad_rel,A", "b_rad_rel,A := |D_Xhat ln(R_rad,A/R_rad,*)| + |delta_lambda_readout,A-delta_lambda_readout,*| + |delta_J_eff,A-delta_J_eff,*| + |Phi_EM_rad,A-Phi_EM_rad,*|", "relative radiative/readout regeneration", "MISSING_RELATIVE_RAD_CLOSURE_OR_BOUND"),
        ("RTC3878_6_composition_gate", "composition_residual", "composition tests see b_tail_rel,A-B, not pure common C_*", "WEP/material source split", "RELATIVE_BRANCH_ONLY"),
        ("RTC3878_7_absolute_gate", "absolute_source_residual", "Newton/PPN/orbital source normalization sees b_common_drift unless G_ref/kappa/source projector are fixed in one convention", "calibrated local-GR guard", "COMMON_BRANCH_STILL_LIVE"),
    ]
    return [
        {
            "contract_id": row_id,
            "quantity": quantity,
            "formula_or_definition": formula,
            "meaning": meaning,
            "status": status,
            "numeric_value": "MISSING_PARENT_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, status in rows
    ]


def arena_readiness_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("AFR3878_0_calibrated_Newton", "Newton/Poisson/local_GR", "use common mode as one calibrated G_eff only if b_common_drift=0 and same Hilbert source enters Poisson/orbital/PPN", "3510 Newton-Poisson payoff", "kappa_ref;G_ref;M_H projector;common drift;boundary terms", "BEST_NEXT_DERIVATION_ROUTE"),
        ("AFR3878_1_WEP", "MICROSCOPE_WEP", "WEP sees relative tail b_tail_rel,Ti-Pt times tau_WEP/material kernel", "1231 WEP arena residual law", "DeltaF_TiPt,c;official tau_WEP;readout kernel;relative coefficient values", "NOT_SCOREABLE"),
        ("AFR3878_2_clocks", "clock_alpha", "clock rows see readout/radiative relative coefficient under one clock convention", "3867 clock candidate", "b_alpha_tau;z_g_tau;s_XF2_tau;clock readout normalization", "NOT_SCOREABLE"),
        ("AFR3878_3_R10", "R10_short_range", "R10 sees relative source/test tail and finite-range kernel, not common calibrated G alone", "3867 R10 product law", "real alpha_bound(lambda);K_R10(lambda);beta source/test;profile convention", "NOT_SCOREABLE"),
        ("AFR3878_4_PPN_orbital", "PPN_orbital", "PPN/orbits require common source drift plus relative source-profile tails under one worldtube convention", "3503 total current/source closure", "tau_PPN;tau_orbital;source profile;projector stress;common drift", "NOT_SCOREABLE"),
    ]
    return [
        {
            "readiness_id": row_id,
            "arena": arena,
            "calibrated_tail_use": use,
            "source_basis": basis,
            "missing_for_claim": missing,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, use, basis, missing, status in rows
    ]


def runner_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUNU3878_0_previous", "z_g_active", "|z_g_active| <= b_Qstar + b_Noether + b_tail", "imports 3877", "previous packed form"),
        ("RUNU3878_1_split", "b_tail", "b_tail -> b_tail_rel + b_common_drift after one calibrated common scale is separated", "3878 common-relative theorem", "COMMON_RELATIVE_SPLIT"),
        ("RUNU3878_2_calibrated_runner", "z_g_active,cal", CALIBRATED_RUNNER, "no-cancellation calibrated-source runner", "RUNNER_SCHEMA_REFINED"),
        ("RUNU3878_3_WEP_guard", "composition tests", "relative material/source tails use b_tail_rel; common C_* alone is not a WEP source charge", "common-mode theorem", "RELATIVE_ONLY_FOR_COMPOSITION"),
        ("RUNU3878_4_Newton_guard", "Newton/PPN/source normalization", "common C_* still needs b_common_drift=0 or explicit source-backed drift bound", "anti-backfill guard", "COMMON_DRIFT_LIVE"),
        ("RUNU3878_5_no_claim", "claim_allowed", "false until b_Qstar,b_Noether,b_tail_rel,b_common_drift and s_XF2_active are zero-proved or sourced in one domain", "acceptance policy", "NO_CLAIM"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "source_logic": logic,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, logic, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    contracts: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    required_contracts = {"b_tail_rel,A", "z_tail_common", "b_common_drift"}
    observed_contracts = {row["quantity"] for row in contracts}
    rows = [
        ("G3878_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3878_1_common_theorem", "common-relative calibrated theorem written", "PASS" if any(row["status"] == "EXACT_ALGEBRAIC_SPLIT" for row in theorem) else "FAIL", "common-relative split"),
        ("G3878_2_relative_zero", "relative zero route isolated", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_RELATIVE_ZERO" for row in theorem) else "FAIL", "connected naturality route"),
        ("G3878_3_common_guard", "common mode anti-backfill guard retained", "PASS" if any(row["status"] == "ANTI_BACKFILL_GUARD" for row in theorem) else "FAIL", "common drift retained"),
        ("G3878_4_contracts", "relative/common tail contracts present", "PASS" if required_contracts.issubset(observed_contracts) else "FAIL", ",".join(sorted(observed_contracts))),
        ("G3878_5_arena", "first arena readiness rows written", "PASS" if any(row["status"] == "BEST_NEXT_DERIVATION_ROUTE" for row in arenas) else "FAIL", "Newton common-mode route selected"),
        ("G3878_6_runner", "calibrated active runner updated", "PASS" if any(row["rule"] == CALIBRATED_RUNNER for row in runner) else "FAIL", CALIBRATED_RUNNER),
        ("G3878_7_no_claim", "no generated row allows a public/local-GR claim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3878_0",
            "target_checkpoint": "3879-Y5-R2FR-calibrated-GN-common-tail-to-Newton-Poisson-chain.md",
            "script": "scripts/Y5_R2FR_3879_calibrated_GN_common_tail_to_Newton_Poisson_chain.py",
            "objective": "attack the common branch directly: derive whether the universal tail scale can be fixed once as G_N/kappa_ref and kept derivative-silent across Newton, PPN, orbital and clock/source domains",
            "why_next": "3878 separates relative material tails from common calibrated source drift; the next local-GR leap is proving the common scale is a fixed coupling rather than a hidden time/range/frame source residual",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "COMMON_RELATIVE_TAIL_SPLIT_AND_CALIBRATED_ACTIVE_RUNNER_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3878 splits b_tail into relative material/source tails plus a common calibrated source drift, preventing both overclaim and over-punishment: common scale is not WEP poison, but it is still a Newton/G/source-calibration gate.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    contracts: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3878 - Readout Naturality or Active-Current First Arena Fill

Generated: `{timestamp}`

## Result

3878 sharpens the 3877 `b_tail` object by splitting it into a common calibrated source scale and relative material/source tails:

`{COMMON_MODE_THEOREM}`

The relative tail carried by composition/readout/source tests is:

`{RELATIVE_TAIL}`

The common branch is:

`{COMMON_TAIL}`

and it remains live unless:

`{COMMON_DRIFT} = 0`

So the calibrated active-current runner becomes:

`{CALIBRATED_RUNNER}`

## Why This Matters

This prevents two bad moves at once. We do not falsely punish MTS for needing one calibrated coupling scale, because GR itself uses a calibrated `G_N`. But we also do not hide a drifting source normalization inside `G_N`; any time/range/frame/domain drift remains `b_common_drift`.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Common-Mode Calibrated Tail Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## Domain-Lock Clause Audit

{markdown_table(clauses, ["clause_id", "owner_clause", "current_status", "residual_if_missing"])}

## Relative Tail Contract

{markdown_table(contracts, ["contract_id", "quantity", "formula_or_definition", "status"])}

## First Arena Fill Readiness

{markdown_table(arenas, ["readiness_id", "arena", "calibrated_tail_use", "status", "missing_for_claim"])}

## Calibrated Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the cleanest route I can see right now: split the coupling problem into `b_tail_rel` and `b_common_drift`. `b_tail_rel` is the thing that would poison WEP/material/source tests. `b_common_drift` is the GR/Newton coupling problem: can MTS fix one universal source scale once, the way GR uses one `G_N`, without letting it drift by time, range, frame, or readout domain? That is now the next target.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3878 COMMON RELATIVE TAIL SPLIT -->"
    end = "<!-- END 3878 COMMON RELATIVE TAIL SPLIT -->"
    block = f"""{start}

## 3878 - Common-relative tail split and calibrated active runner

`3878` refines the current-normalization tail problem:

`{COMMON_MODE_THEOREM}`

Relative tail:

`{RELATIVE_TAIL}`

Common drift guard:

`{COMMON_DRIFT}`

Updated calibrated runner:

`{CALIBRATED_RUNNER}`

Interpretation: a common source/readout scale is not automatically WEP/material poison, but it is not free either. It must be a single calibrated coupling with no time/range/frame/domain drift. This moves the next local-GR/Newton attack onto the common `G_N/kappa_ref/source projector` chain.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3878_COMMON_MODE_CALIBRATED_TAIL_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3878_RELATIVE_TAIL_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3878_ACTIVE_RUNNER_CALIBRATED_UPDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3878_VALIDATION.csv`

Next gate: `3879`, calibrated `G_N` common-tail to Newton-Poisson chain.

<!-- Generated by 3878 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    contracts: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3878_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3878_1_common_split", "common-relative split theorem exists", any(row["status"] == "EXACT_ALGEBRAIC_SPLIT" for row in theorem), "common split present"))
    checks.append(("VAL3878_2_relative_zero", "relative-zero naturality route exists", any(row["status"] == "EXACT_CONDITIONAL_RELATIVE_ZERO" for row in theorem), "relative zero present"))
    checks.append(("VAL3878_3_common_guard", "common-mode anti-backfill guard exists", any(row["status"] == "ANTI_BACKFILL_GUARD" for row in theorem), "common drift guard present"))
    required_clauses = {"b_readout_rel", "D_X ln(w_A/w_*)", "D_X ln(J_A_measure/J_*)", "D_X ln(K_arena,A/K_*)", "b_common_drift"}
    clause_residuals = {row["residual_if_missing"] for row in clauses}
    checks.append(("VAL3878_4_domain_clauses", "domain clauses cover readout/source/measure/kernel/common drift", required_clauses.issubset(clause_residuals), ",".join(sorted(clause_residuals))))
    required_contracts = {"b_tail_rel,A", "z_tail_common", "b_common_drift"}
    contract_quantities = {row["quantity"] for row in contracts}
    checks.append(("VAL3878_5_contracts", "relative/common contracts exist", required_contracts.issubset(contract_quantities), ",".join(sorted(contract_quantities))))
    checks.append(("VAL3878_6_arena_route", "Newton common-mode route selected as next derivation", any(row["status"] == "BEST_NEXT_DERIVATION_ROUTE" for row in arenas), "Newton route present"))
    checks.append(("VAL3878_7_runner_update", "calibrated runner has common/relative update", any(row["rule"] == CALIBRATED_RUNNER for row in runner), CALIBRATED_RUNNER))
    checks.append(("VAL3878_8_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3878_9_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "split the coupling problem" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3878_10_spine", "spine updated with 3878 block", SPINE_PATH.exists() and "BEGIN 3878 COMMON RELATIVE TAIL SPLIT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3878_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3878*") if path.is_file()]
    checks.append(("VAL3878_12_formalization_untouched", "no generated 3878 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3878_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3878_14_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, clauses, contracts, arenas, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3878_15_next_target", "next target attacks common G/Newton chain", any("Newton-Poisson" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3879 Newton common branch"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = common_theorem_rows(timestamp)
    clauses = domain_clause_rows(timestamp)
    contracts = relative_contract_rows(timestamp)
    arenas = arena_readiness_rows(timestamp)
    runner = runner_update_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, clauses, contracts, arenas, runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["common_theorem"], theorem)
    write_csv(OUTPUTS["domain_clauses"], clauses)
    write_csv(OUTPUTS["relative_contract"], contracts)
    write_csv(OUTPUTS["arena_readiness"], arenas)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, clauses, contracts, arenas, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, clauses, contracts, arenas, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_COMMON_RELATIVE_TAIL_SPLIT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
