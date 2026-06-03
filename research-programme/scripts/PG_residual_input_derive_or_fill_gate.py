from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "PG-residual-input-derive-or-fill-gate"
CHECKPOINT_DOC = "461-PG-residual-input-derive-or-fill-gate.md"
STATUS = "PG_residual_input_derive_or_fill_gate_written_all_9_rows_retained_unfilled_no_derived_zero_or_numeric_claim_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "PG_residual_input_gate_only_all_rows_no_claim_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "462-charge-current-equality-direct-derivation-attempt.md"
GATE_PATH = Path("source-intake/mts_residuals/P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv")
STATUS_PATH = Path("source-intake/mts_residuals/P8_PG_residual_input_STATUS.csv")


GATE_COLUMNS = [
    "component_id",
    "symbol",
    "active_pg_rows",
    "dominant_stack_rungs",
    "derive_route",
    "derive_attempt_result",
    "fill_route",
    "current_decision",
    "valid_for_Newton_claim",
    "valid_for_local_GR_claim",
    "evidence_now",
    "evidence_required",
    "next_action",
]

STATUS_COLUMNS = [
    "model_id",
    "branch_id",
    "component_id",
    "symbol",
    "derivation_status",
    "numeric_input_status",
    "valid_for_claim",
    "claim_ceiling",
    "source_gate_doc",
    "notes",
]

PRIORITY_COLUMNS = [
    "rank",
    "target_component",
    "why_priority",
    "proof_or_fill_strategy",
    "next_checkpoint",
]


SOURCE_DOCS = [
    {
        "path": "459-PG-calibration-residual-mapper.md",
        "role": "PG residual mapper and fillable input template origin",
    },
    {
        "path": "460-source-normalized-Newton-branch-theorem-stack.md",
        "role": "SN0-SN11 Newton theorem stack and PG residual bindings",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_calibration_residual_INPUT_TEMPLATE.csv",
        "role": "nine canonical PG residual input rows",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "machine-readable SN0-SN11 theorem stack",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv",
        "role": "PG0-PG10 residual activation map",
    },
    {
        "path": "runs/20260602-193000-source-normalized-Newton-branch-theorem-stack/status.json",
        "role": "status proving 12 stack rungs and 11 PG bindings",
    },
    {
        "path": "runs/20260602-191500-PG-calibration-residual-mapper/results/PG_residual_input_template.csv",
        "role": "run artifact for fillable PG residual rows",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "same-frame weak-field source/Phi gate",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 operator coefficient vector contract",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "second-order beta/gamma source stability attempt",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole blockers",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux closure attempt",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal Geff/kappa attempt",
    },
    {
        "path": "453-global-coupling-superselection-parent-action-contract.md",
        "role": "global coupling superselection route",
    },
    {
        "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Pi_M flux closure route",
    },
    {
        "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge route",
    },
]


