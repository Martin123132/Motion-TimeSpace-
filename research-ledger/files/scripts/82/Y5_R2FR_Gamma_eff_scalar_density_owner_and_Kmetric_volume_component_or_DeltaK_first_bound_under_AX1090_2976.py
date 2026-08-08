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
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2976"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2976-Y5-R2FR-Gamma-eff-scalar-density-owner-and-Kmetric-volume-component-or-DeltaK-first-bound-under-AX1090.md"

SRC_2975_DOC = ROOT / "2975-Y5-R2FR-GammaKhat-sign-convention-and-metric-response-certificate-or-DeltaK-bound-row-under-AX1090.md"
SRC_2975_NEXT = RESIDUALS / "P8_Y5_R2FR_2975_NEXT_TARGET.csv"
SRC_2975_SIGN = RESIDUALS / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv"
SRC_2975_METRIC = RESIDUALS / "P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv"
SRC_2975_DELTAK = RESIDUALS / "P8_Y5_R2FR_2975_DELTAK_COMPONENT_BOUND_ROWS_NONCLAIM.csv"
SRC_2975_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2975_VALIDATION.csv"

SRC_1649_SYMBOL = RAB_QUEUE / "JR1649_REDUCED_GK_SYMBOL_MATCH_AUDIT_NONCLAIM.csv"
SRC_1712_CONJ = RAB_QUEUE / "JR1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv"
SRC_1712_ID = RAB_QUEUE / "JR1712_METRIC_RESPONSE_IDENTITY_AUDIT.csv"
SRC_2217_DENSITY = BETA_DOCS / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv"
SRC_2218_KCOMP = BETA_DOCS / "PARENT_QLOC_KMETRIC_COMPONENTS_2218_NONCLAIM.csv"
SRC_2219_KOWNER = BETA_DOCS / "PARENT_QLOC_KHAT_SOURCE_OWNER_2219_NONCLAIM.csv"
SRC_2221_KERNEL = BETA_DOCS / "PARENT_QLOC_DELTAG_SGAMMA_KMETRIC_KERNEL_FRONTIER_2221_NONCLAIM.csv"
SRC_2799_ACTION = BETA_DOCS / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv"
SRC_2808_METRIC = BETA_DOCS / "GAMMA_KHAT_METRIC_RESPONSE_2808_NONCLAIM.csv"
SRC_2815_SIGN = BETA_DOCS / "KMETRIC_HILBERT_SIGN_DERIVATION_2815_NONCLAIM.csv"
SRC_2816_NORM = BETA_DOCS / "KMETRIC00_KERNEL_NORMALIZATION_2816_NONCLAIM.csv"
SRC_2817_DZ = BETA_DOCS / "STRICT_DOUBLE_ZERO_COEFFICIENT_KILL_2817_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2976_SOURCE_REGISTER.csv",
    "gamma": RESIDUALS / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "kvol": RESIDUALS / "P8_Y5_R2FR_2976_KMETRIC_VOLUME_COMPONENT_ATTEMPT.csv",
    "deltak_vol": RESIDUALS / "P8_Y5_R2FR_2976_DELTAK_VOL_BOUND_ROW_NONCLAIM.csv",
    "rollforward": RESIDUALS / "P8_Y5_R2FR_2976_QLOC_DELTAK_ROLLFORWARD_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2976_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2976_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2976_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2976_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2976_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gamma_copy": PARENT_ACTION / "Gamma_eff_scalar_density_and_Kvol_2976_NOT_DERIVED.csv",
    "deltak_copy": LOCAL_BOUNDS / "DeltaK_vol_bound_row_2976_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2976_response_doublet_density_owner_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


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
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2976_00_2975_doc", SRC_2975_DOC, "NEXT2975_0_2976;K_vol", "2975 selected Gamma_eff/K_vol target"),
        ("SRC2976_01_2975_next", SRC_2975_NEXT, "NEXT2975_0_2976", "machine next-target row"),
        ("SRC2976_02_2975_sign", SRC_2975_SIGN, "SIGN2975_0_canonical;SIGN2975_2_DeltaK", "canonical q_loc-positive sign convention"),
        ("SRC2976_03_2975_metric", SRC_2975_METRIC, "MR2975_0_Gamma_density;MR2975_2_components", "metric-response audit"),
        ("SRC2976_04_2975_deltak", SRC_2975_DELTAK, "DK2975_1_Kvol;DK2975_8_score_gate", "Delta_K rows to refine"),
        ("SRC2976_05_2975_validation", SRC_2975_VALIDATION, "VAL2975_OVERALL", "2975 validation"),
        ("SRC2976_06_1649_symbol", SRC_1649_SYMBOL, "RGM1649_1_Gamma_scalar_density;RGM1649_7_verdict", "reduced GK symbol match audit"),
        ("SRC2976_07_1712_conj", SRC_1712_CONJ, "CJA1712_1_even_density;CJA1712_6_verdict", "response-displacement conjugacy attempt"),
        ("SRC2976_08_1712_identity", SRC_1712_ID, "MRI1712_0_Z_variation;MRI1712_4_verdict", "metric-response identity audit"),
        ("SRC2976_09_2217_density", SRC_2217_DENSITY, "RDP2217_0_parent_action_ansatz;RDP2217_4_density_verdict", "response-doublet density candidate"),
        ("SRC2976_10_2218_kcomp", SRC_2218_KCOMP, "KMC2218_0_volume;KMC2218_6_verdict", "K_metric component split"),
        ("SRC2976_11_2219_kowner", SRC_2219_KOWNER, "KSO2219_1_metric_response_scalar_density;KSO2219_8_verdict", "Khat source-owner alternatives"),
        ("SRC2976_12_2221_kernel", SRC_2221_KERNEL, "KNA2221_0_delta_g_SGamma;KNA2221_7_units_projection", "Delta_g S_Gamma/Kmetric kernel frontier"),
        ("SRC2976_13_2799_action", SRC_2799_ACTION, "GKT2799_0_variational_route;GKT2799_6_verdict", "GK action existence route"),
        ("SRC2976_14_2808_metric", SRC_2808_METRIC, "MRD2808_1_stress_split;MRD2808_6_verdict", "metric-response sign route"),
        ("SRC2976_15_2815_sign", SRC_2815_SIGN, "KHS2815_0_stress_split;KHS2815_3_export_blocker", "Hilbert sign derivation"),
        ("SRC2976_16_2816_norm", SRC_2816_NORM, "KNM2816_0_metric_slot;KNM2816_3_units", "Kmetric00 kernel normalization"),
        ("SRC2976_17_2817_dz", SRC_2817_DZ, "CK2817_0_canonical_formula;CK2817_4_verdict", "strict double-zero coefficient kill"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        anchors_ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "exists": path.exists(),
                    "anchors_required": anchors,
                    "anchors_found": anchors_ok,
                    "missing_anchors": missing,
                    "role": role,
                }
            )
        )
    return rows


