from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4594"
CLAIM_ID = "L-436"
BRANCH_ID = "MTS_R2FR_Y5_CR2_MR_AFTER_TORSION_4594"
MARKER = "PPC4161_CR2_MR_PARENT_SCALE_GAP_OR_FULL_FINITE_RANGE_BOUND_AFTER_TORSION_4594"
PACKET_MARKER = "PPC4161_PACKET_CR2_MR_PARENT_SCALE_GAP_OR_FULL_FINITE_RANGE_BOUND_AFTER_TORSION_4594"
DECISION = "CR2_MR_REDUCED_TO_PARENT_EXTRA_MODE_ZERO_OR_COMPONENTWISE_SCALARON_BODY_CHARGE_BOUND_NONCLAIM"
NEXT_TARGET = "4595-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"

DOC_PATH = POST / "4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
FORMAL_PATH = FORMAL / "610-PPC4161-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4594_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_CR2_ZERO_BOUND_THEOREM.csv"
PROFILE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_FINITE_RANGE_PROFILE_LAW.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_R10_ORBITAL_BOUND_INTERFACE.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4594_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4594_VALIDATION.csv"

DOC_4593 = POST / "4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"
FORMAL_609 = FORMAL / "609-PPC4161-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"
CSV_4593_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4593_NEXT_TARGET.csv"
CSV_4593_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4593_SURVIVOR_UPDATE.csv"
DOC_4454 = POST / "4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md"
FORMAL_470 = FORMAL / "470-PPC4161-cR2-MR-parent-scale-or-short-range-orbital-bound.md"
FORMAL_471 = FORMAL / "471-PPC4161-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"
FORMAL_474 = FORMAL / "474-PPC4161-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md"
FORMAL_486 = FORMAL / "486-PPC4161-parent-two-derivative-no-extra-mode-selector-signature-or-cR2-coefficient-intake.md"
FORMAL_487 = FORMAL / "487-PPC4161-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
DOC_4504 = POST / "4504-Y5-R2FR-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
DOC_4505 = POST / "4505-Y5-R2FR-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
FORMAL_520 = FORMAL / "520-PPC4161-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
FORMAL_521 = FORMAL / "521-PPC4161-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
CSV_4454_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4454_STATUS.csv"
CSV_4455_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4455_STATUS.csv"
CSV_4457_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4457_STATUS.csv"
CSV_4458_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4458_STATUS.csv"
CSV_4504_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4504_STATUS.csv"
CSV_4505_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4505_STATUS.csv"
CSV_4505_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4505_CR2_ZERO_THEOREM.csv"
CSV_4505_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4505_SCALARON_BOUND_CONTRACT.csv"
CSV_4505_PRESSURE = SOURCE_DIR / "P8_Y5_R2FR_4505_DIRECT_SCALAR_PRESSURE_ROWS.csv"
CSV_4561_EFT = SOURCE_DIR / "P8_Y5_R2FR_4561_RESIDUAL_EFT_ENVELOPE_REFRESH.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4594 integrates the c_R2/M_R curvature-square ladder after torsion narrowing: local finite-range curvature modes close only by a parent two-derivative/no-extra-mode selector, componentwise c_R2_eff_total zero, scalaron/body-charge zero, or a source-backed finite R10/orbital/PPN bound.",
        "current_evidence": "Generated cR2 zero/bound theorem, finite-range profile law, R10/orbital bound interface, survivor update, controls, gates and validation.",
        "status": "cr2_mr_zero_or_componentwise_scalaron_body_charge_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using exterior source-free/Ricci-flat language, an alpha=1 anchor, or positive no-hair as if it proved c_R2/M_R closure while body charge, hidden curvature vertices, spin-2 channels or projection coefficients remain live.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until memory/fibre source-charge rows, cGamma, EH adoption, projection/material rows and global parent signatures are closed or source-backed.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    try:
        result = subprocess.run(["git", "-C", str(path), "status", "--short"], text=True, capture_output=True, check=False)
    except OSError:
        return False
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4594_00_4593_doc", DOC_4593, "SURV4593_2_cR2_MR", "4593 selected c_R2/M_R as next broad survivor."),
        ("SRC4594_01_609_formal", FORMAL_609, "SURV4593_2_cR2_MR", "formal 609 handoff to c_R2/M_R."),
        ("SRC4594_02_4593_next", CSV_4593_NEXT, "4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md", "machine-readable next target."),
        ("SRC4594_03_4593_survivor", CSV_4593_SURVIVOR, "SURV4593_2_cR2_MR", "machine-readable survivor row."),
        ("SRC4594_04_4454_doc", DOC_4454, "Mapped `c_R2/M_R`", "curvature-square to Yukawa map."),
        ("SRC4594_05_470_formal", FORMAL_470, "Phi(r) = -G M/r", "formal Yukawa potential map."),
        ("SRC4594_06_471_projection", FORMAL_471, "alpha_0 = +1/3", "standard scalar/spin-2 alpha template."),
        ("SRC4594_07_474_basis", FORMAL_474, "MTS Quadratic Coefficient Normalization", "MTS quadratic coefficient basis map."),
        ("SRC4594_08_486_selector", FORMAL_486, "two-derivative", "parent two-derivative/no-extra-mode selector source."),
        ("SRC4594_09_487_grain", FORMAL_487, "cR2eff", "local grain/no-length-scale cR2 effective intake source."),
        ("SRC4594_10_4504_doc", DOC_4504, "So a live scalaron tail is not locally silent", "scalaron Hessian non-silence theorem."),
        ("SRC4594_11_4505_doc", DOC_4505, "B^T L^-1 B", "positive hidden-block theorem."),
        ("SRC4594_12_520_formal", FORMAL_520, "c_R2_eff_total_or_scalaron_body_charge", "formal 4504 scalaron gate."),
        ("SRC4594_13_521_formal", FORMAL_521, "A_body=0 iff", "formal body-charge law."),
        ("SRC4594_14_4454_status", CSV_4454_STATUS, "mapped_to_scalar_tensor_yukawa_modes", "4454 status."),
        ("SRC4594_15_4455_status", CSV_4455_STATUS, "alpha0=1/3_alpha2=-4/3_template_written", "4455 projection status."),
        ("SRC4594_16_4457_status", CSV_4457_STATUS, "canonical_M0_M2_formula_contract_written", "4457 pole mass contract."),
        ("SRC4594_17_4458_status", CSV_4458_STATUS, "basis_map_derived_parent_values_missing", "4458 MTS normalization status."),
        ("SRC4594_18_4504_status", CSV_4504_STATUS, "c_R2_eff_total_or_scalaron_body_charge", "4504 first open component."),
        ("SRC4594_19_4505_status", CSV_4505_STATUS, "memory_class_scalar;finite_fibre_spectrum", "4505 direct scalar pressure status."),
        ("SRC4594_20_4505_zero_csv", CSV_4505_ZERO, "ZC4505_1_positive_hidden_block", "machine-readable positive hidden block."),
        ("SRC4594_21_4505_bound_csv", CSV_4505_BOUND, "SCB4505_1_body_charge_bound", "machine-readable body-charge bound."),
        ("SRC4594_22_4505_pressure_csv", CSV_4505_PRESSURE, "DSPR4505_0_memory", "machine-readable direct pressure row."),
        ("SRC4594_23_4561_eft", CSV_4561_EFT, "RE4561_1_cR2", "latest residual EFT envelope cR2 row."),
        ("SRC4594_24_claim_435", CLAIMS_PATH, "L-435", "claim-register handoff from 4593."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(line > 0),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4594_0_mode_decomposition",
            "claim": "The c_R2/M_R survivor is a finite-range extra-mode problem, not a generic source-kernel residue.",
            "derivation": "4454-4458 map curvature-square terms into scalar/tensor Yukawa channels with alpha_i and M_i, while 4593 has already isolated torsion.",
            "zero_or_exit": "parent two-derivative/no-extra-mode selector sets all curvature-square propagating coefficients to zero",
            "finite_bound": "Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r); compare each channel without cross-cancellation",
            "status": "CR2_MODE_DECOMPOSITION_INTEGRATED_AFTER_TORSION",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4594_1_componentwise_zero",
            "claim": "Without a named parent identity, c_R2_eff_total closes only by componentwise zero/topological/boundary silence.",
            "derivation": "4504-4505 give c_R2_eff_total=c_cell+c_bare+0.5 B^T L^-1 B+c_measure+c_boundary+c_marker.",
            "zero_or_exit": "c_cell=c_bare=c_measure=c_boundary=c_marker=0 and B_X=0 on every retained physical hidden/memory/fibre direction, or a parent Ward/topological identity proves the sum is identically zero",
            "finite_bound": "|c_R2_eff_total| <= sum absolute component bounds; no tuned cancellation credit",
            "status": "COMPONENTWISE_ZERO_OR_ABSOLUTE_BOUND_REQUIRED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4594_2_positive_hidden_obstruction",
            "claim": "Positive hidden/memory/fibre no-hair is insufficient; the curvature-linear vertex must vanish.",
            "derivation": "If L is positive on the physical quotient, B^T L^-1 B = ||L^-1/2 B||^2 >= 0 and equals zero only when B=0 on the physical subspace.",
            "zero_or_exit": "B_mem=B_h=0, plus C/J/boundary source charges zero if those fields couple to matter/source readout",
            "finite_bound": "0.5 B^T L^-1 B <= 0.5 ||B||^2/lambda_min(L) with source-backed B and lambda_min rows",
            "status": "NO_XR_VERTEX_REQUIRED_NOT_OPTIONAL",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4594_3_body_charge_zero",
            "claim": "Exterior source-free equations do not erase scalaron tails; body and boundary charge must vanish or be bounded.",
            "derivation": "4505 writes the Green-function law for (-Z_X nabla^2+M_X^2)X=rho_X. The exterior amplitude A_body is a weighted interior/boundary charge.",
            "zero_or_exit": "A_body=0 iff Q_X[body]+Q_boundary=0 under the selected Green-function convention",
            "finite_bound": "|A_body| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary|]/(4*pi |Z_X|)",
            "status": "BODY_CHARGE_ZERO_OR_BOUND_REQUIRED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4594_4_empirical_range_bound",
            "claim": "If parent zero/body-charge zero fails, c_R2/M_R must be scored as a finite-range Yukawa/scalar-Hessian branch.",
            "derivation": "4454 supplies the alpha=1 short-range anchor, while 4504 supplies the Hessian profile. Neither is enough alone for an MTS claim.",
            "zero_or_exit": "M_i L_arena >> 1, or full source-backed alpha_i(lambda_i)/A_body projection lies below R10, orbital and PPN bounds",
            "finite_bound": "R10: |alpha_X(lambda)| <= alpha_bound(lambda); orbital: |Delta a/a_N|=|alpha|(1+r/lambda)exp(-r/lambda); Hessian: H_R=|A_body| exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3)",
            "status": "FINITE_RANGE_SCORE_SHAPE_READY_INPUTS_UNSIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def profile_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "FR4594_0_standard_yukawa",
            "target": "curvature-square weak-field potential",
            "formula": "Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)",
            "zero_condition": "all alpha_i=0 or M_i L_arena >> 1 with source-backed lower M_i",
            "needed_inputs": "alpha_i;M_i;arena radius;source/test projection;no-cancellation convention",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "FR4594_1_standard_R2_scalaron",
            "target": "R2/fR scalaron",
            "formula": "R(r)=A_body exp(-m_R r)/r; H_R=|A_body| exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3)",
            "zero_condition": "c_R2_eff_total=0 or A_body=0",
            "needed_inputs": "A_body;m_R;MTS-to-mu normalization;screening/source convention",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "FR4594_2_hidden_memory_fibre",
            "target": "integrated-out memory/fibre scalar contribution",
            "formula": "Delta c_R2_hidden = 0.5 B^T L^-1 B; if L>0 then zero iff B=0",
            "zero_condition": "B_mem=B_h=0 on physical quotient plus source/boundary charge silence",
            "needed_inputs": "Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;Z_h;M2_h;B_h;C_h;J_h;Q_boundary_h",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "FR4594_3_anchor_only_short_range",
            "target": "Eot-Wash alpha=1 anchor",
            "formula": "lambda < 38.6 um for alpha approx 1; M > 0.0051121 eV for a single gravitational-strength Yukawa",
            "zero_condition": "not a zero theorem; anchor only",
            "needed_inputs": "claim-grade alpha(lambda) curve and MTS alpha_i(lambda_i) projection",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "B4594_0_R10_curve",
            "arena": "R10 short-range inverse-square tests",
            "formula": "|alpha_X(lambda)| <= alpha_bound(lambda)",
            "status": "FULL_CURVE_AND_MTS_PROJECTION_REQUIRED",
            "missing_inputs": "claim-grade alpha_bound(lambda);alpha_X mapping;lambda_X;source/test charges;units",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "B4594_1_R10_anchor",
            "arena": "R10 alpha=1 anchor",
            "formula": "lambda<38.6um -> M>0.0051121eV for alpha=1 single-Yukawa",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "missing_inputs": "not valid for non-alpha=1 or multi-channel MTS projection without curve",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "B4594_2_orbital_large_lambda",
            "arena": "orbital/inverse-square acceleration",
            "formula": "|Delta a/a_N|=|alpha|(1+r/lambda)exp(-r/lambda)",
            "status": "FORMULA_READY_VALUES_UNSIGNED",
            "missing_inputs": "alpha;lambda;arena radius;ephemeris/orbital threshold;projection convention",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "B4594_3_PPN_scalaron",
            "arena": "PPN beta/gamma scalaron branch",
            "formula": "standard template: mu <= 1.443476e15 m^2 and lambda_R <= 9.306372e7 m only if MTS-to-f(R) map is signed",
            "status": "STANDARD_TEMPLATE_READY_MTS_NORMALIZATION_UNSIGNED",
            "missing_inputs": "N_MTS_to_fR;c_R2_eff_total;A_body/screening;source convention",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def survivor_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4594_0_EH_principal",
            "residual_family": "EH principal / public parent adoption",
            "status_after_4594": "still public blocker",
            "next_action": "retain parent selector/adoption gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4594_1_cGamma",
            "residual_family": "c_Gamma local memory coupling",
            "status_after_4594": "unchanged finite survivor",
            "next_action": "derive memory support/projector zero or source profile coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4594_2_cR2_MR",
            "residual_family": "c_R2/M_R finite-range curvature-square branch",
            "status_after_4594": "reduced to parent extra-mode zero, componentwise c_R2_eff_total zero, A_body zero, or finite source-backed bound",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4594_3_cT_spin",
            "residual_family": "spin/torsion contact channel",
            "status_after_4594": "conditional spinless zero retained from 4593; finite contact branch remains",
            "next_action": "do not reopen unless polarized/contact torsion is selected",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4594_4_material_projection_global",
            "residual_family": "Lambda/material/projection/global parent",
            "status_after_4594": "unchanged blockers",
            "next_action": "keep promotion firewall active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4594_two_derivative_selector",
            "input_branch": "parent two-derivative/no-extra-mode selector signed",
            "expected_result": "all c_R2/M_R finite-range modes zero",
            "control_status": "SYMBOLIC_ZERO_ROUTE_PASS_PARENT_SIGNATURE_STILL_PRIVATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4594_positive_B_nonzero",
            "input_branch": "L positive and B_X != 0",
            "expected_result": "B^T L^-1 B > 0, so c_R2_eff remains live",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4594_exterior_source_free",
            "input_branch": "exterior source vanishes but A_body != 0",
            "expected_result": "Yukawa exterior tail survives; no local-GR closure",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4594_alpha_anchor_only",
            "input_branch": "only alpha=1 38.6um anchor is available",
            "expected_result": "anchor is nonclaim unless full curve/projection maps are supplied",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_0_sources_exist", "claim": "all local source paths exist", "passed": "PENDING_VALIDATION", "valid_for_claim": "False", "detail": "validated after source register generation", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_1_needles_found", "claim": "all local source needles found", "passed": "PENDING_VALIDATION", "valid_for_claim": "False", "detail": "validated after source register generation", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_2_zero_law_written", "claim": "c_R2_eff_total/A_body zero law is written", "passed": "True", "valid_for_claim": "False", "detail": "componentwise c_R2_eff_total=0 or A_body=0", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_3_finite_bounds_written", "claim": "finite R10/orbital/PPN bound interface is written", "passed": "True", "valid_for_claim": "False", "detail": "alpha(lambda), orbital acceleration and Hessian profiles recorded", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_4_countermodels_kept", "claim": "positive B, body charge and anchor-only countermodels are retained", "passed": "True", "valid_for_claim": "False", "detail": "no closure smuggling", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_5_no_public_claim", "claim": "no cR2/local-GR public pass is emitted", "passed": "True", "valid_for_claim": "False", "detail": "parent signature and numeric projection rows still missing", "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4594_6_next_target_written", "claim": "next direct owner target selected", "passed": "True", "valid_for_claim": "False", "detail": NEXT_TARGET, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "mode_decomposition_integrated": "True",
            "componentwise_zero_law": "True",
            "body_charge_law": "True",
            "finite_bound_interface": "True",
            "parent_zero_or_numeric_bound_signed": "False",
            "local_GR_public_claim": "False",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "cR2_status": "exact zero exits and finite profile bounds derived; parent/numeric rows unsigned",
            "strict_zero_exits": "two_derivative_selector;c_R2_eff_total=0;A_body=0;M_i L_arena>>1",
            "finite_bound_exits": "R10_alpha_curve;orbital_acceleration;PPN_scalaron;Hessian_AE",
            "remaining_broad_survivors": "EH_public_adoption;cGamma;memory_fibre_BC_source_charge;Lambda_material_projection;global_parent",
            "local_GR_public_claim": "False",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "generated_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "4594 reduces c_R2/M_R to the live direct pressure rows: memory/class scalar and finite-cell fibre B/C/source-charge owners.",
            "derive_first": "prove B_mem=C_mem=J_mem=Q_boundary_mem=0 and B_h=C_h=J_h=Q_boundary_h=0 from parent object-language or action-inventory exclusion",
            "fallback": "source Z,M2,B,C,J,Q_boundary/body profiles and execute the scalaron R10/orbital/PPN finite bound contracts",
            "valid_for_claim": "False",
        }
    ]


