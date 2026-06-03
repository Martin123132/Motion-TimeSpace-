from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-only-or-R11-executable-vector-gate"
CHECKPOINT_DOC = "463-EH-only-or-R11-executable-vector-gate.md"
STATUS = "EH_only_or_R11_executable_vector_gate_written_EH_only_failed_R11_vector_template_only_Delta_nonEH_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "EH_or_R11_vector_gate_only_no_EH_R11_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "464-R11-executable-vector-minimum-fill-skeleton.md"
GATE_PATH = Path("source-intake/mts_residuals/R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv")
VECTOR_STATUS_PATH = Path("source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv")
FILL_QUEUE_PATH = Path("source-intake/mts_residuals/R11_OPERATOR_VECTOR_FILL_QUEUE.csv")


GATE_COLUMNS = [
    "gate_id",
    "branch",
    "required_evidence",
    "current_evidence",
    "decision",
    "claim_credit",
    "residual_if_failed",
    "next_action",
]

VECTOR_COLUMNS = [
    "operator_family",
    "affected_rows",
    "required_real_input",
    "current_artifact",
    "current_status",
    "valid_for_claim",
    "why_it_blocks",
    "minimum_next_fill",
]

FILL_QUEUE_COLUMNS = [
    "rank",
    "operator_family",
    "priority_reason",
    "must_supply",
    "downstream_rows",
    "next_checkpoint_or_artifact",
]


SOURCE_DOCS = [
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "canonical R11 EH-only-or-vector contract",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only parent-premise ladder P0-P9",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "P3/P6 sector-reduction attempt and retained sector matrix",
    },
    {
        "path": "442-P6-second-order-operator-restriction-or-R11-demotion.md",
        "role": "higher-curvature/nonlocal P6 demotion into R11 rows",
    },
    {
        "path": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "role": "torsion/nonmetricity P4 demotion into R11 rows",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "retained EH-operator and source-normalization local-bound plan",
    },
    {
        "path": "462-charge-current-equality-direct-derivation-attempt.md",
        "role": "Delta_nonEH charge-current obstruction feeding this gate",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "canonical R11 vector template; currently placeholder only",
    },
    {
        "path": "source-intake/mts_residuals/R11_P6_metric_operator_rows_TEMPLATE.csv",
        "role": "P6 higher-curvature/nonlocal metric operator template",
    },
    {
        "path": "source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv",
        "role": "P4 torsion/nonmetricity connection template",
    },
    {
        "path": "source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "role": "Delta_nonEH residual decomposition row",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/status.json",
        "role": "status proving actual_R11_vector_supplied=false and EH_only_theorem_zero_derived=false",
    },
    {
        "path": "runs/20260602-131500-EH-only-exterior-parent-premise-ladder/status.json",
        "role": "EH-only ladder status",
    },
    {
        "path": "runs/20260602-140000-P6-second-order-operator-restriction-or-R11-demotion/status.json",
        "role": "P6 demotion status",
    },
    {
        "path": "runs/20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row/status.json",
        "role": "P4 connection demotion status",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "EH_only_success_branch",
        "statement": "If P1-P8 of the EH-only ladder are parent-derived and P9 is solved to PPN order, Delta_nonEH is theorem-zero.",
        "math_form": "E_ext^{mu nu}=aG^{mu nu}+bg^{mu nu}; c_nonEH_operator_vector=0",
        "current_status": "not_satisfied",
    },
    {
        "part": "R11_executable_vector_branch",
        "statement": "If EH-only is not derived, every retained non-EH operator family must provide coefficient, units, normalization, weak-field map, affected rows, and valid source paths before it can be scored.",
        "math_form": "E_ext^{mu nu}=aG^{mu nu}+bg^{mu nu}+sum_i c_i H_i^{mu nu}",
        "current_status": "template_only_not_executable",
    },
    {
        "part": "current_decision",
        "statement": "The current corpus has neither an EH-only theorem-zero certificate nor a real R11 vector, so Delta_nonEH remains retained.",
        "math_form": "Delta_nonEH = sum_i c_i Q_i^nonEH / G_eff retained",
        "current_status": "no_EH_or_R11_pass",
    },
]


