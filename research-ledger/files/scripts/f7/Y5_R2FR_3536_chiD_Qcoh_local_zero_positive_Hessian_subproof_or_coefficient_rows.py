from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3536-Y5-R2FR-chiD-Qcoh-local-zero-positive-Hessian-subproof-or-coefficient-rows.md"
CANONICAL_STATUS = OUT / "P8_local_GR_chiD_Qcoh_local_zero_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3536": {"path": Path(__file__).resolve(), "role": "3536 generator"},
    "doc_3535": {
        "path": ROOT / "3535-Y5-R2FR-Yloc-Euler-equations-positive-Hessian-and-R11-factorization-gate.md",
        "role": "3535 Yloc Euler/Hessian handoff",
    },
    "status_3535": {
        "path": OUT / "P8_local_GR_Yloc_Euler_Hessian_R11_factorization_status.csv",
        "role": "3535 canonical status",
    },
    "next_3535": {
        "path": OUT / "P8_Y5_R2FR_3535_NEXT_TARGET.csv",
        "role": "3535-selected chiD/Qcoh target",
    },
    "euler_3535": {
        "path": OUT / "P8_Y5_R2FR_3535_YLOC_EULER_THEOREM.csv",
        "role": "3535 Yloc Euler theorem",
    },
    "r11_3535": {
        "path": OUT / "P8_Y5_R2FR_3535_R11_FACTORIZATION_AUDIT.csv",
        "role": "3535 R11 factorization audit",
    },
    "map_3534": {
        "path": OUT / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv",
        "role": "3534 variable-to-kernel map",
    },
    "domain_clause": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "role": "chi_D/domain parent action clause",
    },
    "domain_variation": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "chi_D variation chain",
    },
    "qcoh_contract": {
        "path": OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv",
        "role": "Qcoh parent action contract",
    },
    "double_zero_origin": {
        "path": OUT / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "role": "double-zero origin attempt",
    },
    "r11_parent_clause": {
        "path": OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv",
        "role": "Y_loc/Sigma/R11 parent clause",
    },
    "alpha3_gate": {
        "path": OUT / "P8_ALPHA3_THEOREM_ZERO_GATE.csv",
        "role": "alpha3 theorem-zero gate",
    },
    "domain_vector_coefficients": {
        "path": OUT / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
        "role": "domain vector/STF coefficient obligations",
    },
    "r11_vector": {
        "path": OUT / "R11_nonEH_operator_vector_executable.csv",
        "role": "R11 operator vector",
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


def chi_subproof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "CHI3536_0_action",
            "target": "chi_D auxiliary domain selector",
            "statement": "Use the already staged auxiliary selector action with no kinetic chi_D and double-zero memory activation.",
            "mathematical_form": "S_D=int sqrt(-g)[lambda_D(chi_D-Sigma_D)+chi_D^2 L_mem,D]+S_top[P_MTS,D,J_B]",
            "derived_result": "The algebraic selector equations are well-defined before any data fitting.",
            "current_status": "FORMAL_CLAUSE_AVAILABLE_NOT_PARENT_ORIGIN",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CHI3536_1_lambda_variation",
            "target": "chi_local=Sigma_local",
            "statement": "Variation with respect to lambda_D enforces the selector equality.",
            "mathematical_form": "delta_lambda S_D=0 => chi_D-Sigma_D=0",
            "derived_result": "If a parent theorem gives Sigma_local=0, then chi_local=0 follows immediately.",
            "current_status": "EXACT_ALGEBRA_CONDITIONAL_ON_LOCAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CHI3536_2_chi_variation",
            "target": "lambda_local=0",
            "statement": "Double-zero activation removes the hidden multiplier stress.",
            "mathematical_form": "delta_chi S_D=0 => lambda_D+2chi_D L_mem,D+chi_D^2 partial_chi L_mem,D=0",
            "derived_result": "At chi_local=0, lambda_local=0; a linear chi_D L_mem term would fail.",
            "current_status": "EXACT_LOCAL_RESULT_IF_SIGMA_LOCAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CHI3536_3_metric_variation",
            "target": "domain selector stress",
            "statement": "The metric stress of the selector/memory sector vanishes locally when chi_local=lambda_local=0 and P_MTS,D is topological.",
            "mathematical_form": "T_D includes lambda_D delta_g Sigma_D + chi_D^2 T_mem,D + delta_g S_top; all vanish/exact under local-zero/topological premises",
            "derived_result": "No local source-normalization/vector/STF stress from chi_D if C2-C4 premises are parent-owned.",
            "current_status": "CONDITIONAL_STRESS_ZERO",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "CHI3536_4_failure",
            "target": "linear scalar selector rejection",
            "statement": "A scalar selector can appear linearly, so the proof fails unless the scalar is auxiliary and squared or numerically bounded.",
            "mathematical_form": "S_mem~chi_D L_mem gives lambda_local=-L_mem at chi=0",
            "derived_result": "linear chi_D is not admissible for a local-GR branch without coefficient rows.",
            "current_status": "FAILURE_MODE_EXPLICIT",
            "valid_for_claim": "False",
        },
    ]


