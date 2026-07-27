from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2812-Y5-R2FR-Ploc-chainmap-equality-or-Cploc-Ccomm-source-bound-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2812_SOURCE_REGISTER.csv",
    "chainmap": MTS / "P8_Y5_R2FR_2812_PLOC_CHAINMAP_EQUALITY_PROOF_ATTEMPT.csv",
    "orthogonal": MTS / "P8_Y5_R2FR_2812_ORTHOGONAL_PROJECTOR_SIGNATURE_AUDIT.csv",
    "csource": MTS / "P8_Y5_R2FR_2812_CPLOC_CCOMM_SOURCE_READY_BOUND_ROWS.csv",
    "qbound": MTS / "P8_Y5_R2FR_2812_QDELTAK_BOUND_ROLLFORWARD.csv",
    "arena": MTS / "P8_Y5_R2FR_2812_ARENA_PROJECTION_GATE.csv",
    "gates": MTS / "P8_Y5_R2FR_2812_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2812_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2812_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2812_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2812_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "chainmap_queue": RAB_QUEUE / "JR2812_PLOC_CHAINMAP_EQUALITY_PROOF_ATTEMPT_NONCLAIM.csv",
    "orthogonal_queue": RAB_QUEUE / "JR2812_ORTHOGONAL_PROJECTOR_SIGNATURE_AUDIT_NONCLAIM.csv",
    "csource_queue": RAB_QUEUE / "JR2812_CPLOC_CCOMM_SOURCE_READY_BOUND_ROWS_NONCLAIM.csv",
    "qbound_beta_doc": BETA_DOCS / "CPLOC_CCOMM_QDELTAK_BOUND_2812_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Cploc_Ccomm_source_ready_bounds_2812_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Cploc_Ccomm_bound_rows_2812_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2812_FIRST_NUMERIC_OPERATOR_BOUND_OR_KHAT00_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def build_sources() -> list[dict[str, Any]]:
    local_sources = [
        ("2811_next", MTS / "P8_Y5_R2FR_2811_NEXT_TARGET.csv", "authoritative 2812 target"),
        ("2811_chainmap", MTS / "P8_Y5_R2FR_2811_PLOC_COMMUTATOR_THEOREM_ATTEMPT.csv", "conditional chain-map theorem predecessor"),
        ("2811_orthogonal", MTS / "P8_Y5_R2FR_2811_PLOC_ORTHOGONAL_PROJECTOR_THEOREM.csv", "orthogonal projector theorem predecessor"),
        ("2811_qbound", MTS / "P8_Y5_R2FR_2811_QDELTAK_BOUND_INTERFACE.csv", "C_Ploc/C_comm q_DeltaK predecessor"),
        ("2811_counterexample", MTS / "P8_Y5_R2FR_2811_PLOC_NORM_COUNTEREXAMPLE.csv", "idempotent-not-norm-one counterexample"),
        ("2810_unit", MTS / "P8_Y5_R2FR_2810_PLOC_UNIT_CERTIFICATE.csv", "P_loc dimensionless unit certificate predecessor"),
        ("2809_derivative", MTS / "P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv", "DeltaK derivative split predecessor"),
        ("2809_components", MTS / "P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv", "DeltaK component table predecessor"),
        ("2485_field_sort", LOCAL_BOUNDS / "Parent_field_sort_table_2485_NONCLAIM.csv", "P_loc as projector/readout field sort"),
        ("2570_quotient_sort", LOCAL_BOUNDS / "Parent_field_sort_quotient_attempt_2570_NONCLAIM.csv", "P_loc fixed-before-variation obstruction"),
        ("2523_readout_reentry", LOCAL_BOUNDS / "Readout_reentry_audit_2523_NONCLAIM.csv", "fixed projector/readout re-entry audit"),
        ("2603_sigma_delta", LOCAL_BOUNDS / "SigmaX_tail_law_bridge_2603_NONCLAIM.csv", "Delta_K projected-divergence schema"),
        ("2407_commutator_doc", WORK / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md", "conditional fixed chain-map proof and failure clauses"),
        ("1014_commutator_doc", WORK / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md", "commutator theorem/bound guardrail"),
        ("1019_projector_doc", WORK / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md", "projector orthogonality route and source-pack pattern"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role in local_sources:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": sp(path),
                "exists_or_reachable": path.exists(),
                "contains_text": bool(text.strip()) if path.exists() else False,
                "role": role,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_chainmap_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CME2812_0_target",
            "parent orthogonal chain-map target",
            "P_loc is selected before local readout and maps the physical residual/current complex to itself with nabla P_loc = P_loc nabla.",
            "would set C_comm=0 on the physical complex",
            "TARGET_SHARP",
            "not yet signed",
        ),
        (
            "CME2812_1_same_complex",
            "same physical complex",
            "Delta_K residuals, Hilbert/source currents, boundary terms, and projected q_loc live in one parent-defined complex C_phys.",
            "needed so a chain-map theorem applies to the actual object, not a convenient proxy",
            "MISSING_PHYSICAL_COMPLEX_EQUALITY",
            "2407 keeps topological-Hilbert equality unsigned",
        ),
        (
            "CME2812_2_same_differential",
            "same derivative operator",
            "the nabla/d operator in q_DeltaK is the same differential for which P_loc is a chain map.",
            "prevents killing a commutator in one complex while scoring another",
            "MISSING_DIFFERENTIAL_OWNER",
            "connection/domain representation terms remain live",
        ),
        (
            "CME2812_3_parent_selection",
            "pre-readout selection",
            "P_loc is chosen by parent structure before source support, material response, observed coframe, or calibration choices.",
            "prevents projector stress/readout re-entry",
            "MISSING_PARENT_SELECTION_SIGNATURE",
            "2523 and 2570 retain readout/source-worldtube dependence",
        ),
        (
            "CME2812_4_boundary_silence",
            "boundary/domain silence",
            "local collar boundaries and domain motion do not change the projected complex.",
            "needed for [P_loc,nabla]=0 and no hidden surface force",
            "MISSING_BOUNDARY_DOMAIN_LOCK",
            "boundary/reference rows remain unsigned",
        ),
        (
            "CME2812_5_verdict",
            "C_comm zero verdict",
            "[P_loc,nabla]Delta_K=0",
            "the algebraic theorem is clean, but same-complex, same-differential, parent-selection and boundary-domain locks are not signed",
            "FAIL_CURRENT_CLAIM",
            "create source-ready C_comm rows",
        ),
    ]
    return [
        {
            "proof_id": row[0],
            "item": row[1],
            "statement": row[2],
            "why_it_matters": row[3],
            "status": row[4],
            "evidence_note": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_orthogonal_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OPS2812_0_target",
            "orthogonal projector signature",
            "A positive parent inner product <.,.>_phys and P_loc=P_loc^dagger=P_loc^2 on C_phys.",
            "would set C_Ploc=1",
            "TARGET_SHARP",
        ),
        (
            "OPS2812_1_inner_product",
            "inner-product owner",
            "the same parent action owns the residual norm used in q_DeltaK and arena projections",
            "without this, norm-one is only a convention in the wrong space",
            "MISSING_PARENT_INNER_PRODUCT",
        ),
        (
            "OPS2812_2_self_adjoint",
            "self-adjointness",
            "P_loc is orthogonal, not oblique, with respect to <.,.>_phys",
            "2811 counterexample shows idempotence is insufficient",
            "MISSING_SELF_ADJOINT_SIGNATURE",
        ),
        (
            "OPS2812_3_arena_norm_compat",
            "arena norm compatibility",
            "R10/WEP/PPN/clock/orbital norms are induced from or bounded by the same parent norm",
            "prevents claiming C_Ploc=1 in one norm and scoring another",
            "MISSING_ARENA_NORM_MAP",
        ),
        (
            "OPS2812_4_verdict",
            "C_Ploc norm verdict",
            "C_Ploc=1",
            "orthogonal projector theorem is available but the parent signature is not in the current corpus",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "audit_id": row[0],
            "item": row[1],
            "statement": row[2],
            "why_it_matters": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_csource_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CB2812_0_CPloc",
            "C_Ploc",
            "||P_loc||_phys",
            "dimensionless",
            "MISSING_NUMERIC_VALUE_OR_ORTHOGONAL_ZERO_THEOREM",
            "source path proving orthogonal projector, or explicit operator norm in physical residual norm",
            "q_DeltaK;PPN;WEP;clock;orbital",
        ),
        (
            "CB2812_1_Ccomm_parallel",
            "C_comm_parallel",
            "||nabla P_loc|| on fixed local collar",
            "m^-1 or geometric inverse length",
            "MISSING_PARALLEL_PROJECTOR_OR_NUMERIC_BOUND",
            "source path proving nabla P_loc=0, or local collar derivative bound",
            "q_DeltaK;PPN preferred-frame/domain leakage",
        ),
        (
            "CB2812_2_Ccomm_domain",
            "C_comm_domain",
            "domain/support derivative contribution to [P_loc,nabla]",
            "m^-1 or support-gradient unit",
            "MISSING_DOMAIN_LOCK_OR_BOUND",
            "source path for fixed source worldtube/homology class, or finite support-motion bound",
            "source-normalization;orbital;R10",
        ),
        (
            "CB2812_3_Ccomm_boundary",
            "C_comm_boundary",
            "boundary/reference derivative contribution to [P_loc,nabla]",
            "m^-1 or boundary-flux-normalized unit",
            "MISSING_BOUNDARY_LOCK_OR_BOUND",
            "source path for no-flux/reference lock, or finite boundary leakage bound",
            "surface traction;clock;orbital",
        ),
        (
            "CB2812_4_Ccomm_total",
            "C_comm",
            "C_comm_parallel + C_comm_domain + C_comm_boundary",
            "m^-1 or common inverse length convention",
            "SOURCE_READY_NONCLAIM",
            "fill the component rows above before scoring",
            "total q_DeltaK residual",
        ),
        (
            "CB2812_5_DeltaK_norm",
            "||Delta_K||",
            "component norm of K_hat-K_metric in the same physical residual norm",
            "stress",
            "MISSING_DELTAK_COMPONENT_NORM",
            "needs DeltaK00, DeltaK0i, trace, tracefree and boundary component values",
            "all local arenas",
        ),
    ]
    return [
        {
            "bound_row_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "units": row[3],
            "status": row[4],
            "source_needed": row[5],
            "arena_links": row[6],
            "numeric_value": "MISSING",
            "source_path": "MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_qbound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QBR2812_0_operator_zero_branch",
            "if OPS2812 and CME2812 close",
            "C_Ploc=1 and C_comm=0, so ||q_DeltaK|| <= D_Delta",
            "conditional only; premises fail in current corpus",
            "ZERO_BRANCH_NOT_CLAIMED",
        ),
        (
            "QBR2812_1_finite_bound_branch",
            "current honest branch",
            "||q_DeltaK|| <= C_Ploc D_Delta + (C_comm_parallel+C_comm_domain+C_comm_boundary)||Delta_K||",
            "source-ready but nonnumeric",
            "ROLLED_FORWARD_BOUND_INTERFACE",
        ),
        (
            "QBR2812_2_no_cancellation",
            "absolute envelope",
            "no negative/canceling credit between D_Delta and C_comm||Delta_K|| without a parent identity",
            "prevents fitted cancellation or measured-G absorption",
            "NO_CANCELLATION_GUARD",
        ),
        (
            "QBR2812_3_score_gate",
            "arena score gate",
            "requires numeric/source-backed C_Ploc, C_comm pieces, Delta_K component norm, zeta/body measure and arena projection",
            "not ready for PPN/WEP/orbital/clock claims",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "rollforward_id": row[0],
            "branch": row[1],
            "bound": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ARENA2812_0_R10_WEP",
            "R10/WEP",
            "acceleration-like residual after body integration and division by g_n",
            "C_Ploc;C_comm;Delta_K norm;zeta_q/body measure;source frame",
            "BLOCKED",
        ),
        (
            "ARENA2812_1_PPN",
            "PPN",
            "preferred-frame/source-normalization metric coefficients",
            "C_comm_domain;DeltaK0i;DeltaK trace/TF;arena projection kernel",
            "BLOCKED",
        ),
        (
            "ARENA2812_2_orbital",
            "orbital/Newton",
            "radial source hair or GM drift residual",
            "DeltaK00;C_comm_domain;no measured-G absorption;source mass convention",
            "BLOCKED",
        ),
        (
            "ARENA2812_3_clock",
            "clock/local time",
            "q_DeltaK^0 or clock-readout residual",
            "C_comm_boundary;DeltaK00 time derivative;clock readout map",
            "BLOCKED",
        ),
    ]
    return [
        {
            "arena_id": row[0],
            "arena": row[1],
            "observable_form": row[2],
            "missing_inputs": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2812_0_chainmap_attempted", "parent orthogonal chain-map proof attempted", True, "proof clauses are explicit"),
        ("CG2812_1_same_complex", "same physical complex is parent-signed", False, "physical residual/current complex equality is missing"),
        ("CG2812_2_same_differential", "same differential/connection owner is parent-signed", False, "connection/domain representation terms remain live"),
        ("CG2812_3_orthogonal_projector", "C_Ploc=1 is parent-signed", False, "inner product/self-adjoint projector signature is missing"),
        ("CG2812_4_commutator_zero", "C_comm=0 is parent-signed", False, "chain-map/covariantly fixed local collar is missing"),
        ("CG2812_5_source_ready_bounds", "C_Ploc/C_comm source-ready rows exist", True, "finite-bound fallback is now explicit"),
        ("CG2812_6_arena_score", "local arena scores can run", False, "numeric operator constants and Delta_K components missing"),
        ("CG2812_7_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "proof and finite-bound routes remain incomplete"),
        ("CG2812_8_nonclaim_pack", "2812 nonclaim proof/bound pack is ready", True, "next target is first finite operator bound or Khat00 component"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "reason": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2812_0_proof_fails_cleanly",
            "The parent orthogonal chain-map proof does not close yet.",
            "The same physical complex, same differential, parent-selected projector and boundary/domain locks are still unsigned.",
            "do not set C_Ploc=1 or C_comm=0",
        ),
        (
            "DEC2812_1_bound_fallback_created",
            "The obstruction is now a source-ready bound pack.",
            "C_Ploc, C_comm_parallel, C_comm_domain, C_comm_boundary and Delta_K norm are separate rows with units and required sources.",
            "fill one row with a real source or theorem next",
        ),
        (
            "DEC2812_2_best_next",
            "Best next move is first finite operator bound or K_hat^{00} source hunt.",
            "The derivation route is sharp but needs a parent signature; empirical/source-row route can still make the residual testable.",
            "target C_comm_domain/boundary or Khat00",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2812_0_2813",
            "next_target": "2813-Y5-R2FR-first-finite-Ccomm-or-CPloc-source-row-or-Khat00-corpus-hunt-under-AX1090.md",
            "script": "scripts/Y5_R2FR_first_finite_Ccomm_or_CPloc_source_row_or_Khat00_corpus_hunt_under_AX1090_2813.py",
            "objective": "try to fill one real source-backed operator row, preferably C_comm_domain/C_comm_boundary or C_Ploc; if no source exists, perform a targeted K_hat^{00} corpus hunt and retain nonclaim status",
            "include": "source-backed units; local collar/domain/boundary scale; physical residual norm; C_Ploc/C_comm rows; DeltaK00/Khat00 search paths; no measured-G absorption",
            "exclude": "invented numeric bounds; proxy scoring as evidence; setting C_comm=0 without chain-map equality; local-GR/WEP/PPN/orbital claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["chainmap"], BRANCH_OUTPUTS["chainmap_queue"], "chainmap_queue"),
        (OUTPUTS["orthogonal"], BRANCH_OUTPUTS["orthogonal_queue"], "orthogonal_queue"),
        (OUTPUTS["csource"], BRANCH_OUTPUTS["csource_queue"], "csource_queue"),
        (OUTPUTS["qbound"], BRANCH_OUTPUTS["qbound_beta_doc"], "qbound_beta_doc"),
        (OUTPUTS["csource"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2812_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def local_path_tokens(value: Any) -> list[Path]:
    if not value:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        token = token.strip()
        if not token or token == "MISSING" or token.startswith("http"):
            continue
        candidate = Path(token)
        if not candidate.is_absolute():
            candidate = WORK / candidate
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2812_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2812_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2812_2_chainmap_attempt_present", any(row["proof_id"] == "CME2812_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["chainmap"]), "chain-map proof attempt safely fails"),
        ("VAL2812_3_orthogonal_attempt_present", any(row["audit_id"] == "OPS2812_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["orthogonal"]), "orthogonal projector signature audit safely fails"),
        ("VAL2812_4_csource_rows_present", len(sections["csource"]) >= 6 and all(row["valid_for_claim"] is False for row in sections["csource"]), "C_Ploc/C_comm source-ready rows are present and nonclaim"),
        ("VAL2812_5_missing_numeric_guard", all(row["numeric_value"] == "MISSING" for row in sections["csource"]), "no numeric operator value is fabricated"),
        ("VAL2812_6_qbound_rollforward_present", any(row["rollforward_id"] == "QBR2812_1_finite_bound_branch" for row in sections["qbound"]), "finite-bound branch is rolled forward"),
        ("VAL2812_7_arena_blocked", all(row["status"] == "BLOCKED" for row in sections["arena"]), "all local arenas remain blocked"),
        ("VAL2812_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2812_9_next_target_2813", any(row["next_id"] == "NEXT2812_0_2813" for row in sections["next"]), "next target is 2813"),
        ("VAL2812_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2812_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2812_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2812_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2812_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2812_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2812_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2812_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2812_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2812 attempts the parent orthogonal chain-map equality, refuses C_Ploc=1/C_comm=0 promotion, and creates source-ready C_Ploc/C_comm bound rows.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2812 - Y5 R2FR Ploc Chainmap Equality Or Cploc Ccomm Source Bound Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2812 tries the real proof: make `P_loc` a parent-selected orthogonal chain map on the same physical residual/current complex used by `q_DeltaK`. That is the route that would justify `C_Ploc=1` and `C_comm=0` without handwaving.",
        "",
        "It still does not close. The algebraic theorem is clean, but the current corpus does not sign the same physical complex, same differential/connection owner, pre-readout projector selection, fixed local collar, or arena-compatible parent norm.",
        "",
        "The gain is practical: the local obstruction is now a source-ready bound interface. `C_Ploc`, `C_comm_parallel`, `C_comm_domain`, `C_comm_boundary`, and `||Delta_K||` are separate rows with units, source requirements, and claim flags locked false.",
        "",
        "## Chainmap Equality Proof Attempt",
        markdown_table(sections["chainmap"], ["proof_id", "item", "statement", "status", "evidence_note"]),
        "",
        "## Orthogonal Projector Signature Audit",
        markdown_table(sections["orthogonal"], ["audit_id", "item", "statement", "status"]),
        "",
        "## C_Ploc / C_comm Source-Ready Bound Rows",
        markdown_table(sections["csource"], ["bound_row_id", "quantity", "definition", "units", "status", "source_needed"]),
        "",
        "## q_DeltaK Bound Rollforward",
        markdown_table(sections["qbound"], ["rollforward_id", "branch", "bound", "status"]),
        "",
        "## Arena Projection Gate",
        markdown_table(sections["arena"], ["arena_id", "arena", "observable_form", "missing_inputs", "status"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "chainmap": build_chainmap_rows(),
        "orthogonal": build_orthogonal_rows(),
        "csource": build_csource_rows(),
        "qbound": build_qbound_rows(),
        "arena": build_arena_rows(),
    }
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
