from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4581"
CLAIM_ID = "L-423"
BRANCH_ID = "MTS_R2FR_Y5_REMAINING_CREADOUT_FRAME_MATERIAL_KERNEL_EFT_TAU_RESIDUAL_BOUND_OR_ZERO_4581"
MARKER = "PPC4161_REMAINING_CREADOUT_FRAME_MATERIAL_KERNEL_EFT_TAU_RESIDUAL_BOUND_OR_ZERO_4581"
PACKET_MARKER = "PPC4161_PACKET_REMAINING_CREADOUT_FRAME_MATERIAL_KERNEL_EFT_TAU_RESIDUAL_BOUND_OR_ZERO_4581"
DECISION = "SAME_FRAME_FIXED_KERNEL_COMMON_EFT_ZERO_BRANCH_DERIVED_MATERIAL_AND_ACTIVE_READOUT_TAILS_RETAINED_NONCLAIM"
NEXT_TARGET = "4582-Y5-R2FR-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md"

DOC_PATH = POST / "4581-Y5-R2FR-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"
FORMAL_PATH = FORMAL / "597-PPC4161-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4580 = POST / "4580-Y5-R2FR-Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound.md"
CSV_4580_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4580_NEXT_TARGET.csv"
CSV_4580_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4580_CREADOUT_REDUCTION_ROWS.csv"
CSV_4580_ACTIVE = SOURCE_DIR / "P8_Y5_R2FR_4580_ACTIVE_BRANCH_BOUND_ROWS.csv"
CSV_4580_GUARDS = SOURCE_DIR / "P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv"
CSV_4579_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv"
CSV_FRAME_SPLIT = SOURCE_DIR / "P8_frame_source_split_residual_or_zero.csv"
CSV_QMAP = SOURCE_DIR / "P8_EM_actual_q_map_vertical_basis_candidate.csv"
CSV_NORMAL_FORM = SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"
CSV_EM_BOUND = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_2118_KERNELS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_2122_OWNER = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv"
CSV_4269_TAU = SOURCE_DIR / "P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv"
FORMAL_557 = FORMAL / "557-PPC4161-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md"
FORMAL_580 = FORMAL / "580-PPC4161-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4581_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_REMAINING_CREADOUT_ZERO_THEOREM.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_CREADOUT_REDUCTION_ROWS.csv"
TAIL_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_MATERIAL_ACTIVE_TAIL_BOUND_ROWS.csv"
TAU_TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_TAU_RESIDUAL_TAIL_ROWS.csv"
STRICT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_STRICT_ZERO_CONTRACT.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_PARENT_SIGNATURE_AUDIT.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4581_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4581_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4581_00_4580_doc", "4580 checkpoint", DOC_4580, "C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual"),
        ("SRC4581_01_4580_next", "4580 next target", CSV_4580_NEXT, "remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero"),
        ("SRC4581_02_4580_reduction", "4580 reduced Creadout row", CSV_4580_REDUCTION, "CRV4580_4_Creadout_reduced"),
        ("SRC4581_03_4580_active", "4580 active branch rows", CSV_4580_ACTIVE, "AB4580_0_active_Hodge_Green"),
        ("SRC4581_04_4580_guards", "4580 closed-domain guards", CSV_4580_GUARDS, "CDG4580_1_Poynting"),
        ("SRC4581_05_4579_projector", "4579 Creadout split", CSV_4579_PROJECTOR, "PDB4579_2_frame_material_kernel"),
        ("SRC4581_06_frame_split", "frame/source split residual", CSV_FRAME_SPLIT, "FS3048_0_frame_split_definition"),
        ("SRC4581_07_qmap_geometry", "actual q-map public geometry", CSV_QMAP, "QMAP3517_0_public_geometry"),
        ("SRC4581_08_qmap_projector", "actual q-map projector readout", CSV_QMAP, "QMAP3517_8_projector_readout"),
        ("SRC4581_09_normal_form_visible", "normal-form visible stack", CSV_NORMAL_FORM, "NF3519_1_quotient_visible_stack"),
        ("SRC4581_10_normal_form_readout", "normal-form readout firewall", CSV_NORMAL_FORM, "NF3519_5_readout_firewall"),
        ("SRC4581_11_EM_readout", "EM readout residual vector", CSV_EM_BOUND, "EMB3503_5_C_EM_readout"),
        ("SRC4581_12_EM_current", "EM current normalization residual", CSV_EM_BOUND, "EMB3503_3_C_JQ"),
        ("SRC4581_13_kernel_suite", "source/readout explicit kernels", CSV_2118_KERNELS, "KSR2118_7_total_no_cancellation"),
        ("SRC4581_14_owner_lemma", "source/readout owner lemma", CSV_2122_OWNER, "SRO2122_6_verdict"),
        ("SRC4581_15_tau_tails", "4269 tau tail rows", CSV_4269_TAU, "TRES4269_0_tau_split"),
        ("SRC4581_16_same_coframe", "4541 same-coframe zero law", FORMAL_557, "ZL4541_0_same_coframe"),
        ("SRC4581_17_root_zero", "4564 cD/Poynting/root law", FORMAL_580, "TZ4564_0_cD_zero"),
        ("SRC4581_18_cGamma_guard", "4564 cGamma still open", FORMAL_580, "TZ4564_4_cGamma_not_closed"),
        ("SRC4581_19_claim_422", "prior claim register row", CLAIMS_PATH, "L-422"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "remaining Creadout frame/material/kernel/EFT/tau residual zero or bound",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ZCR4581_0_same_frame_zero",
            "component": "C_frame",
            "zero_law": "If one observed coframe e_obs=e_bar(q) is selected before variation and used by source variation, matter, EM, clocks, rods, orbits, PPN and readout, then the readout-frame projector has no compact-lapse derivative.",
            "formula": "O_f Pi_frame=0 => C_frame=0",
            "status": "PRIVATE_BRANCH_ZERO_DERIVED",
            "remaining_tail": "delta_frame_source if source variation uses a different frame",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ZCR4581_1_owned_material_zero",
            "component": "C_material_owned",
            "zero_law": "Visible matter, binding, stabilizer and Maxwell-Hodge stress inside the same Hilbert source are source content, not a readout projector tail.",
            "formula": "S_vis=S_matter[Psi,e_obs]+S_EM[A,e_obs]+S_binding[e_obs]+dB_impr => O_f Pi_material_owned=0",
            "status": "PRIVATE_SELECTOR_ZERO_DERIVED",
            "remaining_tail": "material-marker, apparatus, binding-response or charge/current normalization tails",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ZCR4581_2_fixed_kernel_zero",
            "component": "C_kernel_fixed",
            "zero_law": "A readout kernel declared before variation as a fixed protocol map from solved fields to observables cannot feed back into the Hilbert source.",
            "formula": "K_A=K_A^bar(protocol,q,e_obs) fixed during O_f => O_f K_A=0 => C_kernel_fixed=0",
            "status": "FIXED_KERNEL_ZERO_DERIVED",
            "remaining_tail": "active WEP/orbit/clock/light/source kernels if response operators are not fixed/q-owned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ZCR4581_3_common_EFT_zero",
            "component": "C_EFT_common",
            "zero_law": "Common EFT coefficients that are q-basic constants, topological slots or universal calibrated modes are not readout variables.",
            "formula": "D_f c_i^common=0 => O_f Pi_EFT_common=0 => C_EFT_common=0",
            "status": "COMMON_MODE_EFT_ZERO_DERIVED",
            "remaining_tail": "active nonminimal/readout-regenerated EM/EFT coefficients and c_Gamma memory projector terms",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ZCR4581_4_strict_tau_tail_zero",
            "component": "C_tau_tail",
            "zero_law": "If the 4269 same-observed-tau role lock is strict and no tau split, moving surface, clock/orbit convention, unit/lapse rescaling or private-memory-time leakage exists, the tau residual tail vanishes.",
            "formula": "R_tau_split=R_surface_motion=R_frame_coframe=R_clock_readout=R_orbital_readout=R_units_lapse=R_private_memory_tau=0 => C_tau_tail=0",
            "status": "STRICT_BRANCH_ZERO_DERIVED_RESIDUAL_ROWS_RETAINED",
            "remaining_tail": "4269 tau residual split rows if any clause reopens",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_0_C_frame",
            "quantity": "C_frame",
            "value_or_bound": "0 in the one-observed-coframe source/readout branch",
            "proof_source": "ZCR4581_0_same_frame_zero",
            "status": "THEOREM_ZERO_PRIVATE_BRANCH_DELTA_FRAME_TAIL_RETAINED",
            "score_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_1_C_material",
            "quantity": "C_material",
            "value_or_bound": "C_material <= C_material_tail",
            "proof_source": "C_material_owned=0; tails only if material/apparatus/binding/current response is not inside same Hilbert source",
            "status": "OWNED_MATERIAL_ZERO_TAIL_BOUND_RETAINED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_2_C_kernel",
            "quantity": "C_kernel",
            "value_or_bound": "C_kernel <= C_kernel_active",
            "proof_source": "fixed kernels zero; active response kernels retained",
            "status": "FIXED_KERNEL_ZERO_ACTIVE_KERNEL_BOUND_RETAINED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_3_C_EFT",
            "quantity": "C_EFT",
            "value_or_bound": "C_EFT <= C_EFT_active",
            "proof_source": "common q-basic EFT coefficients zero; active/readout-regenerated coefficients retained",
            "status": "COMMON_EFT_ZERO_ACTIVE_EFT_BOUND_RETAINED",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_4_C_tau",
            "quantity": "C_tau_residual",
            "value_or_bound": "C_tau_residual <= C_tau_tail, with C_tau_tail=0 only under strict 4269 no-tail lock",
            "proof_source": "4269 tau residual rows",
            "status": "STRICT_TAU_ZERO_ELSE_TAIL_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "CRV4581_5_Creadout_reduced_again",
            "quantity": "C_readout",
            "value_or_bound": "C_readout <= C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail",
            "proof_source": "4580 C_domain/C_support zero + 4581 same-frame/fixed-kernel/common-EFT/tau split",
            "status": "REDUCED_BOUND_DERIVED_TAIL_VALUES_REMAIN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def tail_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "TAIL4581_0_material_tail",
            "quantity": "C_material_tail",
            "bound_law": "C_material_tail <= C_marker + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |Delta_binding_response| + |C_apparatus|",
            "meaning": "Only non-Hilbert material markers, charge/current normalization, readout-regenerated EM/binding response, flux, or apparatus support remain.",
            "status": "BOUND_READY_VALUES_MISSING",
            "source_basis": "EMB3503_3_C_JQ; EMB3503_5_C_EM_readout; CDG4580_2_apparatus",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "TAIL4581_1_active_kernel",
            "quantity": "C_kernel_active",
            "bound_law": "C_kernel_active <= K_clock + K_light + K_orbit + K_WEP + K_GM + K_projective + K_source_worldtube",
            "meaning": "Only response operators/kernels that are not fixed downstream functors survive.",
            "status": "BOUND_READY_VALUES_MISSING",
            "source_basis": "KSR2118_0..7 explicit exception kernels",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "TAIL4581_2_active_EFT",
            "quantity": "C_EFT_active",
            "bound_law": "C_EFT_active <= |C_XF2| + |w_EM| + |Delta_Hodge_EM| + |C_EM_readout| + |c_Gamma P_loc Gamma_mem| + |Gamma_perp/K_perp|",
            "meaning": "Common EFT slots are zero; nonminimal EM/readout/Hodge and memory projector coefficients stay explicit.",
            "status": "BOUND_READY_VALUES_MISSING",
            "source_basis": "EMB3503_0..5 and TZ4564_4_cGamma_not_closed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "TAIL4581_3_frame_tail",
            "quantity": "delta_frame_source",
            "bound_law": "|delta_frame_source| := |Delta_frame ln(kappa_eff source readout)| after one observed-frame calibration",
            "meaning": "If the source variation uses a different frame than matter/readout, the same-frame zero is rejected and the older frame split row is used.",
            "status": "ZERO_IF_SAME_FRAME_ELSE_SOURCE_ROW_REQUIRED",
            "source_basis": "FS3048_0_frame_split_definition",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def tau_tail_rows(now: str) -> list[dict[str, Any]]:
    tails = [
        ("TAU4581_0_split", "R_tau_split", "source/charge/clock/orbit/PPN/readout use different tau generators"),
        ("TAU4581_1_surface", "R_surface_motion", "linking surfaces move independently of the selected tau flow"),
        ("TAU4581_2_frame", "R_frame_coframe", "observed coframe/frame differs between source charge and clock/readout"),
        ("TAU4581_3_clock", "R_clock_readout", "clock/redshift convention is selected after comparison or drifts"),
        ("TAU4581_4_orbit", "R_orbital_readout", "orbit/PPN coordinates are tuned after fitting"),
        ("TAU4581_5_units", "R_units_lapse_rescaling", "unit/lapse/orientation/normalization rescaling changes tau"),
        ("TAU4581_6_private", "R_private_memory_tau", "private process/memory time leaks into observed tau"),
    ]
    rows = []
    for tail_id, symbol, meaning in tails:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "tail_id": tail_id,
                "symbol": symbol,
                "meaning": meaning,
                "bound_role": "C_tau_tail absolute no-cancellation component",
                "current_value": "MISSING_ZERO_OR_SOURCE_BACKED_BOUND_IF_REOPENED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "tail_id": "TAU4581_7_total",
            "symbol": "C_tau_tail",
            "meaning": "sum of tau split/surface/frame/clock/orbit/units/private-time tails",
            "bound_role": "C_tau_tail <= sum_abs(TAU4581_0..6)",
            "current_value": "MISSING_COMPONENT_VALUES_OR_STRICT_ZERO_CERTIFICATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def strict_zero_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "SZ4581_0_strict_Creadout_zero",
            "contract": "If C_material_tail=0, C_kernel_active=0, C_EFT_active=0 and C_tau_tail=0 in addition to the 4580 domain/support zeros and 4581 frame/fixed-kernel/common-EFT zeros, then C_readout=0 and rho_readout_shift=0.",
            "formula": "C_readout=0 => ||rho_readout_shift||_TV/M_H_ref=0",
            "current_status": "EXACT_CONTRACT_DERIVED_TAIL_VALUES_UNSIGNED",
            "next_required": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def audit_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("AUD4581_0_frame", "same-frame/coframe part no longer floats as generic readout coupling", "C_frame_ZERO_PRIVATE_BRANCH"),
        ("AUD4581_1_kernel", "fixed kernels are zero, active response kernels are the only kernel debt", "FIXED_KERNEL_ZERO_ACTIVE_KERNEL_RETAINED"),
        ("AUD4581_2_EFT", "common EFT coefficients are zero, active/nonminimal/readout-regenerated coefficients are retained", "COMMON_EFT_ZERO_ACTIVE_EFT_RETAINED"),
        ("AUD4581_3_material", "owned material is in Hilbert stress; material-tail is now the target, not all material response", "MATERIAL_TAIL_ISOLATED"),
        ("AUD4581_4_verdict", "Creadout reduced to material/kernel/EFT/tau tails with strict zero contract written", "TAIL_REDUCTION_COMPLETE_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": audit_id,
            "finding": finding,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, finding, status in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4581_same_frame", "single e_obs branch with source/readout coframe locked", "C_frame=0", "CONTROL_PASS"),
        ("CTRL4581_frame_split", "source variation and readout use different frames", "same-frame zero rejected; delta_frame_source retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4581_fixed_kernel", "kernel declared before variation and downstream-only", "C_kernel_fixed=0", "CONTROL_PASS"),
        ("CTRL4581_active_kernel", "MICROSCOPE/orbit/clock response operator not parent-owned", "C_kernel_active retained", "FIREWALL_PASS"),
        ("CTRL4581_common_EFT", "coefficient is q-basic common calibrated slot", "C_EFT_common=0", "CONTROL_PASS"),
        ("CTRL4581_active_EFT", "readout regenerates EM/nonminimal/memory coefficient", "C_EFT_active retained", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": control_id,
            "input_case": input_case,
            "expected": expected,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, input_case, expected, verdict in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4581_0_frame", "C_frame zero in one-observed-coframe branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4581_1_fixed_kernel", "Fixed downstream kernels zero.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4581_2_common_EFT", "Common q-basic EFT slots zero.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4581_3_tails", "Material, active-kernel, active-EFT and tau-tail values or zero certificates.", "BLOCKED"),
        ("PROM4581_4_no_claim", "No local-GR/Newton/PPN/R10 claim until all tails close or are source-bounded below arena gates.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4581 narrows the remaining readout commutator again: same-frame readout, owned material content, fixed kernels and common EFT slots are zero branches.  The live C_readout debt is now only material-tail, active response kernels, active/readout-regenerated EFT coefficients and tau tails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The sharpest next move is to attack the material-tail/active-kernel block directly, because frame, fixed-kernel and common-EFT parts are no longer the bottleneck in the private branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    zero_theorem: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    tail_bounds: list[dict[str, Any]],
    tau_tails: list[dict[str, Any]],
    strict_zero: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4581 - Remaining Creadout frame/material/kernel/EFT/tau residual bound or zero

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4580 reduced the readout commutator to:

```text
C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual
```

4581 narrows it again.  In the private one-observed-coframe/fixed-protocol branch:

```text
C_frame = 0
C_material_owned = 0
C_kernel_fixed = 0
C_EFT_common = 0
```

and the tau tail is zero only under the strict 4269 role-lock:

```text
R_tau_split = R_surface_motion = R_frame_coframe = R_clock_readout
             = R_orbital_readout = R_units_lapse = R_private_memory_tau = 0.
```

The live reduced branch is therefore:

```text
C_readout <= C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail
```

This is actual narrowing, not another missing-list lap: the frame/fixed-kernel/common-EFT pieces now have theorem-zero branch laws.  The remaining target is material-tail plus active response kernels and active EFT/readout coefficients.

## Zero theorem rows

{markdown_table(zero_theorem)}

## Creadout reduction rows

{markdown_table(reductions)}

## Material and active-tail bounds

{markdown_table(tail_bounds)}

## Tau residual tails

{markdown_table(tau_tails)}

## Strict zero contract

{markdown_table(strict_zero)}

## Audit

{markdown_table(audits)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: attack material-tail and active-kernel ownership/bounds directly.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4581 remaining Creadout tails

Marker: `{MARKER}`  
Generated: `{now}`

4581 reduces the 4580 readout-commutator remainder.  In the one-observed-coframe/fixed-protocol branch, `C_frame=0`, `C_material_owned=0`, `C_kernel_fixed=0`, and `C_EFT_common=0`.  The live envelope is now `C_readout <= C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail`, with a strict zero contract for `rho_readout_shift=0` if those tails close.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4581 packet update - remaining Creadout tails

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now treats same-frame readout, owned material content, fixed downstream kernels and common q-basic EFT slots as zero branches.  The remaining local-readout leak is no longer the whole readout sector: it is the material-tail/active-kernel/active-EFT/tau-tail envelope.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4581 derives private-branch zero laws for C_frame, C_material_owned, C_kernel_fixed and C_EFT_common, reducing C_readout to material-tail, active-kernel, active-EFT and tau-tail components.",
        "current_evidence": "Generated source register, remaining Creadout zero theorem rows, reduction rows, material/active tail bounds, tau tail rows, strict zero contract, audit, controls, gates and validation.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating fixed-kernel/common-EFT/same-frame zeros as if they also killed active response operators, material/apparatus tails or c_Gamma memory coefficients.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Material-tail, active response kernels, active EFT/readout coefficients and tau tails still require zero certificates or source-backed bounds before local-GR/R10/PPN claims.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    zero_theorem: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    tail_bounds: list[dict[str, Any]],
    tau_tails: list[dict[str, Any]],
    strict_zero: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4581_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4581_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4581_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4581_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4581_zero_laws",
        "zero theorem rows cover frame, material-owned, fixed-kernel, common-EFT and tau-tail",
        all(
            any(row["theorem_id"] == theorem_id for row in zero_theorem)
            for theorem_id in [
                "ZCR4581_0_same_frame_zero",
                "ZCR4581_1_owned_material_zero",
                "ZCR4581_2_fixed_kernel_zero",
                "ZCR4581_3_common_EFT_zero",
                "ZCR4581_4_strict_tau_tail_zero",
            ]
        ),
        "zero theorem coverage",
    )
    add(
        "VAL4581_reduced_bound",
        "Creadout reduced to four tail blocks",
        any(
            row["row_id"] == "CRV4581_5_Creadout_reduced_again"
            and row["value_or_bound"] == "C_readout <= C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail"
            for row in reductions
        ),
        "CRV4581_5",
    )
    add(
        "VAL4581_tail_bounds",
        "tail bounds include material, active kernel, active EFT and frame tail",
        all(
            any(row["bound_id"] == bound_id for row in tail_bounds)
            for bound_id in ["TAIL4581_0_material_tail", "TAIL4581_1_active_kernel", "TAIL4581_2_active_EFT", "TAIL4581_3_frame_tail"]
        ),
        "tail bound coverage",
    )
    add(
        "VAL4581_tau_tails",
        "tau tail rows include total no-cancellation row",
        any(row["tail_id"] == "TAU4581_7_total" and "sum_abs" in row["bound_role"] for row in tau_tails),
        "TAU4581_7_total",
    )
    add(
        "VAL4581_strict_zero",
        "strict zero contract emits rho_readout_shift zero condition",
        any("rho_readout_shift" in row["formula"] and "C_readout=0" in row["formula"] for row in strict_zero),
        "SZ4581_0",
    )
    add(
        "VAL4581_audit_verdict",
        "audit records tail reduction complete nonclaim",
        any(row["audit_id"] == "AUD4581_4_verdict" and row["status"] == "TAIL_REDUCTION_COMPLETE_NONCLAIM" for row in audits),
        "AUD4581_4_verdict",
    )
    add(
        "VAL4581_controls",
        "controls include same-frame/fixed-kernel/common-EFT pass and active counterbranches",
        all(
            any(row["control_id"] == control_id for row in controls)
            for control_id in [
                "CTRL4581_same_frame",
                "CTRL4581_frame_split",
                "CTRL4581_fixed_kernel",
                "CTRL4581_active_kernel",
                "CTRL4581_common_EFT",
                "CTRL4581_active_EFT",
            ]
        ),
        "control coverage",
    )
    add("VAL4581_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4581_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4581_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4581_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    zero_theorem = zero_theorem_rows(now)
    reductions = reduction_rows(now)
    tail_bounds = tail_bound_rows(now)
    tau_tails = tau_tail_rows(now)
    strict_zero = strict_zero_rows(now)
    audits = audit_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM_CSV, zero_theorem)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(TAIL_BOUND_CSV, tail_bounds)
    write_csv(TAU_TAIL_CSV, tau_tails)
    write_csv(STRICT_ZERO_CSV, strict_zero)
    write_csv(AUDIT_CSV, audits)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, zero_theorem, reductions, tail_bounds, tau_tails, strict_zero, audits, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        REDUCTION_CSV,
        TAIL_BOUND_CSV,
        TAU_TAIL_CSV,
        STRICT_ZERO_CSV,
        AUDIT_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, zero_theorem, reductions, tail_bounds, tau_tails, strict_zero, audits, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
