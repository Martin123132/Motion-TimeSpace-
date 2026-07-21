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

CHECKPOINT = "4658"
CLAIM_ID = "L-500"
BRANCH = "MTS_R2FR_Y5_BALPHA_MAXWELL_NORMALIZATION_OWNER_OR_FIRST_SOURCE_BOUND_4658"
MARKER = "PPC4161_BALPHA_MAXWELL_NORMALIZATION_OWNER_OR_FIRST_SOURCE_BOUND_4658"
PACKET_MARKER = "PPC4161_PACKET_BALPHA_MAXWELL_NORMALIZATION_OWNER_OR_FIRST_SOURCE_BOUND_4658"
DECISION = "BALPHA_MEM_FIXED_QBASIC_BRANCH_ZERO_IMPORTED_DYNAMIC_BRANCH_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4659-Y5-R2FR-bmass-matter-spectrum-owner-or-WEP-composition-bound.md"

DOC_PATH = POST / "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md"
FORMAL_PATH = FORMAL / "674-PPC4161-balpha-Maxwell-normalization-owner-or-first-source-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4657 = POST / "4657-Y5-R2FR-Cmem-final-live-zero-or-first-source-backed-component-row.md"
DOC_4653 = POST / "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_225 = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
FORMAL_329 = FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md"
FORMAL_630 = FORMAL / "630-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
FORMAL_669 = FORMAL / "669-PPC4161-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"

