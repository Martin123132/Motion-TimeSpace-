from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "local_zero_boundary_R11_silence_audit_written_XD_zero_not_sufficient_boundary_R11_stress_open_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "local_zero_implication_rejected_partial_Qcoh_clause_retained_no_boundary_no_flux_no_R11_silence_no_stress_Bianchi_closure"
NEXT_TARGET = "486-R11-boundary-stress-theorem-or-closure-fill-pack.md"

DOC_PATH = Path("485-boundary-no-flux-and-R11-silence-from-local-zero.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_SOURCE_REGISTER.csv")
IMPLICATION_AUDIT_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv")
COUNTEREXAMPLE_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_COUNTEREXAMPLE_LEDGER.csv")
PREMISE_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv")
RESIDUAL_IMPACT_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_RESIDUAL_IMPACT.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_ROUTE_UPDATE.csv")

LOCAL_ZERO_IDENTITY_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_IDENTITY_SCORECARD.csv")
LOCAL_ZERO_IMPACT_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_RESIDUAL_IMPACT.csv")
LOCAL_GR_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
R11_DECISION_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_ZERO_OR_FILL_DECISION.csv")
ALPHA3_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md",
        "role": "conditional scalar stationary boundary no-flux lemma and alpha3 product fallback",
    },
    {
        "source_file": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "R11/domain source-normalization zero route rejected and fill requirements written",
    },
    {
        "source_file": "481-Qcoh-parent-projector-algebra-or-closure.md",
        "role": "trace projector algebra and Qcoh parent ownership contract",
    },
    {
        "source_file": "482-local-residual-vector-from-domain-source-fill.md",
        "role": "explicit local residual vector and local-GR promotion blockers",
    },
    {
        "source_file": "484-parent-local-zero-action-clause-attempt.md",
        "role": "conditional local-zero clause X=nabla.u and Qcoh=hX/3",
    },
    {
        "source_file": str(LOCAL_ZERO_IDENTITY_PATH),
        "role": "identity scorecard from checkpoint 484",
    },
    {
        "source_file": str(LOCAL_ZERO_IMPACT_PATH),
        "role": "residual impact from checkpoint 484",
    },
    {
        "source_file": str(LOCAL_GR_VECTOR_PATH),
        "role": "local residual vector being audited",
    },
    {
        "source_file": str(R11_DECISION_PATH),
        "role": "R11 zero-or-fill decision rows",
    },
    {
        "source_file": str(ALPHA3_TEMPLATE_PATH),
        "role": "alpha3 numeric/theorem product template",
    },
    {
        "source_file": "scripts/boundary_no_flux_and_R11_silence_from_local_zero.py",
        "role": "this checkpoint generator",
    },
]


