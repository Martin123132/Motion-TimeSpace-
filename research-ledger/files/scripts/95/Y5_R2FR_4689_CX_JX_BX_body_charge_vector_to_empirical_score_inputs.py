from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4689"
CLAIM_ID = "L-531"
MARKER = "PPC4161_BODY_CHARGE_SCORE_VECTOR_CURRENT_BRANCH_4689"
PACKET_MARKER = "PPC4161_PACKET_BODY_CHARGE_SCORE_VECTOR_CURRENT_BRANCH_4689"
DECISION = "BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4690-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"

DOC_PATH = POST / "4689-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
FORMAL_PATH = FORMAL / "705-PPC4161-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4688_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4688_NEXT_TARGET.csv"
CSV_4688_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4688_STATUS.csv"
CSV_4601_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4601_BODY_CHARGE_SCORE_VECTOR.csv"
CSV_4601_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4601_FIELD_OPERATOR_INPUTS.csv"
CSV_4601_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4601_ARENA_SCORE_MATRIX.csv"
CSV_4601_MISSING = SOURCE_DIR / "P8_Y5_R2FR_4601_MISSING_INPUT_LEDGER.csv"
CSV_4601_SCHEMA = SOURCE_DIR / "P8_Y5_R2FR_4601_NONCLAIM_RUNNER_SCHEMA.csv"
CSV_4601_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4601_CONTROL_ROWS.csv"
CSV_4601_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4601_STATUS.csv"
CSV_4601_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4601_NEXT_TARGET.csv"
CSV_4601_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4601_VALIDATION.csv"
CSV_4602_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4602_STATUS.csv"
CSV_4602_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4602_NEXT_TARGET.csv"
CSV_4602_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4602_VALIDATION.csv"
FORMAL_617 = FORMAL / "617-PPC4161-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4689_SOURCE_REGISTER.csv"
VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_BODY_CHARGE_SCORE_VECTOR.csv"
OPERATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_FIELD_OPERATOR_INPUTS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_ARENA_SCORE_MATRIX.csv"
MISSING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_MISSING_INPUT_LEDGER.csv"
SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_NONCLAIM_RUNNER_SCHEMA.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4689_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4689_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4689_00_4688_next", CSV_4688_NEXT, "4689-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md", "4688 selected score-vector target."),
        ("SRC4689_01_4688_status", CSV_4688_STATUS, "PPC4161_BOUNDARY_NONHILBERT_GATE_CURRENT_BRANCH_4688", "4688 current branch status."),
        ("SRC4689_02_4601_vector", CSV_4601_VECTOR, "BCV4601_15", "4601 body-charge score vector."),
        ("SRC4689_03_4601_operator", CSV_4601_OPERATOR, "OP4601_0_common", "4601 operator/range/amplitude law."),
        ("SRC4689_04_4601_arena", CSV_4601_ARENA, "ASM4601_4", "4601 arena score matrix."),
        ("SRC4689_05_4601_missing", CSV_4601_MISSING, "MIS4601_0_operator_range", "4601 missing input ledger."),
        ("SRC4689_06_4601_schema", CSV_4601_SCHEMA, "RS4601_19", "4601 nonclaim runner schema."),
        ("SRC4689_07_4601_controls", CSV_4601_CONTROLS, "CTRL4601_range_first", "4601 controls."),
        ("SRC4689_08_4601_status", CSV_4601_STATUS, "PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601", "4601 status."),
        ("SRC4689_09_4601_next", CSV_4601_NEXT, "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md", "4601 next target."),
        ("SRC4689_10_4601_validation", CSV_4601_VALIDATION, "VAL4601_OVERALL", "4601 validation passed."),
        ("SRC4689_11_4602_status", CSV_4602_STATUS, "PPC4161_ZX_MX2_LAMBDAX_RANGE_OWNER_OR_BODY_CHARGE_SCORE_FIRST_FILL_4602", "4602 next rung exists."),
        ("SRC4689_12_4602_next", CSV_4602_NEXT, "4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md", "4602 next target."),
        ("SRC4689_13_4602_validation", CSV_4602_VALIDATION, "VAL4602_OVERALL", "4602 validation passed."),
        ("SRC4689_14_formal617", FORMAL_617, "(-Z_X nabla^2 + M_X^2) delta_X", "formal score-vector interface."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BCV4689_00", "memory", "Z_mem", "operator normalization", "positive numeric/source-backed value or theorem normalization"),
        ("BCV4689_01", "memory", "M2_mem", "operator mass gap", "positive numeric/source-backed value; lambda_mem convention"),
        ("BCV4689_02", "memory", "lambda_mem", "range", "derived from Z_mem/M2_mem with units"),
        ("BCV4689_03", "memory", "B_mem_eff", "curvature/source-normalization source vector", "component zeros or absolute B vector values"),
        ("BCV4689_04", "memory", "C_mem^final_live", "matter-trace coupling", "all C subblocks zero or source-backed norms"),
        ("BCV4689_05", "memory", "J_mem_live", "direct/Poynting/non-Hilbert current", "zero certificate or flux/current profile"),
        ("BCV4689_06", "memory", "Q_boundary_mem", "Green boundary charge", "no-flux/topological theorem or finite boundary integral"),
        ("BCV4689_07", "memory", "W_mem/body profile", "body profile and screening kernel", "body radius/profile/source units"),
        ("BCV4689_08", "fibre", "Z_h", "operator normalization", "positive numeric/source-backed value or theorem normalization"),
        ("BCV4689_09", "fibre", "M2_h", "operator mass gap", "positive numeric/source-backed value; lambda_h convention"),
        ("BCV4689_10", "fibre", "lambda_h", "range", "derived from Z_h/M2_h with units"),
        ("BCV4689_11", "fibre", "B_h", "curvature/source fibre source vector", "parent action exclusion or finite coefficient"),
        ("BCV4689_12", "fibre", "C_h^final_live", "matter-trace fibre coupling", "all C subblocks zero or source-backed norms"),
        ("BCV4689_13", "fibre", "J_h_live", "direct/Poynting/non-Hilbert fibre current", "zero certificate or flux/current profile"),
        ("BCV4689_14", "fibre", "Q_boundary_h", "Green boundary charge", "no-flux/topological theorem or finite boundary integral"),
        ("BCV4689_15", "fibre", "W_h/body profile", "body profile and screening kernel", "body radius/profile/source units"),
    ]
    anchors = {
        "Z_mem": "4595 schema4595_0_memory_Z;4506 BCIN4506_0_memory_density",
        "M2_mem": "4595 schema4595_1_memory_M2;4524 RAI4524_4_mass_range",
        "lambda_mem": "lambda_mem=sqrt(Z_mem/M2_mem)",
        "B_mem_eff": "4595 BM4595_5_combined;4514 BMV4514_6_combined",
        "C_mem^final_live": "4688 BU4688_1_memory;4688 C4688_4_final",
        "J_mem_live": "4596 J4596_5_live_total",
        "Q_boundary_mem": "4595 schema4595_5_memory_boundary;4688 BU4688_3_boundary_separation",
        "W_mem/body profile": "4505 BC4505_2_absolute_bound;4514 BCB4514_3_amplitude",
        "Z_h": "4595 schema4595_6_fibre_Z;4506 BCIN4506_1_fibre_density",
        "M2_h": "4595 schema4595_7_fibre_M2;4524 RAI4524_4_mass_range",
        "lambda_h": "lambda_h=sqrt(Z_h/M2_h)",
        "B_h": "4595 schema4595_8_fibre_B",
        "C_h^final_live": "4688 BU4688_2_fibre;4688 C4688_4_final",
        "J_h_live": "4596 J4596_5_live_total",
        "Q_boundary_h": "4595 schema4595_11_fibre_boundary;4688 BU4688_3_boundary_separation",
        "W_h/body profile": "4505 BC4505_2_absolute_bound;4595 FIB4595_2_amplitude",
    }
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "sector": sector,
            "symbol": symbol,
            "role": role,
            "source_anchor": anchors[symbol],
            "required_for_claim": required,
            "score_status": "MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, sector, symbol, role, required in data
    ]


