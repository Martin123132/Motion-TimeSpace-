from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2855-Y5-R2FR-parent-source-equation-draft-or-user-source-request-under-AX1090.md"

SRC_2854_DOC = ROOT / "2854-Y5-R2FR-first-real-amplitude-source-acquisition-or-blocker-ledger-under-AX1090.md"
SRC_2854_REQUEST = RESIDUALS / "P8_Y5_R2FR_2854_SOURCE_REQUEST_PACK.csv"
SRC_2854_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"
SRC_2854_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2854_VALIDATION.csv"
SRC_2853_REENTRY = RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv"
SRC_2853_RUNNER = RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv"
SRC_2846_FORMULA = RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_1882_SIGMAR = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_SIGMAR_NO_CIRCULARITY_MAP.csv"
SRC_1882_REFUSAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1882_RUNNER_REFUSAL.csv"
SRC_509 = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
SRC_510 = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2855_SOURCE_REGISTER.csv",
    "equations": RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_2855_DERIVATION_STATUS_MATRIX.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2855_USER_SOURCE_REQUEST_LEDGER.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2855_PARENT_ACTION_REENTRY_CONTRACT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2855_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2855_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2855_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2855_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2855_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "draft_copy": LOCAL_BOUNDS / "RAB_PARENT_SOURCE_EQUATION_DRAFT_2855_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_USER_SOURCE_REQUEST_LEDGER_2855_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2855_parent_equation_variational_consistency_NEXT.csv",
    "reentry_copy": BETA_DOCS / "RAB_PARENT_ACTION_REENTRY_CONTRACT_2855_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2855_0_2854_doc", SRC_2854_DOC, "NEXT2854_0_2855;VAL2854_OVERALL", "2854 handoff and validation"),
        ("SRC2855_1_2854_request", SRC_2854_REQUEST, "REQ2854_0_parent_equations;REQ2854_5_GM_glue", "source request pack"),
        ("SRC2855_2_2854_blockers", SRC_2854_BLOCKERS, "BLOCK2854_0_Q_CAB;BLOCK2854_6_full_vector", "blocker ledger"),
        ("SRC2855_3_2854_scan", SRC_2854_SCAN, "SCAN2854_0_Q_CAB;SCAN2854_5_GM", "real source acquisition scan"),
        ("SRC2855_4_2854_validation", SRC_2854_VALIDATION, "VAL2854_OVERALL", "2854 validation"),
        ("SRC2855_5_2853_reentry", SRC_2853_REENTRY, "RE2853_0_parent_source_equation;RE2853_2_GM_glue", "parent action reentry hook"),
        ("SRC2855_6_2853_runner", SRC_2853_RUNNER, "REFUSED_MISSING_PROVENANCE_OR_INPUTS", "strict runner refusal"),
        ("SRC2855_7_2846_formula", SRC_2846_FORMULA, "FORM2846_0_A_total;FORM2846_4_finite_score_rule", "A_total formula and scoring rule"),
        ("SRC2855_8_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2855_9_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM", "parent amplitude contract"),
        ("SRC2855_10_1882_sigmar", SRC_1882_SIGMAR, "SNCM1882_1_generalized_gamma;LINEAR_BOUND_FORM_NONCLAIM", "sigma/b_R symbolic no-circularity map"),
        ("SRC2855_11_1882_refusal", SRC_1882_REFUSAL, "RUN1882_0_combo_gamma_runner;REFUSE_CLAIM_RUN", "gamma-combo runner refusal"),
        ("SRC2855_12_509", SRC_509, "T509_0_charge_identity_needed;T509_2_no_extra_mass_channel", "source-measure theorem"),
        ("SRC2855_13_510", SRC_510, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube source measure theorem"),
        ("SRC2855_14_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full PPN vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def equation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PEQ2855_0_CAB_source",
            "target-map amplitude",
            "L_CAB C_AB = J_CAB; Q_CAB = integral_W J_CAB dV + surface_integral_boundary B_CAB",
            "Q_CAB, C_AB, L_CAB, J_CAB, B_CAB",
            "defines the finite target-map monopole that feeds A_total",
            "DRAFT_EQUATION_NOT_PARENT_DERIVED",
            "parent L_CAB; J_CAB source functional; boundary/corner policy; charge units",
            "PACK2844_0_Q_CAB;PACK2844_1_J_CAB;PACK2844_2_L_CAB",
        ),
        (
            "PEQ2855_1_R_source",
            "residual curvature amplitude",
            "L_R delta_R = J_R; q_R_eff = integral_W J_R dV + surface_integral_boundary B_R",
            "delta_R, L_R, J_R, q_R_eff, B_R",
            "defines the finite curvature-side Green charge in the same convention as Q_CAB",
            "DRAFT_EQUATION_NOT_PARENT_DERIVED",
            "parent L_R; J_R source functional; Green normalization; boundary policy",
            "PACK2844_4_q_R_eff;CONTRACT2844_0_operator",
        ),
        (
            "PEQ2855_2_sigma_sign",
            "operator sign",
            "S_R^(2) = 1/2 <delta_R, L_R delta_R>; sigma_R = sign(G_R) in the chosen Green convention",
            "sigma_R, L_R, G_R",
            "fixes the sign that decides whether Q_CAB and q_R_eff can cancel",
            "DRAFT_SIGN_REQUEST_NOT_DERIVED",
            "quadratic parent action; Green kernel convention; metric/signature convention",
            "CONTRACT2844_5_sign",
        ),
        (
            "PEQ2855_3_amp_current_identity",
            "shared amplitude current",
            "J_CAB + sigma_R J_R = dK_amp and surface_integral_boundary (K_amp + B_CAB + sigma_R B_R) = 0 => Q_CAB + sigma_R q_R_eff = 0",
            "J_CAB, J_R, K_amp, B_CAB, B_R, sigma_R",
            "this is the clean derivation target for theorem-zero A_total rather than a fitted cancellation",
            "DERIVATION_ATTEMPT_REQUIRES_PARENT_IDENTITY",
            "Noether/Bianchi/gauge identity that owns K_amp; boundary silence theorem; no independent source rescaling",
            "CONTRACT2844_1_source_current;RE2853_0_parent_source_equation",
        ),
        (
            "PEQ2855_4_bR_no_shadow",
            "no-shadow or finite b_R",
            "b_R = d ln(A_R)/dC_R | exterior_background, or b_R = 0 from a parent no-shadow theorem",
            "b_R, A_R, C_R",
            "controls whether the gamma lane can leak into a Weyl/log-coframe shadow channel",
            "DRAFT_ALTERNATIVE_REQUEST_NOT_DERIVED",
            "finite b_R source row or parent theorem excluding representative shadow dependence",
            "SNCM1882_1_generalized_gamma;RUN1882_0_combo_gamma_runner",
        ),
        (
            "PEQ2855_5_tail_profile",
            "regular/tail profile",
            "P_arena[C_AB_reg + H_R] = epsilon_tail(arena), with epsilon_tail = 0 by projection theorem or bounded by sourced profile",
            "C_AB_reg, H_R, P_arena, epsilon_tail",
            "prevents homogeneous/tail terms from imitating the 1/r residual in local arenas",
            "DRAFT_PROJECTION_REQUEST_NOT_DERIVED",
            "tail profile; range hierarchy; arena projection; boundary conditions",
            "PACK2844_5_tail_bound;CONTRACT2844_3_regular_tail",
        ),
        (
            "PEQ2855_6_GM_glue",
            "measured-GM source measure",
            "M_source[W] = H_tau[S_outer] - H_tau[ref]; g_00 = -1 + 2 G_ref M_source/r + O(r^-2)",
            "M_source, H_tau, G_ref, g_00",
            "ties the internal source charge to the measured Newtonian potential rather than an arbitrary normalization",
            "CONDITIONAL_DRAFT_FROM_T509_T510",
            "worldtube/Hamiltonian charge equality; no extra mass channel; weak-field metric readout",
            "T509_0_charge_identity_needed;T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout",
        ),
        (
            "PEQ2855_7_full_ppn_vector",
            "full local residual vector",
            "R_PPN = (gamma-1, beta-1, alpha_1, alpha_2, alpha_3, xi, zeta_i, clock, orbital, q_loc) evaluated in one branch",
            "gamma, beta, alpha_i, xi, zeta_i, clock, orbital, q_loc",
            "prevents a gamma-only success from being mistaken for local GR/Newton reduction",
            "SCHEMA_REQUEST_NOT_DERIVED",
            "all non-gamma channels in same convention and branch",
            "PPNV2631_8_total_abs;RG2631_0_no_gamma_only",
        ),
    ]
    return [
        nonclaim(
            {
                "equation_id": equation_id,
                "sector": sector,
                "draft_equation": equation,
                "variables": variables,
                "why_needed": why,
                "status": status,
                "missing_parent_clauses": missing,
                "source_anchors": anchors,
                "derivation_attempt": "DERIVATION" in status or equation_id == "PEQ2855_3_amp_current_identity",
                "request_for_user_source": True,
                "parent_accepted": False,
                "numeric_ready": False,
                "theorem_zero_ready": False,
                "control_only": True,
            }
        )
        for equation_id, sector, equation, variables, why, status, missing, anchors in specs
    ]


