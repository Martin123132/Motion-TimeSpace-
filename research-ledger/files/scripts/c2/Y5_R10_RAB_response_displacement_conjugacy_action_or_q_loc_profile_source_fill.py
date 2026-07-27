from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1352"
TITLE = "1352-Y5-R10-RAB-response-displacement-conjugacy-action-or-q_loc-profile-source-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ACTION_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_DISPLACEMENT_ACTION_TEMPLATE.csv"
IDENTITY_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_METRIC_RESPONSE_IDENTITY_AUDIT.csv"
BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_CONJUGACY_BLOCKER_AUDIT.csv"
QLOC_PROFILE_PATH = OUT_DIR / f"{PACK_ID}_QLOC_PROFILE_SOURCE_ROW.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1352_VALIDATION.csv"


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
            "source_id": "SRC1352_0_1351_doc",
            "source_path": "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill.md",
            "required_anchor": "Current verdict",
            "purpose": "1351 says the operator-bundle theorem is clean but not parent-signed.",
        },
        {
            "source_id": "SRC1352_1_1351_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1351_NEXT_TARGET.csv",
            "required_anchor": "NEXT1351_0_1352",
            "purpose": "handoff to response/displacement conjugacy attempt.",
        },
        {
            "source_id": "SRC1352_2_response_contract",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "required_anchor": "RD516_2_metric_response",
            "purpose": "response-doublet clauses: even density, metric response, source zero, PPN lock, boundary.",
        },
        {
            "source_id": "SRC1352_3_response_variation",
            "source_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "required_anchor": "AV517_3_double_zero",
            "purpose": "formal double-zero derivation at Z=0.",
        },
        {
            "source_id": "SRC1352_4_gamma_candidates",
            "source_path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "required_anchor": "GO516_A_response_doublet_quadratic_density",
            "purpose": "best formal Gamma_eff owner candidate.",
        },
        {
            "source_id": "SRC1352_5_metric_audit",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            "required_anchor": "MA515_2_conjugate_response_field",
            "purpose": "conjugate response field is promising but not constructed.",
        },
        {
            "source_id": "SRC1352_6_passfail",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
            "required_anchor": "PF515_3_response_template_found",
            "purpose": "response template passes only conditionally; local q_loc zero still fails.",
        },
        {
            "source_id": "SRC1352_7_owner_extraction",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1284_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv",
            "required_anchor": "GKO1284_1_response_doublet_quadratic",
            "purpose": "latest owner extraction calls response doublet best formal candidate but not current MTS derived.",
        },
        {
            "source_id": "SRC1352_8_qrow_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1351_QLOC_BOUND_ROW_FILL.csv",
            "required_anchor": "QB1351_0_R10_alpha_lambda",
            "purpose": "nonclaim q_loc arena rows from 1351.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def action_template() -> list[dict[str, object]]:
    rows = [
        {
            "template_id": "RDA1352_0_parent_fields",
            "object": "response/displacement doublet",
            "definition": "R_+^A,R_-^A with Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2",
            "required_parent_clause": "exchange symmetry is a parent symmetry and the component map covers all physical local leakage channels",
            "current_status": "PARTIAL_NOT_COMPONENT_LOCKED",
        },
        {
            "template_id": "RDA1352_1_scalar_density",
            "object": "Gamma_eff[Z,R_even,g]",
            "definition": "Gamma_eff=Gamma0+1/2 Z^A M_AB(g,R_even,D,...) Z^B+O(Z^4)",
            "required_parent_clause": "M_AB is covariant, parent-owned, positive/self-adjoint, unit-normalized, and no linear J_A Z^A term exists",
            "current_status": "FORMAL_TEMPLATE_ONLY",
        },
        {
            "template_id": "RDA1352_2_action",
            "object": "S_GK",
            "definition": "S_GK=-int sqrt(-g) Gamma_eff[Z,R_even,g]",
            "required_parent_clause": "S_GK is a sector of the parent action, not an after-the-fact counterterm",
            "current_status": "NOT_PARENT_SIGNED",
        },
        {
            "template_id": "RDA1352_3_metric_response",
            "object": "K_metric^{mu nu}",
            "definition": "K_metric^{mu nu}=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu} minus the adopted volume/sign convention",
            "required_parent_clause": "the existing/live K_hat equals K_metric term-by-term including derivative, boundary, and projector terms",
            "current_status": "MATCH_NOT_FOUND",
        },
        {
            "template_id": "RDA1352_4_Euler_identity",
            "object": "Z Euler equation",
            "definition": "L_AB Z^B = J_A + B_A_boundary + S_A_source",
            "required_parent_clause": "J_A, B_A, and source-normalization/stress source rows vanish or are bounded",
            "current_status": "SOURCE_ZERO_NOT_DERIVED",
        },
        {
            "template_id": "RDA1352_5_verdict",
            "object": "response/displacement conjugacy action",
            "definition": "If RDA1352_0..4 close, Gamma_eff and K_hat become one variational object and q_loc becomes a Ward residual.",
            "required_parent_clause": "component lock, no-linear-source theorem, metric response match, P_loc owner, and boundary no-flux all pass",
            "current_status": "PROMISING_TEMPLATE_NOT_LIVE_PROOF",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def identity_audit() -> list[dict[str, object]]:
    rows = [
        {
            "identity_id": "MRI1352_0_first_variation",
            "identity": "delta Gamma_eff/delta Z^A = M_AB Z^B + O(Z^3)",
            "derived_under_template": True,
            "physical_payoff": "linear F_1 term vanishes at Z=0 if no linear source term is legal",
            "current_gap": "Z=0 is not yet proven to be the physical local q_loc/PPN/source-normalization state",
            "current_status": "CONDITIONAL_PASS",
        },
        {
            "identity_id": "MRI1352_1_metric_response",
            "identity": "delta_g S_GK gives K_metric and T_GK=Gamma_eff g-K_metric",
            "derived_under_template": True,
            "physical_payoff": "q_loc becomes projected divergence of one variational stress",
            "current_gap": "current MTS K_hat is not matched to K_metric term-by-term",
            "current_status": "FORMAL_IDENTITY_NOT_SYMBOL_MATCHED",
        },
        {
            "identity_id": "MRI1352_2_double_zero",
            "identity": "Gamma_eff-Gamma0=0 and partial_Z Gamma_eff=0 at Z=0",
            "derived_under_template": True,
            "physical_payoff": "local residual starts at second order if Z-source and boundary terms vanish",
            "current_gap": "Gamma0 subtraction and Z-source silence are not parent-signed",
            "current_status": "CONDITIONAL_PASS_NOT_CLAIM",
        },
        {
            "identity_id": "MRI1352_3_Ward_residual",
            "identity": "nabla_mu T_GK^{mu nu}=E_A nabla^nu Z^A + E_even nabla^nu R_even^A + boundary/source terms",
            "derived_under_template": True,
            "physical_payoff": "on shell and source-free, q_loc can vanish without a plateau axiom",
            "current_gap": "source/bath/domain/readout terms remain active",
            "current_status": "WARD_ROUTE_OPEN_NOT_CLOSED",
        },
        {
            "identity_id": "MRI1352_4_verdict",
            "identity": "response/displacement conjugacy could solve the coupling problem only if the blocker list closes",
            "derived_under_template": False,
            "physical_payoff": "best derivation route remains alive but not claimable",
            "current_gap": "component lock, J_Z/B_Z=0, Y5/Y6, P_loc, boundary, and metric symbol match",
            "current_status": "NO_LOCAL_GR_PROMOTION",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def blocker_audit() -> list[dict[str, object]]:
    rows = [
        {
            "blocker_id": "BLK1352_0_component_lock",
            "required_close": "Z^A equals the physical q_loc/PPN/source-normalization residual vector, not a bookkeeping shadow",
            "evidence": "RD516_5 not_derived; 1351 bound rows are templates",
            "status": "OPEN",
            "next_attack": "construct Z^A -> Y_loc^A component map covering Y0-Y6 and local arenas",
        },
        {
            "blocker_id": "BLK1352_1_no_linear_source",
            "required_close": "no legal J_A Z^A, B_A Z^A, source-normalization, or extra-stress linear terms",
            "evidence": "RD516_4 not_derived_hard_block; AV517_4 blocked_by_source_current_rows",
            "status": "OPEN",
            "next_attack": "derive exchange-odd source-current zero theorem or source-pack J_Z/B_Z rows",
        },
        {
            "blocker_id": "BLK1352_2_metric_symbol_match",
            "required_close": "live K_hat equals K_metric[Gamma_eff] term-by-term",
            "evidence": "MA515_1 fail; RESP1349_3 match not found",
            "status": "OPEN",
            "next_attack": "compute metric response of the chosen Gamma_eff and compare to Khat components",
        },
        {
            "blocker_id": "BLK1352_3_operator_positivity",
            "required_close": "M_AB/L_AB positive, self-adjoint, gauge-reduced, and unit-normalized",
            "evidence": "RD516_3 formal_candidate_only",
            "status": "OPEN",
            "next_attack": "state exact inner product, gauge quotient, boundary domain, and units",
        },
        {
            "blocker_id": "BLK1352_4_projector_boundary",
            "required_close": "P_loc parent owner and boundary no-flux theorem",
            "evidence": "RD516_6 open; GK513_4/5 open",
            "status": "OPEN",
            "next_attack": "derive before-readout projector and linking-sphere flux silence",
        },
        {
            "blocker_id": "BLK1352_5_verdict",
            "required_close": "all blockers above close simultaneously",
            "evidence": "multiple open/hard-block rows",
            "status": "CONJUGACY_ACTION_NOT_LIVE",
            "next_attack": "go after component-lock plus no-linear-source theorem first",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def qloc_profile_source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "profile_id": "QPROF1352_0_minimal_residual_source",
            "profile_object": "q_loc^nu finite source vector",
            "expression": "q_loc^nu=P_loc[sum_A E_A nabla^nu Phi^A + J_ext^nu + B_boundary^nu + nabla_mu Delta_K^{mu nu}] plus projector/readout commutator terms if P_loc is not fixed before variation",
            "required_inputs": "E_A;Phi^A;J_ext;B_boundary;Delta_K;P_loc;domain/coframe;units;normalization",
            "units_required": "force-density/stress-divergence units mapped into arena-specific dimensionless or SI observables",
            "source_path_required": "parent action or source profile file for every nonzero term",
            "current_missing": "MISSING_NUMERIC_PROFILE;MISSING_COMPONENT_LOCK;MISSING_DELTA_K;MISSING_PLOC_OWNER;MISSING_UNITS",
            "row_status": "first_profile_source_row_template_not_scoreable",
        },
        {
            "profile_id": "QPROF1352_1_theorem_zero_slot",
            "profile_object": "q_loc^nu theorem-zero certificate",
            "expression": "q_loc^nu=0 only if S_GK, K_metric match, P_loc owner, E_A=0, J_ext=0, B_boundary=0, and projector commutator=0",
            "required_inputs": "all theorem premises with source paths",
            "units_required": "certificate replaces numeric profile only after all premises pass",
            "source_path_required": "parent-signed theorem bundle",
            "current_missing": "MISSING_PARENT_SIGNED_THEOREM_BUNDLE",
            "row_status": "certificate_slot_only_not_claim",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1352_0_conjugacy_action",
            "claim": "response/displacement action is parent-owned",
            "allowed_if": "component lock, M_AB owner, no-linear-source theorem, metric response match, P_loc, and boundary all pass",
            "current_status": "BLOCKED",
            "reason": "template exists but is not live MTS proof",
        },
        {
            "gate_id": "GATE1352_1_Bmem_or_q_loc_zero",
            "claim": "B_mem=0 or q_loc=0 follows from conjugacy",
            "allowed_if": "Z=physical residual and source/boundary terms vanish",
            "current_status": "BLOCKED",
            "reason": "component lock and no-linear-source theorem are missing",
        },
        {
            "gate_id": "GATE1352_2_local_GR",
            "claim": "local GR/PPN/R10 pass",
            "allowed_if": "conjugacy proof closes or QPROF rows become numeric and below bounds",
            "current_status": "BLOCKED",
            "reason": "QPROF rows are templates only",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1352_0_best_route_survives",
            "decision": "The response/displacement route remains the best derivation path because it can make Gamma_eff and K_hat one variational object.",
            "why": "It gives exact double-zero and Ward-residual structure under clear premises.",
            "next_action": "attack component lock and no-linear-source theorem rather than jump straight to empirical scoring",
        },
        {
            "decision_id": "DEC1352_1_not_claimable",
            "decision": "The route is not claimable yet.",
            "why": "the core blocker is not algebra; it is ownership of the coupling map and absence of linear sources",
            "next_action": "keep all R10/PPN/local rows valid_for_claim=false",
        },
        {
            "decision_id": "DEC1352_2_profile_row_staged",
            "decision": "A first q_loc profile source row now exists for the fallback route.",
            "why": "if derivation fails, this row identifies exactly which residual pieces need numeric/source input",
            "next_action": "fill QPROF1352_0 only with real parent/profile data",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1352_0_1353",
            "target_file": "1353-Y5-R10-RAB-Z-component-lock-and-no-linear-source-theorem-or-JZ-source-pack.md",
            "target_script": "scripts/Y5_R10_RAB_Z_component_lock_and_no_linear_source_theorem_or_JZ_source_pack.py",
            "task": "try to prove Z^A is the physical local residual vector and that exchange-odd linear source terms J_Z/B_Z vanish; if not, stage J_Z/B_Z/Y5/Y6 source-pack rows",
            "success_condition": "either component-lock plus no-linear-source theorem, or explicit nonclaim source-pack rows for the live coupling obstruction",
            "do_not": "do not count formal double-zero as physical q_loc zero; do not ignore Y5/Y6; do not edit formalization-workbench or use GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate_outputs(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    identities: list[dict[str, object]],
    blockers: list[dict[str, object]],
    profiles: list[dict[str, object]],
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
        "VAL1352_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in action if row["template_id"] == "RDA1352_5_verdict")
    add(
        "VAL1352_1_action_template_nonclaim",
        "response/displacement action template is written but not promoted",
        verdict["current_status"] == "PROMISING_TEMPLATE_NOT_LIVE_PROOF" and not verdict["claim_allowed"],
        str(verdict["required_parent_clause"]),
    )

    add(
        "VAL1352_2_metric_identities_conditional",
        "metric-response identities are conditional and not symbol-matched",
        any(row["identity_id"] == "MRI1352_1_metric_response" and row["current_status"] == "FORMAL_IDENTITY_NOT_SYMBOL_MATCHED" for row in identities)
        and any(row["identity_id"] == "MRI1352_4_verdict" and row["current_status"] == "NO_LOCAL_GR_PROMOTION" for row in identities),
        "MRI1352_1 and MRI1352_4 present",
    )

    blocker_verdict = next(row for row in blockers if row["blocker_id"] == "BLK1352_5_verdict")
    add(
        "VAL1352_3_blockers_open",
        "conjugacy blocker verdict stays open",
        blocker_verdict["status"] == "CONJUGACY_ACTION_NOT_LIVE",
        str(blocker_verdict["next_attack"]),
    )

    add(
        "VAL1352_4_profile_rows_staged",
        "q_loc profile source rows are staged and nonclaim",
        any(row["profile_id"] == "QPROF1352_0_minimal_residual_source" for row in profiles)
        and all(not row["claim_allowed"] and "not" in str(row["row_status"]).lower() for row in profiles),
        f"rows={len(profiles)}",
    )

    add(
        "VAL1352_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all(row["current_status"] == "BLOCKED" and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['current_status']}" for row in gates),
    )

    all_rows = sources + action + identities + blockers + profiles + gates + decisions + next_target
    add(
        "VAL1352_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in (
            "*P8_Y5_R10_1352*",
            "*1352-Y5-R10-RAB-response-displacement*",
            "*Y5_R10_RAB_response_displacement*",
        ):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1352_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1352_8_next_target_1353",
        "next target routes to component lock and no-linear-source theorem",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1353-Y5-R10-RAB-Z-component-lock"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1352_9_overall",
        "overall 1352 validation",
        all(row["status"] == "PASS" for row in validations),
        "1352 keeps the conjugacy route alive while refusing local-GR promotion",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    identities: list[dict[str, object]],
    blockers: list[dict[str, object]],
    profiles: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1352 constructs the response/displacement conjugacy action as the best live derivation route, but it remains a template rather than a proof. The algebra gives the desired double-zero condition; the physical coupling map is still the missing beast.",
            "**Main progress:** the blocker has sharpened: not `can a quadratic response action make F1 vanish?` — yes, conditionally. The real question is whether `Z^A` is the actual local residual vector and whether exchange-odd linear source terms `J_Z/B_Z`, especially Y5/Y6, are forbidden by the parent theory.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Response/displacement action template",
            table(["template_id", "object", "definition", "required_parent_clause", "current_status"], action),
            "## Metric-response identity audit",
            table(["identity_id", "identity", "derived_under_template", "physical_payoff", "current_gap", "current_status"], identities),
            "## Conjugacy blocker audit",
            table(["blocker_id", "required_close", "evidence", "status", "next_attack"], blockers),
            "## q_loc profile source rows",
            table(["profile_id", "profile_object", "expression", "current_missing", "row_status", "claim_allowed"], profiles),
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
    action = action_template()
    identities = identity_audit()
    blockers = blocker_audit()
    profiles = qloc_profile_source_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, action, identities, blockers, profiles, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ACTION_TEMPLATE_PATH, action)
    write_csv(IDENTITY_AUDIT_PATH, identities)
    write_csv(BLOCKER_PATH, blockers)
    write_csv(QLOC_PROFILE_PATH, profiles)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, action, identities, blockers, profiles, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
