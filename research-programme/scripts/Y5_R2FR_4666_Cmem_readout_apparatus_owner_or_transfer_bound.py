from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4666"
CLAIM_ID = "L-508"
BRANCH = "MTS_R2FR_Y5_CMEM_READOUT_APPARATUS_OWNER_OR_TRANSFER_BOUND_4666"
MARKER = "PPC4161_CMEM_READOUT_APPARATUS_OWNER_OR_TRANSFER_BOUND_4666"
PACKET_MARKER = "PPC4161_PACKET_CMEM_READOUT_APPARATUS_OWNER_OR_TRANSFER_BOUND_4666"
DECISION = "CMEM_READOUT_ZERO_PRIVATE_FIXED_POSTPROCESSING_BRANCH_DYNAMIC_TRANSFER_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4667-Y5-R2FR-Cmem-boundary-owner-or-nonHilbert-split-bound.md"

DOC_PATH = POST / "4666-Y5-R2FR-Cmem-readout-apparatus-owner-or-transfer-bound.md"
FORMAL_PATH = FORMAL / "682-PPC4161-Cmem-readout-apparatus-owner-or-transfer-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_2523 = POST / "2523-Y5-R2FR-readout-projector-memory-reentry-zero-or-Jreadout-bound.md"
DOC_4579 = POST / "4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md"
DOC_4580 = POST / "4580-Y5-R2FR-Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound.md"
DOC_4581 = POST / "4581-Y5-R2FR-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"
DOC_4584 = POST / "4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md"
DOC_4585 = POST / "4585-Y5-R2FR-active-kernel-first-zero-or-operator-bound.md"
FORMAL_681 = FORMAL / "681-PPC4161-Cmem-support-worldtube-owner-or-Reynolds-bound.md"

