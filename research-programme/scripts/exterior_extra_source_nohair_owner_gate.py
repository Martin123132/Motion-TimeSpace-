from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "exterior-extra-source-nohair-owner-gate"
CHECKPOINT_DOC = "435-exterior-extra-source-nohair-owner-gate.md"
STATUS = "exterior_extra_source_nohair_owner_gate_written_all_Rextra_channels_routed_no_parent_zero_no_local_GR_pass"
CLAIM_CEILING = "exterior_extra_source_nohair_owner_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "436-auxiliary-projector-local-Euler-equation-ledger.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger exposing X/projector/boundary/domain channels",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "legal fates for Ward-force channels and retained PPN residual map",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "conditional boundary no-angular kill switch and radial hair warning",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap no-hair and source-normalized force-law contract",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain flux no-hair numeric contract",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson bridge and extra potential/source requirements",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "retained EH/source-normalization local-bound plan",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "source_residual and mu_extra decomposition under Ward/Bianchi ownership",
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C0-C7 zero-route ranking",
    },
    {
        "path": "434-measured-GM-mu-extra-zero-route.md",
        "role": "measured-GM and mu_extra zero contract",
    },
    {
        "path": "runs/20260602-003500-class-only-boundary-action-noangular-theorem/results/gate_results.csv",
        "role": "boundary no-angular gate results",
    },
    {
        "path": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/bulk_X_operator_routes.csv",
        "role": "bulk-X no-hair and force-law route matrix",
    },
    {
        "path": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "bulk-X force-law quantities needed to score R10",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/EH_operator_retained_ledger.csv",
        "role": "retained non-EH operator family ledger",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/source_normalization_channel_plan.csv",
        "role": "source-normalization local-bound channel plan",
    },
    {
        "path": "runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_decomposition.csv",
        "role": "machine-readable mu_extra channels from checkpoint 434",
    },
]


