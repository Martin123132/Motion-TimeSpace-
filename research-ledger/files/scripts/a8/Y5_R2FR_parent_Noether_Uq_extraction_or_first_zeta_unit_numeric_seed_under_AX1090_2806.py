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
DOC = WORK / "2806-Y5-R2FR-parent-Noether-Uq-extraction-or-first-zeta-unit-numeric-seed-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2806_SOURCE_REGISTER.csv",
    "search": MTS / "P8_Y5_R2FR_2806_PARENT_NOETHER_SEARCH_LEDGER.csv",
    "uq_candidates": MTS / "P8_Y5_R2FR_2806_UQ_EXTRACTION_CANDIDATES.csv",
    "extraction": MTS / "P8_Y5_R2FR_2806_UQ_EXTRACTION_VERDICT.csv",
    "numeric_seed": MTS / "P8_Y5_R2FR_2806_ZETA_UNIT_NUMERIC_SEED_TABLE.csv",
    "force_seed": MTS / "P8_Y5_R2FR_2806_FORCE_ROW_NUMERIC_SEED_SCHEMA.csv",
    "runner": MTS / "P8_Y5_R2FR_2806_SEED_RUNNER.csv",
    "gates": MTS / "P8_Y5_R2FR_2806_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2806_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2806_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2806_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2806_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "search_queue": RAB_QUEUE / "JR2806_PARENT_NOETHER_SEARCH_LEDGER_NONCLAIM.csv",
    "uq_queue": RAB_QUEUE / "JR2806_UQ_EXTRACTION_CANDIDATES_NONCLAIM.csv",
    "seed_queue": RAB_QUEUE / "JR2806_ZETA_UNIT_NUMERIC_SEED_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_NOETHER_UQ_ZETA_SEED_2806_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_parent_noether_uq_2806_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2806_EXPLICIT_PARENT_VARIATION_OR_FORCE_SEED_SOURCE_NEXT.csv",
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


