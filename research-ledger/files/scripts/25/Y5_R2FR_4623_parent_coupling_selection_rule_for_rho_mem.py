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

CHECKPOINT = "4623"
CLAIM_ID = "L-465"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_COUPLING_SELECTION_RHOMEM_4623"
MARKER = "PPC4161_PARENT_COUPLING_SELECTION_RULE_FOR_RHOMEM_4623"
PACKET_MARKER = "PPC4161_PACKET_PARENT_COUPLING_SELECTION_RHOMEM_4623"
DECISION = "BETA_COUPLINGS_REDUCED_TO_PARENT_OWNERS_TRACE_BRANCH_KAPPA_LINK_OR_EXTRA_STRUCTURE_NONCLAIM"
NEXT_TARGET = "4624-Y5-R2FR-trace-branch-local-vacuum-exterior-and-WEP-risk.md"

DOC_PATH = POST / "4623-Y5-R2FR-parent-coupling-selection-rule-for-rho-mem.md"
FORMAL_PATH = FORMAL / "639-PPC4161-parent-coupling-selection-rule-for-rho-mem.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4623_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_PARENT_SELECTION_THEOREMS.csv"
BETA_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"
TRACE_BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_TRACE_BRANCH_ROWS.csv"
EM_LINK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_EM_COUPLING_LINK_ROWS.csv"
FRAME_CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_FRAME_DEGENERACY_CONTROLS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4623_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4623_VALIDATION.csv"

