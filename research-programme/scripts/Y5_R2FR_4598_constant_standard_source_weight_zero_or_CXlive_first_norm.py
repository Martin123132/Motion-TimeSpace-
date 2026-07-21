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

CHECKPOINT = "4598"
CLAIM_ID = "L-440"
BRANCH_ID = "MTS_R2FR_Y5_CONSTANT_STANDARD_SOURCE_WEIGHT_GATE_4598"
MARKER = "PPC4161_CONSTANT_STANDARD_SOURCE_WEIGHT_ZERO_OR_CXLIVE_FIRST_NORM_4598"
PACKET_MARKER = "PPC4161_PACKET_CONSTANT_STANDARD_SOURCE_WEIGHT_ZERO_OR_CXLIVE_FIRST_NORM_4598"
DECISION = "CONSTANT_STANDARD_AND_SOURCE_WEIGHT_ZERO_OR_SENSITIVITY_NORM_INSERTED_NONCLAIM"
NEXT_TARGET = "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"

DOC_PATH = POST / "4598-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
FORMAL_PATH = FORMAL / "614-PPC4161-constant-standard-source-weight-zero-or-CXlive-first-norm.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4598_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_CONSTANT_WEIGHT_ZERO_THEOREM.csv"
SENSITIVITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_CX_STANDARD_WEIGHT_SENSITIVITY_BOUND.csv"
BODY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_BODY_CHARGE_ENVELOPE_STANDARD_WEIGHT_UPDATE.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_FIRST_CXLIVE_NORM_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4598_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4598_VALIDATION.csv"