def qcoh_subproof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "QCH3536_0_decomposition",
            "target": "Qcoh trace/STF split",
            "statement": "Only the trace/source-charge part may survive locally; STF/domain/vector components belong in Y_loc.",
            "mathematical_form": "Qcoh_ij = (1/3)Q_tr h_ij + Q_STF_ij; Y_Q={Q_STF_ij,Q_domain,V_domain^i}",
            "derived_result": "The source trace can feed M_H_ref, while non-GR local hair is isolated in Y_Q.",
            "current_status": "ALGEBRAIC_DECOMPOSITION_NOT_PARENT_OWNERSHIP",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QCH3536_1_representation",
            "target": "no linear Q_STF/vector singlet",
            "statement": "On a compact stationary locally isotropic branch, a scalar action has no linear invariant in vector/STF non-singlets without a spurion.",
            "mathematical_form": "partial_{Q_STF} C_i(0)=0 and partial_{V_i} C_i(0)=0 under SO(3)_loc/no-spurion conditions",
            "derived_result": "Q_STF and vector/domain hair have a natural double-zero route via representation theory.",
            "current_status": "CONDITIONAL_REPRESENTATION_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QCH3536_2_positive_hessian",
            "target": "Q_STF/domain stability",
            "statement": "A positive quadratic parent potential would force the compact local branch to Q_STF=0 and V_domain=0.",
            "mathematical_form": "V_Q=(m_STF^2/2)tr(Q_STF^2)+(m_V^2/2)V_iV^i+(m_D^2/2)Q_domain^2+O(Y^3)",
            "derived_result": "If m_STF^2,m_V^2,m_D^2>0, Qcoh non-GR components vanish and contribute to Sigma_loc as positive norms.",
            "current_status": "POSITIVE_HESSIAN_NOT_SOURCED",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QCH3536_3_determinant_current",
            "target": "double-zero origin from coherent current",
            "statement": "A determinant/current route can make the activation at least quadratic, often cubic, near the coherent-zero branch.",
            "mathematical_form": "J_C~det(Qcoh_domain) or tr(Q_STF^2); J_C(0)=0 and dJ_C(0)=0",
            "derived_result": "This is the best MTS-flavoured origin of the p>=2 requirement, but it needs parent ownership of Qcoh.",
            "current_status": "BEST_CLUE_NOT_PARENT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QCH3536_4_failure",
            "target": "Qcoh post-processor failure",
            "statement": "If Qcoh is only an analytic post-processor or fitted projector, none of the local-zero proof can score.",
            "mathematical_form": "no S_parent[Qcoh] or Noether/load definition => no Euler equation for Q_STF=0",
            "derived_result": "Qcoh must be parent-owned or the route falls back to coefficient products.",
            "current_status": "CURRENT_CORPUS_PARENT_OWNERSHIP_MISSING",
            "valid_for_claim": "False",
        },
    ]


