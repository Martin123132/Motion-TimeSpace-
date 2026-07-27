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
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2803-Y5-R2FR-q_loc-force-normalization-and-body-moment-zero-theorem-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2803_SOURCE_REGISTER.csv",
    "identity": MTS / "P8_Y5_R2FR_2803_BODY_MOMENT_IDENTITY.csv",
    "zeta": MTS / "P8_Y5_R2FR_2803_ZETA_ZERO_ATTEMPT.csv",
    "zero": MTS / "P8_Y5_R2FR_2803_ZERO_MOMENT_THEOREM_ATTEMPT.csv",
    "force_bound": MTS / "P8_Y5_R2FR_2803_FORCE_BOUND_INTERFACE.csv",
    "unit_contract": MTS / "P8_Y5_R2FR_2803_QLOC_UNIT_CONTRACT.csv",
    "gates": MTS / "P8_Y5_R2FR_2803_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2803_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2803_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2803_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2803_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "identity_queue": RAB_QUEUE / "JR2803_QLOC_BODY_MOMENT_IDENTITY_NONCLAIM.csv",
    "zero_queue": RAB_QUEUE / "JR2803_QLOC_ZERO_MOMENT_THEOREM_ATTEMPT_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2803_QLOC_FORCE_BOUND_INTERFACE_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "QLOC_BODY_MOMENT_IDENTITY_2803_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_qloc_body_moment_2803_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2803_SURFACE_TRACTION_NO_FLUX_OR_FIRST_FORCE_BOUND_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


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


