from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1264"
TITLE = "1264-Y5-R10-RAB-parent-theta-vR-fill-or-finite-ZR-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS_DIR = ROOT / "source-intake" / "rab-sector" / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
AUXILIARY_ROUTE_PATH = OUT_DIR / f"{PACK_ID}_AUXILIARY_COMPATIBILITY_ROUTE.csv"
THETA_VR_FILL_PATH = OUT_DIR / f"{PACK_ID}_THETA_OMEGA_VR_FILL_AUDIT.csv"
BOUNDARY_TEST_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_ZERO_TEST.csv"
ZR_OPERATOR_STATUS_PATH = OUT_DIR / f"{PACK_ID}_ZR_OPERATOR_STATUS.csv"
FINITE_SOURCE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_SOURCE_ROW_REQUIREMENTS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1264_VALIDATION.csv"
FINITE_TEMPLATE_PATH = RAB_DOCS_DIR / "ZR1264_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"


FINITE_TEMPLATE_FIELDS = [
    "row_id",
    "coefficient_symbol",
    "branch",
    "coefficient_value",
    "coefficient_units",
    "sign_domain",
    "parent_status",
    "theta_omega_status",
    "boundary_status",
    "arena_projection",
    "source_path",
    "source_anchor",
    "valid_for_claim",
    "claim_allowed",
    "notes",
]


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(rows: list[dict[str, object]]) -> bool:
    joined = "\n".join(str(value) for row in rows for value in row.values())
    return "MISSING" in joined or "TBD" in joined or "PLACEHOLDER" in joined


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        AUXILIARY_ROUTE_PATH,
        THETA_VR_FILL_PATH,
        BOUNDARY_TEST_PATH,
        ZR_OPERATOR_STATUS_PATH,
        FINITE_SOURCE_REQUIREMENTS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        FINITE_TEMPLATE_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAB_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1264_0_1263_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_NEXT_TARGET.csv",
            "needle": "NEXT1263_0_1264",
            "purpose": "handoff to parent theta/vR fill or finite Z_R source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_1_1263_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_PRESYMPLECTIC_NULL_DERIVATION_CHAIN.csv",
            "needle": "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED",
            "purpose": "previous presymplectic-null route status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_2_1263_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_PARENT_INPUT_BLOCKERS.csv",
            "needle": "MISSING_RAB_VERTICAL_GENERATOR",
            "purpose": "specific missing v_R blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_3_1263_kinetic",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_KINETIC_TERM_CONTRADICTION_AUDIT.csv",
            "needle": "EXACT_CONDITIONAL_ON_TRUE_NULLNESS",
            "purpose": "conditional contradiction between nullness and nonzero Z_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_4_1262_minimal",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
            "needle": "MIN1262_2_no_vertical_metric_connection",
            "purpose": "no vertical metric/connection blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_5_728_omega",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
            "needle": "OM728_0_covariant_variation_definition",
            "purpose": "parent theta/Omega candidate route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_6_728_blocker",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_728_PARENT_OWNERSHIP_BLOCKER.csv",
            "needle": "POB728_0_L_parent",
            "purpose": "explicit parent Lagrangian blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_7_729_noether",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv",
            "needle": "NPJ729_5_symplectic_flat_closure",
            "purpose": "single-current symplectic-flat closure condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1264_8_1263_boundary",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_RAB_BOUNDARY_CHARGE_AUDIT.csv",
            "needle": "RBA1263_1_surface_momentum",
            "purpose": "R_AB boundary momentum blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    auxiliary_route = [
        {
            "route_id": "AUX1264_0_parent_block",
            "candidate_parent_block": "L_Raux = sqrt(h) Lambda_R^{AB}(R_AB - C_AB[q(Phi),theta,top])",
            "role": "makes R_AB an auxiliary compatibility coordinate rather than a propagating field",
            "variation": "delta_R L_Raux = sqrt(h) Lambda_R^{AB} delta R_AB; delta_Lambda L_Raux = sqrt(h)(R_AB-C_AB)delta Lambda_R",
            "what_it_buys": "on the auxiliary constraint branch Lambda_R=0 and R_AB=C_AB, compact R_AB variations have no kinetic momentum",
            "current_status": "CANDIDATE_PARENT_BLOCK_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "AUX1264_1_theta",
            "candidate_parent_block": "no D_mu R_AB and no D_mu Lambda_R in L_Raux",
            "role": "kills the R_AB symplectic potential contribution",
            "variation": "theta_Raux(delta R,delta Lambda)=0",
            "what_it_buys": "Omega_Raux=0 before adding any gradient counterterm",
            "current_status": "EXACT_IF_PARENT_BLOCK_ADOPTED_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "AUX1264_2_vR",
            "candidate_parent_block": "v_eta: delta_eta R_AB=eta_AB, delta_eta q=0, delta_eta theta=0, delta_eta top=0",
            "role": "candidate field-by-field R_AB vertical generator",
            "variation": "Dq[v_eta]=0 by construction only if q ignores representative R_AB",
            "what_it_buys": "defines the object 1263 asked for, but only relative to the auxiliary quotient ansatz",
            "current_status": "CANDIDATE_GENERATOR_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "AUX1264_3_no_vertical_metric",
            "candidate_parent_block": "operator grammar permits C_AB and Lambda_R but no G_vert(DR,DR), no vertical connection, no Sobolev norm",
            "role": "protects auxiliary status from becoming a hidden physical fibre metric",
            "variation": "adding Z_R h^{ij}D_iR_ABD_jR_AB violates the auxiliary grammar",
            "what_it_buys": "would ban Z_R at parent action level if grammar is primitive-derived",
            "current_status": "PROTECTION_CLAUSE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "AUX1264_4_radiative_readout",
            "candidate_parent_block": "S_eff and readout preserve the auxiliary quotient grammar",
            "role": "prevents loops/readout from regenerating Z_R",
            "variation": "all effective R_AB derivative terms remain outside Image(ParentGenerate)",
            "what_it_buys": "turns a tree-level auxiliary route into a durable local theorem",
            "current_status": "UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theta_vr_fill = [
        {
            "fill_id": "TVR1264_0_theta_candidate",
            "object": "theta_R",
            "candidate_value": "0",
            "derivation": "no derivative of R_AB appears in L_Raux",
            "status": "EXACT_IF_AUXILIARY_PARENT_BLOCK_SIGNED",
            "missing_for_claim": "parent-derived auxiliary compatibility block and no-derivative operator grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "TVR1264_1_omega_candidate",
            "object": "Omega_R",
            "candidate_value": "0",
            "derivation": "Omega_R=delta theta_R, so theta_R=0 gives no R_AB symplectic two-form",
            "status": "EXACT_IF_AUXILIARY_PARENT_BLOCK_SIGNED",
            "missing_for_claim": "prove R_AB is not paired with a hidden momentum or vertical metric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "TVR1264_2_vR_candidate",
            "object": "v_R[eta]",
            "candidate_value": "delta_eta R_AB=eta_AB with all quotient observables fixed",
            "derivation": "representative shift in an auxiliary compatibility coordinate",
            "status": "CANDIDATE_NOT_PARENT_DERIVED",
            "missing_for_claim": "explicit parent quotient map q and proof Dq[v_R]=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fill_id": "TVR1264_3_on_shell_nullness",
            "object": "delta_v S_Raux",
            "candidate_value": "int sqrt(h) Lambda_R eta_AB, vanishing only on Lambda_R=0 branch",
            "derivation": "Euler equation from delta R_AB sets Lambda_R=0 if no other R_AB source exists",
            "status": "ON_SHELL_AUXILIARY_NULL_NOT_OFFSHELL_GAUGE",
            "missing_for_claim": "show on-shell null is enough for the local theorem, or strengthen to first-class gauge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    boundary_test = [
        {
            "test_id": "BT1264_0_no_bulk_derivative",
            "quantity": "Pi_R^n from L_Raux",
            "candidate_result": "0",
            "reason": "L_Raux contains no D_i R_AB",
            "status": "EXACT_IF_AUXILIARY_BLOCK_ONLY",
            "remaining_risk": "any added Z_R term immediately creates Pi_R^n=Z_R n^iD_iR_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BT1264_1_boundary_functional",
            "quantity": "partial B_R/partial R_AB",
            "candidate_result": "0",
            "reason": "not present in the auxiliary block",
            "status": "NOT_PARENT_PROTECTED",
            "remaining_risk": "a boundary/corner term can reintroduce R_AB hair unless excluded by parent boundary grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "BT1264_2_hamiltonian_charge",
            "quantity": "delta H_eta=int_boundary(delta Q_eta-i_eta theta)",
            "candidate_result": "0 if theta_R=0 and Q_eta=0",
            "reason": "no R_AB derivative or boundary generator appears in L_Raux",
            "status": "CONDITIONAL_ON_QR_ZERO_AND_NO_BOUNDARY_BLOCK",
            "remaining_risk": "Q_R/B_R still needs parent zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zr_operator_status = [
        {
            "status_id": "ZOS1264_0_tree_level_auxiliary",
            "operator": "Z_R h^{ij}D_iR_ABD_jR_AB",
            "verdict": "forbidden by the auxiliary compatibility grammar",
            "strength": "EXACT_IF_GRAMMAR_PARENT_SIGNED",
            "why_not_claimed": "grammar is candidate-written, not derived from motion/time/space parent primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "ZOS1264_1_EFT_counterterm",
            "operator": "radiative/readout-generated Z_R",
            "verdict": "still legal unless auxiliary status is symmetry/constraint protected",
            "strength": "UNSIGNED_PROTECTION",
            "why_not_claimed": "no radiative/readout closure theorem yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "ZOS1264_2_finite_residual",
            "operator": "finite Z_R branch",
            "verdict": "retained as fallback if auxiliary grammar fails",
            "strength": "NONCLAIM_FALLBACK",
            "why_not_claimed": "requires sourced Z_R/M_R2/J_R/B_R and arena projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_source_requirements = [
        {
            "requirement_id": "FZR1264_0_ZR",
            "field": "Z_R",
            "required_content": "numeric coefficient, theorem-zero, or explicit prior interval; units; normalization; source path",
            "reject_if": "MISSING/TBD placeholders, docs-only template, or no arena projection",
            "current_status": "MISSING_SOURCE_BACKED_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "FZR1264_1_MR2",
            "field": "M_R^2",
            "required_content": "mass-gap/Hessian or sourced screening scale for ell_R=sqrt(Z_R/M_R^2)",
            "reject_if": "no parent second variation or no units",
            "current_status": "MISSING_SOURCE_BACKED_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "FZR1264_2_JR",
            "field": "J_R",
            "required_content": "matter/source coupling zero theorem or finite coupling value",
            "reject_if": "matter descent not proved and no numeric source map",
            "current_status": "MISSING_SOURCE_BACKED_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "FZR1264_3_BR",
            "field": "B_R",
            "required_content": "boundary zero theorem or finite boundary flux bound",
            "reject_if": "boundary silence is assumed from bulk auxiliary status alone",
            "current_status": "MISSING_SOURCE_BACKED_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "FZR1264_4_arena",
            "field": "tau_R10/tau_PPN/tau_clock/tau_orbital",
            "required_content": "observable projection kernels and acceptance ceiling",
            "reject_if": "coefficient is disconnected from test arena residuals",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_template = [
        {
            "row_id": "ZR1264_TEMPLATE_DO_NOT_SCORE",
            "coefficient_symbol": "Z_R",
            "branch": "finite_ZR_residual_or_theorem_zero",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_UNITS",
            "sign_domain": "MISSING_SIGN_DOMAIN",
            "parent_status": "MISSING_PARENT_AUXILIARY_SIGNATURE_OR_SOURCE",
            "theta_omega_status": "MISSING_THETA_OMEGA_VR_STATUS",
            "boundary_status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "arena_projection": "MISSING_R10_PPN_CLOCK_OR_ORBITAL_PROJECTION",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only source row template. Do not move to raw/accepted or score until placeholders are replaced by sourced values or theorem-zero certificates.",
        }
    ]
    write_csv(FINITE_TEMPLATE_PATH, finite_template, FINITE_TEMPLATE_FIELDS)

    claim_gates = [
        {
            "gate_id": "GATE1264_0_theta_vR_not_claimed",
            "claim": "parent theta/Omega/v_R proof closes",
            "status": "BLOCKED",
            "reason": "auxiliary block gives a candidate theta_R=Omega_R=0 route, but the block is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1264_1_ZR_zero_not_claimed",
            "claim": "Z_R=0",
            "status": "BLOCKED",
            "reason": "requires parent-signed auxiliary grammar plus no vertical metric, boundary, and radiative/readout protection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1264_2_finite_row_not_scoreable",
            "claim": "finite Z_R row is scoreable",
            "status": "BLOCKED",
            "reason": "new finite-Z_R template is docs-only and deliberately contains MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1264_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite residual envelope is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1264_0_partial_fill",
            "decision": "a credible auxiliary-compatibility parent block can make theta_R=0, Omega_R=0, and Pi_R^n=0 at tree level",
            "because": "if R_AB appears only algebraically as Lambda_R(R_AB-C_AB), no derivative momentum or symplectic R_AB pair exists",
            "status": "CANDIDATE_ROUTE_NOT_PARENT_SIGNED",
            "next_action": "derive/sign the auxiliary block and protection clauses from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1264_1_not_enough",
            "decision": "this is not yet a local-GR reduction theorem",
            "because": "on-shell auxiliary nullness, no-vertical-metric protection, boundary zero, and readout stability are still unsigned",
            "status": "BLOCKED_FOR_CLAIM",
            "next_action": "audit auxiliary-constraint protection before falling back to finite Z_R bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1264_2_fallback",
            "decision": "finite Z_R residual intake remains ready but empty",
            "because": "if auxiliary protection fails, R_AB can be physical/vertically metrized and must be bounded empirically",
            "status": "NONCLAIM_TEMPLATE_ONLY",
            "next_action": "do not score until source-backed rows and arena projections exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1264_0_1265",
            "target_file": "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md",
            "target_script": "scripts/Y5_R10_RAB_auxiliary_constraint_protection_or_finite_ZR_bound_runner.py",
            "task": "try to parent-sign the auxiliary compatibility block and prove no vertical metric, boundary, or readout regeneration; if not, convert the finite-ZR source template into a nonclaim bound-runner intake",
            "success_condition": "either protected auxiliary theorem route for Z_R=0 with no closure smuggling, or finite-ZR residual workflow that remains nonclaim but executable",
            "do_not": "do not treat theta_R=0 from the candidate block as a completed parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (AUXILIARY_ROUTE_PATH, auxiliary_route),
        (THETA_VR_FILL_PATH, theta_vr_fill),
        (BOUNDARY_TEST_PATH, boundary_test),
        (ZR_OPERATOR_STATUS_PATH, zr_operator_status),
        (FINITE_SOURCE_REQUIREMENTS_PATH, finite_source_requirements),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    aux_route_written = len(auxiliary_route) == 5 and auxiliary_route[0]["current_status"] == "CANDIDATE_PARENT_BLOCK_NOT_SIGNED"
    theta_candidate_nonclaim = all("CLAIM" not in str(row["status"]).upper() for row in theta_vr_fill)
    boundary_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in boundary_test)
    gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    finite_template_guard = contains_missing_marker(finite_template) and all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in finite_template)
    all_rows_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _path, rows in generated_tables
        for row in rows
    )
    next_is_1265 = next_target[0]["target_file"].startswith("1265-")

    csv_parse_ok = True
    csv_parse_details: list[str] = []
    for path, _rows in [*generated_tables, (FINITE_TEMPLATE_PATH, finite_template)]:
        try:
            parsed_rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAILED:{exc}")

    formalization_writes = generated_inside_formalization()

    validation_rows = [
        validation_row("VAL1264_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1264_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1264_2_aux_route_written", "auxiliary compatibility route is written but unsigned", aux_route_written, f"auxiliary_rows={len(auxiliary_route)}"),
        validation_row("VAL1264_3_theta_candidate_nonclaim", "theta/Omega/vR candidate is not promoted", theta_candidate_nonclaim, f"theta_rows={len(theta_vr_fill)}"),
        validation_row("VAL1264_4_boundary_nonclaim", "boundary test remains nonclaim", boundary_nonclaim, f"boundary_rows={len(boundary_test)}"),
        validation_row("VAL1264_5_claim_gates", "all claim gates remain blocked", gates_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1264_6_template_guard", "finite-ZR template is docs-only and incomplete", finite_template_guard, FINITE_TEMPLATE_PATH.name),
        validation_row("VAL1264_7_nonclaim_policy", "all generated rows remain nonclaim", all_rows_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1264_8_next_target_1265", "next target is auxiliary protection or finite-ZR bound runner", next_is_1265, next_target[0]["target_file"]),
        validation_row("VAL1264_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1264_10_formalization_untouched", "formalization-workbench untouched by generated outputs", not formalization_writes, f"formalization_generated_output_count={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1264_11_overall",
            "overall 1264 validation",
            overall,
            "1264 partially fills the theta/Omega/vR route with an auxiliary compatibility candidate, but keeps Z_R=0 and local tests blocked until parent protection is derived",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1264 finds a plausible route, not a finished theorem: if `R_AB` is an auxiliary compatibility coordinate entering only through `Lambda_R(R_AB-C_AB)`, then `theta_R=0`, `Omega_R=0`, and `Pi_R^n=0` at tree level.

**Main progress:** this is the first concrete candidate for the missing parent `theta/Omega/v_R` fill. It explains exactly how `R_AB` could be non-propagating without a plateau axiom.

**No-claim guard:** the route is still unsigned. A parent-derived auxiliary block, no vertical metric/connection, boundary zero, and radiative/readout protection are still required before any `Z_R=0`, local-GR/Newton, R10, PPN, clock, or orbital claim.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Auxiliary Compatibility Route
{markdown_table(auxiliary_route, ["route_id", "candidate_parent_block", "role", "variation", "what_it_buys", "current_status", "valid_for_claim", "claim_allowed"])}

## Theta Omega vR Fill Audit
{markdown_table(theta_vr_fill, ["fill_id", "object", "candidate_value", "derivation", "status", "missing_for_claim", "valid_for_claim", "claim_allowed"])}

## Boundary Zero Test
{markdown_table(boundary_test, ["test_id", "quantity", "candidate_result", "reason", "status", "remaining_risk", "valid_for_claim", "claim_allowed"])}

## Z_R Operator Status
{markdown_table(zr_operator_status, ["status_id", "operator", "verdict", "strength", "why_not_claimed", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Source Row Requirements
{markdown_table(finite_source_requirements, ["requirement_id", "field", "required_content", "reject_if", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
