from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md"


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
            "source_id": "SRC1166_0_1165_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1165_NEXT_TARGET.csv",
            "needle": "NEXT1165_0_1166",
            "role": "handoff requiring J_C-from-Q variation or local corner certificate.",
        },
        {
            "source_id": "SRC1166_1_1165_origin",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv",
            "needle": "LPC1165_1_origin_from_Q",
            "role": "origin-from-Q clause to attack.",
        },
        {
            "source_id": "SRC1166_2_1165_exactness",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv",
            "needle": "LPC1165_5_exactness_law",
            "role": "delta J_C=dB_C exactness clause to reduce.",
        },
        {
            "source_id": "SRC1166_3_1165_boundary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv",
            "needle": "LPC1165_6_boundary_primitive_silence",
            "role": "boundary primitive silence clause.",
        },
        {
            "source_id": "SRC1166_4_1165_corner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1165_CCORNER_DSF_EPSILON_CERTIFICATE_ROWS.csv",
            "needle": "CCZ1165_0_surface_without_corners",
            "role": "corner certificate row.",
        },
        {
            "source_id": "SRC1166_5_274_theorem_shape",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "Let J_C be a domain 3-form memory current on a spatial domain D with boundary partial D.",
            "role": "lifted 3-form theorem shape.",
        },
        {
            "source_id": "SRC1166_6_274_delta",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "delta J_C = dB_C",
            "role": "candidate exactness law.",
        },
        {
            "source_id": "SRC1166_7_275_volume",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "comes from the determinant / volume form of a 3D spatial domain.",
            "role": "J_C from determinant/volume form.",
        },
        {
            "source_id": "SRC1166_8_275_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "boundary primitive / exactness law `delta J_C = dB_C` | not derived",
            "role": "exactness remains not derived in older checkpoint.",
        },
        {
            "source_id": "SRC1166_9_207_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "physical domain selection is still missing.",
            "role": "parent domain selector remains missing.",
        },
        {
            "source_id": "SRC1166_10_1020_surface",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_0_surface_manifold",
            "role": "corner-free surface requirement.",
        },
        {
            "source_id": "SRC1166_11_1020_kernel",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_4_kernel_weight",
            "role": "closed/bounded kernel weight requirement.",
        },
        {
            "source_id": "SRC1166_12_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes identity.",
        },
        {
            "source_id": "SRC1166_13_1020_zero",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_2_zero_conditions",
            "role": "full zero condition list.",
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


def derivation_rows() -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "JCV1166_0_candidate_definition",
            "step": "define lifted domain 3-form",
            "statement": "On a spatial 3-domain D with reference volume form omega_0, take J_C = N_D^{-1} det(Q) omega_0, equivalently J_C = N_D^{-1} e^1∧e^2∧e^3 when Q maps the reference coframe to e.",
            "result_status": "FORMULA_SHAPE_DERIVED_CONDITIONALLY",
            "what_it_proves": "J_C need not be invented as a disconnected repair field; it can be tied to Q/coframe volume.",
            "remaining_gap": "Q, coframe, domain D, and normalization N_D must be parent-owned.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_1_variation_formula",
            "step": "vary determinant/coframe volume",
            "statement": "For invertible Q and fixed omega_0, delta J_C = J_C Tr(Q^{-1} delta Q) - J_C delta(log N_D), plus domain/coframe-reference terms if D or omega_0 varies.",
            "result_status": "KINEMATIC_VARIATION_FORMULA",
            "what_it_proves": "the local source of lifted-C variation is a trace/load-volume variation, not an arbitrary scalar Cperp force.",
            "remaining_gap": "parent variation must say whether D, omega_0, and N_D are fixed, dynamical, or constrained.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_2_top_degree_closedness",
            "step": "closedness of top form",
            "statement": "On a 3-domain, d(delta J_C)=0 kinematically because delta J_C is a top-degree 3-form.",
            "result_status": "MATH_CLOSEDNESS_DERIVED",
            "what_it_proves": "the first d_rel entry condition is easier for a lifted top-form than for scalar Cperp.",
            "remaining_gap": "closed does not mean relatively exact or boundary-silent.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_3_absolute_exactness",
            "step": "absolute local exactness",
            "statement": "If the local domain is contractible/topologically trivial so H^3(D)=0, closed top-form variations admit delta J_C=dB_C for some 2-form B_C.",
            "result_status": "CONDITIONAL_MATH_THEOREM",
            "what_it_proves": "the lifted route has a real mathematical exactness path unavailable to ordinary scalar Cperp.",
            "remaining_gap": "actual local domain topology and primitive choice must be certified.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_4_relative_obstruction",
            "step": "relative cohomology obstruction",
            "statement": "For an oriented compact connected 3-domain with boundary, the top relative class is measured by the domain integral: relative exactness with boundary silence requires the lifted variation to have zero coherent domain integral, int_D delta J_C = 0, up to certified boundary-class conventions.",
            "result_status": "KEY_OBSTRUCTION_IDENTIFIED",
            "what_it_proves": "the missing theorem is not vague: it is a parent local volume-lock/domain-selector law.",
            "remaining_gap": "derive int_D delta J_C=0 locally without killing the FLRW coherent class.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_5_local_volume_lock",
            "step": "local branch lock",
            "statement": "If the parent equations enforce delta C_D = delta(N_D^{-1} int_D J_C)=0 for stationary local domains, then the relative obstruction vanishes and the local lifted-C residual can be exact/boundary-silent subject to edge certificates.",
            "result_status": "CONDITIONAL_ROUTE_NOT_PARENT_DERIVED",
            "what_it_proves": "a clean local-GR route exists in theorem shape.",
            "remaining_gap": "no parent law currently enforces the volume lock and preserves physical charges.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_6_FLRW_active_class",
            "step": "FLRW branch compatibility",
            "statement": "The same criterion allows FLRW activity: a nonzero homogeneous H^3(D,partialD) class is exactly a nonzero domain integral rather than a local exact residual.",
            "result_status": "BRANCH_COMPATIBILITY_SHAPE",
            "what_it_proves": "local silence and cosmological memory need not be hand-switched if the parent selector controls the integral class.",
            "remaining_gap": "selector law and amplitude normalization remain missing.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "JCV1166_7_verdict",
            "step": "derivation verdict",
            "statement": "1166 does not derive local GR; it reduces lifted-C exactness to the parent condition int_D delta J_C=0 on local stationary domains plus boundary/corner/kernel certificates.",
            "result_status": "PROGRESS_NOT_CLAIM",
            "what_it_proves": "the next target is now precise: derive the local domain-volume lock or fill finite edge-bound rows.",
            "remaining_gap": "parent action, P_D variation, boundary primitive, and local/FLRW selector.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def criterion_rows() -> list[dict[str, object]]:
    return [
        {
            "criterion_id": "REC1166_0_domain_assumptions",
            "criterion": "D is compact, oriented, connected, smooth, three-dimensional, with smooth boundary S=partialD and no active corners.",
            "status": "ASSUMPTION_NOT_ARENA_CERTIFIED",
            "proof_role": "needed before applying the top-form relative exactness criterion",
            "missing_piece": "actual local MTS domain representative",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "REC1166_1_JC_top_form",
            "criterion": "J_C is a true lifted top 3-form tied to Q/coframe volume, not a scalar residual relabelled as a form.",
            "status": "FORMULA_SHAPE_ONLY",
            "proof_role": "prevents scalar Cperp resurrection",
            "missing_piece": "parent-owned J_C[Q,e,D]",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "REC1166_2_exactness_condition",
            "criterion": "delta J_C=dB_C locally if the absolute H^3 obstruction vanishes; in the relative/boundary-silent branch, the decisive obstruction is int_D delta J_C.",
            "status": "MATH_CRITERION_WRITTEN",
            "proof_role": "turns exactness into a measurable/cohomological parent condition",
            "missing_piece": "parent law setting int_D delta J_C=0 locally",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "REC1166_3_boundary_primitive",
            "criterion": "boundary primitive silence requires a primitive B_C whose boundary readout is zero or source-bounded in the same boundary class.",
            "status": "NOT_CERTIFIED",
            "proof_role": "prevents exact bulk terms from leaking into local edge force",
            "missing_piece": "B_C trace/norm and boundary class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "REC1166_4_branch_selector",
            "criterion": "local branch has int_D delta J_C=0 while FLRW branch may carry nonzero coherent integral class.",
            "status": "PARENT_SELECTOR_MISSING",
            "proof_role": "prevents hand-switching between local silence and cosmological activity",
            "missing_piece": "same-parent domain-volume selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def corner_rows() -> list[dict[str, object]]:
    return [
        {
            "corner_id": "LC1166_0_boundary_of_boundary",
            "target": "C_corner",
            "certificate_attempt": "If S=partialD is a smooth closed boundary of a smooth local 3-domain, then partialS=partial(partialD)=empty, so the pure Stokes corner term is mathematically zero.",
            "status": "CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_0_surface_manifold",
            "missing_piece": "prove the actual readout surface is a smooth closed partialD without regulator/cutoff joints",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "corner_id": "LC1166_1_regulator_joints",
            "target": "C_corner",
            "certificate_attempt": "If local readout uses annuli, excised bodies, matched patches, or finite cutoffs, all joints must be enumerated and either zeroed or bounded.",
            "status": "NOT_CERTIFIED",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "missing_piece": "corner/joint ledger for actual arena",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "corner_id": "LC1166_2_closed_weight",
            "target": "norm_dS_Feps",
            "certificate_attempt": "d_S(F_lambda epsilon_C)=0 would remove the weighted-Stokes derivative term; otherwise a norm bound is required.",
            "status": "NOT_CERTIFIED",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_4_kernel_weight",
            "missing_piece": "F_lambda, epsilon_C, and surface derivative on the certified lifted-C boundary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "corner_id": "LC1166_3_zero_verdict",
            "target": "edge zero",
            "certificate_attempt": "C_corner can be conditionally zeroed by smooth closed surface geometry, but full edge zero also needs closed weight, B_C primitive, h_C/r_C silence, and cocycle/projector silence.",
            "status": "FULL_EDGE_ZERO_NOT_PROVED",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_2_zero_conditions",
            "missing_piece": "all non-corner edge terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "run_id": "RUN1166_0_JC_variation",
            "test": "J_C from Q/coframe variation",
            "status": "PARTIAL_PASS_FORMULA_AND_OBSTRUCTION_DERIVED",
            "blocked_by": "parent domain-volume lock;domain representative;P_D variation;normalization",
            "detail": "variation formula and relative obstruction are written, but no parent law enforces int_D delta J_C=0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1166_1_relative_exactness",
            "test": "delta J_C=dB_C promotion",
            "status": "REFUSED_RELATIVE_EXACTNESS_NOT_PARENT_SIGNED",
            "blocked_by": "int_D_delta_JC_zero;B_C_boundary_trace;Hrel_selector",
            "detail": "exactness reduces to a precise integral obstruction rather than closing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1166_2_corner_certificate",
            "test": "C_corner=0 certificate",
            "status": "PARTIAL_PASS_MATH_ZERO_NOT_ARENA_CERTIFIED",
            "blocked_by": "actual_smooth_closed_surface;regulator_joint_ledger;fixed_boundary_class",
            "detail": "boundary-of-boundary zero is available only after the actual readout surface is certified",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1166_3_local_claim",
            "test": "local GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "blocked_by": "RUN1166_0_JC_variation;RUN1166_1_relative_exactness;RUN1166_2_corner_certificate",
            "detail": "1166 is a real derivation reduction but not a local-physics pass",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1166_0_JC_origin",
            "gate": "J_C[Q,e,D] is parent-owned and varied",
            "current_status": "PARTIAL_FORMULA_ONLY",
            "reason": "det(Q)/coframe variation formula exists but parent action/domain variation is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1166_1_local_volume_lock",
            "gate": "int_D delta J_C=0 on stationary local domains",
            "current_status": "BLOCKED_KEY_OBSTRUCTION",
            "reason": "no parent volume-lock/domain-selector law yet",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1166_2_FLRW_selector",
            "gate": "nonzero FLRW integral class allowed by the same parent law",
            "current_status": "BLOCKED",
            "reason": "local/FLRW branch selector still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1166_3_edge_certificates",
            "gate": "corner, closed-weight, B_C primitive, harmonic/residual/cocycle terms certified",
            "current_status": "BLOCKED",
            "reason": "only conditional C_corner math zero is identified",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1166_4_local_promotion",
            "gate": "GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "relative exactness and edge certificates remain nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1166_0_real_progress",
            "decision": "lifted_C_exactness_reduced_to_domain_integral_obstruction",
            "reason": "J_C as a top 3-form gives kinematic closedness; relative silence hinges on int_D delta J_C=0",
            "next_action": "derive the parent local volume-lock/domain-selector law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1166_1_corner_progress",
            "decision": "Ccorner_has_conditional_boundary_of_boundary_zero",
            "reason": "smooth S=partialD gives partialS=empty, but actual local readout surfaces may have cutoffs/corners",
            "next_action": "certify the actual local surface or keep corner row bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1166_2_best_next",
            "decision": "target_parent_volume_lock_or_finite_edge_bound",
            "reason": "this is now the narrowest missing law behind derived local GR for lifted C",
            "next_action": "1167 should try the local volume-lock selector first, then fill finite edge norms if it fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1166_0_1167",
            "next_target": "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md",
            "objective": "derive or reject the parent law enforcing int_D delta J_C=0 on local stationary domains while allowing nonzero FLRW H^3 class; if rejected, fill finite edge-bound rows for C_corner and norm_dS_Feps",
            "include": "domain-volume functional; local stationarity; FLRW homogeneous class; P_D variation; N_D normalization; boundary class; C_corner surface certificate; dS_Feps bound; runner dry-run",
            "exclude": "scalar Cperp promotion; local/FLRW hand switch; projected metric theorem; invented constants; local-GR claim; c_g zero claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    criteria: list[dict[str, object]],
    corners: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    variation_present = any(row["derivation_id"] == "JCV1166_1_variation_formula" for row in derivation)
    obstruction_present = any(row["derivation_id"] == "JCV1166_4_relative_obstruction" for row in derivation)
    volume_lock_blocked = any(row["gate_id"] == "G1166_1_local_volume_lock" and "BLOCKED" in str(row["current_status"]) for row in gates)
    corner_partial = any(row["corner_id"] == "LC1166_0_boundary_of_boundary" and "CONDITIONAL" in str(row["status"]) for row in corners)
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, derivation, criteria, corners, runner, gates, decisions, next_rows)
        for row in table
    )
    csv_parse = True
    parse_detail = "all 1166 CSV outputs parse cleanly"
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
            "check_id": "V1166_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_1_variation_formula_written",
            "result": "pass" if variation_present else "fail",
            "detail": "J_C from det(Q)/coframe variation formula is recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_2_relative_obstruction_identified",
            "result": "pass" if obstruction_present else "fail",
            "detail": "relative exactness is reduced to int_D delta J_C=0 plus boundary certificates",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_3_volume_lock_blocked",
            "result": "pass" if volume_lock_blocked else "fail",
            "detail": "parent local volume-lock law remains blocked rather than assumed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_4_corner_partial_only",
            "result": "pass" if corner_partial else "fail",
            "detail": "C_corner has conditional boundary-of-boundary zero but no arena certificate",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_5_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "runner refuses relative-exactness, corner, and local promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_6_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_7_next_target",
            "result": "pass" if next_rows and "1167" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1167 handoff targets parent volume-lock selector or finite edge-bound fill",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_8_generated_under_post_checkpoint",
            "result": "pass" if under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_9_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1166_SUMMARY",
            "result": "pass" if source_ok and variation_present and obstruction_present and volume_lock_blocked and runner_refuses and all_nonclaim else "fail",
            "detail": "1166 derives the lifted-JC variation/relative-obstruction shape, conditionally zeros pure corners, and names parent volume-lock as the next hard law",
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
    derivation: list[dict[str, object]],
    criteria: list[dict[str, object]],
    corners: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1166 — Y5/R10 J_C from Q parent variation or local corner certificate

**Current verdict:** this is genuine progress, but not a claim. If `J_C` is the lifted domain three-form from `det(Q)`/coframe volume, then local exactness is no longer a slogan: the obstruction reduces to the local domain integral `int_D delta J_C`. The missing parent law is now sharply named as a local volume-lock/domain-selector theorem.

**Main derivation:** `J_C=N_D^-1 det(Q) omega_0` gives `delta J_C = J_C Tr(Q^-1 delta Q) - J_C delta(log N_D)` up to domain/coframe-reference terms. Since `delta J_C` is a top 3-form on a 3-domain, it is kinematically closed. Local relative exactness/boundary silence requires the coherent integral obstruction to vanish: `int_D delta J_C = 0`, plus the boundary/corner/kernel certificates.

**No claim:** no local-GR, R10, PPN, WEP, clock, orbital, projected-metric theorem, or `c_g=0` result follows. The win is that the next missing theorem is precise.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## J_C from Q/coframe variation derivation

{md_table(derivation, ["derivation_id", "step", "statement", "result_status", "what_it_proves", "remaining_gap", "valid_for_claim"])}

## Relative exactness criterion

{md_table(criteria, ["criterion_id", "criterion", "status", "proof_role", "missing_piece", "valid_for_claim"])}

## Local corner certificate attempt

{md_table(corners, ["corner_id", "target", "certificate_attempt", "status", "missing_piece", "valid_for_claim"])}

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
    derivation = stamp(derivation_rows())
    criteria = stamp(criterion_rows())
    corners = stamp(corner_rows())
    runner = stamp(runner_rows())
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())
    outputs = {
        "P8_Y5_R10_1166_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1166_JC_FROM_Q_VARIATION_DERIVATION.csv": derivation,
        "P8_Y5_R10_1166_RELATIVE_EXACTNESS_CRITERION.csv": criteria,
        "P8_Y5_R10_1166_LOCAL_CORNER_CERTIFICATE_ATTEMPT.csv": corners,
        "P8_Y5_R10_1166_RUNNER_DRY_RUN.csv": runner,
        "P8_Y5_R10_1166_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1166_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1166_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, derivation, criteria, corners, runner, gates, decisions, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1166_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, derivation, criteria, corners, runner, gates, decisions, next_rows, validation)

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
