from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4820"
CLAIM_ID = "L-662"
MARKER = "PPC4161_EM_F2_HARDBLOCKER_OR_FIRST_QBAR_MARKER_BOUND_ROW_4820"
DECISION = "EM_F2_TYPED_IMAGE_GATE_RETAINED_FINITE_QBAR_EM_BOUND_STAGED_NONCLAIM"
NEXT_TARGET = "4821-Y5-R2FR-parent-visible-EM-generator-signature-or-HXF2-first-source-row.md"

DOC_PATH = POST / "4820-Y5-R2FR-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md"
FORMAL_PATH = FORMAL / "836-PPC4161-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "EM_F2_hardblocker_bound_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4820_SOURCE_REGISTER.csv"
IMAGE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4820_EMF2_IMAGE_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4820_EMF2_FINITE_BOUND_CONTRACT.csv"
POYNTING_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4820_POYNTING_ONCE_LEDGER.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4820_EMF2_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4820_EMF2_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4820_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4820_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4820_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4820_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4820_VALIDATION.csv"

PATHS = {
    "resume": RESUME_PATH,
    "4819_doc": POST / "4819-Y5-R2FR-qbarXT-JX-source-zero-or-bounded-coupling-row.md",
    "4763_doc": POST / "4763-Y5-R2FR-QbarXH-source-numerator-first-fill-or-qbarXT-hard-blocker.md",
    "4763_hardblocker": SOURCE_DIR / "P8_Y5_R2FR_4763_QBARXT_EMF2_HARDBLOCKER_ROWS.csv",
    "4703_no_extra": SOURCE_DIR / "P8_Y5_R2FR_4703_NO_EXTRA_F2_THEOREM.csv",
    "4704_visible": SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv",
    "4704_hom": SOURCE_DIR / "P8_Y5_R2FR_4704_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv",
    "4704_object": SOURCE_DIR / "P8_Y5_R2FR_4704_PARENT_GENERATOR_OBJECT_LANGUAGE.csv",
    "4262_residual": SOURCE_DIR / "P8_Y5_R2FR_4262_EM_COUPLING_RESIDUAL_REDUCTION.csv",
    "4263_branch": SOURCE_DIR / "P8_Y5_R2FR_4263_EM_RESIDUAL_FINAL_BRANCH_MAP.csv",
    "poynting_vector": SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
    "hodge_current": SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
    "hodge_flow": SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
    "visible_domain": SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv",
    "poynting_status": SOURCE_DIR / "P8_Y5_EM_Poynting_Hilbert_source_accounting_status.csv",
    "unique_f2_status": SOURCE_DIR / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4820_00_resume", PATHS["resume"], "4820-Y5-R2FR-EM-F2-hardblocker", "current handoff"),
        ("SRC4820_01_4819", PATHS["4819_doc"], "EM/F2 hard blocker", "4819 selects EM/F2"),
        ("SRC4820_02_4763_doc", PATHS["4763_doc"], "qbarXT EM/F2 Hard Blocker", "4763 hardblocker doc"),
        ("SRC4820_03_4763_csv", PATHS["4763_hardblocker"], "QBXT4763_1_hidden_Hom", "hidden Hom blocker"),
        ("SRC4820_04_4703", PATHS["4703_no_extra"], "NEF4703_4_current_verdict", "no-extra-F2 theorem"),
        ("SRC4820_05_4704_visible", PATHS["4704_visible"], "VIP4704_3_reduced_exact_bottleneck", "visible image bottleneck"),
        ("SRC4820_06_4704_hom", PATHS["4704_hom"], "HOM4704_0_C_XF2_kernel_norm", "finite H_XF2 rows"),
        ("SRC4820_07_4704_object", PATHS["4704_object"], "OBJ4704_0_parent_Maxwell_norm", "object-language rows"),
        ("SRC4820_08_4262", PATHS["4262_residual"], "R_XF2", "EM coupling residual rows"),
        ("SRC4820_09_4263", PATHS["4263_branch"], "ZERO_BY_POYNTING_ONCE_ONLY", "closed collar/Poynting rows"),
        ("SRC4820_10_poynting", PATHS["poynting_vector"], "EMF3502_2_nonminimal_XF2", "Poynting and nonminimal F2"),
        ("SRC4820_11_hodge_current", PATHS["hodge_current"], "EMB3503_2_C_XF2", "Hodge/current bound vector"),
        ("SRC4820_12_hodge_flow", PATHS["hodge_flow"], "DHB3504_4_hidden_disformal_hodge", "Hodge flow rule"),
        ("SRC4820_13_visible_domain", PATHS["visible_domain"], "VEB3505_6_C_XF2", "visible action domain"),
        ("SRC4820_14_poynting_status", PATHS["poynting_status"], "EM_POYNTING_ONCE_THEOREM", "Poynting once status"),
        ("SRC4820_15_unique_f2", PATHS["unique_f2_status"], "STAT3528_0_unique_F2", "unique F2 status"),
        ("SRC4820_16_runner", PATHS["runner"], "def evaluate_row", "4820 runner"),
    ]


