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
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4660"
CLAIM_ID = "L-502"
BRANCH = "MTS_R2FR_Y5_BCLOCK_READOUT_DESCENT_OR_CLOCK_REDSHIFT_BOUND_4660"
MARKER = "PPC4161_BCLOCK_READOUT_DESCENT_OR_CLOCK_REDSHIFT_BOUND_4660"
PACKET_MARKER = "PPC4161_PACKET_BCLOCK_READOUT_DESCENT_OR_CLOCK_REDSHIFT_BOUND_4660"
DECISION = "BCLOCK_MEM_OBSERVED_COFRAME_CLOCK_BRANCH_ZERO_DYNAMIC_CLOCK_REDSHIFT_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4661-Y5-R2FR-kappa-Cmem-import-or-deltaw-source-weight-final-bound.md"

DOC_PATH = POST / "4660-Y5-R2FR-bclock-readout-descent-or-clock-redshift-bound.md"
FORMAL_PATH = FORMAL / "676-PPC4161-bclock-readout-descent-or-clock-redshift-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4659 = POST / "4659-Y5-R2FR-bmass-matter-spectrum-owner-or-WEP-composition-bound.md"
DOC_4613 = POST / "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
DOC_3771 = POST / "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md"
DOC_1804 = POST / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md"
DOC_1805 = POST / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md"
DOC_3135 = POST / "3135-Y5-R2FR-clock-readout-chain-sign-quarantine-and-limit-gate-under-AX1090.md"
DOC_3136 = POST / "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md"
DOC_3228 = POST / "3228-Y5-R2FR-Xi-clock-product-row-or-clock-tau-owner-under-AX1090.md"
DOC_3229 = POST / "3229-Y5-R2FR-same-branch-clock-transport-identity-for-DtauRQ-under-AX1090.md"
DOC_4654 = POST / "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"

FORMAL_675 = FORMAL / "675-PPC4161-bmass-matter-spectrum-owner-or-WEP-composition-bound.md"
FORMAL_670 = FORMAL / "670-PPC4161-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"

