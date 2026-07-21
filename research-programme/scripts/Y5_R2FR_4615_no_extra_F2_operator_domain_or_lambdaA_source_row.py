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

CHECKPOINT = "4615"
CLAIM_ID = "L-457"
BRANCH_ID = "MTS_R2FR_Y5_NO_EXTRA_F2_OPERATOR_DOMAIN_4615"
MARKER = "PPC4161_NO_EXTRA_F2_OPERATOR_DOMAIN_OR_LAMBDAA_SOURCE_ROW_4615"
PACKET_MARKER = "PPC4161_PACKET_NO_EXTRA_F2_OPERATOR_DOMAIN_4615"
DECISION = "NO_EXTRA_F2_OPERATOR_DOMAIN_EXACT_CONDITIONAL_THEOREM_AND_LAMBDAA_ROW_READY_NONCLAIM"
NEXT_TARGET = "4616-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"

DOC_PATH = POST / "4615-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
FORMAL_PATH = FORMAL / "631-PPC4161-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4615_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_NO_EXTRA_F2_THEOREM.csv"
DOMAIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_OPERATOR_DOMAIN_CLAUSE_ROWS.csv"
COUNTERTERM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_F2_COUNTERTERM_CLASSIFICATION_ROWS.csv"
LAMBDA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_LAMBDAA_SOURCE_ROW_NONCLAIM.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_LAMBDAF2_BOUND_UPDATE_ROWS.csv"
ALPHA_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_BALPHA_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4615_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4615_VALIDATION.csv"

CSV_4614_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4614_NEXT_TARGET.csv"
CSV_4614_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4614_EM_GAUGE_KINETIC_THEOREM.csv"
CSV_4614_BSOURCE = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_SOURCE_ROW_NONCLAIM.csv"
CSV_3994_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3994_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM.csv"
CSV_3994_GATE = SOURCE_DIR / "P8_Y5_R2FR_3994_OPERATOR_DOMAIN_GATE.csv"
CSV_3864_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv"
CSV_3864_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv"
CSV_3864_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv"
CSV_3528_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv"
CSV_1057_COUNTER = SOURCE_DIR / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
CSV_1099_AUDIT = SOURCE_DIR / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
CSV_1397_SOURCE = SOURCE_DIR / "P8_Y5_R10_1397_LAMBDA_A_SOURCE_ROW.csv"
CSV_1398_PRIOR = SOURCE_DIR / "P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv"
CSV_3507_ALPHA = SOURCE_DIR / "P8_EM_scalar_coupling_owner_alpha_residual.csv"
CSV_3505_VISIBLE = SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"

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


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


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


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk",
        "sector", "evidence", "next_action", "risk",
    ]
    rows.append({
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4615 consolidates the exact conditional no-extra-F2 operator-domain theorem and keeps lambda_A/C_XF2 as explicit nonclaim source rows when the visible operator-domain image is not parent-signed.",
        "current_evidence": "Generated no-extra-F2 theorem rows, operator-domain clauses, F2 counterterm classifications, lambda_A source rows, bound updates, b_alpha updates and validation.",
        "status": "no_extra_F2_operator_domain_conditional_theorem_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using ordinary diffeomorphism/gauge symmetry, unit conventions, or calibrated alpha to ban a legal hidden/readout/radiative F_Q^2 coefficient.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until the parent operator-domain image/no-Hom/readout/current clauses are signed or lambda_A/C_XF2 is source-backed.",
    })
    existing = list(rows[0].keys()) if rows else fieldnames
    for name in fieldnames:
        if name not in existing:
            existing.append(name)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=existing)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in existing})


