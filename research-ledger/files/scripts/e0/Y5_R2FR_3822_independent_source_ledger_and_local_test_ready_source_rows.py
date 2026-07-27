from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT = "3822"
BRANCH = "MTS_R2FR_Y5_INDEPENDENT_SOURCE_LEDGER_AND_LOCAL_TEST_READY_SOURCE_ROWS_3822"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3821 = PCW / "3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md"
P_3820 = PCW / "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md"
P_3819 = PCW / "3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md"
P_1013 = PCW / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"

CSV_3821_BOUNDS = OUT / "P8_Y5_R2FR_3821_PRESSURE_BINDING_BOUND_VECTOR.csv"
CSV_3821_CLASSES = OUT / "P8_Y5_R2FR_3821_CLOSED_SOURCE_CLASSIFIER.csv"
CSV_3821_RESID = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv"
CSV_3820_LEDGER = OUT / "P8_Y5_R2FR_3820_INDEPENDENT_SOURCE_LEDGER_TEMPLATE.csv"
CSV_3820_GM = OUT / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv"
CSV_3819_GM = OUT / "P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv"
CSV_1013_OBS = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
CSV_R10_PACK = OUT / "P8_Y5_PARENT_QLOC_1657_LAB_R10_SOURCE_PACK.csv"
CSV_WEP_GUARD = OUT / "P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL.csv"
CSV_CLOCK_LEDGER = OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLOCK_OBSTRUCTION_LEDGER.csv"
CSV_PPN_ORBIT = OUT / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv"
CSV_MICROSCOPE_ORBIT = OUT / "P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv"
CSV_NO_GM_ABSORB = OUT / "P8_Y5_NO_SHADOW_2513_NO_GM_ABSORB_GUARD.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3822_SOURCE_REGISTER.csv",
    "schema": OUT / "P8_Y5_R2FR_3822_SOURCE_EVIDENCE_SCHEMA.csv",
    "ledger": OUT / "P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv",
    "corrections": OUT / "P8_Y5_R2FR_3822_CORRECTION_VECTOR_ARENA_MAP.csv",
    "test_rows": OUT / "P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3822_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3822_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3822_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3822_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3822_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3822_0_3821_doc", P_3821, "Pressure/Binding Bound Vector"),
    ("SRC3822_1_3821_bounds", CSV_3821_BOUNDS, "PBV3821_5_total"),
    ("SRC3822_2_3821_classes", CSV_3821_CLASSES, "CLS3821_0_closed_stationary_lab_body"),
    ("SRC3822_3_3821_residuals", CSV_3821_RESID, "R3821_5_total"),
    ("SRC3822_4_3820_doc", P_3820, "Independent Source Ledger Template"),
    ("SRC3822_5_3820_ledger", CSV_3820_LEDGER, "LED3820_0_lab_source_mass"),
    ("SRC3822_6_3820_gm", CSV_3820_GM, "GST3820_0_product_law"),
    ("SRC3822_7_3819_doc", P_3819, "GM Anti-Circularity Contract"),
    ("SRC3822_8_3819_gm", CSV_3819_GM, "GM3819_1_independent_mass_inputs"),
    ("SRC3822_9_1013_doc", P_1013, "measured-GM obstruction"),
    ("SRC3822_10_1013_obs", CSV_1013_OBS, "OBS1013_7_calibration_PPN_tail"),
    ("SRC3822_11_R10_pack", CSV_R10_PACK, "PACK1657_0_geometry"),
    ("SRC3822_12_WEP_guard", CSV_WEP_GUARD, "WEP2556_0_hilbert_universal"),
    ("SRC3822_13_clock_ledger", CSV_CLOCK_LEDGER, "CLK2599_0_parent_clock"),
    ("SRC3822_14_PPN_orbit", CSV_PPN_ORBIT, "PVR3652_0_gamma"),
    ("SRC3822_15_MICROSCOPE_orbit", CSV_MICROSCOPE_ORBIT, "ORK1070_0_sampling_axis"),
    ("SRC3822_16_no_GM_absorb", CSV_NO_GM_ABSORB, "NAG2513_0_forbid_relative_G"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def base_row(timestamp: str) -> dict[str, str]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
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


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base_row(timestamp),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "exists": str(exists),
                "needle_found": str(needle in text),
                "source_role": "independent source ledger and local test row input",
            }
        )
    return rows


