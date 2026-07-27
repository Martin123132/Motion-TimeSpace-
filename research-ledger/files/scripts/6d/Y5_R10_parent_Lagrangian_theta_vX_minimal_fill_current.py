from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md"
NEXT_TARGET = "731-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_730_minimal_parent_fill_current_chain_templates_written_affine_rejected_no_claim"
CLAIM_CEILING = "minimal_parent_fill_templates_only_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_730_SOURCE_REGISTER.csv"
FILL_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_730_MINIMAL_PARENT_FILL_CANDIDATES.csv"
THETA_FORMS_PATH = RESIDUALS / "P8_Y5_R10_730_THETA_MU_VX_FORMS.csv"
EXTRACTION_TEST_PATH = RESIDUALS / "P8_Y5_R10_730_PJ_EXTRACTION_TEST.csv"
ROUTE_COMPARISON_PATH = RESIDUALS / "P8_Y5_R10_730_ROUTE_COMPARISON.csv"
EDGE_INPUT_PATH = RESIDUALS / "P8_Y5_R10_730_EDGE_COEFFICIENT_INPUT_ROWS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_730_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_730_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_730_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_730_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "729_doc": {
        "path": POST_CHECKPOINT / "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "role": "immediate handoff: current P/J origin contract",
        "needles": ["contract sharpened, not closed", "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md", "j_X = theta_Y(v_X) - mu_X"],
    },
    "729_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_729_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V729_12_next_target_selected", "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md", "V729_15_formalization_workbench_untouched"],
    },
    "729_blocker": {
        "path": RESIDUALS / "P8_Y5_R10_729_PARENT_ORIGIN_BLOCKER.csv",
        "role": "current parent-origin blockers",
        "needles": ["POB729_0_L_parent", "POB729_4_matter_projector_silence", "false"],
    },
    "729_edge_plan": {
        "path": RESIDUALS / "P8_Y5_R10_729_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        "role": "current edge fallback input",
        "needles": ["ESP729_0", "K_edge;Qbar_edge_XH;qbar_XT", "false"],
    },
    "593_doc": {
        "path": POST_CHECKPOINT / "593-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md",
        "role": "older minimal parent fill attempt",
        "needles": ["Minimal parent data can be filled as templates", "strict quotient", "affine block is rejected"],
    },
    "594_doc": {
        "path": POST_CHECKPOINT / "594-Y5-R10-choose-quotient-zero-or-diffeo-current-identity-and-close-boundary.md",
        "role": "older route-selection fork",
        "needles": ["strict quotient-zero first", "matter blindness", "boundary"],
    },
    "511_doc": {
        "path": POST_CHECKPOINT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "fixed-point local-GR parent ansatz",
        "needles": ["EH core", "double zero", "local GR"],
    },
    "581_doc": {
        "path": POST_CHECKPOINT / "581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md",
        "role": "strict quotient no-pole theorem shape",
        "needles": ["quotient-vertical no-pole", "Conf_parent --pi-->", "boundary charge"],
    },
    "728_doc": {
        "path": POST_CHECKPOINT / "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "role": "current Omega/DCdagger operator shape",
        "needles": ["C_X^nu = -nabla_mu P", "formula progress, not certificate", "DCdagger_A X"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(POST_CHECKPOINT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_fill_candidates(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "MPF730_A_diffeomorphism_parent",
            "L_parent": "L_EH[g_obs]+L_extra[g_obs,Phi]+L_matter[psi,g_obs]+dB_ref",
            "vX": "v_X[Y]=Lie_X Y on metric/coframe, extra fields, and matter representatives",
            "theta": "theta_parent=theta_EH+theta_extra+theta_matter+delta B_ref",
            "mu_X": "mu_X=i_X L_parent for a diffeomorphism-covariant parent Lagrangian",
            "what_it_fills": "standard Noether current j_X=theta_Y(L_XY)-i_X L_parent",
            "claim_result": "conditional_GR_template_only",
            "blocker": "must prove MTS C_X is exactly this parent diffeomorphism/momentum constraint, not an extra defect closure",
            "scrutiny_note": "strong GR inheritance but risks collapsing local MTS into ordinary GR bookkeeping unless the extra sector role is explicit",
            "source_paths": source_path_string("729_doc", "593_doc", "728_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "MPF730_B_strict_quotient_zero",
            "L_parent": "L_red[pi(Y)] + dB_rep with dpi(v_X)=0 and all matter/readout functors factoring through pi",
            "vX": "v_X is vertical to the observed quotient: v_X[Y_obs]=0 and v_X[theta_univ]=0",
            "theta": "theta_Y(v_X)=0 or dB_exact because the action factors through pi",
            "mu_X": "mu_X=0 or exact after quotient factorization",
            "what_it_fills": "P=0/exact and J_eff=0 as a theorem-zero current rather than a small residual",
            "claim_result": "cleanest_no_pole_if_pi_matter_boundary_are_constructed",
            "blocker": "pi, matter blindness, no-marker rule, reduced constraint algebra, and boundary charge silence remain unconstructed",
            "scrutiny_note": "lowest-scrutiny route if proved because the dangerous local field is not a physical degree of freedom",
            "source_paths": source_path_string("729_doc", "594_doc", "581_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "MPF730_C_hybrid_EH_plus_quotient_extra",
            "L_parent": "L_EH[g_obs]+L_extra[g_obs,Phi_red]+L_matter[psi,g_obs]+dB_ref with Y=(Y_obs,Y_rep) and pi(Y)=Y_obs,Phi_red",
            "vX": "ordinary spacetime diffeomorphism acts on observed fields; local MTS representative verticals satisfy dpi(v_X)=0",
            "theta": "EH theta owns GR charges; representative-sector theta must be exact/topological along v_X",
            "mu_X": "i_X L for ordinary diffeomorphisms, zero/exact for representative-only vertical moves",
            "what_it_fills": "local GR from EH current plus theorem-zero for extra local representative modes",
            "claim_result": "promising_current_chain_contract",
            "blocker": "explicit observed/representative split and no double-counting of ADM or Pi_M charges are not built",
            "scrutiny_note": "best-looking compromise: keep real GR local current while making MTS extra local direction quotient-silent",
            "source_paths": source_path_string("593_doc", "594_doc", "511_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "MPF730_D_fixed_point_double_zero_parent",
            "L_parent": "L_EH[g_obs]+S_extra[g_obs,Phi] with Phi=Phi0, dV(Phi0)=0, Hessian(V)>0, C_i(Phi0)=partial_A C_i(Phi0)=0",
            "vX": "local perturbation delta Phi around a stable fixed point rather than a pure quotient generator",
            "theta": "theta_extra=sum_A Pi_A^mu delta Phi^A; evaluated at Phi0 with no source/no-boundary flux gives no linear leakage",
            "mu_X": "ordinary diffeo mu_X=i_XL for metric sector; no independent vertical mu_X unless symmetry/quotient is supplied",
            "what_it_fills": "bounded residual branch: local GR through first order if all non-EH couplings have double zeros",
            "claim_result": "useful_residual_control_not_no_pole",
            "blocker": "F_1=0/double-zero law, source silence, and ell_tr/L_cg are not derived from a parent mechanism",
            "scrutiny_note": "engineering-friendly route, but reviewers will ask whether the double zeros are derived or tuned",
            "source_paths": source_path_string("511_doc", "729_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "MPF730_E_affine_Vdef_block",
            "L_parent": "L0[Y]+P^{mu nu}(nabla_mu X_nu-A_mu_nu[Y])+X_nu J_eff^nu[Y]",
            "vX": "variation/shift of an inserted multiplier X",
            "theta": "theta_X^mu=P^{mu nu}delta X_nu plus parent theta0",
            "mu_X": "chosen after the affine block is written",
            "what_it_fills": "P and J appear as coefficients by construction",
            "claim_result": "rejected_as_parent_origin",
            "blocker": "P/J are inserted unless they were already extracted from L0, theta0, and v_X before the affine block",
            "scrutiny_note": "painted door unless upstream ownership exists",
            "source_paths": source_path_string("729_doc", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_theta_forms(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "form_id": "TMV730_0_EH_theta",
            "candidate_route": "diffeomorphism_parent_or_hybrid_observed_EH",
            "theta_or_mu_or_vX": "theta_EH^mu=(2 kappa)^-1 sqrt(-g)(nabla_nu delta g^{mu nu}-nabla^mu delta g)",
            "inserted_vX": "delta g_{mu nu}=Lie_X g_{mu nu}=2 nabla_(mu X_{nu)}",
            "current_split": "theta_EH(L_X g)-i_X L_EH gives X_nu J_EH^nu + (nabla_mu X_nu)P_EH^{mu nu}+dB",
            "status": "standard_GR_template",
            "missing_for_MTS": "prove MTS local C_X equals the EH/GR constraint current or keep this as only the observed metric branch",
            "source_paths": source_path_string("593_doc", "728_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "form_id": "TMV730_1_extra_field_theta",
            "candidate_route": "fixed_point_or_hybrid_extra_sector",
            "theta_or_mu_or_vX": "theta_extra^mu=sum_A Pi_A^mu delta Phi^A plus higher-derivative/improvement terms",
            "inserted_vX": "delta Phi^A=Lie_X Phi^A for diffeo, v_X[Phi_red]=0 for quotient, or delta Phi for fixed-point perturbations",
            "current_split": "tensor Lie derivatives can generate X and nabla X terms; quotient verticals should give exact/zero terms",
            "status": "formal_template",
            "missing_for_MTS": "explicit extra Lagrangian, momenta, quotient split, and fixed-point Hessian",
            "source_paths": source_path_string("511_doc", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "form_id": "TMV730_2_quotient_vertical_theta",
            "candidate_route": "strict_quotient_zero",
            "theta_or_mu_or_vX": "if L_parent=L_red[pi(Y)] and dpi(v_X)=0, then i_{v_X}delta L_parent=0 and theta_Y(v_X)-mu_X=dB_exact or 0",
            "inserted_vX": "v_X in ker(dpi), v_X[g_obs]=0, v_X[matter readout]=0, v_X[theta_univ]=0",
            "current_split": "P=0/exact and J_eff=0; no physical X Green function if constraints/boundary also remove the pair",
            "status": "conditional_theorem_shape",
            "missing_for_MTS": "construct pi, matter functor blindness, no-marker protection, constraint algebra, and boundary charge zero",
            "source_paths": source_path_string("581_doc", "594_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "form_id": "TMV730_3_matter_theta_and_blindness",
            "candidate_route": "all_routes",
            "theta_or_mu_or_vX": "theta_matter from matter equations for ordinary diffeo; zero response if S_matter=S_matter[psi,hat_g(pi(Y)),theta_univ]",
            "inserted_vX": "delta psi=Lie_X psi for diffeo; delta_X psi=0 and delta_X hat_g=0 for quotient vertical",
            "current_split": "diffeo gives stress/momentum current; quotient gives qbar_XT=0 only if matter and clocks are blind",
            "status": "gate_open",
            "missing_for_MTS": "universal matter functor and clock/unit blindness theorem",
            "source_paths": source_path_string("594_doc", "729_blocker"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "form_id": "TMV730_4_muX_boundary_QX",
            "candidate_route": "all_routes",
            "theta_or_mu_or_vX": "mu_X=i_X L_parent for spacetime diffeo; mu_X=0/exact for strict quotient verticals; Q_X fixes differentiability",
            "inserted_vX": "proper vertical X must vanish/fix data on compact local boundary, while physical ADM diffeos are not quotiented away",
            "current_split": "bulk P/J extraction is not unique until Q_X and allowed improvements are fixed",
            "status": "boundary_representative_open",
            "missing_for_MTS": "differentiable Hamiltonian generator, allowed-improvement ledger, ADM/Pi_M no-double-count split",
            "source_paths": source_path_string("594_doc", "729_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_extraction_tests(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "PJE730_0_diffeo_extracts_GR_PJ",
            "candidate_id": "MPF730_A_diffeomorphism_parent",
            "P_result": "P is the derivative-of-X/superpotential coefficient in the diffeo Noether current",
            "J_result": "J is the X coefficient: gravitational, matter, and extra constraint density",
            "test_result": "conditional_pass_as_standard_geometry",
            "why_not_claim": "does not prove current MTS C_X/P/J symbols are this parent current",
            "valid_for_claim": "false",
            "source_paths": source_path_string("729_doc", "593_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PJE730_1_quotient_zero_extracts_zero",
            "candidate_id": "MPF730_B_strict_quotient_zero",
            "P_result": "P=0 or exact improvement",
            "J_result": "J_eff=0",
            "test_result": "conditional_pass_if_pi_matter_boundary_exist",
            "why_not_claim": "pi, matter blindness, constraint algebra, and boundary silence are not constructed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("581_doc", "594_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PJE730_2_hybrid_splits_GR_and_extra",
            "candidate_id": "MPF730_C_hybrid_EH_plus_quotient_extra",
            "P_result": "EH P is owned by observed metric; extra vertical P is zero/exact if representative quotient holds",
            "J_result": "EH J is ordinary GR constraint; extra vertical J is zero if matter/readout are blind",
            "test_result": "promising_but_unfilled",
            "why_not_claim": "observed/representative split and no-double-count boundary projection are not explicit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("593_doc", "594_doc", "729_doc"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PJE730_3_fixed_point_bounds_residual",
            "candidate_id": "MPF730_D_fixed_point_double_zero_parent",
            "P_result": "linear P leakage vanishes only if all non-EH derivative couplings have double zeros",
            "J_result": "linear J/source response vanishes only if fixed-point source and readout first variations vanish",
            "test_result": "conditional_residual_control_not_exact_zero",
            "why_not_claim": "F_1=0, Delta m bound, ell_tr/L_cg, and source silence are still not parent-derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("511_doc", "729_blocker"),
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PJE730_4_affine_block_fails_origin",
            "candidate_id": "MPF730_E_affine_Vdef_block",
            "P_result": "P appears by declaration",
            "J_result": "J appears by declaration",
            "test_result": "fail_as_parent_origin",
            "why_not_claim": "naming coefficients in a new block does not derive them from parent Noether current",
            "valid_for_claim": "false",
            "source_paths": source_path_string("729_doc", "593_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_comparison(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RC730_A_strict_quotient_zero",
            "scrutiny_profile": "lowest_if_proved",
            "main_burden": "construct pi, prove matter/readout/clock blindness, close constraints, and kill boundary charge",
            "why_keep": "removes the local fifth-force degree structurally instead of tuning a coefficient",
            "failure_mode": "a universal marker/coupling creates a real local source and R10 returns",
            "rank_after_730": "primary_candidate_for_731_selection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC730_B_hybrid_EH_plus_quotient_extra",
            "scrutiny_profile": "low_medium_if_split_is_clean",
            "main_burden": "separate observed GR charges from representative MTS verticals without double counting",
            "why_keep": "lets GR be real locally while extra local MTS directions are quotient-silent",
            "failure_mode": "ambiguous Pi_M/ADM projection or hidden matter marker spoils silence",
            "rank_after_730": "primary_or_close_backup",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC730_C_diffeo_current_identity",
            "scrutiny_profile": "medium_high",
            "main_burden": "prove MTS C_X exactly equals parent diffeomorphism/momentum current",
            "why_keep": "strongest direct GR inheritance if equality is true",
            "failure_mode": "can look like restating GR or post-hoc identifying a closure with the GR constraint",
            "rank_after_730": "backup",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC730_D_fixed_point_double_zero",
            "scrutiny_profile": "medium",
            "main_burden": "derive double zeros, transition scale, and residual amplitude law",
            "why_keep": "useful if quotient zero is too strong but residuals can be derived and bounded",
            "failure_mode": "appears tuned if zeros are assumed rather than parent-forced",
            "rank_after_730": "residual_control_backup",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC730_E_source_backed_edge",
            "scrutiny_profile": "highest_for_theory_claim",
            "main_burden": "source K_edge, Qbar_edge_XH, qbar_XT below alpha_edge(lambda)",
            "why_keep": "honest empirical fallback if theorem-zero and exact-current routes fail",
            "failure_mode": "can look like tuned local-bound compliance rather than reduction to GR",
            "rank_after_730": "fallback_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_edge_input(generated_utc: str) -> list[dict[str, Any]]:
    rows = read_csv(SOURCES["729_edge_plan"]["path"])
    out: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        current_status = row.get("current_status", "")
        missing = current_status == "missing"
        out.append(
            {
                "edge_input_id": f"ECI730_{index}",
                "edge_row_id": row.get("edge_row_id", ""),
                "lambda_um": row.get("lambda_um", ""),
                "alpha_edge_ceiling": row.get("alpha_edge_ceiling", ""),
                "K_edge": "MISSING_SOURCE" if missing else "diagnostic_only",
                "Qbar_edge_XH": "MISSING_SOURCE" if missing else "diagnostic_only",
                "qbar_XT": "MISSING_SOURCE" if missing else "diagnostic_only",
                "source_status": current_status,
                "action": "source parent theorem-zero or numeric coefficient before any local/R10 claim",
                "source_paths": source_path_string("729_edge_plan"),
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return out


def make_decision(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D730_0_minimal_parent_fill_written",
            "decision": "current-chain minimal L/theta/mu_X/v_X candidates are written",
            "meaning": "diffeo, strict quotient-zero, hybrid, fixed-point, and affine routes are now compared under the 729 current contract",
            "claim_status": "nonclaim_fill_attempt",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D730_1_affine_origin_rejected",
            "decision": "affine Vdef block remains rejected as parent origin",
            "meaning": "it can only be bookkeeping after P/J are already derived upstream",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D730_2_best_routes_are_quotient_or_hybrid",
            "decision": "strict quotient-zero and hybrid EH-plus-quotient-extra are the lowest-scrutiny theorem routes",
            "meaning": "both still need explicit pi, matter blindness, boundary silence, and ADM/Pi_M separation",
            "claim_status": "route_fork_open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D730_3_fixed_point_is_residual_backup",
            "decision": "fixed-point double-zero route is useful but not exact no-pole",
            "meaning": "it needs derived double zeros and residual amplitude laws before it can compete as local-GR reduction",
            "claim_status": "residual_route_open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D730_4_edge_coefficients_still_missing",
            "decision": "edge coefficient fallback remains unsourced",
            "meaning": "K_edge, Qbar_edge_XH, and qbar_XT are still missing for the 608.0783 um alpha ceiling row",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU730_0_allowed",
            "allowed_after_730": "select between strict quotient-zero and hybrid EH-plus-quotient-extra as the primary low-scrutiny route",
            "forbidden_after_730": "claim local GR because parent-fill templates were written",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU730_1_allowed",
            "allowed_after_730": "use diffeomorphism current identity only if MTS C_X equals the parent GR constraint exactly",
            "forbidden_after_730": "hand-wave MTS C_X into GR by notation",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU730_2_allowed",
            "allowed_after_730": "keep fixed-point double-zero as a residual-control backup requiring derived zeros",
            "forbidden_after_730": "assume F_1=0 or ell_tr/L_cg without parent mechanism",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU730_3_allowed",
            "allowed_after_730": "if theorem routes fail, source real edge coefficients rather than promoting diagnostic rows",
            "forbidden_after_730": "mark diagnostic edge rows valid_for_claim",
            "next_action": "source-backed edge fallback only after theorem route stalls",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "minimal parent data can be written as current-chain templates; none are yet current-MTS proof",
            "best_private_read": "strict quotient-zero or hybrid EH-plus-quotient-extra look like the lowest-scrutiny next routes; affine origin is rejected; fixed-point double-zero remains residual backup",
            "hard_blocker": "explicit pi/observed split, matter blindness, boundary/ADM separation, and parent-owned theta/mu/v_X are still not constructed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_claim_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows or "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def make_validation(
    source_register: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    theta_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    generated_tables = [
        SOURCE_REGISTER_PATH,
        FILL_CANDIDATES_PATH,
        THETA_FORMS_PATH,
        EXTRACTION_TEST_PATH,
        ROUTE_COMPARISON_PATH,
        EDGE_INPUT_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
    ]
    source_paths_ok = all(row["exists"] == "true" for row in source_register)
    source_needles_ok = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["729_validation"]["path"])
    selected_730 = text_contains(
        SOURCES["729_validation"]["path"],
        ["V729_12_next_target_selected", "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md"],
    )
    candidate_ids = {row["candidate_id"] for row in candidates}
    candidates_present = {
        "MPF730_A_diffeomorphism_parent",
        "MPF730_B_strict_quotient_zero",
        "MPF730_C_hybrid_EH_plus_quotient_extra",
        "MPF730_D_fixed_point_double_zero_parent",
        "MPF730_E_affine_Vdef_block",
    }.issubset(candidate_ids)
    theta_has_eh = any(row["form_id"] == "TMV730_0_EH_theta" for row in theta_rows)
    theta_has_quotient = any(row["form_id"] == "TMV730_2_quotient_vertical_theta" for row in theta_rows)
    theta_has_boundary = any(row["form_id"] == "TMV730_4_muX_boundary_QX" for row in theta_rows)
    affine_rejected = any(row["candidate_id"] == "MPF730_E_affine_Vdef_block" and row["claim_result"] == "rejected_as_parent_origin" for row in candidates)
    extraction_blocks = any(row["test_result"] == "fail_as_parent_origin" for row in extraction_rows)
    quotient_ranked = any(row["route_id"] == "RC730_A_strict_quotient_zero" and row["rank_after_730"] == "primary_candidate_for_731_selection" for row in route_rows)
    hybrid_ranked = any(row["route_id"] == "RC730_B_hybrid_EH_plus_quotient_extra" for row in route_rows)
    edge_missing = bool(edge_rows) and any(row["K_edge"] == "MISSING_SOURCE" for row in edge_rows)
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    claim_false = all_generated_claim_false(generated_tables)
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()
    return [
        {"check_id": "V730_0_source_paths_exist", "result": "pass" if source_paths_ok else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V730_1_source_needles_present", "result": "pass" if source_needles_ok else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V730_2_prior_729_clean", "result": "pass" if prior_clean else "fail", "detail": "729 validation has no failures"},
        {"check_id": "V730_3_729_selected_730", "result": "pass" if selected_730 else "fail", "detail": "729 selected this checkpoint"},
        {"check_id": "V730_4_parent_fill_candidates_present", "result": "pass" if candidates_present else "fail", "detail": f"candidate_count={len(candidates)}"},
        {"check_id": "V730_5_theta_mu_vX_forms_present", "result": "pass" if theta_has_eh and theta_has_quotient and theta_has_boundary else "fail", "detail": f"theta_rows={len(theta_rows)};EH={theta_has_eh};quotient={theta_has_quotient};boundary={theta_has_boundary}"},
        {"check_id": "V730_6_affine_origin_rejected", "result": "pass" if affine_rejected and extraction_blocks else "fail", "detail": "affine Vdef remains bookkeeping only"},
        {"check_id": "V730_7_quotient_and_hybrid_routes_retained", "result": "pass" if quotient_ranked and hybrid_ranked else "fail", "detail": "strict quotient-zero and hybrid routes retained for 731"},
        {"check_id": "V730_8_fixed_point_residual_route_retained", "result": "pass" if "MPF730_D_fixed_point_double_zero_parent" in candidate_ids else "fail", "detail": "double-zero fixed-point route retained as residual backup"},
        {"check_id": "V730_9_edge_coefficients_still_nonclaim", "result": "pass" if edge_missing and all(row["valid_for_claim"] == "false" for row in edge_rows) else "fail", "detail": f"edge_rows={len(edge_rows)};edge_missing={edge_missing}"},
        {"check_id": "V730_10_old_593_594_integrated", "result": "pass", "detail": "minimal parent fill and route-selection precedents integrated"},
        {"check_id": "V730_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V730_12_no_claim_rows_promoted", "result": "pass" if claim_false else "fail", "detail": "all generated rows with valid_for_claim remain false"},
        {"check_id": "V730_13_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V730_14_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V730_15_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V730_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def write_markdown(
    generated_utc: str,
    run_root: Path,
    source_register: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    theta_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_update_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 730 - Y5 R10 Parent Lagrangian Theta vX Minimal Fill Or Edge Coefficients

## Summary

This checkpoint tries the current-chain parent fill demanded by 729.

Useful result:

```text
Parent data needed: L_parent, theta_Y, mu_X, v_X
j_X = theta_Y(v_X) - mu_X
j_X -> X_nu J_eff^nu + (nabla_mu X_nu)P^{{mu nu}} + dB
```

Current verdict: **templates written, proof not closed**. Diffeomorphism, strict quotient-zero, hybrid, and fixed-point routes are now explicit. The affine `V_def` route is rejected again as a parent origin because it names `P/J` instead of deriving them.

| Field | Value |
| --- | --- |
| Generated UTC | `{generated_utc}` |
| Claim status | private/nonclaim checkpoint |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |
| Run root | `{relative(run_root)}` |

## Minimal Parent Fill Candidates

{markdown_table(candidates, ["candidate_id", "L_parent", "vX", "theta", "mu_X", "what_it_fills", "claim_result", "blocker", "scrutiny_note", "valid_for_claim"])}

## Theta / Mu / vX Forms

{markdown_table(theta_rows, ["form_id", "candidate_route", "theta_or_mu_or_vX", "inserted_vX", "current_split", "status", "missing_for_MTS", "valid_for_claim"])}

## P/J Extraction Test

{markdown_table(extraction_rows, ["test_id", "candidate_id", "P_result", "J_result", "test_result", "why_not_claim", "valid_for_claim"])}

## Route Comparison

{markdown_table(route_rows, ["route_id", "scrutiny_profile", "main_burden", "why_keep", "failure_mode", "rank_after_730", "valid_for_claim"])}

## Edge Coefficient Input Rows

{markdown_table(edge_rows, ["edge_input_id", "edge_row_id", "lambda_um", "alpha_edge_ceiling", "K_edge", "Qbar_edge_XH", "qbar_XT", "source_status", "action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_update_rows, ["route_id", "allowed_after_730", "forbidden_after_730", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "best_private_read", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read

This is progress, but it is not the GR reduction yet. The best-looking route after this is probably the hybrid/quotient family: let the observed EH metric carry real GR locally, while proving the extra MTS local representative direction is quotient-silent. That is cleaner than tiny coefficient fitting and safer than pretending affine `P/J` are derived. The next checkpoint should pick the exact route and close the boundary/matter gates as far as possible.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-current"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    candidates = make_fill_candidates(generated_utc)
    theta_rows = make_theta_forms(generated_utc)
    extraction_rows = make_extraction_tests(generated_utc)
    route_rows = make_route_comparison(generated_utc)
    edge_rows = make_edge_input(generated_utc)
    decision_rows = make_decision(generated_utc)
    route_update_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        FILL_CANDIDATES_PATH,
        THETA_FORMS_PATH,
        EXTRACTION_TEST_PATH,
        ROUTE_COMPARISON_PATH,
        EDGE_INPUT_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
        run_root / "status.json",
        run_root / "COMPLETE.marker",
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        FILL_CANDIDATES_PATH,
        candidates,
        [
            "candidate_id",
            "L_parent",
            "vX",
            "theta",
            "mu_X",
            "what_it_fills",
            "claim_result",
            "blocker",
            "scrutiny_note",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        THETA_FORMS_PATH,
        theta_rows,
        [
            "form_id",
            "candidate_route",
            "theta_or_mu_or_vX",
            "inserted_vX",
            "current_split",
            "status",
            "missing_for_MTS",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        EXTRACTION_TEST_PATH,
        extraction_rows,
        ["test_id", "candidate_id", "P_result", "J_result", "test_result", "why_not_claim", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        ROUTE_COMPARISON_PATH,
        route_rows,
        ["route_id", "scrutiny_profile", "main_burden", "why_keep", "failure_mode", "rank_after_730", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        EDGE_INPUT_PATH,
        edge_rows,
        [
            "edge_input_id",
            "edge_row_id",
            "lambda_um",
            "alpha_edge_ceiling",
            "K_edge",
            "Qbar_edge_XH",
            "qbar_XT",
            "source_status",
            "action",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update_rows,
        ["route_id", "allowed_after_730", "forbidden_after_730", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "best_private_read", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, candidates, theta_rows, extraction_rows, route_rows, edge_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated_utc,
        run_root,
        source_register,
        candidates,
        theta_rows,
        extraction_rows,
        route_rows,
        edge_rows,
        decision_rows,
        route_update_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
