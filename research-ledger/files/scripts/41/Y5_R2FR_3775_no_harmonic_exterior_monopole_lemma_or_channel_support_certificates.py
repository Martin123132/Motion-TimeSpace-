import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3775"
BRANCH = "MTS_R2FR_Y5_NO_HARMONIC_EXTERIOR_MONOPOLE_LEMMA_OR_CHANNEL_SUPPORT_CERTIFICATES_3775"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3775-Y5-R2FR-no-harmonic-exterior-monopole-lemma-or-channel-support-certificates.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3775_SOURCE_REGISTER.csv",
    "monopole_lemma": RESIDUALS / "P8_Y5_R2FR_3775_NO_HARMONIC_MONOPOLE_LEMMA.csv",
    "certificate_schema": RESIDUALS / "P8_Y5_R2FR_3775_CHANNEL_CERTIFICATE_SCHEMA.csv",
    "channel_certificates": RESIDUALS / "P8_Y5_R2FR_3775_CHANNEL_SUPPORT_CERTIFICATE_ATTEMPT.csv",
    "blocker_vector": RESIDUALS / "P8_Y5_R2FR_3775_CHANNEL_BLOCKER_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3775_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3775_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3775_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3775_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3775_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3775_0_3774_doc": PCW / "3774-Y5-R2FR-muextra-channel-zero-theorem-or-component-bound-vector.md",
        "SRC3775_1_3774_shell_identity": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_SHELL_BALANCE_IDENTITY.csv",
        "SRC3775_2_3774_zero_theorem": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_CHANNEL_ZERO_THEOREM.csv",
        "SRC3775_3_3774_component_bounds": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_COMPONENT_BOUND_VECTOR.csv",
        "SRC3775_4_3774_observable_matrix": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_OBSERVABLE_PROJECTION_MATRIX.csv",
        "SRC3775_5_3773_channels": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_CHANNEL_AUDIT.csv",
        "SRC3775_6_3760_EM_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3775_7_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3775_8_3771_theta_theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
        "SRC3775_9_3768_kappa_theorem": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_EH_COEFFICIENT_THEOREM.csv",
        "SRC3775_10_3769_shadow_theorem": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_ZERO_THEOREM.csv",
        "SRC3775_11_3762_range_locks": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_LOCKS.csv",
        "SRC3775_12_Hamiltonian_charge_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "SRC3775_13_Poisson_Gauss_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3775 no-harmonic monopole lemma and channel certificate input",
        }
        for source_id, path in source_paths().items()
    ]