DOC_4597 = POST / "4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"
FORMAL_613 = FORMAL / "613-PPC4161-Cmem-Ch-qbasic-source-descent-or-live-leakage-bound.md"
CSV_4597_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4597_NEXT_TARGET.csv"
CSV_4597_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv"
CSV_4597_BODY = SOURCE_DIR / "P8_Y5_R2FR_4597_BODY_CHARGE_ENVELOPE_CX_LIVE_UPDATE.csv"
CSV_4597_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4597_STATUS.csv"
CSV_3235_GATE = SOURCE_DIR / "P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv"
CSV_2689_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_2689_TOTAL_PARENT_ACTION_SOURCE_FUNCTOR_AUDIT.csv"
CSV_2763_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_2763_MATTER_SOURCE_FUNCTOR_CONTRACT_ATTEMPT.csv"
CSV_2648_CLAUSE = SOURCE_DIR / "P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_CLAUSE_AUDIT.csv"
CSV_2648_ATTEMPT = SOURCE_DIR / "P8_Y5_SOURCE_FUNCTOR_LABEL_FORGETTING_2648_LABEL_FORGETTING_ATTEMPT.csv"
CSV_1905_LINE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv"
CSV_1905_CONNECTED = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv"
CSV_KAPPA = SOURCE_DIR / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
CSV_1804_CONST = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_CONSTANT_SUPERSELECTION_GATE.csv"

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
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4598 reduces the C_X live matter-trace leakage to a constant/standard superselection gate plus a no-source-weight/action-line gate, or else to explicit sensitivity norms that enter A_mem/A_h without hiding in calibrated G.",
        "current_evidence": "Generated constant/source-weight zero theorem rows, C_X standard-weight sensitivity bounds, updated body-charge envelopes, first norm rows, controls and validation.",
        "status": "constant_standard_source_weight_zero_or_sensitivity_norm_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating fitted units, common G/GM calibration, Ward conservation, or ordinary Hilbert matter as proof that alpha/mass/clock/material standards and source weights cannot vary with the local memory/fibre direction.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until standard/weight/label/Hodge/support/readout/boundary/non-Hilbert rows are parent-zero or source-backed below arena bounds.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4598_00_4597_doc", DOC_4597, "constants/standards", "4597 selects standard/source-weight terms as next live C_X risk."),
        ("SRC4598_01_613_formal", FORMAL_613, "C_X^live", "formal C_X live leakage split."),
        ("SRC4598_02_4597_next", CSV_4597_NEXT, "4598-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md", "machine-readable 4597 handoff."),
        ("SRC4598_03_4597_coeff", CSV_4597_COEFF, "CX4597_0_std", "standard coefficient row."),
        ("SRC4598_04_4597_weight", CSV_4597_COEFF, "CX4597_1_weight", "source-weight coefficient row."),
        ("SRC4598_05_4597_body", CSV_4597_BODY, "CBU4597_0_memory", "A_mem/A_h C_live envelope source."),
        ("SRC4598_06_4597_status", CSV_4597_STATUS, "constant/source-weight", "4597 status missing constants/source weights."),
        ("SRC4598_07_3235_constant", CSV_3235_GATE, "NMG3235_2_constant_superselection", "constant/material standard superselection gate."),
        ("SRC4598_08_3235_weight", CSV_3235_GATE, "NMG3235_3_source_weight", "source-weight countermodel."),
        ("SRC4598_09_2689_prefactor", CSV_2689_AUDIT, "TPA2689_4_no_prefactor_package", "pre-action prefactor obstruction."),
        ("SRC4598_10_2689_line", CSV_2689_AUDIT, "TPA2689_6_connected_action_line", "connected action-density line conditional theorem."),
        ("SRC4598_11_2689_common", CSV_2689_AUDIT, "TPA2689_8_common_coupling_owner", "common coupling owner guard."),
        ("SRC4598_12_2763_pullback", CSV_2763_CONTRACT, "MFC2763_0_matter_pullback", "matter functor fixed constants clause."),
        ("SRC4598_13_2763_counter", CSV_2763_CONTRACT, "MFC2763_3_counterexample", "shadow/source counterexample."),
        ("SRC4598_14_2648_prefactor", CSV_2648_CLAUSE, "LFA2648_1_no_prefactors", "no pre-action prefactor clause."),
        ("SRC4598_15_2648_calibration", CSV_2648_CLAUSE, "LFA2648_4_projected_mass_calibration", "common calibration guard."),
        ("SRC4598_16_2648_attempt", CSV_2648_ATTEMPT, "SFL2648_4_preaction_prefactor_obstruction", "source-weight leak attempt."),
        ("SRC4598_17_1905_line", CSV_1905_LINE, "ADL1905_0_line_owner", "action-density line owner gate."),
        ("SRC4598_18_1905_naturality", CSV_1905_CONNECTED, "CMC1905_1_naturality", "connected naturality collapse theorem."),
        ("SRC4598_19_kappa_global", CSV_KAPPA, "T508_0_global_sector", "global/superselection kappa route."),
        ("SRC4598_20_kappa_top", CSV_KAPPA, "T508_1_topological_zeroform", "topological zero-form route."),
        ("SRC4598_21_1804_const", CSV_1804_CONST, "CSG1804_0_exact_criterion", "constant vertical silence criterion."),
        ("SRC4598_22_1804_units", CSV_1804_CONST, "CSG1804_1_no_unit_rescaling_cheat", "dimensionless observable guard."),
        ("SRC4598_23_1804_alpha", CSV_1804_CONST, "CSG1804_2_alpha_EM", "alpha_EM coefficient gate."),
        ("SRC4598_24_1804_mass", CSV_1804_CONST, "CSG1804_3_mass_ratios", "mass ratio coefficient gate."),
        ("SRC4598_25_1804_clock", CSV_1804_CONST, "CSG1804_4_clock_constants", "clock constant coefficient gate."),
        ("SRC4598_26_claim_439", CLAIMS_PATH, "L-439", "claim-register handoff from 4597."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": False,
            }
        )
    return rows