def source_entries() -> list[tuple[str, Path, str]]:
    return [
        ("2802_next", MTS / "P8_Y5_R2FR_2802_NEXT_TARGET.csv", "authoritative 2803 target"),
        ("2802_coefficient", MTS / "P8_Y5_R2FR_2802_FIRST_OBSERVABLE_COEFFICIENT_DERIVATION.csv", "force-kernel predecessor"),
        ("2802_worldtube", MTS / "P8_Y5_R2FR_2802_WORLD_TUBE_FORCE_MAP.csv", "worldtube force-map predecessor"),
        ("2802_gates", MTS / "P8_Y5_R2FR_2802_CLAIM_GATES.csv", "2802 claim gates"),
        ("2799_q_loc", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "q_loc residual definition"),
        ("2799_bound", MTS / "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "rolled q_loc symbolic bound"),
        ("2733_bound", MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "original q_loc symbolic bound"),
        ("2801_no_cancel", MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv", "no measured-G/cancellation policy"),
        ("1012_constant_GM", MTS / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv", "constant GM analogue"),
        ("1012_source_owner", MTS / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", "source owner analogue"),
    ]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": sp(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BMI2803_0_body_moment",
            "Define compact-body q_loc moment",
            "I_A^i := int_{Sigma_A} q_loc^i sqrt(gamma) d^3x",
            "starting object for WEP/orbital force residual",
            "DEFINITION",
        ),
        (
            "BMI2803_1_expand_q_loc",
            "Insert retained q_loc definition",
            "q_loc^i = P_loc(nabla^i Gamma_eff - nabla_mu K_hat^{mu i})",
            "splits moment into Gamma gradient, K_hat divergence, and projector/domain terms",
            "EXACT_FROM_2799",
        ),
        (
            "BMI2803_2_divergence_identity",
            "Convert volume force to surface/time/projector terms",
            "I_A^i = oint_{partial Sigma_A} tau_q^{ji} n_j dS - d/dt int_{Sigma_A} P_loc K_hat^{0i} sqrt(gamma)d^3x + C_P^i + C_conn^i",
            "exact integrated obstruction identity up to declared projector/connection corrections",
            "DERIVED_IDENTITY_NOT_ZERO",
        ),
        (
            "BMI2803_3_surface_traction",
            "Identify q_loc surface traction",
            "tau_q^{ji} := P_loc(Gamma_eff gamma^{ji} - K_hat^{ji}) plus projector-density corrections",
            "local force is a boundary traction if stationary/projector corrections close",
            "DERIVED_TRACTION_FORM",
        ),
        (
            "BMI2803_4_zero_condition",
            "Exact zero-body-moment condition",
            "oint tau_q^{ji}n_j dS = 0; d/dt int P_loc K_hat^{0i}=0; C_P^i=0; C_conn^i=0",
            "this replaces any smuggled plateau axiom",
            "CONDITION_EXACT_NOT_PROVED",
        ),
        (
            "BMI2803_5_verdict",
            "Body-moment identity verdict",
            "I_A^i is reduced to surface traction, time dipole, projector commutator, and connection correction",
            "big reduction, but no zero theorem yet",
            "PARTIAL_DERIVATION_NONCLAIM",
        ),
    ]
    return [
        {
            "identity_id": row[0],
            "step": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_zeta_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZETA2803_0_contract", "zeta_q=0 route", "matter stress is separately covariantly conserved before projection", "requires parent diffeo action, minimal matter coupling, and matter EOM", "NOT_PARENT_SIGNED"),
        ("ZETA2803_1_extra_sector_absorption", "q_loc absorbed by extra sector not matter", "nabla_mu T_extra^{mu nu} = -zeta_q q_loc^nu and nabla_mu T_m^{mu nu}=0", "requires signed split between matter and extra stress", "NOT_PARENT_SIGNED"),
        ("ZETA2803_2_boundary_silence", "boundary term cannot re-enter matter force", "nabla_mu B_q^{mu nu} gives no compact-body force", "surface no-flux theorem missing", "NOT_PROVED"),
        ("ZETA2803_3_verdict", "zeta_q zero proof", "zeta_q=0 only if ZETA2803_0 through ZETA2803_2 close", "current corpus lacks signed parent split", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "zeta_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "missing_input": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZM2803_0_superpotential", "q_loc is pure divergence/superpotential over compact body", "q_loc^i = nabla_j tau_q^{ji} - d_t D_q^i + C_P^i + C_conn^i", "identity derived, not zero", "PARTIAL_SUCCESS"),
        ("ZM2803_1_surface_no_flux", "surface traction vanishes on compact local boundary", "oint_{partial Sigma_A} tau_q^{ji} n_j dS = 0", "requires parent local-vacuum/no-traction theorem", "MISSING_NO_FLUX_PROOF"),
        ("ZM2803_2_stationary_dipole", "time dipole vanishes", "d/dt int_{Sigma_A} P_loc K_hat^{0i} sqrt(gamma)d^3x = 0", "requires stationary local branch or periodic average theorem", "MISSING_STATIONARITY_PROOF"),
        ("ZM2803_3_projector_commutator", "projector/connection corrections vanish or are bounded", "C_P^i=C_conn^i=0 or explicit small bound", "requires P_loc ownership and domain commutator control", "MISSING_PROJECTOR_CONTROL"),
        ("ZM2803_4_universality", "nonzero body moment is universal per unit mass", "I_A^i/M_A = I_B^i/M_B for all test bodies", "requires matter/source universality theorem", "MISSING_UNIVERSALITY_PROOF"),
        ("ZM2803_5_verdict", "zero/universal body-moment theorem", "ZM2803_1 through ZM2803_4 must close", "not proved; exact obstruction terms are now isolated", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "zero_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "current_result": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_force_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FB2803_0_acceleration_bound",
            "single-body force residual",
            "|delta a_A| <= |zeta_q|/M_A ( int_{partial Sigma_A}|tau_q|dS + |dD_A/dt| + |C_P| + |C_conn| )",
            "acceleration",
            "zeta_q, M_A, surface traction norm, time-dipole bound, projector/connection constants",
            "DERIVED_BOUND_INTERFACE_NONNUMERIC",
        ),
        (
            "FB2803_1_WEP_eta_bound",
            "differential WEP residual",
            "eta_AB <= |zeta_q|/g_N |I_A/M_A - I_B/M_B| + boundary_AB/g_N",
            "dimensionless",
            "body moments for both materials and local g_N",
            "DERIVED_BOUND_INTERFACE_NONNUMERIC",
        ),
        (
            "FB2803_2_orbital_bound",
            "source orbital residual",
            "|delta a_orbit| <= |zeta_q| |I_source|/M_source + |Phi_source|/M_source",
            "acceleration",
            "source body moment and no measured-G absorption score",
            "DERIVED_BOUND_INTERFACE_NONNUMERIC",
        ),
        (
            "FB2803_3_units_gate",
            "unit conversion",
            "[zeta_q q_loc]=force density in SI or L^-3 in geometric stress-balance units",
            "unit contract",
            "parent normalization of Gamma_eff and K_hat",
            "MISSING_QLOC_UNITS",
        ),
        (
            "FB2803_4_runner_status",
            "finite force-bound runner",
            "runner cannot score until FB2803_0 through FB2803_3 inputs are numeric/sourced",
            "nonclaim",
            "all rows stay valid_for_claim=false",
            "RUNNER_BLOCKED_CORRECTLY",
        ),
    ]
    return [
        {
            "bound_id": row[0],
            "quantity": row[1],
            "bound_form": row[2],
            "units": row[3],
            "missing_inputs": row[4],
            "status": row[5],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_unit_rows() -> list[dict[str, Any]]:
    rows = [
        ("UNIT2803_0_model_q", "q_loc model units", "from P_loc(nabla Gamma_eff - nabla K_hat)", "not declared by parent action", "MISSING_PARENT_UNIT_CONVENTION"),
        ("UNIT2803_1_force_density", "physical force-density normalization", "f_q^nu = zeta_q q_loc^nu", "requires zeta_q", "MISSING_ZETA_Q"),
        ("UNIT2803_2_body_measure", "compact-body mass measure", "M_A = int rho_parent sqrt(gamma)d^3x", "requires Y5 source owner", "MISSING_SOURCE_OWNER"),
        ("UNIT2803_3_surface_measure", "boundary traction units", "tau_q integrated over dS must match I_A units", "requires Gamma/K_hat normalization", "MISSING_TRACTION_UNITS"),
    ]
    return [
        {
            "unit_id": row[0],
            "unit_object": row[1],
            "required_relation": row[2],
            "current_status": row[3],
            "blocker": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2803_0_body_identity", "q_loc body moment reduced to exact obstruction identity", True, "surface/time/projector/connection obstruction terms isolated"),
        ("CG2803_1_zeta_zero", "zeta_q=0 is proved", False, "parent matter/extra stress split is unsigned"),
        ("CG2803_2_body_moment_zero", "body moment I_A and boundary flux vanish/universalize", False, "surface no-flux, stationarity, projector, and universality clauses remain open"),
        ("CG2803_3_force_bound_numeric", "finite WEP/orbital force bound is score-ready", False, "zeta_q, q_loc units, body moments, and traction norms are missing"),
        ("CG2803_4_local_claim", "local-GR/WEP/orbital claim can be made", False, "zero theorem and numeric bound both fail"),
        ("CG2803_5_nonclaim_pack", "2803 nonclaim theorem/bound interface is ready", True, "next target is now surface traction no-flux or first real force-bound row"),
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
        ("DEC2803_0_progress", "The plateau axiom has been replaced by an exact body-moment obstruction identity.", "q_loc force now lives in surface traction, time dipole, projector commutator, and connection correction.", "attack surface no-flux first"),
        ("DEC2803_1_no_zero_yet", "The zero theorem is not proved.", "surface traction and projector/time terms remain unsigned.", "do not claim local GR/WEP"),
        ("DEC2803_2_bound_path", "A finite bound route exists but is not numeric.", "acceleration and eta bounds are written but need zeta_q and unit/body inputs.", "prepare first force-bound row only after unit contract"),
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
            "next_id": "NEXT2803_0_2804",
            "next_target": "2804-Y5-R2FR-q_loc-surface-traction-no-flux-or-first-real-force-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_q_loc_surface_traction_no_flux_or_first_real_force_bound_under_AX1090_2804.py",
            "objective": "prove the q_loc surface traction no-flux/stationary/projector clauses, or source zeta_q and units for the first real WEP/orbital force-bound row",
            "include": "tau_q surface traction; dD_A/dt; C_P and C_conn; zeta_q; q_loc units; WEP/orbital bound interface; no measured-G absorption",
            "exclude": "plateau axiom; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["identity"], BRANCH_OUTPUTS["identity_queue"], "identity_queue"),
        (OUTPUTS["zero"], BRANCH_OUTPUTS["zero_queue"], "zero_queue"),
        (OUTPUTS["force_bound"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["identity"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2803_{label}",
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


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source", "destination"):
                value = row.get(key)
                if value:
                    paths.append(Path(str(value)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2803_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2803_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2803_2_body_identity_derived", any(row["identity_id"] == "BMI2803_2_divergence_identity" and row["status"] == "DERIVED_IDENTITY_NOT_ZERO" for row in sections["identity"]), "body moment divergence identity is written"),
        ("VAL2803_3_zero_condition_explicit", any(row["identity_id"] == "BMI2803_4_zero_condition" for row in sections["identity"]), "zero condition is explicit"),
        ("VAL2803_4_zeta_zero_not_claimed", any(row["zeta_id"] == "ZETA2803_3_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["zeta"]), "zeta_q zero proof fails safely"),
        ("VAL2803_5_body_zero_not_claimed", any(row["zero_id"] == "ZM2803_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["zero"]), "body-moment zero theorem fails safely"),
        ("VAL2803_6_force_bound_interface", any(row["bound_id"] == "FB2803_0_acceleration_bound" and row["status"] == "DERIVED_BOUND_INTERFACE_NONNUMERIC" for row in sections["force_bound"]), "acceleration bound interface is staged"),
        ("VAL2803_7_units_missing_recorded", any(row["unit_id"] == "UNIT2803_1_force_density" and row["blocker"] == "MISSING_ZETA_Q" for row in sections["unit_contract"]), "unit/zeta blocker is recorded"),
        ("VAL2803_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2803_9_next_target_2804", any(row["next_id"] == "NEXT2803_0_2804" for row in sections["next"]), "next target is 2804"),
        ("VAL2803_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2803_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2803_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2803_13_cited_paths_exist", cited_paths_exist(sections), "all cited copy/source paths in generated rows exist"),
        ("VAL2803_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2803_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2803_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2803_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2803_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2803 replaces the plateau assumption with an exact q_loc body-moment obstruction identity, keeps zeta/body-zero claims blocked, and stages a nonnumeric force-bound interface.",
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
        "# 2803 - Y5 R2FR q_loc Force Normalization And Body Moment Zero Theorem Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2803 makes the local branch less hand-wavy. Instead of assuming a local-vacuum plateau, it integrates `q_loc` over a compact body.",
        "",
        "The result is an exact obstruction identity: the body moment `I_A^i = int q_loc^i` reduces to a surface traction, a time-dipole term, and projector/connection corrections.",
        "",
        "That is useful progress. Local GR/WEP recovery now has a concrete target: prove the q_loc surface traction has no compact-body flux, the time dipole is stationary or averages away, and the projector/connection corrections vanish or are bounded.",
        "",
        "The zero theorem still does not close. `zeta_q=0` is not parent-signed, and the no-flux/stationarity/projector clauses are not proved. Therefore 2803 makes no local-GR, WEP, orbital, PPN, or source-normalization claim.",
        "",
        "## Body Moment Identity",
        markdown_table(sections["identity"], ["identity_id", "step", "formula", "status", "meaning"]),
        "",
        "## zeta_q Zero Attempt",
        markdown_table(sections["zeta"], ["zeta_id", "claim_piece", "mathematical_form", "missing_input", "status"]),
        "",
        "## Zero Moment Theorem Attempt",
        markdown_table(sections["zero"], ["zero_id", "claim_piece", "mathematical_form", "current_result", "status"]),
        "",
        "## Force Bound Interface",
        markdown_table(sections["force_bound"], ["bound_id", "quantity", "bound_form", "units", "missing_inputs", "status"]),
        "",
        "## q_loc Unit Contract",
        markdown_table(sections["unit_contract"], ["unit_id", "unit_object", "required_relation", "current_status", "blocker"]),
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
        "identity": build_identity_rows(),
        "zeta": build_zeta_rows(),
        "zero": build_zero_rows(),
        "force_bound": build_force_bound_rows(),
        "unit_contract": build_unit_rows(),
        "gates": build_gate_rows(),
        "decision": build_decision_rows(),
        "next": build_next_rows(),
    }

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
