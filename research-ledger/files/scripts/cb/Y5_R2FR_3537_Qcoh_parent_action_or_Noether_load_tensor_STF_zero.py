from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3537-Y5-R2FR-Qcoh-parent-action-or-Noether-load-tensor-STF-zero.md"
CANONICAL_STATUS = OUT / "P8_local_GR_Qcoh_Noether_load_tensor_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3537": {"path": Path(__file__).resolve(), "role": "3537 generator"},
    "doc_3536": {
        "path": ROOT / "3536-Y5-R2FR-chiD-Qcoh-local-zero-positive-Hessian-subproof-or-coefficient-rows.md",
        "role": "3536 chiD/Qcoh handoff",
    },
    "next_3536": {
        "path": OUT / "P8_Y5_R2FR_3536_NEXT_TARGET.csv",
        "role": "3536 selected Qcoh ownership target",
    },
    "qcoh_3536": {
        "path": OUT / "P8_Y5_R2FR_3536_QCOH_SUBPROOF.csv",
        "role": "3536 Qcoh subproof",
    },
    "sigma_3536": {
        "path": OUT / "P8_Y5_R2FR_3536_SIGMA_LOC_CANDIDATE.csv",
        "role": "3536 Sigma_loc candidate",
    },
    "qcoh_contract": {
        "path": OUT / "P8_QCOH_PARENT_ACTION_CONTRACT.csv",
        "role": "Qcoh ownership contract",
    },
    "detq_attempt": {
        "path": OUT / "P8_DETQ_PARENT_THEOREM_ATTEMPT.csv",
        "role": "det(Qcoh) parent theorem attempt",
    },
    "detq_decision": {
        "path": OUT / "P8_DETQ_PARENT_DECISION.csv",
        "role": "det(Qcoh) decision ledger",
    },
    "local_zero_audit": {
        "path": OUT / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv",
        "role": "local zero implication audit",
    },
    "local_zero_counterexamples": {
        "path": OUT / "P8_LOCAL_ZERO_COUNTEREXAMPLE_LEDGER.csv",
        "role": "trace-zero counterexamples",
    },
    "local_zero_requirements": {
        "path": OUT / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
        "role": "extra premise requirements",
    },
    "min_local_gr_blocks": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "minimal local-GR action blocks",
    },
    "mts_symbol_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "MTS symbol to local-GR action map",
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


def ownership_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "QOR3537_0_reject_postprocessor",
            "route": "post-processed smoothing/projector Qcoh",
            "definition": "Qcoh chosen after solving or after picking a domain D",
            "local_zero_result": "not theorem-valid",
            "stress_result": "projector/domain stress unowned",
            "verdict": "REJECT_FOR_DERIVED_LOCAL_GR",
            "valid_for_claim": "False",
        },
        {
            "route_id": "QOR3537_1_independent_action_variable",
            "route": "independent auxiliary/action variable",
            "definition": "S_Q=int sqrt(-g)[1/2 m_STF^2 Q_STF^2 + 1/2 m_D^2 Q_D^2 + constraints tying trace to X/source]",
            "local_zero_result": "Q_STF=Q_D=0 if m^2>0 and no linear source/spurion",
            "stress_result": "constraint multiplier stress must be shown zero or retained",
            "verdict": "VIABLE_BUT_ADDS_PARENT_STRUCTURE",
            "valid_for_claim": "False",
        },
        {
            "route_id": "QOR3537_2_Noether_deformation_tensor",
            "route": "derived Noether/geometric load tensor",
            "definition": "Qcoh_ij := 1/2 L_u h_ij = h_i^mu h_j^nu nabla_(mu u_nu); X=tr Qcoh; Q_STF=Qcoh-(X/3)h",
            "local_zero_result": "if u is the parent-owned stationary observed time/Killing flow and h is Lie-dragged, then Qcoh_ij=0",
            "stress_result": "no independent Q multiplier stress if Qcoh is a derived tensor, but u/h/frame ownership remains required",
            "verdict": "BEST_LOW_ADDITION_ROUTE",
            "valid_for_claim": "False",
        },
    ]


