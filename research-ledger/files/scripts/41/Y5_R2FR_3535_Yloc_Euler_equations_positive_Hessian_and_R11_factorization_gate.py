from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3535-Y5-R2FR-Yloc-Euler-equations-positive-Hessian-and-R11-factorization-gate.md"
CANONICAL_STATUS = OUT / "P8_local_GR_Yloc_Euler_Hessian_R11_factorization_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3535": {"path": Path(__file__).resolve(), "role": "3535 generator"},
    "doc_3534": {
        "path": ROOT / "3534-Y5-R2FR-MTS-variable-to-local-EH-quotient-map-and-double-zero-origin.md",
        "role": "3534 variable map and double-zero handoff",
    },
    "status_3534": {
        "path": OUT / "P8_local_GR_MTS_variable_quotient_double_zero_status.csv",
        "role": "3534 canonical status",
    },
    "next_3534": {
        "path": OUT / "P8_Y5_R2FR_3534_NEXT_TARGET.csv",
        "role": "3534-selected Yloc Euler target",
    },
    "variable_map_3534": {
        "path": OUT / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv",
        "role": "3534 MTS variable map",
    },
    "double_zero_3534": {
        "path": OUT / "P8_Y5_R2FR_3534_DOUBLE_ZERO_THEOREM_ROUTES.csv",
        "role": "3534 double-zero theorem routes",
    },
    "gates_3534": {
        "path": OUT / "P8_Y5_R2FR_3534_PROMOTION_GATES.csv",
        "role": "3534 promotion gates",
    },
    "action_kernel_3533": {
        "path": OUT / "P8_Y5_R2FR_3533_ACTION_KERNEL.csv",
        "role": "3533 local EH quotient action kernel",
    },
    "double_zero_r11_clause": {
        "path": OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv",
        "role": "local silence multiplet/R11 factorization clause",
    },
    "double_zero_memory": {
        "path": OUT / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "role": "double-zero memory origin attempt",
    },
    "domain_variation": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "domain selector variation chain",
    },
    "domain_clause": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "role": "domain selector parent action clause",
    },
    "qcoh_contract": {
        "path": OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv",
        "role": "Qcoh parent action contract",
    },
    "r11_vector": {
        "path": OUT / "R11_nonEH_operator_vector_executable.csv",
        "role": "R11 executable operator vector, currently mostly unfilled",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bounds",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def euler_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "YET3535_0_parent_kernel",
            "target": "local parent kernel",
            "statement": "Use S_loc=S_EH[g_obs]+S_m[g_obs,psi]+S_Y[Y]+sum_i c_i Sigma_loc O_i[g_obs,psi]+S_D+S_boundary.",
            "mathematical_form": "Sigma_loc=G_AB Y^A Y^B; S_Y=int sqrt(-g)(-1/2 G_AB nabla Y^A nabla Y^B - V(Y))",
            "derivation_result": "This kernel is sufficient to make local extra operators vanish at first variation if the Hessian and boundary gates hold.",
            "current_status": "THEOREM_TARGET_DEFINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "YET3535_1_Y_euler",
            "target": "Y_loc=0 Euler equation",
            "statement": "The Y equation has no local source at Y=0 when all operator couplings factor through Sigma_loc.",
            "mathematical_form": "E_A=-nabla_mu(G_AB nabla^mu Y^B)+M^2_AB Y^B + 2G_ABY^B sum_i c_i O_i + O(Y^2)",
            "derivation_result": "At Y=0, E_A=0 exactly, so the local branch is an on-shell branch, not a plateau axiom.",
            "current_status": "FORMAL_ZERO_DERIVED_IF_FACTORING_ASSUMED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "YET3535_2_positive_hessian",
            "target": "stability/uniqueness",
            "statement": "Y=0 is stable and locally unique if the quadratic operator is positive under compact local boundary conditions.",
            "mathematical_form": "delta^2 S_Y = int sqrt(g)(G_AB nabla eta^A nabla eta^B + M^2_AB eta^A eta^B) >= m_gap^2 ||eta||^2",
            "derivation_result": "Positive Hessian/mass gap would derive the local silence branch and define ell_tr/L_cg from the spectrum.",
            "current_status": "NEEDS_PARENT_POSITIVITY_OR_BOUND",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "YET3535_3_metric_variation",
            "target": "local EH stress silence",
            "statement": "Factored R11/source operators have zero metric stress at Y=0 if Sigma_loc is quadratic and no independent multiplier survives.",
            "mathematical_form": "delta_g(Sigma_loc O_i)=Sigma_loc delta_g O_i + O_i delta_g Sigma_loc; both vanish at Y=0 when delta_g Sigma_loc has no Y-independent term",
            "derivation_result": "R11/source stress is killed at the level of metric variation, not just field value.",
            "current_status": "FORMAL_ZERO_IF_SIGMA_PARENT_OWNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "YET3535_4_aux_chi",
            "target": "scalar selector exception",
            "statement": "The auxiliary chi_D route closes locally only for double-zero activation, not linear activation.",
            "mathematical_form": "delta_chi S_D: lambda_D + 2 chi_D L_mem + chi_D^2 partial_chi L_mem=0; chi_D=0 => lambda_D=0",
            "derivation_result": "Metric stress lambda_D delta_g Sigma_D + chi_D^2 T_mem,D vanishes if Sigma_local=chi_D=0; linear chi_D would leave lambda_D=-L_mem.",
            "current_status": "USEFUL_EXACT_LOCAL_VARIATION",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "YET3535_5_boundary_no_flux",
            "target": "H_tau integrability",
            "statement": "The same positive/no-flux boundary conditions needed for Y=0 also remove extra symplectic curl in H_tau.",
            "mathematical_form": "int_boundary i_tau omega_Y[Y,delta Y]=0 when Y=0, deltaY obeys compact local boundary conditions, and B_Y=O(Sigma_loc)",
            "derivation_result": "R_Htau becomes zero under the same local branch theorem rather than by a separate assumption.",
            "current_status": "CONDITIONAL_NO_FLUX_CERTIFICATE_NEEDED",
            "valid_for_claim": "False",
        },
    ]


