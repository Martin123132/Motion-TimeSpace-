from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2915"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2915-Y5-R2FR-Cshadow-component-bound-pack-or-Cobs-parent-normalization-proof-under-AX1090.md"

SRC_2914_DOC = ROOT / "2914-Y5-R2FR-DqZ-geometry-source-acquisition-or-Cobs-no-shadow-bound-under-AX1090.md"
SRC_2914_SHADOW = RESIDUALS / "P8_Y5_R2FR_2914_NO_SHADOW_COMPONENT_BOUND_AUDIT.csv"
SRC_2914_HEADS = RESIDUALS / "P8_Y5_R2FR_2914_DQZ_GEOMETRY_HEAD_ACQUISITION_ROWS.csv"
SRC_2914_NEXT = RESIDUALS / "P8_Y5_R2FR_2914_NEXT_TARGET.csv"
SRC_944_FRAME = RESIDUALS / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv"
SRC_945_BOUNDS = RESIDUALS / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv"
SRC_1027_SCHEMA = RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv"
SRC_1027_DEPS = RESIDUALS / "P8_Y5_R10_1027_DEPENDENCY_LINKS.csv"
SRC_1028_PACK = RESIDUALS / "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv"
SRC_1028_NO_MARKER = RESIDUALS / "P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv"
SRC_1029_THEOREM = RESIDUALS / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv"
SRC_1030_CONTRACT = RESIDUALS / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
SRC_1030_PROVENANCE = RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv"
SRC_1031_TERMINAL = RESIDUALS / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv"
SRC_1031_FALLBACK = RESIDUALS / "P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv"
SRC_1038_QUARANTINE = RESIDUALS / "P8_Y5_R10_1038_LEGACY_LINEAR_CG_QUARANTINE.csv"
SRC_1156_FILL = RESIDUALS / "P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv"
SRC_1156_QMF = RESIDUALS / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
SRC_1157_CG = RESIDUALS / "P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv"
SRC_1157_QMAP = RESIDUALS / "P8_Y5_R10_1157_QMAP_NULL_GENERATOR_PROOF_AUDIT.csv"
SRC_2538_NONH = RESIDUALS / "P8_Y5_NO_SHADOW_2538_NONHILBERT_RESIDUAL_ROW.csv"
SRC_2538_ID = RESIDUALS / "P8_Y5_NO_SHADOW_2538_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv"
SRC_2761_PRODUCTS = RESIDUALS / "P8_Y5_R2FR_2761_PRODUCT_CONTRACT_LEDGER.csv"
SRC_2761_MATRIX = RESIDUALS / "P8_Y5_R2FR_2761_SAME_BRANCH_PRODUCT_CANDIDATE_MATRIX.csv"
SRC_2761_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2761_CLAIM_GATES.csv"
SRC_1092_BALPHA = RESIDUALS / "P8_Y5_R10_1092_BALPHA_TAU_PROJECTION_FALLBACK.csv"
SRC_2888_CSHADOW = RESIDUALS / "P8_Y5_R2FR_2888_CSHADOW_BOUND_ROW_NONCLAIM.csv"
SRC_2888_COUNTER = RESIDUALS / "P8_Y5_R2FR_2888_SHADOW_COUNTERMODEL_LEDGER.csv"
SRC_2888_CERT = RESIDUALS / "P8_Y5_R2FR_2888_TERMINAL_PUBLIC_COFRAME_NO_SHADOW_CERTIFICATE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2915_SOURCE_REGISTER.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_2915_CSHADOW_COMPONENT_ENVELOPE.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_2915_CSHADOW_ZERO_THEOREM_ATTEMPT.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2915_COMPONENT_ACQUISITION_ROWS.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2915_ARENA_ROUTING_AND_PRODUCT_RULES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2915_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2915_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2915_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2915_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2915_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2915_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_copy": PARENT_ACTION / "Cshadow_zero_theorem_attempt_2915_NONCLAIM.csv",
    "component_copy": LOCAL_BOUNDS / "Cshadow_component_bound_pack_2915_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2915_CG_INVARIANT_SOURCE_TEST_OR_DISFORMAL_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2915_00_2914_doc", SRC_2914_DOC, "NEXT2914_0_2915;C_shadow_abs", "2914 handoff to C_shadow components"),
        ("SRC2915_01_2914_shadow", SRC_2914_SHADOW, "SHD2914_1_cg_weyl;SHD2914_5_verdict", "2914 component split"),
        ("SRC2915_02_2914_heads", SRC_2914_HEADS, "HEAD2914_5_C_shadow_abs;HEAD2914_8_promotion_rule", "DqZ geometry head formula"),
        ("SRC2915_03_2914_next", SRC_2914_NEXT, "NEXT2914_0_2915;C_Obs_e=1", "machine-readable 2915 target"),
        ("SRC2915_04_944_frame", SRC_944_FRAME, "FLB944_0_cg_weyl;FLB944_7_epsilon_frame_leak", "frame leak bound pack"),
        ("SRC2915_05_945_bounds", SRC_945_BOUNDS, "BND945_0_cg_value;BND945_7_score_gate", "first frame leak bound rows"),
        ("SRC2915_06_1027_schema", SRC_1027_SCHEMA, "BQT1027_0_visible_geometry;BQT1027_4_claim_gate", "qbarXT component schema"),
        ("SRC2915_07_1027_deps", SRC_1027_DEPS, "DEP1027_2_bound_fallback;DEP1027_3_no_cancellation", "component dependency links"),
        ("SRC2915_08_1028_pack", SRC_1028_PACK, "FMB1028_0_cg;FMB1028_10_total_qbarXT_envelope", "frame marker bound input pack"),
        ("SRC2915_09_1028_no_marker", SRC_1028_NO_MARKER, "NM1028_4_no_shadow_frame;NM1028_6_verdict", "no-marker theorem audit"),
        ("SRC2915_10_1029_theorem", SRC_1029_THEOREM, "NST1029_2_no_extra_frame_slot;NST1029_6_verdict", "c_g no-shadow theorem audit"),
        ("SRC2915_11_1030_contract", SRC_1030_CONTRACT, "SPM1030_2_no_shadow_frame_slot;SPM1030_5_hidden_current_silence", "single-public-metric contract"),
        ("SRC2915_12_1030_provenance", SRC_1030_PROVENANCE, "CPG1030_1_finite_cg_value;CPG1030_4_no_cancellation", "c_g provenance/no-cancellation gate"),
        ("SRC2915_13_1031_terminal", SRC_1031_TERMINAL, "TPM1031_3_vertical_chain_rule;TPM1031_6_verdict", "terminal metric proof audit"),
        ("SRC2915_14_1031_fallback", SRC_1031_FALLBACK, "FCG1031_0_cg_value;FCG1031_3_no_cancellation", "finite c_g/tau fallback"),
        ("SRC2915_15_1038_quarantine", SRC_1038_QUARANTINE, "LCG1038_0_944_linear_shorthand;LCG1038_1_runner_guard", "legacy linear c_g quarantine"),
        ("SRC2915_16_1156_fill", SRC_1156_FILL, "FLB1156_1_c_g;FLB1156_7_epsilon_frame_leak", "later frame-leak fill rows"),
        ("SRC2915_17_1156_qmf", SRC_1156_QMF, "QMF1156_0_descent_criterion;QMF1156_7_verdict", "quotient matter functor signature"),
        ("SRC2915_18_1157_cg", SRC_1157_CG, "CG1157_0_cg_first_fill;CG1157_5_score_interface", "c_g first fill rows"),
        ("SRC2915_19_1157_qmap", SRC_1157_QMAP, "QMAP1157_1_parent_q_object;QMAP1157_8_verdict", "qmap null generator proof audit"),
        ("SRC2915_20_2538_nonH", SRC_2538_NONH, "NHR2538_0_total;NHR2538_5_projected_mass", "non-Hilbert residual rows"),
        ("SRC2915_21_2538_identity", SRC_2538_ID, "NSCI2538_0_target;NSCI2538_7_verdict", "Noether source charge identity attempt"),
        ("SRC2915_22_2761_products", SRC_2761_PRODUCTS, "CON2761_0_clock_observable;CON2761_4_local_insertion_contract", "b_alpha clock product contract"),
        ("SRC2915_23_2761_matrix", SRC_2761_MATRIX, "SBC2761_0_clock_product_admitted;SBC2761_4_R10_product_missing", "same-branch product matrix"),
        ("SRC2915_24_2761_claims", SRC_2761_CLAIMS, "CG2761_1_clock_product_numeric;CG2761_6_local_GR_Newton", "clock product claim gates"),
        ("SRC2915_25_1092_balpha", SRC_1092_BALPHA, "BTP1092_0_best_clock_product;BTP1092_4_verdict", "b_alpha/tau fallback"),
        ("SRC2915_26_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_0_C_shadow_abs;CSH2888_2_d_R_disformal", "older C_shadow bound row"),
        ("SRC2915_27_2888_counter", SRC_2888_COUNTER, "CM2888_0_common_weyl;CM2888_4_qshape_forgetting", "shadow countermodels"),
        ("SRC2915_28_2888_cert", SRC_2888_CERT, "NSC2888_0_exact;NSC2888_6_verdict", "terminal public coframe no-shadow audit"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def component_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CSHC2915_0_total",
            "C_shadow_abs",
            "absolute no-cancellation representative-frame/source shadow envelope",
            "|tau_geom_cg c_g| + |tau_geom_dis b_dis| + |tau_geom_A b_A| + |tau_geom_alpha b_alpha| + |q_nonH| + |Delta_W_support| + |Delta_tau_n|",
            "dimensionless_or_arena_specific",
            "MISSING_COMPONENT_INPUTS",
            "all local arenas",
            "sum_abs only; no cancellation between components",
        ),
        (
            "CSHC2915_1_cg",
            "c_g",
            "common Weyl/conformal ordinary-frame derivative d ln A_g/dXhat",
            "|tau_geom_cg c_g|",
            "dimensionless",
            "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
            "R10;PPN;clock;WEP common mode",
            "naked linear c_g is quarantined for R10 unless a source leg is declared; universal source-test force is beta_s beta_t or c_g^2-like",
        ),
        (
            "CSHC2915_2_b_dis",
            "b_dis",
            "representative disformal/preferred-frame derivative dB_g/dXhat with profile convention",
            "|tau_geom_dis b_dis|",
            "model_dependent",
            "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
            "PPN preferred-frame;clock;orbital",
            "c_g=0 does not kill disformal/vector leakage",
        ),
        (
            "CSHC2915_3_bA",
            "b_A",
            "vertical derivative of material masses/species constants",
            "sum_A |tau_geom_A^A b_A|",
            "dimensionless",
            "MISSING_MASS_CONSTANT_DESCENT_OR_NUMERIC_BA",
            "WEP;clock;composition;R10 material response",
            "WEP/species-blindness cannot remove common source normalization",
        ),
        (
            "CSHC2915_4_balpha",
            "b_alpha",
            "vertical derivative of EM/fine-structure or electromagnetic binding marker",
            "|tau_geom_alpha b_alpha|",
            "dimensionless",
            "CLOCK_PRODUCT_SOURCE_BACKED_BUT_STANDALONE_BLOCKED",
            "clock;EM;WEP transfer;R10 transfer",
            "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 is retained as clock-only nonclaim; no standalone b_alpha transfer",
        ),
        (
            "CSHC2915_5_qnonH",
            "q_nonH",
            "non-Hilbert source current, torsion/nonmetricity/boundary current or improvement source piece",
            "|q_nonH|",
            "source_current_units",
            "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
            "R10;PPN;source normalization;local GR",
            "Hilbert source silence does not silence total source current",
        ),
        (
            "CSHC2915_6_support",
            "Delta_W_support;Delta_tau_n",
            "worldtube/support/tau-normal mismatch under observed-frame choices",
            "|Delta_W_support| + |Delta_tau_n|",
            "dimensionless",
            "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND",
            "orbital;clock;local GR;source support",
            "same coframe is not enough without source support and tau/normal lock",
        ),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "absolute_formula": formula,
                "units": units,
                "current_status": status,
                "arena_links": arenas,
                "guardrail": guardrail,
                "theorem_zero": False,
                "numeric_bound_present": symbol == "b_alpha",
                "claim_note": "nonclaim product only" if symbol == "b_alpha" else "missing theorem-zero or numeric bound",
            }
        )
        for component_id, symbol, definition, formula, units, status, arenas, guardrail in specs
    ]


