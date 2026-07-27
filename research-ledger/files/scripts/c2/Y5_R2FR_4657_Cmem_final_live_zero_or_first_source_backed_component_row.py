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

CHECKPOINT = "4657"
CLAIM_ID = "L-499"
BRANCH = "MTS_R2FR_Y5_CMEM_FINAL_LIVE_ZERO_OR_FIRST_SOURCE_BACKED_COMPONENT_ROW_4657"
MARKER = "PPC4161_CMEM_FINAL_LIVE_ZERO_OR_FIRST_SOURCE_BACKED_COMPONENT_ROW_4657"
PACKET_MARKER = "PPC4161_PACKET_CMEM_FINAL_LIVE_ZERO_OR_FIRST_SOURCE_BACKED_COMPONENT_ROW_4657"
DECISION = "CMEM_FINAL_LIVE_COMPONENT_SPLIT_AND_FIRST_ALPHA_TARGET_SELECTED_NONCLAIM"
NEXT_TARGET = "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md"

DOC_PATH = POST / "4657-Y5-R2FR-Cmem-final-live-zero-or-first-source-backed-component-row.md"
FORMAL_PATH = FORMAL / "673-PPC4161-Cmem-final-live-zero-or-first-source-backed-component-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4656 = POST / "4656-Y5-R2FR-cGamma-parent-memory-extremum-or-CX-final-source-bound.md"
DOC_4601 = POST / "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
CSV_4597_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4597_CMEM_CH_DESCENT_ZERO_BRANCH.csv"
CSV_4597_CXLIVE = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv"
CSV_4598_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4598_CONSTANT_WEIGHT_ZERO_THEOREM.csv"
CSV_4598_SENS = SOURCE_DIR / "P8_Y5_R2FR_4598_CX_STANDARD_WEIGHT_SENSITIVITY_BOUND.csv"
CSV_4598_NORM = SOURCE_DIR / "P8_Y5_R2FR_4598_FIRST_CXLIVE_NORM_ROWS.csv"
CSV_4599_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv"
CSV_4600_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
CSV_4600_NORM = SOURCE_DIR / "P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv"
CSV_4600_BODY = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
CSV_4656_NOHAIR = SOURCE_DIR / "P8_Y5_R2FR_4656_POSITIVE_OPERATOR_NOHAIR_ROWS.csv"
CSV_4656_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4656_CMEM_SOURCE_BOUND_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4657_SOURCE_REGISTER.csv"
DECOMP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_CMEM_FINAL_DECOMPOSITION.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_CMEM_COMPONENT_ZERO_THEOREM.csv"
QUEUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_FIRST_COMPONENT_QUEUE.csv"
ALPHA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_BALPHA_SOURCE_ROW_TEMPLATE.csv"
AMP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_AMEM_INSERTION_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4657_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4657_VALIDATION.csv"


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
        ("SRC4657_00_4656_next", DOC_4656, "4657-Y5-R2FR-Cmem-final-live-zero-or-first-source-backed-component-row.md", "4656 selects C_mem final live as the next non-circling target."),
        ("SRC4657_01_4597_Cmem_qbasic", CSV_4597_CMEM, "DZ4597_0_memory", "C_mem q-basic subterm zero is not full C_mem zero."),
        ("SRC4657_02_4597_CX_live", CSV_4597_CXLIVE, "CX4597_7_live_total", "live matter-trace vector ancestry."),
        ("SRC4657_03_4598_std_weight_zero", CSV_4598_ZERO, "ZW4598_2_combined", "standard/weight zero-or-bound theorem."),
        ("SRC4657_04_4598_alpha", CSV_4598_SENS, "SB4598_0_alpha", "fine-structure/Maxwell normalization first sensitivity row."),
        ("SRC4657_05_4598_std_weight_norm", CSV_4598_NORM, "CXN4598_5_total", "first live norm total row."),
        ("SRC4657_06_4599_LHRS_zero", CSV_4599_ZERO, "LHRS4599_4_combined", "label/Hodge/support/readout combined zero-or-bound row."),
        ("SRC4657_07_4599_LHRS_norm", CSV_4599_NORM, "C4599_4_LHRS", "LHRS live norm row."),
        ("SRC4657_08_4600_final_zero", CSV_4600_ZERO, "BNH4600_4_final_CX_live", "final C_X live split zero-or-bound row."),
        ("SRC4657_09_4600_final_norm", CSV_4600_NORM, "C4600_4_final", "final matter-trace coupling norm row."),
        ("SRC4657_10_4600_Amem", CSV_4600_BODY, "BU4600_1_memory", "A_mem envelope containing C_mem final live."),
        ("SRC4657_11_4601_memory_operator", DOC_4601, "OP4601_1_memory", "memory field operator and source split."),
        ("SRC4657_12_4656_nohair", CSV_4656_NOHAIR, "NOH4656_4_finite_green_bound", "finite Green-function fallback from 4656."),
        ("SRC4657_13_4656_Cmem", CSV_4656_CMEM, "CSB4656_2_Cmem", "4656 C_mem zero-or-value source bound row."),
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


def decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "CDF4657_0_projection",
            "C_mem^final_live := Pi_mem[C_X^final_live]",
            "memory sector inherits the final matter-trace live coefficient by sector projection",
            "Pi_mem linear and same parent branch/readout",
            "PROJECTION_DEFINITION_IMPORTED",
        ),
        (
            "CDF4657_1_std_weight",
            "C_mem^std_weight_live := Pi_mem[C_X^std_weight_live]",
            "constant/source-weight/material sensitivity block",
            "b_alpha_mem,b_mass_mem,b_clock_mem,D_mem ln(kappa_eff),delta_w_mem",
            "FIRST_BLOCK_SELECTED",
        ),
        (
            "CDF4657_2_LHRS",
            "C_mem^LHRS_live := Pi_mem[C_X^LHRS_live]",
            "label, Hodge/EM, support, and readout leakage block",
            "C_label_mem,C_Hodge_mem,C_support_mem,C_readout_mem",
            "ZERO_OR_ABSOLUTE_SUM_READY_VALUES_MISSING",
        ),
        (
            "CDF4657_3_boundary_nonHilbert",
            "C_mem^boundary_nonHilbert_live := Pi_mem[C_X^boundary + C_X^nonHilbert]",
            "boundary/reference/domain-wall plus non-Hilbert current bypass block",
            "C_boundary_mem,C_nonHilbert_mem",
            "ZERO_OR_ABSOLUTE_SUM_READY_VALUES_MISSING",
        ),
        (
            "CDF4657_4_final_sum",
            "C_mem^final_live = C_mem^std_weight_live + C_mem^LHRS_live + C_mem^boundary_nonHilbert_live",
            "C_mem is now a named component vector, not a fog constant",
            "same memory projection applied to the 4600 final C_X split",
            "FINAL_DECOMPOSITION_DERIVED_NONCLAIM",
        ),
        (
            "CDF4657_5_triangle_bound",
            "|C_mem^final_live| <= |C_mem^std_weight_live| + |C_mem^LHRS_live| + |C_mem^boundary| + |C_mem^nonHilbert|",
            "no-cancellation finite fallback bound for A_mem and local residual scoring",
            "source-backed values or exact-zero certificates required for every subblock",
            "BOUND_READY_VALUES_MISSING",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "decomposition_id": row_data[0],
            "formula": row_data[1],
            "meaning": row_data[2],
            "required_condition": row_data[3],
            "status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "ZCM4657_0_linearity",
            "Pi_mem(a+b+c)=Pi_mem(a)+Pi_mem(b)+Pi_mem(c)",
            "the 4600 C_X split descends into the memory trace leg componentwise",
            "linear sector projection on one branch",
            "DERIVED",
        ),
        (
            "ZCM4657_1_sufficient_zero",
            "C_mem^std_weight_live=C_mem^LHRS_live=C_mem^boundary=C_mem^nonHilbert=0 => C_mem^final_live=0",
            "same-branch component zeros are sufficient for exact trace-source silence",
            "all zeros must be signed in the same parent branch",
            "EXACT_ZERO_ROUTE_DERIVED_CONDITIONAL",
        ),
        (
            "ZCM4657_2_no_cancellation_guard",
            "if subblocks are not zero, use the absolute-sum bound rather than cancellation",
            "prevents fitted-G/mass/readout cancellations from being smuggled into C_mem=0",
            "no parent-owned orthogonality/cancellation identity currently sourced",
            "FAIL_CLOSED_TO_BOUND",
        ),
        (
            "ZCM4657_3_std_weight_expansion",
            "|C_mem^std_weight_live| <= |b_alpha_mem||S_alpha^mem| + |b_mass_mem||S_mass^mem| + |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|",
            "the first live block reduces to named sensitivity coefficients and memory source weights",
            "source weights and sensitivities must be theorem-zero or source-backed",
            "FIRST_BLOCK_BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "ZCM4657_4_balpha_zero_contract",
            "b_alpha_mem := Pi_mem[D_X ln(alpha_EM)] = 0",
            "fine-structure/Maxwell normalization drift dies if charge, Maxwell F^2 normalization, current coupling and Hodge/readout all descend through q with no independent memory vertical slot",
            "unique Maxwell-Hodge/current owner plus q-basic charge normalization",
            "NEXT_DERIVATION_TARGET",
        ),
        (
            "ZCM4657_5_live_verdict",
            "current live branch cannot set C_mem^final_live=0",
            "the split is derived, but parent-signed zero/value rows are still missing",
            "all subblocks remain valid_for_claim=false",
            "NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row_data[0],
            "statement": row_data[1],
            "deduction": row_data[2],
            "condition": row_data[3],
            "status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def queue_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FCQ4657_0", 1, "C_mem^std_weight_live", "first block", "dominates all matter-trace sensitivity before label/Hodge/support/boundary complications", "attack b_alpha_mem first"),
        ("FCQ4657_1", 2, "b_alpha_mem", "first coefficient", "connects Maxwell normalization, charge/fine-structure, clocks, EM/Poynting, and R10 source strength", NEXT_TARGET),
        ("FCQ4657_2", 3, "b_mass_mem", "second coefficient", "composition and binding-energy drift; WEP/material arena", "after alpha unless alpha zero proof fails hard"),
        ("FCQ4657_3", 4, "D_mem ln(kappa_eff)", "coupling coefficient", "already structurally constrained by 4654 but must be memory-projected", "reuse delta_kappa lock if branch match is signed"),
        ("FCQ4657_4", 5, "C_mem^LHRS_live", "second block", "label/Hodge/support/readout leakage after standard/weight", "only after first block is zero or bounded"),
        ("FCQ4657_5", 6, "C_mem^boundary_nonHilbert_live", "third block", "boundary and non-Hilbert current bypass", "last because it needs boundary/current source data"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "queue_id": row_data[0],
            "priority": row_data[1],
            "symbol": row_data[2],
            "role": row_data[3],
            "reason": row_data[4],
            "next_action": row_data[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def alpha_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        (
            "BAS4657_0_definition",
            "b_alpha_mem",
            "Pi_mem[D_X ln(alpha_EM)]",
            "dimensionless vertical sensitivity",
            "exact zero if alpha_EM descends through q and has no independent memory vertical generator",
            "source-backed finite value if Maxwell/charge owner not zero",
            "MISSING_PARENT_MAXWELL_NORMALIZATION_OWNER",
        ),
        (
            "BAS4657_1_Maxwell_owner",
            "S_EM",
            "-1/4 int Z_EM F_ab F^ab sqrt(-g_obs)d4x + int J^a A_a",
            "action-normalization clause",
            "same observed metric/Hodge/current owner; no second charge normalization slot",
            "finite Delta_Hodge_EM/readout/current drift row",
            "MISSING_PARENT_ACTION_SOURCE_PATH",
        ),
        (
            "BAS4657_2_charge_owner",
            "e_or_alpha_EM",
            "alpha_EM=e^2/(4*pi hbar c) in chosen unit grammar",
            "normalization/readout clause",
            "e,hbar,c and EM unit conversion are q-basic or topological/superselected for the memory vertical generator",
            "finite b_alpha_mem with units and source path",
            "MISSING_QBASIC_CHARGE_UNIT_GRAMMAR",
        ),
        (
            "BAS4657_3_claim_gate",
            "b_alpha_mem_valid",
            "valid_for_claim=true only if BAS4657_0..2 are parent-signed or numeric/source-backed",
            "promotion rule",
            "no MISSING_* markers; source paths exist; no fitted-G/mass absorption",
            "false until source-backed",
            "VALID_FOR_CLAIM_FALSE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "alpha_id": row_data[0],
            "symbol": row_data[1],
            "formula_or_definition": row_data[2],
            "units": row_data[3],
            "zero_route": row_data[4],
            "finite_fallback": row_data[5],
            "current_status": row_data[6],
            "source_path": "MISSING_SOURCE_PATH" if "MISSING" in row_data[6] else "",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def amplitude_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("AMP4657_0_imported", "|A_mem| <= [exp(R/lambda_mem) int_body(|B_mem_eff||R_obs|+|C_mem^final_live||T|+|J_mem_live|)dV + |Q_boundary_mem|]/(4*pi Z_min)", "4656/4601 finite Green-function envelope", "BOUND_IMPORTED_VALUES_MISSING"),
        ("AMP4657_1_Cmem_inserted", "|C_mem^final_live||T| <= (|C_mem^std_weight_live|+|C_mem^LHRS_live|+|C_mem^boundary|+|C_mem^nonHilbert|)|T|", "4657 inserts the final C_mem split into A_mem", "INSERTION_DERIVED_VALUES_MISSING"),
        ("AMP4657_2_exact_zero_branch", "C_mem^final_live=0 removes the trace-source term from A_mem", "only if all component zeros are same-branch signed", "CONDITIONAL_ZERO_BRANCH"),
        ("AMP4657_3_live_branch", "C_mem^final_live remains in A_mem as an explicit absolute-sum source term", "current branch has no source-backed values, so no local-GR/R10/PPN pass", "FAIL_CLOSED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "amplitude_id": row_data[0],
            "formula": row_data[1],
            "meaning": row_data[2],
            "status": row_data[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4657_0_exact_zero_bundle", "all C_mem subblocks same-branch zero", "PASS_CONDITIONAL", "C_mem^final_live=0 and trace term drops from rho_mem; still needs B/J/Q/Z/M clauses."),
        ("RUN4657_1_current_live_branch", "current source rows", "FAIL_CLOSED_MISSING_VALUES", "C_mem split exists but b_alpha/b_mass/clock/kappa/weight/LHRS/boundary/nonHilbert rows are missing or nonclaim."),
        ("RUN4657_2_bound_branch", "finite no-cancellation route", "SCHEMA_READY_VALUES_MISSING", "A_mem can be scored once every component has a source-backed norm and units."),
        ("RUN4657_3_first_target", "component attack order", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row_data[0],
            "branch": row_data[1],
            "result": row_data[2],
            "detail": row_data[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4657_0_no_cancellation", "do not cancel live subblocks unless the parent action gives an explicit orthogonality/sign identity"),
        ("CTRL4657_1_no_G_hiding", "do not hide C_mem trace leakage inside calibrated G, source mass, orbital GM or nuisance offsets"),
        ("CTRL4657_2_same_branch", "do not combine zero clauses from different branches/readouts/domains"),
        ("CTRL4657_3_EM_Poynting", "treat EM/Poynting as Hilbert stress/action-owned or source-bounded, not as a vague background force"),
        ("CTRL4657_4_local_only", "local private checkpoint only; no GitHub push or public claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row_data[0],
            "rule": row_data[1],
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4657_0",
            "decision": DECISION,
            "rationale": "4657 derives the memory-projected final C split and the sufficient componentwise zero theorem. The live branch still cannot claim C_mem=0, but the next attack is no longer vague: prove b_alpha_mem=0 from Maxwell/charge normalization descent or fill its first source-backed sensitivity row.",
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
            "status": DECISION,
            "exact_zero_status": "CONDITIONAL_COMPONENTWISE_ZERO_DERIVED",
            "live_branch_status": "BLOCKED_VALUES_MISSING",
            "first_component": "b_alpha_mem",
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
            "why": "b_alpha_mem is the first standard/weight coefficient inside C_mem^final_live; zeroing it tests whether Maxwell charge/fine-structure normalization descends through the same parent branch.",
            "acceptance_gate": "prove b_alpha_mem=0 from parent Maxwell/Hodge/current/unit descent, or create a source-backed numeric bound row with units and source path; no claim if placeholders remain.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    decomp: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    alpha: list[dict[str, Any]],
    amps: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + decomp + zeros + queue + alpha + amps + runners + controls + decisions
    checks = [
        ("VAL4657_00_sources_exist", all(row_data["path_exists"] for row_data in sources), "all cited source paths exist"),
        ("VAL4657_01_needles_found", all(row_data["needle_found"] for row_data in sources), "all cited source needles found"),
        ("VAL4657_02_line_anchors", all(int(row_data["line_number"]) > 0 for row_data in sources), "all cited source line anchors positive"),
        ("VAL4657_03_final_split", any(row_data["decomposition_id"] == "CDF4657_4_final_sum" for row_data in decomp), "C_mem final split present"),
        ("VAL4657_04_triangle_bound", any(row_data["decomposition_id"] == "CDF4657_5_triangle_bound" for row_data in decomp), "C_mem absolute-sum bound present"),
        ("VAL4657_05_zero_theorem", any(row_data["zero_id"] == "ZCM4657_1_sufficient_zero" for row_data in zeros), "componentwise same-branch zero theorem present"),
        ("VAL4657_06_no_cancellation_guard", any(row_data["zero_id"] == "ZCM4657_2_no_cancellation_guard" for row_data in zeros), "no-cancellation guard present"),
        ("VAL4657_07_first_target_alpha", any(row_data["symbol"] == "b_alpha_mem" and int(row_data["priority"]) == 2 for row_data in queue), "b_alpha_mem selected as first coefficient"),
        ("VAL4657_08_alpha_nonclaim", all(str(row_data["valid_for_claim"]) == "False" and ("MISSING" in row_data["source_path"] or row_data["current_status"] == "VALID_FOR_CLAIM_FALSE") for row_data in alpha), "alpha rows remain nonclaim placeholders"),
        ("VAL4657_09_Amem_insertion", any(row_data["amplitude_id"] == "AMP4657_1_Cmem_inserted" for row_data in amps), "A_mem insertion row present"),
        ("VAL4657_10_live_fail_closed", any(row_data["run_id"] == "RUN4657_1_current_live_branch" and row_data["result"].startswith("FAIL_CLOSED") for row_data in runners), "current live branch fails closed"),
        ("VAL4657_11_no_claim", all(str(row_data.get("valid_for_claim", "False")) == "False" and str(row_data.get("claim_allowed", "False")) == "False" for row_data in all_rows), "no row is claim-grade"),
        ("VAL4657_12_next_selected", decisions and decisions[0]["next_target"] == NEXT_TARGET, "4658 selected next"),
        ("VAL4657_13_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4657_14_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4657_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4657 C_mem decomposition and first alpha target gate passed" if all(passed for _, passed, _ in checks) else "4657 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    decomp: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    alpha: list[dict[str, Any]],
    amps: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4657 - Cmem final live zero or first source-backed component row

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4657 does the next non-circling thing: it turns `C_mem^final_live` from a single missing symbol into a memory-projected component vector.

From 4600:

`C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live`.

Projecting to the memory trace leg gives:

`C_mem^final_live = C_mem^std_weight_live + C_mem^LHRS_live + C_mem^boundary_nonHilbert_live`,

with the no-cancellation fallback:

`|C_mem^final_live| <= |C_mem^std_weight_live| + |C_mem^LHRS_live| + |C_mem^boundary| + |C_mem^nonHilbert|`.

So the exact zero route is now precise:

`C_mem^std_weight_live=C_mem^LHRS_live=C_mem^boundary=C_mem^nonHilbert=0`

on the same parent branch implies:

`C_mem^final_live=0`.

That removes the trace-source term from:

`rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live`.

The live branch still cannot claim it because the component rows are not parent-signed or numeric/source-backed. But the first coefficient is no longer vague: attack `b_alpha_mem := Pi_mem[D_X ln(alpha_EM)]`.

If Maxwell `F^2`, charge/current normalization, Hodge/readout and unit grammar all descend through `q` with no independent memory vertical slot, then `b_alpha_mem=0`. If not, it must become a sourced finite row before any local-GR/R10/PPN/clock/EM claim.

## Source Register

{table(sources)}

## Cmem Final Decomposition

{table(decomp)}

## Component Zero Theorem

{table(zeros)}

## First Component Queue

{table(queue)}

## b_alpha Source Row Template

{table(alpha)}

## A_mem Insertion Rows

{table(amps)}

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
        "4657 decomposes C_mem^final_live into memory-projected standard/weight, LHRS, boundary and non-Hilbert subblocks. It derives the sufficient same-branch componentwise zero route and the absolute-sum fallback bound, then selects b_alpha_mem as the first concrete coefficient target.",
        "Generated source register, Cmem final decomposition, component zero theorem, first component queue, b_alpha source-row template, A_mem insertion rows, runner, controls, decision, status, next target and validation.",
        "Cmem_final_live_component_split_balpha_first_target_nonclaim",
        NEXT_TARGET,
        "Claiming C_mem=0 by cancellation, mixing branch-specific zeros, hiding trace leakage inside calibrated G or fitted mass, or treating alpha/Maxwell normalization as zero without a parent owner.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/clock/orbital/Maxwell claim until C_mem subblocks are same-branch theorem-zero or source-backed with units and source paths.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4657 turns `C_mem^final_live` into the memory-projected split `C_mem^std_weight_live + C_mem^LHRS_live + C_mem^boundary_nonHilbert_live`. Same-branch zeros of all subblocks are sufficient for exact trace-source silence; otherwise the no-cancellation absolute-sum bound feeds `A_mem`. The live corpus remains nonclaim, but the first concrete coefficient target is now `b_alpha_mem=Pi_mem[D_X ln(alpha_EM)]`, i.e. Maxwell/charge normalization descent.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4657` decomposes `C_mem^final_live`, installs the componentwise zero theorem and selects `b_alpha_mem` as the first source-backed or theorem-zero coefficient target. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    decomp = decomposition_rows(timestamp)
    zeros = zero_theorem_rows(timestamp)
    queue = queue_rows(timestamp)
    alpha = alpha_rows(timestamp)
    amps = amplitude_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, decomp, zeros, queue, alpha, amps, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DECOMP_CSV, decomp)
    write_csv(ZERO_CSV, zeros)
    write_csv(QUEUE_CSV, queue)
    write_csv(ALPHA_CSV, alpha)
    write_csv(AMP_CSV, amps)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, decomp, zeros, queue, alpha, amps, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4657 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
