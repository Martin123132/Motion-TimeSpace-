from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_GK_FIELD_SPECIFIC_COERCIVITY_SOURCE_CHARGE_3586"
CHECKPOINT_ID = "3586"
DOC = ROOT / "3586-Y5-R2FR-field-specific-coercivity-and-source-charge-zero-or-hair-bound-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3585": RESIDUALS / "P8_Y5_R2FR_3585_NEXT_TARGET.csv",
        "status_3585": RESIDUALS / "P8_Y5_R2FR_3585_STATUS.csv",
        "theorem_3585": RESIDUALS / "P8_Y5_R2FR_3585_NO_HOMOGENEOUS_MODE_THEOREM.csv",
        "channels_3585": RESIDUALS / "P8_Y5_R2FR_3585_EXTRA_HAIR_CHANNEL_AUDIT.csv",
        "epsilon_3585": RESIDUALS / "P8_Y5_R2FR_3585_EPSILON_HAIR_BOUND_ROWS.csv",
        "gk_operator_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "gk_eligibility_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "gk_ghost_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_GHOST_TACHYON_CHECKS.csv",
        "positive_contract_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_NOHAIR_CONTRACT.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "coercivity_steps_1979": RESIDUALS / "P8_Y5_PARENT_QLOC_1979_COERCIVITY_PROOF_STEPS.csv",
        "noncoercive_2079": RESIDUALS / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
        "source_charge_contract": RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv",
        "noether_charge_2538": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
        "source_charge_owner_1793": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3586_SOURCE_REGISTER.csv",
        "gk_coercive_theorem": RESIDUALS / "P8_Y5_R2FR_3586_GK_COERCIVE_NOHAIR_THEOREM.csv",
        "source_charge_audit": RESIDUALS / "P8_Y5_R2FR_3586_GK_SOURCE_CHARGE_ZERO_AUDIT.csv",
        "hair_bound_rows": RESIDUALS / "P8_Y5_R2FR_3586_GK_HAIR_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3586_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3586_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3586_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_GK_field_specific_coercivity_source_charge_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3586_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3586 GK field-specific coercivity/source-charge theorem-or-bound input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def gk_coercive_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GKC3586_0_named_channel",
            "named coercive extra channel",
            "u_GK := (A_i, gamma), gamma=Gamma_eff-Gamma_0",
            "3586 chooses the Gamma/Khat channel because 2471 already supplies an explicit stationary quadratic operator.",
            "CHANNEL_SELECTED_FROM_3585",
            "channels_3585",
        ),
        (
            "GKC3586_1_quadratic_form",
            "stationary GK energy",
            "E_GK[u]=int[1/2 Z_A|DA|^2+1/2 m_A2|A|^2+1/2 Z_G|Dgamma|^2+1/2 m_G2 gamma^2+c_AG A.Dgamma]",
            "This is the concrete field-specific operator ansatz, not a generic extra-field placeholder.",
            "OPERATOR_FORM_IMPORTED_NONCLAIM",
            "gk_operator_2471",
        ),
        (
            "GKC3586_2_coercivity_margin",
            "GK coercivity margin",
            "lambda_GK := min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2) - |c_AG| C_cross",
            "If lambda_GK>0 in the selected domain/norm, the quadratic form controls ||A||^2+||gamma||^2.",
            "COERCIVITY_FORMULA_WRITTEN",
            "gk_coercivity_2471",
        ),
        (
            "GKC3586_3_zero_theorem",
            "GK no-hair zero theorem",
            "lambda_GK>0, J_GK=0, Phi_boundary_GK=0, Q_top_GK=0, and projector/gauge kernel fixed => u_GK=0",
            "This is the desired field-specific no-hair theorem. It is mathematically clean but not parent-activated because coefficients/source/boundary clauses are unsigned.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            "positive_contract_1846",
        ),
        (
            "GKC3586_4_finite_bound",
            "GK finite hair bound",
            "||u_GK|| <= (||J_GK||_* + sqrt(||J_GK||_*^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)",
            "If any zero premise fails but lambda_GK>0, the channel is not abandoned; it becomes an explicit finite bound.",
            "FINITE_BOUND_FORMULA_FILLED",
            "coercivity_steps_1979",
        ),
        (
            "GKC3586_5_noncoercive_fallback",
            "GK noncoercive fallback",
            "if lambda_GK<=0 or parent signs are absent, retain epsilon_GK_hair with noncoercive finite-branch inputs",
            "No coercivity, no theorem-zero. The channel stays executable as a residual rather than being smuggled away.",
            "NONCOERCIVE_BRANCH_RETAINED",
            "noncoercive_2079",
        ),
        (
            "GKC3586_6_verdict",
            "3586 GK verdict",
            "GK is bounded/sharpened but not zero-claimed: lambda_GK, J_GK, boundary flux, topology, and projector/gauge kernel are not parent-signed",
            "This is real progress because epsilon_coercive_extra now contains a named GK sub-bound with explicit operator/source/boundary ingredients.",
            "GK_CHANNEL_BOUND_FILLED_NONCLAIM",
            "status_3585",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, mathematical_form, derivation, status, source_key in rows
    ]