def noether_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "QNZ3537_0_definition",
            "target": "Qcoh as deformation tensor",
            "statement": "Define Qcoh from the observed flow/coframe rather than as a fitted load projector.",
            "mathematical_form": "Q_ij = (1/2) L_u h_ij = h_i^mu h_j^nu nabla_(mu u_nu)",
            "derived_result": "Q_trace is the expansion X and Q_STF is the shear/deformation tensor.",
            "current_status": "NEW_BEST_DEFINITION_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QNZ3537_1_Killing_zero",
            "target": "local compact stationary branch",
            "statement": "If u is aligned with a parent-owned stationary Killing/observed time flow, the symmetric deformation vanishes.",
            "mathematical_form": "L_u h_ij=0 => Q_ij=0 => X=0 and Q_STF=0",
            "derived_result": "This kills trace, STF, and vector/domain deformation components without using a plateau axiom.",
            "current_status": "EXACT_GEOMETRIC_ZERO_IF_FLOW_PREMISE_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QNZ3537_2_no_linear_singlet",
            "target": "operator couplings",
            "statement": "With Qcoh=0 and no local vector/STF spurion, scalar local operators cannot be linear in Q_STF or V_domain.",
            "mathematical_form": "C_i(Q)=c_i tr(Q_STF^2)+c_X X^2+c_V V_iV^i+O(Q^3)",
            "derived_result": "The double-zero condition follows from stationarity plus representation/no-spurion logic.",
            "current_status": "CONDITIONAL_OPERATOR_ZERO",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QNZ3537_3_det_current",
            "target": "det(Qcoh) memory current",
            "statement": "The determinant current becomes safely higher order only for parent-owned coherent/deformation Q, not raw unprojected Q with shear leakage.",
            "mathematical_form": "det(Q)=O(Q^3); d det(Q)|_{Q=0}=0; but det(XI+S)=X^3-(X/2)tr(S^2)+det(S)",
            "derived_result": "If Qcoh_ij=0 by the Killing-flow theorem, det(Qcoh) gives p>=2/p=3 activation without shear leakage.",
            "current_status": "SHAPE_CLOSED_CONDITIONALLY_OWNERSHIP_STILL_OPEN",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "QNZ3537_4_limit",
            "target": "what this does not prove",
            "statement": "Qcoh zero does not by itself prove EH-only/R11 silence, boundary no-flux, or source normalization.",
            "mathematical_form": "Q=0 does not imply c_R11=0, delta_g P_D=0, or Delta_symp=0",
            "derived_result": "The theorem can own the domain deformation part of Sigma_loc, not every local-GR row.",
            "current_status": "SCOPE_GUARD_ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def stress_bianchi_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "QSB3537_0_no_multiplier_advantage",
            "issue": "derived tensor route avoids independent Q constraint multiplier stress",
            "if_route_holds": "Qcoh is a function of u,h,g rather than an independent constrained field",
            "remaining_debt": "metric variation of u/h/frame constraints must still be accounted for",
            "observable_risk": "PPN alpha_i/xi and Bianchi/source conservation",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "QSB3537_1_stationary_not_spherical",
            "issue": "stationarity kills expansion/shear only for the chosen observed flow, not every boundary/projector stress",
            "if_route_holds": "Qcoh deformation components vanish",
            "remaining_debt": "boundary tangential shear, normal flux, and non-Q operators can remain",
            "observable_risk": "alpha3, beta, Gdot, R11",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "QSB3537_2_R11_independence",
            "issue": "R11 operator families independent of Qcoh are not killed by Qcoh=0",
            "if_route_holds": "operators factored by Qcoh/Sigma_Q vanish",
            "remaining_debt": "all other R11 rows need Sigma factorization or numeric bounds",
            "observable_risk": "gamma, beta, R10, clock, source normalization",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "QSB3537_3_domain_flux",
            "issue": "domain flux alpha3 needs trivial representative/no-flux in addition to Qcoh deformation zero",
            "if_route_holds": "no local coherent deformation current",
            "remaining_debt": "P_loc^i_mu F_D^mu=0 must be proved or bounded",
            "observable_risk": "alpha3 <= 4e-20",
            "valid_for_claim": "False",
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "QCF3537_0_flow_ownership",
            "if_zero_proof_fails": "u/h observed flow is not parent-owned or not stationary/Killing locally",
            "required_artifact": "flow deformation residual vector: X, Q_STF, V_domain with units and PPN maps",
            "affected_rows": "R5;R6;R7;R8;R11",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "QCF3537_1_Q_STF_operator",
            "if_zero_proof_fails": "linear or unfactored Q_STF operator exists",
            "required_artifact": "W_QSTF_gamma_beta_xi coefficient products",
            "affected_rows": "R3;R4;R8;R11",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "QCF3537_2_domain_flux",
            "if_zero_proof_fails": "domain representative/trivial-class/no-flux theorem not signed",
            "required_artifact": "W_domain_alpha3 epsilon_domain_flux <= 4e-20 or theorem-zero certificate",
            "affected_rows": "R7;R11",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "QCF3537_3_R11_unfactored",
            "if_zero_proof_fails": "R11 family does not factor through Sigma_Q or Sigma_loc",
            "required_artifact": "complete R11 operator coefficient vector with no MISSING markers",
            "affected_rows": "R2;R3;R4;R9;R10;R11",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3537_0_best_route",
            "decision": "Prefer Qcoh as a derived Noether/geometric deformation tensor over a new independent field.",
            "rationale": "It adds less structure and gives an exact stationarity/Killing zero: Q_ij=1/2 L_u h_ij=0.",
            "effect": "Qcoh can plausibly own the domain deformation part of Sigma_loc if u/h are parent-owned.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3537_1_not_full_local_GR",
            "decision": "Do not use Qcoh zero as an all-purpose local-GR pass.",
            "rationale": "Existing counterexamples show trace/deformation zero does not kill boundary flux, R11 towers, or stress ledgers.",
            "effect": "R11, boundary, alpha3 and source-normalization rows remain live.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3537_2_next",
            "decision": "Attack observed-flow ownership and stationary compact branch next.",
            "rationale": "The Qcoh theorem becomes useful only if MTS owns u, h, tau_obs and the local Killing/stationary branch.",
            "effect": "next target is flow/coframe ownership rather than another abstract Q ledger.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3537_0_Qcoh_route",
            "quantity": "Qcoh_parent_ownership_route",
            "value": "best_route_is_Noether_deformation_tensor",
            "meaning": "Qcoh should be identified with 1/2 L_u h rather than a fitted post-processor if this route is to work",
            "claim_effect": "conditional theorem target, not local-GR evidence yet",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3537_1_STF_zero",
            "quantity": "Q_STF_domain_zero",
            "value": "exact_if_observed_flow_is_parent_owned_stationary_Killing",
            "meaning": "stationary compact local branch gives Q=0, X=0 and Q_STF=0",
            "claim_effect": "does not close R11/boundary/source rows alone",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3537_2_next",
            "quantity": "next_best_target",
            "value": "observed_flow_coframe_stationary_branch_ownership",
            "meaning": "prove or bound u/h/tau_obs ownership and local Killing/no-flux branch",
            "claim_effect": "would make the Qcoh local-zero route parent-owned",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3538-Y5-R2FR-observed-flow-coframe-stationary-branch-ownership-or-PPN-vector-bounds.md",
            "next_script": "scripts/Y5_R2FR_3538_observed_flow_coframe_stationary_branch_ownership_or_PPN_vector_bounds.py",
            "objective": "Prove or bound the premise needed by 3537: u/h/tau_obs are parent-owned observed-flow/coframe variables and compact local branches are stationary enough that L_u h=0 and no domain flux survives.",
            "success_gate": "Either derive the observed-flow Killing/no-flux branch from the parent action, or emit PPN/vector/domain-flux coefficient rows for X, Q_STF, V_domain and alpha3.",
            "why_next": "3537 makes Qcoh zero exact if the observed flow/coframe branch is owned; that is now the live hinge.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3537_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_1_best_route_selected", "passed": bool_text(any(row["route_id"] == "QOR3537_2_Noether_deformation_tensor" and row["verdict"] == "BEST_LOW_ADDITION_ROUTE" for row in routes)), "detail": "Noether/geometric deformation tensor route selected", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_2_Killing_zero_present", "passed": bool_text(any(row["proof_id"] == "QNZ3537_1_Killing_zero" and "Q_ij=0" in row["mathematical_form"] for row in proofs)), "detail": "stationary/Killing zero subproof present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_3_det_current_scope_guard", "passed": bool_text(any(row["proof_id"] == "QNZ3537_3_det_current" for row in proofs) and any(row["proof_id"] == "QNZ3537_4_limit" for row in proofs)), "detail": "det-current route and scope guard both present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_4_stress_bianchi_audit", "passed": bool_text({"QSB3537_0_no_multiplier_advantage", "QSB3537_2_R11_independence", "QSB3537_3_domain_flux"} <= {row["audit_id"] for row in audits}), "detail": "stress/Bianchi/R11/domain-flux caveats covered", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_5_coefficient_fallbacks", "passed": bool_text({"QCF3537_0_flow_ownership", "QCF3537_2_domain_flux", "QCF3537_3_R11_unfactored"} <= {row["coefficient_id"] for row in coefficients}), "detail": "fallback coefficient rows staged", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_6_no_false_claims", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + routes + proofs + audits + coefficients + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3538-Y5-R2FR-observed-flow")), "detail": "3538 observed-flow/coframe target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3537_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3537_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3537_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3537 - Qcoh Parent Action Or Noether Load Tensor STF Zero