GATE_ROWS = [
    {
        "gate_id": "EHV0_source_paths",
        "branch": "both",
        "required_evidence": "all cited EH/R11 source paths exist",
        "current_evidence": "source register loaded by this run",
        "decision": "pass",
        "claim_credit": "audit_only",
        "residual_if_failed": "audit_invalid",
        "next_action": "continue",
    },
    {
        "gate_id": "EHV1_EH_only_ladder_closed",
        "branch": "EH_only",
        "required_evidence": "P1-P8 parent-derived: observed frame, full Ward/Euler ownership, no extra fields, Levi-Civita, local 4D metric-only, second order, harmless boundary, constant source normalization",
        "current_evidence": "439 reports central rungs closure/conditional/open; 440/442/443 demote P3/P6/P4",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "c_nonEH_operator_vector;Delta_nonEH",
        "next_action": "do not claim EH-only; use R11 branch unless future parent theorem closes rungs",
    },
    {
        "gate_id": "EHV2_Lovelock_assumptions_earned",
        "branch": "EH_only",
        "required_evidence": "local 4D diffeo metric-only second-order exterior is derived, not assumed",
        "current_evidence": "P6 second-order restriction not derived; higher-curvature/nonlocal operators demoted",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "R2_fR_scalar_mode;Ricci_Weyl_squared;nonlocal_memory_kernel",
        "next_action": "either derive P6 parent restriction or fill P6 R11 rows",
    },
    {
        "gate_id": "EHV3_connection_compatibility_earned",
        "branch": "EH_only",
        "required_evidence": "parent action has only Levi-Civita connection or connection variation kills torsion/nonmetricity/hypermomentum",
        "current_evidence": "P4 connection theorem not parent-derived; P4 R11 template written",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "torsion_nonmetricity;R0/R1/R2/R11 connection residues",
        "next_action": "derive no-independent-connection theorem or fill P4 connection rows",
    },
    {
        "gate_id": "EHV4_R11_template_present",
        "branch": "R11_vector",
        "required_evidence": "canonical vector schema exists",
        "current_evidence": "R11_nonEH_operator_vector_TEMPLATE.csv exists and has retained family rows",
        "decision": "pass",
        "claim_credit": "scaffold_only",
        "residual_if_failed": "cannot_score_R11",
        "next_action": "replace placeholders with real vector rows",
    },
    {
        "gate_id": "EHV5_R11_actual_vector_supplied",
        "branch": "R11_vector",
        "required_evidence": "branch vector has no fill_ placeholders, real coefficient values/units/maps/source paths, and valid_for_claim=true only after validation",
        "current_evidence": "438 status actual_R11_vector_supplied=false; template rows valid_for_claim=false",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "c_nonEH_operator_vector retained",
        "next_action": "write minimum executable vector skeleton and fill highest-priority rows",
    },
    {
        "gate_id": "EHV6_R10_links_for_range_operators",
        "branch": "R11_vector",
        "required_evidence": "finite-range-inducing families reference a valid alpha(lambda) curve or theorem-zero proof",
        "current_evidence": "R2/fR, scalar, bulk-X, nonlocal, and source-normalization rows are template-only",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "alpha(lambda);R10_fifth_force",
        "next_action": "tie R11 scalar/bulk/nonlocal rows to R10 curves or no-range theorem",
    },
    {
        "gate_id": "EHV7_charge_current_delta_nonEH_zero",
        "branch": "both",
        "required_evidence": "Delta_nonEH=0 by EH-only theorem or executable R11 vector scoring below locks",
        "current_evidence": "462 constructs Delta_nonEH but no zero certificate exists",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "Delta_nonEH blocks charge-current equality and Poisson coefficient",
        "next_action": "keep charge-current equality conditional",
    },
    {
        "gate_id": "EHV8_local_GR_or_Newton_promotion",
        "branch": "both",
        "required_evidence": "EH/R11 gate plus source-normalized Newton stack and PPN source stability all pass",
        "current_evidence": "R11 failed; source-normalization rows unfilled; SN11 open",
        "decision": "fail",
        "claim_credit": "none",
        "residual_if_failed": "no Newton or local-GR promotion",
        "next_action": "continue residual/vector work",
    },
]


