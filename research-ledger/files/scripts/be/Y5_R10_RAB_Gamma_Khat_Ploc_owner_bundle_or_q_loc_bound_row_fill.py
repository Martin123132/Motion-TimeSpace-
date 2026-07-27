from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1351"
TITLE = "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_OPERATOR_BUNDLE_THEOREM.csv"
OWNER_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_OWNER_BUNDLE_AUDIT.csv"
QLOC_BOUND_ROWS_PATH = OUT_DIR / f"{PACK_ID}_QLOC_BOUND_ROW_FILL.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1351_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1351_0_1350_doc",
            "source_path": "1350-Y5-R10-RAB-finite-Bmem-and-qloc-residual-runner-contract.md",
            "required_anchor": "Current verdict",
            "purpose": "1350 runner contract: finite B_mem/q_loc cannot score without owner bundle.",
        },
        {
            "source_id": "SRC1351_1_1350_required_inputs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1350_REQUIRED_INPUT_ROWS.csv",
            "required_anchor": "REQ1350_3_Gamma_eff",
            "purpose": "required Gamma_eff, Khat, Ploc, and arena-map inputs.",
        },
        {
            "source_id": "SRC1351_2_GK_contract",
            "source_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "required_anchor": "GK513_0_action_existence",
            "purpose": "operator-bundle clauses for action, metric response, Euler closure, projector, and boundary.",
        },
        {
            "source_id": "SRC1351_3_GK_residual",
            "source_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
            "required_anchor": "QR513_0_nonvariational_stress",
            "purpose": "demotion policy if the variational bundle is absent.",
        },
        {
            "source_id": "SRC1351_4_owner_extraction",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1284_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv",
            "required_anchor": "GKO1284_5_verdict",
            "purpose": "latest Gamma/Khat owner extraction verdict.",
        },
        {
            "source_id": "SRC1351_5_response_audit",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1349_GAMMA_KHAT_RESPONSE_AUDIT.csv",
            "required_anchor": "RESP1349_3_metric_response_contract",
            "purpose": "Khat cannot be defined by hand; response match is not found.",
        },
        {
            "source_id": "SRC1351_6_qbound_spec",
            "source_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "required_anchor": "QB516_0_compact_shell_budget",
            "purpose": "existing q_loc fallback-bound specification.",
        },
        {
            "source_id": "SRC1351_7_qpack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1189_QLOC_COMPONENT_RESIDUAL_INPUT_PACK.csv",
            "required_anchor": "QPACK1189_0_PPN_component_template",
            "purpose": "component residual template rows for local arenas.",
        },
        {
            "source_id": "SRC1351_8_parent_sector",
            "source_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "required_anchor": "PCS1009_4_Gamma_Khat_extra",
            "purpose": "parent-sector contract marks Gamma/Khat extra sector as hard fail.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def conditional_theorem() -> list[dict[str, object]]:
    rows = [
        {
            "theorem_id": "THM1351_0_define_stress",
            "clause": "Define one variational local stress from one parent scalar density.",
            "mathematical_form": "S_GK=-int sqrt(-g) Gamma_eff[g,Phi]; K_metric^{mu nu}=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu}; T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "consequence": "nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu} if K_hat equals the metric response with fixed conventions.",
            "current_status": "CONDITIONAL_ONLY",
        },
        {
            "theorem_id": "THM1351_1_ward_identity",
            "clause": "Use diffeomorphism invariance and the same field list in the action and response.",
            "mathematical_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_boundary^nu + J_external^nu",
            "consequence": "on shell, with boundary no-flux and no external spurion currents, the unprojected residual is zero.",
            "current_status": "CONDITIONAL_ONLY",
        },
        {
            "theorem_id": "THM1351_2_projected_residual",
            "clause": "Project only with a parent-owned local projector.",
            "mathematical_form": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})=P_loc nabla_mu T_GK^{mu nu}",
            "consequence": "if P_loc is parent-owned and commutes with the local branch limit, q_loc^nu=0 on compact source-free solutions.",
            "current_status": "CONDITIONAL_ONLY",
        },
        {
            "theorem_id": "THM1351_3_verdict",
            "clause": "The theorem is mathematically sharp but not a current MTS proof.",
            "mathematical_form": "S_GK + Khat=delta_g Gamma_eff + P_loc owner + Euler/source/boundary closure => q_loc^nu=0",
            "consequence": "local-GR/PPN/R10 gates can reopen only after every premise receives a source path.",
            "current_status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def owner_bundle_audit() -> list[dict[str, object]]:
    rows = [
        {
            "audit_id": "OB1351_0_action_existence",
            "bundle_piece": "S_GK[g,Phi]",
            "required_evidence": "local diffeomorphism-invariant parent action whose Hilbert response is the Gamma/Khat stress",
            "source_evidence": "GK513_0_action_existence=not_supplied; PCS1009_4 hard_fail_current_claim",
            "current_status": "NOT_SUPPLIED",
            "blocking_reason": "without S_GK the bundle is bookkeeping, not a derived local-GR mechanism",
        },
        {
            "audit_id": "OB1351_1_Gamma_eff_formula",
            "bundle_piece": "Gamma_eff",
            "required_evidence": "concrete scalar-density formula with fields, units, derivative terms, branch convention, and source path",
            "source_evidence": "GKO1284_0=CONTRACT_ONLY_NO_CURRENT_FORMULA",
            "current_status": "CONTRACT_ONLY",
            "blocking_reason": "no live formula can be varied or unit-checked",
        },
        {
            "audit_id": "OB1351_2_Khat_metric_response",
            "bundle_piece": "K_hat^{mu nu}",
            "required_evidence": "K_hat equals metric response of the same Gamma_eff density including volume, derivative, and boundary terms",
            "source_evidence": "RESP1349_3=MATCH_NOT_FOUND; GK513_1=not_checked",
            "current_status": "NOT_MATCHED",
            "blocking_reason": "cannot cancel nabla Gamma_eff by defining Khat divergence after the fact",
        },
        {
            "audit_id": "OB1351_3_Ploc_owner",
            "bundle_piece": "P_loc",
            "required_evidence": "covariant parent projector fixed before readout and commuting with local limit",
            "source_evidence": "GK513_4_projector_ownership=open; REQ1350_5=MISSING_PROJECTOR_OWNER",
            "current_status": "OPEN",
            "blocking_reason": "projection could hide force components or tune the residual",
        },
        {
            "audit_id": "OB1351_4_Euler_source_closure",
            "bundle_piece": "Euler/Ward source closure",
            "required_evidence": "all fields building Gamma_eff and Khat are on shell and no X_B/L_cg/bath/spurion current remains",
            "source_evidence": "GK513_2=not_derived; RESP1349_2=FAILS_PARENT_GATE",
            "current_status": "NOT_DERIVED",
            "blocking_reason": "external profiles or bath exchange remain physical source terms",
        },
        {
            "audit_id": "OB1351_5_boundary_no_flux",
            "bundle_piece": "boundary/symplectic no-flux",
            "required_evidence": "boundary terms from S_GK vanish or are fixed topological subtractions on linking spheres",
            "source_evidence": "GK513_5_boundary_no_flux=open; QR513_4_boundary_flux active demotion",
            "current_status": "OPEN",
            "blocking_reason": "bulk zero could still leak through boundary charge/mass flux",
        },
        {
            "audit_id": "OB1351_6_observable_lock",
            "bundle_piece": "R10/PPN/clock/orbital observable maps",
            "required_evidence": "same q_loc profile maps into all named local arenas with units and bounds",
            "source_evidence": "REQ1350_6..8 missing maps; QPACK1189 rows are templates",
            "current_status": "MISSING",
            "blocking_reason": "even a finite residual cannot be scored without response coefficients",
        },
        {
            "audit_id": "OB1351_7_verdict",
            "bundle_piece": "minimal Gamma/Khat/Ploc owner bundle",
            "required_evidence": "OB1351_0 through OB1351_6 all pass with source paths",
            "source_evidence": "multiple required pieces are not supplied/open/not matched",
            "current_status": "OWNER_BUNDLE_NOT_CLOSED",
            "blocking_reason": "q_loc zero and local-GR reduction remain nonclaim",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def qloc_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "QB1351_0_R10_alpha_lambda",
            "arena": "R10 short-range gravity",
            "residual_quantity": "q_loc profile or finite B_mem profile",
            "observable": "alpha(lambda)",
            "profile_expression": "alpha_pred(lambda)=F_R10[q_loc,B_mem,Z_mem,M2_mem,source_geometry]",
            "units_required": "dimensionless alpha; length lambda with SI/natural conversion",
            "bound_source_required": "claim-grade alpha(lambda) curve/table, not anchor-only prose",
            "missing_fields": "MISSING_QLOC_PROFILE;MISSING_CQ_ALPHA_LAMBDA;MISSING_SOURCE_GEOMETRY;MISSING_CLAIM_CURVE",
            "row_status": "template_only_not_scoreable",
        },
        {
            "row_id": "QB1351_1_PPN_vector",
            "arena": "PPN/local weak-field",
            "residual_quantity": "q_loc^nu and Delta_K",
            "observable": "gamma-1,beta-1,alpha_1,alpha_2,alpha_3,xi,Gdot/G",
            "profile_expression": "Delta_PPN=F_PPN[q_loc,weak_field_metric_solution,source_normalization]",
            "units_required": "dimensionless PPN vector and time-drift convention",
            "bound_source_required": "official PPN/source-normalization bounds plus coefficient map",
            "missing_fields": "MISSING_WEAK_FIELD_METRIC_SOLUTION;MISSING_QLOC_TO_PPN_COEFFICIENTS;MISSING_GAUGE_LOCK",
            "row_status": "template_only_not_scoreable",
        },
        {
            "row_id": "QB1351_2_clock_readout",
            "arena": "clock/time/readout",
            "residual_quantity": "q_loc readout tail and hidden-visible coupling",
            "observable": "delta_nu/nu; drift; composition-clock residual",
            "profile_expression": "delta_nu/nu=F_clock[q_loc,b_clock_i,readout_frame,constant_marker_leakage]",
            "units_required": "fractional frequency and drift units",
            "bound_source_required": "clock/readout bound source and coefficient derivation",
            "missing_fields": "MISSING_CLOCK_RESPONSE_COEFFICIENTS;MISSING_READOUT_FRAME;MISSING_CONSTANT_MARKER_MAP",
            "row_status": "template_only_not_scoreable",
        },
        {
            "row_id": "QB1351_3_orbital_force",
            "arena": "orbital/source dynamics",
            "residual_quantity": "q_loc force or metric tail",
            "observable": "acceleration, perihelion, Shapiro, ephemeris, binary timing residuals",
            "profile_expression": "a_res(r)=F_orbit[q_loc,radial_profile,source_charge_equality]",
            "units_required": "acceleration/precession/time-delay units",
            "bound_source_required": "orbital data-bound source and radial response map",
            "missing_fields": "MISSING_RADIAL_PROFILE;MISSING_FORCE_TO_ACCELERATION_MAP;MISSING_SOURCE_CHARGE_EQUALITY",
            "row_status": "template_only_not_scoreable",
        },
        {
            "row_id": "QB1351_4_source_normalization_R11",
            "arena": "Newton/source-normalization/R11",
            "residual_quantity": "q_loc source-normalization component",
            "observable": "measured-GM drift; non-EH operator/source residual",
            "profile_expression": "Delta_GM or c_GK_operator_vector=F_source[q_loc,Pi_M,J_H,Khat]",
            "units_required": "dimensionless drift or operator units with normalization",
            "bound_source_required": "measured-GM/R11 coefficient and bound ledger",
            "missing_fields": "MISSING_SOURCE_NORMALIZATION_OPERATOR;MISSING_R11_COEFFICIENT_VECTOR;MISSING_PIM_RESPONSE",
            "row_status": "template_only_not_scoreable",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1351_0_operator_bundle",
            "claim": "Gamma_eff/K_hat/P_loc owner bundle is derived",
            "allowed_if": "S_GK, concrete Gamma_eff, Khat metric response, P_loc, Ward/Euler, and boundary clauses all have source paths",
            "current_status": "BLOCKED",
            "reason": "at least action existence, Gamma formula, Khat response, Ploc owner, and boundary/source closure are missing",
        },
        {
            "gate_id": "GATE1351_1_q_loc_zero",
            "claim": "q_loc^nu=0 in local compact vacuum",
            "allowed_if": "conditional theorem premises are all parent-signed",
            "current_status": "BLOCKED",
            "reason": "the theorem is conditional but not current-MTS-derived",
        },
        {
            "gate_id": "GATE1351_2_local_GR",
            "claim": "local GR/PPN reduction passes",
            "allowed_if": "q_loc zero or scored q_loc residual is below PPN/source-normalization bounds",
            "current_status": "BLOCKED",
            "reason": "no q_loc zero theorem and no scoreable PPN/source map",
        },
        {
            "gate_id": "GATE1351_3_R10_clock_orbital",
            "claim": "R10, clock, and orbital arenas pass",
            "allowed_if": "same residual profile maps into each arena with source-backed bounds",
            "current_status": "BLOCKED",
            "reason": "bound rows are template-only and not scoreable",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1351_0_theorem_path_kept",
            "decision": "The exact operator-bundle theorem is retained as the clean derivation target.",
            "why": "If S_GK, Khat metric response, P_loc, Euler closure, and boundary silence all close, q_loc zero follows rather than being assumed.",
            "next_action": "attack the response/displacement conjugacy construction as the most promising owner route",
        },
        {
            "decision_id": "DEC1351_1_current_claims_blocked",
            "decision": "No local-GR, PPN, R10, clock, orbital, or q_loc-zero claim is allowed from 1351.",
            "why": "current evidence remains conditional/template-level rather than parent-owned",
            "next_action": "keep q_loc bound rows nonclaim until coefficients and source paths are real",
        },
        {
            "decision_id": "DEC1351_2_bound_rows_ready_for_future",
            "decision": "The fallback residual rows are now arena-separated and ready for real coefficient/source fills.",
            "why": "This prevents symbolic B_mem or q_loc from silently becoming a score.",
            "next_action": "when derivation fails, fill one arena row at a time instead of claiming a global pass",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1351_0_1352",
            "target_file": "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill.md",
            "target_script": "scripts/Y5_R10_RAB_response_displacement_conjugacy_action_or_q_loc_profile_source_fill.py",
            "task": "try to construct a response/displacement parent action where Gamma_eff and K_hat are conjugate scalar/tensor projections of one covariant field; if this fails, fill the first q_loc profile source row without claiming a pass",
            "success_condition": "either a source-checkable conjugacy action template with metric-response identities, or a nonclaim q_loc profile row with units/source/arena requirements",
            "do_not": "do not define Khat by divergence cancellation; do not set q_loc=0 by plateau/closure; do not edit formalization-workbench or use GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    qrows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if status else "FAIL",
                "details": details,
            }
        )

    add(
        "VAL1351_0_sources_exist",
        "registered sources exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    add(
        "VAL1351_1_conditional_theorem_written",
        "operator-bundle theorem is written as conditional, not claim",
        any(row["theorem_id"] == "THM1351_3_verdict" and row["current_status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in theorem)
        and all(not row["claim_allowed"] for row in theorem),
        "THM1351_3_verdict present and nonclaim",
    )

    verdict = next(row for row in owner_audit if row["audit_id"] == "OB1351_7_verdict")
    add(
        "VAL1351_2_owner_bundle_blocked",
        "minimal Gamma/Khat/Ploc owner bundle is not promoted",
        verdict["current_status"] == "OWNER_BUNDLE_NOT_CLOSED" and not verdict["claim_allowed"],
        str(verdict["blocking_reason"]),
    )

    required_arenas = {"R10 short-range gravity", "PPN/local weak-field", "clock/time/readout", "orbital/source dynamics"}
    present_arenas = {str(row["arena"]) for row in qrows}
    add(
        "VAL1351_3_bound_rows_cover_requested_arenas",
        "q_loc bound rows cover R10, PPN, clocks, and orbital arenas",
        required_arenas.issubset(present_arenas),
        f"missing={sorted(required_arenas - present_arenas)}",
    )

    add(
        "VAL1351_4_bound_rows_nonclaim",
        "q_loc bound rows are template-only and nonclaim",
        all(row["row_status"] == "template_only_not_scoreable" and not row["claim_allowed"] for row in qrows),
        f"rows={len(qrows)}",
    )

    add(
        "VAL1351_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_rows = sources + theorem + owner_audit + qrows + gates + decisions + next_target
    add(
        "VAL1351_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits = list(FORMALIZATION.rglob("*1351*")) if FORMALIZATION.exists() else []
    add(
        "VAL1351_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1351_8_next_target_1352",
        "next target routes to response/displacement conjugacy action",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1352-Y5-R10-RAB-response-displacement"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1351_9_overall",
        "overall 1351 validation",
        all(row["status"] == "PASS" for row in validations),
        "1351 preserves derivation route while staging nonclaim q_loc bound rows",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    qrows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1351 writes the clean conditional theorem for `q_loc^nu -> 0`, but the current MTS corpus still does not parent-own the required `Gamma_eff`, `K_hat`, and `P_loc` operator bundle.",
            "**Main progress:** the route is now precise: derive one covariant `S_GK`, prove `K_hat` is the metric response of its `Gamma_eff` density, own `P_loc`, close Ward/Euler/source/boundary terms, then `q_loc` vanishes. Since those premises are not yet sourced, R10/PPN/clock/orbital rows are staged as nonclaim bound templates.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Conditional operator-bundle theorem",
            table(["theorem_id", "clause", "mathematical_form", "consequence", "current_status"], theorem),
            "## Owner-bundle audit",
            table(["audit_id", "bundle_piece", "required_evidence", "current_status", "blocking_reason"], owner_audit),
            "## q_loc bound-row fill",
            table(["row_id", "arena", "residual_quantity", "observable", "missing_fields", "row_status", "claim_allowed"], qrows),
            "## Claim gates",
            table(["gate_id", "claim", "current_status", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    theorem = conditional_theorem()
    owner_audit = owner_bundle_audit()
    qrows = qloc_bound_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, theorem, owner_audit, qrows, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CONDITIONAL_THEOREM_PATH, theorem)
    write_csv(OWNER_AUDIT_PATH, owner_audit)
    write_csv(QLOC_BOUND_ROWS_PATH, qrows)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, theorem, owner_audit, qrows, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
