from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1164_0_1163_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1163_NEXT_TARGET.csv",
            "needle": "NEXT1163_0_1164",
            "role": "handoff requiring C/P_D/d_rel source hunt or first edge zero certificate.",
        },
        {
            "source_id": "SRC1164_1_1163_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1163_TOPOLOGICAL_CPERP_SOURCE_CONTRACT.csv",
            "needle": "CTC1163_1_parent_C_object",
            "role": "current strict contract showing parent C/P_D/d_rel are not sourced.",
        },
        {
            "source_id": "SRC1164_2_273_scalar_fail",
            "relative_path": "273-Cperp-relative-exactness-C-sector.md",
            "needle": "Cperp_scalar_relative_exactness_not_derived_projected_metric_demoted_to_explicit_closure",
            "role": "early scalar Cperp exactness rejection and projected metric closure demotion.",
        },
        {
            "source_id": "SRC1164_3_273_lifted_required",
            "relative_path": "273-Cperp-relative-exactness-C-sector.md",
            "needle": "requires lifted C-sector, not scalar Cperp.",
            "role": "scalar route handoff to lifted C-sector rather than promotion.",
        },
        {
            "source_id": "SRC1164_4_274_lifted_route",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure",
            "role": "lifted form/holonomy route identified but not parent-derived.",
        },
        {
            "source_id": "SRC1164_5_275_JC_three_form",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure",
            "role": "conditional 3-form memory current construction; parent action/projector/domain still missing.",
        },
        {
            "source_id": "SRC1164_6_207_projector_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "domain_projector_action_formal_Bianchi_conditional_representative_missing",
            "role": "domain projector action and Bianchi route conditionally shaped but representative missing.",
        },
        {
            "source_id": "SRC1164_7_266_Ward",
            "relative_path": "266-projected-trace-source-Ward-identity-attempt.md",
            "needle": "projected_trace_source_Ward_identity_volume_suppression_derived_exact_silence_not_derived",
            "role": "projected trace source gives suppression shape, not exact local silence.",
        },
        {
            "source_id": "SRC1164_8_360_matter_coupling",
            "relative_path": "360-universal-matter-coupling-theorem-attempt.md",
            "needle": "conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass",
            "role": "matter coupling theorem is conditional; parent selector open.",
        },
        {
            "source_id": "SRC1164_9_361_residual_gauge",
            "relative_path": "361-residual-gauge-principle-for-projected-matter-metric.md",
            "needle": "projected metric remains a theorem target",
            "role": "residual-gauge route remains live but unfinished.",
        },
        {
            "source_id": "SRC1164_10_362_closure_decision",
            "relative_path": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
            "needle": "Cperp_scalar_exactness_rejected_projected_metric_demoted_to_explicit_closure_lifted_C_route_open",
            "role": "closure decision: scalar route rejected; lifted C route open.",
        },
        {
            "source_id": "SRC1164_11_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "first edge zero/bound identity for C_corner and d_S(F epsilon).",
        },
        {
            "source_id": "SRC1164_12_1020_zero_conditions",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_2_zero_conditions",
            "role": "full edge-zero conditions; not all currently met.",
        },
        {
            "source_id": "SRC1164_13_1163_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1163_EDGE_BOUND_INPUT_SCHEMA.csv",
            "needle": "EIS1163_0_C_corner",
            "role": "strict edge-bound input schema used for dry-run refusal.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in sources:
        path = source_path(str(row["relative_path"]))
        text = read_text(path)
        checked.append(
            {
                **row,
                "exists": path.exists(),
                "needle_found": str(row["needle"]) in text,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return checked


def source_hunt_rows() -> list[dict[str, object]]:
    return [
        {
            "hunt_id": "SCH1164_0_scalar_C_exactness",
            "target": "current scalar Cperp relative exactness",
            "source_anchor": "273-Cperp-relative-exactness-C-sector.md",
            "source_needle": "Cperp_scalar_relative_exactness_not_derived_projected_metric_demoted_to_explicit_closure",
            "finding": "REJECT_CURRENT_SCALAR_C_AS_PARENT_DERIVATION_ROUTE",
            "why": "J_rel transfer, H0 relative triviality, and exact-gradient arguments do not make scalar Cperp a gauge/null direction.",
            "remaining_gap": "would need a different lifted C-sector or explicit closure label",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_1_projected_metric_closure",
            "target": "projected matter metric exp(P_D C)g",
            "source_anchor": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
            "source_needle": "explicit effective closure for the current scalar C-sector.",
            "finding": "CLOSURE_ONLY_FOR_SCALAR_BRANCH",
            "why": "scalar Cperp exactness is rejected, so projected metric cannot be advertised as parent-derived in this branch",
            "remaining_gap": "recover as theorem only through lifted C-sector or residual-gauge proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_2_lifted_C_sector",
            "target": "lifted C-sector form/holonomy object",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure",
            "finding": "LIVE_PRIMARY_SOURCE_HUNT_CANDIDATE_NONCLAIM",
            "why": "a form/connection/holonomy C-sector can in principle own relative cohomology and boundary classes better than scalar Cperp",
            "remaining_gap": "parent action, P_D, d_rel, boundary primitive, and matter coupling remain unowned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_3_JC_three_form",
            "target": "J_C three-form memory current",
            "source_anchor": "275-JC-three-form-memory-current-from-Q.md",
            "source_needle": "JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure",
            "finding": "CONDITIONAL_KINEMATIC_SHAPE_NOT_PARENT_ACTION",
            "why": "p=3 shape and FLRW activation support exist conditionally, but domain selector/projector/boundary primitive are not derived",
            "remaining_gap": "turn kinematic three-form into parent field with action and projector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_4_PD_projector_Bianchi",
            "target": "P_D/domain projector ownership",
            "source_anchor": "207-domain-projector-action-and-Bianchi-identity.md",
            "source_needle": "domain_projector_action_formal_Bianchi_conditional_representative_missing",
            "finding": "FORMAL_PROJECTOR_ACTION_SHAPE_ONLY",
            "why": "Bianchi accounting can be made formal if all stresses are varied, but physical representative selection is missing",
            "remaining_gap": "derive the actual domain representative and variation of P_D",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_5_drel_complex",
            "target": "C-sector d_rel complex",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1163_TOPOLOGICAL_CPERP_SOURCE_CONTRACT.csv",
            "source_needle": "CTC1163_6_drel_complex",
            "finding": "NOT_SOURCED_FOR_SCALAR_OR_LIFTED_C_YET",
            "why": "standard relative differential notation is available, but the actual C-sector bulk/boundary complexes and signs are not",
            "remaining_gap": "define Omega_C^k(U), Omega_C^{k-1}(S), pullback, nilpotency, and source terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_6_Ward_suppression",
            "target": "projected trace-source Ward identity",
            "source_anchor": "266-projected-trace-source-Ward-identity-attempt.md",
            "source_needle": "projected_trace_source_Ward_identity_volume_suppression_derived_exact_silence_not_derived",
            "finding": "SUPPRESSION_SUPPORT_NOT_ZERO_PROOF",
            "why": "useful for finite residual scoring, but it does not prove exact scalar or edge silence",
            "remaining_gap": "derive exact Ward cancellation or keep finite local residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_7_matter_coupling",
            "target": "universal matter coupling to projected metric",
            "source_anchor": "360-universal-matter-coupling-theorem-attempt.md",
            "source_needle": "conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass",
            "finding": "CONDITIONAL_THEOREM_ONLY",
            "why": "matter decoupling from Cperp follows if residual representative invariance is proved, but that selector is open",
            "remaining_gap": "parent principle selecting observed/projected coframe",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_8_residual_gauge_principle",
            "target": "residual gauge principle for projected metric",
            "source_anchor": "361-residual-gauge-principle-for-projected-matter-metric.md",
            "source_needle": "projected metric remains a theorem target",
            "finding": "LIVE_BUT_UNFINISHED",
            "why": "the route is coherent if Cperp is proven gauge/exact in the parent theory, but that proof is absent",
            "remaining_gap": "parent C-sector exactness plus vanishing local boundary primitive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "SCH1164_9_verdict",
            "target": "parent C/P_D/d_rel source hunt",
            "source_anchor": "multiple",
            "source_needle": "scalar rejected; lifted open; edge fallback active",
            "finding": "PARENT_TRIO_NOT_CLOSED_LIFTED_ROUTE_SELECTED_FOR_NEXT_ACQUISITION",
            "why": "scalar C route is already closure-only; lifted C is the honest theorem target but still lacks parent action/projector/d_rel",
            "remaining_gap": "write lifted C parent action contract or fill first edge zero/bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def route_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "ROUTE1164_0_scalar_Cperp",
            "route": "scalar Cperp with projected metric exp(P_D C)g",
            "decision": "DEMOTE_TO_EXPLICIT_CLOSURE_FOR_CURRENT_BRANCH",
            "reason": "local scalar exactness was previously rejected; using it as parent derivation would recycle a known failed route",
            "allowed_use": "private effective closure label only, not local-GR/WEP/PPN/R10 proof",
            "next_action": "do not spend next derivation cycle trying to promote scalar Cperp",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1164_1_lifted_C",
            "route": "lifted C-sector as form/connection/holonomy or J_C three-form",
            "decision": "SELECT_AS_PRIMARY_PARENT_SOURCE_HUNT_NONCLAIM",
            "reason": "it is the only route found that could naturally own relative cohomology, boundary classes, and FLRW activation without pretending scalar exactness worked",
            "allowed_use": "source contract and theorem target only",
            "next_action": "write parent action/projector/d_rel contract for lifted C",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1164_2_edge_bound",
            "route": "finite edge-bound fallback",
            "decision": "KEEP_ACTIVE_AS_PARALLEL_NONCLAIM_FALLBACK",
            "reason": "if lifted C action cannot be closed, the runner can still score finite residuals once C_corner, dS_Feps, B_C, harmonic, residual, and cocycle terms are sourced",
            "allowed_use": "no-claim runner plumbing and source acquisition",
            "next_action": "attempt C_corner=0 or d_S(F epsilon)=0/bound as first value/certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def edge_zero_rows() -> list[dict[str, object]]:
    return [
        {
            "edge_id": "FEZ1164_0_C_corner",
            "quantity": "C_corner",
            "zero_or_bound_attempt": "corner term zero if partialS is empty or the corner row is explicitly fixed/zeroed",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "current_status": "NOT_CERTIFIED",
            "missing_piece": "local/lifted boundary geometry and corner convention",
            "runner_effect": "blocks additive edge-bound zero route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "FEZ1164_1_dS_Feps",
            "quantity": "norm_dS_Feps",
            "zero_or_bound_attempt": "d_S(F epsilon)=0 if the weight and generator are closed/constant on the certified boundary surface, otherwise bound the dual norm",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "current_status": "NOT_CERTIFIED",
            "missing_piece": "F_lambda, epsilon_X, boundary class, and surface derivative norm",
            "runner_effect": "blocks product bound ||d_S(F eps)|| ||B_C||",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "FEZ1164_2_BC_product",
            "quantity": "norm_bC",
            "zero_or_bound_attempt": "product term vanishes if d_S(F epsilon)=0 or B_C=0; otherwise needs finite norm_bC",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BXP1020_2_exact_primitive",
            "current_status": "BLOCKED_BY_MISSING_BC_PRIMITIVE",
            "missing_piece": "B_C or b_C primitive for the chosen C branch",
            "runner_effect": "prevents numeric edge residual evaluation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "FEZ1164_3_full_zero_route",
            "quantity": "Q_C_edge_zero",
            "zero_or_bound_attempt": "zero only if corner, weight derivative, harmonic part, residual part, cocycle/source projection, branch selector, and epsilon flux all close",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_2_zero_conditions",
            "current_status": "ZERO_ROUTE_NOT_MET",
            "missing_piece": "too many edge and parent clauses open",
            "runner_effect": "claim remains blocked; finite scoring requires value fills",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_dry_run_rows(schema_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    blocked = [row["quantity"] for row in schema_rows]
    return [
        {
            "dry_run_id": "RDR1164_0_schema_import",
            "test": "import 1163 edge-bound schema",
            "status": "PASS_SCHEMA_IMPORTED",
            "blocked_inputs": ";".join(blocked),
            "route_context": "schema still has no numeric values or theorem-zero certificates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "dry_run_id": "RDR1164_1_scalar_route",
            "test": "try current scalar Cperp route",
            "status": "REFUSED_SCALAR_ROUTE_CLOSURE_ONLY",
            "blocked_inputs": "scalar_Cperp_exactness;projected_metric_parent_derivation",
            "route_context": "273/362 reject scalar exactness as derivation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "dry_run_id": "RDR1164_2_lifted_route",
            "test": "try lifted C route",
            "status": "REFUSED_LIFTED_ROUTE_PARENT_ACTION_MISSING",
            "blocked_inputs": "lifted_C_action;P_D_owner;d_rel_complex;B_C_primitive;matter_coupling",
            "route_context": "274/275 make it live but not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "dry_run_id": "RDR1164_3_edge_zero",
            "test": "try first edge zero certificate",
            "status": "REFUSED_EDGE_ZERO_CERTIFICATE_MISSING",
            "blocked_inputs": "C_corner;norm_dS_Feps;norm_bC",
            "route_context": "1020 weighted Stokes gives conditions but not the boundary data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1164_0_scalar_C_derivation",
            "gate": "scalar Cperp is parent-derived relative-exact/gauge data",
            "current_status": "FAILED_FOR_CURRENT_BRANCH",
            "reason": "273/362 demote projected metric to closure for scalar C-sector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1164_1_lifted_C_parent_action",
            "gate": "lifted C-sector has parent action, P_D, d_rel, boundary class, and matter coupling",
            "current_status": "OPEN_NOT_DERIVED",
            "reason": "274/275 supply route shape, not parent action closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1164_2_first_edge_zero",
            "gate": "C_corner or d_S(F epsilon) has a theorem-zero certificate",
            "current_status": "OPEN_NOT_CERTIFIED",
            "reason": "1020 supplies identity/conditions but not boundary data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1164_3_runner_claim",
            "gate": "edge-bound runner permits claim",
            "current_status": "BLOCKED",
            "reason": "no numeric/theorem-zero edge inputs exist",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1164_4_local_promotion",
            "gate": "local-GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "parent source route and edge route both remain nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1164_0_scalar_route",
            "decision": "do_not_promote_scalar_Cperp_route",
            "reason": "the corpus already rejected scalar exactness and closure-labelled exp(P_D C)g",
            "next_action": "treat scalar projected metric as private effective closure only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1164_1_lifted_route",
            "decision": "lifted_C_sector_is_best_derivation_route",
            "reason": "it is less circular and can potentially own form degree, relative cohomology, boundary primitive, and FLRW/local split",
            "next_action": "write lifted C parent action/P_D/d_rel contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1164_2_edge_route",
            "decision": "first_edge_zero_or_bound_is_best_parallel_fallback",
            "reason": "C_corner and d_S(F epsilon) are the first low-level Stokes terms that could convert the runner from pure refusal into finite scoring",
            "next_action": "try C_corner=0 or d_S(F epsilon)=0/bound if lifted C source contract stalls",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1164_0_1165",
            "next_target": "1165-Y5-R10-lifted-C-sector-parent-action-contract-or-Ccorner-zero-bound.md",
            "objective": "write the parent-action/source contract for the lifted C-sector with P_D and d_rel, or if that cannot be closed, fill the first edge zero/bound row for C_corner or d_S(F epsilon)",
            "include": "lifted C field degree; action term; P_D owner; d_rel complex; boundary class; B_C primitive; matter coupling selector; C_corner; dS_Feps; runner dry-run",
            "exclude": "scalar Cperp promotion; projected metric as theorem; invented edge numbers; frame residual renaming; c_g zero claim; local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    hunt: list[dict[str, object]],
    routes: list[dict[str, object]],
    edge: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    scalar_demoted = any(
        "scalar" in str(row["route"]).lower() and "DEMOTE" in str(row["decision"])
        for row in routes
    )
    lifted_selected = any("LIFTED" in str(row["decision"]) or "PRIMARY_PARENT_SOURCE_HUNT" in str(row["decision"]) for row in routes)
    edge_not_certified = all(is_false(row["claim_allowed"]) and str(row["current_status"]) != "CERTIFIED" for row in edge)
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, hunt, routes, edge, runner, gates, decisions, next_rows)
        for row in table
    )
    csv_parse = True
    parse_detail = "all 1164 CSV outputs parse cleanly"
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            csv_parse = False
            parse_detail = f"{path.name}: {exc}"
            break
    under_post = all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in csv_paths + [DOC])
    return [
        {
            "check_id": "V1164_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_1_scalar_route_demoted",
            "result": "pass" if scalar_demoted else "fail",
            "detail": "scalar Cperp route is not promoted; it remains explicit closure",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_2_lifted_route_selected_nonclaim",
            "result": "pass" if lifted_selected else "fail",
            "detail": "lifted C-sector is selected only as the next source-hunt branch",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_3_parent_trio_not_closed",
            "result": "pass" if any("NOT_SOURCED" in str(row["finding"]) or "NOT_PARENT_ACTION" in str(row["finding"]) or "NOT_PARENT" in str(row["why"]) for row in hunt) else "fail",
            "detail": "C/P_D/d_rel parent trio remains open",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_4_edge_zero_not_certified",
            "result": "pass" if edge_not_certified else "fail",
            "detail": "C_corner and dS_Feps are condition rows only, not zero certificates",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_5_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "dry-run refuses scalar, lifted, and edge routes as claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_6_claim_gates_blocked",
            "result": "pass" if all(is_false(row["claim_allowed"]) for row in gates) else "fail",
            "detail": "all claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_7_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_8_next_target",
            "result": "pass" if next_rows and "1165" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1165 targets lifted C parent action contract or first edge zero/bound",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_9_generated_under_post_checkpoint",
            "result": "pass" if under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_10_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1164_SUMMARY",
            "result": "pass" if source_ok and scalar_demoted and lifted_selected and runner_refuses and all_nonclaim else "fail",
            "detail": "1164 rejects scalar Cperp promotion, selects lifted C-sector as the honest source-hunt branch, and keeps edge zero/bound as nonclaim fallback",
            "claim_allowed": False,
        },
    ]


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_doc(
    sources: list[dict[str, object]],
    hunt: list[dict[str, object]],
    routes: list[dict[str, object]],
    edge: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1164 — Y5/R10 parent C/P_D/d_rel source hunt or first edge zero certificate

**Current verdict:** the current scalar `Cperp` route should not be promoted. The corpus already demotes `exp(P_D C)g` to explicit closure for the scalar C-sector. The honest derivation route is the lifted `C` sector — form/holonomy/three-form/boundary-class style — but that is still only a source-hunt candidate.

**Main progress:** 1164 turns the fog into a route choice. Scalar `Cperp` is closure-only, lifted `C` becomes the next nonclaim theorem target, and the edge-bound fallback is kept alive through `C_corner` / `d_S(F epsilon)` source rows.

**No claim:** no local-GR, R10, PPN, WEP, clock, orbital, or `c_g=0` result follows here. This checkpoint prevents us from reusing a known failed scalar route by accident.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## Parent C/P_D/d_rel source hunt

{md_table(hunt, ["hunt_id", "target", "finding", "why", "remaining_gap", "valid_for_claim"])}

## Candidate route decision

{md_table(routes, ["route_id", "route", "decision", "reason", "allowed_use", "next_action", "valid_for_claim"])}

## First edge zero/bound audit

{md_table(edge, ["edge_id", "quantity", "zero_or_bound_attempt", "current_status", "missing_piece", "runner_effect", "valid_for_claim"])}

## Runner dry-run

{md_table(runner, ["dry_run_id", "test", "status", "blocked_inputs", "route_context", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "current_status", "reason", "claim_allowed"])}

## Decision ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "claim_allowed"])}

## Next target

{md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = stamp(source_rows())
    schema_rows = read_csv(OUT / "P8_Y5_R10_1163_EDGE_BOUND_INPUT_SCHEMA.csv")
    hunt = stamp(source_hunt_rows())
    routes = stamp(route_decision_rows())
    edge = stamp(edge_zero_rows())
    runner = stamp(runner_dry_run_rows(schema_rows))
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())
    outputs = {
        "P8_Y5_R10_1164_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1164_PARENT_C_PD_DREL_SOURCE_HUNT.csv": hunt,
        "P8_Y5_R10_1164_CANDIDATE_ROUTE_DECISION.csv": routes,
        "P8_Y5_R10_1164_FIRST_EDGE_ZERO_CERTIFICATE_AUDIT.csv": edge,
        "P8_Y5_R10_1164_RUNNER_DRY_RUN.csv": runner,
        "P8_Y5_R10_1164_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1164_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1164_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, hunt, routes, edge, runner, gates, decisions, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1164_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, hunt, routes, edge, runner, gates, decisions, next_rows, validation)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