def combined_sigma_rows() -> list[dict[str, Any]]:
    return [
        {
            "sigma_id": "SIG3536_0_candidate",
            "object": "Sigma_loc",
            "definition": "a_chi chi_D^2 + a_STF tr(Q_STF^2) + a_V V_domain_i V_domain^i + a_D Q_domain^2 + a_boundary ||Phi_boundary||^2 + ...",
            "positivity_condition": "all a_i>0 and all components are parent-owned variables/auxiliaries",
            "what_it_would_prove": "C_i(Y)=c_i Sigma_loc gives C_i(0)=0 and dC_i(0)=0 for domain/memory/R11/source operators",
            "current_status": "CONCRETE_CANDIDATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "sigma_id": "SIG3536_1_local_zero",
            "object": "compact local branch",
            "definition": "Sigma_local=0 iff every positive component chi_D,Q_STF,V_domain,Q_domain,... is zero",
            "positivity_condition": "Sigma_loc is a positive norm, not an indefinite cancellation",
            "what_it_would_prove": "local branch silence follows componentwise with no hidden cancellation",
            "current_status": "NEEDS_POSITIVE_HESSIAN_AND_TOPOLOGICAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "sigma_id": "SIG3536_2_branch_selectivity",
            "object": "local versus FLRW/cosmology branch",
            "definition": "Sigma_local=0 on compact stationary domains; Sigma_FLRW may be nonzero through different boundary/topological/source class",
            "positivity_condition": "branch conditions are parent-derived and not arena switches",
            "what_it_would_prove": "local GR silence does not kill cosmology/galaxy activity by fiat",
            "current_status": "OPEN_BRANCH_THEOREM",
            "valid_for_claim": "False",
        },
    ]