GATE_ROWS = [
    {
        "component_id": "P8_Geff_time_drift",
        "symbol": "dln_Geff_dt",
        "active_pg_rows": "PG7;PG8",
        "dominant_stack_rungs": "SN5;SN7;SN10",
        "derive_route": "global-coupling superselection: one parent constant kappa_0 with no local scalar/domain/range/source running",
        "derive_attempt_result": "not_derived_currently; 452/453 are contracts/attempts, not theorem-zero",
        "fill_route": "numeric local Gdot residual or derived-zero source; target lock currently 9.6e-15 yr^-1 in template",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "conditional constant-coupling language only",
        "evidence_required": "parent superselection proof partial_t,r,A,lambda,frame G_eff=0 or numeric dln_Geff_dt row",
        "next_action": "do not absorb G_eff drift into GM; derive superselection or fill local Gdot residual",
    },
    {
        "component_id": "P8_Meff_conservation",
        "symbol": "dln_Meff_dt",
        "active_pg_rows": "PG1;PG4;PG8",
        "dominant_stack_rungs": "SN3;SN4;SN8;SN10",
        "derive_route": "Ward/topological Pi_M flux closure: d(Pi_M J_H)=0 with Pi_M commuting with exterior/source variation",
        "derive_attempt_result": "not_derived_currently; flux closure is a target, not an established parent identity",
        "fill_route": "mass drift residual after separating G_eff drift",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "451/455 expose closure conditions but do not close them",
        "evidence_required": "closed calibrated Pi_M flux proof or numeric dln_Meff_dt residual",
        "next_action": "derive charge-current equality and Pi_M flux closure before Newton pass",
    },
    {
        "component_id": "P8_species_source_charge",
        "symbol": "eta_source_AB",
        "active_pg_rows": "PG5;PG7;PG8",
        "dominant_stack_rungs": "SN0;SN3;SN7;SN9;SN10",
        "derive_route": "selector-blind source action: no species/material marker in active gravitational source, not just direct matter coframe identity",
        "derive_attempt_result": "not_derived_currently; direct WEP/identity-coframe is not the full source-normalization proof",
        "fill_route": "eta_source_AB residual or species derivative of ln(mu_obs)",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "source-side universality remains distinct from direct geometry WEP",
        "evidence_required": "no-species/source-charge theorem or eta_source_AB residual below source lock",
        "next_action": "keep direct WEP and source-charge rows separate",
    },
    {
        "component_id": "P8_range_dependence",
        "symbol": "alpha(lambda)",
        "active_pg_rows": "PG3;PG5;PG6;PG7;PG8",
        "dominant_stack_rungs": "SN1;SN5;SN6;SN7;SN9;SN10",
        "derive_route": "no finite-range source hair: no massive/scalar/boundary/range operator couples to measured source strength",
        "derive_attempt_result": "not_derived_currently; symbolic R10 language is not an executable alpha(lambda) curve",
        "fill_route": "curve file with lambda, alpha_predicted, alpha_bound, source assumptions",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "no MTS alpha(lambda) prediction curve loaded",
        "evidence_required": "derived no-range theorem or executable alpha(lambda) residual curve",
        "next_action": "do not treat finite-range silence as Newton; fill R10 curve if no theorem-zero exists",
    },
    {
        "component_id": "P8_radial_source_hair",
        "symbol": "partial_r_ln_mu_obs",
        "active_pg_rows": "PG4;PG5;PG6;PG8",
        "dominant_stack_rungs": "SN4;SN6;SN8;SN9;SN10",
        "derive_route": "Gauss/no-hair exterior: partial_r M_eff=0 and no radial mu_extra/G_eff profile outside compact support",
        "derive_attempt_result": "not_derived_currently; Gauss surface equality is open",
        "fill_route": "radial profile or dimensionless envelope relative to measured GM",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "no radial profile or theorem-zero source loaded",
        "evidence_required": "no-radial-hair theorem or partial_r_ln_mu_obs profile",
        "next_action": "derive Gauss equality or fill radial-hair residual",
    },
    {
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "symbol": "mu_extra_boundary_bulk_domain",
        "active_pg_rows": "PG1;PG3;PG4;PG6",
        "dominant_stack_rungs": "SN3;SN4;SN6;SN8;SN10",
        "derive_route": "Ward/no-hair/topological zero: boundary, bulk, domain, projector, memory, and connection channels have no unowned monopole",
        "derive_attempt_result": "not_derived_currently; this is the central measured-GM obstruction",
        "fill_route": "mu_extra/(G_eff M_eff) or explicit exchange coefficient map to R3/R4/R7/R8/R9/R11 locks",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "channels are visible but not zeroed",
        "evidence_required": "mu_extra=0 theorem or coefficient residual map; alpha3/Gdot locks included",
        "next_action": "attempt direct mu_extra zero theorem only after charge-current ownership is clarified",
    },
    {
        "component_id": "P8_frame_calibration_split",
        "symbol": "delta_frame_source",
        "active_pg_rows": "PG0;PG2;PG5;PG8",
        "dominant_stack_rungs": "SN0;SN2;SN5;SN9;SN10",
        "derive_route": "one observed coframe for source variation and matter readout",
        "derive_attempt_result": "partial_conditional_only; identity-frame assumptions exist but source variation is not parent-derived",
        "fill_route": "frame/source calibration residual below WEP, clock, and operator locks",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "same-frame route is written conditionally in 424/460",
        "evidence_required": "parent frame theorem or numeric/derived frame split residual",
        "next_action": "keep frame proof attached to source variation, not only matter geodesics",
    },
    {
        "component_id": "P8_nonlinear_beta_source_residue",
        "symbol": "delta_beta_source",
        "active_pg_rows": "PG9",
        "dominant_stack_rungs": "SN11",
        "derive_route": "second-order weak-field calculation after measured-GM normalization is fixed",
        "derive_attempt_result": "not_derived_currently; first-order Poisson cannot clear beta/gamma",
        "fill_route": "beta-source residual or second-order theorem-zero proof",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "not_required_for_first_order_only_but_blocks_GR_promotion",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "440 is an attempt, not a pass",
        "evidence_required": "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
        "next_action": "run second-order PPN source stability only after first-order source rows are owned",
    },
    {
        "component_id": "R11_EH_operator_ledger",
        "symbol": "c_nonEH_operator_vector",
        "active_pg_rows": "PG0;PG1;PG3;PG6;PG7;PG9",
        "dominant_stack_rungs": "SN1;SN5;SN11",
        "derive_route": "EH-only exterior parent theorem or full non-EH coefficient vector with every local residual scored",
        "derive_attempt_result": "not_derived_currently; R11 vector is still symbolic/unfilled",
        "fill_route": "R11 coefficient-vector file with normalization and mappings to gamma, beta, preferred-frame, xi, and fifth-force rows",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "evidence_now": "438 exposes operator-vector contract but no executable coefficient vector",
        "evidence_required": "EH-only theorem-zero or complete c_nonEH_operator_vector input file",
        "next_action": "derive EH-only exterior or make R11 vector executable",
    },
]