EXTERIOR_SOURCE_OWNER_GATE = [
    {
        "gate_id": "E0_ordinary_mass_monopole",
        "source_channel": "ordinary Pi_M mass flux",
        "allowed_zero_or_safe_form": "closed calibrated monopole M_eff with dM_eff/dr=0",
        "owner_condition": "Pi_M flux closure plus absolute calibration",
        "current_status": "conditional_not_parent_owned",
        "legal_fate": "safe_only_if_parent_fixed_else_retained_source_normalization",
        "rows": "R4;R9;R10",
    },
    {
        "gate_id": "E1_boundary_shear_vector",
        "source_channel": "boundary trace-free, vector, and angular hair",
        "allowed_zero_or_safe_form": "class-only boundary action with no angular/vector arguments",
        "owner_condition": "delta S_boundary/delta B_TF = delta S_boundary/delta B_0i = 0",
        "current_status": "conditional_from_379_not_parent_derived",
        "legal_fate": "retained_boundary_coefficients",
        "rows": "R3;R4;R7;R8;R9",
    },
    {
        "gate_id": "E2_boundary_radial_monopole",
        "source_channel": "boundary radial trace/monopole shift",
        "allowed_zero_or_safe_form": "constant universal calibration only",
        "owner_condition": "no radial/time/source/species dependence and Ward-owned flux",
        "current_status": "not_derived",
        "legal_fate": "retained_unless_constant_universal",
        "rows": "R4;R9;R10",
    },
    {
        "gate_id": "E3_bulk_X",
        "source_channel": "bulk X scalar/vector/memory load field",
        "allowed_zero_or_safe_form": "positive source-free massive exterior no-hair or scored Yukawa law",
        "owner_condition": "(-Delta+m_X^2)X=0 with m_X^2>0 and no exterior source, or alpha_X(lambda_X) supplied",
        "current_status": "symbolic_deferred",
        "legal_fate": "theorem_zero_if_mass_gap_else_R10_curve_required",
        "rows": "R3;R4;R9;R10",
    },
    {
        "gate_id": "E4_projector_domain",
        "source_channel": "projector/domain preferred-frame or preferred-location source",
        "allowed_zero_or_safe_form": "covariant topological/constraint-owned projector and dynamical domain selector",
        "owner_condition": "no fixed external projector, no metric-dependent dropped stress, no L_cg gradient force",
        "current_status": "conditional_open",
        "legal_fate": "retained_vector_shear_coefficients",
        "rows": "R5;R6;R7;R8;R11",
    },
    {
        "gate_id": "E5_auxiliary_offshell",
        "source_channel": "auxiliary/projector/domain Euler equation not on shell",
        "allowed_zero_or_safe_form": "all local auxiliary Euler equations solved in ordinary exterior",
        "owner_condition": "E_A=0 for each auxiliary with no residual stress or force",
        "current_status": "best_theorem_route_open",
        "legal_fate": "derive_C1_or_retain_exchange_force",
        "rows": "R7;R9;R10;R11",
    },
    {
        "gate_id": "E6_nonEH_operator",
        "source_channel": "non-EH operator potential or divergence",
        "allowed_zero_or_safe_form": "EH-only exterior, pure topological boundary, or coefficient vector scored",
        "owner_condition": "non-EH coefficient vector c_nonEH=0 theorem or executable retained ledger",
        "current_status": "retained_symbolic",
        "legal_fate": "R11_coefficient_vector_required",
        "rows": "R3;R4;R8;R10;R11",
    },
    {
        "gate_id": "E7_species_time_range",
        "source_channel": "species, time, or finite-range dependence of measured source",
        "allowed_zero_or_safe_form": "partial_A mu_obs = partial_t mu_obs = partial_lambda mu_obs = 0",
        "owner_condition": "universal matter/source coupling, stationary source, no finite-range tail",
        "current_status": "not_parent_derived",
        "legal_fate": "R1_R9_R10_retained_until_derived_or_scored",
        "rows": "R1;R9;R10",
    },
]


NOHAIR_OWNER_CONDITIONS = [
    {
        "condition_id": "N0_valid_parent_variation",
        "must_show": "every projector, boundary, domain, auxiliary, and bulk variable is varied or proven readout-only",
        "if_solved": "dropped-stress fake GR routes are blocked",
        "current_status": "structural_Ward_ledger_written_not_zero",
    },
    {
        "condition_id": "N1_closed_mass_monopole",
        "must_show": "Pi_M J is closed in compact exterior and absolutely calibrated",
        "if_solved": "ordinary radial mass hair is removed",
        "current_status": "conditional_flux_theorem_calibration_open",
    },
    {
        "condition_id": "N2_boundary_class_only",
        "must_show": "S_boundary depends only on scalar/topological class and fixed universal monopole",
        "if_solved": "angular/vector boundary sources vanish; radial/time hair still needs N1/N6",
        "current_status": "conditional_noangular_not_parent_derived",
    },
    {
        "condition_id": "N3_bulk_mass_gap",
        "must_show": "bulk X has positive source-free exterior operator with regular decaying data",
        "if_solved": "bulk X exterior source is zero or exponentially screened",
        "current_status": "conditional_identity_alpha_curve_missing",
    },
    {
        "condition_id": "N4_projector_domain_covariance",
        "must_show": "P_D and domain data are covariant/dynamical/topological with no local vector/shear force",
        "if_solved": "preferred-frame and preferred-location source channels are controlled",
        "current_status": "conditional_open",
    },
    {
        "condition_id": "N5_EH_operator_selection",
        "must_show": "local exterior operator is EH plus Lambda or non-EH coefficients are supplied",
        "if_solved": "R11 becomes theorem-zero or executable",
        "current_status": "retained_symbolic",
    },
    {
        "condition_id": "N6_universal_source_stationarity",
        "must_show": "mu_obs has no species, clock, time, range, or source-environment dependence",
        "if_solved": "R1/R9/R10 source-normalization channels can seek zero",
        "current_status": "not_derived",
    },
]


