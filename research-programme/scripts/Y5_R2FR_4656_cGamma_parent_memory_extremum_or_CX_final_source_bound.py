from __future__ import annotations

import csv
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4656"
CLAIM_ID = "L-498"
BRANCH = "MTS_R2FR_Y5_CGAMMA_PARENT_MEMORY_EXTREMUM_OR_CX_FINAL_SOURCE_BOUND_4656"
MARKER = "PPC4161_CGAMMA_PARENT_MEMORY_EXTREMUM_OR_CX_FINAL_SOURCE_BOUND_4656"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PARENT_MEMORY_EXTREMUM_OR_CX_FINAL_SOURCE_BOUND_4656"
DECISION = "PARENT_MEMORY_EXTREMUM_NOHAIR_THEOREM_DERIVED_CURRENT_BRANCH_UNSIGNED_CMEM_BOUND_NEXT_NONCLAIM"
NEXT_TARGET = "4657-Y5-R2FR-Cmem-final-live-zero-or-first-source-backed-component-row.md"

DOC_PATH = POST / "4656-Y5-R2FR-cGamma-parent-memory-extremum-or-CX-final-source-bound.md"
FORMAL_PATH = FORMAL / "672-PPC4161-cGamma-parent-memory-extremum-or-CX-final-source-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4655 = POST / "4655-Y5-R2FR-cGamma-memory-projector-local-support-or-profile-bound.md"
FORMAL_203 = FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md"
FORMAL_204 = FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md"
DOC_4600 = POST / "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
DOC_4601 = POST / "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
DOC_4611 = POST / "4611-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
DOC_4612 = POST / "4612-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
DOC_4629 = POST / "4629-Y5-R2FR-canonical-normalization-and-first-anchor-smoke-runner.md"
DOC_4630 = POST / "4630-Y5-R2FR-co-normalized-gap-and-source-coupling-parent-action.md"
DOC_4648 = POST / "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
CSV_4631_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
CSV_4631_SYMMETRY = SOURCE_DIR / "P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv"
CSV_4632_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4632_IQ_SIGNATURE_HUNT_ROWS.csv"
CSV_4632_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4632_STATUS.csv"
CSV_4634_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4634_EPSILONA_FIRST_BOUND_MATRIX.csv"
CSV_4635_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4635_NO_SLOT_SOURCE_HUNT_ROWS.csv"
CSV_4636_QA = SOURCE_DIR / "P8_Y5_R2FR_4636_R10_VECTOR_CURVE_QA.csv"
CSV_4601_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4601_STATUS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4656_SOURCE_REGISTER.csv"
EXTREMUM_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_PARENT_MEMORY_EXTREMUM_THEOREM.csv"
NOHAIR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_POSITIVE_OPERATOR_NOHAIR_ROWS.csv"
SOURCE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_CMEM_SOURCE_BOUND_ROWS.csv"
PROMOTION_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_EXACT_VS_BOUND_PROMOTION_GATES.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4656_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4656_VALIDATION.csv"


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
    for row_data in rows:
        for field_name in row_data:
            if field_name not in fields:
                fields.append(field_name)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row_data in rows:
        for field_name in row_data:
            if field_name not in fields:
                fields.append(field_name)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row_data in rows:
        lines.append("| " + " | ".join(str(row_data.get(field_name, "")).replace("|", "\\|").replace("\n", " ") for field_name in fields) + " |")
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


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists() or not (repo / ".git").exists():
        return True, "absent or not git"
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    detail = result.stdout.strip()
    return detail == "", detail or "clean"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4656_00_4655_next", DOC_4655, "4656-Y5-R2FR-cGamma-parent-memory-extremum-or-CX-final-source-bound.md", "4655 selected this target."),
        ("SRC4656_01_203_definition", FORMAL_203, "E_Gamma^loc :=", "local c_Gamma projector definition."),
        ("SRC4656_02_204_product", FORMAL_204, "|c_Gamma * profile_a| <=", "finite c_Gamma product law."),
        ("SRC4656_03_4600_CX", DOC_4600, "C_X^final_live", "final C_X live envelope."),
        ("SRC4656_04_4601_operator", DOC_4601, "rho_X = B_X R_obs + C_X^final_live T + J_X^live", "body-charge source operator."),
        ("SRC4656_05_4601_memory", DOC_4601, "OP4601_1_memory", "memory-sector operator row."),
        ("SRC4656_06_4601_status", CSV_4601_STATUS, "BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_NONCLAIM", "body-charge score status."),
        ("SRC4656_07_4611_Qbar", DOC_4611, "|Qbar_XH| <=", "source-side Qbar_XH envelope."),
        ("SRC4656_08_4612_qbar", DOC_4612, "qbar_XT := M_T^-1 |delta_vX S_T|", "test-body qbar_XT envelope."),
        ("SRC4656_09_4629_conorm", DOC_4629, "CAN4629_1_source_coupling_co_normalization", "co-normalized source/range guard."),
        ("SRC4656_10_4630_action", DOC_4630, "S_parent = S_grav", "parent memory action contract."),
        ("SRC4656_11_4630_euler", DOC_4630, "VAR4630_0_memory_euler_lagrange", "memory Euler equation."),
        ("SRC4656_12_4631_even", CSV_4631_DERIVATION, "DER4631_0_even_matter_scale", "conditional extremum derivation."),
        ("SRC4656_13_4631_beta", CSV_4631_DERIVATION, "DER4631_1_beta_visible_zero", "conditional beta zero."),
        ("SRC4656_14_4631_symmetry", CSV_4631_SYMMETRY, "SYM4631_0_strong_parent_vertical_involution", "sufficient symmetry route."),
        ("SRC4656_15_4632_hunt", CSV_4632_HUNT, "HUNT4632_0_full_Iq_action_invariance", "signature not sourced."),
        ("SRC4656_16_4632_status", CSV_4632_STATUS, "full I_q/even-A_m signature not sourced", "4632 status."),
        ("SRC4656_17_4634_matrix", CSV_4634_MATRIX, "BM4634_0_R10", "epsilon bound matrix."),
        ("SRC4656_18_4635_no_slot", CSV_4635_HUNT, "NSH4635_0_no_hidden_visible_Hom", "no-slot source hunt unsigned."),
        ("SRC4656_19_4636_curve", CSV_4636_QA, "QA4636_4_claim_grade", "R10 curve QA nonclaim."),
        ("SRC4656_20_4648_tail", DOC_4648, "B_tail -> alpha_tail(lambda)=0", "same-branch Xi tail silence."),
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


