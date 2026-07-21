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

CHECKPOINT = "4843"
CLAIM_ID = "L-685"
MARKER = "PPC4161_SOURCE_UNIVERSALITY_BRANCH_RECONCILIATION_AND_NEWTON_CHAIN_PROPAGATION_4843"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_UNIVERSALITY_RECONCILIATION_4843"
DECISION = "SOURCE_PREFACTOR_ZERO_RESTORED_ON_LITERAL_CORE_ACTION_AND_PRIVATE_GR_PARITY_BRANCH_STRICT_PRIMITIVE_ORIGIN_OPEN_NEWTON_CHAIN_REBASED_NONCLAIM"
NEXT_TARGET = "4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md"

DOC_PATH = POST / "4843-Y5-R2FR-source-universality-branch-reconciliation-and-Newton-chain-propagation.md"
FORMAL_PATH = FORMAL / "859-PPC4161-source-universality-branch-reconciliation-and-Newton-chain-propagation.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "source_universality_reconciliation_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4843_SOURCE_REGISTER.csv"
THEOREM_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4843_SOURCE_UNIVERSALITY_THEOREM_AUDIT.csv"
PROPAGATION_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4843_NEWTON_CHAIN_PROPAGATION_MATRIX.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4843_RECONCILIATION_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4843_RECONCILIATION_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4843_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4843_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4843_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4843_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4843_VALIDATION.csv"