OWNER_FATE_MATRIX = [
    {
        "fate": "theorem_zero",
        "required_evidence": "parent equation plus boundary/regularity conditions prove source channel vanishes",
        "runner_handling": "row may be marked theorem_zero only for that specific channel",
        "claim_status": "allowed_conditionally_if_source_evidence_exists",
    },
    {
        "fate": "harmless_calibration",
        "required_evidence": "constant universal parent-fixed monopole with no species/time/range dependence",
        "runner_handling": "absorbed into measured GM with calibration note",
        "claim_status": "not a new physics residual if all universality gates pass",
    },
    {
        "fate": "retained_scored",
        "required_evidence": "coefficient, curve, or residual amplitude mapped to local-bound row",
        "runner_handling": "score against R3/R4/R7/R8/R9/R10/R11 as applicable",
        "claim_status": "empirical modified-gravity branch only",
    },
    {
        "fate": "symbolic_blocker",
        "required_evidence": "channel known but coefficient/curve missing",
        "runner_handling": "block pass; do not count as small",
        "claim_status": "no local-GR or empirical pass",
    },
    {
        "fate": "invalid_route",
        "required_evidence": "fixed external projector, dropped metric stress, or Ward-owned declared absent",
        "runner_handling": "reject branch",
        "claim_status": "forbidden",
    },
]


INVALID_ROUTES = [
    {
        "route": "fixed_external_projector",
        "why_invalid": "explicit diffeomorphism breaking can masquerade as conservation if not varied",
        "required_fix": "make projector covariant/dynamical/topological or reject branch",
    },
    {
        "route": "metric_dependent_projector_dropped_stress",
        "why_invalid": "Hodge/orthogonal/projector metric dependence carries stress",
        "required_fix": "retain T_projector and score it, or prove it vanishes",
    },
    {
        "route": "Ward_owned_equals_absent",
        "why_invalid": "a conserved hidden flux can still shift mu_obs and PPN rows",
        "required_fix": "prove zero/constant universal calibration or retain as residual",
    },
    {
        "route": "radial_hair_absorbed_into_mass",
        "why_invalid": "r-dependent source profile is a fifth-force/beta channel",
        "required_fix": "derive dM_eff/dr=0 and no R_extra radial source",
    },
    {
        "route": "symbolic_fifth_force_pass",
        "why_invalid": "alpha(lambda) without a curve or theorem-zero is not an empirical result",
        "required_fix": "provide executable alpha(lambda) or prove source-free mass gap",
    },
    {
        "route": "nonEH_operator_unlisted",
        "why_invalid": "Ward-conserved non-EH terms can alter gamma, beta, xi, and fifth-force rows",
        "required_fix": "supply c_nonEH vector or derive EH-only exterior",
    },
]


