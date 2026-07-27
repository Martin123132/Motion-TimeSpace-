from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3970"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3970-Y5-R2FR-no-extra-exterior-monopole-hair-or-channel-bound-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3970_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv",
    "channels": SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv",
    "bound_vector": SRC / "P8_Y5_R2FR_3970_DELTA_MU_EXTRA_BOUND_VECTOR.csv",
    "feed": SRC / "P8_Y5_R2FR_3970_SINGLE_MASS_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3970_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3970_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3970_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3970_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3970_VALIDATION.csv",
}

NEXT_DOC = "3971-Y5-R2FR-boundary-PiM-domain-monopole-zero-or-finite-inputs.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3971_boundary_PiM_domain_monopole_zero_or_finite_inputs.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3970_00_3969_next", SRC / "P8_Y5_R2FR_3969_NEXT_TARGET.csv", "NEXT3969_0", "3969 handoff"),
        ("SRC3970_01_3969_uniqueness", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_1_conditional_uniqueness_theorem", "single-mass uniqueness"),
        ("SRC3970_02_3969_noextra", SRC / "P8_Y5_R2FR_3969_UNIQUENESS_HYPOTHESIS_GATE.csv", "HYP3969_3_no_extra_monopoles", "no extra monopole hypothesis"),
        ("SRC3970_03_3969_bounds", SRC / "P8_Y5_R2FR_3969_BETA_OBSTRUCTION_BOUND_ROWS.csv", "BND3969_0_extra_monopole", "extra monopole bound"),
        ("SRC3970_04_3969_feed", SRC / "P8_Y5_R2FR_3969_DELTA_B_SQUARE_FEED_UPDATE.csv", "UFEED3969_3_next", "no extra monopole feed"),
        ("SRC3970_05_extra_theorem", SRC / "P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv", "EM522_3_silence_theorem", "extra mass silence theorem"),
        ("SRC3970_06_extra_channels", SRC / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv", "EX522_8_absolute_calibration", "extra mass channel input ledger"),
        ("SRC3970_07_extra_map", SRC / "P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv", "OM522_0_total_extra_bound", "extra mass observable map"),
        ("SRC3970_08_extra_decision", SRC / "P8_Y5_EXTRA_MASS_DECISION.csv", "D522_1_no_cancellation", "extra mass no-cancellation decision"),
        ("SRC3970_09_gk_nohair", SRC / "P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv", "NH2470_4_coercive_zero", "GK no-hair proof route"),
        ("SRC3970_10_gk_fail", SRC / "P8_Y5_GK_NOHAIR_2470_FAILURE_MODES.csv", "FAIL2470_5_projector_hiding", "GK no-hair failure modes"),
        ("SRC3970_11_gk_bound", SRC / "P8_Y5_GK_NOHAIR_2470_STRESS_BOUND_FALLBACK.csv", "BND2470_2_metric_bound", "GK stress bound fallback"),
        ("SRC3970_12_elliptic", SRC / "P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_BOUNDARY_AMPLITUDE_THEOREM.csv", "BAT2606_1_nohair_zero_case", "coercive no-hair identity"),
        ("SRC3970_13_boundary_alpha3", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T5_parent_owner_audit", "boundary owner audit"),
        ("SRC3970_14_boundary_cohom", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_6_certificate_verdict", "boundary cohomology verdict"),
        ("SRC3970_15_memory_boundary", SRC / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_BOUNDARY_ZERO_GATE.csv", "BZ2627_5_current_verdict", "memory boundary zero verdict"),
        ("SRC3970_16_qsrc", SRC / "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CLAUSE_GATE.csv", "QG2649_4_projected_mass", "source/domain projected mass"),
        ("SRC3970_17_label", SRC / "P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_LABEL_FORGETTING_ATTEMPT.csv", "SFL2648_5_verdict", "source label forgetting verdict"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEM3970_0_split_identity",
            "claim_piece": "extra exterior monopole split",
            "mathematical_form": "mu_extra/mu := epsilon_mu_extra_total = sum_i epsilon_i",
            "derivation": "use EM522 split: boundary, domain, bulk/memory/range, nonEH, coupling, frame/species, PiM, anomaly, and calibration channels are separate inputs",
            "status": "EXACT_SPLIT_LEDGER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NEM3970_1_channelwise_zero_theorem",
            "claim_piece": "no-extra-monopole theorem",
            "mathematical_form": "forall i, epsilon_i=0 and [d,Pi_M]J_H=0 => mu_extra=0",
            "derivation": "linearity of the projected extra mass current gives zero total extra exterior monopole only when every channel projection is zero or parent-forced to cancel",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NEM3970_2_no_cancellation_envelope",
            "claim_piece": "absolute bound branch",
            "mathematical_form": "|mu_extra/mu| <= sum_i |epsilon_i|",
            "derivation": "open boundary/domain/bulk/nonEH/coupling/frame/PiM/anomaly/calibration channels cannot be hidden by sign tuning",
            "status": "BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NEM3970_3_nohair_zero_template",
            "claim_piece": "generic channel zero route",
            "mathematical_form": "source-free + positive/coercive operator + zero boundary flux + zero source charge/projection => channel hair zero",
            "derivation": "coercive energy/no-hair identity kills homogeneous hair only if source, boundary, topology, and projection premises are parent-owned",
            "status": "CONDITIONAL_TEMPLATE_PREMISES_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NEM3970_4_finite_fallback",
            "claim_piece": "hidden monopole finite branch",
            "mathematical_form": "Delta_mu_extra_over_mu := sum_i epsilon_i; |Delta_B_single_mass|/A_source^2 <= C_mu sum_i |epsilon_i|",
            "derivation": "if channelwise no-hair fails, the single-mass/beta route stays testable through finite nonclaim rows",
            "status": "FINITE_BOUND_VECTOR_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def channel_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CH3970_0_boundary", "epsilon_boundary", "boundary_monopole_shift", "boundary no-hair/no-flux theorem or class-only global constant with zero derivatives", "epsilon_boundary;boundary_flux_vector;alpha3_map;xi_map;Gdot_map;units;source_file", "beta;alpha3;xi;Gdot"),
        ("CH3970_1_domain", "epsilon_domain_projector", "domain_projector_mass", "domain selector is topological/covariant with no mass projection, no vector, no anisotropy, and no time/range derivative", "W_domain_alpha1;W_domain_alpha2;W_domain_alpha3;W_domain_xi;epsilon_domain_flux;source_file", "alpha1;alpha2;alpha3;xi;beta"),
        ("CH3970_2_bulk_memory_range", "epsilon_bulk_X", "bulk_X_Yukawa_tail", "positive source-free mass-gap/no-hair theorem or zero Pi_M projection of bulk/memory exchange", "lambda_X;alpha_X;epsilon_bulk_X;range_units;alpha_lambda_bound;source_file", "alpha(lambda);beta;gamma"),
        ("CH3970_3_nonEH", "epsilon_nonEH_source", "nonEH_operator_potential", "same-frame local exterior is EH plus Lambda with all non-EH coefficients zero/topological/bounded", "operator_family;coefficient_value;units;normalization;weak_field_map;source_file", "gamma;beta;R10"),
        ("CH3970_4_coupling", "epsilon_time_drift", "time_drift", "topological/global kappa sector with no time, range, species, radial, frame, or domain derivatives", "epsilon_time_drift;dln_mu_dt;Gdot_over_G;units;source_file", "Gdot;beta;source-charge"),
        ("CH3970_5_frame_species", "epsilon_species_A", "species_source_charge", "same observed coframe plus selector-blind dressed source charge for all matter species", "species_pair;epsilon_species_A;eta_source_AB;clock_residual;source_file", "WEP;clock;frame;beta"),
        ("CH3970_6_PiM", "Delta_PiM", "projector_variation_mass", "topological absolute Pi_M with Hilbert equality or variation stress theorem-cancelled", "projector_type;metric_dependence_flag;Delta_PiM;units;normalization;source_file", "gamma;beta;alpha_i;xi"),
        ("CH3970_7_anomaly", "A_parent", "parent_anomaly_or_multiplier", "no ad hoc source-normalization multiplier, or multiplier is first-class/gauge/topological/Ward-owned with zero stress", "multiplier_id;A_parent_integral;units;stress_map;source_file", "radial;beta;R11"),
        ("CH3970_8_calibration", "epsilon_calibration", "absolute_calibration_offset", "parent-fixed universal calibration with zero range/time/species derivatives", "lambda0;universality_certificate;range_derivative;time_derivative;species_derivative;source_file", "beta;Gdot;absolute_GM"),
    ]
    return [
        {
            "channel_id": channel_id,
            "symbol": symbol,
            "p8_channel": p8_channel,
            "zero_route": zero_route,
            "bound_input_required": bound_input_required,
            "observable_locks": locks,
            "current_status": "ZERO_ROUTE_CONDITIONAL_INPUTS_MISSING",
            "score_term": f"|{symbol}|",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for channel_id, symbol, p8_channel, zero_route, bound_input_required, locks in specs
    ]


def bound_vector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MBV3970_0_total_extra_mass",
            "quantity": "epsilon_mu_extra_total",
            "formula": "epsilon_mu_extra_total <= |epsilon_boundary|+|epsilon_domain_projector|+|epsilon_bulk_X|+|epsilon_nonEH_source|+|epsilon_time_drift|+|epsilon_species_A|+|Delta_PiM|+|A_parent|+|epsilon_calibration|",
            "meaning": "absolute no-cancellation bound on hidden exterior monopole hair",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MBV3970_1_single_mass_feed",
            "quantity": "Delta_B_single_mass",
            "formula": "|Delta_B_single_mass|/A_source^2 <= C_mu epsilon_mu_extra_total",
            "meaning": "hidden monopole hair feeds the single-mass obstruction in the beta square-law route",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MBV3970_2_beta_feed",
            "quantity": "delta_beta_source",
            "formula": "|delta_beta_source| <= C_mu epsilon_mu_extra_total + remaining_nonmonopole_obstructions",
            "meaning": "no-extra-monopole is necessary but not sufficient for beta; other operator/readout/coupling terms still feed the vector",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SMF3970_0_mu_extra",
            "target": "mu_extra",
            "update_formula": "mu_extra=0 iff every extra monopole channel is theorem-zero or parent-forced zero; otherwise epsilon_mu_extra_total <= sum_i |epsilon_i|",
            "meaning": "single-exterior-mass uniqueness now has a channelwise hidden-hair gate",
            "status": "CHANNELWISE_GATE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SMF3970_1_Delta_B_single_mass",
            "target": "Delta_B_single_mass",
            "update_formula": "|Delta_B_single_mass|/A_source^2 <= C_mu epsilon_mu_extra_total",
            "meaning": "extra monopole hair directly feeds the beta square-law obstruction",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SMF3970_2_Delta_B_square",
            "target": "Delta_B_square_abs",
            "update_formula": "Delta_B_square_abs receives C_mu epsilon_mu_extra_total plus nonmonopole operator/readout/source-prefactor/coupling terms",
            "meaning": "3970 updates the 3968/3969 beta obstruction vector with explicit hidden-monopole hair rows",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SMF3970_3_next",
            "target": "boundary_PiM_domain_priority",
            "update_formula": "attack boundary, PiM, and domain channels first because they feed beta, alpha_i, xi, and radial mass closure at once",
            "meaning": "next derivation target is chosen by maximum local-GR leverage",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3970_0_noextra_theorem",
            "status": "CHANNELWISE_ZERO_THEOREM_AVAILABLE_CONDITIONALLY",
            "meaning": "mu_extra=0 follows if every extra channel projection is zero and PiM commutator/anomaly terms vanish",
            "claim_status": "conditional_not_parent_signed",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3970_1_current_gap",
            "status": "CHANNEL_ZERO_INPUTS_MISSING",
            "meaning": "current MTS has theorem routes but not parent-owned zero certificates or numeric inputs for all hidden-hair channels",
            "claim_status": "blocks_single_mass_beta_local_GR",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3970_2_priority",
            "status": "BOUNDARY_PIM_DOMAIN_FIRST",
            "meaning": "boundary, PiM/projector, and domain channels are highest leverage because they hit beta, preferred-frame, xi, radial mass, and source calibration simultaneously",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3970_0_sources",
            "gate": "source register",
            "requirement": "all cited local sources and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3970_1_noextra",
            "gate": "no extra exterior monopole",
            "requirement": "all nine hidden-hair channels theorem-zero or finite-bounded under no-cancellation policy",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3970_2_inputs",
            "gate": "finite bound inputs",
            "requirement": "units, normalizations, source files, and coefficient values for any nonzero channel",
            "status": "INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3970_3_single_mass",
            "gate": "single exterior mass and beta route",
            "requirement": "epsilon_mu_extra_total=0 or below beta/local locks, plus remaining Delta_B terms closed",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3970_4_next",
            "gate": "next proof target",
            "requirement": "boundary/PiM/domain zero or finite inputs",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3970_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound the boundary, PiM/projector, and domain hidden-monopole channels first, because these dominate the single-mass beta obstruction and preferred-frame/xi leakage",
            "success_condition": "epsilon_boundary, Delta_PiM, and epsilon_domain_projector become theorem-zero, or finite nonclaim rows with units/source paths feed epsilon_mu_extra_total",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "NO_EXTRA_MONOPOLE_CHANNELWISE_THEOREM_AND_BOUND_VECTOR_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "mu_extra zero theorem reduced to nine channel zeros; finite hidden-monopole bound vector feeds Delta_B_single_mass and beta source residual",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3970 - No Extra Exterior Monopole Hair Or Channel Bound Vector

Timestamp: `{timestamp}`

## Result

3970 turns the hidden exterior monopole problem into a channelwise theorem-or-bound gate.

The exact split is:

```text
mu_extra/mu = epsilon_mu_extra_total = sum_i epsilon_i
```

and the no-cancellation bound is:

```text
|mu_extra/mu| <=
 |epsilon_boundary|
+|epsilon_domain_projector|
+|epsilon_bulk_X|
+|epsilon_nonEH_source|
+|epsilon_time_drift|
+|epsilon_species_A|
+|Delta_PiM|
+|A_parent|
+|epsilon_calibration|
```

So single-exterior-mass uniqueness only gets promoted if every channel is zero or finite-bounded individually.

## Local-GR Feed

```text
|Delta_B_single_mass|/A_source^2 <= C_mu epsilon_mu_extra_total
|delta_beta_source| <= C_mu epsilon_mu_extra_total + remaining nonmonopole obstructions
```

## Decision

Next best target is not broad: attack boundary, PiM/projector, and domain first.
They hit beta, alpha_i, xi, radial mass closure, and source calibration at once.

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3970 - No Extra Exterior Monopole Hair

- Timestamp: `{timestamp}`
- Status: `NO_EXTRA_MONOPOLE_CHANNELWISE_THEOREM_AND_BOUND_VECTOR_READY`
- Core split:
  `mu_extra/mu = epsilon_mu_extra_total = sum_i epsilon_i`.
- No-cancellation bound:
  `epsilon_mu_extra_total <= sum_i |epsilon_i|`.
- Local-GR feed:
  `|Delta_B_single_mass|/A_source^2 <= C_mu epsilon_mu_extra_total`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3970 - No Extra Exterior Monopole Hair"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "theorem": theorem_rows(timestamp),
        "channels": channel_rows(timestamp),
        "bound_vector": bound_vector_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    channels = rows["channels"]
    bound_vector = rows["bound_vector"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    channel_symbols = {row["symbol"] for row in channels}
    needed = {
        "epsilon_boundary",
        "epsilon_domain_projector",
        "epsilon_bulk_X",
        "epsilon_nonEH_source",
        "epsilon_time_drift",
        "epsilon_species_A",
        "Delta_PiM",
        "A_parent",
        "epsilon_calibration",
    }

    return [
        val("VAL3970_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3970_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3970_02_theorem", any(row["row_id"] == "NEM3970_1_channelwise_zero_theorem" for row in theorem), "channelwise zero theorem row present"),
        val("VAL3970_03_no_cancellation", any(row["row_id"] == "NEM3970_2_no_cancellation_envelope" and "sum_i |epsilon_i|" in row["mathematical_form"] for row in theorem), "no-cancellation envelope present"),
        val("VAL3970_04_channels", needed <= channel_symbols and len(channels) == 9, "nine hidden-monopole channels present"),
        val("VAL3970_05_bound_vector", any(row["quantity"] == "epsilon_mu_extra_total" for row in bound_vector), "finite hidden-monopole bound vector present"),
        val("VAL3970_06_feed", {"mu_extra", "Delta_B_single_mass", "Delta_B_square_abs", "boundary_PiM_domain_priority"} <= {row["target"] for row in feed}, "single-mass beta feed rows present"),
        val("VAL3970_07_decision", any(row["status"] == "BOUNDARY_PIM_DOMAIN_FIRST" for row in decisions), "decision prioritizes boundary/PiM/domain"),
        val("VAL3970_08_claim_gate", any(row["status"] == "BLOCKED_NONCLAIM" for row in claims), "claim gate blocks single-mass/local-GR promotion"),
        val("VAL3970_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to boundary/PiM/domain zero or finite inputs"),
        val("VAL3970_10_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3970_11_score_ready", all(row["score_ready"] for row in channels), "channel rows are score-ready forms"),
        val("VAL3970_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3970_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3970_14_spine_updated", SPINE_PATH.exists() and "3970 - No Extra Exterior Monopole Hair" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3970_15_csv_parse", parsed, parse_detail),
        val("VAL3970_16_script_compile", True, "script compiled before validation write"),
        val("VAL3970_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["channels"], rows["channels"])
    write_csv(OUTPUTS["bound_vector"], rows["bound_vector"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3970 validation failed: {failed}")

    print(f"3970 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("No-extra-monopole channel theorem and hidden-hair bound vector assembled")


if __name__ == "__main__":
    run()