def status_rows(equations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in equations:
        rows.append(
            nonclaim(
                {
                    "status_id": row["equation_id"].replace("PEQ", "STAT"),
                    "equation_id": row["equation_id"],
                    "parent_derived": False,
                    "finite_numeric_row": False,
                    "source_path_grade": "draft_anchor_only",
                    "can_feed_2853_runner": False,
                    "why_blocked": row["missing_parent_clauses"],
                    "next_resolution": "derive parent identity/action clause or supply exact source path/equation anchor",
                    "control_only": True,
                }
            )
        )
    return rows


def request_rows() -> list[dict[str, Any]]:
    specs = [
        ("USR2855_0_parent_action", "parent action", "action terms whose Euler-Lagrange equations produce L_CAB C_AB and L_R delta_R", "must include signs, measures, fields, boundary terms, and gauge/quotient assumptions"),
        ("USR2855_1_current_identity", "shared current identity", "Noether/Bianchi/gauge line deriving J_CAB + sigma_R J_R = dK_amp", "must not be imposed as a closure axiom or fitted ratio"),
        ("USR2855_2_charge_integrals", "charge integrals", "explicit Q_CAB and q_R_eff integrals in one convention", "must include units and boundary/corner terms"),
        ("USR2855_3_sigma", "sigma_R convention", "operator/Green sign deciding sigma_R", "must specify metric signature and Green-function orientation"),
        ("USR2855_4_bR_tail", "b_R/tail", "finite b_R or no-shadow theorem plus tail/projection bound", "must cover local PPN arenas"),
        ("USR2855_5_GM", "measured-GM glue", "worldtube source charge equals weak-field metric mass", "must close no-extra-mass-channel premise"),
        ("USR2855_6_full_vector", "full PPN vector", "same-branch beta/preferred/source/endpoint/clock/orbital/q_loc residuals", "must be finite or theorem-zero before any local-GR claim"),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "needed_source": needed,
                "minimum_content": content,
                "acceptance_rule": rule,
                "status": "OPEN_SOURCE_REQUEST",
                "control_only": True,
            }
        )
        for request_id, needed, content, rule in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2855_0_variational_identity", "parent source equations imply current identity", "reopen theorem-zero route for Q_CAB + sigma_R q_R_eff", "requires PEQ2855_3 from variational symmetry rather than closure insertion"),
        ("RE2855_1_finite_runner", "finite numeric/source rows supplied", "feed 2853 strict runner", "requires source-backed Q_CAB, q_R_eff, sigma_R, b_R, tail, GM and full vector"),
        ("RE2855_2_GM_branch", "T509/T510 charge glue closes", "normalize PPN amplitude against measured GM", "requires worldtube charge and metric readout in same branch"),
        ("RE2855_3_no_shadow_branch", "b_R=0 or finite b_R sourced", "remove Weyl/log-coframe ambiguity", "requires parent no-shadow theorem or exact finite row"),
    ]
    return [
        nonclaim(
            {
                "reentry_id": reentry_id,
                "trigger": trigger,
                "effect": effect,
                "required_evidence": required,
                "status": "OPEN_REENTRY_NOT_ACTIVE",
                "control_only": True,
            }
        )
        for reentry_id, trigger, effect, required in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2855_0_source_paths", "all cited source paths and anchors exist", "CONTROL_PASS_ONLY", "source register validates previous checkpoint inputs"),
        ("CG2855_1_parent_identity", "J_CAB + sigma_R J_R = dK_amp is parent-derived", "BLOCKED", "identity is drafted but not derived"),
        ("CG2855_2_zero_theorem", "Q_CAB + sigma_R q_R_eff = 0 claimed", "BLOCKED", "boundary theorem and parent identity absent"),
        ("CG2855_3_finite_runner", "2853 strict runner can score", "BLOCKED", "no numeric/source-backed rows yet"),
        ("CG2855_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "GM glue and full PPN vector remain open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2855_0_draft", "Parent source-equation draft written.", "COMPLETE_NONCLAIM", "we now have the exact equations that would populate the missing amplitude rows"),
        ("DEC2855_1_derivation", "The only attractive zero route is the shared amplitude-current identity.", "SELECTED_FOR_TEST", "it would derive Q_CAB + sigma_R q_R_eff = 0 without tuning if owned by a variational parent action"),
        ("DEC2855_2_no_claim", "No local-GR/Newton/R10/PPN claim is made.", "LOCKED", "all source equations are drafts or requests, not accepted parent derivations"),
        ("DEC2855_3_next", "Next target is variational consistency of the current identity.", "SELECTED_2856", "prove it from action/gauge structure or reject it as inserted closure"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2855_0_2856",
                "status": "selected_primary",
                "target_doc": "2856-Y5-R2FR-amp-current-continuity-variational-consistency-or-reject-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_amp_current_continuity_variational_consistency_or_reject_under_AX1090_2856.py",
                "mission": "test whether J_CAB + sigma_R J_R = dK_amp can arise from a variational parent action or gauge identity without being inserted as a closure constraint; if not, retain finite-source fallback and source-request route",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2855_0_draft", OUTPUTS["equations"], BRANCH_OUTPUTS["draft_copy"], "parent source-equation draft nonclaim copy"),
        ("COPY2855_1_request", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "user/source request ledger nonclaim copy"),
        ("COPY2855_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2856"),
        ("COPY2855_3_reentry", OUTPUTS["reentry"], BRANCH_OUTPUTS["reentry_copy"], "parent action reentry contract nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "parent_accepted",
        "numeric_ready",
        "theorem_zero_ready",
        "parent_derived",
        "finite_numeric_row",
        "can_feed_2853_runner",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2855_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2855_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2855_2_equation_count", len(rows_by_name["equations"]) >= 8, "draft equation table includes all required source equations"),
        ("VAL2855_3_no_parent_accepted", not any(row["parent_accepted"] for row in rows_by_name["equations"]), "no drafted equation is marked parent-accepted"),
        ("VAL2855_4_requests_complete", len(rows_by_name["requests"]) >= 7, "user/source request ledger covers all missing rows"),
        ("VAL2855_5_reentry_contract", len(rows_by_name["reentry"]) >= 4, "parent-action reentry contract is present"),
        ("VAL2855_6_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2855_7_next_target_2856", any(row["next_id"] == "NEXT2855_0_2856" and row["selected"] for row in rows_by_name["next"]), "2856 variational consistency test selected"),
        ("VAL2855_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2855_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2855_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2855_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2855_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2855_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2855_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2855_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2855_OVERALL",
            "passed": overall,
            "detail": "2855 drafts the exact parent source equations needed for the finite amplitude/local-GR bridge, keeps them nonclaim, and selects the variational identity test for 2856.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2855 - Y5 R2FR Parent Source Equation Draft Or User Source Request Under AX1090

Status: `Y5_R2FR_2855_parent_source_equation_draft_nonclaim_variational_identity_selected`

## Private Verdict

2855 does not prove local GR yet. It sharpens the missing coupling/amplitude problem into a concrete parent-equation contract.

The best leap-forward target is not another fitted number. It is the current identity:

`J_CAB + sigma_R J_R = dK_amp`

If that identity comes from the parent variational structure, and if the boundary term is silent, then `Q_CAB + sigma_R q_R_eff = 0` follows as a theorem-level cancellation. If it has to be inserted by hand, the route stays closure-only and we fall back to finite source rows.

So the project is not stuck in fog here. It has a precise fork: derive the amplitude-current identity from the action, or reject it and keep the local branch as finite-source/source-request work.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Parent Source Equation Draft

{markdown_table(rows["equations"], ["equation_id", "sector", "draft_equation", "status", "missing_parent_clauses", "parent_accepted", "valid_for_claim"])}

## Derivation Status Matrix

{markdown_table(rows["status"], ["status_id", "equation_id", "parent_derived", "finite_numeric_row", "can_feed_2853_runner", "why_blocked", "valid_for_claim"])}

## User Source Request Ledger

{markdown_table(rows["requests"], ["request_id", "needed_source", "minimum_content", "acceptance_rule", "status", "valid_for_claim"])}

## Parent Action Reentry Contract

{markdown_table(rows["reentry"], ["reentry_id", "trigger", "effect", "required_evidence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["equations"] = equation_rows()
    rows["status"] = status_rows(rows["equations"])
    rows["requests"] = request_rows()
    rows["reentry"] = reentry_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "equations", "status", "requests", "reentry", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2855_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2855_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