def zero_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZW4598_0_constants",
            "target": "C_X^std",
            "zero_branch": "theta_i are quotient-owned, discrete, global/superselection, or topological zero-form constants; Dq[v_X]=0; no readout/unit rescaling cheat",
            "formula": "D_X ln(theta_i)=0 => C_X^std=0",
            "finite_branch": "|C_X^std| <= sum_i |S_i^std| |D_X ln(theta_i)|",
            "status": "EXACT_CONDITIONAL_ZERO_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZW4598_1_source_weight",
            "target": "C_X^weight",
            "zero_branch": "one parent action-density line, connected ordinary matter category, no pre-action source prefactors w_A(X), no kappa_A(X) before variation, common calibration only after label/time/range/frame gates",
            "formula": "S_matter=sum_A S_A and F_src(T_total)=kappa_univ T_total => D_X w_A=D_X kappa_A=0 relative to the source functor",
            "finite_branch": "|C_X^weight T| <= sum_A |D_X ln w_A| |T_A| + sum_A |D_X ln kappa_A| |T_A|",
            "status": "EXACT_CONDITIONAL_ZERO_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZW4598_2_combined",
            "target": "C_X^std_weight",
            "zero_branch": "ZW4598_0 and ZW4598_1 pass in the same parent branch",
            "formula": "C_X^std_weight = C_X^std + C_X^weight = 0",
            "finite_branch": "|C_X^std_weight| <= |C_X^std| + |C_X^weight|",
            "status": "COMBINED_ZERO_OR_ABSOLUTE_BOUND_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def sensitivity_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("SB4598_0_alpha", "b_alpha_X", "D_X ln(alpha_EM)", "alpha_EM source/readout/Maxwell normalization drift", "alpha/EM clock/fine-structure source rows"),
        ("SB4598_1_mass", "b_mA_X,b_mu_X,b_nuc_X", "D_X ln(m_A/m_ref), D_X ln(mu), D_X ln(binding)", "composition and material mass-ratio drift", "WEP/composition/source charge rows"),
        ("SB4598_2_clock", "b_clock_i_X", "K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + ...", "clock standard drift", "clock/local time readout rows"),
        ("SB4598_3_material", "b_mat_X", "D_X ln(theta_material)", "material/preparation/domain standard drift", "material/domain source rows"),
        ("SB4598_4_weight", "delta_w_A_X", "D_X ln(w_A) or D_X ln(kappa_A/kappa_univ)", "relative source-weight prefactor drift", "WEP/source-label rows"),
        ("SB4598_5_total", "C_X^std_weight", "sum of standard and source-weight sensitivity channels", "first C_X_live norm contribution", "insert into A_mem/A_h"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "sensitivity_id": sid,
            "symbol": symbol,
            "definition": definition,
            "physical_channel": channel,
            "finite_bound": "source-backed value or zero certificate required; no bound inversion or fitted-G hiding",
            "observable_link": observable,
            "current_status": "VALUE_MISSING_NONCLAIM" if sid != "SB4598_5_total" else "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for sid, symbol, definition, channel, observable in rows
    ]


