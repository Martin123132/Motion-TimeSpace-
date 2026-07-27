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

DOC = ROOT / "2856-Y5-R2FR-amp-current-continuity-variational-consistency-or-reject-under-AX1090.md"

SRC_2855_DOC = ROOT / "2855-Y5-R2FR-parent-source-equation-draft-or-user-source-request-under-AX1090.md"
SRC_2855_SOURCES = RESIDUALS / "P8_Y5_R2FR_2855_SOURCE_REGISTER.csv"
SRC_2855_EQUATIONS = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2855_STATUS = RESIDUALS / "P8_Y5_R2FR_2855_DERIVATION_STATUS_MATRIX.csv"
SRC_2855_REENTRY = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_ACTION_REENTRY_CONTRACT.csv"
SRC_2855_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2855_USER_SOURCE_REQUEST_LEDGER.csv"
SRC_2855_CLAIM_GATES = RESIDUALS / "P8_Y5_R2FR_2855_CLAIM_GATES.csv"
SRC_2855_NEXT = RESIDUALS / "P8_Y5_R2FR_2855_NEXT_TARGET.csv"
SRC_2855_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2855_VALIDATION.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2853_REENTRY = RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2856_SOURCE_REGISTER.csv",
    "noether": RESIDUALS / "P8_Y5_R2FR_2856_NOETHER_DERIVATION_ATTEMPT.csv",
    "clauses": RESIDUALS / "P8_Y5_R2FR_2856_VARIATIONAL_CLAUSE_AUDIT.csv",
    "candidates": RESIDUALS / "P8_Y5_R2FR_2856_SYMMETRY_CANDIDATE_AUDIT.csv",
    "conditional": RESIDUALS / "P8_Y5_R2FR_2856_CONDITIONAL_THEOREM.csv",
    "obstructions": RESIDUALS / "P8_Y5_R2FR_2856_OBSTRUCTION_LEDGER.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2856_SOURCE_REQUEST_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2856_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2856_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2856_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2856_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2856_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "conditional_copy": LOCAL_BOUNDS / "RAB_AMP_CURRENT_CONDITIONAL_THEOREM_2856_NONCLAIM.csv",
    "obstruction_copy": SOURCE_WEIGHT / "RAB_VARIATIONAL_IDENTITY_OBSTRUCTION_LEDGER_2856_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2856_vertical_generator_or_reject_NEXT.csv",
    "request_copy": BETA_DOCS / "RAB_VARIATIONAL_IDENTITY_SOURCE_REQUEST_2856_NONCLAIM.csv",
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
        ("SRC2856_0_2855_doc", SRC_2855_DOC, "J_CAB + sigma_R J_R = dK_amp;NEXT2855_0_2856;VAL2855_OVERALL", "2855 private verdict and handoff"),
        ("SRC2856_1_2855_sources", SRC_2855_SOURCES, "SRC2855_0_2854_doc;SRC2855_14_2631", "2855 source register"),
        ("SRC2856_2_2855_equations", SRC_2855_EQUATIONS, "PEQ2855_3_amp_current_identity;DERIVATION_ATTEMPT_REQUIRES_PARENT_IDENTITY", "identity draft"),
        ("SRC2856_3_2855_status", SRC_2855_STATUS, "STAT2855_3_amp_current_identity", "derivation status"),
        ("SRC2856_4_2855_reentry", SRC_2855_REENTRY, "RE2855_0_variational_identity;RE2855_1_finite_runner", "parent action reentry contract"),
        ("SRC2856_5_2855_requests", SRC_2855_REQUESTS, "USR2855_1_current_identity;USR2855_0_parent_action", "source request ledger"),
        ("SRC2856_6_2855_claims", SRC_2855_CLAIM_GATES, "CG2855_1_parent_identity;CG2855_4_local_GR_Newton", "blocked claim gates"),
        ("SRC2856_7_2855_next", SRC_2855_NEXT, "NEXT2855_0_2856", "2856 selected"),
        ("SRC2856_8_2855_validation", SRC_2855_VALIDATION, "VAL2855_OVERALL", "2855 validation"),
        ("SRC2856_9_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "earlier current/sign contract"),
        ("SRC2856_10_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "amplitude source pack"),
        ("SRC2856_11_2853_reentry", SRC_2853_REENTRY, "RE2853_0_parent_source_equation;RE2853_1_symmetry_owner", "earlier theorem reentry hook"),
        ("SRC2856_12_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full-vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def noether_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NDR2856_0_parent_variation",
            "Assume a parent action S[Phi,psi] and an infinitesimal vertical transformation delta_epsilon Phi = R[Phi] epsilon.",
            "delta S = integral (E_C delta C_AB + E_R delta delta_R + E_psi delta psi) + boundary(theta_epsilon)",
            "standard variational identity template",
            "CONDITIONAL_FORMAL_STEP",
            "requires actual parent action, field space, and vertical generator",
        ),
        (
            "NDR2856_1_noether_identity",
            "If the transformation is an exact gauge/quotient symmetry, the Euler-Lagrange terms obey an off-shell Noether identity.",
            "R_C^dagger E_C + R_R^dagger E_R + R_psi^dagger E_psi = dN_epsilon",
            "gives the only clean route to a current-continuity identity",
            "CONDITIONAL_FORMAL_STEP",
            "requires symmetry to be parent-signed, not inferred from desired cancellation",
        ),
        (
            "NDR2856_2_linear_source_split",
            "In the exterior linear branch write E_C = L_CAB C_AB - J_CAB and E_R = L_R delta_R - J_R.",
            "R_C^dagger J_CAB + R_R^dagger J_R = R_C^dagger L_CAB C_AB + R_R^dagger L_R delta_R - dN_epsilon",
            "connects source currents to kinetic/operator side",
            "CONDITIONAL_FORMAL_STEP",
            "requires source split and common convention from 2855",
        ),
        (
            "NDR2856_3_required_generator",
            "The target identity needs the generator coefficients to reduce to R_C^dagger = 1 and R_R^dagger = sigma_R in the local amplitude channel.",
            "J_CAB + sigma_R J_R = dK_amp",
            "fixes the exact generator ratio needed for theorem-zero amplitude cancellation",
            "NOT_PROVEN_CURRENT_CORPUS",
            "missing source for the vertical generator and its sigma_R sign convention",
        ),
        (
            "NDR2856_4_boundary_reduction",
            "If K_amp plus the C/R boundary fluxes has zero worldtube boundary integral, the charge identity follows.",
            "surface_integral_boundary(K_amp + B_CAB + sigma_R B_R) = 0 => Q_CAB + sigma_R q_R_eff = 0",
            "turns differential identity into integrated amplitude theorem",
            "NOT_PROVEN_CURRENT_CORPUS",
            "missing boundary/corner silence theorem",
        ),
    ]
    return [
        nonclaim(
            {
                "step_id": step_id,
                "assumption_or_step": assumption,
                "formal_expression": expression,
                "role": role,
                "status": status,
                "missing_evidence": missing,
                "accepted_derivation_step": status == "CONDITIONAL_FORMAL_STEP",
                "parent_signed": False,
                "control_only": True,
            }
        )
        for step_id, assumption, expression, role, status, missing in specs
    ]


def clause_rows() -> list[dict[str, Any]]:
    specs = [
        ("CLAUSE2856_0_parent_action", "parent action exists with C_AB and delta_R in same variational branch", "REQUIRED", "OPEN", "no parent action source term supplied"),
        ("CLAUSE2856_1_vertical_generator", "vertical generator has amplitude-channel adjoint coefficients (1, sigma_R)", "REQUIRED", "OPEN", "generator not sourced"),
        ("CLAUSE2856_2_noether_identity", "symmetry is exact enough to produce an off-shell or controlled on-shell identity", "REQUIRED", "OPEN", "Noether/Bianchi owner not shown"),
        ("CLAUSE2856_3_source_split", "E_C and E_R split into operator minus source currents in one convention", "REQUIRED", "PARTIAL_DRAFT", "2855 drafted split but did not derive/source it"),
        ("CLAUSE2856_4_operator_side", "kinetic/operator contribution becomes an exact divergence or cancels in amplitude projection", "REQUIRED", "OPEN", "operator relation not proven"),
        ("CLAUSE2856_5_boundary_silence", "worldtube boundary/corner flux of K_amp plus B terms vanishes or is included", "REQUIRED", "OPEN", "boundary theorem missing"),
        ("CLAUSE2856_6_no_rescaling", "no independent rescaling of J_CAB and J_R is allowed", "REQUIRED", "OPEN", "source normalization owner missing"),
        ("CLAUSE2856_7_full_vector_guard", "identity must sit inside full local vector closure, not gamma-only", "REQUIRED_FOR_LOCAL_GR", "OPEN", "full PPN vector still unfilled"),
    ]
    return [
        nonclaim(
            {
                "clause_id": clause_id,
                "clause": clause,
                "necessity": necessity,
                "status": status,
                "blocker": blocker,
                "clause_closed": False,
                "control_only": True,
            }
        )
        for clause_id, clause, necessity, status, blocker in specs
    ]


def candidate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SYM2856_0_noether_doublet",
            "Noether doublet/quotient symmetry mixing the C_AB and delta_R amplitude channels",
            "could derive J_CAB + sigma_R J_R = dK_amp if generator ratio and boundary theorem are sourced",
            "BEST_ROUTE_NOT_YET_PROVEN",
            "missing parent generator and action",
            False,
        ),
        (
            "SYM2856_1_bianchi_projection",
            "Bianchi/descent projection where the combined amplitude source is an exact projected divergence",
            "could work if C_AB and delta_R are both descendants of one geometric object",
            "POSSIBLE_BUT_UNSOURCED",
            "missing descent map and projection algebra",
            False,
        ),
        (
            "SYM2856_2_auxiliary_constraint",
            "Auxiliary multiplier imposing J_CAB + sigma_R J_R = dK_amp",
            "reproduces equation but smells like closure insertion unless multiplier is independently required",
            "REJECT_AS_PRIMARY",
            "would be an inserted constraint without independent parent reason",
            False,
        ),
        (
            "SYM2856_3_source_rescaling",
            "Choose source normalizations so Q_CAB = -sigma_R q_R_eff",
            "gets cancellation but is tunable and not a derivation",
            "REJECT",
            "independent rescaling violates no-tuning requirement",
            False,
        ),
        (
            "SYM2856_4_finite_fallback",
            "Do not prove identity; source finite Q_CAB, q_R_eff, sigma_R and score the residual",
            "scientifically safe fallback if symmetry proof fails",
            "RETAIN_AS_FALLBACK",
            "requires real finite/source-backed rows",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "candidate_id": candidate_id,
                "candidate": candidate,
                "could_help_by": could_help,
                "status": status,
                "why_not_closed": why,
                "selected_as_claim_route": selected,
                "control_only": True,
            }
        )
        for candidate_id, candidate, could_help, status, why, selected in specs
    ]


