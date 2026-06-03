from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "mu_extra_zero_owner_or_source_normalization_coefficient_vector_written_mu_extra_sum_rule_and_8_channel_coefficient_vector_no_zero_owner_pass_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "mu_extra_owner_or_coefficient_vector_only_no_mu_extra_zero_constant_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "468-mu-extra-coefficient-vector-to-local-bound-scorecard.md"

DOC_PATH = Path("467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md")
OWNER_GATE_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ZERO_OWNER_GATE.csv")
CHANNEL_LEDGER_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv")
COEFFICIENT_VECTOR_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv")
R11_LINK_PATH = Path("source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ZERO_OR_VECTOR_DECISION.csv")

MU_EXTRA_DECOMP_PATH = Path("runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_decomposition.csv")
MU_EXTRA_REQUIREMENTS_PATH = Path("runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_zero_requirements.csv")
CONSTANT_GM_RUNNER_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv")
CONSTANT_GM_ZERO_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv")
P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
R11_SOURCE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv")
R11_SKELETON_PATH = Path("source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv")


SOURCE_REGISTER = [
    {
        "path": "434-measured-GM-mu-extra-zero-route.md",
        "role": "measured-GM decomposition and eight mu_extra channels",
    },
    {
        "path": "435-exterior-extra-source-nohair-owner-gate.md",
        "role": "exterior extra-source ownership fates and invalid routes",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward/Bianchi warning that owned hidden flux is not absence",
    },
    {
        "path": "466-constant-GM-zero-theorem-or-local-residual-runner.md",
        "role": "constant-GM zero theorem failed and residual runner loaded",
    },
    {
        "path": str(MU_EXTRA_DECOMP_PATH),
        "role": "machine-readable mu_extra channel decomposition",
    },
    {
        "path": str(MU_EXTRA_REQUIREMENTS_PATH),
        "role": "machine-readable mu_extra zero requirements",
    },
    {
        "path": str(CONSTANT_GM_RUNNER_PATH),
        "role": "constant-GM local residual runner input",
    },
    {
        "path": str(P8_TEMPLATE_PATH),
        "role": "P8 bound targets for source-normalization residuals",
    },
    {
        "path": str(R11_SOURCE_VECTOR_PATH),
        "role": "R11 derivative-hair vector exposing missing epsilon_mu coefficient",
    },
    {
        "path": str(R11_SKELETON_PATH),
        "role": "R11 minimum skeleton with source_normalization_operator row",
    },
]


OWNER_GATE_COLUMNS = [
    "gate_id",
    "gate_name",
    "required_statement",
    "current_evidence",
    "status",
    "if_passes",
    "if_fails",
    "next_action",
]