def zero_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ZTH2915_0_exact_conditional",
            "C_shadow=0 exact conditional theorem",
            "If terminal public coframe, no Weyl/disformal/source-prefactor/endpoint slot, quotient-owned constants, Hilbert source ownership, support equivalence and readout closure all close in one parent branch, then C_shadow_abs=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "would remove the geometry shadow term from DqZ_geometry",
            "not current MTS because the parent action/domain exclusions are unsigned",
        ),
        (
            "ZTH2915_1_cg",
            "c_g=0",
            "No independent A_g(Xhat)e_pub matter/readout frame slot, plus q-kernel ownership, implies Lie_v ln A_g=0.",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "kills common Weyl part",
            "single-public-metric/no-extra-frame and q-kernel ownership are not derived",
        ),
        (
            "ZTH2915_2_disformal",
            "b_dis=0",
            "No independent B_g(Xhat)U_muU_nu shadow frame/current slot in ordinary matter/readout action.",
            "NOT_DERIVED_COUNTERMODEL_RETAINED",
            "kills preferred-frame/disformal part",
            "covariance and terminal metric alone do not exclude disformal/current slots",
        ),
        (
            "ZTH2915_3_constants",
            "b_A=b_alpha=0",
            "Masses, material constants, alpha_EM and clock standards are quotient-owned/superselected and cannot depend on vertical representative labels.",
            "NOT_DERIVED_CLOCK_PRODUCT_RETAINED",
            "kills marker/constants branch",
            "clock product exists only as product; no standalone coefficient or transfer theorem",
        ),
        (
            "ZTH2915_4_nonHilbert",
            "q_nonH=0",
            "Noether/Hilbert source charge identity plus canonical improvement and boundary/source tails give no independent active source current.",
            "NOT_DERIVED_RESIDUAL_ROW_RETAINED",
            "kills source-current branch",
            "2538 retains spin/torsion, boundary, readout, improvement and projected-mass residuals",
        ),
        (
            "ZTH2915_5_support",
            "Delta_W_support=Delta_tau_n=0",
            "Observed-frame support, source worldtube, tau and normal locks are parent-owned and invariant under allowed frame choices.",
            "NOT_DERIVED",
            "kills support/tau branch",
            "support equivalence and tau-normal lock remain missing",
        ),
        (
            "ZTH2915_6_verdict",
            "C_shadow zero theorem for current MTS",
            "all ZTH2915 component zero clauses close in one parent branch",
            "CSHADOW_ZERO_NOT_DERIVED_CURRENT_MTS",
            "no DqZ_geometry or local GR claim",
            "component acquisition rows remain mandatory",
        ),
    ]
    return [
        add_common(
            {
                "attempt_id": attempt_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "would_prove": would_prove,
                "blocking_gap": gap,
                "parent_signed": False,
                "theorem_zero_adopted": False,
            }
        )
        for attempt_id, target, statement, status, would_prove, gap in specs
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2915_0_Cshadow_total", "C_shadow_abs", "sum_abs(c_g,b_dis,b_A,b_alpha,q_nonH,Delta_W_support,Delta_tau_n contributions)", "dimensionless_or_arena_specific", "all component rows numeric or theorem-zero", "MISSING_COMPONENT_INPUTS", "all_local_arenas"),
        ("ACQ2915_1_cg_zero", "Z_cg", "parent no-extra-frame theorem for c_g", "boolean", "SPM/terminal coframe + no A_g slot + q-kernel ownership", "FALSE_NOT_PARENT_SIGNED", "R10;PPN;clock"),
        ("ACQ2915_2_cg_value", "c_g", "finite common Weyl coefficient", "dimensionless", "numeric c_g, Xhat normalization, source path, derivation status", "MISSING_PARENT_INPUT_AND_SOURCE", "R10;PPN;clock"),
        ("ACQ2915_3_cg_product_rule", "beta_s_beta_t_or_source_leg", "R10/source-test invariant product rule for c_g", "dimensionless_alpha_lambda_factor", "beta_s,beta_t,K_X,Qbar_XH,tau_R10 or declared source leg with source path", "NAKED_LINEAR_CG_FORBIDDEN", "R10"),
        ("ACQ2915_4_bdis", "b_dis", "finite or zero disformal/preferred-frame coefficient", "model_dependent", "B_g definition, U_mu/current owner, PPN preferred-frame kernel/source path", "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND", "PPN;clock;orbital"),
        ("ACQ2915_5_bA", "b_A", "material mass/species constant coefficient", "dimensionless", "species/material sensitivities, source path, no-marker theorem or numeric row", "MISSING_MASS_CONSTANT_DESCENT_OR_NUMERIC_BA", "WEP;clock;R10"),
        ("ACQ2915_6_balpha_product", "b_alpha*tau_clock_time", "source-backed clock-only product retained as nonclaim", "yr^-1", "BTP1092_0/CON2761_0 product bound; standalone tau transfer absent", "NUMERIC_PRODUCT_NONCLAIM_ONLY", "clock"),
        ("ACQ2915_7_balpha_transfer", "b_alpha;tau_WEP;tau_R10", "standalone b_alpha or cross-arena transfer", "dimensionless", "Xhat normalization, tau_clock/tau_WEP/tau_R10 same-branch map", "MISSING_STANDALONE_BALPHA_AND_TRANSFER", "WEP;R10;local"),
        ("ACQ2915_8_qnonH", "q_nonH", "non-Hilbert active source-current projection", "source_current_units", "Noether/Hilbert identity, improvement flux, boundary/readout rows", "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE", "source;R10;PPN"),
        ("ACQ2915_9_support", "Delta_W_support;Delta_tau_n", "support/tau-normal frame shift", "dimensionless", "worldtube support equivalence, tau/normal lock, source path", "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND", "orbital;local_GR"),
        ("ACQ2915_10_promotion_rule", "promotion_rule", "claim promotion gate", "boolean", "no MISSING markers, all source paths real, no-cancellation, arena projections ready", "PROMOTION_BLOCKED_NOW", "all_local_arenas"),
    ]
    return [
        add_common(
            {
                "acquisition_id": acquisition_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "required_inputs": required,
                "current_status": status,
                "arena_links": arenas,
                "current_value": "2.1e-18 yr^-1" if symbol == "b_alpha*tau_clock_time" else "MISSING",
                "source_hint": ";".join(
                    str(p)
                    for p in [
                        SRC_944_FRAME,
                        SRC_1028_PACK,
                        SRC_1030_PROVENANCE,
                        SRC_1156_FILL,
                        SRC_2761_PRODUCTS,
                        SRC_1092_BALPHA,
                    ]
                ),
                "promotion_allowed_now": False,
            }
        )
        for acquisition_id, symbol, definition, units, required, status, arenas in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2915_0_R10", "R10", "reject naked linear c_g; require beta_s beta_t or source-backed source leg plus K_X/Qbar/tau_R10/bound curve", "NAKED_LINEAR_CG_FORBIDDEN", "no R10 score"),
        ("ARENA2915_1_PPN", "PPN", "common Weyl/disformal response requires gauge-fixed gamma/beta/preferred-frame kernels and disformal separation", "MISSING_PPN_RESPONSE_MATRIX", "no PPN pass"),
        ("ARENA2915_2_clock", "clock/EM", "b_alpha*tau_clock product is source-backed nonclaim, but standalone b_alpha and cross-arena transfer are blocked", "PARTIAL_CLOCK_PRODUCT_ONLY", "clock product retained, no local transfer"),
        ("ARENA2915_3_WEP", "WEP/material", "b_A/b_alpha material sensitivities and source leg must be same-branch, not borrowed from clock product", "MISSING_MATERIAL_SOURCE_MAP", "no WEP/local claim"),
        ("ARENA2915_4_source_orbital", "source/orbital", "q_nonH, Delta_W_support and tau-normal lock must be zero or bounded", "MISSING_SOURCE_SUPPORT_ZERO_OR_BOUND", "no Newton/orbital claim"),
        ("ARENA2915_5_local_GR", "local GR/Newton", "C_shadow_abs and DqZ heads must be closed plus EH/source/PPN gates", "BLOCKED_NONCLAIM", "no local GR claim"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "rule": rule,
                "current_status": status,
                "claim_effect": effect,
            }
        )
        for arena_id, arena, rule, status, effect in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2915_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked"),
        ("RUN2915_1_components", "CSHADOW_COMPONENTS_SPLIT", "c_g,b_dis,b_A,b_alpha,q_nonH,Delta_W_support,Delta_tau_n", True, "component envelope now explicit"),
        ("RUN2915_2_zero_theorem", "CSHADOW_ZERO_NOT_DERIVED", "all component zero clauses", False, "no parent branch signs all no-shadow/no-marker/source-support clauses"),
        ("RUN2915_3_balpha_partial", "BALPHA_CLOCK_PRODUCT_RETAINED_NONCLAIM", "b_alpha*tau_clock_time", True, "first numeric product exists but cannot transfer"),
        ("RUN2915_4_linear_cg_guard", "LEGACY_LINEAR_CG_QUARANTINE_ACTIVE", "R10 c_g branch", True, "require beta_s beta_t or declared source leg"),
        ("RUN2915_5_next", "2916_CG_INVARIANT_PRODUCT_SELECTED", "next target", False, "fix c_g product normal form before using it in R10/local rows"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2915_0_components", "C_shadow component envelope is explicit", "PASS_NONCLAIM_STRUCTURE", "components are named and source routes are attached", True),
        ("CG2915_1_Cshadow_zero", "C_shadow=0 follows for current MTS", "BLOCKED_NONCLAIM", "no-shadow/no-marker/non-Hilbert/support clauses do not close", False),
        ("CG2915_2_cg_score", "c_g finite branch can be scored", "BLOCKED_NONCLAIM", "raw linear c_g is quarantined and finite c_g/source leg is missing", False),
        ("CG2915_3_balpha_clock", "b_alpha clock product is usable as local/GR input", "BLOCKED_TRANSFER", "numeric product is clock-only nonclaim; standalone b_alpha and tau transfer missing", False),
        ("CG2915_4_disformal_source", "b_dis/q_nonH/support rows are score-ready", "BLOCKED_NONCLAIM", "all remain theorem-zero or numeric-source missing", False),
        ("CG2915_5_DqZ_geometry", "DqZ_geometry bound is score-ready", "BLOCKED_NONCLAIM", "C_shadow_abs and DqZ heads remain missing", False),
        ("CG2915_6_local_GR_Newton", "local GR/Newton follows after 2915", "BLOCKED_NONCLAIM", "2915 is component acquisition, not a local-GR proof", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2915_0_result", "Cshadow_componentized_not_killed", "The shadow term is now split into c_g, b_dis, b_A, b_alpha, q_nonH and support/tau pieces, but no component is theorem-zero for current MTS.", "keep C_shadow_abs as strict finite envelope"),
        ("DEC2915_1_partial_win", "b_alpha_clock_product_retained_only", "A real source-backed clock product exists, but it cannot be used as standalone b_alpha or transferred to WEP/R10/local rows.", "preserve as nonclaim clock-only evidence"),
        ("DEC2915_2_cg_guard", "linear_cg_shortcut_rejected", "The old alpha(lambda)~c_g shorthand is invalid unless a source leg is explicitly sourced; universal source-test coupling needs beta_s beta_t/c_g^2 style handling.", "derive invariant c_g product normal form next"),
        ("DEC2915_3_next", "2916_cg_product_or_disformal_kernel", "The highest-leverage next step is to make the c_g branch physically well-formed before any R10/local testing; if that fails, disformal PPN kernel becomes first concrete component row.", "select 2916"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2915_0_2916",
                "selection_status": "selected_primary",
                "target_file": "2916-Y5-R2FR-Cshadow-cg-invariant-source-test-product-or-disformal-PPN-kernel-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Cshadow_cg_invariant_source_test_product_or_disformal_PPN_kernel_under_AX1090_2916.py",
                "task": "derive the invariant source-test product law for c_g inside C_shadow/R10/local geometry, rejecting naked linear c_g unless a source leg is parent-signed; if it fails, stage disformal PPN kernel rows",
                "success_condition": "c_g contribution is rewritten as beta_s beta_t or sourced source-leg product with K_X/Qbar/tau projections, units and no MISSING markers, or c_g is parent theorem-zero",
                "fallback_condition": "keep c_g branch nonclaim and move to b_dis preferred-frame/PPN kernel acquisition",
                "guardrails": "no naked linear c_g R10 scoring; no cancellation among C_shadow components; no local GR/Newton/R10/PPN claim; no source-less numeric values; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("zero_copy", OUTPUTS["zero_attempt"], BRANCH_OUTPUTS["zero_copy"]),
        ("component_copy", OUTPUTS["components"], BRANCH_OUTPUTS["component_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    component_rows_: list[dict[str, Any]],
    zero_rows_: list[dict[str, Any]],
    acquisition_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    zero_verdict = next(row for row in zero_rows_ if row["attempt_id"] == "ZTH2915_6_verdict")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2915_6_local_GR_Newton")
    component_symbols = {str(row["symbol"]) for row in component_rows_}
    acquisition_symbols = {str(row["symbol"]) for row in acquisition_rows_}
    required_components = {"C_shadow_abs", "c_g", "b_dis", "b_A", "b_alpha", "q_nonH", "Delta_W_support;Delta_tau_n"}
    required_acquisition = {"C_shadow_abs", "Z_cg", "c_g", "beta_s_beta_t_or_source_leg", "b_dis", "b_A", "b_alpha*tau_clock_time", "q_nonH", "Delta_W_support;Delta_tau_n", "promotion_rule"}
    balpha_product = next(row for row in acquisition_rows_ if row["symbol"] == "b_alpha*tau_clock_time")
    cg_product_rule = next(row for row in acquisition_rows_ if row["symbol"] == "beta_s_beta_t_or_source_leg")
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2915_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2915_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2915_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2915_3_components_complete", required_components.issubset(component_symbols), "C_shadow component symbols complete"),
        ("VAL2915_4_zero_not_promoted", zero_verdict["current_status"] == "CSHADOW_ZERO_NOT_DERIVED_CURRENT_MTS" and not bool(zero_verdict["theorem_zero_adopted"]), "C_shadow zero theorem remains unpromoted"),
        ("VAL2915_5_acquisition_complete", required_acquisition.issubset(acquisition_symbols), "component acquisition rows complete"),
        (
            "VAL2915_6_balpha_product_nonclaim",
            balpha_product["current_value"] == "2.1e-18 yr^-1" and not bool(balpha_product["valid_for_claim"]) and not bool(balpha_product["promotion_allowed_now"]),
            "b_alpha clock product retained as numeric nonclaim only",
        ),
        (
            "VAL2915_7_linear_cg_quarantined",
            cg_product_rule["current_status"] == "NAKED_LINEAR_CG_FORBIDDEN" and not bool(cg_product_rule["valid_for_claim"]),
            "naked linear c_g is forbidden for scoring",
        ),
        (
            "VAL2915_8_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2915_9_next_target_selected", next_rows_[0]["route_id"] == "NEXT2915_0_2916" and bool(next_rows_[0]["selected"]), "2916 c_g invariant product target selected"),
        ("VAL2915_10_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2915_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2915_12_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2915_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2915 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    component_rows_: list[dict[str, Any]],
    zero_rows_: list[dict[str, Any]],
    acquisition_rows_: list[dict[str, Any]],
    arena_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2915_OVERALL")
    text = f"""# 2915 - Y5/R2FR Cshadow Component Bound Pack Or Cobs Parent Normalization Proof Under AX1090

Status: `Y5_R2FR_2915_Cshadow_componentized_zero_not_derived_balpha_clock_product_nonclaim_linear_cg_quarantined_2916_next`

Claim ceiling: `Cshadow_component_pack_nonclaim_only_no_Cshadow_zero_no_DqZ_geometry_pass_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2915 splits the shadow beast properly. The dangerous term is no longer a single foggy `C_shadow_abs`; it is the absolute no-cancellation envelope

`C_shadow_abs = |tau_geom_cg c_g| + |tau_geom_dis b_dis| + |tau_geom_A b_A| + |tau_geom_alpha b_alpha| + |q_nonH| + |Delta_W_support| + |Delta_tau_n|`.

The zero theorem is exact as a future target, but not current evidence. To set `C_shadow_abs=0`, one parent branch must sign terminal public coframe/no-shadow, no disformal slot, quotient-owned constants, Hilbert/Noether source ownership, support equivalence, tau-normal lock and readout closure. Current MTS does not sign that package.

There is one partial win: the `b_alpha*tau_clock_time` clock product is source-backed and retained as nonclaim, `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1`. But it cannot become standalone `b_alpha`, and it cannot be exported to WEP/R10/local-GR without a same-branch tau/projection map.

The most important guard is also now explicit: naked linear `c_g` is forbidden for R10/source-test scoring. A force prediction needs a source-test product such as `beta_s beta_t`, or a source-backed source leg declared inside `Qbar_XH`; otherwise the old `alpha(lambda) ~ c_g` row is underfactored.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Cshadow Component Envelope

{md_table(component_rows_, ["component_id", "symbol", "current_status", "absolute_formula", "units", "arena_links", "guardrail", "numeric_bound_present", "valid_for_claim"])}

## Cshadow Zero-Theorem Attempt

{md_table(zero_rows_, ["attempt_id", "target", "current_status", "statement", "would_prove", "blocking_gap", "theorem_zero_adopted", "valid_for_claim"])}

## Component Acquisition Rows

{md_table(acquisition_rows_, ["acquisition_id", "symbol", "current_status", "definition", "units", "required_inputs", "current_value", "arena_links", "promotion_allowed_now", "valid_for_claim"])}

## Arena Routing And Product Rules

{md_table(arena_rows_, ["arena_id", "arena", "current_status", "rule", "claim_effect", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is a useful choke-point result. The project has not derived local GR, but the local failure mode is becoming mechanically inspectable:

1. `C_Obs_e` is probably harmless normalization if the public-coframe branch is signed.
2. `C_shadow_abs` is the live hidden-frame/source-support problem.
3. `b_alpha` has one real clock product, but not a transferable local coefficient.
4. `c_g` is high leverage, but the old linear R10 shorthand is not physically safe.

That makes 2916 the right next punch: derive the invariant c_g source-test product law or demote c_g and move to the disformal PPN kernel.

## Not Claimed

- `C_shadow_abs=0` is not derived.
- `c_g`, `b_dis`, `b_A`, `b_alpha`, `q_nonH`, `Delta_W_support`, or `Delta_tau_n` are not claim-valid local inputs.
- The `b_alpha*tau_clock_time` product is retained only as clock-sector nonclaim evidence.
- Naked linear `c_g` is forbidden for R10/source-test scoring.
- `DqZ_geometry=0`, Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    component_rows_ = component_rows()
    zero_rows_ = zero_attempt_rows()
    acquisition_rows_ = acquisition_rows()
    arena_rows_ = arena_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["components"], component_rows_)
    write_csv(OUTPUTS["zero_attempt"], zero_rows_)
    write_csv(OUTPUTS["acquisition"], acquisition_rows_)
    write_csv(OUTPUTS["arena"], arena_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        component_rows_,
        zero_rows_,
        acquisition_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        component_rows_,
        zero_rows_,
        acquisition_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        component_rows_,
        zero_rows_,
        acquisition_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        component_rows_,
        zero_rows_,
        acquisition_rows_,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2915_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