IMPLICATION_AUDIT_ROWS = [
    {
        "test_id": "I0_local_zero_input",
        "question": "What does checkpoint 484 actually give?",
        "local_zero_content": "X_D=0 for stationary compact comoving domains, with Qcoh_mu_nu=(1/3)h_mu_nu X",
        "needed_for_local_GR": "all preferred-frame, R11/source-normalization, and projector-stress residuals silent through PPN order",
        "result": "partial_input_only",
        "reason": "X_D=0 is a scalar trace/volume statement, not a full tensor/operator silence theorem",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I1_boundary_volume_flux",
        "question": "Does X_D=0 imply no boundary volume flux?",
        "local_zero_content": "dV_D/dtau=int_D sqrt(h) chi_D X=0 in the stationary comoving branch",
        "needed_for_local_GR": "no net local domain-volume leakage",
        "result": "conditional_yes",
        "reason": "for the stated stationary comoving class this follows from the same volume-conservation identity",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I2_boundary_alpha3_preferred_momentum",
        "question": "Does boundary volume no-flux imply alpha3 preferred-momentum no-flux?",
        "local_zero_content": "scalar volume flux vanishes",
        "needed_for_local_GR": "P_loc^nu_rho n_mu K_boundary^{mu rho}=0 for all local preferred-momentum directions",
        "result": "not_implied",
        "reason": "trace/volume zero does not remove tangential vector, shear, marker, or normal-exchange components of K_boundary",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I3_domain_vector_rows",
        "question": "Does X_D=0 kill alpha1/alpha2/alpha3/xi domain rows?",
        "local_zero_content": "pure coherent-trace domain source vanishes if every domain coupling factors only through X_D",
        "needed_for_local_GR": "domain selector has no vector/preferred-frame/anisotropic stress rows",
        "result": "conditional_not_parent_owned",
        "reason": "the corpus has not proved all domain couplings factor through the scalar X_D with no marker vector",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I4_R11_source_normalization",
        "question": "Does X_D=0 imply EH-only/R11 silence?",
        "local_zero_content": "operators explicitly proportional to X or Qcoh vanish on the local-zero branch",
        "needed_for_local_GR": "all non-EH/source-normalization operators vanish or are bounded in the weak-field source ledger",
        "result": "not_implied",
        "reason": "R11 contains independent operator families and source-normalization coefficients not algebraically forced by X_D=0",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I5_projector_stress_Bianchi",
        "question": "Does X_D=0 close the projector/domain stress and Bianchi ledger?",
        "local_zero_content": "Qcoh vanishes on the conditional local branch",
        "needed_for_local_GR": "delta_g of projector, domain, boundary, and constraint terms is zero/topological or retained consistently",
        "result": "not_implied",
        "reason": "on-shell zero of a constrained field is not automatically zero metric variation or zero multiplier stress",
        "valid_for_claim": "false",
    },
    {
        "test_id": "I6_total_local_GR",
        "question": "Can checkpoint 484 be promoted to derived local GR?",
        "local_zero_content": "one scalar trace-load route is conditionally suppressed",
        "needed_for_local_GR": "Newton source normalization plus PPN silence plus EH/local-Bianchi closure",
        "result": "reject_promotion",
        "reason": "boundary no-flux, R11 silence, and stress/Bianchi closure remain independent active blockers",
        "valid_for_claim": "false",
    },
]


COUNTEREXAMPLE_ROWS = [
    {
        "counterexample_id": "C0_trace_zero_shear_flux",
        "claim_tested": "trace zero implies preferred-momentum flux zero",
        "local_frame_object": "K_ij with K_xy=K_yx=k, all diagonal entries zero",
        "zero_statement": "Tr(K)=0, so the scalar trace load can be zero",
        "surviving_residue": "for boundary normal n_i=x_i, n_i K_ij P_y^j = k",
        "lesson": "a scalar trace/volume zero cannot by itself kill tangential vector/shear preferred-momentum flux",
        "blocks_component": "LRV_BOUNDARY_R7_ALPHA3;LRV_DOMAIN_R7_ALPHA3;LRV_PROJECTOR_STRESS_ACCOUNTING",
    },
    {
        "counterexample_id": "C1_X_zero_R11_operator",
        "claim_tested": "X_D=0 implies R11/EH-only silence",
        "local_frame_object": "non-EH coefficient c_R11 multiplying an operator not proportional to X",
        "zero_statement": "X_D=0 and Qcoh=0",
        "surviving_residue": "c_R11 O_R11 remains unless the parent action sets c_R11=0 or a bound certificate is supplied",
        "lesson": "local-zero only kills X/Q-trace-coupled operators; it does not select the EH operator by itself",
        "blocks_component": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
    },
    {
        "counterexample_id": "C2_on_shell_zero_metric_variation",
        "claim_tested": "Qcoh=0 implies projector/domain stress is zero",
        "local_frame_object": "constraint term Lambda_Q^{ij}(Q_ij-h_ij X/3)",
        "zero_statement": "Q_ij-h_ij X/3=0 on shell",
        "surviving_residue": "delta_g h_ij and delta_g X terms can carry stress unless Lambda_Q or the full stress ledger is controlled",
        "lesson": "field equation zero is not automatically stress-tensor zero",
        "blocks_component": "LRV_PROJECTOR_STRESS_ACCOUNTING",
    },
]