VECTOR_ROWS = [
    {
        "operator_family": "boundary_topological_terms",
        "affected_rows": "R3;R4;R7;R8;R11",
        "required_real_input": "boundary/topological coefficient or theorem-zero boundary no-hair source",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "boundary hair can shift gamma, beta, alpha3, xi, and source mass",
        "minimum_next_fill": "declare c_boundary/c_GB, units, boundary no-hair proof or residual map",
    },
    {
        "operator_family": "R2_fR_scalar_mode",
        "affected_rows": "R3;R4;R10;R11",
        "required_real_input": "c_R2/c_fR, scalar mass/coupling, gamma/beta and alpha(lambda) map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;R11_P6_metric_operator_rows_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "higher-curvature scalar modes change PPN and finite-range force rows",
        "minimum_next_fill": "derive zero/infinite-mass/no-coupling or supply coefficient plus R10 curve",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "affected_rows": "R3;R8;R11",
        "required_real_input": "c_Ricci/c_Weyl with slip/location/wave-sector weak-field map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;R11_P6_metric_operator_rows_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "quadratic tensor terms can alter gamma, xi, and wave/local operator behaviour",
        "minimum_next_fill": "derive topological combination/zero coefficients or map residuals",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "affected_rows": "R2;R3;R4;R9;R10;R11",
        "required_real_input": "F(phi,C), scalar/class local solution, source coupling, clock/PPN/Gdot/range map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "scalar/class metric terms can fake same-frame while changing clocks, source strength, PPN, and range",
        "minimum_next_fill": "derive scalar/class silence or supply coefficient/residual map",
    },
    {
        "operator_family": "vector_preferred_frame",
        "affected_rows": "R5;R6;R7;R8;R11",
        "required_real_input": "vector/domain coefficient with alpha1/alpha2/alpha3/xi map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "covariant vector/domain structures can still create preferred-frame/location effects",
        "minimum_next_fill": "derive absent/gauge/aligned vector or fill preferred-frame coefficients",
    },
    {
        "operator_family": "torsion_nonmetricity",
        "affected_rows": "R0;R1;R2;R11",
        "required_real_input": "connection coefficients or no-independent-connection theorem",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;R11_P4_connection_rows_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "connection residues affect WEP, clocks, spin, light cones, and source charge",
        "minimum_next_fill": "derive Levi-Civita parent branch or fill P4 connection rows",
    },
    {
        "operator_family": "bulk_X_force_law",
        "affected_rows": "R1;R3;R4;R10;R11",
        "required_real_input": "bulk/load mass, source charge, alpha_X(lambda_X), PPN/source map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "bulk/load sectors can create finite-range and source-normalization residuals",
        "minimum_next_fill": "derive positive source-free no-hair or fill alpha_X curve/vector rows",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "affected_rows": "R7;R9;R10;R11",
        "required_real_input": "kernel norm/form, compact-local silence proof or alpha3/Gdot/fifth-force map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;R11_P6_metric_operator_rows_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "cosmological memory success cannot be imported as local kernel silence",
        "minimum_next_fill": "derive compact-local kernel silence or fill kernel residual map",
    },
    {
        "operator_family": "source_normalization_operator",
        "affected_rows": "R1;R4;R9;R10;R11",
        "required_real_input": "mu_extra, G_eff/M_eff derivative and range/source maps",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv",
        "current_status": "template_only_retained_core_blocker",
        "valid_for_claim": "false",
        "why_it_blocks": "measured GM can carry source/range/time/boundary corrections even if metric operator is EH-like",
        "minimum_next_fill": "derive constant measured GM or fill P8 source-normalization residuals",
    },
    {
        "operator_family": "projector_domain_stress",
        "affected_rows": "R5;R6;R7;R8;R11",
        "required_real_input": "projector/domain stress coefficient and preferred-frame/location map",
        "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "current_status": "template_only",
        "valid_for_claim": "false",
        "why_it_blocks": "readout/projector/domain variation can backreact into local operator rows",
        "minimum_next_fill": "derive topological/metric-independent projector or fill stress vector",
    },
]


