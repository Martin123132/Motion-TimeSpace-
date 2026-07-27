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

CHECKPOINT = "4603"
CLAIM_ID = "L-445"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_TEST_INVARIANT_PRODUCT_GATE_4603"
MARKER = "PPC4161_SOURCE_TEST_CHARGE_INVARIANT_PRODUCT_OR_FIRST_NUMERIC_BOUND_ROW_4603"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_TEST_CHARGE_INVARIANT_PRODUCT_GATE_4603"
DECISION = "SOURCE_TEST_INVARIANT_PRODUCT_DERIVED_SCHEMA_READY_NONCLAIM"
NEXT_TARGET = "4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"

DOC_PATH = POST / "4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
FORMAL_PATH = FORMAL / "619-PPC4161-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4603_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_INVARIANT_PRODUCT_THEOREM.csv"
QBARXH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXH_FACTOR_ROWS.csv"
QBARXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXT_FACTOR_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_IXST_PRODUCT_BOUND_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_ARENA_SCORE_INSERT_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4603_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4603_VALIDATION.csv"

DOC_4602 = POST / "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"
FORMAL_618 = FORMAL / "618-PPC4161-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"
CSV_4602_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4602_NEXT_TARGET.csv"
CSV_4602_INVARIANT = SOURCE_DIR / "P8_Y5_R2FR_4602_INVARIANT_SCORE_LAW.csv"
CSV_4602_SCORE = SOURCE_DIR / "P8_Y5_R2FR_4602_SCORE_VECTOR_RANGE_UPDATE.csv"
CSV_4602_MISSING = SOURCE_DIR / "P8_Y5_R2FR_4602_REMAINING_RANGE_INPUT_BLOCKERS.csv"
CSV_2663_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_CHARGE_NORMALIZATION_2663_QBAR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"
CSV_2664_GATE = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_INPUT_GATE.csv"
CSV_2664_QBAR = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"
CSV_2664_ZERO = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_ZERO_PROOF_AUDIT.csv"
CSV_2665_LOCK = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
CSV_2665_DENOM = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"
CSV_2665_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_QBARXH_LOCK_TEMPLATE_NONCLAIM.csv"
CSV_2937_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_2937_QBAR_TAU_R10_PROJECTION_CONTRACT.csv"
CSV_2938_GATE = SOURCE_DIR / "P8_Y5_R2FR_2938_QBAR_TAU_FIRST_VALUE_GATE.csv"
CSV_1848_SCHEMA = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1848_QBARXT_HANDOFF_SCHEMA.csv"
CSV_1849_BOUND = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1849_BOUNDED_QBARXT_ROW_SCHEMA.csv"
CSV_1849_COMPONENTS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv"
CSV_1850_TOTAL = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1850_QBARXT_TOTAL_ENVELOPE.csv"
CSV_2101_COUPLING = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2101_QBARXT_COUPLING_ROWS.csv"
CSV_2158_DECOMP = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv"
CSV_2956_BOUND = SOURCE_DIR / "P8_Y5_R2FR_2956_QBARXT_BOUND_ROW_NONCLAIM.csv"
CSV_3369_ZERO = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_SOURCE_ZERO_THEOREM.csv"
CSV_3369_COMPONENTS = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_COMPONENT_ROWS_NONCLAIM.csv"
CSV_3369_LAW = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_BOUND_LAW.csv"
CSV_4418_GM = SOURCE_DIR / "P8_Y5_R2FR_4418_MASS_FLUX_GM_CLOSURE_OUTPUT.csv"
CSV_4440_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"
CSV_4462_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4462_SOURCE_COUPLING_THEOREM.csv"
CSV_4462_NEWTON = SOURCE_DIR / "P8_Y5_R2FR_4462_NEWTON_SOURCE_LAWS.csv"
CSV_4465_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4465_SOURCE_CHARGE_DERIVATION.csv"
CSV_4589_MHREF = SOURCE_DIR / "P8_Y5_R2FR_4589_MHREF_QBASIC_THEOREM.csv"
CSV_4589_REF = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_BLIND_REFERENCE_CLAUSES.csv"
CSV_4591_TAU = SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv"

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


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


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
        "domain": "local_gr_empirical_interface",
        "claim": "4603 derives the source/test invariant product needed after the 4602 normalization gate: finite-range scoring must use a source-side Hamiltonian charge times a test-body response divided by the same field stiffness, not separately tuned raw charges.",
        "current_evidence": "Generated invariant product theorem, Qbar_XH factor rows, qbar_XT factor rows, I_X^ST bound rows, arena insertion rows, blockers, controls and validation.",
        "status": "source_test_invariant_product_schema_ready_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a missing Qbar_XH denominator/projector lock or a conditional qbar_XT zero theorem as a numeric alpha/local-GR pass; or absorbing source/test factors into fitted G after the fact.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until Qbar_XH, qbar_XT, Z_X/K_X, tau and tails are either exact zero in one parent branch or source-backed numeric rows.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4603_00_4602_doc", DOC_4602, "I_X^ST", "4602 handoff: invariant product is the next object."),
        ("SRC4603_01_618_formal", FORMAL_618, "Qbar_XS qbar_XT/Z_X", "formal normalization-invariant handoff."),
        ("SRC4603_02_4602_next", CSV_4602_NEXT, "4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md", "machine next target."),
        ("SRC4603_03_4602_invariant", CSV_4602_INVARIANT, "INV4602_1_source_product", "source-product invariant score law."),
        ("SRC4603_04_4602_score", CSV_4602_SCORE, "alpha_X(lambda_X)", "arena score uses invariant alpha law."),
        ("SRC4603_05_4602_missing", CSV_4602_MISSING, "MIS4602_4_source_product", "explicit missing invariant product blocker."),
        ("SRC4603_06_2663_template", CSV_2663_TEMPLATE, "QROW2663_5_alpha_product", "older alpha product template."),
        ("SRC4603_07_2664_gate", CSV_2664_GATE, "QBAR_XH_NOT_CLAIM_READY", "Qbar_XH gate verdict."),
        ("SRC4603_08_2664_qbar", CSV_2664_QBAR, "QXH2664_3_projected_Qbar", "source-side Qbar first row."),
        ("SRC4603_09_2664_zero", CSV_2664_ZERO, "SOURCE_CURRENT_ZERO_NOT_PARENT_SIGNED", "Qbar zero proof failed/currently conditional."),
        ("SRC4603_10_2665_lock", CSV_2665_LOCK, "HLOCK2665_0_target", "Hamiltonian/PiM/MHref lock contract."),
        ("SRC4603_11_2665_denom", CSV_2665_DENOM, "PDG2665_0_same_frame", "denominator/projector gate."),
        ("SRC4603_12_2665_template", CSV_2665_TEMPLATE, "QbarXH_locked", "nonclaim lock template."),
        ("SRC4603_13_2937_contract", CSV_2937_CONTRACT, "R10C2937_0_Qbar_XH", "R10 Qbar/tau projection contract."),
        ("SRC4603_14_2938_gate", CSV_2938_GATE, "FVG2938_0_MHref", "first-value MHref gate."),
        ("SRC4603_15_1848_schema", CSV_1848_SCHEMA, "QBH1848_0_conditional_chain_rule", "test-side chain-rule zero handoff."),
        ("SRC4603_16_1849_bound", CSV_1849_BOUND, "BQT1849_0_visible_geometry", "bounded qbar row schema."),
        ("SRC4603_17_1849_components", CSV_1849_COMPONENTS, "qbar_geom", "test-side component envelope."),
        ("SRC4603_18_1850_total", CSV_1850_TOTAL, "qbar_XT_bound_abs", "test-side total absolute envelope."),
        ("SRC4603_19_2101_coupling", CSV_2101_COUPLING, "QBR2101_5_total_guard", "qbar coupling rows."),
        ("SRC4603_20_2158_decomp", CSV_2158_DECOMP, "JQD2158_7_total_abs_guard", "J_X/qbar decomposition."),
        ("SRC4603_21_2956_bound", CSV_2956_BOUND, "qbar_XT_abs", "R2FR qbar bound row."),
        ("SRC4603_22_3369_zero", CSV_3369_ZERO, "qbar_XT=0", "conditional qbar source-zero theorem."),
        ("SRC4603_23_3369_components", CSV_3369_COMPONENTS, "QBC3369_TOTAL", "current qbar component total."),
        ("SRC4603_24_3369_law", CSV_3369_LAW, "BQL3369_0_total_abs_guard", "current qbar bound law."),
        ("SRC4603_25_4418_gm", CSV_4418_GM, "Poisson", "Newton/GM closure context."),
        ("SRC4603_26_4440_source", CSV_4440_SOURCE, "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "source-charge closure context."),
        ("SRC4603_27_4462_theorem", CSV_4462_THEOREM, "SCT4462_5_scalar_source_coupling", "source coupling theorem."),
        ("SRC4603_28_4462_newton", CSV_4462_NEWTON, "Newton", "Newton source law context."),
        ("SRC4603_29_4465_source", CSV_4465_SOURCE, "DER4465_0_definition", "material/source response law."),
        ("SRC4603_30_4589_mhref", CSV_4589_MHREF, "M_H_ref", "M_H_ref/q-basic theorem."),
        ("SRC4603_31_4589_ref", CSV_4589_REF, "H_ref", "source-blind reference clauses."),
        ("SRC4603_32_4591_tau", CSV_4591_TAU, "e_obs", "tau/e_obs lock theorem."),
        ("SRC4603_33_claim_444", CLAIMS_PATH, "L-444", "claim-register handoff from 4602."),
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


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "IP4603_0_field_rescaling_contract",
            "statement": "After 4602, a finite-range alpha score is not allowed to depend on raw Qbar_XH, raw qbar_XT or raw Z_X separately.",
            "formula": "X=a X_prime => Z_prime=a^2 Z_X, Qbar_prime=a Qbar_XH, qbar_prime=a qbar_XT; Qbar_XH qbar_XT/Z_X is invariant",
            "derivation": "Both source and test charges are functional derivatives with one insertion of X, so they scale linearly under field renormalization, while the quadratic stiffness scales as a^2.",
            "consequence": "Score rows must use I_X^ST or an explicitly equivalent convention; naked Qbar_XH and qbar_XT rows are bookkeeping only.",
            "status": "DERIVED_EXACT_NORMALIZATION_GAUGE_LAW",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "IP4603_1_invariant_product_definition",
            "statement": "The R10/PPN finite-range source/test object is the dimensionless product of a source-side Hamiltonian charge and a test-body response divided by the same field stiffness and Newtonian normalization.",
            "formula": "I_X^ST(lambda_X)=Qbar_XH(lambda_X) qbar_XT(lambda_X)/(4*pi Z_X G_N M_H_ref m_T)",
            "derivation": "Solve (-Z_X nabla^2+M_X^2)X=rho_X with a Yukawa Green kernel and compare the induced test energy qbar_XT X to -G_N M_H_ref m_T/r.",
            "consequence": "lambda_X controls range; I_X^ST controls amplitude; K_X/tau rows are convention and arena-transfer wrappers.",
            "status": "DERIVED_CONDITIONAL_ON_PARENT_CHARGE_DEFINITIONS",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "IP4603_2_source_factor_contract",
            "statement": "The source factor is not a fitted galaxy/cosmology amplitude; it must descend from the Hamiltonian source charge and the Pi_M/M_H_ref lock.",
            "formula": "Qbar_XH=Pi_M^H[Q_bulk_X^H+Q_edge_X^H+Q_shadow_X^H]/M_H_ref",
            "derivation": "Use the 2664-2665 source-current and Hamiltonian/PiM contracts, with edge and shadow pieces kept separate under an absolute envelope.",
            "consequence": "Missing M_H_ref/Pi_M/domain locks block source-side numeric rows before qbar_XT details can produce a claim.",
            "status": "CONTRACT_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "IP4603_3_test_factor_contract",
            "statement": "The test-body factor is zero only if the ordinary matter action, observed coframe and marker constants descend through the parent quotient in the same branch.",
            "formula": "qbar_XT=0 if X in ker(Dq), e_obs=Obs_e(q(Phi)), S_matter=Sbar[Psi,e_obs,theta(q)], Lie_X theta=0, and hidden/boundary tails vanish",
            "derivation": "Lie_X S_matter vanishes by the chain rule only when every visible readout and material marker is q-basic; otherwise use the qbar component envelope.",
            "consequence": "WEP/common universality is not enough; qbar_XT needs a zero theorem or a sourced bound.",
            "status": "VALID_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "IP4603_4_product_zero_or_bound",
            "statement": "The invariant product is exact-zero only if either the source charge or the test response is exact-zero in the same parent branch; otherwise the claim-safe object is an absolute product bound.",
            "formula": "Qbar_XH=0 or qbar_XT=0 => I_X^ST=0; otherwise |I_X^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_X| G_N M_H_ref m_T)",
            "derivation": "This is a direct product law plus triangle inequality; no cancellation credit is allowed between source, test, edge, shadow, boundary or readout pieces.",
            "consequence": "The local branch now has a concrete amplitude gate: prove one factor zero, or fill both factor envelopes and score against R10/PPN/clocks/orbits.",
            "status": "DERIVED_PRODUCT_GATE_NONCLAIM",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbarxh_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QH4603_0_bulk",
            "factor": "Q_bulk_XH(lambda)",
            "definition": "parent Hamiltonian source current integrated over the source worldtube/domain",
            "zero_route": "source current absent in the selected parent branch and domain selector is q-basic",
            "bound_formula": "|Q_bulk_XH| <= integral_W |J_XH| dmu_H",
            "required_inputs": "parent J_XH; W_source; same tau; measure; units; source path",
            "current_status": "MISSING_PARENT_SOURCE_CURRENT_AND_DOMAIN",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_2665_LOCK}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QH4603_1_edge",
            "factor": "Q_edge_XH(lambda)",
            "definition": "source edge/contact/interface contribution before Pi_M projection",
            "zero_route": "compact interior collar plus no source-support edge/interface term",
            "bound_formula": "|Q_edge_XH| <= |epsilon_edge_source|",
            "required_inputs": "edge support theorem or sourced edge bound with units",
            "current_status": "MISSING_EDGE_ZERO_OR_BOUND",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_2665_LOCK}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QH4603_2_shadow",
            "factor": "Q_shadow_XH(lambda)",
            "definition": "non-Hilbert/shadow source-current contribution before Pi_M projection",
            "zero_route": "no direct non-Hilbert source slot plus shadow silence in the same branch",
            "bound_formula": "|Q_shadow_XH| <= |epsilon_shadow_source|",
            "required_inputs": "non-Hilbert zero theorem or sourced shadow current envelope",
            "current_status": "MISSING_SHADOW_SOURCE_ZERO_OR_BOUND",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_ZERO}; {CSV_2665_LOCK}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QH4603_3_projected_source_charge",
            "factor": "Qbar_XH(lambda)",
            "definition": "source-side Hamiltonian charge per reference mass after Pi_M projection",
            "zero_route": "all source pieces zero, or Pi_M projects them to zero, with M_H_ref locked positive",
            "bound_formula": "|Qbar_XH|_abs <= |Pi_M^H|(|Q_bulk|+|Q_edge|+|Q_shadow|)/M_H_ref_lower",
            "required_inputs": "Pi_M^H; M_H_ref_lower; Q_bulk; Q_edge; Q_shadow; fixed reference frame",
            "current_status": "MISSING_MHREF_PIM_AND_SOURCE_COMPONENT_VALUES",
            "units": "parent_X_charge_per_mass",
            "source_paths": f"{CSV_2665_LOCK}; {CSV_2938_GATE}; {CSV_4589_MHREF}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbarxt_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QT4603_0_geom",
            "factor": "qbar_geom",
            "definition": "ordinary test-body X response from observed coframe/Weyl/disformal leakage",
            "zero_route": "Lie_X e_obs=0 by quotient-owned observed coframe",
            "bound_formula": "|qbar_geom| <= |tau_g c_g| + |tau_dis b_dis|",
            "required_inputs": "observed coframe descent; Weyl/disformal coefficients; test profile",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "source_paths": f"{CSV_1849_COMPONENTS}; {CSV_3369_COMPONENTS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QT4603_1_marker",
            "factor": "qbar_marker",
            "definition": "X response of material constants, masses, EM constants, clocks and readout markers",
            "zero_route": "Lie_X theta_A=0 for all ordinary marker constants in the same parent branch",
            "bound_formula": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "required_inputs": "no-marker theorem or numeric sensitivities for each marker family",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "source_paths": f"{CSV_1849_COMPONENTS}; {CSV_2956_BOUND}; {CSV_3369_COMPONENTS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QT4603_2_nonHilbert",
            "factor": "qbar_nonH",
            "definition": "non-Hilbert/source-shadow test-response channel",
            "zero_route": "ordinary matter functor has no non-Hilbert source slot and hidden tails vanish",
            "bound_formula": "|qbar_nonH| <= |q_nonH| + |J_shadow|/|J_H|",
            "required_inputs": "no direct source slot theorem or numeric hidden-tail envelope",
            "current_status": "MISSING_NO_DIRECT_SOURCE_SLOT_OR_NUMERIC_BOUND",
            "source_paths": f"{CSV_2158_DECOMP}; {CSV_3369_COMPONENTS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QT4603_3_support_boundary_domain",
            "factor": "qbar_support + qbar_boundary + qbar_domain",
            "definition": "support/worldtube, boundary/contact and projector/domain variation of the test response",
            "zero_route": "source support and Pi_M/domain are parent-fixed q-basic maps with compact boundary silence",
            "bound_formula": "|qbar_support|+|qbar_boundary|+|qbar_domain| <= |Delta_W|+|epsilon_boundary|+|epsilon_projector|",
            "required_inputs": "fixed support theorem; boundary/contact bound; projector/domain Ward closure",
            "current_status": "MISSING_SUPPORT_BOUNDARY_PROJECTOR_VALUES",
            "source_paths": f"{CSV_2158_DECOMP}; {CSV_3369_COMPONENTS}; {CSV_3369_LAW}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "factor_id": "QT4603_4_total_guard",
            "factor": "qbar_XT_bound_abs",
            "definition": "absolute no-cancellation envelope for the test-body X response",
            "zero_route": "all qbar components zero in the same parent branch",
            "bound_formula": "|qbar_XT| <= |qbar_geom|+|qbar_marker|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|",
            "required_inputs": "all component values or exact-zero certificates",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "source_paths": f"{CSV_3369_LAW}; {CSV_3369_COMPONENTS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def product_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "IX4603_0_zero_branch",
            "quantity": "I_X^ST",
            "formula": "Qbar_XH=0 or qbar_XT=0 => I_X^ST=0",
            "required_inputs": "same-branch source zero or same-branch test response zero; lambda_X branch lock",
            "current_status": "CONDITIONAL_THEOREM_ONLY_NOT_PARENT_SIGNED",
            "numeric_value": "MISSING",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
            "notes": "This is the desired clean local-GR route, but current Qbar/qbar zero theorems are conditional rather than parent-signed together.",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "IX4603_1_absolute_product_bound",
            "quantity": "|I_X^ST|_bound",
            "formula": "|I_X^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_X| G_N M_H_ref m_T)",
            "required_inputs": "Qbar_XH_abs; qbar_XT_abs; Z_X or K_X convention; G_N frame; M_H_ref; m_T; lambda_X",
            "current_status": "BOUND_LAW_DERIVED_VALUES_MISSING",
            "numeric_value": "MISSING",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
            "notes": "This is the first claim-safe product row; it refuses cancellation between source and test-side pieces.",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "IX4603_2_R10_alpha_insert",
            "quantity": "alpha_R10(lambda_X)",
            "formula": "|alpha_R10| <= |K_X| |Qbar_XH|_abs |qbar_XT|_abs |tau_R10| + |alpha_tail_abs|",
            "required_inputs": "K_X; Qbar_XH_abs; qbar_XT_abs; tau_R10; alpha_tail_abs; real bound curve",
            "current_status": "SCHEMA_READY_NOT_SCORE_READY",
            "numeric_value": "MISSING",
            "units": "dimensionless Yukawa strength",
            "claim_allowed": False,
            "valid_for_claim": False,
            "notes": "Compatible with the older 2663 alpha row and the 4602 normalization-invariant law.",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "IX4603_3_no_G_absorption_guard",
            "quantity": "calibration_guard",
            "formula": "Do not absorb Qbar_XH qbar_XT/Z_X into fitted G_N or GM; calibrated Newtonian sector must be held fixed while residual finite-range pieces are scored.",
            "required_inputs": "Newton/GM calibration branch; fixed source mass definition; residual operator split",
            "current_status": "GUARD_ACTIVE",
            "numeric_value": "not_applicable",
            "units": "control",
            "claim_allowed": False,
            "valid_for_claim": False,
            "notes": "This prevents the product from becoming a post-hoc normalization knob.",
            "generated_utc": now,
        },
    ]