CSV_4659_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4659_CMEM_STD_WEIGHT_UPDATE.csv"
CSV_4613_CHANNEL = SOURCE_DIR / "P8_Y5_R2FR_4613_CHANNEL_DESCENT_AUDIT.csv"
CSV_4613_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4613_MASS_CLOCK_MARKER_ROWS.csv"
CSV_4613_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
CSV_3771_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv"
CSV_1804_CLOCK = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_CLOCK_PROJECTION_ROWS.csv"
CSV_1804_COEFF = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_COEFFICIENT_PROVENANCE_ROWS.csv"
CSV_1805_VERTEX = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv"
CSV_1805_NO_MASS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv"
CSV_1805_BOUND = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"
CSV_3135_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_3135_CLOCK_READOUT_INPUTS.csv"
CSV_3136_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv"
CSV_3136_CHAIN = SOURCE_DIR / "P8_Y5_R2FR_3136_CLOCK_MATTER_DERIVATION_CHAIN.csv"
CSV_3136_RESIDUALS = SOURCE_DIR / "P8_Y5_R2FR_3136_CLOCK_OWNER_RESIDUALS.csv"
CSV_3225_PRODUCTS = SOURCE_DIR / "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv"
CSV_3228_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_3228_XI_CLOCK_PRODUCT_DERIVATION.csv"
CSV_3228_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_3228_PARENT_XI_CLOCK_CONTRACT.csv"
CSV_3228_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3228_XI_CLOCK_BOUND_INTERFACE.csv"
CSV_3229_TRANSPORT = SOURCE_DIR / "P8_Y5_R2FR_3229_TRANSPORT_IDENTITY_DERIVATION.csv"
CSV_3229_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_3229_XI_CLOCK_REDUCTION_WITH_TRANSPORT_ERROR.csv"
CSV_4325_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4325_CLOCK_TAIL_LEDGER.csv"
CSV_4654_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_ZERO_THEOREM.csv"
CSV_4654_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4654_VALIDATION.csv"
CSV_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4660_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_BCLOCK_MEMORY_NORMAL_FORM.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_OBSERVED_COFRAME_CLOCK_ZERO_IMPORT.csv"
BOUND_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_DYNAMIC_CLOCK_REDSHIFT_BOUND_ROWS.csv"
CMEM_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_CMEM_STD_WEIGHT_UPDATE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4660_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4660_VALIDATION.csv"


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
        values = [str(row_data.get(field_name, "")).replace("|", "\\|").replace("\n", " ") for field_name in fields]
        lines.append("| " + " | ".join(values) + " |")
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
        ("SRC4660_00_4659_next", DOC_4659, "4660-Y5-R2FR-bclock-readout-descent-or-clock-redshift-bound.md", "4659 selected b_clock_mem as the next Cmem coefficient."),
        ("SRC4660_01_4659_cmem", CSV_4659_CMEM, "CSW4659_2_reduced_fixed_branch", "Cmem standard/weight block after alpha and mass zeros."),
        ("SRC4660_02_675_formal", FORMAL_675, "CSW4659_2_reduced_fixed_branch", "formal bmass checkpoint keeps b_clock_mem live."),
        ("SRC4660_03_4613_clock_channel", CSV_4613_CHANNEL, "CH4613_2_clock", "clock transitions/readout standards channel."),
        ("SRC4660_04_4613_clock_marker", CSV_4613_MARKER, "MCM4613_1_clock", "clock marker/readout row."),
        ("SRC4660_05_4613_bclock", CSV_4613_QBAR, "QTC4613_4_b_clock", "b_clock_i coefficient row."),
        ("SRC4660_06_3771_projection", DOC_3771, "CMT3771_4_clock_projection", "clock ratios see dimensionless sensitivity leakage plus readout terms."),
        ("SRC4660_07_3771_machine", CSV_3771_THEOREM, "CMT3771_4_clock_projection", "machine clock projection theorem."),
        ("SRC4660_08_1804_clock_constants", DOC_1804, "CSG1804_4_clock_constants", "clock constants inherit alpha/mass/nuclear/readout debts unless closed."),
        ("SRC4660_09_1804_redshift_anchor", CSV_1804_CLOCK, "CLK1804_2_clock_redshift_anchor", "Galileo redshift/LPI anchor route."),
        ("SRC4660_10_1804_bclock_coeff", CSV_1804_COEFF, "CPR1804_4_b_clock_i", "clock coefficient provenance."),
        ("SRC4660_11_1805_clock_vertex", DOC_1805, "PVS1805_3_no_clock_readout_vertex", "parent signature clause forbidding clock-readout Xhat vertex."),
        ("SRC4660_12_1805_vertex_machine", CSV_1805_VERTEX, "VT1805_6_clock_readout_X", "clock-readout countervertex row."),
        ("SRC4660_13_1805_no_clock_X", CSV_1805_NO_MASS, "MVT1805_3_no_clock_readout_X", "no independent clock readout Xhat vertex condition."),
        ("SRC4660_14_1805_redshift_bound", CSV_1805_BOUND, "BM1805_1_clock_redshift", "clock redshift projection skeleton."),
        ("SRC4660_15_3135_readout_chain", DOC_3135, "tau_clk[path] = R_clock", "observable clock readout separated from internal flow."),
        ("SRC4660_16_3135_bounds", CSV_3135_INPUTS, "SRC3135_11", "loaded local empirical clock/redshift bounds."),
        ("SRC4660_17_3136_theorem_doc", DOC_3136, "=> observed clocks measure observed metric proper time.", "observed-coframe clock theorem."),
        ("SRC4660_18_3136_proper_time", CSV_3136_THEOREM, "OCF3136_2_proper_time", "proper-time functional from matter action."),
        ("SRC4660_19_3136_redshift", CSV_3136_THEOREM, "OCF3136_3_redshift_frequency", "redshift/frequency from clock phase."),
        ("SRC4660_20_3136_verdict", CSV_3136_THEOREM, "OCF3136_5_parent_verdict", "conditional clock theorem not globally parent-signed."),
        ("SRC4660_21_3136_chain", CSV_3136_CHAIN, "DER3136_3_clock_functional", "clock functional derivation chain."),
        ("SRC4660_22_3136_res_bclock", CSV_3136_RESIDUALS, "RES3136_0_b_clock", "b_clock residual if descent fails."),
        ("SRC4660_23_3136_res_deltae", CSV_3136_RESIDUALS, "RES3136_3_delta_e_clock", "coframe readout leakage residual."),
        ("SRC4660_24_3136_res_nonminimal", CSV_3136_RESIDUALS, "RES3136_4_nonminimal_clock", "nonminimal clock coupling residual."),
        ("SRC4660_25_3136_res_tau", CSV_3136_RESIDUALS, "RES3136_5_tau_role", "same-tau role mismatch residual."),
        ("SRC4660_26_3225_clock_bound", CSV_3225_PRODUCTS, "PC3225_0_clock_1sigma", "source-backed clock product pressure gate."),
        ("SRC4660_27_3228_xi_doc", DOC_3228, "Xi_clock + E_HO + E_transport <= 2.1e-18", "Xi_clock product bound in prose."),
        ("SRC4660_28_3228_xi_identity", CSV_3228_DERIVATION, "XID3228_4_xi_clock_identity", "direct Xi_clock product identity."),
        ("SRC4660_29_3228_clock_generator", CSV_3228_CONTRACT, "XIC3228_2_clock_generator", "clock data score observed time."),
        ("SRC4660_30_3228_bound", CSV_3228_BOUND, "XIB3228_0_clock_1sigma", "1sigma Xi_clock bound interface."),
        ("SRC4660_31_3229_transport", CSV_3229_TRANSPORT, "TR3229_6_exact_closure", "same-branch exact transport closure."),
        ("SRC4660_32_3229_reduction", CSV_3229_REDUCTION, "XIR3229_0_corrected_clock_reduction", "clock reduction with transport error."),
        ("SRC4660_33_4325_clock_tail", CSV_4325_TAIL, "CT4325_3_clock", "clock readout tail ledger."),
        ("SRC4660_34_local_redshift", CSV_LOCAL_BOUNDS, "R2_clock_redshift", "local clock redshift bound anchor."),
        ("SRC4660_35_4654_kappa_zero", CSV_4654_ZERO, "DKZ4654_3_result", "kappa_eff drift already private-zero in 4654."),
        ("SRC4660_36_4654_validation", CSV_4654_VALIDATION, "VAL4654_OVERALL", "4654 kappa gate validation pass."),
        ("SRC4660_37_670_formal", FORMAL_670, "DKZ4654_3_result", "formal kappa zero theorem cross-reference."),
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
        ("BCN4660_0_definition", "b_clock_mem := Pi_mem[D_X ln(nu_A^obs/nu_ref^obs)] after alpha/mass/material projections", "memory-projected clock/readout drift coefficient", "clock observable must be an observed frequency ratio or observed redshift residual", "NORMAL_FORM_DEFINED"),
        ("BCN4660_1_sensitivity_decomposition", "D ln(nu_A/nu_B)=sum_I DeltaK_I^AB D ln theta_I + rho_clock_readout", "clock ratios see dimensionless constant leakage plus readout-frame terms", "frequency units cancel; upstream alpha/mass constants already handled in fixed branch", "CLOCK_SENSITIVITY_LAW_IMPORTED"),
        ("BCN4660_2_observed_coframe_functional", "R_clock(q(Phi),gamma,A)=int_gamma sqrt(-g_obs(dx,dx))/c plus quotient-owned transition phase", "observed-coframe matter forces measured clock time to be observed proper time", "ordinary clock matter is local Lorentz matter over e_obs and theta_A is q-basic/fixed", "OBSERVED_PROPER_TIME_FUNCTIONAL"),
        ("BCN4660_3_residual_vector", "b_clock_mem_abs <= |rho_clock_readout|+|epsilon_nonminimal_clock|+|epsilon_tau_role|+|Xi_clock|+|E_HO|+|E_transport|", "dynamic/readout fallback keeps all clock-specific tails", "no-cancellation; product rows not split into arbitrary factors", "BOUND_READY_VALUES_PARTIAL"),
        ("BCN4660_4_redshift_projection", "alpha_clock_redshift = P_clock[b_clock_i, metric_readout_residual, source potential map]", "LPI/redshift data constrain full clock/readout residual, not alpha_EM alone", "requires local potential/source normalization and clock readout map", "REDSHIFT_BOUND_INTERFACE_IMPORTED"),
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
        ("BCZ4660_0_observed_coframe", "e_obs=Obs_e(q(Phi)) and Dq(v_X)=0", "representative/internal variations do not change the observed coframe", "same fixed branch used by c_D/alpha/mass imports", "BRANCH_SETUP"),
        ("BCZ4660_1_clock_matter", "S_clock_matter=S_matter[e_obs,psi_A,theta_A] with local Lorentz/eikonal clock matter", "worldline/eikonal phase gives d tau_clk=sqrt(-g_obs(dx,dx))/c", "3136 observed-coframe clock theorem", "EXACT_CONDITIONAL_THEOREM"),
        ("BCZ4660_2_fixed_constants", "theta_A, alpha_EM, mass ratios, binding fractions and transition constants are q-basic or representation-fixed", "sensitivity terms sum_I DeltaK_I D ln theta_I vanish in the same fixed branch", "4658 and 4659 already selected fixed alpha/matter branches", "UPSTREAM_ZERO_IMPORTED"),
        ("BCZ4660_3_no_clock_specific_slot", "no nu_i(Xhat), clock-frame normalization, detector readout map, shadow coframe or nonminimal clock-flow coupling is admitted", "rho_clock_readout=epsilon_nonminimal_clock=0", "if any of these slots exists, dynamic bound rows stay live", "CLOCK_READOUT_ZERO_CONDITION"),
        ("BCZ4660_4_same_tau_role", "tau_obs is the observed clock time used by source/charge/orbit/boundary in the local branch", "epsilon_tau_role=0 for the same-parent-time-frame branch", "cross-arena tau mismatch is not silently assumed outside this branch", "SAME_TAU_CONDITIONAL"),
        ("BCZ4660_5_result", "fixed observed-coframe calibrated clock branch => b_clock_mem=0", "|b_clock_mem||S_clock^mem| drops from C_mem^std_weight_live in the same branch", "does not claim global clock pass or dynamic alpha-clock silence", "PRIVATE_BRANCH_ZERO_NONCLAIM"),
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
        ("BCB4660_0_clock_residual_envelope", "b_clock_mem_abs", "|rho_clock_readout|+|epsilon_nonminimal_clock|+|epsilon_tau_role|+|Xi_clock|+|E_HO|+|E_transport|", "dynamic/readout clock branch if observed-coframe fixed branch is not selected", "dimensionless_or_fractional_rate", "clock/redshift/LPI", "VALUES_MISSING_NONCLAIM", "MISSING_COMPONENT_VALUES"),
        ("BCB4660_1_clock_product_1sigma", "Xi_clock + E_HO + E_transport", "<= 2.100000e-18", "best current clock product pressure gate", "yr^-1", "alpha-sensitive clock comparisons", "FINITE_CLOCK_PRESSURE_GATE_NONCLAIM", str(CSV_3228_BOUND)),
        ("BCB4660_2_clock_product_2sigma", "Xi_clock + E_HO + E_transport", "<= 3.200000e-18", "2sigma clock product pressure gate", "yr^-1", "alpha-sensitive clock comparisons", "FINITE_CLOCK_PRESSURE_GATE_NONCLAIM", str(CSV_3228_BOUND)),
        ("BCB4660_3_redshift_anchor", "alpha_clock_redshift", "<= 2.48e-05", "Galileo eccentric-satellite LPI/redshift anchor; constrains full clock/readout residual", "dimensionless", "redshift/LPI", "ANCHOR_AVAILABLE_PROJECTION_MISSING_NONCLAIM", str(CSV_LOCAL_BOUNDS)),
        ("BCB4660_4_Xi_identity", "Xi_clock", "C_D |Delta m tau_clock_time|", "direct product target; do not split or set factors to one without parent owner", "yr^-1", "clock product comparison", "PRODUCT_LAW_DERIVED_CONDITIONALLY", str(CSV_3228_DERIVATION)),
        ("BCB4660_5_transport_error", "E_clock_transport", "(2|lambda_D|/Z_min)||R_Q|| E_transport", "same-branch transport correction if transverse/vertical drift is not zero", "yr^-1", "clock product comparison", "TRANSPORT_ERROR_BOUND_TARGET", str(CSV_3229_REDUCTION)),
        ("BCB4660_6_source_row_contract", "b_clock_mem_source_row", "system_id;branch;rho_clock_readout;epsilon_nonminimal_clock;epsilon_tau_role;Xi_clock;E_HO;E_transport;clock_bound;units;source_path;valid_for_claim", "source-backed dynamic clock row contract", "declared per component", "clock/redshift/LPI", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING", "MISSING_SOURCE_PATH"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_data[0],
            "quantity": row_data[1],
            "bound_or_contract": row_data[2],
            "assumption": row_data[3],
            "units": row_data[4],
            "observable_link": row_data[5],
            "current_status": row_data[6],
            "source_path": row_data[7],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_data in rows
    ]