SOURCES = {
    "core_action": ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
    "fundamental_action": ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
    "visible_import": FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
    "adoption_4446": SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv",
    "rank_4537": SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv",
    "density_4587": POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md",
    "zero_4758": SOURCE_DIR / "P8_Y5_R2FR_4758_PRIVATE_SOURCE_ZERO_PROPAGATION_ROWS.csv",
    "doc_4758": POST / "4758-Y5-R2FR-owner-no-wA-edge-activation-or-epsilonGsrc-projection-inputs.md",
    "newton_4838": SOURCE_DIR / "P8_Y5_R2FR_4838_NEWTON_RUNNER_OUTPUT.csv",
    "doc_4841": POST / "4841-Y5-R2FR-single-action-density-line-no-source-only-weight-theorem-or-first-delta-w-row.md",
    "doc_4842": POST / "4842-Y5-R2FR-parent-matter-category-no-Hom-source-prefactor-proof-or-first-kappaA-hidden-marker-row.md",
    "strict_origin": SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "runner": RUNNER,
    "generator": Path(__file__),
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
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


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
        ("SRC4843_00_core_action", SOURCES["core_action"], "standard matter Lagrangian", "literal MTS full action contains one standard matter term"),
        ("SRC4843_01_fundamental_action", SOURCES["fundamental_action"], "L_matter", "second core action source repeats one matter block and Hilbert variation"),
        ("SRC4843_02_visible_import", SOURCES["visible_import"], "same Hilbert source", "GR-parity visible matter import contract"),
        ("SRC4843_03_adoption_4446", SOURCES["adoption_4446"], "GR_PARITY_SM_IMPORT_PRIVATE_BRANCH_ADOPTED_NONCLAIM", "private no-source-prefactor adoption"),
        ("SRC4843_04_rank_4537", SOURCES["rank_4537"], "RR4537_2_GR_parity_adopted_branch", "component graph rank cross-check"),
        ("SRC4843_05_density_4587", SOURCES["density_4587"], "D_v(rho_H dV_H)=0", "density q-basic theorem and Poynting once-only lock"),
        ("SRC4843_06_zero_4758", SOURCES["zero_4758"], "SZ4758_0_Delta_w_A", "already propagated private source-weight zero"),
        ("SRC4843_07_doc_4758", SOURCES["doc_4758"], "Delta_w_A=0", "explicit branch-state correction and metric-side handoff"),
        ("SRC4843_08_newton_4838", SOURCES["newton_4838"], "RUN4838_0_live_Newton_zero_missing", "current Newton residual runner"),
        ("SRC4843_09_doc_4841", SOURCES["doc_4841"], "delta_w_species", "later off-branch delta-w fallback"),
        ("SRC4843_10_doc_4842", SOURCES["doc_4842"], "kappa_A_source_rel", "later graph/no-Hom fallback"),
        ("SRC4843_11_strict_origin", SOURCES["strict_origin"], "OLT1338_2_MTS_primitive_constructor", "strict primitive-origin control"),
        ("SRC4843_12_runner", SOURCES["runner"], "def evaluate_row", "4843 executable reconciliation runner"),
        ("SRC4843_13_generator", SOURCES["generator"], 'CHECKPOINT = "4843"', "4843 generator and validator"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("SUR4843_0_literal_action", "literal MTS matter syntax", "S_core=int sqrt(-g)[R/(2 kappa)-L_Lambda+L_matter]", "ONE_MATTER_BLOCK_BY_DECLARED_ACTION_SYNTAX", "strict primitive uniqueness remains separate"),
        ("SUR4843_1_Hilbert_variation", "single Hilbert source", "T_H=-2/sqrt(-g) delta S_matter/delta g before readout", "EXACT_ON_LITERAL_AND_IMPORTED_BRANCHES", "non-Hilbert/boundary currents remain separate"),
        ("SUR4843_2_relative_prefactor", "relative source-prefactor zero", "kappa_A=kappa_common*1; P_perp kappa=0", "BRANCH_EXACT_ZERO", "reopens only if an explicit hidden/source/readout prefactor is added"),
        ("SUR4843_3_graph_rank", "component graph rank", "rank(M_graph|P_perp)=n-1; ker on P_perp is zero", "CONSISTENCY_CHECK_NOT_PRIMARY_PREMISE", "current global parent edge ownership remains irrelevant to adopted branch zero"),
        ("SUR4843_4_density_feed", "source-prefactor density feed", "E_source_prefactor=delta_w_species=kappa_A_source_rel=0", "PROPAGATED_ZERO", "other 4587 density components remain"),
        ("SUR4843_5_Newton_feed", "Newton source-prefactor feed", "delta_MHref_prefactor=delta_Newton_source_prefactor=0", "PROPAGATED_ZERO", "E_00, PPN, PiM/Htau, boundary and non-Hilbert pieces remain"),
        ("SUR4843_6_strict_origin", "strict primitive origin", "derive the declared matter/action syntax uniquely from motion-time-space primitives", "OPEN_NOT_REQUIRED_FOR_PRIVATE_CORRESPONDENCE", "required for a global primitive-origin claim"),
        ("SUR4843_7_history_fix", "4841/4842 branch status", "finite delta_w/kappa_A runners apply off branch or after a reactivation guard fails", "REBASED_AS_FALLBACK_NOT_LIVE_PRIVATE_BLOCKER", "do not reopen private w_A without explicit reactivation evidence"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "object": obj,
            "mathematical_form": form,
            "current_result": result,
            "remaining_scope": remaining,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, obj, form, result, remaining in rows
    ]


def propagation_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PROP4843_0_delta_w", "delta_w_species", "0", "4841 source-only weight feed removed on literal/private branch", "off-branch finite runner retained"),
        ("PROP4843_1_kappaA", "kappa_A_source_rel", "0", "4842 relative source-prefactor feed removed on literal/private branch", "hidden/readout reactivation guard retained"),
        ("PROP4843_2_density", "E_source_prefactor", "0", "source-prefactor component removed from 4840 density envelope", "action/constant/lift/Hodge/Poynting/support/readout pieces remain"),
        ("PROP4843_3_MHref", "delta_MHref_prefactor", "0", "source-prefactor component removed from 4839 source descent", "PiM/Htau, boundary, nonHilbert and physical MHref remain"),
        ("PROP4843_4_Newton", "delta_Newton_source_prefactor", "0", "source-prefactor component removed from 4838 Newton envelope", "E00, PPN, boundary, common-G and source profile remain"),
        ("PROP4843_5_PPN", "source-weight PPN subvector", "0", "WEP/gamma/beta/preferred-frame source-weight pieces remain zero from 4758", "non-source PPN vector remains"),
        ("PROP4843_6_next", "primary live derivation", "E_00", "attack metric residual from literal MTS action", NEXT_TARGET),
    ]
    return [
        {
            "propagation_id": propagation_id,
            "quantity": quantity,
            "branch_value": value,
            "effect": effect,
            "survivor_or_guard": survivor,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for propagation_id, quantity, value, effect, survivor in rows
    ]


def base_flags() -> dict[str, str]:
    return {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }


def private_flags() -> dict[str, str]:
    return {
        **base_flags(),
        "declared_full_action_signed": "true",
        "one_matter_action_line_signed": "true",
        "standard_visible_import_signed": "true",
        "hilbert_variation_before_readout_signed": "true",
        "single_public_metric_coframe_signed": "true",
        "common_measure_signed": "true",
        "no_species_source_prefactor_signed": "true",
        "no_material_active_source_reentry_signed": "true",
        "no_hidden_marker_source_signed": "true",
        "no_readout_source_selector_signed": "true",
        "no_second_source_metric_signed": "true",
        "no_post_variation_rescale_signed": "true",
        "common_mode_calibration_only_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    reactivated = private_flags()
    reactivated["no_hidden_marker_source_signed"] = "false"
    return [
        {
            "row_id": "RUN4843_0_literal_core_action_zero_pass",
            "route_type": "private_source_zero",
            "route": "literal declared MTS full action plus standard visible matter branch",
            "branch_scope": "literal_core_action_private_correspondence",
            "source_path": str(SOURCES["core_action"]),
            "equation_ref": "full action; one L_matter; metric variation to T_H",
            "notes": "relative active-source prefactors are absent from the declared action syntax; one common normalization remains calibration",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_1_private_GR_parity_rollforward_pass",
            "route_type": "private_source_zero",
            "route": "4446 plus 4537 plus 4758 private GR-parity rollforward",
            "branch_scope": "PPC4161_private_GR_parity_import",
            "source_path": str(SOURCES["adoption_4446"]),
            "equation_ref": "ADOPT4446_0; RR4537_2; SZ4758_0",
            "notes": "restores the previously adopted private source-universality zero",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_2_public_strict_origin_control_blocked",
            "route_type": "strict_parent_origin",
            "route": "strict global primitive-origin source-universality control",
            "branch_scope": "global_MTS_primitive_origin",
            "source_path": str(SOURCES["strict_origin"]),
            "equation_ref": "OLT1338_2_MTS_primitive_constructor",
            "notes": "private action syntax does not prove unique origin from motion-time-space primitives",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_3_live_remaining_Newton_envelope_missing",
            "route_type": "remaining_newton_envelope",
            "route": "live non-source-prefactor Newton residual envelope",
            "branch_scope": "private_source_zero_remaining_metric_source_tails",
            "source_path": str(SOURCES["newton_4838"]),
            "equation_ref": "RUN4838_2_live_Newton_bound_missing; DRV4587_0..8",
            "notes": "source-prefactor zero is active but remaining physical coefficients are not numeric",
            "timestamp_utc": timestamp,
            "source_prefactor_zero_signed": "true",
            **base_flags(),
        },
        {
            "row_id": "RUN4843_4_remaining_Newton_envelope_smoke_pass",
            "route_type": "remaining_newton_envelope",
            "route": "nonclaim arithmetic smoke after source-prefactor removal",
            "branch_scope": "schema_smoke",
            "source_path": str(SOURCES["newton_4838"]),
            "equation_ref": "4838 Newton envelope rebased after 4758 source zero",
            "notes": "checks that removing source prefactors does not erase E00/PPN/boundary/nonHilbert tails",
            "timestamp_utc": timestamp,
            "source_prefactor_zero_signed": "true",
            "E_action_vertical_abs": "0.0002",
            "E_constant_marker_abs": "0.0003",
            "E_matter_lift_abs": "0.0001",
            "E_Hodge_EM_abs": "0.0002",
            "E_Poynting_boundary_abs": "0.0004",
            "E_nonminimal_EM_abs": "0.0001",
            "E_distributional_shell_abs": "0.0005",
            "E_readout_state_abs": "0.0002",
            "E_nonHilbert_abs": "0.0006",
            "E_PiM_Htau_abs": "0.0004",
            "E_E00_abs": "0.0008",
            "E_PPN_abs": "0.0007",
            "P_Newton_qbar_abs": "0.4",
            "Qbar_source_XH_bound_abs": "0.25",
            "K_source_abs": "0.2",
            "tau_BY5_remaining_abs": "2.0",
            **base_flags(),
        },
        {
            "row_id": "RUN4843_5_hidden_marker_reactivation_control",
            "route_type": "private_source_zero",
            "route": "hidden marker source reactivation control",
            "branch_scope": "reactivated_off_branch",
            "source_path": str(SOURCES["doc_4842"]),
            "equation_ref": "kappa_A_source_rel hidden-marker countermodel",
            "notes": "one failed reactivation guard must reopen the finite 4842 route",
            "timestamp_utc": timestamp,
            **reactivated,
        },
        {
            "row_id": "RUN4843_6_forbidden_reopen_private_wA",
            "route_type": "private_source_zero",
            "route": "forbidden private source-weight reopening",
            "branch_scope": "forbidden",
            "source_path": str(SOURCES["doc_4758"]),
            "equation_ref": "SZ4758_0_Delta_w_A",
            "notes": "REOPEN_PRIVATE_WA_WITHOUT_REACTIVATION is forbidden",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_7_forbidden_full_density_zero",
            "route_type": "private_source_zero",
            "route": "forbidden full density promotion",
            "branch_scope": "forbidden",
            "source_path": str(SOURCES["density_4587"]),
            "equation_ref": "DRV4587_8_total",
            "notes": "SOURCE_PREF_ZERO_EQUALS_FULL_DENSITY_ZERO is forbidden",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_8_forbidden_public_promotion",
            "route_type": "strict_parent_origin",
            "route": "forbidden private-to-public promotion",
            "branch_scope": "forbidden",
            "source_path": str(SOURCES["adoption_4446"]),
            "equation_ref": "ADOPT4446_2_public_claim_control",
            "notes": "PRIVATE_BRANCH_PUBLIC_PROMOTION is forbidden",
            "timestamp_utc": timestamp,
            **private_flags(),
        },
        {
            "row_id": "RUN4843_9_forbidden_G_absorption",
            "route_type": "remaining_newton_envelope",
            "route": "forbidden residual absorption into calibrated G",
            "branch_scope": "forbidden",
            "source_path": str(SOURCES["newton_4838"]),
            "equation_ref": "KGN4838_6_no_GM_launder",
            "notes": "G_ABSORPTION cannot remove non-common residuals",
            "timestamp_utc": timestamp,
            **base_flags(),
        },
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def row_by_id(rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    return next(row for row in rows if row.get("row_id") == row_id)


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


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4843_0_history",
            "decision": "4841/4842 are retained as off-branch/reactivation fallback tools, not private-branch live blockers.",
            "effect": "restores the 4446/4537/4758 branch state and stops source-weight recirculation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4843_1_zero",
            "decision": "The literal core-action and private GR-parity branches have one matter action/Hilbert source line, so relative source prefactors vanish after common-mode calibration.",
            "effect": "propagates zero through delta_w, kappa_A, density-prefactor, MHref-prefactor and Newton-prefactor rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4843_2_next",
            "decision": NEXT_TARGET,
            "effect": "moves to the real metric-side E00 obstruction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4843_0_literal_action", "one literal matter action line", "PASS_BRANCH_EXACT", "core action declares one L_matter and one Hilbert variation"),
        ("CG4843_1_private_adoption", "private GR-parity no-prefactor branch", "PASS_PRIVATE", "4446/4537/4758 adoption remains active"),
        ("CG4843_2_prefactor_propagation", "source-prefactor zero propagation", "PASS_PRIVATE", "zero reaches 4840/4839/4838 source-prefactor components"),
        ("CG4843_3_strict_origin", "global primitive-origin theorem", "BLOCKED", "MTS primitive uniqueness and global interface exhaustion remain unsigned"),
        ("CG4843_4_density", "full density q-basicness", "NOT_IMPLIED", "nonprefactor density/Poynting/support/readout components remain"),
        ("CG4843_5_Newton", "full Newton/local GR", "NOT_ALLOWED", "E00, PPN, MHref/PiM, boundary, nonHilbert and common-G gates remain"),
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


def write_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4843-Y5-R2FR-source-universality-branch-reconciliation-and-Newton-chain-propagation.md`
Marker: `{MARKER}`

## Where we are

4843 corrects a branch-state regression. Checkpoints 4446, 4537 and 4758 had already closed relative ordinary-matter source weights inside the literal/private GR-parity branch:

```text
S_matter appears once on the declared action line
T_H = -2/sqrt(-g) delta S_matter/delta g before readout
no SpeciesLabel/MaterialLabel/HiddenMarker/Readout -> Coeff_active_source map
therefore P_perp kappa_A = delta_w_species = kappa_A_source_rel = 0
```

4841/4842 remain valid off-branch fallback runners. They reactivate only if an explicit source-prefactor, hidden marker, second source metric or readout rescaling is introduced.

## Live blockers

- Source-prefactor contributions to density, `M_H_ref`, Newton and the source-weight PPN subvector are zero on the literal/private branch.
- This does not zero the full density or Newton envelope.
- The live frontier is metric-side: `E_00`, the EH/A_MF parent origin, physical `M_H_ref`/`Pi_M-H_tau`, boundary/non-Hilbert leakage, PPN side channels and common-`G` stationarity.
- Numeric `G_N` remains calibration unless a parent scale law is derived.

## Next target

`{NEXT_TARGET}`
""",
    )


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

    add("VAL4843_00_sources_exist", all(str(row["exists"]) == "True" for row in sources), "all cited source paths exist")
    add("VAL4843_01_needles_found", all(str(row["needle_found"]) == "True" for row in sources), "all cited source needles found")
    add("VAL4843_02_runner_compiles", compile_ok(RUNNER), "runner compiles")
    add("VAL4843_03_generator_compiles", compile_ok(Path(__file__)), "generator compiles")
    inputs = read_csv(RUNNER_INPUT)
    add("VAL4843_04_output_count", len(outputs) == len(inputs), f"outputs={len(outputs)} inputs={len(inputs)}")
    add("VAL4843_05_claims_false", all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in outputs), "all runner rows remain nonclaim")
    literal = row_by_id(outputs, "RUN4843_0_literal_core_action_zero_pass")
    private = row_by_id(outputs, "RUN4843_1_private_GR_parity_rollforward_pass")
    add("VAL4843_06_literal_zero", literal["runner_status"] == "SOURCE_UNIVERSALITY_ZERO_PASS_PRIVATE_NONCLAIM" and close_to(literal["kappaA_source_rel_abs"], 0.0), "literal core action branch source-prefactor zero passes")
    add("VAL4843_07_private_rollforward", private["runner_status"] == "SOURCE_UNIVERSALITY_ZERO_PASS_PRIVATE_NONCLAIM" and close_to(private["delta_Newton_source_prefactor_abs"], 0.0), "4446/4537/4758 private zero propagates through Newton source-prefactor row")
    strict = row_by_id(outputs, "RUN4843_2_public_strict_origin_control_blocked")
    add("VAL4843_08_strict_origin_blocked", strict["runner_status"] == "BLOCKED_STRICT_PRIMITIVE_ORIGIN", strict["missing_for_claim"])
    live = row_by_id(outputs, "RUN4843_3_live_remaining_Newton_envelope_missing")
    add("VAL4843_09_live_envelope_blocked", live["runner_status"] == "BLOCKED_REMAINING_NEWTON_ENVELOPE", live["missing_for_claim"])
    smoke = row_by_id(outputs, "RUN4843_4_remaining_Newton_envelope_smoke_pass")
    add("VAL4843_10_smoke_values", all([
        close_to(smoke["density_nonprefactor_abs"], 0.002),
        close_to(smoke["source_descent_nonprefactor_abs"], 0.003),
        close_to(smoke["Newton_nonprefactor_abs"], 0.0045),
        close_to(smoke["qbar_remaining_abs"], 0.0018),
        close_to(smoke["alpha_remaining_abs"], 0.00009),
        close_to(smoke["BY5_remaining_abs"], 0.0036),
    ]), "remaining nonprefactor envelope arithmetic passes")
    reactivated = row_by_id(outputs, "RUN4843_5_hidden_marker_reactivation_control")
    add("VAL4843_11_reactivation_guard", reactivated["runner_status"] == "BLOCKED_PRIVATE_SOURCE_ZERO_CLAUSES" and "MISSING_no_hidden_marker_source_signed" in reactivated["missing_for_claim"], "hidden marker correctly reopens the finite route")
    forbidden = [row for row in outputs if row["row_id"].startswith("RUN4843_6_") or row["row_id"].startswith("RUN4843_7_") or row["row_id"].startswith("RUN4843_8_") or row["row_id"].startswith("RUN4843_9_")]
    add("VAL4843_12_forbidden_routes", all(row["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row in forbidden), "all forbidden branch promotions and absorptions fail")
    add("VAL4843_13_resume_rebased", "4841/4842 remain valid off-branch fallback runners" in read_text(RESUME_PATH) and NEXT_TARGET in read_text(RESUME_PATH), "resume records corrected branch state and next E00 target")
    cleanup_pycache()
    add("VAL4843_14_no_pycache", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ removed")
    return checks


def write_docs(timestamp: str, sources: list[dict[str, Any]], theorems: list[dict[str, Any]], propagation: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4843 Y5 R2FR source-universality branch reconciliation and Newton-chain propagation

**Status:** 4843 corrects the live branch state. The literal MTS action already contains one standard `L_matter` block and one metric variation, while the private GR-parity branch explicitly adopted one visible matter action with no source/species/material-label map into active-source coefficients. Therefore relative `delta_w_species` and `kappa_A_source_rel` vanish on those branches after the universal common mode is separated. The later 4841/4842 runners remain useful only off branch or after a reactivation guard fails.

**Decision:** `{DECISION}`.

## Core derivation

The declared action syntax is:

```text
S_core = int sqrt(-g) [R/(2 kappa) - L_Lambda + L_matter]
T_H = -2/sqrt(-g) delta S_matter/delta g
```

On the literal/private standard-visible branch, write any putative source coefficient as:

```text
kappa_A = kappa_common 1_A + delta kappa_A
```

The action grammar has one common matter coefficient and no active-source argument built from species, material, hidden or readout labels. Hence:

```text
P_perp delta kappa = 0
delta_w_species = 0
kappa_A_source_rel = 0
E_source_prefactor = 0
delta_MHref_prefactor = 0
delta_Newton_source_prefactor = 0
```

The 4537 connected-graph rank result is a consistency check on the imported component expansion; it is not needed to re-prove a source coefficient absent from the adopted action syntax.

This does **not** imply the full density or Newton residual is zero. The retained nonprefactor envelope is:

```text
E_density_nonpref = E_action_vertical + E_constant_marker + E_matter_lift
                  + E_Hodge_EM + E_Poynting_boundary + E_nonminimal_EM
                  + E_distributional_shell + E_readout_state
E_source_descent_nonpref = E_density_nonpref + E_nonHilbert + E_PiM_Htau
E_Newton_nonpref = E_source_descent_nonpref + E_00 + E_PPN
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Theorem audit

{md_table(theorems, ["theorem_id", "object", "current_result", "remaining_scope"])}

## Newton-chain propagation

{md_table(propagation, ["propagation_id", "quantity", "branch_value", "effect", "survivor_or_guard"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "delta_w_species_abs", "kappaA_source_rel_abs", "delta_Newton_source_prefactor_abs", "density_nonprefactor_abs", "Newton_nonprefactor_abs", "missing_for_claim"])}

## Validation

{md_table(validations, ["check_id", "status", "detail"])}

## What changed

- The source-weight loop is closed again on the literal/private branch; 4841/4842 are off-branch fallback machinery.
- Zero is propagated into the exact source-prefactor pieces of the density, `M_H_ref`, Newton and PPN chains.
- Every non-source residual remains explicit, so this is not a local-GR or Newton claim.
- The next derivation target moves to the metric side: `E_00` from the literal MTS action.

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 859 PPC4161 source-universality branch reconciliation and Newton-chain propagation

Checkpoint: `{DOC_PATH}`

4843 restores the already-adopted literal/private branch result: one standard matter action line, varied once to one Hilbert stress before readout, contains no relative active-source coefficient. Thus `delta_w_species=kappa_A_source_rel=E_source_prefactor=delta_MHref_prefactor=delta_Newton_source_prefactor=0` on that branch. The 4841/4842 finite runners remain reactivation/off-branch tools.

This is not full density, Newton or local-GR closure. The surviving frontier is `E_00`, non-source PPN components, physical `M_H_ref/Pi_M-H_tau`, boundary/non-Hilbert leakage and common-`G` stationarity.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_formal_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "source_universality_branch_reconciliation_and_Newton_chain_propagation",
        "current_evidence": "4843 restores the literal/private branch source-prefactor zero already adopted at 4446/4537/4758 and propagates it into density, MHref, Newton and source-weight PPN components.",
        "status": "source_universality_reconciled_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "strict primitive/global parent origin remains unsigned and non-source E00/PPN/source-current/boundary residuals remain",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "private branch zero must not be promoted to full density/Newton/local-GR or public primitive proof",
        "title": "Source universality branch reconciliation and Newton-chain propagation",
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
        f"""## PPC4161 4843 source-universality branch reconciliation

`{MARKER}` corrects a branch-state regression. The literal core action and adopted private GR-parity branch each contain one matter action/Hilbert source line with no species/material/hidden/readout active-source coefficient. Therefore `delta_w_species=kappa_A_source_rel=E_source_prefactor=delta_MHref_prefactor=delta_Newton_source_prefactor=0` on that branch. Checkpoints 4841/4842 remain off-branch reactivation runners. Full density/Newton/local-GR remains nonclaim because `E_00`, non-source PPN, physical source-current, boundary/non-Hilbert and common-`G` gates survive. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4843 source-universality reconciliation

`{PACKET_MARKER}` restores the 4446/4537/4758 private source-weight zero and propagates it through the 4838-4842 source-prefactor chain. Do not reopen `w_A/kappa_A` inside the literal/private branch unless a hidden/source/readout prefactor reactivation guard actually fails. Next: `{NEXT_TARGET}`.""",
    )


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    theorems = theorem_rows(timestamp)
    propagation = propagation_rows(timestamp)
    inputs = runner_inputs(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_AUDIT, theorems)
    write_csv(PROPAGATION_MATRIX, propagation)
    write_csv(RUNNER_INPUT, inputs)
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(
        STATUS_CSV,
        [{
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "status": "private_branch_reconciled_nonclaim",
            "live_claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }],
    )
    write_csv(
        NEXT_TARGET_CSV,
        [{
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "source-prefactor zero is restored on the literal/private branch; the real remaining root is the metric E00 residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }],
    )
    write_resume(timestamp)
    outputs = run_runner()
    cleanup_pycache()
    validations = validate(timestamp, sources, outputs)
    write_csv(VALIDATION_CSV, validations)
    write_docs(timestamp, sources, theorems, propagation, outputs, validations)
    update_formal_registers(timestamp)
    cleanup_pycache()

    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"4843 validation failed: {failed}")
    print(f"4843 complete: {DOC_PATH}")


if __name__ == "__main__":
    main()