def gamma_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GAM2976_0_density_ansatz",
            "Gamma_eff",
            "Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
            "FORMAL_RESPONSE_DOUBLET_CANDIDATE",
            "candidate is written, not adopted as the current MTS parent density",
            SRC_2217_DENSITY,
        ),
        (
            "GAM2976_1_scalar_density",
            "sqrt(-g) Gamma_eff",
            "local diffeomorphism scalar-density slot for S_GK=-int sqrt(-g) Gamma_eff",
            "DENSITY_SLOT_FORMAL_ONLY",
            "field content, branch domain, units and metric dependence are incomplete",
            SRC_2799_ACTION,
        ),
        (
            "GAM2976_2_exchange_evenness",
            "E:Z->-Z",
            "exchange-even density forbids a linear Z source if source/readout sectors are also even",
            "CONDITIONAL_TEMPLATE_ONLY",
            "Y5/Y6/source/readout even-channel debt remains open",
            SRC_2217_DENSITY,
        ),
        (
            "GAM2976_3_background",
            "Gamma0",
            "Gamma0 must be constant or background-subtracted so nabla Gamma0 does not source q_loc",
            "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "subtraction exists as a candidate but not a parent-owned branch rule",
            SRC_2217_DENSITY,
        ),
        (
            "GAM2976_4_MAB",
            "M_AB",
            "H_AB=partial_A partial_B Gamma_eff|_{Z=0}=M_AB",
            "MISSING_MAB_OWNER_UNITS_POSITIVITY",
            "M_AB source, units, positivity and gauge/constraint removal not closed",
            SRC_2217_DENSITY,
        ),
        (
            "GAM2976_5_Zbasis",
            "Z^A",
            "response-displacement direction must equal the actual quotient-vertical/local residual generator",
            "MISSING_Z_BASIS_PHYSICAL_LOCK",
            "2973 kept full Z physical lock failed",
            SRC_1712_CONJ,
        ),
        (
            "GAM2976_6_verdict",
            "Gamma_eff scalar density owner",
            "source-backed Gamma_eff with fields, units, metric dependence and parent branch signature",
            "NOT_PARENT_SIGNED_KVOL_TEMPLATE_ONLY",
            "use DeltaK_vol bound row until density ownership closes",
            SRC_1649_SYMBOL,
        ),
    ]
    return [
        add_common(
            {
                "gamma_audit_id": gamma_id,
                "object": obj,
                "candidate_or_requirement": statement,
                "status": status,
                "blocking_gap": gap,
                "source_path": str(source),
                "parent_signed": False,
                "finite_value_present": False,
                "accepted_for_scoring": False,
            }
        )
        for gamma_id, obj, statement, status, gap, source in rows
    ]