def source_charge_audit_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GSC3586_0_JGK_definition",
            "J_GK",
            "J_GK := (J_A, J_gamma) in L_GK u_GK = J_GK",
            "SOURCE_CURRENT_DEFINED_FOR_BOUND",
            "The no-hair theorem needs zero source charge in the same operator channel.",
            "gk_operator_2471",
        ),
        (
            "GSC3586_1_hilbert_noether_route",
            "ordinary matter does not independently source GK",
            "J_GK=0 if the ordinary matter action has no direct A_i/gamma vertex beyond common observed geometry",
            "CONDITIONAL_SOURCE_ZERO_ROUTE",
            "This is the Noether/source-charge owner route, not an empirical assumption.",
            "noether_charge_2538",
        ),
        (
            "GSC3586_2_source_charge_owner",
            "parent source-charge owner",
            "source normalization and measured mass are parent Hilbert/Hamiltonian charges before readout",
            "MISSING_PARENT_SOURCE_CHARGE_OWNER",
            "Without this, source-charge zero cannot be claim-grade.",
            "source_charge_owner_1793",
        ),
        (
            "GSC3586_3_species_source_guard",
            "no species/source-only slot",
            "ordinary matter grammar forbids source-only species multipliers that could feed J_GK",
            "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT",
            "A pre-action weight can survive Noether conservation unless parent grammar forbids it.",
            "source_charge_contract",
        ),
        (
            "GSC3586_4_boundary_improvement_guard",
            "non-Hilbert boundary/improvement currents",
            "boundary, improvement, torsion/projector, and readout currents must be zero, exact/projected silent, or finite bounded",
            "RETAIN_NONHILBERT_RESIDUALS",
            "This is the remaining source-side leakage into J_GK.",
            "noether_charge_2538",
        ),
        (
            "GSC3586_5_audit_verdict",
            "GK source charge zero",
            "J_GK=0 is conditional only; finite ||J_GK||_* row is mandatory until parent action signs the source owner",
            "SOURCE_ZERO_NOT_CLAIMED_BOUND_ROW_ACTIVE",
            "3586 can bound GK hair, but source zero is not yet derived.",
            "epsilon_3585",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "object": obj,
            "mathematical_form": mathematical_form,
            "status": status,
            "notes": notes,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for audit_id, obj, mathematical_form, status, notes, source_key in rows
    ]


