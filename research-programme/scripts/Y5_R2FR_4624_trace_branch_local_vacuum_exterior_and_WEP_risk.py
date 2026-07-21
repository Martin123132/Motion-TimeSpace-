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

CHECKPOINT = "4624"
CLAIM_ID = "L-466"
BRANCH_ID = "MTS_R2FR_Y5_TRACE_BRANCH_EXTERIOR_WEP_GATE_4624"
MARKER = "PPC4161_TRACE_BRANCH_LOCAL_VACUUM_EXTERIOR_AND_WEP_RISK_4624"
PACKET_MARKER = "PPC4161_PACKET_TRACE_BRANCH_EXTERIOR_WEP_GATE_4624"
DECISION = "TRACE_BRANCH_EXTERIOR_HOMOGENEOUS_BUT_BOUNDARY_CHARGE_OR_YUKAWA_SCREENING_REQUIRED_NONCLAIM"
NEXT_TARGET = "4625-Y5-R2FR-trace-charge-zero-screening-or-yukawa-bound-row.md"

DOC_PATH = POST / "4624-Y5-R2FR-trace-branch-local-vacuum-exterior-and-WEP-risk.md"
FORMAL_PATH = FORMAL / "640-PPC4161-trace-branch-local-vacuum-exterior-and-WEP-risk.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4624_SOURCE_REGISTER.csv"
EXTERIOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_TRACE_EXTERIOR_THEOREM_ROWS.csv"
YUKAWA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_TRACE_YUKAWA_PROFILE_ROWS.csv"
WEP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_WEP_RESIDUAL_VECTOR_ROWS.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_LOCAL_GR_GATES.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4624_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4624_VALIDATION.csv"

CSV_4623_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4623_NEXT_TARGET.csv"
CSV_4623_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4623_PARENT_SELECTION_THEOREMS.csv"
CSV_4623_TRACE = SOURCE_DIR / "P8_Y5_R2FR_4623_TRACE_BRANCH_ROWS.csv"
CSV_4623_BETA = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"
CSV_4623_FRAME = SOURCE_DIR / "P8_Y5_R2FR_4623_FRAME_DEGENERACY_CONTROLS.csv"
CSV_4623_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4623_VALIDATION.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4622_LOCAL = SOURCE_DIR / "P8_Y5_R2FR_4622_LOCAL_VACUUM_BRANCH_TESTS.csv"

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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
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


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4624_00_4623_next", CSV_4623_NEXT, "4624-Y5-R2FR-trace-branch-local-vacuum-exterior-and-WEP-risk.md", "4623 selected trace branch exterior/WEP gate."),
        ("SRC4624_01_4623_trace_theorem", CSV_4623_THEOREM, "PSEL4623_1_trace_branch", "4623 trace branch theorem."),
        ("SRC4624_02_4623_trace_row", CSV_4623_TRACE, "TR4623_0_minimal_trace_branch", "4623 minimal trace branch row."),
        ("SRC4624_03_4623_exterior", CSV_4623_TRACE, "TR4623_2_exterior_nohair_feed", "4623 exterior nohair feed row."),
        ("SRC4624_04_4623_betaT", CSV_4623_BETA, "BOWN4623_1_beta_T", "4623 beta_T owner row."),
        ("SRC4624_05_4623_frame", CSV_4623_FRAME, "FR4623_0_no_R_T_double_count", "4623 frame control."),
        ("SRC4624_06_4623_validation", CSV_4623_VALIDATION, "VAL4623_OVERALL", "4623 validation."),
        ("SRC4624_07_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 nohair theorem."),
        ("SRC4624_08_4621_bound", CSV_4621_IDENTITY, "MPI4621_3_finite_amplitude_bound", "4621 finite amplitude bound."),
        ("SRC4624_09_4621_Zmem", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "4621 Zmem lower row."),
        ("SRC4624_10_4621_M2mem", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "4621 M2mem lower row."),
        ("SRC4624_11_4622_exterior", CSV_4622_LOCAL, "LVT4622_0_exterior_vacuum", "4622 exterior vacuum branch test."),
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