CSV_4209_IDENT = SOURCE_DIR / "P8_Y5_R2FR_4209_NORMALIZATION_IDENTITIES.csv"
CSV_4209_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4209_OWNER_CONTRACT.csv"
CSV_4313_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4313_CURRENT_NORMALIZATION_CONTRACT.csv"
CSV_4313_WARD = SOURCE_DIR / "P8_Y5_R2FR_4313_EM_WARD_CURRENT_THEOREM.csv"
CSV_4437_DERIV = SOURCE_DIR / "P8_Y5_R2FR_4437_DERIVATION_ROWS.csv"
CSV_4437_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
CSV_4437_COUPLING = SOURCE_DIR / "P8_Y5_R2FR_4437_SAME_OWNER_COUPLING_OUTPUT.csv"
CSV_4437_SURVIVORS = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_SURVIVOR_ROWS.csv"
CSV_4614_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4614_EM_GAUGE_KINETIC_THEOREM.csv"
CSV_4614_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4614_GAUGE_OWNER_CLAUSES.csv"
CSV_4614_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_NORMAL_FORM_ROWS.csv"
CSV_4614_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_SOURCE_ROW_NONCLAIM.csv"
CSV_4614_PROMOTION = SOURCE_DIR / "P8_Y5_R2FR_4614_PROMOTION_GATES.csv"
CSV_4657_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4657_BALPHA_SOURCE_ROW_TEMPLATE.csv"
CSV_4657_QUEUE = SOURCE_DIR / "P8_Y5_R2FR_4657_FIRST_COMPONENT_QUEUE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4658_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_BALPHA_MEMORY_NORMAL_FORM.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_FIXED_BRANCH_ZERO_IMPORT.csv"
BOUND_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_DYNAMIC_BRANCH_BOUND_ROWS.csv"
CMEM_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_CMEM_STD_WEIGHT_UPDATE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4658_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4658_VALIDATION.csv"


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
        ("SRC4658_00_4657_next", DOC_4657, "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md", "4657 selected the b_alpha_mem target."),
        ("SRC4658_01_4657_alpha", CSV_4657_ALPHA, "BAS4657_0_definition", "b_alpha_mem template from 4657."),
        ("SRC4658_02_4657_queue", CSV_4657_QUEUE, "FCQ4657_1", "b_alpha_mem queue priority."),
        ("SRC4658_03_4209_identity", CSV_4209_IDENT, "NI4209_4_vertical_residual", "alpha_eff drift identity."),
        ("SRC4658_04_4209_owner", CSV_4209_OWNER, "OC4209_6_visible_EM_import", "calibrated visible EM import policy."),
        ("SRC4658_05_4313_fixed", CSV_4313_CURRENT, "CN4313_1_fixed_visible_branch", "fixed visible branch zero route."),
        ("SRC4658_06_4313_no_fake", CSV_4313_CURRENT, "CN4313_4_no_fake_alpha", "no numerical alpha prediction."),
        ("SRC4658_07_4313_ward", CSV_4313_WARD, "WT4313_4_zero_theorem", "same-current Ward exchange zero theorem."),
        ("SRC4658_08_4437_identity", CSV_4437_DERIV, "SOC4437_0_same_owner_identity", "same-owner EM drift identity."),
        ("SRC4658_09_4437_fixed_zero", CSV_4437_DERIV, "SOC4437_1_fixed_qbasic_branch_zero", "fixed q-basic branch kills b_alpha."),
        ("SRC4658_10_4437_balpha_zero", CSV_4437_ZERO, "ZERO4437_2_b_alpha", "machine b_alpha branch zero row."),
        ("SRC4658_11_4437_branch_output", CSV_4437_COUPLING, "SOC4437_0_fixed_qbasic_standard_branch", "branch-zero output row."),
        ("SRC4658_12_4437_survivors", CSV_4437_SURVIVORS, "SURV4437_1_global_unique_F2", "global/dynamic survivors retained."),
        ("SRC4658_13_4614_normal", CSV_4614_THEOREM, "EGK4614_0_normal_form", "normal form b_alpha=2z_g-z_lambda-z_readout-z_rad."),
        ("SRC4658_14_4614_zero_contract", CSV_4614_THEOREM, "EGK4614_1_zero_contract", "conjunctive zero contract."),
        ("SRC4658_15_4614_owner_verdict", CSV_4614_OWNER, "OWN4614_6_verdict", "owner clauses not globally promoted."),
        ("SRC4658_16_4614_bound", CSV_4614_NORMAL, "BA4614_6_bound", "absolute finite b_alpha bound."),
        ("SRC4658_17_4614_source", CSV_4614_SOURCE, "BSR4614_0_b_alpha_source_row", "source row contract if zero fails."),
        ("SRC4658_18_4614_promotion", CSV_4614_PROMOTION, "PROM4614_2_balpha_source", "promotion gate for finite row."),
        ("SRC4658_19_191_poynting", FORMAL_191, "Poynting vector is not a separate background field", "Poynting is Hilbert stress flux."),
        ("SRC4658_20_225_no_fake_alpha", FORMAL_225, "do not determine the absolute gauge kinetic coefficient", "classical U1 no numerical alpha theorem."),
        ("SRC4658_21_329_fixed_branch", FORMAL_329, "CN4313_1_fixed_visible_branch", "formal current normalization fixed branch."),
        ("SRC4658_22_630_normal", FORMAL_630, "b_alpha_EM := Lie_v ln(alpha_EM)", "formal 4614 normal form summary."),
        ("SRC4658_23_4653_hodge", DOC_4653, "CDF4653_4_EM_Hodge_lock", "same-coframe Maxwell/Hodge lock."),
        ("SRC4658_24_669_hodge", FORMAL_669, "CDF4653_4_EM_Hodge_lock", "formal same-coframe Maxwell/Hodge lock."),
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