def hair_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GHB3586_0_lambda_GK",
            "lambda_GK",
            "min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2) - |c_AG| C_cross",
            "MISSING_PARENT_COEFFICIENTS_AND_DOMAIN_CONSTANTS",
            "operator lower-bound coefficient",
            "positive iff GK coercivity is signed in the selected norm",
            "gk_coercivity_2471",
        ),
        (
            "GHB3586_1_J_GK_norm",
            "J_GK_norm",
            "||(J_A,J_gamma)||_*",
            "MISSING_PARENT_ZERO_OR_SOURCE_NORM",
            "dual operator norm",
            "zero iff ordinary matter carries no independent GK source charge",
            "source_charge_owner_1793",
        ),
        (
            "GHB3586_2_Phi_boundary_GK",
            "Phi_boundary_GK",
            "absolute GK boundary flux from integration by parts",
            "MISSING_BOUNDARY_ZERO_OR_FINITE_FLUX",
            "field energy flux",
            "zero iff boundary/reference/topology removes the GK boundary term",
            "positive_pack_1846",
        ),
        (
            "GHB3586_3_Q_top_GK",
            "Q_top_GK",
            "harmonic/topological/gauge-kernel GK charge not controlled by local coercivity",
            "MISSING_TOPOLOGY_PROJECTOR_KERNEL_AUDIT",
            "field norm or stress norm",
            "must be zero or bounded separately",
            "gk_eligibility_2471",
        ),
        (
            "GHB3586_4_epsilon_GK_hair",
            "epsilon_GK_hair",
            "K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]",
            "FINITE_BOUND_FORMULA_READY_VALUES_MISSING",
            "same normalization as epsilon_coercive_extra",
            "valid only if lambda_GK>0; otherwise switch to noncoercive finite branch",
            "coercivity_steps_1979",
        ),
        (
            "GHB3586_5_epsilon_coercive_extra_refined",
            "epsilon_coercive_extra",
            "epsilon_GK_hair + epsilon_bulk_memory_range_hair + remaining_named_coercive_channels",
            "REFINED_NONCLAIM",
            "same normalization as epsilon_hom_mode",
            "3586 fills the GK subchannel, not every extra sector",
            "epsilon_3585",
        ),
        (
            "GHB3586_6_epsilon_cross_hair_GK",
            "epsilon_cross_hair",
            "max(0, |c_AG|C_cross - min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2)) * ||u_GK||^2",
            "FINITE_CROSS_EXCESS_FORMULA_READY_VALUES_MISSING",
            "field energy norm",
            "cross-term instability is now a concrete excess term",
            "gk_coercivity_2471",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "status": status,
            "units": units,
            "meaning": meaning,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, status, units, meaning, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3586_0_sources", "PASS", "all source paths and selected anchors exist", "next_3585"),
        ("GATE3586_1_GK_operator_named", "PASS", "GK is a named field-specific coercive channel, not generic extra hair", "gk_operator_2471"),
        ("GATE3586_2_zero_theorem", "PASS_CONDITIONAL_THEOREM", "lambda_GK>0 plus J/boundary/topology/kernel zero implies GK hair zero", "positive_contract_1846"),
        ("GATE3586_3_bound_formula", "PASS_NONCLAIM_BOUND_FORMULA", "finite epsilon_GK_hair bound row has operator/source/boundary terms", "coercivity_steps_1979"),
        ("GATE3586_4_parent_claim", "FAIL_CURRENT_CLAIM", "coefficients, source charge zero, boundary flux, and topology/projector kernel remain unsigned", "gk_eligibility_2471"),
        ("GATE3586_5_local_GR", "FAIL_CURRENT_CLAIM", "local GR/Newton still needs remaining hair channels, E_stat, gauge/corner, GM calibration, and PPN closure", "status_3585"),
        ("GATE3586_6_no_cancellation", "PASS_GUARD", "GK hair is bounded by absolute channel terms, not cancelled against other channels", "epsilon_3585"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "GK_COERCIVE_CHANNEL_BOUND_FILLED_ZERO_THEOREM_CONDITIONAL",
            "strongest_result": "3586 turns the Gamma/Khat extra-hair channel into a concrete coercive theorem/bound: if lambda_GK>0 and J_GK, boundary flux, topology, and projector/gauge kernel vanish, then u_GK=(A,gamma)=0. If not, epsilon_GK_hair has an explicit finite formula in terms of lambda_GK, J_GK_norm, Phi_boundary_GK, and Q_top_GK.",
            "still_missing": "parent-signed GK coefficients, domain constants, source-charge zero, boundary/reference flux zero, topology/projector kernel audit, remaining extra channels, EM gauge/corner term, source coupling/GM calibration, and PPN closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3585"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3586_0",
            "target_doc": "3587-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md",
            "target_script": "scripts/Y5_R2FR_3587_GK_parent_coefficient_source_boundary_owner_or_numeric_bound_inputs.py",
            "objective": "try to source/sign the concrete GK inputs lambda_GK, J_GK_norm, Phi_boundary_GK, and Q_top_GK, or fill them as explicit finite nonclaim values/rows",
            "success_gate": "GK channel either becomes theorem-zero with parent-signed inputs or has all finite bound terms populated with units, source paths, and no MISSING markers",
            "reason": "3586 converted one extra-hair channel from vague obstruction into concrete inputs; the next useful move is to sign or fill those inputs rather than start a new vague channel",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3585": "NEXT3585_0",
        "status_3585": "NO_HOMOGENEOUS_MODE_ROUTE_CHANNELIZED_NOT_ZERO_CLAIMED",
        "theorem_3585": "NHE3585_2_coercive_extra_zero",
        "channels_3585": "CHA3585_1_GammaKhat_GK",
        "epsilon_3585": "EHB3585_1_epsilon_coercive_extra",
        "gk_operator_2471": "OP2471_0_stationary_energy",
        "gk_coercivity_2471": "COER2471_1_cross_bound",
        "gk_eligibility_2471": "NHG2471_5_eligibility",
        "gk_ghost_2471": "GT2471_4_cross",
        "positive_contract_1846": "NHC1846_2_zero_result",
        "positive_pack_1846": "OP1846_3_self_adjoint_domain",
        "coercivity_steps_1979": "PRF1979_4_coercivity",
        "noncoercive_2079": "FIN2079_0_branch_law",
        "source_charge_contract": "S6_no_connection_source_charge",
        "noether_charge_2538": "NSCI2538_5_nonhilbert_channels",
        "source_charge_owner_1793": "Y5SC1793_7_verdict",
    }
    validations.append(("VAL3586_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3586 source paths exist"))
    validations.append(("VAL3586_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3586 anchors found"))
    validations.append(("VAL3586_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3586 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3586_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3586_4_GK_named", any(row["theorem_id"] == "GKC3586_0_named_channel" for row in theorem), "GK named channel selected"))
    validations.append(("VAL3586_5_zero_theorem_present", any(row["theorem_id"] == "GKC3586_3_zero_theorem" for row in theorem), "GK conditional zero theorem present"))
    validations.append(("VAL3586_6_bound_terms_present", {"lambda_GK", "J_GK_norm", "Phi_boundary_GK", "Q_top_GK", "epsilon_GK_hair"}.issubset({str(row["symbol"]) for row in bounds}), "GK bound terms present"))
    validations.append(("VAL3586_7_source_zero_not_overclaimed", any(row["audit_id"] == "GSC3586_5_audit_verdict" and "NOT_CLAIMED" in str(row["status"]) for row in audit), "source zero remains nonclaim"))
    validations.append(("VAL3586_8_parent_claim_blocked", any(row["gate_id"] == "GATE3586_4_parent_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "parent claim remains blocked"))
    validations.append(("VAL3586_9_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorem + audit + bounds + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3586_10_next_target_selected", any(row["next_id"] == "NEXT3586_0" for row in next_target), "GK input-fill next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + audit + bounds + gates + status)
    validations.append(("VAL3586_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3586*")) or any(FORMALIZATION.rglob("3586-Y5-R2FR*"))
    validations.append(("VAL3586_12_formalization_workbench_untouched", not formalization_touched, "no 3586 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3586 — field-specific coercivity and source-charge zero or hair-bound fill",
        "",
        "## Verdict",
        "3586 takes one named extra-hair channel — `Gamma/Khat` (`u_GK=(A,gamma)`) — and turns it into a concrete theorem-or-bound object.  The conditional zero route is:",
        "",
        "`lambda_GK>0`, `J_GK=0`, `Phi_boundary_GK=0`, `Q_top_GK=0`, and projector/gauge kernel fixed imply `u_GK=0`.",
        "",
        "The nonzero route is now explicit rather than vague:",
        "",
        "`epsilon_GK_hair = K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]`.",
        "",
        "This does not prove local GR, but it materially improves the branch: one piece of `epsilon_coercive_extra` has named operator coefficients, source charge, boundary flux, and topology/projector inputs.",
        "",
        "## GK coercive theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Source-charge audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}` `{row['object']}`: {row['status']} — {row['notes']}")
    lines.extend(["", "## Hair-bound rows"])
    for row in bounds:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    theorem = gk_coercive_theorem_rows(source_paths)
    audit = source_charge_audit_rows(source_paths)
    bounds = hair_bound_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "gk_coercive_theorem": theorem,
        "source_charge_audit": audit,
        "hair_bound_rows": bounds,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, theorem, audit, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, audit, bounds, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3586 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