def r11_factor_rows() -> list[dict[str, Any]]:
    return [
        {
            "family_id": "R11F3535_0_boundary_topological",
            "operator_family": "boundary_topological_terms",
            "factorization_needed": "topological/exact or Sigma_loc times boundary scalar",
            "zero_condition": "delta_g term exact/topological and no normal momentum flux; otherwise W_boundary products remain",
            "current_status": "NOT_PARENT_SIGNED",
            "fallback_row": "boundary alpha3/beta/Gdot coefficient products",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_1_curvature_squared",
            "operator_family": "R2/fR/Ricci/Weyl squared",
            "factorization_needed": "c_R(Y)=Sigma_loc c_R0 or theorem that coefficient is zero in local quotient",
            "zero_condition": "c_R(0)=partial_A c_R(0)=0 and no independent q-basic tower",
            "current_status": "UNFACTORED_IN_R11_VECTOR",
            "fallback_row": "gamma/beta/xi/alpha(lambda) coefficient map",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_2_scalar_tensor",
            "operator_family": "scalar_tensor_class_metric",
            "factorization_needed": "F_phi(Y)R and scalar source coupling start at Sigma_loc or have positive mass gap with no source linear term",
            "zero_condition": "no Brans-Dicke-like linear scalar source survives compact local branch",
            "current_status": "UNFACTORED_IN_R11_VECTOR",
            "fallback_row": "clock/gamma/beta/Gdot/R10 scalar map",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_3_vector_preferred_frame",
            "operator_family": "vector_preferred_frame",
            "factorization_needed": "local vector is a non-singlet Y^A and cannot appear linearly in a scalar action without a spurion",
            "zero_condition": "SO(3)/stationary compact local symmetry owns no vector spurion; alpha_i products zero",
            "current_status": "CONDITIONAL_REPRESENTATION_ROUTE",
            "fallback_row": "alpha1/alpha2/alpha3/xi domain vector products",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_4_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity",
            "factorization_needed": "torsion/nonmetricity components are Y^A with positive Hessian or are absent from observed connection",
            "zero_condition": "observed Levi-Civita connection of g_obs is the local matter/EM connection",
            "current_status": "UNFACTORED_IN_R11_VECTOR",
            "fallback_row": "WEP/clock/lightcone/spin coefficient map",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_5_bulk_memory_range",
            "operator_family": "bulk_X_force_law; nonlocal_memory_kernel",
            "factorization_needed": "source coupling q_X and memory kernel amplitude factor by Sigma_loc or compact branch support is exact-zero",
            "zero_condition": "no local Yukawa/source charge or nonlocal memory flux remains when Y=0",
            "current_status": "UNFACTORED_IN_R11_VECTOR",
            "fallback_row": "R10 alpha(lambda), Gdot, alpha3 kernel products",
            "valid_for_claim": "False",
        },
        {
            "family_id": "R11F3535_6_source_normalization",
            "operator_family": "source_normalization_operator; projector_domain_stress",
            "factorization_needed": "mu_extra_domain and projector stress are topological/exact or Sigma_loc factored",
            "zero_condition": "Pi_M/Hilbert source charge owns the mass channel and domain projector has no metric stress",
            "current_status": "HIGHEST_PRESSURE_OPEN",
            "fallback_row": "R5/R6/R7/R8/R11 source normalization products",
            "valid_for_claim": "False",
        },
    ]


