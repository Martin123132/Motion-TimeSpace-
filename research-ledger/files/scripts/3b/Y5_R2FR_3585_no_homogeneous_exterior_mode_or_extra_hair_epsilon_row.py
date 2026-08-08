from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_NO_HOMOGENEOUS_EXTERIOR_EXTRA_HAIR_3585"
CHECKPOINT_ID = "3585"
DOC = ROOT / "3585-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3584": RESIDUALS / "P8_Y5_R2FR_3584_NEXT_TARGET.csv",
        "status_3584": RESIDUALS / "P8_Y5_R2FR_3584_STATUS.csv",
        "theorem_3584": RESIDUALS / "P8_Y5_R2FR_3584_PARENT_ESTAT_THEOREM_ATTEMPT.csv",
        "clauses_3584": RESIDUALS / "P8_Y5_R2FR_3584_STATIONARITY_CLAUSE_AUDIT.csv",
        "epsilon_3584": RESIDUALS / "P8_Y5_R2FR_3584_ESTAT_EPSILON_STACK.csv",
        "residuals_3583": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "gk_nohair_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv",
        "gk_fail_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_FAILURE_MODES.csv",
        "gk_metric_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_METRIC_REDUCTION_STATUS.csv",
        "gk_gates_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_CLAIM_GATES.csv",
        "extra_energy_506": RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
        "sector_silence_506": RESIDUALS / "P8_MTS_SECTOR_SILENCE_STATUS.csv",
        "bmr_positive_557": RESIDUALS / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
        "boundary_cohom_549": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
        "eh_nohair_530": RESIDUALS / "P8_Y5_EH_NOHAIR_THEOREM_TARGETS.csv",
        "action_coverage_1276": RESIDUALS / "P8_Y5_R10_1276_A511_ACTION_BLOCK_COVERAGE.csv",
        "newton_1339": RESIDUALS / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3585_SOURCE_REGISTER.csv",
        "nohom_theorem": RESIDUALS / "P8_Y5_R2FR_3585_NO_HOMOGENEOUS_MODE_THEOREM.csv",
        "channel_audit": RESIDUALS / "P8_Y5_R2FR_3585_EXTRA_HAIR_CHANNEL_AUDIT.csv",
        "epsilon_rows": RESIDUALS / "P8_Y5_R2FR_3585_EPSILON_HAIR_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3585_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3585_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3585_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_no_homogeneous_exterior_extra_hair_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3585_VALIDATION.csv",
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
            "role": "3585 no-homogeneous-mode / extra-hair theorem-or-bound input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def nohom_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "NHE3585_0_decomposition",
            "homogeneous exterior-mode split",
            "delta Phi_hom = h_TT^rad + X_coercive + X_massless/top + X_gauge/proj",
            "A hidden exterior mode can only enter through radiative metric modes, extra-sector fields, topological/boundary charges, or gauge/projector-hidden components.",
            "DECOMPOSITION_WRITTEN",
            "epsilon_3584",
        ),
        (
            "NHE3585_1_EH_no_news",
            "EH radiative sector",
            "Bondi/news or Killing-energy flux N_AB N^AB=0 plus stationary boundary data => h_TT^rad=0 in the local stationary branch",
            "Radiative homogeneous GR waves are not compatible with the no-radiation/stationary exterior boundary class; if news is nonzero it is an epsilon_hom_mode contribution.",
            "CONDITIONAL_ZERO_FOR_RADIATIVE_EH_MODES",
            "theorem_3584",
        ),
        (
            "NHE3585_2_coercive_extra_zero",
            "massive/coercive extra-sector no-hair",
            "L_X X=0, <X,L_X X> >= c_X||X||^2, zero boundary flux, zero source charge => X=0",
            "This imports the old energy-identity route and sharpens it: positivity plus boundary/source silence kills the extra mode, not a declaration of silence.",
            "CONDITIONAL_ZERO_FOR_COERCIVE_EXTRA_MODES",
            "extra_energy_506",
        ),
        (
            "NHE3585_3_cross_term_bound",
            "mixed/cross operator bound",
            "|<X,CY>| <= eta E_X + eta' E_Y with eta+eta'<1",
            "The positive-operator proof only survives if cross terms cannot overturn coercivity. Otherwise the cross term becomes epsilon_cross_hair.",
            "BOUND_REQUIRED_FOR_COERCIVITY",
            "gk_fail_2470",
        ),
        (
            "NHE3585_4_topological_boundary_escape",
            "topological/boundary hair escape channel",
            "harmonic/topological class or finite boundary charge survives unless relative class/reference fixes its flux",
            "No-hair cannot erase topological charges by positivity. They must be fixed, measured, subtracted, or bounded.",
            "NOT_ZERO_BY_DEFAULT_BOUNDARY_EPSILON_REQUIRED",
            "boundary_cohom_549",
        ),
        (
            "NHE3585_5_projector_gauge_escape",
            "projector/gauge-hidden hair",
            "P_loc delta Phi=0 does not imply delta Phi=0 unless kernel/gauge/topology are audited",
            "This prevents using the local projection as a hiding place for nonprojected stress or source residuals.",
            "NOT_ZERO_BY_DEFAULT_PROJECTOR_EPSILON_REQUIRED",
            "gk_fail_2470",
        ),
        (
            "NHE3585_6_Estat_update",
            "3584 E_stat update",
            "Z_no_hom_mode = Z_EH_no_news & Z_coercive_extra & Z_cross_bound & Z_top_boundary & Z_projector_kernel",
            "3585 closes only the conditional theorem shape. Current MTS still lacks signed field-specific positivity, boundary flux, topology, and projector kernel clauses.",
            "NO_HOM_MODE_ROUTE_SHARPENED_NOT_CLAIMED",
            "status_3584",
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


def channel_audit_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "CHA3585_0_EH_TT",
            "EH_radiative_TT",
            "PASS_IF_ZERO_NEWS_OR_NO_RADIATION_BOUNDARY_SIGNED",
            "epsilon_news",
            "The public EM anchor/no-radiation route supports this, but gravitational news/no incoming wave must be explicitly part of the branch.",
            "eh_nohair_530",
        ),
        (
            "CHA3585_1_GammaKhat_GK",
            "Gamma/Khat local response",
            "PASS_IF_POSITIVE_ENERGY_IDENTITY_AND_BOUNDARY_ZERO_SIGNED",
            "epsilon_GK_hair",
            "2470 has the method but not the signed positivity/boundary clauses.",
            "gk_nohair_2470",
        ),
        (
            "CHA3585_2_bulk_memory_range",
            "bulk/memory/range extra modes",
            "PASS_IF_FIELD_SPECIFIC_OPERATOR_POSITIVE_AND_SOURCE_CHARGE_ZERO",
            "epsilon_bulk_memory_range_hair",
            "Mass gap alone is not enough; source/test coupling and boundary flux must vanish or be bounded.",
            "bmr_positive_557",
        ),
        (
            "CHA3585_3_domain_projector",
            "domain/projector selector",
            "UNSIGNED_PROJECTOR_KERNEL_AUDIT_REQUIRED",
            "epsilon_projector_hair",
            "Projection silence is not full-field silence unless kernel/gauge/topological sectors are audited.",
            "sector_silence_506",
        ),
        (
            "CHA3585_4_boundary_topology",
            "boundary/topological sector",
            "UNSIGNED_RELATIVE_COHOMOLOGY_OR_BOUNDARY_FLUX_REQUIRED",
            "epsilon_top_boundary_hair",
            "Topological charge can survive as a real boundary observable and must not be killed by local positivity.",
            "boundary_cohom_549",
        ),
        (
            "CHA3585_5_metric_operator",
            "non-EH metric operator family",
            "UNSIGNED_EH_DOMINANCE_OR_NON_EH_VECTOR_REQUIRED",
            "epsilon_nonEH_hair",
            "Lovelock gives a conditional EH route, but retained R11/non-EH operators remain a source of local hair.",
            "action_coverage_1276",
        ),
        (
            "CHA3585_6_source_normalization",
            "source/coupling normalization",
            "STILL_SEPARATE_SOURCE_COUPLING_GATE",
            "epsilon_source_coupling",
            "Even zero exterior hair does not calibrate G, measured GM, or source weights.",
            "newton_1339",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": channel_id,
            "channel": channel,
            "status": status,
            "fallback_row": fallback_row,
            "notes": notes,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for channel_id, channel, status, fallback_row, notes, source_key in rows
    ]


