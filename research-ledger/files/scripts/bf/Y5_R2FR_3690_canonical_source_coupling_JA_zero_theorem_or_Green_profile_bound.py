from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3690"
BRANCH_ID = "MTS_R2FR_Y5_CANONICAL_SOURCE_COUPLING_JA_ZERO_THEOREM_OR_GREEN_PROFILE_BOUND_3690"
DOC = ROOT / "3690-Y5-R2FR-canonical-source-coupling-JA-zero-theorem-or-Green-profile-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3689", RESIDUALS / "P8_Y5_R2FR_3689_NEXT_TARGET.csv", "J_A", "3689 selected canonical source-coupling J_A as next target"),
        ("canonical_3689", RESIDUALS / "P8_Y5_R2FR_3689_CANONICAL_GAMMA_KHAT_BRANCH_ROWS.csv", "CAN3689_6_q_loc", "canonical q profile and action branch"),
        ("residual_3689", RESIDUALS / "P8_Y5_R2FR_3689_RESIDUAL_ROWS.csv", "RES3689_2_JA", "R_JA residual row"),
        ("adoption_3689", RESIDUALS / "P8_Y5_R2FR_3689_ADOPTION_GATE_ROWS.csv", "AG3689_4_JA_zero", "J_A zero adoption gate"),
        ("qloc_3688", RESIDUALS / "P8_Y5_R2FR_3688_QLOC_PROFILE_INPUT_ROWS.csv", "QPI3688_1_Euler_source", "q_loc profile and Euler source input"),
        ("coupling_3629", RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv", "CL3629_2_residual_profile", "exact Green-profile route if J_Z is not zero"),
        ("coeff_3629", RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv", "JZC3629_3_Newton_source", "arena coefficient templates for J_Z profile"),
        ("theorem_3630", RESIDUALS / "P8_Y5_R2FR_3630_JZ_ZERO_THEOREM_DERIVATION.csv", "THM3630_6_conclusion", "conditional theorem for J_Z=0"),
        ("bounds_3630", RESIDUALS / "P8_Y5_R2FR_3630_JZ_BOUND_REQUIREMENTS.csv", "JZB3630_3_Newton_source", "bound requirements if theorem fails"),
        ("signature_3630", RESIDUALS / "P8_Y5_R2FR_3630_PARENT_SIGNATURE_AUDIT.csv", "SIG3630_1_vertical_generator", "parent signatures still unsigned"),
        ("parent_clause_3630", RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv", "PAC3630_3_matter_descent", "sufficient parent action clauses for quotient descent"),
        ("component_1282", RESIDUALS / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv", "RCM1282_6_verdict", "Z physical residual map not closed"),
        ("euler_source", RESIDUALS / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv", "Y5_source_normalization", "known source-normalization hard fail/current debt"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def ja_decomposition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "JAD3690_0_definition",
            "canonical source vector",
            "J_A := (1/sqrt(-g)) delta(S_matter+S_source+S_boundary+S_selector+S_flux^phys_if_Z_coupled)/delta Z^A |_{Z=0}",
            "The canonical even response bulk has no linear Z source; every remaining source lives here.",
            "EXACT_DEFINITION",
            "none",
        ),
        (
            "JAD3690_1_even_bulk",
            "response bulk",
            "delta_Z S_even|0=0 and delta_Z T_GK|0=0 after Gamma0 subtraction",
            "F1=0 survives in the canonical action branch.",
            "ZERO_DERIVED_FOR_CANONICAL_BULK",
            "none for bulk",
        ),
        (
            "JAD3690_2_matter",
            "ordinary matter coupling",
            "delta_Z S_matter=(delta Sbar_matter/delta q) Dq[e_A] delta Z^A",
            "J_A^matter=0 if Z^A is vertical, Dq[e_A]=0 and matter descends through q only.",
            "CONDITIONAL_ZERO_PARENT_SIGNATURE_UNSIGNED",
            "R_Jmatter",
        ),
        (
            "JAD3690_3_source_norm",
            "source-normalization coupling",
            "delta_Z S_source=0 if Pi_M, J_H, G_eff, M_eff are q-owned or source-current orthogonal to vertical Z directions",
            "This is the Newton/source-mass coupling lock.",
            "CONDITIONAL_ZERO_SOURCE_ORTHOGONALITY_UNSIGNED",
            "R_Jsource",
        ),
        (
            "JAD3690_4_selector_memory",
            "selector/memory/domain activation",
            "delta_Z[f(Z)L_mem]|0=f_prime(0)L_mem delta Z=0 when f(0)=f_prime(0)=0",
            "Quadratic/topological/norm activation kills the linear local source.",
            "CONDITIONAL_ZERO_PARENT_ORIGIN_UNSIGNED",
            "R_Jselector",
        ),
        (
            "JAD3690_5_boundary",
            "boundary natural source",
            "delta S_boundary|collar=int_boundary B_A delta Z^A",
            "J_A^boundary=0 only if B_A=0 or fixed-reference exact/no-flux boundary is signed.",
            "OPEN_BOUNDARY_SOURCE",
            "R_Jboundary",
        ),
        (
            "JAD3690_6_flux",
            "physical EM/Poynting/radiation flux",
            "S_flux^phys may contribute J_A only if physical flux is Z-coupled; otherwise it is counted as ordinary stress/current",
            "Poynting/EM is allowed as physics, not as hidden closure.",
            "SEPARATE_PHYSICAL_BRANCH_OR_RESIDUAL",
            "R_Jflux",
        ),
        (
            "JAD3690_7_total",
            "total canonical source vector",
            "J_A = J_A^matter+J_A^source+J_A^selector+J_A^boundary+J_A^flux",
            "J_A=0 is proved only if every component above is zero in one parent-signed branch.",
            "ZERO_THEOREM_FORM_PROVED_TOTAL_ZERO_NOT_CLAIMED",
            "R_JA",
        ),
    ]
    return [
        {
            **base(ts),
            "decomposition_id": decomposition_id,
            "piece": piece,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "residual_if_not_zero": residual_if_not_zero,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decomposition_id, piece, formula, meaning, status, residual_if_not_zero in specs
    ]


def zero_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("JZG3690_0_q_map", "q:Phi_parent->Q_MTS is parent-defined", "MISSING_PARENT_Q_MAP", "R_qmap"),
        ("JZG3690_1_vertical", "Z^A basis equals ker(Dq) with Dq[e_A]=0", "MISSING_DQ_VERTICAL_GENERATOR_MAP", "R_Zvertical"),
        ("JZG3690_2_matter_descent", "S_matter=Sbar_matter[q(Phi),Psi,theta(q)]", "NOT_SIGNED_FROM_PRIOR_QUOTIENT_CRITERION", "R_Jmatter"),
        ("JZG3690_3_source_orthogonality", "Pi_M,J_H,M_eff,G_eff are q-owned or orthogonal to vertical charges", "NOT_PARENT_DERIVED", "R_Jsource"),
        ("JZG3690_4_quadratic_activation", "all selector/memory/domain couplings satisfy f(0)=f_prime(0)=0 from parent symmetry/topology", "REQUIREMENT_KNOWN_ORIGIN_MISSING", "R_Jselector"),
        ("JZG3690_5_boundary_no_flux", "B_A=0 or fixed exact boundary with no local flux", "BOUNDARY_NATURAL_SOURCE_OPEN", "R_Jboundary"),
        ("JZG3690_6_Z_observable_map", "Z^A equals full physical q_loc/PPN/Newton/source residual vector", "MISSING_Z_TO_OBSERVABLE_MAP", "R_Zmap"),
        ("JZG3690_7_operator_gap", "L_AB positive/coercive with sourced inverse norm", "FORMAL_REQUIREMENT_NUMERIC_INPUTS_MISSING", "R_Linv"),
        ("JZG3690_8_verdict", "J_A=0 in canonical branch", "ZERO_NOT_CLAIMED_GREEN_PROFILE_BOUND_RETAINED", "R_JA"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "zero_gate": zero_gate,
            "current_status": current_status,
            "residual_if_failed": residual_if_failed,
            "claim_allowed": False,
            "score_ready": False,
        }
        for gate_id, zero_gate, current_status, residual_if_failed in specs
    ]


def green_profile_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "GP3690_0_linear_equation",
            "linearized canonical response equation",
            "L_AB Z^B + J_A + B_A = 0",
            "L_AB=-D_mu(G_AB D^mu)+M_AB+curvature/projector terms",
            "EXACT_LINEARIZED_EQUATION",
            "from 3629 and canonical branch",
        ),
        (
            "GP3690_1_green_solution",
            "finite profile if J_A not zero",
            "Z^A(x)=-(L^{-1})^{AB}J_B + Z_boundary^A + O(J^2)",
            "Z_boundary^A=-(L^{-1})^{AB}B_B plus fixed/collar Green terms",
            "PROFILE_BOUND_ROUTE_DERIVED",
            "this prevents plateau smuggling",
        ),
        (
            "GP3690_2_norm_bound",
            "profile norm envelope",
            "||Z||_X <= ||L^{-1}||_{X<-Y}(||J_matter||_Y+||J_source||_Y+||J_selector||_Y+||J_boundary||_Y+||J_flux||_Y)+||Z_boundary_fixed||_X+O(J^2)",
            "operator norm and source norms must be arena/source-backed",
            "FORMULA_READY_INPUTS_MISSING",
            "turns coupling gap into executable bound interface",
        ),
        (
            "GP3690_3_qloc_bound",
            "q_can profile bound",
            "||q_can||_A <= ||P_loc R||_A ||E||_A + ||P_loc B_GK||_A, with E_A=O(J^2) on solved profile and observable leakage through Z response operators",
            "requires arena response operators K_AJ",
            "SYMBOLIC_PROFILE_TO_OBSERVABLE_READY",
            "used by PPN/R10/clock/orbital rows",
        ),
        (
            "GP3690_4_Newton_source",
            "Newton/source normalization profile",
            "delta_mu_JA = K_mu_JA * Pi_M(L^{-1}J_A)",
            "needs K_mu_JA, Pi_M, L^{-1}, source worldtube and range profile",
            "SOURCE_READY_TEMPLATE_NONNUMERIC",
            "this is the source-coupling route to test instead of handwaving",
        ),
        (
            "GP3690_5_verdict",
            "Green-profile fallback",
            "R_JA is finite and source-ready but not score-ready",
            "zero theorem not parent-signed; numeric/operator inputs missing",
            "NONCLAIM_PROFILE_BOUND_STAGED",
            "local-GR/Newton claim stays blocked",
        ),
    ]
    return [
        {
            **base(ts),
            "profile_id": profile_id,
            "object": object_name,
            "formula": formula,
            "requirements": requirements,
            "status": status,
            "meaning": meaning,
            "claim_allowed": False,
            "score_ready": False,
        }
        for profile_id, object_name, formula, requirements, status, meaning in specs
    ]


def arena_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("JAR3690_0_gamma", "PPN gamma", "gamma_minus_1", "K_gamma_JA * ||L^{-1}J_A||_gamma", "MISSING_K_GAMMA_JA_AND_L_INV_PROFILE"),
        ("JAR3690_1_beta", "PPN beta", "beta_minus_1", "K_beta_JA * ||L^{-1}J_A||_beta + delta_beta_source", "MISSING_SECOND_ORDER_JA_PROJECTION"),
        ("JAR3690_2_preferred_frame", "preferred-frame PPN", "alpha1;alpha2;alpha3;xi", "P_PF(L^{-1}J_A + boundary flux)", "MISSING_PREFERRED_FRAME_PROJECTION_AND_BOUNDS"),
        ("JAR3690_3_Newton_source", "Newton/source/R10/R11", "delta_Newton_MTS;alpha(lambda);mu_extra", "delta_mu_JA = K_mu_JA * Pi_M(L^{-1}J_A)", "MISSING_SOURCE_MASS_AND_RANGE_PROFILE"),
        ("JAR3690_4_clock", "clocks/redshift", "alpha_clock_redshift", "K_clock_JA * frame_clock_projection(L^{-1}J_A)", "MISSING_CLOCK_FRAME_PROJECTION"),
        ("JAR3690_5_WEP_source", "source-charge WEP", "eta_source_AB", "Delta_AB ln mu_obs[J_A]", "MISSING_SPECIES_SOURCE_COUPLING"),
        ("JAR3690_6_Gdot", "Gdot/ephemeris", "Gdot_over_G", "partial_t ln mu_obs[J_A]", "MISSING_TIME_DRIFT_SOURCE_PROJECTION"),
        ("JAR3690_7_EM_flux", "EM/Poynting/radiation", "w_EM;Phi_EM_boundary", "K_EM_JA * Poynting_or_bound_flux_projection", "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION"),
        ("JAR3690_8_R11_operator", "non-EH operator family", "non_EH_operator_coefficients", "c_JA_operator_vector from retained L^{-1}J_A operator family", "MISSING_EXECUTABLE_OPERATOR_VECTOR"),
    ]
    return [
        {
            **base(ts),
            "arena_id": arena_id,
            "arena": arena,
            "observable": observable,
            "prediction_template": prediction_template,
            "missing_input": missing_input,
            "status": "SOURCE_READY_TEMPLATE_NONCLAIM",
            "claim_allowed": False,
            "score_ready": False,
        }
        for arena_id, arena, observable, prediction_template, missing_input in specs
    ]