def monopole_lemma_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "NHL3775_0_exterior_setup",
            "Let E_R be the observed local exterior outside a source surface S_Rc, with asymptotic or comparison surface S_R, and let each residual channel i induce a scalar monopole perturbation phi_i of the same observed potential used by the Gauss readout.",
            "This fixes the arena: no channel can affect measured GM unless it appears as an l=0 charge in this same observed exterior problem.",
            "SETUP",
        ),
        (
            "NHL3775_1_divergence_form",
            "Write the channel equation in the exterior as div A_i = rho_i^ext + div j_i + h_i, where h_i is the harmonic/cohomology representative not captured by local divergence data.",
            "Any local operator residual, projector leak, EM/Poynting stress, range source, kappa drift, or readout mismatch can be projected into this form after the 3774 shell split.",
            "EXACT_CONDITIONAL_DECOMPOSITION",
        ),
        (
            "NHL3775_2_monopole_coefficient",
            "The channel monopole is Q_i = Q_i^inner_extra + int_E rho_i^ext dV + int_boundary j_i dot dS + Q_i^harmonic_l0.",
            "Integrate the divergence equation over E_R and use Stokes. The inner term is the unmatched source-side contribution not already counted in M_H; the harmonic term is the coefficient of the exterior 1/r mode.",
            "EXACT_MONOPOLE_CHARGE_FORMULA",
        ),
        (
            "NHL3775_3_no_cancellation_zero",
            "Under the no-cancellation discipline, Q_i is zero only if each owner is individually zero or a parent action signs a protected cancellation: Q_i^inner_extra=0, int_E rho_i^ext=0, boundary flux=0, and Q_i^harmonic_l0=0.",
            "This prevents tuning a positive EM exterior energy against a negative boundary or range charge and calling it a derivation.",
            "EXACT_NO_CANCELLATION_ZERO_CRITERION",
        ),
        (
            "NHL3775_4_same_source_inclusion",
            "If a channel is physically real but is varied inside the same descended Hilbert source, its contribution belongs to M_H rather than mu_extra.",
            "This is the proper way to handle EM field energy, binding energy, apparatus energy, and interior source normalization: include them in total stress, do not delete them.",
            "EXACT_SOURCE_INCLUSION_RULE",
        ),
        (
            "NHL3775_5_support_falloff_rule",
            "If a channel has no unmatched inner charge, no exterior support, only exact-divergence flux that decays faster than 1/r^2 or cancels on homologous surfaces, and no harmonic l=0 class, then it cannot change measured GM.",
            "The exterior potential then has no 1/r coefficient from that channel, so it may alter higher multipoles or gauge data but not the Newtonian monopole.",
            "EXACT_NO_HARMONIC_MONOPOLE_LEMMA",
        ),
        (
            "NHL3775_6_failure_mode",
            "If any of inner_extra, exterior_volume, boundary_flux, or harmonic_l0 remains unsigned, the channel is not disproved; it becomes a component bound row Q_i/M_H.",
            "This converts failed derivation into a finite empirical task rather than a vague theory hole.",
            "EXACT_BOUND_FALLBACK",
        ),
    ]
    return [
        {
            **base(timestamp),
            "lemma_id": lemma_id,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "claim_allowed": False,
        }
        for lemma_id, statement, derivation, status in rows
    ]


def certificate_schema_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CERT3775_A_same_source", "same_source_inclusion", "channel is varied inside the same descended Hilbert/coframe source M_H", "moves physical stress into M_H instead of mu_extra"),
        ("CERT3775_B_inner_zero", "zero_inner_extra_monopole", "unmatched interior source-side monopole is zero", "prevents hidden active-mass shifts inside the source surface"),
        ("CERT3775_C_ext_zero", "zero_exterior_volume_support", "exterior residual density has zero l=0 volume integral", "kills exterior shell source"),
        ("CERT3775_D_flux_zero", "zero_boundary_flux", "exact-divergence/current flux vanishes on homologous exterior boundaries", "kills boundary/reference/projector flux"),
        ("CERT3775_E_harmonic_zero", "zero_harmonic_l0", "no exterior cohomology or homogeneous 1/r mode survives", "kills invisible harmonic monopole hair"),
        ("CERT3775_F_bound_ready", "bound_ready", "numeric or source-backed symbolic bound exists for the remaining Q_i", "fallback if zero proof fails"),
    ]
    return [
        {
            **base(timestamp),
            "certificate_id": certificate_id,
            "certificate": certificate,
            "definition": definition,
            "role": role,
            "claim_allowed": False,
        }
        for certificate_id, certificate, definition, role in rows
    ]