OWNER_GATE_ROWS = [
    {
        "gate_id": "MO0_sum_rule",
        "gate_name": "mu_extra channel sum rule",
        "required_statement": "mu_extra = sum_i mu_i and epsilon_mu = sum_i epsilon_i with epsilon_i := mu_i/(G_eff M_eff)",
        "current_evidence": "434 gives eight mu_extra channels; 465/466 define epsilon_mu",
        "status": "pass_identity",
        "if_passes": "mu_extra can be scored channel-by-channel",
        "if_fails": "source-normalization cannot be audited",
        "next_action": "use channel ledger and coefficient vector",
    },
    {
        "gate_id": "MO1_owner_not_absence",
        "gate_name": "Ward-owned hidden flux is not automatically zero",
        "required_statement": "owned/conserved channel must still be zero, constant universal calibration, or explicitly scored",
        "current_evidence": "429 and 434 explicitly warn that Ward ownership alone does not prove mu_extra=0",
        "status": "pass_policy",
        "if_passes": "prevents fake GR by conserved hidden stress",
        "if_fails": "mu_extra could be hidden inside GM",
        "next_action": "require owner verdict plus coefficient for each channel",
    },
    {
        "gate_id": "MO2_boundary_owner",
        "gate_name": "boundary/topological source owner",
        "required_statement": "boundary source is topological/pure calibration or its coefficient is scored",
        "current_evidence": "boundary_monopole_shift retained; boundary no-hair conditional not parent-derived",
        "status": "retained_not_zero",
        "if_passes": "boundary epsilon row can be theorem-zero or calibration",
        "if_fails": "boundary contribution remains in coefficient vector",
        "next_action": "supply c_boundary/e_boundary coefficient or parent no-hair theorem",
    },
    {
        "gate_id": "MO3_domain_projector_owner",
        "gate_name": "domain/projector source owner",
        "required_statement": "projector/domain stress is covariant/dynamical/topological and has no monopole/vector/shear leakage",
        "current_evidence": "domain_projector_mass conditional_open; 435 keeps projector/domain coefficients retained",
        "status": "retained_not_zero",
        "if_passes": "domain epsilon row can be zeroed",
        "if_fails": "preferred-frame/location/vector rows remain active",
        "next_action": "supply c_domain/e_domain coefficient or projector no-hair theorem",
    },
    {
        "gate_id": "MO4_bulk_range_owner",
        "gate_name": "bulk/range source owner",
        "required_statement": "bulk X has source-free positive mass-gap no-hair or executable finite-range force curve",
        "current_evidence": "bulk_X_Yukawa_tail symbolic_deferred; R10 curve missing",
        "status": "symbolic_blocker",
        "if_passes": "bulk epsilon row can map to theorem-zero or R10 curve",
        "if_fails": "alpha(lambda) remains unscoreable",
        "next_action": "supply epsilon_bulk_X or R10 alpha(lambda) curve",
    },
    {
        "gate_id": "MO5_nonEH_owner",
        "gate_name": "non-EH operator owner",
        "required_statement": "EH-only exterior theorem or non-EH coefficient vector maps operator potential into residual rows",
        "current_evidence": "nonEH_operator_potential retained_symbolic; 464 R11 vector still skeleton-only",
        "status": "symbolic_blocker",
        "if_passes": "R11 source-normalization row becomes executable",
        "if_fails": "operator potential stays retained",
        "next_action": "link c_nonEH vector to epsilon_nonEH_source",
    },
    {
        "gate_id": "MO6_species_time_frame_owner",
        "gate_name": "species/time/frame source owner",
        "required_statement": "source universality, time stationarity, and same-frame source pullback are parent-derived or scored",
        "current_evidence": "species_source_charge, time_drift, and frame rows are not parent-derived",
        "status": "retained_not_zero",
        "if_passes": "derivative hair can be zeroed",
        "if_fails": "eta/Gdot/frame residual rows remain active",
        "next_action": "supply source-charge, time-drift, and frame-split rows",
    },
    {
        "gate_id": "MO7_constant_calibration_owner",
        "gate_name": "absolute calibration owner",
        "required_statement": "constant offset is parent-fixed, universal, source/range/time/frame independent",
        "current_evidence": "absolute_calibration_offset is harmless only if parent-fixed; not derived",
        "status": "conditional_harmless_not_parent_fixed",
        "if_passes": "epsilon_calibration may be absorbed into measured GM",
        "if_fails": "calibration offset remains retained",
        "next_action": "derive parent fixed calibration or keep epsilon_calibration row",
    },
    {
        "gate_id": "MO8_all_channels_closed",
        "gate_name": "mu_extra zero theorem",
        "required_statement": "all epsilon_i are theorem-zero or harmless universal constants and all derivative channels vanish",
        "current_evidence": "multiple channels are retained, symbolic, or conditional; no numeric coefficients supplied",
        "status": "fail",
        "if_passes": "mu_extra=0 or harmless calibration; constant GM can advance",
        "if_fails": "coefficient vector is mandatory",
        "next_action": "do not promote Newton; generate coefficient vector",
    },
]