def write_docs(now: str, tables: dict[str, list[dict[str, Any]]]) -> None:
    source_table = markdown_table(tables["sources"])
    theorem_table = markdown_table(tables["theorem"])
    profile_table = markdown_table(tables["profile"])
    bound_table = markdown_table(tables["bound"])
    survivor_table = markdown_table(tables["survivor"])
    control_table = markdown_table(tables["control"])
    promotion_table = markdown_table(tables["promotion"])
    decision_table = markdown_table(tables["decision"])
    status_table = markdown_table(tables["status"])
    next_table = markdown_table(tables["next"])

    body = f"""# 4594 Y5 R2FR cR2/MR parent scale gap or full finite-range bound after torsion

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4594 moves the next broad local-GR survivor from a label into a hard zero-or-bound law.

After the source-kernel branch and torsion/spin branch are narrowed, `c_R2/M_R` is the finite-range curvature-square branch. The weak-field shape is:

```text
Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)
lambda_i = 1/M_i.
```

The strict exits are:

```text
1. parent two-derivative/no-extra-mode selector;
2. componentwise c_R2_eff_total = 0;
3. scalaron/body charge A_body = 0;
4. M_i L_arena >> 1 with parent-owned lower mass scale;
5. source-backed finite bound below R10/orbital/PPN thresholds.
```

The central no-smuggling law is:

```text
c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary + c_marker.
```

If `L` is positive on the physical quotient,

```text
B^T L^-1 B = ||L^-1/2 B||^2 >= 0,
```

so positive no-hair alone does **not** close the branch. The curvature-linear vertex `B` must vanish, or it must be bounded.

The exterior scalaron tail is also not erased by source-free exterior equations:

```text
R(r) = A_body exp(-m_R r)/r,
A_body = weighted interior/body charge + boundary charge.
```

So `c_R2/M_R` closes only by parent zero, body-charge zero, parent heavy scale, or a real finite comparison. No public local-GR/R10/PPN claim is emitted.

## Source Register

{source_table}

## cR2 Zero/Bound Theorem

{theorem_table}

## Finite-Range Profile Law

{profile_table}

## R10/Orbital Bound Interface

{bound_table}

## Survivor Update

{survivor_table}

## Controls

{control_table}

## Promotion Gates

{promotion_table}

## Decision

{decision_table}

## Status

{status_table}

## Next Target

{next_table}
"""
    write_text(DOC_PATH, body)

    formal_body = f"""# 610 PPC4161 cR2/MR parent scale gap or full finite-range bound after torsion

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4594 integrates the c_R2/M_R finite-range ladder after 4593. The live branch is:

```text
Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)
```

with exact closure only by parent no-extra-mode selection, componentwise `c_R2_eff_total=0`, scalaron/body-charge zero, parent-owned heavy mass scale, or source-backed finite R10/orbital/PPN bound.

The key obstruction is:

```text
c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary + c_marker.
```

For positive `L`, `B^T L^-1 B=||L^-1/2 B||^2`, so hidden/memory/fibre curvature vertices must be killed or bounded. Exterior source-free equations do not erase `A_body`.

The next owner target is `{NEXT_TARGET}`.

## Theorem Rows

{theorem_table}

## Bound Interface

{bound_table}

## Survivor Update

{survivor_table}

## Decision

{decision_table}
"""
    write_text(FORMAL_PATH, formal_body)