def channel_certificate_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "CCA3775_0_boundary_reference",
            "Q_boundary_ref",
            "reference/boundary Hamiltonian term",
            "not_physical_source",
            "not_applicable",
            "not_applicable",
            "MISSING_FIXED_REFERENCE_ZERO_FLUX",
            "MISSING_REFERENCE_HARMONIC_SILENCE",
            "MISSING_FIXED_REFERENCE_INTEGRABILITY_COMPONENT",
            "Boundary channel can be killed by fixed reference + integrability, but current contract does not sign it.",
        ),
        (
            "CCA3775_1_projector_domain",
            "Q_projector_domain",
            "projector commutator or domain-wall flux",
            "not_physical_source",
            "MISSING_NO_DOMAIN_WALL_INNER_CHARGE",
            "MISSING_PROJECTOR_COMMUTATOR_L0_VOLUME_ZERO",
            "MISSING_PROJECTOR_BOUNDARY_FLUX_ZERO",
            "MISSING_PROJECTOR_HARMONIC_L0_ZERO",
            "MISSING_PROJECTOR_COMMUTATOR_DOMAIN_WALL_COMPONENT",
            "Needs Pi_M to commute with exterior divergence and source domain to be material/comoving.",
        ),
        (
            "CCA3775_2_nonEH_operator",
            "Q_nonEH",
            "non-EH exterior operator residual",
            "not_physical_source",
            "MISSING_NON_EH_INTERIOR_MONOPOLE_ZERO_OR_INCLUSION",
            "MISSING_NON_EH_EXTERIOR_L0_VOLUME_ZERO",
            "MISSING_NON_EH_BOUNDARY_FLUX_ZERO",
            "MISSING_NON_EH_HARMONIC_L0_ZERO",
            "MISSING_NON_EH_L0_OPERATOR_COMPONENT",
            "Needs local EH/Poisson to be parent-derived in the l=0 exterior sector.",
        ),
        (
            "CCA3775_3_memory_bulk",
            "Q_memory_bulk",
            "memory/topological exterior charge",
            "not_physical_source",
            "MISSING_MEMORY_INTERIOR_CLASS_ZERO",
            "MISSING_MEMORY_VOLUME_ZERO",
            "MISSING_MEMORY_BOUNDARY_FLUX_ZERO",
            "MISSING_MEMORY_COHOMOLOGY_L0_ZERO",
            "MISSING_MEMORY_TOPOLOGICAL_HARMONIC_MONOPOLE_COMPONENT",
            "Needs a cohomology/support certificate; local exactness alone is insufficient if a global charge remains.",
        ),
        (
            "CCA3775_4_range",
            "Q_range",
            "finite-range or unscreened mediator",
            "not_in_Hilbert_source_unless_parent_signed",
            "MISSING_RANGE_SOURCE_CHARGE_ZERO",
            "MISSING_RANGE_EXTERIOR_L0_PROFILE_ZERO",
            "MISSING_RANGE_BOUNDARY_KERNEL_FLUX_ZERO",
            "MISSING_UNSCREENED_HARMONIC_OR_YUKAWA_L0_ZERO",
            "MISSING_RANGE_SOURCE_CHARGE_AND_BOUND_CURVE_COMPONENTS",
            "Needs no-mediator/no-source-charge theorem or a real alpha(lambda) bound curve with source charges.",
        ),
        (
            "CCA3775_5_coupling_kappa",
            "Q_delta_kappa",
            "G_eff/kappa reweighting between source and readout",
            "not_physical_source",
            "MISSING_KAPPA_INTERIOR_SOURCE_NORMALIZATION_ZERO",
            "MISSING_KAPPA_EXTERIOR_GRADIENT_ZERO",
            "MISSING_KAPPA_BOUNDARY_CALIBRATION_FLUX_ZERO",
            "MISSING_KAPPA_HARMONIC_L0_ZERO",
            "9.6e-15 yr^-1 envelope imported, dimensionless projection missing",
            "Gdot bound is wired, but the spatial/source/readout projection coefficient is not signed.",
        ),
        (
            "CCA3775_6_readout_frame",
            "Q_readout_frame",
            "orbit/readout frame mismatch",
            "not_physical_source",
            "MISSING_READOUT_INNER_CALIBRATION_ZERO",
            "MISSING_READOUT_EXTERIOR_VOLUME_ZERO",
            "MISSING_READOUT_BOUNDARY_FLUX_ZERO",
            "MISSING_READOUT_HARMONIC_L0_ZERO",
            "MISSING_ORBITAL_FRAME_READOUT_COMPONENT",
            "Needs slow-orbit geodesic readout in the same q_obs potential as the flux definition.",
        ),
        (
            "CCA3775_7_EM_Poynting",
            "Q_EM_Poynting",
            "EM field energy and Poynting momentum",
            "MISSING_EM_TOTAL_HILBERT_SOURCE_INCLUSION",
            "MISSING_EM_INTERIOR_BINDING_MONOPOLE_INCLUSION_OR_ZERO",
            "MISSING_EM_EXTERIOR_L0_STRESS_ZERO",
            "MISSING_EM_POYNTING_BOUNDARY_FLUX_ZERO",
            "MISSING_EM_HARMONIC_L0_ZERO",
            "MISSING_EM_HILBERT_DESCENT_OR_EXTERIOR_L0_STRESS_COMPONENT",
            "EM is the dangerous honest channel: its stress is real, so the clean route is inclusion in the same total Hilbert source, not deletion.",
        ),
        (
            "CCA3775_8_source_theta",
            "Q_source_theta",
            "source action and constants/material marker leakage",
            "MISSING_SOURCE_THETA_HILBERT_INCLUSION",
            "MISSING_SOURCE_THETA_INTERIOR_MONOPOLE_ZERO",
            "MISSING_SOURCE_THETA_EXTERIOR_SUPPORT_ZERO",
            "MISSING_SOURCE_THETA_BOUNDARY_FLUX_ZERO",
            "MISSING_SOURCE_THETA_HARMONIC_L0_ZERO",
            "MISSING_NEWTON_SOURCE_THETA_PROJECTION_COMPONENT",
            "This is the hidden active-mass route: source/theta leakage must descend through q_obs or be bounded.",
        ),
    ]
    output = []
    for row in rows:
        (
            certificate_id,
            channel,
            description,
            same_source_inclusion,
            zero_inner_extra_monopole,
            zero_exterior_volume_support,
            zero_boundary_flux,
            zero_harmonic_l0,
            bound_status,
            conclusion,
        ) = row
        certificates = [
            same_source_inclusion,
            zero_inner_extra_monopole,
            zero_exterior_volume_support,
            zero_boundary_flux,
            zero_harmonic_l0,
        ]
        channel_closed = all(value in {"not_applicable", "SIGNED"} for value in certificates)
        output.append(
            {
                **base(timestamp),
                "certificate_attempt_id": certificate_id,
                "channel": channel,
                "description": description,
                "same_source_inclusion": same_source_inclusion,
                "zero_inner_extra_monopole": zero_inner_extra_monopole,
                "zero_exterior_volume_support": zero_exterior_volume_support,
                "zero_boundary_flux": zero_boundary_flux,
                "zero_harmonic_l0": zero_harmonic_l0,
                "bound_status": bound_status,
                "channel_closed": channel_closed,
                "conclusion": conclusion,
                "claim_allowed": False,
            }
        )
    return output


