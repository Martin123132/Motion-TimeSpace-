from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3460-Y5-R2FR-source-current-owner-for-doublet-or-Y5-source-normalization-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3460": Path(__file__).resolve(),
    "doc_3459": ROOT / "3459-Y5-R2FR-response-doublet-energy-identity-source-zero-or-q_loc-bound-under-AX1090.md",
    "energy_3459": OUT / "P8_Y5_R2FR_3459_ENERGY_IDENTITY_DERIVATION.csv",
    "bounds_3459": OUT / "P8_Y5_R2FR_3459_RESIDUAL_BOUNDS.csv",
    "source_gate_3459": OUT / "P8_Y5_R2FR_3459_SOURCE_ZERO_GATE.csv",
    "doc_1063": ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md",
    "source_forgetting_1063": OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
    "owner_audit_1063": OUT / "P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv",
    "relative_weight_1063": OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
    "relative_bound_1063": OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "ward_owner": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
    "parent_terms": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "r11_minimum": OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
    "r11_route": OUT / "P8_R11_SOURCE_NORMALIZATION_THEOREM_OR_NUMERIC_ROUTE.csv",
    "euler_source": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "source_norm_template": OUT / "P8_source_normalization_residual_vector_TEMPLATE.csv",
    "source_norm_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


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
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", "<br>").replace("|", "/"))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3460": "generator for this checkpoint",
        "doc_3459": "energy identity predecessor",
        "energy_3459": "integrated doublet identity input",
        "bounds_3459": "q_loc/amplitude bound input",
        "source_gate_3459": "source-current gate input",
        "doc_1063": "source-label forgetting predecessor",
        "source_forgetting_1063": "conditional theorem and counterexample input",
        "owner_audit_1063": "Noether/source owner audit",
        "relative_weight_1063": "relative source-weight prior matrix",
        "relative_bound_1063": "local bound anchors for relative weights",
        "ward_universality": "source-current Ward universality contract",
        "ward_owner": "Ward/source owner identity contract",
        "parent_terms": "parent action term contract for source owner",
        "r11_minimum": "R11 source-normalization operator minimum rows",
        "r11_route": "theorem/numeric/closure source-normalization route",
        "euler_source": "response-doublet source-current ledger",
        "source_norm_template": "source-normalization residual vector template",
        "source_norm_stack": "source-normalization theorem stack",
        "local_bounds": "local empirical bound anchors",
    }
    return [
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def y5_owner_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "Y5O3460_0_target",
            "statement": "The doublet source current J_A vanishes if the measured source normalization mu_obs is a label-forgotten, quotient/even Hilbert source functional before source coupling is selected.",
            "formal_condition": "mu_obs[Z,Psi] = kappa_univ * M_H[Psi,e_obs(q(Phi))] with partial_Z kappa_univ=0 and partial_Z M_H at Z=0 equal to 0",
            "consequence": "s_Y5,A := partial_ZA ln(mu_obs) evaluated at Z=0 is 0, hence the Y5 contribution to J_A is zero.",
            "current_status": "CONDITIONAL_THEOREM_SHAPE",
            "blocking_gap": "parent category has not proven label forgetting/source owner before readout",
            "source_path": str(SOURCES["source_forgetting_1063"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "Y5O3460_1_same_action_hilbert_current",
            "statement": "If the same ordinary matter action supplies both matter equations and Hilbert stress, a separate arbitrary source current is disallowed.",
            "formal_condition": "T_m^{mu nu}=2/sqrt(-g) delta S_matter/delta g_obs_mu_nu and E_Psi=delta S_matter/delta Psi",
            "consequence": "source current is not independently fitted; it is the Hilbert current of the same action.",
            "current_status": "STRONG_CONDITIONAL_LEMMA",
            "blocking_gap": "relative prefactors inside the matter/source sector still survive unless minimality/label-forgetting is signed",
            "source_path": str(SOURCES["ward_universality"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "Y5O3460_2_relative_weight_counterexample",
            "statement": "A species-labelled source functional remains covariant and additive while violating universal source normalization.",
            "formal_condition": "S_source = sum_A kappa_A S_A or E_mu_nu = sum_A kappa_A T_A, with kappa_A constant by species",
            "consequence": "s_Y5 or Delta_w_AB can survive without breaking diffeomorphism covariance, so covariance alone cannot prove J_A=0.",
            "current_status": "COUNTEREXAMPLE_SURVIVES",
            "blocking_gap": "need parent source-label forgetting or explicit relative-weight bound rows",
            "source_path": str(SOURCES["relative_weight_1063"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "Y5O3460_3_measured_G_absorption_rule",
            "statement": "Measured G can absorb only a common universal constant multiplier, not species, time, radial, range, frame, or doublet-dependent source normalization.",
            "formal_condition": "mu_obs = G_ref M_H * C0 is calibration-only if D_t C0=D_r C0=D_lambda C0=D_species C0=partial_Z C0=0",
            "consequence": "all nonconstant pieces remain physical residuals feeding J_A, R11, WEP, PPN, Gdot, or R10.",
            "current_status": "RULE_DERIVED_NOT_ZERO_PROOF",
            "blocking_gap": "derivative silence of all source-normalization channels is not parent-proven",
            "source_path": str(SOURCES["source_norm_stack"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "Y5O3460_4_verdict",
            "statement": "J_A=0 is not currently parent-derived, but the exact condition for it is now the zero of s_Y5 plus boundary and non-Hilbert source channels.",
            "formal_condition": "J_norm <= C_Y5 ||s_Y5|| + C_w ||Delta w|| + Q_nonH + Q_boundary + Q_domain + Q_range + Q_time",
            "consequence": "source-current work can plug into the 3459 amplitude bound row-by-row.",
            "current_status": "NOT_CLAIMED_BUT_BOUND_FORM_READY",
            "blocking_gap": "no numeric/source-backed s_Y5 or theorem-zero parent signature",
            "source_path": str(SOURCES["bounds_3459"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_current_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "JSD3460_0_sY5",
            "component": "measured-G/source-normalization derivative",
            "definition": "s_Y5,A := partial_ZA ln(mu_obs) evaluated at Z=0",
            "zero_route": "label-forgotten Hilbert source, constant universal coupling, no source-only species/range/time/frame slots",
            "bound_route": "source a vector or norm for s_Y5,A and multiply by response constant C_Y5",
            "feeds": "J_norm;RDB3459_0_Z_amplitude;RDB3459_1_q_loc_Hilbert_branch",
            "status": "PRIMARY_LIVE_INPUT",
            "source_path": str(SOURCES["r11_minimum"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "JSD3460_1_relative_weight",
            "component": "species-labelled relative source weight",
            "definition": "Delta_w_AB := w_A-w_B or source/test weighted analogue",
            "zero_route": "parent source functor forgets labels before source coupling",
            "bound_route": "WEP/PPN/Gdot/R10 product rows from 1063",
            "feeds": "J_norm species/source term",
            "status": "COUNTEREXAMPLE_RETAINED",
            "source_path": str(SOURCES["relative_bound_1063"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "JSD3460_2_nonHilbert_current",
            "component": "non-Hilbert or unowned source current",
            "definition": "q_nonH or source current not obtained by Hilbert variation of the same matter action",
            "zero_route": "single parent Noether current owner and no retained q_res channel",
            "bound_route": "Q_nonH retained in absolute residual vector",
            "feeds": "J_norm and source-normalization residual vector",
            "status": "OPEN_OWNER_CHANNEL",
            "source_path": str(SOURCES["ward_owner"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "JSD3460_3_boundary_domain_support",
            "component": "boundary/domain/support source leakage",
            "definition": "source work from boundary, domain projector, support shift, radial/range hair, or memory kernel",
            "zero_route": "no-flux/topological boundary plus domain/projector source silence",
            "bound_route": "Q_boundary_source + Q_domain_source + Q_range + Q_time",
            "feeds": "J_norm;B_flux separation;R11 source-normalization rows",
            "status": "OPEN_BOUNDARY_DOMAIN_CHANNEL",
            "source_path": str(SOURCES["parent_terms"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "JSD3460_4_second_order_ppn_source",
            "component": "second-order source-normalization residue",
            "definition": "delta_beta_source and gamma/beta source response after first-order measured-GM calibration",
            "zero_route": "second-order weak-field source solution in observed frame",
            "bound_route": "PPN beta/gamma source-weight response operator",
            "feeds": "local GR promotion gate after Newton source normalization",
            "status": "DEFERRED_BUT_EXPLICIT",
            "source_path": str(SOURCES["r11_minimum"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def y5_bound_plug_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "Y5B3460_0_source_work_norm",
            "quantity": "J_norm",
            "formula": "J_norm <= C_Y5 ||s_Y5|| + C_w ||Delta_w|| + Q_nonH + Q_boundary_source + Q_domain_source + Q_range + Q_time",
            "plugs_into": "RDB3459_0_Z_amplitude",
            "required_inputs": "C_Y5;s_Y5_norm;C_w;Delta_w_norm;Q_nonH;Q_boundary_source;Q_domain_source;Q_range;Q_time",
            "current_value": "MISSING_SOURCE_OWNER_OR_NUMERIC_VECTOR",
            "status": "BOUND_FORM_READY_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "Y5B3460_1_amplitude_with_Y5",
            "quantity": "||Z||",
            "formula": "||Z|| <= (J_norm + sqrt(J_norm^2 + 4 lambda_min |B_flux|))/(2 lambda_min)",
            "plugs_into": "RDB3459_0_Z_amplitude",
            "required_inputs": "lambda_min;B_flux;J_norm from Y5B3460_0",
            "current_value": "FORMULA_ONLY",
            "status": "3459_BOUND_INSTANTIATED_WITH_Y5_INPUT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "Y5B3460_2_q_loc_source_branch",
            "quantity": "Q_q_loc",
            "formula": "Q_q_loc <= N_P [C_Y5 ||s_Y5|| + C_w ||Delta_w|| + Q_nonH + Q_boundary_source + Q_domain_source + Q_range + Q_time + Q_boundary_flux] + Q_DeltaK",
            "plugs_into": "RDB3459_1_q_loc_Hilbert_branch",
            "required_inputs": "N_P;all J_norm inputs;Q_boundary_flux;Q_DeltaK;P_loc definition",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUTS",
            "status": "QLOC_BOUND_PLUGIN_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "Y5B3460_3_relative_weight_empirical_anchors",
            "quantity": "relative source-weight products",
            "formula": "WEP: |Delta_w_AB tau_WEP| <= 2.8e-15; PPN gamma/beta require response operators; Gdot/R10 require time/range maps",
            "plugs_into": "Y5B3460_0_source_work_norm",
            "required_inputs": "tau_WEP;C_gamma_source_weight;C_beta_source_weight;K_w(lambda);tau_R10;time map",
            "current_value": "ANCHORS_EXIST_PRODUCTS_MISSING",
            "status": "EMPIRICAL_ANCHOR_NOT_MTS_PREDICTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3460_0_JA_zero",
            "claim": "J_A=0 for response-doublet local branch",
            "gate_pass": False,
            "reason": "source-label forgetting and Noether current owner remain conditional; relative weight counterexample survives",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3460_1_Y5_source_normalization_zero",
            "claim": "s_Y5=0 / measured-G source normalization has no active doublet derivative",
            "gate_pass": False,
            "reason": "constant common calibration rule is written, but derivative silence of species/range/time/radial/domain channels is not parent-proven",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3460_2_bound_ready",
            "claim": "J_norm bound can be numerically plugged into 3459",
            "gate_pass": False,
            "reason": "formula is ready, but s_Y5/Delta_w/Q_nonH/source-domain inputs are missing or symbolic",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3460_3_Newton_GR_promotion",
            "claim": "Newton/local GR source coupling is derived",
            "gate_pass": False,
            "reason": "Y5 source owner is one necessary gate; PPN second-order and boundary/projector pieces also remain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3460_0_result",
            "decision": "Do not claim J_A=0. Keep the theorem route but expose s_Y5,A as the exact missing source-normalization derivative.",
            "because": "relative source weights survive covariance/additivity/same-action language unless the parent source category forgets labels before coupling selection.",
            "next_action": "Try to prove the parent source category label-forgetting/minimality clause; if not, fill s_Y5/Delta_w/Q_nonH numeric or theorem-zero rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3461-Y5-R2FR-parent-source-category-label-forgetting-or-sY5-coefficient-fill-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3461_parent_source_category_label_forgetting_or_sY5_coefficient_fill.py",
            "objective": "Attempt the actual parent-category proof that ordinary matter source coupling is label-forgotten before source selection. If it fails, fill s_Y5/Delta_w/Q_nonH source-normalization coefficient rows so 3460 can plug into the 3459 amplitude bound.",
            "success_gate": "Either s_Y5=0 is parent-derived, or Y5B3460_0 gets concrete theorem-zero/numeric component inputs with units and source paths.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_modified_count_since(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if mtime >= start_utc:
            count += 1
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["y5_owner_theorem_attempt"]
    decomposition_rows = rows_by_name["source_current_decomposition"]
    bound_rows = rows_by_name["y5_bound_plug_rows"]
    gate_rows = rows_by_name["claim_gates"]
    next_rows = rows_by_name["next_target"]

    generated_paths = [
        OUT / "P8_Y5_R2FR_3460_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3460_Y5_OWNER_THEOREM_ATTEMPT.csv",
        OUT / "P8_Y5_R2FR_3460_SOURCE_CURRENT_DECOMPOSITION.csv",
        OUT / "P8_Y5_R2FR_3460_Y5_BOUND_PLUG_ROWS.csv",
        OUT / "P8_Y5_R2FR_3460_CLAIM_GATES.csv",
        OUT / "P8_Y5_R2FR_3460_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3460_NEXT_TARGET.csv",
    ]
    csv_parse_ok = True
    csv_details: list[str] = []
    for path in generated_paths:
        try:
            parsed = read_csv(path)
            csv_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_details.append(f"{path.name}:{exc}")

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3460_0_sources_exist",
            "description": "all source paths exist",
            "passed": all(bool(row["exists"]) for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_1_theorem_or_counterexample",
            "description": "theorem attempt includes conditional zero and surviving counterexample",
            "passed": any(row["theorem_id"] == "Y5O3460_0_target" for row in theorem_rows)
            and any(row["theorem_id"] == "Y5O3460_2_relative_weight_counterexample" for row in theorem_rows),
            "detail": ";".join(row["theorem_id"] for row in theorem_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_2_sY5_component_present",
            "description": "s_Y5 source-normalization derivative is explicit",
            "passed": any(row["component_id"] == "JSD3460_0_sY5" and "partial_ZA ln(mu_obs)" in str(row["definition"]) for row in decomposition_rows),
            "detail": ";".join(row["component_id"] for row in decomposition_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_3_bound_plugs_into_3459",
            "description": "Y5 bound rows plug into 3459 amplitude/q_loc formulas",
            "passed": any(row["bound_id"] == "Y5B3460_0_source_work_norm" and "J_norm <=" in str(row["formula"]) for row in bound_rows)
            and any(row["bound_id"] == "Y5B3460_1_amplitude_with_Y5" and "lambda_min" in str(row["formula"]) for row in bound_rows),
            "detail": ";".join(row["bound_id"] for row in bound_rows),
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_4_no_claims",
            "description": "all generated gates and rows remain nonclaim",
            "passed": all(
                str(row.get("claim_allowed", "False")) == "False"
                for rows in rows_by_name.values()
                for row in rows
                if isinstance(row, dict)
            )
            and not any(bool(row["gate_pass"]) for row in gate_rows),
            "detail": "claim_allowed=false and all gates fail/open",
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_5_csv_parse",
            "description": "generated CSV files parse cleanly",
            "passed": csv_parse_ok,
            "detail": ";".join(csv_details),
        }
    )
    checks.append(
        {
            "check_id": "VAL3460_6_next_target_3461",
            "description": "next target is label-forgetting proof or sY5 coefficient fill",
            "passed": len(next_rows) == 1 and "3461-Y5-R2FR-parent-source-category-label-forgetting" in str(next_rows[0]["next_doc"]),
            "detail": str(next_rows[0]["next_doc"]) if next_rows else "missing next row",
        }
    )
    modified_count = formalization_modified_count_since(start_utc)
    checks.append(
        {
            "check_id": "VAL3460_7_formalization_untouched",
            "description": "formalization-workbench unchanged during this script",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        }
    )
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3460_8_overall",
            "description": "3460 source-current owner/Y5 checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3460 - Source-Current Owner For Doublet Or Y5 Source-Normalization Bound Under AX1090",
        "",
        "## Purpose",
        "",
        "This checkpoint attacks the `J_A=0` clause exposed by 3459. The result is a clean fork: if the parent source category forgets species labels and uses one Hilbert/Noether source owner, the Y5 source current vanishes. If not, the surviving object is the source-normalization derivative `s_Y5,A := partial_ZA ln(mu_obs)` evaluated at `Z=0`, which plugs directly into the 3459 amplitude bound.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"]),
        "",
        "## Y5 Owner Theorem Attempt",
        "",
        md_table(rows_by_name["y5_owner_theorem_attempt"]),
        "",
        "## Source Current Decomposition",
        "",
        md_table(rows_by_name["source_current_decomposition"]),
        "",
        "## Y5 Bound Plug Rows",
        "",
        md_table(rows_by_name["y5_bound_plug_rows"]),
        "",
        "## Claim Gates",
        "",
        md_table(rows_by_name["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"]),
        "",
        "## Bottom Line",
        "",
        "- Derived fork: `J_A=0` follows only from label-forgotten Hilbert source ownership; covariance/additivity alone do not kill relative source weights.",
        "- New plug-in variable: `s_Y5,A = partial_ZA ln(mu_obs)` at `Z=0` is the exact measured-G/source-normalization derivative feeding the 3459 amplitude bound.",
        "- Current status: no Newton/local-GR source-coupling claim, but the missing input is now concrete enough to prove or bound row-by-row.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "y5_owner_theorem_attempt": y5_owner_theorem_attempt(),
        "source_current_decomposition": source_current_decomposition(),
        "y5_bound_plug_rows": y5_bound_plug_rows(),
        "claim_gates": claim_gates(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    output_map = {
        "source_register": OUT / "P8_Y5_R2FR_3460_SOURCE_REGISTER.csv",
        "y5_owner_theorem_attempt": OUT / "P8_Y5_R2FR_3460_Y5_OWNER_THEOREM_ATTEMPT.csv",
        "source_current_decomposition": OUT / "P8_Y5_R2FR_3460_SOURCE_CURRENT_DECOMPOSITION.csv",
        "y5_bound_plug_rows": OUT / "P8_Y5_R2FR_3460_Y5_BOUND_PLUG_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3460_CLAIM_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3460_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3460_NEXT_TARGET.csv",
    }
    for name, path in output_map.items():
        write_csv(path, rows_by_name[name])
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUT / "P8_Y5_BRR545_3460_VALIDATION.csv", rows_by_name["validation"])
    write_doc(rows_by_name)
    print(f"wrote {DOC}")
    print("wrote 8 csv outputs")


if __name__ == "__main__":
    main()
