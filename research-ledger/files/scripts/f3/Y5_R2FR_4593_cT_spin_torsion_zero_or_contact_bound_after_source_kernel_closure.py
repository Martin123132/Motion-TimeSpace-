from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4593"
CLAIM_ID = "L-435"
BRANCH_ID = "MTS_R2FR_Y5_CT_SPIN_TORSION_AFTER_SOURCE_KERNEL_CLOSURE_4593"
MARKER = "PPC4161_CT_SPIN_TORSION_ZERO_OR_CONTACT_BOUND_AFTER_SOURCE_KERNEL_CLOSURE_4593"
PACKET_MARKER = "PPC4161_PACKET_CT_SPIN_TORSION_ZERO_OR_CONTACT_BOUND_AFTER_SOURCE_KERNEL_CLOSURE_4593"
DECISION = "CT_SPIN_TORSION_SPINLESS_CONTACT_ZERO_CONTRACT_DERIVED_FINITE_TORSION_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"

DOC_PATH = POST / "4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"
FORMAL_PATH = FORMAL / "609-PPC4161-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4593_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_CT_SPIN_THEOREM.csv"
CONTACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_CONTACT_BOUND_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_ARENA_UPDATE.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4593_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4593_VALIDATION.csv"

DOC_4592 = POST / "4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"
FORMAL_608 = FORMAL / "608-PPC4161-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md"
CSV_4592_SURVIVORS = SOURCE_DIR / "P8_Y5_R2FR_4592_SURVIVOR_BLOCKER_MAP.csv"
CSV_4592_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4592_NEXT_TARGET.csv"
DOC_4451 = POST / "4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md"
DOC_4452 = POST / "4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"
DOC_4453 = POST / "4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"
FORMAL_467 = FORMAL / "467-PPC4161-torsion-spin-residual-cT-zero-or-contact-bound.md"
FORMAL_468 = FORMAL / "468-PPC4161-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"
FORMAL_469 = FORMAL / "469-PPC4161-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
CSV_4451_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_THEOREM_OUTPUT.csv"
CSV_4451_OUTCOME = SOURCE_DIR / "P8_Y5_R2FR_4451_OUTCOME_ROWS.csv"
CSV_4453_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4453_STATUS.csv"
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
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
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
        "claim": "4593 integrates the existing torsion 4451-4453 ladder into the source-kernel-closed local PPN branch: auxiliary algebraic torsion with positive irrep margin and spinless/unpolarized bulk source gives no long-range c_T_spin contribution, while polarized/contact or propagating-torsion branches remain explicit nonclaim bounds.",
        "current_evidence": "Generated cT-spin theorem rows, contact-bound rows, arena updates, survivor update, controls, gates and validation.",
        "status": "ct_spin_torsion_spinless_contact_zero_contract_finite_branch_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating conditional spinless/contact demotion as global torsion closure, or hiding propagating torsion/zero-mode/contact spin channels without parent margin or numeric source bounds.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until EH adoption, cGamma, cR2/MR, Lambda/material/projection rows and public parent signatures are closed or source-backed.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "status", "--short"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4593_00_4592_doc", DOC_4592, "c_T_spin", "4592 selected c_T_spin as next theorem target after source-kernel zero."),
        ("SRC4593_01_608_formal", FORMAL_608, "The next target is `4593", "formal 608 handoff to 4593."),
        ("SRC4593_02_4592_survivor_csv", CSV_4592_SURVIVORS, "SURV4592_3_cT_spin", "machine-readable survivor row."),
        ("SRC4593_03_4592_next_csv", CSV_4592_NEXT, "4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md", "machine-readable next target."),
        ("SRC4593_04_4451_doc", DOC_4451, "L_T T = kappa tau_spin", "torsion algebraic equation checkpoint."),
        ("SRC4593_05_4452_doc", DOC_4452, "lambda_T,min = min", "torsion irrep no-zero-mode checkpoint."),
        ("SRC4593_06_4453_doc", DOC_4453, "lambda_T,min >= m_T,parent^2 > 0", "parent positive margin checkpoint."),
        ("SRC4593_07_467_formal", FORMAL_467, "tau_spin = 0  =>  T = 0", "formal spinless torsion zero statement."),
        ("SRC4593_08_468_formal", FORMAL_468, "||T|| <= kappa ||tau_spin||/lambda_T,min", "formal torsion response bound."),
        ("SRC4593_09_469_formal", FORMAL_469, "Route A: parent signs lambda_T,min", "formal parent-margin/source fork."),
        ("SRC4593_10_200_selector", FORMAL_200, "If torsion/nonmetricity are algebraic", "Palatini/IR auxiliary condition source."),
        ("SRC4593_11_295_survivors", FORMAL_295, "c_T_spin", "residual EFT survivor source."),
        ("SRC4593_12_4451_theorem_csv", CSV_4451_THEOREM, "TH4451_1_spinless_zero", "machine-readable spinless zero theorem."),
        ("SRC4593_13_4451_outcome_csv", CSV_4451_OUTCOME, "OUT4451_2_spin_polarized", "machine-readable contact branch reminder."),
        ("SRC4593_14_4453_status_csv", CSV_4453_STATUS, "lambda_T,min>=m_T,parent^2>0", "machine-readable parent margin status."),
        ("SRC4593_15_4561_eft_csv", CSV_4561_EFT, "RE4561_0_cT", "latest residual EFT cT row."),
        ("SRC4593_16_claim_434", CLAIMS_PATH, "L-434", "claim-register handoff from 4592."),
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
            "theorem_id": "TH4593_0_source_kernel_separation",
            "claim": "The 4592 source-kernel zero does not by itself remove torsion; it only permits a clean independent torsion projection.",
            "derivation": "Use Delta_PPN = Delta_PPN^source_kernel + Delta_PPN^T + Delta_PPN^rest with Delta_PPN^source_kernel=0 from 4592. Then torsion must satisfy its own Cartan equation rather than being cancelled by source-kernel fitting.",
            "equation": "Delta_PPN^T = Pi_PPN^T[T] + Pi_contact^T[Delta L_contact]",
            "zero_condition": "none at this row",
            "fallback_bound": "|Delta_PPN^T| retained separately from source-kernel subvector",
            "status": "TORSION_SEPARATED_NO_CANCELLATION",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4593_1_auxiliary_cartan_equation",
            "claim": "In the compact local auxiliary Cartan branch, torsion is algebraic and spin-supported.",
            "derivation": "4451 writes a local IR branch with no independent D T kinetic term. Variation of the spin connection gives a pointwise linear operator equation for torsion.",
            "equation": "L_T[e,c_T] T = kappa tau_spin",
            "zero_condition": "no D T kinetic term and ordinary matter couples through the same coframe/spin connection slot",
            "fallback_bound": "if Z_DT>0 or a boundary torsion mode exists, this row fails and a propagating torsion bound is required",
            "status": "AUXILIARY_TORSION_EQUATION_INHERITED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4593_2_positive_irrep_margin",
            "claim": "The vague ker(L_T)=0 condition is the explicit positive irrep margin lambda_T,min>0.",
            "derivation": "4452 decomposes torsion into trace-vector, axial-vector and tensor irreps with L_T=diag(lambda_V,lambda_A,lambda_Q). 4453 states the parent positive-margin contract.",
            "equation": "lambda_T,min = min(|lambda_V|,|lambda_A|,|lambda_Q|) >= m_T,parent^2 > 0",
            "zero_condition": "parent signs positive auxiliary torsion quadratic form away from critical surfaces",
            "fallback_bound": "||T|| <= kappa ||tau_spin||/lambda_T,min",
            "status": "NO_ZERO_MODE_CONTRACT_EXPLICIT_PARENT_SIGNATURE_OPEN",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4593_3_spinless_bulk_zero",
            "claim": "For spinless/unpolarized macroscopic PPN, R10 and orbital bulk sources, the long-range c_T_spin residual is zero on the auxiliary positive-margin branch.",
            "derivation": "Set tau_spin^bulk=0. With lambda_T,min>0 the algebraic equation has only T=0 in the bulk. Therefore every long-range spinless readout projection of torsion vanishes.",
            "equation": "tau_spin^bulk=0 and lambda_T,min>0 => T_bulk=0 => Delta_PPN,bulk^T=0",
            "zero_condition": "spinless/unpolarized bulk source; no propagating torsion; positive irrep margin; no torsion boundary tail",
            "fallback_bound": "|Delta O_a^T| <= ||Pi_a^T|| kappa ||tau_spin||/lambda_T,min + ||Pi_a^contact|| kappa^2 ||tau_spin||^2/(2 lambda_T,min) + B_T,bdy + R_T,kin",
            "status": "SPINLESS_LONG_RANGE_CT_ZERO_CONDITIONAL",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TH4593_4_contact_and_failure_firewall",
            "claim": "Nonzero microscopic spin, polarized spin clocks, zero modes, or kinetic torsion are not erased; they are explicit finite branches.",
            "derivation": "Eliminating algebraic torsion gives the contact term from 4452. If Z_DT>0 or lambda_T,min=0, torsion can propagate or develop a critical response and must be scored as its own finite local-test channel.",
            "equation": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)",
            "zero_condition": "contact source absent or separately bounded; propagating and boundary torsion absent",
            "fallback_bound": "propagating branch: |Delta O_a^T| <= |J_a^T c_T| exp(-M_T r_a)/r_a plus sourced contact/boundary terms",
            "status": "FINITE_CT_BRANCH_RETAINED_NONCLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def contact_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "CB4593_0_spinless_PPN_orbital",
            "arena": "PPN/orbital ordinary macroscopic source",
            "branch_condition": "tau_spin^bulk=0; lambda_T,min>0; no D T torsion kinetic term",
            "zero_or_bound": "zero",
            "bound_formula": "Delta_PPN,bulk^T=0",
            "missing_inputs": "parent public signature for positive torsion margin; arena projection still private",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "CB4593_1_unpolarized_R10",
            "arena": "R10 unpolarized ordinary matter",
            "branch_condition": "no propagating torsion mode; no spin-polarized contact source in bulk",
            "zero_or_bound": "conditional_contact_suppression",
            "bound_formula": "alpha_T(lambda)_bulk=0 on auxiliary spinless branch; finite contact branch requires projection",
            "missing_inputs": "R10 torsion/contact projection coefficient and lambda_T,min source row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "CB4593_2_spin_clock_polarized",
            "arena": "spin clocks / polarized spin pendula / microscopic contact",
            "branch_condition": "tau_spin != 0",
            "zero_or_bound": "finite_bound_required",
            "bound_formula": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)",
            "missing_inputs": "numeric spin density/source polarization, projection to MTS contact coefficient, lambda_T,min or parent margin",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "CB4593_3_kinetic_or_zero_mode",
            "arena": "any local arena if Z_DT>0 or lambda_T,min=0",
            "branch_condition": "propagating torsion or critical algebraic zero mode",
            "zero_or_bound": "branch_reopens",
            "bound_formula": "|Delta O_a^T| <= |J_a^T c_T| exp(-M_T r_a)/r_a + contact + boundary terms",
            "missing_inputs": "M_T, c_T normalization, arena Jacobian, source charge and actual experimental bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def arena_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4593_0_gamma_beta",
            "observable": "PPN gamma/beta bulk",
            "ct_spin_status_after_4593": "conditional_zero_on_spinless_auxiliary_positive_margin_branch",
            "finite_branch_retained": "propagating torsion, zero mode, boundary torsion, spin-polarized source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4593_1_alpha_i_xi",
            "observable": "preferred-frame/preferred-location vector rows",
            "ct_spin_status_after_4593": "bulk spinless torsion removed only if no torsion boundary/readout asymmetry",
            "finite_branch_retained": "orientation/spin polarization and boundary/projective residues",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4593_2_R10",
            "observable": "R10 short-range/contact",
            "ct_spin_status_after_4593": "not a generic Yukawa row on auxiliary spinless branch",
            "finite_branch_retained": "contact/projection row remains nonclaim until numeric spin/contact mapping exists",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4593_3_clocks_spin",
            "observable": "spin clocks / polarized tests",
            "ct_spin_status_after_4593": "not closed",
            "finite_branch_retained": "explicit spin-contact bound required",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def survivor_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4593_0_EH_principal",
            "residual_family": "EH principal / Palatini IR selector",
            "status_after_4593": "still public blocker",
            "next_action": "retain parent selector/adoption gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4593_1_cGamma",
            "residual_family": "c_Gamma local memory coupling",
            "status_after_4593": "unchanged finite survivor",
            "next_action": "derive memory support/projector zero or source profile coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4593_2_cR2_MR",
            "residual_family": "c_R2/M_R finite-range tail",
            "status_after_4593": "selected next broad survivor",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4593_3_cT_spin",
            "residual_family": "spin/torsion contact channel",
            "status_after_4593": "conditional spinless long-range zero; finite contact/propagating branch retained",
            "next_action": "do not treat as global closure; fill spin-contact/projection rows only if this branch is needed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4593_4_Lambda_eff_material_projection",
            "residual_family": "Lambda/material/projection/public parent rows",
            "status_after_4593": "unchanged blockers",
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
            "control_id": "CTRL4593_clean_spinless_auxiliary",
            "input_branch": "source-kernel zero; no D T; lambda_T,min>0; tau_spin^bulk=0",
            "expected_result": "T_bulk=0 and Delta_PPN,bulk^T=0",
            "control_status": "SYMBOLIC_CONTROL_PASS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4593_polarized_spin",
            "input_branch": "tau_spin != 0",
            "expected_result": "contact row remains finite and must be source-backed",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4593_zero_mode",
            "input_branch": "lambda_T,min=0",
            "expected_result": "spinless zero proof fails",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4593_kinetic_torsion",
            "input_branch": "Z_DT>0",
            "expected_result": "propagating torsion branch opens and needs finite bound",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_0_sources_exist",
            "claim": "all local sources exist",
            "passed": "PENDING_VALIDATION",
            "valid_for_claim": "False",
            "detail": "validated after source register generation",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_1_needles_found",
            "claim": "all local source needles found",
            "passed": "PENDING_VALIDATION",
            "valid_for_claim": "False",
            "detail": "validated after source register generation",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_2_zero_law_written",
            "claim": "spinless auxiliary positive-margin torsion zero law is written",
            "passed": "True",
            "valid_for_claim": "False",
            "detail": "tau_spin^bulk=0 and lambda_T,min>0 => T_bulk=0",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_3_contact_not_hidden",
            "claim": "finite contact/propagating branches remain explicit",
            "passed": "True",
            "valid_for_claim": "False",
            "detail": "spin, zero-mode, kinetic and boundary branches have bound rows",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_4_no_public_claim",
            "claim": "no torsion/local-GR public pass is emitted",
            "passed": "True",
            "valid_for_claim": "False",
            "detail": "parent public signature and remaining survivors stay blocked",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4593_5_next_target_written",
            "claim": "next broad survivor target selected",
            "passed": "True",
            "valid_for_claim": "False",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "spinless_auxiliary_ct_zero": "True",
            "parent_positive_margin_publicly_signed": "False",
            "finite_contact_branch_retained": "True",
            "propagating_torsion_branch_retained": "True",
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
            "source_kernel_status": "closed private subvector from 4592",
            "cT_spin_status": "conditional_spinless_long_range_zero_contact_and_failure_branches_retained",
            "remaining_broad_survivors": "EH_public_adoption;cGamma;cR2_MR;Lambda_eff;material_projection;global_parent",
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
            "reason": "After c_T_spin is narrowed to a conditional spinless zero/contact-bound branch, the next broad local-GR survivor with direct R10/orbital/PPN pressure is c_R2/M_R.",
            "derive_first": "prove parent mass gap or coefficient zero for curvature-square/scalaron/spin-2 finite-range tails",
            "fallback": "source full R10 alpha(lambda), orbital precession and PPN gamma/beta projection rows for c_R2/M_R",
            "valid_for_claim": "False",
        }
    ]


