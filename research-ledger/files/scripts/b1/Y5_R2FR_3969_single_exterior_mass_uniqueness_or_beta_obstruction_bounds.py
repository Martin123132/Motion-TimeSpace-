from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3969"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3969-Y5-R2FR-single-exterior-mass-uniqueness-or-beta-obstruction-bounds.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3969_SOURCE_REGISTER.csv",
    "uniqueness": SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv",
    "hypotheses": SRC / "P8_Y5_R2FR_3969_UNIQUENESS_HYPOTHESIS_GATE.csv",
    "bounds": SRC / "P8_Y5_R2FR_3969_BETA_OBSTRUCTION_BOUND_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3969_DELTA_B_SQUARE_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3969_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3969_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3969_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3969_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3969_VALIDATION.csv",
}

NEXT_DOC = "3970-Y5-R2FR-no-extra-exterior-monopole-hair-or-channel-bound-vector.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3970_no_extra_exterior_monopole_hair_or_channel_bound_vector.py"


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
        ("SRC3969_00_3968_next", SRC / "P8_Y5_R2FR_3968_NEXT_TARGET.csv", "NEXT3968_0", "3968 handoff"),
        ("SRC3969_01_3968_square", SRC / "P8_Y5_R2FR_3968_SINGLE_MASS_SQUARE_LAW_THEOREM.csv", "SQL3968_1_single_mass_exterior_proposition", "single-mass square law"),
        ("SRC3969_02_3968_premises", SRC / "P8_Y5_R2FR_3968_PARENT_PREMISE_TESTS.csv", "PREM3968_1_single_monopole", "single monopole premise"),
        ("SRC3969_03_3968_obstructions", SRC / "P8_Y5_R2FR_3968_BETA_SQUARE_LAW_OBSTRUCTION_VECTOR.csv", "OBS3968_0_single_mass", "single-mass obstruction"),
        ("SRC3969_04_3968_feed", SRC / "P8_Y5_R2FR_3968_BETA_VECTOR_FEED_UPDATE.csv", "BFEED3968_1_delta_beta_source", "delta beta feed"),
        ("SRC3969_05_eh_mass", SRC / "P8_Y5_EH_MASS_PARAMETER_THEOREM.csv", "EH528_1_AB_square_from_mass_parameter", "EH mass parameter theorem"),
        ("SRC3969_06_eh_nohair", SRC / "P8_Y5_EH_NOHAIR_THEOREM_TARGETS.csv", "EHNH530_4_measured_mass_lock", "EH no-hair mass lock"),
        ("SRC3969_07_eh_uniqueness", SRC / "P8_Y5_EH_UNIQUENESS_2484_THEOREM_ATTEMPT.csv", "THM2484_0_conditional_uniqueness_statement", "conditional EH uniqueness"),
        ("SRC3969_08_eh_hyp", SRC / "P8_Y5_EH_UNIQUENESS_2484_HYPOTHESIS_AUDIT.csv", "HYP2484_3_no_extra_local_tensors", "no extra local tensors"),
        ("SRC3969_09_eh_blockers", SRC / "P8_Y5_EH_UNIQUENESS_2484_PARENT_NORMAL_FORM_BLOCKERS.csv", "NFB2484_6_residual_budget", "normal-form residual budget"),
        ("SRC3969_10_eh_residual", SRC / "P8_Y5_EH_UNIQUENESS_2484_RESIDUAL_UPDATE.csv", "ERES2484_3_DeltaE_MTS", "DeltaE residual"),
        ("SRC3969_11_eh_claims", SRC / "P8_Y5_EH_UNIQUENESS_2484_CLAIM_GATES.csv", "GATE2484_4_Newton_local_GR", "EH claim gate"),
        ("SRC3969_12_stationary", SRC / "P8_Y5_STATIONARY_SOURCE_2468_EXTERIOR_QLOC_RESULT.csv", "EXT2468_0_stationary_q_zero", "stationary exterior q zero"),
        ("SRC3969_13_worldtube", SRC / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_8_weak_field_readout_after_charge_glue", "worldtube weak-field readout"),
        ("SRC3969_14_hamiltonian", SRC / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv", "HSM541_5_Gauss_orbital_readout", "Hamiltonian source measure contract"),
        ("SRC3969_15_extra_mass", SRC / "P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv", "EM522_3_silence_theorem", "extra mass silence theorem"),
        ("SRC3969_16_extra_bounds", SRC / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv", "EX522_6_projector_stress", "extra mass bound inputs"),
        ("SRC3969_17_flux", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "no extra mass channel theorem"),
        ("SRC3969_18_flux_residual", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv", "SMR509_7_Delta_PPN", "source measure flux residual map"),
        ("SRC3969_19_hilbert_contract", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM7_second_order_source_stability", "Hilbert second-order source stability"),
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


def uniqueness_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "UQ3969_0_target",
            "claim_piece": "single exterior mass uniqueness",
            "mathematical_form": "Exterior[g_obs] = EH vacuum/SdS monopole family with one charge mu plus separately subtracted background",
            "derivation": "this is the missing parent-owned premise needed by 3968 to promote B_source=A_source^2 from conditional pattern to MTS route",
            "status": "TARGET_EXACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UQ3969_1_conditional_uniqueness_theorem",
            "claim_piece": "EH exterior uniqueness",
            "mathematical_form": "If DeltaE_munu=0, T_ext=0, no extra local tensors, fixed boundary class, and one asymptotic/time generator, then exterior solution has one monopole mu",
            "derivation": "conditional Birkhoff/Schwarzschild/SdS logic: local EH vacuum constraints leave mass and background constants, not independent source charges",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UQ3969_2_square_law_corollary",
            "claim_piece": "beta square-law inheritance",
            "mathematical_form": "g00=-1+2mu/(rho c^2)-2mu^2/(rho^2 c^4)+O(c^-6), mu=A_source mu0 => B_source=A_source^2",
            "derivation": "one exterior mass parameter forces the quadratic coefficient to be the square of the linear coefficient in observed isotropic PPN readout",
            "status": "DERIVED_CONDITIONAL_COROLLARY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UQ3969_3_background_guard",
            "claim_piece": "local background subtraction",
            "mathematical_form": "Lambda/tidal/domain background terms are not beta U^2 and must be fixed, subtracted, or mapped to xi/tidal residuals",
            "derivation": "without this guard a background curvature term could be mistaken for source nonlinear response",
            "status": "POLICY_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UQ3969_4_not_current_MTS_claim",
            "claim_piece": "parent-signature limit",
            "mathematical_form": "MTS must sign EH dominance, no-hair, worldtube charge glue, same readout, and no extra monopole before uniqueness becomes a claim",
            "derivation": "the proof is a valid route, but current corpus still retains live obstruction channels",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def hypothesis_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("HYP3969_0_public_metric", "one observed metric/coframe owns local gravity and PPN readout", "g_obs is parent public geometry through O(U^2)", "partial_unsigned", "Delta_B_readout"),
        ("HYP3969_1_EH_operator", "exterior operator is EH/SdS after residual silence", "DeltaE_munu=0 or below local PPN/R10/clocks/orbits locks", "conditional_open", "Delta_B_operator"),
        ("HYP3969_2_vacuum_exterior", "compact source-free collar has no ordinary or hidden source current", "T_H=0 and q_loc=0 and J_extra=0 outside worldtube", "conditional_open", "Delta_B_q_loc;Delta_B_single_mass"),
        ("HYP3969_3_no_extra_monopoles", "no independent scalar/vector/projector/domain/boundary/memory/range 1/r charge", "mu_extra=0 channelwise, not by cancellation", "not_signed", "Delta_B_single_mass"),
        ("HYP3969_4_fixed_boundary_reference", "boundary/reference/corner/falloff class fixed before readout", "Delta_symp=Delta_boundary=0 or finite-bounded", "not_signed", "Delta_B_boundary_domain"),
        ("HYP3969_5_worldtube_charge_glue", "Hamiltonian/Hilbert/Gauss mass are the same charge", "B_xi/G_eff=M_eff[Pi_M J_H]=mu_ext/G_eff", "not_signed", "Delta_B_PiM;Delta_cal"),
        ("HYP3969_6_same_readout", "observed isotropic PPN coordinate/readout is fixed before beta extraction", "no post-variation U or mass redefinition at O(U^2)", "not_signed", "Delta_B_readout"),
        ("HYP3969_7_constant_coupling", "kappa_MTS, ell_J, and source scale do not drift by source/range/frame/time", "partial kappa and source-current scale derivatives vanish", "not_signed", "Delta_B_coupling"),
    ]
    return [
        {
            "hypothesis_id": hypothesis_id,
            "hypothesis": hypothesis,
            "required_identity": identity,
            "current_status": status,
            "failure_feeds": feeds,
            "effect_if_all_pass": "single exterior mass uniqueness signs B_source=A_source^2 route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for hypothesis_id, hypothesis, identity, status, feeds in specs
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BND3969_0_extra_monopole", "Delta_mu_extra_over_mu", "hidden exterior monopole charge", "|Delta_B_single_mass|/A_source^2 <= C_mu |Delta_mu_extra/mu|", "extra mass channelwise bound rows or no-hair theorem", "beta_minus_1<=7.8e-05;gamma_minus_1<=2.3e-05;alpha(lambda) locks"),
        ("BND3969_1_operator_tail", "DeltaE_U2", "non-EH operator U^2 coefficient", "|Delta_B_operator|/A_source^2 <= C_EH ||DeltaE_U2||", "R11/EH operator coefficient map", "beta_minus_1<=7.8e-05"),
        ("BND3969_2_boundary_charge", "Delta_boundary_U2", "boundary/reference U^2 monopole or flux", "|Delta_B_boundary_domain|/A_source^2 <= C_B |Delta_boundary_U2|", "boundary no-flux theorem or finite flux row", "beta;alpha3;xi"),
        ("BND3969_3_projector_measure", "Delta_PiM_U2", "Pi_M variation/source-measure quadratic tail", "|Delta_B_PiM|/A_source^2 <= C_PiM |Delta_PiM_U2|", "Pi_M chain-map and projector stress row", "beta;alpha_i;xi"),
        ("BND3969_4_q_loc_second_order", "q_loc_U2", "local projection current at second order", "|Delta_B_q_loc|/A_source^2 <= C_q ||q_loc_U2||", "second-order Ward zero or q_loc beta projection", "beta;alpha3;zeta_i"),
        ("BND3969_5_readout_gauge", "Delta_readout_U2", "readout/coframe/gauge U^2 transfer", "|Delta_B_readout|/A_source^2 <= C_R |Delta_readout_U2|", "fixed-before-readout theorem through O(U^2)", "beta;gamma;clocks"),
        ("BND3969_6_coupling_scale", "Delta_kappa_ellJ_U2", "coupling/source-current scale second-order drift", "|Delta_B_coupling|/A_source^2 <= C_k(|delta_kappa_U2|+|delta_ellJ_U2|)", "constant coupling/source-current scale theorem", "beta;Gdot;source-charge"),
        ("BND3969_7_total", "Delta_B_square_abs", "absolute beta obstruction envelope", "|delta_beta_source| <= sum_i |Delta_B_i|/|A_source|^2", "all channel rows theorem-zero or finite sourced", "beta_minus_1<=7.8e-05"),
    ]
    return [
        {
            "bound_id": bound_id,
            "symbol": symbol,
            "meaning": meaning,
            "bound_law": law,
            "required_input": required_input,
            "observable_locks": locks,
            "current_status": "BOUND_FORM_ONLY_INPUTS_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, symbol, meaning, law, required_input, locks in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "UFEED3969_0_single_mass",
            "target": "Delta_B_single_mass",
            "update_formula": "Delta_B_single_mass=0 if HYP3969_0..7 pass; otherwise |Delta_B_single_mass| is bounded by extra-monopole/operator/boundary/projector/readout/coupling rows",
            "meaning": "single-mass uniqueness is now a hypothesis-gated theorem, not a vibe",
            "status": "CONDITIONAL_THEOREM_OR_BOUND_FORM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UFEED3969_1_Delta_B_square",
            "target": "Delta_B_square",
            "update_formula": "Delta_B_square_abs <= |Delta_B_single_mass|+|Delta_B_operator|+|Delta_B_source_prefactor|+|Delta_B_q_loc|+|Delta_B_PiM|+|Delta_B_boundary_domain|+|Delta_B_readout|+|Delta_B_coupling|",
            "meaning": "3968 obstruction vector now has a uniqueness proof branch and first bound laws",
            "status": "SYMBOLIC_BOUND_FEED_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UFEED3969_2_beta_source",
            "target": "delta_beta_source",
            "update_formula": "delta_beta_source=0 if single-mass theorem passes; else |delta_beta_source| <= Delta_B_square_abs/|A_source|^2",
            "meaning": "beta source residual becomes zero-by-theorem or finite-by-bound",
            "status": "EXACT_BRANCH_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "UFEED3969_3_next",
            "target": "no_extra_exterior_monopole",
            "update_formula": "prove mu_extra=0 channelwise or fill Delta_mu_extra_over_mu bound rows",
            "meaning": "the best next target is killing hidden exterior monopole hair, because that is the central single-mass hypothesis",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3969_0_conditional_uniqueness_route",
            "status": "SINGLE_MASS_UNIQUENESS_AVAILABLE_CONDITIONALLY",
            "meaning": "EH/SdS exterior uniqueness gives the exact mass-parameter route needed by 3968",
            "claim_status": "conditional_not_parent_signed",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3969_1_current_gap",
            "status": "NO_EXTRA_MONOPOLE_HAIR_NOT_SIGNED",
            "meaning": "the central remaining MTS-owned proof is channelwise absence of hidden exterior monopole hair",
            "claim_status": "blocks_beta_and_local_GR_claim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3969_2_bound_fallback",
            "status": "BETA_OBSTRUCTION_BOUND_FORMS_READY",
            "meaning": "if no-hair uniqueness fails, each obstruction has a bound-form row feeding Delta_B_square_abs",
            "claim_status": "nonclaim_until_numeric_or_theorem_zero",
            "next_action": "fill channel rows with theorem zeros or sourced coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3969_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3969_1_uniqueness_theorem",
            "gate": "single exterior mass uniqueness",
            "requirement": "EH exterior, one parent-owned monopole, no extra charges, fixed boundary/readout/coupling",
            "status": "CONDITIONAL_PROOF_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3969_2_bound_rows",
            "gate": "beta obstruction bounds",
            "requirement": "each obstruction has theorem-zero or finite sourced input",
            "status": "BOUND_FORMS_ONLY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3969_3_beta_local_GR",
            "gate": "beta/local-GR promotion",
            "requirement": "single-mass theorem passes or Delta_B_square_abs/A^2 below beta lock, plus other PPN vector gates",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3969_4_next_target",
            "gate": "next proof target",
            "requirement": "prove no-extra-exterior-monopole hair or fill channel bound vector",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3969_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive channelwise no-extra-exterior-monopole hair for boundary/domain/bulk-memory/nonEH/coupling/frame/PiM/anomaly sectors, or create finite bound rows for Delta_mu_extra_over_mu",
            "success_condition": "mu_extra=0 is theorem-signed channelwise, or hidden monopole hair has finite nonclaim rows feeding Delta_B_single_mass and Delta_B_square_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "SINGLE_EXTERIOR_MASS_UNIQUENESS_CONDITIONAL_AND_BOUND_FORMS_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "conditional single-mass uniqueness theorem assembled; current MTS claim blocked by no-extra-monopole and parent-signature gaps; beta obstruction bound laws written",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3969 - Single Exterior Mass Uniqueness Or Beta Obstruction Bounds

Timestamp: `{timestamp}`

## Result

3969 sharpens the 3968 square-law route.

The conditional theorem is:

```text
EH/SdS exterior + compact source-free collar + no extra local tensors
+ fixed boundary/reference + one observed readout + one parent-owned monopole
=> exterior metric has one mass parameter mu
=> g00=-1+2mu/(rho c^2)-2mu^2/(rho^2 c^4)+O(c^-6)
=> B_source=A_source^2
=> delta_beta_source=0
```

That is a real route to beta, but it is not yet an MTS claim.
The MTS-owned task is now narrower: prove that no hidden exterior monopole hair survives.

## Bound Fallback

If uniqueness does not close, beta receives:

```text
|delta_beta_source| <= Delta_B_square_abs / |A_source|^2
Delta_B_square_abs <= sum_i |Delta_B_i|
```

where the active obstruction channels are extra monopole charge, non-EH operator tail, boundary/reference flux, PiM/projector variation, q_loc second order, readout/coframe transfer, and coupling/source-scale drift.

## Source Intake

Source needles found: `{found}/{len(sources)}`.

## Decision

Next target: channelwise no-extra-exterior-monopole hair, or finite hidden-monopole bound rows.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3969 - Single Exterior Mass Uniqueness

- Timestamp: `{timestamp}`
- Status: `SINGLE_EXTERIOR_MASS_UNIQUENESS_CONDITIONAL_AND_BOUND_FORMS_READY`
- Conditional theorem:
  EH/SdS exterior with one parent-owned monopole gives one mass parameter `mu`, hence `B_source=A_source^2` and `delta_beta_source=0`.
- Current claim status: nonclaim. MTS still must parent-sign no extra exterior monopole hair, EH dominance, worldtube/Gauss charge glue, fixed readout, fixed boundary/reference, and fixed coupling/source scale.
- Bound fallback:
  `|delta_beta_source| <= Delta_B_square_abs/|A_source|^2`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3969 - Single Exterior Mass Uniqueness"
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
        "uniqueness": uniqueness_rows(timestamp),
        "hypotheses": hypothesis_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    uniqueness = rows["uniqueness"]
    hypotheses = rows["hypotheses"]
    bounds = rows["bounds"]
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

    hypothesis_ids = {row["hypothesis_id"] for row in hypotheses}
    bound_symbols = {row["symbol"] for row in bounds}

    return [
        val("VAL3969_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3969_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3969_02_uniqueness_theorem", any(row["row_id"] == "UQ3969_1_conditional_uniqueness_theorem" for row in uniqueness), "conditional single-mass uniqueness theorem row present"),
        val("VAL3969_03_square_corollary", any(row["row_id"] == "UQ3969_2_square_law_corollary" and "B_source=A_source^2" in row["mathematical_form"] for row in uniqueness), "square-law corollary present"),
        val("VAL3969_04_not_parent_signed", any(row["status"] == "CONDITIONAL_NOT_PARENT_SIGNED" for row in uniqueness), "claim-limiting conditional row present"),
        val("VAL3969_05_hypotheses", {"HYP3969_3_no_extra_monopoles", "HYP3969_5_worldtube_charge_glue", "HYP3969_7_constant_coupling"} <= hypothesis_ids, "key uniqueness hypotheses present"),
        val("VAL3969_06_bound_rows", {"Delta_mu_extra_over_mu", "DeltaE_U2", "Delta_boundary_U2", "Delta_PiM_U2", "q_loc_U2", "Delta_readout_U2", "Delta_kappa_ellJ_U2", "Delta_B_square_abs"} <= bound_symbols, "beta obstruction bound rows complete"),
        val("VAL3969_07_feed", {"Delta_B_single_mass", "Delta_B_square", "delta_beta_source", "no_extra_exterior_monopole"} <= {row["target"] for row in feed}, "Delta_B and beta feed rows present"),
        val("VAL3969_08_decision", any(row["status"] == "NO_EXTRA_MONOPOLE_HAIR_NOT_SIGNED" for row in decisions), "decision selects no-extra-monopole hair next"),
        val("VAL3969_09_claim_gate", any(row["status"] == "BLOCKED_NONCLAIM" for row in claims), "claim gate blocks beta/local-GR promotion"),
        val("VAL3969_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to no-extra exterior monopole hair or bound vector"),
        val("VAL3969_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3969_12_score_ready", all(row["score_ready"] for row in bounds), "bound rows are score-ready forms"),
        val("VAL3969_13_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3969_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3969_15_spine_updated", SPINE_PATH.exists() and "3969 - Single Exterior Mass Uniqueness" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3969_16_csv_parse", parsed, parse_detail),
        val("VAL3969_17_script_compile", True, "script compiled before validation write"),
        val("VAL3969_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["uniqueness"], rows["uniqueness"])
    write_csv(OUTPUTS["hypotheses"], rows["hypotheses"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
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
        raise SystemExit(f"3969 validation failed: {failed}")

    print(f"3969 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Single-exterior-mass uniqueness theorem and beta obstruction bound rows assembled")


if __name__ == "__main__":
    run()