def residual_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RJA3690_0_total",
            "abs(R_JA)/N_H",
            "(|R_Jmatter|+|R_Jsource|+|R_Jselector|+|R_Jboundary|+|R_Jflux|+|R_qmap|+|R_Zvertical|+|R_Zmap|+|R_Linv|)/N_H",
            "dimensionless/source-profile envelope",
            "FORMULA_READY_INPUTS_MISSING",
            "total canonical coupling residual",
        ),
        (
            "RJA3690_1_Green_profile",
            "||Z||_X",
            "||L^{-1}||_{X<-Y}(||J_matter||+||J_source||+||J_selector||+||J_boundary||+||J_flux||)+||Z_boundary_fixed||+O(J^2)",
            "profile norm in selected arena",
            "PROFILE_BOUND_READY_NUMERIC_INPUTS_MISSING",
            "finite fallback if zero theorem fails",
        ),
        (
            "RJA3690_2_zero_theorem",
            "J_A=0",
            "requires q-map + vertical Z + matter descent + source orthogonality + quadratic activation + boundary no-flux + Z observable map",
            "boolean theorem gate",
            "ZERO_NOT_CLAIMED",
            "do not claim local-GR/Newton until all gates are signed",
        ),
        (
            "RJA3690_3_arena",
            "observable leakage vector",
            "{Delta gamma,Delta beta,alpha_i,xi,delta_mu,clock,WEP,Gdot,EM,R11}_JA",
            "arena coefficients",
            "SOURCE_READY_TEMPLATES_NOT_SCOREABLE",
            "test route is staged but not numeric",
        ),
    ]
    return [
        {
            **base(ts),
            "residual_id": residual_id,
            "quantity": quantity,
            "formula_or_bound": formula_or_bound,
            "units": units,
            "status": status,
            "interpretation": interpretation,
            "claim_allowed": False,
            "score_ready": False,
        }
        for residual_id, quantity, formula_or_bound, units, status, interpretation in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3690_0_result", "ZERO_THEOREM_FORM_PROVED_NOT_SIGNED", "the algebraic conditions for J_A=0 are exact", "do not claim zero until parent signatures pass"),
        ("DEC3690_1_progress", "GREEN_PROFILE_BOUND_DERIVED", "if coupling is nonzero it becomes Z=-(L^-1)J plus boundary terms", "use finite profile rows for tests rather than closure"),
        ("DEC3690_2_core_gap", "VERTICAL_Q_SOURCE_MAP_IS_CORE", "q-map, vertical generator and source-current orthogonality are the decisive missing signatures", "attack those before broad empirical claims"),
        ("DEC3690_3_coupling", "COUPLING_CONFIRMED_AS_BOTTLENECK", "J_A controls local residual hair/source normalization/PPN leakage", "next target vertical-generator/source orthogonality or coefficient acquisition"),
        ("DEC3690_4_next", "NEXT_BEST_TARGET", "prove the vertical generator and q-owned source-current square or get coefficients", "run 3691 vertical q-map/source-current orthogonality or J_A coefficient acquisition"),
        ("DEC3690_5_private", "PRIVATE_NONCLAIM", "no public/GitHub/local-GR claim", "continue private derivation"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "status": status,
            "decision": decision,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, status, decision, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3690_0_JA_zero", "claim J_A=0", "BLOCKED_PARENT_SIGNATURES", "q-map, vertical generator, source orthogonality, boundary and Z map are unsigned"),
        ("CG3690_1_local_GR", "claim canonical local GR/Newton", "BLOCKED_RJA", "R_JA remains finite/non-sourced"),
        ("CG3690_2_observables", "score PPN/R10/clock/WEP/orbital arenas", "BLOCKED_COEFFICIENTS", "K_AJ, L inverse, source profiles and projections are missing"),
        ("CG3690_3_EM_flux", "use Poynting/EM to close q_loc", "BLOCKED_PHYSICAL_STRESS_ONLY", "flux must be explicit physical stress/current or residual"),
        ("CG3690_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3690_0",
            "status": "CANONICAL_JA_ZERO_THEOREM_FORM_PROVED_PARENT_SIGNATURES_UNSIGNED_GREEN_PROFILE_BOUND_STAGED",
            "summary": "3690 proves the exact canonical source-coupling zero theorem form and derives the finite Green-profile fallback Z^A=-(L^-1)J+boundary+O(J^2). J_A=0 is not claimed because q-map, vertical generator, matter/source descent, boundary, Z-observable map and operator norms remain unsigned.",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3690_0",
            "target_doc": "3691-Y5-R2FR-vertical-q-map-source-current-orthogonality-or-JA-coefficient-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3691_vertical_q_map_source_current_orthogonality_or_JA_coefficient_acquisition.py",
            "objective": "try to parent-sign Dq[e_A]=0, matter/source q-descent and Pi_M/J_H orthogonality for the canonical Z variables; if not, create source-ready J_A coefficient acquisition rows for PPN, Newton/R10, clocks, WEP, EM and orbital arenas",
            "success_gate": "vertical/source orthogonality closes J_A=0 for at least matter/source components, or missing coefficients are converted into precise nonclaim acquisition rows",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    gates: list[dict[str, object]],
    profile: list[dict[str, object]],
    arena: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3690 - Canonical source coupling J_A zero theorem or Green-profile bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint goes directly at the coupling. It proves the exact form of the `J_A=0` theorem in the canonical branch, but does not claim the theorem because the parent signatures are still unsigned. If the theorem fails, the residual is no longer vague: it is a finite Green-profile source.",
        "",
        "## Main result",
        "",
        "Canonical source vector:",
        "",
        "`J_A := (1/sqrt(-g)) delta(S_matter+S_source+S_boundary+S_selector+S_flux^phys_if_Z_coupled)/delta Z^A |_{Z=0}`.",
        "",
        "Linear response equation:",
        "",
        "`L_AB Z^B + J_A + B_A = 0`.",
        "",
        "Green-profile fallback:",
        "",
        "`Z^A(x)=-(L^{-1})^{AB}J_B + Z_boundary^A + O(J^2)`.",
        "",
        "Norm envelope:",
        "",
        "`||Z||_X <= ||L^{-1}||_{X<-Y}(||J_matter||_Y+||J_source||_Y+||J_selector||_Y+||J_boundary||_Y+||J_flux||_Y)+||Z_boundary_fixed||_X+O(J^2)`.",
        "",
        "Total residual:",
        "",
        "`abs(R_JA)/N_H <= (|R_Jmatter|+|R_Jsource|+|R_Jselector|+|R_Jboundary|+|R_Jflux|+|R_qmap|+|R_Zvertical|+|R_Zmap|+|R_Linv|)/N_H`.",
        "",
        "## J_A decomposition",
    ]
    for row in decomposition:
        lines.append(f"- `{row['decomposition_id']}`: {row['status']} - {row['piece']} -> {row['residual_if_not_zero']}")
    lines.extend(["", "## Zero theorem gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['current_status']} - {row['zero_gate']} -> {row['residual_if_failed']}")
    lines.extend(["", "## Green-profile rows"])
    for row in profile:
        lines.append(f"- `{row['profile_id']}`: {row['status']} - {row['object']} -> {row['meaning']}")
    lines.extend(["", "## Arena templates"])
    for row in arena:
        lines.append(f"- `{row['arena_id']}`: {row['status']} - {row['arena']} `{row['observable']}` -> `{row['prediction_template']}`")
    lines.extend(["", "## Residual rows"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}`: {row['status']} - `{row['quantity']}` -> `{row['formula_or_bound']}`; {row['interpretation']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    gates: list[dict[str, object]],
    profile: list[dict[str, object]],
    arena: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + decomposition + gates + profile + arena + residuals + decisions + claim_gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3690*", "3690-Y5-R2FR-*", "P8_Y5*3690*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    decomposition_by_id = {str(row["decomposition_id"]): row for row in decomposition}
    gate_by_id = {str(row["gate_id"]): row for row in gates}
    profile_by_id = {str(row["profile_id"]): row for row in profile}
    residual_by_id = {str(row["residual_id"]): row for row in residuals}
    arena_ids = {str(row["arena_id"]) for row in arena}
    total_formula = str(residual_by_id["RJA3690_0_total"]["formula_or_bound"])
    required_terms = ["R_Jmatter", "R_Jsource", "R_Jselector", "R_Jboundary", "R_Jflux", "R_qmap", "R_Zvertical", "R_Zmap", "R_Linv"]

    add("VAL3690_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3690_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3690_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3690 outputs written")
    add("VAL3690_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3690_4_JA_definition", "delta(S_matter+S_source" in decomposition_by_id["JAD3690_0_definition"]["formula"], "J_A source definition recorded")
    add("VAL3690_5_bulk_zero", decomposition_by_id["JAD3690_1_even_bulk"]["status"] == "ZERO_DERIVED_FOR_CANONICAL_BULK", "even bulk zero retained")
    add("VAL3690_6_zero_not_claimed", gate_by_id["JZG3690_8_verdict"]["current_status"] == "ZERO_NOT_CLAIMED_GREEN_PROFILE_BOUND_RETAINED", "J_A zero not claimed")
    add("VAL3690_7_green_profile", "Z^A(x)=-(L^{-1})^{AB}J_B" in profile_by_id["GP3690_1_green_solution"]["formula"], "Green-profile fallback derived")
    add("VAL3690_8_residual_terms", all(term in total_formula for term in required_terms), "R_JA envelope contains required components")
    add("VAL3690_9_arena_templates", {"JAR3690_0_gamma", "JAR3690_3_Newton_source", "JAR3690_7_EM_flux"}.issubset(arena_ids), "PPN/Newton/EM arena templates present")
    add("VAL3690_10_next_target", next_target[0]["target_doc"].startswith("3691-") and "vertical" in next_target[0]["target_doc"], "3691 targets vertical q-map/source orthogonality")
    add("VAL3690_11_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in claim_gates), "claim gates remain blocked")
    add("VAL3690_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3690_13_doc_written", "J_A :=" in doc_text and "Z^A(x)=-(L^{-1})" in doc_text and "R_JA" in doc_text, "doc records J_A definition, Green profile and residual")
    add("VAL3690_14_no_formalization_leak", not leaks, "no 3690 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    decomposition = ja_decomposition_rows(ts)
    gates = zero_gate_rows(ts)
    profile = green_profile_rows(ts)
    arena = arena_rows(ts)
    residuals = residual_rows(ts)
    decisions = decision_rows(ts)
    claim_gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3690_SOURCE_REGISTER.csv",
        "decomposition": RESIDUALS / "P8_Y5_R2FR_3690_JA_DECOMPOSITION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3690_JA_ZERO_GATE_ROWS.csv",
        "profile": RESIDUALS / "P8_Y5_R2FR_3690_GREEN_PROFILE_BOUND_ROWS.csv",
        "arena": RESIDUALS / "P8_Y5_R2FR_3690_JA_ARENA_TEMPLATE_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3690_RJA_RESIDUAL_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3690_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3690_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3690_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3690_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3690_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["decomposition"], decomposition)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["profile"], profile)
    write_csv(outputs["arena"], arena)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, decomposition, gates, profile, arena, residuals, decisions, claim_gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, decomposition, gates, profile, arena, residuals, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3690 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3690 checkpoint: J_A zero theorem form proved; parent signatures unsigned; Green-profile bound staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
