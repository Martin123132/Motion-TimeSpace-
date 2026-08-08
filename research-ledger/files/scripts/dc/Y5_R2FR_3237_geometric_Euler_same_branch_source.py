from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3237-Y5-R2FR-geometric-Euler-same-branch-source-zero-or-bound-for-Jperp-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3237_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3237_GEOMETRIC_EULER_DERIVATION.csv"
GATES = OUT / "P8_Y5_R2FR_3237_SAME_BRANCH_EULER_GATES.csv"
BOUND = OUT / "P8_Y5_R2FR_3237_JGEOM_COMPONENT_BOUND.csv"
UPDATE = OUT / "P8_Y5_R2FR_3237_JPERP_LOCAL_GR_GATE_UPDATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3237_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3237_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_terms = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered_terms):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:220]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


SOURCES = [
    {
        "input_id": "SRC3237_00_3236_handoff",
        "location": "post_checkpoint",
        "relative_path": "3236-Y5-R2FR-memory-projector-domain-commutation-or-finite-bound-for-Jperp-under-AX1090.md",
        "role": "3236 handoff selecting geometric/Euler source as remaining top-level J_perp channel",
        "terms": ["3237-Y5-R2FR-geometric", "J_geom_bound", "geometric/Euler", "remaining top-level"],
    },
    {
        "input_id": "SRC3237_01_3231_geom_source",
        "location": "post_checkpoint",
        "relative_path": "3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md",
        "role": "J_perp source decomposition and geometric/source curvature row",
        "terms": ["JPA3231_1_geom", "MISSING_PARENT_EULER_SAME_BRANCH", "J_geom_bound"],
    },
    {
        "input_id": "SRC3237_02_3230_transverse_operator",
        "location": "post_checkpoint",
        "relative_path": "3230-Y5-R2FR-transverse-branch-amplitude-bound-for-Etransport-under-AX1090.md",
        "role": "transverse operator law O_perp v_perp = J_perp plus source terms",
        "terms": ["O_perp v_perp", "J_perp^tau", "v_perp"],
    },
    {
        "input_id": "SRC3237_03_1009_parent_chain",
        "location": "post_checkpoint",
        "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "role": "parent action hard block and Gamma/Khat/q_loc action-existence target",
        "terms": ["S_GK", "Gamma_eff/K_hat/q_loc", "Euler closure", "double-zero"],
    },
    {
        "input_id": "SRC3237_04_1010_qloc_route",
        "location": "post_checkpoint",
        "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "role": "exact q_loc route, metric-response identity, Helmholtz gap, Euler/double-zero gate",
        "terms": ["q_loc^nu", "Helmholtz", "K_hat", "Delta_K"],
    },
    {
        "input_id": "SRC3237_05_1025_euler_zero_precedent",
        "location": "post_checkpoint",
        "relative_path": "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "role": "branch extremum precedent showing parent Euler zero is not automatic",
        "terms": ["MISSING_PARENT_EULER_ZERO", "parent Euler expression", "Euler"],
    },
    {
        "input_id": "SRC3237_06_3236_jperp_update",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3236_JPERP_UPDATE.csv",
        "role": "machine-readable current J_perp sum with J_geom_bound still unresolved",
        "terms": ["J_geom_bound", "J_memory_projector_bound", "J_perp"],
    },
    {
        "input_id": "SRC3237_07_3231_source_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv",
        "role": "machine-readable J_geom row and missing same-branch parent Euler gate",
        "terms": ["JPA3231_1_geom", "MISSING_PARENT_EULER_SAME_BRANCH", "geometric/source curvature"],
    },
    {
        "input_id": "SRC3237_08_gk_first_variation",
        "location": "mts_residuals",
        "relative_path": "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "role": "Gamma/Khat/q_loc action-existence, Helmholtz, Euler, double-zero, projector, boundary contract",
        "terms": ["GK513_0_action_existence", "GK513_2_Euler_closure", "GK513_3_double_zero", "GK513_5_boundary_no_flux"],
    },
    {
        "input_id": "SRC3237_09_gk_action_candidates",
        "location": "mts_residuals",
        "relative_path": "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "role": "candidate S_GK routes and residual fallback",
        "terms": ["GK514_A_metric_response_scalar_density", "q_loc becomes the Ward residual", "fallback_required"],
    },
    {
        "input_id": "SRC3237_10_metric_response_evidence",
        "location": "mts_residuals",
        "relative_path": "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
        "role": "evidence ledger that metric response is required but not yet matched",
        "terms": ["Gamma_eff", "K_hat", "required_gate", "metric-response"],
    },
    {
        "input_id": "SRC3237_11_1009_claim_gate",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1009_CLAIM_GATE.csv",
        "role": "claim gate keeping local-GR closed while GK/q_loc clauses are unsigned",
        "terms": ["CG1009_3_GK_q_loc_zero", "CG1009_5_Htau_MHref_local_GR", "false"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": bool_text(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    derivation_rows = [
        {
            "derivation_id": "GEO3237_0_object",
            "object": "geometric transverse source",
            "formula": "J_geom := P_perp[delta_perp E_loc(Phi0)] + P_perp[(delta_perp O_loc)v_parallel] + B_geom[v_perp] + W_geom[v_perp]",
            "zero_route": "bulk part vanishes if E_loc=0 on the same parent branch, O_loc is the linearized Euler operator of the parent action, P_perp removes gauge/reparametrization directions, and boundary/worldtube terms are silent",
            "finite_residual": "otherwise retain ||J_geom||_2 as a no-cancellation component of J_perp",
            "status": "GEOMETRIC_SOURCE_DEFINITION_SHARPENED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GEO3237_1_first_variation",
            "object": "parent Euler first variation",
            "formula": "delta_v S_loc = integral_M E_A(Phi) v^A sqrt(-g)d^4x + integral_boundary Theta(v)",
            "zero_route": "for v_perp on the same solution branch, E_A(Phi0)=0 and Theta(v_perp)=0 imply no bulk source from the parent Euler block",
            "finite_residual": "J_Euler_residual_bound := C_E ||E_parent(Phi0)||_2 + C_boundary ||Theta_geom[v_perp]||",
            "status": "CONDITIONAL_EULER_ZERO_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GEO3237_2_Ward_q_loc_link",
            "object": "q_loc Ward/Euler identity",
            "formula": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_GK^nu, with q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu})",
            "zero_route": "if S_GK exists, K_hat=K_metric[Gamma_eff], Helmholtz holds, E_A=0, B_GK=0, and P_loc is parent-owned, then q_loc^nu=0 follows rather than being imposed",
            "finite_residual": "J_q_loc_bound := C_q ||q_loc||_2 + C_K ||Delta_K||_2 + C_H ||H_GK||_2 + C_BGK ||B_GK||",
            "status": "WARD_ROUTE_WRITTEN_QLOC_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GEO3237_3_same_branch",
            "object": "same-branch/gauge exclusion",
            "formula": "P_perp E_A=0 is legal only after P_perp is defined by the parent tangent split T_C = T_gauge + T_branch + T_perp and commutes with the local readout limit",
            "zero_route": "same-branch theorem requires v_perp not to move the physical solution family, source labels, domain, or observer readout",
            "finite_residual": "J_branch_bound := C_branch ||D_perp P_branch||_op ||E_parent|| + C_readout ||D_perp R_readout||",
            "status": "SAME_BRANCH_CLAUSE_EXPLICIT",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GEO3237_4_double_zero",
            "object": "local fixed-point amplitude/first derivative",
            "formula": "T_GK(Phi0)=0 and D_perp T_GK(Phi0)=0, equivalently Gamma_eff(Phi0)g-K_hat(Phi0)=0 and D_perp[Gamma_eff g-K_hat]_{Phi0}=0",
            "zero_route": "if the response sector is even/quadratic around the local branch and the metric response is exact, PPN/source hair begins at controlled second order",
            "finite_residual": "J_F1_bound := C_F1 ||D_perp[Gamma_eff g-K_hat]_{Phi0}||",
            "status": "DOUBLE_ZERO_NEEDED_NOT_PROVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "GEO3237_5_total_zero",
            "object": "J_geom=0 theorem shape",
            "formula": "J_geom=0 if parent action, metric response, Helmholtz integrability, Euler on-shellness, double-zero, same-branch projector ownership, and boundary/worldtube silence all hold together",
            "zero_route": "this is a proper derivation route to local-GR silence, not a plateau axiom",
            "finite_residual": "if any clause is unsigned, use JGB3237_8_total_abs_guard",
            "status": "ZERO_THEOREM_CONDITIONAL_FAILS_CURRENT_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    gate_rows = [
        {
            "gate_id": "GEG3237_0_parent_action",
            "gate": "local parent action exists",
            "statement": "S_loc contains a diffeomorphism-invariant local sector S_GK whose fields also define Gamma_eff and K_hat.",
            "status": "UNSIGNED",
            "failure_mode": "Gamma_eff/K_hat stay bookkeeping terms and cannot produce an Euler/Ward zero",
            "effect": "retain q_loc and J_geom residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_1_metric_response",
            "gate": "K_hat metric response",
            "statement": "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff] including volume, derivative, connection, and boundary terms.",
            "status": "UNSIGNED",
            "failure_mode": "Delta_K=K_hat-K_metric survives and acts as local force/source hair",
            "effect": "retain J_metric_response_gap_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_2_Helmholtz",
            "gate": "Helmholtz integrability",
            "statement": "the proposed stress has symmetric second variation up to boundary/gauge terms.",
            "status": "UNSIGNED",
            "failure_mode": "no variational action exists for the claimed stress",
            "effect": "retain J_Helmholtz_gap_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_3_Euler_on_shell",
            "gate": "same-branch Euler equations",
            "statement": "the local exterior is an on-shell solution of the same parent Euler equations used to define the local operator.",
            "status": "UNSIGNED",
            "failure_mode": "MISSING_PARENT_EULER_SAME_BRANCH remains the geometric source",
            "effect": "retain J_Euler_residual_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_4_double_zero",
            "gate": "fixed point double-zero",
            "statement": "the local response stress and its first transverse derivative vanish at Phi0.",
            "status": "UNSIGNED",
            "failure_mode": "F_1 survives and PPN/source-normalization hair appears at first order",
            "effect": "retain J_F1_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_5_projector_branch",
            "gate": "parent-owned same-branch projector",
            "statement": "P_perp and P_loc are parent-owned, commute with the local limit, and exclude gauge/reparametrization directions without readout tuning.",
            "status": "UNSIGNED",
            "failure_mode": "projector/readout variation can hide force components",
            "effect": "retain J_branch_bound and J_projection_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_6_boundary_worldtube",
            "gate": "geometric boundary and worldtube silence",
            "statement": "Theta_geom, corner terms, source-worldtube displacements, and symplectic flux vanish or are proper/topological.",
            "status": "UNSIGNED",
            "failure_mode": "bulk Euler zero leaks through boundary/collar terms",
            "effect": "retain J_boundary_geom_bound and J_worldtube_geom_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "GEG3237_7_verdict",
            "gate": "geometric source zero",
            "statement": "J_geom=0 requires all prior gates together; no single GR/Bianchi analogy or plateau statement is enough.",
            "status": "FAIL_CURRENT_CLAIM",
            "failure_mode": "geometric source remains a named residual in J_perp",
            "effect": "local-GR/PPN branch stays blocked but with a sharper residual vector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    bound_rows = [
        {
            "bound_id": "JGB3237_0_Euler_residual",
            "quantity": "J_Euler_residual_bound",
            "formula": "||P_perp E_parent(Phi0)||_2 <= C_E ||E_parent(Phi0)||_2",
            "required_inputs": "parent Euler equations; local exterior branch; norm and units for E_parent",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_1_metric_response_gap",
            "quantity": "J_metric_response_gap_bound",
            "formula": "||P_loc nabla_mu Delta_K^{mu nu}||_2 <= C_K ||Delta_K||_{H1}",
            "required_inputs": "Gamma_eff formula; K_hat formula; derivative/boundary convention; H1 norm",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_2_Helmholtz_gap",
            "quantity": "J_Helmholtz_gap_bound",
            "formula": "||J_H||_2 <= C_H ||H_GK|| where H_GK is the antisymmetric second-variation obstruction",
            "required_inputs": "stress functional; second variation calculation; boundary symmetry class",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_3_q_loc_residual",
            "quantity": "J_q_loc_bound",
            "formula": "||P_loc(nabla Gamma_eff - div K_hat)||_2 <= C_q ||q_loc||_2",
            "required_inputs": "q_loc profile or theorem-zero; P_loc ownership; local test projection units",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_4_double_zero_F1",
            "quantity": "J_F1_bound",
            "formula": "||D_perp T_GK(Phi0)||_2 <= C_F1 ||D_perp[Gamma_eff g-K_hat]_{Phi0}||_2",
            "required_inputs": "fixed point Phi0; response Hessian; first-variation source path",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_5_branch_projector",
            "quantity": "J_branch_bound",
            "formula": "||(D_perp P_branch)E_parent||_2 <= C_branch ||D_perp P_branch||_op ||E_parent||_2",
            "required_inputs": "parent tangent split; branch projector; operator norm or theorem-zero",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_6_boundary_geom",
            "quantity": "J_boundary_geom_bound",
            "formula": "||B_geom[v_perp]|| <= C_B||Theta_geom[v_perp]|| + C_corner||corner_geom||",
            "required_inputs": "boundary symplectic potential; collar/corner terms; no-flux theorem or numeric norm",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_7_worldtube_geom",
            "quantity": "J_worldtube_geom_bound",
            "formula": "||W_geom[v_perp]|| <= C_W ||Delta_W_geom||",
            "required_inputs": "source worldtube definition; displacement map; local support/collar norm",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "JGB3237_8_total_abs_guard",
            "quantity": "J_geom_bound",
            "formula": "||J_geom||_2 <= J_Euler_residual_bound + J_metric_response_gap_bound + J_Helmholtz_gap_bound + J_q_loc_bound + J_F1_bound + J_branch_bound + J_boundary_geom_bound + J_worldtube_geom_bound",
            "required_inputs": "each component theorem-zero or finite source-backed numeric bound; no cancellation allowed",
            "status": "NO_CANCELLATION_BOUND_READY_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3237_0_refined_jperp",
            "target": "J_perp source norm",
            "formula": "||J_perp^tau||_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4)C_F2_perp||F^2||_2 + J_Poynting_bound + J_memory_projector_bound",
            "change": "J_geom_bound is now the explicit JGB3237_8 no-cancellation envelope rather than an opaque placeholder",
            "status": "REFINED_LOCAL_GR_RESIDUAL_VECTOR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3237_1_q_loc_gate",
            "target": "q_loc/local PPN gate",
            "formula": "q_loc^nu=0 only after S_GK, Delta_K=0, H_GK=0, E_A=0, double-zero, P_loc ownership, and boundary silence",
            "change": "geometric source zero has been reduced to the Gamma/Khat metric-response/Helmholtz/Euler problem instead of a plateau axiom",
            "status": "QLOC_REMAINS_EXPLICIT_RESIDUAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3237_2_transverse_amplitude",
            "target": "transverse amplitude law",
            "formula": "a_perp=J_perp_bound/m_perp_min, with J_perp_bound now carrying JGB3237_8",
            "change": "any unsigned geometric/Euler piece feeds the local branch amplitude and clock/PPN residual estimate",
            "status": "FEEDS_3230_YPERP_AND_LOCAL_TESTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3237_0_result",
            "decision": "GEOMETRIC_EULER_ZERO_ROUTE_DERIVED_AS_CONDITIONAL_QLOC_REMAINS_RESIDUAL",
            "because": "a clean Euler/Ward route exists in theorem shape, but it requires S_GK, exact metric response, Helmholtz integrability, on-shell same-branch Euler equations, double-zero, projector ownership, and boundary/worldtube silence; those are not parent-signed together",
            "claim_status": "NO_LOCAL_GR_NO_NEWTON_NO_PPN_NO_CLOCK_NO_R10_CLAIM",
            "next_action": "do not drop J_geom; carry JGB3237_8 in J_perp until the Gamma/Khat metric-response and Helmholtz clauses are either proved or numerically bounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3237_1_next_target",
            "decision": "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090",
            "because": "3237 shows the geometric source problem bottlenecks at the actual S_GK/K_hat/Gamma_eff variational owner rather than at another source-channel audit",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "try to construct or reject S_GK by checking K_hat=K_metric[Gamma_eff] and Helmholtz symmetry; if it fails, keep q_loc as a finite local residual input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    output_paths = [INPUTS, DERIVATION, GATES, BOUND, UPDATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    evidence_ready = all("MISSING_SOURCE" not in str(row["evidence_hits"]) and "NO_MATCH" not in str(row["evidence_hits"]) for row in input_rows)
    euler_identity = any(row["derivation_id"] == "GEO3237_1_first_variation" for row in derivation_rows)
    qloc_identity = any("q_loc^nu" in str(row["formula"]) and "Helmholtz" in str(row["zero_route"]) for row in derivation_rows)
    gates_present = {"GEG3237_1_metric_response", "GEG3237_2_Helmholtz", "GEG3237_3_Euler_on_shell", "GEG3237_6_boundary_worldtube"}.issubset(
        {str(row["gate_id"]) for row in gate_rows}
    )
    total_bound = any(row["bound_id"] == "JGB3237_8_total_abs_guard" and "J_geom_bound" in str(row["quantity"]) for row in bound_rows)
    jperp_update = any(row["update_id"] == "UP3237_0_refined_jperp" and "J_geom_bound" in str(row["formula"]) for row in update_rows)
    next_target = decision_rows[-1]["decision"].startswith("3238-")
    claim_true_count = 0
    for row_group in [input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows]:
        for row in row_group:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(not str(path).lower().startswith(str(FW).lower()) for path in output_paths + [DOC])
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in output_paths:
        try:
            parsed_rows = read_csv(path)
            if not parsed_rows:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3237_00_inputs_exist", "pass": bool_text(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3237_01_evidence_hits", "pass": bool_text(evidence_ready), "detail": "no MISSING_SOURCE or NO_MATCH in source register", "generated_utc": now},
        {"check_id": "VAL3237_02_Euler_variation", "pass": bool_text(euler_identity), "detail": "parent Euler first-variation route present", "generated_utc": now},
        {"check_id": "VAL3237_03_q_loc_Ward_route", "pass": bool_text(qloc_identity), "detail": "q_loc Ward/Euler route and Helmholtz dependency present", "generated_utc": now},
        {"check_id": "VAL3237_04_gates_present", "pass": bool_text(gates_present), "detail": "metric response, Helmholtz, Euler, and boundary gates present", "generated_utc": now},
        {"check_id": "VAL3237_05_total_bound", "pass": bool_text(total_bound), "detail": "J_geom no-cancellation envelope present", "generated_utc": now},
        {"check_id": "VAL3237_06_jperp_update", "pass": bool_text(jperp_update), "detail": "J_perp refined with JGB3237_8", "generated_utc": now},
        {"check_id": "VAL3237_07_claims_blocked", "pass": bool_text(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3237_08_no_formalization_workbench_edit", "pass": bool_text(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3237_09_csv_parse", "pass": bool_text(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3237_10_next_target", "pass": bool_text(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3237 - Geometric Euler Same-branch Source Zero Or Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, PPN pass, R10 pass, clock pass, source-normalization claim, or public-facing result.

## Result

3237 sharpens the remaining geometric piece of the transverse source vector.

The useful thing we can derive is conditional:

```text
delta_v S_loc
= integral_M E_A(Phi) v^A sqrt(-g)d^4x
 + integral_boundary Theta(v).
```

So the geometric source can vanish only if the local exterior is on shell for the same parent Euler system, the transverse projector is parent-owned and not a readout trick, and the boundary/worldtube terms are silent.

For the Gamma/Khat/q_loc part the real route is:

```text
nabla_mu T_GK^{{mu nu}}
= sum_A E_A nabla^nu Phi^A + B_GK^nu,

q_loc^nu
= P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}).
```

Thus `q_loc^nu=0` is derivable only if `S_GK` exists, `K_hat=K_metric[Gamma_eff]`, Helmholtz integrability holds, the branch is on shell, the local fixed point is double-zero, and boundary/projector clauses close.

The no-cancellation envelope is:

```text
||J_geom||_2
<= J_Euler_residual_bound
 + J_metric_response_gap_bound
 + J_Helmholtz_gap_bound
 + J_q_loc_bound
 + J_F1_bound
 + J_branch_bound
 + J_boundary_geom_bound
 + J_worldtube_geom_bound.
```

Current verdict: `GEOMETRIC_EULER_ZERO_ROUTE_DERIVED_AS_CONDITIONAL_QLOC_REMAINS_RESIDUAL`.

This is progress, but not a claim: the geometric source problem is now reduced to the actual `S_GK/K_hat/Gamma_eff` variational-owner problem rather than being left as a vague missing piece.

## Geometric Euler Derivation

{md_table(derivation_rows, ["derivation_id", "object", "formula", "zero_route", "finite_residual", "status", "valid_for_claim"])}

## Same-branch Euler Gates

{md_table(gate_rows, ["gate_id", "gate", "statement", "status", "failure_mode", "effect", "valid_for_claim"])}

## Jgeom Component Bound

{md_table(bound_rows, ["bound_id", "quantity", "formula", "required_inputs", "status", "valid_for_claim"])}

## Jperp Local-GR Gate Update

{md_table(update_rows, ["update_id", "target", "formula", "change", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_GEOMETRIC_EULER_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_SAME_BRANCH_EULER_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_JGEOM_COMPONENT_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_JPERP_LOCAL_GR_GATE_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3237_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (DERIVATION, derivation_rows),
        (GATES, gate_rows),
        (BOUND, bound_rows),
        (UPDATE, update_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, derivation_rows, gate_rows, bound_rows, update_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
