from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3238_INPUTS.csv"
CANDIDATES = OUT / "P8_Y5_R2FR_3238_SGK_CANDIDATE_COMPARATOR.csv"
METRIC_RESPONSE = OUT / "P8_Y5_R2FR_3238_METRIC_RESPONSE_TEST.csv"
HELMHOLTZ = OUT / "P8_Y5_R2FR_3238_HELMHOLTZ_OPERATOR_TEST.csv"
QLOC_BOUND = OUT / "P8_Y5_R2FR_3238_QLOC_BOUND_INTERFACE.csv"
UPDATE = OUT / "P8_Y5_R2FR_3238_LOCAL_GR_GATE_UPDATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3238_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3238_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
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
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
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
        "input_id": "SRC3238_00_3237_handoff",
        "location": "post_checkpoint",
        "relative_path": "3237-Y5-R2FR-geometric-Euler-same-branch-source-zero-or-bound-for-Jperp-under-AX1090.md",
        "role": "3237 handoff reducing J_geom to SGK/Khat/Gamma_eff owner problem",
        "terms": ["DEC3237_1_next_target", "S_GK/K_hat/Gamma_eff", "q_loc^nu"],
    },
    {
        "input_id": "SRC3238_01_2799_route",
        "location": "post_checkpoint",
        "relative_path": "2799-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-residual-retention-under-AX1090.md",
        "role": "earlier action-existence ladder and q_loc residual retention",
        "terms": ["HGS2799_2_Helmholtz", "QRES2799_1_Gamma_metric_response_gap", "FAIL_CURRENT_CLAIM"],
    },
    {
        "input_id": "SRC3238_02_2941_template",
        "location": "post_checkpoint",
        "relative_path": "2941-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-parent-action-adoption-gate-under-AX1090.md",
        "role": "weak A_nu action template and strong adoption failure",
        "terms": ["PASS_AS_CONSTRUCTIVE_ACTION_TEMPLATE", "S_GK", "strong Helmholtz/adoption"],
    },
    {
        "input_id": "SRC3238_03_2942_A_origin",
        "location": "post_checkpoint",
        "relative_path": "2942-Y5-R2FR-vertical-generator-origin-gauge-symmetry-or-A-mu-closure-demotion-under-AX1090.md",
        "role": "A_mu origin obstruction and closure-only demotion",
        "terms": ["CLOSURE_ONLY_UNTIL", "A_mu", "Ward"],
    },
    {
        "input_id": "SRC3238_04_3076_symbol_match",
        "location": "post_checkpoint",
        "relative_path": "3076-Y5-R2FR-Gamma-eff-Khat-symbol-match-or-P4-numeric-vector-under-AX1090.md",
        "role": "Gamma_eff/Khat symbol-match obstruction and Delta_K vector",
        "terms": ["Delta_K", "KMR3076_2_tensor_identity", "SYMBOL_MATCH_NOT_SIGNED"],
    },
    {
        "input_id": "SRC3238_05_metric_contract",
        "location": "mts_residuals",
        "relative_path": "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "role": "metric response pass/fail contract",
        "terms": ["MR514_1_Khat_metric_response", "MR514_5_double_zero", "MR514_2_Ward_identity"],
    },
    {
        "input_id": "SRC3238_06_2941_gate",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv",
        "role": "machine weak action pass and strong adoption fail",
        "terms": ["GKT2941_0_weak_action_existence", "PASS_AS_CONSTRUCTIVE_ACTION_TEMPLATE", "FAIL_CURRENT_STRONG_ADOPTION"],
    },
    {
        "input_id": "SRC3238_07_2941_helmholtz",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2941_HELMHOLTZ_STRONG_ADOPTION_GATE.csv",
        "role": "Helmholtz/adoption split",
        "terms": ["HG2941_0_A_equation", "HG2941_2_existing_symbol_match", "HG2941_7_strong_verdict"],
    },
    {
        "input_id": "SRC3238_08_2942_demotion",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2942_SGK_CLOSURE_DEMOTION_LEDGER.csv",
        "role": "S_GK closure-only policy after A_mu origin fails",
        "terms": ["DEM2942_0_SGK_status", "DEM2942_2_A_mu_status", "DEM2942_3_multiplier_guard"],
    },
    {
        "input_id": "SRC3238_09_3076_Khat_match",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3076_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
        "role": "Khat component-level metric-response match audit",
        "terms": ["KMR3076_2_tensor_identity", "KMR3076_8_helmholtz", "MISSING_COMPONENT_FORMULA"],
    },
    {
        "input_id": "SRC3238_10_3076_DeltaK",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3076_DELTAK_OBSTRUCTION_VECTOR_NONCLAIM.csv",
        "role": "Delta_K obstruction vector and component source needs",
        "terms": ["DK3076_0_total", "Delta_K_total", "DeltaK_00"],
    },
    {
        "input_id": "SRC3238_11_3076_Gamma_owner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3076_GAMMA_EFF_OWNER_AUDIT.csv",
        "role": "Gamma_eff density owner audit",
        "terms": ["GEO3076_0_live_symbol_role", "NOT_LIVE_SCALAR_DENSITY_OWNER", "MISSING_PARENT_DENSITY_FORMULA"],
    },
    {
        "input_id": "SRC3238_12_3064_double_zero",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3064_GK_DOUBLE_ZERO_ATTEMPT.csv",
        "role": "double-zero attempt and remaining physical basis/gap blockers",
        "terms": ["DZGK3064_1_derivative_zero", "CONDITIONAL_TEMPLATE_ONLY", "MISSING_Z_BASIS_PHYSICAL_LOCK"],
    },
    {
        "input_id": "SRC3238_13_3237_bound",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3237_JGEOM_COMPONENT_BOUND.csv",
        "role": "J_geom bound rows that 3238 refines through Delta_K/Helmholtz/q_loc",
        "terms": ["JGB3237_1_metric_response_gap", "JGB3237_2_Helmholtz_gap", "JGB3237_8_total_abs_guard"],
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
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    candidate_rows = [
        {
            "candidate_id": "SGKC3238_0_weak_A_template",
            "candidate": "synthetic A_nu action template",
            "action": "S_A=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma]+B_GK",
            "derivation_test": "delta_A S_A gives -nabla_mu Khat^{mu nu}+nabla^nu Gamma_eff-J_M^nu=0 with Khat^{mu nu}=partial L_K/partial(nabla_mu A_nu)",
            "pass_status": "WEAK_PASS_FORMAL_EULER_HELMHOLTZ",
            "adoption_status": "NOT_MTS_PARENT_ADOPTED",
            "why_not_claim": "A_nu, L_K, L_Gamma, J_M, P_loc and B_GK are not parent-derived; direct multiplier reading would manufacture closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SGKC3238_1_strong_metric_response",
            "candidate": "strong SGK scalar-density owner",
            "action": "S_GK=-int sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D)+B_GK",
            "derivation_test": "K_hat_live^{mu nu} must equal K_metric^{mu nu}[Gamma_eff]=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu} with all derivative/boundary terms",
            "pass_status": "FAIL_CURRENT_SOURCE_SET",
            "adoption_status": "DELTA_K_RETAINED",
            "why_not_claim": "Gamma_eff is not yet a live parent density and K_hat has no component birth certificate matching K_metric",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SGKC3238_2_response_doublet_even",
            "candidate": "even response-doublet density",
            "action": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) inside a parent scalar density",
            "derivation_test": "T_GK(Phi0)=0 and D_Z T_GK(Phi0)=0 if background subtraction, Z-basis, M_AB, and metric response are parent-owned",
            "pass_status": "CONDITIONAL_TEMPLATE_ONLY",
            "adoption_status": "DOUBLE_ZERO_NOT_PARENT_SIGNED",
            "why_not_claim": "physical Z/q_loc basis, M_AB owner, units, positivity, and readout evenness are missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "SGKC3238_3_residual_bound_branch",
            "candidate": "retain q_loc/Delta_K/H_GK residuals",
            "action": "no parent SGK action is accepted",
            "derivation_test": "q_loc and J_geom carry explicit residual norm rows until SGK/Khat/Helmholtz clauses close",
            "pass_status": "PASS_AS_DISCIPLINE_BRANCH",
            "adoption_status": "NONCLAIM_BOUND_INTERFACE_READY",
            "why_not_claim": "bounded residual is an honest test input, not a GR reduction proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    metric_rows = [
        {
            "test_id": "MRT3238_0_density_owner",
            "target": "Gamma_eff",
            "required_identity": "Gamma_eff=Gamma_eff(g,Phi,nablaPhi,D,branch) is a parent scalar density with units, no post-readout selector, and declared boundary convention",
            "current_result": "FAILED_CURRENT_SOURCE_SET",
            "residual_if_fail": "epsilon_Gamma_owner_abs enters Delta_K and q_loc",
            "next_evidence_needed": "source-backed Gamma_eff formula with field content, units, branch domain, metric dependence, and background subtraction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "MRT3238_1_metric_variation_operator",
            "target": "K_metric[Gamma_eff]",
            "required_identity": "K_metric^{mu nu}:=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu}, including derivative, improvement, connection, domain, and boundary terms",
            "current_result": "FORMAL_OPERATOR_DEFINED",
            "residual_if_fail": "none for the formal operator; live claim still requires symbol match",
            "next_evidence_needed": "explicit Gamma_eff density so K_metric can be computed component-by-component",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "MRT3238_2_live_Khat_match",
            "target": "Delta_K^{mu nu}",
            "required_identity": "Delta_K^{mu nu}:=K_hat_live^{mu nu}-K_metric^{mu nu}[Gamma_eff]=0 in 00, 0i, trace, tracefree, derivative/boundary and units slots",
            "current_result": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "residual_if_fail": "P_loc div Delta_K survives in q_loc and J_geom",
            "next_evidence_needed": "K_hat live tensor component birth certificate and term-by-term comparison to K_metric",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "test_id": "MRT3238_3_Ward_reduction",
            "target": "q_loc metric-response split",
            "required_identity": "q_loc^nu=P_loc[(nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu})-nabla_mu Delta_K^{mu nu}] plus projector/domain/boundary terms",
            "current_result": "DERIVED_AS_SPLIT_NOT_ZERO",
            "residual_if_fail": "local force is bounded by Euler/boundary plus Delta_K divergence",
            "next_evidence_needed": "same-branch Euler equations, boundary no-flux, P_loc commutator and Delta_K component norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    helmholtz_rows = [
        {
            "helmholtz_id": "H3238_0_definition",
            "target": "strong variational stress",
            "operator": "H_GK[(mu nu),(alpha beta)] := delta(sqrt(-g)T_hat^{mu nu})/delta g_{alpha beta} - delta(sqrt(-g)T_hat^{alpha beta})/delta g_{mu nu}",
            "zero_condition": "H_GK=0 up to boundary/gauge constraints is necessary for T_hat to be a Hilbert stress from a local action",
            "current_status": "OPERATOR_DEFINED_COMPONENTS_MISSING",
            "residual_if_fail": "J_Helmholtz_gap_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "helmholtz_id": "H3238_1_weak_A_sector",
            "target": "A_nu Euler equation",
            "operator": "A-sector Helmholtz passes because the synthetic equation is varied directly from S_A",
            "zero_condition": "synthetic A equation is action-generated",
            "current_status": "WEAK_PASS_ONLY",
            "residual_if_fail": "not the active problem; adoption fails elsewhere",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "helmholtz_id": "H3238_2_live_Khat_stress",
            "target": "existing MTS Gamma_eff/Khat stress",
            "operator": "evaluate H_GK using T_hat^{mu nu}=Gamma_eff g^{mu nu}-K_hat_live^{mu nu} under the signed convention",
            "zero_condition": "live Khat components satisfy second-variation symmetry with Gamma_eff density",
            "current_status": "NOT_EVALUABLE_WITHOUT_COMPONENT_BIRTH_CERTIFICATE",
            "residual_if_fail": "DeltaK_integrability and H_GK survive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "helmholtz_id": "H3238_3_boundary_domain",
            "target": "boundary/domain/improvement terms",
            "operator": "H_GK must include all derivative, Hodge, projector, corner and domain-response terms before declaring symmetry",
            "zero_condition": "boundary terms are exact/proper/topological or included symmetrically in the variation",
            "current_status": "UNSIGNED",
            "residual_if_fail": "B_GK and DeltaK_derivative_boundary survive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    qloc_rows = [
        {
            "bound_id": "QB3238_0_q_loc_split",
            "quantity": "q_loc^nu",
            "formula": "q_loc^nu=P_loc[(nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu})-nabla_mu Delta_K^{mu nu}]+projector/domain/boundary terms",
            "bound": "||q_loc||_D <= C_E||E_GK||_D + C_B||B_GK||_D + C_DK||Delta_K||_{H1(D)} + C_P||[P_loc,nabla]|| ||Delta_K||_D + C_H||H_GK||_D",
            "required_inputs": "E_GK; B_GK; Delta_K component norms; P_loc commutator norm; Helmholtz obstruction norm; arena units",
            "status": "BOUND_INTERFACE_DERIVED_VALUES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "QB3238_1_DeltaK_components",
            "quantity": "Delta_K component vector",
            "formula": "Delta_K=(DeltaK_00, DeltaK_0i, DeltaK_trace, DeltaK_TF, DeltaK_derivative_boundary, DeltaK_units, DeltaK_projector_domain)",
            "bound": "||Delta_K||_{H1} <= sum_c C_c ||DeltaK_c||_{H1}",
            "required_inputs": "component birth certificates and units for live K_hat and K_metric",
            "status": "COMPONENT_VECTOR_READY_SOURCE_BIRTH_CERTIFICATES_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "QB3238_2_Helmholtz_gap",
            "quantity": "H_GK",
            "formula": "H_GK=anti-symmetrized second metric variation of sqrt(-g)(Gamma_eff g-K_hat_live)",
            "bound": "J_Helmholtz_gap_bound <= C_H ||H_GK||_D",
            "required_inputs": "stress functional; tensor components; boundary convention; gauge/domain restrictions",
            "status": "OPERATOR_READY_NUMERIC_SYMBOLIC_EVALUATION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "QB3238_3_local_claim_gate",
            "quantity": "local-GR/Newton promotion",
            "formula": "promotion allowed only if q_loc=0 or all q_loc projections are below sourced PPN/R10/clock/orbital/source tolerances",
            "bound": "blocked until QB3238_0 through QB3238_2 are theorem-zero or sourced",
            "required_inputs": "projection coefficients and arena-specific bound rows",
            "status": "NO_LOCAL_GR_NO_NEWTON_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    update_rows = [
        {
            "update_id": "UP3238_0_3237_refinement",
            "target": "J_geom_bound",
            "formula": "J_geom_bound keeps J_metric_response_gap_bound + J_Helmholtz_gap_bound + J_q_loc_bound, now expressed through Delta_K/H_GK/q_loc split",
            "change": "3238 converts the 3237 SGK bottleneck into a concrete residual operator test rather than a generic missing action label",
            "status": "REFINED_GEOMETRIC_RESIDUAL_GATE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3238_1_weak_template_policy",
            "target": "S_GK weak action template",
            "formula": "weak A_nu action can generate the q current, but cannot be promoted until A_nu/source/projector/boundary/stress are parent-owned",
            "change": "use the template as a construction aid only; never as a local-GR proof",
            "status": "WEAK_PASS_STRONG_FAIL_LOCKED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "update_id": "UP3238_2_next_component_target",
            "target": "Delta_K component birth certificate",
            "formula": "Delta_K=0 or bounded requires live K_hat and K_metric components in 00, 0i, trace, TF, derivative/boundary, units and projector/domain slots",
            "change": "next work should try to fill component certificates before any PPN/local numeric promotion",
            "status": "FEEDS_3239_COMPONENT_WORK",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3238_0_result",
            "decision": "WEAK_SGK_TEMPLATE_EXISTS_STRONG_METRIC_RESPONSE_HELMHOLTZ_ADOPTION_FAILS_CURRENT_CORPUS",
            "because": "the A_nu template genuinely produces the q-current as an Euler equation, but the live MTS Gamma_eff/K_hat symbols are not yet proven to be one Hilbert metric-response object and the Helmholtz test is not evaluable without component birth certificates",
            "claim_status": "NO_LOCAL_GR_NO_NEWTON_NO_PPN_NO_CLOCK_NO_R10_NO_WEP_CLAIM",
            "next_action": "retain q_loc/Delta_K/H_GK as explicit residuals and build Delta_K component birth certificates or arena bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3238_1_next_target",
            "decision": "3239-Y5-R2FR-DeltaK-component-birth-certificate-or-qLoc-arena-bound-under-AX1090",
            "because": "strong SGK adoption now reduces to a finite list of component identities or bounds, especially live K_hat versus K_metric in 00, 0i, trace, tracefree, derivative/boundary, units and projector/domain slots",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "try to source or derive each Delta_K component; if no component source exists, stage the q_loc arena-bound rows without claiming local GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, candidate_rows, metric_rows, helmholtz_rows, qloc_rows, update_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    metric_rows: list[dict[str, object]],
    helmholtz_rows: list[dict[str, object]],
    qloc_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    output_paths = [INPUTS, CANDIDATES, METRIC_RESPONSE, HELMHOLTZ, QLOC_BOUND, UPDATE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    evidence_ready = all("MISSING_SOURCE" not in str(row["evidence_hits"]) and "NO_MATCH" not in str(row["evidence_hits"]) for row in input_rows)
    weak_template_locked = any(row["candidate_id"] == "SGKC3238_0_weak_A_template" and row["pass_status"] == "WEAK_PASS_FORMAL_EULER_HELMHOLTZ" for row in candidate_rows)
    strong_fail_locked = any(row["candidate_id"] == "SGKC3238_1_strong_metric_response" and row["pass_status"] == "FAIL_CURRENT_SOURCE_SET" for row in candidate_rows)
    metric_split = any(row["test_id"] == "MRT3238_3_Ward_reduction" and "Delta_K" in str(row["required_identity"]) for row in metric_rows)
    helmholtz_operator = any(row["helmholtz_id"] == "H3238_0_definition" and "H_GK" in str(row["operator"]) for row in helmholtz_rows)
    qloc_bound = any(row["bound_id"] == "QB3238_0_q_loc_split" and "||q_loc||" in str(row["bound"]) for row in qloc_rows)
    next_target = decision_rows[-1]["decision"].startswith("3239-")
    claim_true_count = 0
    for row_group in [input_rows, candidate_rows, metric_rows, helmholtz_rows, qloc_rows, update_rows, decision_rows]:
        for row in row_group:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(not str(path).lower().startswith(str(FW).lower()) for path in output_paths + [DOC])
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in output_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3238_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3238_01_evidence_hits", "pass": b(evidence_ready), "detail": "no MISSING_SOURCE or NO_MATCH in source register", "generated_utc": now},
        {"check_id": "VAL3238_02_weak_template_locked", "pass": b(weak_template_locked), "detail": "weak A_nu action template recorded as formal pass only", "generated_utc": now},
        {"check_id": "VAL3238_03_strong_fail_locked", "pass": b(strong_fail_locked), "detail": "strong metric-response adoption fails current source set", "generated_utc": now},
        {"check_id": "VAL3238_04_metric_split", "pass": b(metric_split), "detail": "q_loc split through Delta_K written", "generated_utc": now},
        {"check_id": "VAL3238_05_Helmholtz_operator", "pass": b(helmholtz_operator), "detail": "H_GK antisymmetric second-variation operator present", "generated_utc": now},
        {"check_id": "VAL3238_06_q_loc_bound", "pass": b(qloc_bound), "detail": "q_loc residual bound interface present", "generated_utc": now},
        {"check_id": "VAL3238_07_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3238_08_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3238_09_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3238_10_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    metric_rows: list[dict[str, object]],
    helmholtz_rows: list[dict[str, object]],
    qloc_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3238 - SGK Metric-response Helmholtz Gap Or qLoc Bound for Local GR under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, PPN pass, R10 pass, clock pass, WEP pass, source-normalization claim, or public-facing result.

## Result

3238 separates a real construction from a false promotion.

The weak construction is useful:

```text
S_A = int sqrt(-g)[L_K(g,tau,nabla A)
      + A_nu nabla^nu Gamma_eff
      - A_nu J_M^nu
      + L_Gamma] + B_GK,

Khat^{{mu nu}} := partial L_K / partial(nabla_mu A_nu),

delta_A S_A -> -nabla_mu Khat^{{mu nu}} + nabla^nu Gamma_eff - J_M^nu = 0.
```

So the `q`-current can be action-generated in a synthetic/template sense. That is not nothing.

But it is not yet an MTS local-GR derivation, because `A_nu`, `L_K`, `L_Gamma`, `J_M`, `P_loc`, `B_GK`, and the Hilbert stress of the new sector are not parent-owned in the live corpus.

The strong route is:

```text
S_GK = -int sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D) + B_GK,

K_metric^{{mu nu}}[Gamma_eff]
 := 2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_mu_nu,

Delta_K^{{mu nu}}
 := K_hat_live^{{mu nu}} - K_metric^{{mu nu}}[Gamma_eff].
```

Then

```text
q_loc^nu
= P_loc[(nabla^nu Gamma_eff - nabla_mu K_metric^{{mu nu}})
        - nabla_mu Delta_K^{{mu nu}}]
  + projector/domain/boundary terms.
```

If the strong action is real, the first bracket becomes an Euler/Ward/boundary expression. If `Delta_K=0`, Helmholtz symmetry holds, the exterior is source-free/on-shell, and boundary/projector terms vanish, `q_loc=0` is derived rather than imposed.

Current verdict: `WEAK_SGK_TEMPLATE_EXISTS_STRONG_METRIC_RESPONSE_HELMHOLTZ_ADOPTION_FAILS_CURRENT_CORPUS`.

The gain is concrete: the next target is no longer vague `derive S_GK`; it is the finite component problem `Delta_K=0 or bounded`, plus the Helmholtz obstruction `H_GK`.

## SGK Candidate Comparator

{md_table(candidate_rows, ["candidate_id", "candidate", "action", "derivation_test", "pass_status", "adoption_status", "why_not_claim", "valid_for_claim"])}

## Metric-response Test

{md_table(metric_rows, ["test_id", "target", "required_identity", "current_result", "residual_if_fail", "next_evidence_needed", "valid_for_claim"])}

## Helmholtz Operator Test

{md_table(helmholtz_rows, ["helmholtz_id", "target", "operator", "zero_condition", "current_status", "residual_if_fail", "valid_for_claim"])}

## qLoc Bound Interface

{md_table(qloc_rows, ["bound_id", "quantity", "formula", "bound", "required_inputs", "status", "valid_for_claim"])}

## Local-GR Gate Update

{md_table(update_rows, ["update_id", "target", "formula", "change", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_SGK_CANDIDATE_COMPARATOR.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_METRIC_RESPONSE_TEST.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_HELMHOLTZ_OPERATOR_TEST.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_QLOC_BOUND_INTERFACE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_LOCAL_GR_GATE_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3238_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, candidate_rows, metric_rows, helmholtz_rows, qloc_rows, update_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (CANDIDATES, candidate_rows),
        (METRIC_RESPONSE, metric_rows),
        (HELMHOLTZ, helmholtz_rows),
        (QLOC_BOUND, qloc_rows),
        (UPDATE, update_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, candidate_rows, metric_rows, helmholtz_rows, qloc_rows, update_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, candidate_rows, metric_rows, helmholtz_rows, qloc_rows, update_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
