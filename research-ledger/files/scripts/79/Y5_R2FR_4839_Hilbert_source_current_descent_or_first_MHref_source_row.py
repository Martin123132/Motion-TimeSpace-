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

CHECKPOINT = "4839"
CLAIM_ID = "L-681"
MARKER = "PPC4161_HILBERT_SOURCE_CURRENT_DESCENT_OR_FIRST_MHREF_SOURCE_ROW_4839"
PACKET_MARKER = "PPC4161_PACKET_HILBERT_SOURCE_CURRENT_DESCENT_OR_FIRST_MHREF_SOURCE_ROW_4839"
DECISION = "HILBERT_SOURCE_CURRENT_DESCENT_UNSIGNED_FIRST_MHREF_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md"

DOC_PATH = POST / "4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md"
FORMAL_PATH = FORMAL / "855-PPC4161-Hilbert-source-current-descent-or-first-MHref-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "hilbert_source_MHref_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4839_SOURCE_REGISTER.csv"
DESCENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4839_HILBERT_SOURCE_DESCENT_AUDIT.csv"
CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4839_MHREF_SOURCE_ROW_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4839_MHREF_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4839_MHREF_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4839_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4839_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4839_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4839_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4839_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4838_doc": POST / "4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md",
    "4838_output": SOURCE_DIR / "P8_Y5_R2FR_4838_NEWTON_RUNNER_OUTPUT.csv",
    "1016_doc": POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "1017_doc": POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "source_current_contract": SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv",
    "parent_source_identity": SOURCE_DIR / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
    "source_measure": SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "hilbert_current": SOURCE_DIR / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
    "density_qbasic": SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
    "newton_hamiltonian": SOURCE_DIR / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv",
    "newton_residuals": SOURCE_DIR / "P8_Y5_R2FR_3772_NEWTON_GM_RESIDUAL_COEFFICIENTS.csv",
    "4829_output": SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_RUNNER_OUTPUT.csv",
    "4829_contract": SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_BOUND_CONTRACT.csv",
    "em_source": SOURCE_DIR / "P8_Y5_R2FR_3620_MAXWELL_SOURCE_CALIBRATION_GATE.csv",
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
        ("SRC4839_00_resume", SOURCES["resume"], "4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md", "4838 selected this source-current target."),
        ("SRC4839_01_4838_doc", SOURCES["4838_doc"], "KAPPA_G_SOURCE_NEWTON_LIMIT_UNSIGNED_SOURCE_DENOMINATOR_STAGED_NONCLAIM", "Newton bridge handoff."),
        ("SRC4839_02_4838_output", SOURCES["4838_output"], "RUN4838_2_live_Newton_bound_missing", "live Newton source denominator blocked."),
        ("SRC4839_03_1016_schema", SOURCES["1016_doc"], "FIS1016_0_M_H_ref", "first M_H_ref input schema."),
        ("SRC4839_04_1017_schema", SOURCES["1017_doc"], "MHR1017_0_M_H_ref_denominator", "Hamiltonian denominator schema."),
        ("SRC4839_05_source_current", SOURCES["source_current_contract"], "SC1_Hilbert_source_definition", "Hilbert current definition contract."),
        ("SRC4839_06_parent_identity", SOURCES["parent_source_identity"], "I499_3_parent_source_identity", "Hilbert mass closure residual identity."),
        ("SRC4839_07_source_measure", SOURCES["source_measure"], "T509_0_charge_identity_needed", "source measure/exterior flux equality."),
        ("SRC4839_08_Hilbert_def", SOURCES["hilbert_current"], "HC3558_0_same_frame_Hilbert_current_definition", "same-frame Hilbert current definition."),
        ("SRC4839_09_Hilbert_closure", SOURCES["hilbert_current"], "HC3558_2_closure_sufficient_conditions", "closure sufficient conditions."),
        ("SRC4839_10_density", SOURCES["density_qbasic"], "HDQ3561_1_pullback_density_theorem", "density q-basic pullback theorem."),
        ("SRC4839_11_countermodel", SOURCES["density_qbasic"], "HDQ3561_3_source_weight_countermodel", "source-only weight countermodel."),
        ("SRC4839_12_active_mass", SOURCES["newton_hamiltonian"], "NSH3772_2_active_equals_Hilbert", "active mass equals Hilbert mass conditionally."),
        ("SRC4839_13_residual", SOURCES["newton_residuals"], "NGR3772_2_Hamiltonian_Hilbert_charge", "Hamiltonian-Hilbert residual row."),
        ("SRC4839_14_4829_output", SOURCES["4829_output"], "RUN4829_3_live_MHref_missing", "live M_H_ref row remains missing."),
        ("SRC4839_15_4829_contract", SOURCES["4829_contract"], "MHC4829_1_direct_MHref", "direct M_H_ref contract."),
        ("SRC4839_16_EM", SOURCES["em_source"], "MCG3620_2_unique_F2", "EM stress inclusion remains a source clause."),
        ("SRC4839_17_runner", SOURCES["runner"], "def evaluate_row", "4839 executable runner."),
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