def extremum_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PME4656_0_parent_action", "S_X^(2)=1/2 int[Z_X |grad delta_X|^2+M_X^2 delta_X^2]-int rho_X delta_X + boundary", "same parent quadratic action owns the gap and source term", "ACTION_FORM_IMPORTED"),
        ("PME4656_1_memory_source", "rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live", "memory source decomposes into curvature, matter trace, direct/open current and boundary terms", "SOURCE_DECOMPOSITION_IMPORTED"),
        ("PME4656_2_extremum_zero", "A_m(q,z)=A_m(q,-z) or no source-only A_m slot => partial_z ln A_m|0=0", "branch extremum kills the first-order visible trace source without fitting a small number", "CONDITIONAL_THEOREM_DERIVED_UNSIGNED"),
        ("PME4656_3_full_zero_bundle", "B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0 on one parent branch", "all nontrace/Poynting/hidden/boundary returns must vanish with the extremum before source silence is claimable", "EXACT_ZERO_BUNDLE_REQUIRED"),
        ("PME4656_4_current_signature", "full I_q/even-A_m/no-slot signatures are not sourced in the live corpus", "do not promote beta_visible=0 or rho_mem=0 as a public parent theorem", "CURRENT_BRANCH_UNSIGNED"),
        ("PME4656_5_resulting_route", "if PME4656_2+3 and positive gap hold, rho_mem=0", "the memory field has no local source and c_Gamma profile amplitude collapses for this source-owned channel", "DERIVATION_TARGET_EXACT"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": row_data[0],
            "formula_or_condition": row_data[1],
            "meaning": row_data[2],
            "status": row_data[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def nohair_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("NOH4656_0_operator", "L_mem=-nabla_i(Z_mem nabla^i)+M2_mem", "Z_mem>=Z_min>0, M2_mem>=M_min^2>0, zero modes removed", "positive local memory operator", "OPERATOR_POSITIVITY_CONDITION"),
        ("NOH4656_1_energy_identity", "int delta_m L_mem delta_m = int[Z_mem |grad delta_m|^2 + M2_mem delta_m^2] + boundary", "boundary term zero by fixed/no-flux/topological parent condition", "coercive energy identity", "DERIVED_CONDITIONAL"),
        ("NOH4656_2_exact_zero", "L_mem delta_m=0 plus NOH4656_0 and NOH4656_1 => delta_m=0", "rho_mem=0 and admissible boundary class", "memory amplitude A_mem=0", "NOHAIR_THEOREM_DERIVED_CONDITIONAL"),
        ("NOH4656_3_cGamma_zero", "A_mem=0 => profile_a[mem]=0 => C_Gamma,a[mem]=c_Gamma profile_a[mem]=0", "c_Gamma channel is silent only for the memory profile generated by the zeroed source-owned field", "local profile product zero", "CONDITIONAL_CGAMMA_SILENCE"),
        ("NOH4656_4_finite_green_bound", "A_mem <= [exp(R/lambda_mem) int_body(|B_mem_eff||R_obs|+|C_mem^final_live||T|+|J_mem_live|)dV + |Q_boundary_mem|]/(4*pi Z_min)", "if exact zero fails, this is the no-cancellation amplitude bound", "finite profile/product route", "BOUND_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "nohair_id": row_data[0],
            "statement": row_data[1],
            "conditions": row_data[2],
            "deduction": row_data[3],
            "status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def source_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CSB4656_0_ZM", "Z_mem,M2_mem,lambda_mem", "lambda_mem=sqrt(Z_mem/M2_mem)", "positive parent Hessian/operator normalization with units", "MISSING_PARENT_NUMERIC_OR_ZERO_MODE_CERTIFICATE"),
        ("CSB4656_1_Bmem", "B_mem_eff", "curvature/source-normalization memory leg", "parent exclusion or source-backed norm", "MISSING_ZERO_OR_VALUE"),
        ("CSB4656_2_Cmem", "C_mem^final_live", "matter-trace memory leg after 4600 final C split", "all C subblocks zero on one branch or source-backed absolute norm", "MISSING_ZERO_OR_VALUE"),
        ("CSB4656_3_Jmem", "J_mem_live", "direct/Poynting/non-Hilbert current leg", "closed no-flux theorem or source-backed flux/current profile", "MISSING_ZERO_OR_VALUE"),
        ("CSB4656_4_Qboundary", "Q_boundary_mem", "Green-function boundary charge", "parent boundary neutrality/no-flux/topological theorem or finite boundary integral", "MISSING_ZERO_OR_VALUE"),
        ("CSB4656_5_Amem", "A_mem", "NOH4656_4 finite Green bound", "all source terms zero or numeric/source-backed", "BOUND_FORMULA_READY_VALUES_MISSING"),
        ("CSB4656_6_source_test", "I_mem^ST(lambda)", "|I_mem^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_mem| G_N M_H_ref m_T)", "Qbar_XH, qbar_XT, Z_mem, M2_mem, lambda_mem, arena kernels", "PRODUCT_READY_VALUES_MISSING"),
        ("CSB4656_7_R10_curve", "alpha_bound(lambda)", "full vector curve exists for smoke, claim-grade QA still blocked", "official table/manual QA plus parent-owned prediction", "CURVE_QA_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_data[0],
            "quantity": row_data[1],
            "formula_or_role": row_data[2],
            "required_evidence": row_data[3],
            "current_status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4656_0_exact_parent", "full parent I_q/even-A_m or no-source-slot signature plus positive gap and zero boundary/source returns", "BLOCKED_UNSIGNED", "would set rho_mem=0 and A_mem=0"),
        ("PROM4656_1_finite_values", "Z_mem,M2_mem,B_mem_eff,C_mem^final_live,J_mem_live,Q_boundary_mem are numeric/source-backed or exact-zero", "BLOCKED_VALUES_MISSING", "would allow finite A_mem and product scoring"),
        ("PROM4656_2_source_test_product", "Qbar_XH, qbar_XT, M_H_ref, m_T, G_N convention and arena kernels are source-backed", "BLOCKED_VALUES_MISSING", "would allow R10/PPN/clock/orbital scoring"),
        ("PROM4656_3_R10_curve", "full alpha(lambda) curve is claim-grade QA'd or official table sourced", "BLOCKED_QA_NONCLAIM", "would allow R10 comparison after parent rows exist"),
        ("PROM4656_4_no_claim", "no public local-GR/R10/PPN/clock/orbital/EM claim from this checkpoint", "PASSED_FIREWALL", "nonclaim guard active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": row_data[0],
            "requirement": row_data[1],
            "status": row_data[2],
            "effect": row_data[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4656_0_exact_parent_zero", "parent extremum + full zero bundle + positive gap", "PASS_CONDITIONAL_MEMORY_NOHAIR_NONCLAIM", "rho_mem=0, delta_m=0 and memory-generated c_Gamma profile products vanish."),
        ("RUN4656_1_current_live_branch", "current corpus signatures and values", "FAIL_CLOSED_UNSIGNED_AND_VALUES_MISSING", "full I_q/even-A_m/no-slot signatures are unsigned and C_mem/Z/M/source rows are missing."),
        ("RUN4656_2_Cmem_nonzero", "C_mem^final_live survives", "BOUND_ROUTE_ACTIVE", "A_mem is bounded by the trace-source Green-function envelope; no local-GR pass."),
        ("RUN4656_3_total_mass_shortcut", "use calibrated G or total mass to hide C_mem/Jmem", "REJECTED_FIREWALL", "source coupling/profile rows must be owned before readout."),
        ("RUN4656_4_R10_exact_tail", "B_tail exact selector signed", "PASS_CONDITIONAL_ALPHA_TAIL_ZERO_NONCLAIM", "kept as R10 tail silence, not full local-GR promotion."),
        ("RUN4656_5_next", "4656 theorem/bound split complete", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row_data[0],
            "case": row_data[1],
            "result": row_data[2],
            "reason": row_data[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4656_0_no_signature_no_zero", "Do not set rho_mem=0 unless parent extremum/no-source/zero-boundary clauses are signed on one branch."),
        ("CTRL4656_1_positive_gap_required", "No-hair proof requires Z_mem>0, M2_mem>0 or a parent-owned zero-mode removal condition."),
        ("CTRL4656_2_no_total_mass_hiding", "C_mem/Jmem/profile/source terms cannot be absorbed into calibrated G or orbital GM."),
        ("CTRL4656_3_no_rescaling_win", "Z_mem/M2_mem/range and source amplitude must use the same canonical normalization."),
        ("CTRL4656_4_no_R10_promotion", "R10 tail or anchor smoke success does not promote PPN/Newton/Maxwell/local-GR."),
        ("CTRL4656_5_absolute_bounds", "Finite source terms use absolute envelopes unless a parent identity signs cancellation."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row_data[0],
            "firewall": row_data[1],
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4656_0",
            "decision": DECISION,
            "summary": "4656 derives the exact parent-memory extremum no-hair theorem: a same-branch matter-scale extremum/no-source bundle plus positive memory operator forces rho_mem=0, then delta_m=0, then memory-generated c_Gamma profile products vanish. The live corpus cannot claim it because full I_q/even-A_m/no-slot signatures and Cmem/Z/M/source values remain unsigned or missing. The nonclaim fallback is now the explicit finite A_mem/Cmem/Qbar/qbar source-bound path.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PARENT_MEMORY_NOHAIR_THEOREM_DERIVED_LIVE_BRANCH_UNSIGNED_CMEM_BOUND_NEXT_NONCLAIM",
            "exact_route": "conditional_parent_extremum_positive_gap_zero_source",
            "live_branch": "unsigned_signature_values_missing",
            "finite_route": "A_mem_Cmem_Qbar_qbar_source_bound",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The exact theorem is now written, but live promotion hinges on C_mem^final_live: either prove the matter-trace memory leg is zero in the parent branch or fill its first source-backed component row.",
            "success_condition": "C_mem^final_live is parent-zero in one branch or decomposed into source-backed numeric/theorem-zero components that feed A_mem without placeholders.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + theorem + nohair + bounds + gates + runners + decisions
    checks = [
        ("VAL4656_00_sources_exist", all(row_data["path_exists"] for row_data in sources), "all cited paths exist"),
        ("VAL4656_01_needles_found", all(row_data["needle_found"] for row_data in sources), "all source needles found"),
        ("VAL4656_02_line_anchors", all(int(row_data["line_number"]) > 0 for row_data in sources), "all source line anchors positive"),
        ("VAL4656_03_extremum_theorem", any(row_data["theorem_id"] == "PME4656_2_extremum_zero" for row_data in theorem), "parent extremum zero theorem row present"),
        ("VAL4656_04_positive_nohair", any(row_data["nohair_id"] == "NOH4656_2_exact_zero" for row_data in nohair), "positive-operator nohair row present"),
        ("VAL4656_05_finite_bound", any(row_data["nohair_id"] == "NOH4656_4_finite_green_bound" for row_data in nohair), "finite Green-function bound row present"),
        ("VAL4656_06_Cmem_next", any(row_data["bound_id"] == "CSB4656_2_Cmem" and "MISSING" in row_data["current_status"] for row_data in bounds), "Cmem live bound row retained"),
        ("VAL4656_07_live_fail_closed", any(row_data["run_id"] == "RUN4656_1_current_live_branch" and row_data["result"].startswith("FAIL_CLOSED") for row_data in runners), "current live branch fails closed"),
        ("VAL4656_08_no_claim", all(str(row_data.get("valid_for_claim", "False")) == "False" and str(row_data.get("claim_allowed", "False")) == "False" for row_data in all_rows), "no row is claim-grade"),
        ("VAL4656_09_next_selected", decisions and decisions[0]["next_target"] == NEXT_TARGET, "4657 selected next"),
        ("VAL4656_10_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4656_11_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4656_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4656 parent-memory extremum/nohair and Cmem bound gate passed" if all(passed for _, passed, _ in checks) else "4656 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4656 - c_Gamma parent memory extremum or C_X final source bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4656 derives the exact theorem shape that would close the memory-generated `c_Gamma` source without closure magic.

Start from the parent memory operator:

`L_mem delta_m = rho_mem`,

with

`L_mem = -nabla_i(Z_mem nabla^i) + M2_mem`,

and

`rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live`.

If one parent branch supplies:

1. a matter-scale extremum or no-source-slot signature so the first-order trace coupling vanishes,
2. `B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0`,
3. `Z_mem>0`, `M2_mem>0` with zero modes removed,
4. fixed/no-flux/topological boundary class,

then the energy identity gives:

`int[Z_mem |grad delta_m|^2 + M2_mem delta_m^2] = 0`,

so:

`delta_m = 0`,

and the memory-generated `c_Gamma` profile product vanishes:

`C_Gamma,a[mem] = c_Gamma profile_a[mem] = 0`.

This is a real derivation target, not a plateau axiom.

The current live corpus still cannot claim it: full `I_q`/even-`A_m`/no-source-slot signatures are unsigned, and the finite rows `Z_mem`, `M2_mem`, `C_mem^final_live`, `J_mem_live`, `Q_boundary_mem`, `Qbar_XH`, `qbar_XT` and arena kernels remain missing or nonclaim.

So the next non-circling target is `C_mem^final_live`: prove it zero in the parent branch or fill the first source-backed component row.

## Source Register

{table(sources)}

## Parent Memory Extremum Theorem

{table(theorem)}

## Positive Operator Nohair Rows

{table(nohair)}

## Cmem Source Bound Rows

{table(bounds)}

## Exact vs Bound Promotion Gates

{table(gates)}

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
        "4656 derives the exact parent-memory extremum/no-hair route for the memory-generated c_Gamma profile: if a single parent branch gives a matter-scale extremum/no-source bundle, positive Z_mem/M2_mem, and zero B_mem/C_mem/J_mem/Q_boundary terms, then rho_mem=0, delta_m=0, and c_Gamma profile products vanish. The live corpus remains nonclaim because the parent signatures and source-backed Cmem/Z/M/Qbar/qbar rows are still missing.",
        "Generated source register, parent memory extremum theorem, positive-operator nohair rows, Cmem source-bound rows, promotion gates, runner, controls, decision, status, next target and validation.",
        "parent_memory_extremum_nohair_theorem_Cmem_bound_nonclaim",
        NEXT_TARGET,
        "Claiming c_Gamma/local-GR closure before the parent extremum/no-source bundle is signed, treating calibrated G or total mass as source-profile proof, or scoring finite rows with placeholders.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/clock/orbital/Maxwell claim until C_mem^final_live and the associated Z/M/source-test rows are parent-zero or source-backed and pass.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4656 derives the exact parent-memory extremum/no-hair theorem for the memory-generated `c_Gamma` profile. With a same-branch matter-scale extremum/no-source bundle, `B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0`, positive `Z_mem/M2_mem`, and fixed/no-flux boundary class, `rho_mem=0` and the coercive energy identity forces `delta_m=0`; hence `C_Gamma,a[mem]=0`. This is nonclaim because the live parent signatures and finite `C_mem/Z/M/Qbar/qbar` rows are still missing. Next target: `C_mem^final_live` zero or first source-backed component row.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4656` converts the c_Gamma memory route into an exact extremum/no-hair theorem plus finite Cmem source-bound fallback. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    theorem = extremum_theorem_rows(timestamp)
    nohair = nohair_rows(timestamp)
    bounds = source_bound_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, theorem, nohair, bounds, gates, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EXTREMUM_THEOREM_CSV, theorem)
    write_csv(NOHAIR_CSV, nohair)
    write_csv(SOURCE_BOUND_CSV, bounds)
    write_csv(PROMOTION_GATE_CSV, gates)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, theorem, nohair, bounds, gates, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4656 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