CHANNEL_LEDGER_COLUMNS = [
    "channel",
    "source_class",
    "symbolic_form",
    "epsilon_symbol",
    "owner_required",
    "current_status",
    "owner_verdict",
    "affected_rows",
    "bound_target",
    "residual_artifact_required",
    "claim_effect",
    "next_action",
]


CHANNEL_LEDGER_ROWS = [
    {
        "channel": "radial_Meff_hair",
        "source_class": "mass_flux_radial",
        "symbolic_form": "dM_eff/dr != 0",
        "epsilon_symbol": "epsilon_radial_Meff",
        "owner_required": "Pi_M flux closure plus no radial memory leakage",
        "current_status": "conditional_not_parent_owned",
        "owner_verdict": "retained_coefficient_required",
        "affected_rows": "R4;R10",
        "bound_target": "zero radial hair or mapped PPN/fifth-force residual",
        "residual_artifact_required": "P8_radial_mu_profile_or_zero.csv",
        "claim_effect": "blocks radius-independent measured GM",
        "next_action": "derive radial no-hair or fill epsilon_radial_Meff(r)",
    },
    {
        "channel": "boundary_monopole_shift",
        "source_class": "boundary_topological",
        "symbolic_form": "mu_boundary = constant or time/radial dependent",
        "epsilon_symbol": "epsilon_boundary",
        "owner_required": "class/topological boundary no-hair or constant universal calibration",
        "current_status": "retained",
        "owner_verdict": "retained_coefficient_required",
        "affected_rows": "R4;R7;R8;R9",
        "bound_target": "beta/alpha3/xi/Gdot locks",
        "residual_artifact_required": "P8_mu_extra_boundary_coefficients.csv",
        "claim_effect": "blocks hidden boundary-GM absorption",
        "next_action": "derive boundary no-hair or fill epsilon_boundary",
    },
    {
        "channel": "domain_projector_mass",
        "source_class": "projector_domain",
        "symbolic_form": "mu_domain[P_D,D] != 0",
        "epsilon_symbol": "epsilon_domain_projector",
        "owner_required": "covariant projector plus no-vector/no-shear/no-monopole leakage",
        "current_status": "conditional_open",
        "owner_verdict": "retained_coefficient_required",
        "affected_rows": "R5;R6;R7;R8;R11",
        "bound_target": "alpha1/alpha2/alpha3/xi/operator ledger",
        "residual_artifact_required": "P8_mu_extra_domain_projector_coefficients.csv",
        "claim_effect": "blocks preferred-frame/location silence",
        "next_action": "derive projector no-leak theorem or fill epsilon_domain_projector",
    },
    {
        "channel": "bulk_X_Yukawa_tail",
        "source_class": "bulk_range",
        "symbolic_form": "delta a/a_GR = alpha_X (1+r/lambda_X) exp(-r/lambda_X)",
        "epsilon_symbol": "epsilon_bulk_X",
        "owner_required": "positive source-free mass-gap no-hair or executable force-law below bounds",
        "current_status": "symbolic_deferred",
        "owner_verdict": "R10_curve_or_coefficient_required",
        "affected_rows": "R10",
        "bound_target": "alpha(lambda) curve",
        "residual_artifact_required": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "claim_effect": "blocks fifth-force silence",
        "next_action": "fill epsilon_bulk_X plus lambda_X or theorem-zero",
    },
    {
        "channel": "nonEH_operator_potential",
        "source_class": "nonEH_operator",
        "symbolic_form": "Phi = Phi_EH + c_i Phi_i",
        "epsilon_symbol": "epsilon_nonEH_source",
        "owner_required": "EH-only exterior or coefficient vector retained and scored",
        "current_status": "retained_symbolic",
        "owner_verdict": "R11_coefficient_vector_required",
        "affected_rows": "R3;R4;R10;R11",
        "bound_target": "gamma/beta/R10/R11 coefficient locks",
        "residual_artifact_required": "R11_nonEH_operator_vector_executable.csv",
        "claim_effect": "blocks EH-only/Newton promotion",
        "next_action": "derive EH-only or map non-EH coefficients into epsilon_nonEH_source",
    },
    {
        "channel": "species_source_charge",
        "source_class": "species_material_source",
        "symbolic_form": "Delta_A mu_obs != 0",
        "epsilon_symbol": "epsilon_species_A",
        "owner_required": "same source normalization for all compositions",
        "current_status": "not_derived",
        "owner_verdict": "retained_coefficient_required",
        "affected_rows": "R1;R2",
        "bound_target": "eta_source_AB <= 2.8e-15 or theorem-zero",
        "residual_artifact_required": "P8_species_source_charge_residual_or_zero.csv",
        "claim_effect": "blocks source-side WEP",
        "next_action": "derive selector-blind source action or fill epsilon_species_A",
    },
    {
        "channel": "time_drift",
        "source_class": "time_memory_source",
        "symbolic_form": "partial_t mu_obs != 0",
        "epsilon_symbol": "epsilon_time_drift",
        "owner_required": "stationary G_eff, M_eff, boundary/domain/bulk source",
        "current_status": "not_derived",
        "owner_verdict": "retained_coefficient_required",
        "affected_rows": "R9",
        "bound_target": "Gdot_over_G <= 9.6e-15 yr^-1 or theorem-zero",
        "residual_artifact_required": "P8_time_drift_residual_or_zero.csv",
        "claim_effect": "blocks local Gdot silence",
        "next_action": "derive stationarity or fill epsilon_time_drift",
    },
    {
        "channel": "absolute_calibration_offset",
        "source_class": "constant_calibration",
        "symbolic_form": "mu_obs = lambda0 G_ref M_bare",
        "epsilon_symbol": "epsilon_calibration",
        "owner_required": "constant universal calibration absorbed into measured GM",
        "current_status": "harmless_if_parent_fixed_not_derived",
        "owner_verdict": "conditional_calibration_not_claimable",
        "affected_rows": "R4;R9",
        "bound_target": "parent-fixed universal constant with zero derivatives",
        "residual_artifact_required": "P8_absolute_calibration_owner.csv",
        "claim_effect": "does not block if parent-fixed; currently not earned",
        "next_action": "derive parent-fixed calibration or retain epsilon_calibration",
    },
]


