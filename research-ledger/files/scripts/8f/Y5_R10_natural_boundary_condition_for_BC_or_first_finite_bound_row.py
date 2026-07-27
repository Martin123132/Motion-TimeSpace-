from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1171_0_1170_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_NEXT_TARGET.csv",
            "needle": "NEXT1170_0_1171",
            "role": "handoff to natural boundary condition or finite bound row.",
        },
        {
            "source_id": "SRC1171_1_1170_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1170_VALIDATION.csv",
            "needle": "V1170_SUMMARY",
            "role": "1170 validation summary.",
        },
        {
            "source_id": "SRC1171_2_1170_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv",
            "needle": "BST1170_0_stokes_split",
            "role": "boundary primitive plus top-class split.",
        },
        {
            "source_id": "SRC1171_3_1170_no_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_PHI_BC_RELATION.csv",
            "needle": "PBC1170_1_no_flux_condition",
            "role": "sufficient no-flux condition not derived.",
        },
        {
            "source_id": "SRC1171_4_1170_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_PHI_BC_RELATION.csv",
            "needle": "PBC1170_2_finite_bound",
            "role": "finite boundary fallback.",
        },
        {
            "source_id": "SRC1171_5_1170_local_gap",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_LOCAL_ZERO_CERTIFICATE.csv",
            "needle": "LZC1170_1_boundary_primitive",
            "role": "main local zero boundary gap.",
        },
        {
            "source_id": "SRC1171_6_1170_stokes_guard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_WEIGHTED_STOKES_C_SECTOR.csv",
            "needle": "WSC1170_3_zero_or_bound",
            "role": "strict zero-or-bound acceptance rule.",
        },
        {
            "source_id": "SRC1171_7_1170_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1170_CLAIM_GATES.csv",
            "needle": "G1170_1_local_zero",
            "role": "local zero gate blocked by boundary flux.",
        },
        {
            "source_id": "SRC1171_8_274_decomp",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "lifted-C exact/top decomposition.",
        },
        {
            "source_id": "SRC1171_9_1020_bound",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "source-backed finite bound precedent.",
        },
        {
            "source_id": "SRC1171_10_1020_guard",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "CG1020_8_guardrail",
            "role": "weighted-Stokes guardrail.",
        },
        {
            "source_id": "SRC1171_11_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward conservation guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def variation_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "NBC1171_0_generic_variation",
            "object": "B_C exact-sector action",
            "statement": "For a generic exact-sector kinetic term with H_C=d_D B_C, variation has the form delta S_B = bulk(delta B_C, d_D^dagger H_C + source) + int_partialD delta B_C wedge Pi_B, where Pi_B is the boundary conjugate momentum.",
            "status": "FORMAL_VARIATION_SHAPE",
            "derives": "the natural boundary datum is the conjugate momentum Pi_B, not the boundary value B_C itself.",
            "missing": "actual parent C-sector Lagrangian and exact sign/Hodge conventions",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NBC1171_1_neumann_natural_condition",
            "object": "natural boundary condition",
            "statement": "The ordinary free-endpoint/natural condition is Pi_B|partialD=0. This can mean no normal H_C flux, but it does not imply int_partialD B_C=0.",
            "status": "NO_LOCAL_ZERO_FROM_GENERIC_NATURAL_BC",
            "derives": "generic variational naturalness is weaker than the local zero theorem needs.",
            "missing": "special parent term proving B_C itself is pure gauge, exact with closed weight, or zero on the lifted-C residual boundary",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NBC1171_2_dirichlet_condition",
            "object": "Dirichlet/fixed B_C boundary",
            "statement": "Fixing pullback(B_C) or setting pullback(B_C)=0 would kill the boundary primitive, but this is an imposed boundary condition unless derived as a physical residual-sector boundary from the parent action.",
            "status": "CLOSURE_NOT_THEOREM",
            "derives": "a possible closure condition, not a derivation.",
            "missing": "parent reason for residual-sector B_C boundary silence and proof physical Hamiltonian/charge generators survive",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NBC1171_3_gauge_guard",
            "object": "B_C gauge shift",
            "statement": "On a closed two-boundary, int_partialD(B_C + d_S Lambda_C)=int_partialD B_C. Therefore the integrated B_C boundary primitive cannot be gauged away by an ordinary exact shift.",
            "status": "GAUGE_SHORTCUT_REJECTED",
            "derives": "the boundary integral is the real obstruction, not a removable representative artifact.",
            "missing": "separate treatment of large gauge/relative cohomology sectors if introduced later",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NBC1171_4_compact_support_or_infinity",
            "object": "outer boundary route",
            "statement": "A falloff/compact-support theorem at infinity could silence the outer boundary of an isolated system, but it does not automatically silence arbitrary local laboratory or solar-system subdomain boundaries.",
            "status": "ASYMPTOTIC_ROUTE_ONLY",
            "derives": "asymptotic boundary control is not enough for local PPN/R10 unless the local domain boundary is physically chosen around support with no residual flux.",
            "missing": "source-support theorem plus domain-choice rule compatible with PPN/R10 tests",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NBC1171_5_verdict",
            "object": "natural boundary theorem verdict",
            "statement": "1171 does not derive a parent natural-boundary theorem strong enough to set int_partialD B_C=0. The honest route is now a finite B_C boundary-bound source row or a more specific parent boundary action.",
            "status": "THEOREM_NOT_CLOSED_MOVE_TO_BOUND_ROW",
            "derives": "a no-go against the cheap natural-boundary shortcut.",
            "missing": "parent boundary action or source-backed finite B_C norms",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def no_go_rows() -> list[dict[str, object]]:
    rows = [
        {
            "nog_id": "NOG1171_0_neumann_gap",
            "claim_tested": "natural BC gives local zero",
            "result": "fail_as_general_theorem",
            "reason": "Pi_B=0 controls conjugate momentum/normal derivative, not the integral of B_C on the boundary",
            "what_would_fix": "parent action where boundary equation directly imposes residual pullback(B_C)=0 or exact closed-weight cancellation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "nog_id": "NOG1171_1_dirichlet_gap",
            "claim_tested": "set pullback B_C=0",
            "result": "closure_only",
            "reason": "Dirichlet boundary values restrict admissible histories; they are not automatically selected by a local vacuum theorem",
            "what_would_fix": "derive residual-sector Dirichlet from finite-action/falloff/symmetry without killing physical charges",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "nog_id": "NOG1171_2_gauge_gap",
            "claim_tested": "gauge away boundary integral",
            "result": "fail_on_closed_boundary",
            "reason": "closed-boundary integral of an exact gauge shift vanishes, leaving int_partialD B_C unchanged",
            "what_would_fix": "separate parent theorem that B_C has zero boundary cohomology coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "nog_id": "NOG1171_3_bianchi_gap",
            "claim_tested": "silent boundary flux without stress ledger",
            "result": "fail_conservation_guard",
            "reason": "any source/flux removal must appear in the Ward/Bianchi bookkeeping",
            "what_would_fix": "stress tensor/current ledger for B_C, Phi_C, Sigma_C, and domain projector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def finite_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "FBC1171_0_first_boundary_bound_row",
            "arena": "local_R10_PPN_clock_orbital_generic",
            "quantity": "Q_C_boundary_exact",
            "bound_formula": "|int_partialD B_C| <= area(partialD) * sup_partialD|B_C|, or <= ||1||_* ||B_C||_* in the chosen boundary norm",
            "weighted_stokes_extension": "+ C_corner + ||d_S(F_lambda epsilon_C)||_* ||b_C||_* + |harmonic_edge_C| + |residual_edge_C|",
            "units": "MISSING_BOUNDARY_BC_UNITS",
            "numeric_value": "MISSING_BC_NORM",
            "source_path": "MISSING_SOURCE_BACKED_BC_NORM_OR_PARENT_ZERO_THEOREM",
            "status": "STAGED_NONCLAIM_FIRST_BOUND_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "FBC1171_1_required_area_norm",
            "arena": "local_boundary_geometry",
            "quantity": "area(partialD) or ||1||_*",
            "bound_formula": "finite surface measure for the selected test domain",
            "weighted_stokes_extension": "must use the same surface convention as B_C and weighted-Stokes terms",
            "units": "MISSING_SURFACE_UNITS",
            "numeric_value": "MISSING_DOMAIN_GEOMETRY",
            "source_path": "MISSING_DOMAIN_SPEC",
            "status": "REQUIRED_INPUT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "FBC1171_2_required_BC_norm",
            "arena": "lifted_C_boundary",
            "quantity": "||B_C||_* or sup_partialD|B_C|",
            "bound_formula": "must be derived from parent C-sector or measured/source-bounded in arena",
            "weighted_stokes_extension": "if B_C=d_S b_C+h_C+r_C, then b_C, h_C, r_C each require norm rows",
            "units": "MISSING_BC_UNITS",
            "numeric_value": "MISSING_BC_VALUE",
            "source_path": "MISSING_PARENT_BC_PROFILE",
            "status": "REQUIRED_INPUT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "FBC1171_3_required_kernel_derivative",
            "arena": "weighted_Stokes_C",
            "quantity": "||d_S(F_lambda epsilon_C)||_*",
            "bound_formula": "zero theorem or finite derivative norm",
            "weighted_stokes_extension": "multiplies ||b_C||_* in exact-boundary branch",
            "units": "MISSING_WEIGHT_DERIVATIVE_UNITS",
            "numeric_value": "MISSING_DSF_EPS_VALUE",
            "source_path": "MISSING_CLOSED_WEIGHT_CERTIFICATE_OR_BOUND",
            "status": "REQUIRED_INPUT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "FBC1171_4_acceptance_gate",
            "arena": "all_local_arenas",
            "quantity": "local exact-sector residual",
            "bound_formula": "claim only if every term is numeric/source-backed or parent-zero",
            "weighted_stokes_extension": "corner, harmonic, residual, kernel derivative, and primitive norms all included",
            "units": "BLOCKED_UNTIL_ALL_TERMS_DEFINED",
            "numeric_value": "NOT_EVALUATED",
            "source_path": "NO_CLAIM_FROM_1171",
            "status": "RUNNER_MUST_REFUSE_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def form_degree_rows() -> list[dict[str, object]]:
    rows = [
        {
            "degree_id": "FDL1171_0_BC",
            "object": "B_C",
            "degree": "2-form on spatial D; top-degree pullback on partialD",
            "boundary_role": "integrates over partialD",
            "zero_implication": "none by degree alone",
            "missing": "parent primitive definition and norm",
            "valid_for_claim": False,
        },
        {
            "degree_id": "FDL1171_1_bC",
            "object": "b_C",
            "degree": "1-form primitive on S if pullback(B_C)=d_S b_C",
            "boundary_role": "appears in weighted-Stokes derivative residual",
            "zero_implication": "requires corner-free S and closed weight",
            "missing": "existence and norm of b_C",
            "valid_for_claim": False,
        },
        {
            "degree_id": "FDL1171_2_weight",
            "object": "F_lambda epsilon_C",
            "degree": "weight/representative factor paired with exact-boundary primitive",
            "boundary_role": "d_S(F_lambda epsilon_C) multiplies b_C in residual",
            "zero_implication": "zero only if closed/constant in the actual weighted identity",
            "missing": "degree and closure certificate that does not remove physical generators",
            "valid_for_claim": False,
        },
        {
            "degree_id": "FDL1171_3_Phi_C",
            "object": "Phi_C",
            "degree": "2-form boundary flux in spatial continuity split",
            "boundary_role": "exact-sector time-transport flux",
            "zero_implication": "must be natural-boundary silent or source-bounded",
            "missing": "Phi_C-B_C parent transport law",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1171_0_generic_natural_bc",
            "test": "does generic natural BC imply int_partialD B_C=0",
            "status": "FAILS_AS_GENERAL_THEOREM",
            "result": "natural BC gives Pi_B=0, not B_C boundary integral zero",
            "blocked_by": "parent_special_boundary_action;residual_Dirichlet_theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1171_1_gauge_shortcut",
            "test": "can exact gauge shift remove int_partialD B_C",
            "status": "REFUSED_GAUGE_INVARIANT_INTEGRAL",
            "result": "closed-boundary integral is unchanged by B_C -> B_C + d_S Lambda_C",
            "blocked_by": "boundary_cohomology_coefficient_zero_theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1171_2_first_finite_bound_row",
            "test": "can finite row be staged",
            "status": "PASS_SCHEMA_NONCLAIM",
            "result": "first B_C boundary-bound row exists but has MISSING inputs and valid_for_claim=false",
            "blocked_by": "B_C_norm;surface_area;dSFeps;corner;harmonic;residual;units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1171_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "1171 narrows the gap to specific boundary-bound inputs but does not pass local tests",
            "blocked_by": "finite_bound_inputs_or_parent_boundary_zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1171_0_natural_bc",
            "gate": "natural-boundary theorem for B_C",
            "current_status": "FAILED_AS_GENERIC_THEOREM",
            "reason": "generic natural condition sets conjugate boundary momentum, not boundary primitive integral",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1171_1_parent_special_bc",
            "gate": "parent special boundary action",
            "current_status": "BLOCKED",
            "reason": "no parent action term currently derives residual pullback(B_C)=0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1171_2_finite_bound",
            "gate": "finite B_C boundary-bound row",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "reason": "row exists but B_C norm, surface geometry, kernel derivative, harmonic/residual, corner, and units are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1171_3_charge_guard",
            "gate": "physical-charge preservation",
            "current_status": "BLOCKED",
            "reason": "must show residual boundary silence does not delete physical mass/time/rotation/charge generators",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1171_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "neither parent boundary zero nor finite numeric/source bound is available",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1171_0_no_generic_natural_bc",
            "decision": "do_not_claim_boundary_zero_from_generic_naturalness",
            "reason": "the variational boundary term does not set B_C itself to zero",
            "next_action": "look for a special parent boundary action or source finite B_C norm",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1171_1_bound_row_created",
            "decision": "stage_first_finite_BC_bound_row",
            "reason": "the theorem route currently fails; a finite bound is the honest fallback",
            "next_action": "derive/source B_C profile or norm in the simplest local arena",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1171_2_best_next",
            "decision": "target_BC_norm_owner",
            "reason": "all local residual scoring now depends on either B_C=0 theorem or an actual B_C norm",
            "next_action": "try deriving B_C primitive/norm from J_C=dB_C+J_top on a contractible local domain",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1171_0_1172",
            "next_target": "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            "objective": "derive or source a B_C primitive/norm from the local exact-sector equation, then feed the finite boundary-bound row without claiming a pass",
            "include": "local contractible domain; Hodge/Poincare bound for B_C from J_C; gauge fixing; boundary norm; surface geometry; units; no-claim runner",
            "exclude": "generic natural-boundary zero; gauge-erasing boundary integral; local claim; c_g zero; invented values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    variations: list[dict[str, object]],
    nogos: list[dict[str, object]],
    bounds: list[dict[str, object]],
    degrees: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1171_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_1_variation_shape_written",
            "result": "pass" if any("Pi_B" in str(r["statement"]) for r in variations) else "fail",
            "detail": "generic boundary variation identifies conjugate momentum rather than B_C value",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_2_natural_bc_not_overclaimed",
            "result": "pass" if any(r["status"] == "NO_LOCAL_ZERO_FROM_GENERIC_NATURAL_BC" for r in variations) else "fail",
            "detail": "generic natural boundary route is refused as local zero proof",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_3_no_go_rows_written",
            "result": "pass" if len(nogos) >= 4 and all(r["claim_allowed"] is False for r in nogos) else "fail",
            "detail": "Neumann, Dirichlet, gauge, and Bianchi gaps are explicitly recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_4_first_bound_row_created",
            "result": "pass"
            if any(r["bound_id"] == "FBC1171_0_first_boundary_bound_row" for r in bounds)
            else "fail",
            "detail": "first finite B_C boundary-bound row is staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_5_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in bounds)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_6_form_degree_ledger_written",
            "result": "pass" if len(degrees) >= 4 else "fail",
            "detail": "B_C, b_C, F epsilon_C, and Phi_C degree roles are logged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses natural-boundary, gauge, finite-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1171 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_9_no_claim_rows",
            "result": "pass"
            if all(
                r.get("valid_for_claim") is False
                for r in variations + nogos + bounds + degrees + gates + nexts
            )
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_10_next_target",
            "result": "pass" if nexts and "1172" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1172 handoff targets B_C primitive/norm owner or finite bound runner",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1171_SUMMARY",
            "result": "pass",
            "detail": "1171 rejects the generic natural-boundary shortcut, stages the first finite B_C boundary-bound row, and moves the next target to deriving/sourcing B_C primitive norms",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    variations: list[dict[str, object]],
    nogos: list[dict[str, object]],
    bounds: list[dict[str, object]],
    degrees: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1171 — Y5/R10 natural boundary condition for B_C or first finite bound row",
        "**Current verdict:** the generic natural-boundary route does not close the local branch. A standard variational boundary condition sets the conjugate boundary momentum `Pi_B`, not the boundary primitive integral `int_partialD B_C`. So `B_C=0` cannot be claimed from generic naturalness.",
        "**Main progress:** this checkpoint converts the obstruction into a source-ready finite-bound row: `|int_partialD B_C| <= area(partialD) sup|B_C|` or `||1||_* ||B_C||_*`, plus the weighted-Stokes corner, kernel-derivative, harmonic, and residual terms.",
        "**Important no-go:** the boundary integral cannot be erased by the ordinary gauge shift `B_C -> B_C + d_S Lambda_C` on a closed boundary, because the integrated exact shift vanishes. If the integral is nonzero, it is a real boundary/cohomology coefficient.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Natural boundary variation attempt\n\n" + table(variations),
        "## No-go ledger\n\n" + table(nogos),
        "## First finite B_C boundary-bound row\n\n" + table(bounds),
        "## Form-degree ledger\n\n" + table(degrees),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    variations = variation_attempt_rows()
    nogos = no_go_rows()
    bounds = finite_bound_rows()
    degrees = form_degree_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, variations, nogos, bounds, degrees, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1171_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1171_NATURAL_BOUNDARY_VARIATION_ATTEMPT.csv": variations,
        "P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv": nogos,
        "P8_Y5_R10_1171_FIRST_FINITE_BC_BOUND_ROW.csv": bounds,
        "P8_Y5_R10_1171_FORM_DEGREE_LEDGER.csv": degrees,
        "P8_Y5_R10_1171_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1171_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1171_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1171_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1171_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, variations, nogos, bounds, degrees, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