STATUS_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "PG_residual_input_gate",
        "component_id": row["component_id"],
        "symbol": row["symbol"],
        "derivation_status": "retained_unfilled",
        "numeric_input_status": "not_loaded",
        "valid_for_claim": "false",
        "claim_ceiling": CLAIM_CEILING,
        "source_gate_doc": CHECKPOINT_DOC,
        "notes": row["current_decision"],
    }
    for row in GATE_ROWS
]


PRIORITY_ROWS = [
    {
        "rank": "1",
        "target_component": "P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra",
        "why_priority": "charge-current equality decides whether the Hamiltonian charge can become measured source mass",
        "proof_or_fill_strategy": "attempt B_xi/G_eff = M_eff[Pi_M J_H] directly; if it fails, fill dln_Meff_dt and mu_extra rows",
        "next_checkpoint": "462-charge-current-equality-direct-derivation-attempt.md",
    },
    {
        "rank": "2",
        "target_component": "R11_EH_operator_ledger",
        "why_priority": "operator purity controls Poisson coefficient and PPN stability",
        "proof_or_fill_strategy": "derive EH-only exterior or produce executable c_nonEH_operator_vector",
        "next_checkpoint": "463-EH-only-or-R11-executable-vector-gate.md",
    },
    {
        "rank": "3",
        "target_component": "P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence",
        "why_priority": "constant GM is legal only if derivative/source/range hair is absent or scored",
        "proof_or_fill_strategy": "derive superselection/no-source/no-range identities or fill residual curves",
        "next_checkpoint": "464-constant-GM-derivative-hair-fill-gate.md",
    },
    {
        "rank": "4",
        "target_component": "P8_nonlinear_beta_source_residue",
        "why_priority": "local GR requires beta/gamma stability after measured-GM normalization",
        "proof_or_fill_strategy": "second-order weak-field source/operator calculation",
        "next_checkpoint": "465-second-order-PPN-source-stability-gate.md",
    },
]


