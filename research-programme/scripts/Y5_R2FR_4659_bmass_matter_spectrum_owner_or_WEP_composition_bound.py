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

CHECKPOINT = "4659"
CLAIM_ID = "L-501"
BRANCH = "MTS_R2FR_Y5_BMASS_MATTER_SPECTRUM_OWNER_OR_WEP_COMPOSITION_BOUND_4659"
MARKER = "PPC4161_BMASS_MATTER_SPECTRUM_OWNER_OR_WEP_COMPOSITION_BOUND_4659"
PACKET_MARKER = "PPC4161_PACKET_BMASS_MATTER_SPECTRUM_OWNER_OR_WEP_COMPOSITION_BOUND_4659"
DECISION = "BMASS_MEM_FIXED_QBASIC_MATTER_BRANCH_ZERO_IMPORTED_DYNAMIC_WEP_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4660-Y5-R2FR-bclock-readout-descent-or-clock-redshift-bound.md"

DOC_PATH = POST / "4659-Y5-R2FR-bmass-matter-spectrum-owner-or-WEP-composition-bound.md"
FORMAL_PATH = FORMAL / "675-PPC4161-bmass-matter-spectrum-owner-or-WEP-composition-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4658 = POST / "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md"
DOC_4613 = POST / "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
DOC_1804 = POST / "1804-Y5-R2FR-constant-superselection-alpha-mass-clock-provenance.md"
DOC_1805 = POST / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md"
DOC_2443 = POST / "2443-Y5-R2FR-parent-matter-spectrum-owner-signature-or-bmhat-bnuc-source-leg-bound-pack.md"
DOC_3466 = POST / "3466-Y5-R2FR-unique-F2-Hodge-owner-or-WEP-nuclear-mass-component-row.md"

FORMAL_226 = FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md"
FORMAL_460 = FORMAL / "460-PPC4161-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
FORMAL_552 = FORMAL / "552-PPC4161-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"
FORMAL_629 = FORMAL / "629-PPC4161-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
FORMAL_674 = FORMAL / "674-PPC4161-balpha-Maxwell-normalization-owner-or-first-source-bound.md"