## Summary
- **Best route:** identify `Qcoh` as a derived Noether/geometric deformation tensor, not a fitted post-processor.
- **Concrete definition:** `Q_ij = 1/2 L_u h_ij = h_i^mu h_j^nu nabla_(mu u_nu)`.
- **Exact conditional zero:** if the compact local branch has a parent-owned stationary observed flow, then `L_u h=0`, hence `Q_ij=0`, `X=0`, and `Q_STF=0`.
- **Double-zero help:** `det(Qcoh)` then gives a safe p>=2/p=3 activation shape without raw shear leakage.
- **Scope guard:** this does not by itself close R11, boundary flux, source normalization, or full local GR.

## Core Subproof
If `u` is the observed local time flow and `h` is its spatial projector/coframe, define

`Qcoh_ij := 1/2 L_u h_ij`.

On a stationary compact local branch,

`L_u h_ij = 0`,

so

`Qcoh_ij=0`, `X=tr(Qcoh)=0`, and `Q_STF=0`.

That is the cleanest Qcoh route so far: it uses geometry already needed for local GR, rather than inventing a new Q-field first.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Ownership Routes
{markdown_table(routes, ["route_id", "route", "definition", "local_zero_result", "stress_result", "verdict", "valid_for_claim"])}

## Noether Zero Proof
{markdown_table(proofs, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])}