def build_source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def build_image_audit(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EFZ4820_0_symmetry_countermodel",
            "object": "lambda_F2 hidden scalar countermodel",
            "statement": "Diffeomorphism covariance and U(1) gauge invariance alone allow lambda_F2=lambda_0+epsilon I_hid multiplying F_Q^2.",
            "formula": "Delta S_F2=-1/4 int dmu_obs lambda_F2(Phi,readout,hidden) F_Q^2",
            "status": "COUNTERMODEL_ACTIVE",
            "source_id": "NEF4703_0;VIP4704_2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EFZ4820_1_exact_image_zero",
            "object": "parent visible EM image",
            "statement": "If the visible EM coefficient algebra is exhausted by the parent Maxwell norm and fixed representation data, vertical hidden directions have no target Hom into F_Q^2.",
            "formula": "A_F2^vis=Image(Gen_EM)=C_P N_Q <F_Q,F_Q>_P => D_v lambda_F2=0 for v in ker(Dq)",
            "status": "EXACT_CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "source_id": "NEF4703_1;VIP4704_0;VIP4704_1",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EFZ4820_2_current_bottleneck",
            "object": "single scalar-functional bottleneck",
            "statement": "The remaining proof is not vague coupling: prove the parent scalar-functional visible EM generator has only q-basic/fixed arguments and no hidden/readout/material target into Coeff(F_Q^2).",
            "formula": "Scal_parent^vis(EM) subset q-basic plus fixed representation constants",
            "status": "DERIVATION_TARGET_READY",
            "source_id": "VIP4704_3",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EFZ4820_3_finite_bound_law",
            "object": "finite hidden-Hom branch",
            "statement": "If the image theorem remains unsigned, retain H_XF2 and propagate it through alpha/current/readout and qbar_EM.",
            "formula": "|s_XF2|<=H_XF2+|delta_lambda_rad|+|delta_lambda_readout|; |b_alpha|<=2|z_g|+|s_XF2|",
            "status": "BOUND_BRANCH_READY_VALUES_MISSING",
            "source_id": "HOM4704_0;HOM4704_1",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EFZ4820_4_poynting_once_guard",
            "object": "Poynting/source accounting",
            "statement": "Poynting is not a second source if it is already varied in the same Hilbert EM stress; open boundary flux must be zero or retained as Phi_EM_rad.",
            "formula": "Phi_EM_rad=int_boundary S_Poynting.n dA dt; c_Poynt_extra=0 only in once-owned branch",
            "status": "CONDITIONAL_ONCE_THEOREM_FLUX_BOUND_RETAINED",
            "source_id": "EMF3502;4263",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def build_bound_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "EFB4820_0_lambdaF2",
            "quantity": "lambdaF2_bound_abs",
            "formula": "H_XF2_abs + delta_lambda_rad_abs + delta_lambda_readout_abs",
            "required_inputs": "H_XF2_abs; delta_lambda_rad_abs; delta_lambda_readout_abs; source_signed; units_signed; same_branch_signed",
            "claim_status": "missing_live_values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EFB4820_1_balpha",
            "quantity": "b_alpha_bound_abs",
            "formula": "2*z_g_abs + lambdaF2_bound_abs",
            "required_inputs": "z_g_abs plus EFB4820_0",
            "claim_status": "missing_live_values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EFB4820_2_qbarEM",
            "quantity": "qbar_EM_bound_abs",
            "formula": "K_qbar_EM_abs*(b_alpha_bound_abs + C_JQ_abs + C_Hodge_readout_abs + Phi_EM_rad_abs)",
            "required_inputs": "K_qbar_EM_abs; C_JQ_abs; C_Hodge_readout_abs; Phi_EM_rad_abs; source/units/branch signs",
            "claim_status": "first executable qbar_EM component row staged",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EFB4820_3_forbidden_shortcuts",
            "quantity": "anti_circularity_guard",
            "formula": "reject alpha_obs_as_zero, calibration_as_derivation, Poynting double count, bound_as_source, measured-G absorption, GR import",
            "required_inputs": "source path and notes must avoid forbidden tokens",
            "claim_status": "active_runner_guard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def build_poynting_ledger(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "POY4820_0_once_owned",
            "quantity": "c_Poynt_extra",
            "law": "If Maxwell fields are varied in the same observed Hilbert action before Pi_M/readout, Poynting flux is EM stress transport, not an extra source.",
            "formula": "c_Poynt_extra=0 in same-visible-action once-owned branch",
            "status": "EXACT_CONDITIONAL_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "POY4820_1_open_flux",
            "quantity": "Phi_EM_rad_abs",
            "law": "Open radiative/background EM flux through the collar is not zero by vocabulary; it must be zero by closed-collar theorem or retained numerically.",
            "formula": "Phi_EM_rad_abs=|int_boundary S_Poynting.n dA dt|",
            "status": "BOUND_OR_ZERO_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "POY4820_2_no_double_count",
            "quantity": "EM stress/accounting guard",
            "law": "The same Poynting contribution cannot be counted once inside T_EM and again as an independent MTS source coefficient.",
            "formula": "T_total=T_matter+T_EM+T_extra; no duplicate Phi_EM source leg",
            "status": "RUNNER_FORBIDDEN_TOKEN_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def build_runner_input(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RUN4820_0_current_image_missing",
            "route_type": "image_zero",
            "route": "live image theorem",
            "source_path": str(PATHS["4704_visible"]),
            "parent_image_signed": False,
            "no_hidden_hom_signed": False,
            "fixed_representation_signed": False,
            "same_current_signed": False,
            "readout_radiative_closure_signed": False,
            "boundary_flux_signed": False,
            "notes": "current live row must block",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_1_conditional_image_pass",
            "route_type": "image_zero",
            "route": "conditional exact image theorem",
            "source_path": str(PATHS["4704_visible"]),
            "parent_image_signed": True,
            "no_hidden_hom_signed": True,
            "fixed_representation_signed": True,
            "same_current_signed": True,
            "readout_radiative_closure_signed": True,
            "boundary_flux_signed": True,
            "notes": "theorem shape smoke only",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_2_forbidden_alpha_obs_zero",
            "route_type": "image_zero",
            "route": "forbidden alpha calibration shortcut",
            "source_path": "ALPHA_OBS_AS_ZERO_CALIBRATION_AS_DERIVATION",
            "parent_image_signed": True,
            "no_hidden_hom_signed": True,
            "fixed_representation_signed": True,
            "same_current_signed": True,
            "readout_radiative_closure_signed": True,
            "boundary_flux_signed": True,
            "notes": "must fail forbidden guard",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_3_live_finite_missing",
            "route_type": "finite_bound",
            "route": "live finite H_XF2 bound",
            "source_path": str(PATHS["4704_hom"]),
            "H_XF2_abs": "MISSING_PARENT_COEFFICIENT",
            "z_g_abs": "MISSING_CURRENT_OWNER",
            "delta_lambda_rad_abs": "MISSING_RADIOUT_CLOSURE",
            "delta_lambda_readout_abs": "MISSING_READOUT_BOUND",
            "C_JQ_abs": "MISSING_CHARGE_CURRENT_OWNER",
            "C_Hodge_readout_abs": "MISSING_HODGE_READOUT_BOUND",
            "Phi_EM_rad_abs": "MISSING_FLUX_OR_ZERO",
            "K_qbar_EM_abs": "MISSING_PROJECTION_FACTOR",
            "source_signed": False,
            "units_signed": False,
            "same_branch_signed": False,
            "notes": "live values remain missing",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_4_finite_bound_smoke_pass",
            "route_type": "finite_bound",
            "route": "finite qbar_EM law smoke",
            "source_path": str(PATHS["4704_hom"]),
            "H_XF2_abs": "0.02",
            "z_g_abs": "0.01",
            "delta_lambda_rad_abs": "0.03",
            "delta_lambda_readout_abs": "0.04",
            "C_JQ_abs": "0.01",
            "C_Hodge_readout_abs": "0.02",
            "Phi_EM_rad_abs": "0.03",
            "K_qbar_EM_abs": "0.5",
            "source_signed": True,
            "units_signed": True,
            "same_branch_signed": True,
            "notes": "numeric smoke only: qbar_EM=0.085",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_5_current_poynting_missing",
            "route_type": "poynting_once",
            "route": "live Poynting once",
            "source_path": str(PATHS["poynting_status"]),
            "same_visible_action_signed": False,
            "hilbert_stress_owned": False,
            "poynting_once_signed": False,
            "closed_collar_or_flux_bound_signed": False,
            "notes": "current live row must retain flux branch",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_6_poynting_once_smoke_pass",
            "route_type": "poynting_once",
            "route": "Poynting once theorem smoke",
            "source_path": str(PATHS["4263_branch"]),
            "same_visible_action_signed": True,
            "hilbert_stress_owned": True,
            "poynting_once_signed": True,
            "closed_collar_or_flux_bound_signed": True,
            "notes": "conditional theorem smoke only",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4820_7_forbidden_double_count",
            "route_type": "poynting_once",
            "route": "forbidden Poynting double count",
            "source_path": "POYNTING_DOUBLE_COUNT_BOUND_AS_SOURCE",
            "same_visible_action_signed": True,
            "hilbert_stress_owned": True,
            "poynting_once_signed": True,
            "closed_collar_or_flux_bound_signed": True,
            "notes": "must fail forbidden guard",
            "timestamp_utc": timestamp,
        },
    ]


