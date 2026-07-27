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
DOC = WORK / "2805-Y5-R2FR-q_loc-superpotential-no-traction-or-zeta-unit-source-acquisition-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2805_SOURCE_REGISTER.csv",
    "superpotential": MTS / "P8_Y5_R2FR_2805_SUPERPOTENTIAL_NO_TRACTION_ATTEMPT.csv",
    "contract": MTS / "P8_Y5_R2FR_2805_PARENT_ACTION_CONTRACT_FOR_UQ.csv",
    "zeta_units": MTS / "P8_Y5_R2FR_2805_ZETA_UNIT_SOURCE_ACQUISITION.csv",
    "numeric_schema": MTS / "P8_Y5_R2FR_2805_FIRST_NUMERIC_FORCE_ROW_SCHEMA.csv",
    "runner": MTS / "P8_Y5_R2FR_2805_FORCE_ROW_RUNNER.csv",
    "gates": MTS / "P8_Y5_R2FR_2805_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2805_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2805_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2805_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2805_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "superpotential_queue": RAB_QUEUE / "JR2805_QLOC_SUPERPOTENTIAL_ATTEMPT_NONCLAIM.csv",
    "contract_queue": RAB_QUEUE / "JR2805_PARENT_ACTION_CONTRACT_FOR_UQ_NONCLAIM.csv",
    "unit_queue": RAB_QUEUE / "JR2805_ZETA_UNIT_SOURCE_ACQUISITION_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "QLOC_SUPERPOTENTIAL_ZETA_UNIT_2805_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_qloc_superpotential_2805_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2805_PARENT_NOETHER_UQ_OR_NUMERIC_FORCE_SEED_NEXT.csv",
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
        ("2804_next", MTS / "P8_Y5_R2FR_2804_NEXT_TARGET.csv", "authoritative 2805 target"),
        ("2804_no_flux", MTS / "P8_Y5_R2FR_2804_SURFACE_TRACTION_NO_FLUX_ATTEMPT.csv", "surface no-flux predecessor"),
        ("2804_force_bound", MTS / "P8_Y5_R2FR_2804_FIRST_REAL_FORCE_BOUND_ATTEMPT.csv", "force-bound predecessor"),
        ("2804_acquisition", MTS / "P8_Y5_R2FR_2804_UNIT_AND_SOURCE_ACQUISITION_LEDGER.csv", "unit/source acquisition predecessor"),
        ("2804_gates", MTS / "P8_Y5_R2FR_2804_CLAIM_GATES.csv", "2804 claim gates"),
        ("2803_identity", MTS / "P8_Y5_R2FR_2803_BODY_MOMENT_IDENTITY.csv", "body moment identity"),
        ("2803_units", MTS / "P8_Y5_R2FR_2803_QLOC_UNIT_CONTRACT.csv", "unit contract predecessor"),
        ("2799_q_loc", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc definition"),
        ("1012_source_owner", MTS / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", "source-owner analogue"),
        ("2801_no_cancel", MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv", "no measured-G/cancellation policy"),
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


def build_superpotential_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "UQ2805_0_target",
            "superpotential no-traction target",
            "tau_q^{ji}=nabla_k U_q^{kji}+R_q^{ji}, with U_q^{kji}=-U_q^{jki}",
            "If R_q=0 and curvature/projector leakage is zero or bounded, closed compact flux is killed.",
            "TARGET_DEFINED",
        ),
        (
            "UQ2805_1_candidate_from_tau",
            "candidate decomposition from existing tau_q",
            "tau_q^{ji}=P_loc(Gamma_eff gamma^{ji}-K_hat^{ji})+delta tau_projector+density terms",
            "This expression is symmetric/metric-like in part and is not itself an antisymmetric-divergence certificate.",
            "NO_UQ_EXTRACTED_FROM_EXISTING_ROWS",
        ),
        (
            "UQ2805_2_noether_route",
            "Noether/Iyer-Wald style parent route",
            "delta S_parent = E_A delta Phi^A + d theta; J_xi=theta(Phi,L_xi Phi)-i_xi L; J_xi=dQ_xi+C_xi",
            "A parent action could supply Q_xi as the superpotential and identify tau_q with dQ_xi plus constraints.",
            "PARENT_ACTION_NOT_AVAILABLE",
        ),
        (
            "UQ2805_3_curvature_leakage",
            "curvature/remainder leakage if U_q exists",
            "Phi_A^i=int_{Sigma_A}[nabla_j,nabla_k]U_q^{kji}+oint R_q^{ji}n_j dS",
            "Even with U_q, curvature/remainder must be killed or bounded.",
            "LEAKAGE_CONTROL_MISSING",
        ),
        (
            "UQ2805_4_no_traction_boundary",
            "boundary no-traction alternative",
            "tau_q^{ji}n_j|_{partial Sigma_A}=0",
            "Needs a source-support/local collar theorem; cannot be assumed by choosing the boundary after the fact.",
            "NO_SURFACE_SILENCE_THEOREM",
        ),
        (
            "UQ2805_5_verdict",
            "superpotential/no-traction verdict",
            "No parent-signed U_q, no R_q bound, and no no-traction collar theorem exist in current evidence.",
            "No-flux route remains open but unproved.",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "superpotential_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("CON2805_0_parent_action", "local covariant parent action exists", "S_parent[Phi,g,psi] with boundary term and variational one-form theta", "MISSING_PARENT_ACTION_OBJECT", "needed to define Noether current and charge"),
        ("CON2805_1_q_loc_embedding", "q_loc appears in parent Euler/constraint identity", "C_xi or E_A L_xi Phi^A contains zeta_q q_loc^nu xi_nu", "MISSING_QLOC_TO_NOETHER_MAP", "needed to identify tau_q with a Noether flux"),
        ("CON2805_2_charge_extraction", "antisymmetric charge two-form exists", "J_xi=dQ_xi+C_xi; U_q derived from Q_xi with antisymmetry U_q^{kji}=-U_q^{jki}", "MISSING_UQ_CHARGE_EXTRACTION", "needed for closed-surface cancellation"),
        ("CON2805_3_remainder_control", "remainder is zero or bounded", "R_q^{ji}=0 or ||R_q||_partial <= sourced epsilon_R", "MISSING_RQ_BOUND", "needed before no-flux or finite bound can score"),
        ("CON2805_4_curvature_control", "curvature commutator term is zero/topological/bounded", "int [nabla,nabla]U_q <= sourced epsilon_curv", "MISSING_CURVATURE_LEAKAGE_BOUND", "needed because antisymmetry alone does not kill curved-space leakage"),
        ("CON2805_5_matter_split", "matter stress split is parent-signed", "nabla_mu T_m^{mu nu}=zeta_q q_loc^nu+nabla_mu B_q^{mu nu}", "MISSING_ZETA_Q_NORMALIZATION", "needed for physical acceleration units"),
        ("CON2805_6_boundary_choice", "compact-body boundary is physical, not fitted", "partial Sigma_A lies in a parent-defined exterior collar/source support boundary", "MISSING_BOUNDARY_OWNERSHIP", "prevents post-hoc no-traction"),
        ("CON2805_7_verdict", "contract for a future parent action", "CON2805_0 through CON2805_6 must be signed", "CONTRACT_WRITTEN_NOT_SATISFIED", "do not promote local branch yet"),
    ]
    return [
        {
            "contract_id": row[0],
            "required_clause": row[1],
            "mathematical_contract": row[2],
            "current_status": row[3],
            "why_needed": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_zeta_unit_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZU2805_0_zeta_q", "zeta_q", "normalization in f_q^nu=zeta_q q_loc^nu", "force_density_per_q_loc_unit", "MISSING_PARENT_MATTER_SPLIT", "cannot score any force bound"),
        ("ZU2805_1_q_loc_units", "q_loc units", "from P_loc(nabla Gamma_eff - nabla K_hat)", "model_units_to_be_declared", "MISSING_GAMMA_KHAT_NORMALIZATION", "cannot compare to acceleration"),
        ("ZU2805_2_tau_units", "tau_q units", "surface traction integral gives force after zeta_q normalization", "traction_units_to_be_declared", "MISSING_BOUNDARY_TRACTION_NORMALIZATION", "cannot score boundary flux"),
        ("ZU2805_3_body_mass", "M_A", "same mass measure used in force, Poisson, and source owner rows", "kg_or_geometric_length", "MISSING_Y5_SOURCE_OWNER", "cannot score WEP/orbit"),
        ("ZU2805_4_surface_area", "A_A", "physical compact-body boundary area", "m^2_or_L^2", "MISSING_BOUNDARY_CHOICE", "cannot evaluate traction norm"),
        ("ZU2805_5_local_g", "g_N", "local Newtonian field for eta_AB denominator", "m/s^2_or_L^-1", "MISSING_SOURCE_MODEL", "cannot score WEP eta"),
        ("ZU2805_6_no_absorption_score", "no measured-G absorption", "residual force/source hair is scored separately from fitted GM", "policy_to_runner_lock", "POLICY_EXISTS_NOT_NUMERIC", "cannot claim orbital pass"),
    ]
    return [
        {
            "source_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "required_units": row[3],
            "status": row[4],
            "blocking_effect": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_numeric_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NFR2805_0_single_body",
            "delta_a_A_bound",
            "|delta a_A| <= |zeta_q|/M_A [A_A(||P Gamma_eff||+||P K_hat||+||delta tau||)+|dD_A/dt|+epsilon_P+epsilon_conn]",
            "zeta_q; M_A; A_A; boundary norms; time dipole; projector constants",
            "NO_NUMERIC_INPUTS",
        ),
        (
            "NFR2805_1_WEP_pair",
            "eta_AB_bound",
            "eta_AB <= |zeta_q|/g_N |I_A/M_A-I_B/M_B| + |Phi_A/M_A-Phi_B/M_B|/g_N",
            "zeta_q; g_N; two body moments; two masses; two boundary fluxes",
            "NO_NUMERIC_INPUTS",
        ),
        (
            "NFR2805_2_orbital_source",
            "delta_a_orbit_bound",
            "|delta a_orb| <= |zeta_q| |I_source|/M_source + |Phi_source|/M_source",
            "zeta_q; source body moment; source mass; boundary flux; no-absorption score",
            "NO_NUMERIC_INPUTS",
        ),
        (
            "NFR2805_3_superpotential_bound",
            "curvature_remainder_bound",
            "|Phi_A| <= Vol_A||Riemann*U_q|| + A_A||R_q||_partial",
            "U_q norm; curvature scale; R_q norm; volume; area",
            "NO_UQ_INPUTS",
        ),
    ]
    return [
        {
            "schema_id": row[0],
            "candidate_row": row[1],
            "bound_form": row[2],
            "required_numeric_inputs": row[3],
            "status": row[4],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_runner_rows(schema_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": f"RUN2805_{index}",
            "schema_id": row["schema_id"],
            "schema_ok": True,
            "numeric_inputs_present": False,
            "unit_contract_present": False,
            "source_paths_present": True,
            "score_ready": False,
            "claim_allowed": False,
            "failure_reasons": f"{row['status']};MISSING_ZETA_Q_OR_UQ;VALID_FOR_CLAIM_FALSE",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for index, row in enumerate(schema_rows)
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2805_0_superpotential_contract", "superpotential proof contract is written", True, "U_q/R_q/curvature/parent-action clauses are explicit"),
        ("CG2805_1_Uq_extracted", "parent-signed U_q is extracted", False, "current rows do not provide parent Noether charge or antisymmetric U_q"),
        ("CG2805_2_no_traction", "surface no-traction/no-flux theorem is proved", False, "no local collar theorem or remainder control exists"),
        ("CG2805_3_zeta_units", "zeta_q and q_loc units are sourced", False, "parent matter split and Gamma/Khat normalization are missing"),
        ("CG2805_4_numeric_force_row", "first numeric WEP/orbital force row is score-ready", False, "numeric inputs and unit contracts are absent"),
        ("CG2805_5_local_claim", "local-GR/WEP/orbital claim can be made", False, "proof and bound routes both remain blocked"),
        ("CG2805_6_nonclaim_pack", "2805 nonclaim proof/acquisition pack is ready", True, "next target is parent Noether extraction or numeric seed acquisition"),
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
        ("DEC2805_0_no_Uq_yet", "No parent-signed superpotential was extracted.", "Existing tau_q is a traction expression, not an antisymmetric Noether-charge certificate.", "hunt parent Noether/U_q explicitly"),
        ("DEC2805_1_contract_written", "The exact parent action contract is now written.", "A future action must sign U_q, R_q, curvature leakage, matter split, and boundary ownership.", "use this as acceptance gate for local branch"),
        ("DEC2805_2_numeric_fallback_blocked", "Numeric force row remains blocked.", "zeta_q, q_loc units, body measure, and boundary norms are missing.", "source normalization/units before any runner claim"),
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
            "next_id": "NEXT2805_0_2806",
            "next_target": "2806-Y5-R2FR-parent-Noether-Uq-extraction-or-first-zeta-unit-numeric-seed-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_Noether_Uq_extraction_or_first_zeta_unit_numeric_seed_under_AX1090_2806.py",
            "objective": "inspect parent/action-like corpus rows for an actual Noether charge U_q; if absent, create the first numeric seed acquisition table for zeta_q/q_loc units and boundary norms",
            "include": "Noether current J_xi; charge Q_xi; U_q antisymmetry; R_q bound; zeta_q; q_loc units; Gamma/Khat normalization; force-row numeric seed schema",
            "exclude": "inventing U_q; plateau axiom; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["superpotential"], BRANCH_OUTPUTS["superpotential_queue"], "superpotential_queue"),
        (OUTPUTS["contract"], BRANCH_OUTPUTS["contract_queue"], "contract_queue"),
        (OUTPUTS["zeta_units"], BRANCH_OUTPUTS["unit_queue"], "unit_queue"),
        (OUTPUTS["contract"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2805_{label}",
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
        ("VAL2805_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2805_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2805_2_superpotential_attempted", any(row["superpotential_id"] == "UQ2805_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["superpotential"]), "superpotential/no-traction route is attempted and not promoted"),
        ("VAL2805_3_contract_written", any(row["contract_id"] == "CON2805_7_verdict" and row["current_status"] == "CONTRACT_WRITTEN_NOT_SATISFIED" for row in sections["contract"]), "parent action contract is written and unsatisfied"),
        ("VAL2805_4_zeta_units_blocked", any(row["source_id"] == "ZU2805_0_zeta_q" and row["status"] == "MISSING_PARENT_MATTER_SPLIT" for row in sections["zeta_units"]), "zeta_q blocker is recorded"),
        ("VAL2805_5_numeric_schema_nonclaim", all(str(row["score_ready"]).lower() == "false" for row in sections["numeric_schema"]), "numeric schemas remain nonclaim"),
        ("VAL2805_6_runner_blocks_claim", all(str(row["claim_allowed"]).lower() == "false" and str(row["score_ready"]).lower() == "false" for row in sections["runner"]), "runner blocks all force-row claims"),
        ("VAL2805_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2805_8_next_target_2806", any(row["next_id"] == "NEXT2805_0_2806" for row in sections["next"]), "next target is 2806"),
        ("VAL2805_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2805_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2805_11_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2805_12_cited_paths_exist", cited_paths_exist(sections), "all cited copy/source paths in generated rows exist"),
        ("VAL2805_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2805_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2805_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2805_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2805_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2805 attempts U_q superpotential/no-traction closure, refuses promotion, writes the parent-action contract, and keeps zeta/unit numeric fallback nonclaim.",
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
        "# 2805 - Y5 R2FR q_loc Superpotential No-Traction Or zeta/unit Source Acquisition Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2805 tries the cleanest mathematical closure for the local branch: make `tau_q` a parent-signed antisymmetric superpotential/no-traction object.",
        "",
        "That proof does not close. The current corpus gives a traction expression for `tau_q`, but not a parent Noether charge `U_q`, not a controlled remainder `R_q`, and not a local surface-silence theorem.",
        "",
        "The useful gain is a stricter parent-action contract. A future parent action must supply the Noether current, the antisymmetric charge, the q_loc embedding, the remainder/curvature bound, the matter split `zeta_q`, and physical boundary ownership.",
        "",
        "The numeric fallback also remains blocked: no first WEP/orbital force row can score until `zeta_q`, q_loc units, body mass measure, and boundary norms are sourced. No local-GR, WEP, orbital, PPN, or source-normalization claim is made.",
        "",
        "## Superpotential No-Traction Attempt",
        markdown_table(sections["superpotential"], ["superpotential_id", "claim_piece", "mathematical_form", "status", "meaning"]),
        "",
        "## Parent Action Contract For U_q",
        markdown_table(sections["contract"], ["contract_id", "required_clause", "mathematical_contract", "current_status", "why_needed"]),
        "",
        "## zeta_q / Unit Source Acquisition",
        markdown_table(sections["zeta_units"], ["source_id", "quantity", "definition", "required_units", "status", "blocking_effect"]),
        "",
        "## First Numeric Force Row Schema",
        markdown_table(sections["numeric_schema"], ["schema_id", "candidate_row", "bound_form", "required_numeric_inputs", "status"]),
        "",
        "## Force Row Runner",
        markdown_table(sections["runner"], ["runner_id", "schema_id", "schema_ok", "numeric_inputs_present", "unit_contract_present", "score_ready", "claim_allowed", "failure_reasons"]),
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
        "superpotential": build_superpotential_rows(),
        "contract": build_contract_rows(),
        "zeta_units": build_zeta_unit_rows(),
        "numeric_schema": build_numeric_schema_rows(),
    }
    sections["runner"] = build_runner_rows(sections["numeric_schema"])
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