def exterior_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EXT4624_0_exterior_homogeneous",
            "statement": "In the trace-only branch, outside compact matter with T_obs=0 and R_obs=0, the local memory equation is homogeneous: (-Z_mem nabla^2 + M2_mem) delta_m = 0.",
            "derivation": "4623 removes independent EM/Poynting/wave sources in the trace-only branch. Exterior vacuum sets the trace/curvature source to zero.",
            "result": "HOMOGENEOUS_EXTERIOR_EQUATION",
            "claim_gap": "homogeneous does not mean zero unless boundary/scalar charge is zero or screened",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EXT4624_1_boundary_charge_warning",
            "statement": "A compact body with nonzero interior trace coupling can induce a boundary scalar charge Q_mem, so exterior delta_m may be Yukawa rather than zero.",
            "derivation": "Integrating the sourced interior equation across the body gives a boundary flux for the exterior homogeneous equation.",
            "result": "VACUUM_PLATEAU_NOT_AUTOMATIC",
            "claim_gap": "need Q_mem=0, screening, large M2_mem, or empirical Yukawa bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EXT4624_2_exact_zero_gate",
            "statement": "The trace branch gives Delta_v m_mem=0 in exterior only if the interior trace charge and boundary flux vanish, or if the selected domain boundary condition fixes delta_m=0.",
            "derivation": "This is the 4621 no-hair theorem applied to the exterior domain with explicit boundary terms retained.",
            "result": "EXACT_CONDITIONAL_LOCAL_GR_SUPPRESSION_GATE",
            "claim_gap": "boundary/scalar charge zero not yet parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def yukawa_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "YUK4624_0_spherical_exterior",
            "assumptions": "static spherical exterior, constant positive Z_mem and M2_mem, homogeneous exterior equation",
            "profile": "delta_m(r) = Q_mem exp(-r/lambda_mem)/(4*pi Z_mem r)",
            "definitions": "lambda_mem = sqrt(Z_mem/M2_mem); Q_mem is the body scalar charge/boundary flux",
            "local_gr_limit": "Q_mem=0 or r/lambda_mem large enough that the profile is negligible",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "YUK4624_1_trace_charge",
            "assumptions": "weak trace branch and compact body source",
            "profile": "Q_mem approx integral_body beta_T T_obs dV plus frame-equivalent curvature bookkeeping",
            "definitions": "composition dependence enters through beta_T species or binding-energy dependence",
            "local_gr_limit": "universal tiny beta_T, screened beta_T, or zero trace charge",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "profile_id": "YUK4624_2_newtonian_residual",
            "assumptions": "test body A has scalar sensitivity alpha_A = partial_m ln m_A",
            "profile": "a_mem,A = -alpha_A grad(delta_m_source)",
            "definitions": "relative to Newtonian acceleration, residual scales like alpha_A Q_source exp(-r/lambda)(1+r/lambda)/(4*pi Z_mem G M_source)",
            "local_gr_limit": "residual below PPN/WEP/orbital bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def wep_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "wep_id": "WEP4624_0_universal_trace",
            "case": "universal beta_T and universal test-body sensitivity",
            "residual": "composition-independent scalar acceleration can mimic a Yukawa correction to G rather than a WEP violation",
            "risk": "still constrained by inverse-square, orbital, PPN and local-G variation tests",
            "needed_input": "beta_T, Q_source, Z_mem, M2_mem, lambda_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "wep_id": "WEP4624_1_species_dependent_trace",
            "case": "species/composition-dependent beta_T or alpha_A",
            "residual": "eta_AB approximately (alpha_A-alpha_B) Q_source exp(-r/lambda)(1+r/lambda)/(4*pi Z_mem g r^2)",
            "risk": "direct WEP/Eotvos failure unless difference is zero, screened, or bounded",
            "needed_input": "composition sensitivities alpha_A, alpha_B and source scalar charge",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "wep_id": "WEP4624_2_screened_or_massive",
            "case": "large M2_mem or environmental screening",
            "residual": "Yukawa profile suppressed by exp(-r/lambda_mem) or by small effective Q_mem",
            "risk": "screening itself needs parent derivation, not a closure patch",
            "needed_input": "parent potential/gap and screening law",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def gate_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "GATE4624_0_exact_GR_exterior", "condition": "trace-only branch + positive operator + Q_mem=0 + boundary flux zero", "result_if_closed": "Delta_v m_mem=0 exterior and memory branch does not perturb local GR", "status": "BOUNDARY_CHARGE_UNSIGNED", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "GATE4624_1_yukawa_bound", "condition": "Q_mem finite and lambda_mem finite with residual below inverse-square/WEP/orbital bounds", "result_if_closed": "local GR recovered empirically as a bounded short-range/weak scalar correction", "status": "NUMERIC_SOURCE_ROWS_MISSING", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "GATE4624_2_trace_screening", "condition": "parent derives universal trace decoupling or environmental screening without composition leakage", "result_if_closed": "matter interior source does not leak unacceptable exterior force", "status": "PARENT_SCREENING_MISSING", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4624_0_vacuum_not_zero", "rule": "Do not equate exterior homogeneous equation with zero field; boundary scalar charge must be killed or bounded.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4624_1_wep_not_optional", "rule": "Any trace coupling to matter must feed a WEP/inverse-square/orbital residual vector.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4624_2_screening_parent_owned", "rule": "Screening or large mass gap must be parent-derived/source-backed, not inserted as closure.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4624_0_Qmem", "blocks": "exact exterior local-GR suppression", "missing": "Q_mem=0 proof or source-backed scalar charge value", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4624_1_lambda", "blocks": "Yukawa suppression claim", "missing": "Z_mem, M2_mem and lambda_mem values/bounds", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4624_2_composition", "blocks": "WEP safety", "missing": "universal vs species-dependent beta_T and test-body sensitivities", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4624_0_exact_zero", "promotion_condition": "Prove Q_mem=0 and zero boundary flux on trace branch, with 4621 positivity.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4624_1_empirical_yukawa", "promotion_condition": "Provide Q_mem, lambda_mem, alpha_A/B and compare to inverse-square/WEP/orbital bounds.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "decision_id": "DEC4624_0", "decision": DECISION, "meaning": "Trace-only is still the best low-scrutiny path, but exterior vacuum only makes the equation homogeneous; local GR needs scalar charge zero, screening, or Yukawa bounds.", "status": "NONCLAIM_PRIVATE_DERIVATION_STAGE", "best_route": "derive Q_mem=0 or parent screening; fallback to source-backed Yukawa/WEP bound rows", "next_target": NEXT_TARGET, "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now}
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE", "summary": "Trace branch exterior equation, Yukawa profile and WEP residual vector derived; exact local-GR suppression now requires Q_mem zero or bound.", "valid_for_claim": False, "claim_allowed": False, "next_target": NEXT_TARGET, "timestamp_utc": now}
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "timestamp_utc": now, "next_target": NEXT_TARGET, "reason": "The next live unknown is the body scalar charge or screening/gap that suppresses the exterior Yukawa profile.", "derive_first": "Q_mem=0 or screening from parent trace branch", "fallback": "finite Yukawa/WEP source-backed bound row", "valid_for_claim": False}
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4624 - Trace Branch Local Vacuum Exterior And WEP Risk",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4624 tests the clean trace-only route against the thing that can quietly kill it: exterior vacuum makes the memory equation homogeneous, but it does **not** automatically make the memory field zero.",
        "",
        "Trace-only exterior equation:",
        "",
        "`(-Z_mem nabla^2 + M2_mem) delta_m = 0` outside compact matter, when `T_obs=0`, `R_obs=0`, and independent EM/Poynting/wave owners are absent.",
        "",
        "But a compact body can still source a boundary scalar charge:",
        "",
        "`delta_m(r) = Q_mem exp(-r/lambda_mem)/(4*pi Z_mem r)`, with `lambda_mem = sqrt(Z_mem/M2_mem)`.",
        "",
        "So the local-GR route is now precise: prove `Q_mem=0`, derive screening/large mass gap, or carry a finite Yukawa/WEP residual bound.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Exterior Theorem Rows",
        markdown_table(tables["exterior"]),
        "",
        "## Yukawa Profile Rows",
        markdown_table(tables["yukawa"]),
        "",
        "## WEP Residual Vector Rows",
        markdown_table(tables["wep"]),
        "",
        "## Local-GR Gates",
        markdown_table(tables["gates"]),
        "",
        "## Controls",
        markdown_table(tables["controls"]),
        "",
        "## Blockers",
        markdown_table(tables["blockers"]),
        "",
        "## Promotion Gates",
        markdown_table(tables["promotion"]),
        "",
        "## Decision",
        markdown_table(tables["decision"]),
        "",
        "## Status",
        markdown_table(tables["status"]),
        "",
        "## Next Target",
        markdown_table(tables["next"]),
        "",
        "## Claim Safety",
        "",
        "All rows remain `valid_for_claim=false`. This checkpoint improves the derivation by preventing a fake local-vacuum plateau claim.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 640 - PPC4161 Trace Branch Local Vacuum Exterior And WEP Risk

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Exterior Trace Branch

