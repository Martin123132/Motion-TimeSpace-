from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3622"
BRANCH_ID = "MTS_R2FR_Y5_TQ_NQ_PARENT_FIBRE_METRIC_OR_SOURCE_BOUND_ACQUISITION_3622"
DOC = ROOT / "3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3622_SOURCE_REGISTER.csv",
        "fibre_metric_theorem": RESIDUALS / "P8_Y5_R2FR_3622_TQ_NQ_FIBRE_METRIC_THEOREM.csv",
        "rescaling_countermodel": RESIDUALS / "P8_Y5_R2FR_3622_TQ_RESCALE_COUNTERMODEL_AUDIT.csv",
        "source_bound_acquisition": RESIDUALS / "P8_Y5_R2FR_3622_WEM_PHI_BOUND_ACQUISITION_LEDGER.csv",
        "finite_runner_update": RESIDUALS / "P8_Y5_R2FR_3622_FINITE_RUNNER_UPDATE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3622_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3622_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3622_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_TQ_NQ_parent_fibre_metric_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3622_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3621": (
            RESIDUALS / "P8_Y5_R2FR_3621_NEXT_TARGET.csv",
            "3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md",
        ),
        "joint_packet_3621": (
            RESIDUALS / "P8_Y5_R2FR_3621_JOINT_OWNER_PACKET.csv",
            "N_Q=<T_Q,T_Q>_P",
        ),
        "finite_runner_3621": (
            RESIDUALS / "P8_Y5_R2FR_3621_FINITE_BOUND_RUNNER_TEMPLATE.csv",
            "Phi_EM_boundary",
        ),
        "tq_signature_1100": (
            RESIDUALS / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "TQS1100_2_fixed_generator_norm",
        ),
        "tq_theorem_1100": (
            RESIDUALS / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
            "TQT1100_2_rescaling_countermodel",
        ),
        "tq_acquisition_1100": (
            RESIDUALS / "P8_Y5_R10_1100_TQ_REQUIRED_SOURCE_ACQUISITION_LEDGER.csv",
            "ACQ1100_2_norm",
        ),
        "tq_audit_1929": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_1929_TQ_GAUGE_NORM_SIGNATURE_AUDIT.csv",
            "TQS1929_5_verdict",
        ),
        "noether_3291": (
            RESIDUALS / "P8_Y5_R2FR_3291_TQ_NOETHER_OWNER_LEMMA.csv",
            "TQN3291_1_minimal_coupling_variation",
        ),
        "fibre_metric_609": (
            RESIDUALS / "P8_Y5_R10_609_FIBRE_METRIC_OWNERSHIP.csv",
            "FM609_3_metric_verdict",
        ),
        "charge_lattice_885": (
            RESIDUALS / "P8_Y5_R10_885_CHARGE_LATTICE_ATTEMPT.csv",
            "CL885_5_lattice_verdict",
        ),
        "bf_lattice_926": (
            RESIDUALS / "P8_Y5_R10_926_BF_LATTICE_THEOREM_ATTEMPT.csv",
            "BF926_4_ratio_lattice",
        ),
        "common_scale_runner": (
            RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv",
            "UCRUN3510_1_Newton_GM",
        ),
        "wep_components_2100": (
            RESIDUALS / "P8_Y5_PARENT_QLOC_2100_WEP_COMPONENT_BOUND_ROWS.csv",
            "WCB2100_5_total_guard",
        ),
        "poynting_3463": (
            RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
            "EM3463_2_poynting",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def fibre_metric_theorem_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_0_compact_generator",
            "claim_piece": "compact charge generator",
            "statement": "If the visible EM direction is a compact parent U(1) generator, T_Q is fixed up to the integral lattice convention exp(2*pi*T_Q)=1.",
            "formula": "T_Q in Lambda_G; exp(2*pi*T_Q)=1; matter weights n_A in Z",
            "derived_effect": "relative charge labels are fixed representation data",
            "current_status": "PARTIAL_SUCCESS_RELATIVE_LABELS_ONLY",
            "source_path": str(sources["tq_signature_1100"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_1_compactness_limit",
            "claim_piece": "compactness does not fix coupling",
            "statement": "Compact U(1) fixes relative integer labels but not the base charge unit or Maxwell kinetic coefficient.",
            "formula": "n_A in Z does not imply fixed N_Q or fixed C_P N_Q",
            "derived_effect": "charge quantization alone cannot derive alpha_EM or source normalization",
            "current_status": "LIMIT_PROVED_COUNTERMODEL_RETAINED",
            "source_path": str(sources["tq_theorem_1100"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_2_fixed_fibre_metric",
            "claim_piece": "fixed parent fibre metric/norm",
            "statement": "A nonrescalable parent fibre metric, symplectic form, level, or lattice index can fix N_Q=<T_Q,T_Q>_P.",
            "formula": "G_P fixed and q-basic; N_Q=G_P(T_Q,T_Q); D_v N_Q=0 for v in ker(Dq)",
            "derived_effect": "the inherited parent contribution to the Maxwell kinetic coefficient is X-silent",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(sources["fibre_metric_609"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_3_curvature_subblock",
            "claim_piece": "unique curvature norm",
            "statement": "If the parent action has a single curvature norm and no independent visible F_Q^2 slot, the Q subblock gives Z_Q=C_P N_Q.",
            "formula": "S_parent superset -C_P/4 int <F_parent,*F_parent>_P => S_Q=-C_P N_Q/4 int F_Q wedge *F_Q",
            "derived_effect": "lambda_F2=0 only if no independent counterterm slot exists",
            "current_status": "CONDITIONAL_REQUIRES_DOMAIN_EXHAUSTION",
            "source_path": str(sources["tq_signature_1100"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_4_same_current",
            "claim_piece": "same Noether current",
            "statement": "With fixed T_Q and representation weights, minimal coupling gives the same J_Q used by source/test readout.",
            "formula": "D_A=d+n_A A_Q T_Q; J_Q=delta S_matter/delta A_Q=sum_A n_A J_A",
            "derived_effect": "kappa_J is absent if no source-only current morphism is allowed",
            "current_status": "EXACT_CONDITIONAL_CURRENT_OWNER",
            "source_path": str(sources["noether_3291"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "TNF3622_5_joint_signature",
            "claim_piece": "T_Q/N_Q spine",
            "statement": "T_Q/N_Q closes the shared EM normalization spine only if compact generator, fixed norm, unique curvature norm, same current owner, and readout closure are signed together.",
            "formula": "compact_TQ && fixed_NQ && unique_F2 && same_JQ && readout_closure => D_v(C_P N_Q)=D_v J_Q=0",
            "derived_effect": "lambda_F2, b_alpha norm-part and kappa_J can collapse together",
            "current_status": "JOINT_SIGNATURE_NOT_PARENT_SIGNED",
            "source_path": str(sources["tq_audit_1929"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def rescaling_countermodel_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "countermodel_id": "RCM3622_0_continuous_norm_rescale",
            "countermodel": "If N_Q is not fixed, the continuous kinetic normalization can float even when charge labels are integer.",
            "form": "T_Q fixed as lattice label but Z_Q=C_P N_Q + lambda_F2 remains continuous",
            "blocks": "alpha_EM and EM source-weight prediction",
            "status": "COUNTERMODEL_RETAINED",
            "source_path": str(sources["tq_theorem_1100"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "countermodel_id": "RCM3622_1_base_charge_unit",
            "countermodel": "Compact charge lattice can fix relative n_A while leaving the observed base unit Q_* unowned.",
            "form": "q_A=n_A Q_*; n_A in Z but Q_* not derived",
            "blocks": "absolute current/source calibration",
            "status": "COUNTERMODEL_RETAINED",
            "source_path": str(sources["charge_lattice_885"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "countermodel_id": "RCM3622_2_independent_F2",
            "countermodel": "Even with a fixed parent norm, an independent lambda_A F_Q^2 counterterm reopens the kinetic coefficient.",
            "form": "Z_Q=C_P N_Q + lambda_A",
            "blocks": "unique F2 / b_alpha theorem zero",
            "status": "COUNTERMODEL_RETAINED",
            "source_path": str(sources["tq_signature_1100"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "countermodel_id": "RCM3622_3_current_morphism",
            "countermodel": "A source/test current morphism can rescale J_Q after the Noether current exists.",
            "form": "J_Q^readout=(1+kappa_J)J_Q^Noether",
            "blocks": "source/test coupling and WEP/R10 current calibration",
            "status": "COUNTERMODEL_RETAINED",
            "source_path": str(sources["noether_3291"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_bound_acquisition_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "acquisition_id": "SBA3622_0_w_EM",
            "coefficient": "w_EM",
            "target_bound": "direct EM source-weight / binding-energy coupling bound",
            "candidate_arenas": "WEP composition; Newton_GM; PPN source terms; EM binding fraction",
            "current_bound_status": "MISSING_DIRECT_NUMERIC_BOUND",
            "available_local_source_path": str(sources["common_scale_runner"][0]),
            "needed_next": "source-backed map from w_EM to eta, GM, or PPN with EM binding/source fraction",
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "acquisition_id": "SBA3622_1_Phi_EM_boundary",
            "coefficient": "Phi_EM_boundary",
            "target_bound": "stationary source no-flux theorem or radiative Poynting flux bound",
            "candidate_arenas": "orbital energy loss; radiative flux accounting; H_tau boundary flux; stationary source charge",
            "current_bound_status": "MISSING_H_TAU_SCALE_OR_NUMERIC_FLUX_BOUND",
            "available_local_source_path": str(sources["poynting_3463"][0]),
            "needed_next": "closed worldtube/no-radiation theorem or numeric flux/H_tau normalization row",
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_runner_update_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": "FRU3622_0_lambda_F2",
            "coefficient": "lambda_F2",
            "update": "T_Q/N_Q theorem would remove norm-origin lambda_F2 only with unique F2/domain exhaustion.",
            "runner_status": "STILL_BLOCKED_PARENT_SIGNATURE_MISSING",
            "source_path": str(sources["finite_runner_3621"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": "FRU3622_1_b_alpha",
            "coefficient": "b_alpha",
            "update": "fixed N_Q would zero the norm contribution, but readout/radiative closure remains required.",
            "runner_status": "STILL_BLOCKED_READOUT_CLOSURE_MISSING",
            "source_path": str(sources["finite_runner_3621"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": "FRU3622_2_kappa_J",
            "coefficient": "kappa_J",
            "update": "same Noether current theorem exists conditionally, but source-only current morphism exclusion remains unsigned.",
            "runner_status": "STILL_BLOCKED_CURRENT_MORPHISM_MISSING",
            "source_path": str(sources["finite_runner_3621"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": timestamp and BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": "FRU3622_3_wEM_Phi",
            "coefficient": "w_EM;Phi_EM_boundary",
            "update": "direct source-bound acquisition is staged but not source-backed; runner remains blocked.",
            "runner_status": "STILL_BLOCKED_DIRECT_BOUND_MISSING",
            "source_path": str(output_paths()["source_bound_acquisition"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3622_0_TQ_NQ_result",
            "decision": "T_Q/N_Q has a clean conditional theorem: compact generator plus fixed parent fibre metric/norm would silence the inherited normalization branch.",
            "status": "PASS_CONDITIONAL_NOT_PARENT_SIGNED",
            "next_action": "try to derive the parent fibre metric/level/charge-lattice source path",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3622_1_countermodel",
            "decision": "Compact U(1) alone is insufficient: it fixes relative integer labels but not the coupling or base charge unit.",
            "status": "COUNTERMODEL_RETAINED",
            "next_action": "do not claim alpha/source calibration from charge quantization alone",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3622_2_bounds",
            "decision": "Direct w_EM and Phi_EM_boundary source-bound acquisition is staged but not acquired; finite runner stays blocked.",
            "status": "BOUND_ACQUISITION_STAGED_NOT_SOURCE_BACKED",
            "next_action": "either source direct bounds or attack no-flux/Hilbert source theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3622_3_next_target",
            "decision": "3623 should attack the parent fibre metric/level certificate or acquire direct w_EM/Phi bounds.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3623-Y5-R2FR-parent-fibre-level-certificate-or-wEM-Phi-bound-source.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3622_0",
            "result": "TQ_NQ_CONDITIONAL_THEOREM_NOT_SIGNED_BOUND_ACQUISITION_STAGED",
            "summary": "3622 derives the exact conditional T_Q/N_Q fibre-metric route and records why compact U(1) alone is insufficient; direct w_EM/Phi bounds are staged but not source-backed.",
            "TQ_NQ_parent_signed": False,
            "bound_acquisition_source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3622_0",
            "target_doc": "3623-Y5-R2FR-parent-fibre-level-certificate-or-wEM-Phi-bound-source.md",
            "target_script": "scripts/Y5_R2FR_3623_parent_fibre_level_certificate_or_wEM_Phi_bound_source.py",
            "objective": "try to source/derive a parent fibre metric, level, lattice index, or compact gauge certificate that fixes N_Q; if that fails, acquire direct source-backed bounds for w_EM and Phi_EM_boundary",
            "success_gate": "either N_Q is parent-fixed by an explicit certificate, or w_EM/Phi_EM_boundary receive direct source-backed numeric/nonclaim bound rows",
            "reason": "3622 proves compact charge labels alone are insufficient; the missing object is a fixed parent norm/level or empirical fallback bounds.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "TQ_NQ_route": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "compact_U1": "RELATIVE_LABELS_ONLY_NOT_COUPLING",
            "bounds": "wEM_Phi_STAGED_NOT_SOURCE_BACKED",
            "next_pressure_point": "parent_fibre_metric_level_certificate_or_direct_bounds",
            "claim_status": "NO_CLAIM",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3622 Y5 R2FR: T_Q/N_Q parent fibre metric or source-bound acquisition",
                "",
                "## Verdict",
                "- The `T_Q/N_Q` route is mathematically clean but not parent-signed.",
                "- Compact `U(1)` helps: it fixes relative integer charge labels.",
                "- Compact `U(1)` is not enough: it does not fix the base charge unit or Maxwell kinetic coefficient.",
                "- The missing object is a parent-fixed fibre metric, level, lattice index, symplectic form, or equivalent certificate fixing `N_Q=<T_Q,T_Q>_P`.",
                "",
                "## Conditional theorem",
                "- If `T_Q` is a compact parent generator and `G_P` is a fixed q-basic parent fibre metric, then:",
                "- `N_Q=G_P(T_Q,T_Q)` and `D_v N_Q=0`.",
                "- If the parent curvature norm is unique, `Z_Q=C_P N_Q`.",
                "- If the same Noether current owner and readout closure also hold, then the inherited normalization part of `lambda_F2`, `b_alpha`, and `kappa_J` collapses.",
                "",
                "## Countermodel retained",
                "- Integer labels `n_A` do not by themselves determine `Q_*`, `N_Q`, or `C_P N_Q`.",
                "- A fixed norm without no-extra-`F2` still permits `Z_Q=C_P N_Q+lambda_A`.",
                "- A Noether current without source-current morphism exclusion still permits `J_Q^readout=(1+kappa_J)J_Q`.",
                "",
                "## Bound acquisition",
                "- `w_EM`: direct source-weight/binding-energy bound is staged but not source-backed.",
                "- `Phi_EM_boundary`: stationary no-flux or numeric Poynting/H_tau flux bound is staged but not source-backed.",
                "- The finite runner remains blocked correctly.",
                "",
                "## Next target",
                "- `3623-Y5-R2FR-parent-fibre-level-certificate-or-wEM-Phi-bound-source.md`.",
                "- First try to derive/source a parent fibre metric/level/lattice certificate for `N_Q`.",
                "- Backup: acquire direct source-backed nonclaim bounds for `w_EM` and `Phi_EM_boundary`.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: conditional theorem plus staged acquisition ledger.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3622_0_sources_exist", sources_exist, "all required 3622 source paths exist"))
    results.append(("VAL3622_1_needles_found", needles_found, "all selected 3622 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3622_2_outputs_exist", outputs_exist, "all pre-validation 3622 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3622_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    theorem_rows = read_csv(paths["fibre_metric_theorem"]) if paths["fibre_metric_theorem"].exists() else []
    fixed_metric_written = any("N_Q=G_P(T_Q,T_Q)" in row["formula"] for row in theorem_rows)
    compact_limit_written = any(row["current_status"] == "LIMIT_PROVED_COUNTERMODEL_RETAINED" for row in theorem_rows)
    theorem_not_signed = bool(theorem_rows) and all(row["parent_signed"] == "False" for row in theorem_rows)
    results.append(("VAL3622_4_fixed_metric_formula_written", fixed_metric_written, "fixed fibre metric N_Q formula written"))
    results.append(("VAL3622_5_compactness_limit_written", compact_limit_written, "compact U1 limit/countermodel written"))
    results.append(("VAL3622_6_theorem_not_promoted", theorem_not_signed, "TQ/NQ theorem remains nonclaim"))

    acquisition_rows = read_csv(paths["source_bound_acquisition"]) if paths["source_bound_acquisition"].exists() else []
    has_wem = any(row["coefficient"] == "w_EM" for row in acquisition_rows)
    has_phi = any(row["coefficient"] == "Phi_EM_boundary" for row in acquisition_rows)
    acquisition_blocked = bool(acquisition_rows) and all(row["source_backed"] == "False" and row["score_ready"] == "False" for row in acquisition_rows)
    results.append(("VAL3622_7_wem_phi_acquisition_rows", has_wem and has_phi, "w_EM and Phi acquisition rows written"))
    results.append(("VAL3622_8_acquisition_nonclaim_blocked", acquisition_blocked, "bound acquisition remains staged/nonclaim"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3622_9_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3622*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3622 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3622_10_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["fibre_metric_theorem"], fibre_metric_theorem_rows())
    write_csv(paths["rescaling_countermodel"], rescaling_countermodel_rows())
    write_csv(paths["source_bound_acquisition"], source_bound_acquisition_rows())
    write_csv(paths["finite_runner_update"], finite_runner_update_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3622 validation failed: {failed}")
    print(f"wrote 3622 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