PREMISE_REQUIREMENT_ROWS = [
    {
        "premise_id": "P0_domain_selector",
        "required_extra_premise": "parent action selects compact local comoving domains without a marker vector",
        "why_local_zero_not_enough": "X_D=0 assumes the branch/domain class rather than deriving the selector",
        "sufficient_theorem_form": "delta S/delta chi_D=0 selects scalar stationary local class and FLRW active class with no hand scale",
        "fallback_if_not_derived": "keep domain vector/source rows as closure or numeric coefficients",
        "blocks_components": "LRV_QCOH_DOMAIN_SELECTOR;LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3;LRV_DOMAIN_R8_XI",
    },
    {
        "premise_id": "P1_boundary_scalar_no_flux",
        "required_extra_premise": "boundary action is scalar-only, stationary, marker-free, and Ward-flux closed",
        "why_local_zero_not_enough": "volume no-flux is scalar; alpha3 is a projected momentum flux",
        "sufficient_theorem_form": "S_boundary=sqrt(gamma)F(scalars) implies tau_AB=tau gamma_AB and n_mu P_loc K_boundary^{mu nu}=0",
        "fallback_if_not_derived": "fill W_boundary_alpha3 epsilon_boundary_flux and sibling boundary rows",
        "blocks_components": "LRV_BOUNDARY_R7_ALPHA3",
    },
    {
        "premise_id": "P2_R11_EH_operator",
        "required_extra_premise": "local compact branch reduces to EH-only or every retained R11 coefficient is theorem-zero/bounded",
        "why_local_zero_not_enough": "X_D=0 does not remove operator families independent of X/Qcoh",
        "sufficient_theorem_form": "parent weak-field operator ledger has valid zero rows for vector, source-normalization, and projector-stress families",
        "fallback_if_not_derived": "fill R11 executable vector coefficients with units, normalization, weak-field map, and bounds",
        "blocks_components": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
    },
    {
        "premise_id": "P3_stress_Bianchi",
        "required_extra_premise": "projector/domain/boundary/constraint stress is zero, topological, or explicitly retained with Bianchi conservation",
        "why_local_zero_not_enough": "on-shell X=Qcoh=0 does not prove delta_g of the defining terms is zero",
        "sufficient_theorem_form": "T_extra_mu_nu=0 or nabla_mu(T_EH+T_extra)^{mu nu}=0 with T_extra residual below PPN bounds",
        "fallback_if_not_derived": "write a retained stress residual vector and score it",
        "blocks_components": "LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_TOTAL_ALPHA3_GUARD",
    },
    {
        "premise_id": "P4_no_total_cancellation",
        "required_extra_premise": "each alpha3 channel is zero/bounded individually unless a parent Ward identity enforces exact cancellation",
        "why_local_zero_not_enough": "local-zero can suppress one channel while another channel survives",
        "sufficient_theorem_form": "boundary, domain, R11, and stress channels each carry zero certificates or a parent cancellation identity",
        "fallback_if_not_derived": "do not total-score alpha3; keep channel-by-channel guard active",
        "blocks_components": "LRV_TOTAL_ALPHA3_GUARD",
    },
]


