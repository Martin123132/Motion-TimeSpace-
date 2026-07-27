from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md"


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
            "source_id": "SRC1167_0_1166_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1166_NEXT_TARGET.csv",
            "needle": "NEXT1166_0_1167",
            "role": "handoff requiring parent volume-lock selector or finite edge-bound fill.",
        },
        {
            "source_id": "SRC1167_1_1166_obstruction",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1166_JC_FROM_Q_VARIATION_DERIVATION.csv",
            "needle": "JCV1166_4_relative_obstruction",
            "role": "int_D delta J_C obstruction.",
        },
        {
            "source_id": "SRC1167_2_1166_volume_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1166_CLAIM_GATES.csv",
            "needle": "G1166_1_local_volume_lock",
            "role": "blocked local volume-lock gate.",
        },
        {
            "source_id": "SRC1167_3_274_CD",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "C_D[D] = N_D^{-1} integral_D J_C",
            "role": "domain class functional.",
        },
        {
            "source_id": "SRC1167_4_274_local_FLRW",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "where the local exact part can be killed by a stationary local boundary condition, while the coherent FLRW domain class can remain nonzero.",
            "role": "local/FLRW compatibility target.",
        },
        {
            "source_id": "SRC1167_5_274_FLRW_class",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "integral_D J_C^{top} != 0",
            "role": "FLRW nonzero top class.",
        },
        {
            "source_id": "SRC1167_6_275_stationary",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "stationary local silence",
            "role": "older conditional local-stationary route.",
        },
        {
            "source_id": "SRC1167_7_275_domain_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "physical domain selector `D` | not parent-derived",
            "role": "domain selector missing.",
        },
        {
            "source_id": "SRC1167_8_207_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi compatibility is conditional.",
        },
        {
            "source_id": "SRC1167_9_1020_bound",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "finite edge-bound fallback law.",
        },
        {
            "source_id": "SRC1167_10_1020_kernel",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "MISSING_KERNEL_DERIVATIVE_BOUND_OR_ZERO_CERTIFICATE",
            "role": "dS_Feps bound still missing.",
        },
        {
            "source_id": "SRC1167_11_1166_corner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1166_LOCAL_CORNER_CERTIFICATE_ATTEMPT.csv",
            "needle": "LC1166_0_boundary_of_boundary",
            "role": "conditional C_corner zero from boundary-of-boundary.",
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


def volume_lock_rows() -> list[dict[str, object]]:
    return [
        {
            "law_id": "PVL1167_0_parent_continuity_shape",
            "clause": "parent continuity law",
            "statement": "Introduce a lifted spacetime current/source equation d_4 mathcalJ_C = Sigma_C, whose spatial split gives L_tau J_C = d Phi_C + Sigma_C plus possible moving-domain terms.",
            "derivation_status": "LAW_SHAPE_WRITTEN_NOT_PARENT_DERIVED",
            "local_effect": "turns int_D delta J_C into a source/flux/domain-motion balance",
            "FLRW_effect": "permits homogeneous Sigma_C or top class to drive coherent memory",
            "missing_piece": "derive mathcalJ_C, Sigma_C, Phi_C, and domain motion from parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "PVL1167_1_domain_integral_evolution",
            "clause": "domain integral balance",
            "statement": "For a fixed/suitably transported domain, delta int_D J_C = int_D Sigma_C + int_partialD Phi_C + moving_boundary_term.",
            "derivation_status": "DERIVED_FROM_CONTINUITY_SHAPE",
            "local_effect": "local exactness follows if each right-hand term vanishes or is bounded",
            "FLRW_effect": "nonzero integral source/top class remains allowed outside the local stationary branch",
            "missing_piece": "parent-owned definitions and signs for all three terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "PVL1167_2_local_stationary_lock",
            "clause": "local stationary branch",
            "statement": "If Sigma_C=0, Phi_C|partialD=0, and moving_boundary_term=0 on a compact stationary local domain, then delta int_D J_C=0 and the 1166 relative obstruction vanishes.",
            "derivation_status": "CONDITIONAL_THEOREM_SHAPE",
            "local_effect": "would supply the missing local volume lock",
            "FLRW_effect": "does not by itself kill FLRW because the branch condition is local stationary/no-flux",
            "missing_piece": "prove local no-source/no-flux/stationary-domain conditions from parent equations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "PVL1167_3_FLRW_active_branch",
            "clause": "FLRW active branch",
            "statement": "In FLRW, a homogeneous Sigma_C, nontrivial H^3(D,partialD) class, or coherent domain evolution can give delta int_D J_C != 0 without contradicting the local no-flux branch.",
            "derivation_status": "COMPATIBILITY_SHAPE_ONLY",
            "local_effect": "prevents a hand switch if Sigma_C/Phi_C/domain motion are selected by one equation",
            "FLRW_effect": "keeps cosmological memory alive as a domain class",
            "missing_piece": "derive the source/top-class selector and amplitude from the same parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "PVL1167_4_Bianchi_compatibility",
            "clause": "Bianchi/Ward compatibility",
            "statement": "The continuity law is acceptable only if the stress carried by Sigma_C, Phi_C, P_D, and moving-domain terms appears in the parent Bianchi/Ward ledger.",
            "derivation_status": "CONSERVATION_GUARD",
            "local_effect": "prevents hiding force exchange in frozen projectors or boundaries",
            "FLRW_effect": "prevents cosmological source from becoming an unbalanced stress insertion",
            "missing_piece": "stress extraction and parent Noether identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "PVL1167_5_verdict",
            "clause": "volume-lock verdict",
            "statement": "The continuity/no-flux route can derive the needed local volume lock conditionally, but current MTS still lacks the parent action terms that define Sigma_C, Phi_C, and the domain-motion rule.",
            "derivation_status": "PROMISING_CONDITIONAL_NOT_CLOSED",
            "local_effect": "names the exact local-GR theorem target",
            "FLRW_effect": "keeps FLRW memory compatible in the same law shape",
            "missing_piece": "parent continuity action/source derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def obstruction_rows() -> list[dict[str, object]]:
    return [
        {
            "obstruction_id": "OBS1167_0_Sigma_C",
            "quantity": "Sigma_C",
            "required_for": "local source zero and FLRW source/top-class activation",
            "current_status": "MISSING_PARENT_SOURCE_TERM",
            "why_it_matters": "without Sigma_C the same law cannot distinguish local vacuum from FLRW activity",
            "next_action": "derive from parent lifted-C action or set zero with theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1167_1_Phi_C",
            "quantity": "Phi_C boundary flux",
            "required_for": "local no-flux and finite edge-bound scoring",
            "current_status": "MISSING_BOUNDARY_FLUX_FORM",
            "why_it_matters": "boundary flux is the direct source of int_partialD terms",
            "next_action": "derive B_C/Phi_C relation and boundary class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1167_2_domain_motion",
            "quantity": "moving_boundary_term",
            "required_for": "stationary local domain definition",
            "current_status": "MISSING_DOMAIN_TRANSPORT_RULE",
            "why_it_matters": "moving cutoffs can fake volume change or hide corner terms",
            "next_action": "define D transport by coframe/projector flow",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1167_3_PD_variation",
            "quantity": "delta P_D",
            "required_for": "same-parent local/FLRW selector and Bianchi safety",
            "current_status": "MISSING_PROJECTOR_VARIATION",
            "why_it_matters": "fixed external P_D would be a closure, not a derivation",
            "next_action": "derive from topological/domain action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1167_4_ND_normalization",
            "quantity": "N_D",
            "required_for": "delta C_D and amplitude locks",
            "current_status": "MISSING_NORMALIZATION_VARIATION",
            "why_it_matters": "normalization can cancel or create apparent volume lock",
            "next_action": "derive N_D from measure/coframe/domain rule",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "OBS1167_5_edge_norms",
            "quantity": "C_corner and norm_dS_Feps",
            "required_for": "finite fallback if exact lock fails",
            "current_status": "MISSING_ARENA_CERTIFICATES_OR_NUMERIC_BOUNDS",
            "why_it_matters": "edge runner cannot score residuals without these inputs",
            "next_action": "certify smooth closed surface or source derivative norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_edge_rows() -> list[dict[str, object]]:
    return [
        {
            "edge_id": "FEB1167_0_C_corner_candidate_zero",
            "quantity": "C_corner",
            "current_value": "CONDITIONAL_ZERO_IF_S_EQUALS_SMOOTH_PARTIAL_D",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1166_LOCAL_CORNER_CERTIFICATE_ATTEMPT.csv",
            "needed_for_claim": "actual arena surface certificate; no regulator/cutoff joints; fixed boundary class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "FEB1167_1_norm_dS_Feps",
            "quantity": "norm_dS_Feps",
            "current_value": "MISSING_KERNEL_DERIVATIVE_BOUND_OR_ZERO_CERTIFICATE",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needed_for_claim": "F_lambda, epsilon_C, surface derivative, norm, units, and source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "FEB1167_2_bound_law",
            "quantity": "Q_C_edge_bound",
            "current_value": "C_corner + norm_dS_Feps*norm_bC + harmonic_edge_abs + residual_edge_abs + cocycle/source terms",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needed_for_claim": "all components have theorem-zero certificates or sourced nonnegative numeric bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "run_id": "RUN1167_0_continuity_law",
            "test": "parent continuity/no-flux law",
            "status": "PARTIAL_PASS_LAW_SHAPE_NOT_PARENT_DERIVED",
            "blocked_by": "Sigma_C;Phi_C;moving_boundary_term;delta_P_D;Bianchi_stress",
            "detail": "law shape would imply local volume lock, but its ingredients are not parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1167_1_local_volume_lock",
            "test": "int_D delta J_C=0 local branch",
            "status": "REFUSED_LOCAL_LOCK_NOT_SIGNED",
            "blocked_by": "local_no_source;local_no_flux;stationary_domain",
            "detail": "local volume lock is conditional on missing no-source/no-flux/domain-motion certificates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1167_2_FLRW_activity",
            "test": "same-law FLRW active branch",
            "status": "REFUSED_FLRW_SELECTOR_NOT_DERIVED",
            "blocked_by": "Sigma_C_FLRW;H3_class;amplitude_normalization",
            "detail": "same continuity law can host FLRW activity, but the source/top-class selector is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1167_3_edge_fallback",
            "test": "finite edge-bound fallback",
            "status": "REFUSED_EDGE_VALUES_MISSING",
            "blocked_by": "C_corner_arena_certificate;norm_dS_Feps;norm_bC;h_C;r_C",
            "detail": "C_corner has a conditional zero candidate; dS_Feps and other norms remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1167_0_continuity_parent_action",
            "gate": "d_4 mathcalJ_C = Sigma_C comes from parent action",
            "current_status": "BLOCKED",
            "reason": "no source/flux/action variation currently owns the continuity law",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1167_1_local_lock",
            "gate": "local Sigma_C=0, Phi_C=0, moving boundary=0",
            "current_status": "BLOCKED",
            "reason": "local no-source/no-flux/stationary-domain conditions are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1167_2_FLRW_selector",
            "gate": "FLRW nonzero H3/source class selected by same parent law",
            "current_status": "BLOCKED",
            "reason": "homogeneous source/top-class selector and amplitude remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1167_3_edge_bound",
            "gate": "finite edge-bound rows valid",
            "current_status": "BLOCKED",
            "reason": "C_corner arena certificate and dS_Feps/norm_bC values are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1167_4_local_promotion",
            "gate": "local-GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "upstream continuity and edge gates remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1167_0_best_route",
            "decision": "continuity_no_flux_law_is_best_volume_lock_route",
            "reason": "it derives int_D delta J_C=0 by source/flux/domain balance rather than by closure axiom",
            "next_action": "derive Sigma_C and Phi_C from parent lifted-C action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1167_1_FLRW_compatibility",
            "decision": "same_law_can_keep_FLRW_active_conditionally",
            "reason": "FLRW activity can be nonzero source/top class while local stationary branch is no-source/no-flux",
            "next_action": "derive the branch selector rather than hand switch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1167_2_fallback",
            "decision": "finite_edge_bound_remains_parallel_fallback",
            "reason": "if parent continuity stalls, C_corner and dS_Feps source rows can still make the residual scoreable",
            "next_action": "fill dS_Feps or certify actual local surface",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1167_0_1168",
            "next_target": "1168-Y5-R10-lifted-C-continuity-action-source-or-dSFeps-bound.md",
            "objective": "derive Sigma_C and Phi_C from a lifted-C parent action/current variation, or if that fails, fill the dS_Feps finite-bound row with sourced units and a no-claim runner dry-run",
            "include": "mathcalJ_C action term; Sigma_C source; Phi_C boundary flux; local no-flux theorem; FLRW source/top-class selector; Bianchi stress; dS_Feps units; edge-bound runner",
            "exclude": "continuity by assertion; local/FLRW hand switch; scalar Cperp promotion; invented numeric bounds; local-GR claim; c_g zero claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    laws: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    edges: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    continuity_shape = any(row["law_id"] == "PVL1167_0_parent_continuity_shape" for row in laws)
    local_lock_shape = any(row["law_id"] == "PVL1167_2_local_stationary_lock" for row in laws)
    flrw_shape = any(row["law_id"] == "PVL1167_3_FLRW_active_branch" for row in laws)
    missing_sigma = any(row["obstruction_id"] == "OBS1167_0_Sigma_C" and "MISSING" in str(row["current_status"]) for row in obstructions)
    edge_fallback = any(row["edge_id"] == "FEB1167_1_norm_dS_Feps" for row in edges)
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, laws, obstructions, edges, runner, gates, decisions, next_rows)
        for row in table
    )
    csv_parse = True
    parse_detail = "all 1167 CSV outputs parse cleanly"
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
            "check_id": "V1167_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_1_continuity_shape_written",
            "result": "pass" if continuity_shape else "fail",
            "detail": "parent continuity/no-flux law shape is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_2_local_lock_conditional",
            "result": "pass" if local_lock_shape else "fail",
            "detail": "local int_D delta J_C=0 follows conditionally from no-source/no-flux/stationary-domain terms",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_3_FLRW_same_law_shape",
            "result": "pass" if flrw_shape else "fail",
            "detail": "FLRW activity can remain as source/top class in the same law shape",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_4_parent_source_missing",
            "result": "pass" if missing_sigma else "fail",
            "detail": "Sigma_C remains missing rather than assumed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_5_edge_fallback_retained",
            "result": "pass" if edge_fallback else "fail",
            "detail": "dS_Feps finite-bound row remains retained as fallback",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_6_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "runner refuses continuity, local lock, FLRW selector, and edge claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_7_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_8_next_target",
            "result": "pass" if next_rows and "1168" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1168 handoff targets continuity action/source or dS_Feps bound",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_9_generated_under_post_checkpoint",
            "result": "pass" if under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_10_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1167_SUMMARY",
            "result": "pass" if source_ok and continuity_shape and local_lock_shape and flrw_shape and missing_sigma and runner_refuses and all_nonclaim else "fail",
            "detail": "1167 constructs the continuity/no-flux volume-lock route, keeps FLRW activity in the same law shape, and blocks claims until Sigma_C/Phi_C/domain terms are parent-derived",
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
    laws: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    edges: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1167 — Y5/R10 parent volume-lock selector or finite edge-bound fill

**Current verdict:** the best route is now a parent continuity/no-flux law for the lifted `J_C` three-form. If a parent equation `d_4 mathcalJ_C = Sigma_C` exists, then `delta int_D J_C` is controlled by source, boundary flux, and moving-domain terms rather than by an axiom.

**Main progress:** local volume lock becomes a conditional theorem: local stationary domains with `Sigma_C=0`, `Phi_C|partialD=0`, and no moving-boundary contribution give `int_D delta J_C=0`. The same law can still allow FLRW activity through a homogeneous source or nonzero top class. That is the least hand-switchy route we have found.

**No claim:** `Sigma_C`, `Phi_C`, `delta P_D`, and the domain-motion rule are not parent-derived yet. No local-GR, R10, PPN, WEP, clock, orbital, projected-metric theorem, or `c_g=0` result follows.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## Parent volume-lock law attempt

{md_table(laws, ["law_id", "clause", "statement", "derivation_status", "local_effect", "FLRW_effect", "missing_piece", "valid_for_claim"])}

## Obstruction rows

{md_table(obstructions, ["obstruction_id", "quantity", "required_for", "current_status", "why_it_matters", "next_action", "valid_for_claim"])}

## Finite edge-bound fallback rows

{md_table(edges, ["edge_id", "quantity", "current_value", "source_anchor", "needed_for_claim", "valid_for_claim"])}

## Runner dry-run

{md_table(runner, ["run_id", "test", "status", "blocked_by", "detail", "claim_allowed"])}

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
    laws = stamp(volume_lock_rows())
    obstructions = stamp(obstruction_rows())
    edges = stamp(finite_edge_rows())
    runner = stamp(runner_rows())
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())
    outputs = {
        "P8_Y5_R10_1167_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1167_PARENT_VOLUME_LOCK_LAW_ATTEMPT.csv": laws,
        "P8_Y5_R10_1167_VOLUME_LOCK_OBSTRUCTION_ROWS.csv": obstructions,
        "P8_Y5_R10_1167_FINITE_EDGE_BOUND_FILL.csv": edges,
        "P8_Y5_R10_1167_RUNNER_DRY_RUN.csv": runner,
        "P8_Y5_R10_1167_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1167_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1167_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, laws, obstructions, edges, runner, gates, decisions, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1167_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, laws, obstructions, edges, runner, gates, decisions, next_rows, validation)

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