def source_entries() -> list[tuple[str, Path, str, str]]:
    return [
        ("2805_next", MTS / "P8_Y5_R2FR_2805_NEXT_TARGET.csv", "authoritative 2806 target", "2806 handoff"),
        ("2805_contract", MTS / "P8_Y5_R2FR_2805_PARENT_ACTION_CONTRACT_FOR_UQ.csv", "parent-action U_q contract", "contract predecessor"),
        ("2805_superpotential", MTS / "P8_Y5_R2FR_2805_SUPERPOTENTIAL_NO_TRACTION_ATTEMPT.csv", "superpotential failure predecessor", "contract predecessor"),
        ("2805_zeta_units", MTS / "P8_Y5_R2FR_2805_ZETA_UNIT_SOURCE_ACQUISITION.csv", "zeta/unit blockers", "numeric seed predecessor"),
        ("1008_doc", WORK / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md", "parent theta/Q_tau extraction audit", "Noether search hit"),
        ("1008_parent_variation", MTS / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv", "theta/Q_tau extraction rows", "Noether search hit"),
        ("1008_charge_piece", MTS / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv", "Q_tau piece ledger", "Noether search hit"),
        ("12_gauge_noether", WORK / "12-gauge-noether-origin-audit.md", "Noether warning audit", "Noether search hit"),
        ("2184_charge_chain", MTS / "P8_Y5_PARENT_QLOC_2184_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv", "q_loc-related Noether/Hamiltonian charge chain", "Noether search hit"),
        ("2393_vertical_charge", MTS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv", "vertical Noether charge attempt", "Noether search hit"),
        ("parent_noether_chain", MTS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv", "parent Noether closure chain", "Noether search hit"),
        ("2699_residual_decomp", MTS / "P8_Y5_R2FR_2699_NOETHER_RESIDUAL_DECOMPOSITION.csv", "q_loc residual decomposition", "Noether search hit"),
        ("2801_no_cancel", MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv", "no cancellation/no absorption policy", "force seed guard"),
    ]


def build_sources() -> list[dict[str, Any]]:
    rows = []
    for source_id, path, role, source_class in source_entries():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": sp(path),
                "exists": path.exists(),
                "role": role,
                "source_class": source_class,
                "contains_text": bool(text.strip()) if path.exists() else False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_search_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SEARCH2806_0_1008",
            "1008 parent theta/Q_tau audit",
            "theta_MTS, J_tau, Q_tau^MTS",
            "formal Noether/charge decomposition exists but every candidate is refused without explicit parent L, theta, sector charge pieces, and source constraints",
            "CONTRACT_FOUND_NOT_UQ",
            WORK / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        ),
        (
            "SEARCH2806_1_gauge_noether",
            "gauge-Noether warning audit",
            "Noether identity",
            "Noether identity relates equations; it does not set the target residual to zero without a genuine constrained parent action",
            "WARNING_NOT_PROOF",
            WORK / "12-gauge-noether-origin-audit.md",
        ),
        (
            "SEARCH2806_2_2184",
            "q_loc Noether/Hamiltonian charge chain",
            "J_tau, Q_tau, H_tau",
            "chain is exact conditional on supplied action and source measure, but PiM/Hilbert identity remains missing",
            "CONDITIONAL_CHAIN_NOT_UQ",
            MTS / "P8_Y5_PARENT_QLOC_2184_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
        ),
        (
            "SEARCH2806_3_2393",
            "vertical Noether charge theorem",
            "Q_v, C_v, B_v",
            "formal vertical charge contract exists, but Q_v, C_v, improvement, compact boundary conditions, and parent L/Theta are not extracted",
            "CLOSEST_ANALOGUE_NOT_EXTRACTED",
            MTS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv",
        ),
        (
            "SEARCH2806_4_parent_chain",
            "parent Noether closure chain",
            "Q_M[tau]",
            "generic parent mass charge form exists with residual pieces, but it is not the q_loc surface superpotential U_q",
            "GENERIC_CHARGE_NOT_UQ",
            MTS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        ),
        (
            "SEARCH2806_5_2699",
            "R2FR Noether residual decomposition",
            "q_boundary_flux, q_Ploc_commutator, q_readout_defect",
            "residual channels are identified and no-cancellation envelope is explicit, but no antisymmetric U_q or zero theorem is supplied",
            "RESIDUAL_LEDGER_NOT_UQ",
            MTS / "P8_Y5_R2FR_2699_NOETHER_RESIDUAL_DECOMPOSITION.csv",
        ),
    ]
    return [
        {
            "search_id": row[0],
            "source": row[1],
            "objects_found": row[2],
            "finding": row[3],
            "status": row[4],
            "source_path": sp(row[5]),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_uq_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "UQC2806_0_EH_Qtau",
            "Q_tau^EH",
            "EH covariant phase-space charge",
            "can be comparison template for GR",
            "not the MTS q_loc superpotential; import requires parent MTS reduction/silence",
            "REJECT_AS_UQ",
        ),
        (
            "UQC2806_1_total_Qtau",
            "Q_tau^MTS",
            "total parent Hamiltonian charge candidate",
            "would be a parent charge if theta/Q_tau extraction closed",
            "1008 says theta_MTS and retained sector charges are not extracted",
            "NOT_EXTRACTED",
        ),
        (
            "UQC2806_2_vertical_Qv",
            "Q_v",
            "vertical Noether charge from q/kernel direction",
            "closest structural analogue to U_q",
            "2393 leaves Q_v, C_v, B_v, parent L/Theta, and boundary conditions missing",
            "CLOSEST_BUT_NOT_EXTRACTED",
        ),
        (
            "UQC2806_3_parent_QM",
            "Q_M[tau]",
            "parent mass charge in local exterior closure chain",
            "useful for source-normalization/Newton bridge",
            "generic mass charge does not equal tau_q^{ji}=nabla_k U_q^{kji}+R_q^{ji}",
            "GENERIC_CHARGE_NOT_UQ",
        ),
        (
            "UQC2806_4_noether_identity",
            "Noether identity",
            "dJ=-E L_xi Phi plus boundary terms",
            "organizes residual ownership",
            "identity alone is not an antisymmetric charge or zero-flux theorem",
            "IDENTITY_NOT_UQ",
        ),
        (
            "UQC2806_5_verdict",
            "U_q",
            "required antisymmetric q_loc surface superpotential",
            "would close no-flux if parent-signed with controlled remainder",
            "no current source supplies U_q with antisymmetry, q_loc embedding, R_q bound, curvature bound, and boundary ownership",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "candidate_id": row[0],
            "candidate_object": row[1],
            "candidate_type": row[2],
            "useful_role": row[3],
            "rejection_or_gap": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_extraction_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXT2806_0_parent_L", "explicit parent Lagrangian/current chain", "delta L_parent=E_A delta Phi^A+dTheta_parent", "found only as required contract, not supplied across all sectors", "MISSING"),
        ("EXT2806_1_theta", "parent symplectic potential", "Theta_parent with EH, matter, extra, projector, boundary/reference pieces", "1008/2393 require it; not extracted", "MISSING"),
        ("EXT2806_2_current", "Noether current for q_loc-generating transformation", "J_q=Theta_parent(delta_q Phi)-mu_q", "vertical-current analogue exists only conditionally", "MISSING"),
        ("EXT2806_3_charge", "antisymmetric charge/superpotential", "J_q=dQ_q+C_q and U_q from Q_q", "no Q_q/U_q supplied", "MISSING"),
        ("EXT2806_4_remainder", "controlled residual remainder", "R_q=0 or ||R_q|| bounded", "no bound or theorem", "MISSING"),
        ("EXT2806_5_boundary", "physical compact boundary ownership", "partial Sigma_A in parent-defined collar/source support", "no collar theorem", "MISSING"),
        ("EXT2806_6_verdict", "U_q extraction verdict", "all extraction clauses pass", "none of the decisive clauses pass; extraction fails safely", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "extraction_id": row[0],
            "required_object": row[1],
            "mathematical_requirement": row[2],
            "current_evidence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_numeric_seed_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEED2806_0_zeta_q", "zeta_q", "f_q^nu=zeta_q q_loc^nu", "force_density_per_q_loc_unit", "parent matter/extra stress split", "MISSING_PARENT_MATTER_SPLIT", "highest"),
        ("SEED2806_1_q_loc_units", "q_loc_units", "q_loc=P_loc(nabla Gamma_eff-nabla_mu K_hat^{mu nu})", "declared_model_unit", "Gamma_eff/K_hat normalization in parent action", "MISSING_GAMMA_KHAT_NORMALIZATION", "highest"),
        ("SEED2806_2_tau_norm", "||tau_q||_partial", "||P_loc(Gamma_eff gamma-K_hat)+delta tau|| on compact boundary", "traction_or_model_surface_unit", "local solution profile or analytic no-flux theorem", "MISSING_BOUNDARY_NORMS", "high"),
        ("SEED2806_3_time_dipole", "|dD_A/dt|", "d/dt int P_loc K_hat^{0i} sqrt(gamma)d^3x", "force_or_model_momentum_rate", "stationarity/periodic average theorem or profile", "MISSING_TIME_DIPOLE_BOUND", "high"),
        ("SEED2806_4_projector_constants", "epsilon_P,epsilon_conn", "C_P+C_conn correction budget", "force_or_model_correction_unit", "P_loc commutator/domain constants", "MISSING_PROJECTOR_CONSTANTS", "high"),
        ("SEED2806_5_body_measure", "M_A,A_A,Vol_A", "mass/area/volume for compact body boundary", "kg,m2,m3 or geometric units", "Y5 source-owner/worldtube measure", "MISSING_SOURCE_OWNER", "high"),
        ("SEED2806_6_local_field", "g_N", "Newtonian denominator for eta_AB", "m/s^2 or geometric acceleration", "source model and no measured-G absorption split", "MISSING_SOURCE_MODEL", "medium"),
        ("SEED2806_7_Uq_seed", "U_q,R_q,curvature_scale", "|Phi_A|<=Vol_A||Riemann*U_q||+A_A||R_q||", "charge_norm_and_curvature_units", "parent Noether charge extraction", "MISSING_UQ", "proof-route"),
    ]
    return [
        {
            "seed_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "required_units": row[3],
            "source_needed": row[4],
            "status": row[5],
            "priority": row[6],
            "numeric_value": "MISSING",
            "source_path": "MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_force_seed_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FS2806_0_single_body",
            "delta_a_A",
            "|delta a_A| <= |zeta_q|/M_A [A_A tau_norm_A + time_dipole_A + epsilon_P + epsilon_conn]",
            "SEED2806_0_zeta_q;SEED2806_2_tau_norm;SEED2806_3_time_dipole;SEED2806_4_projector_constants;SEED2806_5_body_measure",
            "NOT_SCORE_READY",
        ),
        (
            "FS2806_1_WEP_pair",
            "eta_AB",
            "eta_AB <= |zeta_q|/g_N |I_A/M_A-I_B/M_B| + |Phi_A/M_A-Phi_B/M_B|/g_N",
            "SEED2806_0_zeta_q;SEED2806_5_body_measure;SEED2806_6_local_field;two material profiles",
            "NOT_SCORE_READY",
        ),
        (
            "FS2806_2_orbital_source",
            "delta_a_orbit",
            "|delta a_orbit| <= |zeta_q||I_source|/M_source + |Phi_source|/M_source, with no measured-G absorption",
            "SEED2806_0_zeta_q;SEED2806_5_body_measure;SEED2806_6_local_field;no_absorption_score",
            "NOT_SCORE_READY",
        ),
        (
            "FS2806_3_superpotential_flux",
            "Phi_A",
            "|Phi_A| <= Vol_A||Riemann*U_q|| + A_A||R_q||_partial",
            "SEED2806_7_Uq_seed;SEED2806_5_body_measure",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "force_seed_id": row[0],
            "observable": row[1],
            "bound_or_row_form": row[2],
            "required_seed_ids": row[3],
            "status": row[4],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_runner_rows(seed_rows: list[dict[str, Any]], force_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(seed_rows):
        rows.append(
            {
                "runner_id": f"RUN2806_SEED_{index}",
                "input_id": row["seed_id"],
                "input_type": "numeric_seed",
                "schema_ok": True,
                "numeric_value_present": False,
                "source_path_present": False,
                "score_ready": False,
                "claim_allowed": False,
                "failure_reasons": f"{row['status']};NUMERIC_VALUE_MISSING;SOURCE_PATH_MISSING;VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    for index, row in enumerate(force_rows):
        rows.append(
            {
                "runner_id": f"RUN2806_FORCE_{index}",
                "input_id": row["force_seed_id"],
                "input_type": "force_seed_schema",
                "schema_ok": True,
                "numeric_value_present": False,
                "source_path_present": False,
                "score_ready": False,
                "claim_allowed": False,
                "failure_reasons": f"{row['status']};REQUIRED_SEEDS_NOT_SCORE_READY;VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2806_0_search_complete", "targeted parent-Noether corpus search completed", True, "1008, 12, 2184, 2393, parent chain, and 2699 rows were inspected"),
        ("CG2806_1_Uq_extracted", "parent-signed U_q was extracted", False, "closest candidates are conditional contracts, not extracted antisymmetric superpotentials"),
        ("CG2806_2_no_flux_reopen", "surface no-flux theorem can reopen", False, "U_q, R_q bound, curvature leakage, and boundary ownership remain missing"),
        ("CG2806_3_numeric_seed_ready", "first zeta/unit numeric seed row is score-ready", False, "all seeds still lack numeric values and source paths"),
        ("CG2806_4_force_row_score", "first WEP/orbital force row can score", False, "required seeds are not score-ready"),
        ("CG2806_5_local_claim", "local-GR/WEP/orbital claim can be made", False, "Noether proof and numeric bound routes both blocked"),
        ("CG2806_6_nonclaim_pack", "2806 nonclaim search/seed pack is ready", True, "next target is explicit parent variation extraction or numeric source acquisition"),
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
        ("DEC2806_0_Uq_absent", "No claimable U_q is present in the inspected corpus.", "All relevant Noether files provide formal contracts/templates or generic charges, not an extracted q_loc antisymmetric superpotential.", "do not use Noether language as a shortcut"),
        ("DEC2806_1_best_proof_route", "The best proof route is explicit parent variation extraction.", "Only a real L_parent, Theta_parent, J_q, Q_q/U_q, R_q and boundary ownership can close no-flux.", "attack parent variation directly"),
        ("DEC2806_2_best_bound_route", "The best empirical route is numeric seed acquisition.", "zeta_q, q_loc units, boundary norms, body measure, and projector constants are the minimal table for a real force runner.", "build first source-backed seed row before scoring"),
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
            "next_id": "NEXT2806_0_2807",
            "next_target": "2807-Y5-R2FR-explicit-parent-variation-extraction-or-first-source-backed-force-seed-under-AX1090.md",
            "script": "scripts/Y5_R2FR_explicit_parent_variation_extraction_or_first_source_backed_force_seed_under_AX1090_2807.py",
            "objective": "try to assemble an explicit parent variation chain for q_loc from existing action rows; if absent, fill one source-backed numeric seed row for zeta_q/q_loc units/boundary norm acquisition",
            "include": "L_parent; Theta_parent; J_q; Q_q/U_q; R_q; boundary ownership; zeta_q; q_loc units; first source-backed seed row",
            "exclude": "inventing U_q; EH-only import; generic Q_M promoted as q_loc proof; proxy scoring; local-GR/WEP/orbital claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["search"], BRANCH_OUTPUTS["search_queue"], "search_queue"),
        (OUTPUTS["uq_candidates"], BRANCH_OUTPUTS["uq_queue"], "uq_queue"),
        (OUTPUTS["numeric_seed"], BRANCH_OUTPUTS["seed_queue"], "seed_queue"),
        (OUTPUTS["extraction"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2806_{label}",
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
            for key in ("source_path", "destination"):
                value = row.get(key)
                if value and value != "MISSING":
                    paths.append(Path(str(value)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2806_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2806_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2806_2_search_hits_recorded", len(sections["search"]) >= 6, "targeted Noether search hits are recorded"),
        ("VAL2806_3_Uq_verdict_blocks", any(row["candidate_id"] == "UQC2806_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["uq_candidates"]), "U_q extraction verdict blocks claim"),
        ("VAL2806_4_extraction_verdict_blocks", any(row["extraction_id"] == "EXT2806_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["extraction"]), "extraction verdict fails safely"),
        ("VAL2806_5_seed_rows_nonclaim", all(str(row["score_ready"]).lower() == "false" for row in sections["numeric_seed"]), "numeric seed rows remain nonclaim"),
        ("VAL2806_6_force_seed_nonclaim", all(str(row["score_ready"]).lower() == "false" for row in sections["force_seed"]), "force seed rows remain nonclaim"),
        ("VAL2806_7_runner_blocks_claim", all(str(row["claim_allowed"]).lower() == "false" and str(row["score_ready"]).lower() == "false" for row in sections["runner"]), "runner blocks all rows"),
        ("VAL2806_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2806_9_next_target_2807", any(row["next_id"] == "NEXT2806_0_2807" for row in sections["next"]), "next target is 2807"),
        ("VAL2806_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2806_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2806_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2806_13_cited_paths_exist", cited_paths_exist(sections), "all cited copy/source paths in generated rows exist"),
        ("VAL2806_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2806_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2806_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2806_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2806_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2806 inspects targeted parent-Noether/q_loc charge sources, finds no claimable U_q, and stages nonclaim zeta/unit numeric seed tables for the first force-bound row.",
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
        "# 2806 - Y5 R2FR Parent Noether U_q Extraction Or First zeta/unit Numeric Seed Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2806 performs the targeted corpus search for a real parent Noether `U_q` rather than assuming it is missing.",
        "",
        "Result: no claimable `U_q` is present. The useful older Noether files provide contracts, templates, EH/reference charge shapes, vertical charge analogues, and generic mass-charge chains, but none supplies an extracted antisymmetric q_loc surface superpotential with q_loc embedding, remainder bound, curvature bound, and boundary ownership.",
        "",
        "This does not kill the local route. It means the proof-first route must now go after an explicit parent variation chain: `L_parent -> Theta_parent -> J_q -> Q_q/U_q -> R_q/boundary ownership`.",
        "",
        "The fallback is now a concrete numeric-seed table for the first force-bound row. It remains nonclaim because `zeta_q`, q_loc units, boundary norms, body measure, projector constants, and source paths are all still missing.",
        "",
        "## Parent Noether Search Ledger",
        markdown_table(sections["search"], ["search_id", "source", "objects_found", "status", "finding"]),
        "",
        "## U_q Extraction Candidates",
        markdown_table(sections["uq_candidates"], ["candidate_id", "candidate_object", "candidate_type", "status", "rejection_or_gap"]),
        "",
        "## U_q Extraction Verdict",
        markdown_table(sections["extraction"], ["extraction_id", "required_object", "mathematical_requirement", "status", "current_evidence"]),
        "",
        "## zeta/unit Numeric Seed Table",
        markdown_table(sections["numeric_seed"], ["seed_id", "quantity", "definition", "required_units", "status", "priority"]),
        "",
        "## Force Row Numeric Seed Schema",
        markdown_table(sections["force_seed"], ["force_seed_id", "observable", "bound_or_row_form", "required_seed_ids", "status"]),
        "",
        "## Seed Runner",
        markdown_table(sections["runner"], ["runner_id", "input_id", "input_type", "numeric_value_present", "source_path_present", "score_ready", "claim_allowed", "failure_reasons"]),
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
        "search": build_search_rows(),
        "uq_candidates": build_uq_candidate_rows(),
        "extraction": build_extraction_rows(),
        "numeric_seed": build_numeric_seed_rows(),
    }
    sections["force_seed"] = build_force_seed_rows()
    sections["runner"] = build_runner_rows(sections["numeric_seed"], sections["force_seed"])
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