In the trace-only branch, exterior vacuum gives:

`(-Z_mem nabla^2 + M2_mem) delta_m = 0`.

For a static spherical exterior with constant positive coefficients:

`delta_m(r) = Q_mem exp(-r/lambda_mem)/(4*pi Z_mem r)`,

where `lambda_mem = sqrt(Z_mem/M2_mem)`.

Thus exterior local GR is exact only if `Q_mem=0` or boundary flux vanishes; otherwise it is a Yukawa/fifth-force bound problem. The residual acceleration of a test body A scales as:

`a_mem,A = -alpha_A grad(delta_m_source)`.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4624 derives that trace-only exterior vacuum is homogeneous but not automatically zero, requiring scalar charge zero, screening, or Yukawa/WEP bounds.",
        "current_evidence": "Generated exterior theorem rows, Yukawa profile rows, WEP residual vector, local-GR gates, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "trace_branch_exterior_yukawa_gate_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Smuggling local-GR recovery by treating exterior vacuum as zero-field despite possible body scalar charge.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/PPN/WEP pass until Q_mem, lambda_mem and composition sensitivities are derived or bounded.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4624_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, EXTERIOR_CSV, YUKAWA_CSV, WEP_CSV, GATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4624_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4624_02_homogeneous_not_zero", any(row["theorem_id"] == "EXT4624_1_boundary_charge_warning" for row in tables["exterior"]), "boundary charge warning present")
    add("VAL4624_03_yukawa_profile", any(row["profile_id"] == "YUK4624_0_spherical_exterior" for row in tables["yukawa"]), "Yukawa profile row present")
    add("VAL4624_04_wep_vector", any(row["wep_id"] == "WEP4624_1_species_dependent_trace" for row in tables["wep"]), "WEP residual row present")
    add("VAL4624_05_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4624_06_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4624_07_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4624_08_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4624_09_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4624_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4624_11_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4624_12_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4624_13_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4624_OVERALL", all(row["status"] == "PASS" for row in rows), "4624 trace branch exterior/WEP gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "exterior": exterior_rows(now),
        "yukawa": yukawa_rows(now),
        "wep": wep_rows(now),
        "gates": gate_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(EXTERIOR_CSV, tables["exterior"])
    write_csv(YUKAWA_CSV, tables["yukawa"])
    write_csv(WEP_CSV, tables["wep"])
    write_csv(GATE_CSV, tables["gates"])
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
## PPC4161 Local Addendum - Trace Branch Local Vacuum Exterior And WEP Risk

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4624 derives the trace-only exterior gate: vacuum makes the memory equation homogeneous, not automatically zero. A compact body can leave `delta_m(r)=Q_mem exp(-r/lambda_mem)/(4*pi Z_mem r)`. Exact local-GR suppression therefore needs `Q_mem=0`/zero boundary flux, parent screening/large gap, or a finite Yukawa/WEP bound.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Trace Branch Local Vacuum Exterior And WEP Risk

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now blocks fake exterior-vacuum closure. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4624 validation failed: {failed}")
    print(f"4624 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
