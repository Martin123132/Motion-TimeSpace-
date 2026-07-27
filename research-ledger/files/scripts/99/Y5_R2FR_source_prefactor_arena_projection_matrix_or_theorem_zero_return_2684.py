from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2684"
BRANCH_ID = "Y5_R2FR_SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_OR_THEOREM_ZERO_RETURN_2684"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2684-Y5-R2FR-source-prefactor-arena-projection-matrix-or-theorem-zero-return.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2684_SOURCE_REGISTER.csv",
    "projection_audit": RESIDUALS / "P8_Y5_R2FR_2684_ARENA_PROJECTION_REQUIREMENTS_AUDIT.csv",
    "projection_matrix": RESIDUALS / "P8_Y5_R2FR_2684_SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "coefficient_arena_map": RESIDUALS / "P8_Y5_R2FR_2684_COEFFICIENT_TO_ARENA_MAP_NONCLAIM.csv",
    "projection_silence_gates": RESIDUALS / "P8_Y5_R2FR_2684_PROJECTION_SILENCE_GATES_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2684_PROJECTION_MATRIX_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2684_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2684_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2684_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2684_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2684_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_projection_matrix": LOCAL_BOUNDS / "source_prefactor_arena_projection_matrix_2684_NONCLAIM.csv",
    "local_coefficient_arena_map": LOCAL_BOUNDS / "coefficient_to_arena_map_2684_NONCLAIM.csv",
    "local_projection_silence": LOCAL_BOUNDS / "projection_silence_gates_2684_NONCLAIM.csv",
    "wep_projection_matrix": WEP_COEFF / "source_prefactor_arena_projection_matrix_2684_NONCLAIM.csv",
    "source_weight_projection_matrix": SOURCE_INTAKE / "source-weight" / "SOURCE_PREFACTOR_ARENA_PROJECTION_MATRIX_2684_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2684_2683_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2683_NEXT_TARGET.csv",
        "required_needles": ["NEXT2683_0_selected", "K_pref and tau_arena", "no row is claim-ready"],
        "purpose": "confirms selected 2684 projection target",
    },
    {
        "source_id": "SRC2684_2683_SOURCE_PACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2683_FINITE_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
        "required_needles": ["SP2683_5_arena_product", "MISSING_ARENA_PROJECTION_MATRIX", "independent_of_bound_inversion"],
        "purpose": "imports finite source-prefactor source-pack blockers",
    },
    {
        "source_id": "SRC2684_2683_ZERO_GATES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv",
        "required_needles": ["TZ2683_6_common_projection_silence", "ARENA_PROJECTION_SILENCE_NOT_SIGNED", "THEOREM_ZERO_NOT_PROVED"],
        "purpose": "keeps theorem-zero/projection-silence route open",
    },
    {
        "source_id": "SRC2684_DPM2652",
        "relative_path": "source-intake/local_bounds/Delta_w_projection_matrix_2652_NONCLAIM.csv",
        "required_needles": ["DPM2652_1_WEP_MICROSCOPE", "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING", "DPM2652_6_no_cancellation_policy"],
        "purpose": "imports existing Delta_w projection matrix stubs",
    },
    {
        "source_id": "SRC2684_K2439",
        "relative_path": "source-intake/beta-source/docs/K_PROJECTION_MATRIX_2439_NONCLAIM.csv",
        "required_needles": ["NCE2439_0_WEP", "NCE2439_3_R10", "NO_CROSS_ARENA_CANCELLATION_ALLOWED"],
        "purpose": "imports K-vector/no-cancellation arena envelope policy",
    },
    {
        "source_id": "SRC2684_R10_2194",
        "relative_path": "source-intake/beta-source/docs/PARENT_QLOC_R10_ALPHA_TEMPLATE_2194_NONCLAIM.csv",
        "required_needles": ["MTS_q_loc_R10_alpha_template_2194", "MISSING_PARENT_ALPHA_PREDICTED", "THEOREM_ZERO_UNSIGNED"],
        "purpose": "imports R10 alpha projection template and blockers",
    },
    {
        "source_id": "SRC2684_PPN2631",
        "relative_path": "source-intake/local_bounds/Full_PPN_vector_ledger_2631_NONCLAIM.csv",
        "required_needles": ["PPNV2631_4_wR", "MISSING_TAU_K_QBAR_PROJECTIONS", "PPNV2631_8_total_abs"],
        "purpose": "imports PPN source-weight vector blockers",
    },
    {
        "source_id": "SRC2684_CLOCK2675",
        "relative_path": "source-intake/clocks/branch_locked_local/P8_Y5_2675_CLOCK_READOUT_ROWS_NONCLAIM.csv",
        "required_needles": ["CLK2675_1_tau_readout", "MISSING_PARENT_TAU_CLOCK_XHAT_MAP", "CLK2675_3_shared_source_leg"],
        "purpose": "imports clock projection/readout blockers",
    },
    {
        "source_id": "SRC2684_TAU1067",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
        "required_needles": ["TAQ1067_0_tau_zero_option", "MISSING_NUMERIC_PROJECTION", "TAQ1067_4_refusal_rule"],
        "purpose": "imports WEP tau acquisition and refusal rule",
    },
    {
        "source_id": "SRC2684_LGR2633",
        "relative_path": "source-intake/local_bounds/Conditional_local_GR_theorem_2633_NONCLAIM.csv",
        "required_needles": ["THM2633_4_local_GR_claim_gate", "CLAIM_GATE_WRITTEN_NOT_PASSED", "source normalization"],
        "purpose": "imports local-GR conditional theorem claim gate",
    },
    {
        "source_id": "SRC2684_RV2606",
        "relative_path": "source-intake/local_bounds/Finite_local_residual_vector_2606_NONCLAIM.csv",
        "required_needles": ["RV2606_9_projection_norms", "MISSING_OPERATOR_PROJECTION_NORMS", "RESIDUAL_VECTOR_ACTIVE_NONCLAIM"],
        "purpose": "imports finite residual projection-norm blockers",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
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


def projection_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PRA2684_0_contract",
            "projection_claim": "source-prefactor finite rows can be compared to local data",
            "required_contract": "observable_arena = K_pref(arena) * tau_arena * epsilon_prefactor_total with units, sign convention, source path and common normalizer",
            "current_status": "CONTRACT_WRITTEN_VALUES_MISSING",
            "missing_for_claim": "K_pref; tau_arena; common source normalizer; coefficient values; arena kernels; no-cancellation envelope",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2683_NEXT_TARGET.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "stage arena matrix as nonclaim rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "PRA2684_1_existing_matrix_status",
            "projection_claim": "existing Delta_w/K matrices are enough for scoring",
            "required_contract": "kernel stubs must have material tensors, parent coefficient values, source/test worldtubes, and numeric normalizers",
            "current_status": "EXISTING_MATRICES_ARE_STUBS_NONCLAIM",
            "missing_for_claim": "parent Delta_w_eff; material tensors; range kernels; operator matrix; clock sensitivity; orbital source map",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/local_bounds/Delta_w_projection_matrix_2652_NONCLAIM.csv")),
                    str(path_for("source-intake/beta-source/docs/K_PROJECTION_MATRIX_2439_NONCLAIM.csv")),
                ]
            ),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "do not treat existing matrices as numeric evidence",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "PRA2684_2_no_cross_arena_cancellation",
            "projection_claim": "one arena can hide another by fitted cancellation",
            "required_contract": "absolute no-cancellation envelopes are per arena and cannot cancel across WEP/R10/PPN/clock/orbital units",
            "current_status": "NO_CROSS_ARENA_CANCELLATION_POLICY_ENFORCED",
            "missing_for_claim": "numeric absolute envelope for every arena",
            "source_paths": str(path_for("source-intake/beta-source/docs/K_PROJECTION_MATRIX_2439_NONCLAIM.csv")),
            "gate_pass": "true",
            "valid_for_claim": "false",
            "next_action": "keep this as a refusal guard, not a claim",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "PRA2684_3_theorem_zero_escape",
            "projection_claim": "projection matrix unnecessary if source-prefactor target is parent-zero",
            "required_contract": "parent zero theorem must kill coefficient values and projection-silence/readout tails in every arena",
            "current_status": "THEOREM_ZERO_ESCAPE_OPEN_NOT_SIGNED",
            "missing_for_claim": "source-prefactor target absence; hidden scalar triviality; action-line owner; readout/radiative closure; projection silence",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "return to parent zero theorem as the clean derivation route",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "PRA2684_4_verdict",
            "projection_claim": "local source-prefactor branch is score-ready",
            "required_contract": "all arena matrix rows pass and all finite source-pack rows are sourced or zero-certified",
            "current_status": "ARENA_PROJECTION_MATRIX_STAGED_NONCLAIM_BRANCH_BLOCKED",
            "missing_for_claim": "finite coefficients plus arena projections plus common normalizer",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2683_FINITE_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "try parent source-prefactor zero theorem before filling numeric rows",
            "timestamp_utc": stamp(),
        },
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "APM2684_0_WEP",
            "WEP_MICROSCOPE_TiPt",
            "eta_TiPt",
            "eta_TiPt = K_WEP[Ti,Pt,Earth,readout] * tau_WEP * epsilon_prefactor_total + tail_WEP",
            "dimensionless eta",
            "positive absolute eta contribution",
            "official Ti/Pt material tensor; Earth source worldtube; tau_WEP; K_WEP; common source normalizer",
            "MISSING_WEP_MATERIAL_TENSOR_TAU_AND_PARENT_VALUES",
            "source-intake/local_bounds/Delta_w_projection_matrix_2652_NONCLAIM.csv",
        ),
        (
            "APM2684_1_R10",
            "R10_short_range",
            "alpha_Yukawa(lambda)",
            "alpha_pref(lambda)=K_R10(lambda)*tau_R10(lambda)*Qbar_source_test(lambda)*epsilon_prefactor_total + tail_R10(lambda)",
            "dimensionless alpha(lambda)",
            "positive absolute alpha(lambda) contribution",
            "range kernel; lambda grid; source/test composition; tau_R10; Qbar; real bound curve; parent values",
            "MISSING_R10_RANGE_KERNEL_TAU_QBAR_AND_PARENT_VALUES",
            "source-intake/beta-source/docs/PARENT_QLOC_R10_ALPHA_TEMPLATE_2194_NONCLAIM.csv",
        ),
        (
            "APM2684_2_PPN",
            "PPN_source_weight_vector",
            "Delta gamma; Delta beta; alpha_i; xi",
            "Delta_PPN_source = M_PPN * epsilon_prefactor_total + retained q_loc/readout/boundary legs",
            "dimensionless PPN deviations",
            "componentwise absolute PPN vector contribution",
            "weak-field operator matrix; GR limit matching; source/test split; common GM convention; parent values",
            "MISSING_PPN_OPERATOR_MATRIX_GR_LIMIT_AND_PARENT_VALUES",
            "source-intake/local_bounds/Full_PPN_vector_ledger_2631_NONCLAIM.csv",
        ),
        (
            "APM2684_3_clock",
            "clock_and_constant_drift",
            "Delta ln nu_i or d ln alpha/dt",
            "Delta ln nu_i = K_clock_i * tau_clock * epsilon_prefactor_total + alpha/mass/readout tails",
            "dimensionless shift or yr^-1 drift after declared time normalizer",
            "positive absolute clock drift/shift contribution",
            "clock sensitivity vector; observed time map; tau_clock; alpha/mass split; parent values",
            "MISSING_CLOCK_SENSITIVITY_TAU_TIME_AND_PARENT_VALUES",
            "source-intake/clocks/branch_locked_local/P8_Y5_2675_CLOCK_READOUT_ROWS_NONCLAIM.csv",
        ),
        (
            "APM2684_4_orbital",
            "orbital_GM_inverse_square",
            "Delta ln(GM)_obs; inverse-square residual",
            "Delta ln(GM)_obs = K_orbital * tau_orbital * epsilon_prefactor_total + finite-range/projector/readout tails",
            "dimensionless GM/source deviation",
            "positive absolute orbital residual contribution",
            "source body composition; orbital GM convention; inverse-square kernel; tau_orbital; parent values",
            "MISSING_ORBITAL_SOURCE_MAP_TAU_AND_PARENT_VALUES",
            "source-intake/local_bounds/Delta_w_projection_matrix_2652_NONCLAIM.csv",
        ),
        (
            "APM2684_5_Newton_source",
            "Newton_Poisson_source_normalization",
            "Delta rho_H/rho_H or Delta G_source",
            "nabla^2 U = 4*pi*G_parent*rho_H + K_Newton*tau_Newton*epsilon_prefactor_total + residuals",
            "dimensionless source normalization",
            "positive absolute Newton-source residual",
            "G_parent owner; Hilbert source normalization; measured-GM transfer; parent values",
            "MISSING_NEWTON_SOURCE_NORMALIZATION_AND_PARENT_VALUES",
            "source-intake/local_bounds/Conditional_local_GR_theorem_2633_NONCLAIM.csv",
        ),
        (
            "APM2684_6_total_envelope",
            "all_local_arenas",
            "B_total_abs",
            "B_total_abs = sum_arena |K_arena*tau_arena*epsilon_prefactor_total| with no cross-arena cancellation",
            "arena-declared absolute envelopes",
            "NO_CROSS_ARENA_CANCELLATION_ALLOWED",
            "all arena rows plus common source normalizer and all finite source-pack coefficients",
            "MISSING_ALL_ARENA_NUMERIC_ENVELOPES",
            "source-intake/beta-source/docs/K_PROJECTION_MATRIX_2439_NONCLAIM.csv",
        ),
    ]
    return [
        {
            "projection_id": row[0],
            "arena": row[1],
            "observable": row[2],
            "projection_formula": row[3],
            "units": row[4],
            "sign_convention": row[5],
            "required_inputs": row[6],
            "source_path": str(path_for(row[8])),
            "common_normalizer_required": "true",
            "no_cancellation_role": "absolute_envelope_component",
            "current_status": row[7],
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def coefficient_arena_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAM2684_0_cIhid", "c(I_hid)", "WEP;R10;clock;PPN;local-GR", "hidden scalar source-prefactor projects wherever the parent source leg enters", "MISSING_PARENT_ZERO_OR_NUMERIC_SOURCE_COEFFICIENT;MISSING_ARENA_KERNELS"),
        ("CAM2684_1_Delta_w_AB", "Delta_w_AB", "WEP;Newton-source;R10;PPN;orbital;local-GR", "pre-action species/source weight projects directly through source/test composition", "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W;MISSING_TAU_K_QBAR_PROJECTIONS"),
        ("CAM2684_2_cA_pre", "c_A_pre or kappa_A", "WEP;PPN;clock;source-normalization;Newton-source", "pre-current normalization shifts the Hilbert/source leg before readout", "MISSING_READOUT_ORDER_THEOREM_OR_C_A_VALUE;MISSING_COMMON_SOURCE_NORMALIZER"),
        ("CAM2684_3_Ceff_tail", "C_eff_source_tail", "EM;clock;R10;WEP;PPN-readout", "readout/radiative tail contributes as additive arena-specific source tail", "MISSING_NO_EXTENSION_OR_NUMERIC_TAIL;MISSING_READOUT_KERNELS"),
        ("CAM2684_4_epsilon_total", "epsilon_prefactor_total", "all local source arenas", "absolute sum of all active source-prefactor components in common source normalizer", "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER"),
    ]
    return [
        {
            "map_id": map_id,
            "symbol": symbol,
            "arena_links": arenas,
            "projection_role": role,
            "required_projection_inputs": "K_pref; tau_arena; observable convention; source/test worldtube; units; source path; sign convention",
            "current_status": status,
            "source_path": str(OUTPUTS["projection_matrix"]),
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive theorem-zero for this coefficient or source its arena projection inputs",
            "timestamp_utc": stamp(),
        }
        for map_id, symbol, arenas, role, status in rows
    ]


def projection_silence_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PSG2684_0_WEP_silence", "WEP projection kernel carries no extra source charge and tau_WEP=0 or sourced", "would kill eta source-prefactor projection", "WEP_PROJECTION_SILENCE_NOT_SIGNED"),
        ("PSG2684_1_R10_silence", "R10 source/test/range kernel carries no independent prefactor and tau_R10=0 or sourced", "would kill alpha(lambda) source-prefactor projection", "R10_PROJECTION_SILENCE_NOT_SIGNED"),
        ("PSG2684_2_PPN_silence", "weak-field PPN operator matrix has no source-prefactor residual leg", "would kill source-weight PPN vector", "PPN_PROJECTION_SILENCE_NOT_SIGNED"),
        ("PSG2684_3_clock_silence", "observed time/clock readout carries no source-prefactor tail", "would kill clock drift source-prefactor projection", "CLOCK_PROJECTION_SILENCE_NOT_SIGNED"),
        ("PSG2684_4_orbital_silence", "orbital GM transfer and inverse-square kernel carry no source-prefactor tail", "would kill orbital/Newton source residual", "ORBITAL_PROJECTION_SILENCE_NOT_SIGNED"),
        ("PSG2684_5_common_source_leg", "one parent source leg feeds WEP, R10, clocks, PPN and orbital tests without arena-specific screens", "would stop arena-by-arena fitting", "SHARED_SOURCE_LEG_OWNER_NOT_SIGNED"),
        ("PSG2684_6_verdict", "all projection-silence gates close", "would permit theorem-zero route to bypass finite projection matrix", "PROJECTION_SILENCE_NOT_PROVED"),
    ]
    return [
        {
            "gate_id": gate_id,
            "projection_silence_clause": clause,
            "if_signed_effect": effect,
            "current_status": status,
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv")),
            "next_action": "prove projection silence or retain finite arena matrix row",
            "timestamp_utc": stamp(),
        }
        for gate_id, clause, effect, status in rows
    ]