def utc_now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def read_csv_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": item["path"],
            "exists": str(exists(item["path"])),
            "role": item["role"],
        }
        for item in SOURCE_DOCS
    ]


def gate_results(source_paths_missing: int, template_rows: int, stack_rows: int) -> list[dict[str, Any]]:
    derived_zero_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "derived_zero")
    numeric_filled_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "numeric_filled")
    retained_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "retained_unfilled_no_claim")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
        },
        {
            "gate": "template_rows_loaded",
            "status": "pass" if template_rows == 9 else "fail",
            "evidence": f"{template_rows} PG residual input template rows",
        },
        {
            "gate": "Newton_stack_loaded",
            "status": "pass" if stack_rows == 12 else "fail",
            "evidence": f"{stack_rows} SN stack rows",
        },
        {
            "gate": "all_input_components_decided",
            "status": "pass" if len(GATE_ROWS) == 9 else "fail",
            "evidence": f"{len(GATE_ROWS)} derive/fill decisions written",
        },
        {
            "gate": "derived_zero_rows",
            "status": "fail",
            "evidence": f"{derived_zero_rows} rows derived zero in current evidence",
        },
        {
            "gate": "numeric_filled_rows",
            "status": "fail",
            "evidence": f"{numeric_filled_rows} numeric residual rows loaded",
        },
        {
            "gate": "retained_no_claim_rows",
            "status": "pass" if retained_rows == 9 else "fail",
            "evidence": f"{retained_rows} rows retained as explicit no-claim blockers",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "no PG residual input row has theorem-zero or valid numeric fill evidence",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "delta_beta_source and R11 operator vector remain retained/unfilled",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def theorem_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "PG residual input gate written",
            "status": "pass",
            "evidence": "nine PG residual rows given derive/fill decisions",
        },
        {
            "claim": "any residual row derived zero",
            "status": "fail",
            "evidence": "none derived from current parent stack",
        },
        {
            "claim": "any residual row numerically filled",
            "status": "fail",
            "evidence": "no numeric residuals or alpha(lambda)/R11 vector loaded",
        },
        {
            "claim": "first-order Newton branch promotable",
            "status": "fail",
            "evidence": "SN0-SN10 still lack row certificates",
        },
        {
            "claim": "local GR branch promotable",
            "status": "fail",
            "evidence": "SN11 and R11 operator vector still unfilled",
        },
    ]


