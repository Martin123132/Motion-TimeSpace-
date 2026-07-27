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

CHECKPOINT = "4612"
CLAIM_ID = "L-454"
BRANCH_ID = "MTS_R2FR_Y5_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_4612"
MARKER = "PPC4161_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_OR_FIRST_SOURCE_BACKED_INPUT_4612"
PACKET_MARKER = "PPC4161_PACKET_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_4612"
DECISION = "QBARXT_TEST_BODY_RESPONSE_ENVELOPE_READY_FIRST_SOURCE_BACKED_QUEUE_NONCLAIM"
NEXT_TARGET = "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"

DOC_PATH = POST / "4612-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
FORMAL_PATH = FORMAL / "628-PPC4161-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4612_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv"
VISIBLE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_VISIBLE_MATTER_RESPONSE_ROWS.csv"
MARKER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_MARKER_CONSTANT_RESPONSE_ROWS.csv"
HIDDEN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_HIDDEN_TAIL_RESPONSE_ROWS.csv"
BOUNDARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_BOUNDARY_DOMAIN_READOUT_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_PRODUCT_COUPLING_HANDOFF_ROWS.csv"
PRIORITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4612_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4612_VALIDATION.csv"

CSV_4611_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4611_NEXT_TARGET.csv"
CSV_4611_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4611_PRODUCT_HANDOFF_ROWS.csv"
CSV_4603_QBARXT = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXT_FACTOR_ROWS.csv"
CSV_3371_ENVELOPE = SOURCE_DIR / "P8_Y5_R2FR_3371_QBARXT_UPDATED_ENVELOPE_NONCLAIM.csv"
CSV_3369_LAW = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_BOUND_LAW.csv"
CSV_3369_COMPONENTS = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_COMPONENT_ROWS_NONCLAIM.csv"
CSV_3094_HANDOFF = SOURCE_DIR / "P8_Y5_R2FR_3094_QBARXT_HANDOFF_SCHEMA.csv"
CSV_3095_COMPONENTS = SOURCE_DIR / "P8_Y5_R2FR_3095_QBARXT_COMPONENT_ENVELOPE.csv"
CSV_3096_TOTAL = SOURCE_DIR / "P8_Y5_R2FR_3096_QBARXT_TOTAL_ENVELOPE.csv"
CSV_PARENT_1849 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv"
CSV_PARENT_1850 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1850_QBARXT_TOTAL_ENVELOPE.csv"
CSV_PARENT_2158 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv"
CSV_2673_ZERO = SOURCE_DIR / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
CSV_2673_MATTER = SOURCE_DIR / "P8_Y5_R2FR_JX_QBARXT_2673_MATTER_CHANNEL_AUDIT.csv"
CSV_2673_TEMPLATE = SOURCE_DIR / "P8_Y5_R2FR_JX_QBARXT_2673_FIRST_COEFFICIENT_TEMPLATE_NONCLAIM.csv"
CSV_2673_GATES = SOURCE_DIR / "P8_Y5_R2FR_JX_QBARXT_2673_CLAIM_GATES.csv"

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
        "claim": "4612 assembles qbar_XT as the test-body/matter response analogue of Qbar_XH, with visible geometry, constants/markers, hidden/source tails, boundary/domain/readout and product-coupling handoff rows.",
        "current_evidence": "Generated qbar_XT theorem rows, visible/marker/hidden/boundary response rows, product handoff rows, first source-backed priority queue and validation.",
        "status": "qbarXT_test_body_response_envelope_ready_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Hiding the same coupling on the test-body side by assuming matter constants, EM markers, hidden frames, domain selectors or readout maps are vertically silent without a parent-signed proof.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, WEP, clock, PPN, orbital, Newton, Maxwell or local-GR claim until qbar_XT components are exact-zero or source-backed and combined with Qbar_XH, K_X, Z_X and arena tau rows.",
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
        ("SRC4612_00_4611_handoff", CSV_4611_NEXT, "4612-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md", "4611 requested qbar_XT response envelope."),
        ("SRC4612_01_4611_product", CSV_4611_PRODUCT, "PROD4611_1_test_side", "4611 product handoff names qbar_XT as next missing side."),
        ("SRC4612_02_4603_geom", CSV_4603_QBARXT, "QT4603_0_geom", "4603 geometry factor row."),
        ("SRC4612_03_4603_marker", CSV_4603_QBARXT, "QT4603_1_marker", "4603 marker factor row."),
        ("SRC4612_04_4603_nonH", CSV_4603_QBARXT, "QT4603_2_nonHilbert", "4603 non-Hilbert factor row."),
        ("SRC4612_05_4603_total", CSV_4603_QBARXT, "QT4603_4_total_guard", "4603 total qbar_XT guard."),
        ("SRC4612_06_3371_full", CSV_3371_ENVELOPE, "ENV3371_0_qbarXT_full_abs", "3371 expanded qbar_XT hidden-tail envelope."),
        ("SRC4612_07_3369_law", CSV_3369_LAW, "BQL3369_0_total_abs_guard", "3369 qbar_XT no-cancellation law."),
        ("SRC4612_08_3369_components", CSV_3369_COMPONENTS, "QBC3369_TOTAL", "3369 component total row."),
        ("SRC4612_09_3094_handoff", CSV_3094_HANDOFF, "QBH3094_4_total_abs_guard", "3094 handoff schema."),
        ("SRC4612_10_3095_total", CSV_3095_COMPONENTS, "QBC3095_5_total_abs_guard", "3095 component envelope total."),
        ("SRC4612_11_3095_geom", CSV_3095_COMPONENTS, "QBC3095_0_qbar_geom", "3095 geometry matter response."),
        ("SRC4612_12_3095_constants", CSV_3095_COMPONENTS, "QBC3095_1_qbar_constants", "3095 constants response."),
        ("SRC4612_13_3095_source_weight", CSV_3095_COMPONENTS, "QBC3095_3_qbar_source_weight", "3095 source-weight response."),
        ("SRC4612_14_3096_total", CSV_3096_TOTAL, "ENV3096_1_no_cancellation", "3096 no-cancellation envelope."),
        ("SRC4612_15_parent_1849", CSV_PARENT_1849, "QBC1849_5_total_abs_guard", "parent qbarXT component envelope."),
        ("SRC4612_16_parent_1850", CSV_PARENT_1850, "ENV1850_1_no_cancellation", "parent qbarXT total envelope."),
        ("SRC4612_17_parent_2158", CSV_PARENT_2158, "JQD2158_7_total_abs_guard", "J_X/qbar_XT decomposition."),
        ("SRC4612_18_2673_verdict", CSV_2673_ZERO, "JX2673_7_verdict", "2673 qbarXT zero verdict."),
        ("SRC4612_19_2673_matter", CSV_2673_MATTER, "MAT2673_5_verdict", "2673 matter-channel verdict."),
        ("SRC4612_20_2673_template", CSV_2673_TEMPLATE, "QXT2673_0_qbarXT", "2673 first coefficient template."),
        ("SRC4612_21_2673_gates", CSV_2673_GATES, "CG2673_1_qbarXT_zero", "2673 claim gate for qbarXT zero."),
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
            "row_id": "QXT4612_0_variational_definition",
            "quantity": "qbar_XT",
            "formula": "qbar_XT := M_T^-1 |delta_{v_X} S_T| in the selected normalization",
            "zero_condition": "matter action, observed frame, constants, support/domain and readout all descend through q with v_X in ker(Dq)",
            "source_anchor": "QBH3094_0_conditional_chain_rule;JX2673_0_contract",
            "current_status": "DEFINITION_ASSEMBLED_ZERO_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXT4612_1_visible_hidden_split",
            "quantity": "qbar_XT_bound_abs",
            "formula": "|qbar_XT| <= |qbar_visible| + |qbar_hidden_tail|",
            "zero_condition": "visible matter and hidden-tail blocks both exact-zero in the same parent branch",
            "source_anchor": "ENV3371_0_qbarXT_full_abs",
            "current_status": "VISIBLE_HIDDEN_SPLIT_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXT4612_2_component_envelope",
            "quantity": "qbar_XT_bound_abs",
            "formula": "|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|",
            "zero_condition": "every component is theorem-zero or source-backed in the same branch",
            "source_anchor": "BQL3369_0_total_abs_guard;QBC3095_5_total_abs_guard;JQD2158_7_total_abs_guard",
            "current_status": "ABSOLUTE_RESPONSE_ENVELOPE_ASSEMBLED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXT4612_3_no_smuggling_rule",
            "quantity": "qbar_XT_claim_firewall",
            "formula": "no WEP/common-mode wording, no measured-G calibration, no readout convention, and no component cancellation may be used to erase qbar_XT",
            "zero_condition": "parent-signed descent or source-backed coefficient for each channel",
            "source_anchor": "ENV3096_1_no_cancellation;CG2673_1_qbarXT_zero;CG2673_4_verdict",
            "current_status": "FIREWALL_READY_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QXT4612_4_product_handoff",
            "quantity": "I_X^ST(lambda)",
            "formula": "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)",
            "zero_condition": "Qbar_XH and qbar_XT both zero/bounded, with Z_X/K_X/tau sourced",
            "source_anchor": "PROD4611_1_test_side;QXT2673_3_alpha_feed",
            "current_status": "TEST_SIDE_ROLLUP_READY_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def visible_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "VIS4612_0_geom",
            "quantity": "qbar_geom",
            "formula": "qbar_geom=(2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu",
            "zero_route": "observed matter metric/coframe descends through q, so Lie_v ghat=0 for v_X in ker(Dq)",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "source_anchor": "QBC3095_0_qbar_geom;QBC3369_0_geom;QT4603_0_geom",
            "observable_links": "R10;PPN;clock;WEP_common_mode;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "VIS4612_1_weyl_disformal",
            "quantity": "c_g,b_dis",
            "formula": "|qbar_geom| <= |tau_g c_g| + |tau_dis b_dis|",
            "zero_route": "hidden Weyl/disformal matter frame absent or parent-owned by observed quotient data",
            "current_status": "MISSING_CG_BDIS_ZERO_OR_BOUND",
            "source_anchor": "QT4603_0_geom;QBC3369_0_geom;JQD2158_0_geom",
            "observable_links": "PPN;clock;WEP;R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def marker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MRK4612_0_constants",
            "quantity": "qbar_constants",
            "formula": "qbar_constants=M_T^-1 sum_A int J_theta^A Lie_v theta_A",
            "zero_route": "masses, charges, alpha_EM, clock and representation constants are quotient-owned or vertical-silent",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_NUMERIC_BOUND",
            "source_anchor": "QBC3095_1_qbar_constants;JQD2158_1_constants;MAT2673_1_atomic_masses;MAT2673_2_EM",
            "observable_links": "WEP;clock;fine_structure;EM;particle_mass;R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MRK4612_1_material_markers",
            "quantity": "qbar_marker",
            "formula": "|qbar_marker| <= sum_marker |s_marker b_marker|",
            "zero_route": "material, isotope, preparation, source/readout labels are representation data fixed before variation",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "source_anchor": "QBC3095_2_qbar_marker;QBC3369_1_marker;JQD2158_2_marker",
            "observable_links": "WEP_source_charge;clock;R10;readout",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MRK4612_2_EM_alpha",
            "quantity": "s_alpha b_alpha",
            "formula": "alpha_EM/charge-sector contribution is retained as |s_alpha b_alpha| unless EM descent is parent-signed",
            "zero_route": "EM constants and fine-structure readout descend through q or have zero X derivative",
            "current_status": "MISSING_EM_DESCENT_CERTIFICATE",
            "source_anchor": "MAT2673_2_EM;QBC3095_1_qbar_constants;ENV3371_0_qbarXT_full_abs",
            "observable_links": "EM;fine_structure;clock;R10;WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def hidden_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HID4612_0_source_weight",
            "quantity": "qbar_source_weight",
            "formula": "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| plus measured-GM calibration tail",
            "zero_route": "universal source current theorem with no species/source-only weights",
            "current_status": "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
            "source_anchor": "QBC3095_3_qbar_source_weight;JQD2158_3_source_weight",
            "observable_links": "WEP_source_charge;orbital;R10_source_mass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HID4612_1_nonHilbert",
            "quantity": "qbar_nonH",
            "formula": "|qbar_nonH| <= |q_nonH| + |J_shadow|/|J_H|",
            "zero_route": "ordinary matter functor has no non-Hilbert/source-shadow slot and hidden tails vanish",
            "current_status": "MISSING_NO_DIRECT_SOURCE_SLOT_OR_NUMERIC_BOUND",
            "source_anchor": "QBC3369_2_nonHilbert;QT4603_2_nonHilbert;JQD2158_4_nonHilbert",
            "observable_links": "source_mass;WEP;Newton;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HID4612_2_hidden_frame",
            "quantity": "F_X_prime, disformal_coeff",
            "formula": "hidden conformal/disformal X derivative retained as coefficient row unless zeroed",
            "zero_route": "F_X_prime=0 and disformal_coeff=0 or hidden frame factors through q",
            "current_status": "MISSING_HIDDEN_FRAME_ZERO_OR_BOUND",
            "source_anchor": "JX2673_4_hidden_frame;MAT2673_3_hidden_frame;QXT2673_2_hidden_frame",
            "observable_links": "PPN;clock;WEP;R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def boundary_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BDR4612_0_support",
            "quantity": "qbar_support",
            "formula": "|qbar_support| <= |Delta_W_support|",
            "zero_route": "test/source support worldtube is fixed by q-basic Hilbert source before readout",
            "current_status": "MISSING_FIXED_SUPPORT_THEOREM_OR_NUMERIC_BOUND",
            "source_anchor": "QBC3369_3_support;QT4603_3_support_boundary_domain",
            "observable_links": "orbital GM;source_mass;PPN",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BDR4612_1_boundary",
            "quantity": "qbar_boundary",
            "formula": "|qbar_boundary| <= |epsilon_boundary_contact| + |B_X_flux| + |Phi_boundary_X|",
            "zero_route": "compact interior collar and no contact/interface/boundary flux support",
            "current_status": "CONTACT_OR_BOUNDARY_SURVIVOR_OPEN",
            "source_anchor": "QBC3369_4_boundary;JQD2158_5_boundary",
            "observable_links": "PPN;R10;orbital;WEP material",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BDR4612_2_domain",
            "quantity": "qbar_domain",
            "formula": "|qbar_domain| <= |epsilon_Qv_projector_piece| + |epsilon_Cv_constraint_missing|",
            "zero_route": "domain/projector/source measure is a parent-fixed q-basic chain map",
            "current_status": "MISSING_PROJECTOR_VARIATION_AND_WARD_CLOSURE",
            "source_anchor": "QBC3369_5_domain;JX2673_5_domain_projector_source",
            "observable_links": "Newton;orbital;PPN;source_mass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BDR4612_3_readout",
            "quantity": "qbar_readout",
            "formula": "post-variation readout selector C_readout[A] and measured-G/source-normalization absorption tail",
            "zero_route": "variation occurs before readout and source normalization is fixed, not tuned after the fact",
            "current_status": "MISSING_VARIATION_BEFORE_READOUT_OR_NUMERIC_BOUND",
            "source_anchor": "JQD2158_6_readout;QXT2673_4_no_cancellation",
            "observable_links": "orbital;clock;WEP;R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def product_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PCO4612_0_double_response",
            "quantity": "source_test_product",
            "formula": "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)",
            "current_status": "SOURCE_AND_TEST_ENVELOPES_READY_VALUES_MISSING",
            "source_anchor": "QXT4612_4_product_handoff;QBAR4611_4_product_handoff",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PCO4612_1_alpha_feed",
            "quantity": "alpha_bulk(lambda_X)",
            "formula": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT*tau_R10 + alpha_tail_abs",
            "current_status": "BLOCKED_BY_QBAR_KX_QBARXT_TAU_AND_BOUND",
            "source_anchor": "QXT2673_3_alpha_feed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PCO4612_2_coupling_firewall",
            "quantity": "coupling_product_claim_gate",
            "formula": "no local test can score until Qbar_XH, qbar_XT, K_X, Z_X, M_H_ref, m_T and arena tau are all sourced",
            "current_status": "PRODUCT_GATE_NOT_SCORE_READY",
            "source_anchor": "CG2673_2_first_coefficient;CG2673_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def priority_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "priority": 1,
            "target_quantity": "qbar_constants, qbar_marker, s_alpha b_alpha",
            "why_first": "these are the ordinary matter/EM/clock channels most likely to be scrutinized and most likely to contaminate WEP, clock and R10 tests",
            "candidate_sources": "QBC3095_1_qbar_constants;MAT2673_1_atomic_masses;MAT2673_2_EM;QBC3095_2_qbar_marker",
            "acceptance_gate": "each matter/EM/clock/material marker is quotient-owned with Lie_v theta_A=0 or has sourced sensitivity/coefficient rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 2,
            "target_quantity": "qbar_geom, c_g, b_dis",
            "why_first": "this is the direct local-GR route: if ordinary matter sees only the descended observed metric/coframe, qbar_geom can zero cleanly",
            "candidate_sources": "QBC3095_0_qbar_geom;QT4603_0_geom;JQD2158_0_geom",
            "acceptance_gate": "observed metric/coframe descent proof or source-backed Weyl/disformal bounds",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 3,
            "target_quantity": "hidden frame F_X_prime/disformal_coeff",
            "why_first": "a hidden matter frame can mimic a fifth-force coupling even when the visible chain rule passes",
            "candidate_sources": "JX2673_4_hidden_frame;MAT2673_3_hidden_frame;QXT2673_2_hidden_frame",
            "acceptance_gate": "hidden frame absent/factors through q or finite coefficient row is sourced",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 4,
            "target_quantity": "qbar_source_weight and qbar_nonH",
            "why_first": "source-only weights and non-Hilbert tails are the coupling loophole that can survive ordinary metric descent",
            "candidate_sources": "QBC3095_3_qbar_source_weight;QBC3369_2_nonHilbert;JQD2158_4_nonHilbert",
            "acceptance_gate": "universal source-current theorem or numeric hidden-tail/source-weight bound",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 5,
            "target_quantity": "qbar_support, qbar_boundary, qbar_domain, qbar_readout",
            "why_first": "these prevent post-readout or domain changes from being mistaken for physics",
            "candidate_sources": "QBC3369_3_support;QBC3369_4_boundary;QBC3369_5_domain;JQD2158_6_readout",
            "acceptance_gate": "fixed support/domain/readout certificates or explicit coefficient bounds",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 6,
            "target_quantity": "K_X, Z_X, tau_R10/tau_PPN/tau_clock/tau_orbital",
            "why_first": "after qbar_XT, the product still needs arena kernels and propagator normalization before scoring",
            "candidate_sources": "QXT2673_3_alpha_feed;4611 product handoff",
            "acceptance_gate": "arena-specific source-backed product rows and bound curves",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4612_0_no_public_push",
            "rule": "work stays local/private; no GitHub push, no public repo mutation",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4612_1_no_WEP_wording_proof",
            "rule": "universality/equivalence-principle language is not accepted as qbar_XT=0 proof without channel descent",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4612_2_no_marker_hiding",
            "rule": "masses, alpha_EM, clocks, material labels and readout markers must be zeroed or bounded explicitly",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4612_3_no_component_cancellation",
            "rule": "absolute component envelope forbids cancellation between geometry, marker, hidden, boundary/domain and readout channels",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4612_0_matter_markers",
            "blocks": "qbar_XT zero/local-GR claim",
            "missing": "constant/material/EM/clock vertical silence or numeric coefficient rows",
            "resolution": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4612_1_geometry_frame",
            "blocks": "visible matter response zero",
            "missing": "observed metric/coframe descent or Weyl/disformal bounds",
            "resolution": "prove Lie_v ghat=0 from q descent or source c_g/b_dis rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4612_2_hidden_tail",
            "blocks": "qbar_XT bound",
            "missing": "non-Hilbert/source-weight/hidden-frame/support/domain/readout coefficients",
            "resolution": "fill qbar_XT priority queue with exact-zero or source-backed rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4612_3_product",
            "blocks": "arena testing",
            "missing": "K_X, Z_X and tau projections plus Qbar_XH/qbar_XT numeric/source rows",
            "resolution": "product coupling gate after qbar_XT channel work",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4612_0_source_traceability",
            "requirement": "every cited qbarXT source path exists and every cited row needle is found",
            "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4612_1_component_zero_or_bound",
            "requirement": "every qbar_XT component is exact-zero signed or source-backed numeric with units",
            "current_status": "BLOCKED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4612_2_marker_EM_descent",
            "requirement": "masses, clocks, material labels and alpha_EM/charge constants are vertical-silent or bounded",
            "current_status": "BLOCKED_NEXT_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4612_3_product_ready",
            "requirement": "Qbar_XH, qbar_XT, K_X, Z_X and arena tau rows are all claim-valid",
            "current_status": "BLOCKED_PRODUCT_NOT_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "meaning": "qbar_XT is now one auditable matter/test-body response envelope with explicit visible, marker, hidden-tail and readout/domain channels.",
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "The test-body coupling side is no longer scattered across older R10/q_loc rows; it is now a single qbar_XT response envelope and priority queue.",
        "what_did_not_move": "No qbar_XT zero, local-GR, Newton, Maxwell, R10, WEP, clock, PPN or orbital claim; components remain symbolic until exact-zero or source-backed.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "The qbar_XT envelope says the nearest derivational pressure point is ordinary matter markers: masses, EM/fine-structure, clocks and material labels.",
        "derive_first": "prove theta_A vertical silence or quotient ownership channel-by-channel for matter, EM, clock and material markers",
        "fallback": "stage first source-backed qbar_XT coefficient rows with units and source paths",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4612 - `qbar_XT` Test-Body Response Envelope Or First Source-Backed Input

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint does for the test-body side what `4611` did for `Qbar_XH`. The compact contract is:

