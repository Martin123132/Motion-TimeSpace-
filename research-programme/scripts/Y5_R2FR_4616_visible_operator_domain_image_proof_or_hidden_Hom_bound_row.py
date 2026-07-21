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

CHECKPOINT = "4616"
CLAIM_ID = "L-458"
BRANCH_ID = "MTS_R2FR_Y5_VISIBLE_OPERATOR_DOMAIN_IMAGE_4616"
MARKER = "PPC4161_VISIBLE_OPERATOR_DOMAIN_IMAGE_OR_HIDDEN_HOM_BOUND_4616"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_OPERATOR_DOMAIN_IMAGE_4616"
DECISION = "VISIBLE_OPERATOR_DOMAIN_IMAGE_REDUCED_TO_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_NONCLAIM_HIDDEN_HOM_ROWS_STAGED"
NEXT_TARGET = "4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"

DOC_PATH = POST / "4616-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"
FORMAL_PATH = FORMAL / "632-PPC4161-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4616_SOURCE_REGISTER.csv"
IMAGE_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
OBJECT_LANGUAGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_PARENT_GENERATOR_OBJECT_LANGUAGE.csv"
HOM_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
DECISION_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_OPERATOR_DOMAIN_DECISION_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_PROMOTION_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4616_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4616_VALIDATION.csv"

