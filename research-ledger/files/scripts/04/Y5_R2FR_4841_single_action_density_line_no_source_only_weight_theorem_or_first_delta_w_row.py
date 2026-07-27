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

CHECKPOINT = "4841"
CLAIM_ID = "L-683"
MARKER = "PPC4161_SINGLE_ACTION_DENSITY_LINE_NO_SOURCE_ONLY_WEIGHT_THEOREM_OR_FIRST_DELTA_W_ROW_4841"
PACKET_MARKER = "PPC4161_PACKET_SINGLE_ACTION_DENSITY_LINE_NO_SOURCE_ONLY_WEIGHT_THEOREM_OR_FIRST_DELTA_W_ROW_4841"
DECISION = "SINGLE_ACTION_DENSITY_LINE_UNSIGNED_FIRST_DELTA_W_SPECIES_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4842-Y5-R2FR-parent-matter-category-no-Hom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md"

DOC_PATH = POST / "4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md"
FORMAL_PATH = FORMAL / "857-PPC4161-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "single_action_density_delta_w_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4841_SOURCE_REGISTER.csv"
THEOREM_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4841_SINGLE_ACTION_DENSITY_THEOREM_AUDIT.csv"
CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4841_DELTA_W_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4841_DELTA_W_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4841_DELTA_W_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4841_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4841_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4841_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4841_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4841_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4840_doc": POST / "4840-Y5-R2FR-source-action-pullback-signature-or-first-density-qbasic-bound-row.md",
    "4840_output": SOURCE_DIR / "P8_Y5_R2FR_4840_DENSITY_RUNNER_OUTPUT.csv",
    "4840_contract": SOURCE_DIR / "P8_Y5_R2FR_4840_DENSITY_QBASIC_CONTRACT.csv",
    "2646_owner": SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv",
    "2646_delta": SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv",
    "2646_validator": SOURCE_DIR / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_VALIDATOR_RESULTS.csv",
    "2612_nohom": SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
    "2587_contract": SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "no_source_only": SOURCE_DIR / "P8_EM_no_source_only_matter_functor_residual.csv",
    "3561_theorem": SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
    "3293_signature": SOURCE_DIR / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv",
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
        ("SRC4841_00_resume", SOURCES["resume"], "4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md", "4840 selected this delta-w target."),
        ("SRC4841_01_4840_doc", SOURCES["4840_doc"], "DQB4840_4_next", "single action-density handoff."),
        ("SRC4841_02_4840_output", SOURCES["4840_output"], "RUN4840_2_live_density_bound_missing", "live density bound blocked by delta_w."),
        ("SRC4841_03_4840_contract", SOURCES["4840_contract"], "DQB4840_1_bound", "density residual contract includes delta_w."),
        ("SRC4841_04_2646_owner", SOURCES["2646_owner"], "MNO2646_1_conditional_owner_lemma", "conditional owner theorem."),
        ("SRC4841_05_2646_countermodel", SOURCES["2646_owner"], "MNO2646_5_countermodel", "source-only countermodel."),
        ("SRC4841_06_2646_delta", SOURCES["2646_delta"], "DWS2646_0_delta_w_species", "delta_w coefficient row."),
        ("SRC4841_07_2646_injection", SOURCES["2646_delta"], "DWS2646_2_Xi_injection_rule", "JH/DqZ injection rule."),
        ("SRC4841_08_2646_validator", SOURCES["2646_validator"], "CASE2646_6_G_absorption", "anti-G-absorption validator."),
        ("SRC4841_09_2612_nohom", SOURCES["2612_nohom"], "HOM2612_0_target", "no-source-only Hom target."),
        ("SRC4841_10_2612_species", SOURCES["2612_nohom"], "HOM2612_1_species", "species no-Hom clause."),
        ("SRC4841_11_2587_line", SOURCES["2587_contract"], "MCA2587_2_minimal_matter_terms", "minimal matter action line."),
        ("SRC4841_12_2587_no_slot", SOURCES["2587_contract"], "MCA2587_3_no_source_only_slot", "no source-only slot."),
        ("SRC4841_13_no_source_only", SOURCES["no_source_only"], "NSSR3509_0_delta_w_species", "source-only residual definition."),
        ("SRC4841_14_kappa_source", SOURCES["no_source_only"], "NSSR3509_2_kappa_A_source", "active source selector residual."),
        ("SRC4841_15_3561_countermodel", SOURCES["3561_theorem"], "HDQ3561_3_source_weight_countermodel", "density countermodel."),
        ("SRC4841_16_3293_signature", SOURCES["3293_signature"], "HSSIG3293_1_source_only_exclusion", "Hilbert-source exclusion theorem."),
        ("SRC4841_17_source_current", SOURCES["source_current"], "SC1_Hilbert_source_definition", "variation-before-readout current."),
        ("SRC4841_18_runner", SOURCES["runner"], "def evaluate_row", "4841 executable runner."),
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