## Stress/Bianchi Audit
{markdown_table(audits, ["audit_id", "issue", "if_route_holds", "remaining_debt", "observable_risk", "valid_for_claim"])}

## Coefficient Fallbacks
{markdown_table(coefficients, ["coefficient_id", "if_zero_proof_fails", "required_artifact", "affected_rows", "valid_for_claim"])}

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
    routes = ownership_route_rows()
    proofs = noether_zero_rows()
    audits = stress_bianchi_rows()
    coefficients = coefficient_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3537_SOURCE_REGISTER.csv",
        "ownership_routes": OUT / "P8_Y5_R2FR_3537_QCOH_OWNERSHIP_ROUTES.csv",
        "noether_zero": OUT / "P8_Y5_R2FR_3537_QCOH_NOETHER_ZERO_PROOF.csv",
        "stress_bianchi": OUT / "P8_Y5_R2FR_3537_STRESS_BIANCHI_AUDIT.csv",
        "coefficient_fallbacks": OUT / "P8_Y5_R2FR_3537_COEFFICIENT_FALLBACKS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3537_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3537_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3537_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3537_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["ownership_routes"], routes, ["route_id", "route", "definition", "local_zero_result", "stress_result", "verdict", "valid_for_claim"])
    write_csv(outputs["noether_zero"], proofs, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])
    write_csv(outputs["stress_bianchi"], audits, ["audit_id", "issue", "if_route_holds", "remaining_debt", "observable_risk", "valid_for_claim"])
    write_csv(outputs["coefficient_fallbacks"], coefficients, ["coefficient_id", "if_zero_proof_fails", "required_artifact", "affected_rows", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, routes, proofs, audits, coefficients, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, routes, proofs, audits, coefficients, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
