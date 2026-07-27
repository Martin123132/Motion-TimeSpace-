from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_WEP_alpha_sensitivity_source_fill_or_screening_stress_test.py"
DOC_PATH = ROOT / "651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md"

STATUS = "Y5_R10_WEP_alpha_sensitivity_source_fill_stress_test_blocks_unit_source_screen_nonclaim"
CLAIM_CEILING = "WEP_alpha_sensitivity_stress_test_only_no_WEP_or_local_GR_claim"
NEXT_TARGET = "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md"

ETA_MICROSCOPE_BOUND = 2.8e-15
SCREEN_BOUND_FOR_KAPPA_ONE = 2.932961e-8

ELEMENTS = {
    "Al": {"Z": 13, "A": 27.0},
    "Ti": {"Z": 22, "A": 48.0},
    "V": {"Z": 23, "A": 51.0},
    "Rh": {"Z": 45, "A": 103.0},
    "Pt": {"Z": 78, "A": 195.0},
}

MATERIALS = {
    "PtRh10": {"Pt": 0.90, "Rh": 0.10},
    "TA6V": {"Ti": 0.90, "Al": 0.06, "V": 0.04},
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def q_alpha_coulomb(z: float, a: float) -> float:
    return 7.7e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def q_surface_binding(z: float, a: float) -> float:
    return -0.036 / (a ** (1.0 / 3.0)) - 1.4e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def material_charge(material_id: str, charge_kind: str) -> float:
    total = 0.0
    for element_id, mass_fraction in MATERIALS[material_id].items():
        element = ELEMENTS[element_id]
        if charge_kind == "Q_alpha_Coulomb":
            charge = q_alpha_coulomb(element["Z"], element["A"])
        elif charge_kind == "Q_surface_binding":
            charge = q_surface_binding(element["Z"], element["A"])
        else:
            raise ValueError(charge_kind)
        total += mass_fraction * charge
    return total


def source_register_rows() -> list[dict[str, object]]:
    local_sources = [
        ("S651_0", "checkpoint_650_doc", ROOT / "650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md", "prior cross-arena screening contract"),
        ("S651_1", "validation_650", OUT / "P8_Y5_BRR545_650_VALIDATION.csv", "prior validation"),
        ("S651_2", "screen_rule_650", OUT / "P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv", "shared screen variable owner"),
        ("S651_3", "projection_requirements_650", OUT / "P8_Y5_R10_650_ARENA_PROJECTION_REQUIREMENTS.csv", "WEP missing-projection clause"),
        ("S651_4", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "MICROSCOPE bound ledger row"),
        ("S651_5", "bound_input_ledger_645", OUT / "P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv", "WEP numeric bound source slot"),
        ("S651_6", "WEP_species_universality_371", ROOT / "371-WEP-species-universality-or-active-eta-runner.md", "prior WEP species universality no-go"),
        ("S651_7", "WEP_observed_coframe_373", ROOT / "373-one-observed-coframe-parent-selector-or-WEP-closure.md", "prior one-coframe closure contract"),
        ("S651_8", "WEP_common_F_388", ROOT / "388-WEP-species-symmetry-common-F-parent-selector-attempt.md", "prior species-blind geometry functor contract"),
        ("S651_9", "generator_script_651", SCRIPT_PATH, "this checkpoint generator"),
    ]
    rows = [
        {
            "source_id": source_id,
            "source_type": "local_path",
            "label": label,
            "path_or_url": rel(path),
            "exists_or_reachable": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in local_sources
    ]
    rows.extend(
        [
            {
                "source_id": "S651_10",
                "source_type": "web_source",
                "label": "MICROSCOPE_final_PRL_arxiv",
                "path_or_url": "https://arxiv.org/abs/2209.15487",
                "exists_or_reachable": "not_checked_by_local_validator",
                "role": "source for Ti/Pt WEP result eta(Ti,Pt) and mission final result",
                "valid_for_claim": "false",
            },
            {
                "source_id": "S651_11",
                "source_type": "web_source",
                "label": "MICROSCOPE_material_alloys",
                "path_or_url": "https://microscope3.sciencesconf.org/conference/microscope3/pages/2013_Hardy_ASR_Validation_of_the_in_flight_calibration_procedures_for_the_MICROSCOPE_space_mission_.pdf",
                "exists_or_reachable": "not_checked_by_local_validator",
                "role": "source for PtRh10 and TA6V alloy mass-fraction model",
                "valid_for_claim": "false",
            },
            {
                "source_id": "S651_12",
                "source_type": "web_source",
                "label": "Damour_Donoghue_2010_dilaton_charges",
                "path_or_url": "https://arxiv.org/abs/1007.2792",
                "exists_or_reachable": "not_checked_by_local_validator",
                "role": "source for alpha/Coulomb and nuclear-binding composition charges",
                "valid_for_claim": "false",
            },
            {
                "source_id": "S651_13",
                "source_type": "web_source",
                "label": "Damour_2012_review_two_charge_model",
                "path_or_url": "https://www.theisticscience.com/papers/tree/Gravity/Damour_2012_Class._Quantum_Grav._29_184001.pdf",
                "exists_or_reachable": "not_checked_by_local_validator",
                "role": "source for simplified Q1 prime/Q2 prime charge formulas used as a smoke estimate",
                "valid_for_claim": "false",
            },
        ]
    )
    return rows


def microscope_material_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for material_id, composition in MATERIALS.items():
        for element_id, mass_fraction in composition.items():
            element = ELEMENTS[element_id]
            rows.append(
                {
                    "material_model_id": f"MM651_{material_id}_{element_id}",
                    "material_id": material_id,
                    "experiment_role": "MICROSCOPE_Pt_reference_or_test_mass" if material_id == "PtRh10" else "MICROSCOPE_Ti_test_mass",
                    "element": element_id,
                    "mass_fraction": f"{mass_fraction:.6f}",
                    "Z": element["Z"],
                    "A_used": f"{element['A']:.1f}",
                    "composition_source": "MICROSCOPE alloy source: PtRh10=90% Pt/10% Rh, TA6V=90% Ti/6% Al/4% V",
                    "model_limit": "mass-fraction alloy average with nominal A values; not a full isotope/chemical material model",
                    "valid_for_claim": "false",
                }
            )
    return rows


def charge_estimate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for material_id in MATERIALS:
        q_e = material_charge(material_id, "Q_alpha_Coulomb")
        q_2 = material_charge(material_id, "Q_surface_binding")
        rows.append(
            {
                "charge_row_id": f"Q651_{material_id}_alpha",
                "material_id": material_id,
                "charge_kind": "Q_alpha_Coulomb",
                "formula": "Q1_prime = 7.7e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged",
                "charge_value": f"{q_e:.12e}",
                "source": "Damour-Donoghue alpha/Coulomb dilaton charge smoke formula",
                "claim_grade": "source_backed_smoke_estimate_not_full_material_model",
                "valid_for_claim": "false",
            }
        )
        rows.append(
            {
                "charge_row_id": f"Q651_{material_id}_surface",
                "material_id": material_id,
                "charge_kind": "Q_surface_binding",
                "formula": "Q2_prime = -0.036/A^(1/3)-1.4e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged",
                "charge_value": f"{q_2:.12e}",
                "source": "Damour-Donoghue simplified nuclear surface/Coulomb smoke formula",
                "claim_grade": "source_backed_smoke_estimate_not_full_material_model",
                "valid_for_claim": "false",
            }
        )
    for charge_kind, label in [("Q_alpha_Coulomb", "alpha_Coulomb"), ("Q_surface_binding", "surface_binding")]:
        delta = material_charge("TA6V", charge_kind) - material_charge("PtRh10", charge_kind)
        rows.append(
            {
                "charge_row_id": f"Q651_delta_TA6V_minus_PtRh10_{label}",
                "material_id": "TA6V_minus_PtRh10",
                "charge_kind": f"Delta_{charge_kind}",
                "formula": "Delta Q = Q(TA6V)-Q(PtRh10)",
                "charge_value": f"{delta:.12e}",
                "source": "computed from source-backed alloy smoke model",
                "claim_grade": "stress_test_only",
                "valid_for_claim": "false",
            }
        )
    return rows


def WEP_alpha_stress_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    stress_inputs = [
        ("WAS651_0_alpha_Coulomb", "Q_alpha_Coulomb", "alpha/Coulomb composition channel"),
        ("WAS651_1_surface_binding", "Q_surface_binding", "nuclear surface/binding composition channel"),
    ]
    for stress_id, charge_kind, channel in stress_inputs:
        delta_q = abs(material_charge("TA6V", charge_kind) - material_charge("PtRh10", charge_kind))
        eta_unit_source = delta_q * SCREEN_BOUND_FOR_KAPPA_ONE
        overshoot = eta_unit_source / ETA_MICROSCOPE_BOUND
        beta_required = ETA_MICROSCOPE_BOUND / eta_unit_source
        rows.append(
            {
                "stress_id": stress_id,
                "channel": channel,
                "eta_bound_used": f"{ETA_MICROSCOPE_BOUND:.6e}",
                "shared_screen_used": "S_lab_alpha from 650",
                "assumed_abs_kappa_alpha": "1",
                "delta_Q_TA6V_minus_PtRh10_abs": f"{delta_q:.12e}",
                "unit_source_eta_prediction": f"{eta_unit_source:.12e}",
                "overshoot_factor_vs_MICROSCOPE": f"{overshoot:.6e}",
                "required_abs_beta_source_max": f"{beta_required:.12e}",
                "verdict": "unit_source_fails_requires_source_normalization_or_zero_theorem",
                "score_ready": "false",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "stress_id": "WAS651_2_clock_screen_only",
            "channel": "cross-arena rule diagnostic",
            "eta_bound_used": f"{ETA_MICROSCOPE_BOUND:.6e}",
            "shared_screen_used": "S_lab_alpha from 650",
            "assumed_abs_kappa_alpha": "1",
            "delta_Q_TA6V_minus_PtRh10_abs": "not_applicable",
            "unit_source_eta_prediction": "not_applicable",
            "overshoot_factor_vs_MICROSCOPE": "not_applicable",
            "required_abs_beta_source_max": "not_applicable",
            "verdict": "clock_screen_alone_is_not_a_WEP_pass_because_force_source_normalization_is_independent",
            "score_ready": "false",
            "valid_for_claim": "false",
        }
    )
    return rows


def screening_option_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "WG651_0_common_geometry_zero",
            "route": "prove species-blind geometry / common observed coframe",
            "condition": "parent action forces all matter to one ehat and forbids F_A(C_D), m_A(C_D), alpha_A(C_D)",
            "current_result": "conditional_only_from_373_388",
            "WEP_result_if_closed": "direct composition alpha channel zero",
            "status": "best_derivation_route_not_yet_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WG651_1_source_normalization_bound",
            "route": "derive small beta_source for local Earth/Test-mass force",
            "condition": "beta_source_alpha <= about 5e-5 for alpha/Coulomb unit-kappa stress row, or stronger if surface channel included",
            "current_result": "not_derived",
            "WEP_result_if_closed": "finite alpha branch can survive WEP without a zero theorem",
            "status": "numeric_target_written",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WG651_2_same_screen_only",
            "route": "use clock screen S_lab_alpha with no source-normalization theorem",
            "condition": "eta_AB = Delta Q * S_lab_alpha for unit source",
            "current_result": "fails_by_four_orders_in_smoke_estimate",
            "WEP_result_if_closed": "not_applicable",
            "status": "rejected_as_claim_route",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WG651_3_arena_specific_WEP_screen",
            "route": "invent S_WEP different from S_clock",
            "condition": "S_WEP << S_clock without parent domain reason",
            "current_result": "forbidden_by_650_no_special_pleading",
            "WEP_result_if_closed": "invalid",
            "status": "policy_fail",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D651_0",
            "route": "WEP_alpha_sensitivity_source_fill",
            "decision": "source_backed_smoke_estimate_written",
            "why": "MICROSCOPE materials and Damour-Donoghue charges give a nonzero Ti/Pt alpha-composition lever arm",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D651_1",
            "route": "clock_screen_only",
            "decision": "rejected_as_WEP_claim_route",
            "why": "with unit source normalization the shared clock screen still overshoots MICROSCOPE by about four orders",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D651_2",
            "route": "best_next_theorem",
            "decision": "derive_source_normalization_or_common_geometry_zero",
            "why": "WEP now needs either beta_source suppression, species-blind one-coframe theorem, or alpha channel absence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC651_0",
            "next_target": NEXT_TARGET,
            "work_item": "Try to prove a common-geometry zero theorem for the WEP alpha/composition channel.",
            "acceptance_condition": "parent action forbids species-dependent F_A, m_A, alpha_A and leaves one observed coframe for all matter",
        },
        {
            "contract_id": "NC651_1",
            "next_target": NEXT_TARGET,
            "work_item": "If zero theorem fails, derive or source beta_source_alpha for Earth/test-mass force normalization.",
            "acceptance_condition": "beta_source_alpha is parent-derived/source-backed and below the numeric target written in 651",
        },
        {
            "contract_id": "NC651_2",
            "next_target": NEXT_TARGET,
            "work_item": "Upgrade the alloy smoke estimate only if exact isotope/material charge data are needed.",
            "acceptance_condition": "full material model replaces nominal A mass-fraction averaging before any claim",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    delta_qe = abs(material_charge("TA6V", "Q_alpha_Coulomb") - material_charge("PtRh10", "Q_alpha_Coulomb"))
    eta_qe = delta_qe * SCREEN_BOUND_FOR_KAPPA_ONE
    beta_qe = ETA_MICROSCOPE_BOUND / eta_qe
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "MICROSCOPE_eta_bound": f"{ETA_MICROSCOPE_BOUND:.3e}",
            "shared_screen_kappa_one": f"{SCREEN_BOUND_FOR_KAPPA_ONE:.3e}",
            "delta_Q_alpha_Coulomb_abs": f"{delta_qe:.3e}",
            "unit_source_eta_alpha_Coulomb": f"{eta_qe:.3e}",
            "required_beta_source_alpha_max": f"{beta_qe:.3e}",
            "WEP_claim": "false",
            "hardest_blocker": "source-force normalization beta_source or common-geometry zero theorem is missing",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    material_rows: list[dict[str, object]],
    charge_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    local_sources = [row for row in source_rows if row["source_type"] == "local_path"]
    checks.append(("V651_0_local_source_paths_exist", all(row["exists_or_reachable"] == "true" for row in local_sources), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_650_VALIDATION.csv")
    checks.append(("V651_1_prior_650_validation_clean", all(row.get("result") == "pass" for row in prior), "650 validation remains clean"))
    material_sums = {
        material_id: sum(float(row["mass_fraction"]) for row in material_rows if row["material_id"] == material_id)
        for material_id in MATERIALS
    }
    checks.append(("V651_2_material_fractions_sum_to_one", all(abs(total - 1.0) < 1e-9 for total in material_sums.values()), f"material fraction sums: {material_sums}"))
    delta_rows = [row for row in charge_rows if row["material_id"] == "TA6V_minus_PtRh10"]
    checks.append(("V651_3_delta_charges_nonzero", len(delta_rows) == 2 and all(abs(float(row["charge_value"])) > 1e-3 for row in delta_rows), "Ti/Pt alpha and surface charge differences are nonzero at smoke level"))
    unit_rows = [row for row in stress_rows if row["stress_id"] in {"WAS651_0_alpha_Coulomb", "WAS651_1_surface_binding"}]
    checks.append(("V651_4_unit_source_overshoots", all(float(row["overshoot_factor_vs_MICROSCOPE"]) > 1e4 for row in unit_rows), "unit-source WEP smoke overshoots MICROSCOPE by more than four orders"))
    checks.append(("V651_5_beta_target_written", any(float(row["required_abs_beta_source_max"]) < 5e-5 for row in unit_rows), "source-normalization target below 5e-5 is written"))
    checks.append(("V651_6_clock_screen_not_WEP_pass", any(row["stress_id"] == "WAS651_2_clock_screen_only" and "not_a_WEP_pass" in row["verdict"] for row in stress_rows), "clock screen alone is explicitly not a WEP pass"))
    checks.append(("V651_7_zero_and_bound_routes_present", any(row["gate_id"] == "WG651_0_common_geometry_zero" for row in gate_rows) and any(row["gate_id"] == "WG651_1_source_normalization_bound" for row in gate_rows), "zero theorem and source-bound routes are both present"))
    checks.append(("V651_8_arena_specific_screen_forbidden", any(row["gate_id"] == "WG651_3_arena_specific_WEP_screen" and row["status"] == "policy_fail" for row in gate_rows), "arena-specific WEP screen is forbidden"))
    checks.append(("V651_9_all_rows_nonclaim", all(row.get("valid_for_claim") == "false" for group in [source_rows, material_rows, charge_rows, stress_rows, gate_rows, decision] for row in group), "all output rows remain nonclaim"))
    checks.append(("V651_10_decision_selects_652", all(row["next_target"] == NEXT_TARGET for row in decision + next_rows), "decision and next contract point to 652"))
    checks.append(("V651_11_summary_blocks_WEP_claim", summary[0]["WEP_claim"] == "false" and float(summary[0]["required_beta_source_alpha_max"]) < 5e-5, "summary blocks WEP claim and records beta target"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V651_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    material_rows: list[dict[str, object]],
    charge_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 651 Y5/R10 WEP Alpha-Sensitivity Source Fill or Screening Stress Test",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The MICROSCOPE Ti/Pt WEP row is now connected to a source-backed smoke model for alpha/Coulomb and nuclear-binding composition charges.",
        "- The result is not a WEP pass: the shared clock screen alone is not enough if the WEP force source normalization is order unity.",
        f"- With `|kappa_alpha|=1`, `S_lab_alpha={SCREEN_BOUND_FOR_KAPPA_ONE:.3e}`, and unit source normalization, the alpha/Coulomb row predicts `eta~5.84e-11`, far above `2.8e-15`.",
        "- Therefore the finite-alpha branch needs either a parent-derived common-geometry zero theorem or a source-normalization suppression target of order `beta_source_alpha <= 5e-5` in this smoke model.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "source_type", "label", "path_or_url", "exists_or_reachable", "role"]),
        "",
        "## MICROSCOPE Material Model",
        "",
        markdown_table(material_rows, ["material_model_id", "material_id", "element", "mass_fraction", "Z", "A_used", "model_limit"]),
        "",
        "## Damour-Donoghue Charge Estimate",
        "",
        markdown_table(charge_rows, ["charge_row_id", "material_id", "charge_kind", "formula", "charge_value", "claim_grade"]),
        "",
        "## WEP Alpha Stress Test",
        "",
        markdown_table(stress_rows, ["stress_id", "channel", "eta_bound_used", "shared_screen_used", "delta_Q_TA6V_minus_PtRh10_abs", "unit_source_eta_prediction", "overshoot_factor_vs_MICROSCOPE", "required_abs_beta_source_max", "verdict"]),
        "",
        "## Screening Option Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "route", "condition", "current_result", "WEP_result_if_closed", "status"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "decision", "why", "next_target"]),
        "",
        "## Next Contract",
        "",
        markdown_table(next_rows, ["contract_id", "work_item", "acceptance_condition"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is not fatal, but it is properly sharp: WEP is saying `do not confuse local time-drift screening with force-source suppression`.",
        "- The cleanest survival route is still the derivation route: one observed coframe, species-blind geometry, no species-dependent alpha or mass class functions.",
        "- If that theorem fails, the finite-alpha branch needs a real source-normalization derivation, not another phenomenological knob.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "MICROSCOPE_eta_bound", "shared_screen_kappa_one", "delta_Q_alpha_Coulomb_abs", "unit_source_eta_alpha_Coulomb", "required_beta_source_alpha_max", "WEP_claim", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    material_rows = microscope_material_rows()
    charge_rows = charge_estimate_rows()
    stress_rows = WEP_alpha_stress_rows()
    gate_rows = screening_option_gate_rows()
    decision = decision_rows()
    next_rows = next_contract_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, material_rows, charge_rows, stress_rows, gate_rows, decision, next_rows, summary)

    write_csv(OUT / "P8_Y5_R10_651_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv", material_rows)
    write_csv(OUT / "P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv", charge_rows)
    write_csv(OUT / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv", stress_rows)
    write_csv(OUT / "P8_Y5_R10_651_SCREENING_OPTION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_651_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_651_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_R10_651_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_651_VALIDATION.csv", validation)
    write_doc(source_rows, material_rows, charge_rows, stress_rows, gate_rows, decision, next_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"unit_source_alpha_eta={summary[0]['unit_source_eta_alpha_Coulomb']}")
    print(f"required_beta_source_alpha_max={summary[0]['required_beta_source_alpha_max']}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