def proof_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "YEG3535_0_Y_variable_ownership",
            "gate": "Y_loc components must be parent action variables or derived Noether/load tensors.",
            "evidence_needed": "explicit variable list and variation for Gamma/Khat/chi_D/Qcoh/memory/flow/EM hidden sectors",
            "current_result": "not satisfied by current corpus",
            "blocks": "Y=0 theorem promotion",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "YEG3535_1_no_linear_source",
            "gate": "No term J_A[g_obs,psi]Y^A and no linear scalar selector term may appear.",
            "evidence_needed": "symmetry/quotient/no-spurion theorem for every Y component; chi_D squared route for scalar selector",
            "current_result": "partly formal, not parent signed",
            "blocks": "WEP/R10/PPN local silence",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "YEG3535_2_positive_operator",
            "gate": "Quadratic Y operator has positive spectrum on compact local branch.",
            "evidence_needed": "G_AB positive, M^2_AB positive, boundary conditions, no negative/zero modes except gauge quotients",
            "current_result": "missing numeric/theorem spectrum",
            "blocks": "ell_tr/L_cg derivation and Y=0 uniqueness",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "YEG3535_3_universal_R11_factorization",
            "gate": "Every R11/source/EM hidden operator is Sigma_loc factored, topological, or explicitly bounded.",
            "evidence_needed": "complete operator-family row with zero theorem or coefficient; no MISSING markers",
            "current_result": "fails because R11 vector still has MISSING rows",
            "blocks": "local GR/PPN/Maxwell stress promotion",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "YEG3535_4_boundary_reference",
            "gate": "Boundary and reference terms have no Y-linear symplectic flux or mass-channel offset.",
            "evidence_needed": "no-flux boundary conditions and fixed H_ref/source frame",
            "current_result": "not parent signed",
            "blocks": "R_Htau, M_H_ref and Gdot/source denominator",
            "valid_for_claim": "False",
        },
    ]


def verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "VER3535_0_real_progress",
            "question": "Did this derive anything, or just name a gap?",
            "answer": "It derives the formal Euler identity: if all local extra couplings factor through Sigma_loc=G_ABY^AY^B, then Y=0 is an on-shell local branch and metric/source first variations vanish.",
            "meaning": "The local GR route is now a concrete parent-action theorem target, not a vague plateau.",
            "claim_allowed": "False",
        },
        {
            "verdict_id": "VER3535_1_why_not_claim",
            "question": "Why no local GR claim yet?",
            "answer": "The theorem premises are not yet proved for actual MTS variables: variable ownership, positive spectrum, universal factorization and boundary no-flux remain open.",
            "meaning": "Current output strengthens the derivation path but does not finish it.",
            "claim_allowed": "False",
        },
        {
            "verdict_id": "VER3535_2_best_next",
            "question": "Best next target?",
            "answer": "Attack the positive Hessian/source-free Euler operator component-by-component, starting with chi_D/Qcoh because they carry the strongest existing double-zero clues.",
            "meaning": "3536 should try to prove the chi_D-Qcoh local zero theorem or produce coefficient rows.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3535_0_euler_identity",
            "quantity": "Yloc_Euler_double_zero_identity",
            "value": "formally_derived_if_Sigma_factorization_holds",
            "meaning": "Y=0 is an on-shell local branch under the Sigma_loc factorized action",
            "claim_effect": "not claim-valid because premises are unsigned",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3535_1_R11",
            "quantity": "R11_factorization",
            "value": "required_but_not_satisfied_by_current_R11_vector",
            "meaning": "existing R11 rows still contain missing coefficients unless killed by the new theorem",
            "claim_effect": "PPN/R10/local-GR remains blocked",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3535_2_next",
            "quantity": "next_best_target",
            "value": "chiD_Qcoh_local_zero_positive_Hessian_subproof",
            "meaning": "the best concrete proof target is deriving chi_local=0, lambda_local=0 and Qcoh_STF=0 with positive/no-spurion structure",
            "claim_effect": "could close the most MTS-specific part of Y_loc",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3536-Y5-R2FR-chiD-Qcoh-local-zero-positive-Hessian-subproof-or-coefficient-rows.md",
            "next_script": "scripts/Y5_R2FR_3536_chiD_Qcoh_local_zero_positive_Hessian_subproof_or_coefficient_rows.py",
            "objective": "Try to prove the MTS-specific subproof: chi_local=Sigma_local=0, lambda_local=0, and Qcoh_STF/domain load zero on compact local branches, with a positive Hessian/no-linear-spurion argument.",
            "success_gate": "Either chi_D/Qcoh produce a parent-owned Y_loc zero and double-zero operator factor, or all domain/source-normalization/vector/STF channels receive explicit bound-row obligations.",
            "why_next": "3535 gives the general Euler theorem; chi_D and Qcoh are the strongest actual MTS candidates for owning Sigma_loc.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    r11: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3535_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_1_euler_identity_present", "passed": bool_text(any(row["theorem_id"] == "YET3535_1_Y_euler" and "E_A" in row["mathematical_form"] for row in theorem)), "detail": "Y_loc Euler equation identity present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_2_positive_hessian_gate_present", "passed": bool_text(any(row["theorem_id"] == "YET3535_2_positive_hessian" for row in theorem) and any(row["gate_id"] == "YEG3535_2_positive_operator" for row in gates)), "detail": "positive Hessian/spectrum gate present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_3_metric_variation_silence_present", "passed": bool_text(any(row["theorem_id"] == "YET3535_3_metric_variation" for row in theorem)), "detail": "metric stress silence derivation present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_4_r11_families_covered", "passed": bool_text({"R11F3535_1_curvature_squared", "R11F3535_3_vector_preferred_frame", "R11F3535_6_source_normalization"} <= {row["family_id"] for row in r11}), "detail": "curvature, vector/preferred-frame and source-normalization R11 families covered", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_5_no_false_promotion", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + theorem + r11 + gates + status) and all(row["claim_allowed"] == "False" for row in verdicts + next_rows)), "detail": "no local-GR/Newton/PPN/EM claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3536-Y5-R2FR-chiD-Qcoh")), "detail": "3536 chiD/Qcoh subproof target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3535_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3535_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3535_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    r11: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3535 - Yloc Euler Equations, Positive Hessian, And R11 Factorization Gate

## Summary
- **Actual derivation step:** if the parent action factors local extra operators through `Sigma_loc=G_AB Y^A Y^B`, then the `Y_loc=0` Euler equation is satisfied exactly.
- **Why this matters:** local silence becomes an on-shell branch, not a plateau axiom.
- **Metric/source stress:** `delta_g(Sigma_loc O_i)` also vanishes at `Y=0`, provided `Sigma_loc` has no Y-independent metric variation.
- **Still not claimed:** positivity, variable ownership, universal R11/source factorization, and boundary no-flux are not yet parent-signed.
- **Best next target:** prove the MTS-specific `chi_D/Qcoh` local-zero subproof, because those are the strongest candidates for owning `Sigma_loc`.

## Euler Identity
For

`S_loc = S_EH[g_obs] + S_m[g_obs,psi] + S_Y[Y] + sum_i c_i Sigma_loc O_i[g_obs,psi] + S_boundary`

with

`Sigma_loc = G_AB Y^A Y^B`,

the extra-field equation has the schematic form

`E_A = -nabla_mu(G_AB nabla^mu Y^B) + M^2_AB Y^B + 2G_ABY^B sum_i c_i O_i + O(Y^2)`.

Therefore `Y=0` is on shell if the kernel is parent-owned and no unfactored linear source term exists. The hard part is no longer mysterious: prove the premises, or bound the unfactored rows.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Euler Theorem
{markdown_table(theorem, ["theorem_id", "target", "statement", "mathematical_form", "derivation_result", "current_status", "valid_for_claim"])}

## R11 Factorization Audit
{markdown_table(r11, ["family_id", "operator_family", "factorization_needed", "zero_condition", "current_status", "fallback_row", "valid_for_claim"])}

## Proof Gates
{markdown_table(gates, ["gate_id", "gate", "evidence_needed", "current_result", "blocks", "valid_for_claim"])}

## Verdict
{markdown_table(verdicts, ["verdict_id", "question", "answer", "meaning", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    theorem = euler_theorem_rows()
    r11 = r11_factor_rows()
    gates = proof_gate_rows()
    verdicts = verdict_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3535_SOURCE_REGISTER.csv",
        "euler_theorem": OUT / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv",
        "r11_factorization": OUT / "P8_Y5_R2FR_3535_R11_FACTORIZATION_AUDIT.csv",
        "proof_gates": OUT / "P8_Y5_R2FR_3535_PROOF_GATES.csv",
        "verdict": OUT / "P8_Y5_R2FR_3535_VERDICT.csv",
        "status": OUT / "P8_Y5_R2FR_3535_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3535_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3535_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["euler_theorem"], theorem, ["theorem_id", "target", "statement", "mathematical_form", "derivation_result", "current_status", "valid_for_claim"])
    write_csv(outputs["r11_factorization"], r11, ["family_id", "operator_family", "factorization_needed", "zero_condition", "current_status", "fallback_row", "valid_for_claim"])
    write_csv(outputs["proof_gates"], gates, ["gate_id", "gate", "evidence_needed", "current_result", "blocks", "valid_for_claim"])
    write_csv(outputs["verdict"], verdicts, ["verdict_id", "question", "answer", "meaning", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, theorem, r11, gates, verdicts, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, theorem, r11, gates, verdicts, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