def kvol_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KV2976_0_template",
            "K_vol^{mu nu}",
            "K_vol^{mu nu} := Gamma_eff g^{mu nu} in the 2975 q_loc-positive bookkeeping convention",
            "T_q=Gamma_eff g-K_hat and T_metric=Gamma_eff g-K_metric",
            "BOOKKEEPING_TEMPLATE_LOCKED",
            SRC_2975_SIGN,
        ),
        (
            "KV2976_1_variation_origin",
            "volume variation",
            "K_vol is the convention-dependent Gamma_eff g^{mu nu} term after varying sqrt(-g)",
            "requires declared volume/sign convention and no mixed metric slot",
            "FORMAL_SHAPE_ONLY",
            SRC_2218_KCOMP,
        ),
        (
            "KV2976_2_metric_slot",
            "covariant g_{mu nu} slot",
            "Kmetric-chain kernels use the same covariant metric slot as the 2808 Hilbert definition",
            "prevents covariant/contravariant sign mixing",
            "SLOT_LOCKED_NONCLAIM",
            SRC_2816_NORM,
        ),
        (
            "KV2976_3_Khat_vol",
            "K_hat_vol",
            "live K_hat volume slot must equal Gamma_eff g^{mu nu} for DeltaK_vol=0",
            "requires current K_hat source owner and component comparison",
            "MISSING_KHAT_VOL_MATCH",
            SRC_2219_KOWNER,
        ),
        (
            "KV2976_4_units",
            "K_vol units",
            "K_vol has stress-density units only after Gamma_eff units and metric normalization are declared",
            "Gamma_eff units, Z/M units and source pairing are missing",
            "UNITS_NOT_CLOSED",
            SRC_2218_KCOMP,
        ),
        (
            "KV2976_5_score",
            "K_vol score value",
            "no numeric or theorem-zero K_vol score is available",
            "needs Gamma_eff value/profile and Khat_vol comparison",
            "NOT_SCORE_READY",
            SRC_2975_DELTAK,
        ),
    ]
    return [
        add_common(
            {
                "kvol_id": kvol_id,
                "object": obj,
                "definition_or_statement": statement,
                "condition_or_meaning": condition,
                "status": status,
                "source_path": str(source),
                "template_locked": kvol_id in {"KV2976_0_template", "KV2976_2_metric_slot"},
                "parent_signed": False,
                "finite_value_present": False,
                "accepted_for_scoring": False,
            }
        )
        for kvol_id, obj, statement, condition, status, source in rows
    ]