def schema_rows(timestamp: str) -> list[dict[str, str]]:
    specs = [
        ("SES3822_0_independent_source", "independent_source", "source mass/geometry/composition is supplied before and outside the tested gravitational residual", "can feed a claim only after numeric values, units, uncertainty and provenance exist"),
        ("SES3822_1_product_evidence", "product_evidence", "the observable constrains G_ref*M_H_ref or a derived product such as mu=GM", "cannot prove source normalization by itself"),
        ("SES3822_2_partial_readout", "partial_readout", "official readout/geometry/time-axis information exists but not the full parent projection kernel", "useful for smoke tests; no claim"),
        ("SES3822_3_template_only", "template_only", "allowed and forbidden source inputs are specified but values are missing", "schema-ready; no numerical claim"),
        ("SES3822_4_forbidden_as_source", "forbidden_as_source", "same observable would be used both to define the source and test the prediction", "must remain blocked"),
    ]
    return [
        {
            **base_row(timestamp),
            "schema_id": schema_id,
            "status_label": label,
            "definition": definition,
            "claim_policy": policy,
        }
        for schema_id, label, definition, policy in specs
    ]


def ledger_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "arena_id": "ARENA3822_0_R10_lab",
            "arena": "R10_short_range_lab",
            "source_class": "closed_stationary_lab_body",
            "source_evidence_status": "template_only",
            "allowed_inputs": "weighed attractor/test masses; composition/density-volume; apparatus geometry; separation profile; boundary/reference; 3821 stress-virial zero-or-bound vector",
            "forbidden_inputs": "Yukawa force fit or alpha(lambda) residual converted into source mass",
            "mass_input_policy": "independent_source_required_before_alpha_claim",
            "correction_vector": "epsilon_pressure_binding_total;epsilon_open_domain;epsilon_surface_stress;R_PiM_commutator",
            "test_use": "R10 can constrain short-range residuals only after source mass/geometry is independently supplied",
        },
        {
            "arena_id": "ARENA3822_1_WEP",
            "arena": "WEP_MICROSCOPE_lab",
            "source_class": "closed_or_orbiting_test_body_pair",
            "source_evidence_status": "partial_readout",
            "allowed_inputs": "material composition; test-body mass/inertia; official orbit/readout kernel; parent material coupling vector; stress-virial correction vector",
            "forbidden_inputs": "eta residual used to choose composition weight or source normalization",
            "mass_input_policy": "composition_source_independent_but_parent_kernel_missing",
            "correction_vector": "epsilon_pressure_binding_total;epsilon_parent_exchange;epsilon_source_weight;epsilon_pi;epsilon_ai",
            "test_use": "WEP constrains species/source universality once parent material/source kernel is fixed",
        },
        {
            "arena_id": "ARENA3822_2_PPN",
            "arena": "PPN_gamma_beta",
            "source_class": "bound_orbital_body",
            "source_evidence_status": "product_evidence",
            "allowed_inputs": "independent body model if available; density/radius/composition priors; PPN readout covariance; fixed G_ref policy",
            "forbidden_inputs": "ephemeris mu=GM used as M_H_ref for the same PPN/Newton claim",
            "mass_input_policy": "product_only_until_independent_body_mass_and_PiM_fixedness",
            "correction_vector": "epsilon_pressure_binding_total;R_mu_split;R_PiM_commutator;Delta_PPN_readout",
            "test_use": "PPN can constrain metric/readout tails but not source normalization from mu alone",
        },
        {
            "arena_id": "ARENA3822_3_clock",
            "arena": "clock_redshift_Gdot",
            "source_class": "geophysical_or_lab_clock_source",
            "source_evidence_status": "template_only",
            "allowed_inputs": "geodetic potential model; independent mass/density model; clock trajectory; tau/reference lock; boundary clock class",
            "forbidden_inputs": "clock residual used to define the same tau/source potential it tests",
            "mass_input_policy": "independent_potential_model_required",
            "correction_vector": "epsilon_covariant_frame;epsilon_boundary_ref;R_clock_tau;R_source_ledger",
            "test_use": "clock rows test tau/source stability after boundary clock ownership is fixed",
        },
        {
            "arena_id": "ARENA3822_4_orbital",
            "arena": "orbital_GM_Gauss",
            "source_class": "bound_orbital_body",
            "source_evidence_status": "product_evidence",
            "allowed_inputs": "mu_fit as product observable; independent mass model where available; PPN/orbit covariance; radial range bins",
            "forbidden_inputs": "M_H_ref=mu_fit/G_ref as source mass for Newton recovery",
            "mass_input_policy": "mu_fit_product_only",
            "correction_vector": "R_mu_split;R_GM_anti_circularity;R_PiM_commutator;epsilon_pressure_binding_total",
            "test_use": "orbital data test product consistency/range/readout tails after source mass is separately fixed",
        },
        {
            "arena_id": "ARENA3822_5_EM_stress",
            "arena": "EM_Poynting_source_stress",
            "source_class": "closed_or_open_EM_system",
            "source_evidence_status": "template_only",
            "allowed_inputs": "same-current Hilbert stress; EM field energy; Poynting flux; apparatus/support stress; total-system domain",
            "forbidden_inputs": "matter-only tube when field energy or Poynting flux has exterior support",
            "mass_input_policy": "total_Hilbert_source_required",
            "correction_vector": "epsilon_open_domain;epsilon_parent_exchange;epsilon_field;epsilon_surface_stress",
            "test_use": "EM stress can enter the same active mass only through total-domain Hilbert accounting",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def correction_rows(timestamp: str) -> list[dict[str, str]]:
    rows = []
    for arena in ledger_rows(timestamp):
        rows.append(
            {
                **base_row(timestamp),
                "map_id": arena["arena_id"].replace("ARENA", "CVM"),
                "arena": arena["arena"],
                "source_evidence_status": arena["source_evidence_status"],
                "stress_virial_vector": "epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange",
                "source_mass_vector": arena["correction_vector"],
                "no_cancellation_policy": "sum_abs components unless a theorem-zero row is source-signed",
                "claim_policy": "valid_for_claim=false until every required component is theorem-zero or numerically bounded",
            }
        )
    return rows


def test_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "test_row_id": "LTR3822_0_R10_alpha_lambda",
            "arena": "R10_short_range_lab",
            "observable_or_bound": "alpha(lambda) or force residual",
            "source_input_status": "template_only_no_numeric_source_mass_or_geometry",
            "prediction_status": "schema_ready_nonclaim",
            "must_not_use": "force residual as mass normalization",
            "ready_when": "lab source pack has masses, geometry, separation, uncertainty, stress-virial correction and Pi_M/source kernel",
        },
        {
            "test_row_id": "LTR3822_1_WEP_eta",
            "arena": "WEP_MICROSCOPE_lab",
            "observable_or_bound": "eta_AB",
            "source_input_status": "partial_readout_nonclaim",
            "prediction_status": "bound_target_ready_kernel_missing",
            "must_not_use": "eta residual to define species/source weight",
            "ready_when": "material map, orbit/readout kernel, tau/source projection and parent current owner are all fixed",
        },
        {
            "test_row_id": "LTR3822_2_PPN_gamma_beta",
            "arena": "PPN_gamma_beta",
            "observable_or_bound": "gamma_minus_1;beta_minus_1",
            "source_input_status": "product_evidence_only",
            "prediction_status": "residual_vector_ready_source_mass_missing",
            "must_not_use": "ephemeris mu as independent mass",
            "ready_when": "independent body mass/source charge and PPN readout vector are fixed",
        },
        {
            "test_row_id": "LTR3822_3_clock_tau",
            "arena": "clock_redshift_Gdot",
            "observable_or_bound": "clock redshift;Gdot-like drift",
            "source_input_status": "template_only_clock_owner_missing",
            "prediction_status": "obstruction_ledger_ready",
            "must_not_use": "clock anomaly to set tau/source potential",
            "ready_when": "boundary clock class and independent potential/source model are signed",
        },
        {
            "test_row_id": "LTR3822_4_orbital_mu",
            "arena": "orbital_GM_Gauss",
            "observable_or_bound": "mu_fit=GM;range residual;precession",
            "source_input_status": "product_evidence_only",
            "prediction_status": "anti_circularity_guard_ready",
            "must_not_use": "M_H_ref=mu_fit/G_ref",
            "ready_when": "independent source mass and Pi_M/Gauss fixedness exist before orbital comparison",
        },
        {
            "test_row_id": "LTR3822_5_EM_source_stress",
            "arena": "EM_Poynting_source_stress",
            "observable_or_bound": "field energy/Poynting stress contribution",
            "source_input_status": "template_only_total_domain_required",
            "prediction_status": "total_Hilbert_accounting_ready_nonclaim",
            "must_not_use": "matter-only support as total source when field support leaks",
            "ready_when": "same-current EM owner, total-domain closure and Poynting flux bound are signed",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in grouped["sources"])
    required_arenas = {"R10_short_range_lab", "WEP_MICROSCOPE_lab", "PPN_gamma_beta", "clock_redshift_Gdot", "orbital_GM_Gauss", "EM_Poynting_source_stress"}
    present_arenas = {row["arena"] for row in grouped["ledger"]}
    all_nonclaim = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in grouped["ledger"] + grouped["test_rows"])
    no_blank_forbidden = all(row.get("forbidden_inputs") for row in grouped["ledger"]) and all(row.get("must_not_use") for row in grouped["test_rows"])
    orbital_guard = any(row["arena"] == "orbital_GM_Gauss" and row["mass_input_policy"] == "mu_fit_product_only" for row in grouped["ledger"])
    rows = [
        ("GATE3822_0_sources", "PASS_NONCLAIM" if sources_pass else "FAIL", "all source paths and needles present" if sources_pass else "missing source path or needle"),
        ("GATE3822_1_required_arenas", "PASS_NONCLAIM" if required_arenas <= present_arenas else "FAIL", "R10/WEP/PPN/clock/orbital/EM source rows present"),
        ("GATE3822_2_no_claim_rows", "PASS_NONCLAIM" if all_nonclaim else "FAIL", "all ledger and test rows remain nonclaim"),
        ("GATE3822_3_forbidden_inputs", "PASS_GUARD" if no_blank_forbidden else "FAIL", "each row declares forbidden source-smuggling inputs"),
        ("GATE3822_4_orbital_GM_guard", "PASS_GUARD" if orbital_guard else "FAIL", "orbital mu_fit is product evidence only"),
        ("GATE3822_5_independent_source_claim", "BLOCKED_INPUT_REQUIRED", "no numeric independent source row is claim-ready"),
        ("GATE3822_6_Newton_local_GR_claim", "BLOCKED", "source ledger is test-ready but source normalization/Pi_M/PPN gates remain open"),
    ]
    return [
        {
            **base_row(timestamp),
            "gate_id": gate_id,
            "gate_status": status,
            "claim_allowed": "false",
            "detail": detail,
        }
        for gate_id, status, detail in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC3822_0_source_rows_now_test_facing",
            "decision": "Use the local arena ledger as the next empirical interface.",
            "rationale": "It separates independent source evidence from product evidence before any future fit.",
            "next_action": "populate or bound individual arena components without opening claims",
        },
        {
            "decision_id": "DEC3822_1_orbital_product_only",
            "decision": "Keep orbital GM as product evidence only.",
            "rationale": "This preserves the anti-circularity rule from 3819/3820 while keeping orbital tests useful.",
            "next_action": "derive Pi_M/Gauss fixedness or compare product residuals only",
        },
        {
            "decision_id": "DEC3822_2_next_target",
            "decision": "Move to Pi_M total fixedness and commutator zero-or-bound.",
            "rationale": "Once source rows are tagged, the largest remaining mathematical blocker is [d,Pi_M]J_H and worldtube/domain stability.",
            "next_action": "3823",
        },
    ]
    return [{**base_row(timestamp), **row} for row in rows]