def arena_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4603_0_R10",
            "arena": "R10 short-range Yukawa",
            "score_insert": "alpha_R10(lambda_X)=K_X I_X^ST tau_R10 + alpha_tail_abs",
            "survival_condition": "real alpha(lambda) bound curve plus numeric/source-backed I_X^ST below bound",
            "current_status": "BLOCKED_BY_QBARXH_QBARXT_KX_TAU_TAIL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4603_1_PPN",
            "arena": "local PPN and local-GR recovery",
            "score_insert": "PPN residual vector receives finite-range source/test product and boundary/direct-current tails",
            "survival_condition": "I_X^ST zero or bounded below PPN residual thresholds in the same calibrated branch",
            "current_status": "BLOCKED_BY_PRODUCT_VALUES_AND_ARENA_KERNEL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4603_2_clock_WEP",
            "arena": "clocks, WEP and material response",
            "score_insert": "qbar_marker and material sensitivities feed qbar_XT unless quotient-owned constants zero them",
            "survival_condition": "same-branch no-marker theorem or numeric material/clock bounds",
            "current_status": "BLOCKED_BY_QBAR_MARKER_AND_MATERIAL_ROWS",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4603_3_orbital_GM",
            "arena": "orbital/GM calibration",
            "score_insert": "common Newtonian GM must be locked before residual finite-range product is scored",
            "survival_condition": "M_H_ref/Pi_M/source charge lock and no post-hoc G absorption",
            "current_status": "BLOCKED_BY_SOURCE_DENOMINATOR_AND_CALIBRATION",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "AR4603_4_EM_Poynting",
            "arena": "EM/Poynting/background-field leakage",
            "score_insert": "Hodge/readout/Poynting source tails stay explicit in qbar or J_X unless parent-zero",
            "survival_condition": "same-Hodge/source-support/readout zero theorem or sourced EM tail bound",
            "current_status": "BLOCKED_BY_OPEN_HODGE_SUPPORT_READOUT_TAILS",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4603_0_MHref_PiM_lock",
            "missing_object": "M_H_ref lower bound and Pi_M^H projector lock",
            "why_it_matters": "without this, Qbar_XH can absorb source/reference/boundary variation and the product is not a physical amplitude",
            "best_next_action": NEXT_TARGET,
            "source_paths": f"{CSV_2665_DENOM}; {CSV_2938_GATE}; {CSV_4589_MHREF}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4603_1_QbarXH_components",
            "missing_object": "Q_bulk, Q_edge, Q_shadow values or zero theorems",
            "why_it_matters": "source-side charge cannot be used in R10/PPN scoring without source current and edge/shadow ownership",
            "best_next_action": "after MHref/PiM lock, fill Qbar_XH components or prove source zero",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_2664_ZERO}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4603_2_qbarXT_zero_or_components",
            "missing_object": "same-branch qbar_XT zero certificate or component bounds",
            "why_it_matters": "test-side response is the other half of the invariant product and cannot be replaced by WEP/common-mode language",
            "best_next_action": "prove qbar chain-rule zero or fill qbar component envelope",
            "source_paths": f"{CSV_3369_ZERO}; {CSV_3369_LAW}; {CSV_3369_COMPONENTS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4603_3_K_tau_tail",
            "missing_object": "K_X, tau_R10 and alpha_tail_abs numeric/source-backed rows",
            "why_it_matters": "even a product bound does not become an arena score until the transfer kernel and tails are locked",
            "best_next_action": "use product row only after source/test factors are live",
            "source_paths": f"{CSV_2663_TEMPLATE}; {CSV_2937_CONTRACT}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4603_4_real_bound_comparison",
            "missing_object": "final real alpha(lambda), PPN, clock, orbital and EM arena bounds",
            "why_it_matters": "local-GR recovery is an empirical residual statement, not just an algebraic source/test product",
            "best_next_action": "defer until product row has parent-owned inputs",
            "source_paths": str(CSV_4602_SCORE),
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4603_0_no_placeholder_numeric",
            "control": "No numeric alpha/product row is emitted from symbolic or placeholder Qbar/qbar/K/tau inputs.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4603_1_no_cancellation",
            "control": "Use absolute envelopes for source/test factors; edge, shadow, boundary, marker and readout terms cannot cancel by assumption.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4603_2_no_G_absorption",
            "control": "Finite-range source/test product cannot be hidden in fitted G_N, GM, H_ref, M_H_ref or a readout normalization.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4603_3_same_branch",
            "control": "A Qbar zero theorem, qbar zero theorem, range input and arena kernel must refer to the same parent branch.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4603_0_source_factor",
            "promotion_requirement": "Qbar_XH is zero or bounded from parent-owned Q_bulk/Q_edge/Q_shadow, Pi_M and M_H_ref rows.",
            "current_status": "FAIL_MHREF_PIM_SOURCE_COMPONENTS_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4603_1_test_factor",
            "promotion_requirement": "qbar_XT is zero by the same parent quotient chain rule or bounded by all component rows.",
            "current_status": "FAIL_QBARXT_PARENT_SIGNATURE_OR_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4603_2_product_score",
            "promotion_requirement": "I_X^ST, K_X, lambda_X, tau_R10/PPN/clock/orbital kernels and tails are all source-backed and below bounds.",
            "current_status": "FAIL_PRODUCT_AND_ARENA_INPUTS_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4603_3_local_GR_claim",
            "promotion_requirement": "All local residuals vanish or are bounded in the same calibrated Newton/GR branch without post-hoc absorption.",
            "current_status": "FAIL_DO_NOT_CLAIM_LOCAL_GR",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "reason": "The exact invariant product and its zero/bound law are now derived, but Qbar_XH and qbar_XT are not parent-signed/numeric in the same branch.",
            "claim": "no R10/PPN/local-GR pass",
            "next_target": NEXT_TARGET,
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "status": DECISION,
            "what_moved": "The amplitude problem is no longer vague coupling language: it is a source/test product gate with a zero route and an absolute bound route.",
            "what_did_not_move": "No numeric I_X^ST, alpha_R10, PPN residual or local-GR pass is claimed.",
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The source-side denominator/projector lock is the sharpest first missing factor: without M_H_ref/Pi_M, Qbar_XH and therefore I_X^ST are not physically owned.",
            "derive_first": "derive M_H_ref positivity/reference lock and Pi_M same-frame projector silence, then insert Qbar_XH_abs",
            "fallback": "retain Qbar_XH_abs as nonclaim source factor with explicit MISSING_MHREF_PIM/source-component blockers",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4603 - Y5 R2FR Source/Test Charge Invariant Product Or First Numeric Bound Row