def render_doc(timestamp: str, run_dir: Path, source_paths_missing: int, template_rows: int, stack_rows: int) -> str:
    source_rows = source_register()
    gates = gate_results(source_paths_missing, template_rows, stack_rows)
    theorem_status = theorem_status_rows()

    return f"""# 461 - PG Residual Input Derive-Or-Fill Gate

Private residual-input checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 460 made the source-normalized Newton branch finite: SN0-SN10 for first-order Newton and SN11 for local-GR/PPN promotion. This checkpoint attacks the nine fillable PG residual input rows directly.

For each row, the allowed outcomes are:

```text
derived_zero,
numeric_filled / curve_filled / vector_filled,
or retained_unfilled_no_claim.
```

No row is allowed to pass by rhetoric, analogy, or calibration absorption.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PG_residual_input_derive_or_fill_gate.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Derive/fill CSV | `{GATE_PATH}` |
| Status CSV | `{STATUS_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["source_file", "exists", "role"])}

## 4. Derive-Or-Fill Decisions

The derive/fill decision table has been written to `{GATE_PATH}`.

{md_table(GATE_ROWS, GATE_COLUMNS)}

## 5. Machine Status Rows

The no-claim status table has been written to `{STATUS_PATH}`.

{md_table(STATUS_ROWS, STATUS_COLUMNS)}

## 6. Priority Queue

{md_table(PRIORITY_ROWS, PRIORITY_COLUMNS)}

## 7. Main Technical Read

The clean result is brutal but useful: none of the nine PG residual input rows are presently derived-zero, and none are numerically filled. The best partial row is `P8_frame_calibration_split`, because the same-frame route exists conditionally, but it still does not prove source variation in the parent action. Every other row remains a hard blocker.

The central first-order Newton obstruction is still:

```text
B_xi/G_eff = M_eff[Pi_M J_H]
mu_obs = G_eff M_eff + mu_extra
mu_extra = 0
d ln mu_obs = 0 in time, radius, species, range, frame, and domain
```

If this cannot be derived, it has to become actual residual data: drift, source charge, radial hair, fifth-force curve, `mu_extra/(GM)`, frame split, beta source residue, or R11 coefficient vector.

## 8. Gate Results

{md_table(gates, ["gate", "status", "evidence"])}

## 9. Theorem Status

{md_table(theorem_status, ["claim", "status", "evidence"])}

## 10. Decision

This checkpoint turns the PG residual inputs from placeholders into a no-escape gate. Current corpus status: all nine rows are retained, unfilled, and invalid for claim. That means no measured-GM derivation, no Newton promotion, and no local-GR promotion yet.

The project is still moving in the right direction: the failure is now exact and executable. The next serious derivation target is the rank-one obstruction, charge-current equality:

```text
B_xi/G_eff = M_eff[Pi_M J_H]
```

If that identity lands, several rows become attackable at once. If it fails, we stop pretending and fill the `dln_Meff_dt` and `mu_extra_boundary_bulk_domain` residual channels.

Practical read: this is not grim; it is disciplined. The boxing scorecard says we are not knocked out, but we are not allowed to claim the round until the source mass is owned. The next punch is not another broad audit. It is the direct charge-current derivation attempt.

## 11. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 462-charge-current-equality-direct-derivation-attempt.md | rank-one first-order Newton blocker; decides whether Hamiltonian charge can become measured source mass |
| 2 | 463-EH-only-or-R11-executable-vector-gate.md | operator row controls Poisson coefficient and local-GR promotion |
| 3 | 464-constant-GM-derivative-hair-fill-gate.md | derivative/source/range rows decide whether constant GM absorption is legal |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    template_path = ROOT / "source-intake/mts_residuals/P8_PG_calibration_residual_INPUT_TEMPLATE.csv"
    stack_path = ROOT / "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv"
    template_rows = read_csv_count(template_path)
    stack_rows = read_csv_count(stack_path)

    source_paths_missing = sum(1 for item in SOURCE_DOCS if not exists(item["path"]))
    missing_sources = [item["path"] for item in SOURCE_DOCS if not exists(item["path"])]

    write_csv(ROOT / GATE_PATH, GATE_ROWS, GATE_COLUMNS)
    write_csv(ROOT / STATUS_PATH, STATUS_ROWS, STATUS_COLUMNS)
    write_csv(results_dir / "PG_residual_input_derive_or_fill_gate.csv", GATE_ROWS, GATE_COLUMNS)
    write_csv(results_dir / "PG_residual_input_status.csv", STATUS_ROWS, STATUS_COLUMNS)
    write_csv(results_dir / "PG_residual_priority_queue.csv", PRIORITY_ROWS, PRIORITY_COLUMNS)

    doc_text = render_doc(timestamp, run_dir, source_paths_missing, template_rows, stack_rows)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    retained_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "retained_unfilled_no_claim")
    derived_zero_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "derived_zero")
    numeric_filled_rows = sum(1 for row in GATE_ROWS if row["current_decision"] == "numeric_filled")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": source_paths_missing,
        "missing_sources": missing_sources,
        "template_rows": template_rows,
        "Newton_stack_rows": stack_rows,
        "derive_fill_rows": len(GATE_ROWS),
        "status_rows": len(STATUS_ROWS),
        "retained_unfilled_rows": retained_rows,
        "derived_zero_rows": derived_zero_rows,
        "numeric_filled_rows": numeric_filled_rows,
        "all_rows_decided": len(GATE_ROWS) == 9,
        "all_current_claim_flags_blocked": True,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=utc_now_tag())
    args = parser.parse_args()
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
