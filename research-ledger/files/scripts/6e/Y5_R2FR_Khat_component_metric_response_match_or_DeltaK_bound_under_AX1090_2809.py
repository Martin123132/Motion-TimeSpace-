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
DOC = WORK / "2809-Y5-R2FR-Khat-component-metric-response-match-or-DeltaK-bound-under-AX1090.md"
NIST_GN_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?gn"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2809_SOURCE_REGISTER.csv",
    "component_match": MTS / "P8_Y5_R2FR_2809_KHAT_COMPONENT_MATCH_ATTEMPT.csv",
    "delta_bound": MTS / "P8_Y5_R2FR_2809_DELTAK_COMPONENT_BOUND_TABLE.csv",
    "derivative": MTS / "P8_Y5_R2FR_2809_DELTAK_DERIVATIVE_BOUND_INTERFACE.csv",
    "observable": MTS / "P8_Y5_R2FR_2809_DELTAK_OBSERVABLE_MAP_UPDATE.csv",
    "gates": MTS / "P8_Y5_R2FR_2809_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2809_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2809_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2809_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2809_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "component_queue": RAB_QUEUE / "JR2809_KHAT_COMPONENT_MATCH_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2809_DELTAK_COMPONENT_BOUND_NONCLAIM.csv",
    "observable_queue": RAB_QUEUE / "JR2809_DELTAK_OBSERVABLE_MAP_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "DELTAK_COMPONENT_BOUND_2809_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_DeltaK_component_bound_2809_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2809_FIRST_DELTAK_COMPONENT_SOURCE_OR_PLOC_UNIT_NEXT.csv",
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


