from __future__ import annotations

import csv
import math
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4840"
CLAIM_ID = "L-682"
MARKER = "PPC4161_SOURCE_ACTION_PULLBACK_SIGNATURE_OR_FIRST_DENSITY_QBASIC_BOUND_ROW_4840"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_ACTION_PULLBACK_SIGNATURE_OR_FIRST_DENSITY_QBASIC_BOUND_ROW_4840"
DECISION = "SOURCE_ACTION_PULLBACK_UNSIGNED_FIRST_DENSITY_QBASIC_BOUND_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md"

DOC_PATH = POST / "4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md"
FORMAL_PATH = FORMAL / "856-PPC4161-source-action-pullback-signature-or-first-density-qbasic-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "source_action_pullback_density_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4840_SOURCE_REGISTER.csv"
PULLBACK_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4840_SOURCE_ACTION_PULLBACK_AUDIT.csv"
CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4840_DENSITY_QBASIC_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4840_DENSITY_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4840_DENSITY_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4840_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4840_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4840_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4840_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4840_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4839_doc": POST / "4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md",
    "4839_output": SOURCE_DIR / "P8_Y5_R2FR_4839_MHREF_RUNNER_OUTPUT.csv",
    "3561_theorem": SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
    "3561_decomp": SOURCE_DIR / "P8_Y5_R2FR_3561_DENSITY_RESIDUAL_DECOMPOSITION.csv",
    "3561_bound": SOURCE_DIR / "P8_Y5_R2FR_3561_BOUND_VECTOR.csv",
    "3293_signature": SOURCE_DIR / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
    "2587_contract": SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "2646_owner": SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
    "2612_nohom": SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
    "3142_em": SOURCE_DIR / "P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv",
    "no_source_only": SOURCE_DIR / "P8_EM_no_source_only_matter_functor_residual.csv",
    "4835_output": SOURCE_DIR / "P8_Y5_R2FR_4835_QBARXT_RUNNER_OUTPUT.csv",
    "4836_output": SOURCE_DIR / "P8_Y5_R2FR_4836_THETA_RUNNER_OUTPUT.csv",
    "source_current": SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def as_float(value: Any) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return math.nan