def runner_rows(projections: list[dict[str, Any]], maps: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in projections:
        rows.append(
            {
                "runner_id": f"RUN2684_{row['projection_id']}",
                "target_id": row["projection_id"],
                "stage": "arena_projection_matrix",
                "has_K_pref": "false",
                "has_tau_arena": "false",
                "has_common_normalizer": "false",
                "has_parent_values": "false",
                "bound_inversion_used": "false",
                "missing_blocker": row["current_status"],
                "score_ready": "false",
                "valid_for_claim": "false",
                "runner_verdict": "REFUSE_SCORE_PROJECTION_ROW_STUB_ONLY",
                "timestamp_utc": stamp(),
            }
        )
    rows.append(
        {
            "runner_id": "RUN2684_COEFFICIENT_MAP_VERDICT",
            "target_id": "coefficient_arena_map",
            "stage": "coefficient_to_arena_map",
            "has_K_pref": "false",
            "has_tau_arena": "false",
            "has_common_normalizer": "false",
            "has_parent_values": "false",
            "bound_inversion_used": "false",
            "missing_blocker": ";".join(row["current_status"] for row in maps),
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": "COEFFICIENT_MAP_NONCLAIM",
            "timestamp_utc": stamp(),
        }
    )
    rows.append(
        {
            "runner_id": "RUN2684_PROJECTION_SILENCE_VERDICT",
            "target_id": "projection_silence_gates",
            "stage": "theorem_zero_projection_silence",
            "has_K_pref": "n/a",
            "has_tau_arena": "n/a",
            "has_common_normalizer": "n/a",
            "has_parent_values": "false",
            "bound_inversion_used": "false",
            "missing_blocker": ";".join(row["gate_id"] for row in gates if row["parent_signed"] == "false"),
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": "PROJECTION_SILENCE_NOT_PROVED",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2684_0_projection_matrix_complete", "all arena K_pref/tau rows have numeric/source-backed values", "FAIL", "arena rows are stubs with missing kernels, tau factors and parent values"),
        ("CG2684_1_source_pack_complete", "finite source-prefactor coefficients are zero-certified or independently sourced", "FAIL", "2683 source-pack rows remain MISSING"),
        ("CG2684_2_common_normalizer_complete", "all arenas use one declared source-normalized basis", "FAIL", "common normalizer is still missing"),
        ("CG2684_3_no_bound_inversion", "experimental bounds are not used as coefficient/projection values", "PASS_GUARD_ONLY", "runner keeps all bound-inversion shortcuts refused"),
        ("CG2684_4_theorem_zero_projection_silence", "projection silence/theorem-zero route closes", "FAIL", "projection silence gates are unsigned"),
        ("CG2684_5_local_GR_or_empirical_claim", "WEP/R10/PPN/clock/orbital/local-GR promotion", "REFUSED", "2684 is a projection gate only and cannot claim a pass"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": "true" if status == "PASS_GUARD_ONLY" else "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2684_0_private_verdict",
            "decision": "ARENA_PROJECTION_MATRIX_STAGED_NONCLAIM",
            "rationale": "the local coupling branch now has explicit WEP/R10/PPN/clock/orbital projection rows, but every row is missing parent values and kernels",
            "claim_allowed": "false",
            "next_action": "try parent source-prefactor zero theorem before sourcing numeric projection rows",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2684_1_best_route",
            "decision": "DERIVATION_FIRST_RECOMMENDED",
            "rationale": "a theorem-zero/no-source-prefactor proof would remove the whole finite projection burden and is less scrutiny-prone than fitting K/tau rows",
            "claim_allowed": "false",
            "next_action": "2685 parent source-prefactor zero theorem minimal contract or Delta_w first input",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2684_2_fallback_route",
            "decision": "IF_ZERO_THEOREM_FAILS_FILL_DELTA_W_FIRST",
            "rationale": "Delta_w_AB is the highest-leverage finite coupling row because it touches WEP, Newton-source, R10, PPN and orbital tests",
            "claim_allowed": "false",
            "next_action": "do not fill c_A or C_eff before Delta_w/common normalizer is disciplined",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2684_0_selected",
            "kind": "selected",
            "target_doc": "2685-Y5-R2FR-parent-source-prefactor-zero-theorem-minimal-contract-or-delta-w-first-input.md",
            "target_script": "scripts/Y5_R2FR_parent_source_prefactor_zero_theorem_minimal_contract_or_delta_w_first_input_2685.py",
            "purpose": "attempt the clean derivation: prove no parent source-prefactor target/no arena-specific source leg; if it fails, demote to the first independent Delta_w_AB source/projection input contract",
            "acceptance_gate": "either every zero-theorem premise is parent-signed, or Delta_w_AB remains nonclaim with explicit source, units, K/tau projection, common normalizer and no-cancellation requirements",
            "forbidden_shortcuts": "assuming Delta_w=0; using WEP/R10 bounds as Delta_w values; importing existing projection stubs as numeric; treating post-current c_A as pre-current c_A; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2684_0_coupling", "local coupling / GR-reduction spine", "FINITE_PROJECTION_BURDEN_EXPLICIT", "we now know exactly which arena projection rows are needed before a finite coupling can touch data"),
        ("STATUS2684_1_derivation", "parent source-prefactor zero route", "BEST_ROUTE_NEXT", "deriving no source-prefactor target would beat a long finite-input programme and is the clean GR-reduction path"),
        ("STATUS2684_2_testing", "WEP/R10/PPN/clock/orbital", "TESTING_STILL_BLOCKED_FROM_THIS_BRANCH", "local tests require coefficients and projection kernels, not just comparison bounds"),
    ]
    return [
        {
            "status_id": status_id,
            "sector": sector,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "false",
            "next_action": "run 2685 derivation-first zero theorem target",
            "timestamp_utc": stamp(),
        }
        for status_id, sector, status, meaning in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2684_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(source_rows: list[dict[str, Any]], audit: list[dict[str, Any]], projections: list[dict[str, Any]], maps: list[dict[str, Any]], gates: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    audit_nonclaim = all(row["valid_for_claim"] == "false" for row in audit)
    projection_rows_blocked = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" and row["current_status"].startswith("MISSING") for row in projections)
    map_rows_blocked = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in maps)
    silence_unsigned = all(row["parent_signed"] == "false" and row["claim_allowed"] == "false" for row in gates)
    runner_refuses = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner)
    claim_blocked = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    no_bound_inversion_guard = any(row["gate_id"] == "CG2684_3_no_bound_inversion" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2685" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2684_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2684_audit_nonclaim", audit_nonclaim, "projection audit rows remain nonclaim"),
        ("VAL2684_projection_rows_blocked", projection_rows_blocked, "all arena projection rows are blocked stubs"),
        ("VAL2684_coefficient_map_blocked", map_rows_blocked, "all coefficient-to-arena rows retain MISSING blockers"),
        ("VAL2684_projection_silence_unsigned", silence_unsigned, "projection-silence theorem gates remain unsigned"),
        ("VAL2684_runner_refuses_stubs", runner_refuses, "runner refuses every projection stub"),
        ("VAL2684_claim_gates_block_claims", claim_blocked, "all claim gates block promotion"),
        ("VAL2684_no_bound_inversion_guard", no_bound_inversion_guard, "bound-inversion refusal guard remains active"),
        ("VAL2684_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2684_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2684_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2684_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2684_next_target_selected", next_target_ok, "2685 derivation-first target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2684_OVERALL",
            "passed": as_bool(overall),
            "detail": "2684 stages the source-prefactor arena projection matrix as nonclaim and selects a derivation-first zero-theorem target",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(source_rows: list[dict[str, Any]], audit: list[dict[str, Any]], projections: list[dict[str, Any]], maps: list[dict[str, Any]], gates: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_target: list[dict[str, Any]], status: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2684 — Y5/R2FR Source-Prefactor Arena Projection Matrix or Theorem-Zero Return",
                "",
                "## Private Verdict",
                "",
                "The finite coupling branch can now be written as a disciplined projection problem: every local arena needs `K_pref`, `tau_arena`, a common source normalizer, a sign convention, source paths, and an absolute no-cancellation role.",
                "",
                "The existing corpus already has WEP/R10/PPN/clock/orbital projection stubs, but they remain stubs. They do not contain parent coefficient values, numeric kernels, common normalizers, or projection-silence theorems.",
                "",
                "Best next route: try the parent source-prefactor zero theorem. If it closes, we avoid fitting a forest of local coupling rows. If it fails, `Delta_w_AB` should be the first finite input because it touches WEP, Newton-source, R10, PPN, and orbital arenas.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Projection Requirements Audit",
                "",
                markdown_table(audit),
                "",
                "## Arena Projection Matrix",
                "",
                markdown_table(projections),
                "",
                "## Coefficient-To-Arena Map",
                "",
                markdown_table(maps),
                "",
                "## Projection-Silence Gates",
                "",
                markdown_table(gates),
                "",
                "## Runner Results",
                "",
                markdown_table(runner),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    audit = projection_audit_rows()
    projections = projection_matrix_rows()
    maps = coefficient_arena_map_rows()
    gates = projection_silence_gate_rows()
    runner = runner_rows(projections, maps, gates)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["projection_audit"], audit)
    write_csv(OUTPUTS["projection_matrix"], projections)
    write_csv(OUTPUTS["coefficient_arena_map"], maps)
    write_csv(OUTPUTS["projection_silence_gates"], gates)
    write_csv(OUTPUTS["runner_results"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_projection_matrix"], projections)
    write_csv(BRANCH_OUTPUTS["local_coefficient_arena_map"], maps)
    write_csv(BRANCH_OUTPUTS["local_projection_silence"], gates)
    write_csv(BRANCH_OUTPUTS["wep_projection_matrix"], projections)
    write_csv(BRANCH_OUTPUTS["source_weight_projection_matrix"], projections)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, audit, projections, maps, gates, runner, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, audit, projections, maps, gates, runner, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