RESIDUAL_IMPACT_ROWS = [
    {
        "component_id": "LRV_QCOH_PARENT_VARIABLE",
        "before_485": "partial_formal_clause",
        "after_485": "partial_formal_clause_retained",
        "reason": "485 does not revoke X=nabla.u or Qcoh=hX/3; it rejects only the over-strong implication to all local-GR silence",
        "claim_effect": "still improved theorem target, not claim-valid",
    },
    {
        "component_id": "LRV_QCOH_PROJECTOR_OWNERSHIP",
        "before_485": "partial_owned_by_scalar_definition",
        "after_485": "partial_owned_but_stress_limited",
        "reason": "trace projector route is clean algebraically, but trace-only definition does not remove metric-variation or boundary leakage",
        "claim_effect": "raw smoothing objection reduced; Bianchi/PPN still blocked",
    },
    {
        "component_id": "LRV_BOUNDARY_R7_ALPHA3",
        "before_485": "failed_for_claim",
        "after_485": "still_failed_for_claim",
        "reason": "X_D=0 gives at most volume no-flux; alpha3 requires projected preferred-momentum no-flux",
        "claim_effect": "blocks alpha3/local-GR until scalar boundary theorem or numeric product exists",
    },
    {
        "component_id": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3;LRV_DOMAIN_R8_XI",
        "before_485": "conditional_zero_if_all_domain_couplings_reduce_to_X",
        "after_485": "conditional_only_not_parent_owned",
        "reason": "trace-domain source can vanish, but vector/anisotropy/marker/stress couplings are not forced to factor through X_D",
        "claim_effect": "domain PPN rows remain open",
    },
    {
        "component_id": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "before_485": "failed_for_claim",
        "after_485": "still_failed_for_claim",
        "reason": "R11/EH-only silence is an operator-selection theorem, not a consequence of scalar expansion zero",
        "claim_effect": "blocks Newton source normalization and local-GR",
    },
    {
        "component_id": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "before_485": "retained_debt",
        "after_485": "retained_debt_sharpened",
        "reason": "on-shell zero does not remove constraint/projector/domain stress under metric variation",
        "claim_effect": "Bianchi and PPN closure still blocked",
    },
    {
        "component_id": "LRV_TOTAL_ALPHA3_GUARD",
        "before_485": "guard_active",
        "after_485": "guard_active_required",
        "reason": "local-zero can suppress one scalar channel only; no channel-cancellation identity exists",
        "claim_effect": "no total alpha3 score allowed",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_local_zero_clause",
        "status": "keep_partial_win",
        "meaning": "X=nabla.u and Qcoh=hX/3 remain useful parent-clause candidates",
        "next_action": "carry the trace-load result forward but do not promote it",
    },
    {
        "decision_id": "D1_implication_to_boundary_no_flux",
        "status": "rejected",
        "meaning": "local volume no-flux does not imply alpha3 preferred-momentum no-flux",
        "next_action": "derive scalar boundary no-flux premise or fill W_boundary_alpha3 epsilon_boundary_flux",
    },
    {
        "decision_id": "D2_implication_to_R11_silence",
        "status": "rejected",
        "meaning": "X_D=0 does not select the EH operator or zero all R11/source-normalization rows",
        "next_action": "derive EH/R11 local operator theorem or fill executable coefficient vector",
    },
    {
        "decision_id": "D3_implication_to_stress_Bianchi",
        "status": "rejected",
        "meaning": "on-shell local-zero does not prove projector/domain/boundary stress is absent",
        "next_action": "write stress theorem or retained-stress closure pack",
    },
    {
        "decision_id": "D4_local_GR_promotion",
        "status": "forbidden",
        "meaning": "no Newton, PPN, alpha3, R11, or local-GR promotion is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "LOCAL_ZERO_TO_LOCAL_GR_SHORTCUT",
        "previous_status": "active_test",
        "new_status": "rejected_as_shortcut",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "QCOH_TRACE_PARENT_CLAUSE",
        "previous_status": "partial_formal_clause",
        "new_status": "retained_partial_clause",
        "accepted_for_claim": "false",
        "next_target": "stress_Bianchi_and_R11 ownership",
    },
    {
        "route_id": "BOUNDARY_R11_STRESS",
        "previous_status": "active_blocker",
        "new_status": "independent_theorem_or_closure_pack_required",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        exists = (ROOT / row["source_file"]).exists()
        rows.append({**row, "exists": str(exists)})
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    identity_rows = read_csv(LOCAL_ZERO_IDENTITY_PATH)
    vector_rows = read_csv(LOCAL_GR_VECTOR_PATH)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    local_zero_rows = [
        row
        for row in identity_rows
        if row.get("identity_id") == "LZ3_local_zero_class"
        and row.get("attempt_result") == "conditional_pass"
    ]
    claim_valid_implications = [
        row for row in IMPLICATION_AUDIT_ROWS if row.get("valid_for_claim") == "true"
    ]
    active_blocker_components = {
        "LRV_BOUNDARY_R7_ALPHA3",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "LRV_PROJECTOR_STRESS_ACCOUNTING",
    }
    vector_component_ids = {row.get("component_id", "") for row in vector_rows}
    blockers_present = active_blocker_components.issubset(vector_component_ids)

    return [
        {
            "rule_id": "V485_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V485_1_local_zero_loaded",
            "rule": "checkpoint 484 conditional local-zero row is loaded",
            "result": "pass" if local_zero_rows else "fail",
            "evidence": f"LZ3_conditional_rows={len(local_zero_rows)}",
            "claim_effect": "confirms input to implication audit",
        },
        {
            "rule_id": "V485_2_blockers_present",
            "rule": "boundary, R11, and stress blockers exist in the local residual vector",
            "result": "pass" if blockers_present else "fail",
            "evidence": ";".join(sorted(active_blocker_components & vector_component_ids)),
            "claim_effect": "audit targets the active local-GR blockers",
        },
        {
            "rule_id": "V485_3_implication_rejected",
            "rule": "local-zero is not treated as sufficient for boundary/R11/stress silence",
            "result": "pass",
            "evidence": "I2_boundary_alpha3_preferred_momentum=not_implied;I4_R11_source_normalization=not_implied;I5_projector_stress_Bianchi=not_implied",
            "claim_effect": "no hidden local-GR promotion",
        },
        {
            "rule_id": "V485_4_no_claim_valid_rows",
            "rule": "no implication row is valid for claim",
            "result": "pass" if not claim_valid_implications else "fail",
            "evidence": f"claim_valid_implication_rows={len(claim_valid_implications)}",
            "claim_effect": "no Newton/PPN/local-GR pass",
        },
        {
            "rule_id": "V485_5_counterexamples_written",
            "rule": "explicit counterexamples show why trace zero does not imply the missing tensor/operator/stress zeros",
            "result": "pass" if len(COUNTEREXAMPLE_ROWS) == 3 else "fail",
            "evidence": f"counterexample_rows={len(COUNTEREXAMPLE_ROWS)}",
            "claim_effect": "shortcut rejected rather than hand-waved",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(timestamp: str, generated_at_utc: str, run_dir: Path, sources: list[dict[str, str]], validations: list[dict[str, str]]) -> str:
    return f"""# 485 - Boundary No-Flux And R11 Silence From Local Zero

Private local-GR/Newton/PPN derivation audit. This is not a public alpha3 pass, R11 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `484` gave the best local route so far:

```text
X = nabla_mu u^mu
Qcoh_mu_nu = (1/3) h_mu_nu X
stationary compact comoving local domains can give X_D=0.
```

This checkpoint asks the dangerous next question:

```text
Does that local-zero clause also force boundary alpha3 no-flux,
R11/source-normalization silence, and projector stress/Bianchi closure?
```

Short answer:

```text
No.

X_D=0 is useful and should be kept.
But it is a scalar trace/volume statement.
It does not by itself kill vector/tensor boundary flux,
independent R11/source-normalization operators,
or metric-variation stress from projectors and constraints.
```

Boxing-score version:

```text
We found a real counterpunch, but it does not win the whole round by itself.
No panic, no promotion, no fake knockout.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_no_flux_and_R11_silence_from_local_zero.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Implication Audit

{markdown_table(IMPLICATION_AUDIT_ROWS)}

The key distinction is:

```text
X_D=0 controls a scalar trace/volume channel.
PPN alpha3 and local-GR silence require vector, tensor, operator, and stress channels to vanish too.
```

## 5. Why The Shortcut Fails

The boundary alpha3 object is not merely the scalar volume flux. It has the schematic form:

```text
Phi_boundary^nu = P_loc^nu_rho n_mu K_boundary^(mu rho).
```

Local-zero can give:

```text
dV_D/dtau = int_D sqrt(h) chi_D X = 0.
```

But `Phi_boundary^nu=0` requires a projected momentum-flux theorem.

The same distinction hits R11:

```text
X_D=0 kills X/Qcoh-trace-coupled operators.
It does not kill operator families whose coefficients are independent of X.
```

And it hits Bianchi/stress:

```text
Qcoh=0 on shell is not the same as delta_g Qcoh=0 or T_extra_mu_nu=0.
```

## 6. Counterexample Ledger

{markdown_table(COUNTEREXAMPLE_ROWS)}

The smallest mathematical counterexample is enough:

```text
K_xy = K_yx = k, all diagonal K_ii = 0.
```

This has zero trace, but a boundary normal in the `x` direction leaves a preferred `y` momentum flux:

```text
n_i K_ij P_y^j = k.
```

So trace-zero or volume-zero cannot be silently upgraded into alpha3 no-flux.

## 7. Extra Premises Required

{markdown_table(PREMISE_REQUIREMENT_ROWS)}

These are the exact extra contracts a future parent action must satisfy.

If those contracts are derived, the local-zero route becomes powerful.

If they are not derived, the honest route is a closure/numeric fill pack for the boundary, R11, and stress rows.

## 8. Residual Impact

{markdown_table(RESIDUAL_IMPACT_ROWS)}

## 9. Validation

{markdown_table(validations)}

## 10. Decision

{markdown_table(DECISION_ROWS)}

## 11. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 12. Claim Ceiling

Allowed:

```text
The local-zero clause is a real partial result:
X=nabla.u and Qcoh=hX/3 give a clean coherent trace-load route.
Stationary compact comoving domains can conditionally set X_D=0.
```

Allowed:

```text
The shortcut X_D=0 => boundary/R11/stress silence has been tested and rejected.
The remaining parent-action contracts are now explicit.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived the Newtonian limit.
MTS passes PPN.
MTS has alpha3=0 or mu_extra=0.
Boundary volume no-flux is the same as preferred-momentum no-flux.
R11/source-normalization silence follows from X_D=0.
On-shell Qcoh=0 proves projector/domain stress is absent.
```

## 13. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | either derive boundary/R11/stress theorem clauses or write closure-fill rows explicitly |
| 2 | alpha3 evaluator refresh | only after theorem-zero certificates or numeric products exist |
| 3 | local PPN residual certificate | only after boundary/R11/stress rows are either derived-zero or bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-boundary-no-flux-and-R11-silence-from-local-zero"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(IMPLICATION_AUDIT_PATH, IMPLICATION_AUDIT_ROWS)
    write_csv(COUNTEREXAMPLE_PATH, COUNTEREXAMPLE_ROWS)
    write_csv(PREMISE_REQUIREMENTS_PATH, PREMISE_REQUIREMENT_ROWS)
    write_csv(RESIDUAL_IMPACT_PATH, RESIDUAL_IMPACT_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    claim_valid_implications = [
        row for row in IMPLICATION_AUDIT_ROWS if row.get("valid_for_claim") == "true"
    ]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "implication_audit": str(ROOT / IMPLICATION_AUDIT_PATH),
        "counterexample_ledger": str(ROOT / COUNTEREXAMPLE_PATH),
        "premise_requirements": str(ROOT / PREMISE_REQUIREMENTS_PATH),
        "residual_impact": str(ROOT / RESIDUAL_IMPACT_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "implication_rows": len(IMPLICATION_AUDIT_ROWS),
        "counterexample_rows": len(COUNTEREXAMPLE_ROWS),
        "premise_requirement_rows": len(PREMISE_REQUIREMENT_ROWS),
        "residual_impact_rows": len(RESIDUAL_IMPACT_ROWS),
        "claim_valid_implication_rows": len(claim_valid_implications),
        "failed_validation_rows": len(failed_validations),
        "local_zero_kept_as_partial_clause": True,
        "local_zero_to_boundary_no_flux_implication": False,
        "local_zero_to_R11_silence_implication": False,
        "local_zero_to_stress_Bianchi_implication": False,
        "boundary_volume_no_flux_conditional": True,
        "boundary_preferred_momentum_no_flux_derived": False,
        "R11_silence_derived": False,
        "stress_Bianchi_closed": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "alpha3_passed": False,
        "mu_extra_zero_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