def deltak_vol_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DKV2976_0_definition",
            "DeltaK_vol^{mu nu}",
            "DeltaK_vol^{mu nu}:=K_hat_vol^{mu nu}-Gamma_eff g^{mu nu}",
            "stress",
            "DEFINITION_LOCKED_NONCLAIM",
            "Khat_vol source owner and Gamma_eff scalar density",
            SRC_2975_DELTAK,
        ),
        (
            "DKV2976_1_absolute_bound",
            "||DeltaK_vol||",
            "||DeltaK_vol|| <= ||K_hat_vol|| + ||Gamma_eff g||",
            "stress norm",
            "MISSING_KHAT_VOL_AND_GAMMA_NORMS",
            "same-frame norm, Gamma_eff profile, Khat_vol profile",
            SRC_2218_KCOMP,
        ),
        (
            "DKV2976_2_zero_route",
            "DeltaK_vol=0",
            "if K_hat_vol=Gamma_eff g in the same metric slot and volume convention",
            "theorem condition",
            "MISSING_KHAT_VOL_COMPONENT_CERTIFICATE",
            "Khat component comparison table",
            SRC_2219_KOWNER,
        ),
        (
            "DKV2976_3_q_loc_insert",
            "eps_DeltaK_vol",
            "eps_DeltaK_vol <= q_*^{-1}(C_Ploc D_DeltaK_vol + C_comm_vol ||DeltaK_vol||)",
            "dimensionless after q_*",
            "MISSING_QSTAR_PROJECTOR_CONSTANTS_AND_DERIVATIVES",
            "q_*, C_Ploc, C_comm_vol, DeltaK_vol derivative constants",
            SRC_2975_DELTAK,
        ),
        (
            "DKV2976_4_no_cancellation",
            "absolute envelope",
            "DeltaK_vol cannot cancel DeltaK_deltaM/deltaZ/deriv/boundary or Ward terms without a parent identity",
            "guardrail",
            "NO_CANCELLATION_GUARD_ACTIVE",
            "parent identity proving cancellation",
            SRC_2975_DELTAK,
        ),
    ]
    return [
        add_common(
            {
                "deltak_vol_id": row_id,
                "symbol": symbol,
                "definition_or_bound": definition,
                "units": units,
                "status": status,
                "required_input": required,
                "source_path": str(source),
                "lower_bound": 0,
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "finite_value_present": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, status, required, source in rows
    ]


def rollforward_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RF2976_0_DeltaK_split",
            "Delta_K",
            "Delta_K = DeltaK_vol + DeltaK_deltaM + DeltaK_deltaZ + DeltaK_deriv + DeltaK_boundary",
            "extends 2975 component split with volume row isolated",
        ),
        (
            "RF2976_1_DDelta_split",
            "D_Delta",
            "D_Delta <= D_vol + D_deltaM + D_deltaZ + D_deriv + D_boundary plus connection constants",
            "first volume derivative row must be bounded before q_loc scoring",
        ),
        (
            "RF2976_2_double_zero_note",
            "strict double-zero",
            "F(m_*)=F'(m_*)=0 can kill algebraic chain coefficients but not K_vol, hidden kernels or boundary terms by itself",
            "prevents overclaiming the useful 2817 lemma",
        ),
        (
            "RF2976_3_score_policy",
            "eps_q_loc_component",
            "keep absolute sum over Ward, DeltaK_vol and remaining Delta_K pieces until source-backed cancellations exist",
            "no local-GR or arena score promotion",
        ),
    ]
    return [
        add_common(
            {
                "rollforward_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "meaning": meaning,
                "source_path": str(SRC_2817_DZ if row_id == "RF2976_2_double_zero_note" else SRC_2975_DELTAK),
                "accepted_for_scoring": False,
            }
        )
        for row_id, quantity, formula, meaning in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2976_0_gamma_candidate", "formal Gamma_eff response-doublet density candidate exists", True, "FORMAL_TEMPLATE_ONLY_NOT_PARENT_CLAIM"),
        ("CG2976_1_gamma_owner", "Gamma_eff scalar density parent-signed", False, "GAMMA_OWNER_MISSING"),
        ("CG2976_2_kvol_template", "K_vol bookkeeping template locked", True, "BOOKKEEPING_TEMPLATE_ONLY"),
        ("CG2976_3_khat_vol_match", "K_hat_vol equals Gamma_eff g", False, "KHAT_VOL_MATCH_MISSING"),
        ("CG2976_4_deltak_vol_zero", "DeltaK_vol=0", False, "DELTAK_VOL_RETAINED"),
        ("CG2976_5_q_loc_score", "eps_q_loc_component score-ready", False, "QLOC_SCORE_INPUTS_MISSING"),
        ("CG2976_6_local_GR", "local GR/Newton reduction", False, "LOCAL_GR_NOT_DERIVED"),
        ("CG2976_7_arena_claims", "R10/PPN/clock/orbital/WEP claims", False, "NO_ARENA_CLAIM_ALLOWED"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2976_0_formal_density",
            "Keep the response-doublet Gamma_eff density as the best formal candidate.",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) gives the desired double-zero shape.",
            "do not promote until M_AB, Z basis, units, source-current and boundary clauses close",
        ),
        (
            "DEC2976_1_kvol",
            "K_vol template is now isolated under the 2975 convention.",
            "K_vol=Gamma_eff g is a bookkeeping component, not a source-backed tensor match.",
            "retain DeltaK_vol",
        ),
        (
            "DEC2976_2_double_zero",
            "The 2817 double-zero coefficient kill is useful but not sufficient.",
            "it attacks algebraic chain pieces, not K_vol, hidden kernels or live Khat adoption.",
            "keep it as support for later K_deltaM/K_deltaZ rows",
        ),
        (
            "DEC2976_3_next",
            "The next derivation target is response-doublet ownership of M_AB and Z^A.",
            "without M_AB/Z units and physical lock, Gamma_eff remains a formal ansatz.",
            "run 2977 on M_AB/Z owner, units, and no-linear-source lock",
        ),
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
        for decision_id, decision, because, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2976_0_2977",
                "priority": "selected_primary",
                "next_doc": "2977-Y5-R2FR-response-doublet-MAB-Zbasis-owner-and-no-linear-source-lock-or-DeltaK-deltaM-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_response_doublet_MAB_Zbasis_owner_and_no_linear_source_lock_or_DeltaK_deltaM_row_under_AX1090_2977.py",
                "objective": "Try to parent-sign the response-doublet Gamma_eff density by sourcing M_AB, Z^A, units, positivity and no-linear-source/source-current silence; if not, emit DeltaK_deltaM/DeltaK_deltaZ bound rows.",
                "include": "M_AB;Z^A;R_even;Gamma0 subtraction;units;positivity;exchange evenness;no linear source;J_Z;B_Z;DeltaK_deltaM;DeltaK_deltaZ",
                "exclude": "plateau axiom;bookkeeping stress claim;full K_metric certificate;full Z-basis scoring;Y5/Y6/PPN closure;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "copy_id": "COPY2976_0_gamma",
                "source_output": str(OUTPUTS["gamma"]),
                "branch_copy": str(BRANCH_OUTPUTS["gamma_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2976_1_deltak",
                "source_output": str(OUTPUTS["deltak_vol"]),
                "branch_copy": str(BRANCH_OUTPUTS["deltak_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2976_2_next",
                "source_output": str(OUTPUTS["next"]),
                "branch_copy": str(BRANCH_OUTPUTS["next_copy"]),
                "status": "copied",
            }
        ),
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources = all_rows["sources"]
    gamma = all_rows["gamma"]
    kvol = all_rows["kvol"]
    deltak = all_rows["deltak_vol"]
    claims = all_rows["claims"]
    next_rows = all_rows["next"]

    checks = [
        ("VAL2976_0_sources_exist", all(row["exists"] for row in sources), "all cited local source paths exist", True),
        ("VAL2976_1_anchors_found", all(row["anchors_found"] for row in sources), "all cited source anchors found", True),
        (
            "VAL2976_2_gamma_candidate_present",
            any(row["gamma_audit_id"] == "GAM2976_0_density_ansatz" and row["status"] == "FORMAL_RESPONSE_DOUBLET_CANDIDATE" for row in gamma),
            "formal Gamma_eff response-doublet candidate present",
            True,
        ),
        (
            "VAL2976_3_gamma_not_parent_signed",
            any(row["gamma_audit_id"] == "GAM2976_6_verdict" and row["status"] == "NOT_PARENT_SIGNED_KVOL_TEMPLATE_ONLY" for row in gamma),
            "Gamma_eff scalar-density owner remains unproved",
            True,
        ),
        (
            "VAL2976_4_kvol_template_locked",
            any(row["kvol_id"] == "KV2976_0_template" and row["status"] == "BOOKKEEPING_TEMPLATE_LOCKED" for row in kvol),
            "K_vol bookkeeping template isolated under 2975 convention",
            True,
        ),
        (
            "VAL2976_5_deltak_vol_nonclaim",
            any(row["deltak_vol_id"] == "DKV2976_0_definition" for row in deltak) and all(not row["accepted_for_scoring"] for row in deltak),
            "DeltaK_vol bound rows exist and remain nonclaim",
            True,
        ),
        (
            "VAL2976_6_no_cancellation",
            any(row["deltak_vol_id"] == "DKV2976_4_no_cancellation" and row["status"] == "NO_CANCELLATION_GUARD_ACTIVE" for row in deltak),
            "absolute no-cancellation guard present",
            True,
        ),
        (
            "VAL2976_7_claims_blocked_except_templates",
            all(
                (row["claim_gate_id"] in {"CG2976_0_gamma_candidate", "CG2976_2_kvol_template"} and row["condition_passed"])
                or (not row["condition_passed"])
                for row in claims
            ),
            "all physics claim gates remain blocked except formal/template rows",
            True,
        ),
        (
            "VAL2976_8_next_target_written",
            bool(next_rows) and next_rows[0]["next_id"] == "NEXT2976_0_2977",
            "2977 response-doublet M_AB/Z owner target selected",
            True,
        ),
        ("VAL2976_9_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        (
            "VAL2976_10_csvs_parse",
            all(csv_parses(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"]) and all(csv_parses(path) for path in BRANCH_OUTPUTS.values()),
            "all generated CSV files parse",
            True,
        ),
        (
            "VAL2976_11_outputs_under_post_checkpoint",
            all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL2976_12_formalization_clean",
            not any(FORMALIZATION.rglob("*2976*")) if FORMALIZATION.exists() else True,
            "no 2976 outputs were written to formalization-workbench",
            True,
        ),
        ("VAL2976_13_doc_written", DOC.exists(), "2976 markdown checkpoint exists", True),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2976_OVERALL", "passed": overall, "check": "2976 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2976 — Gamma_eff Scalar-Density Owner and Kmetric Volume Component, or DeltaK_vol Bound

Status: `Y5_R2FR_2976_Gamma_eff_formal_density_retained_Kvol_template_locked_DeltaK_vol_bound_written_nonclaim`

Claim ceiling: `no_parent_signed_Gamma_eff_no_Khat_vol_match_no_DeltaK_vol_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The best formal density candidate remains `Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)`.
- This is useful: it gives the double-zero shape we want, but it is not parent-signed because `M_AB`, `Z^A`, units, positivity, source-current silence and boundary terms are still open.
- Under the `2975` sign convention, the bookkeeping volume component is now isolated as `K_vol^{{mu nu}} := Gamma_eff g^{{mu nu}}`.
- That is not a live tensor match: `K_hat_vol = Gamma_eff g` is not proved, so `DeltaK_vol := K_hat_vol - Gamma_eff g` is retained.
- Next target is the response-doublet owner lock: `M_AB`, `Z^A`, units, exchange-even/no-linear-source, `J_Z`, and `B_Z`.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## Gamma_eff Scalar-Density Audit

{md_table(all_rows["gamma"], ["gamma_audit_id", "object", "candidate_or_requirement", "status", "blocking_gap", "parent_signed"])}

## K_vol Component Attempt

{md_table(all_rows["kvol"], ["kvol_id", "object", "definition_or_statement", "status", "template_locked", "parent_signed", "accepted_for_scoring"])}

## DeltaK_vol Bound Rows

{md_table(all_rows["deltak_vol"], ["deltak_vol_id", "symbol", "definition_or_bound", "units", "status", "required_input", "upper_bound", "accepted_for_scoring"])}

## q_loc / Delta_K Rollforward

{md_table(all_rows["rollforward"], ["rollforward_id", "quantity", "formula", "meaning", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "gamma": gamma_rows(),
        "kvol": kvol_rows(),
        "deltak_vol": deltak_vol_rows(),
        "rollforward": rollforward_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["gamma"], BRANCH_OUTPUTS["gamma_copy"])
    shutil.copyfile(OUTPUTS["deltak_vol"], BRANCH_OUTPUTS["deltak_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2976 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