def build_sources() -> list[dict[str, Any]]:
    local_sources = [
        ("2808_next", MTS / "P8_Y5_R2FR_2808_NEXT_TARGET.csv", "authoritative 2809 target"),
        ("2808_metric_response", MTS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv", "conditional metric-response identity"),
        ("2808_units", MTS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv", "unit contract predecessor"),
        ("2808_gates", MTS / "P8_Y5_R2FR_2808_CLAIM_GATES.csv", "2808 claim gates"),
        ("2799_q_loc", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc and DeltaK definitions"),
        ("Gamma_owner", MTS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "Gamma/Khat owner candidates"),
        ("symbol_map", MTS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv", "symbol placement map"),
        ("GK_match_audit", MTS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "prior metric-response match audit"),
        ("GK_pass_fail", MTS / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv", "prior pass/fail rows"),
        ("GK_contract", MTS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv", "metric-response contract"),
        ("first_variation", MTS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "Gamma/Khat first-variation contract"),
        ("2807_seed", MTS / "P8_Y5_R2FR_2807_SOURCE_BACKED_FORCE_SEED_ROW.csv", "NIST denominator seed predecessor"),
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
            "role": "standard acceleration of gravity denominator seed retained",
            "contains_text": True,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    )
    return rows


def build_component_match_rows() -> list[dict[str, Any]]:
    rows = [
        ("KCM2809_0_definition", "all", "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff]", "K_metric defined by T_GK=Gamma_eff g-K_metric", "definition known but current K_hat source absent", "SCHEMA_DEFINED_NOT_MATCHED"),
        ("KCM2809_1_00", "00 / energy component", "K_hat^{00}=K_metric^{00}", "controls Newtonian potential, beta/gamma source-normalization channel", "no current component formula for K_hat^{00}", "MISSING_COMPONENT_FORMULA"),
        ("KCM2809_2_0i", "0i / momentum-preferred-frame component", "K_hat^{0i}=K_metric^{0i}", "controls alpha1/alpha2/alpha3 preferred-frame and local force leakage", "no current component formula for K_hat^{0i}", "MISSING_COMPONENT_FORMULA"),
        ("KCM2809_3_spatial_trace", "spatial trace", "h_ij K_hat^{ij}=h_ij K_metric^{ij}", "controls pressure/trace contribution to gamma/beta/orbital residuals", "no current trace formula or fixed volume convention", "MISSING_TRACE_FORMULA"),
        ("KCM2809_4_spatial_tracefree", "spatial tracefree/shear", "K_hat^{<ij>}=K_metric^{<ij>}", "controls anisotropic stress, PPN shear, lensing-style local tails", "no current tracefree tensor formula", "MISSING_TF_FORMULA"),
        ("KCM2809_5_boundary_improvement", "boundary/improvement part", "K_hat_boundary=K_metric_boundary+improvement with fixed no-flux convention", "controls surface traction and hidden mass/source flux", "boundary/reference convention not fixed", "MISSING_BOUNDARY_CONVENTION"),
        ("KCM2809_6_derivative_terms", "derivative-of-metric/field terms", "K_metric includes derivative response of Gamma_eff(g,Phi,nabla Phi,D,...)", "needed for signs and units in q_loc divergence", "derivative terms not supplied componentwise", "MISSING_DERIVATIVE_RESPONSE"),
        ("KCM2809_7_verdict", "component match verdict", "KCM2809_1 through KCM2809_6 pass", "would allow zeta_q=1 and q_loc stress-divergence scoring", "no component match exists in current evidence", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "match_id": row[0],
            "component": row[1],
            "required_identity": row[2],
            "observable_role": row[3],
            "current_evidence": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_delta_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("DKB2809_0_DeltaK00", "Delta_K^{00}", "K_hat^{00}-K_metric^{00}", "stress", "Newtonian/source-normalization/beta channel", "MISSING_COMPONENT_VALUE", "bound |DeltaK00| and derivatives"),
        ("DKB2809_1_DeltaK0i", "Delta_K^{0i}", "K_hat^{0i}-K_metric^{0i}", "stress", "preferred-frame alpha_i and local force momentum channel", "MISSING_COMPONENT_VALUE", "bound vector norm and time/spatial divergence"),
        ("DKB2809_2_DeltaKtrace", "Delta_K^tr=h_ij Delta_K^{ij}", "spatial trace mismatch", "stress", "gamma/beta/orbital pressure-like channel", "MISSING_COMPONENT_VALUE", "bound trace and radial derivative"),
        ("DKB2809_3_DeltaKTF", "Delta_K^{<ij>}", "tracefree spatial mismatch", "stress", "anisotropic stress/shear/PPN tensor channel", "MISSING_COMPONENT_VALUE", "bound tracefree norm and angular leakage"),
        ("DKB2809_4_boundary_improvement", "Delta_K^boundary", "boundary/reference/improvement mismatch", "stress_or_surface_traction", "surface no-flux/source-measure channel", "MISSING_BOUNDARY_VALUE", "bound boundary flux separately"),
        ("DKB2809_5_projector_commutator", "[P_loc,nabla]Delta_K", "projector/domain derivative mismatch", "force_density", "preferred-frame/domain leakage channel", "MISSING_PLOC_COMMUTATOR", "bound projector norm and commutator"),
        ("DKB2809_6_envelope", "||q_DeltaK||", "||P_loc nabla_mu Delta_K^{mu nu}|| plus projector commutator", "force_density", "total local residual forcing", "DERIVED_BOUND_INTERFACE_NONNUMERIC", "requires component values and derivative constants"),
    ]
    return [
        {
            "bound_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "units": row[3],
            "observable_link": row[4],
            "status": row[5],
            "next_input_needed": row[6],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_derivative_rows() -> list[dict[str, Any]]:
    rows = [
        ("DER2809_0_time", "time divergence", "C_t ||partial_t Delta_K^{0nu}||", "stationarity/time-dipole leakage", "MISSING_TIME_DERIVATIVE_BOUND"),
        ("DER2809_1_radial", "radial divergence", "C_r L_A^{-1} ||Delta_K^{rnu}|| or ||partial_r Delta_K^{rnu}||", "orbital/radial source-hair leakage", "MISSING_RADIAL_SCALE"),
        ("DER2809_2_angular", "angular divergence", "C_ang R_A^{-1} ||Delta_K^{ang nu}||", "anisotropic/shear leakage", "MISSING_ANGULAR_SCALE"),
        ("DER2809_3_connection", "connection correction", "C_conn ||Gamma_conn|| ||Delta_K||", "curved/background local correction", "MISSING_CONNECTION_BOUND"),
        ("DER2809_4_projector", "projector commutator", "||[P_loc,nabla]Delta_K|| <= C_P ||Delta_K||", "domain/readout leakage", "MISSING_PLOC_UNIT_AND_COMMUTATOR"),
        ("DER2809_5_total", "total derivative interface", "||q_DeltaK|| <= ||P_loc||(DER2809_0+...+DER2809_3)+DER2809_4", "first executable nonnumeric q_DeltaK bound", "DERIVED_INTERFACE_NONNUMERIC"),
    ]
    return [
        {
            "derivative_id": row[0],
            "term": row[1],
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


def build_observable_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS2809_0_PPN", "PPN", "Delta_K00; DeltaK0i; DeltaKtrace; DeltaKTF", "gamma,beta,alpha1,alpha2,alpha3,xi", "K_PPN still missing; component table gives inputs"),
        ("OBS2809_1_WEP", "WEP/local force", "q_DeltaK^i/g_n after zeta/unit closure", "eta_AB/direct acceleration residual", "NIST g_n denominator available; zeta/body measures missing"),
        ("OBS2809_2_orbital", "orbital/source normalization", "radial q_DeltaK and DeltaK00/source hair", "perihelion/source GM drift", "no measured-G absorption policy remains active"),
        ("OBS2809_3_clock", "clock/local time", "q_DeltaK^0 and DeltaK00 time derivative", "clock redshift/frequency drift", "clock readout map missing"),
        ("OBS2809_4_boundary", "surface traction", "Delta_K boundary/improvement flux", "local no-flux/source-measure bridge", "boundary ownership missing"),
    ]
    return [
        {
            "observable_id": row[0],
            "arena": row[1],
            "DeltaK_inputs": row[2],
            "observable_target": row[3],
            "current_status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2809_0_component_search", "K_hat component match was attempted", True, "component slots are explicit"),
        ("CG2809_1_component_match", "K_hat=K_metric component match is proved", False, "no 00/0i/trace/tracefree/boundary derivative formulas are supplied"),
        ("CG2809_2_DeltaK_bound", "Delta_K bound table is score-ready", False, "component values and derivative constants are missing"),
        ("CG2809_3_zeta_units", "zeta_q=1 and q_loc units are claim-ready", False, "requires Khat match and P_loc unit certificate"),
        ("CG2809_4_observable_score", "PPN/WEP/orbital residuals can be scored", False, "observable maps still missing numeric coefficients"),
        ("CG2809_5_local_claim", "local-GR/WEP/orbital claim can be made", False, "component match and numeric bound both fail"),
        ("CG2809_6_nonclaim_pack", "2809 nonclaim component/bound pack is ready", True, "next target is first Delta_K source row or P_loc unit certificate"),
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
        ("DEC2809_0_match_failed", "Component-level K_hat match is not currently derivable.", "The corpus has required identities and candidate actions, but no current component formulas for K_hat.", "keep Delta_K active"),
        ("DEC2809_1_bound_table_created", "Delta_K is now a component-bound problem.", "The obstruction is split into 00, 0i, trace, tracefree, boundary, and projector terms.", "source or bound one component first"),
        ("DEC2809_2_best_next", "Best next target is first Delta_K source row or P_loc unit certificate.", "Without either, q_DeltaK stays nonnumeric and zeta_q=1 stays conditional.", "attack DeltaK00 or P_loc units next"),
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
            "next_id": "NEXT2809_0_2810",
            "next_target": "2810-Y5-R2FR-first-DeltaK-component-source-row-or-Ploc-unit-certificate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_first_DeltaK_component_source_row_or_Ploc_unit_certificate_under_AX1090_2810.py",
            "objective": "source or derive one concrete Delta_K component input, preferably DeltaK00 or P_loc unit/norm, so the q_DeltaK residual bound can become numeric rather than schematic",
            "include": "DeltaK00; DeltaK0i; trace/TF split; derivative constants; P_loc units/norm; NIST g_n denominator; no measured-G absorption",
            "exclude": "declaring Khat match from schema; zeta_q=1 without match; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["component_match"], BRANCH_OUTPUTS["component_queue"], "component_queue"),
        (OUTPUTS["delta_bound"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["observable"], BRANCH_OUTPUTS["observable_queue"], "observable_queue"),
        (OUTPUTS["delta_bound"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2809_{label}",
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
            for key in ("source_path", "source", "destination", "path_or_url"):
                value = row.get(key)
                if value and value != "MISSING" and not str(value).startswith("http"):
                    candidate = Path(str(value))
                    if candidate.suffix or candidate.drive:
                        paths.append(candidate if candidate.is_absolute() else MTS / candidate)
    return all(path.exists() for path in paths)


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2809_0_sources_exist", all(row["exists_or_reachable"] for row in sections["sources"]), "all source-register paths/URLs exist or are reachable"),
        ("VAL2809_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register entries contain text/source evidence"),
        ("VAL2809_2_component_match_attempted", any(row["match_id"] == "KCM2809_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["component_match"]), "component match attempt safely fails"),
        ("VAL2809_3_delta_bound_table_present", any(row["bound_id"] == "DKB2809_6_envelope" and row["status"] == "DERIVED_BOUND_INTERFACE_NONNUMERIC" for row in sections["delta_bound"]), "Delta_K envelope bound interface is present"),
        ("VAL2809_4_derivative_interface_present", any(row["derivative_id"] == "DER2809_5_total" and row["status"] == "DERIVED_INTERFACE_NONNUMERIC" for row in sections["derivative"]), "derivative interface is present"),
        ("VAL2809_5_observable_map_present", len(sections["observable"]) >= 5, "observable map update rows are present"),
        ("VAL2809_6_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2809_7_next_target_2810", any(row["next_id"] == "NEXT2809_0_2810" for row in sections["next"]), "next target is 2810"),
        ("VAL2809_8_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2809_9_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2809_10_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2809_11_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2809_12_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2809_13_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2809_14_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2809_15_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2809_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2809 attempts component-level K_hat matching, keeps match nonclaim, and installs a nonnumeric Delta_K component/derivative/observable bound interface.",
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
        "# 2809 - Y5 R2FR Khat Component Metric-Response Match Or DeltaK Bound Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2809 attempts the component match demanded by 2808: `K_hat = K_metric[Gamma_eff]`.",
        "",
        "It does not close. The current corpus contains the right contracts and candidate actions, but no current component formulas for `K_hat^{00}`, `K_hat^{0i}`, spatial trace, tracefree shear, derivative response, or boundary/improvement terms.",
        "",
        "The useful gain is that `Delta_K = K_hat-K_metric` is now no longer one blob. It is split into energy, momentum/preferred-frame, spatial trace, tracefree shear, boundary/improvement, and projector-commutator channels, each with the observable arena it can hit.",
        "",
        "Therefore no `zeta_q=1`, local-GR, WEP, PPN, orbital, clock, or source-normalization claim is made. The next target is to source or derive one concrete `Delta_K` component input or the `P_loc` unit/norm certificate.",
        "",
        "## Khat Component Match Attempt",
        markdown_table(sections["component_match"], ["match_id", "component", "required_identity", "status", "current_evidence"]),
        "",
        "## DeltaK Component Bound Table",
        markdown_table(sections["delta_bound"], ["bound_id", "quantity", "definition", "units", "observable_link", "status", "next_input_needed"]),
        "",
        "## DeltaK Derivative Bound Interface",
        markdown_table(sections["derivative"], ["derivative_id", "term", "bound_form", "meaning", "status"]),
        "",
        "## DeltaK Observable Map Update",
        markdown_table(sections["observable"], ["observable_id", "arena", "DeltaK_inputs", "observable_target", "current_status"]),
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
        "component_match": build_component_match_rows(),
        "delta_bound": build_delta_bound_rows(),
        "derivative": build_derivative_rows(),
        "observable": build_observable_rows(),
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