def close_to(value: Any, target: float, tolerance: float = 1e-14) -> bool:
    number = as_float(value)
    return math.isfinite(number) and abs(number - target) <= tolerance


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4840_00_resume", SOURCES["resume"], "4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md", "4839 selected this pullback target."),
        ("SRC4840_01_4839_doc", SOURCES["4839_doc"], "HSC4839_4_next", "source-action pullback handoff."),
        ("SRC4840_02_4839_output", SOURCES["4839_output"], "RUN4839_4_live_descent_bound_missing", "live source descent row remains blocked."),
        ("SRC4840_03_3561_theorem", SOURCES["3561_theorem"], "HDQ3561_1_pullback_density_theorem", "density q-basic theorem."),
        ("SRC4840_04_3561_countermodel", SOURCES["3561_theorem"], "HDQ3561_3_source_weight_countermodel", "source-only countermodel."),
        ("SRC4840_05_3561_decomp", SOURCES["3561_decomp"], "HDR3561_0_E_action_pullback", "density residual decomposition."),
        ("SRC4840_06_3561_bound", SOURCES["3561_bound"], "BD3561_0_E_action_pullback", "bound vector row."),
        ("SRC4840_07_3293_signature", SOURCES["3293_signature"], "HSSIG3293_0_target", "Hilbert-source signature target."),
        ("SRC4840_08_3293_gap", SOURCES["3293_signature"], "HSSIG3293_3_parent_gap", "parent action descent gap."),
        ("SRC4840_09_2587_contract", SOURCES["2587_contract"], "MCA2587_2_minimal_matter_terms", "minimal matter pullback contract."),
        ("SRC4840_10_2587_no_slot", SOURCES["2587_contract"], "MCA2587_3_no_source_only_slot", "no source-only slot contract."),
        ("SRC4840_11_2646_owner", SOURCES["2646_owner"], "MNO2646_1_conditional_owner_lemma", "single action-density owner."),
        ("SRC4840_12_2612_nohom", SOURCES["2612_nohom"], "HOM2612_0_target", "no-Hom source-only route."),
        ("SRC4840_13_3142_em", SOURCES["3142_em"], "EMQ3142_4_Hilbert_stress", "EM q-basic stress theorem."),
        ("SRC4840_14_no_source_only", SOURCES["no_source_only"], "NSSR3509_0_delta_w_species", "source-only residual rows."),
        ("SRC4840_15_4835_output", SOURCES["4835_output"], "RUN4835_3_live_qbarXT_bound_missing", "matter quotient source row blocked."),
        ("SRC4840_16_4836_output", SOURCES["4836_output"], "RUN4836_2_live_theta_bound_missing", "theta constant row blocked."),
        ("SRC4840_17_source_current", SOURCES["source_current"], "SC1_Hilbert_source_definition", "source current definition."),
        ("SRC4840_18_runner", SOURCES["runner"], "def evaluate_row", "4840 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def pullback_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("SAP4840_0_signature", "Hilbert-source signature", "one descended source functional; local sources are variational derivatives only", "CONDITIONAL_SIGNATURE_EXISTS", "parent action adoption"),
        ("SAP4840_1_pullback", "source action pullback", "S_src=q^*Sbar_src[q(Phi),psi,theta,A_obs]", "CORE_UNSIGNED", "actual MTS parent action or no-extra-slot theorem"),
        ("SAP4840_2_density", "density q-basic theorem", "rho_H dV_H=rhobar_H(q(Phi),psi,theta) if pullback and q-owned measure/time/coframe hold", "EXACT_CONDITIONAL_NOT_LIVE", "sign pullback clauses"),
        ("SAP4840_3_source_weights", "source-only weights", "delta_w_species and kappa_A_source are countermodels if legal", "LIVE_COUNTERMODEL", "single action-density/no-Hom proof"),
        ("SAP4840_4_hidden_marker", "hidden marker source coefficient", "hidden/domain/material labels must not map to active-source prefactors", "LIVE_COUNTERMODEL", "no-Hom hidden marker theorem"),
        ("SAP4840_5_EM", "EM q-basic stress", "owned Maxwell scalar density gives q-basic T_EM; flux remains explicit", "CONDITIONAL_OPEN_FROM_4837", "EM owner or finite flux row"),
        ("SAP4840_6_theta", "constant sector", "theta must be representation/superselection data or retained as derivative row", "OPEN_FROM_4836", "theta derivative or zero theorem"),
        ("SAP4840_7_vertical", "vertical density derivative", "D_v rho_H=0 by chain rule only after Dq(v)=0 and matter/gauge/on-shell terms vanish", "CONDITIONAL_NOT_LIVE", "vertical profile bound if not zero"),
        ("SAP4840_8_anti", "anti-circularity", "no density qbasic assertion, no post-variation selector, no measured GM", "GUARD_ACTIVE", "runner forbidden rows"),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "mathematical_form": form,
            "current_result": result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, form, result, needed in rows
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DQB4840_0_zero", "density q-basic zero", "all source-action pullback, q-owned stack, variation-before-readout, source-only exclusion and EM/theta clauses signed", "conditional_only"),
        ("DQB4840_1_bound", "density_qbasic_residual_abs", "E_action_pullback+delta_w_species+kappa_A+hidden_marker+measure/tau/EM/theta/lift/boundary/nonHilbert/readout terms", "runner_ready_values_missing"),
        ("DQB4840_2_vertical", "vertical_density_residual_abs", "rho_vertical_slope*vertical_amplitude + matter_Euler + gauge_fix + boundary_layer", "runner_ready_values_missing"),
        ("DQB4840_3_feed", "density residual to MHref/Newton feed", "delta_MHref_density=qbar feed -> alpha/BY5 source-normalization rows", "runner_ready_values_missing"),
        ("DQB4840_4_next", "single action-density line", "prove no source-only weights or fill first delta_w_species row", "next_target"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def base_flags() -> dict[str, str]:
    return {"source_signed": "true", "units_signed": "true", "same_branch_signed": "true", "no_cancellation_guard": "true"}


def zero_flags() -> dict[str, str]:
    return {
        **base_flags(),
        "parent_action_diffeomorphic_signed": "true",
        "q_map_signed": "true",
        "observed_stack_q_owned_signed": "true",
        "source_action_pullback_signed": "true",
        "single_action_density_line_signed": "true",
        "variation_before_readout_signed": "true",
        "measure_coframe_time_qbasic_signed": "true",
        "EM_qbasic_or_flux_retained_signed": "true",
        "theta_representation_superselection_signed": "true",
        "no_source_only_weights_signed": "true",
        "no_kappa_A_source_selector_signed": "true",
        "no_hidden_marker_source_signed": "true",
        "matter_labels_fixed_or_on_shell_signed": "true",
        "no_boundary_source_layer_signed": "true",
        "nonHilbert_current_zero_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4840_0_live_pullback_zero_missing",
            "route_type": "pullback_zero",
            "route": "live source-action pullback density zero audit",
            "source_path": str(SOURCES["3561_theorem"]),
            "equation_ref": "HDQ3561_1_pullback_density_theorem;HDQ3561_3_source_weight_countermodel",
            "notes": "current branch has theorem shape but not parent-signed source-action pullback and source-only exclusion",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4840_1_conditional_pullback_zero_pass",
            "route_type": "pullback_zero",
            "route": "conditional parent-signed source-action pullback theorem",
            "source_path": str(SOURCES["3293_signature"]),
            "equation_ref": "HSSIG3293_0_target;HSSIG3293_1_source_only_exclusion",
            "notes": "nonclaim theorem-shape smoke row",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4840_2_live_density_bound_missing",
            "route_type": "pullback_bound",
            "route": "live density q-basic bound row missing",
            "source_path": str(SOURCES["3561_bound"]),
            "equation_ref": "BD3561_0_E_action_pullback;BD3561_1_delta_w_species;BD3561_4_nonHilbert_bypass",
            "notes": "bound vector exists but live coefficients are not source-backed",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4840_3_density_bound_smoke_pass",
            "route_type": "pullback_bound",
            "route": "finite source-action density q-basic smoke",
            "source_path": str(SOURCES["3561_decomp"]),
            "equation_ref": "HDR3561_0_E_action_pullback;HDR3561_1_delta_w_species;HDR3561_4_nonHilbert_bypass",
            "notes": "nonclaim arithmetic smoke for density q-basic residual feed",
            "timestamp_utc": timestamp,
            **base_flags(),
            "E_action_pullback_abs": "0.0010",
            "delta_w_species_abs": "0.0007",
            "kappa_A_source_abs": "0.0008",
            "hidden_marker_source_abs": "0.0006",
            "E_measure_qbasic_abs": "0.0009",
            "E_tau_frame_abs": "0.0005",
            "E_EM_qbasic_abs": "0.0008",
            "E_theta_abs": "0.0006",
            "E_matter_lift_abs": "0.0007",
            "E_boundary_source_abs": "0.0004",
            "E_nonHilbert_bypass_abs": "0.0010",
            "E_readout_mask_abs": "0.0005",
            "P_density_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_density_abs": "2.0",
        },
        {
            "row_id": "RUN4840_4_live_vertical_profile_missing",
            "route_type": "vertical_profile_bound",
            "route": "live vertical density profile row missing",
            "source_path": str(SOURCES["3561_theorem"]),
            "equation_ref": "HDQ3561_2_vertical_zero_corollary",
            "notes": "vertical derivative profile schema exists but no slope/amplitude/source values are filled",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4840_5_vertical_profile_smoke_pass",
            "route_type": "vertical_profile_bound",
            "route": "finite vertical density profile smoke",
            "source_path": str(SOURCES["3561_theorem"]),
            "equation_ref": "HDQ3561_2_vertical_zero_corollary",
            "notes": "nonclaim arithmetic smoke for vertical density residual",
            "timestamp_utc": timestamp,
            **base_flags(),
            "rho_vertical_slope_abs": "0.003",
            "vertical_amplitude_abs": "0.5",
            "matter_Euler_residual_abs": "0.0004",
            "gauge_fix_residual_abs": "0.0003",
            "boundary_layer_abs": "0.0002",
            "P_density_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_density_abs": "2.0",
        },
        {
            "row_id": "RUN4840_6_forbidden_density_assertion",
            "route_type": "pullback_zero",
            "route": "forbidden density qbasic assertion",
            "source_path": str(SOURCES["3561_theorem"]),
            "equation_ref": "HDQ3561_3_source_weight_countermodel",
            "notes": "DENSITY_QBASIC_BY_ASSERTION ignores countermodels",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4840_7_forbidden_source_weight_zero",
            "route_type": "pullback_zero",
            "route": "forbidden source-only weight asserted zero",
            "source_path": str(SOURCES["2646_owner"]),
            "equation_ref": "MNO2646_1_conditional_owner_lemma",
            "notes": "SOURCE_ONLY_WEIGHT_ASSERTED_ZERO is not a proof of one action-density line",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4840_8_forbidden_kappa_selector",
            "route_type": "pullback_bound",
            "route": "forbidden kappa_A selector retained as source",
            "source_path": str(SOURCES["no_source_only"]),
            "equation_ref": "NSSR3509_2_kappa_A_source",
            "notes": "KAPPA_A_SOURCE_SELECTOR cannot be treated as derived Hilbert source",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4840_9_forbidden_EM_dropped",
            "route_type": "pullback_bound",
            "route": "forbidden EM stress dropped",
            "source_path": str(SOURCES["3142_em"]),
            "equation_ref": "EMQ3142_4_Hilbert_stress",
            "notes": "EM_STRESS_DROPPED cannot close density q-basicness",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4840_10_forbidden_measured_GM_source",
            "route_type": "pullback_zero",
            "route": "forbidden measured GM source",
            "source_path": str(SOURCES["4839_doc"]),
            "equation_ref": "no GM laundering",
            "notes": "MEASURED_GM_AS_SOURCE cannot sign source-action pullback",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def row_by_id(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    return next(row for row in rows if row.get("row_id") == row_id)


def status_csv(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "status": "private_nonclaim_gate_installed",
            "live_claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4840_0_reduction",
            "decision": "Density q-basicness is reduced to source-action pullback plus no source-only weights/selectors.",
            "effect": "turns MHref source ownership into parent matter grammar, not a fitted source row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4840_1_nonclaim",
            "decision": "Live density zero and live bound rows remain blocked.",
            "effect": "no local-GR/Newton claim; finite density feed runner is staged",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4840_2_next",
            "decision": NEXT_TARGET,
            "effect": "attack the most dangerous countermodel: source-only action-density weights",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4840_0_theorem", "density q-basic theorem exists", "PASS_CONDITIONAL", "3561 theorem is usable but not parent-signed"),
        ("CG4840_1_pullback_zero", "live pullback zero", "BLOCKED_UNSIGNED", "parent source action and no-source-only clauses are not signed"),
        ("CG4840_2_live_bound", "live density bound row", "BLOCKED_MISSING_VALUES", "bound vector exists but coefficients are missing"),
        ("CG4840_3_vertical_profile", "live vertical profile row", "BLOCKED_MISSING_VALUES", "slope/amplitude/source values are missing"),
        ("CG4840_4_smoke", "runner arithmetic", "PASS_NONCLAIM", "density and vertical profile smoke rows compute"),
        ("CG4840_5_local_GR", "local GR/Newton claim", "NOT_ALLOWED", "source-action pullback remains unsigned"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, meaning in rows
    ]


def compile_ok(path: Path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError:
        return False
    return True


def cleanup_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(timestamp: str, sources: list[dict[str, Any]], outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4840_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4840_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all source needles found")
    add("VAL4840_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4840_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    input_rows = read_csv(RUNNER_INPUT)
    add("VAL4840_04_output_count", len(outputs) == len(input_rows), f"outputs={len(outputs)} inputs={len(input_rows)}")
    add("VAL4840_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "runner hard-codes nonclaim rows")
    live_zero = row_by_id(outputs, "RUN4840_0_live_pullback_zero_missing")
    add("VAL4840_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_SOURCE_ACTION_PULLBACK_ZERO_CLAUSES", live_zero["missing_for_claim"])
    live_bound = row_by_id(outputs, "RUN4840_2_live_density_bound_missing")
    add("VAL4840_07_live_bound_blocked", live_bound["runner_status"] == "BLOCKED_SOURCE_ACTION_DENSITY_BOUND_INPUTS", live_bound["missing_for_claim"])
    density = row_by_id(outputs, "RUN4840_3_density_bound_smoke_pass")
    add("VAL4840_08_density_smoke_values", all([
        close_to(density["source_action_residual_abs"], 0.0031),
        close_to(density["density_qbasic_residual_abs"], 0.0085),
        close_to(density["delta_MHref_density_abs"], 0.0085),
        close_to(density["alpha_source_abs"], 0.0001880625),
        close_to(density["BY5_density_feed_abs"], 0.017),
    ]), "density bound smoke row computes expected source-action and density feed")
    vertical = row_by_id(outputs, "RUN4840_5_vertical_profile_smoke_pass")
    add("VAL4840_09_vertical_smoke_values", all([
        close_to(vertical["vertical_density_residual_abs"], 0.0024),
        close_to(vertical["alpha_source_abs"], 0.0000531),
        close_to(vertical["BY5_density_feed_abs"], 0.0048),
    ]), "vertical profile smoke row computes expected residual feed")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4840_6_") or row["row_id"].startswith("RUN4840_7_") or row["row_id"].startswith("RUN4840_8_") or row["row_id"].startswith("RUN4840_9_") or row["row_id"].startswith("RUN4840_10_")]
    add("VAL4840_10_forbidden_routes_fail", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden shortcuts fail")
    add("VAL4840_11_next_target_recorded", NEXT_TARGET in read_text(NEXT_TARGET_CSV) and NEXT_TARGET in read_text(RESUME_PATH), "next target recorded in CSV and resume")
    cleanup_pycache()
    add("VAL4840_12_no_pycache_left", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_next_target(timestamp: str) -> None:
    write_csv(
        NEXT_TARGET_CSV,
        [
            {
                "checkpoint": CHECKPOINT,
                "next_target": NEXT_TARGET,
                "reason": "4840 reduces density q-basicness to the single action-density/no-source-only-weight theorem.",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        ],
    )


def write_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md`
Marker: `{MARKER}`

## Where we are

4840 attacks the source-action pullback needed by 4839:

```text
S_src = q^* Sbar_src[q(Phi), psi, theta, A_obs]
rho_H dV_H = rhobar_H(q(Phi), psi, theta)
D_v(rho_H dV_H)=0 if Dq(v)=0 and matter/gauge/on-shell terms vanish
```

## Live blockers

- The density theorem exists, but the actual parent source-action pullback is not signed.
- Source-only weights, active-source selectors, hidden marker source coefficients, EM/flux leakage, theta constants, boundary layers and non-Hilbert bypasses remain live unless proved zero or bounded.
- Live density and vertical-profile source rows are still missing numeric/source-backed coefficients.
- Local GR/Newton remains nonclaim until this density source row feeds 4839 and then 4838 with live values.

## Next target

`{NEXT_TARGET}`
""",
    )


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4840 Y5 R2FR source action pullback signature or first density qbasic bound row

**Status:** 4840 reduces the `M_H_ref`/Newton source-denominator problem to the parent matter grammar. If the ordinary matter+EM source action is a pullback through the observed stack, and source-only weights/selectors are illegal, then `rho_H dV_H` is q-basic by the 3561 theorem. The live branch remains nonclaim because the parent source-action pullback and no-source-only theorem are not signed.

**Decision:** `{DECISION}`.

## Core derivation

```text
S_src = q^* Sbar_src[q(Phi), psi, theta, A_obs]
T_H = variation of S_src with respect to g_obs before readout
rho_H dV_H = n_mu tau_nu T_H_mu_nu dSigma_H
rho_H dV_H = rhobar_H(q(Phi), psi, theta)
```

For a vertical direction `v` with `Dq(v)=0`:

```text
D_v(rho_H dV_H) =
  d rhobar_H(Dq(v)) + Euler_matter + gauge + boundary
```

The first term is zero only if the source action really factors through `q` and no source-only coefficient survives.

## Source Register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Pullback Audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Runner Contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner Output

{md_table(outputs, ["row_id", "runner_status", "source_action_residual_abs", "density_qbasic_residual_abs", "vertical_density_residual_abs", "delta_MHref_density_abs", "alpha_source_abs", "BY5_density_feed_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The live local-source problem is now narrowed from “coupling” to a parent matter-grammar theorem.
- The runner distinguishes source-action residual, full density-qbasic residual, and vertical-profile residual.
- The most dangerous countermodel is isolated: relative source-only action-density weights or active-source selectors.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 856 PPC4161 source action pullback signature or first density qbasic bound row

Checkpoint: `{DOC_PATH}`

4840 reduces source-current descent to source-action pullback and density q-basicness. The live route is still blocked, but the next theorem is now the single action-density/no-source-only-weight exclusion.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "source_action_pullback_signature_or_first_density_qbasic_bound_row",
        "current_evidence": "4840 reduces density q-basicness to parent source-action pullback and source-only-weight exclusion; zero/direct-bound/vertical-profile runner branches are staged.",
        "status": "source_action_density_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "single action-density line, no source-only weights/selectors, EM q-basicness, theta constants and live density bound rows remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live density q-basic coefficients are not source-backed",
        "title": "Source action pullback signature or first density qbasic bound row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID not in existing:
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(claim_row.keys()))
            writer.writerow(claim_row)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4840 source-action pullback / density q-basic gate

`{MARKER}`. The local source denominator is now reduced to the parent matter grammar: prove `S_src=q^*Sbar_src` with one action-density line and no source-only weights/selectors, or retain a finite density-qbasic residual feeding `M_H_ref`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4840 source action pullback signature or first density qbasic bound row

`{PACKET_MARKER}`. `{MARKER}` reduces the Hilbert source-density problem to one action-density line and no source-only active-source selectors. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    audit = pullback_audit(timestamp)
    contract = contract_rows(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PULLBACK_AUDIT, audit)
    write_csv(CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(STATUS_CSV, status_csv(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_next_target(timestamp)
    write_resume(timestamp)

    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, audit, contract, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()

    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4840 validation failed: {failed}")
    print(f"4840 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()