CSV_4622_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4622_NEXT_TARGET.csv"
CSV_4622_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4622_RHOMEM_CHANNEL_DECOMPOSITION.csv"
CSV_4622_EM = SOURCE_DIR / "P8_Y5_R2FR_4622_EM_POYNTING_ZERO_AND_BOUND_RULES.csv"
CSV_4622_COUPLING = SOURCE_DIR / "P8_Y5_R2FR_4622_COUPLING_COEFFICIENT_ROWS_NONCLAIM.csv"
CSV_4622_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4622_BOUND_FEED_ROWS.csv"
CSV_4622_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4622_VALIDATION.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4620_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv"
CSV_4620_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv"
CSV_4620_IMPACT = SOURCE_DIR / "P8_Y5_R2FR_4620_CMEMORY_BOUND_IMPACT_ROWS.csv"

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
        ("SRC4623_00_4622_next", CSV_4622_NEXT, "4623-Y5-R2FR-parent-coupling-selection-rule-for-rho-mem.md", "4622 selected parent coupling selection."),
        ("SRC4623_01_4622_betaF", CSV_4622_COUPLING, "COUP4622_2_beta_F", "4622 beta_F row."),
        ("SRC4623_02_4622_betaS", CSV_4622_COUPLING, "COUP4622_4_beta_S", "4622 beta_S/Poynting row."),
        ("SRC4623_03_4622_em", CSV_4622_DECOMP, "RDEC4622_2_em_invariant", "4622 EM invariant channel."),
        ("SRC4623_04_4622_poynting", CSV_4622_DECOMP, "RDEC4622_3_poynting", "4622 Poynting channel."),
        ("SRC4623_05_4622_wave", CSV_4622_DECOMP, "RDEC4622_4_wave_stress", "4622 wave channel."),
        ("SRC4623_06_4622_poynting_rule", CSV_4622_EM, "EMP4622_1_poynting_volume_to_boundary", "4622 Poynting theorem rule."),
        ("SRC4623_07_4622_static_em", CSV_4622_EM, "EMP4622_2_static_EM_not_zero", "4622 static EM warning."),
        ("SRC4623_08_4622_bound_feed", CSV_4622_BOUND, "BF4622_0_rho_norm", "4622 rho norm feed."),
        ("SRC4623_09_4622_validation", CSV_4622_VALIDATION, "VAL4622_OVERALL", "4622 validation."),
        ("SRC4623_10_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 no-hair theorem."),
        ("SRC4623_11_4620_kappa", CSV_4620_NUMERIC, "KNUM4620_0_first_numeric_template", "4620 kappa_memF2 row."),
        ("SRC4623_12_4620_zero", CSV_4620_ZERO, "KZ4620_0_typed_domain_zero", "4620 kappa zero route."),
        ("SRC4623_13_4620_impact", CSV_4620_IMPACT, "IM4620_0_Cmemory", "4620 C_memory impact."),
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


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_0_variational_owner",
            "statement": "Every rho_mem beta coefficient must be the m_mem derivative of a parent scalar-density coupling C_A(m_mem) O_A, evaluated on the selected branch.",
            "derivation": "rho_mem is the Euler-Lagrange source for delta_m. A source channel is therefore owned by the parent action term that varies with m_mem, not by a fitted residual row.",
            "consequence": "beta_A rows are not free knobs; each needs an owner or a zero theorem.",
            "status": "EXACT_SELECTION_REQUIREMENT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_1_trace_branch",
            "statement": "If m_mem enters matter only through a conformal metric/mass-scale factor, then rho_mem reduces to a trace source beta_T T_obs up to frame-equivalent curvature terms; null radiation and Maxwell trace do not source it directly.",
            "derivation": "Variation of a conformal matter metric gives delta S_matter proportional to T^a_a delta ln A(m). In four dimensions the Maxwell stress tensor is trace-free for the minimal kinetic term.",
            "consequence": "This is the least-scrutiny route for local vacuum: exterior T=0/R=0 gives rho_mem=0 unless independent gauge-kinetic, observer-flux, or wave-envelope couplings are present.",
            "status": "EXACT_CONDITIONAL_TRACE_BRANCH",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_2_betaF_kappa_link",
            "statement": "If the parent contains S_EM=-1/4 int Z_Q_eff(m_mem) F_Q^2, then beta_F is not independent: beta_F = +/- kappa_memF2/4 by convention.",
            "derivation": "Varying the Maxwell kinetic coefficient with respect to m_mem gives a source proportional to partial_m Z_Q_eff F_Q^2. 4620 names that derivative kappa_memF2.",
            "consequence": "The EM scalar-invariant source is killed by the 4620 kappa-zero routes or bounded by the same first numeric row; do not create a separate free beta_F.",
            "status": "EXACT_CONDITIONAL_EM_LINK",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_3_poynting_requires_observer_or_boundary",
            "statement": "A volume beta_S div S_EM term is not a parent-covariant scalar unless the parent action includes an observer/coframe/current structure; otherwise Poynting enters only as a boundary or finite flux row.",
            "derivation": "S_EM is an observer-relative energy flux. Without a parent observer field u^a or coframe theta, it is not an invariant scalar-density source for m_mem.",
            "consequence": "beta_S=0 as a volume coupling in the covariant no-observer branch; if theta/u exists, beta_S must be sourced and treated as boundary/absorption.",
            "status": "EXACT_CONDITIONAL_COVARIANCE_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_4_parity_betaG",
            "statement": "If m_mem and the parent branch are parity-even, the pseudoscalar beta_G F_Q starF_Q source is forbidden; it survives only with pseudoscalar memory or explicit parity/CP-odd parent structure.",
            "derivation": "F_Q starF_Q is parity odd. A parity-even scalar source action cannot contain m_mem F_Q starF_Q without breaking the branch parity assignment.",
            "consequence": "beta_G has a clean zero route that is stronger than fitting it away.",
            "status": "EXACT_CONDITIONAL_PARITY_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PSEL4623_5_frame_degeneracy",
            "statement": "beta_R R_obs and beta_T T_obs are frame-degenerate unless the parent frame is fixed; a nonminimal M_eff^2(m)R term can be traded for matter trace coupling after an Einstein-frame transformation.",
            "derivation": "The scalar-curvature coupling changes the effective gravitational scale. Moving to a fixed Einstein normalization shifts the m_mem dependence into matter scales and trace coupling.",
            "consequence": "Do not double-count beta_R and beta_T as independent local sources without a frame-owner row.",
            "status": "EXACT_FRAME_CONTROL",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def beta_matrix_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_0_beta_R",
            "symbol": "beta_R",
            "parent_owner": "nonminimal gravitational normalization M_eff^2(m_mem) R",
            "selection_rule": "Allowed only if parent chooses Jordan/nonminimal curvature owner; frame-degenerate with beta_T.",
            "derived_relation": "beta_R = +/- 1/2 partial_m M_eff^2 on the selected branch",
            "current_status": "OWNER_OR_FRAME_NOT_FIXED",
            "next_action": "choose frame owner or source partial_m M_eff^2",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_1_beta_T",
            "symbol": "beta_T",
            "parent_owner": "matter metric/mass-scale dependence A_m(m_mem) or particle mass derivative",
            "selection_rule": "Allowed in trace branch; exterior vacuum zero if T_obs=0, but inside matter and WEP tests remain live.",
            "derived_relation": "beta_T = partial_m ln A_m or species mass derivative sum, depending on normalization",
            "current_status": "TRACE_BRANCH_OWNER_POSSIBLE_VALUE_MISSING",
            "next_action": "derive universal vs species-dependent trace coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_2_beta_F",
            "symbol": "beta_F",
            "parent_owner": "Maxwell kinetic coefficient Z_Q_eff(m_mem)",
            "selection_rule": "Not independent from 4620 kappa_memF2; zero if typed-domain/no-Hom or extremum kills kappa_memF2.",
            "derived_relation": "beta_F = +/- kappa_memF2/4",
            "current_status": "TIED_TO_4620_KAPPA_MEMF2",
            "next_action": "use kappa_memF2 zero/numeric row, not a new beta_F fit",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_3_beta_G",
            "symbol": "beta_G",
            "parent_owner": "EM theta-like pseudoscalar coefficient theta_Q(m_mem) F_Q starF_Q",
            "selection_rule": "Forbidden on parity-even scalar branch; allowed only with pseudoscalar memory or explicit CP/parity-odd parent term.",
            "derived_relation": "beta_G = +/- partial_m theta_Q/4 if allowed",
            "current_status": "PARITY_OWNER_MISSING",
            "next_action": "assign m_mem parity and parent CP rule",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_4_beta_S",
            "symbol": "beta_S",
            "parent_owner": "observer/coframe flux functional or boundary action",
            "selection_rule": "Zero as a covariant volume scalar unless parent includes observer/coframe/current structure; otherwise finite boundary row.",
            "derived_relation": "no volume beta_S in no-observer branch; boundary coefficient if theta/u is parent-owned",
            "current_status": "VOLUME_COUPLING_REJECTED_CONDITIONALLY_BOUNDARY_OPEN",
            "next_action": "prove no parent observer flux owner or source boundary coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "beta_id": "BOWN4623_5_beta_gw",
            "symbol": "beta_gw",
            "parent_owner": "averaged wave stress/envelope coupling",
            "selection_rule": "Zero in pure trace/conformal branch for radiation-like trace-free stress; allowed only with observer energy-density/envelope owner.",
            "derived_relation": "beta_gw multiplies rho_gw_eff only if averaging map and observer/coframe are parent-owned",
            "current_status": "WAVE_ENVELOPE_OWNER_MISSING",
            "next_action": "derive trace branch zero or source wave-envelope coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def trace_branch_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "trace_id": "TR4623_0_minimal_trace_branch",
            "branch_condition": "m_mem enters visible matter only through conformal metric/mass-scale dependence and does not enter Z_Q_eff, theta_Q, observer flux, or wave envelope coefficients.",
            "source_result": "rho_mem = beta_T T_obs plus frame-equivalent beta_R R_obs bookkeeping",
            "local_zero": "outside matter in GR/Newtonian exterior: T_obs=0 and R_obs=0, so rho_mem=0",
            "surviving_risk": "inside matter beta_T can drive fifth-force/WEP residuals unless screened or universal and bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "trace_id": "TR4623_1_radiation_trace_zero",
            "branch_condition": "pure trace/conformal coupling with minimal Maxwell/radiation stress",
            "source_result": "EM radiation and high-frequency radiation-like stress do not source rho_mem through T^a_a",
            "local_zero": "null EM waves have F^2=F starF=0 and T_EM trace=0",
            "surviving_risk": "static EM F^2 source returns if Z_Q_eff(m_mem) is allowed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "trace_id": "TR4623_2_exterior_nohair_feed",
            "branch_condition": "trace branch plus 4621 Z_mem/M2_mem positivity plus zero boundary flux",
            "source_result": "rho_mem=0 in local exterior vacuum",
            "local_zero": "4621 no-hair theorem then gives Delta_v m_mem=0",
            "surviving_risk": "boundary flux, bodies, laboratories and composition-dependent beta_T remain tests",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def em_link_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "link_id": "EML4623_0_betaF_kappa",
            "parent_term": "S_EM=-1/4 int Z_Q_eff(m_mem) F_Q^2",
            "variation": "delta S_EM / delta m_mem = -1/4 kappa_memF2 F_Q^2",
            "selection_result": "beta_F is kappa_memF2/4 up to sign convention",
            "consequence": "4620 kappa-zero gates also kill the EM scalar source; finite beta_F must use the 4620 kappa row.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "link_id": "EML4623_1_no_double_count",
            "parent_term": "trace branch plus optional Maxwell kinetic branch",
            "variation": "trace branch gives no independent Maxwell trace source; Maxwell kinetic branch gives beta_F only if Z_Q_eff depends on m_mem",
            "selection_result": "do not count both a generic beta_F and kappa_memF2",
            "consequence": "local EM residual path is narrower and testable: kappa_memF2, static field invariants, and boundary flux.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "link_id": "EML4623_2_null_vs_static",
            "parent_term": "EM scalar invariant branch",
            "variation": "null radiation has F_Q^2=F_Q starF_Q=0, static/non-null fields generally do not",
            "selection_result": "wave/radiation zero does not imply laboratory static-field zero",
            "consequence": "R10/clock/lab bounds must use finite static-field source rows if beta_F survives.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def frame_control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "FR4623_0_no_R_T_double_count",
            "rule": "Use either Jordan curvature owner beta_R or Einstein trace owner beta_T for the same conformal scalar effect unless a parent action proves both independent.",
            "reason": "Frame transformations move M_eff(m)R dependence into matter scales.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "FR4623_1_betaF_kappa_lock",
            "rule": "beta_F must be locked to kappa_memF2 when the owner is Z_Q_eff(m_mem).",
            "reason": "The same parent coefficient controls both EM kinetic variation and memory scalar source.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "FR4623_2_observer_flux_lock",
            "rule": "beta_S needs an observer/coframe or boundary owner.",
            "reason": "Poynting flux is not an observer-free scalar volume coupling.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4623_0_no_free_betas", "rule": "No beta coefficient may be introduced without a parent owner, a derived relation, or an explicit finite nonclaim row.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4623_1_trace_not_everywhere_zero", "rule": "Trace branch zero is exterior/radiation-friendly but does not erase matter-interior or WEP risk.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4623_2_static_em_survives", "rule": "If kappa_memF2 survives, static EM invariants remain a local source even when Poynting divergence vanishes.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4623_0_frame_owner", "blocks": "trace/curvature local source claim", "missing": "parent choice of Jordan beta_R owner or Einstein beta_T trace owner", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4623_1_betaT_value", "blocks": "matter/WEP scoring", "missing": "universal or species-dependent beta_T derivation/value", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4623_2_independent_EM_owner", "blocks": "EM local source zero", "missing": "parent proof that Z_Q_eff is m_mem independent, or finite kappa_memF2 row", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4623_0_trace_branch_exact", "promotion_condition": "Parent signs trace-only branch, kappa_memF2=0, beta_S/beta_gw observer owners absent, beta_G parity-forbidden, and 4621 source/boundary zero holds.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4623_1_finite_coupling_bound", "promotion_condition": "Any surviving beta has a parent-owned numeric value and local source norm feeding the 4621 bound.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4623_0",
            "decision": DECISION,
            "meaning": "The source-coupling problem is narrower: beta_F is tied to kappa_memF2, beta_S requires observer/boundary structure, beta_G needs parity violation, beta_R/beta_T are frame-controlled, and the least-scrutiny branch is trace-only.",
            "status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "best_route": "develop the trace-only branch to local exterior vacuum/no-hair, then separately bound matter/WEP risk",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "Parent coupling selection rules reduce rho_mem beta coefficients to owned parent derivatives, trace branch, kappa-linked EM source, parity rule, and observer/boundary Poynting rule.",
            "valid_for_claim": False,
            "claim_allowed": False,
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
            "reason": "The least-scrutiny path is now trace-only local exterior vacuum; it must be checked against matter/WEP risk instead of assumed safe.",
            "derive_first": "trace-branch exterior no-hair and frame-owner relation",
            "fallback": "finite beta_T/kappa_memF2/source-profile bound rows",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4623 - Parent Coupling Selection Rule For rho_mem",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4623 narrows the coupling problem. The beta terms are not free theory knobs: each must be the variation of a parent scalar-density coupling with respect to `m_mem`.",
        "",
        "Main selection rule:",
        "",
        "`rho_mem = sum_A beta_A O_A`, where `beta_A = partial_m C_A(m_mem)|branch` for an actual parent action term `C_A(m_mem) O_A`.",
        "",
        "The cleanest local-GR route is the trace-only branch: if memory enters visible matter only through a conformal metric/mass-scale factor, `rho_mem` reduces to a trace source. Then exterior vacuum and radiation-like stress are naturally quiet, but matter interiors and WEP/fifth-force tests remain live.",
        "",
        "Most important concrete move: `beta_F` is not independent. If the parent EM term is `-1/4 Z_Q_eff(m_mem) F_Q^2`, then `beta_F = +/- kappa_memF2/4`. That ties the EM source-channel problem back to the 4620 coefficient instead of inventing a new free coupling.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Parent Selection Theorems",
        markdown_table(tables["theorems"]),
        "",
        "## Beta Ownership Matrix",
        markdown_table(tables["beta_matrix"]),
        "",
        "## Trace Branch Rows",
        markdown_table(tables["trace_branch"]),
        "",
        "## EM Coupling Link Rows",
        markdown_table(tables["em_link"]),
        "",
        "## Frame Degeneracy Controls",
        markdown_table(tables["frame_controls"]),
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
        "All rows remain `valid_for_claim=false`. This is a derivation narrowing checkpoint, not a local-GR or WEP pass.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 639 - PPC4161 Parent Coupling Selection Rule For rho_mem

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Coupling Selection