def coefficient_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation_id": "CO3536_0_chi_linear",
            "if_proof_fails": "chi_D is not auxiliary/squared or Sigma_local=0 is not parent-derived",
            "required_row": "C_chi_linear or W_chi_source residual with units, source path and PPN/WEP/R10 map",
            "affected_observables": "R1 WEP source; R5/R6/R7/R8 PPN; R10; R11",
            "current_status": "NO_NUMERIC_ROW",
            "valid_for_claim": "False",
        },
        {
            "obligation_id": "CO3536_1_Qcoh_STF",
            "if_proof_fails": "Q_STF/vector/domain components are not killed by parent isotropy/positive Hessian",
            "required_row": "W_QSTF_gamma_beta_xi and W_domain_alpha_i coefficient products",
            "affected_observables": "gamma; beta; alpha1; alpha2; alpha3; xi",
            "current_status": "DOMAIN_VECTOR_COEFFICIENTS_EXIST_BUT_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "obligation_id": "CO3536_2_Qcoh_parent_ownership",
            "if_proof_fails": "Qcoh is not an action variable or derived Noether/load tensor",
            "required_row": "Qcoh closure branch demotion plus source-normalization residual map",
            "affected_observables": "Newton source mass; PPN; R11; source charge",
            "current_status": "PARENT_OWNERSHIP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "obligation_id": "CO3536_3_topological_projector",
            "if_proof_fails": "P_MTS,D is not metric-independent/topological",
            "required_row": "projector_domain_stress coefficient with PPN/R11 map",
            "affected_observables": "alpha1; alpha2; alpha3; xi; R11",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_OWNED",
            "valid_for_claim": "False",
        },
        {
            "obligation_id": "CO3536_4_R11_factorization",
            "if_proof_fails": "not every local operator factors through Sigma_loc",
            "required_row": "complete R11 operator vector with no MISSING markers or theorem-zero certificates",
            "affected_observables": "R2; R3; R4; R7; R8; R9; R10; R11",
            "current_status": "R11_VECTOR_HAS_MISSING_ROWS",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3536_0_partial_subproof",
            "decision": "Accept the chi_D algebraic local-zero chain as exact conditional mathematics.",
            "rationale": "If Sigma_local=0, the double-zero auxiliary action gives chi_local=0, lambda_local=0 and no selector stress.",
            "effect": "chi_D is no longer vague; the missing piece is the parent theorem for Sigma_local=0.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3536_1_Qcoh_route",
            "decision": "Use Qcoh trace/STF decomposition as the strongest MTS route to Sigma_loc.",
            "rationale": "Trace can feed source charge while STF/vector/domain parts are non-GR Y_loc hair with representation/norm-square zeros.",
            "effect": "next work should parent-own Qcoh and its positive Hessian.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3536_2_no_local_GR_promotion",
            "decision": "Do not promote local GR/Newton/PPN.",
            "rationale": "Sigma_local=0, Qcoh parent ownership, topological projector and R11 factorization remain unsigned.",
            "effect": "coefficient obligations remain active.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3536_0_chiD",
            "quantity": "chi_D_local_zero",
            "value": "exact_conditional_if_Sigma_local_zero",
            "meaning": "chi_local=0 and lambda_local=0 follow algebraically from the double-zero auxiliary action if Sigma_local=0",
            "claim_effect": "not claim-valid because Sigma_local=0 is unproved",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3536_1_Qcoh",
            "quantity": "Qcoh_local_zero",
            "value": "representation_positive_Hessian_route_not_parent_owned",
            "meaning": "Q_STF/vector/domain components have a credible no-linear-singlet route but no parent Euler equation yet",
            "claim_effect": "Qcoh cannot yet close PPN/R11 rows",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3536_2_Sigma",
            "quantity": "Sigma_loc",
            "value": "concrete_candidate_not_derived",
            "meaning": "a positive norm-square Sigma candidate is now explicit, but positivity and branch selectivity remain theorem targets",
            "claim_effect": "double-zero not yet usable for claims",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3536_3_next",
            "quantity": "next_best_target",
            "value": "Qcoh_parent_action_or_Noether_load_tensor",
            "meaning": "the shortest path is to make Qcoh a real parent variable/load tensor and derive its STF/domain zero equation",
            "claim_effect": "would turn the best double-zero clue into an owned theorem",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3537-Y5-R2FR-Qcoh-parent-action-or-Noether-load-tensor-STF-zero.md",
            "next_script": "scripts/Y5_R2FR_3537_Qcoh_parent_action_or_Noether_load_tensor_STF_zero.py",
            "objective": "Try to make Qcoh parent-owned as an action variable or derived Noether/load tensor, then derive the local STF/domain zero with a positive Hessian/no-spurion argument.",
            "success_gate": "Either Qcoh owns an Euler/Noether equation forcing Q_STF=0 and domain load zero locally, or Qcoh is demoted to closure with explicit PPN/R11 coefficient rows.",
            "why_next": "3536 closed the chi_D algebra conditionally; Qcoh ownership is now the shortest route to owning Sigma_loc.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    chi_rows: list[dict[str, Any]],
    qcoh_rows: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    obligations: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3536_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_1_chi_exact_chain", "passed": bool_text({"CHI3536_1_lambda_variation", "CHI3536_2_chi_variation", "CHI3536_3_metric_variation"} <= {row["proof_id"] for row in chi_rows}), "detail": "chi_D lambda/chi/metric variation chain present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_2_linear_chi_rejected", "passed": bool_text(any(row["proof_id"] == "CHI3536_4_failure" and "linear" in row["statement"] for row in chi_rows)), "detail": "linear scalar selector failure is explicit", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_3_Qcoh_STF_route", "passed": bool_text({"QCH3536_0_decomposition", "QCH3536_1_representation", "QCH3536_2_positive_hessian"} <= {row["proof_id"] for row in qcoh_rows}), "detail": "Qcoh trace/STF representation/Hessian route present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_4_sigma_candidate", "passed": bool_text(any(row["sigma_id"] == "SIG3536_0_candidate" and "chi_D^2" in row["definition"] and "tr(Q_STF^2)" in row["definition"] for row in sigma_rows)), "detail": "Sigma_loc positive norm-square candidate includes chi_D and Q_STF", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_5_obligations_if_fail", "passed": bool_text({"CO3536_0_chi_linear", "CO3536_1_Qcoh_STF", "CO3536_4_R11_factorization"} <= {row["obligation_id"] for row in obligations}), "detail": "coefficient obligations staged for failed subproof pieces", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_6_no_false_claims", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + chi_rows + qcoh_rows + sigma_rows + obligations + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3537-Y5-R2FR-Qcoh")), "detail": "3537 Qcoh ownership target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3536_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3536_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3536_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    chi_rows: list[dict[str, Any]],
    qcoh_rows: list[dict[str, Any]],
    sigma_rows: list[dict[str, Any]],
    obligations: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3536 - chiD/Qcoh Local-Zero Positive-Hessian Subproof Or Coefficient Rows

## Summary
- **chi_D result:** the auxiliary double-zero selector algebra closes exactly if `Sigma_local=0`: `chi_local=0`, `lambda_local=0`, and selector/memory stress vanishes under topological projector premises.
- **Qcoh result:** trace/STF decomposition gives a credible MTS route: trace can be source charge, while STF/vector/domain parts become positive-norm `Y_loc` hair.
- **Sigma candidate:** `Sigma_loc = a_chi chi_D^2 + a_STF tr(Q_STF^2) + a_V V_domain^2 + ...`.
- **Hard blocker:** the corpus still does not parent-own `Qcoh` or prove `Sigma_local=0`, positive Hessian, branch selectivity, topological projector, and R11 factorization.
- **No promotion:** local GR/Newton/PPN remains unclaimed; coefficient obligations are explicit if the Qcoh/chi route fails.

## chi_D Exact Conditional Chain
`delta_lambda S_D=0 => chi_D=Sigma_D`

`delta_chi S_D=0 => lambda_D + 2 chi_D L_mem,D + chi_D^2 partial_chi L_mem,D = 0`

So if the parent theory proves `Sigma_local=0`, then `chi_local=0` and `lambda_local=0`. This is real algebraic progress: the remaining fight is proving `Sigma_local=0`, not guessing a plateau.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## chiD Subproof
{markdown_table(chi_rows, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])}