def blocker_vector_rows(timestamp: str, certificates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in certificates:
        blockers = [
            row["same_source_inclusion"],
            row["zero_inner_extra_monopole"],
            row["zero_exterior_volume_support"],
            row["zero_boundary_flux"],
            row["zero_harmonic_l0"],
            row["bound_status"],
        ]
        missing = [str(item) for item in blockers if str(item).startswith("MISSING_")]
        rows.append(
            {
                **base(timestamp),
                "blocker_id": row["certificate_attempt_id"].replace("CCA", "CBV"),
                "channel": row["channel"],
                "missing_count": len(missing),
                "missing_items": ";".join(missing),
                "best_next_action": best_next_action(str(row["channel"])),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def best_next_action(channel: str) -> str:
    actions = {
        "Q_boundary_ref": "derive fixed-reference/integrability silence",
        "Q_projector_domain": "derive Pi_M divergence-commutation and material-domain wall zero",
        "Q_nonEH": "derive local EH/Poisson l=0 exterior operator from parent action",
        "Q_memory_bulk": "derive cohomology/no-harmonic memory certificate",
        "Q_range": "derive no mediator/source charge or source-backed alpha(lambda)",
        "Q_delta_kappa": "derive q_obs-owned/superselected kappa plus spatial projection",
        "Q_readout_frame": "derive slow-orbit same-potential readout",
        "Q_EM_Poynting": "derive EM/Poynting inclusion in same total Hilbert source",
        "Q_source_theta": "derive source/theta descent for zero interior extra monopole",
    }
    return actions.get(channel, "derive or bound channel")


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    lemma_emitted = any(row["lemma_id"] == "NHL3775_5_support_falloff_rule" for row in grouped["monopole_lemma"])
    charge_formula = any(row["lemma_id"] == "NHL3775_2_monopole_coefficient" for row in grouped["monopole_lemma"])
    all_channels_present = len(grouped["channel_certificates"]) == 9
    all_closed = all(row["channel_closed"] is True for row in grouped["channel_certificates"])
    em_honest = any(row["channel"] == "Q_EM_Poynting" and "inclusion" in str(row["conclusion"]) for row in grouped["channel_certificates"])
    blockers_exist = any(int(row["missing_count"]) > 0 for row in grouped["blocker_vector"])
    rows = [
        ("CG3775_0_sources", "all 3775 source paths exist", sources_exist, "path hygiene"),
        ("CG3775_1_monopole_formula", "exact Q_i monopole coefficient formula emitted", charge_formula, "inner/exterior/flux/harmonic owners separated"),
        ("CG3775_2_no_harmonic_lemma", "support/falloff no-harmonic lemma emitted", lemma_emitted, "real zero route exists"),
        ("CG3775_3_channel_certificates", "all nine channels receive certificate attempts", all_channels_present, "no channel skipped"),
        ("CG3775_4_EM_honesty", "EM/Poynting is treated as real stress needing inclusion or bound", em_honest, "not deleted by language"),
        ("CG3775_5_all_channels_closed", "all channels are closed by certificates", all_closed, "expected false in current branch"),
        ("CG3775_6_blockers_explicit", "missing certificates remain blockers", blockers_exist, "no claim with unsigned channels"),
        ("CG3775_7_Newton_GM_claim", "measured-GM Newton claim allowed", False, "blocked until channel certificates or numeric bounds close"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3775_0", "The exact monopole formula is Q_i=Q_i^inner_extra+int_E rho_i^ext dV+boundary flux+Q_i^harmonic_l0.", "use this as the required certificate format for every local-GR channel"),
        ("DEC3775_1", "Compact exterior falloff alone is not enough: hidden interior monopoles still shift measured GM unless they are in M_H or zero.", "prioritize same-Hilbert-source inclusion for EM, binding, source, and theta terms"),
        ("DEC3775_2", "EM/Poynting is not a nuisance to erase; it is a real stress-energy owner and should be absorbed into the total Hilbert source if the route is to look like GR.", "attack EM/source inclusion next"),
        ("DEC3775_3", "No current Q_i channel is closed; this is not a failure of the route but a precise proof contract.", "do not claim Newton/local-GR until certificates or numeric bounds close"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3775_0",
            "target_doc": "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md",
            "target_script": "scripts/Y5_R2FR_3776_total_Hilbert_source_inclusion_EM_Poynting_and_interior_monopole_closure.py",
            "objective": "derive whether EM/Poynting stress, binding energy, source action, and constants/material markers are included in the same total Hilbert source so their interior/exterior monopoles move into M_H instead of mu_extra",
            "reason": "3775 proves exterior falloff alone cannot close hidden mass; the clean GR-like route is total-source inclusion rather than deleting real stress-energy",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "NO_HARMONIC_MONOPOLE_LEMMA_DERIVED_CERTIFICATE_MATRIX_EMITTED_NOT_CLOSED",
            "summary": "3775 derives the exact channel monopole law: each Q_i splits into unmatched interior extra monopole, exterior volume support, boundary flux, and harmonic l=0 charge. The no-harmonic lemma is real: if all four owners vanish, or the physical stress is included in the same Hilbert source, that channel cannot alter measured GM. The current branch does not close any full channel certificate; the next high-value route is total Hilbert-source inclusion, especially for EM/Poynting and source/theta interior monopoles.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3775 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3775 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("monopole_formula", "Q_i inner/exterior/flux/harmonic formula emitted", any(row["lemma_id"] == "NHL3775_2_monopole_coefficient" for row in grouped["monopole_lemma"])),
        ("no_cancellation", "no-cancellation zero criterion emitted", any(row["lemma_id"] == "NHL3775_3_no_cancellation_zero" for row in grouped["monopole_lemma"])),
        ("support_lemma", "no-harmonic support/falloff lemma emitted", any(row["lemma_id"] == "NHL3775_5_support_falloff_rule" for row in grouped["monopole_lemma"])),
        ("schema_complete", "six certificate schema rows emitted", len(grouped["certificate_schema"]) == 6),
        ("channels_complete", "all nine channels have certificate attempts", len(grouped["channel_certificates"]) == 9),
        ("em_inclusion_flagged", "EM/Poynting requires inclusion or bound", any(row["channel"] == "Q_EM_Poynting" and "MISSING_EM_TOTAL_HILBERT_SOURCE_INCLUSION" in row["same_source_inclusion"] for row in grouped["channel_certificates"])),
        ("no_channel_claimed", "no channel is currently closed", all(row["channel_closed"] is False for row in grouped["channel_certificates"])),
        ("blockers_explicit", "blocker vector has missing items for every channel", all(int(row["missing_count"]) > 0 for row in grouped["blocker_vector"])),
        ("next_target", "3776 total Hilbert source inclusion target emitted", grouped["next_target"][0]["target_doc"] == "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md"),
        ("no_formalization_leak", "no 3775 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3775*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3775 - No-Harmonic Exterior Monopole Lemma Or Channel Support Certificates",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3775 tightens the whole local-GR route. The thing that can spoil Newtonian measured `GM` is not mystical: every channel has four owners: unmatched interior monopole, exterior volume support, boundary flux, and harmonic `1/r` hair. Kill those, or include the real stress in the same Hilbert source, and the channel cannot move `GM`. Fail that, and it becomes a bound row.",
        "",
        "## No-Harmonic Monopole Lemma",
    ]
    for row in grouped["monopole_lemma"]:
        lines.append(f"- `{row['lemma_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Certificate Schema"])
    for row in grouped["certificate_schema"]:
        lines.append(f"- `{row['certificate_id']}` `{row['certificate']}`: {row['definition']} Role: {row['role']}.")
    lines.extend(["", "## Channel Certificate Attempt"])
    for row in grouped["channel_certificates"]:
        lines.append(
            f"- `{row['certificate_attempt_id']}` `{row['channel']}` closed=`{row['channel_closed']}`: "
            f"same_source=`{row['same_source_inclusion']}`, inner=`{row['zero_inner_extra_monopole']}`, "
            f"exterior=`{row['zero_exterior_volume_support']}`, flux=`{row['zero_boundary_flux']}`, "
            f"harmonic=`{row['zero_harmonic_l0']}`. Conclusion: {row['conclusion']}"
        )
    lines.extend(["", "## Blocker Vector"])
    for row in grouped["blocker_vector"]:
        lines.append(f"- `{row['blocker_id']}` `{row['channel']}` missing=`{row['missing_count']}`: {row['best_next_action']}.")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    channel_certificates = channel_certificate_rows(timestamp)
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "monopole_lemma": monopole_lemma_rows(timestamp),
        "certificate_schema": certificate_schema_rows(timestamp),
        "channel_certificates": channel_certificates,
        "blocker_vector": blocker_vector_rows(timestamp, channel_certificates),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["monopole_lemma"], grouped["monopole_lemma"])
    write_csv(OUTPUTS["certificate_schema"], grouped["certificate_schema"])
    write_csv(OUTPUTS["channel_certificates"], grouped["channel_certificates"])
    write_csv(OUTPUTS["blocker_vector"], grouped["blocker_vector"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3775 validation failed: {failures}")
    print("wrote 3775 checkpoint: no-harmonic monopole lemma and channel certificates emitted")


if __name__ == "__main__":
    main()