For any source operator `O_A`, the coefficient must satisfy:

`beta_A = partial_m C_A(m_mem)|branch`

for a parent scalar-density term `C_A(m_mem) O_A`.

Consequences:

1. `beta_F` is locked to `kappa_memF2`: if `S_EM=-1/4 int Z_Q_eff(m_mem)F_Q^2`, then `beta_F=+/- kappa_memF2/4`.
2. `beta_S` is not an observer-free covariant volume source; it needs a parent observer/coframe or becomes a boundary/finite flux row.
3. `beta_G` is forbidden on a parity-even scalar branch unless the parent has pseudoscalar/CP-odd structure.
4. `beta_R` and `beta_T` are frame-degenerate and need one parent owner.
5. The trace-only branch is the least-scrutiny local exterior route: exterior `T_obs=0` and `R_obs=0` can feed the 4621 no-hair theorem, while matter/WEP risk remains.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4623 derives parent coupling selection rules for rho_mem and ties beta_F to kappa_memF2 rather than treating beta couplings as free knobs.",
        "current_evidence": "Generated parent selection theorems, beta ownership matrix, trace branch rows, EM coupling link rows, frame controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "parent_coupling_selection_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming trace exterior silence while ignoring matter/WEP risk or independent EM kinetic coupling.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/WEP/PPN pass until parent frame owner, beta_T behavior, kappa_memF2 route, and source/boundary rows are closed or bounded.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    add("VAL4623_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, THEOREM_CSV, BETA_MATRIX_CSV, TRACE_BRANCH_CSV, EM_LINK_CSV, FRAME_CONTROL_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4623_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4623_02_betaF_kappa_link", any(row["theorem_id"] == "PSEL4623_2_betaF_kappa_link" for row in tables["theorems"]), "beta_F/kappa_memF2 theorem present")
    add("VAL4623_03_trace_branch", any(row["trace_id"] == "TR4623_0_minimal_trace_branch" for row in tables["trace_branch"]), "trace branch row present")
    add("VAL4623_04_poynting_observer_rule", any(row["symbol"] == "beta_S" and "observer" in row["selection_rule"] for row in tables["beta_matrix"]), "beta_S observer/boundary rule present")
    add("VAL4623_05_frame_controls", len(tables["frame_controls"]) >= 3, "frame/beta lock controls present")
    add("VAL4623_06_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4623_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4623_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4623_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4623_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4623_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4623_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4623_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4623_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4623_OVERALL", all(row["status"] == "PASS" for row in rows), "4623 parent coupling selection checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorems": theorem_rows(now),
        "beta_matrix": beta_matrix_rows(now),
        "trace_branch": trace_branch_rows(now),
        "em_link": em_link_rows(now),
        "frame_controls": frame_control_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorems"])
    write_csv(BETA_MATRIX_CSV, tables["beta_matrix"])
    write_csv(TRACE_BRANCH_CSV, tables["trace_branch"])
    write_csv(EM_LINK_CSV, tables["em_link"])
    write_csv(FRAME_CONTROL_CSV, tables["frame_controls"])
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
## PPC4161 Local Addendum - Parent Coupling Selection Rule For rho_mem

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4623 reduces the `rho_mem` beta couplings to parent owners. `beta_F` is locked to `kappa_memF2/4` if the owner is `Z_Q_eff(m_mem)F_Q^2`; `beta_S` needs an observer/coframe or boundary owner; `beta_G` needs parity-odd structure; `beta_R`/`beta_T` are frame-degenerate; the least-scrutiny local exterior route is trace-only, with matter/WEP risk retained.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Parent Coupling Selection Rule For rho_mem

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now refuses free beta couplings. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4623 validation failed: {failed}")
    print(f"4623 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
