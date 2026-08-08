from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Y5_SOURCE_NORMALIZATION_OWNER_2583"
CHECKPOINT_ID = "2583"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2583-Y5-R2FR-Y5-source-normalization-owner-or-q_loc-R11-bound-implementation.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_NORM_2583_SOURCE_REGISTER.csv",
    "owner_audit": OUT / "P8_Y5_SOURCE_NORM_2583_OWNER_THEOREM_AUDIT.csv",
    "r11_vector": OUT / "P8_Y5_SOURCE_NORM_2583_R11_COEFFICIENT_VECTOR.csv",
    "constant_gm": OUT / "P8_Y5_SOURCE_NORM_2583_CONSTANT_GM_RESIDUAL_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_SOURCE_NORM_2583_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_NORM_2583_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_NORM_2583_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_NORM_2583_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_NORM_2583_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2583_VALIDATION.csv",
}

COPY_TARGETS = {
    "owner_audit": QUEUE / "JR2583_Y5_SOURCE_NORMALIZATION_OWNER_AUDIT_NONCLAIM.csv",
    "r11_vector": LOCAL_BOUNDS / "Y5_R11_source_normalization_vector_2583_NONCLAIM.csv",
    "constant_gm": LOCAL_BOUNDS / "Y5_constant_GM_residual_rows_2583_NONCLAIM.csv",
    "next_target": QUEUE / "JR2583_PIM_JH_FLUX_CLOSURE_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2583_00_2582_handoff",
        "source_path": ROOT / "2582-Y5-R2FR-response-doublet-GammaKhat-metric-response-or-q_loc-bound-fill.md",
        "needles": ["NEXT2582_0_selected", "OBS2582_0_Y5_even_scalar", "VAL2582_OVERALL"],
        "role": "active handoff selecting Y5 source-normalization owner or q_loc/R11 bound implementation",
    },
    {
        "source_id": "SRC2583_01_1012_Y5",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O1012_8_verdict", "Y5C1012_0_radial_Meff_hair", "V1012_SUMMARY"],
        "role": "prior Y5 source-normalization owner/bound checkpoint",
    },
    {
        "source_id": "SRC2583_02_theorem_stack",
        "source_path": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "needles": ["S0_same_frame", "S4_no_absorption_cheat", "S5_Newton_gate"],
        "role": "source-normalization theorem stack and no-absorption rule",
    },
    {
        "source_id": "SRC2583_03_r11_minimum",
        "source_path": OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "needles": ["R11SN_0_radial_Meff_hair", "R11SN_7_absolute_calibration_offset"],
        "role": "eight-channel R11 source-normalization vector",
    },
    {
        "source_id": "SRC2583_04_r11_missing",
        "source_path": OUT / "P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv",
        "needles": ["R11SN_0_radial_Meff_hair", "R11SN_7_absolute_calibration_offset"],
        "role": "missing ledger for R11 source-normalization inputs",
    },
    {
        "source_id": "SRC2583_05_r11_gates",
        "source_path": OUT / "P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
        "needles": ["G1_no_missing_for_claim", "G3_even_scalar_guard", "G5_no_promotion"],
        "role": "acceptance gates preventing fake Newton/source-normalization pass",
    },
    {
        "source_id": "SRC2583_06_constant_gm_input",
        "source_path": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "needles": ["P8_Geff_time_drift", "P8_radial_source_hair", "P8_nonlinear_beta_source_residue"],
        "role": "constant-GM residual runner input rows",
    },
    {
        "source_id": "SRC2583_07_constant_gm_matrix",
        "source_path": OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "needles": ["P8_Geff_time_drift", "P8_range_dependence", "P8_nonlinear_beta_source_residue"],
        "role": "constant-GM bound matrix and scoreability gates",
    },
    {
        "source_id": "SRC2583_08_worldtube_glue",
        "source_path": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "needles": ["W504_2_mass_charge_form", "W504_4_worldtube_source_measure_glue"],
        "role": "worldtube/source measured-mass glue clauses",
    },
    {
        "source_id": "SRC2583_09_2582_validation",
        "source_path": OUT / "P8_Y5_BRR545_2582_VALIDATION.csv",
        "needles": ["VAL2582_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def owner_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("Y5O2583_0_same_frame", "matter, clocks, source current, and orbit use one observed coframe", "S_matter[psi,e_obs] defines J_H[e_obs] and same e_obs defines rods/clocks/orbital readout", "CONDITIONAL_NOT_PARENT_DERIVED", "source normalization can hide in a frame split"),
        ("Y5O2583_1_constant_universal_coupling", "G_eff/kappa is constant, universal, and source/range/species/frame blind", "partial_t,r,A,lambda,frame G_eff = 0", "NOT_PARENT_DERIVED", "Gdot, range dependence or species source charge remains active"),
        ("Y5O2583_2_PiM_parent_origin", "Pi_M is parent-owned before readout", "Pi_M: J_H -> H^2_abs(Sigma_ext) mass-flux class with no post-fit GM mask", "NOT_PARENT_DERIVED", "measured GM can be a calibration projector"),
        ("Y5O2583_3_flux_closure", "projected Hilbert mass flux is closed in compact exterior", "d(Pi_M J_H)=0 or -Pi_M dJ_extra+[d,Pi_M]J_H+A_parent=0", "EXACT_OBSTRUCTION_NOT_ZERO", "M_eff can drift radially or temporally"),
        ("Y5O2583_4_worldtube_glue", "worldtube source measure equals exterior parent charge before orbital fitting", "M_source[W]=integral_S Q_M[tau]=M_eff", "NOT_DERIVED_CORE_MISSING_PIECE", "closed charge may be the wrong measured source"),
        ("Y5O2583_5_no_extra_mu_channels", "mu_extra channels are zero/topological or bounded", "mu_obs=G_EH M_EH + sum_i mu_i with every mu_i theorem-zero or row-scored", "RETAINED_DEBT", "extra source-normalization channels remain live"),
        ("Y5O2583_6_no_absorption_cheat", "range/time/species/radial dependence is not absorbed into measured GM", "partial_r mu_extra = partial_t mu_extra = partial_A mu_extra = partial_lambda mu_extra = 0 or residual rows stay active", "RULE_WRITTEN_NOT_SATISFIED", "single calibration can hide local physics"),
        ("Y5O2583_7_Newton_Poisson_orbit", "same charge sources Poisson/Gauss and inverse-square orbit", "nabla^2 Phi=4 pi G_ref rho_H and a_r=-G_ref M_ref/r^2", "CONDITIONAL_NOT_PARENT_DERIVED", "Newton-looking limit can be normalized after the fact"),
        ("Y5O2583_8_verdict", "measured-GM/source-normalization owner theorem", "all Y5O2583_0 through Y5O2583_7 parent-signed and no missing R11/source-normalization channels remain", "Y5_SOURCE_NORMALIZATION_OWNER_NOT_DERIVED_CURRENT_CORPUS", "Newton/local-GR remains blocked by measured-GM ownership"),
    ]
    return [
        stamp(
            {
                "audit_id": audit_id,
                "required_clause": clause,
                "mathematical_form": form,
                "current_status": status,
                "failure_if_missing": failure,
                "valid_for_claim": False,
            }
        )
        for audit_id, clause, form, status, failure in rows
    ]


def r11_vector_rows() -> list[dict[str, Any]]:
    rows = [
        ("Y5C2583_0_radial_Meff_hair", "radial_Meff_hair", "epsilon_radial_Meff", "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE", "partial_r ln(mu_obs); beta_minus_1; alpha(lambda)", "R4;R10;R11"),
        ("Y5C2583_1_boundary_monopole_shift", "boundary_monopole_shift", "epsilon_boundary", "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT", "beta_minus_1; alpha3; xi; Gdot_over_G", "R4;R7;R8;R9;R11"),
        ("Y5C2583_2_domain_projector_mass", "domain_projector_mass", "epsilon_domain_projector", "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS", "alpha1; alpha2; alpha3; xi; R11", "R5;R6;R7;R8;R11"),
        ("Y5C2583_3_bulk_X_Yukawa_tail", "bulk_X_Yukawa_tail", "epsilon_bulk_X", "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE", "alpha(lambda); R10 fifth force", "R10;R11"),
        ("Y5C2583_4_nonEH_operator_potential", "nonEH_operator_potential", "epsilon_nonEH_source", "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP", "gamma_minus_1; beta_minus_1; alpha(lambda); R11", "R3;R4;R10;R11"),
        ("Y5C2583_5_species_source_charge", "species_source_charge", "epsilon_species_A", "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR", "eta_WEP_source_charge; clock source residual", "R1;R2;R11"),
        ("Y5C2583_6_time_drift", "time_drift", "epsilon_time_drift", "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT", "Gdot_over_G", "R9;R11"),
        ("Y5C2583_7_absolute_calibration_offset", "absolute_calibration_offset", "epsilon_calibration", "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET", "beta_minus_1; Gdot_over_G", "R4;R9;R11"),
    ]
    return [
        stamp(
            {
                "coefficient_id": coefficient_id,
                "channel": channel,
                "symbol": symbol,
                "coefficient_value_or_theorem": value,
                "coefficient_units": "dimensionless_or_channel_declared",
                "observable_link": observable,
                "affected_rows": affected,
                "runner_status": "RETAINED_NONCLAIM_SOURCE_NORMALIZATION_COEFFICIENT",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for coefficient_id, channel, symbol, value, observable, affected in rows
    ]


def constant_gm_rows() -> list[dict[str, Any]]:
    rows = [
        ("GM2583_0_Geff_time_drift", "dln_Geff_dt", "Gdot_over_G", "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT", "yr^-1", "9.6e-15 yr^-1 or derived zero"),
        ("GM2583_1_Meff_conservation", "dln_Meff_dt", "beta_minus_1;Gdot_over_G", "MISSING_NUMERIC_OR_DERIVED_ZERO_MASS_FLUX", "yr^-1", "beta/Gdot locks after decomposition"),
        ("GM2583_2_species_source_charge", "eta_source_AB", "eta_WEP_source_charge", "MISSING_NUMERIC_OR_DERIVED_ZERO_SOURCE_CHARGE", "dimensionless", "2.8e-15 or derived universal source charge"),
        ("GM2583_3_radial_source_hair", "partial_r_ln_mu_obs", "gamma_minus_1;beta_minus_1;alpha(lambda)", "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO", "inverse_length_or_dimensionless_envelope", "zero radial hair or mapped PPN/fifth-force residuals"),
        ("GM2583_4_range_dependence", "alpha(lambda)", "delta_G_or_fifth_force_yukawa", "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM", "range-dependent", "verified alpha(lambda) bound curve or derived zero"),
        ("GM2583_5_frame_calibration_split", "delta_frame_source", "eta_WEP_direct_geometry;clock_redshift;operator_ledger", "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT", "dimensionless", "one observed frame or explicit residual below row locks"),
        ("GM2583_6_nonlinear_beta_source", "delta_beta_source", "beta_minus_1", "MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR", "dimensionless", "7.8e-05 or derived second-order source closure"),
    ]
    return [
        stamp(
            {
                "gm_row_id": gm_row_id,
                "symbol": symbol,
                "observable_link": observable,
                "predicted_value": predicted,
                "prediction_units": units,
                "bound_or_target": bound,
                "runner_status": "RETAINED_NONCLAIM_CONSTANT_GM_ROW",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for gm_row_id, symbol, observable, predicted, units, bound in rows
    ]


def runner_refusal_rows(r11_rows: list[dict[str, Any]], gm_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in r11_rows:
        rows.append(
            stamp(
                {
                    "runner_id": f"Y5R2583_{row['coefficient_id']}",
                    "target_id": row["coefficient_id"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": "MISSING_COEFFICIENT_VALUE_OR_THEOREM;RETAINED_UNFILLED_BLOCKS_CLAIM;VALID_FOR_CLAIM_FALSE",
                    "claim_allowed": False,
                }
            )
        )
    for row in gm_rows:
        rows.append(
            stamp(
                {
                    "runner_id": f"GMR2583_{row['gm_row_id']}",
                    "target_id": row["gm_row_id"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": "MISSING_PREDICTED_VALUE_OR_THEOREM;RETAINED_UNFILLED_BLOCKS_CLAIM;VALID_FOR_CLAIM_FALSE",
                    "claim_allowed": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2583_0_Y5_owner", "measured-GM/source-normalization owner theorem passes", "BLOCKED_NONCLAIM", "same-frame, PiM origin, flux closure, worldtube glue and extra channels remain unsigned", False),
        ("CG2583_1_R11_coefficients", "R11/source-normalization coefficient vector is claim-ready", "BLOCKED_NONCLAIM", "eight channels remain missing theorem-zero or numeric coefficient values", False),
        ("CG2583_2_constant_GM", "constant measured-GM branch is claim-ready", "BLOCKED_NONCLAIM", "Gdot, M_eff conservation, radial/range/species/frame/beta rows remain unfilled", False),
        ("CG2583_3_no_absorption", "measured-GM calibration is not hiding derivative hair", "BLOCKED_NONCLAIM", "no-absorption rule exists but required rows are not scored", False),
        ("CG2583_4_Htau_MHref_local_GR", "H_tau/M_H_ref/Newton/local-GR gates can reopen", "BLOCKED_NONCLAIM", "Y5 source-normalization remains retained residual", False),
        ("CG2583_5_bound_implementation", "Y5 bound implementation skeleton is installed", "PASS_GUARDRAIL", "owner theorem failed and all bound rows are explicit nonclaim rows", True),
        ("CG2583_6_no_shortcuts", "odd symmetry, fitted GM calibration, or single-radius normalization can prove Newton", "PASS_GUARDRAIL", "all shortcuts are refused", True),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2583_0_owner_not_proved",
            "decision": "Y5_SOURCE_NORMALIZATION_OWNER_NOT_PROVED",
            "reason": "PiM origin, flux closure, worldtube source-measure glue, universal G and eight mu_extra channels remain unsigned or unfilled",
            "effect": "no Newton/local-GR claim",
        },
        {
            "decision_id": "DEC2583_1_bound_skeleton_installed",
            "decision": "R11_AND_CONSTANT_GM_BOUND_SKELETON_RESTATED",
            "reason": "all high-pressure measured-GM rows are explicit and nonclaim instead of hidden inside calibration",
            "effect": "future tests can fill channel-by-channel",
        },
        {
            "decision_id": "DEC2583_2_root_next",
            "decision": "PIM_JH_FLUX_CLOSURE_SELECTED_NEXT",
            "reason": "without d(Pi_M J_H)=0 or a scored obstruction, measured GM cannot reduce to Newton/GR",
            "effect": "next checkpoint should derive or score -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2583_0_selected",
            "selection_status": "selected",
            "target_file": "2584-Y5-R2FR-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "target_script": "scripts/Y5_R2FR_PiM_JH_flux_closure_or_measured_GM_obstruction_score_2584.py",
            "task": "derive compact-exterior closure of d(Pi_M J_H)=0, or score the exact obstruction -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent as the measured-GM/source-normalization residual",
            "acceptance_target": "PiM/Hilbert mass flux closure is parent-signed, or obstruction terms become source-backed nonclaim residual rows with units and arena projections",
            "guardrails": "no post-readout projector; no fitted GM calibration; no odd-symmetry overclaim; no H_tau/M_H_ref/Newton/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "owner_audit": OUTPUTS["owner_audit"],
        "r11_vector": OUTPUTS["r11_vector"],
        "constant_gm": OUTPUTS["constant_gm"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2583_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2583_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2583_01_owner_theorem_blocked",
        any(row["audit_id"] == "Y5O2583_8_verdict" and row["current_status"] == "Y5_SOURCE_NORMALIZATION_OWNER_NOT_DERIVED_CURRENT_CORPUS" for row in data["owner_audit"]),
        "Y5 source-normalization owner theorem remains blocked",
    )
    add(
        "VAL2583_02_r11_vector",
        len(data["r11_vector"]) == 8 and all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["r11_vector"]),
        "eight-channel R11 vector exists and remains nonclaim",
    )
    add(
        "VAL2583_03_constant_gm_rows",
        len(data["constant_gm"]) == 7 and all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["constant_gm"]),
        "constant-GM residual rows exist and remain nonclaim",
    )
    add(
        "VAL2583_04_runner_refuses",
        all(row["claim_allowed"] is False and row["verdict"] == "REFUSED_CLAIM_RETAINED_UNFILLED" for row in data["runner_refusal"]),
        "runner refuses every unfilled R11/constant-GM row",
    )
    add(
        "VAL2583_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows Y5, R11, constant-GM, Newton or local-GR claim",
    )
    add(
        "VAL2583_06_next_target_written",
        any(row["route_id"] == "NEXT2583_0_selected" for row in data["next"]),
        "2584 PiM JH flux closure target selected",
    )
    add(
        "VAL2583_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )
    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2583-Y5-R2FR-Y5-source-normalization*",
            "*Y5_R2FR_Y5_source_normalization_owner*",
            "*P8_Y5_SOURCE_NORM_2583*",
            "*JR2583*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2583_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2583 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2583_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2583_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2583_OVERALL",
        overall,
        "2583 keeps measured-GM/source-normalization ownership blocked, restates R11 and constant-GM nonclaim rows, and selects PiM JH flux closure next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2583 Y5 R2FR Y5 Source Normalization Owner Or q_loc R11 Bound Implementation",
        "",
        "**Status:** private nonclaim derivation checkpoint. Measured-GM/source-normalization ownership is not derived.",
        "",
        "**Main result:** Y5 is the measured-source bridge. The project cannot claim Newton/GR reduction unless same-frame matter/readout, constant universal coupling, parent-owned `Pi_M`, compact-exterior flux closure, worldtube source glue, zero/bounded `mu_extra` channels, no absorption of derivative hair, and Poisson/orbital calibration close together. Current corpus has the decomposition and no-cheat gates, but not the owner theorem or filled numeric coefficient rows.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Y5 Owner Theorem Audit",
        markdown_table(data["owner_audit"], ["audit_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
        "",
        "## R11 Source-Normalization Coefficient Vector",
        markdown_table(data["r11_vector"], ["coefficient_id", "channel", "symbol", "coefficient_value_or_theorem", "coefficient_units", "observable_link", "affected_rows", "runner_status", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Constant-GM Residual Rows",
        markdown_table(data["constant_gm"], ["gm_row_id", "symbol", "observable_link", "predicted_value", "prediction_units", "bound_or_target", "runner_status", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "verdict", "failure_reasons", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    r11 = r11_vector_rows()
    gm = constant_gm_rows()
    data = {
        "sources": source_register_rows(),
        "owner_audit": owner_audit_rows(),
        "r11_vector": r11,
        "constant_gm": gm,
        "runner_refusal": runner_refusal_rows(r11, gm),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["owner_audit"], data["owner_audit"])
    write_csv(OUTPUTS["r11_vector"], data["r11_vector"])
    write_csv(OUTPUTS["constant_gm"], data["constant_gm"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2583_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