def theorem_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("SAD4841_0_target", "single action-density line", "all ordinary sectors enter one parent action density with common measure and no relative source-only factor", "CONDITIONAL_THEOREM_SHAPE", "parent matter category/action-line signature"),
        ("SAD4841_1_delta_w", "relative source weight", "w_A=w_common(1+epsilon_A), delta_w=P_perp epsilon", "LIVE_COUNTERMODEL", "epsilon_A theorem-zero or first row"),
        ("SAD4841_2_common_mode", "common mode is not relative source weight", "universal w_common belongs to source/G/action normalization, not WEP composition", "GUARD_ACTIVE", "common-mode projector and G/GM no-laundering"),
        ("SAD4841_3_nohom_species", "species no-Hom", "Hom(SpeciesLabel, ActiveSourceWeight)=common constants only", "NOT_PARENT_SIGNED", "parent object-language proof"),
        ("SAD4841_4_hidden_readout", "hidden/readout no-Hom", "hidden markers and readout/worldtube selectors cannot map to active-source prefactors before variation", "NOT_PARENT_SIGNED", "4842 no-Hom target"),
        ("SAD4841_5_theta", "theta separation", "mass/charge/alpha constants do not license gravitational active-source multipliers", "SEPARATION_CLEAN_NOT_ZERO_PROOF", "constant owner and source owner signed together"),
        ("SAD4841_6_injection", "JH/DqZ injection", "delta_w feeds Hilbert density and q/DqZ source residuals until theorem-zero", "RUNNER_READY", "source-backed epsilon vector and projections"),
        ("SAD4841_7_anti", "anti-circularity", "bounds, G absorption, species fits and cancellation cannot erase delta_w", "GUARD_ACTIVE", "runner forbidden rows"),
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
        ("DWC4841_0_zero", "delta_w_species=0", "single action-density line + connected matter category + no-Hom source-prefactor clauses signed", "conditional_only"),
        ("DWC4841_1_delta_w_row", "delta_w_species_abs", "P_perp_common_mode*||epsilon_A|| + composition uncertainty + common-mode leak", "runner_ready_values_missing"),
        ("DWC4841_2_injection", "JH_DqZ_injection_abs", "(P_source_delta_w+P_DqZ_delta_w)*delta_w_species", "runner_ready_values_missing"),
        ("DWC4841_3_density_feed", "density_qbasic_feed_abs", "P_density_from_delta_w*delta_w + JH_DqZ_injection", "runner_ready_values_missing"),
        ("DWC4841_4_nohom", "no-Hom residual bound", "R_species_hom+R_hidden_hom+R_readout_hom+R_action_line", "runner_ready_values_missing"),
        ("DWC4841_5_next", "parent matter category no-Hom", "prove no source-prefactor morphism or fill kappa_A/hidden-marker row", "next_target"),
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
        "parent_matter_category_signed": "true",
        "single_action_density_line_signed": "true",
        "common_measure_normalization_signed": "true",
        "connected_ordinary_matter_category_signed": "true",
        "species_label_no_source_hom_signed": "true",
        "hidden_marker_no_source_hom_signed": "true",
        "readout_selector_no_source_hom_signed": "true",
        "theta_constants_separated_signed": "true",
        "current_normalization_representation_signed": "true",
        "variation_before_readout_signed": "true",
        "source_functor_total_Hilbert_signed": "true",
        "common_mode_projector_signed": "true",
        "no_species_only_jacobian_signed": "true",
        "no_post_variation_selector_signed": "true",
        "no_bound_as_source_signed": "true",
        "no_G_or_GM_absorption_signed": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4841_0_live_delta_w_zero_missing",
            "route_type": "delta_w_zero",
            "route": "live single action-density no-source-weight zero audit",
            "source_path": str(SOURCES["2646_owner"]),
            "equation_ref": "MNO2646_1_conditional_owner_lemma;MNO2646_6_verdict",
            "notes": "conditional theorem exists but parent matter category/action-line/no-Hom clauses are unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4841_1_conditional_delta_w_zero_pass",
            "route_type": "delta_w_zero",
            "route": "conditional parent-signed single action-density theorem",
            "source_path": str(SOURCES["2646_owner"]),
            "equation_ref": "MNO2646_1_conditional_owner_lemma",
            "notes": "nonclaim theorem-shape smoke row",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4841_2_live_delta_w_bound_missing",
            "route_type": "delta_w_bound",
            "route": "live first delta_w_species row missing",
            "source_path": str(SOURCES["2646_delta"]),
            "equation_ref": "DWS2646_0_delta_w_species;DWS2646_2_Xi_injection_rule",
            "notes": "schema exists but parent epsilon vector, composition basis and projections are missing",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4841_3_delta_w_bound_smoke_pass",
            "route_type": "delta_w_bound",
            "route": "finite delta_w species smoke",
            "source_path": str(SOURCES["2646_delta"]),
            "equation_ref": "DWS2646_0_delta_w_species;DWS2646_2_Xi_injection_rule",
            "notes": "nonclaim arithmetic smoke for relative source weight and density feed",
            "timestamp_utc": timestamp,
            **base_flags(),
            "epsilon_A_vector_norm_abs": "0.003",
            "P_perp_common_mode_abs": "1.0",
            "composition_weight_uncertainty_abs": "0.0002",
            "common_mode_leak_abs": "0.0001",
            "P_source_delta_w_abs": "0.5",
            "P_DqZ_delta_w_abs": "0.25",
            "P_density_from_delta_w_abs": "1.0",
            "P_delta_w_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_delta_w_abs": "2.0",
        },
        {
            "row_id": "RUN4841_4_live_nohom_bound_missing",
            "route_type": "nohom_residual_bound",
            "route": "live no-Hom residual row missing",
            "source_path": str(SOURCES["2612_nohom"]),
            "equation_ref": "HOM2612_0_target;HOM2612_4_verdict",
            "notes": "no-Hom residual schema exists but parent object-language values are missing",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4841_5_nohom_bound_smoke_pass",
            "route_type": "nohom_residual_bound",
            "route": "finite no-Hom residual smoke",
            "source_path": str(SOURCES["2612_nohom"]),
            "equation_ref": "HOM2612_1_species;HOM2612_2_hidden_invariant;HOM2612_3_readout_worldtube",
            "notes": "nonclaim arithmetic smoke for no-Hom residual feed",
            "timestamp_utc": timestamp,
            **base_flags(),
            "R_species_hom_abs": "0.0008",
            "R_hidden_hom_abs": "0.0007",
            "R_readout_hom_abs": "0.0006",
            "R_action_line_abs": "0.0009",
            "P_delta_w_qbar_abs": "1.0",
            "Qbar_source_XH_bound_abs": "0.01475",
            "K_source_abs": "1.5",
            "tau_BY5_delta_w_abs": "2.0",
        },
        {
            "row_id": "RUN4841_6_forbidden_source_weight_asserted_zero",
            "route_type": "delta_w_zero",
            "route": "forbidden source-only weight asserted zero",
            "source_path": str(SOURCES["2646_owner"]),
            "equation_ref": "MNO2646_5_countermodel",
            "notes": "SOURCE_ONLY_WEIGHT_ASSERTED_ZERO ignores the retained countermodel",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4841_7_forbidden_common_mode_hides_relative",
            "route_type": "delta_w_bound",
            "route": "forbidden common-mode hides relative weight",
            "source_path": str(SOURCES["2646_delta"]),
            "equation_ref": "DWS2646_1_common_mode_projector",
            "notes": "COMMON_MODE_HIDES_RELATIVE_WEIGHT is blocked by P_perp",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4841_8_forbidden_G_absorption",
            "route_type": "delta_w_bound",
            "route": "forbidden G absorption",
            "source_path": str(SOURCES["2646_validator"]),
            "equation_ref": "CASE2646_6_G_absorption",
            "notes": "G_ABSORPTION cannot remove relative source weights",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
        {
            "row_id": "RUN4841_9_forbidden_nohom_declaration",
            "route_type": "delta_w_zero",
            "route": "forbidden no-Hom by declaration",
            "source_path": str(SOURCES["2612_nohom"]),
            "equation_ref": "HOM2612_4_verdict",
            "notes": "NOHOM_BY_DECLARATION is not a parent object-language proof",
            "timestamp_utc": timestamp,
            **zero_flags(),
        },
        {
            "row_id": "RUN4841_10_forbidden_bound_as_source",
            "route_type": "delta_w_bound",
            "route": "forbidden bound as source",
            "source_path": str(SOURCES["2646_validator"]),
            "equation_ref": "CASE2646_4_bound_anchor",
            "notes": "BOUND_AS_SOURCE cannot replace a prediction row",
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
            "decision_id": "DEC4841_0_theorem",
            "decision": "delta_w_species is zero only if the parent owns one action-density line and no source-prefactor Hom.",
            "effect": "prevents source weights being erased by calibration or assertion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4841_1_nonclaim",
            "decision": "Live zero and live delta_w rows remain blocked.",
            "effect": "finite delta_w runner feed is staged without local-GR/Newton claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4841_2_next",
            "decision": NEXT_TARGET,
            "effect": "attack parent matter category/no-Hom source-prefactor proof directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4841_0_owner_theorem", "conditional owner theorem exists", "PASS_CONDITIONAL", "2646 theorem is useful but not parent-signed"),
        ("CG4841_1_live_zero", "live delta_w zero", "BLOCKED_UNSIGNED", "matter category/action-line/no-Hom clauses are not signed"),
        ("CG4841_2_live_delta_w", "live first delta_w row", "BLOCKED_MISSING_VALUES", "epsilon vector, composition basis and projections are missing"),
        ("CG4841_3_live_nohom", "live no-Hom residual", "BLOCKED_MISSING_VALUES", "parent object-language residual values are missing"),
        ("CG4841_4_smoke", "runner arithmetic", "PASS_NONCLAIM", "delta_w and no-Hom smoke rows compute"),
        ("CG4841_5_local_GR", "local GR/Newton claim", "NOT_ALLOWED", "source-only weight branch remains unsigned or unbounded"),
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

    add("VAL4841_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4841_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all source needles found")
    add("VAL4841_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4841_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    input_rows = read_csv(RUNNER_INPUT)
    add("VAL4841_04_output_count", len(outputs) == len(input_rows), f"outputs={len(outputs)} inputs={len(input_rows)}")
    add("VAL4841_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "runner hard-codes nonclaim rows")
    live_zero = row_by_id(outputs, "RUN4841_0_live_delta_w_zero_missing")
    add("VAL4841_06_live_zero_blocked", live_zero["runner_status"] == "BLOCKED_DELTA_W_ZERO_CLAUSES", live_zero["missing_for_claim"])
    live_delta = row_by_id(outputs, "RUN4841_2_live_delta_w_bound_missing")
    add("VAL4841_07_live_delta_w_blocked", live_delta["runner_status"] == "BLOCKED_DELTA_W_BOUND_INPUTS", live_delta["missing_for_claim"])
    delta = row_by_id(outputs, "RUN4841_3_delta_w_bound_smoke_pass")
    add("VAL4841_08_delta_w_smoke_values", all([
        close_to(delta["delta_w_species_abs"], 0.0033),
        close_to(delta["JH_DqZ_injection_abs"], 0.002475),
        close_to(delta["density_qbasic_feed_abs"], 0.005775),
        close_to(delta["alpha_source_abs"], 0.000127771875),
        close_to(delta["BY5_delta_w_feed_abs"], 0.01155),
    ]), "delta_w smoke row computes expected relative source-weight feed")
    nohom = row_by_id(outputs, "RUN4841_5_nohom_bound_smoke_pass")
    add("VAL4841_09_nohom_smoke_values", all([
        close_to(nohom["delta_w_species_abs"], 0.003),
        close_to(nohom["alpha_source_abs"], 0.000066375),
        close_to(nohom["BY5_delta_w_feed_abs"], 0.006),
    ]), "no-Hom residual smoke row computes expected feed")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4841_6_") or row["row_id"].startswith("RUN4841_7_") or row["row_id"].startswith("RUN4841_8_") or row["row_id"].startswith("RUN4841_9_") or row["row_id"].startswith("RUN4841_10_")]
    add("VAL4841_10_forbidden_routes_fail", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden shortcuts fail")
    add("VAL4841_11_next_target_recorded", NEXT_TARGET in read_text(NEXT_TARGET_CSV) and NEXT_TARGET in read_text(RESUME_PATH), "next target recorded in CSV and resume")
    cleanup_pycache()
    add("VAL4841_12_no_pycache_left", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_next_target(timestamp: str) -> None:
    write_csv(
        NEXT_TARGET_CSV,
        [
            {
                "checkpoint": CHECKPOINT,
                "next_target": NEXT_TARGET,
                "reason": "4841 leaves the live proof at the parent matter category/no-Hom source-prefactor theorem.",
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
Last checkpoint: `4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md`
Marker: `{MARKER}`

## Where we are

4841 attacks the source-only weight countermodel:

```text
w_A = w_common (1 + epsilon_A)
delta_w_species = P_perp_common_mode epsilon_A
density_qbasic_feed = P_density delta_w_species + JH_DqZ_injection
```

## Live blockers

- The conditional theorem is clear: one parent action-density line plus no source-prefactor Hom kills relative `delta_w_species`.
- The live branch has not signed the parent matter category, connected ordinary-matter action line, or no-Hom species/hidden/readout clauses.
- A first live `delta_w_species` row still needs parent epsilon vector, composition basis, projections and no-G/GM absorption proof.
- Local GR/Newton remains nonclaim until this feeds 4840, 4839 and 4838 with live values or theorem-zero.

## Next target

`{NEXT_TARGET}`
""",
    )


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4841 Y5 R2FR single action-density line no source-only weight theorem or first delta-w row

**Status:** 4841 isolates the source-only-weight countermodel behind the density-qbasic problem. The clean theorem is exact but conditional: if ordinary matter is one connected parent action-density line and species/hidden/readout labels have no morphism to active-source prefactors except the universal common mode, then relative `delta_w_species` vanishes. The live branch is still nonclaim because those parent object-language clauses are not signed.

**Decision:** `{DECISION}`.

## Core derivation

```text
w_A = w_common (1 + epsilon_A)
delta_w_species = P_perp_common_mode epsilon_A
```

The common mode can belong to calibrated action/source normalization, but the relative component cannot be hidden in `G`, `GM`, a bound anchor, or cancellation. If the zero theorem is not signed, the finite feed is:

```text
JH_DqZ_injection = (P_source_delta_w + P_DqZ_delta_w) delta_w_species
density_qbasic_feed = P_density delta_w_species + JH_DqZ_injection
```

## Source Register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Theorem Audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Runner Contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner Output

{md_table(outputs, ["row_id", "runner_status", "delta_w_species_abs", "JH_DqZ_injection_abs", "density_qbasic_feed_abs", "alpha_source_abs", "BY5_delta_w_feed_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- `delta_w_species` is now separated from the universal common mode by an explicit projector.
- The source-only countermodel is no longer vague: it feeds Hilbert density and `DqZ` through a named injection law.
- The next proof target is the parent no-Hom/object-language theorem, not another empirical patch.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 857 PPC4161 single action-density line no source-only weight theorem or first delta-w row

Checkpoint: `{DOC_PATH}`

4841 isolates relative source-only action-density weights. Conditional theorem: one connected action-density line plus no source-prefactor Hom sets `delta_w_species=0`; otherwise the finite `delta_w` row feeds density q-basicness and the local Newton source denominator.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "single_action_density_line_no_source_only_weight_theorem_or_first_delta_w_row",
        "current_evidence": "4841 isolates delta_w_species as the relative source-only action-density countermodel and stages zero/direct/no-Hom residual runner branches.",
        "status": "single_action_density_delta_w_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent matter category, connected action-density line, no-Hom source-prefactor proof and live epsilon/projection rows remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live delta_w/no-Hom rows are not source-backed",
        "title": "Single action-density line no source-only weight theorem or first delta-w row",
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
        f"""## PPC4161 4841 single action-density / delta-w gate

`{MARKER}`. The source-only weight countermodel is now typed as `delta_w_species=P_perp epsilon_A`: a relative active-source/action-density coefficient after the universal common mode is removed. Zero requires a parent action-density/no-Hom theorem; otherwise a finite delta-w row feeds density q-basicness and `M_H_ref`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4841 single action-density line no source-only weight theorem or first delta-w row

`{PACKET_MARKER}`. `{MARKER}` turns the source-only-weight problem into a projector-controlled `delta_w_species` row and selects the parent no-Hom proof next. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    audit = theorem_audit(timestamp)
    contract = contract_rows(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_AUDIT, audit)
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
        raise SystemExit(f"4841 validation failed: {failed}")
    print(f"4841 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()