FILL_QUEUE_ROWS = [
    {
        "rank": "1",
        "operator_family": "source_normalization_operator",
        "priority_reason": "largest Newton blocker and already tied to P8 residual inputs",
        "must_supply": "mu_extra/(GM), dln_Geff_dt, dln_Meff_dt, eta_source_AB, alpha(lambda), or theorem-zero source",
        "downstream_rows": "R1;R4;R9;R10;R11;SN7;SN10",
        "next_checkpoint_or_artifact": "464-R11-executable-vector-minimum-fill-skeleton.md",
    },
    {
        "rank": "2",
        "operator_family": "R2_fR_scalar_mode",
        "priority_reason": "P6 failure couples directly to gamma, beta, and fifth-force rows",
        "must_supply": "c_R2/c_fR, scalar mass/coupling, weak-field gamma/beta map, R10 curve if finite range",
        "downstream_rows": "R3;R4;R10;R11;SN1;SN5",
        "next_checkpoint_or_artifact": "R11_P6_metric_operator_rows executable fill",
    },
    {
        "rank": "3",
        "operator_family": "torsion_nonmetricity",
        "priority_reason": "P4 connection compatibility is a crisp theorem-or-vector subproblem",
        "must_supply": "no-independent-connection theorem or torsion/nonmetricity coefficients and WEP/clock/light maps",
        "downstream_rows": "R0;R1;R2;R11;SN0;SN1",
        "next_checkpoint_or_artifact": "R11_P4_connection_rows executable fill",
    },
    {
        "rank": "4",
        "operator_family": "boundary_topological_terms",
        "priority_reason": "boundary hair affects charge-current equality, mu_extra, alpha3, and Gauss mass",
        "must_supply": "class/topological boundary no-hair proof or boundary coefficient map",
        "downstream_rows": "R3;R4;R7;R8;R11;Delta_symp;Delta_extra",
        "next_checkpoint_or_artifact": "boundary no-hair coefficient map",
    },
    {
        "rank": "5",
        "operator_family": "vector_preferred_frame;projector_domain_stress",
        "priority_reason": "preferred-frame/location rows are severe and can survive covariant language",
        "must_supply": "alpha1/alpha2/alpha3/xi maps or theorem-zero alignment/gauge proof",
        "downstream_rows": "R5;R6;R7;R8;R11",
        "next_checkpoint_or_artifact": "preferred-frame vector/domain coefficient map",
    },
]


STATUS_ROWS = [
    {
        "claim": "EH-only theorem-zero branch",
        "status": "fail",
        "evidence": "P3/P4/P6/P8 and PPN completion remain open or demoted",
        "claim_credit": "none",
    },
    {
        "claim": "R11 executable vector supplied",
        "status": "fail",
        "evidence": "canonical template exists but all rows are placeholders/valid_for_claim=false",
        "claim_credit": "none",
    },
    {
        "claim": "Delta_nonEH zeroed",
        "status": "fail",
        "evidence": "neither EH-only theorem nor executable vector certificate exists",
        "claim_credit": "none",
    },
    {
        "claim": "R11 gate architecture",
        "status": "pass",
        "evidence": "EH-only branch, vector branch, and fill queue written",
        "claim_credit": "architecture_only",
    },
    {
        "claim": "Newton/local-GR promotion",
        "status": "fail",
        "evidence": "R11, source-normalization, and SN11 remain retained",
        "claim_credit": "none",
    },
]


def utc_now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


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


