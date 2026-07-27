from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2661"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md"

CHECKPOINT = "2661"
BRANCH_ID = "Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661"
PARENT_BRANCH = "Y5_R2FR_COUPLING_RESIDUAL_VECTOR_RUNNER_2660"
PREFIX = "P8_Y5_R10_PROJECTION_2661"
RUN_DIR = ROOT / "runs" / "2661-R10-projection-smoke" / "results"

MTS_CANDIDATE_CURVE = RESIDUALS / "R10_alpha_lambda_curve_MTS_2661_PROJECTION_SMOKE_NONCLAIM.csv"
BOUND_CANDIDATE_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_2661_ANCHOR_SMOKE.csv"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "projection_slice": RESIDUALS / f"{PREFIX}_PROJECTION_SLICE.csv",
    "factor_gate": RESIDUALS / f"{PREFIX}_FACTOR_GATE.csv",
    "candidate_mts_curve": MTS_CANDIDATE_CURVE,
    "candidate_bound_curve": BOUND_CANDIDATE_CURVE,
    "runner_summary": RESIDUALS / f"{PREFIX}_RUNNER_SUMMARY.csv",
    "nonclaim_anchor_check": RESIDUALS / f"{PREFIX}_NONCLAIM_ANCHOR_CHECK.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2661_R10_PROJECTION_INPUT_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "R10_projection_2661_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "R10_PROJECTION_2661_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2661_R10_PROJECTION_FACTOR_GATE.csv",
    "quarantine": QUARANTINE / "P8_Y5_2661_R10_RUNNER_SUMMARY.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2660_doc": {
        "path": ROOT / "2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md",
        "needles": ["APM2660_0_R10", "NEXT2660_0_selected", "VAL2660_OVERALL"],
        "role": "immediate handoff selecting R10 projection first-fill",
    },
    "563_doc": {
        "path": ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "needles": ["R10_RUNNER_563_ANCHOR_SMOKE_RECHECK", "B563_1_no_numeric_MTS_alpha", "V563_10_no_overclaim"],
        "role": "source-backed anchor-only R10 bound smoke and nonclaim runner precedent",
    },
    "437_doc": {
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needles": ["R10_alpha_lambda_executable_curve_contract_written", "C10_2_bound_match", "claim_ceiling_enforced"],
        "role": "R10 alpha(lambda) executable curve contract",
    },
    "947_doc": {
        "path": ROOT / "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
        "needles": ["PFA947_0_R10_projection", "BI947_0_cg_R10", "V947_4_R10_projection_blocked"],
        "role": "prior R10 projection fill attempt and bound interface",
    },
    "1029_doc": {
        "path": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
        "needles": ["TAU1029_0_R10", "CGI1029_1_finite_cg_R10", "V1029_13_no_overclaim"],
        "role": "finite c_g and tau_R10 source requirements",
    },
    "2659_doc": {
        "path": ROOT / "2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md",
        "needles": ["ODT2659_6_verdict", "FRV2659_0_c_g_common_frame", "VAL2659_OVERALL"],
        "role": "visible-domain theorem remains unsigned, so c_g remains finite/residual",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH, RUN_DIR]:
        path.parent.mkdir(parents=True, exist_ok=True)
    RUN_DIR.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2661_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def projection_slice_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "slice_id": "R10P2661_0_formula",
            "quantity": "alpha_R10(lambda)",
            "required_formula": "alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g + alpha_tail_abs(lambda)",
            "current_fill": "symbolic_only",
            "missing_input": "K_X(lambda);Qbar_XH;tau_R10;c_g;tail envelope",
            "status": "PROJECTION_FORMULA_READY_NONCLAIM",
            "source_ref": "2660:APM2660_0_R10;947:PFA947_0_R10_projection",
        },
        {
            "slice_id": "R10P2661_1_tau_R10",
            "quantity": "tau_R10",
            "required_formula": "dimensionless map from parent coupling normalization to Yukawa alpha(lambda) convention",
            "current_fill": "MISSING_TAU_R10",
            "missing_input": "source/test profile, geometry convention, range profile, same-frame normalization",
            "status": "MISSING_ARENA_PROJECTION",
            "source_ref": "1029:TAU1029_0_R10",
        },
        {
            "slice_id": "R10P2661_2_KX",
            "quantity": "K_X(lambda)",
            "required_formula": "finite-range kernel/shape factor for the X channel in the R10 source-test geometry",
            "current_fill": "MISSING_K_X_LAMBDA",
            "missing_input": "kernel theorem or sourced profile convention",
            "status": "MISSING_PROFILE_KERNEL",
            "source_ref": "563:B563_1_no_numeric_MTS_alpha",
        },
        {
            "slice_id": "R10P2661_3_Qbar_XH",
            "quantity": "Qbar_XH",
            "required_formula": "source/Hamiltonian charge projection for the X channel",
            "current_fill": "MISSING_QBAR_XH",
            "missing_input": "source-current owner, Hilbert/source normalization, no-hidden-tail theorem or numeric row",
            "status": "MISSING_SOURCE_CHARGE_PROJECTION",
            "source_ref": "563:B563_1_no_numeric_MTS_alpha",
        },
        {
            "slice_id": "R10P2661_4_cg",
            "quantity": "c_g",
            "required_formula": "parent common-frame coefficient or theorem-zero from visible-domain signature",
            "current_fill": "MISSING_C_G",
            "missing_input": "visible-domain theorem or finite c_g source",
            "status": "MISSING_PARENT_COEFFICIENT",
            "source_ref": "2659:FRV2659_0_c_g_common_frame",
        },
        {
            "slice_id": "R10P2661_5_bound_curve",
            "quantity": "alpha_bound(lambda)",
            "required_formula": "full external alpha(lambda) bound curve or explicitly labelled anchor-only smoke rows",
            "current_fill": "anchor_only_rows_available_nonclaim",
            "missing_input": "digitized/full machine-readable curve for claim use",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "source_ref": "563:R10_ANCHOR rows;437:C10_2_bound_match",
        },
        {
            "slice_id": "R10P2661_6_no_cancellation",
            "quantity": "alpha_tail_abs(lambda)",
            "required_formula": "absolute envelope for marker/source/non-Hilbert tails",
            "current_fill": "MISSING_TAIL_ENVELOPE",
            "missing_input": "b_alpha, b_mass, q_nonH/domain tails and projections",
            "status": "MISSING_TAIL_BOUND",
            "source_ref": "2660:ENV2660_0_R10",
        },
        {
            "slice_id": "R10P2661_7_verdict",
            "quantity": "R10 projection slice",
            "required_formula": "all factors numeric/source-backed or theorem-zero, with full bound curve for claims",
            "current_fill": "symbolic_anchor_smoke_only",
            "missing_input": "tau_R10, K_X(lambda), Qbar_XH, c_g, tail envelope, claim-valid bound curve",
            "status": "R10_PROJECTION_NOT_SCORE_READY",
            "source_ref": "this checkpoint",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def factor_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("FAC2661_0_tau_R10", "tau_R10", "MISSING_ARENA_PROJECTION", "derive/source R10 source-test transfer factor"),
        ("FAC2661_1_KX", "K_X(lambda)", "MISSING_PROFILE_KERNEL", "derive/source finite-range kernel over lambda"),
        ("FAC2661_2_Qbar_XH", "Qbar_XH", "MISSING_SOURCE_CHARGE_PROJECTION", "derive/source Hilbert/source charge projection"),
        ("FAC2661_3_cg", "c_g", "MISSING_PARENT_COEFFICIENT", "derive visible-domain zero or source finite c_g"),
        ("FAC2661_4_tail", "alpha_tail_abs(lambda)", "MISSING_TAIL_ENVELOPE", "source/derive marker and non-Hilbert tails"),
        ("FAC2661_5_bound", "alpha_bound(lambda)", "ANCHOR_ONLY_FULL_CURVE_MISSING", "digitize/import full claim-valid bound curve"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "factor_id": factor_id,
            "factor": factor,
            "status": status,
            "next_action": next_action,
            "blocks_score": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for factor_id, factor, status, next_action in rows
    ]


def candidate_bound_rows() -> list[dict[str, Any]]:
    rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv")
    out: list[dict[str, Any]] = []
    for row in rows:
        copied = dict(row)
        copied["valid_for_claim"] = "false"
        copied["notes"] = f"2661 reused anchor-only noncurve smoke row; {copied.get('notes', '')}"
        out.append(copied)
    if not out:
        out.append(
            {
                "bound_id": "R10_ANCHOR_2661_MISSING",
                "dataset_id": "MISSING_BOUND_ANCHOR_SOURCE",
                "lambda_value": "MISSING_LAMBDA",
                "lambda_units": "m",
                "alpha_bound": "MISSING_ALPHA_BOUND",
                "alpha_bound_source": "MISSING_SOURCE",
                "digitization_method": "MISSING",
                "source_file": "MISSING_SOURCE_FILE",
                "valid_for_claim": "false",
                "notes": "anchor source file missing; nonclaim blocker",
            }
        )
    return out


def candidate_mts_curve_rows(bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bound in bound_rows:
        rows.append(
            {
                "model_id": "MTS_coupling_vector_R10_projection_2661",
                "branch_id": "R10_projection_symbolic_smoke_nonclaim",
                "curve_id": "R10_alpha_lambda_curve_MTS_2661_PROJECTION_SMOKE_NONCLAIM",
                "lambda_value": bound.get("lambda_value", "MISSING_LAMBDA"),
                "lambda_units": bound.get("lambda_units", "m"),
                "alpha_predicted": "K_X(lambda)*Qbar_XH*tau_R10*c_g + alpha_tail_abs(lambda)",
                "alpha_bound": bound.get("alpha_bound", "MISSING_ALPHA_BOUND"),
                "alpha_bound_source": f"source-intake/local_bounds/{BOUND_CANDIDATE_CURVE.name}::{bound.get('bound_id', 'MISSING_BOUND_ID')}",
                "force_law_form": "Yukawa_potential_alpha_projection_symbolic",
                "derivation_status": "symbolic_R10_projection_nonclaim_missing_tau_K_Qbar_cg_tail",
                "formula_reference": f"{DOC_PATH.name}::R10P2661_0_formula",
                "source_file": DOC_PATH.name,
                "assumptions": "anchor_only_bound_rows;missing_projection_factors;no_tau_one;no_cancellation",
                "valid_for_claim": "false",
                "notes": "2661 candidate row intentionally symbolic; comparator must reject it for claim scoring.",
            }
        )
    return rows


def runner_summary_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    status = result["status"]
    return [
        {
            "summary_id": "RUNSUM2661_0_projection_smoke",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "output_dir": status["output_dir"],
            "mts_rows": status["mts_rows"],
            "valid_mts_rows": status["valid_mts_rows"],
            "bound_rows": status["bound_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "passed_rows": status["passed_rows"],
            "blocked_or_failed_rows": status["blocked_or_failed_rows"],
            "R10_pass_for_claim": status["R10_pass_for_claim"],
            "claim_allowed": status["claim_allowed"],
            "valid_for_claim": False,
            "timestamp_utc": stamp(),
        }
    ]


def nonclaim_anchor_check_rows(bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_positive = True
    anchor_only = True
    issues: list[str] = []
    for row in bound_rows:
        try:
            lambda_value = float(str(row.get("lambda_value", "")))
            alpha_bound = float(str(row.get("alpha_bound", "")))
        except ValueError:
            numeric_positive = False
            issues.append(f"{row.get('bound_id', 'unknown')}:non_numeric")
            continue
        if lambda_value <= 0 or alpha_bound <= 0:
            numeric_positive = False
            issues.append(f"{row.get('bound_id', 'unknown')}:non_positive")
        method = str(row.get("digitization_method", ""))
        if "anchor_only" not in method:
            anchor_only = False
            issues.append(f"{row.get('bound_id', 'unknown')}:not_anchor_only")
    return [
        {
            "check_id": "ANCH2661_0_anchor_rows",
            "rows": len(bound_rows),
            "numeric_positive": numeric_positive,
            "anchor_only": anchor_only,
            "full_curve_available": False,
            "valid_for_claim": False,
            "status": "PASS_NONCLAIM_ANCHOR_SMOKE" if numeric_positive and anchor_only else "FAIL_ANCHOR_AUDIT",
            "issues": ";".join(issues),
            "timestamp_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2661_0_projection_factors", "tau_R10, K_X, Qbar_XH, c_g and tail envelope are numeric/source-backed or theorem-zero", "FAIL_FACTORS_MISSING", "FAC2661 rows"),
        ("CG2661_1_bound_curve", "full claim-valid alpha(lambda) bound curve is available", "FAIL_ANCHOR_ONLY_NONCLAIM", "ANCH2661_0_anchor_rows"),
        ("CG2661_2_runner", "R10 comparator passes with valid MTS and bound rows", "FAIL_RUNNER_BLOCKED", "RUNSUM2661_0_projection_smoke"),
        ("CG2661_3_visible_domain", "visible-domain zero switch is parent-signed", "FAIL_VISIBLE_DOMAIN_UNSIGNED", "2660:VDP2660_5_verdict"),
        ("CG2661_4_verdict", "R10 projection can support a claim", "CLAIM_BLOCKED", "factors missing; anchor only; runner false"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2661_0_projection_status",
            "decision": "R10 projection formula is wired but not score-ready",
            "reason": "the current row is symbolic and the external bound rows are anchor-only noncurve smoke rows",
            "next_action": "do not claim R10; fill tau_R10/profile convention or acquire a full curve first",
        },
        {
            "decision_id": "DEC2661_1_best_next",
            "decision": "try the profile/projection derivation before external curve digitization",
            "reason": "a full bound curve still cannot score without K_X, Qbar_XH, tau_R10 and c_g/tail values",
            "next_action": "derive/source R10 source-test profile normalization and tau_R10 map",
        },
        {
            "decision_id": "DEC2661_2_data_policy",
            "decision": "anchor rows remain useful only for smoke tests",
            "reason": "they validate units/schema and threshold bookkeeping but cannot replace a full alpha(lambda) curve",
            "next_action": "keep anchor rows nonclaim and preserve comparator refusal",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2661_0_selected",
            "status": "selected",
            "next_doc": "2662-Y5-R2FR-R10-profile-normalization-and-tau-map-or-bound-curve-digitizer.md",
            "next_script": "scripts/Y5_R2FR_R10_profile_normalization_and_tau_map_or_bound_curve_digitizer_2662.py",
            "task": "derive/source the R10 source-test profile normalization and tau_R10 map first; only then digitize/import a full alpha(lambda) bound curve if useful",
            "must_include": "Yukawa convention, source/test geometry profile, K_X(lambda), Qbar_XH normalization, tau_R10 units, no tau=1 shortcut, no-cancellation tail policy",
            "must_exclude": "R10 pass claim, alpha=1 anchor as full curve, invented finite c_g, closure-only zero as derived theorem, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2661_0_progress", "R10 projection", "WIRED_AND_MACHINE_REFUSED", "projection formula and candidate rows now run through the existing comparator and fail safely"),
        ("STAT2661_1_data", "external R10 bound", "ANCHOR_ONLY_NONCLAIM", "2020/2007 anchors are source-backed threshold smoke rows, not a full curve"),
        ("STAT2661_2_theory", "MTS-side factors", "MISSING_PROJECTION_AND_COEFFICIENTS", "tau_R10, K_X, Qbar_XH, c_g and tails remain the live blockers"),
        ("STAT2661_3_next", "best route", "PROFILE_NORMALIZATION_FIRST", "derive/source the R10 projection map before spending effort on full bound digitization"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["factor_gate"], BRANCH_COPIES["queue"], "R10 projection factor queue"),
        "local_bounds": (OUTPUTS["candidate_bound_curve"], BRANCH_COPIES["local_bounds"], "R10 anchor-bound smoke copy"),
        "source_weight": (OUTPUTS["projection_slice"], BRANCH_COPIES["source_weight"], "R10 projection slice"),
        "microscope": (OUTPUTS["factor_gate"], BRANCH_COPIES["microscope"], "R10 factor gate local residual copy"),
        "quarantine": (OUTPUTS["runner_summary"], BRANCH_COPIES["quarantine"], "R10 runner refusal summary"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2661_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2661-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2661*",
        "*Y5_R2FR_R10_projection_first_fill_or_visible_domain_source_signature_2661*",
        "*JR2661*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    projection_ok = any(row["slice_id"] == "R10P2661_7_verdict" and row["status"] == "R10_PROJECTION_NOT_SCORE_READY" for row in rows["projection_slice"])
    factors_ok = len(rows["factor_gate"]) == 6 and all(row["blocks_score"] for row in rows["factor_gate"])
    candidate_ok = len(read_csv(MTS_CANDIDATE_CURVE)) >= 1 and len(read_csv(BOUND_CANDIDATE_CURVE)) >= 1 and all(str(row.get("valid_for_claim", "")).lower() == "false" for row in read_csv(MTS_CANDIDATE_CURVE) + read_csv(BOUND_CANDIDATE_CURVE))
    runner_ok = any(row["R10_pass_for_claim"] is False and row["claim_allowed"] is False and int(row["valid_mts_rows"]) == 0 for row in rows["runner_summary"])
    anchor_ok = any(row["status"] == "PASS_NONCLAIM_ANCHOR_SMOKE" and row["full_curve_available"] is False for row in rows["nonclaim_anchor_check"])
    claim_ok = any(row["gate_id"] == "CG2661_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2662-Y5-R2FR-R10-profile-normalization" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2661_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2661_01_projection", projection_ok, "R10 projection slice is explicit and not score-ready"),
        ("VAL2661_02_factors", factors_ok, "all projection factors block score until sourced"),
        ("VAL2661_03_candidates_nonclaim", candidate_ok, "candidate MTS and bound rows are present and nonclaim"),
        ("VAL2661_04_runner_refuses", runner_ok, "existing comparator refuses symbolic/nonclaim rows"),
        ("VAL2661_05_anchor_smoke", anchor_ok, "anchor rows are numeric-positive but nonclaim/noncurve"),
        ("VAL2661_06_claim_gates_blocked", claim_ok, "claim gates block R10 claim"),
        ("VAL2661_07_next_target", next_ok, "2662 R10 profile/tau map target selected"),
        ("VAL2661_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2661_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2661_10_formalization_untouched", formal_ok, "no 2661 outputs are written under formalization-workbench"),
        ("VAL2661_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2661_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2661 wires the R10 projection slice, runs the existing comparator as a nonclaim smoke, blocks scoring, and selects R10 profile/tau normalization next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2661 - R10 Projection First Fill Or Visible Domain Source Signature

## Purpose

This checkpoint wires the first R10 slice of the coupling residual vector into the existing alpha(lambda) comparator. It deliberately keeps the rows nonclaim until the projection factors and bound curve are real.

## Result

- The R10 projection formula is explicit: `alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g + alpha_tail_abs(lambda)`.
- The current candidate rows are symbolic and use anchor-only bound smoke rows, so the existing comparator correctly refuses claim scoring.
- The useful next target is not a victory lap and not a full data scrape yet: derive/source the R10 profile normalization and `tau_R10` map first.
- No R10, local-GR, PPN, WEP, clock, orbital or Newton claim is allowed.

## Source Register

{markdown_table(rows["source_register"])}

## Projection Slice

{markdown_table(rows["projection_slice"])}

## Factor Gate

{markdown_table(rows["factor_gate"])}

## Candidate MTS Curve

{markdown_table(read_csv(MTS_CANDIDATE_CURVE))}

## Candidate Bound Curve

{markdown_table(read_csv(BOUND_CANDIDATE_CURVE))}

## Runner Summary

{markdown_table(rows["runner_summary"])}

## Nonclaim Anchor Check

{markdown_table(rows["nonclaim_anchor_check"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "projection_slice": projection_slice_rows(),
        "factor_gate": factor_gate_rows(),
    }
    bound_rows = candidate_bound_rows()
    mts_rows = candidate_mts_curve_rows(bound_rows)
    write_csv(BOUND_CANDIDATE_CURVE, bound_rows)
    write_csv(MTS_CANDIDATE_CURVE, mts_rows)
    runner_result = run_runner(MTS_CANDIDATE_CURVE, BOUND_CANDIDATE_CURVE, RUN_DIR)
    rows["runner_summary"] = runner_summary_rows(runner_result)
    rows["nonclaim_anchor_check"] = nonclaim_anchor_check_rows(bound_rows)
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