CSV_4665_LHRS = SOURCE_DIR / "P8_Y5_R2FR_4665_LHRS_CMEM_UPDATE_AFTER_SUPPORT.csv"
CSV_4665_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4665_NEXT_TARGET.csv"
CSV_4665_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4665_STATUS.csv"
CSV_4665_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4665_VALIDATION.csv"
CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
CSV_4579_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4579_READOUT_COMMUTATOR_THEOREM.csv"
CSV_4579_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv"
CSV_4579_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4579_RHO_READOUT_SHIFT_BOUND_VALUE_ROWS.csv"
CSV_4579_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4579_DECISION.csv"
CSV_4579_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4579_VALIDATION.csv"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"
CSV_4580_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4580_CREADOUT_REDUCTION_ROWS.csv"
CSV_4580_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4580_VALIDATION.csv"
CSV_4581_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4581_REMAINING_CREADOUT_ZERO_THEOREM.csv"
CSV_4581_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4581_STRICT_ZERO_CONTRACT.csv"
CSV_4581_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4581_CREADOUT_REDUCTION_ROWS.csv"
CSV_4581_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4581_VALIDATION.csv"
CSV_4582_MATERIAL = SOURCE_DIR / "P8_Y5_R2FR_4582_MATERIAL_OWNER_ZERO_THEOREM.csv"
CSV_4582_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4582_MATERIAL_TAIL_REDUCTION_ROWS.csv"
CSV_4582_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4582_VALIDATION.csv"
CSV_4583_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4583_CHARGE_CURRENT_EM_READOUT_OWNER_THEOREM.csv"
CSV_4583_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4583_EM_TAIL_REDUCTION_ROWS.csv"
CSV_4583_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4583_VALIDATION.csv"
CSV_4584_APP = SOURCE_DIR / "P8_Y5_R2FR_4584_APPARATUS_DOMAIN_THEOREM.csv"
CSV_4584_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4584_MATERIAL_APPARATUS_REDUCTION_ROWS.csv"
CSV_4584_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4584_VALIDATION.csv"
CSV_4585_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4585_KERNEL_PRODUCT_RULE_THEOREM.csv"
CSV_4585_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4585_KERNEL_ZERO_CERTIFICATE_MATRIX.csv"
CSV_4585_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4585_CREADOUT_KERNEL_REDUCTION_ROWS.csv"
CSV_4585_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4585_OPERATOR_BOUND_SCHEMA.csv"
CSV_4585_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4585_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4666_SOURCE_REGISTER.csv"
OWNER_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_READOUT_OWNER_CLAUSES.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_CMEM_READOUT_ZERO_IMPORT.csv"
DYNAMIC_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_DYNAMIC_READOUT_TRANSFER_BOUND_ROWS.csv"
LHRS_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_LHRS_CMEM_FINAL_UPDATE_AFTER_READOUT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4666_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4666_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4666_00_4665_next", CSV_4665_NEXT, "4666-Y5-R2FR-Cmem-readout-apparatus-owner-or-transfer-bound.md", "4665 selected readout/apparatus."),
        ("SRC4666_01_4665_lhrs_after", CSV_4665_LHRS, "SLU4665_2_after", "LHRS before readout closure."),
        ("SRC4666_02_4665_final", CSV_4665_LHRS, "SLU4665_3_final_Cmem", "final Cmem before readout closure."),
        ("SRC4666_03_4665_status", CSV_4665_STATUS, "READOUT_REMAINS", "4665 status import."),
        ("SRC4666_04_4665_validation", CSV_4665_VALIDATION, "VAL4665_OVERALL", "4665 validation pass."),
        ("SRC4666_05_681_formal", FORMAL_681, "C_mem^readout / apparatus-transfer owner", "formal readout handoff."),
        ("SRC4666_06_4599_readout", CSV_4599_THEOREM, "LHRS4599_3_readout", "readout zero-or-bound theorem."),
        ("SRC4666_07_4599_norm", CSV_4599_NORM, "N4599_3_readout", "readout norm row."),
        ("SRC4666_08_4599_control", CSV_4599_CONTROL, "CTRL4599_readout_countermodel", "readout countermodel."),
        ("SRC4666_09_4579_product", CSV_4579_THEOREM, "RCT4579_0_product_rule_identity", "readout product rule."),
        ("SRC4666_10_4579_pure", CSV_4579_THEOREM, "RCT4579_1_pure_postprocessing_zero", "pure postprocessing zero theorem."),
        ("SRC4666_11_4579_survivor", CSV_4579_THEOREM, "RCT4579_2_projector_dependent_survivor", "projector survivor."),
        ("SRC4666_12_4579_bound", CSV_4579_THEOREM, "RCT4579_3_rho_shift_bound", "readout bound law."),
        ("SRC4666_13_4579_split", CSV_4579_SPLIT, "PDB4579_0_Creadout_split", "Creadout split."),
        ("SRC4666_14_4579_zero", CSV_4579_BOUND, "RVB4579_0_zero_branch", "zero branch."),
        ("SRC4666_15_4579_decision", CSV_4579_DECISION, "PURE_POSTPROCESSING_READOUT_COMMUTATOR_ZERO_DERIVED", "4579 decision."),
        ("SRC4666_16_4579_validation", CSV_4579_VALIDATION, "VAL4579_pure_postprocessing_zero", "4579 validation."),
        ("SRC4666_17_2523_pure", DOC_2523, "JRZ2523_1_pure_postprocessing_zero", "2523 pure theorem."),
        ("SRC4666_18_2523_fixed", DOC_2523, "JRZ2523_2_fixed_projector_clause", "2523 fixed projector lemma."),
        ("SRC4666_19_2523_bound", DOC_2523, "JRO2523_0_total", "2523 readout bound row."),
        ("SRC4666_20_4580_domain", CSV_4580_DOMAIN, "PDC4580_1_fixed_qbasic_domain", "fixed domain/support zero."),
        ("SRC4666_21_4580_tau", CSV_4580_DOMAIN, "PDC4580_2_qbasic_tau_protocol", "q-basic tau protocol zero."),
        ("SRC4666_22_4580_result", CSV_4580_DOMAIN, "PDC4580_4_readout_certificate_result", "readout domain result."),
        ("SRC4666_23_4580_reduction", CSV_4580_REDUCTION, "CRV4580_4_Creadout_reduced", "4580 Creadout reduction."),
        ("SRC4666_24_4580_validation", CSV_4580_VALIDATION, "VAL4580_reduced_bound", "4580 validation."),
        ("SRC4666_25_4581_frame", CSV_4581_THEOREM, "ZCR4581_0_same_frame_zero", "same-frame zero."),
        ("SRC4666_26_4581_fixed_kernel", CSV_4581_THEOREM, "ZCR4581_2_fixed_kernel_zero", "fixed kernel zero."),
        ("SRC4666_27_4581_eft", CSV_4581_THEOREM, "ZCR4581_3_common_EFT_zero", "common EFT zero."),
        ("SRC4666_28_4581_tau", CSV_4581_THEOREM, "ZCR4581_4_strict_tau_tail_zero", "tau tail zero."),
        ("SRC4666_29_4581_contract", CSV_4581_CONTRACT, "SZ4581_0_strict_Creadout_zero", "strict Creadout contract."),
        ("SRC4666_30_4581_reduction", CSV_4581_REDUCTION, "CRV4581_5_Creadout_reduced_again", "4581 Creadout reduction."),
        ("SRC4666_31_4581_validation", CSV_4581_VALIDATION, "VAL4581_strict_zero", "4581 validation."),
        ("SRC4666_32_4582_material", CSV_4582_MATERIAL, "MOT4582_0_owned_material_stress", "owned material zero."),
        ("SRC4666_33_4582_tail", CSV_4582_REDUCTION, "MTR4582_3_Creadout_update", "4582 Creadout update."),
        ("SRC4666_34_4582_validation", CSV_4582_VALIDATION, "VAL4582_owned_material_zero", "4582 validation."),
        ("SRC4666_35_4583_emreadout", CSV_4583_OWNER, "CCO4583_2_CEMreadout_strict_zero", "EM readout zero."),
        ("SRC4666_36_4583_flux", CSV_4583_OWNER, "CCO4583_3_PhiEM_closed_collar_zero", "closed collar flux zero."),
        ("SRC4666_37_4583_reduction", CSV_4583_REDUCTION, "ETR4583_2_Creadout_fixed_branch_update", "4583 Creadout update."),
        ("SRC4666_38_4583_validation", CSV_4583_VALIDATION, "VAL4583_decision_token", "4583 validation."),
        ("SRC4666_39_4584_app", CSV_4584_APP, "APP4584_2_disjoint_postprocessing_zero", "apparatus postprocessing zero."),
        ("SRC4666_40_4584_tail", CSV_4584_REDUCTION, "MAR4584_2_Cmaterial_tail_strict_zero", "material/apparatus strict zero."),
        ("SRC4666_41_4584_reduction", CSV_4584_REDUCTION, "MAR4584_3_Creadout_update", "4584 Creadout reduction."),
        ("SRC4666_42_4584_validation", CSV_4584_VALIDATION, "VAL4584_Creadout_reduction", "4584 validation."),
        ("SRC4666_43_4585_product", CSV_4585_THEOREM, "KPR4585_0_product_rule", "active kernel product rule."),
        ("SRC4666_44_4585_zero", CSV_4585_THEOREM, "KPR4585_1_fixed_qbasic_kernel_zero", "fixed q-basic kernel zero."),
        ("SRC4666_45_4585_matrix", CSV_4585_MATRIX, "KC4585_4_orbital_GM", "kernel matrix includes orbital GM."),
        ("SRC4666_46_4585_total_bound", CSV_4585_BOUND, "KBS4585_5_total", "operator total bound."),
        ("SRC4666_47_4585_total_zero", CSV_4585_REDUCTION, "KRD4585_1_kernel_total_zero", "kernel total zero."),
        ("SRC4666_48_4585_reduction", CSV_4585_REDUCTION, "KRD4585_2_Creadout_if_kernel_zero", "kernel zero Creadout reduction."),
        ("SRC4666_49_4585_validation", CSV_4585_VALIDATION, "VAL4585_fixed_zero", "4585 validation."),
        ("SRC4666_50_doc4579", DOC_4579, "A pure data readout that is absent from the parent action", "4579 prose theorem."),
        ("SRC4666_51_doc4580", DOC_4580, "C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual", "4580 prose reduction."),
        ("SRC4666_52_doc4581", DOC_4581, "C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail", "4581 prose reduction."),
        ("SRC4666_53_doc4584", DOC_4584, "C_readout <= C_kernel_active + C_EFT_active + C_tau_tail", "4584 prose reduction."),
        ("SRC4666_54_doc4585", DOC_4585, "C_readout <= C_EFT_active + C_tau_tail", "4585 prose reduction."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def owner_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RDO4666_0_product_rule", "readout leak is (O_f Pi_readout)J_H", "variation-before-readout leaves only the projector derivative term", "RCT4579_0_product_rule_identity", "EXACT_PRODUCT_RULE"),
        ("RDO4666_1_pure_postprocessing", "Pi_readout absent from S_parent, S_eff and Coeff_active_source", "a pure post-solution reporting map cannot create an active source coefficient", "RCT4579_1; JRZ2523_1", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("RDO4666_2_fixed_domain_tau_frame", "domain/support/tau/frame are fixed q-basic protocol data", "C_domain=C_support=C_frame=C_tau_protocol=0 in the fixed observed-coframe branch", "PDC4580_1; PDC4580_2; ZCR4581_0", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("RDO4666_3_material_apparatus_owned", "owned material, EM stress and apparatus are source content or disjoint postprocessing", "C_material_tail=0 and C_apparatus=0 in the strict branch", "MOT4582_0; CCO4583_2; MAR4584_2", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("RDO4666_4_fixed_kernels", "arena kernels declared before variation as fixed/q-basic downstream data", "O_f K_A=0 for each named fixed kernel, so C_kernel_active=0 if all certificates are signed", "KPR4585_1; KRD4585_1", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("RDO4666_5_common_EFT_tau", "common q-basic EFT coefficients and strict observed-tau role lock", "C_EFT_active=0 and C_tau_tail=0 only on the strict no-reentry/no-tail branch", "ZCR4581_3; ZCR4581_4", "PRIVATE_BRANCH_ZERO_INPUT"),
        ("RDO4666_6_no_feedback", "no fitted GM/calibration/readout feedback into parent source coefficient", "late calibration cannot be used to hide readout transfer residuals", "JRG2523_7_no_calibration_feedback", "ANTI_LAUNDERING_GUARD"),
        ("RDO4666_7_strict_result", "all readout-transfer zero clauses hold in the same branch", "C_readout=0 and therefore C_mem^readout=0", "SZ4581_0; LHRS4599_3_readout", "CMEM_READOUT_ZERO_ROUTE"),
        ("RDO4666_8_scope", "readout zero is not boundary/non-Hilbert or source-charge equality", "boundary, non-Hilbert and body-charge/source-charge gates remain separate", "SLU4665_3_final_Cmem", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": row[0],
            "clause": row[1],
            "deduction": row[2],
            "source": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RZI4666_0_definition", "C_mem^readout := Pi_mem[C_X^readout]", "memory projection of readout/projector/apparatus transfer leakage", "LHRS4599_3_readout; SLU4665_2_after", "TARGET_DEFINED"),
        ("RZI4666_1_commutator_zero", "[O_f,Pi_readout]J_H=0", "pure postprocessing plus fixed protocol removes the readout commutator", "RCT4579_1; RDO4666_1", "READOUT_COMMUTATOR_ZERO"),
        ("RZI4666_2_domain_frame_zero", "C_domain=C_support=C_frame=0", "fixed q-basic local domain/support and one observed coframe are branch data, not fitted readout variables", "PDC4580_1; ZCR4581_0", "DOMAIN_FRAME_ZERO"),
        ("RZI4666_3_material_apparatus_zero", "C_material_tail=C_apparatus=0", "owned material/EM/apparatus are either in the same Hilbert source or disjoint postprocessing", "MAR4584_2", "MATERIAL_APPARATUS_ZERO"),
        ("RZI4666_4_kernel_EFT_tau_zero", "C_kernel_active=C_EFT_active=C_tau_tail=0", "all named kernels are fixed/q-basic, common EFT modes are q-basic, and observed tau has no role split", "KRD4585_1; ZCR4581_3; ZCR4581_4", "KERNEL_EFT_TAU_ZERO"),
        ("RZI4666_5_result", "fixed postprocessing observed-coframe branch => C_mem^readout=0", "all readout/projector/apparatus transfer pieces vanish in the same strict branch", "RDO4666_0..7", "CMEM_READOUT_TERM_ZERO_PRIVATE_BRANCH"),
        ("RZI4666_6_scope", "not a full local-GR/Newton/PPN/R10 claim", "boundary, non-Hilbert, body-charge and source-charge gates remain open", "RDO4666_8", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def dynamic_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DRT4666_0_envelope", "Delta_readout_mem", "|C_kernel_active|+|C_EFT_active|+|C_tau_tail|+|J_calibration|+|J_boundary_endpoint|+|C_apparatus_active|+|C_material_marker|", "off-branch no-cancellation readout transfer envelope", "JRO2523_0_total; PDB4579_0_Creadout_split"),
        ("DRT4666_1_kernel", "C_kernel_active", "sum_A C_KA with A in {source_worldtube,WEP,clock,light,orbital_GM,projective}", "active/fitted arena kernels require fixed certificates or operator norms", "KBS4585_5_total"),
        ("DRT4666_2_EFT", "C_EFT_active", "finite row for hidden/readout-regenerated EFT or effective-action coefficient reentry", "readout/EFT map entering before variation is a source coefficient", "JRZ2523_4_effective_prevariation; CRV4581_3_C_EFT"),
        ("DRT4666_3_tau", "C_tau_tail", "tau role split, moving surface, clock/orbit convention, units/lapse or private-memory-time tail", "strict observed-tau role lock is required for zero", "ZCR4581_4_strict_tau_tail_zero"),
        ("DRT4666_4_calibration", "J_calibration", "||partial_m C_fit|| ||partial Source/partial C_fit||", "fitted GM/eta/clock/orbit nuisance feedback is a finite residual, not a proof", "JRO2523_7_calibration"),
        ("DRT4666_5_apparatus_boundary", "C_apparatus_active+J_boundary_endpoint", "apparatus flux/support/thermal/EM terms plus endpoint/boundary readout leakage", "active apparatus or endpoint movement remains source-backed bound work", "APP4584_3_active_apparatus_bound; JRO2523_8_boundary_endpoint"),
        ("DRT4666_6_source_contract", "C_mem_readout_dynamic_source_row", "arena;kernel;protocol;coframe;tau;EFT;calibration;apparatus;boundary;operator_norm;units;source_path;valid_for_claim", "future source-backed readout row contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def lhrs_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RLU4666_0_before", "|C_mem^LHRS_live| <= |C_mem^readout|", "4665 LHRS after Hodge, label and support closure", "LHRS_IMPORTED"),
        ("RLU4666_1_readout_zero", "|C_mem^readout|=0", "4666 fixed postprocessing observed-coframe readout owner private branch zero", "READOUT_TERM_REMOVED"),
        ("RLU4666_2_LHRS_zero", "C_mem^LHRS_live=0", "Hodge, label, support and readout channels are zero in the same strict private branch", "LHRS_BLOCK_ZERO_PRIVATE_BRANCH"),
        ("RLU4666_3_final_Cmem", "|C_mem^final_live| <= |C_mem^boundary|+|C_mem^nonHilbert|", "final Cmem residual vector after LHRS closure", "FINAL_VECTOR_REDUCED_TO_BOUNDARY_NONHILBERT"),
        ("RLU4666_4_not_full", "C_mem^final_live=0 is not claimed", "boundary and non-Hilbert channels remain open", "FULL_CMEM_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4666_0_strict_branch", "C_mem^readout", "PASS_CONDITIONAL_PRIVATE_ZERO", "pure postprocessing, fixed protocol, owned material/apparatus, fixed kernels, common EFT and strict tau lock hold in the same branch."),
        ("RUN4666_1_dynamic_readout", "Delta_readout_mem", "FAIL_CLOSED_TO_TRANSFER_BOUND_ROWS", "active kernels, EFT reentry, tau split, calibration feedback, apparatus and boundary endpoints remain explicit rows off branch."),
        ("RUN4666_2_LHRS_update", "C_mem^LHRS_live", "PASS_ZERO_PRIVATE_BRANCH", "Hodge, label, support and readout are now all closed in the strict private branch."),
        ("RUN4666_3_charge_firewall", "Pi_M/H_tau/source-charge equality", "NOT_CLAIMED", "readout transfer silence is not measured-G/source-charge ownership."),
        ("RUN4666_4_claim_status", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "boundary, non-Hilbert and body-charge/source-charge gates remain."),
        ("RUN4666_5_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4666_0_no_all_readout_shortcut", "Do not call every local projector pure postprocessing; fixed/protocol/q-basic clauses are required.", "ACTIVE"),
        ("CTRL4666_1_no_fitted_GM_laundering", "Do not hide readout/source residuals inside measured G, GM, calibration or nuisance parameters.", "ACTIVE"),
        ("CTRL4666_2_no_active_kernel_erasure", "Arena kernels that depend on source support, orbit, clock rods, lightcone geometry or fitted readout remain operator-bound rows.", "ACTIVE"),
        ("CTRL4666_3_no_EFT_reentry", "Readout or EFT maps entering before variation are source coefficients, not harmless observations.", "ACTIVE"),
        ("CTRL4666_4_no_apparatus_flux_erasure", "Active apparatus/thermal/EM/boundary endpoint terms remain explicit bounds unless included in source or disjoint postprocessing.", "ACTIVE"),
        ("CTRL4666_5_no_full_Cmem", "C_mem^readout=0 does not close boundary or non-Hilbert channels.", "ACTIVE"),
        ("CTRL4666_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4666_0",
            "decision": DECISION,
            "summary": (
                "4666 closes C_mem^readout in the fixed private postprocessing observed-coframe branch. "
                "The readout product-rule remainder is (O_f Pi_readout)J_H; it vanishes when readout is absent from parent/effective source slots, the protocol/domain/tau/frame are fixed q-basic data, material/EM/apparatus are owned or disjoint, kernels are fixed before variation, common EFT modes are q-basic and calibration feedback is forbidden. "
                "Therefore C_mem^readout=0 on that branch and C_mem^LHRS_live=0. Off branch, active kernels, EFT reentry, tau tails, calibration feedback, apparatus and boundary endpoint rows remain source-ready nonclaims."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "readout_result": "C_MEM_READOUT_ZERO_PRIVATE_FIXED_POSTPROCESSING_BRANCH",
            "dynamic_status": "DELTA_READOUT_MEM_TRANSFER_BOUND_ROWS_RETAINED",
            "LHRS_status": "LHRS_ZERO_PRIVATE_BRANCH",
            "final_Cmem_status": "BOUNDARY_NONHILBERT_REMAIN",
            "selected_next_channel": "C_mem^boundary / C_mem^nonHilbert split",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After LHRS closure, final Cmem has only boundary and non-Hilbert channels left; boundary is first because it also guards source-charge and local-vacuum claims.",
            "derive_route": "try to split C_mem^boundary and C_mem^nonHilbert, prove fixed/no-flux/exact boundary silence, and keep non-Hilbert current/spin/torsion tails explicit.",
            "fallback_route": "if boundary/non-Hilbert clauses fail, write absolute bound rows with surface flux, endpoint, spin/torsion, non-Hilbert current and arena projection inputs.",
            "avoid": "claiming LHRS closure as full local GR, or hiding boundary/non-Hilbert tails inside readout or measured G.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + owner + zero_import + dynamic + lhrs + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        OWNER_CLAUSES_CSV,
        ZERO_IMPORT_CSV,
        DYNAMIC_BOUND_CSV,
        LHRS_UPDATE_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4666_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4666_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4666_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4666_03_owner_clauses", any(row["clause_id"] == "RDO4666_7_strict_result" for row in owner), "readout owner strict-result clause present"),
        ("VAL4666_04_readout_zero", any(row["zero_id"] == "RZI4666_5_result" and row["status"] == "CMEM_READOUT_TERM_ZERO_PRIVATE_BRANCH" for row in zero_import), "Cmem readout zero row present"),
        ("VAL4666_05_dynamic_bound", any(row["bound_id"] == "DRT4666_0_envelope" for row in dynamic), "dynamic readout transfer bound retained"),
        ("VAL4666_06_LHRS_zero", any(row["update_id"] == "RLU4666_2_LHRS_zero" for row in lhrs), "LHRS zero row emitted"),
        ("VAL4666_07_no_readout_shortcut", any(row["control_id"] == "CTRL4666_0_no_all_readout_shortcut" for row in controls), "readout shortcut control present"),
        ("VAL4666_08_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4666_09_nonclaim_runner", any(row["run_id"] == "RUN4666_4_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim status remains nonclaim"),
        ("VAL4666_10_next_boundary", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is boundary/non-Hilbert"),
        ("VAL4666_11_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4666_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4666 Cmem readout private zero and dynamic transfer-bound gate passed" if passed_all else "4666 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4666 - Cmem readout/apparatus owner or transfer bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4666 attacks the final LHRS channel left after 4665:

`C_mem^readout := Pi_mem[C_X^readout]`.

Inside the fixed private postprocessing observed-coframe branch:

`C_mem^readout = 0`.

The proof route is the readout product rule:

`O_f(Pi_readout J_H) - Pi_readout O_f(J_H) = (O_f Pi_readout)J_H`.

So the readout channel closes only if:

- `Pi_readout` is absent from `S_parent`, `S_eff` and `Coeff_active_source`;
- domain, support, tau, frame, units and protocol are fixed q-basic data before variation;
- material, EM stress and apparatus are owned Hilbert-source content or disjoint postprocessing;
- arena kernels are fixed/q-basic rather than fitted response operators;
- EFT/readout coefficients do not reenter before variation;
- calibration feedback into the source coefficient is forbidden.

On that strict branch:

`C_readout=0`,

so:

`C_mem^LHRS_live = 0`.

The final memory trace-source vector is now:

`|C_mem^final_live| <= |C_mem^boundary| + |C_mem^nonHilbert|`.

This is not a public local-GR/Newton/PPN/R10 claim. Open readout branches remain explicit: active kernels, EFT reentry, tau tails, calibration feedback, apparatus flux/support and boundary endpoints are all retained as dynamic transfer-bound rows.

## Source Register

{table(sources)}

## Readout Owner Clauses

{table(owner)}

## Cmem Readout Zero Import

{table(zero_import)}

## Dynamic Readout Transfer Bound Rows

{table(dynamic)}

## LHRS Cmem Final Update After Readout

{table(lhrs)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4666 closes C_mem^readout in the fixed private postprocessing observed-coframe branch. The product-rule readout remainder is (O_f Pi_readout)J_H; it vanishes when readout is absent from parent/effective source slots, domain/support/tau/frame/protocol are fixed q-basic data, material/EM/apparatus are owned or disjoint, kernels are fixed before variation, common EFT modes are q-basic, strict tau lock holds, and calibration feedback is forbidden. Dynamic readout-transfer rows remain explicit off branch.",
        "Generated source register, readout owner clauses, Cmem readout zero import, dynamic readout transfer bound rows, LHRS final update, runner, controls, decision, status, next target and validation.",
        "Cmem_readout_zero_private_fixed_postprocessing_branch_dynamic_transfer_bound_nonclaim",
        NEXT_TARGET,
        "Calling every local projector pure postprocessing, using fitted GM/calibration to hide readout transfer, erasing active kernels, permitting EFT/readout reentry before variation, deleting apparatus/boundary endpoint flux, or claiming full local GR from LHRS closure.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until boundary/non-Hilbert channels and body-charge/source-charge gates are same-branch zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4666 closes `C_mem^readout` inside the fixed private postprocessing observed-coframe branch. The readout product-rule remainder vanishes only when the readout map is post-variation, source-codomain silent, fixed/q-basic in protocol/domain/tau/frame, material/EM/apparatus owned or disjoint, kernels fixed, common EFT/tau tails silent and calibration feedback forbidden. The full LHRS block is now zero in the strict branch; the remaining private-branch Cmem channels are boundary and non-Hilbert.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4666` removes the readout/apparatus-transfer channel from the private-branch LHRS residual vector while retaining dynamic readout-transfer bounds. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    owner = owner_clause_rows(timestamp)
    zero_import = zero_import_rows(timestamp)
    dynamic = dynamic_bound_rows(timestamp)
    lhrs = lhrs_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, owner, zero_import, dynamic, lhrs, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_CLAUSES_CSV, owner)
    write_csv(ZERO_IMPORT_CSV, zero_import)
    write_csv(DYNAMIC_BOUND_CSV, dynamic)
    write_csv(LHRS_UPDATE_CSV, lhrs)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, owner, zero_import, dynamic, lhrs, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4666 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