def gate_results(source_paths_missing: int, template_rows: int, gate_rows: int, vector_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
        },
        {
            "gate": "R11_template_loaded",
            "status": "pass" if template_rows == 10 else "fail",
            "evidence": f"{template_rows} canonical retained operator template rows",
        },
        {
            "gate": "EH_or_R11_gate_rows_written",
            "status": "pass" if gate_rows == 9 else "fail",
            "evidence": f"{gate_rows} branch decision gates",
        },
        {
            "gate": "operator_family_status_rows_written",
            "status": "pass" if vector_rows == 10 else "fail",
            "evidence": f"{vector_rows} retained non-EH family rows",
        },
        {
            "gate": "EH_only_theorem_zero_derived",
            "status": "fail",
            "evidence": "P3/P4/P6/P8/SN11 remain open or demoted",
        },
        {
            "gate": "actual_R11_vector_supplied",
            "status": "fail",
            "evidence": "template-only rows with fill placeholders and valid_for_claim=false",
        },
        {
            "gate": "Delta_nonEH_zeroed",
            "status": "fail",
            "evidence": "neither branch clears c_nonEH_operator_vector",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "R11 and P8 source-normalization rows remain retained",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "EH/R11 gate only; PPN/source stability not solved",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(timestamp: str, run_dir: Path, source_paths_missing: int, template_rows: int, gate_rows: int, vector_rows: int) -> str:
    source_rows = source_register()
    gates = gate_results(source_paths_missing, template_rows, gate_rows, vector_rows)

    return f"""# 463 - EH-Only or R11 Executable Vector Gate

Private EH/R11 operator checkpoint. This is not a public Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 462 isolated `Delta_nonEH` as the operator obstruction inside the charge-current equality:

```text
Delta_nonEH = sum_i c_i Q_i^nonEH / G_eff
```

This checkpoint asks the exact fork:

```text
Can MTS currently prove EH-only locally?

If not, does it currently provide an executable R11 coefficient vector?
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/EH_only_or_R11_executable_vector_gate.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| EH/R11 gate CSV | `{GATE_PATH}` |
| Vector status CSV | `{VECTOR_STATUS_PATH}` |
| Fill queue CSV | `{FILL_QUEUE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["source_file", "exists", "role"])}

## 4. Theorem Statement

{md_table(THEOREM_STATEMENT, ["part", "statement", "math_form", "current_status"])}

## 5. EH-Only or R11 Gate

The branch gate has been written to `{GATE_PATH}`.

{md_table(GATE_ROWS, GATE_COLUMNS)}

## 6. Operator Family Vector Status

The operator-family status table has been written to `{VECTOR_STATUS_PATH}`.

{md_table(VECTOR_ROWS, VECTOR_COLUMNS)}

## 7. Minimum Fill Queue

The fill queue has been written to `{FILL_QUEUE_PATH}`.

{md_table(FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)}

## 8. Machine Status

{md_table(STATUS_ROWS, ["claim", "status", "evidence", "claim_credit"])}

## 9. Technical Decision

The answer to the fork is:

```text
EH-only?        no current parent theorem.
R11 executable? no current real vector.
```

So the legal operator result remains:

```text
E_ext^{{mu nu}} = a G^{{mu nu}} + b g^{{mu nu}} + sum_i c_i H_i^{{mu nu}}
```

with the `c_i` still symbolic. That means `Delta_nonEH` stays active in the charge-current equality and in the Poisson coefficient.

## 10. Why This Is Still Progress

This is not just another no. It is now a fork with a work order:

```text
either close P3/P4/P6/P8/SN11 as a parent theorem,
or fill ten non-EH operator-family rows with real coefficients and weak-field maps.
```

The R11 vector is where a retained modified-gravity branch becomes testable instead of vague.

## 11. Gate Results

{md_table(gates, ["gate", "status", "evidence"])}

## 12. Decision

`Delta_nonEH` is not zeroed. EH-only local GR is not derived, and the current R11 vector is template-only. No Newton, PPN, or local-GR promotion is allowed from this branch.

Practical read: this is the referee saying, "choose your gloves." Either MTS proves the extra sectors leave the ring, or they fight as explicit R11 coefficient rows. The next move is to build the minimum executable R11 vector skeleton so the retained branch can eventually be scored instead of just named.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 464-R11-executable-vector-minimum-fill-skeleton.md | convert the template-only R11 vector into a branch-specific executable skeleton with placeholders separated from real no-claim rows |
| 2 | 465-constant-GM-derivative-hair-fill-gate.md | source-normalization is the highest-priority R11 family for Newton |
| 3 | 466-P6-P4-theorem-zero-retry-or-demotion.md | if trying EH-only again, attack P6 and P4 with parent-action theorem attempts |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    template_path = ROOT / "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv"
    template_rows = read_csv_count(template_path)
    source_paths_missing = sum(1 for item in SOURCE_DOCS if not exists(item["path"]))
    missing_sources = [item["path"] for item in SOURCE_DOCS if not exists(item["path"])]

    write_csv(ROOT / GATE_PATH, GATE_ROWS, GATE_COLUMNS)
    write_csv(ROOT / VECTOR_STATUS_PATH, VECTOR_ROWS, VECTOR_COLUMNS)
    write_csv(ROOT / FILL_QUEUE_PATH, FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)
    write_csv(results_dir / "EH_only_or_R11_gate.csv", GATE_ROWS, GATE_COLUMNS)
    write_csv(results_dir / "R11_executable_vector_status.csv", VECTOR_ROWS, VECTOR_COLUMNS)
    write_csv(results_dir / "R11_operator_vector_fill_queue.csv", FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)
    write_csv(results_dir / "theorem_status.csv", STATUS_ROWS, ["claim", "status", "evidence", "claim_credit"])

    gate_rows = read_csv_count(ROOT / GATE_PATH)
    vector_rows = read_csv_count(ROOT / VECTOR_STATUS_PATH)
    fill_queue_rows = read_csv_count(ROOT / FILL_QUEUE_PATH)

    doc_text = render_doc(timestamp, run_dir, source_paths_missing, template_rows, gate_rows, vector_rows)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": source_paths_missing,
        "missing_sources": missing_sources,
        "template_rows": template_rows,
        "gate_rows": gate_rows,
        "vector_status_rows": vector_rows,
        "fill_queue_rows": fill_queue_rows,
        "EH_only_theorem_zero_derived": False,
        "actual_R11_vector_supplied": False,
        "Delta_nonEH_zeroed": False,
        "R11_promoted": False,
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