CSV_4615_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4615_NEXT_TARGET.csv"
CSV_4615_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4615_OPERATOR_DOMAIN_CLAUSE_ROWS.csv"
CSV_4615_LAMBDA = SOURCE_DIR / "P8_Y5_R2FR_4615_LAMBDAA_SOURCE_ROW_NONCLAIM.csv"
CSV_3994_GATE = SOURCE_DIR / "P8_Y5_R2FR_3994_OPERATOR_DOMAIN_GATE.csv"
CSV_3865_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv"
CSV_3865_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_3865_IMAGE_PROOF_AUDIT.csv"
CSV_2766_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_3528_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv"
CSV_3118_HOM = SOURCE_DIR / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"
CSV_2659_THEOREM = SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CSV_4432_NOHOM = SOURCE_DIR / "P8_Y5_R2FR_4432_CONSTRUCTOR_NOHOM_INPUT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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
        values = [str(row.get(header, "")).replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4616_00_4615_next", CSV_4615_NEXT, "4616-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md", "4615 selected the image/Hom target."),
        ("SRC4616_01_4615_domain", CSV_4615_DOMAIN, "OD4615_0_parent_image", "4615 parent image clause."),
        ("SRC4616_02_4615_lambda", CSV_4615_LAMBDA, "C_XF2", "4615 retained hidden F2 coefficient rows."),
        ("SRC4616_03_3994_gate", CSV_3994_GATE, "ODG3994_1_hidden_hom", "3994 hidden-Hom gate."),
        ("SRC4616_04_3865_image_theorem", CSV_3865_THEOREM, "VOI3865_0_image_theorem", "3865 exact conditional visible image theorem."),
        ("SRC4616_05_3865_audit", CSV_3865_AUDIT, "IPA3865_1_quotient_fullness", "3865 image-proof audit."),
        ("SRC4616_06_2766_domain", CSV_2766_DOMAIN, "VOE2766_2_quotient_functor_exactness", "2766 visible operator-domain exhaustion attempt."),
        ("SRC4616_07_3528_operator_result", CSV_3528_DOMAIN, "OP3528_2_hidden_scalar_lambda", "3528 hidden scalar F2 countermodel."),
        ("SRC4616_08_3118_hom_gate", CSV_3118_HOM, "NHV3118_1", "3118 no-hidden-visible coefficient Hom gate."),
        ("SRC4616_09_2659_typed_theorem", CSV_2659_THEOREM, "ODT2659_1_exact_typed_theorem", "2659 typed-domain exclusion lemma."),
        ("SRC4616_10_4432_factorized_nohom", CSV_4432_NOHOM, "NHOM4432_0_exact_factorized_noHom_contract", "4432 reusable factorized no-Hom contract pattern."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def image_proof_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "VIP4616_0_exact_image_zero_theorem",
            "claim_piece": "visible coefficient image zero theorem",
            "formal_statement": "If A_F2^vis=Image(Gen_EM) and Gen_EM contains only the parent Maxwell norm C_P N_Q <F_Q,F_Q> with fixed representation data, then every vertical v in ker(Dq) satisfies D_v lambda_F2=0.",
            "derivation": "lambda_F2 is a function only of q(Phi), fixed charge-lattice normalization and fixed representation constants. For v in ker(Dq), D_v q(Phi)=0 and D_v theta_rep=0, so D_v lambda_F2=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "current_status": "PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_UNSIGNED",
            "source_refs": "VOI3865_0_image_theorem;ODT2659_1_exact_typed_theorem;OD4615_0_parent_image",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "VIP4616_1_hidden_Hom_kernel_theorem",
            "claim_piece": "hidden-Hom kernel",
            "formal_statement": "Hom_parent(C_hid,Coeff(F_Q^2)) is zero or constant if Coeff(F_Q^2) is not an independent target object and all visible coefficients factor through q(Phi) plus fixed representation data.",
            "derivation": "A nonconstant hidden coefficient needs a target coefficient object. If the visible EM coefficient object is exhausted by the parent image, the only allowed maps factor through q; vertical hidden directions are killed by Dq(v)=0.",
            "result": "EXACT_CONDITIONAL_NO_HOM",
            "current_status": "NO_HOM_NOT_PARENT_SIGNED",
            "source_refs": "NHV3118_0;ODG3994_1_hidden_hom;NHOM4432_0_exact_factorized_noHom_contract",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "VIP4616_2_scalar_functional_countermodel",
            "claim_piece": "surviving scalar functional obstruction",
            "formal_statement": "If the parent admits a hidden invariant scalar I_hid and a visible target Coeff(F_Q^2), then lambda_F2=lambda_0+epsilon I_hid is covariant and U(1)-gauge invariant.",
            "derivation": "F_Q^2 is already a visible scalar density and I_hid is a scalar. Their product is legal unless the parent object language forbids the coefficient target or the hidden argument.",
            "result": "COUNTERMODEL_RETAINED",
            "current_status": "ORDINARY_SYMMETRY_CANNOT_CLOSE_BRANCH",
            "source_refs": "OP3528_2_hidden_scalar_lambda;NHV3118_1;VOE2766_3_no_hidden_visible_hom",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "VIP4616_3_reduced_exact_bottleneck",
            "claim_piece": "single parent scalar-functional bottleneck",
            "formal_statement": "The 4616 target reduces to proving Scal_parent^vis for EM contains only q-basic parent data and fixed representation constants, with no hidden/readout/material scalar argument into Coeff(F_Q^2).",
            "derivation": "Combining 2659, 2766, 3865, 3994 and 4615 collapses no-extra-F2, hidden-Hom and alpha-drift into one typed image/exhaustion problem.",
            "result": "COUPLING_GAP_COMPRESSED_TO_ONE_SIGNATURE",
            "current_status": "DERIVATION_TARGET_READY",
            "source_refs": "VIP4616_0_exact_image_zero_theorem;VIP4616_1_hidden_Hom_kernel_theorem;VIP4616_2_scalar_functional_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "proof_id": "VIP4616_4_finite_branch_bound_identity",
            "claim_piece": "hidden-Hom finite branch",
            "formal_statement": "If the scalar-functional bottleneck remains unsigned, define H_XF2:=sup_X |D_X ln lambda_A| and propagate b_alpha_X=2 z_g-s_XF2 with |s_XF2|<=H_XF2+|delta_lambda_rad|+|delta_lambda_readout|.",
            "derivation": "The visible coefficient branch is no longer vague: every failure mode is a derivative of a hidden/readout/radiative coefficient into the Maxwell kinetic normalization.",
            "result": "NONCLAIM_BOUND_BRANCH_STAGED",
            "current_status": "NEEDS_REAL_PARENT_COEFFICIENT_OR_BOUND_INPUTS",
            "source_refs": "LAR4615_1_s_XF2;VOI3865_3_joint_identity",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def object_language_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "object_id": "OBJ4616_0_parent_Maxwell_norm",
            "sort": "parent generator",
            "object": "C_P N_Q <F_Q,F_Q>_P",
            "allowed_arguments": "q(Phi);F_parent;fixed_charge_lattice;fixed_representation_constants",
            "forbidden_arguments_if_exact": "I_hid;readout_marker;material_marker;boundary_selector;free_lambda_A",
            "status": "ALLOWED_PARENT_IMAGE_CORE",
            "zero_effect": "only q-basic/fixed coefficient survives",
            "if_unsigned": "lambda_A and C_XF2 remain live",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "object_id": "OBJ4616_1_hidden_scalar_argument",
            "sort": "hidden scalar functional",
            "object": "I_hid(Phi) or Xhat scalar",
            "allowed_arguments": "hidden/representative variables before quotient",
            "forbidden_arguments_if_exact": "Coeff(F_Q^2)",
            "status": "COUNTERMODEL_UNLESS_NO_HOM_SIGNED",
            "zero_effect": "D_v f(I_hid)=0 because no target exists",
            "if_unsigned": "f(I_hid)F_Q^2 creates b_alpha/WEP/clock/R10 pressure",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "object_id": "OBJ4616_2_constant_sector",
            "sort": "fixed representation data",
            "object": "theta_rep;charge unit;field normalization;universal lambda_0",
            "allowed_arguments": "superselection/fixed representation labels",
            "forbidden_arguments_if_exact": "local vertical variables;apparatus readout drift",
            "status": "CONSTANT_VALUE_CALIBRATION_NOT_DRIFT",
            "zero_effect": "absolute alpha may remain calibrated but D_v alpha=0",
            "if_unsigned": "constant-sector universality remains a parent-signature gap",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "object_id": "OBJ4616_3_readout_radiative_tail",
            "sort": "effective/readout action",
            "object": "delta_lambda_rad(mu,X);delta_lambda_readout(apparatus)",
            "allowed_arguments": "loops;thresholds;apparatus projections",
            "forbidden_arguments_if_exact": "non-q-basic local hidden/readout tails",
            "status": "UNSIGNED_STABILITY_CLAUSE",
            "zero_effect": "tree-level image theorem stays stable under reduction",
            "if_unsigned": "clock/spectroscopy and alpha-product residuals stay live",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "object_id": "OBJ4616_4_source_boundary_flux",
            "sort": "boundary/local projection",
            "object": "Poynting/source-scale/boundary projection into EM stress",
            "allowed_arguments": "stationary closed source worldtube if flux is zero",
            "forbidden_arguments_if_exact": "boundary-generated coefficient of F_Q^2",
            "status": "BOUNDARY_SILENCE_NOT_GLOBAL",
            "zero_effect": "Maxwell stress/source scale inherits parent image",
            "if_unsigned": "finite EM source-scale rows remain required",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def hom_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_0_C_XF2_kernel_norm",
            "symbol": "H_XF2",
            "definition": "sup_X |D_X ln lambda_A| over the active hidden/readout vertical directions",
            "arena": "master EM hidden-Hom coefficient",
            "formula": "|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|",
            "required_inputs": "parent scalar functional coefficient; lambda_A normalization; vertical generator normalization",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "dimensionless derivative per normalized vertical unit",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_1_alpha_drift_joint_bound",
            "symbol": "B_alpha_Hom",
            "definition": "hidden-Hom contribution to alpha drift after current normalization",
            "arena": "clocks/spectroscopy/fine-structure",
            "formula": "|b_alpha_X| <= 2|z_g| + H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|",
            "required_inputs": "z_g source row; H_XF2; radiative/readout closure or bounds; arena tau",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "dimensionless projected drift",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_2_R10_alpha_leg",
            "symbol": "B_R10_Hom",
            "definition": "short-range Yukawa alpha leg sourced by hidden-Hom EM binding/source coefficient",
            "arena": "R10 short-range force",
            "formula": "|alpha_R10^Hom(lambda)| <= |K_R10_EM(lambda)| (H_XF2 + B_readout + B_rad)",
            "required_inputs": "K_R10_EM(lambda); H_XF2; material EM binding fractions; real alpha_bound(lambda)",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "Yukawa alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_3_PPN_EM_stress_leg",
            "symbol": "B_PPN_EM_Hom",
            "definition": "EM stress/source-scale PPN residual from non-image F2 coefficient",
            "arena": "PPN/local GR",
            "formula": "|gamma-1|_EM <= |K_PPN_EM| (H_XF2 + B_boundary + B_rad)",
            "required_inputs": "K_PPN_EM; local source EM fraction; boundary/Poynting flux bound; H_XF2",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "dimensionless PPN residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_4_clock_readout_leg",
            "symbol": "B_clock_Hom",
            "definition": "clock/frequency residual from F2 coefficient hidden-Hom or readout tail",
            "arena": "atomic clocks and spectroscopy",
            "formula": "|delta nu/nu| <= |K_clock_alpha| (H_XF2 + B_readout + B_rad) tau_clock",
            "required_inputs": "K_clock_alpha; tau_clock; readout closure or numeric readout bound; H_XF2",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "fractional frequency shift",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "HOM4616_5_orbital_source_scale_leg",
            "symbol": "B_orb_EM_Hom",
            "definition": "orbital/source calibration residual if EM source mass or field stress sees non-image F2 coefficient",
            "arena": "orbital systems",
            "formula": "|delta a/a|_EM <= |K_orb_EM| (H_XF2 + B_boundary + B_source_readout)",
            "required_inputs": "K_orb_EM; source EM energy fraction; boundary flux or silence theorem; H_XF2",
            "source_path": str(HOM_BOUND_CSV),
            "source_status": "STAGED_NONCLAIM_NO_NUMERIC_VALUE",
            "units": "dimensionless orbital residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4616_0",
            "decision": DECISION,
            "what_changed": "4616 does not merely relist missing couplings: it proves the exact typed image/no-Hom zero branch and compresses the remaining EM coupling problem to parent scalar-functional exhaustion.",
            "claim_status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "if_exact_branch": "If parent scalar-functional exhaustion is signed, lambda_A/C_XF2 have no target object and b_alpha_F2 source closes modulo current/readout/radiative clauses.",
            "if_finite_branch": "If a hidden/readout/radiative target survives, use H_XF2 and arena K/tau rows rather than loose language.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4616_0_no_symmetry_shortcut",
            "rule": "Do not use covariance or U(1) gauge invariance to ban lambda(Phi)F_Q^2.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4616_1_no_calibration_hiding",
            "rule": "A universal constant lambda_0 may be calibration debt, but hidden/readout derivatives are physical residuals.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4616_2_no_alpha_only_bound",
            "rule": "Alpha data alone cannot isolate s_XF2 unless z_g and readout/radiative terms are zeroed or bounded in the same arena.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4616_3_private_local_only",
            "rule": "No GitHub operation is part of this checkpoint.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4616_0_parent_scalar_functional_exhaustion",
            "claim_blocked": "visible image/no-Hom zero",
            "missing_signature": "Scal_parent^vis has no hidden/readout/material scalar argument into Coeff(F_Q^2)",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4616_1_quotient_fullness",
            "claim_blocked": "Allowed[S_vis]=Image(ParentGenerate)",
            "missing_signature": "visible quotient functor is full/exact on coefficient objects",
            "next_action": "construct universal property or retain lambda_A",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4616_2_radiative_readout_stability",
            "claim_blocked": "tree-level no-extra-F2 stability",
            "missing_signature": "S_eff and readout maps remain q-basic/image-stable after loops, thresholds and apparatus projection",
            "next_action": "derive readout/radiative closure or bound delta_lambda_rad/readout",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4616_3_numeric_Hom_bounds",
            "claim_blocked": "finite fallback scoring",
            "missing_signature": "H_XF2, K_R10_EM, K_PPN_EM, K_clock_alpha, K_orb_EM and tau arena inputs",
            "next_action": "fill first source-backed Hom/K/tau product value if proof fails",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4616_0_exact_zero_branch",
            "requirement": "parent scalar-functional exhaustion + quotient fullness + fixed representation constants + no hidden/readout Hom + radiative/readout stability",
            "current_status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4616_1_finite_bound_branch",
            "requirement": "source-backed numeric H_XF2/K/tau rows and no-cancellation arena projection",
            "current_status": "BLOCKED_NUMERIC_INPUTS_MISSING",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "Exact zero branch proved conditionally; remaining EM coupling obstruction is parent scalar-functional exhaustion, with hidden-Hom finite rows staged.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "why": "4616 reduces the no-extra-F2/Hom branch to the parent scalar-functional object language.",
            "derive_path": "prove the parent EM visible scalar algebra has no target object Coeff(F_Q^2) except the parent norm and fixed constants",
            "fallback_path": "fill the first source-backed H_XF2 or K_A*H_XF2 bound row",
            "claim_allowed": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4616 - Visible Operator-Domain Image Proof Or Hidden-Hom Bound Row

Generated UTC: `{now}`

Marker: `{MARKER}`

## Result

4616 turns the EM coupling question into a sharper fork:

```text
Exact branch:
A_F2^vis = Image(Gen_EM)
Gen_EM = C_P N_Q <F_Q,F_Q>_P
Coeff(F_Q^2) has no independent target object
=> D_v lambda_F2 = 0 for v in ker(Dq).
```

The useful point is not that the branch is claimed. It is that the remaining proof is now one thing:

```text
Scal_parent^vis has no hidden/readout/material scalar functional
that can map into Coeff(F_Q^2).
```

If that fails, the branch is not hand-waved away. It becomes the finite hidden-Hom coefficient

```text
H_XF2 := sup_X |D_X ln lambda_A|
```

with the joint identity

```text
|b_alpha_X| <= 2|z_g| + H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|.
```

## Source Register

{markdown_table(tables["sources"])}

## Visible Image Proof Attempt

{markdown_table(tables["image_proof"])}

## Parent Generator Object Language

{markdown_table(tables["object_language"])}

## Hidden-Hom Bound Rows Nonclaim

{markdown_table(tables["hom_bounds"])}

## Decision Rows

{markdown_table(tables["decision"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Status

{markdown_table(tables["status"])}

## Next Target

`{NEXT_TARGET}`

Take the parent scalar-functional exhaustion route first. If it does not close, stop pretending the EM coupling is zero and fill the first real `H_XF2` or `K_A H_XF2` bound value.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 632 - Visible Operator-Domain Image Proof Or Hidden-Hom Bound Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Exact Conditional Branch

If

```text
A_F2^vis = Image(Gen_EM),
Gen_EM = C_P N_Q <F_Q,F_Q>_P,
Coeff(F_Q^2) is not an independent target object,
theta_rep is fixed,
and v in ker(Dq),
```

then

```text
D_v lambda_F2 = 0.
```

The proof is direct: every surviving coefficient factors through `q(Phi)` or fixed representation data, so vertical derivatives vanish.

## Countermodel Guard

If a hidden invariant scalar `I_hid` and a target `Coeff(F_Q^2)` survive, then

```text
lambda_F2 = lambda_0 + epsilon I_hid
```

is a legal covariant and U(1)-gauge-invariant counterterm. Therefore the exact branch requires parent scalar-functional exhaustion, not ordinary symmetry language.

## Finite Branch

If the image theorem remains unsigned, keep

```text
H_XF2 := sup_X |D_X ln lambda_A|,
|b_alpha_X| <= 2|z_g| + H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|.
```

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "sector": "local_gr_empirical_interface",
        "claim": "4616 proves the exact conditional visible-image/no-hidden-Hom zero branch for the EM F2 coefficient and reduces the remaining coupling gap to parent scalar-functional exhaustion; finite hidden-Hom bound rows are staged as nonclaim fallback.",
        "evidence": "Generated visible image proof rows, parent generator object-language rows, hidden-Hom bound rows, decision rows, controls, blockers, promotion gates, status, next target and validation.",
        "status": "visible_operator_image_conditional_theorem_nonclaim_hidden_Hom_bounds_staged",
        "next_action": NEXT_TARGET,
        "risk": "Using ordinary covariance, gauge invariance, field normalization, or calibrated alpha to forbid a legal hidden/readout scalar map into Coeff(F_Q^2).",
        "owner": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until the parent scalar-functional exhaustion/no-Hom/readout/radiative/current clauses are signed or H_XF2/K/tau rows are source-backed.",
    }
    existing = read_text(CLAIMS_PATH)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not existing.endswith("\n"):
            handle.write("\n")
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4616_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, IMAGE_PROOF_CSV, OBJECT_LANGUAGE_CSV, HOM_BOUND_CSV, DECISION_ROWS_CSV,
        CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4616_01_csv_parse", csv_ok, ";".join(details))

    proof_text = "\n".join(str(row) for row in tables["image_proof"])
    object_text = "\n".join(str(row) for row in tables["object_language"])
    bound_text = "\n".join(str(row) for row in tables["hom_bounds"])
    blocker_text = "\n".join(str(row) for row in tables["blockers"])
    add("VAL4616_02_exact_image_theorem", "D_v lambda_F2=0" in proof_text and "EXACT_CONDITIONAL_THEOREM" in proof_text, "conditional image theorem present")
    add("VAL4616_03_countermodel_guard", "lambda_0+epsilon I_hid" in proof_text and "COUNTERMODEL_RETAINED" in proof_text, "hidden scalar countermodel retained")
    add("VAL4616_04_single_bottleneck", "parent scalar-functional" in proof_text and "Scal_parent^vis" in proof_text, "single bottleneck named")
    add("VAL4616_05_object_language", "C_P N_Q <F_Q,F_Q>_P" in object_text and "I_hid" in object_text, "object language rows present")
    add("VAL4616_06_hidden_Hom_bounds", "H_XF2" in bound_text and "K_R10_EM" in bound_text and "K_PPN_EM" in bound_text, "finite Hom bound rows present")
    add("VAL4616_07_blockers", "Scal_parent^vis" in blocker_text and "H_XF2" in blocker_text, "blockers present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4616_08_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4616_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4616_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4616_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4616_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4616_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4616_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4616_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4616_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4616_OVERALL", all(row["status"] == "PASS" for row in rows), "4616 visible-image/Hom checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "image_proof": image_proof_rows(now),
        "object_language": object_language_rows(now),
        "hom_bounds": hom_bound_rows(now),
        "decision": decision_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(IMAGE_PROOF_CSV, tables["image_proof"])
    write_csv(OBJECT_LANGUAGE_CSV, tables["object_language"])
    write_csv(HOM_BOUND_CSV, tables["hom_bounds"])
    write_csv(DECISION_ROWS_CSV, tables["decision"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Visible Operator-Domain Image Or Hidden-Hom Bound

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4616 compresses the EM coupling problem to a precise parent object-language signature. If the visible EM coefficient algebra is exactly the parent image `Gen_EM=C_P N_Q <F_Q,F_Q>_P` with no independent target `Coeff(F_Q^2)`, then `D_v lambda_F2=0` for `v in ker(Dq)`. If a hidden scalar functional can still map into that coefficient target, keep `H_XF2:=sup_X |D_X ln lambda_A|` and propagate `|b_alpha_X| <= 2|z_g| + H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Visible Operator-Domain Image Or Hidden-Hom Bound

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats the EM coupling gap as a parent scalar-functional exhaustion problem. The next move is not another broad audit: either prove no hidden/readout/material scalar functional targets `Coeff(F_Q^2)`, or fill the first real `H_XF2`/`K_A H_XF2` bound row.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4616 validation failed: {failed}")
    print(f"4616 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