Generated: `{now}`

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Claim register row: `{CLAIM_ID}`
Previous target: `{DOC_4602}`

## Result

This checkpoint takes the 4602 correction seriously: the physical amplitude is not a raw source charge and not raw `Z_X`.

The derived finite-range product is:

```text
I_X^ST(lambda_X) =
    Qbar_XH(lambda_X) qbar_XT(lambda_X)
    / (4*pi Z_X G_N M_H_ref m_T)
```

with:

```text
Qbar_XH = Pi_M^H[Q_bulk_X^H + Q_edge_X^H + Q_shadow_X^H]/M_H_ref
```

and:

```text
|qbar_XT| <= |qbar_geom| + |qbar_marker| + |qbar_nonH|
             + |qbar_support| + |qbar_boundary| + |qbar_domain|.
```

The clean derivation route is now brutally simple:

```text
Qbar_XH = 0  or  qbar_XT = 0  =>  I_X^ST = 0.
```

If that cannot be parent-signed in one branch, the score-safe fallback is:

```text
|I_X^ST| <= |Qbar_XH|_abs |qbar_XT|_abs
            / (4*pi |Z_X| G_N M_H_ref m_T).
```

So this is a genuine narrowing of the coupling problem: the local route lives or dies on one product gate, not a cloud of loose coupling language.

