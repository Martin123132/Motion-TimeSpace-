from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1516-Y5-parent-cR11-source-normalization-owner-or-GM-transfer-gate.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1515_validation": OUT / "P8_Y5_BRR545_1515_VALIDATION.csv",
    "1515_products": OUT / "P8_Y5_PARENT_EPSILON_1515_PRODUCT_SOURCE_PACK.csv",
    "1515_pivot": OUT / "P8_Y5_PARENT_EPSILON_1515_C_R11_PIVOT_MATRIX.csv",
    "1515_next": OUT / "P8_Y5_PARENT_EPSILON_1515_NEXT_TARGET.csv",
    "1138_canonical": OUT / "P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
    "1138_zero": OUT / "P8_Y5_R10_1138_C_ZERO_ROUTE_AUDIT.csv",
    "1148_alias": OUT / "P8_Y5_R10_1148_C_R11_ALIAS_AND_PRODUCT_LOCK.csv",
    "1148_owner": OUT / "P8_Y5_R10_1148_SOURCE_OWNER_ZERO_THEOREM_AUDIT.csv",
    "1148_channels": OUT / "P8_Y5_R10_1148_SOURCE_NORMALIZATION_CHANNEL_VECTOR.csv",
    "1148_numeric": OUT / "P8_Y5_R10_1148_C_R11_NUMERIC_SOURCE_ROUTE.csv",
    "1149_lemma": OUT / "P8_Y5_R10_1149_SOURCE_OWNER_MINIMAL_LEMMA_ATTEMPT.csv",
    "1149_product_rule": OUT / "P8_Y5_R10_1149_PROJECTED_CURRENT_PRODUCT_RULE_GUARD.csv",
    "1149_fallback": OUT / "P8_Y5_R10_1149_CHANNEL_BOUND_FALLBACK_QUEUE.csv",
    "1150_glue": OUT / "P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
    "1150_first_row": OUT / "P8_Y5_R10_1150_PIM_EQUALITY_COMMUTATOR_FIRST_ROW.csv",
    "1150_guards": OUT / "P8_Y5_R10_1150_NO_SHORTCUT_GUARDS.csv",
    "source_theorem_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "newton_stack": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
    "scorecard": OUT / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "newton_contract": OUT / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
    "current_owner": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
}

ALIAS_LOCK = OUT / "P8_Y5_PARENT_CR11_1516_ALIAS_LOCK.csv"
OWNER_AUDIT = OUT / "P8_Y5_PARENT_CR11_1516_SOURCE_OWNER_AUDIT.csv"
GM_TRANSFER_GATE = OUT / "P8_Y5_PARENT_CR11_1516_GM_TRANSFER_CHAIN_GATE.csv"
PIM_REQUIREMENTS = OUT / "P8_Y5_PARENT_CR11_1516_PIM_EQUALITY_COMMUTATOR_REQUIREMENTS.csv"
CHANNEL_LOCK = OUT / "P8_Y5_PARENT_CR11_1516_CHANNEL_VECTOR_LOCK.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_CR11_1516_REJECTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_CR11_1516_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_CR11_1516_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_CR11_1516_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1516_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1516"
QUAR_ALIAS = QUARANTINE / "CR11_ALIAS_LOCK_NONCLAIM.csv"
QUAR_OWNER = QUARANTINE / "CR11_SOURCE_OWNER_AUDIT_NONCLAIM.csv"
QUAR_GM = QUARANTINE / "CR11_GM_TRANSFER_GATE_NONCLAIM.csv"
QUAR_PIM = QUARANTINE / "PIM_EQUALITY_COMMUTATOR_REQUIREMENTS_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "CR11_DECISION_NONCLAIM.csv"
BRANCH_ALIAS = BRANCH_RESIDUALS / "cr11_alias_lock_nonclaim_1516.csv"
BRANCH_GM = BRANCH_RESIDUALS / "cr11_gm_transfer_gate_nonclaim_1516.csv"
BRANCH_PIM = BRANCH_RESIDUALS / "pim_equality_commutator_requirements_nonclaim_1516.csv"
BRANCH_DECISION_COPY = BRANCH_RESIDUALS / "cr11_decision_nonclaim_1516.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def alias_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AL1516_0_symbol",
            "c_R11_flux_alpha3",
            "c_domain_source_normalization_operator",
            "LOCKED_ALIAS_NOT_FREE_COEFFICIENT",
            "branch-specific alpha3 notation for the older R11/domain source-normalization operator",
            source_list("1515_pivot", "1148_alias", "1138_canonical"),
        ),
        (
            "AL1516_1_newton_bridge",
            "c_R11 source normalization",
            "measured-GM / Newton source-normalization residual",
            "NEWTON_FIRST_ALPHA3_SECOND",
            "closing c_R11 matters because it controls source mass calibration before alpha3 product scoring",
            source_list("1148_alias", "newton_stack"),
        ),
        (
            "AL1516_2_product_guard",
            "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
            "R11 alpha3 product",
            "PRODUCT_SHORTCUT_FORBIDDEN",
            "K, c, and epsilon must be sourced/theorem-zeroed individually unless a parent identity defines the product",
            source_list("1515_products", "1150_guards"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "alias_id": alias_id,
            "symbol": symbol,
            "canonical_object": canonical,
            "status": status,
            "meaning": meaning,
            "source_paths": sources,
            **flags(),
        }
        for alias_id, symbol, canonical, status, meaning, sources in rows
    ]