def conditional_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CT2856_0_conditional_lemma",
            "If a parent action has an exact vertical symmetry whose amplitude-channel adjoint generator is (1, sigma_R), and if the operator side is an exact divergence dK_amp, then J_CAB + sigma_R J_R = dK_amp.",
            "conditional lemma only",
            "NOT_CLAIMED",
        ),
        (
            "CT2856_1_integrated_corollary",
            "If additionally surface_integral_boundary(K_amp + B_CAB + sigma_R B_R)=0, then Q_CAB + sigma_R q_R_eff = 0 and the leading A_total amplitude vanishes.",
            "conditional integrated corollary",
            "NOT_CLAIMED",
        ),
        (
            "CT2856_2_rejection_condition",
            "If no parent action/generator/descent map can be sourced, the identity is closure-only and must not be used as a proof of local GR.",
            "rejection rule",
            "ACTIVE_GUARD",
        ),
    ]
    return [
        nonclaim(
            {
                "conditional_id": conditional_id,
                "statement": statement,
                "kind": kind,
                "status": status,
                "parent_proven": False,
                "usable_for_claim": False,
                "control_only": True,
            }
        )
        for conditional_id, statement, kind, status in specs
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS2856_0_generator", "MISSING_VERTICAL_GENERATOR", "need explicit transformation that maps C_AB/delta_R into the required amplitude doublet", "blocks theorem-zero identity"),
        ("OBS2856_1_action", "MISSING_PARENT_ACTION_OWNER", "need action terms whose variation yields the two source equations", "blocks Noether derivation"),
        ("OBS2856_2_operator", "MISSING_OPERATOR_DIVERGENCE", "need L_CAB and L_R relation that leaves dK_amp rather than arbitrary remainder", "blocks differential identity"),
        ("OBS2856_3_boundary", "MISSING_BOUNDARY_SILENCE", "need worldtube/corner theorem or included boundary charge", "blocks integrated Q identity"),
        ("OBS2856_4_sign", "MISSING_SIGMA_R_SIGN_OWNER", "need parent Green sign convention, not chosen post hoc", "blocks sign-stable cancellation"),
        ("OBS2856_5_full_vector", "MISSING_FULL_VECTOR_CLOSURE", "need beta/preferred/source/endpoint/clock/orbital/q_loc closure", "blocks local-GR claim even if gamma amplitude cancels"),
    ]
    return [
        nonclaim(
            {
                "obstruction_id": obstruction_id,
                "code": code,
                "needed_resolution": resolution,
                "blocks": blocks,
                "resolved": False,
                "control_only": True,
            }
        )
        for obstruction_id, code, resolution, blocks in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2856_0_generator", "vertical generator", "exact line/source showing delta C_AB and delta delta_R with coefficient ratio (1, sigma_R)"),
        ("REQ2856_1_action", "parent action", "action terms and variations producing L_CAB C_AB=J_CAB and L_R delta_R=J_R"),
        ("REQ2856_2_noether", "Noether/Bianchi identity", "off-shell or controlled on-shell identity that yields the source-current divergence"),
        ("REQ2856_3_boundary", "boundary theorem", "worldtube/corner flux cancellation or included charge definition"),
        ("REQ2856_4_fallback_rows", "finite fallback rows", "source-backed Q_CAB, q_R_eff, sigma_R, b_R, tail, GM, and full-vector rows if proof fails"),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "needed_source": needed,
                "minimum_content": content,
                "status": "OPEN_SOURCE_REQUEST",
                "accepted_only_if": "exact source path plus equation/table anchor plus convention; no closure-only insertion",
                "control_only": True,
            }
        )
        for request_id, needed, content in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2856_0_conditional_math", "conditional Noether lemma drafted", "PASS_CONTROL_ONLY", "formal conditional derivation route is explicit"),
        ("CG2856_1_parent_generator", "vertical generator source exists", "BLOCKED", "no generator source supplied"),
        ("CG2856_2_current_identity", "J_CAB + sigma_R J_R = dK_amp proven", "BLOCKED", "identity remains conditional"),
        ("CG2856_3_integrated_zero", "Q_CAB + sigma_R q_R_eff = 0 proven", "BLOCKED", "boundary silence theorem absent"),
        ("CG2856_4_local_GR", "local GR/Newton reduction claimed", "BLOCKED", "full vector and GM glue remain open"),
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
        ("DEC2856_0_result", "Variational route is mathematically coherent as a conditional lemma.", "CONDITIONAL_ONLY", "Noether identity can yield the desired current relation if the exact parent generator exists"),
        ("DEC2856_1_not_proven", "The route is not closed in the current corpus.", "NOT_CLAIMED", "generator/action/operator/boundary owners are still missing"),
        ("DEC2856_2_best_route", "The best next attack is to find or construct the vertical generator.", "SELECTED_2857", "without it the identity is just a closure axiom wearing a nice hat"),
        ("DEC2856_3_fallback", "Finite-source fallback remains active.", "RETAINED", "if generator hunt fails, score real finite rows rather than using theorem-zero"),
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
                "next_id": "NEXT2856_0_2857",
                "status": "selected_primary",
                "target_doc": "2857-Y5-R2FR-vertical-generator-source-hunt-or-minimal-action-construction-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_vertical_generator_source_hunt_or_minimal_action_construction_under_AX1090_2857.py",
                "mission": "hunt for an existing parent vertical generator or construct a minimal non-claim action ansatz whose symmetry could derive J_CAB + sigma_R J_R = dK_amp; reject the theorem-zero route if the generator is tunable or inserted",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2856_0_conditional", OUTPUTS["conditional"], BRANCH_OUTPUTS["conditional_copy"], "conditional theorem nonclaim copy"),
        ("COPY2856_1_obstructions", OUTPUTS["obstructions"], BRANCH_OUTPUTS["obstruction_copy"], "obstruction ledger nonclaim copy"),
        ("COPY2856_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2857"),
        ("COPY2856_3_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "source request copy"),
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
        "parent_signed",
        "clause_closed",
        "selected_as_claim_route",
        "parent_proven",
        "usable_for_claim",
        "resolved",
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
        ("VAL2856_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2856_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2856_2_noether_steps", len(rows_by_name["noether"]) >= 5, "Noether derivation attempt has required steps"),
        ("VAL2856_3_required_clauses_open", any(row["status"] == "OPEN" for row in rows_by_name["clauses"]), "required proof clauses remain explicitly open"),
        ("VAL2856_4_conditional_not_claimed", not any(row["usable_for_claim"] for row in rows_by_name["conditional"]), "conditional theorem is not usable for claim"),
        ("VAL2856_5_obstructions_present", len(rows_by_name["obstructions"]) >= 6, "obstruction ledger covers generator/action/operator/boundary/sign/full-vector"),
        ("VAL2856_6_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2856_7_next_target_2857", any(row["next_id"] == "NEXT2856_0_2857" and row["selected"] for row in rows_by_name["next"]), "2857 vertical generator hunt selected"),
        ("VAL2856_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2856_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2856_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2856_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2856_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2856_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2856_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2856_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2856_OVERALL",
            "passed": overall,
            "detail": "2856 derives a conditional Noether route for the amplitude-current identity, refuses theorem-zero/local-GR claims, and selects a vertical-generator hunt for 2857.",
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
    content = f"""# 2856 - Y5 R2FR Amplitude Current Continuity Variational Consistency Or Reject Under AX1090

Status: `Y5_R2FR_2856_conditional_noether_route_not_parent_proven_vertical_generator_next`

## Private Verdict

This checkpoint does not close local GR. It does something narrower but valuable: it shows the exact form a legitimate derivation would have to take.

The amplitude identity can be obtained in a clean way only if a parent Noether/Bianchi/gauge identity supplies the amplitude-channel generator with adjoint coefficients `(1, sigma_R)`.

In that case the variational identity can reduce to:

`J_CAB + sigma_R J_R = dK_amp`

and, with boundary silence, to:

`Q_CAB + sigma_R q_R_eff = 0`

But the current corpus checkpoint does not yet source the vertical generator, the parent action owner, the operator divergence, or the boundary theorem. So the theorem-zero route is coherent but not proven. It is not rejected as mathematics; it is rejected as a claim.

The next move is sharp: hunt for or construct the vertical generator. If that generator is tunable or inserted merely to cancel the amplitude, the route gets demoted to closure-only and we return to finite source rows.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Noether Derivation Attempt

{markdown_table(rows["noether"], ["step_id", "formal_expression", "status", "missing_evidence", "parent_signed", "valid_for_claim"])}

## Variational Clause Audit

{markdown_table(rows["clauses"], ["clause_id", "clause", "necessity", "status", "blocker", "clause_closed", "valid_for_claim"])}

## Symmetry Candidate Audit

{markdown_table(rows["candidates"], ["candidate_id", "candidate", "status", "why_not_closed", "selected_as_claim_route", "valid_for_claim"])}

## Conditional Theorem

{markdown_table(rows["conditional"], ["conditional_id", "statement", "kind", "status", "parent_proven", "usable_for_claim"])}

## Obstruction Ledger

{markdown_table(rows["obstructions"], ["obstruction_id", "code", "needed_resolution", "blocks", "resolved", "valid_for_claim"])}

## Source Request Ledger

{markdown_table(rows["requests"], ["request_id", "needed_source", "minimum_content", "accepted_only_if", "status", "valid_for_claim"])}

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
    rows["noether"] = noether_rows()
    rows["clauses"] = clause_rows()
    rows["candidates"] = candidate_rows()
    rows["conditional"] = conditional_rows()
    rows["obstructions"] = obstruction_rows()
    rows["requests"] = request_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "noether", "clauses", "candidates", "conditional", "obstructions", "requests", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2856_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2856_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