def append_spine_and_packet() -> None:
    spine_block = f"""## PPC4161 Local Addendum - cR2/MR Finite-Range Gate After Torsion

Marker: `{MARKER}`
Source checkpoint: `4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md`

After source-kernel and torsion narrowing, `c_R2/M_R` is reduced to an exact finite-range gate: parent two-derivative/no-extra-mode selector, componentwise `c_R2_eff_total=0`, scalaron/body-charge zero, parent heavy mass scale, or a source-backed R10/orbital/PPN finite bound. Positive hidden-sector no-hair is not enough; if `B^T L^-1 B` is live, the curvature-linear vertex `B` must be owned.
"""
    packet_block = f"""## PPC4161 Packet Addendum - cR2/MR Finite-Range Gate After Torsion

Marker: `{PACKET_MARKER}`
Source checkpoint: `4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md`

The private local packet now has a hard c_R2/M_R gate instead of a vague higher-curvature survivor. The next direct pressure rows are memory/class scalar and finite-cell fibre source-charge owners: `B_mem,C_mem,J_mem,Q_boundary_mem` and `B_h,C_h,J_h,Q_boundary_h`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        PROFILE_CSV,
        BOUND_CSV,
        SURVIVOR_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]

    def pass_row(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool_text(passed), "detail": detail, "valid_for_claim": "False"}

    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] == "True" for row in tables["sources"])
    needle_ok = all(row["needle_found"] == "True" for row in tables["sources"])
    rows.append(pass_row("VAL4594_00_source_paths_exist", source_ok, "all source-register local paths exist"))
    rows.append(pass_row("VAL4594_01_needles_found", needle_ok, "all source-register needles found"))

    for csv_path in generated_csvs:
        parsed = read_csv(csv_path)
        rows.append(pass_row(f"VAL4594_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows"))

    no_claim_true = True
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            if str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true":
                no_claim_true = False
    rows.append(pass_row("VAL4594_12_no_claim_rows_true", no_claim_true, "generated rows keep valid_for_claim/claim_allowed false"))

    theorem_text = " ".join(str(value) for row in tables["theorem"] for value in row.values())
    profile_text = " ".join(str(value) for row in tables["profile"] for value in row.values())
    bound_text = " ".join(str(value) for row in tables["bound"] for value in row.values())
    control_text = " ".join(str(value) for row in tables["control"] for value in row.values())
    rows.append(pass_row("VAL4594_13_component_zero_law", "c_R2_eff_total" in theorem_text and "B^T L^-1 B" in theorem_text, "componentwise c_R2 law present"))
    rows.append(pass_row("VAL4594_14_body_charge_law", "A_body=0" in theorem_text and "Q_X[body]+Q_boundary" in theorem_text, "body-charge zero law present"))
    rows.append(pass_row("VAL4594_15_finite_profiles", "Phi/Phi_N" in profile_text and "H_R=" in profile_text, "finite-range Yukawa/Hessian profiles present"))
    rows.append(pass_row("VAL4594_16_r10_orbital_bounds", "alpha_bound(lambda)" in bound_text and "38.6um" in bound_text and "Delta a/a_N" in bound_text, "R10 anchor, curve gate and orbital bound present"))
    rows.append(pass_row("VAL4594_17_countermodels", "B_X != 0" in control_text and "A_body != 0" in control_text and "alpha=1" in control_text, "countermodels retained"))
    rows.append(pass_row("VAL4594_18_next_memory_fibre", NEXT_TARGET in read_text(NEXT_CSV), "next memory/fibre owner target selected"))
    rows.append(pass_row("VAL4594_19_doc_written", DOC_PATH.exists() and MARKER in read_text(DOC_PATH), f"{DOC_PATH} written"))
    rows.append(pass_row("VAL4594_20_formal_written", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), f"{FORMAL_PATH} written"))
    rows.append(pass_row("VAL4594_21_claim_register", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), f"{CLAIM_ID} in claims register"))
    rows.append(pass_row("VAL4594_22_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present"))
    rows.append(pass_row("VAL4594_23_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present"))
    rows.append(pass_row("VAL4594_24_public_stage_clean", git_clean(PUBLIC_STAGE), "public-stage git status remains clean or repo absent"))
    rows.append(pass_row("VAL4594_25_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo git status remains clean or repo absent"))
    return rows


def update_promotion_with_validation(tables: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_ok = next(row for row in validation_rows if row["check_id"] == "VAL4594_00_source_paths_exist")["passed"]
    needle_ok = next(row for row in validation_rows if row["check_id"] == "VAL4594_01_needles_found")["passed"]
    updated = []
    for row in tables["promotion"]:
        row = dict(row)
        if row["gate_id"] == "PROM4594_0_sources_exist":
            row["passed"] = source_ok
        if row["gate_id"] == "PROM4594_1_needles_found":
            row["passed"] = needle_ok
        updated.append(row)
    return updated


def main() -> int:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "profile": profile_rows(now),
        "bound": bound_rows(now),
        "survivor": survivor_rows(now),
        "control": control_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(PROFILE_CSV, tables["profile"])
    write_csv(BOUND_CSV, tables["bound"])
    write_csv(SURVIVOR_CSV, tables["survivor"])
    write_csv(CONTROL_CSV, tables["control"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])

    write_docs(now, tables)
    append_spine_and_packet()
    append_claim_once()

    validation_rows = validate(tables)
    tables["promotion"] = update_promotion_with_validation(tables, validation_rows)
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_docs(now, tables)
    validation_rows = validate(tables)
    write_csv(VALIDATION_CSV, validation_rows)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"validation {len(validation_rows) - len(failed)}/{len(validation_rows)} passed")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