def next_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "target_doc": "3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3823_PiM_total_fixedness_commutator_and_worldtube_domain_zero_or_bound.py",
            "objective": "Try to prove or bound Pi_M_total fixedness, [d,Pi_M]J_H, and source worldtube/domain stability so the 3822 arena rows can receive a real source-normalization kernel.",
            "success_gate": "Either Pi_M_total is fixed enough that the commutator/domain residuals vanish in the local branch, or each arena gets a finite PiM/worldtube residual component.",
            "avoid": "do not claim Newton/local GR; do not use orbital GM as source mass; do not edit formalization-workbench; do not use GitHub",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, str]]:
    return [
        {
            **base_row(timestamp),
            "status": "PASS_NONCLAIM_LOCAL_SOURCE_LEDGER_AND_TEST_ROWS_BUILT",
            "summary": "3822 builds local arena source-ledger rows for R10/WEP/PPN/clock/orbital/EM, carries the 3821 stress-virial correction vector into each, and keeps orbital GM as product evidence only.",
        }
    ]


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_markdown(grouped: dict[str, list[dict[str, str]]]) -> None:
    text = f"""# 3822 - Independent Source Ledger And Local Test-Ready Source Rows

## Status

`PASS_NONCLAIM_LOCAL_SOURCE_LEDGER_AND_TEST_ROWS_BUILT`

This checkpoint turns the active-mass/source-normalization branch into a test-facing ledger. It does not claim local GR or Newton. It says, arena by arena, what can be used as independent source evidence, what is only product evidence, and what input would be source-smuggling.

## Source Evidence Schema

{md_table(grouped["schema"], ["schema_id", "status_label", "definition", "claim_policy"])}

## Local Arena Source Ledger

{md_table(grouped["ledger"], ["arena_id", "arena", "source_evidence_status", "allowed_inputs", "forbidden_inputs", "mass_input_policy"])}

## Correction Vector Arena Map

{md_table(grouped["corrections"], ["map_id", "arena", "stress_virial_vector", "source_mass_vector", "no_cancellation_policy"])}

## Local Test-Ready Source Rows

{md_table(grouped["test_rows"], ["test_row_id", "arena", "observable_or_bound", "source_input_status", "prediction_status", "must_not_use"])}

## Claim Gates

{md_table(grouped["gates"], ["gate_id", "gate_status", "claim_allowed", "detail"])}

## Next Target

`3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md`

Target: prove or bound `Pi_M_total` fixedness, `[d,Pi_M]J_H`, and source worldtube/domain stability so the test-facing rows get an actual source-normalization kernel.

## Machine Outputs

{md_table(grouped["status"], ["status", "summary"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace(
        "# Local GR Coupling Spine - Current State After 3821",
        "# Local GR Coupling Spine - Current State After 3822",
    )
    paragraph = (
        "`3822` turns the active-mass/source-normalization route into a local test-facing ledger: R10, WEP/MICROSCOPE, PPN, clocks, orbital `GM`, and EM/Poynting each now carry "
        "an explicit source-evidence status, allowed independent inputs, forbidden smuggling inputs, and the shared 3821 stress-virial correction vector. The important guard is preserved: orbital `mu_fit=GM` remains product evidence only, never `M_H_ref=mu_fit/G_ref` for the same Newton/local-GR claim. "
        "This makes the next mathematical blocker sharper: `Pi_M_total` fixedness and `[d,Pi_M]J_H` must be proved zero or bounded for the arena rows.\n\n"
    )
    if "`3822` turns the active-mass/source-normalization route" not in text:
        marker = "`3821` constructs the pressure/binding closure mechanism"
        index = text.find(marker)
        if index != -1:
            line_end = text.find("\n\n", index)
            if line_end != -1:
                text = text[: line_end + 2] + paragraph + text[line_end + 2 :]
    old_target = """`3822-Y5-R2FR-independent-source-ledger-and-local-test-ready-source-rows.md`