def epsilon_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "EHB3585_0_epsilon_news",
            "epsilon_news",
            "integral_Iplus |N_AB|^2 duduOmega or local gravitational-wave energy flux through exterior boundary",
            "zero iff no radiative gravitational homogeneous mode in the stationary branch",
            "energy/time or normalized Hamiltonian residual",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "theorem_3584",
        ),
        (
            "EHB3585_1_epsilon_coercive_extra",
            "epsilon_coercive_extra",
            "sum_X max(0, boundary_flux_X + source_charge_X - c_X||X||^2 lower-bound certificate)",
            "captures failure of positive-operator no-hair for massive/coercive extra fields",
            "field-energy or normalized source residual",
            "MISSING_FIELD_SPECIFIC_COERCIVITY_INPUTS",
            "extra_energy_506",
        ),
        (
            "EHB3585_2_epsilon_cross_hair",
            "epsilon_cross_hair",
            "uncancelled mixed A/Gamma/memory/operator cross-term bound",
            "captures cross terms that can defeat coercivity",
            "field-energy or normalized source residual",
            "MISSING_CROSS_TERM_BOUND",
            "gk_fail_2470",
        ),
        (
            "EHB3585_3_epsilon_top_boundary_hair",
            "epsilon_top_boundary_hair",
            "absolute boundary/topological flux or relative cohomology charge not fixed by reference class",
            "captures hair that positivity cannot remove",
            "boundary flux/source norm",
            "MISSING_TOPOLOGY_OR_BOUNDARY_FLUX_VALUE",
            "boundary_cohom_549",
        ),
        (
            "EHB3585_4_epsilon_projector_hair",
            "epsilon_projector_hair",
            "norm((1-P_loc)delta Phi_hair) plus induced stress/source projection",
            "captures components hidden by projection/gauge/kernel assumptions",
            "operator/stress norm",
            "MISSING_PROJECTOR_KERNEL_AUDIT",
            "gk_fail_2470",
        ),
        (
            "EHB3585_5_epsilon_nonEH_hair",
            "epsilon_nonEH_hair",
            "norm of retained R11/non-EH operator response in the local exterior",
            "captures failure of EH dominance/extra operator silence",
            "PPN/source norm",
            "MISSING_EH_DOMINANCE_OR_NON_EH_VECTOR",
            "action_coverage_1276",
        ),
        (
            "EHB3585_6_epsilon_hom_mode",
            "epsilon_hom_mode",
            "epsilon_news + epsilon_coercive_extra + epsilon_cross_hair + epsilon_top_boundary_hair + epsilon_projector_hair + epsilon_nonEH_hair",
            "decomposes the 3584 homogeneous-mode residual into physical channels",
            "same normalization as epsilon_Estat",
            "NO_CANCELLATION_HOM_STACK_READY_VALUES_MISSING",
            "epsilon_3584",
        ),
        (
            "EHB3585_7_epsilon_Estat_after_3585",
            "epsilon_Estat",
            "epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair",
            "3585 refines epsilon_hom_mode/epsilon_extra_hair but does not zero them claim-grade",
            "same normalization as R_ann residual",
            "REFINED_NONCLAIM",
            "epsilon_3584",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "meaning": meaning,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, definition, meaning, units, status, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3585_0_sources", "PASS", "all source paths and selected anchors exist", "next_3584"),
        ("GATE3585_1_nohair_method", "PASS_CONDITIONAL_THEOREM", "energy-identity/coercivity no-hair route is written and channelized", "gk_nohair_2470"),
        ("GATE3585_2_EH_radiation", "PASS_IF_ZERO_NEWS_BOUNDARY_SIGNED", "EH radiative modes are killed by stationary/no-news boundary, not by local algebra alone", "eh_nohair_530"),
        ("GATE3585_3_extra_hair_claim", "FAIL_CURRENT_CLAIM", "field-specific positivity, source charge zero, cross-term, topology, and projector kernel clauses remain unsigned", "sector_silence_506"),
        ("GATE3585_4_Estat_claim", "FAIL_CURRENT_CLAIM", "epsilon_hom_mode and epsilon_extra_hair are refined but not zeroed", "status_3584"),
        ("GATE3585_5_local_GR", "FAIL_CURRENT_CLAIM", "local GR/Newton still needs E_stat, gauge/corner, source coupling, GM calibration, and PPN closure", "newton_1339"),
        ("GATE3585_6_bound_fallback", "PASS_NONCLAIM_FALLBACK", "homogeneous/extrafield hair has explicit no-cancellation epsilon rows", "epsilon_3584"),
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
            "status": "NO_HOMOGENEOUS_MODE_ROUTE_CHANNELIZED_NOT_ZERO_CLAIMED",
            "strongest_result": "3585 sharpens the E_stat obstruction: radiative EH modes can be killed by a zero-news/no-radiation boundary; massive/coercive extra modes can be killed by a positive self-adjoint energy identity with zero boundary/source charge; but topological/boundary, cross-term, non-EH, and projector-kernel hair remain explicit epsilon channels.",
            "still_missing": "field-specific coercivity signs, zero source charges, zero boundary fluxes, cross-term smallness, relative cohomology/reference lock, projector kernel audit, non-EH operator vector, source coupling normalization, GM calibration, and PPN closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3584"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3585_0",
            "target_doc": "3586-Y5-R2FR-field-specific-coercivity-and-source-charge-zero-or-hair-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_3586_field_specific_coercivity_and_source_charge_zero_or_hair_bound_fill.py",
            "objective": "attack the strongest zero route inside 3585: field-specific positive/coercive extra-sector operators with zero source charge and zero boundary flux, or fill the corresponding epsilon_coercive_extra and epsilon_cross_hair rows",
            "success_gate": "at least one named extra channel gets a parent-signed coercive zero theorem, or its finite hair bound row receives explicit operator/source/boundary terms",
            "reason": "3585 shows the no-hair proof can only be promoted channel-by-channel; coercive extra modes are the cleanest non-GR hair to try first",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    channels: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3584": "NEXT3584_0",
        "status_3584": "PARENT_ESTAT_ROUTE_DERIVED_AS_UNIQUENESS_LEMMA",
        "theorem_3584": "PET3584_3_no_homogeneous_kernel",
        "clauses_3584": "SCA3584_4_no_homogeneous_mode",
        "epsilon_3584": "ESE3584_3_epsilon_hom",
        "residuals_3583": "GRS3583_7_R_ann_abs_after_3583",
        "gk_nohair_2470": "NH2470_2_energy_identity",
        "gk_fail_2470": "FAIL2470_4_topological_hair",
        "gk_metric_2470": "MET2470_2_bound_route",
        "gk_gates_2470": "GATE2470_2_stress_bound",
        "extra_energy_506": "E506_scalar_positive_operator",
        "sector_silence_506": "motion_time_flow_modes",
        "bmr_positive_557": "BMR557_1_massive_positive_operator",
        "boundary_cohom_549": "BCT549_4_volume_no_flux_not_alpha3_no_flux",
        "eh_nohair_530": "EHNH530_1_metric_only_local_exterior",
        "action_coverage_1276": "AC1276_3_extra_silence",
        "newton_1339": "NEW1339_2_GM_calibration",
    }
    validations.append(("VAL3585_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3585 source paths exist"))
    validations.append(("VAL3585_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3585 anchors found"))
    validations.append(("VAL3585_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3585 output files written"))
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
    validations.append(("VAL3585_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3585_4_channel_decomposition_present", any(row["theorem_id"] == "NHE3585_0_decomposition" for row in theorem), "homogeneous-mode decomposition present"))
    validations.append(("VAL3585_5_coercive_zero_present", any(row["theorem_id"] == "NHE3585_2_coercive_extra_zero" for row in theorem), "coercive extra zero theorem row present"))
    validations.append(("VAL3585_6_escape_channels_present", {"epsilon_top_boundary_hair", "epsilon_projector_hair", "epsilon_nonEH_hair"}.issubset({str(row["symbol"]) for row in epsilons}), "escape-channel epsilon rows present"))
    validations.append(("VAL3585_7_claim_blocked", any(row["gate_id"] == "GATE3585_3_extra_hair_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "extra hair claim remains blocked"))
    validations.append(("VAL3585_8_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in theorem + channels + epsilons + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3585_9_next_target_selected", any(row["next_id"] == "NEXT3585_0" for row in next_target), "field-specific coercivity next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in theorem + channels + epsilons + gates + status)
    validations.append(("VAL3585_10_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3585*")) or any(FORMALIZATION.rglob("3585-Y5-R2FR*"))
    validations.append(("VAL3585_11_formalization_workbench_untouched", not formalization_touched, "no 3585 checkpoint output appears in formalization-workbench"))
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
    channels: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3585 — no homogeneous exterior mode or extra-hair epsilon row",
        "",
        "## Verdict",
        "3585 does not prove full no-hair, but it turns the dangerous `3584` homogeneous-mode blocker into a channel theorem.  Radiative EH modes are killed only by a zero-news/no-radiation boundary; massive/coercive extra modes are killed only by a positive self-adjoint energy identity with zero boundary flux and zero source charge.",
        "",
        "Everything else stays honest as a residual: cross terms, topological/boundary hair, projector-hidden modes, and retained non-EH operators.  The updated stack is:",
        "",
        "`epsilon_hom_mode = epsilon_news + epsilon_coercive_extra + epsilon_cross_hair + epsilon_top_boundary_hair + epsilon_projector_hair + epsilon_nonEH_hair`.",
        "",
        "So this checkpoint is progress because it says exactly what kind of hair can be killed by theorem and what kind must be bounded.",
        "",
        "## No-homogeneous-mode theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['mathematical_form']} ({row['status']})")
    lines.extend(["", "## Channel audit"])
    for row in channels:
        lines.append(f"- `{row['channel_id']}` `{row['channel']}`: {row['status']} -> `{row['fallback_row']}`")
    lines.extend(["", "## Epsilon rows"])
    for row in epsilons:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['definition']} ({row['status']})")
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
    theorem = nohom_theorem_rows(source_paths)
    channels = channel_audit_rows(source_paths)
    epsilons = epsilon_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "nohom_theorem": theorem,
        "channel_audit": channels,
        "epsilon_rows": epsilons,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, theorem, channels, epsilons, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, channels, epsilons, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3585 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