## Private Decision

`{DECISION}`

No R10, PPN, clock, orbital, EM, Newton or local-GR pass is claimed. The immediate best target is `{NEXT_TARGET}`, because the source-side `M_H_ref/Pi_M` lock is upstream of any numeric `Qbar_XH` or `I_X^ST` row.

## Source Register

{markdown_table(tables["sources"])}

## Invariant Product Theorem

{markdown_table(tables["theorem"])}

## Qbar_XH Source Factor Rows

{markdown_table(tables["qbarxh"])}

## qbar_XT Test Factor Rows

{markdown_table(tables["qbarxt"])}

## I_X^ST Product Bound Rows

{markdown_table(tables["product"])}

## Arena Score Insert Rows

{markdown_table(tables["arena"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

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
    return f"""# PPC4161 619 - Source/Test Charge Invariant Product Or First Numeric Bound Row

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For a finite-range local mode `X`,

```text
(-Z_X nabla^2 + M_X^2)X = rho_X,
lambda_X = sqrt(Z_X/M_X^2).
```

Under a field redefinition `X=aX'`, both source and test charges scale linearly while the stiffness scales quadratically:

```text
Z' = a^2 Z_X,  Qbar'_XH = a Qbar_XH,  qbar'_XT = a qbar_XT.
```

Therefore the invariant amplitude object is:

```text
I_X^ST(lambda_X)=Qbar_XH(lambda_X) qbar_XT(lambda_X)/(4*pi Z_X G_N M_H_ref m_T).
```

The exact zero route is:

```text
Qbar_XH=0 or qbar_XT=0  =>  I_X^ST=0.
```

The bounded route is:

```text
|I_X^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_X| G_N M_H_ref m_T).
```

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4603_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4603_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")

    csv_paths = [SOURCE_REGISTER, THEOREM_CSV, QBARXH_CSV, QBARXT_CSV, PRODUCT_CSV, ARENA_CSV, BLOCKERS_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4603_02_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    add("VAL4603_03_invariant_product_defined", "I_X^ST(lambda_X)" in theorem_text and "Qbar_XH qbar_XT/Z_X" in theorem_text, "invariant product and rescaling law present")
    add("VAL4603_04_zero_or_bound_route", "Qbar_XH=0 or qbar_XT=0" in theorem_text and "|I_X^ST|" in theorem_text, "zero route and absolute product bound present")

    qh_text = "\n".join(str(row) for row in tables["qbarxh"])
    qt_text = "\n".join(str(row) for row in tables["qbarxt"])
    product_text = "\n".join(str(row) for row in tables["product"])
    add("VAL4603_05_source_factor_rows", "Q_bulk_XH" in qh_text and "Q_shadow_XH" in qh_text and "Qbar_XH" in qh_text, "Qbar source factors present")
    add("VAL4603_06_test_factor_rows", "qbar_geom" in qt_text and "qbar_marker" in qt_text and "qbar_XT_bound_abs" in qt_text, "qbar test factors present")
    add("VAL4603_07_product_rows_nonclaim", "|I_X^ST|_bound" in product_text and "alpha_R10" in product_text, "product and alpha insert rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "product_numeric_present"} and value is True:
                    all_false = False
    add("VAL4603_08_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4603_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4603_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4603_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4603_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4603_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4603_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4603_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4603_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4603_OVERALL", all(row["status"] == "PASS" for row in rows), "4603 source/test invariant product gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "qbarxh": qbarxh_rows(now),
        "qbarxt": qbarxt_rows(now),
        "product": product_rows(now),
        "arena": arena_rows(now),
        "blockers": blocker_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(QBARXH_CSV, tables["qbarxh"])
    write_csv(QBARXT_CSV, tables["qbarxt"])
    write_csv(PRODUCT_CSV, tables["product"])
    write_csv(ARENA_CSV, tables["arena"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
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
## PPC4161 Local Addendum - Source/Test Invariant Product Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The finite-range local amplitude is now routed through `I_X^ST = Qbar_XH qbar_XT/(4*pi Z_X G_N M_H_ref m_T)`. Exact local silence requires `Qbar_XH=0` or `qbar_XT=0` in the same parent branch; otherwise the branch must use the absolute product bound and arena kernels.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Source/Test Charge Invariant Product Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now has a concrete coupling gate: prove one side of the source/test product zero, or fill the absolute `I_X^ST` row before R10/PPN/clock/orbital scoring. No local-GR pass is inferred from symbolic factors.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4603 validation failed: {failed}")
    print(f"4603 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
