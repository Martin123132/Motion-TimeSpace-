from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1367"
TITLE = "1367-Y5-R10-RAB-Kmetric-memory-scalar-chain-kernel-or-q_loc-arena-thresholds"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KERNEL_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv"
THRESHOLD_PATH = OUT_DIR / f"{PACK_ID}_QLOC_ARENA_THRESHOLD_INTAKE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1367_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1367_0_1366_doc",
            "source_path": "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
            "required_anchor": "NEXT1366_0_1367",
            "purpose": "1366 handoff to Kmetric chain kernels or q_loc arena thresholds.",
        },
        {
            "source_id": "SRC1367_1_1366_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1366_NEXT_TARGET.csv",
            "required_anchor": "NEXT1366_0_1367",
            "purpose": "machine-readable 1367 target.",
        },
        {
            "source_id": "SRC1367_2_1366_envelope",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
            "required_anchor": "ENV1366_0_total_epsilon_GK_q_loc",
            "purpose": "q_loc envelope rows requiring units and thresholds.",
        },
        {
            "source_id": "SRC1367_3_1289_first_kernel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "required_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "purpose": "first Kmetric memory-scalar chain kernel formula.",
        },
        {
            "source_id": "SRC1367_4_1289_delta_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
            "required_anchor": "DTC1289_2_DeltaK00_template",
            "purpose": "DeltaK00 comparison template and missing fields.",
        },
        {
            "source_id": "SRC1367_5_1289_claim_gates",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_CLAIM_GATES.csv",
            "required_anchor": "CG1289_1_first_derivative_component",
            "purpose": "1289 claim gates block symbolic kernels.",
        },
        {
            "source_id": "SRC1367_6_798_gamma_expansion",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_2_local_locked_expansion",
            "purpose": "local locked expansion and conditional quadratic suppression.",
        },
        {
            "source_id": "SRC1367_7_776_kgamma_ledger",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_4_current_Khat_match",
            "purpose": "Khat/Kgamma comparison remains missing.",
        },
        {
            "source_id": "SRC1367_8_1181_external_ppn",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "required_anchor": "SRC1181W_0_Cassini_gamma",
            "purpose": "source-backed PPN gamma comparator candidate.",
        },
        {
            "source_id": "SRC1367_9_1244_policy_feed",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict one-sigma gamma-derived q_R policy feed.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def kernel_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "kernel_id": "KER1367_0_chain_kernel_formula",
                "component": "Kmetric_chain^{00}",
                "formula": "C_sign[L_cg^-2 F_prime(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}]+K_conn^{00}+K_domain^{00}+K_boundary^{00}",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
                "computed_status": "SYMBOLIC_FORMULA_ONLY",
                "missing_values": "MISSING_C_SIGN;MISSING_M_m_00_KERNEL;MISSING_M_L_00_KERNEL;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00;MISSING_UNITS_LEDGER",
                "claim_effect": "cannot compare Kmetric to K_hat or bound Delta_K",
            },
            {
                "kernel_id": "KER1367_1_m_metric_response_kernel",
                "component": "M_m^{00}",
                "formula": "M_m^{00}:=delta m / delta g_00 contribution to Kmetric",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
                "computed_status": "MISSING_KERNEL",
                "missing_values": "m parent definition; q-owned local profile; metric variation rule; units",
                "claim_effect": "memory-gradient source cannot be translated into stress response",
            },
            {
                "kernel_id": "KER1367_2_Lcg_metric_response_kernel",
                "component": "M_L^{00}",
                "formula": "M_L^{00}:=delta L_cg / delta g_00 contribution to Kmetric",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
                "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00",
                "computed_status": "MISSING_KERNEL",
                "missing_values": "L_cg parent definition; local silence or metric response; units",
                "claim_effect": "L_cg drift can re-enter q_loc even when F_prime(m_*)=0",
            },
            {
                "kernel_id": "KER1367_3_connection_domain_boundary_kernels",
                "component": "K_conn;K_domain;K_boundary",
                "formula": "metric response from connection, domain/projector, and boundary/reference dependence",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
                "source_anchor": "KGL776_2_derivative_terms;KGL776_3_boundary_reference_terms",
                "computed_status": "OPEN_KERNELS",
                "missing_values": "connection variation; P_loc/domain commutator; boundary no-flux or fixed-reference row",
                "claim_effect": "hidden response terms can dominate local tests",
            },
            {
                "kernel_id": "KER1367_4_zero_gate",
                "component": "Kmetric_chain^{00}_zero_gate",
                "formula": "F_prime(m_*)=0 plus L_cg metric silence plus K_conn=K_domain=K_boundary=0",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
                "source_anchor": "KDR1289_1_local_zero_condition_for_chain_kernel;GSE798_2_local_locked_expansion",
                "computed_status": "CONDITIONAL_ZERO_NOT_DERIVED",
                "missing_values": "parent lock to m_*; proof F_prime zero; L_cg metric silence; boundary/domain no-flux",
                "claim_effect": "double-zero algebra remains conditional, not a local-GR theorem",
            },
            {
                "kernel_id": "KER1367_5_DeltaK00_template",
                "component": "Delta_K^{00}",
                "formula": "K_L^{00}-[Kmetric_volume^{00}+Kmetric_chain^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}]",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
                "source_anchor": "DTC1289_2_DeltaK00_template",
                "computed_status": "TEMPLATE_IMPROVED_NOT_COMPUTABLE",
                "missing_values": "full Kmetric; current Khat match; boundary and response limits",
                "claim_effect": "Delta_K remains a retained q_loc component",
            },
            {
                "kernel_id": "KER1367_6_verdict",
                "component": "Kmetric memory-scalar chain-kernel computation",
                "formula": "KER1367_0 through KER1367_5 all source-backed",
                "source_path": "aggregate_kernel_attempt",
                "source_anchor": "KER1367_0_to_KER1367_5",
                "computed_status": "KERNELS_NOT_COMPUTABLE_CURRENTLY",
                "missing_values": "C_sign;M_m;M_L;K_conn;K_domain;K_boundary;units;live Khat comparison",
                "claim_effect": "fall back to q_loc arena threshold acquisition",
            },
        ]
    )


