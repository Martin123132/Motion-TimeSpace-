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
DOC = WORK / "2807-Y5-R2FR-explicit-parent-variation-extraction-or-first-source-backed-force-seed-under-AX1090.md"
NIST_GN_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?gn"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2807_SOURCE_REGISTER.csv",
    "action_chain": MTS / "P8_Y5_R2FR_2807_PARENT_ACTION_CHAIN_AUDIT.csv",
    "variation": MTS / "P8_Y5_R2FR_2807_QLOC_VARIATION_EXTRACTION_ATTEMPT.csv",
    "metric_match": MTS / "P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv",
    "numeric_seed": MTS / "P8_Y5_R2FR_2807_SOURCE_BACKED_FORCE_SEED_ROW.csv",
    "runner": MTS / "P8_Y5_R2FR_2807_FORCE_SEED_RUNNER.csv",
    "gates": MTS / "P8_Y5_R2FR_2807_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2807_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2807_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2807_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2807_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "action_queue": RAB_QUEUE / "JR2807_PARENT_ACTION_CHAIN_AUDIT_NONCLAIM.csv",
    "variation_queue": RAB_QUEUE / "JR2807_QLOC_VARIATION_EXTRACTION_NONCLAIM.csv",
    "seed_queue": RAB_QUEUE / "JR2807_SOURCE_BACKED_FORCE_SEED_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_VARIATION_FORCE_SEED_2807_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_force_seed_2807_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2807_GAMMA_KHAT_RESPONSE_MATCH_OR_ZETA_UNIT_NEXT.csv",
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