## Qcoh Subproof
{markdown_table(qcoh_rows, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])}

## Sigma Candidate
{markdown_table(sigma_rows, ["sigma_id", "object", "definition", "positivity_condition", "what_it_would_prove", "current_status", "valid_for_claim"])}

## Coefficient Obligations
{markdown_table(obligations, ["obligation_id", "if_proof_fails", "required_row", "affected_observables", "current_status", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

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
    chi_rows = chi_subproof_rows()
    qcoh_rows = qcoh_subproof_rows()
    sigma_rows = combined_sigma_rows()
    obligations = coefficient_obligation_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3536_SOURCE_REGISTER.csv",
        "chi_subproof": OUT / "P8_Y5_R2FR_3536_CHID_SUBPROOF.csv",
        "qcoh_subproof": OUT / "P8_Y5_R2FR_3536_QCOH_SUBPROOF.csv",
        "sigma_candidate": OUT / "P8_Y5_R2FR_3536_SIGMA_LOC_CANDIDATE.csv",
        "coefficient_obligations": OUT / "P8_Y5_R2FR_3536_COEFFICIENT_OBLIGATIONS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3536_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3536_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3536_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3536_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["chi_subproof"], chi_rows, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])
    write_csv(outputs["qcoh_subproof"], qcoh_rows, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])
    write_csv(outputs["sigma_candidate"], sigma_rows, ["sigma_id", "object", "definition", "positivity_condition", "what_it_would_prove", "current_status", "valid_for_claim"])
    write_csv(outputs["coefficient_obligations"], obligations, ["obligation_id", "if_proof_fails", "required_row", "affected_observables", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, chi_rows, qcoh_rows, sigma_rows, obligations, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, chi_rows, qcoh_rows, sigma_rows, obligations, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
