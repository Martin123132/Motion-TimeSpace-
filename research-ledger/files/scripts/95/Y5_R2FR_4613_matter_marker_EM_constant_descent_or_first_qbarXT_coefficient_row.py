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

CHECKPOINT = "4613"
CLAIM_ID = "L-455"
BRANCH_ID = "MTS_R2FR_Y5_MATTER_MARKER_EM_CONSTANT_DESCENT_4613"
MARKER = "PPC4161_MATTER_MARKER_EM_CONSTANT_DESCENT_OR_FIRST_QBARXT_COEFFICIENT_ROW_4613"
PACKET_MARKER = "PPC4161_PACKET_MATTER_MARKER_EM_CONSTANT_DESCENT_4613"
DECISION = "MATTER_MARKER_EM_CONSTANT_DESCENT_CONDITIONAL_ZERO_AND_COEFFICIENT_ROWS_READY_NONCLAIM"
NEXT_TARGET = "4614-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"

DOC_PATH = POST / "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
FORMAL_PATH = FORMAL / "629-PPC4161-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4613_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_THETA_MARKER_DESCENT_THEOREM.csv"
CHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_CHANNEL_DESCENT_AUDIT.csv"
EM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_EM_ALPHA_DESCENT_ROWS.csv"
MASS_CLOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_MASS_CLOCK_MARKER_ROWS.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
QBARXT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4613_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4613_VALIDATION.csv"