COEFFICIENT_VECTOR_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "channel",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "observable_link",
    "bound_or_target",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def coefficient_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    observable_by_channel = {
        "radial_Meff_hair": "partial_r_ln_mu_obs;alpha(lambda)",
        "boundary_monopole_shift": "beta_minus_1;alpha3;xi;Gdot_over_G",
        "domain_projector_mass": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "bulk_X_Yukawa_tail": "alpha(lambda)",
        "nonEH_operator_potential": "gamma_minus_1;beta_minus_1;alpha(lambda);operator_ledger",
        "species_source_charge": "eta_source_AB;clock_redshift",
        "time_drift": "Gdot_over_G",
        "absolute_calibration_offset": "beta_minus_1;Gdot_over_G",
    }
    for ledger in CHANNEL_LEDGER_ROWS:
        epsilon_symbol = ledger["epsilon_symbol"]
        rows.append(
            {
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "mu_extra_owner_or_coefficient_vector",
                "vector_id": "P8_mu_extra_source_normalization_coefficient_vector",
                "channel": ledger["channel"],
                "coefficient_symbol": epsilon_symbol,
                "coefficient_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT",
                "coefficient_units": "dimensionless",
                "normalization": f"{epsilon_symbol} = mu_{ledger['channel']} / (G_eff M_eff)",
                "operator_form": ledger["symbolic_form"],
                "weak_field_map": ledger["owner_required"],
                "affected_rows": ledger["affected_rows"],
                "observable_link": observable_by_channel[ledger["channel"]],
                "bound_or_target": ledger["bound_target"],
                "predicted_residual_or_bound_source": f"MISSING_{ledger['channel'].upper()}_RESIDUAL_OR_ZERO_SOURCE",
                "derivation_status": "retained_unfilled" if "conditional_calibration" not in ledger["owner_verdict"] else "conditional_harmless_not_parent_fixed",
                "formula_reference": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
                "source_file": str(CHANNEL_LEDGER_PATH),
                "assumptions": "same-frame compact exterior; coefficient normalized to measured G_eff M_eff; no tuned cancellation credit",
                "valid_for_claim": "false",
                "notes": f"owner_verdict={ledger['owner_verdict']}; {ledger['next_action']}",
            }
        )
    return rows