def build_decision(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4820_0_result",
            "decision": DECISION,
            "meaning": "No-extra-F2 is now an executable typed-image gate; live branch remains unsigned, finite qbar_EM bound is staged.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4820_1_poynting",
            "decision": "POYNTING_ONCE_RETAINED_OPEN_FLUX_BOUND_REQUIRED",
            "meaning": "Poynting can help source accounting, but only once; open collar flux remains an explicit residual.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4820_2_next_target",
            "decision": NEXT_TARGET,
            "meaning": "Either sign the parent visible EM generator/no-Hom theorem or source the first H_XF2 numeric/bound row.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": gate_id,
            "firewall": firewall,
            "status": "ACTIVE_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, firewall in [
            ("G4820_0_no_Maxwell_claim", "Do not claim MTS derives Maxwell/QED; 29 audit still says Maxwell recovery not passed."),
            ("G4820_1_no_alpha_prediction", "Do not claim alpha_EM predicted; calibrated constant is not derivation."),
            ("G4820_2_no_F2_zero_claim", "Do not claim C_XF2=0 until parent image/no-Hom/readout/radiative/current clauses are signed."),
            ("G4820_3_no_qbar_EM_claim", "Do not claim qbar_EM=0 or bounded from smoke rows; live H_XF2 and projection values are missing."),
            ("G4820_4_no_Poynting_double_count", "Do not count EM stress as Hilbert source and independent Poynting source in the same branch."),
            ("G4820_5_no_local_GR_claim", "Do not claim local GR/Newton/PPN/R10 closure from 4820; it only sharpens the EM component."),
        ]
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The bottleneck is now either a parent visible EM generator/no-Hom signature or the first real H_XF2 finite bound row.",
            "must_not_use": "alpha_obs_as_zero; calibration_as_derivation; Poynting double count; GR import; bound-as-source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def run_runner() -> None:
    subprocess.run(["python", str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)


def append_claim_register(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "EM_F2_hardblocker_or_first_qbar_marker_bound_row",
        "current_evidence": "4820 promotes the EM/F2 blocker into an executable typed-image/no-Hom gate and finite qbar_EM bound runner; live values remain unsigned/missing.",
        "status": "em_f2_gate_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "hidden Hom into F_Q^2; alpha calibration as derivation; Poynting double count; missing H_XF2 source row",
        "sector": "local_gr_EM_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "conditional image theorem only; finite bound smoke only; no Maxwell/local-GR claim",
        "title": "EM/F2 hardblocker or first qbar marker bound row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def append_once(path: Path, block: str, marker: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def write_docs(timestamp: str) -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    image_rows = read_csv(IMAGE_AUDIT)
    bound_rows = read_csv(BOUND_CONTRACT)
    poy_rows = read_csv(POYNTING_LEDGER)
    output_rows = read_csv(RUNNER_OUTPUT)
    decision_rows = read_csv(DECISION_CSV)
    gates = read_csv(CLAIM_GATES)
    doc = f"""# 4820 - EM/F2 hardblocker or first qbar marker bound row

Marker: `{MARKER}`
Decision: `{DECISION}`
Claim row: `{CLAIM_ID}` private nonclaim
Generated: `{timestamp}`

## Result

4820 compresses the EM/source-coupling gap into a stricter executable fork:

```text
exact route:
A_F2^vis = Image(Gen_EM) = C_P N_Q <F_Q,F_Q>_P
and no hidden/readout/material Hom into Coeff(F_Q^2)
=> D_v lambda_F2 = 0, b_alpha_EM = 0, qbar_EM = 0

finite route:
|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|
|b_alpha_EM| <= 2|z_g| + |s_XF2|
|qbar_EM| <= K_qbar_EM (|b_alpha_EM| + |C_JQ| + |C_Hodge_readout| + |Phi_EM_rad|)
```

The exact route remains conditional because the parent visible EM generator/no-Hom clauses are not signed. The finite route is now executable but live `H_XF2`, current, readout, radiative, charge-current and projection values are missing.

## Source register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"])}

## EM/F2 image-zero audit

{md_table(image_rows, ["row_id", "object", "statement", "formula", "status"])}

## Finite bound contract

{md_table(bound_rows, ["contract_id", "quantity", "formula", "required_inputs", "claim_status"])}

## Poynting once ledger

{md_table(poy_rows, ["row_id", "quantity", "law", "formula", "status"])}

## Runner output

{md_table(output_rows, ["row_id", "route_type", "runner_status", "lambdaF2_bound_abs", "b_alpha_bound_abs", "qbar_EM_bound_abs", "poynting_extra_abs", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "firewall", "status", "claim_allowed"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "meaning"])}

## What changed

- `C_XF2` is no longer a fog-word. It is either killed by a typed parent image/no-Hom theorem or retained as `H_XF2`.
- Poynting is promoted as useful source accounting, but the runner forbids double counting it.
- `alpha_EM` remains calibrated in the local branch unless the parent image theorem is signed; calibration is not counted as derivation.
- No local-GR, Newton, PPN, R10, clock, orbital, Maxwell/QED, alpha, or `qbar_EM=0` claim is made.

## Next target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    packet = f"""## {MARKER}

- Doc: `{DOC_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
- Summary: EM/F2 hardblocker is now an executable typed-image/no-Hom gate plus finite `H_XF2 -> b_alpha -> qbar_EM` bound branch; live branch remains nonclaim.
"""
    append_once(PACKET_PATH, packet, MARKER)
    spine = f"""## {MARKER}

4820 sharpens the Maxwell/EM stress bridge without claiming it:

```text
exact: parent visible EM image + no hidden Hom => D_v lambda_F2=0 => qbar_EM=0
finite: |qbar_EM| <= K_qbar_EM (2|z_g|+H_XF2+|delta_lambda_rad|+|delta_lambda_readout|+|C_JQ|+|C_Hodge_readout|+|Phi_EM_rad|)
```

The route is competitive because it treats Poynting as Hilbert EM stress/flux exactly once, but it remains private nonclaim until the parent generator or `H_XF2` source row is real.
"""
    append_once(SPINE_PATH, spine, MARKER)
    resume = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4820-Y5-R2FR-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md`
Marker: `{MARKER}`

## Where we are

4820 converted the EM/F2 hardblocker into an executable fork:

```text
exact route:
A_F2^vis=Image(Gen_EM)=C_P N_Q <F_Q,F_Q>_P and no hidden Hom into Coeff(F_Q^2)
=> D_v lambda_F2=0, b_alpha_EM=0, qbar_EM=0

finite route:
|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|
|b_alpha_EM| <= 2|z_g| + |s_XF2|
|qbar_EM| <= K_qbar_EM (|b_alpha_EM|+|C_JQ|+|C_Hodge_readout|+|Phi_EM_rad|)
```

## Live blockers

- Parent visible EM generator/no-Hom theorem is still unsigned.
- Live `H_XF2`, `z_g`, readout/radiative, charge-current, Hodge-readout, Poynting-flux and `K_qbar_EM` values are missing.
- Poynting is allowed as Hilbert EM stress/flux once, but double counting is forbidden.

## Next target

`{NEXT_TARGET}`
"""
    RESUME_PATH.write_text(resume, encoding="utf-8")


def validate(timestamp: str) -> list[dict[str, Any]]:
    source_rows = read_csv(SOURCE_REGISTER)
    output_rows = read_csv(RUNNER_OUTPUT)
    status_by_id = {row["row_id"]: row["runner_status"] for row in output_rows}
    qbar_by_id = {row["row_id"]: row["qbar_EM_bound_abs"] for row in output_rows}
    claims_text = read_text(CLAIMS_PATH)
    resume_text = read_text(RESUME_PATH)
    validation = [
        ("VAL4820_0_sources", all(row["exists"] == "True" and row["needle_found"] == "True" for row in source_rows), str(SOURCE_REGISTER)),
        ("VAL4820_1_image_audit", len(read_csv(IMAGE_AUDIT)) >= 5 and "EFZ4820_2_current_bottleneck" in read_text(IMAGE_AUDIT), str(IMAGE_AUDIT)),
        ("VAL4820_2_bound_contract", len(read_csv(BOUND_CONTRACT)) >= 4 and "EFB4820_2_qbarEM" in read_text(BOUND_CONTRACT), str(BOUND_CONTRACT)),
        ("VAL4820_3_poynting_ledger", len(read_csv(POYNTING_LEDGER)) >= 3 and "POY4820_2_no_double_count" in read_text(POYNTING_LEDGER), str(POYNTING_LEDGER)),
        ("VAL4820_4_live_image_blocks", status_by_id.get("RUN4820_0_current_image_missing") == "BLOCKED_EM_F2_IMAGE_ZERO_CLAUSES", str(RUNNER_OUTPUT)),
        ("VAL4820_5_conditional_image_pass", status_by_id.get("RUN4820_1_conditional_image_pass") == "EM_F2_IMAGE_ZERO_PASS_NONCLAIM", str(RUNNER_OUTPUT)),
        ("VAL4820_6_forbidden_alpha_fails", status_by_id.get("RUN4820_2_forbidden_alpha_obs_zero") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", str(RUNNER_OUTPUT)),
        ("VAL4820_7_live_finite_blocks", status_by_id.get("RUN4820_3_live_finite_missing") == "BLOCKED_EM_F2_FINITE_BOUND_INPUTS", str(RUNNER_OUTPUT)),
        ("VAL4820_8_finite_smoke_pass", status_by_id.get("RUN4820_4_finite_bound_smoke_pass") == "EM_F2_FINITE_BOUND_PASS_NONCLAIM" and qbar_by_id.get("RUN4820_4_finite_bound_smoke_pass", "").startswith("8.49"), str(RUNNER_OUTPUT)),
        ("VAL4820_9_poynting_controls", status_by_id.get("RUN4820_5_current_poynting_missing") == "BLOCKED_POYNTING_ONCE_CLAUSES" and status_by_id.get("RUN4820_6_poynting_once_smoke_pass") == "POYNTING_ONCE_PASS_NONCLAIM", str(RUNNER_OUTPUT)),
        ("VAL4820_10_forbidden_poynting_fails", status_by_id.get("RUN4820_7_forbidden_double_count") == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", str(RUNNER_OUTPUT)),
        ("VAL4820_11_claim_gates", all(row["claim_allowed"] == "False" for row in read_csv(CLAIM_GATES)), str(CLAIM_GATES)),
        ("VAL4820_12_claim_register", CLAIM_ID in claims_text and DECISION in claims_text, str(CLAIMS_PATH)),
        ("VAL4820_13_resume", NEXT_TARGET in resume_text and MARKER in resume_text, str(RESUME_PATH)),
        ("VAL4820_14_docs", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH};{FORMAL_PATH}"),
        ("VAL4820_15_pycache", not (SCRIPT_DIR / "__pycache__").exists(), str(SCRIPT_DIR / "__pycache__")),
    ]
    rows = [
        {
            "check_id": check_id,
            "description": check_id.replace("_", " "),
            "result": "PASS" if passed else "FAIL",
            "evidence": evidence,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, evidence in validation
    ]
    rows.append(
        {
            "check_id": "VAL4820_OVERALL",
            "description": "all 4820 validation gates pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": str(VALIDATION_CSV),
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    write_csv(SOURCE_REGISTER, build_source_register(timestamp))
    write_csv(IMAGE_AUDIT, build_image_audit(timestamp))
    write_csv(BOUND_CONTRACT, build_bound_contract(timestamp))
    write_csv(POYNTING_LEDGER, build_poynting_ledger(timestamp))
    write_csv(RUNNER_INPUT, build_runner_input(timestamp))
    run_runner()
    write_csv(DECISION_CSV, build_decision(timestamp))
    write_csv(CLAIM_GATES, claim_gate_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
    append_claim_register(timestamp)
    write_docs(timestamp)
    py_compile.compile(str(Path(__file__)), doraise=True)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation_rows = validate(timestamp)
    write_csv(VALIDATION_CSV, validation_rows)
    if validation_rows[-1]["result"] != "PASS":
        print(f"{MARKER}: validation FAIL; inspect {VALIDATION_CSV}")
        return 1
    print(f"{MARKER}: validation PASS; next {NEXT_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