def descent_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("HSD4839_0_definition", "same-frame Hilbert current", "J_H[tau]=T_H^{mu nu}[e_obs] n_mu tau_nu dSigma from variation of S_src before readout", "EXACT_CONDITIONAL_DEFINITION", "parent source action and q_obs branch"),
        ("HSD4839_1_density", "Hilbert source density", "rho_H dV_H=n_mu tau_nu T_H^{mu nu}dSigma_H", "EXACT_DEFINITION_UNSIGNED_OWNER", "q-basic source action/measure/time/coframe"),
        ("HSD4839_2_pullback", "source-action pullback", "S_src=q^*Sbar_src[q(Phi),psi,theta,A_obs] with no source-only weights", "CORE_UNSIGNED", "4840 source-action signature"),
        ("HSD4839_3_variation", "variation before readout", "T_H is computed before orbital GM, R10, clock, or fitted readout", "GUARD_ACTIVE", "no post-readout mask"),
        ("HSD4839_4_MHref", "first M_H_ref source row", "M_H_ref=H_tau[S_outer]-H_ref=int_W rho_H dV_H plus tolerances", "RUNNER_READY_VALUES_MISSING", "real source-backed H_tau/H_ref/rho_H row"),
        ("HSD4839_5_Hamiltonian", "Hamiltonian-Hilbert equality", "surface charge equals volume Hilbert mass current in same branch", "CONDITIONAL_UNSIGNED", "integrability/reference/worldtube/PiM closure"),
        ("HSD4839_6_EM", "ordinary EM stress included once", "stationary EM stress belongs in T_H while Poynting/readout residual remains explicit", "OPEN_FROM_4837", "EM normal form or finite residual row"),
        ("HSD4839_7_anti_circularity", "no GM laundering", "M_H_ref is not bare mass, orbital GM, reference-only zero, or fitted normalization", "GUARD_ACTIVE", "forbidden-source runner checks"),
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
        ("HSC4839_0_zero", "Hilbert source descent zero", "all source-action, q-map, variation, q-basic density, worldtube, Hamiltonian and anti-circularity clauses signed", "conditional_only"),
        ("HSC4839_1_direct_MHref", "M_H_ref source row", "H_tau_outer-H_ref equals integral rho_H dV_H equals M_H_ref within tolerances", "runner_ready_values_missing"),
        ("HSC4839_2_descent_bound", "source_descent_residual_abs", "sum retained source-action, variation, qbasic, tau/frame, EM, theta, worldtube, nonHilbert, PiM/Htau and readout-mask residuals", "runner_ready_values_missing"),
        ("HSC4839_3_feed", "delta_MHref to Newton feed", "qbar=P_Newton_qbar*delta_MHref; alpha=K_source*Qbar_source_XH*qbar; BY5=tau*qbar", "runner_ready_values_missing"),
        ("HSC4839_4_next", "source-action pullback signature", "prove or bound S_src=q^*Sbar_src and density q-basicness", "next_target"),
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
        "q_observed_map_signed": "true",
        "matter_action_pullback_signed": "true",
        "variation_before_readout_signed": "true",
        "same_frame_tau_n_dSigma_signed": "true",
        "Hilbert_density_qbasic_signed": "true",
        "compact_worldtube_support_signed": "true",
        "Hamiltonian_surface_charge_match_signed": "true",
        "H_ref_branch_fixed_signed": "true",
        "PiM_identity_chainmap_signed": "true",
        "ordinary_EM_stress_included_once_signed": "true",
        "no_source_only_weights_signed": "true",
        "no_nonHilbert_source_bypass_signed": "true",
        "no_boundary_source_layer_signed": "true",
        "positive_MHref_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4839_0_live_descent_zero_missing",
            "route_type": "source_descent_zero",
            "route": "live Hilbert source descent zero audit",
            "source_path": str(SOURCES["hilbert_current"]),
            "equation_ref": "HC3558_0_same_frame_Hilbert_current_definition;HDQ3561_1_pullback_density_theorem",
            "notes": "current branch has conditional definitions but not parent-signed source action pullback and MHref ownership",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4839_1_conditional_descent_zero_pass",
            "route_type": "source_descent_zero",
            "route": "conditional parent-signed Hilbert source theorem",
            "source_path": str(SOURCES["density_qbasic"]),
            "equation_ref": "HDQ3561_1_pullback_density_theorem",
            "notes": "nonclaim theorem-shape smoke row",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4839_2_live_MHref_source_missing",
            "route_type": "direct_MHref_source",
            "route": "live first M_H_ref source row missing",
            "source_path": str(SOURCES["4829_contract"]),
            "equation_ref": "MHC4829_1_direct_MHref",
            "notes": "schema exists but no source-backed H_tau/H_ref/integral rho_H values",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4839_3_direct_MHref_source_smoke_pass",
            "route_type": "direct_MHref_source",
            "route": "direct first M_H_ref source-row smoke",
            "source_path": str(SOURCES["1017_doc"]),
            "equation_ref": "MHR1017_0_M_H_ref_denominator",
            "notes": "nonclaim arithmetic smoke for surface and volume source-charge consistency",
            "timestamp_utc": timestamp,
            **base_flags(),
            "H_tau_outer_abs": "3.0",
            "H_ref_abs": "1.0",
            "integral_rhoH_abs": "2.002",
            "M_H_ref_abs": "2.0",
            "reference_tolerance_abs": "1e-12",
            "volume_tolerance_abs": "0.01",
            "P_Newton_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_MHref_abs": "2.0",
        },
        {
            "row_id": "RUN4839_4_live_descent_bound_missing",
            "route_type": "source_descent_bound",
            "route": "live finite Hilbert source descent row missing",
            "source_path": str(SOURCES["newton_residuals"]),
            "equation_ref": "NGR3772_1_active_inertial;NGR3772_2_Hamiltonian_Hilbert_charge",
            "notes": "finite row schema is available but coefficients are not source-backed",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4839_5_descent_bound_smoke_pass",
            "route_type": "source_descent_bound",
            "route": "finite Hilbert source descent residual smoke",
            "source_path": str(SOURCES["source_current_contract"]),
            "equation_ref": "SC0_single_observed_coframe_input;SC1_Hilbert_source_definition",
            "notes": "nonclaim arithmetic smoke for descent residual feeding delta_MHref",
            "timestamp_utc": timestamp,
            **base_flags(),
            "E_action_pullback_abs": "0.0010",
            "E_variation_readout_abs": "0.0008",
            "E_measure_qbasic_abs": "0.0009",
            "E_tau_frame_abs": "0.0007",
            "E_EM_once_abs": "0.0008",
            "E_theta_constants_abs": "0.0006",
            "E_worldtube_boundary_abs": "0.0011",
            "E_nonHilbert_current_abs": "0.0010",
            "E_PiM_Htau_abs": "0.0012",
            "E_readout_mask_abs": "0.0005",
            "P_Newton_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_MHref_abs": "2.0",
        },
        {
            "row_id": "RUN4839_6_forbidden_measured_GM_source",
            "route_type": "direct_MHref_source",
            "route": "forbidden measured GM source",
            "source_path": str(SOURCES["4838_doc"]),
            "equation_ref": "no measured GM absorption",
            "notes": "MEASURED_GM_AS_SOURCE cannot define M_H_ref",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4839_7_forbidden_variation_after_readout",
            "route_type": "source_descent_zero",
            "route": "forbidden variation after readout",
            "source_path": str(SOURCES["hilbert_current"]),
            "equation_ref": "HC3558_0_same_frame_Hilbert_current_definition",
            "notes": "VARIATION_AFTER_READOUT cannot define the Hilbert current",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4839_8_forbidden_density_assertion",
            "route_type": "source_descent_zero",
            "route": "forbidden density qbasic assertion",
            "source_path": str(SOURCES["density_qbasic"]),
            "equation_ref": "HDQ3561_3_source_weight_countermodel",
            "notes": "DENSITY_QBASIC_BY_ASSERTION ignores the source-only weight countermodel",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4839_9_forbidden_nonHilbert_bypass",
            "route_type": "source_descent_bound",
            "route": "forbidden non-Hilbert bypass ignored",
            "source_path": str(SOURCES["parent_source_identity"]),
            "equation_ref": "I499_3_parent_source_identity",
            "notes": "NONHILBERT_BYPASS_IGNORED would erase the extra-current term",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4839_10_forbidden_reference_only_zero",
            "route_type": "direct_MHref_source",
            "route": "forbidden reference-only zero",
            "source_path": str(SOURCES["1017_doc"]),
            "equation_ref": "HPT1017_4_denominator_guard",
            "notes": "REFERENCE_ONLY_ZERO cannot produce a positive source denominator",
            "timestamp_utc": timestamp,
            **base_flags(),
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
            "decision_id": "DEC4839_0_bridge",
            "decision": "Use Hilbert current descent as the source side of the Newton bridge.",
            "effect": "turns M_H_ref into an action/source-current object rather than fitted GM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4839_1_block",
            "decision": "Live source descent and live M_H_ref source row remain blocked.",
            "effect": "no local-GR/Newton claim; finite runner feed is staged",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4839_2_next",
            "decision": NEXT_TARGET,
            "effect": "attack source-action pullback and density q-basicness directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4839_0_definition", "Hilbert current definition exists", "PASS_CONDITIONAL", "definition is precise but owner unsigned"),
        ("CG4839_1_descent_zero", "live source descent zero", "BLOCKED_UNSIGNED", "source-action pullback/density/worldtube/Hamiltonian clauses are not all signed"),
        ("CG4839_2_direct_MHref", "live M_H_ref source row", "BLOCKED_MISSING_VALUES", "H_tau/H_ref/integral rho_H values are not source-backed"),
        ("CG4839_3_descent_bound", "finite source descent residual", "BLOCKED_MISSING_VALUES", "live coefficients are not filled"),
        ("CG4839_4_smoke", "runner arithmetic", "PASS_NONCLAIM", "direct and descent-bound smoke rows compute as expected"),
        ("CG4839_5_local_GR", "local GR/Newton claim", "NOT_ALLOWED", "source current denominator remains unsigned/non-sourced"),
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

    add("VAL4839_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4839_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all source needles found")
    add("VAL4839_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4839_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    input_rows = read_csv(RUNNER_INPUT)
    add("VAL4839_04_output_count", len(outputs) == len(input_rows), f"outputs={len(outputs)} inputs={len(input_rows)}")
    add("VAL4839_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "runner hard-codes nonclaim rows")
    live_zero = row_by_id(outputs, "RUN4839_0_live_descent_zero_missing")
    add("VAL4839_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_HILBERT_SOURCE_DESCENT_ZERO_CLAUSES", live_zero["missing_for_claim"])
    live_direct = row_by_id(outputs, "RUN4839_2_live_MHref_source_missing")
    add("VAL4839_07_live_direct_blocked", live_direct["runner_status"] == "BLOCKED_DIRECT_MHREF_SOURCE_INPUTS", live_direct["missing_for_claim"])
    direct = row_by_id(outputs, "RUN4839_3_direct_MHref_source_smoke_pass")
    add("VAL4839_08_direct_MHref_smoke_values", all([
        close_to(direct["M_H_ref_abs"], 2.0),
        close_to(direct["M_H_ref_calc_abs"], 2.0),
        close_to(direct["M_H_ref_surface_mismatch_abs"], 0.0),
        close_to(direct["M_H_ref_volume_mismatch_abs"], 0.002),
        close_to(direct["delta_MHref_abs"], 0.001),
        close_to(direct["alpha_source_abs"], 0.000022125),
        close_to(direct["BY5_MHref_feed_abs"], 0.002),
    ]), "direct MHref smoke row computes surface/volume mismatch and feed")
    bound = row_by_id(outputs, "RUN4839_5_descent_bound_smoke_pass")
    add("VAL4839_09_descent_bound_smoke_values", all([
        close_to(bound["source_descent_residual_abs"], 0.0086),
        close_to(bound["delta_MHref_abs"], 0.0086),
        close_to(bound["alpha_source_abs"], 0.000190275),
        close_to(bound["BY5_MHref_feed_abs"], 0.0172),
    ]), "descent bound smoke row computes expected residual feed")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4839_6_") or row["row_id"].startswith("RUN4839_7_") or row["row_id"].startswith("RUN4839_8_") or row["row_id"].startswith("RUN4839_9_") or row["row_id"].startswith("RUN4839_10_")]
    add("VAL4839_10_forbidden_routes_fail", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden shortcuts fail")
    add("VAL4839_11_next_target_recorded", NEXT_TARGET in read_text(NEXT_TARGET_CSV) and NEXT_TARGET in read_text(RESUME_PATH), "next target recorded in CSV and resume")
    cleanup_pycache()
    add("VAL4839_12_no_pycache_left", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_next_target(timestamp: str) -> None:
    write_csv(
        NEXT_TARGET_CSV,
        [
            {
                "checkpoint": CHECKPOINT,
                "next_target": NEXT_TARGET,
                "reason": "4839 narrows M_H_ref ownership to source-action pullback and density q-basicness.",
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
Last checkpoint: `4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md`
Marker: `{MARKER}`

## Where we are

4839 attacks the source side of the local GR/Newton bridge:

```text
J_H[tau] = T_H^{{mu nu}}[e_obs] n_mu tau_nu dSigma
rho_H dV_H = n_mu tau_nu T_H^{{mu nu}} dSigma_H
M_H_ref = H_tau[S_outer] - H_ref = integral_W rho_H dV_H
delta_MHref = source_descent_residual or normalized M_H_ref mismatch
```

## Live blockers

- Hilbert current and density are defined conditionally, but the parent source action pullback is not signed.
- A first `M_H_ref` source row still needs real `H_tau`, `H_ref`, and `integral rho_H` values or a theorem-zero.
- Source-only weights, variation after readout, non-Hilbert bypass, EM stress omission, reference-only zero and measured `GM` are forbidden.
- Local GR/Newton remains nonclaim until this source denominator feeds 4838 with live values.

## Next target

`{NEXT_TARGET}`
""",
    )


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4839 Y5 R2FR Hilbert source current descent or first MHref source row

**Status:** 4839 turns `M_H_ref` into the actual source-current object demanded by 4838. The conditional route is clear: define `T_H` by varying the same observed matter+EM action before readout, build `rho_H dV_H`, and require the Hamiltonian surface charge to equal the volume Hilbert source mass. The live branch remains nonclaim because the parent source-action pullback and first source-backed `M_H_ref` values are not yet supplied.

**Decision:** `{DECISION}`.

## Core derivation

```text
T_H^{{mu nu}} = (2/sqrt(-g_obs)) delta S_src[e_obs,A_obs,psi,theta]/delta g_obs_mu_nu
J_H[tau] = T_H^{{mu nu}} n_mu tau_nu dSigma
rho_H dV_H = n_mu tau_nu T_H^{{mu nu}} dSigma_H
M_H_ref = H_tau[S_outer] - H_ref = integral_W rho_H dV_H
```

If `S_src=q^*Sbar_src` and the measure/coframe/time/EM source data are q-owned before readout, then `rho_H dV_H` is q-basic. If the Hamiltonian surface charge and the Hilbert volume charge match, `M_H_ref` becomes the source denominator needed by 4838. Otherwise the finite branch is:

```text
source_descent_residual =
  E_action_pullback + E_variation_readout + E_measure_qbasic
  + E_tau_frame + E_EM_once + E_theta_constants
  + E_worldtube_boundary + E_nonHilbert_current
  + E_PiM_Htau + E_readout_mask
```

## Source Register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Descent Audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Runner Contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner Output

{md_table(outputs, ["row_id", "runner_status", "source_descent_residual_abs", "M_H_ref_abs", "M_H_ref_surface_mismatch_abs", "M_H_ref_volume_mismatch_abs", "delta_MHref_abs", "alpha_source_abs", "BY5_MHref_feed_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The source denominator is now explicitly `M_H_ref=H_tau-H_ref=integral rho_H dV_H`, not bare mass or orbital `GM`.
- The runner can test a theorem-zero route, a direct first source row, or a finite source-descent residual.
- The live branch remains blocked, but the exact missing object is smaller: source-action pullback plus density q-basicness.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 855 PPC4161 Hilbert source current descent or first MHref source row

Checkpoint: `{DOC_PATH}`

4839 turns the local Newton source denominator into a same-frame Hilbert source-current problem. `J_H`, `rho_H`, and `M_H_ref` are now tied to variation-before-readout and Hamiltonian/volume charge equality; live values remain missing.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "Hilbert_source_current_descent_or_first_MHref_source_row",
        "current_evidence": "4839 converts M_H_ref into a same-frame Hilbert source-current/source-action object and stages zero/direct/bound runner branches; live rows remain blocked.",
        "status": "Hilbert_source_MHref_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent source-action pullback, q-basic density, Hamiltonian surface/volume equality, EM stress inclusion and live H_tau/H_ref/rho_H rows remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live source-current/MHref rows are not source-backed",
        "title": "Hilbert source current descent or first MHref source row",
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
        f"""## PPC4161 4839 Hilbert source current / MHref gate

`{MARKER}`. The source denominator needed by the Newton bridge is now expressed as a same-frame Hilbert source-current object: `M_H_ref=H_tau-H_ref=integral rho_H dV_H`. The live route is still blocked, but the next missing theorem is sharply localized to source-action pullback and density q-basicness. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4839 Hilbert source current descent or first MHref source row

`{PACKET_MARKER}`. `{MARKER}` converts `M_H_ref` from a denominator placeholder into a variation-before-readout Hilbert source object. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    audit = descent_audit(timestamp)
    contract = contract_rows(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DESCENT_AUDIT, audit)
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
        raise SystemExit(f"4839 validation failed: {failed}")
    print(f"4839 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()