def threshold_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "threshold_id": "THR1367_0_PPN_gamma_Cassini",
                "arena": "PPN_gamma",
                "source": "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv::SRC1181W_0_Cassini_gamma; P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv::RPF1244_0_policy",
                "comparator": "gamma = 1 + (2.1 +/- 2.3)e-5; sigma_gamma=2.3e-5; q_R_hat_abs_guardrail=4.6e-05 under existing QR convention",
                "units": "dimensionless",
                "usable_for_q_loc": "MAP_MISSING",
                "required_projection": "q_loc_to_PPN_gamma_response_matrix; GM convention; sign convention; no cancellation",
                "status": "SOURCE_BACKED_COMPARATOR_NONCLAIM_MAP_MISSING",
            },
            {
                "threshold_id": "THR1367_1_PPN_beta_eta_LLR",
                "arena": "PPN_beta_Nordtvedt",
                "source": "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv::SRC1181W_1_LLR_beta_eta",
                "comparator": "eta=(4.4 +/- 4.5)e-4; beta-1=(1.2 +/- 1.1)e-4 using Cassini gamma",
                "units": "dimensionless",
                "usable_for_q_loc": "MAP_MISSING",
                "required_projection": "q_loc_to_beta_eta_response; lunar/orbital convention; source normalization",
                "status": "SOURCE_BACKED_COMPARATOR_NONCLAIM_MAP_MISSING",
            },
            {
                "threshold_id": "THR1367_2_PPN_preferred_frame_framework",
                "arena": "PPN_alpha_i_xi",
                "source": "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv::SRC1181W_2_Will_PPN_framework",
                "comparator": "framework reference only; no numeric preferred-frame bound promoted here",
                "units": "dimensionless",
                "usable_for_q_loc": "NUMERIC_BOUND_MISSING",
                "required_projection": "preferred-frame q_loc response operator and source-backed alpha_i/xi bounds",
                "status": "FRAMEWORK_ONLY_NUMERIC_THRESHOLD_MISSING",
            },
            {
                "threshold_id": "THR1367_3_clock_threshold",
                "arena": "clock_redshift_frequency",
                "source": "MISSING_CLOCK_SOURCE_PATH",
                "comparator": "MISSING_CLOCK_BOUND",
                "units": "MISSING_DIMENSIONLESS_OR_FREQUENCY_UNITS",
                "usable_for_q_loc": "SOURCE_MISSING",
                "required_projection": "q_loc_to_clock_response; tau/coframe lock; clock species coupling",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "threshold_id": "THR1367_4_orbital_threshold",
                "arena": "orbital_precession_ephemeris",
                "source": "MISSING_ORBITAL_SOURCE_PATH",
                "comparator": "MISSING_ORBITAL_BOUND",
                "units": "MISSING_ACCELERATION_OR_PRECESSION_UNITS",
                "usable_for_q_loc": "SOURCE_MISSING",
                "required_projection": "q_loc_to_orbital_acceleration; GM convention; source mass denominator",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "threshold_id": "THR1367_5_R10_fifth_force_threshold",
                "arena": "R10_short_range_fifth_force",
                "source": "MISSING_R10_BOUND_SOURCE_PATH_FOR_QLOC_PROJECTION",
                "comparator": "MISSING_ALPHA_LAMBDA_OR_ACCELERATION_BOUND",
                "units": "MISSING_ALPHA_LAMBDA_OR_ACCELERATION_UNITS",
                "usable_for_q_loc": "SOURCE_OR_PROJECTION_MISSING",
                "required_projection": "q_loc_to_alpha(lambda); source composition; range kernel; units",
                "status": "MISSING_SOURCE_INPUT",
            },
            {
                "threshold_id": "THR1367_6_acceptance_gate",
                "arena": "q_loc_envelope_all",
                "source": "THR1367_0_to_THR1367_5",
                "comparator": "claimable only after arena thresholds plus q_loc response maps are source-backed",
                "units": "REQUIRED_COMPATIBLE_UNITS",
                "usable_for_q_loc": "BLOCKED",
                "required_projection": "all thresholds, all maps, all units, no MISSING markers",
                "status": "CLAIM_BLOCKED",
            },
        ]
    )