def operator_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("OP4689_0_common", "common_X", "(-Z_X nabla^2 + M_X^2) delta_X = rho_X", "rho_X = B_X R_obs + C_X^final_live T + J_X^live", "lambda_X=sqrt(Z_X/M_X^2)", "|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|)", "Z_X>0, M_X^2>0, zero modes removed, and B_X=C_X^final_live=J_X^live=Q_boundary_X=0 in the same parent branch", "DERIVED_STRUCTURE_VALUES_MISSING"),
        ("OP4689_1_memory", "memory", "(-Z_mem nabla^2 + M2_mem) delta_m = rho_mem", "rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live", "lambda_mem=sqrt(Z_mem/M2_mem)", "|A_mem| <= [exp(R_body/lambda_mem) int_body (|B_mem_eff||R_obs|+|C_mem^final_live||T|+|J_mem_live|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)", "B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0 plus positive L_mem", "MEMORY_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING"),
        ("OP4689_2_fibre", "fibre", "(-Z_h nabla^2 + M2_h) delta_h = rho_h", "rho_h = B_h R_obs + C_h^final_live T + J_h_live", "lambda_h=sqrt(Z_h/M2_h)", "|A_h| <= [exp(R_body/lambda_h) int_body (|B_h||R_obs|+|C_h^final_live||T|+|J_h_live|) dV + |Q_boundary_h|]/(4*pi |Z_h|)", "B_h=C_h^final_live=J_h_live=Q_boundary_h=0 plus positive L_h", "FIBRE_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": operator_id,
            "sector": sector,
            "field_equation": equation,
            "source_density": source_density,
            "range_law": range_law,
            "amplitude_bound": amplitude_bound,
            "zero_switch": zero_switch,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for operator_id, sector, equation, source_density, range_law, amplitude_bound, zero_switch, status in data
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ASM4689_0", "R10", "short-range inverse-square", "alpha_X(lambda_X) from A_X or K_R10_X Qbar_XS qbar_XT/(G_N M_S m_T M_X^2)", "Z_X;M_X^2;lambda_X;B_X;C_X^final_live;J_X_live;Q_boundary_X;K_R10_X;Qbar_XS;qbar_XT;alpha_bound(lambda)", "full source-backed alpha(lambda) curve and MTS projection convention"),
        ("ASM4689_1", "PPN", "gamma,beta,alpha_i,xi,zeta_i,Gdot", "Delta p_i <= sum_X ||K_iX|| |A_X| + direct_tail_i", "A_X vector;K_gamma,K_beta,K_alpha_i,K_xi,K_zeta,K_Gdot;EH principal block;survivor tails", "compare against GR baseline and PPN limits without absorbing into fitted G/GM"),
        ("ASM4689_2", "clock_WEP", "clock redshift, WEP eta, material universality", "Delta O <= K_C C_X^final_live + K_shadow E_shadow_projector + K_std C_X^std_weight_live + material_tail", "material sensitivities;clock kernels;source/test composition;standard/weight rows;shadow rows", "source-backed material coefficients and same-frame calibration"),
        ("ASM4689_3", "orbital_GM", "orbital acceleration/light-time/GM transfer", "Delta a/a_N = alpha_X (1+r/lambda_X) exp(-r/lambda_X) plus boundary/reference drift terms", "alpha_X;lambda_X;Q_boundary_X;Delta_symp_X;J_boundary_X;C_X^final_live;GM calibration rule;orbital threshold", "no absorption into fitted GM unless a separate nuisance/control branch is declared"),
        ("ASM4689_4", "EM_Poynting", "EM stress, Poynting flux, alpha_EM/current owner", "Delta O_EM <= K_EM(|J_X^EM_open|+|Delta_Hodge_EM_X|+|Phi_EM_rad|+|C_XF2|+|b_alpha|)", "same-Hodge/current owner;closed collar or Poynting flux profile;EM readout tail;units", "stationary no-flux theorem or sourced radiative/open-flux profile"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": arena_id,
            "arena": arena,
            "observable_target": observable,
            "score_law": score_law,
            "required_inputs": required_inputs,
            "acceptance_gate": acceptance_gate,
            "score_status": "SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for arena_id, arena, observable, score_law, required_inputs, acceptance_gate in data
    ]


def missing_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("MIS4689_0_operator_range", "Z_X,M_X^2,lambda_X", "parent quadratic operator/eigenvalue with unit convention", "4690 target"),
        ("MIS4689_1_body_source_vector", "B_X,C_X^final_live,J_X_live,Q_boundary_X", "component zero certificates or finite source-backed values", "after range owner"),
        ("MIS4689_2_body_profile", "R_body,R_obs,T,W_X,screening", "body/source profile in declared units", "before any numeric amplitude"),
        ("MIS4689_3_source_test_charges", "Qbar_XS,qbar_XT,M_S,m_T,G_N", "same-frame source/test charge and calibration convention", "before R10 alpha"),
        ("MIS4689_4_arena_kernels", "K_R10,K_PPN,K_clock,K_orbit,K_EM", "transfer operators with dimensions and baseline convention", "before scoring"),
        ("MIS4689_5_external_bounds", "alpha_bound(lambda),PPN/clock/orbital thresholds", "source-backed bounds or official tables", "before pass/fail claim"),
        ("MIS4689_6_EM_flux", "Phi_EM_rad,Delta_Hodge_EM,C_XF2,b_alpha", "stationary no-flux theorem or finite EM/Poynting profile", "before EM branch scoring"),
        ("MIS4689_7_no_cancellation", "component signs/correlation", "parent-owned cancellation if not using absolute sums", "default absolute envelope"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "missing_id": missing_id,
            "missing_input": missing_input,
            "required_evidence": evidence,
            "priority": priority,
            "current_status": "MISSING_BLOCKS_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for missing_id, missing_input, evidence, priority in data
    ]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RS4689_00", "run_id", "string", "unique run tag"),
        ("RS4689_01", "sector", "enum(memory,fibre)", "which X sector is scored"),
        ("RS4689_02", "arena", "enum(R10,PPN,clock_WEP,orbital_GM,EM_Poynting)", "test arena"),
        ("RS4689_03", "Z_X", "numeric_or_THEOREM_ZERO", "operator normalization"),
        ("RS4689_04", "M2_X", "numeric_or_THEOREM_ZERO", "operator mass gap"),
        ("RS4689_05", "lambda_X", "numeric", "range in declared units"),
        ("RS4689_06", "B_X_norm", "numeric_or_zero_certificate", "curvature/source vector norm"),
        ("RS4689_07", "C_X_final_norm", "numeric_or_zero_certificate", "final matter-trace coupling norm"),
        ("RS4689_08", "J_X_live_norm", "numeric_or_zero_certificate", "live current norm"),
        ("RS4689_09", "Q_boundary_X_norm", "numeric_or_zero_certificate", "Green boundary charge norm"),
        ("RS4689_10", "K_arena", "numeric_or_matrix", "arena transfer kernel"),
        ("RS4689_11", "source_charge", "numeric_or_zero_certificate", "source body charge"),
        ("RS4689_12", "test_charge", "numeric_or_zero_certificate", "test body charge"),
        ("RS4689_13", "calibration", "string_with_units", "G_N/GM/source convention"),
        ("RS4689_14", "bound_reference", "source_path_or_url", "empirical bound source"),
        ("RS4689_15", "predicted_value", "numeric", "computed residual or alpha"),
        ("RS4689_16", "units", "string", "units for every numeric input"),
        ("RS4689_17", "source_paths", "semicolon_paths", "local/web provenance"),
        ("RS4689_18", "valid_for_claim", "boolean", "true only when all numeric/theorem/source conditions pass"),
        ("RS4689_19", "blockers", "semicolon_strings", "missing fields if invalid"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "column_id": column_id,
            "column_name": column_name,
            "type": type_name,
            "meaning": meaning,
            "required_before_claim": True,
            "schema_status": "REQUIRED_COLUMN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for column_id, column_name, type_name, meaning in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4689_0_score_vector", "body-charge score vector", "memory/fibre source components named and arena-linked", NEXT_TARGET),
        ("SURV4689_1_operator_range", "Z_X/M_X^2/lambda_X", "first hard blocker for amplitude and R10/PPN projection", NEXT_TARGET),
        ("SURV4689_2_source_terms", "B_X/C_X/J_X/Q_boundary_X", "cannot be numerically scored until operator/range owner exists", "follow after 4690"),
        ("SURV4689_3_empirical_arenas", "R10/PPN/clock/orbital/EM", "interface rows ready but values/bounds/kernels missing", "defer pass/fail claims"),
        ("SURV4689_4_claim_firewall", "local-GR/R10/PPN public claim", "blocked until all required columns are numeric/theorem-zero and sourced", "keep private nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4689": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4689_placeholder_block", "any score row uses MISSING, placeholder, inferred-from-bound, or unsourced numeric values", "valid_for_claim remains false and claim_allowed remains false", "GUARD_ACTIVE"),
        ("CTRL4689_range_first", "B/C/J/Q values are proposed but Z_X,M_X^2,lambda_X are missing", "amplitude and R10 scoring remain blocked", "COUNTERMODEL_CAUGHT"),
        ("CTRL4689_GM_absorption", "orbital or PPN residual is hidden inside fitted G/GM without a declared nuisance comparison", "score row rejected; calibration must be explicit", "GUARD_ACTIVE"),
        ("CTRL4689_Poynting_firewall", "Poynting/EM flux is set to zero by convention rather than same-Hodge closed-collar theorem", "EM_Poynting and J_X_live rows stay open", "COUNTERMODEL_CAUGHT"),
        ("CTRL4689_no_cancellation", "B,C,J,Q terms cancel numerically without a parent signed relation", "absolute-sum bound used; no cancellation credit", "GUARD_ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "input_branch": branch,
            "expected": expected,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, branch, expected, status in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4689 imports the body-charge score-vector interface into the current branch. The local branch now has a declared operator, source-density vector, amplitude bound, arena score matrix, missing-input ledger and nonclaim runner schema. The first hard blocker is Z_X/M_X^2/lambda_X operator-range ownership.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "sector-separated body-charge score vector; field operator/range/amplitude law; R10/PPN/clock/orbital/EM arena score matrix; missing-input ledger; nonclaim runner schema",
            "not_derived": "numeric Z_X/M_X^2/lambda_X; numeric or theorem-zero B_X,C_X,J_X,Q_boundary_X; source/test charges; arena kernels; external bound comparisons; local-GR/R10/PPN pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4689_0",
            "target": NEXT_TARGET,
            "reason": "The score interface shows the first hard blocker is not B/C/J bookkeeping but the operator/range owner: without Z_X,M_X^2 and lambda_X no body-charge amplitude or R10/PPN projection is scoreable.",
            "derive_first": "derive parent quadratic operator normalization, mass gap and range for memory/fibre sectors in the same quotient domain",
            "fallback": "emit the first nonclaim source row for Z_X,M_X^2,lambda_X with explicit units and blockers",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4689 - Y5/R2FR C_X/J_X/B_X Body-Charge Vector To Empirical Score Inputs

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4689 turns the local residual ledger into a test-facing score-vector interface:

```text
(-Z_X nabla^2 + M_X^2) delta_X = B_X R_obs + C_X^final_live T + J_X^live
lambda_X = sqrt(Z_X/M_X^2)

|A_X| <= [exp(R_body/lambda_X) int_body |B_X R_obs + C_X^final_live T + J_X^live| dV
          + |Q_boundary_X|]/(4*pi |Z_X|).
```

Every arena score is now a declared map:

```text
Delta O_a <= sum_X ||K_aX|| |A_X| + |direct_tail_a|.
```

This is not a pass claim. It is the bridge from derivation bookkeeping to empirical scoring. The first hard blocker is now explicit: parent-owned `Z_X`, `M_X^2` and `lambda_X`.

## Source Register

{table(rows["sources"])}

## Body-Charge Score Vector

{table(rows["vectors"])}

## Field Operator Inputs

{table(rows["operators"])}

## Arena Score Matrix

{table(rows["arenas"])}

## Missing Input Ledger

{table(rows["missing"])}

## Nonclaim Runner Schema

{table(rows["schema"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4689 - Y5/R2FR", "# 705 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4689 imports the body-charge score-vector interface into the current branch: field operator, source density, amplitude bound, arena score matrix, missing-input ledger and nonclaim runner schema.",
                "current_evidence": "Generated source register, body-charge score vector, operator inputs, arena matrix, missing-input ledger, runner schema, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Attempting R10/PPN/local-GR scoring before parent-owned Z_X, M_X^2, lambda_X and source/test charge conventions exist.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Body-Charge Score Vector

Marker: `{MARKER}`

4689 turns the local residual ledger into score-ready form:

```text
(-Z_X nabla^2 + M_X^2) delta_X = B_X R_obs + C_X^final_live T + J_X^live,
lambda_X = sqrt(Z_X/M_X^2).
```

This is the bridge from derivation to tests. The first hard blocker is now operator/range ownership: without `Z_X`, `M_X^2` and `lambda_X`, neither body-charge amplitude nor R10/PPN projection is scoreable.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Body-Charge Score Vector

Marker: `{PACKET_MARKER}`

The packet now includes the nonclaim score-vector interface. Any future runner row must carry operator/range inputs, source/test charges, arena kernels, calibration, bound references, units and source paths before `valid_for_claim=true` is allowed.

- vector csv: `{VECTOR_CSV.name}`
- arena csv: `{ARENA_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4689_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4689_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4689_2_memory_and_fibre", {row["sector"] for row in rows["vectors"]} == {"memory", "fibre"}, "memory and fibre score vectors present"),
        ("VAL4689_3_required_symbols", all(symbol in {row["symbol"] for row in rows["vectors"]} for symbol in ["Z_mem", "M2_mem", "lambda_mem", "C_mem^final_live", "Z_h", "M2_h", "lambda_h", "C_h^final_live"]), "required B/C/J/operator symbols present"),
        ("VAL4689_4_operator_law", any("(-Z_X nabla^2 + M_X^2)" in row["field_equation"] for row in rows["operators"]), "operator/range/amplitude law present"),
        ("VAL4689_5_five_arenas", len(rows["arenas"]) == 5, "five arena rows present"),
        ("VAL4689_6_missing_ledger", rows["missing"][0]["missing_input"] == "Z_X,M_X^2,lambda_X", "missing input ledger names hard blocker"),
        ("VAL4689_7_runner_schema", len(rows["schema"]) == 20 and rows["schema"][-1]["column_name"] == "blockers", "runner schema has claim guard columns"),
        ("VAL4689_8_next_range_owner", rows["next"][0]["target"] == NEXT_TARGET, "next range-owner target selected"),
        ("VAL4689_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-531"),
        ("VAL4689_10_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4689_11_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4689_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4689_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4689_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4689_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4689_14_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4689_15_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4689_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "vectors": vector_rows(timestamp),
        "operators": operator_rows(timestamp),
        "arenas": arena_rows(timestamp),
        "missing": missing_rows(timestamp),
        "schema": schema_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        VECTOR_CSV: rows["vectors"],
        OPERATOR_CSV: rows["operators"],
        ARENA_CSV: rows["arenas"],
        MISSING_CSV: rows["missing"],
        SCHEMA_CSV: rows["schema"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