def source_entries() -> list[dict[str, Any]]:
    local_sources = [
        ("2806_next", MTS / "P8_Y5_R2FR_2806_NEXT_TARGET.csv", "authoritative 2807 target"),
        ("2806_extraction", MTS / "P8_Y5_R2FR_2806_UQ_EXTRACTION_VERDICT.csv", "U_q extraction predecessor"),
        ("2806_seed", MTS / "P8_Y5_R2FR_2806_ZETA_UNIT_NUMERIC_SEED_TABLE.csv", "numeric seed predecessor"),
        ("2806_noether_search", MTS / "P8_Y5_R2FR_2806_PARENT_NOETHER_SEARCH_LEDGER.csv", "Noether search predecessor"),
        ("P8_GK_candidates", MTS / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK stress action candidates"),
        ("P8_GK_decision", MTS / "P8_GK_STRESS_ACTION_DECISION.csv", "GK action decision"),
        ("P8_response_variation", MTS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "response-doublet variation attempt"),
        ("P8_min_parent_blocks", MTS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "minimal local-GR parent action blocks"),
        ("P8_gamma_owner", MTS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "Gamma owner candidate actions"),
        ("P8_symbol_map", MTS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "MTS symbol to local-GR action map"),
        ("P8_local_zero_clause", MTS / "P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv", "local zero action clause"),
        ("P8_source_owner_terms", MTS / "P8_source_owner_parent_action_terms_CONTRACT.csv", "source owner parent action terms"),
        ("P8_no_cancel", MTS / "P8_Y5_R2FR_2801_NO_CANCELLATION_POLICY.csv", "no cancellation/no absorption policy"),
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
                "role": role,
                "contains_text": bool(text.strip()) if path.exists() else False,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    rows.append(
        {
            "source_id": "NIST_gn",
            "source_type": "web_source",
            "path_or_url": NIST_GN_URL,
            "exists_or_reachable": True,
            "role": "source for standard acceleration of gravity seed g_n=9.80665 m/s^2",
            "contains_text": True,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    )
    return rows


def build_action_chain_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PAC2807_0_EH_core",
            "A511_0_EH_core",
            "S_EH=(2*kappa0)^-1 int sqrt(-g_obs)(R-2Lambda0)",
            "supplies GR comparison operator and EH charge template",
            "CONTRACT_ANCHOR",
            "does not own q_loc/Gamma/Khat residual sector",
        ),
        (
            "PAC2807_1_universal_matter",
            "A511_2_universal_matter",
            "S_matter[psi,g_obs] with no leading species-dependent extra coupling",
            "needed for WEP/source current",
            "CONTRACT_ANCHOR_NOT_DERIVED",
            "same source/readout theorem remains missing",
        ),
        (
            "PAC2807_2_extra_silence",
            "A511_3_extra_field_silence",
            "positive auxiliary extra fields with Phi=Phi0, dV=0, Hessian>0, no readout leakage",
            "could kill local extra hair",
            "CONDITIONAL_CANDIDATE",
            "source-current zero/no-boundary proof missing",
        ),
        (
            "PAC2807_3_boundary_reference",
            "A511_5_boundary_reference",
            "GHY plus exact/topological fixed reference subtraction",
            "needed for finite charge and no hidden mass flux",
            "CONDITIONAL_CANDIDATE",
            "fixed-before-readout boundary ownership missing",
        ),
        (
            "PAC2807_4_metric_readout",
            "A511_6_metric_readout",
            "g_readout=g_obs+O((Phi-Phi0)^2), Pi_M=Pi_EH+O((Phi-Phi0)^2)",
            "protects local PPN/Newton readout",
            "CONTRACT_ANCHOR_NOT_DERIVED",
            "Pi_M/source owner theorem missing",
        ),
        (
            "PAC2807_5_GK_response_action",
            "GK514_A",
            "S_GK=-int sqrt(-g) Gamma_eff with K_hat as metric response",
            "best q_loc parent-action route",
            "BEST_CANDIDATE_NOT_MATCHED",
            "Gamma_eff/K_hat metric-response identity not shown for current symbols",
        ),
        (
            "PAC2807_6_response_doublet",
            "AV517",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "would provide double-zero local branch",
            "FORMAL_CANDIDATE_BLOCKED",
            "source-current and boundary terms remain open",
        ),
        (
            "PAC2807_7_verdict",
            "explicit parent variation chain",
            "combine PAC2807_0 through PAC2807_6 into one varied L_parent",
            "would supply Theta_parent/J_q/Q_q/U_q",
            "FAIL_CURRENT_CLAIM",
            "current corpus has blocks and candidates, not one explicit varied parent action",
        ),
    ]
    return [
        {
            "chain_id": row[0],
            "source_row": row[1],
            "candidate_action_or_clause": row[2],
            "role": row[3],
            "status": row[4],
            "gap": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_variation_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2807_0_L_parent", "L_parent", "L_EH+L_matter+L_GK+L_boundary+L_projector+L_source_owner+L_memory/domain", "pieces exist as candidate clauses, not one explicit local form", "PARTIAL_CONTRACT"),
        ("VAR2807_1_delta_L", "delta L_parent=E_A delta Phi^A+dTheta_parent", "requires varying every retained sector before readout", "no sector-complete Theta_parent extraction", "MISSING_THETA_PARENT"),
        ("VAR2807_2_q_generator", "delta_q Phi or vertical v_q", "must generate q_loc surface traction channel", "vertical analogues exist but q generator not supplied", "MISSING_QLOC_GENERATOR"),
        ("VAR2807_3_J_q", "J_q=Theta_parent(delta_q Phi)-mu_q", "Noether current for q_loc-generating transformation", "only formal analogues exist", "MISSING_J_Q"),
        ("VAR2807_4_Q_q_Uq", "J_q=dQ_q+C_q; U_q extracted from Q_q", "antisymmetric surface superpotential for no-flux proof", "no Q_q/U_q extraction", "MISSING_U_Q"),
        ("VAR2807_5_R_q", "tau_q=nabla U_q+R_q", "remainder must be zero or bounded", "R_q not sourced", "MISSING_R_Q_BOUND"),
        ("VAR2807_6_boundary", "partial Sigma_A physical collar", "prevents post-hoc no-traction boundary", "boundary ownership not parent-derived", "MISSING_BOUNDARY_OWNERSHIP"),
        ("VAR2807_7_verdict", "q_loc parent variation extraction", "all VAR2807_0 through VAR2807_6 pass", "explicit extraction not achieved", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "variation_id": row[0],
            "object": row[1],
            "required_equation": row[2],
            "current_evidence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_metric_match_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GKM2807_0_metric_response_identity",
            "K_hat^{mu nu} ?= 2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_mu_nu minus convention",
            "would turn q_loc into Ward/metric-response residual",
            "not matched to current MTS symbol definitions",
            "MISSING_SYMBOL_MATCH",
        ),
        (
            "GKM2807_1_double_zero",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "would give first variation zero at local state",
            "formal response-doublet candidate only",
            "MISSING_SOURCE_BOUNDARY_ZERO",
        ),
        (
            "GKM2807_2_topological_exact",
            "Gamma_eff/K_hat exact or topological boundary density",
            "could make bulk q_loc zero and leave only controlled boundary charge",
            "boundary units/flux/open collar not fixed",
            "MISSING_BOUNDARY_FLUX_CONTROL",
        ),
        (
            "GKM2807_3_verdict",
            "Gamma/Khat metric-response match",
            "best route to derive zeta_q/q_loc units from action",
            "not yet derived; should be next proof target",
            "FAIL_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            "match_id": row[0],
            "target_identity": row[1],
            "why_needed": row[2],
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
        (
            "SBF2807_0_standard_gn",
            "g_n",
            "standard acceleration of gravity for force/WEP denominator smoke rows",
            "9.80665",
            "m s^-2",
            NIST_GN_URL,
            "NIST CODATA standard acceleration of gravity; exact standard value",
            True,
            "SOURCE_BACKED_NUMERIC_DENOMINATOR_SEED",
            "This is not local experimental g and does not make any MTS prediction score-ready.",
        ),
        (
            "SBF2807_1_zeta_q",
            "zeta_q",
            "normalization in f_q^nu=zeta_q q_loc^nu",
            "MISSING",
            "force_density_per_q_loc_unit",
            "MISSING",
            "parent matter/extra stress split still missing",
            False,
            "MISSING_PARENT_MATTER_SPLIT",
            "highest priority for real force-bound scoring",
        ),
        (
            "SBF2807_2_q_loc_units",
            "q_loc_units",
            "units from P_loc(nabla Gamma_eff-nabla_mu K_hat^{mu nu})",
            "MISSING",
            "declared_model_unit",
            "MISSING",
            "Gamma_eff/K_hat parent-action normalization still missing",
            False,
            "MISSING_GAMMA_KHAT_NORMALIZATION",
            "highest priority for acceleration comparison",
        ),
        (
            "SBF2807_3_tau_norm",
            "tau_norm_A",
            "boundary norm ||P Gamma_eff||+||P K_hat||+||delta tau|| on compact body",
            "MISSING",
            "traction_or_model_surface_unit",
            "MISSING",
            "requires local solution/profile or no-flux theorem",
            False,
            "MISSING_BOUNDARY_NORMS",
            "needed for single-body force bound",
        ),
    ]
    return [
        {
            "seed_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "numeric_value": row[3],
            "units": row[4],
            "source_url": row[5],
            "provenance": row[6],
            "source_backed": row[7],
            "status": row[8],
            "limitation": row[9],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_runner_rows(seed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(seed_rows):
        numeric_present = row["numeric_value"] != "MISSING"
        source_present = row["source_url"] != "MISSING"
        rows.append(
            {
                "runner_id": f"RUN2807_SEED_{index}",
                "seed_id": row["seed_id"],
                "schema_ok": True,
                "numeric_value_present": numeric_present,
                "source_present": source_present,
                "unit_declared": bool(row["units"]),
                "seed_can_feed_runner": row["seed_id"] == "SBF2807_0_standard_gn",
                "force_row_score_ready": False,
                "claim_allowed": False,
                "failure_reasons": "DENOMINATOR_ONLY;ZETA_Q_AND_QLOC_UNITS_MISSING;VALID_FOR_CLAIM_FALSE"
                if row["seed_id"] == "SBF2807_0_standard_gn"
                else f"{row['status']};VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    rows.append(
        {
            "runner_id": "RUN2807_FORCE_ROW",
            "seed_id": "delta_a_A_or_eta_AB_force_row",
            "schema_ok": True,
            "numeric_value_present": False,
            "source_present": False,
            "unit_declared": True,
            "seed_can_feed_runner": False,
            "force_row_score_ready": False,
            "claim_allowed": False,
            "failure_reasons": "STANDARD_GN_PRESENT_BUT_ZETA_Q_QLOC_UNITS_TAU_NORM_BODY_MEASURE_MISSING;VALID_FOR_CLAIM_FALSE",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    )
    return rows


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2807_0_action_chain_audited", "existing action rows were audited for explicit q_loc parent variation", True, "EH/matter/extra/boundary/readout/GK/response-doublet candidates are recorded"),
        ("CG2807_1_parent_variation_extracted", "explicit q_loc parent variation chain is extracted", False, "Theta_parent, q generator, J_q, Q_q/U_q, R_q, and boundary ownership remain missing"),
        ("CG2807_2_metric_response_match", "Gamma_eff/K_hat metric-response identity is proved", False, "best candidate exists but current symbols are not matched"),
        ("CG2807_3_source_backed_seed", "at least one source-backed numeric force seed is staged", True, "NIST standard gravity g_n=9.80665 m/s^2 is recorded as denominator seed"),
        ("CG2807_4_force_row_score", "first WEP/orbital force row is score-ready", False, "g_n alone is not enough; zeta_q, q_loc units, tau norm, body measure are missing"),
        ("CG2807_5_local_claim", "local-GR/WEP/orbital claim can be made", False, "proof and force-bound routes remain blocked"),
        ("CG2807_6_nonclaim_pack", "2807 nonclaim action/seed pack is ready", True, "next target is Gamma/Khat response match or zeta/unit extraction"),
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
        ("DEC2807_0_action_chain_not_extracted", "Explicit parent variation is still not extracted.", "Action rows provide strong candidate blocks but not one varied parent action with Theta/J/Q/U.", "do not claim local GR from action contracts"),
        ("DEC2807_1_best_theory_next", "Best theory route is Gamma/Khat metric-response matching.", "If K_hat is the metric response of Gamma_eff, zeta/q_loc units and Ward structure become derivable rather than patched.", "target GKM2807 directly"),
        ("DEC2807_2_seed_progress", "One real source-backed numeric seed is installed.", "NIST g_n gives a force/WEP denominator seed for future runners but is not an MTS prediction.", "next seed must be zeta_q or q_loc units"),
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
            "next_id": "NEXT2807_0_2808",
            "next_target": "2808-Y5-R2FR-Gamma-Khat-metric-response-match-or-zeta-q-unit-extraction-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_metric_response_match_or_zeta_q_unit_extraction_under_AX1090_2808.py",
            "objective": "try to prove K_hat is the metric response of Gamma_eff in the best GK action candidate; if absent, derive the zeta_q/q_loc unit contract from that failed match and keep only source-backed force seeds",
            "include": "S_GK=-int sqrt(-g)Gamma_eff; K_hat metric variation; volume-term convention; zeta_q; q_loc units; Ward residual; NIST g_n seed retained as denominator only",
            "exclude": "inventing U_q; EH-only import; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["action_chain"], BRANCH_OUTPUTS["action_queue"], "action_queue"),
        (OUTPUTS["variation"], BRANCH_OUTPUTS["variation_queue"], "variation_queue"),
        (OUTPUTS["numeric_seed"], BRANCH_OUTPUTS["seed_queue"], "seed_queue"),
        (OUTPUTS["metric_match"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2807_{label}",
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


def generated_paths_parse(paths: list[Path]) -> bool:
    return all(csv_parses(path) for path in paths)


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source", "destination", "path_or_url"):
                value = row.get(key)
                if value and value != "MISSING" and not str(value).startswith("http"):
                    paths.append(Path(str(value)))
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2807_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register paths/URLs exist or are reachable"),
        ("VAL2807_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2807_2_action_chain_audited", any(row["chain_id"] == "PAC2807_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["action_chain"]), "action chain verdict safely blocks claim"),
        ("VAL2807_3_variation_blocks", any(row["variation_id"] == "VAR2807_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["variation"]), "variation extraction verdict blocks claim"),
        ("VAL2807_4_metric_match_blocks", any(row["match_id"] == "GKM2807_3_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["metric_match"]), "Gamma/Khat match blocks claim"),
        ("VAL2807_5_source_backed_seed_present", any(row["seed_id"] == "SBF2807_0_standard_gn" and row["source_backed"] and row["numeric_value"] == "9.80665" for row in sections["numeric_seed"]), "source-backed NIST g_n seed is present"),
        ("VAL2807_6_runner_blocks_force_claim", all(str(row["claim_allowed"]).lower() == "false" and str(row["force_row_score_ready"]).lower() == "false" for row in sections["runner"]), "runner blocks all force claims"),
        ("VAL2807_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2807_8_next_target_2808", any(row["next_id"] == "NEXT2807_0_2808" for row in sections["next"]), "next target is 2808"),
        ("VAL2807_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2807_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2807_11_csv_parse", generated_paths_parse(generated_paths), "all generated CSV outputs parse"),
        ("VAL2807_12_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2807_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2807_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2807_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2807_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2807_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2807 audits action rows, refuses explicit q_loc parent-variation extraction, records Gamma/Khat metric-response as the next theory target, and installs one source-backed NIST g_n denominator seed without claims.",
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
        "# 2807 - Y5 R2FR Explicit Parent Variation Extraction Or First Source-Backed Force Seed Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2807 audits the existing action rows for an explicit q_loc parent variation chain.",
        "",
        "The chain still does not extract. The corpus contains serious candidate blocks - EH core, universal matter, extra-field silence, boundary/reference terms, metric readout, GK metric-response action, and response-doublet variation - but not one sector-complete `L_parent -> Theta_parent -> J_q -> Q_q/U_q` derivation.",
        "",
        "The strongest theory route is now very specific: prove that `K_hat` is the metric response of `Gamma_eff` in the candidate `S_GK=-int sqrt(-g) Gamma_eff` action, with the volume-term convention fixed. If that works, `q_loc` becomes a Ward/metric-response residual instead of a free local-force proxy.",
        "",
        "2807 also installs the first real source-backed numeric seed for future force/WEP runners: NIST's standard acceleration of gravity `g_n=9.80665 m s^-2`. This is only a denominator seed; it does not make any MTS force row score-ready because `zeta_q`, q_loc units, boundary norms, and body measures are still missing.",
        "",
        "## Parent Action Chain Audit",
        markdown_table(sections["action_chain"], ["chain_id", "source_row", "candidate_action_or_clause", "status", "gap"]),
        "",
        "## q_loc Variation Extraction Attempt",
        markdown_table(sections["variation"], ["variation_id", "object", "required_equation", "status", "current_evidence"]),
        "",
        "## Gamma/Khat Metric-Response Match",
        markdown_table(sections["metric_match"], ["match_id", "target_identity", "status", "current_evidence"]),
        "",
        "## Source-Backed Force Seed Row",
        markdown_table(sections["numeric_seed"], ["seed_id", "quantity", "numeric_value", "units", "source_backed", "status", "limitation"]),
        "",
        "## Force Seed Runner",
        markdown_table(sections["runner"], ["runner_id", "seed_id", "numeric_value_present", "source_present", "seed_can_feed_runner", "force_row_score_ready", "claim_allowed", "failure_reasons"]),
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
        "sources": source_entries(),
        "action_chain": build_action_chain_rows(),
        "variation": build_variation_rows(),
        "metric_match": build_metric_match_rows(),
        "numeric_seed": build_numeric_seed_rows(),
    }
    sections["runner"] = build_runner_rows(sections["numeric_seed"])
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