def source_rows(now: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4615_00_4614_handoff", CSV_4614_NEXT, "4615-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md", "4614 selected no-extra-F2 gate."),
        ("SRC4615_01_4614_next", CSV_4614_THEOREM, "EGK4614_4_next_source_throat", "4614 names lambda_A/f_X F2 throat."),
        ("SRC4615_02_4614_lambda", CSV_4614_BSOURCE, "BSR4614_1_lambdaA_source_row", "4614 lambdaA source row."),
        ("SRC4615_03_3994_symmetry", CSV_3994_THEOREM, "F2G3994_0_ord_symmetry_countermodel", "ordinary symmetry countermodel."),
        ("SRC4615_04_3994_zero", CSV_3994_THEOREM, "F2G3994_1_no_extra_F2_zero", "3994 no-extra-F2 theorem."),
        ("SRC4615_05_3994_identity", CSV_3994_THEOREM, "F2G3994_2_canonical_identity", "3994 finite identity."),
        ("SRC4615_06_3994_poynting", CSV_3994_THEOREM, "F2G3994_4_Poynting_flux_bound", "3994 Poynting law."),
        ("SRC4615_07_3994_parent", CSV_3994_GATE, "ODG3994_0_parent_image", "3994 parent image gate."),
        ("SRC4615_08_3994_hom", CSV_3994_GATE, "ODG3994_1_hidden_hom", "3994 hidden Hom gate."),
        ("SRC4615_09_3994_current", CSV_3994_GATE, "ODG3994_2_current_owner", "3994 current owner gate."),
        ("SRC4615_10_3994_rad", CSV_3994_GATE, "ODG3994_3_radiative_readout", "3994 radiative/readout gate."),
        ("SRC4615_11_3864_zero", CSV_3864_THEOREM, "NEF3864_1_no_extra_F2_theorem", "3864 exact no-extra-F2 theorem."),
        ("SRC4615_12_3864_verdict", CSV_3864_THEOREM, "NEF3864_4_current_verdict", "3864 current corpus verdict."),
        ("SRC4615_13_3864_handoff", CSV_3864_THEOREM, "NEF3864_5_handoff", "3864 handoff."),
        ("SRC4615_14_3864_parent", CSV_3864_AUDIT, "ODA3864_0_parent_image", "3864 parent image audit."),
        ("SRC4615_15_3864_hidden", CSV_3864_AUDIT, "ODA3864_2_hidden_scalar", "3864 hidden scalar audit."),
        ("SRC4615_16_3864_current", CSV_3864_AUDIT, "ODA3864_4_current_leg", "3864 current leg audit."),
        ("SRC4615_17_3864_bound", CSV_3864_BOUND, "LFB3864_2_active_lambdaF2", "3864 active lambdaF2 bound."),
        ("SRC4615_18_3528_parent", CSV_3528_DOMAIN, "OP3528_0_parent_F2", "3528 parent F2 operator class."),
        ("SRC4615_19_3528_hidden", CSV_3528_DOMAIN, "OP3528_2_hidden_scalar_lambda", "3528 hidden scalar class."),
        ("SRC4615_20_1057_constant", CSV_1057_COUNTER, "CT1057_0_constant_lambda", "1057 constant counterterm."),
        ("SRC4615_21_1057_hidden", CSV_1057_COUNTER, "CT1057_1_hidden_scalar", "1057 hidden scalar counterterm."),
        ("SRC4615_22_1057_rad", CSV_1057_COUNTER, "CT1057_2_radiative", "1057 radiative counterterm."),
        ("SRC4615_23_1099_gauge", CSV_1099_AUDIT, "EXC1099_1_U1_gauge", "1099 U1 gauge insufficiency."),
        ("SRC4615_24_1099_units", CSV_1099_AUDIT, "EXC1099_2_fixed_units", "1099 unit proof rejection."),
        ("SRC4615_25_1397_lambda", CSV_1397_SOURCE, "LAM1397_0_lambda_A", "1397 lambda source row."),
        ("SRC4615_26_1397_derivative", CSV_1397_SOURCE, "LAM1397_2_alphaEM_drift", "1397 alpha derivative row."),
        ("SRC4615_27_1398_lambda", CSV_1398_PRIOR, "LAP1398_0_lambda_A", "1398 lambda prior vector."),
        ("SRC4615_28_3507_CXF2", CSV_3507_ALPHA, "ARE3507_1_C_XF2", "3507 C_XF2 throat."),
        ("SRC4615_29_3505_CXF2", CSV_3505_VISIBLE, "VEB3505_6_C_XF2", "3505 visible C_XF2 row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line_of(path, needle) > 0,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "generated_utc": now,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NEF4615_0_symmetry_countermodel",
            "claim": "Diffeomorphism covariance and U(1) gauge invariance do not forbid an independent F_Q^2 coefficient.",
            "formula": "DeltaS_F2=-1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2",
            "derivation": "F_Q^2 is itself a visible gauge-invariant scalar density; a scalar coefficient is allowed by ordinary field-theory symmetry.",
            "status": "COUNTERMODEL_RETAINED_NO_SHORTCUT",
            "source_anchor": "F2G3994_0_ord_symmetry_countermodel;NEF3864_0_symmetry_legality;EXC1099_1_U1_gauge",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NEF4615_1_conditional_zero",
            "claim": "No-extra-F2 is exact if the visible operator domain is only the parent-generated image and that image contains no independent Coeff(F_Q^2).",
            "formula": "Allowed[S_vis]=Image(ParentGenerate) and Image(F_Q^2)=C_P N_Q F_Q^2 only => D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0",
            "derivation": "Typed image theorem: with no coefficient object in the visible operator algebra, hidden/readout variables have no target Hom into F_Q^2 normalization.",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "source_anchor": "F2G3994_1_no_extra_F2_zero;NEF3864_1_no_extra_F2_theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NEF4615_2_constant_calibration",
            "claim": "A universal hidden-independent constant lambda_0 F_Q^2 is calibration debt, not local vertical drift.",
            "formula": "D_v lambda_0=0 but alpha_EM value remains externally calibrated",
            "derivation": "A constant coefficient changes the absolute alpha value but not the local derivative or WEP/clock/R10 drift by itself.",
            "status": "CALIBRATION_NOT_LOCAL_RESIDUAL_NO_ALPHA_VALUE_CLAIM",
            "source_anchor": "F2G3994_3_constant_calibration_split;NEF3864_2_constant_lambda_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NEF4615_3_finite_identity",
            "claim": "If a finite F2 coefficient survives, it must be bounded jointly with current normalization.",
            "formula": "s_XF2:=D_X ln lambda_A, z_g:=D_X ln g_J, b_alpha_X=2 z_g-s_XF2",
            "derivation": "Canonical EM normalization gives alpha_eff proportional to g_J^2/lambda_A.",
            "status": "FINITE_BRANCH_DERIVED_JOINT_BOUND_REQUIRED",
            "source_anchor": "F2G3994_2_canonical_identity;NEF3864_3_canonical_finite_identity;LFB3864_0_canonical_identity",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NEF4615_4_current_verdict",
            "claim": "Current corpus does not parent-sign the visible operator-domain image/no-Hom/radiative/current package.",
            "formula": "parent_image and no_hidden_Hom and readout_closure and z_g=0 are all required",
            "derivation": "3864 and 3994 prove the conditional theorem but their own audits mark the parent-image, hidden Hom, radiative/readout and same-current clauses unsigned.",
            "status": "NO_EXTRA_F2_NOT_CLAIMED_CURRENT_CORPUS",
            "source_anchor": "NEF3864_4_current_verdict;ODG3994_0_parent_image;ODG3994_1_hidden_hom;ODG3994_2_current_owner;ODG3994_3_radiative_readout",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def domain_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("OD4615_0_parent_image", "visible operator-domain image", "Allowed[S_vis]=Image(ParentGenerate) with no free Coeff(F_Q^2)", "UNSIGNED_PARENT_IMAGE_THEOREM", "ODA3864_0_parent_image;ODG3994_0_parent_image"),
        ("OD4615_1_hidden_Hom", "hidden/readout Hom into Coeff(F_Q^2)", "no hidden, motion, time, material or readout map can feed lambda_F2", "CONDITIONAL_NO_HOM_UNSIGNED", "ODA3864_2_hidden_scalar;ODG3994_1_hidden_hom"),
        ("OD4615_2_same_current", "same current normalization", "J_Q and A_Q current extracted before readout from one parent current owner", "z_g_LIVE", "ODA3864_4_current_leg;ODG3994_2_current_owner"),
        ("OD4615_3_radiative_readout", "radiative/readout regenerated F2", "effective action and readout maps remain q-basic/image-stable", "UNSIGNED_RADIOUT_CLOSURE", "ODA3864_3_radiative_readout;ODG3994_3_radiative_readout"),
        ("OD4615_4_Poynting_flux", "boundary Poynting flux", "closed stationary source worldtube or finite flux bound", "CONTROLLED_BRANCH_ZERO_AVAILABLE_GENERAL_BOUND_MISSING", "ODG3994_4_Poynting_flux;F2G3994_4_Poynting_flux_bound"),
        ("OD4615_5_source_scale", "EM source-scale propagation", "lambda_F2/current residuals do not alter EM binding/source mass/Poynting scale", "SOURCE_SCALE_BOUND_SYMBOLIC", "ODA3864_5_source_scale;LFB3864_4_source_scale_update"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "slot": slot,
            "required_for_zero": required,
            "current_status": status,
            "source_anchor": anchor,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for gate_id, slot, required, status, anchor in rows
    ]


def counterterm_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("F2C4615_0_parent_F2", "parent-generated Maxwell kinetic term", "C_P <F_Q T_Q,F_Q T_Q>_P", "KEEP_AS_DERIVATION_ROUTE", "OP3528_0_parent_F2"),
        ("F2C4615_1_constant_lambda", "constant independent visible F2 counterterm", "lambda_A F_Q^2", "CALIBRATION_DEBT_NOT_LOCAL_DRIFT", "OP3528_1_constant_lambda;CT1057_0_constant_lambda"),
        ("F2C4615_2_hidden_scalar", "hidden scalar gauge-kinetic coefficient", "f(I_hid) F_Q^2", "BOUND_BRANCH_REQUIRED_IF_PRESENT", "OP3528_2_hidden_scalar_lambda;CT1057_1_hidden_scalar"),
        ("F2C4615_3_radiative_lambda", "loop/threshold/readout regenerated F2", "delta_lambda_A(mu,X) F_Q^2", "BOUND_BRANCH_REQUIRED_IF_PRESENT", "OP3528_3_radiative_lambda;CT1057_2_radiative"),
        ("F2C4615_4_readout_lambda", "apparatus/readout coefficient", "lambda_readout(R_obs)F_Q^2", "READOUT_CLOSURE_REQUIRED", "EXC1099_5_radiative;ODG3994_3_radiative_readout"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "operator_class": operator_class,
            "example": example,
            "verdict": verdict,
            "source_anchor": anchor,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, operator_class, example, verdict, anchor in rows
    ]


def lambda_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("LAR4615_0_lambda_A", "lambda_A", "standalone observed Maxwell kinetic counterterm", "DeltaS_lambda=-(lambda_A/4) int dmu_obs F_Q^2", "MISSING_PARENT_ACTION_COEFFICIENT", "same convention as g_EM^-2"),
        ("LAR4615_1_s_XF2", "s_XF2", "active vertical derivative of lambda_A", "D_X ln lambda_A", "MISSING_DERIVATIVE_MAP", "dimensionless derivative"),
        ("LAR4615_2_C_XF2", "C_XF2", "hidden/motion/time scalar multiplier of F^2 or F*F", "f_X(Phi)F_Q^2 or g_X(Phi)F_Q*F_Q", "MISSING_NO_HOM_PROOF_OR_VALUE", "model_dependent"),
        ("LAR4615_3_delta_lambda_rad", "delta_lambda_rad", "radiative/readout regenerated F2 coefficient", "delta lambda_A(mu,X,readout)", "MISSING_RADIOUT_CLOSURE_OR_VALUE", "dimensionless"),
        ("LAR4615_4_rho_lambda", "rho_lambda_A", "counterterm size relative to inherited parent norm", "lambda_A/(C_P N_Q)", "MISSING_C_P_N_Q_AND_LAMBDA_A", "dimensionless"),
        ("LAR4615_5_binding_feed", "beta_EM(lambda_A)", "EM binding/material response induced by finite lambda_A", "beta_bind,A includes f_EM,A beta_EM(lambda_A)", "MISSING_BINDING_MAP", "dimensionless"),
        ("LAR4615_6_R10_leg", "R10_alpha_bulk_lambda_A_leg", "short-range material leg from finite lambda_A", "alpha_bulk,ST(lambda) includes K_bulk_ST beta_bulk,S beta_bulk,T + tail", "MISSING_R10_KERNEL_AND_BOUND_INPUTS", "dimensionless Yukawa alpha"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "formula": formula,
            "current_value": current_value,
            "units": units,
            "status": "source_row_nonclaim",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, quantity, definition, formula, current_value, units in rows
    ]


def bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("LBU4615_0_canonical_identity", "s_XF2", "|s_XF2| <= 2|z_g| + |b_alpha_X|", "from b_alpha_X=2z_g-s_XF2; no cancellation credit", "MISSING_ALPHA_AND_ZG_SOURCE_ROWS"),
        ("LBU4615_1_zg_zero_branch", "s_XF2 if z_g=0", "|s_XF2|=|b_alpha_X|", "same-current owner special branch", "MISSING_ZG_ZERO_THEOREM_AND_ALPHA_BOUND"),
        ("LBU4615_2_active_lambdaF2", "B_lambdaF2_4615", "B_lambdaF2 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|", "active local F2 residual excludes pure constant calibration", "SYMBOLIC_ONLY"),
        ("LBU4615_3_F2perp", "C_F2_perp", "C_F2_perp <= (C_Q_leak+C_lambda_leak+C_hidden_leak+C_readout_leak)/Z_min", "finite F2-perpendicular source bound form", "MISSING_Z_MIN_AND_LEAK_NUMERATORS"),
        ("LBU4615_4_source_scale", "B_EM_scale", "B_EM_scale <= B_EM_scale_without_F2 + B_lambdaF2", "substitutes explicit no-extra-F2 residual into source-scale gate", "SYMBOLIC_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "target": target,
            "formula": formula,
            "derivation": derivation,
            "numeric_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, target, formula, derivation, status in rows
    ]


def balpha_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BAU4615_0_lambda_insert",
            "quantity": "b_alpha_EM",
            "update_formula": "b_alpha_EM = 2 z_g - s_XF2 - z_readout - z_rad",
            "zero_condition": "s_XF2=C_XF2=delta_lambda_rad=delta_lambda_readout=z_g=0 in the same parent branch",
            "current_status": "BALPHA_THROAT_REFINED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BAU4615_1_QbarXT",
            "quantity": "qbar_theta_marker_abs",
            "update_formula": "qbar_theta_marker contains |b_alpha_EM| with |s_XF2| and lambda_A/C_XF2 rows explicit",
            "zero_condition": "4615 no-extra-F2 plus 4614 current/readout zero package",
            "current_status": "QBARXT_EM_COEFFICIENT_BRANCH_EXPLICIT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BAU4615_2_Maxwell",
            "quantity": "Maxwell/EM stress residual",
            "update_formula": "finite lambda_A/C_XF2 propagates into EM stress/source-scale rows, not just clock alpha",
            "zero_condition": "operator-domain exhaustion plus observed Hodge/current/readout closure",
            "current_status": "MAXWELL_LIMIT_STILL_CONDITIONAL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4615_0_no_public_push", "rule": "work stays local/private; no GitHub push, no public repo mutation", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4615_1_no_symmetry_shortcut", "rule": "ordinary diffeomorphism or U(1) gauge invariance cannot ban scalar F_Q^2 coefficients", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4615_2_no_unit_alpha", "rule": "constant calibration is not an alpha prediction and dimensionless alpha variation cannot be unit-hidden", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4615_3_no_alpha_only_bound", "rule": "s_XF2 must be bounded jointly with z_g via b_alpha_X=2z_g-s_XF2", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4615_4_no_constant_drift_pressure", "rule": "universal hidden-independent lambda_0 is calibration debt, not local drift by itself", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4615_0_parent_image", "blocks": "no-extra-F2 proof", "missing": "Allowed[S_vis]=Image(ParentGenerate) with no free Coeff(F_Q^2)", "resolution": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4615_1_hidden_Hom", "blocks": "C_XF2 zero", "missing": "no hidden/readout Hom into Coeff(F_Q^2)", "resolution": "derive no-Hom clause or retain C_XF2", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4615_2_current_leg", "blocks": "isolating s_XF2 from alpha", "missing": "same-current owner z_g=0 or joint z_g/s_XF2 bound", "resolution": "derive current owner or keep joint bound", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4615_3_radiative_readout", "blocks": "tree-level F2 closure", "missing": "effective/readout action remains in the same parent image", "resolution": "derive readout closure or retain delta_lambda_rad/readout", "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4615_0_source_traceability", "requirement": "every cited no-extra-F2 source path exists and every cited row needle is found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4615_1_no_extra_F2_zero", "requirement": "parent image, no-Hom, same-current, readout/radiative closure and Poynting/source scale all close", "current_status": "BLOCKED_PARENT_UNSIGNED", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4615_2_lambda_source", "requirement": "lambda_A/s_XF2/C_XF2/delta_lambda rows have values, units, derivative map and source paths", "current_status": "BLOCKED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4615_3_arena_scoring", "requirement": "b_alpha/z_g/s_XF2 products are projected to clock, WEP, R10, Maxwell and source-scale arenas", "current_status": "BLOCKED_ARENA_INPUTS_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "meaning": "The no-extra-F2 route is an exact conditional theorem, but current MTS keeps lambda_A/C_XF2 finite unless the operator-domain image is parent-signed.",
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "The legal F2 counterterm is no longer a vague EM problem: it is split into parent image, hidden Hom, same-current, radiative/readout and source-scale gates with explicit lambda rows.",
        "what_did_not_move": "No no-extra-F2, alpha, Maxwell, WEP, clock, R10, Newton or local-GR claim; the parent-image theorem remains unsigned.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "The strongest remaining clause is the parent visible operator-domain image; if it closes, hidden Hom and lambda_A have nowhere to live.",
        "derive_first": "prove Allowed[S_vis]=Image(ParentGenerate) for the visible EM coefficient algebra, with no free Coeff(F_Q^2)",
        "fallback": "retain hidden-Hom/C_XF2 and lambda_A source rows with finite bounds",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4615 - No-Extra-`F^2` Operator Domain Or `lambda_A` Source Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

The ordinary shortcut is dead:

```text
DeltaS_F2 = -1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2
```

is diffeomorphism covariant and U(1) gauge invariant. So no-extra-`F^2` needs the stronger typed-image theorem:

```text
Allowed[S_vis]=Image(ParentGenerate)
and Image(F_Q^2)=C_P N_Q F_Q^2 only
=> D_v lambda_F2 = D_v f_X = D_v delta_lambda_rad = 0.
```

If that package is not parent-signed, keep the finite branch:

```text
s_XF2 := D_X ln lambda_A,
z_g := D_X ln g_J,
b_alpha_X = 2 z_g - s_XF2.
```

This is a real narrowing: the next proof target is the visible operator-domain image, not another broad local-GR checklist.

## Source Register

{markdown_table(tables["sources"])}

## No-Extra-`F^2` Theorem

{markdown_table(tables["theorem"])}

## Operator-Domain Clause Rows

{markdown_table(tables["domain"])}

## `F^2` Counterterm Classification

{markdown_table(tables["counterterms"])}

## `lambda_A/C_XF2` Source Rows

{markdown_table(tables["lambda"])}

## `lambdaF2` Bound Updates

{markdown_table(tables["bounds"])}

## `b_alpha` Update Rows

{markdown_table(tables["balpha_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The next derivation should attack the parent visible operator-domain image directly. If that does not close, the finite hidden-Hom/`C_XF2` and `lambda_A` source rows remain live.

Private nonclaim. No GitHub action. No no-extra-`F^2`, alpha, Maxwell, WEP, clock, R10, PPN, orbital, Newton or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 631 - No-Extra-`F^2` Operator-Domain Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Countermodel Guard

Ordinary covariance and visible U(1) gauge invariance allow

```text
DeltaS_F2 = -1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2.
```

Thus the no-extra-`F^2` zero branch requires

```text
Allowed[S_vis]=Image(ParentGenerate),
Image(F_Q^2)=C_P N_Q F_Q^2 only,
no free Coeff(F_Q^2),
no Hom(hidden/readout,Coeff(F_Q^2)),
same-current owner,
and radiative/readout closure.
```

On that branch,

```text
D_v lambda_F2 = D_v f_X = D_v delta_lambda_rad = 0.
```

## Finite Branch

If the image theorem is unsigned,

```text
s_XF2 := D_X ln lambda_A,
z_g := D_X ln g_J,
b_alpha_X = 2 z_g - s_XF2.
```

Alpha, WEP, clock and R10 bounds must then treat `s_XF2` and `z_g` jointly.

Next target: `{NEXT_TARGET}`.
"""


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
    add("VAL4615_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, DOMAIN_CSV, COUNTERTERM_CSV, LAMBDA_CSV, BOUND_CSV,
        ALPHA_UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4615_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    domain_text = "\n".join(str(row) for row in tables["domain"])
    counterterm_text = "\n".join(str(row) for row in tables["counterterms"])
    lambda_text = "\n".join(str(row) for row in tables["lambda"])
    bound_text = "\n".join(str(row) for row in tables["bounds"])
    add("VAL4615_02_countermodel", "COUNTERMODEL_RETAINED_NO_SHORTCUT" in theorem_text and "lambda(Phi,readout,hidden)" in theorem_text, "ordinary-symmetry countermodel present")
    add("VAL4615_03_conditional_zero", "Allowed[S_vis]=Image(ParentGenerate)" in theorem_text and "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED" in theorem_text, "conditional no-extra-F2 theorem present")
    add("VAL4615_04_domain_clauses", "visible operator-domain image" in domain_text and "hidden/readout Hom" in domain_text, "operator-domain clauses present")
    add("VAL4615_05_counterterms", "hidden scalar gauge-kinetic coefficient" in counterterm_text and "radiative_lambda" in counterterm_text, "counterterm classes present")
    add("VAL4615_06_lambda_rows", "s_XF2" in lambda_text and "C_XF2" in lambda_text and "lambda_A" in lambda_text, "lambda/CXF2 rows present")
    add("VAL4615_07_bounds", "b_alpha_X=2z_g-s_XF2" in bound_text and "B_lambdaF2" in bound_text, "finite bound rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4615_08_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4615_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4615_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4615_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4615_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4615_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4615_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4615_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4615_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4615_OVERALL", all(row["status"] == "PASS" for row in rows), "4615 no-extra-F2 operator-domain gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "domain": domain_rows(now),
        "counterterms": counterterm_rows(now),
        "lambda": lambda_rows(now),
        "bounds": bound_rows(now),
        "balpha_update": balpha_update_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(DOMAIN_CSV, tables["domain"])
    write_csv(COUNTERTERM_CSV, tables["counterterms"])
    write_csv(LAMBDA_CSV, tables["lambda"])
    write_csv(BOUND_CSV, tables["bounds"])
    write_csv(ALPHA_UPDATE_CSV, tables["balpha_update"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - No-Extra-F2 Operator-Domain Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The EM operator-domain problem now has a typed form: ordinary covariance and U(1) gauge invariance allow `lambda(Phi,readout,hidden)F_Q^2`, so no-extra-F2 requires `Allowed[S_vis]=Image(ParentGenerate)` with no free `Coeff(F_Q^2)`, no hidden/readout Hom into that coefficient, same-current owner and radiative/readout closure. If unsigned, keep `s_XF2:=D_X ln lambda_A`, `z_g:=D_X ln g_J`, and `b_alpha_X=2z_g-s_XF2`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - No-Extra-F2 Operator-Domain Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats independent `F_Q^2` as the central EM counterterm. The next target is the parent visible operator-domain image proof; if it fails, hidden-Hom/C_XF2 and lambda_A rows remain finite nonclaim coefficients.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4615 validation failed: {failed}")
    print(f"4615 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
