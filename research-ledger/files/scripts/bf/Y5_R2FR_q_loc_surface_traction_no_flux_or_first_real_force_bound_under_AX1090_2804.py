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
DOC = WORK / "2804-Y5-R2FR-q_loc-surface-traction-no-flux-or-first-real-force-bound-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2804_SOURCE_REGISTER.csv",
    "no_flux": MTS / "P8_Y5_R2FR_2804_SURFACE_TRACTION_NO_FLUX_ATTEMPT.csv",
    "traction_bound": MTS / "P8_Y5_R2FR_2804_TRACTION_BOUND_DECOMPOSITION.csv",
    "force_bound": MTS / "P8_Y5_R2FR_2804_FIRST_REAL_FORCE_BOUND_ATTEMPT.csv",
    "runner": MTS / "P8_Y5_R2FR_2804_FORCE_BOUND_RUNNER.csv",
    "unit_sources": MTS / "P8_Y5_R2FR_2804_UNIT_AND_SOURCE_ACQUISITION_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2804_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2804_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2804_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2804_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2804_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "no_flux_queue": RAB_QUEUE / "JR2804_QLOC_SURFACE_TRACTION_NO_FLUX_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2804_FIRST_REAL_FORCE_BOUND_ATTEMPT_NONCLAIM.csv",
    "unit_queue": RAB_QUEUE / "JR2804_UNIT_SOURCE_ACQUISITION_LEDGER_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "QLOC_SURFACE_TRACTION_BOUND_2804_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_qloc_surface_traction_2804_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2804_QLOC_SUPERPOTENTIAL_OR_TRACTION_SOURCE_NEXT.csv",
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
        ("2803_next", MTS / "P8_Y5_R2FR_2803_NEXT_TARGET.csv", "authoritative 2804 target"),
        ("2803_identity", MTS / "P8_Y5_R2FR_2803_BODY_MOMENT_IDENTITY.csv", "body-moment obstruction identity"),
        ("2803_force_bound", MTS / "P8_Y5_R2FR_2803_FORCE_BOUND_INTERFACE.csv", "force-bound predecessor"),
        ("2803_zero", MTS / "P8_Y5_R2FR_2803_ZERO_MOMENT_THEOREM_ATTEMPT.csv", "zero-moment theorem predecessor"),
        ("2803_units", MTS / "P8_Y5_R2FR_2803_QLOC_UNIT_CONTRACT.csv", "unit blocker predecessor"),
        ("2803_gates", MTS / "P8_Y5_R2FR_2803_CLAIM_GATES.csv", "2803 claim gates"),
        ("2799_q_loc", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc definition"),
        ("2799_bound", MTS / "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "rolled q_loc bound interface"),
        ("2801_no_cancel", MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv", "no measured-G/cancellation policy"),
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


def build_no_flux_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SNF2804_0_surface_traction_object",
            "surface traction to kill",
            "Phi_A^i := oint_{partial Sigma_A} tau_q^{ji} n_j dS",
            "tau_q^{ji}=P_loc(Gamma_eff gamma^{ji}-K_hat^{ji})+delta tau_projector+density terms",
            "DEFINED_FROM_2803",
            "This is now the precise local-vacuum surface object, not a vague plateau.",
        ),
        (
            "SNF2804_1_superpotential_route",
            "antisymmetric superpotential would kill flux on closed compact surfaces",
            "tau_q^{ji}=nabla_k U_q^{kji}+R_q^{ji}, U_q^{kji}=-U_q^{jki}; Phi_A^i=int_{Sigma_A}[nabla_j,nabla_k]U_q^{kji}+oint R_q^{ji}n_jdS",
            "need U_q parent-signed and curvature/remainder controlled",
            "SUPERPOTENTIAL_NOT_SIGNED",
            "This is the cleanest no-flux theorem route, but the parent action has not supplied U_q.",
        ),
        (
            "SNF2804_2_local_vacuum_surface_route",
            "traction vanishes on the chosen compact-body boundary",
            "tau_q^{ji}|_{partial Sigma_A}=0",
            "need a theorem that the body boundary lies in a q_loc-silent collar, not a fitted plateau",
            "NO_LOCAL_SURFACE_SILENCE_THEOREM",
            "Cannot assume this; it must follow from field equations or source support.",
        ),
        (
            "SNF2804_3_stationary_dipole_route",
            "time dipole term vanishes or averages away",
            "d/dt int_{Sigma_A} P_loc K_hat^{0i}sqrt(gamma)d^3x=0 or <dD_A^i/dt>_orbit=0",
            "need stationary/periodic local branch theorem",
            "STATIONARITY_NOT_SIGNED",
            "Without this, local force can leak through time-dependent internal momentum.",
        ),
        (
            "SNF2804_4_projector_connection_route",
            "projector/connection corrections vanish or are bounded",
            "C_P^i=C_conn^i=0 or |C_P^i+C_conn^i|<=epsilon_PC",
            "need P_loc commutation and connection correction control",
            "PROJECTOR_CONNECTION_NOT_CLOSED",
            "This is the same hard projector ownership issue seen earlier, now in force language.",
        ),
        (
            "SNF2804_5_verdict",
            "surface-traction no-flux theorem",
            "Phi_A^i=0 only if SNF2804_1 or SNF2804_2 plus SNF2804_3 and SNF2804_4 close",
            "no theorem route currently closes",
            "FAIL_CURRENT_CLAIM",
            "No local-GR/WEP claim; however, the required clauses are now exact.",
        ),
    ]
    return [
        {
            "no_flux_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "required_evidence": row[3],
            "status": row[4],
            "interpretation": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_traction_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TBD2804_0_flux_decomposition",
            "Phi_A^i",
            "oint P_loc Gamma_eff n^i dS - oint P_loc K_hat^{ji}n_j dS + Phi_density^i + Phi_projector^i",
            "surface force flux split into Gamma, K_hat, density, and projector pieces",
            "exact decomposition up to declared correction terms",
        ),
        (
            "TBD2804_1_norm_bound",
            "|Phi_A|",
            "<= A_A(||P_loc Gamma_eff||_partial + ||P_loc K_hat||_partial + ||delta tau_projector||_partial)",
            "first real surface-traction norm bound form",
            "nonnumeric until boundary area and norms are sourced",
        ),
        (
            "TBD2804_2_superpotential_curvature_bound",
            "|Phi_A| if tau_q=nabla U_q+R_q",
            "<= Vol_A ||Riemann * U_q|| + A_A ||R_q||_partial",
            "if superpotential exists, only curvature/remainder leakage remains",
            "requires parent U_q and curvature scale",
        ),
        (
            "TBD2804_3_stationary_correction",
            "|dD_A/dt|",
            "<= omega_A |D_A| or zero under exact stationary branch",
            "time-dipole correction for force bound",
            "requires stationarity or orbital average theorem",
        ),
        (
            "TBD2804_4_projector_connection_bound",
            "|C_P+C_conn|",
            "<= epsilon_P + epsilon_conn",
            "commutator/connection correction budget",
            "requires P_loc domain constants",
        ),
    ]
    return [
        {
            "bound_piece_id": row[0],
            "quantity": row[1],
            "bound_form": row[2],
            "meaning": row[3],
            "status": row[4],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_force_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FFB2804_0_single_body_acceleration",
            "delta a_A",
            "|delta a_A| <= |zeta_q|/M_A [A_A(||P Gamma_eff||+||P K_hat||+||delta tau||)+|dD_A/dt|+epsilon_P+epsilon_conn]",
            "acceleration",
            "zeta_q; M_A; boundary area; Gamma/K_hat boundary norms; time-dipole; projector constants",
            "BOUND_FORM_DERIVED_NOT_NUMERIC",
        ),
        (
            "FFB2804_1_WEP_eta",
            "eta_AB",
            "<= (|zeta_q|/g_N)|I_A/M_A-I_B/M_B| + |Phi_A/M_A-Phi_B/M_B|/g_N",
            "dimensionless",
            "two-body moments; source/test-body masses; local g_N; zeta_q",
            "BOUND_FORM_DERIVED_NOT_NUMERIC",
        ),
        (
            "FFB2804_2_orbital_residual",
            "delta a_orb",
            "<= |zeta_q| |I_source|/M_source + |Phi_source|/M_source, scored without measured-G absorption",
            "acceleration",
            "source body moment; no-absorption split; orbital radius/source model",
            "BOUND_FORM_DERIVED_NOT_NUMERIC",
        ),
        (
            "FFB2804_3_first_real_row_verdict",
            "first force-bound row",
            "no numeric row can be claimed until zeta_q and q_loc units are sourced",
            "nonclaim",
            "parent normalization and boundary norm data are absent",
            "RUNNER_BLOCKED_CORRECTLY",
        ),
    ]
    return [
        {
            "force_bound_id": row[0],
            "observable": row[1],
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


def build_runner_rows(force_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(force_rows):
        rows.append(
            {
                "runner_id": f"RUN2804_{index}",
                "input_id": row["force_bound_id"],
                "schema_ok": True,
                "units_declared": bool(row["units"]),
                "numeric_inputs_present": False,
                "source_paths_present": True,
                "score_ready": False,
                "claim_allowed": False,
                "failure_reasons": f"{row['status']};{row['missing_inputs']};VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_unit_source_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2804_0_zeta_q", "zeta_q", "normalization in f_q^nu=zeta_q q_loc^nu", "parent matter/extra stress split", "MISSING_PARENT_NORMALIZATION", "highest priority"),
        ("ACQ2804_1_q_loc_units", "q_loc units", "[zeta_q q_loc]=force density", "Gamma_eff/K_hat parent action normalization", "MISSING_QLOC_UNIT_CONVENTION", "highest priority"),
        ("ACQ2804_2_surface_norms", "||P Gamma_eff||_partial and ||P K_hat||_partial", "surface traction norm", "local solution or analytic no-flux theorem", "MISSING_BOUNDARY_NORMS", "needed for numeric force row"),
        ("ACQ2804_3_body_measure", "M_A and A_A", "same body mass and boundary area used in force/source map", "Y5 source owner/worldtube measure", "MISSING_SOURCE_OWNER", "needed for WEP/orbital row"),
        ("ACQ2804_4_projector_constants", "epsilon_P, epsilon_conn", "projector/connection correction budget", "P_loc commutator and domain constants", "MISSING_PROJECTOR_CONTROL", "needed for no-flux or bound"),
        ("ACQ2804_5_no_absorption", "measured-G no-absorption score", "force/source hair not hidden in fitted GM", "2801 policy plus source row scoring", "POLICY_EXISTS_NOT_SCORED", "needed before orbital claim"),
    ]
    return [
        {
            "acquisition_id": row[0],
            "quantity": row[1],
            "role": row[2],
            "source_needed": row[3],
            "status": row[4],
            "priority": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2804_0_surface_object", "q_loc surface traction object is explicit", True, "tau_q/Phi_A decomposition is written"),
        ("CG2804_1_no_flux", "surface traction no-flux theorem is proved", False, "superpotential/local-surface-silence route is not parent-signed"),
        ("CG2804_2_stationary_projector", "stationary dipole and projector/connection terms vanish", False, "stationarity and P_loc commutator control are missing"),
        ("CG2804_3_first_force_bound", "first real WEP/orbital force-bound row is score-ready", False, "zeta_q, q_loc units, and boundary norms are absent"),
        ("CG2804_4_local_claim", "local GR/WEP/orbital claim can be made", False, "no-flux and numeric-bound routes both fail"),
        ("CG2804_5_nonclaim_pack", "2804 nonclaim no-flux/bound pack is ready", True, "next target is superpotential/source acquisition"),
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
        ("DEC2804_0_no_flux_not_proved", "Surface no-flux is not proved.", "The exact routes require a parent superpotential or a local surface-silence theorem; neither is sourced.", "do not claim local GR/WEP"),
        ("DEC2804_1_bound_shape_improved", "The first force-bound shape is now sharper.", "The bound is in Gamma/K_hat boundary norms plus time/projector corrections, not an amorphous q_loc proxy.", "source zeta_q and q_loc units next"),
        ("DEC2804_2_best_next", "Best next target is superpotential or source acquisition.", "Either prove tau_q is an exact antisymmetric superpotential/no-traction object, or obtain the normalization needed for numeric bounds.", "2805 should choose proof-first with bound fallback"),
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
            "next_id": "NEXT2804_0_2805",
            "next_target": "2805-Y5-R2FR-q_loc-superpotential-no-traction-or-zeta-unit-source-acquisition-under-AX1090.md",
            "script": "scripts/Y5_R2FR_q_loc_superpotential_no_traction_or_zeta_unit_source_acquisition_under_AX1090_2805.py",
            "objective": "prove tau_q is a parent-signed antisymmetric superpotential/no-traction object, or source zeta_q/q_loc units for the first numeric WEP/orbital force-bound row",
            "include": "U_q superpotential; tau_q remainder R_q; curvature leakage; zeta_q; q_loc units; Gamma/K_hat boundary norms; no measured-G absorption",
            "exclude": "plateau axiom; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["no_flux"], BRANCH_OUTPUTS["no_flux_queue"], "no_flux_queue"),
        (OUTPUTS["force_bound"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["unit_sources"], BRANCH_OUTPUTS["unit_queue"], "unit_queue"),
        (OUTPUTS["traction_bound"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2804_{label}",
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
        ("VAL2804_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2804_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2804_2_surface_object_defined", any(row["no_flux_id"] == "SNF2804_0_surface_traction_object" for row in sections["no_flux"]), "surface traction object is defined"),
        ("VAL2804_3_no_flux_not_promoted", any(row["no_flux_id"] == "SNF2804_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["no_flux"]), "no-flux theorem fails safely"),
        ("VAL2804_4_traction_bound_decomposed", any(row["bound_piece_id"] == "TBD2804_1_norm_bound" for row in sections["traction_bound"]), "traction norm bound is decomposed"),
        ("VAL2804_5_force_bound_not_numeric", all(str(row["score_ready"]).lower() == "false" for row in sections["force_bound"]), "force-bound rows remain nonnumeric"),
        ("VAL2804_6_runner_blocks_claim", all(str(row["claim_allowed"]).lower() == "false" and str(row["score_ready"]).lower() == "false" for row in sections["runner"]), "runner blocks all force-bound claims"),
        ("VAL2804_7_acquisition_high_priority", any(row["acquisition_id"] == "ACQ2804_0_zeta_q" and row["priority"] == "highest priority" for row in sections["unit_sources"]), "zeta_q acquisition is prioritized"),
        ("VAL2804_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2804_9_next_target_2805", any(row["next_id"] == "NEXT2804_0_2805" for row in sections["next"]), "next target is 2805"),
        ("VAL2804_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2804_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2804_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2804_13_cited_paths_exist", cited_paths_exist(sections), "all cited copy/source paths in generated rows exist"),
        ("VAL2804_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2804_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2804_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2804_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2804_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2804 defines the q_loc surface traction no-flux proof clauses, refuses promotion, sharpens the first force-bound shape, and selects superpotential/zeta-unit acquisition as 2805.",
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
        "# 2804 - Y5 R2FR q_loc Surface Traction No-Flux Or First Real Force Bound Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2804 tries the clean route: make the compact-body surface traction vanish without sneaking in a plateau axiom.",
        "",
        "The no-flux proof does not close. It would close if `tau_q` were parent-signed as an antisymmetric superpotential with controlled curvature/remainder, or if the parent field equations gave a true local surface-silence theorem. Neither is currently in the corpus.",
        "",
        "The fallback does improve the situation: the first force-bound row is now written in concrete boundary data, `Gamma_eff`, `K_hat`, time-dipole, and projector/connection terms. It is still nonnumeric because `zeta_q`, q_loc units, body measure, and boundary norms are not sourced.",
        "",
        "Therefore 2804 makes no local-GR, WEP, orbital, PPN, or source-normalization claim. The next best move is proof-first again: hunt for a parent superpotential/no-traction structure; failing that, source `zeta_q` and unit contracts.",
        "",
        "## Surface Traction No-Flux Attempt",
        markdown_table(sections["no_flux"], ["no_flux_id", "claim_piece", "mathematical_form", "status", "interpretation"]),
        "",
        "## Traction Bound Decomposition",
        markdown_table(sections["traction_bound"], ["bound_piece_id", "quantity", "bound_form", "meaning", "status"]),
        "",
        "## First Real Force Bound Attempt",
        markdown_table(sections["force_bound"], ["force_bound_id", "observable", "bound_form", "units", "missing_inputs", "status"]),
        "",
        "## Force Bound Runner",
        markdown_table(sections["runner"], ["runner_id", "input_id", "schema_ok", "units_declared", "numeric_inputs_present", "score_ready", "claim_allowed", "failure_reasons"]),
        "",
        "## Unit And Source Acquisition Ledger",
        markdown_table(sections["unit_sources"], ["acquisition_id", "quantity", "role", "status", "priority"]),
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
        "no_flux": build_no_flux_rows(),
        "traction_bound": build_traction_bound_rows(),
        "force_bound": build_force_bound_rows(),
    }
    sections["runner"] = build_runner_rows(sections["force_bound"])
    sections["unit_sources"] = build_unit_source_rows()
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