RESIDUAL_ROW_MAP = [
    {
        "row_id": "R3_gamma",
        "source_channels": "boundary shear; bulk X; non-EH slip",
        "current_status": "retained",
        "required_for_pass": "no shear/bulk/non-EH source or scored coefficient below lock",
    },
    {
        "row_id": "R4_beta",
        "source_channels": "radial hair; boundary monopole; nonlinear source; non-EH potential",
        "current_status": "retained",
        "required_for_pass": "mu_extra zero or beta residual below lock",
    },
    {
        "row_id": "R5_alpha1",
        "source_channels": "domain/projector vector",
        "current_status": "retained",
        "required_for_pass": "covariant dynamical domain/projector with no vector hair",
    },
    {
        "row_id": "R6_alpha2",
        "source_channels": "domain/projector vector or preferred frame",
        "current_status": "retained",
        "required_for_pass": "same as R5 plus source-locked coefficient",
    },
    {
        "row_id": "R7_alpha3",
        "source_channels": "unowned momentum flux; boundary/projector exchange",
        "current_status": "retained_contingent",
        "required_for_pass": "C1 auxiliary on-shell and Ward-owned flux zero/retained below lock",
    },
    {
        "row_id": "R8_xi",
        "source_channels": "boundary/domain anisotropy",
        "current_status": "retained",
        "required_for_pass": "class-only no-angular plus covariant domain no-location theorem",
    },
    {
        "row_id": "R9_Gdot",
        "source_channels": "time-dependent boundary/domain/bulk/source normalization",
        "current_status": "retained_contingent",
        "required_for_pass": "partial_t mu_obs=0 theorem or numeric drift below lock",
    },
    {
        "row_id": "R10_fifth_force",
        "source_channels": "bulk X, radial hair, finite-range domain/boundary tail",
        "current_status": "symbolic_deferred",
        "required_for_pass": "alpha(lambda) curve or theorem-zero no-hair",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "source_channels": "non-EH operator and projector stress",
        "current_status": "retained_symbolic",
        "required_for_pass": "EH-only exterior or executable coefficient vector",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "all exterior extra source channels are named and routed",
        "status": "pass",
        "evidence": "E0-E7 owner gates and R3-R11 residual row map written",
    },
    {
        "claim": "valid legal fates are theorem-zero, harmless calibration, retained/scored, symbolic blocker, or invalid",
        "status": "pass",
        "evidence": "owner fate matrix written",
    },
    {
        "claim": "exterior extra sources vanish from the current parent action",
        "status": "fail",
        "evidence": "boundary, bulk X, projector/domain, auxiliary, and non-EH sources remain conditional or retained",
    },
    {
        "claim": "mu_extra=0 is promoted",
        "status": "fail",
        "evidence": "no parent no-hair owner proof for all R_extra channels",
    },
    {
        "claim": "local GR/Newton/PPN can be claimed",
        "status": "fail",
        "evidence": "0 theorem-zero row upgrades and R10/R11 remain symbolic blockers",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "exterior_source_owner_gate_written",
        "status": "pass",
        "evidence": "8 exterior source gates recorded",
    },
    {
        "gate": "nohair_owner_conditions_written",
        "status": "pass",
        "evidence": "7 no-hair owner conditions recorded",
    },
    {
        "gate": "invalid_routes_forbidden",
        "status": "pass",
        "evidence": "6 fake-GR/source-hiding routes rejected",
    },
    {
        "gate": "boundary_nohair_parent_derived",
        "status": "fail",
        "evidence": "class-only boundary action remains conditional and radial hair open",
    },
    {
        "gate": "bulk_X_nohair_or_curve_derived",
        "status": "fail",
        "evidence": "m_X, q_X, Q_X, q_test, and alpha_X(lambda_X) missing",
    },
    {
        "gate": "projector_domain_nohair_derived",
        "status": "fail",
        "evidence": "projector/domain covariance and no-vector/no-shear theorem remain open",
    },
    {
        "gate": "auxiliary_on_shell_derived",
        "status": "fail",
        "evidence": "C1 Euler-equation ledger not yet supplied",
    },
    {
        "gate": "nonEH_operator_resolved",
        "status": "fail",
        "evidence": "R11 coefficient vector or EH-only theorem still missing",
    },
    {
        "gate": "mu_extra_zero_promoted",
        "status": "fail",
        "evidence": "R_extra channels are routed but not all killed or harmless",
    },
    {
        "gate": "runner_rows_promoted_to_theorem_zero",
        "status": "fail",
        "evidence": "0 row upgrades; R3/R4/R7/R8/R9/R10/R11 retained or symbolic",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "owner gate only; no Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The exterior extra-source no-hair owner gate is now explicit: every R_extra/mu_extra channel must be theorem-zero, harmless constant universal calibration, retained and scored, symbolic-blocking, or invalid if hidden by dropped stress. This prevents boundary, bulk X, projector/domain, auxiliary, and non-EH terms from being silently absorbed into measured GM. The current corpus does not yet derive the no-hair owner conditions, so mu_extra=0 is not promoted and R3/R4/R7/R8/R9/R10/R11 remain retained or symbolic.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "436-auxiliary-projector-local-Euler-equation-ledger.md",
        "why_next": "C1 is the strongest direct Ward route: put every auxiliary/projector/domain Euler equation on shell or retain its force",
    },
    {
        "rank": 2,
        "target": "R10 alpha(lambda) executable curve contract",
        "why_next": "bulk/range tails cannot remain symbolic if empirical local testing is next",
    },
    {
        "rank": 3,
        "target": "R11 non-EH coefficient vector contract",
        "why_next": "EH-only exterior or an executable c_nonEH vector is required before local-GR scoring",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 435 - Exterior Extra-Source No-Hair Owner Gate

Private no-hair/source-normalization/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 434 made measured source normalization explicit: `mu_obs = G_eff M_eff + mu_extra`. This checkpoint asks what must happen to every exterior extra source in `mu_extra`: theorem-zero, harmless calibration, retained/scored, symbolic blocker, or invalid if hidden.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/exterior_extra_source_nohair_owner_gate.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Exterior Source Owner Gate

{markdown_table(EXTERIOR_SOURCE_OWNER_GATE, ["gate_id", "source_channel", "current_status", "legal_fate", "rows"])}

Core rule:

```text
R_extra is not allowed to disappear by prose.

For each exterior source channel S_i:

S_i -> theorem_zero
   or harmless_constant_universal_calibration
   or retained_scored_residual
   or symbolic_blocker
   or invalid_route.

Ward-owned nonzero flux is not theorem-zero.
Dropped stress is not theorem-zero.
Range/species/time dependence is not measured-GM calibration.
```

## 5. No-Hair Owner Conditions

{markdown_table(NOHAIR_OWNER_CONDITIONS, ["condition_id", "must_show", "if_solved", "current_status"])}

## 6. Owner Fate Matrix

{markdown_table(OWNER_FATE_MATRIX, ["fate", "required_evidence", "runner_handling", "claim_status"])}

## 7. Invalid Routes

{markdown_table(INVALID_ROUTES, ["route", "why_invalid", "required_fix"])}

## 8. Residual Row Map

{markdown_table(RESIDUAL_ROW_MAP, ["row_id", "source_channels", "current_status", "required_for_pass"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is the bouncer at the door. Extra exterior source channels can enter the theory only with ID: a parent no-hair theorem, a harmless universal calibration, or a scored residual. No ID, no local-GR claim.

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "exterior_source_owner_gate.csv", EXTERIOR_SOURCE_OWNER_GATE)
    write_csv(results_dir / "nohair_owner_conditions.csv", NOHAIR_OWNER_CONDITIONS)
    write_csv(results_dir / "owner_fate_matrix.csv", OWNER_FATE_MATRIX)
    write_csv(results_dir / "invalid_routes.csv", INVALID_ROUTES)
    write_csv(results_dir / "residual_row_map.csv", RESIDUAL_ROW_MAP)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "exterior_source_gates": len(EXTERIOR_SOURCE_OWNER_GATE),
        "nohair_owner_conditions": len(NOHAIR_OWNER_CONDITIONS),
        "invalid_routes": len(INVALID_ROUTES),
        "residual_rows_mapped": len(RESIDUAL_ROW_MAP),
        "all_Rextra_channels_routed": True,
        "boundary_nohair_parent_derived": False,
        "bulk_X_nohair_or_curve_derived": False,
        "projector_domain_nohair_derived": False,
        "auxiliary_on_shell_derived": False,
        "nonEH_operator_resolved": False,
        "mu_extra_zero_promoted": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 435 exterior extra-source no-hair owner gate artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
