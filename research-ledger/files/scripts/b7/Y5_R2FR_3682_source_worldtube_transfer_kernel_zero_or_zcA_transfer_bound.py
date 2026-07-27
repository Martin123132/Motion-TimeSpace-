from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3682"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_WORLDTUBE_TRANSFER_KERNEL_ZERO_OR_ZCA_TRANSFER_BOUND_3682"
DOC = ROOT / "3682-Y5-R2FR-source-worldtube-transfer-kernel-zero-or-zcA-transfer-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3681", RESIDUALS / "P8_Y5_R2FR_3681_NEXT_TARGET.csv", "z_cA_transfer", "3681 selected source-worldtube transfer as next throat"),
        ("split_3681", RESIDUALS / "P8_Y5_R2FR_3681_ZCA_POST_SPLIT_ROWS.csv", "CAS3681_1_transfer", "3681 reduced post-current c_A to transfer plus reentry"),
        ("theorem_1817", RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv", "KWT1817_1_downstream_linearity", "conditional fixed downstream K_arena theorem attempt"),
        ("audit_1817", RESIDUALS / "P8_Y5_PARENT_QLOC_1817_ARENA_TRANSFER_AUDIT.csv", "ATA1817_5_verdict", "arena transfer kernels not closed in 1817"),
        ("acq_1817", RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_TRANSFER_ACQUISITION_LEDGER.csv", "ACQ1817_2_Hilbert_charge_identity", "source transfer ledger identifies Hilbert charge identity as a hard missing input"),
        ("readout_1802", RESIDUALS / "P8_Y5_PARENT_QLOC_1802_READOUT_TYPE_SPLIT.csv", "RTS1802_0_pure_postprocessing", "pure postprocessing is typed separately from pre-action/readout feedback"),
        ("gate_1802", RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv", "MRT1802_5_general_readout", "general readout no-reentry remains blocked"),
        ("vbr_1454", RESIDUALS / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv", "VBR1454_5_official_readout_gap", "R10 variation-before-readout still lacks official arrays/design map"),
        ("slot_1451", RESIDUALS / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv", "OG1451_6_verdict", "source-only slot theorem remains unsigned"),
        ("slot_matrix_1451", RESIDUALS / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv", "SM1451_6_verdict", "source-only slot countermodels remain active"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def fixed_kernel_theorem_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "FKT3682_0_target",
            "prove full z_cA_transfer,A = 0",
            "Full transfer zero would require fixed downstream kernel, fixed worldtube support, fixed normalizer/calibration, no readout feedback, and Hilbert-source charge identity.",
            "FULL_TRANSFER_ZERO_NOT_PROVED",
            "only the fixed downstream kernel subslot can be zeroed by type alone",
            False,
        ),
        (
            "FKT3682_1_fixed_linear_downstream",
            "fixed downstream linear K_arena has no Xhat amplitude derivative",
            "If K_arena is a fixed linear post-solution map from solved parent current to reported arena data, independent of Xhat, varied fields, source labels, support choice, calibration, and effective action, then D_Xhat ln K_arena = 0.",
            "EXACT_TYPED_FIXED_KERNEL_ZERO",
            "z_Kfixed,A = 0 under the typed fixed-kernel contract",
            True,
        ),
        (
            "FKT3682_2_normalization_preserving_clause",
            "normalization-preserving postprocessing does not create source coupling",
            "If int K_arena[J] = int J in the arena normalizer and the normalizer is fixed independently of Xhat, K_arena can reshape readout bins but cannot supply a source-strength coefficient.",
            "CONDITIONAL_NORMALIZER_ZERO_CLAUSE",
            "keeps z_Knorm,A zero only when the normalizer certificate is supplied",
            True,
        ),
        (
            "FKT3682_3_support_choice_survives",
            "worldtube/source support choice is not killed by fixed-linearity alone",
            "If the support map W_A, source worldtube, boundary truncation, or material label changes with Xhat, the arena report can acquire D_Xhat ln W_A even when K_arena is linear.",
            "SUPPORT_RESIDUAL_RETAINED",
            "z_Ksupport,A remains live",
            False,
        ),
        (
            "FKT3682_4_calibration_feedback_survives",
            "calibration/readout feedback is not killed by fixed-linearity alone",
            "If K_arena depends on fitted calibration, measured-G normalization, readout thresholds, or fields varied in the parent action, [D_Xhat,K_arena]J can be nonzero.",
            "FEEDBACK_AND_NORMALIZATION_RESIDUAL_RETAINED",
            "z_Knorm,A and z_Kfeedback,A remain live unless separately signed",
            False,
        ),
        (
            "FKT3682_5_Hilbert_charge_identity_gap",
            "source charge used by Newton/GR arenas is not yet parent-owned",
            "G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc is the required bridge; without R_Hsrc=0 or a bound, source mass can still be imported by readout.",
            "R_HSRC_IDENTITY_MISSING",
            "z_RHsrc,A becomes the hard next component",
            False,
        ),
        (
            "FKT3682_6_verdict",
            "current corpus proves z_cA_transfer,A = 0",
            "The fixed downstream piece is zero by typed contract, but support, normalizer, feedback and Hilbert-source identity are not signed.",
            "FULL_ZCA_TRANSFER_ZERO_NOT_PROVED_FIXED_SUBSLOT_ZERO",
            "reduce z_cA_transfer to physical residual pieces instead of calling it solved",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "theorem_zero_subslot": theorem_zero_subslot,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for theorem_id, claim, mathematical_statement, status, consequence, theorem_zero_subslot in specs
    ]


def transfer_split_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZTR3682_0_fixed_kernel",
            "z_Kfixed,A",
            "0",
            "fixed linear downstream normalization-preserving postprocessing kernel",
            "EXACT_TYPED_FIXED_KERNEL_ZERO",
            "dimensionless transfer fraction",
            "FKT3682_1_fixed_linear_downstream",
            "this is the real bite: a pure fixed readout kernel cannot be a hidden source coefficient",
            0,
        ),
        (
            "ZTR3682_1_support",
            "z_Ksupport,A",
            "D_Xhat ln W_A[source worldtube, boundary, support]",
            "source-worldtube/support selection and boundary truncation",
            "MISSING_WORLDTUBE_SUPPORT_THEOREM_OR_BOUND",
            "dimensionless support fraction",
            "KWT1817_2_worldtube_support;ATA1817_1_WEP",
            "must be parent-signed or source-bounded before WEP/PPN/Newton claims",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_2_normalizer",
            "z_Knorm,A",
            "D_Xhat ln N_A[arena normalizer, measured-G, calibration]",
            "arena/source normalization and calibration map",
            "MISSING_NORMALIZATION_CALIBRATION_CERTIFICATE",
            "dimensionless normalizer fraction",
            "RTS1802_4_calibration_feedback;ATA1817_3_PPN_orbit",
            "the path where G_ref or GM-like calibration can sneak in",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_3_feedback",
            "z_Kfeedback,A",
            "||[D_Xhat,K_arena]J_parent||/||K_arena[J_parent]||",
            "field-dependent readout, projector, or effective-action feedback",
            "MISSING_NO_FEEDBACK_COMMUTATOR_OR_BOUND",
            "dimensionless commutator fraction",
            "RTS1802_2_projector_domain;MRT1802_5_general_readout",
            "zero only for genuinely fixed postprocessing",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_4_RHsrc",
            "z_RHsrc,A",
            "||R_Hsrc||/||Pi_M^H J_H^dress||",
            "failure of Hilbert dressed source current to equal arena source charge",
            "MISSING_HILBERT_CHARGE_IDENTITY_OR_BOUND",
            "dimensionless source-identity fraction",
            "KWT1817_3_charge_source_identity;ACQ1817_2_Hilbert_charge_identity",
            "this is the main GR/Newton source bridge",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_5_transfer_reduced",
            "z_cA_transfer,A",
            "z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A",
            "post-fixed-kernel transfer component",
            "REDUCED_FIXED_KERNEL_SUBSLOT_REMOVED",
            "dimensionless transfer fraction",
            "ZTR3682_1_support;ZTR3682_2_normalizer;ZTR3682_3_feedback;ZTR3682_4_RHsrc",
            "no cancellation allowed between live residual pieces",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_6_post_current_total",
            "z_cA_post,A",
            "z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A + z_cA_reentry,A",
            "3681 post-current component after fixed-kernel subslot removal",
            "UPDATED_TRANSFER_REENTRY_VECTOR",
            "dimensionless current/readout fraction",
            "CAS3681_3_post_current_total;ZTR3682_5_transfer_reduced",
            "parent-source c_A and fixed pure readout kernel are removed; physical residuals remain",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "ZTR3682_7_zg_core_update",
            "z_g_core,A",
            "z_Qstar + z_lattice,A + z_Noether,A + z_readout,A + z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A + z_cA_reentry,A",
            "direct current normalization vector after fixed-kernel transfer reduction",
            "UPDATED_NO_CANCELLATION_VECTOR",
            "dimensionless canonical derivative",
            "ZTR3682_6_post_current_total",
            "the current-coupling debt is now explicit enough to attack piecewise",
            "MISSING_COMPONENT_VALUE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for split_id, symbol, formula_or_value, meaning, status, units, source_anchor, interpretation, numeric_value in specs:
        rows.append(
            {
                **base(ts),
                "split_id": split_id,
                "symbol": symbol,
                "formula_or_value": formula_or_value,
                "meaning": meaning,
                "status": status,
                "units": units,
                "source_anchor": source_anchor,
                "interpretation": interpretation,
                "numeric_value": numeric_value,
                "valid_for_claim": False,
                "claim_allowed": False,
                "score_ready": False,
            }
        )
    return rows


def component_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "KCB3682_0_fixed_kernel_zero",
            "z_Kfixed,A",
            "0",
            "dimensionless transfer fraction",
            "typed theorem zero for fixed linear downstream normalization-preserving postprocessing",
            "FKT3682_1_fixed_linear_downstream",
        ),
        (
            "KCB3682_1_support_bound",
            "abs(z_Ksupport,A)",
            "MISSING_WORLDTUBE_SUPPORT_BOUND_VALUE",
            "dimensionless support fraction",
            "needs source-worldtube/support map, boundary convention and Xhat derivative",
            "MISSING_SOURCE_WORLDTUBE_SUPPORT_PATH",
        ),
        (
            "KCB3682_2_normalizer_bound",
            "abs(z_Knorm,A)",
            "MISSING_NORMALIZER_BOUND_VALUE",
            "dimensionless normalizer fraction",
            "needs arena normalizer/calibration certificate and measured-G/GM ownership",
            "MISSING_ARENA_NORMALIZER_SOURCE_PATH",
        ),
        (
            "KCB3682_3_feedback_bound",
            "abs(z_Kfeedback,A)",
            "MISSING_FEEDBACK_COMMUTATOR_BOUND_VALUE",
            "dimensionless commutator fraction",
            "needs no-feedback theorem or response matrix bound for [D_Xhat,K_arena]",
            "MISSING_READOUT_FEEDBACK_SOURCE_PATH",
        ),
        (
            "KCB3682_4_RHsrc_identity",
            "R_Hsrc",
            "G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H",
            "source-current residual with arena units inherited from Q_tau",
            "identity row for the Newton/GR source bridge; must be zeroed or norm-bounded",
            "ACQ1817_2_Hilbert_charge_identity",
        ),
        (
            "KCB3682_5_RHsrc_bound",
            "abs(z_RHsrc,A)",
            "MISSING_RHSRC_BOUND_VALUE",
            "dimensionless source-identity fraction",
            "needs norm of R_Hsrc relative to Pi_M^H J_H^dress and boundary flux dB_H",
            "MISSING_HILBERT_CHARGE_IDENTITY_SOURCE_PATH",
        ),
        (
            "KCB3682_6_transfer_envelope",
            "abs(z_cA_transfer,A)",
            "abs(z_Ksupport,A)+abs(z_Knorm,A)+abs(z_Kfeedback,A)+abs(z_RHsrc,A)",
            "absolute no-cancellation envelope",
            "fixed kernel is removed; remaining transfer must be bounded componentwise",
            "ZTR3682_5_transfer_reduced",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": "THEOREM_ZERO_SUBSLOT_NONCLAIM" if bound_id == "KCB3682_0_fixed_kernel_zero" else "INPUT_REQUIRED_NONCLAIM",
            "interpretation": interpretation,
            "source_path_or_missing": source_path_or_missing,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, interpretation, source_path_or_missing in specs
    ]


def arena_acquisition_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "ACQ3682_0_WEP_worldtube_support",
            "WEP/MICROSCOPE",
            "z_Ksupport,A",
            "source-intake/microscope/source_worldtube/P_WEP_R_source_Earth_worldtube.csv",
            "dimensionless support derivative",
            "Earth/source worldtube support and material label map",
            "MISSING_SOURCE_PATH_FROM_1817_LEDGER",
        ),
        (
            "ACQ3682_1_WEP_official_readout_kernel",
            "WEP/MICROSCOPE",
            "z_Kfeedback,A",
            "source-intake/microscope/official_readout/P_WEP_K_CMSM_readout.csv",
            "dimensionless readout commutator",
            "official design/readout kernel and no-feedback certificate",
            "MISSING_SOURCE_PATH_FROM_1817_LEDGER",
        ),
        (
            "ACQ3682_2_R10_profile_kernel",
            "R10 short-range gravity",
            "z_Ksupport,A;z_Knorm,A",
            "source-intake/R10/P_R10_kernel_profile_bound_inputs.csv",
            "dimensionless transfer fraction",
            "R10 density profile, separation kernel, lambda/alpha bound normalizer",
            "MISSING_R10_KERNEL_AND_PROFILE_INPUTS",
        ),
        (
            "ACQ3682_3_PPN_orbital_response",
            "PPN/orbital/Newton",
            "z_RHsrc,A;z_Knorm,A",
            "source-intake/ppn/P_PPN_orbital_response_matrix.csv",
            "dimensionless source-identity fraction",
            "GM/G_ref ownership, orbital response matrix, Hilbert charge bridge",
            "MISSING_PPN_RESPONSE_AND_HILBERT_CHARGE_IDENTITY",
        ),
        (
            "ACQ3682_4_clock_EM_transfer",
            "clock/EM/fine-structure",
            "z_Kfeedback,A;z_Knorm,A",
            "source-intake/clocks/P_clock_EM_transfer_normalizer.csv",
            "dimensionless clock/source transfer",
            "clock transfer normalizer, tau_clock, EM owner and no-feedback map",
            "MISSING_TAU_CLOCK_EM_OWNER_AND_TRANSFER_MAP",
        ),
        (
            "ACQ3682_5_parent_Hilbert_charge_identity",
            "parent GR/Newton bridge",
            "R_Hsrc",
            "source-intake/parent/P_Hilbert_worldtube_charge_identity.csv",
            "arena source-current units",
            "G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc with R_Hsrc=0 or finite norm",
            "MISSING_PARENT_IDENTITY_PROOF_OR_BOUND",
        ),
    ]
    return [
        {
            **base(ts),
            "acquisition_id": acquisition_id,
            "arena": arena,
            "target_component": target_component,
            "needed_source_path": needed_source_path,
            "units": units,
            "normalizer_or_content": normalizer_or_content,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for acquisition_id, arena, target_component, needed_source_path, units, normalizer_or_content, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3682_0_reduction",
            "fixed pure downstream kernel subslot is theorem-zero",
            "REAL_REDUCTION",
            "a fixed linear normalization-preserving postprocessing map cannot create D_Xhat ln source strength",
            "remove z_Kfixed,A from z_cA_transfer,A",
        ),
        (
            "DEC3682_1_not_full_zero",
            "full z_cA_transfer,A is not theorem-zero",
            "SUPPORT_NORMALIZER_FEEDBACK_RHSRC_RETAINED",
            "worldtube support, calibration normalizer, readout feedback and Hilbert-source identity are independent physical routes",
            "carry those components forward explicitly",
        ),
        (
            "DEC3682_2_next_route",
            "Hilbert worldtube charge identity is now the best next throat",
            "NEXT_BEST_TARGET",
            "R_Hsrc is the piece that decides whether Newton/GR source mass is derived from parent Hilbert current or imported by arena readout",
            "derive R_Hsrc=0 or write a bound row",
        ),
        (
            "DEC3682_3_claim_discipline",
            "no WEP/R10/PPN/clock/local-GR claim",
            "PRIVATE_NONCLAIM",
            "a fixed-kernel subslot zero is not a calibrated source universality theorem",
            "continue privately",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3682_0_full_transfer_zero", "claim z_cA_transfer,A=0", "BLOCKED_RESIDUAL_COMPONENTS", "support, normalizer, feedback and R_Hsrc remain unsigned"),
        ("CG3682_1_source_universality", "claim Newton/GR source universality", "BLOCKED_RHSRC_AND_NORMALIZER", "G_ref^-1 Q_tau bridge is missing and calibration ownership remains live"),
        ("CG3682_2_local_arena_pass", "claim WEP/R10/PPN/clock pass", "BLOCKED_ARENA_KERNEL_INPUTS", "arena-specific official readout kernels and normalizers are missing"),
        ("CG3682_3_zg_zero_or_alpha_direct", "treat alpha/clock as direct s_XF2 bound", "BLOCKED_ZG_COMPONENTS_LIVE", "z_g core still includes live source/readout transfer pieces"),
        ("CG3682_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "FIXED_TRANSFER_KERNEL_SUBSLOT_ZERO_FULL_TRANSFER_BLOCKED_RHSRC_NEXT_NONCLAIM",
            "summary": "3682 proves the narrow typed subcase: a fixed linear downstream normalization-preserving K_arena has D_Xhat ln K_arena=0 and cannot be a hidden source coefficient. The full z_cA_transfer zero is not proved because support, normalizer, feedback and Hilbert-source identity remain live.",
            "claim_ceiling": "no z_cA_transfer zero, z_g zero, Newton/GR source universality, WEP/R10/PPN/clock pass, direct alpha bound, or public claim is made",
            "useful_result": "z_cA_transfer,A is reduced to z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A after z_Kfixed,A=0",
            "next_missing_piece": "derive G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc with R_Hsrc=0, or source-bound R_Hsrc",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3682_0",
            "target_doc": "3683-Y5-R2FR-Hilbert-worldtube-charge-identity-or-RHsrc-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3683_Hilbert_worldtube_charge_identity_or_RHsrc_bound_row.py",
            "objective": "derive G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc with R_Hsrc=0, or produce a nonclaim finite R_Hsrc residual/bound row with source norm, boundary flux, units and source paths",
            "success_gate": "R_Hsrc is theorem-zero from parent Hilbert/worldtube charge identity, or a source-backed nonclaim residual row exists and z_cA_transfer has only support/normalizer/feedback/R_Hsrc residuals",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3682 - Source-worldtube transfer kernel zero or z_cA transfer bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint does not just say the coupling is missing. It removes the one transfer piece that really is removable by type: a fixed linear downstream normalization-preserving `K_arena` cannot be a hidden source coefficient.",
        "",
        "## Main result",
        "",
        "`z_Kfixed,A = 0` for a fixed downstream readout kernel independent of `Xhat`, source labels, support choice, calibration, varied fields, and effective action.",
        "",
        "The full transfer component is not zero. The reduced component is:",
        "",
        "`z_cA_transfer,A = z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A`.",
        "",
        "The source bridge now sits in the identity:",
        "",
        "`G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc`.",
        "",
        "So the next route is not to re-audit generic coupling again; it is to attack `R_Hsrc` and the worldtube/normalizer terms directly.",
        "",
        "## Fixed-kernel theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## Transfer split rows"])
    for row in split:
        lines.append(f"- `{row['split_id']}`: {row['status']} - `{row['symbol']}` -> `{row['formula_or_value']}`")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Arena acquisition rows"])
    for row in acquisition:
        lines.append(f"- `{row['acquisition_id']}`: {row['status']} - {row['arena']} needs `{row['needed_source_path']}` for `{row['target_component']}`")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + theorem + split + bounds + acquisition + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3682*", "3682-Y5-R2FR-*", "P8_Y5*3682*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    theorem_by_id = {str(row["theorem_id"]): row for row in theorem}
    split_by_id = {str(row["split_id"]): row for row in split}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}
    acquisition_arenas = {str(row["arena"]) for row in acquisition}

    add("VAL3682_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3682_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3682_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3682 outputs written")
    add("VAL3682_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3682_4_fixed_kernel_zero", theorem_by_id["FKT3682_1_fixed_linear_downstream"]["status"] == "EXACT_TYPED_FIXED_KERNEL_ZERO" and split_by_id["ZTR3682_0_fixed_kernel"]["numeric_value"] == 0, "fixed downstream kernel subslot is zero")
    add("VAL3682_5_not_full_transfer_zero", theorem_by_id["FKT3682_6_verdict"]["status"] == "FULL_ZCA_TRANSFER_ZERO_NOT_PROVED_FIXED_SUBSLOT_ZERO", "full transfer zero is not claimed")
    add("VAL3682_6_reduced_transfer_formula", split_by_id["ZTR3682_5_transfer_reduced"]["formula_or_value"] == "z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A", "z_cA_transfer reduced to live residuals")
    add("VAL3682_7_post_current_formula", "z_cA_reentry,A" in str(split_by_id["ZTR3682_6_post_current_total"]["formula_or_value"]), "post-current total retains reentry")
    add("VAL3682_8_RHsrc_identity_row", "G_ref^-1 Q_tau" in str(bound_by_id["KCB3682_4_RHsrc_identity"]["bound_or_formula"]) and "Pi_M^H J_H^dress" in str(bound_by_id["KCB3682_4_RHsrc_identity"]["bound_or_formula"]), "R_Hsrc bridge identity is recorded")
    add("VAL3682_9_acquisition_arenas", {"WEP/MICROSCOPE", "R10 short-range gravity", "PPN/orbital/Newton", "clock/EM/fine-structure", "parent GR/Newton bridge"}.issubset(acquisition_arenas), "acquisition ledger covers WEP, R10, PPN/orbit, clock/EM and parent bridge")
    add("VAL3682_10_all_acq_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False and row["score_ready"] is False for row in acquisition), "all acquisition rows are nonclaim")
    add("VAL3682_11_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3682_12_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3682_13_doc_written", "z_Kfixed,A = 0" in doc_text and "z_cA_transfer,A = z_Ksupport,A + z_Knorm,A + z_Kfeedback,A + z_RHsrc,A" in doc_text and "G_ref^-1 Q_tau" in doc_text, "doc records fixed-kernel zero, reduced transfer and source identity")
    add("VAL3682_14_next_target", next_target[0]["target_doc"].startswith("3683-") and "R_Hsrc" in next_target[0]["objective"], "3683 targets Hilbert worldtube charge identity")
    add("VAL3682_15_no_formalization_leak", not leaks, "no 3682 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = fixed_kernel_theorem_rows(ts)
    split = transfer_split_rows(ts)
    bounds = component_bound_rows(ts)
    acquisition = arena_acquisition_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3682_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3682_FIXED_KERNEL_TYPED_ZERO_THEOREM.csv",
        "split": RESIDUALS / "P8_Y5_R2FR_3682_ZCA_TRANSFER_SPLIT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3682_KARENA_COMPONENT_BOUND_ROWS.csv",
        "acquisition": RESIDUALS / "P8_Y5_R2FR_3682_ARENA_KERNEL_ACQUISITION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3682_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3682_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3682_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3682_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3682_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["split"], split)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["acquisition"], acquisition)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, split, bounds, acquisition, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, split, bounds, acquisition, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3682 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3682 checkpoint: fixed K_arena subslot zero; support/normalizer/feedback/R_Hsrc retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