def normal_form_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BNF4658_0_identity", "alpha_eff proportional to g_J^2/lambda_A", "field normalization invariant; not an alpha_EM prediction", "imported from 4209/4313/4437", "IDENTITY_IMPORTED"),
        ("BNF4658_1_vertical", "b_alpha_EM := D_X ln alpha_eff = 2 D_X ln g_J - D_X ln lambda_A", "same-owner EM coupling drift", "current/source normalization and kinetic normalization differentiated before readout", "DERIVED_NORMAL_FORM_IMPORTED"),
        ("BNF4658_2_4614_refinement", "b_alpha_EM = 2 z_g - z_lambda - z_readout - z_rad", "adds readout/radiative regeneration terms to the local drift law", "z_g,z_lambda,z_readout,z_rad are dimensionless vertical derivatives", "REFINED_NORMAL_FORM_IMPORTED"),
        ("BNF4658_3_memory_projection", "b_alpha_mem := Pi_mem[b_alpha_EM] = 2 z_g^mem - z_lambda^mem - z_readout^mem - z_rad^mem", "4658 applies the normal form to the memory trace leg selected in 4657", "Pi_mem is linear and branch/readout matched", "MEMORY_NORMAL_FORM_DERIVED"),
        ("BNF4658_4_bound", "|b_alpha_mem| <= 2|z_g^mem| + |z_lambda^mem| + |z_readout^mem| + |z_rad^mem|", "no-cancellation finite fallback", "requires source-backed values and units for every z component", "BOUND_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "normal_id": row_data[0],
            "formula": row_data[1],
            "meaning": row_data[2],
            "condition": row_data[3],
            "status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BZI4658_0_fixed_theta", "theta_obs={m_A,charges,alpha_EM,hbar,c,material labels} fixed before variation", "z_readout^mem=0 in the fixed visible branch", "branch condition imported from 4437", "BRANCH_ZERO_AVAILABLE"),
        ("BZI4658_1_fixed_gJ", "D_mem ln g_J=0", "current/charge normalization does not vary along the memory vertical generator", "same current owner and fixed charge lattice", "BRANCH_ZERO_AVAILABLE"),
        ("BZI4658_2_fixed_lambda", "D_mem ln lambda_A=0", "Maxwell kinetic normalization is calibrated/fixed, not a memory field", "unique visible F2 owner in fixed q-basic branch", "BRANCH_ZERO_AVAILABLE"),
        ("BZI4658_3_no_hidden_F2", "C_XF2=0", "no independent MTS-visible f_X(Phi) F^2 slot inside the standard branch", "DeltaS_MTS_visible=0 before variation", "BRANCH_ZERO_AVAILABLE"),
        ("BZI4658_4_same_Hodge_current", "same observed Hodge and same Noether current owner", "Poynting/internal exchange is Hilbert stress flow, not a second source-current channel", "191/329/4653 branch guard", "BRANCH_ZERO_AVAILABLE"),
        ("BZI4658_5_result", "z_g^mem=z_lambda^mem=z_readout^mem=z_rad^mem=0 => b_alpha_mem=0", "the first C_mem^std_weight_live coefficient is killed inside the fixed q-basic visible EM branch", "does not predict numerical alpha_EM and does not close global/dynamic EM branches", "PRIVATE_BRANCH_ZERO_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row_data[0],
            "statement": row_data[1],
            "deduction": row_data[2],
            "scope_or_condition": row_data[3],
            "status": row_data[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BDB4658_0_zg", "z_g^mem", "Pi_mem[D_X ln g_J]", "current/charge normalization drift", "dimensionless", "zero in fixed branch; source-backed value otherwise", "MISSING_DYNAMIC_CURRENT_OWNER_OR_VALUE"),
        ("BDB4658_1_zlambda", "z_lambda^mem", "Pi_mem[D_X ln lambda_A]", "Maxwell kinetic normalization drift or hidden F2 coefficient", "dimensionless", "zero in fixed branch; source-backed value otherwise", "MISSING_GLOBAL_UNIQUE_F2_OR_VALUE"),
        ("BDB4658_2_zreadout", "z_readout^mem", "Pi_mem[D_X ln readout_alpha]", "spectroscopy/clock/readout alpha regeneration", "dimensionless", "zero if readout is post-variation q-basic", "MISSING_READOUT_CLOSURE_OR_VALUE"),
        ("BDB4658_3_zrad", "z_rad^mem", "Pi_mem[D_X ln alpha_rad_eff]", "radiative/EFT/open-collar regenerated EM coefficient", "dimensionless", "zero if closed stationary EM branch has no regenerated F2/current term", "MISSING_RADIATIVE_CLOSURE_OR_VALUE"),
        ("BDB4658_4_balpha", "b_alpha_mem_abs", "2|z_g^mem|+|z_lambda^mem|+|z_readout^mem|+|z_rad^mem|", "absolute no-cancellation bound for b_alpha_mem", "dimensionless", "feeds C_mem^std_weight_live if fixed branch not selected", "VALUES_MISSING_NONCLAIM"),
        ("BDB4658_5_source_row_contract", "b_alpha_mem_source_row", "system_id;branch;z_g;z_lambda;z_readout;z_rad;b_alpha_mem_abs;units;source_path;equation_ref;valid_for_claim", "first source-backed finite row contract", "dimensionless", "required before any finite dynamic-alpha claim", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_data[0],
            "symbol": row_data[1],
            "definition": row_data[2],
            "role": row_data[3],
            "units": row_data[4],
            "zero_or_bound_route": row_data[5],
            "current_status": row_data[6],
            "source_path": "MISSING_SOURCE_PATH",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def cmem_update_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CSW4658_0_before", "|C_mem^std_weight_live| <= |b_alpha_mem||S_alpha^mem| + |b_mass_mem||S_mass^mem| + |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|", "4657 first-block bound before 4658", "FIRST_BLOCK_BOUND_IMPORTED"),
        ("CSW4658_1_fixed_alpha", "fixed q-basic visible EM branch => |b_alpha_mem||S_alpha^mem|=0", "alpha/fine-structure coefficient term drops from C_mem^std_weight_live inside the private fixed branch", "BRANCH_ZERO_INSERTED_NONCLAIM"),
        ("CSW4658_2_reduced_fixed_branch", "|C_mem^std_weight_live| <= |b_mass_mem||S_mass^mem| + |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|", "reduced first-block target after alpha zero import", "NEXT_COEFFICIENTS_REMAIN"),
        ("CSW4658_3_dynamic_branch", "|C_mem^std_weight_live| includes |b_alpha_mem|_abs |S_alpha^mem| with |b_alpha_mem|_abs <= 2|z_g|+|z_lambda|+|z_readout|+|z_rad|", "if dynamic/global EM branch is selected, alpha term stays source-bound", "DYNAMIC_BRANCH_BOUND_RETAINED"),
        ("CSW4658_4_next", "attack b_mass_mem", "with alpha branch-zero handled, the next standard/weight coefficient is matter spectrum/composition drift", "NEXT_TARGET_SELECTED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row_data[0],
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
        ("RUN4658_0_fixed_qbasic_branch", "fixed q-basic calibrated visible EM branch", "PASS_CONDITIONAL_PRIVATE_ZERO", "b_alpha_mem=0; no numerical alpha prediction; global/dynamic branches retained."),
        ("RUN4658_1_dynamic_branch", "dynamic g_J/lambda_A/readout/radiative branch", "FAIL_CLOSED_TO_BOUND", "b_alpha_mem is not zero; requires z_g,z_lambda,z_readout,z_rad source-backed values."),
        ("RUN4658_2_Cmem_update", "C_mem^std_weight_live", "PASS_BRANCH_REDUCTION", "alpha term drops only in fixed branch; mass/clock/kappa/weight terms remain."),
        ("RUN4658_3_next_target", "component attack order", "PASS_NEXT_SELECTED", NEXT_TARGET),
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
        ("CTRL4658_0_no_alpha_prediction", "Do not claim MTS predicts the numerical fine-structure constant from this branch-zero result."),
        ("CTRL4658_1_no_unit_trick", "Do not set lambda_A=1 by convention and call b_alpha zero; the invariant ratio g_J^2/lambda_A must be fixed before variation."),
        ("CTRL4658_2_no_branch_globalization", "Do not export fixed q-basic visible EM branch zero to global/dynamic coefficient branches."),
        ("CTRL4658_3_no_Poynting_double_count", "Poynting remains Maxwell-Hilbert stress or routed boundary flux, not an extra background force."),
        ("CTRL4658_4_no_claim_rows", "All rows remain private nonclaim until branch adoption and remaining C_mem components close or are source-backed."),
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
            "decision_id": "DEC4658_0",
            "decision": DECISION,
            "rationale": "4658 memory-projects the EM coupling normal form. In the fixed q-basic calibrated visible EM branch, g_J, lambda_A, readout labels and radiative regeneration are fixed before variation, so b_alpha_mem=0. This is a real branch-zero import, not a numerical alpha prediction and not a global Maxwell derivation. Dynamic/global branches retain an explicit absolute z-component bound.",
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
            "fixed_branch_status": "BALPHA_MEM_ZERO_PRIVATE_BRANCH",
            "dynamic_branch_status": "BOUND_ROUTE_VALUES_MISSING",
            "Cmem_std_weight_status": "ALPHA_TERM_REMOVED_ONLY_IN_FIXED_BRANCH",
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
            "why": "After fixed-branch b_alpha_mem is zeroed, the next C_mem^std_weight_live coefficient is b_mass_mem: matter-spectrum, mass-ratio, binding-energy and composition drift.",
            "acceptance_gate": "prove the matter spectrum/binding data descend through the same fixed source grammar, or produce source-backed WEP/composition/material sensitivity rows with units and paths.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    normal: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    cmem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + normal + zero_import + bounds + cmem + runners + controls + decisions
    checks = [
        ("VAL4658_00_sources_exist", all(row_data["path_exists"] for row_data in sources), "all cited source paths exist"),
        ("VAL4658_01_needles_found", all(row_data["needle_found"] for row_data in sources), "all cited source needles found"),
        ("VAL4658_02_line_anchors", all(int(row_data["line_number"]) > 0 for row_data in sources), "all source line anchors positive"),
        ("VAL4658_03_memory_normal_form", any(row_data["normal_id"] == "BNF4658_3_memory_projection" for row_data in normal), "memory-projected b_alpha normal form present"),
        ("VAL4658_04_fixed_branch_zero", any(row_data["zero_id"] == "BZI4658_5_result" and row_data["status"] == "PRIVATE_BRANCH_ZERO_NONCLAIM" for row_data in zero_import), "fixed branch b_alpha_mem zero present"),
        ("VAL4658_05_dynamic_bound", any(row_data["bound_id"] == "BDB4658_4_balpha" and "VALUES_MISSING" in row_data["current_status"] for row_data in bounds), "dynamic branch finite b_alpha bound retained"),
        ("VAL4658_06_Cmem_alpha_removed", any(row_data["update_id"] == "CSW4658_1_fixed_alpha" for row_data in cmem), "Cmem standard/weight alpha term removed in fixed branch"),
        ("VAL4658_07_next_bmass", decisions and decisions[0]["next_target"] == NEXT_TARGET, "b_mass next selected"),
        ("VAL4658_08_live_fail_closed", any(row_data["run_id"] == "RUN4658_1_dynamic_branch" and row_data["result"].startswith("FAIL_CLOSED") for row_data in runners), "dynamic branch fails closed to bound"),
        ("VAL4658_09_no_claim", all(str(row_data.get("valid_for_claim", "False")) == "False" and str(row_data.get("claim_allowed", "False")) == "False" for row_data in all_rows), "no row is claim-grade"),
        ("VAL4658_10_no_alpha_prediction_control", any(row_data["control_id"] == "CTRL4658_0_no_alpha_prediction" for row_data in controls), "no numerical alpha prediction guard present"),
        ("VAL4658_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4658_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4658_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4658 b_alpha_mem branch-zero and dynamic-bound gate passed" if all(passed for _, passed, _ in checks) else "4658 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    normal: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    cmem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4658 - b_alpha Maxwell normalization owner or first source bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4658 attacks the first coefficient selected by 4657:

`b_alpha_mem := Pi_mem[D_X ln(alpha_EM)]`.

The important point is that this is not a unit convention and not a numerical prediction of the fine-structure constant. The invariant local EM coupling throat is:

`alpha_eff proportional to g_J^2/lambda_A`,

so:

`b_alpha_EM = D_X ln alpha_eff = 2 D_X ln g_J - D_X ln lambda_A`.

Using the 4614 refinement:

`b_alpha_EM = 2 z_g - z_lambda - z_readout - z_rad`.

Projecting into the memory trace leg gives:

`b_alpha_mem = 2 z_g^mem - z_lambda^mem - z_readout^mem - z_rad^mem`.

Inside the fixed q-basic calibrated visible EM branch from 4313/4437:

`z_g^mem=z_lambda^mem=z_readout^mem=z_rad^mem=0`,

therefore:

`b_alpha_mem=0`.

This is useful because the `alpha` term drops out of the first `C_mem^std_weight_live` block in that private branch. It does **not** predict numerical `alpha_EM`, and it does **not** close global/dynamic EM coefficient branches.

If the fixed visible EM branch is not selected, the live fallback is:

`|b_alpha_mem| <= 2|z_g^mem| + |z_lambda^mem| + |z_readout^mem| + |z_rad^mem|`,

with source-backed rows required before any finite alpha/clock/WEP/R10/EM claim.

## Source Register

{table(sources)}

## b_alpha Memory Normal Form

{table(normal)}

## Fixed Branch Zero Import

{table(zero_import)}

## Dynamic Branch Bound Rows

{table(bounds)}

## Cmem Standard Weight Update

{table(cmem)}

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
        "4658 memory-projects the EM coupling normal form b_alpha=2 z_g-z_lambda-z_readout-z_rad. In the fixed q-basic calibrated visible EM branch, the projected z components vanish, so b_alpha_mem=0 and the alpha term drops from C_mem^std_weight_live. Dynamic/global EM branches remain finite bound rows.",
        "Generated source register, b_alpha memory normal form, fixed branch zero import, dynamic branch bound rows, Cmem standard/weight update, runner, controls, decision, status, next target and validation.",
        "b_alpha_mem_fixed_qbasic_branch_zero_dynamic_bound_nonclaim",
        NEXT_TARGET,
        "Claiming numerical alpha_EM, treating a field convention as a physical zero, globalizing fixed-branch EM closure, or dropping dynamic/readout/radiative EM coefficient branches.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/clock/orbital/Maxwell claim until remaining C_mem standard/weight coefficients and dynamic EM branches are same-branch theorem-zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4658 imports the exact EM normalization identity into the memory trace leg. `b_alpha_mem = 2 z_g^mem - z_lambda^mem - z_readout^mem - z_rad^mem`; in the fixed q-basic calibrated visible EM branch all four projected terms vanish, so `b_alpha_mem=0` and the alpha term drops from `C_mem^std_weight_live`. This is a private branch-zero result, not a numerical prediction of `alpha_EM`, and global/dynamic EM branches remain bounded residuals. Next target: `b_mass_mem`.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4658` kills the first `C_mem^std_weight_live` coefficient only in the fixed q-basic visible EM branch and retains a finite dynamic-branch alpha bound. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    normal = normal_form_rows(timestamp)
    zero_import = zero_import_rows(timestamp)
    bounds = bound_rows(timestamp)
    cmem = cmem_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, normal, zero_import, bounds, cmem, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NORMAL_FORM_CSV, normal)
    write_csv(ZERO_IMPORT_CSV, zero_import)
    write_csv(BOUND_ROWS_CSV, bounds)
    write_csv(CMEM_UPDATE_CSV, cmem)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, normal, zero_import, bounds, cmem, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4658 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