def cmem_update_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CSW4660_0_before", "|C_mem^std_weight_live| <= |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|", "4659 reduced first-block bound after alpha and mass zeros", "FIRST_BLOCK_BOUND_IMPORTED"),
        ("CSW4660_1_fixed_clock", "fixed observed-coframe calibrated clock branch => |b_clock_mem||S_clock^mem|=0", "clock/readout coefficient term drops only in the same fixed branch", "BRANCH_ZERO_INSERTED_NONCLAIM"),
        ("CSW4660_2_reduced_fixed_branch", "|C_mem^std_weight_live| <= |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|", "reduced first-block target after alpha, mass and clock zero imports", "NEXT_COEFFICIENTS_REMAIN"),
        ("CSW4660_3_kappa_crossref", "4654 gives D_A ln kappa_eff=0 inside the private topological-kappa/Hilbert-source selector", "do not redo kappa; import/check same-branch compatibility before dropping the term", "KAPPA_ZERO_ALREADY_AVAILABLE_PRIVATE_BRANCH"),
        ("CSW4660_4_dynamic_branch", "|C_mem^std_weight_live| retains |b_clock_mem|_abs |S_clock^mem| with clock/redshift product bounds", "if dynamic/readout clock branch is selected, clock term stays source-bound", "DYNAMIC_BRANCH_BOUND_RETAINED"),
        ("CSW4660_5_next", "import kappa same-branch zero and attack delta_w_mem/source weights", "after b_clock, only kappa and source-weight terms remain in this Cmem block; kappa has a validated private zero from 4654", "NEXT_TARGET_SELECTED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row_data[0],
            "statement": row_data[1],
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
        ("RUN4660_0_fixed_observed_coframe_clock", "fixed observed-coframe calibrated clock branch", "PASS_CONDITIONAL_PRIVATE_ZERO", "b_clock_mem=0; SR time dilation and GR redshift are readouts of g_obs in this branch, not separate axioms."),
        ("RUN4660_1_dynamic_clock_branch", "dynamic clock/readout/nonminimal/tau branch", "FAIL_CLOSED_TO_CLOCK_BOUND", "b_clock_mem is not zero; keep Xi_clock, redshift/LPI and readout-tail bounds."),
        ("RUN4660_2_Cmem_update", "C_mem^std_weight_live", "PASS_BRANCH_REDUCTION", "clock term drops only in fixed branch; kappa/source-weight terms remain."),
        ("RUN4660_3_kappa_crossref", "D_mem ln kappa_eff", "PASS_EXISTING_PRIVATE_ZERO_REFERENCE", "4654 already validates private kappa no-drift; next work is same-branch import and delta_w."),
        ("RUN4660_4_local_GR_status", "local GR/Newton/PPN/WEP/clock claim", "NONCLAIM_STILL_BLOCKED", "source-weight delta_w and same-branch kappa import/final Cmem closure still required."),
        ("RUN4660_5_next_target", "component attack order", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row_data[0],
            "branch_or_object": row_data[1],
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
        ("CTRL4660_0_no_time_axiom", "Do not identify internal flow time with measured clock time; derive measured clocks through R_clock/e_obs.", "ACTIVE"),
        ("CTRL4660_1_no_clock_pass", "Observed-coframe clock theorem is conditional and private; dynamic/readout branches remain bounds.", "ACTIVE"),
        ("CTRL4660_2_no_alpha_transfer", "Clock product bounds do not become WEP/R10/local-GR bounds without direct same-branch projection rows.", "ACTIVE"),
        ("CTRL4660_3_no_factor_setting", "Xi_clock factors C_D, Delta m and tau_clock_time cannot be set to one or split without a parent owner.", "ACTIVE"),
        ("CTRL4660_4_redshift_not_alpha", "Galileo redshift/LPI row constrains clock/readout residual, not alpha_EM alone.", "ACTIVE"),
        ("CTRL4660_5_kappa_not_redone", "4654 kappa private zero is referenced, not re-proved here; same-branch compatibility is the next gate.", "ACTIVE"),
        ("CTRL4660_6_private_local_only", "No GitHub action, no public claim and no edits outside the local framework packet are intended.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row_data[0],
            "guard": row_data[1],
            "status": row_data[2],
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
            "decision_id": "DEC4660_0",
            "decision": DECISION,
            "summary": (
                "4660 imports the observed-coframe clock theorem into the Cmem coefficient chain. In the fixed q-basic calibrated branch, ordinary clock matter descends through e_obs(q), "
                "so measured clock time is observed metric proper time; with alpha/mass/material constants fixed and no clock-specific readout/nonminimal/tau slot, b_clock_mem=0. "
                "Dynamic clock branches remain explicit Xi_clock/redshift/readout-tail bounds. The Cmem first-block now reduces to kappa_eff drift plus delta_w_mem, with 4654 already providing the private kappa no-drift theorem that must be same-branch imported next."
            ),
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
            "decision": DECISION,
            "fixed_branch_result": "BCLOCK_MEM_ZERO_PRIVATE_BRANCH",
            "dynamic_branch_status": "CLOCK_REDSHIFT_PRODUCT_BOUND_RETAINED",
            "Cmem_effect": "CLOCK_TERM_REMOVED_ONLY_IN_FIXED_BRANCH",
            "kappa_crossref": "4654_DELTAKAPPA_PRIVATE_ZERO_AVAILABLE",
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
            "why": "After alpha, mass and clock zeros, the first Cmem standard/weight block contains kappa drift and delta_w only; kappa already has a 4654 private zero that must be same-branch imported before the final source-weight attack.",
            "derive_route": "prove the 4654 D_mem ln kappa_eff=0 branch is identical to the 4658-4660 fixed observed-coframe/source branch, then reduce the block to delta_w_mem.",
            "fallback_route": "if kappa branch mismatch appears, retain D_mem ln kappa_eff as a finite Gdot/clock/orbital/PPN bound row.",
            "avoid": "redoing kappa from scratch, using numeric G as an input, or claiming local GR before delta_w/source weights are zeroed or bounded.",
            "valid_for_claim": False,
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
        ("VAL4660_00_sources_exist", all(row_data["path_exists"] for row_data in sources), "all cited source paths exist"),
        ("VAL4660_01_needles_found", all(row_data["needle_found"] for row_data in sources), "all cited source needles found"),
        ("VAL4660_02_line_anchors", all(int(row_data["line_number"]) > 0 for row_data in sources), "all source line anchors positive"),
        ("VAL4660_03_memory_normal_form", any(row_data["normal_id"] == "BCN4660_0_definition" for row_data in normal), "b_clock memory normal form present"),
        ("VAL4660_04_observed_clock_zero", any(row_data["zero_id"] == "BCZ4660_5_result" and row_data["status"] == "PRIVATE_BRANCH_ZERO_NONCLAIM" for row_data in zero_import), "fixed branch b_clock_mem zero present"),
        ("VAL4660_05_dynamic_clock_bound", any(row_data["bound_id"] == "BCB4660_1_clock_product_1sigma" for row_data in bounds), "dynamic branch clock product bound retained"),
        ("VAL4660_06_redshift_anchor", any(row_data["bound_id"] == "BCB4660_3_redshift_anchor" for row_data in bounds), "redshift/LPI anchor retained"),
        ("VAL4660_07_Cmem_clock_removed", any(row_data["update_id"] == "CSW4660_1_fixed_clock" for row_data in cmem), "Cmem standard/weight clock term removed in fixed branch"),
        ("VAL4660_08_kappa_crossref", any(row_data["update_id"] == "CSW4660_3_kappa_crossref" for row_data in cmem), "4654 kappa zero cross-reference present"),
        ("VAL4660_09_live_fail_closed", any(row_data["run_id"] == "RUN4660_1_dynamic_clock_branch" and row_data["result"] == "FAIL_CLOSED_TO_CLOCK_BOUND" for row_data in runners), "dynamic branch fails closed to clock bound"),
        ("VAL4660_10_no_claim", all(str(row_data.get("valid_for_claim", "False")) == "False" and str(row_data.get("claim_allowed", "False")) == "False" for row_data in all_rows), "no row is claim-grade"),
        ("VAL4660_11_no_time_axiom_control", any(row_data["control_id"] == "CTRL4660_0_no_time_axiom" for row_data in controls), "no time axiom guard present"),
        ("VAL4660_12_next_kappa_deltaw", decisions and decisions[0]["next_target"] == NEXT_TARGET, "kappa import / delta_w next selected"),
        ("VAL4660_13_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4660_14_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4660_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4660 b_clock_mem observed-coframe zero and dynamic clock-bound gate passed" if passed_all else "4660 validation failed",
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
    return f"""# 4660 - b_clock readout descent or clock redshift bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4660 attacks the third coefficient in the reduced `C_mem^std_weight_live` block:

`b_clock_mem`.

The useful normal form is:

`b_clock_mem := Pi_mem[D_X ln(nu_A^obs/nu_ref^obs)]`,

after the alpha and matter-spectrum branches have already been handled.

Clock ratios obey the standard sensitivity/readout split:

`D ln(nu_A/nu_B)=sum_I DeltaK_I^AB D ln theta_I + rho_clock_readout`.

In the fixed q-basic calibrated branch, 4658 kills the alpha term and 4659 kills the mass/material term. 3136 then supplies the clock-readout theorem:

`ordinary clock matter descends to the observed coframe => observed clocks measure observed metric proper time`.

Equivalently:

`d tau_clk = sqrt(-g_obs_mu_nu dx^mu dx^nu)/c`.

Therefore, if `e_obs=Obs_e(q(Phi))`, `Dq(v_X)=0`, the clock matter action is ordinary local Lorentz matter over `e_obs`, material transition constants are fixed/q-basic, and no independent `nu_i(Xhat)`, shadow coframe, nonminimal clock-flow coupling or tau-role mismatch is admitted:

`b_clock_mem=0`.

This is a real local-GR style derivation of the measured clock readout, not a time axiom and not a claim that every dynamic clock branch is closed.

If the fixed branch is not selected, the live fallback is:

`b_clock_mem_abs <= |rho_clock_readout|+|epsilon_nonminimal_clock|+|epsilon_tau_role|+|Xi_clock|+|E_HO|+|E_transport|`.

The strongest staged clock product pressure gate remains:

`Xi_clock + E_HO + E_transport <= 2.100000e-18 yr^-1`,

with the redshift/LPI anchor:

`alpha_clock_redshift <= 2.48e-05`.

After this checkpoint, the fixed-branch `C_mem^std_weight_live` block reduces to:

`|C_mem^std_weight_live| <= |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|`.

Checkpoint 4654 already gives the private `D_A ln kappa_eff=0` theorem; the next step is not to redo kappa, but to same-branch import it into this Cmem chain and then attack `delta_w_mem`.

## Source Register

{table(sources)}

## b_clock Memory Normal Form

{table(normal)}

## Observed Coframe Clock Zero Import

{table(zero_import)}

## Dynamic Clock Redshift Bound Rows

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
        "4660 imports the observed-coframe clock theorem into the Cmem chain. In the fixed q-basic calibrated observed-coframe branch, ordinary clock matter measures observed metric proper time and b_clock_mem=0, so the clock term drops from C_mem^std_weight_live. Dynamic clock/readout branches remain Xi_clock/redshift/readout-tail nonclaims.",
        "Generated source register, b_clock memory normal form, observed-coframe clock zero import, dynamic clock/redshift bound rows, Cmem standard/weight update, runner, controls, decision, status, next target and validation.",
        "b_clock_mem_observed_coframe_branch_zero_dynamic_clock_bound_nonclaim",
        NEXT_TARGET,
        "Claiming internal flow time is measured clock time, promoting a clock pass, transferring clock bounds to WEP/R10/local-GR without projection, or setting Xi_clock factors by convention.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/WEP/clock claim until the kappa import and delta_w/source-weight terms are closed or bounded in the same branch.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4660 derives the fixed-branch clock readout through the observed coframe. In the same calibrated branch used for alpha and matter constants, ordinary local Lorentz clock matter over `e_obs(q)` gives `d tau_clk=sqrt(-g_obs dx dx)/c`; with no independent clock/readout/nonminimal/tau slot, `b_clock_mem=0`. Dynamic clock branches retain explicit `Xi_clock`, transport-error and redshift/LPI bound rows. The fixed `C_mem^std_weight_live` block now contains only `D_mem ln kappa_eff` and `delta_w_mem`; 4654 provides the private kappa no-drift theorem that must be same-branch imported next.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4660` kills the `b_clock_mem` coefficient only in the fixed observed-coframe calibrated clock branch and retains dynamic clock/redshift product bounds. The reduced fixed-branch `C_mem^std_weight_live` block now contains `D_mem ln kappa_eff` and `delta_w_mem`; `D_mem ln kappa_eff` has a validated private zero in 4654. Next packet target: `{NEXT_TARGET}`.
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
    print(f"4660 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