def claim_gates() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1367_0_kernel_formula_exists",
                "claim": "first Kmetric chain-kernel formula is written",
                "gate_pass": True,
                "reason": "1289 supplies symbolic Kmetric_chain^{00} structure.",
            },
            {
                "gate_id": "GATE1367_1_kernel_computable",
                "claim": "Kmetric memory-scalar chain kernels are source-backed and computable",
                "gate_pass": False,
                "reason": "M_m, M_L, K_conn, K_domain, K_boundary, units, and sign convention are missing.",
            },
            {
                "gate_id": "GATE1367_2_PPN_gamma_threshold_available",
                "claim": "PPN gamma comparator exists as nonclaim threshold input",
                "gate_pass": True,
                "reason": "Cassini gamma and 1244 one-sigma policy feed are already recorded.",
            },
            {
                "gate_id": "GATE1367_3_q_loc_projection_ready",
                "claim": "q_loc envelope can be projected to PPN/clock/orbital/R10 arenas",
                "gate_pass": False,
                "reason": "q_loc-to-observable response maps and most thresholds are missing.",
            },
            {
                "gate_id": "GATE1367_4_local_GR_reopen",
                "claim": "local-GR/PPN/Newton gates can reopen",
                "gate_pass": False,
                "reason": "kernel computation and q_loc arena projection remain nonclaim/missing.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1367_0_kernel_formula_not_enough",
                "decision": "Do not treat the Kmetric chain-kernel formula as a computed response.",
                "why": "the formula is sharper, but every physical kernel needed for Delta_K remains missing.",
                "next_action": "derive M_m and M_L from parent definitions of m and L_cg, or keep Delta_K envelope active.",
            },
            {
                "decision_id": "DEC1367_1_thresholds_start_with_PPN_gamma",
                "decision": "Use Cassini gamma as the first nonclaim local arena threshold input.",
                "why": "it is already source-backed in the corpus, but q_loc-to-gamma projection is missing.",
                "next_action": "build q_loc response-map rows before any threshold scoring.",
            },
            {
                "decision_id": "DEC1367_2_next_best_route",
                "decision": "Attack m/L_cg metric-response kernels before adding more thresholds.",
                "why": "without kernels, q_loc remains disconnected from the action and local observables.",
                "next_action": "hunt parent definitions of m and L_cg and derive their metric variations.",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1367_0_1368",
                "target_file": "1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels-or-q_loc-projection-map.md",
                "target_script": "scripts/Y5_R10_RAB_m_Lcg_parent_metric_response_kernels_or_q_loc_projection_map.py",
                "task": "hunt/derive parent metric-response kernels M_m and M_L for the memory scalar Gamma_eff=L_cg^-2F(m); if absent, build q_loc-to-PPN-gamma projection-map requirements",
                "success_condition": "either M_m/M_L are source-backed nonclaim kernels with units, or q_loc-to-gamma projection rows state all missing response coefficients and conventions",
                "do_not": "do not claim local GR, q_loc zero, Khat match, q_proxy-only pass, fitted cancellation, formalization-workbench edits, or GitHub action",
            }
        ]
    )