R11_LINK_COLUMNS = [
    "r11_family",
    "p8_channel",
    "epsilon_symbol",
    "r11_operator_dependency",
    "required_for_valid_claim",
    "current_status",
    "next_action",
]


def r11_link_rows() -> list[dict[str, str]]:
    return [
        {
            "r11_family": "source_normalization_operator",
            "p8_channel": row["channel"],
            "epsilon_symbol": row["epsilon_symbol"],
            "r11_operator_dependency": "mu_extra_or_delta_GM_operator_vector",
            "required_for_valid_claim": "coefficient_value, units, normalization, weak-field map, bound/source path, assumptions",
            "current_status": "retained_unfilled",
            "next_action": row["next_action"],
        }
        for row in CHANNEL_LEDGER_ROWS
    ]


DECISION_COLUMNS = ["decision_item", "status", "evidence", "next_action"]


def source_register_rows() -> list[dict[str, str]]:
    return [
        {"path": item["path"], "exists": str((ROOT / item["path"]).exists()), "role": item["role"]}
        for item in SOURCE_REGISTER
    ]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def count_token(rows: list[dict[str, Any]], token: str) -> int:
    return sum(str(value).count(token) for row in rows for value in row.values())


def decision_rows(source_paths_missing: int, decomp_rows_loaded: int, coefficient_vector: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_coefficients = sum(1 for row in coefficient_vector if "MISSING_" in row["coefficient_value"])
    claimable_rows = sum(1 for row in coefficient_vector if row["valid_for_claim"] == "true")
    return [
        {
            "decision_item": "source_paths",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
            "next_action": "continue with cited source register",
        },
        {
            "decision_item": "mu_extra_decomposition_loaded",
            "status": "pass" if decomp_rows_loaded == 8 else "fail",
            "evidence": f"mu_extra decomposition rows loaded = {decomp_rows_loaded}",
            "next_action": "use eight-channel coefficient vector",
        },
        {
            "decision_item": "mu_extra_sum_rule_written",
            "status": "pass_identity",
            "evidence": "epsilon_mu = sum_i epsilon_i with channel normalization",
            "next_action": "score each epsilon_i separately",
        },
        {
            "decision_item": "mu_extra_zero_owner_theorem",
            "status": "fail",
            "evidence": "channels remain retained, symbolic, conditional, or not parent-derived",
            "next_action": "do not claim mu_extra=0",
        },
        {
            "decision_item": "coefficient_vector_executable",
            "status": "fail",
            "evidence": f"missing coefficient rows = {missing_coefficients}; claimable rows = {claimable_rows}",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_item": "constant_GM_promoted",
            "status": "fail",
            "evidence": "epsilon_mu vector not zeroed or numerically scored",
            "next_action": "keep constant GM no-claim",
        },
        {
            "decision_item": "Newton_or_local_GR_promoted",
            "status": "fail",
            "evidence": "mu_extra source-normalization blocker remains active",
            "next_action": "feed coefficient vector to local-bound scorecard",
        },
    ]


def render_doc(
    run_dir: Path,
    source_rows: list[dict[str, str]],
    coefficient_vector: list[dict[str, str]],
    links: list[dict[str, str]],
    decisions: list[dict[str, str]],
    decomp_rows_loaded: int,
    missing_coefficients: int,
) -> str:
    return f"""# 467 - mu_extra Zero Owner or Source-Normalization Coefficient Vector

Private measured-GM/source-normalization checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 466 made the constant-GM theorem fail in a useful way: the blocker is now concentrated in

```text
epsilon_mu := mu_extra / (G_eff M_eff).
```

This checkpoint asks whether `mu_extra=0` can be owner-derived. If not, every hidden contribution must become a coefficient row.

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/mu_extra_zero_owner_or_source_normalization_coefficient_vector.py` |
| Run directory | `{run_dir}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Owner gate CSV | `{OWNER_GATE_PATH}` |
| Channel ledger CSV | `{CHANNEL_LEDGER_PATH}` |
| Coefficient vector CSV | `{COEFFICIENT_VECTOR_PATH}` |
| R11 link CSV | `{R11_LINK_PATH}` |
| Decision CSV | `{DECISION_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["path", "exists", "role"])}

## 4. Sum Rule

The useful algebraic move is:

```text
mu_extra = sum_i mu_i
epsilon_mu = mu_extra/(G_eff M_eff)
epsilon_mu = sum_i epsilon_i
epsilon_i := mu_i/(G_eff M_eff).
```

So `mu_extra=0` can only be claimed if every channel is theorem-zero, or if a channel is a parent-fixed universal constant calibration with zero derivative hair. Otherwise the channel enters the source-normalization coefficient vector.

## 5. Owner Gate

The owner gate has been written to `{OWNER_GATE_PATH}`.

{md_table(OWNER_GATE_ROWS, OWNER_GATE_COLUMNS)}

## 6. Channel Owner Ledger

The channel owner ledger has been written to `{CHANNEL_LEDGER_PATH}`. It loaded `{decomp_rows_loaded}` prior mu_extra decomposition rows and refactors them into coefficient channels.

{md_table(CHANNEL_LEDGER_ROWS, CHANNEL_LEDGER_COLUMNS)}

## 7. Coefficient Vector

The coefficient vector has been written to `{COEFFICIENT_VECTOR_PATH}`.

{md_table(coefficient_vector, COEFFICIENT_VECTOR_COLUMNS)}

## 8. R11 Link

The R11 source-normalization link has been written to `{R11_LINK_PATH}`.

{md_table(links, R11_LINK_COLUMNS)}

## 9. Decision

{md_table(decisions, DECISION_COLUMNS)}

## 10. Result

The sum rule lands, but the zero owner theorem does not. The corpus has enough structure to name the eight hidden measured-GM channels, but not enough parent derivation to set them all to zero.

That is not a dead end; it is the right demotion. `mu_extra` is no longer one mysterious blocker. It is an eight-row source-normalization coefficient vector. Current missing coefficient rows: `{missing_coefficients}`.

Practical read: the punch is cleaner now. If MTS wants derived Newton, these epsilon rows must vanish from the parent action. If they do not vanish, they become the modified-gravity scorecard rather than being smuggled into `GM`.

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | turn the eight epsilon rows into local-bound scorecard rows or theorem-zero certificates |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | bulk/range epsilon cannot be scored without a curve |
| 3 | `R11_nonEH_operator_vector_executable.csv` | non-EH potential epsilon cannot be scored without an operator vector |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-mu-extra-zero-owner-or-source-normalization-coefficient-vector"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    source_paths_missing = sum(1 for row in source_rows if row["exists"] != "True")
    decomp_rows = read_csv_rows(MU_EXTRA_DECOMP_PATH)
    requirement_rows = read_csv_rows(MU_EXTRA_REQUIREMENTS_PATH)
    constant_gm_rows = read_csv_rows(CONSTANT_GM_RUNNER_PATH)
    r11_source_rows = read_csv_rows(R11_SOURCE_VECTOR_PATH)

    coefficient_vector = coefficient_rows()
    links = r11_link_rows()
    decisions = decision_rows(source_paths_missing, len(decomp_rows), coefficient_vector)
    missing_coefficients = sum(1 for row in coefficient_vector if "MISSING_" in row["coefficient_value"])
    missing_markers = count_token(coefficient_vector, "MISSING_")
    generic_fill_tokens = (
        count_token(OWNER_GATE_ROWS, "fill_")
        + count_token(CHANNEL_LEDGER_ROWS, "fill_")
        + count_token(coefficient_vector, "fill_")
        + count_token(links, "fill_")
    )

    write_csv(ROOT / OWNER_GATE_PATH, OWNER_GATE_ROWS, OWNER_GATE_COLUMNS)
    write_csv(ROOT / CHANNEL_LEDGER_PATH, CHANNEL_LEDGER_ROWS, CHANNEL_LEDGER_COLUMNS)
    write_csv(ROOT / COEFFICIENT_VECTOR_PATH, coefficient_vector, COEFFICIENT_VECTOR_COLUMNS)
    write_csv(ROOT / R11_LINK_PATH, links, R11_LINK_COLUMNS)
    write_csv(ROOT / DECISION_PATH, decisions, DECISION_COLUMNS)

    write_csv(results_dir / "mu_extra_zero_owner_gate.csv", OWNER_GATE_ROWS, OWNER_GATE_COLUMNS)
    write_csv(results_dir / "mu_extra_channel_owner_ledger.csv", CHANNEL_LEDGER_ROWS, CHANNEL_LEDGER_COLUMNS)
    write_csv(results_dir / "mu_extra_source_normalization_coefficient_vector.csv", coefficient_vector, COEFFICIENT_VECTOR_COLUMNS)
    write_csv(results_dir / "R11_mu_extra_source_normalization_link.csv", links, R11_LINK_COLUMNS)
    write_csv(results_dir / "decision.csv", decisions, DECISION_COLUMNS)
    write_csv(results_dir / "source_register.csv", source_rows, ["path", "exists", "role"])

    doc = render_doc(
        run_dir=Path("runs") / f"{timestamp}-mu-extra-zero-owner-or-source-normalization-coefficient-vector",
        source_rows=source_rows,
        coefficient_vector=coefficient_vector,
        links=links,
        decisions=decisions,
        decomp_rows_loaded=len(decomp_rows),
        missing_coefficients=missing_coefficients,
    )
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "source_paths_missing": source_paths_missing,
        "mu_extra_decomposition_rows_loaded": len(decomp_rows),
        "mu_extra_requirement_rows_loaded": len(requirement_rows),
        "constant_GM_runner_rows_loaded": len(constant_gm_rows),
        "R11_source_normalization_rows_loaded": len(r11_source_rows),
        "owner_gate_rows": len(OWNER_GATE_ROWS),
        "channel_ledger_rows": len(CHANNEL_LEDGER_ROWS),
        "coefficient_vector_rows": len(coefficient_vector),
        "R11_link_rows": len(links),
        "decision_rows": len(decisions),
        "mu_extra_sum_rule_written": True,
        "mu_extra_zero_owner_theorem_passed": False,
        "coefficient_vector_written": True,
        "coefficient_vector_claimable_rows": sum(1 for row in coefficient_vector if row["valid_for_claim"] == "true"),
        "coefficient_vector_missing_coefficient_rows": missing_coefficients,
        "missing_markers_in_coefficient_vector": missing_markers,
        "generic_fill_placeholder_tokens_in_outputs": generic_fill_tokens,
        "mu_extra_zero_promoted": False,
        "constant_GM_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", status)
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default="20260602-214500")
    arguments = parser.parse_args()
    print(json.dumps(write_run(arguments.timestamp), indent=2))


if __name__ == "__main__":
    main()