def owner_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("OWN1516_0_same_frame", "one observed coframe for matter/source/orbit/readout", "MISSING_PARENT_COFRAME_OWNER", "frame/source normalization can hide in c_R11", source_list("1148_owner", "current_owner")),
        ("OWN1516_1_constant_coupling", "constant universal source-blind coupling", "MISSING_CONSTANT_COUPLING_SUPERSELECTION", "Gdot/range/species/frame/domain dependence remains live", source_list("1148_owner", "newton_contract")),
        ("OWN1516_2_parent_charge", "measured source mass is parent Hilbert/Noether/Hamiltonian charge before fitting", "MISSING_PARENT_SOURCE_CHARGE", "measured GM remains orbital calibration rather than derived source owner", source_list("1148_owner", "1149_lemma")),
        ("OWN1516_3_flux_closure", "projected Hilbert mass current closes with full product rule", "COMMUTATOR_OBSTRUCTION_ACTIVE", "Ward conservation alone is insufficient because [d,Pi_M]J_H can leak", source_list("1149_lemma", "1149_product_rule")),
        ("OWN1516_4_mu_extra_zero", "boundary/domain/bulk/nonEH/frame/species/calibration channels have no mass projection", "MISSING_MU_EXTRA_ZERO_VECTOR", "c_R11 remains live through channel vector", source_list("1148_channels", "scorecard")),
        ("OWN1516_5_worldtube_glue", "exterior charge equals the Hilbert worldtube source mass", "MISSING_WORLDTUBE_GLUE", "closed charge can still be the wrong mass", source_list("1149_lemma", "1150_glue")),
        ("OWN1516_6_verdict", "c_R11 source-normalization owner theorem", "THEOREM_NOT_DERIVED_CURRENT_CORPUS", "no source-normalized Newton or local-GR promotion", source_list("1148_owner", "1150_glue")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "needed_statement": statement,
            "current_status": status,
            "failure_if_missing": failure,
            "source_paths": sources,
            **flags(),
        }
        for owner_id, statement, status, failure, sources in rows
    ]


def gm_transfer_rows() -> list[dict[str, Any]]:
    rows = [
        ("GM1516_0_charge", "observed-time Hamiltonian/Hilbert charge", "CONDITIONAL_NOT_PARENT_DERIVED", "H_xi or B_xi must be the same source charge used by matter", source_list("1149_lemma")),
        ("GM1516_1_pim_equality", "B_xi/G_eff = M_H[Pi_M J_H]", "MISSING_CHARGE_CURRENT_IDENTITY", "without equality, a conserved charge can be the wrong source", source_list("1149_lemma", "1150_glue")),
        ("GM1516_2_poisson", "EH/local 00 equation gives standard Poisson coefficient", "CONDITIONAL_R11_VECTOR_UNFILLED", "left-hand EH and source-normalization residuals both matter", source_list("newton_stack", "source_theorem_stack")),
        ("GM1516_3_gauss", "Gauss surface mass equals enclosed source mass with no extra projection", "NOT_DERIVED_NOT_SCORED", "volume/boundary/domain/projector/memory residuals remain unfilled", source_list("scorecard", "1148_channels")),
        ("GM1516_4_orbit", "slow orbital readout returns mu_obs = r^2|a_r| = G_eff M_source", "NOT_PARENT_DERIVED", "orbital GM cannot be used as proof of source equality", source_list("newton_contract", "1150_guards")),
        ("GM1516_5_ppn", "first-order Newton source remains stable through beta/gamma/preferred-frame order", "SECOND_ORDER_SOURCE_STABILITY_MISSING", "Newton-looking limit is not local GR until PPN source/operator residues close", source_list("newton_stack", "scorecard")),
        ("GM1516_6_verdict", "source-normalized Newton / GM transfer", "GM_TRANSFER_NOT_DERIVED_CURRENT_CORPUS", "c_R11 remains a live local-GR/Newton blocker", source_list("1515_validation", "1148_owner", "1150_glue")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "required_identity": required,
            "source_paths": sources,
            **flags(),
        }
        for gate_id, gate, status, required, sources in rows
    ]


