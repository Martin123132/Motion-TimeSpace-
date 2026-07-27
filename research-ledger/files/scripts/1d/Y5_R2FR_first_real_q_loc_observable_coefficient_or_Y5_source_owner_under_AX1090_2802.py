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
DOC = WORK / "2802-Y5-R2FR-first-real-q_loc-observable-coefficient-or-Y5-source-owner-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2802_SOURCE_REGISTER.csv",
    "coefficient": MTS / "P8_Y5_R2FR_2802_FIRST_OBSERVABLE_COEFFICIENT_DERIVATION.csv",
    "worldtube": MTS / "P8_Y5_R2FR_2802_WORLD_TUBE_FORCE_MAP.csv",
    "source_owner": MTS / "P8_Y5_R2FR_2802_K_SOURCE_OWNER_ATTEMPT.csv",
    "ppn": MTS / "P8_Y5_R2FR_2802_K_PPN_ATTEMPT.csv",
    "closure": MTS / "P8_Y5_R2FR_2802_CLOSURE_OR_BOUND_DECISION.csv",
    "gates": MTS / "P8_Y5_R2FR_2802_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2802_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2802_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2802_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2802_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "coefficient_queue": RAB_QUEUE / "JR2802_FIRST_QLOC_OBSERVABLE_COEFFICIENT_NONCLAIM.csv",
    "worldtube_queue": RAB_QUEUE / "JR2802_WORLD_TUBE_FORCE_MAP_NONCLAIM.csv",
    "source_owner_queue": RAB_QUEUE / "JR2802_K_SOURCE_OWNER_ATTEMPT_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "QLOC_FIRST_COEFFICIENT_2802_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_qloc_force_kernel_2802_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2802_QLOC_FORCE_NORMALIZATION_OR_BODY_MOMENT_ZERO_NEXT.csv",
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
        ("2801_next", MTS / "P8_Y5_R2FR_2801_NEXT_TARGET.csv", "authoritative 2802 target"),
        ("2801_map_attempt", MTS / "P8_Y5_R2FR_2801_QLOC_OBSERVABLE_MAP_ATTEMPT.csv", "observable map gaps"),
        ("2801_runner", MTS / "P8_Y5_R2FR_2801_COEFFICIENT_RUNNER.csv", "coefficient runner failures"),
        ("2801_numeric_bound", MTS / "P8_Y5_R2FR_2801_FIRST_NUMERIC_BOUND_ROW_ATTEMPT.csv", "numeric proxy nonclaim row"),
        ("2801_gates", MTS / "P8_Y5_R2FR_2801_CLAIM_GATES.csv", "2801 claim gates"),
        ("2799_q_loc_residual", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc definition"),
        ("2733_bound_interface", MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "q_loc symbolic bound interface"),
        ("1012_source_owner", MTS / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", "source-normalization owner analogue"),
        ("1012_source_coefficients", MTS / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv", "source coefficient analogue"),
        ("1012_constant_GM", MTS / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv", "constant measured-GM residual analogue"),
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


def build_coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "COEFF2802_0_stress_balance_normalizer",
            "zeta_q",
            "nabla_mu T_m^{mu nu} = zeta_q q_loc^nu + nabla_mu B_q^{mu nu}",
            "normalizes q_loc as a force-density/nonconservation residual",
            "MISSING_PARENT_NORMALIZATION",
            "This is the only scalar normalizer needed before q_loc can become a force observable.",
        ),
        (
            "COEFF2802_1_body_acceleration_kernel",
            "K_force[A]",
            "delta a_A^i = (zeta_q/M_A) int_{Sigma_A} q_loc^i sqrt(gamma) d^3x + (1/M_A)oint_{partial Sigma_A} B_q^{ij} dS_j + O(v^2/c^2)",
            "first exact q_loc-to-observable kernel structure",
            "DERIVED_CONDITIONAL_KERNEL",
            "The map form follows from stress balance, but it is not numeric until zeta_q, q_loc units, body measure, and boundary term are parent-signed.",
        ),
        (
            "COEFF2802_2_eta_difference_kernel",
            "K_eta[AB]",
            "eta_AB = |(zeta_q/g_N)(I_A^i/M_A - I_B^i/M_B) + boundary_AB| with I_A^i=int_{Sigma_A} q_loc^i sqrt(gamma)d^3x",
            "WEP comparison kernel",
            "DERIVED_CONDITIONAL_KERNEL",
            "A universal or zero body moment kills WEP violation; a species-dependent moment makes the branch testable.",
        ),
        (
            "COEFF2802_3_zero_body_moment_condition",
            "Z_body",
            "int_{Sigma_A} q_loc^i sqrt(gamma)d^3x = 0 and oint_{partial Sigma_A} B_q^{ij}dS_j = 0 for every compact local body",
            "exact local invisibility condition for force/WEP channel",
            "CONDITION_EXACT_NOT_PROVED",
            "This is the cleanest route to local GR: prove zero body moments rather than assuming a plateau.",
        ),
        (
            "COEFF2802_4_K_source_block",
            "K_source",
            "epsilon_mu cannot be read from nabla_mu T_m^{mu nu} alone; it needs the 00/Poisson source owner map",
            "source-normalization coefficient",
            "NOT_DERIVED_SOURCE_OWNER_MISSING",
            "The force kernel does not prove that the same charge sources Poisson/Gauss/orbit/clocks.",
        ),
        (
            "COEFF2802_5_K_PPN_block",
            "K_PPN",
            "Delta PPN requires h_mu_nu[q_loc] from the weak-field Green problem and gauge-fixed PPN readout",
            "PPN coefficient",
            "NOT_DERIVED_WEAK_FIELD_MAP_MISSING",
            "Stress-balance alone gives a force residual, not the metric coefficients beta/gamma/alpha_i/xi.",
        ),
        (
            "COEFF2802_6_verdict",
            "first coefficient verdict",
            "K_force[A] kernel is conditionally derived; K_source and K_PPN remain unfilled",
            "route verdict",
            "PARTIAL_SUCCESS_NONCLAIM",
            "Observable-map closure is not dead, but it collapses to zeta_q plus body-moment/boundary-zero proof.",
        ),
    ]
    return [
        {
            "coefficient_id": row[0],
            "symbol": row[1],
            "expression": row[2],
            "observable_role": row[3],
            "status": row[4],
            "interpretation": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_worldtube_rows() -> list[dict[str, Any]]:
    rows = [
        ("WT2802_0_local_balance", "Start from local balance law", "nabla_mu T_m^{mu nu} = f_q^nu", "f_q^nu := zeta_q q_loc^nu + nabla_mu B_q^{mu nu}", "identity form only; zeta_q not sourced"),
        ("WT2802_1_integrate_body", "Integrate spatial component over compact body", "F_A^i = int_{Sigma_A} f_q^i sqrt(gamma)d^3x", "delta a_A^i = F_A^i/M_A", "body measure and M_A owner must be same parent source"),
        ("WT2802_2_boundary_split", "Separate bulk q_loc from boundary flux", "F_A^i = zeta_q I_A^i + Phi_A^i", "I_A^i=int q_loc^i; Phi_A^i=oint B_q^{ij}dS_j", "no-boundary theorem must kill Phi_A^i"),
        ("WT2802_3_wep_condition", "Compare two bodies in same external field", "eta_AB = |delta a_A-delta a_B|/g_N", "species-universal I_A/M_A gives no differential WEP signal", "universality/zero body-moment theorem missing"),
        ("WT2802_4_orbital_condition", "Single-source orbital residual", "delta a_orbit^i = (zeta_q/M_source)I_source^i + Phi_source^i/M_source", "feeds orbital residual if source body moment nonzero", "cannot absorb into measured GM without no-cancellation score"),
        ("WT2802_5_units_condition", "Physical units required", "[zeta_q q_loc] = force density", "K_force units are acceleration per q_loc norm", "q_loc norm convention missing"),
    ]
    return [
        {
            "worldtube_id": row[0],
            "step": row[1],
            "formula": row[2],
            "result": row[3],
            "open_condition": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_source_owner_rows() -> list[dict[str, Any]]:
    rows = [
        ("KS2802_0_same_parent_mass", "same M_A in force kernel and Poisson source", "M_A = int_{Sigma_A} rho_parent sqrt(gamma)d^3x", "not parent-signed", "K_source cannot be claimed"),
        ("KS2802_1_poisson_owner", "same charge sources Poisson/Gauss", "nabla^2 Phi = 4 pi G rho_parent", "not parent-signed", "Newton reduction still conditional"),
        ("KS2802_2_orbit_owner", "same charge sets inverse-square orbital acceleration", "a_r = -G M_parent/r^2 + residual", "not parent-signed", "orbital map cannot score"),
        ("KS2802_3_no_measured_G_absorption", "source hair is not hidden in fitted G or GM", "partial_r,t,A,lambda mu_extra = 0 or row-scored", "policy exists but not scored", "no-cancellation remains guardrail not evidence"),
        ("KS2802_4_K_source_verdict", "K_source derivation", "K_source = 0 only if KS2802_0 through KS2802_3 close", "fail_current_claim", "K_source remains residual budget"),
    ]
    return [
        {
            "source_owner_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "status": row[3],
            "effect_on_K_source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_ppn_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN2802_0_field_equation", "linearized field equation with q_loc source", "L_EH h_mu_nu + L_X h_mu_nu = S_matter + S_q[q_loc]", "MISSING_S_q_OPERATOR", "no K_PPN coefficient"),
        ("PPN2802_1_green_map", "Green map from q_loc to metric perturbation", "h_mu_nu^q(x)=int G_mu_nu,alpha(y;x) q_loc^alpha(y)d^4y", "MISSING_GREEN_FUNCTION", "no gamma/beta/alpha_i/xi readout"),
        ("PPN2802_2_gauge_readout", "PPN gauge and potentials", "h_00,h_0i,h_ij -> gamma,beta,alpha1,alpha2,alpha3,xi", "MISSING_PPN_GAUGE_NORMALIZATION", "preferred-frame rows stay blocked"),
        ("PPN2802_3_source_split", "separate metric source from measured-G/source-normalization", "S_q must not be reabsorbed into G M", "MISSING_NO_ABSORPTION_SCORE", "no local-GR claim"),
        ("PPN2802_4_K_PPN_verdict", "K_PPN derivation", "K_PPN requires PPN2802_0 through PPN2802_3", "fail_current_claim", "K_PPN remains explicit residual budget"),
    ]
    return [
        {
            "ppn_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "status": row[3],
            "effect_on_K_PPN": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_closure_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2802_0_route_survives", "observable-map closure route", "survives narrowly", "K_force[A] kernel was obtained conditionally", "derive zeta_q and zero/universal body moment"),
        ("CL2802_1_not_enough_for_claim", "local-GR/WEP/PPN claim", "blocked", "K_source and K_PPN remain unfilled and K_force lacks normalization", "no claim"),
        ("CL2802_2_best_derivation", "zero body-moment theorem", "best next route", "if I_A^i=Phi_A^i=0 for every compact body, WEP/orbital force residual dies", "prove from q_loc being pure internal superpotential or parent Bianchi zero"),
        ("CL2802_3_bound_fallback", "finite bound route", "fallback", "if body moment is nonzero, source zeta_q, q_loc units, and body profiles for WEP/orbital bounds", "build runner only after real units"),
    ]
    return [
        {
            "closure_id": row[0],
            "route": row[1],
            "decision": row[2],
            "because": row[3],
            "next_action": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2802_0_first_force_kernel", "first q_loc force-kernel structure derived", True, "K_force[A] map form is conditionally derived from stress balance"),
        ("CG2802_1_parent_normalization", "zeta_q is parent-signed and unit-safe", False, "parent normalization and q_loc units are missing"),
        ("CG2802_2_body_moment_zero", "q_loc body moments and boundary flux vanish", False, "zero/universal body-moment theorem is not proved"),
        ("CG2802_3_K_source", "K_source is derived or zero", False, "Poisson/Gauss/orbit/source owner remains unsigned"),
        ("CG2802_4_K_PPN", "K_PPN is derived or zero", False, "weak-field Green map and PPN readout are missing"),
        ("CG2802_5_local_claim", "local GR/WEP/PPN branch can claim pass", False, "normalization, body moment, K_source, and K_PPN gates fail"),
        ("CG2802_6_nonclaim_pack", "2802 nonclaim derivation pack is ready", True, "failure mode and next theorem target are explicit"),
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
        ("DEC2802_0_real_progress", "A real map form was obtained, but not a claim coefficient.", "The force/WEP kernel follows from local stress balance once q_loc is interpreted through zeta_q.", "promote K_force[A] to the next target, not to evidence"),
        ("DEC2802_1_Ksource_Kppn", "K_source and K_PPN are still the GR/Newton blockers.", "Force nonconservation does not by itself prove Poisson source ownership or metric PPN coefficients.", "derive source owner or weak-field Green map next"),
        ("DEC2802_2_no_more_proxy", "Stop trying to score the 7.4e-6 proxy.", "It has no observable units until zeta_q and body measure exist.", "use it only after unit/normalization closure"),
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
            "next_id": "NEXT2802_0_2803",
            "next_target": "2803-Y5-R2FR-q_loc-force-normalization-and-body-moment-zero-theorem-under-AX1090.md",
            "script": "scripts/Y5_R2FR_q_loc_force_normalization_and_body_moment_zero_theorem_under_AX1090_2803.py",
            "objective": "prove zeta_q=0, or prove q_loc body moments/boundary flux vanish universally; if not, source q_loc units and prepare real WEP/orbital force bounds",
            "include": "zeta_q normalization; q_loc units; body integral I_A; boundary flux Phi_A; universality/zero theorem; no measured-G absorption",
            "exclude": "proxy scoring; local-GR/WEP/PPN claim; fitted cancellation; K_source/K_PPN claim without owner/Green map; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["coefficient"], BRANCH_OUTPUTS["coefficient_queue"], "coefficient_queue"),
        (OUTPUTS["worldtube"], BRANCH_OUTPUTS["worldtube_queue"], "worldtube_queue"),
        (OUTPUTS["source_owner"], BRANCH_OUTPUTS["source_owner_queue"], "source_owner_queue"),
        (OUTPUTS["coefficient"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2802_{label}",
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
        ("VAL2802_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all source-register paths exist"),
        ("VAL2802_1_sources_nonempty", all(row["contains_text"] for row in sections["sources"]), "all source-register paths contain text"),
        ("VAL2802_2_force_kernel_present", any(row["coefficient_id"] == "COEFF2802_1_body_acceleration_kernel" and row["status"] == "DERIVED_CONDITIONAL_KERNEL" for row in sections["coefficient"]), "conditional q_loc body-acceleration kernel is present"),
        ("VAL2802_3_verdict_partial_nonclaim", any(row["coefficient_id"] == "COEFF2802_6_verdict" and row["status"] == "PARTIAL_SUCCESS_NONCLAIM" for row in sections["coefficient"]), "2802 verdict is partial success nonclaim"),
        ("VAL2802_4_worldtube_steps_present", len(sections["worldtube"]) >= 6, "worldtube force-map steps are written"),
        ("VAL2802_5_K_source_blocked", any(row["source_owner_id"] == "KS2802_4_K_source_verdict" and row["status"] == "fail_current_claim" for row in sections["source_owner"]), "K_source remains blocked"),
        ("VAL2802_6_K_PPN_blocked", any(row["ppn_id"] == "PPN2802_4_K_PPN_verdict" and row["status"] == "fail_current_claim" for row in sections["ppn"]), "K_PPN remains blocked"),
        ("VAL2802_7_no_proxy_scoring", any(row["decision_id"] == "DEC2802_2_no_more_proxy" for row in sections["decision"]), "proxy-scoring refusal is recorded"),
        ("VAL2802_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2802_9_next_target_2803", any(row["next_id"] == "NEXT2802_0_2803" for row in sections["next"]), "next target is 2803"),
        ("VAL2802_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2802_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2802_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2802_13_cited_paths_exist", cited_paths_exist(sections), "all cited copy/source paths in generated rows exist"),
        ("VAL2802_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2802_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2802_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2802_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2802_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2802 derives a conditional q_loc worldtube force kernel, keeps K_source/K_PPN blocked, refuses proxy scoring, and selects zeta_q/body-moment zero as 2803.",
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
        "# 2802 - Y5 R2FR First Real q_loc Observable Coefficient Or Y5 Source Owner Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2802 gets a real piece of structure, but not yet a claimable coefficient.",
        "",
        "The first usable map is the worldtube force kernel: if the retained residual enters local stress balance as `nabla_mu T_m^{mu nu} = zeta_q q_loc^nu + nabla_mu B_q^{mu nu}`, then a compact body gets `delta a_A^i = (zeta_q/M_A) int q_loc^i + boundary/M_A` at leading local order.",
        "",
        "That is progress because it says exactly how `q_loc` would become WEP/orbital physics. It also says exactly how local GR is recovered: prove `zeta_q=0`, or prove every compact-body moment and boundary flux of `q_loc` vanishes/universalizes.",
        "",
        "But `K_source` and `K_PPN` still do not close. The force kernel does not prove Poisson/Gauss/orbit source ownership, and it does not solve the weak-field metric Green problem. So there is no local-GR, WEP, PPN, orbital, or source-normalization claim from 2802.",
        "",
        "## First Observable Coefficient Derivation",
        markdown_table(sections["coefficient"], ["coefficient_id", "symbol", "expression", "status", "interpretation"]),
        "",
        "## Worldtube Force Map",
        markdown_table(sections["worldtube"], ["worldtube_id", "step", "formula", "result", "open_condition"]),
        "",
        "## K_source Owner Attempt",
        markdown_table(sections["source_owner"], ["source_owner_id", "claim_piece", "mathematical_form", "status", "effect_on_K_source"]),
        "",
        "## K_PPN Attempt",
        markdown_table(sections["ppn"], ["ppn_id", "claim_piece", "mathematical_form", "status", "effect_on_K_PPN"]),
        "",
        "## Closure Or Bound Decision",
        markdown_table(sections["closure"], ["closure_id", "route", "decision", "because", "next_action"]),
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
        "coefficient": build_coefficient_rows(),
        "worldtube": build_worldtube_rows(),
        "source_owner": build_source_owner_rows(),
        "ppn": build_ppn_rows(),
        "closure": build_closure_rows(),
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