def body_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4598_0_Csplit",
            "target": "C_X live after 4598",
            "formula": "C_X^post4598 = C_X^std_weight_live + C_X^label + C_X^Hodge + C_X^support_readout + C_X^boundary + C_X^nonHilbert",
            "zero_condition": "C_X^std_weight_live=0 only if constants/standards are superselected and source weights/prefactors are illegal in the same parent branch",
            "finite_bound": "|C_X^post4598| <= |C_X^std_weight_live|+|C_X^label|+|C_X^Hodge|+|C_X^support_readout|+|C_X^boundary|+|C_X^nonHilbert|",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4598_1_memory",
            "target": "A_mem",
            "formula": "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^post4598||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "zero_condition": "B_mem_eff=C_mem^post4598=J_mem_live=Q_boundary_mem=0",
            "finite_bound": "standards/source weights now enter through C_mem^std_weight_live, not hidden inside C_mem",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "BU4598_2_fibre",
            "target": "A_h",
            "formula": "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^post4598||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "zero_condition": "B_h=C_h^post4598=J_h_live=Q_boundary_h=0",
            "finite_bound": "standards/source weights now enter through C_h^std_weight_live, not hidden inside C_h",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CXN4598_0_alpha", "b_alpha_X", "fine-structure/Maxwell normalization drift", "prove unique Maxwell F^2/current owner and q-basic readout", "clock/EM/R10 sensitivity"),
        ("CXN4598_1_mass", "b_mass_X", "mass-ratio/binding/material mass drift", "prove matter spectrum and binding data are parent-owned/superselected", "WEP/composition/source charge sensitivity"),
        ("CXN4598_2_clock", "b_clock_X", "clock transition standard drift", "prove clock readout inherits zero from alpha/mass/nuclear and tau-lock", "clock/local time sensitivity"),
        ("CXN4598_3_kappa", "D_X ln(kappa_eff)", "universal source coupling drift", "global/topological zero-form kappa or common coupling owner", "Gdot/G/source calibration sensitivity"),
        ("CXN4598_4_weight", "D_X ln(w_A),D_X ln(kappa_A/kappa_univ)", "relative source weight drift", "no pre-action source prefactor and connected action-density line", "WEP/source-label sensitivity"),
        ("CXN4598_5_total", "C_X^std_weight_live", "combined first live norm", "all rows above theorem-zero in one branch", "A_mem/A_h numerator input"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": cid,
            "symbol": symbol,
            "role": role,
            "derive_first": derive,
            "finite_fallback": fallback,
            "current_status": "MISSING_PARENT_ZERO_OR_VALUE" if cid != "CXN4598_5_total" else "FIRST_NORM_ROW_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for cid, symbol, role, derive, fallback in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4598_superselected_constants",
            "input_branch": "all constants/standards quotient-owned or topological superselection",
            "expected": "C_X^std=0",
            "status": "SYMBOLIC_CONTROL_PASS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4598_alpha_drift",
            "input_branch": "alpha_EM or mass ratio varies with X",
            "expected": "C_X^std remains live and cannot be removed by unit convention",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4598_preaction_weight",
            "input_branch": "S_matter=sum_A w_A(X) S_A is allowed",
            "expected": "C_X^weight remains live even when Hilbert variation is well-defined",
            "status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4598_common_G_guard",
            "input_branch": "only a common G/GM calibration is known",
            "expected": "relative source weights and dimensionless constants cannot be hidden in common calibration",
            "status": "NO_FITTED_G_HIDING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4598_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4598_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4598_2_zero_or_norm",
            "claim": "constant/source-weight zero-or-norm theorem written",
            "passed": True,
            "detail": "C_X^std_weight is zero only under superselection plus no-prefactor/action-line gates; otherwise sensitivity rows remain",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4598_3_body_update",
            "claim": "A_mem/A_h envelopes use C_X^post4598",
            "passed": True,
            "detail": "standard/source-weight pieces now explicit inside body-charge numerator",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4598_4_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "detail": "no numeric standard/weight values or parent signatures complete",
            "valid_for_claim": False,
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
            "standard_zero_or_norm": True,
            "source_weight_zero_or_norm": True,
            "body_charge_envelope_updated": True,
            "parent_zero_or_numeric_bound_signed": False,
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
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
            "derived": "constant/standard superselection zero-or-sensitivity law; no-preaction-source-weight/action-line zero-or-norm law; C_X^post4598 and A_mem/A_h envelope update; first C_X_live norm rows",
            "not_derived": "parent-signed alpha/mass/clock/material/kappa superselection; parent-signed no source prefactors/action-density line; numeric sensitivity values; local-GR/R10/PPN scoring",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
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
            "reason": "After constants/source weights are isolated, the largest remaining C_X_live family is label/Hodge/support/readout re-entry.",
            "derive_first": "prove label forgetting plus same Maxwell-Hodge/current owner plus variation-before-readout in one parent branch",
            "fallback": "fill first finite C_X label/Hodge/support-readout norm row",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4598 Y5 R2FR constant-standard source-weight zero or C_X live first norm

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4598 attacks the first two live pieces in the `C_X` leakage vector from 4597:

```text
C_X^std        = standards/constants/material drift,
C_X^weight     = source-only action/source prefactor drift.
```

The standard/constant zero branch is:

```text
theta_i in quotient-owned, discrete, global/superselection, or topological-zero-form sector
and Dq[v_X]=0
=> D_X ln(theta_i)=0
=> C_X^std=0.
```

The source-weight zero branch is:

```text
S_matter=sum_A S_A,
one parent action-density line,
connected ordinary matter source category,
no w_A(X) S_A or kappa_A(X) T_A before variation
=> C_X^weight=0 up to one common calibration mode.
```

If either branch is not parent-signed, the finite row is:

```text
|C_X^std_weight| <= sum_i |S_i^std| |D_X ln(theta_i)|
                  + sum_A |D_X ln(w_A)| |T_A|/|T|
                  + sum_A |D_X ln(kappa_A/kappa_univ)| |T_A|/|T|.
```

This updates the live coupling to:

```text
C_X^post4598 = C_X^std_weight_live + C_X^label + C_X^Hodge
             + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

The memory/fibre envelopes now use `C_mem^post4598` and `C_h^post4598`, so standards and source weights are no longer hidden inside an undifferentiated `C_X`.

No local-GR, R10, PPN or orbital pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## Constant/Weight Zero Theorem

{markdown_table(tables["zero"])}

## C_X Standard/Weight Sensitivity Bound

{markdown_table(tables["sensitivity"])}

## Body-Charge Envelope Standard/Weight Update

{markdown_table(tables["body"])}

## First C_X Live Norm Rows

{markdown_table(tables["coefficients"])}

## Controls

{markdown_table(tables["controls"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

{markdown_table(tables["next"])}
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 614 - Constant/Standard Source-Weight Zero Or C_X Live First Norm

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For `X in {{m,h}}`,

```text
C_X^post4598 = C_X^std_weight_live + C_X^label + C_X^Hodge
             + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

The standard term vanishes only if every relevant `theta_i` is quotient-owned or superselected:

```text
D_X ln(theta_i)=0 => C_X^std=0.
```

The source-weight term vanishes only if pre-action source prefactors are illegal:

```text
S_matter=sum_A S_A, no w_A(X)S_A, no kappa_A(X)T_A => C_X^weight=0.
```

Otherwise `C_X^std_weight_live` is an explicit sensitivity norm and enters `A_mem/A_h`.

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL4598_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4598_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        SENSITIVITY_CSV,
        BODY_UPDATE_CSV,
        COEFFICIENT_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4598_02_csv_parse", csv_ok, ";".join(details))

    zero_text = "\n".join(str(row) for row in tables["zero"])
    add(
        "VAL4598_03_zero_theorem",
        "C_X^std=0" in zero_text and "D_X w_A=D_X kappa_A=0" in zero_text and "C_X^std_weight = C_X^std + C_X^weight = 0" in zero_text,
        "constant and source-weight zero branches written",
    )

    sensitivity_text = "\n".join(str(row) for row in tables["sensitivity"])
    add("VAL4598_04_sensitivity_rows", "b_alpha_X" in sensitivity_text and "delta_w_A_X" in sensitivity_text, "first sensitivity rows written")

    body_text = "\n".join(str(row) for row in tables["body"])
    add("VAL4598_05_body_update", "C_mem^post4598" in body_text and "C_h^post4598" in body_text, "A_mem/A_h use post4598 C_X")

    control_text = "\n".join(str(row) for row in tables["controls"])
    add("VAL4598_06_no_fitted_G_hiding", "NO_FITTED_G_HIDING" in control_text, "common G/GM calibration guard retained")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4598_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4598_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4598_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4598_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4598_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4598_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4598_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4598_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4598_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4598_OVERALL", all(row["status"] == "PASS" for row in rows), "4598 constant/source-weight zero-or-sensitivity gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "zero": zero_theorem_rows(now),
        "sensitivity": sensitivity_rows(now),
        "body": body_update_rows(now),
        "coefficients": coefficient_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(ZERO_THEOREM_CSV, tables["zero"])
    write_csv(SENSITIVITY_CSV, tables["sensitivity"])
    write_csv(BODY_UPDATE_CSV, tables["body"])
    write_csv(COEFFICIENT_CSV, tables["coefficients"])
    write_csv(CONTROL_CSV, tables["controls"])
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
## PPC4161 Local Addendum - Constant/Source-Weight C_X Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The `C_X` live matter-trace leakage vector is now narrowed again: constants/standards vanish only by quotient-owned/topological/superselection ownership, and source weights vanish only by a one-line parent action-density/no-prefactor theorem. Otherwise they enter `A_mem/A_h` as explicit sensitivity norms, with no fitted-G or unit-rescaling hiding.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Constant/Source-Weight C_X Norm

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now has standards/constants and source weights as concrete zero-or-norm rows inside the memory/fibre body-charge envelope. The next useful branch is label/Hodge/support-readout re-entry.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4598 validation failed: {failed}")
    print(f"4598 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