def pim_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("PIM1516_0_R_eq", "R_eq_integral", "int_A_ext(Pi_M J_H - J_M_top - dB_zero)", "MISSING_R_EQ_INTEGRAL", "source-backed equality residual or parent equality theorem", source_list("1150_first_row")),
        ("PIM1516_1_commutator", "I_commutator", "int_A_ext [d,Pi_M]J_H", "MISSING_I_COMMUTATOR", "source-backed commutator residual or parent commutator-zero theorem", source_list("1150_first_row", "1149_product_rule")),
        ("PIM1516_2_boundary", "B_zero_flux", "int_boundary dB_zero", "MISSING_B_ZERO_FLUX", "boundary exact flux value or parent boundary-zero theorem", source_list("1150_first_row")),
        ("PIM1516_3_projector_stress", "epsilon_projector_stress", "projector_stress_beta_equiv or source-normalized T_PiM residual", "MISSING_PROJECTOR_STRESS_MAP", "stress map or theorem-zero certificate for Pi_M projector route", source_list("1150_first_row", "1150_guards")),
        ("PIM1516_4_mass_ref", "M_H_ref", "reference Hilbert source mass for normalizing residuals", "MISSING_M_H_REF", "same-frame source mass reference with units and source path", source_list("1150_first_row")),
        ("PIM1516_5_total", "epsilon_PiM_total_abs", "sum of absolute equality/commutator/boundary/stress components over M_H_ref", "FIRST_ROW_TEMPLATE_UNFILLED", "strict nonclaim runner row before any GM transfer scoring", source_list("1150_first_row", "1149_fallback")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "required_replacement": replacement,
            "source_paths": sources,
            **flags(),
        }
        for requirement_id, quantity, formula, status, replacement, sources in rows
    ]