Target: populate local test-ready source rows using independent evidence status, carry the 3821 stress-virial correction vector into R10/WEP/PPN/clock/orbital gates, and keep orbital `GM` as product evidence only.

This is the best next move because the active-mass derivation now has a closed-source pressure cancellation mechanism; the next bottleneck is test-facing source evidence and arena tagging.
"""
    new_target = """`3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md`

Target: prove or bound `Pi_M_total` fixedness, `[d,Pi_M]J_H`, and source worldtube/domain stability so the 3822 local arena rows can receive a real source-normalization kernel.

This is the best next move because the source rows are now tagged; the main remaining mathematical risk is that the projector/source domain moves with readout and reintroduces hidden `GM` calibration.
"""
    text = text.replace(old_target, new_target)
    artifacts = [
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3822_SOURCE_EVIDENCE_SCHEMA.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3822_CORRECTION_VECTOR_ARENA_MAP.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv",
        "source-intake\\mts_residuals\\P8_Y5_R2FR_3822_CLAIM_GATES.csv",
        "source-intake\\mts_residuals\\P8_Y5_BRR545_3822_VALIDATION.csv",
    ]
    insertion = "".join(f"- `{artifact}`\n" for artifact in artifacts)
    if artifacts[0] not in text:
        text = text.replace("## Machine Artifacts\n\n", "## Machine Artifacts\n\n" + insertion)
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    cache = PCW / "scripts" / "__pycache__"
    if cache.exists() and cache.is_dir():
        shutil.rmtree(cache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("sources_exist", all(row["exists"] == "True" for row in grouped["sources"]), "every cited source path exists")
    add("needles_found", all(row["needle_found"] == "True" for row in grouped["sources"]), "every cited source needle was found")
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            csv_ok = csv_ok and path.exists() and len(parse_csv(path)) > 0
        except Exception:
            csv_ok = False
    add("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse")
    add("doc_written", DOC_PATH.exists() and "Local Arena Source Ledger" in read_text(DOC_PATH), "3822 markdown document written")
    required_arenas = {"R10_short_range_lab", "WEP_MICROSCOPE_lab", "PPN_gamma_beta", "clock_redshift_Gdot", "orbital_GM_Gauss", "EM_Poynting_source_stress"}
    present_arenas = {row["arena"] for row in grouped["ledger"]}
    add("required_arenas_present", required_arenas <= present_arenas, "R10/WEP/PPN/clock/orbital/EM rows present")
    add("all_rows_nonclaim", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in grouped["ledger"] + grouped["test_rows"]), "all local rows remain nonclaim")
    add("forbidden_inputs_declared", all(row.get("forbidden_inputs") for row in grouped["ledger"]) and all(row.get("must_not_use") for row in grouped["test_rows"]), "each row declares forbidden inputs")
    add("orbital_product_only", any(row["arena"] == "orbital_GM_Gauss" and row["mass_input_policy"] == "mu_fit_product_only" for row in grouped["ledger"]), "orbital GM marked product-only")
    add("stress_vector_carried", all("epsilon" in row["stress_virial_vector"] for row in grouped["corrections"]), "3821 stress-virial vector carried into every arena")
    add("claim_gates_closed", all(row.get("claim_allowed") == "false" for row in grouped["gates"]), "no claim gate allows a claim")
    add("newton_local_gr_blocked", any(row["gate_id"] == "GATE3822_6_Newton_local_GR_claim" and row["gate_status"] == "BLOCKED" for row in grouped["gates"]), "Newton/local GR claim remains blocked")
    add("next_target_selected", grouped["next"][0]["target_doc"].startswith("3823-Y5"), "3823 PiM fixedness target selected")
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    add("spine_updated", "Current State After 3822" in spine_text and "3823-Y5-R2FR-PiM-total" in spine_text, "live spine updated to 3822 and 3823 target")
    fwb_hits = list(FWB.rglob("*3822*")) if FWB.exists() else []
    add("formalization_clean", len(fwb_hits) == 0, "no 3822 files written under formalization-workbench")
    add("pycache_removed", not (PCW / "scripts" / "__pycache__").exists(), "scripts __pycache__ removed")
    bad_chars = "\ufffd" in read_text(DOC_PATH) or "\ufffd" in read_text(Path(__file__)) or "\ufffd" in spine_text
    add("bad_chars_clean", not bad_chars, "new doc/script/spine contain no mojibake replacement characters")
    return rows


def main() -> None:
    timestamp = now_utc()
    grouped: dict[str, list[dict[str, str]]] = {}
    grouped["sources"] = source_rows(timestamp)
    grouped["schema"] = schema_rows(timestamp)
    grouped["ledger"] = ledger_rows(timestamp)
    grouped["corrections"] = correction_rows(timestamp)
    grouped["test_rows"] = test_rows(timestamp)
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["decisions"] = decision_rows(timestamp)
    grouped["next"] = next_rows(timestamp)
    grouped["status"] = status_rows(timestamp)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