def validate_outputs(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    thresholds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, details: str) -> None:
        validations.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "details": details,
            }
        )

    add(
        "VAL1367_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in kernels if row["kernel_id"] == "KER1367_6_verdict")
    add(
        "VAL1367_1_kernels_not_computable",
        "Kmetric chain kernels are not promoted as computable",
        str(verdict["computed_status"]) == "KERNELS_NOT_COMPUTABLE_CURRENTLY" and not bool(verdict["claim_allowed"]),
        str(verdict["missing_values"]),
    )

    add(
        "VAL1367_2_kernel_formula_retained",
        "symbolic Kmetric_chain formula is retained as nonclaim",
        any(row["kernel_id"] == "KER1367_0_chain_kernel_formula" and row["computed_status"] == "SYMBOLIC_FORMULA_ONLY" for row in kernels),
        "Kmetric_chain formula exists but is not scoreable",
    )

    ppn = next(row for row in thresholds if row["threshold_id"] == "THR1367_0_PPN_gamma_Cassini")
    add(
        "VAL1367_3_PPN_gamma_threshold_loaded",
        "PPN gamma threshold input is source-backed but map-missing",
        "sigma_gamma=2.3e-5" in str(ppn["comparator"]) and str(ppn["usable_for_q_loc"]) == "MAP_MISSING",
        str(ppn["required_projection"]),
    )

    required_thresholds = {
        "THR1367_0_PPN_gamma_Cassini",
        "THR1367_1_PPN_beta_eta_LLR",
        "THR1367_2_PPN_preferred_frame_framework",
        "THR1367_3_clock_threshold",
        "THR1367_4_orbital_threshold",
        "THR1367_5_R10_fifth_force_threshold",
        "THR1367_6_acceptance_gate",
    }
    add(
        "VAL1367_4_threshold_ledger_complete",
        "threshold ledger covers PPN gamma, beta/eta, preferred frame, clock, orbital, R10, and acceptance",
        required_thresholds.issubset({str(row["threshold_id"]) for row in thresholds}),
        f"threshold_rows={len(thresholds)}",
    )

    add(
        "VAL1367_5_thresholds_nonclaim",
        "threshold rows remain nonclaim or missing rather than scored",
        all(not row["claim_allowed"] and str(row["status"]) in {
            "SOURCE_BACKED_COMPARATOR_NONCLAIM_MAP_MISSING",
            "FRAMEWORK_ONLY_NUMERIC_THRESHOLD_MISSING",
            "MISSING_SOURCE_INPUT",
            "CLAIM_BLOCKED",
        } for row in thresholds),
        ";".join(f"{row['threshold_id']}={row['status']}" for row in thresholds),
    )

    add(
        "VAL1367_6_claim_gates_block_claim",
        "claim gates block kernel computation, q_loc projection, and local-GR claims",
        all((row["gate_pass"] is False or row["gate_id"] in {"GATE1367_0_kernel_formula_exists", "GATE1367_2_PPN_gamma_threshold_available"}) and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + kernels + thresholds + gates + decisions + next_target
    add(
        "VAL1367_7_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1367*", "*1367-Y5-R10-RAB-Kmetric*", "*Y5_R10_RAB_Kmetric*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1367_8_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1367_9_next_target_1368",
        "next target routes to m/Lcg metric response kernels or q_loc projection map",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1367_10_overall",
        "overall 1367 validation",
        all(row["status"] == "PASS" for row in validations),
        "1367 keeps Kmetric kernels noncomputable and stages q_loc arena threshold intake rows",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    kernels: list[dict[str, object]],
    thresholds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1367 does not compute the `K_metric[Gamma_eff]` memory-scalar chain kernels. The formula for `Kmetric_chain^{00}` is real and useful, but `M_m`, `M_L`, connection, domain, boundary, sign, and units rows are still missing.",
            "**Main progress:** the fallback testing lane now has its first source-backed arena comparator: Cassini/PPN `gamma` from the existing 1181/1244 policy rows. It is not a q_loc pass because the `q_loc -> PPN gamma` response map is still missing.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Kmetric memory-scalar chain-kernel attempt",
            table(["kernel_id", "component", "formula", "source_path", "source_anchor", "computed_status", "missing_values", "claim_effect"], kernels),
            "## qloc arena threshold intake",
            table(["threshold_id", "arena", "source", "comparator", "units", "usable_for_q_loc", "required_projection", "status"], thresholds),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    kernels = kernel_rows()
    thresholds = threshold_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, kernels, thresholds, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(KERNEL_ATTEMPT_PATH, kernels)
    write_csv(THRESHOLD_PATH, thresholds)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, kernels, thresholds, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