def channel_lock_rows() -> list[dict[str, Any]]:
    channel_rows = []
    source_channels = [
        ("CH1516_0", "radial_Meff_hair", "epsilon_radial_Meff", "beta; alpha(lambda); R11"),
        ("CH1516_1", "boundary_monopole_shift", "epsilon_boundary", "beta; alpha3; xi; Gdot; R11"),
        ("CH1516_2", "domain_projector_mass", "epsilon_domain_projector / c_domain_source_normalization_operator", "alpha1; alpha2; alpha3; xi; R11"),
        ("CH1516_3", "bulk_X_Yukawa_tail", "epsilon_bulk_X", "alpha(lambda); R10; R11"),
        ("CH1516_4", "nonEH_operator_potential", "epsilon_nonEH_source", "gamma; beta; alpha(lambda); R11"),
        ("CH1516_5", "species_source_charge", "epsilon_species_A", "WEP; clocks; R11"),
        ("CH1516_6", "time_drift", "epsilon_time_drift", "Gdot; R9; R11"),
        ("CH1516_7", "absolute_calibration_offset", "epsilon_calibration", "beta; Gdot; R11"),
    ]
    for channel_id, channel, coefficient, maps_to in source_channels:
        channel_rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "channel_id": channel_id,
                "source_channel": channel,
                "coefficient_symbol": coefficient,
                "current_status": "RETAINED_OR_MISSING",
                "maps_to": maps_to,
                "source_paths": source_list("1148_channels", "scorecard"),
                **flags(),
            }
        )
    channel_rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "channel_id": "CH1516_8_verdict",
            "source_channel": "source_normalization_operator_total",
            "coefficient_symbol": "c_R11_flux_alpha3",
            "current_status": "ALL_CHANNELS_RETAINED_OR_MISSING",
            "maps_to": "Newton/measured-GM; alpha3 product; R11 ledger",
            "source_paths": source_list("1148_channels", "1515_products"),
            **flags(),
        }
    )
    return channel_rows


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1516_0_measured_GM_input", "use observed orbital GM as proof of source equality", "REJECTED", "that makes the target readout an input"),
        ("REJ1516_1_bare_mass", "identify bare rest mass with dressed gravitational source mass", "REJECTED", "binding/reference/source-map terms are the missing content"),
        ("REJ1516_2_ward_only", "use Ward conservation alone as source-owner proof", "REJECTED", "projected product rule keeps [d,Pi_M]J_H"),
        ("REJ1516_3_topology_wrong_object", "count a closed topological current as measured mass", "REJECTED", "closed wrong object can mimic success"),
        ("REJ1516_4_GM_absorption", "absorb c_R11 into fitted measured GM", "REJECTED", "derivative/vector/anisotropic/source hair cannot be hidden"),
        ("REJ1516_5_product_shortcut", "fill K*c or alpha3 products directly", "REJECTED", "factor provenance and GM transfer must close first"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1516_0_alias", "c_R11 alias lock", "LOCKED_TO_SOURCE_NORMALIZATION", "c_R11 is not a free alpha3 knob"),
        ("DEC1516_1_owner", "source-owner theorem", "NOT_DERIVED", "same-frame charge, Pi_M owner, commutator silence, mu_extra zero, and worldtube glue remain open"),
        ("DEC1516_2_gm", "GM transfer chain", "NOT_DERIVED_NOT_SCORED", "orbital GM and Newton source normalization remain conditional"),
        ("DEC1516_3_next", "PiM equality/commutator runner", "NEXT_1517_PIM_RUNNER", "strict runner prevents future equality/commutator rows becoming free knobs"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1516_0_Newton", "source-normalized Newtonian limit", "NOT_CLAIMED", "source charge to orbital GM transfer is not derived"),
        ("LOCAL1516_1_GR", "derived local GR", "NOT_CLAIMED", "Newton source normalization plus PPN source stability remain open"),
        ("LOCAL1516_2_PPN", "PPN/source residual vector", "NOT_CLAIMED", "beta/gamma/preferred-frame source residues not closed"),
        ("LOCAL1516_3_alpha3", "R11 alpha3 product", "NOT_CLAIMED", "c_R11, K, and epsilon remain unsourced/nonzero"),
        ("LOCAL1516_4_R10", "R10/source-normalization branch", "NOT_CLAIMED", "R10 scoring still lacks source-normalization transfer and real curve/kernel inputs"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1516_0_1517",
            "next_target": "1517-Y5-parent-PiM-equality-commutator-bound-runner-or-worldtube-glue-reentry.md",
            "script": "scripts/Y5_parent_PiM_equality_commutator_bound_runner_or_worldtube_glue_reentry.py",
            "objective": "build a strict nonclaim runner for R_eq_integral, I_commutator, B_zero_flux, projector_stress, M_H_ref, and epsilon_PiM_total_abs; route any future theorem evidence through the same schema before source-normalized Newton claims",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ALIAS_LOCK, QUAR_ALIAS),
        (OWNER_AUDIT, QUAR_OWNER),
        (GM_TRANSFER_GATE, QUAR_GM),
        (PIM_REQUIREMENTS, QUAR_PIM),
        (DECISION, QUAR_DECISION),
        (ALIAS_LOCK, BRANCH_ALIAS),
        (GM_TRANSFER_GATE, BRANCH_GM),
        (PIM_REQUIREMENTS, BRANCH_PIM),
        (DECISION, BRANCH_DECISION_COPY),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    modified = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= START_TS:
            modified += 1
    return modified


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    alias_data = read_csv(ALIAS_LOCK)
    owner_data = read_csv(OWNER_AUDIT)
    gm_data = read_csv(GM_TRANSFER_GATE)
    pim_data = read_csv(PIM_REQUIREMENTS)
    channel_data = read_csv(CHANNEL_LOCK)
    decision_data = read_csv(DECISION)
    next_data = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1516_0_sources", all(path.exists() for path in SOURCE_FILES.values()), "all cited 1516 input source paths exist"),
        ("VAL1516_1_alias_locked", any(row["status"] == "LOCKED_ALIAS_NOT_FREE_COEFFICIENT" for row in alias_data), "c_R11 is locked to source-normalization"),
        ("VAL1516_2_owner_not_derived", any(row["owner_id"] == "OWN1516_6_verdict" and "NOT_DERIVED" in row["current_status"] for row in owner_data), "source-owner theorem remains unproved"),
        ("VAL1516_3_gm_transfer_not_derived", any(row["gate_id"] == "GM1516_6_verdict" and "NOT_DERIVED" in row["current_status"] for row in gm_data), "GM transfer chain remains unproved"),
        ("VAL1516_4_pim_requirements_unfilled", all("MISSING" in row["current_status"] or "UNFILLED" in row["current_status"] for row in pim_data), "PiM equality/commutator runner inputs remain unfilled nonclaim rows"),
        ("VAL1516_5_channel_vector_retained", any(row["channel_id"] == "CH1516_8_verdict" and row["current_status"] == "ALL_CHANNELS_RETAINED_OR_MISSING" for row in channel_data), "source-normalization channel vector stays retained"),
        ("VAL1516_6_decision_next", any(row["result"] == "NEXT_1517_PIM_RUNNER" for row in decision_data), "decision selects PiM equality/commutator runner"),
        ("VAL1516_7_next_target", any("PiM-equality-commutator" in row["next_target"] for row in next_data), "next target is the PiM equality/commutator runner"),
        ("VAL1516_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1516 CSVs parse cleanly"),
        ("VAL1516_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        (
            "VAL1516_10_branch_copies",
            all(path.exists() for path in [QUAR_ALIAS, QUAR_OWNER, QUAR_GM, QUAR_PIM, QUAR_DECISION, BRANCH_ALIAS, BRANCH_GM, BRANCH_PIM, BRANCH_DECISION_COPY]),
            "branch/quarantine nonclaim copies written",
        ),
        ("VAL1516_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1516_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1516_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1516 locks c_R11 to source-normalization, blocks GM/Newton promotion, and selects the PiM equality/commutator runner"
            if overall
            else "1516 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    aliases: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    gm_rows: list[dict[str, Any]],
    pim_rows: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1516 - Parent c_R11 Source-Normalization Owner or GM Transfer Gate",
                "",
                "## Verdict",
                "- c_R11 is not a free alpha3 coefficient: it is locked to the source-normalization / measured-GM residual family.",
                "- The source-owner theorem is not derived: same-frame source charge, Pi_M ownership, commutator silence, mu_extra zero, worldtube glue, and PPN source stability remain open.",
                "- Therefore source-normalized Newton and local GR are not claimed; a closed current is not enough unless it is proven to be the same object as the orbital GM source.",
                "- The next best target is a strict PiM equality/commutator runner, so future theorem or numeric evidence cannot become a hidden free knob.",
                "",
                "## Alias Lock",
                md_table(aliases, ["alias_id", "symbol", "canonical_object", "status"]),
                "",
                "## Source Owner Audit",
                md_table(owners, ["owner_id", "needed_statement", "current_status", "failure_if_missing"]),
                "",
                "## GM Transfer Chain Gate",
                md_table(gm_rows, ["gate_id", "gate", "current_status", "required_identity"]),
                "",
                "## PiM Equality / Commutator Requirements",
                md_table(pim_rows, ["requirement_id", "quantity", "current_status", "required_replacement"]),
                "",
                "## Channel Vector Lock",
                md_table(channels, ["channel_id", "source_channel", "coefficient_symbol", "current_status"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    aliases = alias_rows()
    owners = owner_audit_rows()
    gm_rows = gm_transfer_rows()
    pim_rows = pim_requirement_rows()
    channels = channel_lock_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(ALIAS_LOCK, aliases)
    write_csv(OWNER_AUDIT, owners)
    write_csv(GM_TRANSFER_GATE, gm_rows)
    write_csv(PIM_REQUIREMENTS, pim_rows)
    write_csv(CHANNEL_LOCK, channels)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        ALIAS_LOCK,
        OWNER_AUDIT,
        GM_TRANSFER_GATE,
        PIM_REQUIREMENTS,
        CHANNEL_LOCK,
        REJECTION_LEDGER,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(aliases, owners, gm_rows, pim_rows, channels, rejections, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