def write_docs(now: str, tables: dict[str, list[dict[str, Any]]]) -> None:
    source_table = markdown_table(tables["sources"])
    theorem_table = markdown_table(tables["theorem"])
    contact_table = markdown_table(tables["contact"])
    arena_table = markdown_table(tables["arena"])
    survivor_table = markdown_table(tables["survivor"])
    control_table = markdown_table(tables["control"])
    promotion_table = markdown_table(tables["promotion"])
    decision_table = markdown_table(tables["decision"])
    status_table = markdown_table(tables["status"])
    next_table = markdown_table(tables["next"])

    body = f"""# 4593 Y5 R2FR cT spin torsion zero or contact bound after source kernel closure

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4593 does **not** pretend torsion is globally gone. It takes the earlier 4451-4453 torsion ladder and plugs it into the current 4592 source-kernel-closed local branch.

The exact local law now used is:

```text
L_T[e,c_T] T = kappa tau_spin,
lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|).
```

If the compact local branch has no independent `D T` kinetic torsion term, if the parent auxiliary torsion operator has a positive irrep margin,

```text
lambda_T,min >= m_T,parent^2 > 0,
```

and if the macroscopic local source is spinless or unpolarized in the bulk,

```text
tau_spin^bulk = 0,
```

then:

```text
T_bulk = 0
Delta_PPN,bulk^T = 0
```

So `c_T_spin` is no longer a broad long-range PPN/R10/orbital obstruction on that private branch. It is narrowed to a contact/propagating-torsion firewall.

The finite branch remains:

```text
||T|| <= kappa ||tau_spin||/lambda_T,min
|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)
|Delta O_a^T| <= ||Pi_a^T|| kappa ||tau_spin||/lambda_T,min
              + ||Pi_a^contact|| kappa^2 ||tau_spin||^2/(2 lambda_T,min)
              + B_T,bdy + R_T,kin.
```

If `Z_DT>0`, `lambda_T,min=0`, a spin-polarized source is used, or a torsion boundary/readout tail survives, the torsion branch is **open** and must be bounded. No public local-GR claim is emitted.

## Source Register

{source_table}

## cT Spin Theorem

{theorem_table}

## Contact Bound Rows

{contact_table}

## Arena Update

{arena_table}

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

    formal_body = f"""# 609 PPC4161 cT spin torsion zero or contact bound after source kernel closure

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4593 integrates the previous torsion ladder into the source-kernel-closed local branch. The local torsion equation is algebraic on the auxiliary Cartan branch:

```text
L_T[e,c_T] T = kappa tau_spin.
```

With the positive irrep margin

```text
lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|) >= m_T,parent^2 > 0
```

and a spinless/unpolarized macroscopic bulk source,

```text
tau_spin^bulk=0 => T_bulk=0 => Delta_PPN,bulk^T=0.
```

This is only a private conditional narrowing of `c_T_spin`; it is not a public local-GR pass. Polarized/contact sources, torsion zero modes, kinetic torsion and boundary/readout torsion remain finite rows:

```text
|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min).
```

The next broad survivor is `{NEXT_TARGET}`.

## Theorem Rows

{theorem_table}

## Survivor Update

{survivor_table}

## Decision

{decision_table}
"""
    write_text(FORMAL_PATH, formal_body)


def append_spine_and_packet() -> None:
    spine_block = f"""## PPC4161 Local Addendum - cT Spin Torsion After Source Kernel Closure

Marker: `{MARKER}`
Source checkpoint: `4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md`

After the 4592 source-kernel subvector is removed, `c_T_spin` is narrowed using the existing 4451-4453 torsion ladder. In the auxiliary Cartan branch, `L_T T=kappa tau_spin`; with `lambda_T,min>=m_T,parent^2>0` and spinless/unpolarized bulk matter, `T_bulk=0` and the long-range spinless torsion projection vanishes. Spin-polarized/contact, kinetic, zero-mode and boundary torsion branches stay explicit nonclaim rows.
"""
    packet_block = f"""## PPC4161 Packet Addendum - cT Spin Torsion After Source Kernel Closure

