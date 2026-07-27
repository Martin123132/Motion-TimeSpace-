from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3971"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3971-Y5-R2FR-boundary-PiM-domain-monopole-zero-or-finite-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3971_SOURCE_REGISTER.csv",
    "triad": SRC / "P8_Y5_R2FR_3971_BOUNDARY_PIM_DOMAIN_TRIAD_THEOREM_OR_BOUND.csv",
    "zero_tests": SRC / "P8_Y5_R2FR_3971_TRIAD_ZERO_TESTS.csv",
    "finite_inputs": SRC / "P8_Y5_R2FR_3971_TRIAD_FINITE_INPUT_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3971_EXTRA_MONOPOLE_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3971_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3971_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3971_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3971_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3971_VALIDATION.csv",
}

NEXT_DOC = "3972-Y5-R2FR-boundary-reference-no-flux-zero-or-first-finite-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3972_boundary_reference_no_flux_zero_or_first_finite_row.py"


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
        ("SRC3971_00_3970_next", SRC / "P8_Y5_R2FR_3970_NEXT_TARGET.csv", "NEXT3970_0", "3970 handoff"),
        ("SRC3971_01_3970_boundary", SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv", "CH3970_0_boundary", "boundary channel"),
        ("SRC3971_02_3970_domain", SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv", "CH3970_1_domain", "domain channel"),
        ("SRC3971_03_3970_PiM", SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv", "CH3970_6_PiM", "PiM channel"),
        ("SRC3971_04_3970_bound", SRC / "P8_Y5_R2FR_3970_DELTA_MU_EXTRA_BOUND_VECTOR.csv", "MBV3970_0_total_extra_mass", "hidden monopole total"),
        ("SRC3971_05_3970_feed", SRC / "P8_Y5_R2FR_3970_SINGLE_MASS_FEED_UPDATE.csv", "SMF3970_3_next", "triad priority feed"),
        ("SRC3971_06_EX_boundary", SRC / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv", "EX522_0_boundary_improvement", "extra mass boundary row"),
        ("SRC3971_07_EX_domain", SRC / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv", "EX522_1_domain_projector", "extra mass domain row"),
        ("SRC3971_08_EX_PiM", SRC / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv", "EX522_6_projector_stress", "extra mass PiM row"),
        ("SRC3971_09_EM_silence", SRC / "P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv", "EM522_3_silence_theorem", "extra mass silence theorem"),
        ("SRC3971_10_boundary_alpha3", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T5_parent_owner_audit", "boundary parent owner audit"),
        ("SRC3971_11_boundary_cohom", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_6_certificate_verdict", "boundary cohomology verdict"),
        ("SRC3971_12_boundary_obstruction", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_3_projector_stress", "boundary obstruction ledger"),
        ("SRC3971_13_boundary_residual", SRC / "P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_ROW.csv", "BRR545_0_boundary_reference_retained", "boundary reference residual"),
        ("SRC3971_14_PV_topological", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV1_topological_absolute_charge_route", "PiM topological route"),
        ("SRC3971_15_PV_boundary", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV3_boundary_only_nohair", "PiM boundary no-hair"),
        ("SRC3971_16_PV_domain", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV4_domain_homology_variation_owned", "PiM domain variation"),
        ("SRC3971_17_PV_map", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV6_modified_exterior_residual_map", "PiM residual map"),
        ("SRC3971_18_COM_verdict", SRC / "P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv", "COM1518_8_verdict", "PiM commutator verdict"),
        ("SRC3971_19_FCM_chainmap", SRC / "P8_Y5_PARENT_PIM_1518_FIXED_CHAINMAP_CONTRACT.csv", "FCM1518_3_chainmap", "PiM fixed chainmap"),
        ("SRC3971_20_PIM_total", SRC / "P8_Y5_PARENT_CR11_1516_PIM_EQUALITY_COMMUTATOR_REQUIREMENTS.csv", "PIM1516_5_total", "PiM total requirement"),
        ("SRC3971_21_domain_gate", SRC / "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CLAUSE_GATE.csv", "QG2649_4_projected_mass", "domain projected mass gate"),
        ("SRC3971_22_domain_constructor", SRC / "P8_Y5_SOURCE_DOMAIN_QUOTIENT_2649_QSRC_CONSTRUCTOR_ATTEMPT.csv", "QSRC2649_4_spurion_and_projector_gap", "domain spurion/projector gap"),
        ("SRC3971_23_localzero_boundary", SRC / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv", "I2_boundary_alpha3_preferred_momentum", "local zero boundary implication"),
        ("SRC3971_24_localzero_projector", SRC / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv", "I5_projector_stress_Bianchi", "local zero projector stress"),
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


def triad_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "TRI3971_0_triad_split",
            "claim_piece": "dominant hidden-monopole triad",
            "mathematical_form": "epsilon_mu_extra_total = |epsilon_boundary| + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels",
            "meaning": "boundary, PiM/projector, and domain are the first target because they jointly control beta, alpha_i, xi, radial mass closure, and source calibration",
            "status": "EXACT_PRIORITY_SPLIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3971_1_boundary_zero_route",
            "claim_piece": "boundary hidden monopole zero",
            "mathematical_form": "epsilon_boundary=0 if B_zero_flux=0, Delta_symp=0, boundary stress has no vector/shear/normal exchange, and residual reference is fixed before readout",
            "meaning": "scalar trace/no-volume flux is not enough; the boundary must have no monopole, derivative, preferred-frame, or reference leakage",
            "status": "CONDITIONAL_ZERO_ROUTE_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3971_2_PiM_zero_route",
            "claim_piece": "PiM/projector hidden monopole zero",
            "mathematical_form": "Delta_PiM=0 if Pi_M is fixed topological/chain-map, [d,Pi_M]J_H=0, delta_g Pi_M=0, and physical J_H lies in the parent mass-current complex",
            "meaning": "the Gamma-natural piece was reduced earlier, but metric/Hodge/domain/readout/projector-stress pieces remain",
            "status": "CONDITIONAL_ZERO_ROUTE_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3971_3_domain_zero_route",
            "claim_piece": "domain hidden monopole zero",
            "mathematical_form": "epsilon_domain_projector=0 if the domain selector is scalar/topological/covariant, has no marker vector/anisotropy, and does not reintroduce source labels or readout masks",
            "meaning": "domain volume/trace silence does not automatically kill preferred-frame, xi, or source-normalization leakage",
            "status": "CONDITIONAL_ZERO_ROUTE_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRI3971_4_triad_bound",
            "claim_piece": "finite triad fallback",
            "mathematical_form": "epsilon_triad_abs := |epsilon_boundary|+|Delta_PiM|+|epsilon_domain_projector|",
            "meaning": "if theorem zeros fail, the triad becomes a finite nonclaim input to epsilon_mu_extra_total and Delta_B_single_mass",
            "status": "BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_test_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZT3971_0_boundary_flux", "boundary", "B_zero_flux=0 and Delta_symp=0", "exact/improvement boundary terms have zero linked-sphere flux and fixed reference subtraction", "B_zero_flux;Delta_symp"),
        ("ZT3971_1_boundary_tensor", "boundary", "T_boundary_vector=T_boundary_TF=n.P_loc.K_boundary=0", "scalar trace alone is insufficient; vector/shear/normal exchange must vanish", "boundary_flux_vector;W_boundary_alpha3;W_boundary_xi"),
        ("ZT3971_2_boundary_derivative", "boundary", "partial_t,r,frame epsilon_boundary=0", "constant monopole is harmless only if derivative-silent and parent-fixed", "dln_mu_boundary_dt;partial_r_ln_mu_boundary;frame_derivative"),
        ("ZT3971_3_PiM_chainmap", "PiM", "[d,Pi_M]J_H=0", "PiM must be a fixed chain-map on the physical Hilbert current complex", "I_commutator"),
        ("ZT3971_4_PiM_stress", "PiM", "delta_g Pi_M=0 or T_PiM mapped below locks", "Hodge/DeWitt/domain implementations must not hide projector stress", "projector_stress_beta_equiv;T_PiM_norm"),
        ("ZT3971_5_PiM_equality", "PiM", "Pi_M J_H = J_M_top + dB_zero with R_eq=0", "topological charge must be the same object as Hilbert/source mass", "R_eq_integral;B_zero_flux"),
        ("ZT3971_6_domain_scalar", "domain", "domain selector has no vector, anisotropy, marker, or source label return", "domain trace/volume zero is not enough for alpha_i/xi/source normalization", "W_domain_alpha1;W_domain_alpha2;W_domain_alpha3;W_domain_xi"),
        ("ZT3971_7_domain_projected_mass", "domain", "d(Pi_M J_H)=0 with no domain/homology variation", "projected mass must be closed and calibrated, not a post-readout mask", "epsilon_domain_projector;domain_homology_variation"),
    ]
    return [
        {
            "test_id": test_id,
            "channel": channel,
            "zero_condition": zero_condition,
            "why_needed": why_needed,
            "finite_fallback_terms": fallback_terms,
            "current_status": "ZERO_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for test_id, channel, zero_condition, why_needed, fallback_terms in specs
    ]


def finite_input_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FIN3971_0_boundary", "epsilon_boundary", "dimensionless", "(|B_zero_flux|+|Delta_symp|+|boundary_flux_vector|)/M_H_ref", "B_zero_flux;Delta_symp;boundary_flux_vector;M_H_ref;source_file", "beta;alpha3;xi;Gdot;radial_mass"),
        ("FIN3971_1_PiM", "Delta_PiM", "dimensionless", "(|I_commutator|+|R_eq_integral|+|B_zero_flux|+|projector_stress_beta_equiv|)/M_H_ref", "I_commutator;R_eq_integral;B_zero_flux;projector_stress_beta_equiv;M_H_ref;source_file", "beta;gamma;alpha_i;xi;radial_mass"),
        ("FIN3971_2_domain", "epsilon_domain_projector", "dimensionless", "|epsilon_domain_flux|+|W_domain_alpha1 epsilon_domain_vector|+|W_domain_alpha2 epsilon_domain_vector|+|W_domain_alpha3 epsilon_domain_flux|+|W_domain_xi epsilon_domain_anisotropy|", "W_domain_alpha1;W_domain_alpha2;W_domain_alpha3;W_domain_xi;epsilon_domain_vector;epsilon_domain_flux;epsilon_domain_anisotropy;source_file", "alpha1;alpha2;alpha3;xi;beta"),
        ("FIN3971_3_triad_total", "epsilon_triad_abs", "dimensionless", "|epsilon_boundary|+|Delta_PiM|+|epsilon_domain_projector|", "FIN3971_0_boundary;FIN3971_1_PiM;FIN3971_2_domain", "epsilon_mu_extra_total;Delta_B_single_mass;delta_beta_source"),
    ]
    return [
        {
            "input_id": input_id,
            "symbol": symbol,
            "units": units,
            "formula": formula,
            "required_inputs": required_inputs,
            "observable_locks": locks,
            "current_status": "FINITE_INPUT_ROW_READY_VALUES_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, symbol, units, formula, required_inputs, locks in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "TRF3971_0_epsilon_mu_extra",
            "target": "epsilon_mu_extra_total",
            "update_formula": "epsilon_mu_extra_total <= epsilon_triad_abs + remaining_channels_abs",
            "meaning": "boundary/PiM/domain now form the first explicit block of the hidden-monopole budget",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRF3971_1_Delta_B_single_mass",
            "target": "Delta_B_single_mass",
            "update_formula": "|Delta_B_single_mass|/A_source^2 <= C_mu (epsilon_triad_abs + remaining_channels_abs)",
            "meaning": "the triad is now directly connected to the beta square-law obstruction",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRF3971_2_PPN_vector",
            "target": "Delta_PPN_source_abs",
            "update_formula": "boundary/PiM/domain feed beta, alpha1, alpha2, alpha3, xi, gamma, and radial/source-normalization channels",
            "meaning": "these are not just Newton-mass issues; they are PPN preferred-frame/location risks",
            "status": "PPN_FEED_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "TRF3971_3_next",
            "target": "boundary_reference_first",
            "update_formula": "attempt boundary B_zero_flux=Delta_symp=0 or fill epsilon_boundary first finite row",
            "meaning": "boundary is the narrowest first subchannel because the residual row already has a denominator and missing numerator terms",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3971_0_triad_written",
            "status": "BOUNDARY_PIM_DOMAIN_TRIAD_READY",
            "meaning": "the highest-leverage hidden-monopole channels are separated into zero tests and finite input rows",
            "claim_status": "symbolic_nonclaim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3971_1_no_promotion",
            "status": "ZERO_TESTS_NOT_PARENT_SIGNED",
            "meaning": "conditional lemmas exist, but none of boundary/PiM/domain is parent-owned enough to remove it from the mass/beta budget",
            "claim_status": "blocks_single_mass_beta_local_GR",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3971_2_next_boundary",
            "status": "BOUNDARY_REFERENCE_FIRST",
            "meaning": "boundary has the most concrete first finite row: epsilon_boundary_reference_abs=(|B_zero_flux|+|Delta_symp|)/M_H_ref",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3971_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3971_1_triad",
            "gate": "boundary/PiM/domain triad",
            "requirement": "all three channels have theorem-zero route or finite input row",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3971_2_zero_claim",
            "gate": "triad zero promotion",
            "requirement": "epsilon_boundary=Delta_PiM=epsilon_domain_projector=0 parent-signed",
            "status": "BLOCKED_ZERO_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3971_3_inputs",
            "gate": "finite input promotion",
            "requirement": "numeric/source-backed values, units, denominators, and weak-field maps for all nonzero triad pieces",
            "status": "INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3971_4_next",
            "gate": "next target",
            "requirement": "boundary reference no-flux zero or first finite row",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3971_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attempt boundary reference/no-flux zero first; if it fails, create the first finite epsilon_boundary row using B_zero_flux, Delta_symp, M_H_ref, units, and source path requirements",
            "success_condition": "boundary reference contribution is theorem-zero, or epsilon_boundary_reference_abs becomes a finite nonclaim input feeding epsilon_boundary and epsilon_mu_extra_total",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "BOUNDARY_PIM_DOMAIN_TRIAD_ZERO_TESTS_AND_FINITE_INPUTS_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "boundary/PiM/domain hidden-monopole channels now have explicit zero tests and finite input rows feeding epsilon_mu_extra_total and Delta_B_single_mass",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3971 - Boundary PiM Domain Monopole Zero Or Finite Inputs

Timestamp: `{timestamp}`

## Result

3971 splits the highest-leverage hidden-monopole triad:

```text
epsilon_triad_abs =
 |epsilon_boundary| + |Delta_PiM| + |epsilon_domain_projector|
```

and feeds it into:

```text
epsilon_mu_extra_total <= epsilon_triad_abs + remaining_channels_abs
|Delta_B_single_mass|/A_source^2 <= C_mu (epsilon_triad_abs + remaining_channels_abs)
```

## Why This Matters

Boundary, `Pi_M/projector`, and domain are not just mass-bookkeeping nuisances.
They also feed beta, alpha1, alpha2, alpha3, xi, gamma, radial mass closure, and source calibration.

## Decision

The next best narrow target is boundary reference/no-flux:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref
```

Either prove `B_zero_flux=Delta_symp=0`, or make this the first finite nonclaim input row.

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3971 - Boundary/PiM/Domain Hidden-Monopole Triad

- Timestamp: `{timestamp}`
- Status: `BOUNDARY_PIM_DOMAIN_TRIAD_ZERO_TESTS_AND_FINITE_INPUTS_READY`
- Triad:
  `epsilon_triad_abs = |epsilon_boundary| + |Delta_PiM| + |epsilon_domain_projector|`.
- Feed:
  `epsilon_mu_extra_total <= epsilon_triad_abs + remaining_channels_abs`.
- Claim status: nonclaim. Zero routes are conditional; finite values and source rows are missing.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3971 - Boundary/PiM/Domain Hidden-Monopole Triad"
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
        "triad": triad_rows(timestamp),
        "zero_tests": zero_test_rows(timestamp),
        "finite_inputs": finite_input_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    triad = rows["triad"]
    zero_tests = rows["zero_tests"]
    finite_inputs = rows["finite_inputs"]
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

    finite_symbols = {row["symbol"] for row in finite_inputs}
    zero_channels = {row["channel"] for row in zero_tests}

    return [
        val("VAL3971_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3971_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3971_02_triad", any(row["row_id"] == "TRI3971_0_triad_split" for row in triad), "triad split row present"),
        val("VAL3971_03_zero_routes", {"boundary", "PiM", "domain"} <= zero_channels, "zero tests cover boundary, PiM, and domain"),
        val("VAL3971_04_finite_inputs", {"epsilon_boundary", "Delta_PiM", "epsilon_domain_projector", "epsilon_triad_abs"} <= finite_symbols, "finite input rows cover triad and total"),
        val("VAL3971_05_feed", {"epsilon_mu_extra_total", "Delta_B_single_mass", "Delta_PPN_source_abs", "boundary_reference_first"} <= {row["target"] for row in feed}, "extra-monopole and PPN feed rows present"),
        val("VAL3971_06_decision", any(row["status"] == "BOUNDARY_REFERENCE_FIRST" for row in decisions), "decision selects boundary reference first"),
        val("VAL3971_07_claim_gate", any(row["status"] == "BLOCKED_ZERO_NOT_PARENT_SIGNED" for row in claims), "claim gate blocks zero promotion"),
        val("VAL3971_08_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to boundary reference zero or finite row"),
        val("VAL3971_09_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3971_10_score_ready", all(row["score_ready"] for row in finite_inputs), "finite input rows are score-ready forms"),
        val("VAL3971_11_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3971_12_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3971_13_spine_updated", SPINE_PATH.exists() and "3971 - Boundary/PiM/Domain Hidden-Monopole Triad" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3971_14_csv_parse", parsed, parse_detail),
        val("VAL3971_15_script_compile", True, "script compiled before validation write"),
        val("VAL3971_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["triad"], rows["triad"])
    write_csv(OUTPUTS["zero_tests"], rows["zero_tests"])
    write_csv(OUTPUTS["finite_inputs"], rows["finite_inputs"])
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
        raise SystemExit(f"3971 validation failed: {failed}")

    print(f"3971 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Boundary/PiM/domain triad zero tests and finite input rows assembled")


if __name__ == "__main__":
    run()