CSV_4612_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4612_NEXT_TARGET.csv"
CSV_4612_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4612_MARKER_CONSTANT_RESPONSE_ROWS.csv"
CSV_4612_PRIORITY = SOURCE_DIR / "P8_Y5_R2FR_4612_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CSV_4264_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4264_THETA_MARKER_THEOREM.csv"
CSV_4264_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_4264_MARKER_BOUND_ROWS.csv"
CSV_4475_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4475_MARKER_BULK_COUPLING_ZERO_THEOREM.csv"
CSV_4474_FILL = SOURCE_DIR / "P8_Y5_R2FR_4474_MARKER_COUPLING_FILL_ROWS.csv"
CSV_3771_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv"
CSV_3771_COEFF = SOURCE_DIR / "P8_Y5_R2FR_3771_CONSTANT_MARKER_RESIDUAL_COEFFICIENTS.csv"
CSV_2674_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_2674_MATTER_CHANNEL_DESCENT_AUDIT.csv"
CSV_2674_TEMPLATE = SOURCE_DIR / "P8_Y5_R2FR_2674_QBARXT_BOUND_TEMPLATE_NONCLAIM.csv"
CSV_1046_AUDIT = SOURCE_DIR / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"
CSV_1046_ROWS = SOURCE_DIR / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
CSV_1396_ALPHA = SOURCE_DIR / "P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv"
CSV_CONSTANT_CONTRACT = SOURCE_DIR / "P8_constant_sector_universality_CONTRACT.csv"

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
        "claim": "4613 derives the conditional matter-marker/EM constant descent branch for qbar_XT and stages explicit coefficient rows when alpha, mass, clock, material or source-normalization markers do not descend.",
        "current_evidence": "Generated theta-marker descent theorem rows, channel audit, EM alpha rows, mass/clock/marker rows, qbarXT coefficient rows, qbarXT update rows and validation.",
        "status": "matter_marker_EM_constant_descent_conditional_zero_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating calibrated constants as derived physics or using units/common-mode rescaling to hide dimensionless alpha, mass-ratio, clock, material or source-normalization leakage.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No qbar_XT, WEP, clock, R10, Newton, Maxwell or local-GR pass until the constant/marker zero branch is parent-signed or finite coefficients are sourced.",
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
        ("SRC4613_00_4612_handoff", CSV_4612_NEXT, "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md", "4612 selected marker/constant/EM descent."),
        ("SRC4613_01_4612_marker", CSV_4612_MARKER, "MRK4612_0_constants", "4612 qbar constants row."),
        ("SRC4613_02_4612_EM", CSV_4612_MARKER, "MRK4612_2_EM_alpha", "4612 EM alpha marker row."),
        ("SRC4613_03_4612_priority", CSV_4612_PRIORITY, "qbar_constants, qbar_marker, s_alpha b_alpha", "4612 priority queue."),
        ("SRC4613_04_4264_chain_rule", CSV_4264_THEOREM, "TMT4264_3_matter_descent_chain_rule", "4264 exact conditional matter chain rule."),
        ("SRC4613_05_4264_bound", CSV_4264_THEOREM, "TMT4264_4_marker_deformation_bound", "4264 retained deformation bound."),
        ("SRC4613_06_4264_alpha_bound", CSV_4264_BOUNDS, "MB4264_1_charge_alpha_marker", "4264 alpha/charge marker bound row."),
        ("SRC4613_07_4264_source_norm", CSV_4264_BOUNDS, "MB4264_4_source_norm_marker", "4264 source-normalization marker row."),
        ("SRC4613_08_4475_projection", CSV_4475_THEOREM, "LMB4475_0_coefficient_definition", "4475 marker coupling projection law."),
        ("SRC4613_09_4475_verdict", CSV_4475_THEOREM, "LMB4475_7_verdict", "4475 exact conditional marker zero verdict."),
        ("SRC4613_10_4474_lambda", CSV_4474_FILL, "MCF4474_1_lambda_M", "4474 finite marker coefficient row."),
        ("SRC4613_11_3771_split", CSV_3771_THEOREM, "CMT3771_0_theta_split", "3771 theta split."),
        ("SRC4613_12_3771_zero", CSV_3771_THEOREM, "CMT3771_2_conditional_zero", "3771 conditional theta zero theorem."),
        ("SRC4613_13_3771_clock", CSV_3771_THEOREM, "CMT3771_4_clock_projection", "3771 clock projection."),
        ("SRC4613_14_3771_WEP", CSV_3771_THEOREM, "CMT3771_5_WEP_projection", "3771 WEP projection."),
        ("SRC4613_15_3771_coeff_alpha", CSV_3771_COEFF, "CMC3771_1_b_alpha", "3771 b_alpha coefficient row."),
        ("SRC4613_16_3771_coeff_source", CSV_3771_COEFF, "CMC3771_8_b_source_norm", "3771 source-normalization coefficient row."),
        ("SRC4613_17_2674_audit_EM", CSV_2674_AUDIT, "CH2674_3_EM_fine_structure", "2674 EM descent audit."),
        ("SRC4613_18_2674_template", CSV_2674_TEMPLATE, "BND2674_3_EM_alpha", "2674 EM alpha coefficient template."),
        ("SRC4613_19_1046_audit", CSV_1046_AUDIT, "CMA1046_5_verdict", "1046 constant/marker split verdict."),
        ("SRC4613_20_1046_rows", CSV_1046_ROWS, "QMC1046_3_qbar_marker_abs", "1046 qbar marker absolute row."),
        ("SRC4613_21_1396_alpha", CSV_1396_ALPHA, "EMG1396_0_alphaEM", "1396 alphaEM arena gate."),
        ("SRC4613_22_constant_contract", CSV_CONSTANT_CONTRACT, "C2_no_direct_constant_vertices", "constant sector no direct vertices contract."),
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
            "theorem_id": "TMD4613_0_theta_split",
            "claim": "theta_A splits into unit/common-scale conventions, dimensionless physical constants, representation/material labels and source/readout markers",
            "derivation": "dimensionful unit conventions cannot create dimensionless observables, but alpha_EM, mass ratios, binding fractions, clock ratios and source-normalization ratios can",
            "formula": "theta_A=(u_common,c_I,m_A,b_A,marker_A,source_norm)",
            "status": "EXACT_SPLIT_ADOPTED",
            "source_anchor": "CMT3771_0_theta_split",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TMD4613_1_qbasic_constant_zero",
            "claim": "If theta_obs is fixed/q-basic before variation, then D_X theta_obs=0 and qbar_constants/qbar_marker receive no J_theta Lie_v(theta) term",
            "derivation": "For S_matter=Sbar[psi,e_obs(q),theta_obs], delta_v S_matter has chain-rule terms through e_obs and theta_obs; v_X in ker(Dq) kills e_obs(q), and q-basic theta_obs kills the theta term",
            "formula": "delta_v S_matter|theta = sum_A int J_theta^A Lie_v(theta_A)=0",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "source_anchor": "TMT4264_1_qbasic_calibrated_zero;TMT4264_3_matter_descent_chain_rule;CMT3771_2_conditional_zero",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TMD4613_2_deformation_branch",
            "claim": "If any physical theta_A depends on hidden parent fields before variation, retain a coefficient rather than calling it calibration",
            "derivation": "Substituting nonzero Lie_v theta_A into delta_v S_matter gives a real qbar_XT channel; triangle inequality forbids cancellation with geometry/source terms",
            "formula": "|qbar_theta| <= sum_A |s_A b_A| + |qbar_marker_tail|",
            "status": "RETAINED_COEFFICIENT_BRANCH",
            "source_anchor": "TMT4264_4_marker_deformation_bound;CMC3771_0_total_theta",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TMD4613_3_EM_alpha_branch",
            "claim": "The EM/fine-structure channel zeros only if the gauge kinetic data and charge representations are q-basic or superselected",
            "derivation": "For L_EM=-1/4 Z_EM(theta,X)F^2 plus charged matter, b_alpha is the vertical derivative of the dimensionless gauge/charge data; unit rescaling cannot hide it",
            "formula": "b_alpha_EM := Lie_v ln(alpha_EM); qbar_EM <= |s_alpha b_alpha_EM| + charge/readout tails",
            "status": "EM_ZERO_CONDITIONAL_B_ALPHA_RETAINED",
            "source_anchor": "CMA1046_0_alpha_EM;BND2674_3_EM_alpha;EMG1396_0_alphaEM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TMD4613_4_marker_operator_branch",
            "claim": "Material/source marker couplings zero only if the marker-containing parent operator is absent and no spurion, auxiliary, finite source or boundary route substitutes for it",
            "derivation": "lambda_M is the projection of the parent bulk action onto a marker monomial; if the projection vanishes and counterroutes are absent, the marker bulk term vanishes",
            "formula": "lambda_M=Pi_{F_M O_marker}(S_bulk); lambda_M=0 iff marker operator absent plus no counterroute",
            "status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "source_anchor": "LMB4475_0_coefficient_definition;LMB4475_7_verdict",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "TMD4613_5_qbarXT_update",
            "claim": "The qbarXT marker/constant contribution is now qbar_theta_marker_abs and feeds the 4612 absolute envelope",
            "derivation": "Insert the theta/marker coefficient sum into qbar_constants+qbar_marker+s_alpha b_alpha inside the 4612 no-cancellation envelope",
            "formula": "|qbar_XT| <= ... + |qbar_theta_marker| + ... ; |qbar_theta_marker| <= |b_alpha|+|b_mu|+|b_mA|+|b_nuc|+|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M-tail|",
            "status": "QBARXT_UPDATE_READY_NONCLAIM",
            "source_anchor": "MRK4612_0_constants;MRK4612_1_material_markers;MRK4612_2_EM_alpha",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def channel_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CH4613_0_alpha_EM",
            "channel": "alpha_EM / gauge charge",
            "clean_zero_route": "Z_EM, charge reps and alpha_EM are quotient-owned/superselected with Lie_v ln(alpha_EM)=0",
            "finite_branch": "retain b_alpha_EM and EM readout tails",
            "observable_links": "clock;EM spectra;WEP;R10;Maxwell",
            "current_status": "ZERO_CONDITIONAL_NEXT_TARGET",
            "source_anchor": "CMA1046_0_alpha_EM;EMG1396_0_alphaEM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CH4613_1_mass_ratios",
            "channel": "particle masses, mass ratios, Yukawa/binding data",
            "clean_zero_route": "observable mass ratios and binding fractions are fixed representation data",
            "finite_branch": "retain b_mu, b_mA and b_nuc",
            "observable_links": "WEP;composition;clock;R10;Newton",
            "current_status": "CONDITIONAL_ZERO_OR_COEFFICIENT",
            "source_anchor": "CMA1046_1_particle_masses;CMC3771_2_b_mu;CMC3771_4_b_nuc",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CH4613_2_clock",
            "channel": "clock transitions/readout standards",
            "clean_zero_route": "clock transition ratios derive only from q-basic constants and descended observed frame",
            "finite_branch": "retain b_clock_i and readout-frame terms",
            "observable_links": "clock comparison;redshift;alpha drift",
            "current_status": "CONDITIONAL_ZERO_OR_COEFFICIENT",
            "source_anchor": "CMT3771_4_clock_projection;CMC3771_6_b_clock",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CH4613_3_material_marker",
            "channel": "material/source/test labels",
            "clean_zero_route": "labels are representation data fixed before variation and not fields/spurions/source multipliers",
            "finite_branch": "retain b_material_label and lambda_M-tail",
            "observable_links": "WEP;composition;R10;readout",
            "current_status": "CONDITIONAL_ZERO_OR_COEFFICIENT",
            "source_anchor": "CMA1046_3_material_markers;LMB4475_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "CH4613_4_source_norm",
            "channel": "source normalization / measured GM common mode",
            "clean_zero_route": "active/passive/inertial source normalization is the same conserved current",
            "finite_branch": "retain b_source_norm and GM calibration tail",
            "observable_links": "Newton GM;Gdot;orbital;PPN;R10",
            "current_status": "CONDITIONAL_ZERO_OR_COEFFICIENT",
            "source_anchor": "CMT3771_7_Newton_source_projection;CMC3771_8_b_source_norm;C6_measured_GM_absolute_calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def em_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4613_0_gauge_kinetic",
            "quantity": "b_alpha_EM",
            "derivation": "If S_EM contains -1/4 Z_EM(X)F^2, then Lie_v ln alpha_EM is minus the vertical derivative of the physical gauge kinetic normalization after representation normalization",
            "zero_condition": "Lie_v Z_EM=0 and charge representation data fixed",
            "fallback_formula": "|qbar_EM| <= |s_alpha b_alpha_EM| + |b_charge| + |EM_readout_tail|",
            "current_status": "NEXT_TARGET_ZERO_OR_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4613_1_no_unit_hiding",
            "quantity": "alpha_EM",
            "derivation": "alpha_EM is dimensionless, so a unit/common-scale rescaling cannot remove b_alpha_EM from clock, spectra, WEP or R10 material charges",
            "zero_condition": "alpha_EM is q-basic/superselected, not merely rescaled",
            "fallback_formula": "Delta ln(nu_a/nu_b)=Delta K_alpha^{ab} b_alpha_EM tau_clock + other b_I terms",
            "current_status": "UNIT_FIREWALL_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EM4613_2_Maxwell_limit",
            "quantity": "Maxwell/EM stress descent",
            "derivation": "Maxwell limit survives in the clean branch when EM stress is varied only through the descended observed metric/coframe and fixed gauge constants",
            "zero_condition": "no alpha_EM(X)F^2, no hidden matter frame, no source-only charge weights, fixed EM readout",
            "fallback_formula": "retain b_alpha_EM and EM stress/readout residuals in qbar_XT and Q_bulk_EM/Poynting",
            "current_status": "MAXWELL_LIMIT_CONDITIONAL_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def mass_clock_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MCM4613_0_mass_ratios",
            "quantity": "b_mu,b_mA,b_nuc",
            "formula": "observable mass/material leakage is retained after removing pure common unit mode",
            "zero_condition": "mass ratios, binding fractions and material response data are q-basic/superselected",
            "fallback_formula": "eta_AB <= sum_I |Delta Q_I^{AB}| |b_I| tau_WEP plus EM/binding/source-current residuals",
            "source_anchor": "CMT3771_5_WEP_projection;CMC3771_2_b_mu;CMC3771_3_b_mA;CMC3771_4_b_nuc",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MCM4613_1_clock",
            "quantity": "b_clock_i",
            "formula": "clock ratios see sensitivity-weighted dimensionless constant leakage plus readout-frame terms",
            "zero_condition": "clock transitions derive from q-basic constants and no independent clock marker exists",
            "fallback_formula": "delta ln(nu_a/nu_b)=sum_I Delta K_I^{ab} b_I + readout_frame_tail",
            "source_anchor": "CMT3771_4_clock_projection;CMC3771_6_b_clock",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MCM4613_2_material_label",
            "quantity": "b_material_label,lambda_M",
            "formula": "material labels are silent only if absent from parent bulk/boundary/action grammar",
            "zero_condition": "no marker-containing operator, no spurion, no auxiliary, no finite diagnostic source, no boundary marker route",
            "fallback_formula": "R_marker_abs=abs(c_R2_marker)+abs(C_marker)+abs(T_marker_projection)+abs(boundary_marker)",
            "source_anchor": "LMB4475_7_verdict;MCF4474_9_no_cancellation_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("QTC4613_0_epsilon_theta", "epsilon_theta", "aggregate constants/material-marker leakage after unit/common-mode quotient", "sup_A,I |zeta^A Lie_EA theta_I|", "MISSING_PARENT_THETA_SUPERSELECTION", "dimensionless_or_normalized_vertical_derivative", "WEP;clock;R10;PPN;Newton"),
        ("QTC4613_1_b_alpha", "b_alpha_EM", "fine-structure/gauge kinetic leakage", "Lie_v ln(alpha_EM)", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM", "dimensionless", "clock;EM;WEP;R10;Maxwell"),
        ("QTC4613_2_b_mu", "b_mu", "mass-ratio leakage", "Lie_v ln(m_e/m_p)", "MISSING_B_MU_OR_PARENT_ZERO_THEOREM", "dimensionless", "clock;WEP;composition"),
        ("QTC4613_3_b_mass_material", "b_mA,b_nuc", "material mass and binding leakage", "Lie_v ln(m_A/m_ref), Lie_v ln(E_binding/m_ref)", "MISSING_MATERIAL_MASS_MARKER_DESCENT", "dimensionless", "WEP;R10;Newton"),
        ("QTC4613_4_b_clock", "b_clock_i", "clock apparatus/readout marker leakage after alpha/mass projection", "Lie_v ln(clock_i/reference)", "MISSING_CLOCK_MARKER_DESCENT", "dimensionless_or_clock_fractional", "clock;redshift;LPI"),
        ("QTC4613_5_b_material_label", "b_material_label,lambda_M", "material/source/preparation marker leakage", "Pi_marker(S_parent) or Lie_v marker label", "MISSING_MATERIAL_LABEL_SUPERSELECTION_OR_MARKER_OPERATOR_ABSENCE", "dimensionless_or_operator_units", "WEP;R10;composition;readout"),
        ("QTC4613_6_b_source_norm", "b_source_norm", "active/passive/inertial source normalization leakage", "Lie_v ln(mu_obs/M_inertial)", "MISSING_NEWTON_SOURCE_NORMALIZATION_OWNER", "dimensionless", "Newton GM;Gdot;orbital;PPN"),
        ("QTC4613_7_qbar_theta_marker_abs", "qbar_theta_marker_abs", "absolute no-cancellation theta/marker contribution to qbar_XT", "sum_abs(QTC4613_0..6 plus readout tails)", "MISSING_COMPONENT_VALUES", "dimensionless_after_normalization", "all_local_arenas"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "current_value": current_value,
            "units": units,
            "observable_links": observable_links,
            "status": "template_nonclaim",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for row_id, symbol, definition, formula, current_value, units, observable_links in rows
    ]


def qbarxt_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXU4613_0_theta_marker_insert",
            "quantity": "qbar_theta_marker_abs",
            "update_formula": "|qbar_theta_marker| <= |epsilon_theta|+|b_alpha_EM|+|b_mu|+|b_mA|+|b_nuc|+|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M_tail|",
            "zero_condition": "all theta/marker channels are q-basic/superselected/absent in the same parent branch",
            "current_status": "ABSOLUTE_SUM_SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXU4613_1_qbarXT",
            "quantity": "qbar_XT_bound_abs",
            "update_formula": "|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_source_weight|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|",
            "zero_condition": "4612 response envelope plus 4613 theta/marker zero in the same branch",
            "current_status": "QBARXT_STILL_NONCLAIM_BUT_MARKER_SLOT_REFINED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXU4613_2_product",
            "quantity": "I_X^ST(lambda)",
            "update_formula": "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)",
            "zero_condition": "source and test response envelopes exact-zero or source-backed, with K_X/Z_X/tau sourced",
            "current_status": "PRODUCT_REMAINS_BLOCKED_BY_VALUES_AND_ARENAS",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4613_0_no_public_push", "rule": "work stays local/private; no GitHub push, no public repo mutation", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4613_1_no_unit_hiding", "rule": "dimensionless constants and ratios cannot be erased by unit conventions", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4613_2_no_calibration_as_derivation", "rule": "calibrating theta_obs before variation is a conditional branch, not a derivation of constants", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4613_3_no_marker_cancellation", "rule": "alpha, mass, clock, material, source-normalization and marker terms use absolute sums", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4613_0_EM", "blocks": "Maxwell/EM stress and qbar_XT marker zero", "missing": "parent proof that alpha_EM/gauge kinetic data are q-basic or source-backed b_alpha_EM", "resolution": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4613_1_masses", "blocks": "WEP/clock/R10 marker zero", "missing": "mass-ratio, binding and material-label superselection or coefficients", "resolution": "fill b_mu/b_mA/b_nuc/b_material_label rows if no theorem", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4613_2_source_norm", "blocks": "Newton GM and local-GR source calibration", "missing": "active/passive/inertial source normalization owner", "resolution": "derive conserved source current equality or retain b_source_norm", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4613_3_product", "blocks": "R10/PPN/clock/orbital scoring", "missing": "qbar_theta_marker values plus Qbar_XH/qbar_XT/K_X/Z_X/tau rows", "resolution": "continue product-gate source acquisition after EM descent", "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4613_0_source_traceability", "requirement": "every cited marker/constant source path exists and every cited row needle is found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4613_1_theta_zero_branch", "requirement": "theta_obs q-basic/calibrated before variation is parent-signed for every active matter/EM/clock/material channel", "current_status": "CONDITIONAL_NOT_PARENT_SIGNED", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4613_2_coefficient_branch", "requirement": "all surviving b_alpha/b_mu/b_mA/b_clock/b_marker/b_source_norm/lambda_M rows have values, units and source paths", "current_status": "BLOCKED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4613_3_EM_Maxwell", "requirement": "no alpha_EM(X)F^2 or charge-representation leakage before Maxwell/EM stress is claimed", "current_status": "BLOCKED_NEXT_TARGET", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "meaning": "The clean marker route is now an exact conditional chain-rule theorem; the non-clean route is explicit qbarXT coefficient rows.",
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "Matter constants, alpha_EM, masses, clocks, material labels and source normalization are split into a q-basic zero branch versus explicit finite qbarXT coefficients.",
        "what_did_not_move": "No constant derivation, qbarXT zero, Maxwell, Newton, WEP, clock, R10 or local-GR claim; EM gauge kinetic descent is the next proof target.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "alpha_EM is dimensionless and cannot be hidden by units, while the EM sector is central to Maxwell stress, clocks, WEP and R10 material response.",
        "derive_first": "prove the EM gauge kinetic function and charge representation data are q-basic/superselected so b_alpha_EM=0",
        "fallback": "stage b_alpha_EM as the first source-backed qbarXT coefficient row with clock/WEP/R10 projections",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4613 - Matter Marker / EM Constant Descent Or First `qbar_XT` Coefficient Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint makes the marker/constant fork explicit:

```text
S_matter = Sbar[psi, e_obs(q), theta_obs]
```

with `v_X in ker(Dq)`. If `theta_obs` is q-basic/calibrated before variation, then

```text
delta_v S_matter|theta = sum_A int J_theta^A Lie_v(theta_A) = 0.
```

If not, the theory must retain

```text
|qbar_theta_marker| <= |b_alpha|+|b_mu|+|b_mA|+|b_nuc|+|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M-tail|.
```

This is progress, but not a claim: calibration is not derivation, and dimensionless constants cannot be hidden by units.

## Source Register

{markdown_table(tables["sources"])}

## Theta/Marker Descent Theorem

{markdown_table(tables["theorem"])}

## Channel Descent Audit

{markdown_table(tables["channels"])}

## EM / Alpha Descent Rows

{markdown_table(tables["em"])}

## Mass / Clock / Marker Rows

{markdown_table(tables["mass_clock"])}

## First `qbar_XT` Coefficient Rows

{markdown_table(tables["coefficients"])}

## `qbar_XT` Update Rows

{markdown_table(tables["qbarxt_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The next derivation should attack the EM gauge kinetic branch directly: either `b_alpha_EM=0` follows from quotient/superselection ownership, or it becomes the first finite source-backed coefficient row.

Private nonclaim. No GitHub action. No qbarXT, Maxwell, Newton, WEP, clock, R10, PPN, orbital or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 629 - Matter Marker / EM Constant Descent Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Conditional Descent Theorem

Let

```text
S_matter = Sbar[psi, e_obs(q), theta_obs]
```

with `v_X in ker(Dq)`. If `theta_obs` is fixed/q-basic before variation, then

```text
delta_v S_matter|theta = sum_A int J_theta^A Lie_v(theta_A) = 0.
```

Thus the constant/marker part of `qbar_XT` vanishes only on the calibrated q-basic branch.

## Deformation Branch

If any physical constant or marker is parent-field dependent, retain

```text
|qbar_theta_marker| <= |b_alpha|+|b_mu|+|b_mA|+|b_nuc|+|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M-tail|.
```

For EM,

```text
b_alpha_EM := Lie_v ln(alpha_EM).
```

This is zero only if gauge kinetic data and charge representations are quotient-owned/superselected.

## Status

This closes one conceptual loophole: constants can be calibrated, but only a parent-signed q-basic/superselection statement makes them silent. Otherwise they become explicit coefficients.

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
    add("VAL4613_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, CHANNEL_CSV, EM_CSV, MASS_CLOCK_CSV, COEFFICIENT_CSV,
        QBARXT_UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4613_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    em_text = "\n".join(str(row) for row in tables["em"])
    coefficient_text = "\n".join(str(row) for row in tables["coefficients"])
    update_text = "\n".join(str(row) for row in tables["qbarxt_update"])
    add("VAL4613_02_chain_rule", "delta_v S_matter|theta" in theorem_text and "EXACT_CONDITIONAL_ZERO_THEOREM" in theorem_text, "conditional chain-rule zero present")
    add("VAL4613_03_deformation_branch", "|qbar_theta|" in theorem_text and "RETAINED_COEFFICIENT_BRANCH" in theorem_text, "deformation branch present")
    add("VAL4613_04_EM_alpha", "b_alpha_EM" in em_text and "Maxwell" in em_text, "EM alpha/Maxwell rows present")
    add("VAL4613_05_coefficients", "QTC4613_1_b_alpha" in coefficient_text and "QTC4613_6_b_source_norm" in coefficient_text, "coefficient rows present")
    add("VAL4613_06_qbarxt_update", "qbar_theta_marker_abs" in update_text and "qbar_XT_bound_abs" in update_text, "qbarXT update present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4613_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4613_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4613_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4613_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4613_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4613_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4613_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4613_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4613_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4613_OVERALL", all(row["status"] == "PASS" for row in rows), "4613 matter-marker/EM constant descent gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "channels": channel_rows(now),
        "em": em_rows(now),
        "mass_clock": mass_clock_rows(now),
        "coefficients": coefficient_rows(now),
        "qbarxt_update": qbarxt_update_rows(now),
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
    write_csv(CHANNEL_CSV, tables["channels"])
    write_csv(EM_CSV, tables["em"])
    write_csv(MASS_CLOCK_CSV, tables["mass_clock"])
    write_csv(COEFFICIENT_CSV, tables["coefficients"])
    write_csv(QBARXT_UPDATE_CSV, tables["qbarxt_update"])
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
## PPC4161 Local Addendum - Matter Marker / EM Constant Descent Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The constant/marker part of `qbar_XT` now has a clean conditional route: if `S_matter=Sbar[psi,e_obs(q),theta_obs]` and `theta_obs` is q-basic/calibrated before variation, then `sum_A int J_theta^A Lie_v(theta_A)=0`. If that branch is not parent-signed, the surviving slot is `qbar_theta_marker_abs`, with explicit coefficients `b_alpha_EM`, `b_mu`, `b_mA`, `b_nuc`, `b_clock`, `b_material_label`, `b_source_norm` and `lambda_M` tails.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Matter Marker / EM Constant Descent Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now distinguishes calibrated q-basic constants from derived constants. The next target is the EM gauge kinetic branch because `alpha_EM` is dimensionless and controls Maxwell stress, clocks, WEP and R10 material response.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4613 validation failed: {failed}")
    print(f"4613 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
