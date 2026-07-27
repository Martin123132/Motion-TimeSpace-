from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2545"
BRANCH_ID = "MTS_R2FR_PARENT_THETA_QTAU_FIXED_REFERENCE_OR_MHREF_FIRST_ROW_2545"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2545-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2545_SOURCE_REGISTER.csv",
    "exact": RESIDUALS / "P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv",
    "recheck": RESIDUALS / "P8_Y5_NO_SHADOW_2545_THETA_QTAU_GATE_RECHECK.csv",
    "reduction": RESIDUALS / "P8_Y5_NO_SHADOW_2545_BZERO_RESIDUAL_REDUCTION.csv",
    "mhref": RESIDUALS / "P8_Y5_NO_SHADOW_2545_MHREF_FIRST_ROW_UPDATE.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2545_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2545_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2545_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2545_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2545_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2545_VALIDATION.csv",
}

BRANCH_COPIES = {
    "exact": POST_ROOT / "source-intake" / "beta-source" / "docs" / "Exact_improvement_cancellation_2545_NONCLAIM.csv",
    "reduction": POST_ROOT / "source-intake" / "local_bounds" / "Bzero_residual_reduction_2545_NONCLAIM.csv",
    "mhref": POST_ROOT / "source-intake" / "local_bounds" / "MHref_first_row_update_2545_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "BOUNDARY_CLASSIFICATION2545_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2545_0_2544_doc", "2544-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md", "NEXT2544_0_selected", "2544 selected parent theta/Qtau/fixed-reference/MHref gate"),
    ("SRC2545_1_2544_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2544_VALIDATION.csv", "VAL2544_OVERALL,PASS", "2544 validation anchor"),
    ("SRC2545_2_2544_theorem", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BZERO_NOFLUX_THEOREM_AUDIT.csv", "BZT2544_6_verdict", "current Bzero theorem obstruction rows"),
    ("SRC2545_3_2544_bound", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BZERO_FIRST_BOUND_ROW.csv", "BZR2544_0_first_row", "current nonclaim Bzero numerator/denominator row"),
    ("SRC2545_4_2544_dependency", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BOUNDARY_DENOMINATOR_DEPENDENCY.csv", "BDD2544_2_MHref", "current denominator dependency rows"),
    ("SRC2545_5_2380_doc", "2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md", "EIC2380_3_k_invariance", "older exact-improvement derivation precedent"),
    ("SRC2545_6_2380_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2380_VALIDATION.csv", "VAL2380_OVERALL", "2380 validation anchor"),
    ("SRC2545_7_2380_exact", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv", "EIC2380_3_k_invariance", "exact-improvement cancellation rows"),
    ("SRC2545_8_2380_recheck", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_THETA_QTAU_GATE_RECHECK.csv", "TQR2380_5_MHref", "theta/Qtau and MHref recheck precedent"),
    ("SRC2545_9_2380_reduction", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv", "BRR2380_5_total", "Bzero residual decomposition precedent"),
    ("SRC2545_10_2380_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_NEXT_TARGET.csv", "NEXT2380_0_selected", "boundary classification next target precedent"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def exact_improvement_derivation_rows() -> list[dict[str, object]]:
    rows = [
        (
            "EIC2545_0_setup",
            "exact boundary improvement setup",
            "Let L_prime = L + d mu for a boundary/improvement (n-1)-form mu.",
            "mu is a genuine exact improvement on the same field bundle and boundary class",
            "only the theta and Q_tau representatives shift; equations of motion are unchanged",
            "non-exact, corner, topological, or readout-dependent pieces are not covered",
        ),
        (
            "EIC2545_1_theta_shift",
            "symplectic potential shift",
            "delta L_prime = E_A delta Phi^A + d(theta + delta mu), so theta_prime = theta + delta mu.",
            "single parent variation exists and delta acts on fields, not on the chosen generator tau",
            "exact improvement contribution to theta is delta mu",
            "parent MTS theta still not globally extracted sector-by-sector",
        ),
        (
            "EIC2545_2_charge_shift",
            "Noether charge representative shift",
            "J_tau_prime = theta_prime(L_tau Phi) - i_tau L_prime = J_tau + d(i_tau mu), hence Q_tau_prime = Q_tau + i_tau mu up to exact/corner terms.",
            "tau is fixed, the Cartan identity is used in the same boundary class, and corner ambiguities are absent or separately retained",
            "exact improvement contribution to Q_tau is i_tau mu",
            "field-dependent tau, corner terms, and global cohomology can create residuals",
        ),
        (
            "EIC2545_3_k_invariance",
            "Hamiltonian surface one-form cancellation",
            "k_tau_prime = delta Q_tau_prime - i_tau theta_prime = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau when [delta,i_tau]=0.",
            "fixed tau, fixed surface embedding, no anomalous corner/codimension-two contribution",
            "exact boundary improvements do not change delta H_tau",
            "if tau or the surface/readout is field-dependent, a commutator residual remains",
        ),
        (
            "EIC2545_4_boundary_component",
            "Bzero exact-improvement component",
            "B_zero_flux_exact := integral_S(delta(i_tau mu)-i_tau(delta mu)) = 0 under the fixed-tau exact-improvement clauses.",
            "every candidate Bzero term is classified as exact mu with no corner/topological/field-dependent remainder",
            "the exact-improvement part of B_zero_flux is conditionally zero",
            "classification of actual MTS boundary/reference terms is still missing",
        ),
        (
            "EIC2545_5_not_MHref",
            "denominator caveat",
            "The cancellation law reduces a numerator channel only; it does not create H_tau, H_ref, M_H_ref, or the source-measure bridge.",
            "none",
            "local GR/Newton remains blocked until M_H_ref and source equality are derived or bounded",
            "positive same-frame M_H_ref and Pi_M J_H = J_M_top + dB_zero",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "derivation_step": step,
            "statement": statement,
            "condition": condition,
            "result": result,
            "remaining_obstruction": obstruction,
        }
        for row_id, step, statement, condition, result, obstruction in rows
    ]


def theta_qtau_gate_recheck_rows() -> list[dict[str, object]]:
    rows = [
        ("TQR2545_0_no_circle", "same target already attempted", "2339/2340/2380 staged theta_Qtau_Htau_Href/MHref rows but did not promote", "do not repeat the first-row table; carry forward the exact boundary-improvement cancellation law", "component reduction only, not global closure", "classify actual boundary/reference terms into exact/corner/topological/field-dependent classes"),
        ("TQR2545_1_parent_variation", "single parent current-chain variation", "MISSING_SINGLE_PARENT_VARIATION", "exact-improvement algebra is available once a parent variation and mu term are identified", "not enough to own theta_MTS globally", "sector certificates for EH anchor, matter/source, boundary/reference, extra/projector/glue"),
        ("TQR2545_2_theta_Qtau", "theta_MTS and Q_tau^MTS extraction", "MISSING_PARENT_THETA_QTAU", "boundary exact-improvement shifts are algebraically controlled", "Q_tau total remains unowned outside the exact-improvement component", "write component ledger: Q_EH, Q_matter/source, Q_boundary_exact, Q_corner, Q_extra, Q_projector"),
        ("TQR2545_3_fixed_reference", "fixed H_ref/counterterm before readout", "MISSING_FIXED_REFERENCE_CERTIFICATE", "exact improvements cannot be used as post-hoc cancellation knobs in delta H", "H_ref still must be fixed by a source-independent selector", "derive or bound Delta_ref for unfixed/non-exact reference choices"),
        ("TQR2545_4_integrability", "H_tau integrability", "MISSING_HTAU_INTEGRABILITY", "exact improvement does not spoil delta H_tau when [delta,i_tau]=0", "other nonintegrable sector pieces still block H_tau", "compute residual one-form Delta_H_res over sector matrix"),
        ("TQR2545_5_MHref", "positive same-frame M_H_ref", "MISSING_POSITIVE_MHREF", "unchanged: denominator missing", "Bzero/R_eq/I_commutator/PPN rows remain non-score-ready", "fill H_tau-H_ref from parent charge or keep MHref row nonclaim"),
        ("TQR2545_6_source_measure", "Hamiltonian charge equals measured source normalization", "MISSING_SOURCE_MEASURE_BRIDGE", "unchanged: exact boundary-improvement cancellation is not the Poisson/Gauss bridge", "Newton/GR recovery cannot be claimed from a conserved charge alone", "prove Pi_M J_H = J_M_top + dB_zero or retain R_eq"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "gate": gate,
            "status_before_2545": before,
            "new_2545_result": result,
            "claim_effect": effect,
            "next_action": next_action,
        }
        for row_id, gate, before, result, effect, next_action in rows
    ]


def bzero_residual_reduction_rows() -> list[dict[str, object]]:
    rows = [
        ("BRR2545_0_exact_improvement", "B_exact_improvement", "integral_S(delta(i_tau mu)-i_tau(delta mu))", "CONDITIONAL_ZERO_DERIVED", "mu exact; tau fixed; surface fixed; no corner anomaly; [delta,i_tau]=0", "Delta_exact_commutator"),
        ("BRR2545_1_corner", "B_corner", "corner/codimension-two contribution to Q_tau or theta", "UNCLASSIFIED_RETAINS_BOUND_ROW", "corner term absent or paired by fixed corner convention", "epsilon_corner_abs"),
        ("BRR2545_2_topological", "B_topological_or_nonexact", "closed-but-not-exact or topological boundary representative", "UNCLASSIFIED_RETAINS_BOUND_ROW", "cohomology class fixed and source-independent or projected silent", "epsilon_top_abs"),
        ("BRR2545_3_field_dependent_tau", "B_delta_tau", "delta(i_tau mu)-i_tau(delta mu) when delta tau != 0 or readout surface moves", "UNCLASSIFIED_RETAINS_BOUND_ROW", "tau and S_outer locked before variation", "epsilon_delta_tau_abs"),
        ("BRR2545_4_reference", "B_reference_unfixed", "H_ref shift or post-readout counterterm choice", "MISSING_FIXED_REFERENCE", "H_ref selector fixed before source/readout and independent of fitted residual", "Delta_ref_over_MH"),
        ("BRR2545_5_total", "B_zero_flux_reduced", "B_zero_flux = B_exact_improvement_zero + B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux", "REDUCED_NOT_CLOSED", "all non-exact/corner/tau/reference/flux pieces vanish or are bounded with M_H_ref", "epsilon_Bzero_abs remains non-score-ready"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "component": component,
            "formula": formula,
            "status": status,
            "zero_condition": zero_condition,
            "residual_if_condition_fails": residual,
        }
        for row_id, component, formula, status, zero_condition, residual in rows
    ]


def mhref_update_rows() -> list[dict[str, object]]:
    rows = [
        ("MHR2545_0_denominator", "M_H_ref", "M_H_ref := H_tau[S_outer] - H_ref", "STILL_MISSING_VALUES", "no denominator derived; exact-improvement cancellation only reduces a numerator component", "false"),
        ("MHR2545_1_bzero_reduced_numerator", "B_zero_flux_remainder", "B_rem := B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux", "REMAINDER_VECTOR_DEFINED", "exact-improvement piece removed from the hard numerator if classification succeeds", "false"),
        ("MHR2545_2_claim_switch", "epsilon_Bzero_abs", "abs(B_rem)/M_H_ref", "NON_SCORE_READY", "requires classified B_rem and positive same-frame M_H_ref", "false"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "status": status,
            "update_from_2545": update,
            "score_ready": score_ready,
        }
        for row_id, quantity, formula, status, update, score_ready in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC2545_0_derivation_gain", "keep exact-improvement cancellation law", "it is a real local algebraic result for theta/Q_tau shifts: exact boundary improvements cancel from delta H_tau under fixed tau", "B_zero_flux is reduced to a remainder classification problem, not one undifferentiated mystery term", "COMPONENT_DERIVATION_ACCEPTED_CONDITIONALLY"),
        ("DEC2545_1_no_global_promotion", "do not claim B_zero_flux=0, M_H_ref, local GR or Newton recovery", "actual MTS boundary/reference terms are not yet classified and denominator/source-measure bridge is still missing", "2544 Bzero row remains nonclaim but now has a sharper numerator decomposition", "GLOBAL_CLAIMS_BLOCKED"),
        ("DEC2545_2_no_circling", "do not repeat generic M_H_ref first-row staging as the next step", "older line already staged M_H_ref and parent charge rows; the new work must classify boundary pieces or derive fixed reference", "2546 selected as boundary term classification/fixed-reference selector", "ANTI_CIRCLING_ROUTE_SELECTED"),
        ("DEC2545_3_github_policy", "no GitHub update from 2545", "useful private derivation progress, but still no stable public claim", "continue private goal until a clean derived/conditional/blocked checkpoint exists", "NO_GITHUB"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "decision": decision,
                "reason": reason,
                "consequence": consequence,
                "status": status,
            }
        )
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG2545_0_exact_improvement_component", "exact boundary improvement cancellation derived under fixed-tau assumptions", "PASS_CONDITIONAL_COMPONENT_ONLY", "can remove exact-improvement numerator component only after term classification"),
        ("CG2545_1_boundary_classification", "all actual MTS boundary/reference terms classified as exact or residual", "FAIL_PENDING_CLASSIFICATION", "B_zero_flux global zero not allowed"),
        ("CG2545_2_fixed_reference", "fixed H_ref/counterterm selector before readout", "FAIL", "Delta_ref remains live"),
        ("CG2545_3_MHref", "positive same-frame M_H_ref denominator", "FAIL", "normalized local residuals remain non-score-ready"),
        ("CG2545_4_source_measure", "Hamiltonian charge equals measured source charge", "FAIL", "Newton/GR source normalization bridge remains blocked"),
        ("CG2545_5_local_GR_Newton", "local GR/Newton recovery", "FAIL_NONCLAIM", "private derivation progress only"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("REF2545_0_exact_to_global", "declare B_zero_flux=0 because exact improvements cancel", "false", "the actual MTS boundary/reference stack may include corner, topological, field-dependent tau, unfixed reference, or nonintegrable flux pieces", "BRR2545_1_corner;BRR2545_2_topological;BRR2545_3_field_dependent_tau;BRR2545_4_reference;CG2545_1_boundary_classification"),
        ("REF2545_1_MHref_from_orbit", "fill M_H_ref using observed orbital GM before deriving source-measure bridge", "false", "this would borrow Newton to prove Newton/GR recovery", "TQR2545_5_MHref;TQR2545_6_source_measure;CG2545_4_source_measure"),
        ("REF2545_2_reference_cancellation", "choose H_ref after seeing B_zero_flux to cancel the residual", "false", "fixed reference must be selected before source/readout and cannot be a fitted knob", "TQR2545_3_fixed_reference;CG2545_2_fixed_reference"),
        ("REF2545_3_public_claim", "publish 2545 as local GR/Newton evidence", "false", "component derivation is promising but global denominator and source bridge remain absent", "CG2545_3_MHref;CG2545_4_source_measure;CG2545_5_local_GR_Newton"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason, "blocking_rows": blocking}) for row_id, claim, allowed, reason, blocking in rows]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2545_0_selected",
            "selected",
            "2546-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md",
            "scripts/Y5_R2FR_boundary_term_classification_exact_vs_corner_reference_2546.py",
            "classify every actual MTS boundary/reference/improvement term into exact-mu, corner, topological/non-exact, field-dependent-tau, unfixed-reference, or nonintegrable-flux classes",
            "retain a finite B_rem vector with one row per unclassified/non-exact component and keep epsilon_Bzero_abs nonclaim",
        ),
        (
            "NEXT2545_1_parallel",
            "parallel",
            "2546b-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md",
            "scripts/Y5_R2FR_fixed_reference_selector_or_Delta_ref_row_2546b.py",
            "derive a source-independent H_ref/counterterm selector fixed before readout",
            "stage Delta_ref_over_MH as a nonclaim residual row",
        ),
        (
            "NEXT2545_2_parallel",
            "parallel",
            "2546c-Y5-R2FR-Htau-integrability-one-form-or-DeltaH-row.md",
            "scripts/Y5_R2FR_Htau_integrability_one_form_or_DeltaH_row_2546c.py",
            "prove the reduced k_tau one-form is closed on the private branch after exact improvements cancel",
            "stage Delta_H_res/M_H_ref nonclaim component",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "priority": priority,
                "next_file": next_file,
                "next_script": next_script,
                "success_condition": success,
                "fallback_condition": fallback,
            }
        )
        for row_id, priority, next_file, next_script, success, fallback in rows
    ]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for copy_id, destination in BRANCH_COPIES.items():
        source = OUTPUTS[copy_id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return True, "git modified-file count for formalization-workbench is 0"
        return False, f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or row.get("copy_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2545_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2545_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2545_02_outputs_exist", all(path.exists() for path in generated), "all 2545 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2545_03_csv_parse", parse_ok, parse_detail)

    exact = read_csv(outputs["exact"])
    reduction = read_csv(outputs["reduction"])
    mhref = read_csv(outputs["mhref"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2545_04_exact_improvement_law_present",
        any(row["row_id"] == "EIC2545_3_k_invariance" for row in exact)
        and any(row["row_id"] == "EIC2545_4_boundary_component" for row in exact),
        "exact-improvement k_tau cancellation and boundary component rows present",
    )
    add(
        "VAL2545_05_remainder_classes_present",
        {"B_corner", "B_topological_or_nonexact", "B_delta_tau", "B_reference_unfixed"}.issubset({row["component"] for row in reduction}),
        "corner/topological/tau/reference remainders retained",
    )
    add(
        "VAL2545_06_MHref_not_promoted",
        all(row["score_ready"] == "false" for row in mhref),
        "M_H_ref rows remain non-score-ready",
    )
    add(
        "VAL2545_07_global_gates_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2545_0_exact_improvement_component"),
        "global Bzero/MHref/source/local-GR gates remain blocked",
    )
    add(
        "VAL2545_08_next_selected",
        any(row["row_id"] == "NEXT2545_0_selected" for row in next_rows),
        "boundary term classification selected next",
    )
    add(
        "VAL2545_09_github_blocked",
        any(row["row_id"] == "REF2545_3_public_claim" and row["allowed"] == "false" for row in read_csv(outputs["refusal"])),
        "public claim/GitHub framing blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2545_10_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2545_11_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2545_12_formalization_untouched", formal_ok, formal_detail)
    add("VAL2545_13_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2545_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2545 derives the exact-improvement cancellation component, keeps global/local claims blocked, and selects boundary classification/fixed-reference next" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    source = read_csv(outputs["source"])
    exact = read_csv(outputs["exact"])
    recheck = read_csv(outputs["recheck"])
    reduction = read_csv(outputs["reduction"])
    mhref = read_csv(outputs["mhref"])
    decision = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    refusals = read_csv(outputs["refusal"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2545 - parent theta/Qtau fixed-reference or M_H_ref first row

## Result

2545 is not another table-circle. It reopens the 2544 parent theta/Qtau/fixed-reference/MHref target, checks the older 2380 attempt, and extracts one real algebraic gain:

`L' = L + d mu`, `theta' = theta + delta mu`, `Q'_tau = Q_tau + i_tau mu`, so

`k'_tau = delta Q'_tau - i_tau theta' = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau`

whenever `tau` and the integration surface are fixed and there are no corner/topological/anomalous pieces. In plain terms: exact boundary improvements do not change the Hamiltonian surface one-form. That gives a conditional zero for the exact-improvement part of `B_zero_flux`.

This does **not** derive `M_H_ref`, `H_ref`, full `theta_MTS`, full `Q_tau^MTS`, the source-measure bridge, or local GR/Newton recovery. The gain is narrower but real: `B_zero_flux` is now split into an exact piece that can cancel algebraically and a remainder vector that must be classified or bounded.

## Source Register

{table(["source_id", "source_path", "path_exists", "needle_found", "role"], source)}

## Exact Improvement Cancellation Derivation

{table(["row_id", "derivation_step", "statement", "condition", "result", "remaining_obstruction"], exact)}

## Theta/Qtau Gate Recheck

{table(["row_id", "gate", "status_before_2545", "new_2545_result", "claim_effect", "next_action"], recheck)}

## Bzero Residual Reduction

{table(["row_id", "component", "formula", "status", "zero_condition", "residual_if_condition_fails"], reduction)}

## M_H_ref First Row Update

{table(["row_id", "quantity", "formula", "status", "update_from_2545", "score_ready"], mhref)}

## Decision Ledger

{table(["row_id", "decision", "reason", "consequence", "status"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Refusal Runner

{table(["row_id", "claim", "allowed", "reason", "blocking_rows"], refusals)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["exact"])}`
- `{rel(outputs["recheck"])}`
- `{rel(outputs["reduction"])}`
- `{rel(outputs["mhref"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a genuine small derivation win. We are not smuggling GR in; we used the standard current-chain algebra that any acceptable parent action must satisfy. The exact-improvement part of the boundary problem can disappear by algebra, but only after the actual MTS boundary/reference terms are classified as exact improvements with fixed `tau`. If they are corners, topological terms, field-dependent readout/surface terms, or unfixed references, they stay as residuals.

The project is therefore slightly less grim than 2544: the boundary blocker has structure now. But it is not solved. The next useful shot is to classify the actual boundary/reference terms, not to stage another generic `M_H_ref` row.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["exact"], exact_improvement_derivation_rows())
    write_csv(OUTPUTS["recheck"], theta_qtau_gate_recheck_rows())
    write_csv(OUTPUTS["reduction"], bzero_residual_reduction_rows())
    write_csv(OUTPUTS["mhref"], mhref_update_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