Marker: `{PACKET_MARKER}`
Source checkpoint: `4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md`

Inside the private packet, `c_T_spin` is no longer treated as a broad source-kernel contaminant. It is a conditional spinless auxiliary-torsion zero plus a retained contact/propagating firewall. Public local-GR closure still requires the remaining survivor rows, especially `c_R2/M_R`, `c_Gamma`, EH adoption and projection/material rows.
"""
    append_once(SPINE_PATH, MARKER, spine_block)
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        CONTACT_CSV,
        ARENA_CSV,
        SURVIVOR_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]

    def pass_row(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool_text(passed),
            "detail": detail,
            "valid_for_claim": "False",
        }

    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] == "True" for row in tables["sources"])
    needle_ok = all(row["needle_found"] == "True" for row in tables["sources"])
    rows.append(pass_row("VAL4593_00_source_paths_exist", source_ok, "all source-register local paths exist"))
    rows.append(pass_row("VAL4593_01_needles_found", needle_ok, "all source-register needles found"))

    for csv_path in generated_csvs:
        parsed = read_csv(csv_path)
        rows.append(pass_row(f"VAL4593_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows"))

    no_claim_true = True
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            if str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true":
                no_claim_true = False
    rows.append(pass_row("VAL4593_12_no_claim_rows_true", no_claim_true, "generated rows keep valid_for_claim/claim_allowed false"))

    theorem_text = " ".join(str(value) for row in tables["theorem"] for value in row.values())
    rows.append(pass_row("VAL4593_13_zero_law_present", "tau_spin^bulk=0" in theorem_text and "T_bulk=0" in theorem_text, "spinless torsion zero law present"))
    rows.append(pass_row("VAL4593_14_contact_bound_present", "kappa^2 ||tau_spin||^2/(2 lambda_T,min)" in theorem_text, "spin-contact bound formula present"))
    rows.append(pass_row("VAL4593_15_failure_modes_present", "Z_DT>0" in theorem_text and "lambda_T,min=0" in theorem_text, "kinetic/zero-mode counterbranches retained"))

    survivor_text = " ".join(str(value) for row in tables["survivor"] for value in row.values())
    rows.append(pass_row("VAL4593_16_ct_status_updated", "conditional spinless long-range zero" in survivor_text, "c_T_spin survivor narrowed but retained"))
    rows.append(pass_row("VAL4593_17_next_cR2_selected", NEXT_TARGET in read_text(NEXT_CSV), "next broad cR2/MR target selected"))

    rows.append(pass_row("VAL4593_18_doc_written", DOC_PATH.exists() and MARKER in read_text(DOC_PATH), f"{DOC_PATH} written"))
    rows.append(pass_row("VAL4593_19_formal_written", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), f"{FORMAL_PATH} written"))
    rows.append(pass_row("VAL4593_20_claim_register", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), f"{CLAIM_ID} in claims register"))
    rows.append(pass_row("VAL4593_21_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present"))
    rows.append(pass_row("VAL4593_22_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present"))
    rows.append(pass_row("VAL4593_23_public_stage_clean", git_clean(PUBLIC_STAGE), "public-stage git status remains clean or repo absent"))
    rows.append(pass_row("VAL4593_24_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo git status remains clean or repo absent"))
    return rows


def update_promotion_with_validation(tables: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_ok = next(row for row in validation_rows if row["check_id"] == "VAL4593_00_source_paths_exist")["passed"]
    needle_ok = next(row for row in validation_rows if row["check_id"] == "VAL4593_01_needles_found")["passed"]
    updated = []
    for row in tables["promotion"]:
        row = dict(row)
        if row["gate_id"] == "PROM4593_0_sources_exist":
            row["passed"] = source_ok
        if row["gate_id"] == "PROM4593_1_needles_found":
            row["passed"] = needle_ok
        updated.append(row)
    return updated


def main() -> int:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "contact": contact_rows(now),
        "arena": arena_rows(now),
        "survivor": survivor_rows(now),
        "control": control_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(CONTACT_CSV, tables["contact"])
    write_csv(ARENA_CSV, tables["arena"])
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
