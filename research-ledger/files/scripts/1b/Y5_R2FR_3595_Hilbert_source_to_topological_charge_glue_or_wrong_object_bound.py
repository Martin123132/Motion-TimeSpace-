from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3595"
BRANCH_ID = "MTS_R2FR_Y5_HILBERT_TO_TOPOLOGICAL_CHARGE_GLUE_3595"
DOC = ROOT / "3595-Y5-R2FR-Hilbert-source-to-topological-charge-glue-or-wrong-object-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3594": (RESIDUALS / "P8_Y5_R2FR_3594_NEXT_TARGET.csv", "NEXT3594_0"),
        "status_3594": (
            RESIDUALS / "P8_Y5_R2FR_3594_STATUS.csv",
            "FIXED_TOPOLOGICAL_PIM_STRESS_ZERO_CONDITIONAL_SOURCE_EQUALITY_BLOCKED",
        ),
        "residual_3594": (
            RESIDUALS / "P8_Y5_R2FR_3594_EPSILON_PIM_RESIDUAL_UPDATE.csv",
            "epsilon_PiM_parent",
        ),
        "theorem_3594": (
            RESIDUALS / "P8_Y5_R2FR_3594_FIXED_TOPOLOGICAL_PIM_THEOREM_ATTEMPT.csv",
            "FTP3594_5_wrong_object_obstruction",
        ),
        "validation_3594": (RESIDUALS / "P8_Y5_BRR545_3594_VALIDATION.csv", "VAL3594_13_formalization_workbench_untouched"),
        "top_hilbert_attempt": (RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv", "EH501_0_equality_statement"),
        "top_hilbert_obstructions": (
            RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
            "OB501_0_independent_topological_label",
        ),
        "top_hilbert_decision": (RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv", "D501_1_best_route"),
        "parent_noether": (RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv", "T505_source_measure_matching"),
        "parent_noether_chain": (RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv", "D505_6_worldtube_readout"),
        "source_measure_theorem": (RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_0_charge_identity_needed"),
        "source_measure_residuals": (RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv", "SMR509_1_Delta_PiM"),
        "worldtube_theorem": (RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure"),
        "worldtube_proof": (RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv", "P510_5"),
        "worldtube_decision": (RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_DECISION.csv", "D510_2"),
        "parent_source_identity": (RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv", "I499_3_parent_source_identity"),
        "parent_source_residuals": (
            RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
            "S499_6_frame_species_source",
        ),
        "charge_residuals": (RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv", "Delta_PiM"),
        "charge_direct": (RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv", "CC7_closed_flux_and_Gauss_calibration"),
        "em_hodge_bound": (RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_7_Delta_PiM_metric"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3595_SOURCE_REGISTER.csv",
        "glue_theorem": RESIDUALS / "P8_Y5_R2FR_3595_HILBERT_TO_TOPOLOGICAL_GLUE_THEOREM.csv",
        "wrong_object_residuals": RESIDUALS / "P8_Y5_R2FR_3595_WRONG_OBJECT_RESIDUAL_DECOMPOSITION.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3595_EPSILON_PIM_PARENT_WRONG_OBJECT_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3595_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3595_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3595_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Hilbert_topological_charge_glue_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3595_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def glue_theorem_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "HGT3595_0_target",
            "3595 target",
            "Prove Pi_M J_H = J_M_top + dB_zero, or retain epsilon_PiM_parent as a wrong-object residual.",
            "3594 conditionally killed metric/domain projector stress, leaving Hilbert/source equality as the dominant source-coupling obstruction.",
            "TARGET_IMPORTED",
            "next_3594",
        ),
        (
            "HGT3595_1_deRham_decomposition",
            "fixed exterior cohomology decomposition",
            "For a closed Hilbert mass 2-current J_M on E with H^2(E)=R[S2], J_M = ell_M(J_M) omega_M_top + dB + R_perp.",
            "This is the exact mathematical bridge: the topological representative is legal if the non-mass cohomology R_perp is zero and the exact piece has zero relevant boundary flux.",
            "CONDITIONAL_THEOREM_DERIVED",
            "top_hilbert_attempt",
        ),
        (
            "HGT3595_2_QM_not_independent",
            "charge scalar must be Hilbert-defined",
            "Q_M := ell_M(Pi_M J_H) := integral_S Pi_M J_H := M_source[W] before orbital readout.",
            "If Q_M is an independent topological label, dJ_M_top=0 proves closure of the wrong object, not Newtonian source mass.",
            "MAIN_NO_CHEAT_CONDITION",
            "top_hilbert_obstructions",
        ),
        (
            "HGT3595_3_zero_boundary_exact_term",
            "exact term must be harmless",
            "Pi_M J_H - J_M_top = dB_zero and integral_boundary dB_zero = 0.",
            "The exact remainder is allowed only if it has no compact linking-surface flux or is a universal derivative-silent reference constant.",
            "CONDITIONAL_BOUNDARY_ZERO",
            "top_hilbert_obstructions",
        ),
        (
            "HGT3595_4_worldtube_dressed_source",
            "dressed source measure",
            "M_source[W] := H_tau[S_outer] - H_tau[reference], not bare rest mass.",
            "The source charge measured by gravity must already include binding, field, boundary, and EM/Poynting dressing owned by the parent charge.",
            "NECESSARY_DEFINITION_LOCK",
            "worldtube_theorem",
        ),
        (
            "HGT3595_5_em_poynting_once",
            "Hilbert source includes EM/Poynting once",
            "J_H_total = J_matter + J_EM + J_Poynting + J_binding, with no hidden double count.",
            "A topological equality that silently drops EM stress would be a source-coupling cheat.",
            "RETAINED_EXPLICIT_GUARD",
            "em_hodge_bound",
        ),
        (
            "HGT3595_6_conditional_glue_theorem",
            "Hilbert-to-topological glue theorem",
            "If d(Pi_M J_H)=0, H^2(E)=R[S2], Q_M=ell_M(Pi_M J_H)=M_source[W], R_perp=0, integral_boundary dB_zero=0, and EM/Poynting are included once, then Pi_M J_H = J_M_top + dB_zero and epsilon_PiM_parent=0.",
            "This is a real route to the source-coupling proof, but every premise must be parent-owned before public/local-GR credit.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "parent_noether",
        ),
        (
            "HGT3595_7_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the theorem form but not the parent-owned worldtube/source-measure lock; epsilon_wrong_object stays active.",
            "The next useful work is to prove Q_M=ell_M(Pi_M J_H)=M_source[W] with dressed Hilbert source, or fill the wrong-object residual rows.",
            "THEOREM_CONDITIONAL_WRONG_OBJECT_BOUND_ACTIVE",
            "top_hilbert_decision",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def wrong_object_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "WOR3595_0_total",
            "R_wrong",
            "Pi_M J_H - J_M_top - dB_zero",
            "total wrong-object/equality residual",
            "ACTIVE_NONCLAIM",
            "top_hilbert_attempt",
        ),
        (
            "WOR3595_1_Q_label",
            "R_Qlabel",
            "(ell_M(Pi_M J_H)-Q_M) omega_M_top",
            "topological label not defined from same Hilbert source",
            "MAIN_BLOCKER",
            "top_hilbert_obstructions",
        ),
        (
            "WOR3595_2_cohomology",
            "R_perp",
            "non-mass cohomology/harmonic component of Pi_M J_H",
            "fixed exterior cohomology not reduced to the single mass class",
            "CONDITIONAL_ZERO_OR_BOUND",
            "top_hilbert_attempt",
        ),
        (
            "WOR3595_3_boundary_exact",
            "R_Bzero",
            "dB_zero with nonzero compact linking-surface flux",
            "boundary/improvement term shifts measured mass",
            "OPEN_BOUNDARY_BLOCKER",
            "top_hilbert_obstructions",
        ),
        (
            "WOR3595_4_worldtube_measure",
            "R_worldtube",
            "M_source[W] - ell_M(Pi_M J_H)",
            "dressed source measure not locked to exterior charge",
            "OPEN_MAIN_BLOCKER",
            "worldtube_theorem",
        ),
        (
            "WOR3595_5_extra_exchange",
            "R_extra_exchange",
            "Pi_M dJ_extra + hidden/domain/nonEH/memory/range exchange",
            "total parent conservation does not imply separate Hilbert mass-channel closure",
            "OPEN_EXCHANGE_BLOCKER",
            "parent_source_identity",
        ),
        (
            "WOR3595_6_frame_species",
            "R_frame_species",
            "same-source-frame/species mismatch in J_H",
            "source current must be the same observed Hilbert current for matter, clocks, rods, EM, and orbits",
            "OPEN_FRAME_WEP_BLOCKER",
            "parent_source_residuals",
        ),
        (
            "WOR3595_7_em_once",
            "R_EM_once",
            "missing or double-counted EM/Poynting/binding contribution in J_H_total",
            "Hilbert source cannot be matter-only if EM stress contributes to mass",
            "OPEN_EM_GUARD",
            "em_hodge_bound",
        ),
        (
            "WOR3595_8_calibration",
            "R_calibration",
            "M_top/Hilbert charge differs from Gauss/orbital GM",
            "even true equality still needs measured-GM calibration",
            "DOWNSTREAM_OPEN",
            "charge_direct",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, formula, meaning, status, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("WPB3595_0_epsilon_Qlabel", "epsilon_Qlabel", "abs(ell_M(Pi_M J_H)-Q_M)/abs(M_H_ref)", "dimensionless", "MISSING_QM_HILBERT_DEFINITION", "Q_M source definition, ell_M normalization, M_H_ref, source path", "top_hilbert_obstructions"),
        ("WPB3595_1_epsilon_Rperp", "epsilon_Rperp", "||R_perp||_M/abs(M_H_ref)", "dimensionless cohomology residual", "0 if H2(E)=R[S2] and no nonmass class; otherwise missing norm", "topology certificate or nonmass cohomology norm", "top_hilbert_attempt"),
        ("WPB3595_2_epsilon_Bzero", "epsilon_Bzero", "abs(integral_boundary dB_zero)/abs(M_H_ref)", "dimensionless boundary/reference residual", "MISSING_BOUNDARY_ZERO_OR_CONSTANT_CALIBRATION", "B_zero flux/reference theorem or sourced boundary coefficient", "top_hilbert_obstructions"),
        ("WPB3595_3_epsilon_worldtube", "epsilon_worldtube", "abs(M_source[W]-ell_M(Pi_M J_H))/abs(M_H_ref)", "dimensionless worldtube/source-measure residual", "MISSING_DRESSED_SOURCE_MEASURE_LOCK", "dressed Hamiltonian source measure, reference subtraction, source path", "worldtube_theorem"),
        ("WPB3595_4_epsilon_extra_exchange", "epsilon_extra_exchange", "abs(int_A Pi_M dJ_extra)/abs(M_H_ref)", "dimensionless exchange/source-normalization residual", "MISSING_ZERO_OR_NUMERIC_CHANNEL_BOUNDS", "channelwise extra-current projections and local bounds", "parent_source_identity"),
        ("WPB3595_5_epsilon_frame_species", "epsilon_frame_species", "abs(R_frame_species)/abs(M_H_ref)", "dimensionless WEP/frame source residual", "MISSING_SAME_SOURCE_FRAME_THEOREM", "same observed coframe/source theorem or WEP/source residual", "parent_source_residuals"),
        ("WPB3595_6_epsilon_EM_once", "epsilon_EM_once", "abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding])/abs(M_H_ref)", "dimensionless EM accounting residual", "MISSING_ONCE_ONLY_EM_STRESS_ACCOUNTING", "EM stress/Poynting/binding Hilbert source map", "em_hodge_bound"),
        ("WPB3595_7_epsilon_wrong_object_total", "epsilon_PiM_parent_wrong_object", "epsilon_Qlabel+epsilon_Rperp+epsilon_Bzero+epsilon_worldtube+epsilon_extra_exchange+epsilon_frame_species+epsilon_EM_once", "dimensionless source-coupling residual", "NOT_SCORE_READY_TOTAL", "all component zero theorems or numeric/source-backed bounds", "residual_3594"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": p[source_id],
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_id in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3595_0_conditional_glue", "Hilbert-to-topological glue theorem", "PASS_CONDITIONAL_THEOREM", "de Rham/topological route is explicit but premises are not parent-certified", "parent_noether"),
        ("PROM3595_1_wrong_object_zero", "epsilon_PiM_parent_wrong_object=0", "FAIL_CURRENT_CLAIM", "Q_M/worldtube/Hilbert source lock remains open", "top_hilbert_obstructions"),
        ("PROM3595_2_bound_pack", "wrong-object bound rows complete", "PASS_NONCLAIM", "residual rows are source-ready but not numeric/score-ready", "source_measure_residuals"),
        ("PROM3595_3_EM_guard", "EM/Poynting/binding included once", "OPEN_GUARDED", "cannot omit EM stress from the source charge", "em_hodge_bound"),
        ("PROM3595_4_no_GM_Newton_claim", "no measured-GM/Newton/PPN/local-GR promotion", "PASS_GUARD", "Gauss/orbital calibration and PPN readout remain downstream", "charge_residuals"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "CONDITIONAL_HILBERT_TO_TOPO_GLUE_DERIVED_WRONG_OBJECT_BOUND_ACTIVE",
            "strongest_result": "3595 derives the exact conditional glue route: in a fixed S2 x I exterior with closed Hilbert mass current and H2(E)=R[S2], Pi_M J_H decomposes as ell_M(Pi_M J_H) omega_M_top + dB + R_perp. If Q_M is defined from the same dressed Hilbert/worldtube source, R_perp=0, boundary exact flux is zero, and EM/Poynting/binding are included once, then the topological charge is not the wrong object and epsilon_PiM_parent can vanish.",
            "decision": "do not promote source coupling; retain epsilon_PiM_parent_wrong_object until Q_M=ell_M(Pi_M J_H)=M_source[W] is parent-signed and component residuals are zero or bounded",
            "still_missing": "parent-owned Q_M Hilbert definition, dressed worldtube source measure, zero exact boundary flux, no extra-current projection, same source frame/species theorem, EM/Poynting once-only source accounting, Gauss/orbital calibration, PPN source stability",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["top_hilbert_attempt"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3595_0",
            "target_doc": "3596-Y5-R2FR-worldtube-Hilbert-source-measure-lock-or-wrong-object-input-fill.md",
            "target_script": "scripts/Y5_R2FR_3596_worldtube_Hilbert_source_measure_lock_or_wrong_object_input_fill.py",
            "objective": "prove Q_M=ell_M(Pi_M J_H)=M_source[W] as a dressed Hilbert/Hamiltonian source measure including EM/Poynting/binding once, or fill source-ready epsilon_Qlabel/epsilon_worldtube/epsilon_EM_once rows",
            "success_gate": "worldtube source measure is parent-owned before readout and equal to exterior Hilbert/topological charge, or wrong-object residual inputs remain explicit and nonclaim",
            "reason": "3595 derives the cohomology glue theorem; the dominant remaining blocker is the Hilbert-defined charge scalar and dressed worldtube source measure",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    wrong: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3595_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3595 source paths exist"))
    validations.append(("VAL3595_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3595 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3595_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3595 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3595_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3595_4_glue_theorem_present", any(row["theorem_id"] == "HGT3595_6_conditional_glue_theorem" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in theorem), "conditional Hilbert/topological glue theorem row present"))
    validations.append(("VAL3595_5_wrong_object_total_present", any(row["symbol"] == "R_wrong" for row in wrong), "wrong-object residual decomposition includes total R_wrong"))
    required_bounds = {"epsilon_Qlabel", "epsilon_Rperp", "epsilon_Bzero", "epsilon_worldtube", "epsilon_extra_exchange", "epsilon_frame_species", "epsilon_EM_once", "epsilon_PiM_parent_wrong_object"}
    validations.append(("VAL3595_6_bound_pack_complete", required_bounds.issubset({str(row["symbol"]) for row in bounds}), "wrong-object bound pack includes all required components"))
    validations.append(("VAL3595_7_wrong_object_claim_blocked", any(row["gate_id"] == "PROM3595_1_wrong_object_zero" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "wrong-object zero claim remains blocked"))
    validations.append(("VAL3595_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, wrong, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3595_9_no_local_gr_claim", any(row["gate_id"] == "PROM3595_4_no_GM_Newton_claim" and row["status"] == "PASS_GUARD" for row in gates), "measured-GM/Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3595_10_next_target_selected", any(row["next_id"] == "NEXT3595_0" for row in next_target), "3596 worldtube source-measure lock target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, wrong, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3595_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = list(FORMALIZATION.rglob("*3595*")) if FORMALIZATION.exists() else []
    validations.append(("VAL3595_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3595 checkpoint output appears in formalization-workbench"))
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
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


def write_doc(theorem, wrong, bounds, gates, status, next_target, validation) -> None:
    lines = [
        "# 3595 - Hilbert source to topological charge glue or wrong-object bound",
        "",
        "## Verdict",
        "3595 gets the exact mathematical route on paper: a closed Hilbert mass current in a fixed `S2 x I` exterior decomposes into the normalized topological mass representative plus an exact term and any non-mass cohomology residue.",
        "",
        "So the topological route can work **only if** `Q_M` is not an independent label: it must be `ell_M(Pi_M J_H)=M_source[W]` before orbital readout, with zero exact boundary flux and EM/Poynting/binding included once.",
        "",
        "## Glue Theorem",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Wrong-Object Residuals"])
    for row in wrong:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Bound Rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` / `{row['symbol']}`: {row['current_value']} - {row['formula']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
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
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    theorem = glue_theorem_rows(source_map)
    wrong = wrong_object_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["glue_theorem"], theorem)
    write_csv(out_paths["wrong_object_residuals"], wrong)
    write_csv(out_paths["bound_rows"], bounds)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, wrong, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, wrong, bounds, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