CSV_4658_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4658_CMEM_STD_WEIGHT_UPDATE.csv"
CSV_4613_THETA = SOURCE_DIR / "P8_Y5_R2FR_4613_THETA_MARKER_DESCENT_THEOREM.csv"
CSV_4613_CHANNEL = SOURCE_DIR / "P8_Y5_R2FR_4613_CHANNEL_DESCENT_AUDIT.csv"
CSV_4613_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4613_MASS_CLOCK_MARKER_ROWS.csv"
CSV_4613_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
CSV_4613_BLOCK = SOURCE_DIR / "P8_Y5_R2FR_4613_CLAIM_BLOCKERS.csv"
CSV_1804_MASS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_MASS_RATIO_AUDIT.csv"
CSV_1804_COEFF = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_COEFFICIENT_PROVENANCE_ROWS.csv"
CSV_1804_CLAIM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1804_CLAIM_GATE.csv"
CSV_1805_VERTEX = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv"
CSV_1805_NO_MASS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv"
CSV_1805_BOUND = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"
CSV_1805_CLAIM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_CLAIM_GATE.csv"
CSV_1805_DECISION = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1805_DECISION_LEDGER.csv"
CSV_2443_SIG = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2443_PARENT_MATTER_SPECTRUM_SIGNATURE_AUDIT.csv"
CSV_2443_PRODUCT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2443_BMHAT_BNUC_PRODUCT_BOUND_PACK.csv"
CSV_2443_PROJECTION = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2443_SHARED_LOCAL_ARENA_PROJECTION_QUEUE.csv"
CSV_2443_SOURCE_LEG = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2443_SOURCE_LEG_OWNER_AUDIT.csv"
CSV_3466_MASS = SOURCE_DIR / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv"
CSV_3466_NCE = SOURCE_DIR / "P8_Y5_R2FR_3466_NO_CANCELLATION_ENVELOPE_UPDATE.csv"
CSV_3466_CLAIM = SOURCE_DIR / "P8_Y5_R2FR_3466_CLAIM_GATES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4659_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_BMASS_MEMORY_NORMAL_FORM.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_FIXED_MATTER_BRANCH_ZERO_IMPORT.csv"
BOUND_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_DYNAMIC_WEP_COMPOSITION_BOUND_ROWS.csv"
CMEM_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_CMEM_STD_WEIGHT_UPDATE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4659_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4659_VALIDATION.csv"


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
        ("SRC4659_00_4658_next", DOC_4658, "4659-Y5-R2FR-bmass-matter-spectrum-owner-or-WEP-composition-bound.md", "4658 selected b_mass_mem as the next coefficient."),
        ("SRC4659_01_4658_cmem", CSV_4658_CMEM, "CSW4658_2_reduced_fixed_branch", "C_mem standard/weight block after alpha zero."),
        ("SRC4659_02_674_formal", FORMAL_674, "CSW4658_2_reduced_fixed_branch", "formal alpha checkpoint keeps b_mass_mem live."),
        ("SRC4659_03_226_theta", FORMAL_226, "theta_obs = {m_A, charges, alpha_EM, hbar, c, material labels}", "standard visible matter import contract."),
        ("SRC4659_04_226_gr_parity", FORMAL_226, "GR reduces to Newton/PPN using calibrated matter constants", "GR-parity calibration rule."),
        ("SRC4659_05_629_marker_sum", FORMAL_629, "|qbar_theta_marker| <= |b_alpha|+|b_mu|+|b_mA|", "mass channels inside qbar theta-marker envelope."),
        ("SRC4659_06_552_gr_parity", FORMAL_552, "GR_PARITY_IMPORT_CAN_SIGN_COMPONENT_SOURCE_UNIVERSALITY_IF_ADOPTED", "GR-parity imported matter branch is available."),
        ("SRC4659_07_460_standard_matter", FORMAL_460, "STANDARD_LMATTER_COMPONENT_IMPORT_GRAPH_CONTRACT_WRITTEN_PARENT_SM_ORIGIN_AND_REQ_VALUE_REMAIN_NONCLAIM", "standard L_matter component import contract."),
        ("SRC4659_08_4613_qbasic", CSV_4613_THETA, "TMD4613_1_qbasic_constant_zero", "exact conditional q-basic theta zero theorem."),
        ("SRC4659_09_4613_mass_ratios", CSV_4613_CHANNEL, "CH4613_1_mass_ratios", "mass ratios treated as fixed representation data or retained coefficients."),
        ("SRC4659_10_4613_marker", CSV_4613_MARKER, "MCM4613_0_mass_ratios", "mass/material leakage retained after common unit mode removal."),
        ("SRC4659_11_4613_bmu", CSV_4613_QBAR, "QTC4613_2_b_mu", "b_mu coefficient row."),
        ("SRC4659_12_4613_bmass", CSV_4613_QBAR, "QTC4613_3_b_mass_material", "b_mA/b_nuc coefficient row."),
        ("SRC4659_13_4613_block", CSV_4613_BLOCK, "BLK4613_1_masses", "mass branch blocker if not theorem-zero."),
        ("SRC4659_14_1804_mass", DOC_1804, "CSG1804_3_mass_ratios", "mass ratios need parent matter-spectrum ownership."),
        ("SRC4659_15_1804_verdict", CSV_1804_MASS, "MRA1804_4_verdict", "mass-ratio theorem-zero blocked unless spectrum owned."),
        ("SRC4659_16_1804_coeff", CSV_1804_COEFF, "CPR1804_2_b_mA", "b_mA provenance row."),
        ("SRC4659_17_1804_gate", CSV_1804_CLAIM, "CL1804_1_mass_zero", "mass zero claim gate remains blocked outside fixed branch."),
        ("SRC4659_18_1805_fixed", CSV_1805_NO_MASS, "MVT1805_0_fixed_rep_spectrum", "fixed matter representation gives exact conditional mass silence."),
        ("SRC4659_19_1805_verdict", CSV_1805_NO_MASS, "MVT1805_4_verdict", "no-mass-vertex theorem not globally promoted."),
        ("SRC4659_20_1805_mass_vertex", CSV_1805_VERTEX, "VT1805_3_mass_X", "mass-X countervertex remains legal outside fixed branch."),
        ("SRC4659_21_1805_bound", CSV_1805_BOUND, "BM1805_2_WEP_alpha_mass", "WEP alpha/mass/nuclear matrix skeleton."),
        ("SRC4659_22_1805_decision", CSV_1805_DECISION, "DEC1805_2_mass_clock_status", "mass/clock remain live in dynamic branch."),
        ("SRC4659_23_2443_signature", CSV_2443_SIG, "MSS2443_0_parent_signature", "matter-spectrum owner signature shape."),
        ("SRC4659_24_2443_verdict", CSV_2443_SIG, "MSS2443_5_verdict", "matter-spectrum owner not currently signed."),
        ("SRC4659_25_2443_envelope", CSV_2443_PRODUCT, "PBP2443_4_absolute_envelope", "WEP no-cancellation product envelope."),
        ("SRC4659_26_2443_projection", CSV_2443_PROJECTION, "SAP2443_0_WEP", "shared WEP arena projection skeleton."),
        ("SRC4659_27_2443_source_leg", CSV_2443_SOURCE_LEG, "SLO2443_5_verdict", "source leg owner still blocks local-GR claim."),
        ("SRC4659_28_3466_definition", CSV_3466_MASS, "MASS3466_0_definition", "D_mhat_eff product definition."),
        ("SRC4659_29_3466_bound", CSV_3466_MASS, "MASS3466_2_alloy_single_channel_bound", "finite WEP mass-channel ceiling."),
        ("SRC4659_30_3466_guard", CSV_3466_NCE, "NCE3466_3_no_cancellation_guard", "single-channel ceiling cannot be treated as pass."),
        ("SRC4659_31_3466_claim", CSV_3466_CLAIM, "CG3466_2_mass_source_product", "b_mhat/source-leg product missing."),
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
        (
            "BMN4659_0_vector_definition",
            "b_mass_mem := (b_mu^mem,b_mA^mem,b_nuc^mem,b_material^mem)",
            "memory-projected matter-spectrum/composition drift vector after common unit mode is removed",
            "b_mu,b_mA,b_nuc,b_material are dimensionless vertical derivatives or normalized material-marker responses",
            "VECTOR_NORMAL_FORM_DEFINED",
        ),
        (
            "BMN4659_1_component_law",
            "b_mu^mem=Pi_mem[D_X ln(m_e/m_p)], b_mA^mem=Pi_mem[D_X ln(m_A/m_ref)], b_nuc^mem=Pi_mem[D_X ln(E_bind/m_ref)]",
            "mass ratios and binding fractions are physical observable channels, not removable unit choices",
            "common mass scale is quotiented; only dimensionless ratios/material responses are scored",
            "COMPONENT_LAW_IMPORTED",
        ),
        (
            "BMN4659_2_absolute_bound",
            "|b_mass_mem|_1 <= |b_mu^mem|+|b_mA^mem|+|b_nuc^mem|+|b_material^mem|",
            "no-cancellation fallback for dynamic matter/composition branch",
            "requires source-backed coefficients, arena sensitivities and source-leg products",
            "BOUND_READY_VALUES_PARTIAL",
        ),
        (
            "BMN4659_3_WEP_product_map",
            "D_mhat_eff := S_E^q*b_mhat",
            "WEP/local matter source row sees a product of source-leg projection and mass-ratio coefficient",
            "single-channel ceilings bound the product, not b_mhat alone",
            "PRODUCT_MAP_IMPORTED",
        ),
        (
            "BMN4659_4_GR_parity_import",
            "standard S_matter[g,fields,theta_SM] with fixed theta_SM gives D_X theta_SM=0 along v_X in ker(Dq)",
            "local-GR reduction may import the same calibrated matter constants that GR imports",
            "this is a local reduction branch, not a derivation of SM masses from MTS",
            "GR_PARITY_BRANCH_STATEMENT",
        ),
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
        (
            "BMZ4659_0_qbasic_theta",
            "S_matter=Sbar[psi,e_obs(q),theta_obs] and v_X in ker(Dq)",
            "chain-rule theta term is sum_A J_theta^A Lie_v(theta_A)",
            "imported from 4613 q-basic theorem",
            "SETUP_IMPORTED",
        ),
        (
            "BMZ4659_1_fixed_rep_spectrum",
            "theta_mass(Phi)=theta_rep or theta_bar(q(Phi))",
            "Dq[v_X]=0 implies Lie_v ln(m_A/m_B)=0",
            "fixed calibrated visible matter / GR-parity import branch",
            "EXACT_CONDITIONAL_ZERO",
        ),
        (
            "BMZ4659_2_no_X_mass_vertices",
            "no m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat) or beta_A(Xhat) vertex in the selected branch",
            "b_mu^mem=b_mA^mem=b_nuc^mem=0",
            "this is branch selection/adoption; it is not a global parent microphysics theorem",
            "BRANCH_ZERO_CONDITION",
        ),
        (
            "BMZ4659_3_fixed_material_labels",
            "material/species/preparation labels are representation/readout labels fixed before variation",
            "b_material^mem=0 if no marker operator, spurion, auxiliary or boundary marker route is admitted",
            "inherits 4613 material-marker silence condition",
            "EXACT_CONDITIONAL_ZERO",
        ),
        (
            "BMZ4659_4_result",
            "fixed q-basic calibrated visible matter branch => b_mass_mem=0",
            "|b_mass_mem||S_mass^mem| drops from C_mem^std_weight_live in the same branch",
            "does not predict electron/proton/nuclear masses and does not close dynamic matter/composition branches",
            "PRIVATE_BRANCH_ZERO_NONCLAIM",
        ),
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
        (
            "BDB4659_0_live_components",
            "b_mu^mem,b_mA^mem,b_nuc^mem,b_material^mem",
            "|b_mass_mem|_1 <= |b_mu^mem|+|b_mA^mem|+|b_nuc^mem|+|b_material^mem|",
            "dynamic matter/composition branch if fixed spectrum is not adopted",
            "dimensionless",
            "feeds C_mem^std_weight_live and WEP/clock/R10 composition rows",
            "VALUES_MISSING_NONCLAIM",
            "MISSING_COMPONENT_VALUES",
        ),
        (
            "BDB4659_1_WEP_matrix",
            "eta_AB",
            "eta_AB = DeltaQ_alpha_AB*beta_source_alpha*b_alpha*tau_WEP + DeltaQ_mass_AB*b_mA*tau_WEP + DeltaQ_nuc_AB*b_nuc*tau_WEP + ...",
            "WEP alpha/mass/nuclear source-test skeleton",
            "dimensionless eta",
            "finite fallback for composition drift",
            "COMPOSITION_MATRIX_PARTIAL_NONCLAIM",
            str(CSV_1805_BOUND),
        ),
        (
            "BDB4659_2_product_definition",
            "D_mhat_eff",
            "D_mhat_eff := S_E^q*b_mhat",
            "source-leg projection and matter-spectrum coefficient are not separated",
            "dimensionless product",
            "mass-channel WEP row",
            "PRODUCT_DEFINED_PARENT_OWNER_MISSING",
            str(CSV_3466_MASS),
        ),
        (
            "BDB4659_3_single_channel_ceiling",
            "abs(D_mhat_eff)_single_channel",
            "abs(D_mhat_eff) <= 8.446537954729e-13",
            "Ti/Pt one-channel ceiling if alpha/direct/shadow/readout channels are zero",
            "dimensionless",
            "smoke ceiling only, cannot be used as WEP pass",
            "FINITE_NONCLAIM_MASS_CHANNEL_CEILING",
            str(CSV_3466_MASS),
        ),
        (
            "BDB4659_4_ONERA_crosscheck",
            "abs(D_mhat_eff)_ONERA_single_channel",
            "abs(D_mhat_eff) <= 8.408408408408e-13",
            "ONERA sensitivity crosscheck under same single-channel premise",
            "dimensionless",
            "consistency check only",
            "CONSISTENT_ONERA_CROSSCHECK_NONCLAIM",
            str(CSV_3466_MASS),
        ),
        (
            "BDB4659_5_no_cancellation",
            "WEP_product_envelope",
            "|DeltaQ_mhat*S_E^q*b_mhat| + |DeltaQ_e*S_E^q*b_alpha| + |DeltaQ_nuc*S_E^q*b_nuc| + |direct terms| <= eta_bound",
            "absolute envelope keeps all live channels as magnitudes",
            "dimensionless eta envelope",
            "prevents treating a single-channel ceiling as a pass",
            "NO_CANCELLATION_GUARD_STILL_BLOCKS_CLAIM",
            str(CSV_2443_PRODUCT),
        ),
        (
            "BDB4659_6_source_row_contract",
            "b_mass_mem_source_row",
            "system_id;branch;b_mu;b_mA;b_nuc;b_material;S_E_q;tau_WEP;DeltaQ;arena_bound;units;source_path;valid_for_claim",
            "source-backed finite dynamic mass row contract",
            "dimensionless or declared normalized units",
            "required before finite dynamic-mass claim",
            "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING",
            "MISSING_SOURCE_PATH",
        ),
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
        (
            "CSW4659_0_before",
            "|C_mem^std_weight_live| <= |b_mass_mem||S_mass^mem| + |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|",
            "4658 reduced first-block bound after alpha zero",
            "FIRST_BLOCK_BOUND_IMPORTED",
        ),
        (
            "CSW4659_1_fixed_mass",
            "fixed q-basic calibrated visible matter branch => |b_mass_mem||S_mass^mem|=0",
            "matter-spectrum/composition coefficient term drops only in the same fixed branch",
            "BRANCH_ZERO_INSERTED_NONCLAIM",
        ),
        (
            "CSW4659_2_reduced_fixed_branch",
            "|C_mem^std_weight_live| <= |b_clock_mem||S_clock^mem| + |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|",
            "reduced first-block target after alpha and mass zero imports",
            "NEXT_COEFFICIENTS_REMAIN",
        ),
        (
            "CSW4659_3_dynamic_branch",
            "|C_mem^std_weight_live| retains |b_mass_mem|_1 |S_mass^mem| with WEP/composition product bounds",
            "if dynamic matter-spectrum/composition branch is selected, mass term stays source-bound",
            "DYNAMIC_BRANCH_BOUND_RETAINED",
        ),
        (
            "CSW4659_4_next",
            "attack b_clock_mem",
            "after alpha and fixed-matter branch zeros, the next standard/weight coefficient is clock/readout drift",
            "NEXT_TARGET_SELECTED",
        ),
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
        (
            "RUN4659_0_fixed_qbasic_matter_branch",
            "fixed q-basic calibrated visible matter / GR-parity import branch",
            "PASS_CONDITIONAL_PRIVATE_ZERO",
            "b_mass_mem=0; no numerical mass prediction; dynamic matter/composition branches retained.",
        ),
        (
            "RUN4659_1_dynamic_matter_branch",
            "dynamic m_A/y_A/Lambda_QCD/B_A/material-marker branch",
            "FAIL_CLOSED_TO_WEP_BOUND",
            "b_mass_mem is not zero; use absolute component/product rows and no-cancellation guard.",
        ),
        (
            "RUN4659_2_Cmem_update",
            "C_mem^std_weight_live",
            "PASS_BRANCH_REDUCTION",
            "mass term drops only in fixed branch; clock/kappa/source-weight terms remain.",
        ),
        (
            "RUN4659_3_local_GR_status",
            "local GR/Newton/PPN/WEP claim",
            "NONCLAIM_STILL_BLOCKED",
            "clock/readout, kappa/source normalization and relative source-weight branches remain live.",
        ),
        (
            "RUN4659_4_next_target",
            "component attack order",
            "PASS_NEXT_SELECTED",
            NEXT_TARGET,
        ),
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
        ("CTRL4659_0_no_mass_prediction", "4659 does not predict electron/proton/nuclear masses or Yukawa/QCD scales.", "ACTIVE"),
        ("CTRL4659_1_no_dynamic_zero_smuggling", "Dynamic mass/composition/readout/material branches remain finite bound rows unless their coefficients are source-backed or theorem-zero in the same branch.", "ACTIVE"),
        ("CTRL4659_2_no_WEP_pass_from_single_channel", "The 8.4465e-13 D_mhat_eff ceiling is a one-channel nonclaim ceiling and cannot be promoted while other channels are live.", "ACTIVE"),
        ("CTRL4659_3_GR_parity_not_parent_SM", "The calibrated matter branch is a local-GR reduction/import branch, not a derivation of Standard Model microphysics from MTS.", "ACTIVE"),
        ("CTRL4659_4_source_leg_product_guard", "D_mhat_eff=S_E^q*b_mhat is a product; b_mhat and source-leg projection are not independently owned.", "ACTIVE"),
        ("CTRL4659_5_private_local_only", "No GitHub action, no public claim and no edits outside the local framework packet are intended.", "ACTIVE"),
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
            "decision_id": "DEC4659_0",
            "decision": DECISION,
            "summary": (
                "4659 turns b_mass_mem into a clean same-branch split. In the fixed q-basic calibrated visible matter / GR-parity import branch, "
                "theta_mass and material labels are representation or quotient data, so the memory-projected mass-ratio, material-mass and binding coefficients vanish. "
                "Therefore the mass term drops from C_mem^std_weight_live in that branch. Outside that branch, mass/composition drift remains live and is carried by WEP product bounds, "
                "including D_mhat_eff=S_E^q*b_mhat and the no-cancellation envelope."
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
            "fixed_branch_result": "BMASS_MEM_ZERO_PRIVATE_BRANCH",
            "dynamic_branch_status": "WEP_COMPOSITION_PRODUCT_BOUND_RETAINED",
            "Cmem_effect": "MASS_TERM_REMOVED_ONLY_IN_FIXED_BRANCH",
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
            "why": "After alpha and fixed-matter branch zeros, b_clock_mem is the next live standard/weight coefficient in C_mem^std_weight_live.",
            "derive_route": "show clock/readout labels descend through q-basic calibrated matter/readout grammar, or derive a redshift/clock sensitivity bound with source paths.",
            "fallback_route": "retain b_clock_i and clock readout-frame tails as finite LPI/redshift rows.",
            "avoid": "claiming local-GR pass before clock/kappa/source-weight terms are zeroed or bounded in the same branch.",
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
        ("VAL4659_00_sources_exist", all(row_data["path_exists"] for row_data in sources), "all cited source paths exist"),
        ("VAL4659_01_needles_found", all(row_data["needle_found"] for row_data in sources), "all cited source needles found"),
        ("VAL4659_02_line_anchors", all(int(row_data["line_number"]) > 0 for row_data in sources), "all source line anchors positive"),
        ("VAL4659_03_memory_normal_form", any(row_data["normal_id"] == "BMN4659_0_vector_definition" for row_data in normal), "b_mass memory vector normal form present"),
        ("VAL4659_04_fixed_branch_zero", any(row_data["zero_id"] == "BMZ4659_4_result" and row_data["status"] == "PRIVATE_BRANCH_ZERO_NONCLAIM" for row_data in zero_import), "fixed branch b_mass_mem zero present"),
        ("VAL4659_05_dynamic_WEP_bound", any(row_data["bound_id"] == "BDB4659_3_single_channel_ceiling" for row_data in bounds), "dynamic branch WEP mass ceiling retained"),
        ("VAL4659_06_Cmem_mass_removed", any(row_data["update_id"] == "CSW4659_1_fixed_mass" for row_data in cmem), "Cmem standard/weight mass term removed in fixed branch"),
        ("VAL4659_07_live_fail_closed", any(row_data["run_id"] == "RUN4659_1_dynamic_matter_branch" and row_data["result"] == "FAIL_CLOSED_TO_WEP_BOUND" for row_data in runners), "dynamic branch fails closed to WEP bound"),
        ("VAL4659_08_no_claim", all(str(row_data.get("valid_for_claim", "False")) == "False" and str(row_data.get("claim_allowed", "False")) == "False" for row_data in all_rows), "no row is claim-grade"),
        ("VAL4659_09_no_mass_prediction_control", any(row_data["control_id"] == "CTRL4659_0_no_mass_prediction" for row_data in controls), "no mass prediction guard present"),
        ("VAL4659_10_next_bclock", decisions and decisions[0]["next_target"] == NEXT_TARGET, "b_clock next selected"),
        ("VAL4659_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4659_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4659_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4659 b_mass_mem fixed-branch zero and dynamic WEP-bound gate passed" if passed_all else "4659 validation failed",
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
    return f"""# 4659 - b_mass matter spectrum owner or WEP composition bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4659 attacks the second coefficient in the reduced `C_mem^std_weight_live` block:

`b_mass_mem`.

The useful normal form is:

`b_mass_mem := (b_mu^mem,b_mA^mem,b_nuc^mem,b_material^mem)`,

where:

`b_mu^mem=Pi_mem[D_X ln(m_e/m_p)]`,

`b_mA^mem=Pi_mem[D_X ln(m_A/m_ref)]`,

and:

`b_nuc^mem=Pi_mem[D_X ln(E_bind/m_ref)]`.

The common dimensionful mass scale is not scored. Only dimensionless mass ratios, binding fractions, material/species responses and readout/preparation markers survive.

The fixed q-basic calibrated visible matter branch gives a real conditional zero:

`S_matter=Sbar[psi,e_obs(q),theta_obs]`, `v_X in ker(Dq)`, and `theta_mass=theta_rep` or `theta_bar(q(Phi))`.

Therefore:

`D_X theta_mass = 0`,

so:

`b_mu^mem=b_mA^mem=b_nuc^mem=b_material^mem=0`,

and hence:

`b_mass_mem=0`.

This is not a prediction of electron, proton, nuclear, Yukawa or QCD masses. It is the fair local-GR/standard-matter import branch: the same kind of calibrated matter data GR uses when reducing to Newton/PPN. If the dynamic matter/composition branch is selected instead, the mass term remains live and is carried by WEP/product rows such as:

`D_mhat_eff := S_E^q*b_mhat`,

with the current nonclaim single-channel ceiling:

`abs(D_mhat_eff) <= 8.446537954729e-13`.

The no-cancellation guard remains active, so no WEP/local-GR pass is claimed.

## Source Register

{table(sources)}

## b_mass Memory Normal Form

{table(normal)}

## Fixed Matter Branch Zero Import

{table(zero_import)}

## Dynamic WEP Composition Bound Rows

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
        "4659 memory-projects the matter-spectrum/composition drift vector. In the fixed q-basic calibrated visible matter / GR-parity import branch, theta_mass and material labels are representation or quotient data, so b_mass_mem=0 and the mass term drops from C_mem^std_weight_live. Dynamic matter/composition branches remain WEP/product-bound nonclaims.",
        "Generated source register, b_mass memory normal form, fixed matter branch zero import, dynamic WEP composition bound rows, Cmem standard/weight update, runner, controls, decision, status, next target and validation.",
        "b_mass_mem_fixed_qbasic_branch_zero_dynamic_WEP_bound_nonclaim",
        NEXT_TARGET,
        "Claiming MTS predicts Standard Model masses, treating a calibrated local-GR matter import as parent microphysics, promoting single-channel WEP ceilings to a pass, or dropping dynamic material/composition/source-leg products.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/clock/orbital/WEP claim until clock/readout, kappa/source normalization and relative source-weight terms are zeroed or source-backed in the same branch.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4659 turns `b_mass_mem` into a same-branch split. In the fixed q-basic calibrated visible matter / GR-parity import branch, matter-spectrum constants, dimensionless mass ratios, binding fractions and material labels are representation or quotient data fixed before variation, so the memory-projected mass vector vanishes: `b_mass_mem=0`. This removes the `|b_mass_mem||S_mass^mem|` term from `C_mem^std_weight_live` only in that branch. It is not a prediction of SM masses. Dynamic matter/composition branches retain WEP/product bounds such as `D_mhat_eff=S_E^q*b_mhat`, with no-cancellation guards still blocking local-GR/WEP claims. Next target: `b_clock_mem`.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4659` kills the `b_mass_mem` coefficient only in the fixed q-basic calibrated visible matter branch and retains dynamic WEP/composition product bounds. The reduced fixed-branch `C_mem^std_weight_live` block now contains `b_clock_mem`, `D_mem ln kappa_eff`, and `delta_w_mem`. Next packet target: `{NEXT_TARGET}`.
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
    print(f"4659 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