```text
qbar_XT := M_T^-1 |delta_vX S_T|
```

with the no-cancellation envelope

```text
|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|.
```

The result is useful but not claimable. It identifies exactly where the coupling can still hide: matter constants, EM/fine-structure, clocks, material markers, hidden frames, source weights, domain/support shifts and readout selectors.

## Source Register

{markdown_table(tables["sources"])}

## `qbar_XT` Response Theorem

{markdown_table(tables["theorem"])}

## Visible Matter Response

{markdown_table(tables["visible"])}

## Marker/Constant/EM Response

{markdown_table(tables["marker"])}

## Hidden/Source-Tail Response

{markdown_table(tables["hidden"])}

## Boundary/Domain/Readout Response

{markdown_table(tables["boundary"])}

## Product Coupling Handoff

{markdown_table(tables["product"])}

## First Source-Backed Priority Queue

{markdown_table(tables["priority"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The next derivation attempt should attack `theta_A` channel-by-channel: masses, EM/fine-structure, clocks, material labels and source/readout markers. If they do not descend cleanly, they must become explicit coefficient rows.

Private nonclaim. No GitHub action. No R10, WEP, PPN, clock, orbital, Newton, Maxwell or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 628 - `qbar_XT` Test-Body Response Envelope

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Test-Body Response Definition

The test-body/matter response is treated as

```text
qbar_XT := M_T^-1 |delta_vX S_T|
```

in the same normalization used by the source-test product.

The expanded absolute envelope is

```text
|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|.
```

The exact-zero branch is

```text
Lie_v ghat=0,
Lie_v theta_A=0,
no hidden Weyl/disformal frame,
no source-only weights or non-Hilbert tails,
fixed support/domain/readout,
all in the same parent branch.
```

## Product Link

The local source-test product remains

```text
|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T).
```

## Status

This addendum makes the coupling hunt sharper. It does not zero `qbar_XT`; it makes every surviving channel explicit enough to attack or source.

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
    add("VAL4612_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, VISIBLE_CSV, MARKER_CSV, HIDDEN_CSV, BOUNDARY_CSV, PRODUCT_CSV,
        PRIORITY_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        csv_details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4612_01_csv_parse", csv_ok, ";".join(csv_details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    marker_text = "\n".join(str(row) for row in tables["marker"])
    hidden_text = "\n".join(str(row) for row in tables["hidden"])
    boundary_text = "\n".join(str(row) for row in tables["boundary"])
    priority_text = "\n".join(str(row) for row in tables["priority"])
    product_text = "\n".join(str(row) for row in tables["product"])
    add("VAL4612_02_variational_definition", "qbar_XT := M_T^-1 |delta_{v_X} S_T|" in theorem_text, "qbar_XT variational definition present")
    add("VAL4612_03_component_envelope", "|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|" in theorem_text, "component envelope present")
    add("VAL4612_04_marker_EM_explicit", "alpha_EM" in marker_text and "MISSING_EM_DESCENT_CERTIFICATE" in marker_text, "EM/marker channels explicit")
    add("VAL4612_05_hidden_tail_explicit", "F_X_prime" in hidden_text and "qbar_nonH" in hidden_text, "hidden tail channels explicit")
    add("VAL4612_06_boundary_readout_explicit", "qbar_readout" in boundary_text and "qbar_domain" in boundary_text, "boundary/domain/readout channels explicit")
    add("VAL4612_07_product_handoff", "alpha_bulk(lambda_X)" in product_text and "K_X" in priority_text, "product and arena handoff present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4612_08_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4612_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4612_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4612_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4612_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4612_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4612_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4612_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4612_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4612_OVERALL", all(row["status"] == "PASS" for row in rows), "4612 qbar_XT test-body response envelope")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "visible": visible_rows(now),
        "marker": marker_rows(now),
        "hidden": hidden_rows(now),
        "boundary": boundary_rows(now),
        "product": product_rows(now),
        "priority": priority_rows(now),
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
    write_csv(VISIBLE_CSV, tables["visible"])
    write_csv(MARKER_CSV, tables["marker"])
    write_csv(HIDDEN_CSV, tables["hidden"])
    write_csv(BOUNDARY_CSV, tables["boundary"])
    write_csv(PRODUCT_CSV, tables["product"])
    write_csv(PRIORITY_CSV, tables["priority"])
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
## PPC4161 Local Addendum - qbar_XT Test-Body Response Envelope

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The test-body side is now compacted as `qbar_XT := M_T^-1 |delta_vX S_T|` with the absolute envelope `|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|`. This is the anti-smuggling counterpart to the `Qbar_XH` source-side envelope: matter constants, EM/fine-structure, clocks, material labels, hidden frames, source weights, support/domain and readout maps must be zeroed or explicitly bounded.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - qbar_XT Test-Body Response Envelope

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local-GR packet now has source and test response envelopes: `Qbar_XH` and `qbar_XT`. The next pressure point is the marker/constant/EM channel because it is where WEP, clocks, alpha_EM and material tests will attack the framework first.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4612 validation failed: {failed}")
    print(f"4612 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
