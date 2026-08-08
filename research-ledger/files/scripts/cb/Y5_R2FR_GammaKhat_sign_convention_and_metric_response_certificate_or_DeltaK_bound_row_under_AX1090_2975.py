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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2975"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2975-Y5-R2FR-GammaKhat-sign-convention-and-metric-response-certificate-or-DeltaK-bound-row-under-AX1090.md"

SRC_2974_DOC = ROOT / "2974-Y5-R2FR-q_loc-component-owner-and-local-vacuum-identity-or-bound-row-under-AX1090.md"
SRC_2974_NEXT = RESIDUALS / "P8_Y5_R2FR_2974_NEXT_TARGET.csv"
SRC_2974_IDENTITY = RESIDUALS / "P8_Y5_R2FR_2974_QLOC_OWNER_IDENTITY_AUDIT.csv"
SRC_2974_BOUND = RESIDUALS / "P8_Y5_R2FR_2974_QLOC_BOUND_DECOMPOSITION_NONCLAIM.csv"
SRC_2974_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2974_VALIDATION.csv"

SRC_2206_WARD = BETA_DOCS / "PARENT_QLOC_WARD_IDENTITY_2206_NONCLAIM.csv"
SRC_2207_KMR = BETA_DOCS / "PARENT_QLOC_KHAT_METRIC_RESPONSE_AUDIT_2207_NONCLAIM.csv"
SRC_2218_KCOMP = BETA_DOCS / "PARENT_QLOC_KMETRIC_COMPONENTS_2218_NONCLAIM.csv"
SRC_2220_KHAT_BIRTH = BETA_DOCS / "PARENT_QLOC_TRACEFREE_KHAT_BIRTH_CERTIFICATE_2220_NONCLAIM.csv"
SRC_2799_ACTION = BETA_DOCS / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv"
SRC_2808_METRIC = BETA_DOCS / "GAMMA_KHAT_METRIC_RESPONSE_2808_NONCLAIM.csv"
SRC_2810_UNITS = BETA_DOCS / "PLOC_QDELTAK_UNIT_UPDATE_2810_NONCLAIM.csv"
SRC_2811_BOUND = BETA_DOCS / "PLOC_QDELTAK_BOUND_INTERFACE_2811_NONCLAIM.csv"
SRC_2812_ROLL = BETA_DOCS / "CPLOC_CCOMM_QDELTAK_BOUND_2812_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2975_SOURCE_REGISTER.csv",
    "sign": RESIDUALS / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "metric": RESIDUALS / "P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv",
    "deltak": RESIDUALS / "P8_Y5_R2FR_2975_DELTAK_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "rollforward": RESIDUALS / "P8_Y5_R2FR_2975_QLOC_BOUND_ROLLFORWARD_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2975_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2975_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2975_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2975_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2975_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "metric_copy": PARENT_ACTION / "GammaKhat_sign_metric_response_2975_NOT_DERIVED.csv",
    "deltak_copy": LOCAL_BOUNDS / "DeltaK_component_bound_rows_2975_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2975_Gamma_eff_scalar_density_owner_next_NONCLAIM.csv",
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
        ("SRC2975_00_2974_doc", SRC_2974_DOC, "NEXT2974_0_2975;sign-convention", "2974 selected Gamma/Khat sign and metric-response target"),
        ("SRC2975_01_2974_next", SRC_2974_NEXT, "NEXT2974_0_2975", "machine next-target row"),
        ("SRC2975_02_2974_identity", SRC_2974_IDENTITY, "ID2974_1_sign_convention;ID2974_7_verdict", "q_loc identity and sign guard"),
        ("SRC2975_03_2974_bound", SRC_2974_BOUND, "QB2974_2_DeltaK;QB2974_5_no_cancellation", "q_loc Delta_K fallback bound"),
        ("SRC2975_04_2974_validation", SRC_2974_VALIDATION, "VAL2974_OVERALL", "2974 validation"),
        ("SRC2975_05_2206_ward", SRC_2206_WARD, "WID2206_0_define_stress;WID2206_4_current_verdict", "opposite-sign Ward row"),
        ("SRC2975_06_2207_kmr", SRC_2207_KMR, "KMR2207_0_candidate_density_exists;KMR2207_5_overall", "K_hat metric-response evidence audit"),
        ("SRC2975_07_2218_kmetric", SRC_2218_KCOMP, "KMC2218_0_volume;KMC2218_6_verdict", "formal K_metric component split"),
        ("SRC2975_08_2220_khat_birth", SRC_2220_KHAT_BIRTH, "TIB2220_0_tensor_shape;TIB2220_9_verdict", "trace-free Khat birth certificate attempt"),
        ("SRC2975_09_2799_action", SRC_2799_ACTION, "GKT2799_0_variational_route;GKT2799_6_verdict", "action-existence theorem attempt"),
        ("SRC2975_10_2808_metric", SRC_2808_METRIC, "MRD2808_1_stress_split;MRD2808_6_verdict", "canonical metric-response sign route"),
        ("SRC2975_11_2810_units", SRC_2810_UNITS, "QDU2810_0_DeltaK;QDU2810_4_acceleration", "Delta_K units"),
        ("SRC2975_12_2811_bound", SRC_2811_BOUND, "QB2811_0_CPloc;QB2811_5_score_gate", "Delta_K bound interface"),
        ("SRC2975_13_2812_roll", SRC_2812_ROLL, "QBR2812_0_operator_zero_branch;QBR2812_3_score_gate", "Delta_K roll-forward envelope"),
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


def sign_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SIGN2975_0_canonical",
            "canonical q_loc-positive stress",
            "T_q^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "nabla_mu T_q^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}",
            "SELECTED_BOOKKEEPING_CONVENTION",
            SRC_2808_METRIC,
        ),
        (
            "SIGN2975_1_metric",
            "metric-response stress",
            "T_metric^{mu nu}:=Gamma_eff g^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "if K_hat=K_metric then q_loc^nu=P_loc nabla_mu T_metric^{mu nu}",
            "SELECTED_FOR_DELTAK_ACCOUNTING",
            SRC_2808_METRIC,
        ),
        (
            "SIGN2975_2_DeltaK",
            "Delta_K convention",
            "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}",
            "q_loc^nu=P_loc(nabla_mu T_metric^{mu nu})-P_loc(nabla_mu Delta_K^{mu nu}) plus projector/connection terms",
            "LOCKED_NONCLAIM_RESIDUAL_CONVENTION",
            SRC_2810_UNITS,
        ),
        (
            "SIGN2975_3_2206_translate",
            "opposite sign row translation",
            "T_2206^{mu nu}:=K_hat^{mu nu}-Gamma_eff g^{mu nu}=-T_q^{mu nu}",
            "Ward zero is sign-equivalent, but scoring must use the canonical q_loc-positive T_q",
            "TRANSLATED_NOT_USED_FOR_SCORING",
            SRC_2206_WARD,
        ),
        (
            "SIGN2975_4_guard",
            "sign/volume guard",
            "all Delta_K rows inherit the canonical T_q, K_metric and Delta_K definitions",
            "no mixed-sign cancellation or measured-G absorption allowed",
            "GUARD_ACTIVE",
            SRC_2974_IDENTITY,
        ),
    ]
    return [
        add_common(
            {
                "sign_id": sign_id,
                "object": obj,
                "definition": definition,
                "q_loc_relation": relation,
                "status": status,
                "source_path": str(source),
                "convention_selected": sign_id != "SIGN2975_3_2206_translate",
                "parent_theorem": False,
                "accepted_for_scoring": False,
            }
        )
        for sign_id, obj, definition, relation, status, source in rows
    ]


def metric_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MR2975_0_Gamma_density",
            "Gamma_eff scalar density",
            "explicit local scalar density Gamma_eff(g,Phi,nabla Phi,D,...) with field content, units and metric dependence",
            "MISSING_GAMMA_EFF_COMPONENT_FORMULA",
            SRC_2207_KMR,
        ),
        (
            "MR2975_1_variation",
            "K_metric formula",
            "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} with derivative/boundary conventions",
            "FORMAL_DEFINITION_ONLY",
            SRC_2799_ACTION,
        ),
        (
            "MR2975_2_components",
            "K_metric component split",
            "K_metric=K_vol+K_deltaM+K_deltaZ+K_deriv+K_boundary",
            "COMPONENTS_LISTED_VALUES_MISSING",
            SRC_2218_KCOMP,
        ),
        (
            "MR2975_3_Khat_match",
            "K_hat equals K_metric",
            "source path showing current K_hat is defined as the same metric response under the same sign/volume/boundary convention",
            "MISSING_COMPONENT_BY_COMPONENT_CERTIFICATE",
            SRC_2207_KMR,
        ),
        (
            "MR2975_4_tracefree_route",
            "trace-free Khat birth",
            "trace-free improvement channel exists as a candidate but live Khat adoption, boundary/projector and amplitude response remain unsigned",
            "CANDIDATE_NOT_LIVE_CERTIFICATE",
            SRC_2220_KHAT_BIRTH,
        ),
        (
            "MR2975_5_Helmholtz",
            "Helmholtz symmetry",
            "second variation of sqrt(-g)T_metric is symmetric up to allowed boundary terms",
            "MISSING_HELMHOLTZ_CERTIFICATE",
            SRC_2799_ACTION,
        ),
        (
            "MR2975_6_verdict",
            "K_hat=K_metric[Gamma_eff]",
            "all metric-response rows close with source/equation paths",
            "NOT_DERIVED_DELTAK_RETAINED",
            SRC_2808_METRIC,
        ),
    ]
    return [
        add_common(
            {
                "metric_audit_id": metric_id,
                "object": obj,
                "required_statement": statement,
                "status": status,
                "source_path": str(source),
                "parent_signed": False,
                "component_value_present": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for metric_id, obj, statement, status, source in rows
    ]


def deltak_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DK2975_0_definition",
            "Delta_K^{mu nu}",
            "K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "stress",
            "DEFINITION_LOCKED_NONCLAIM",
            "source-backed K_hat/K_metric components",
            SRC_2810_UNITS,
        ),
        (
            "DK2975_1_Kvol",
            "DeltaK_vol",
            "K_hat_vol-K_vol where K_vol is the Gamma_eff g^{mu nu} volume/sign term",
            "stress",
            "MISSING_KVOL_VALUE",
            "Gamma_eff density and volume convention",
            SRC_2218_KCOMP,
        ),
        (
            "DK2975_2_KdeltaM",
            "DeltaK_deltaM",
            "K_hat_deltaM-K_deltaM from metric variation of M_AB",
            "stress",
            "MISSING_DELTA_MAB_VALUE",
            "M_AB metric dependence",
            SRC_2218_KCOMP,
        ),
        (
            "DK2975_3_KdeltaZ",
            "DeltaK_deltaZ",
            "K_hat_deltaZ-K_deltaZ from metric variation of Z basis",
            "stress",
            "MISSING_DELTA_Z_VALUE",
            "Z^A metric/coframe dependence",
            SRC_2218_KCOMP,
        ),
        (
            "DK2975_4_Kderiv",
            "DeltaK_deriv",
            "K_hat_deriv-K_deriv from derivative/principal-symbol/domain/CDB dependence",
            "stress",
            "MISSING_DERIVATIVE_TERMS",
            "derivative order and integration-by-parts convention",
            SRC_2218_KCOMP,
        ),
        (
            "DK2975_5_Kboundary",
            "DeltaK_boundary",
            "K_hat_boundary-K_boundary from boundary primitive, corners, P_loc, source worldtubes and support variation",
            "stress",
            "MISSING_BOUNDARY_TERMS",
            "proper boundary/no-flux theorem or retained value",
            SRC_2218_KCOMP,
        ),
        (
            "DK2975_6_DDelta",
            "D_Delta",
            "C_t||partial_t Delta_K^{0nu}||+C_r||partial_r Delta_K^{rnu}||+C_ang||partial_ang Delta_K||+C_conn||Gamma_conn||||Delta_K||",
            "force-density norm",
            "MISSING_COMPONENT_DERIVATIVE_VALUES",
            "Delta_K component profiles and derivative constants",
            SRC_2811_BOUND,
        ),
        (
            "DK2975_7_projector_constants",
            "C_Ploc,C_comm",
            "||q_DeltaK|| <= C_Ploc D_Delta + (C_comm_parallel+C_comm_domain+C_comm_boundary)||Delta_K||",
            "operator/bound constants",
            "MISSING_PROJECTOR_CONSTANTS",
            "orthogonal projector theorem or source-backed constants",
            SRC_2812_ROLL,
        ),
        (
            "DK2975_8_score_gate",
            "eps_DeltaK",
            "eps_DeltaK <= q_*^{-1}(C_Ploc D_Delta + C_comm||Delta_K||)",
            "dimensionless after q_*",
            "NOT_SCORE_READY",
            "q_*, Delta_K components, C_Ploc/C_comm and arena projections",
            SRC_2974_BOUND,
        ),
    ]
    return [
        add_common(
            {
                "deltak_id": deltak_id,
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
        for deltak_id, symbol, definition, units, status, required, source in rows
    ]


def rollforward_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RF2975_0_master_q_loc",
            "eps_q_loc_component",
            "||Z_q|| <= q_*^{-1}(eps_Ward + eps_DeltaK + eps_Ploc_comm + eps_boundary)",
            "2974 master bound preserved under canonical sign",
        ),
        (
            "RF2975_1_DeltaK_insert",
            "eps_DeltaK",
            "eps_DeltaK <= q_*^{-1}(C_Ploc D_Delta + C_comm||Delta_K||)",
            "first Delta_K insertion after sign lock",
        ),
        (
            "RF2975_2_zero_branch",
            "Delta_K zero route",
            "if K_hat=K_metric and P_loc is covariantly fixed then eps_DeltaK=0",
            "conditional branch not claimed",
        ),
        (
            "RF2975_3_no_cancellation",
            "absolute envelope",
            "Ward, Delta_K, P_loc commutator and boundary rows are summed in absolute value unless a parent identity proves cancellation",
            "guard remains active",
        ),
    ]
    return [
        add_common(
            {
                "rollforward_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "meaning": meaning,
                "source_path": str(SRC_2974_BOUND if row_id == "RF2975_0_master_q_loc" else SRC_2812_ROLL),
                "finite_value_present": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, quantity, formula, meaning in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2975_0_sign", "single q_loc-positive sign convention selected", True, "BOOKKEEPING_CONVENTION_LOCKED_NOT_THEOREM"),
        ("CG2975_1_Gamma_density", "Gamma_eff scalar density source-backed", False, "MISSING_GAMMA_EFF_FORMULA"),
        ("CG2975_2_Kmetric", "K_metric components computed", False, "KMETRIC_COMPONENTS_MISSING_VALUES"),
        ("CG2975_3_Khat_match", "K_hat=K_metric", False, "METRIC_RESPONSE_CERTIFICATE_MISSING"),
        ("CG2975_4_DeltaK_zero", "Delta_K=0", False, "DELTAK_RETAINED"),
        ("CG2975_5_q_loc_zero", "q_loc zero theorem", False, "QLOC_ZERO_NOT_PARENT_SIGNED"),
        ("CG2975_6_local_GR", "local GR/Newton reduction", False, "LOCAL_GR_NOT_DERIVED"),
        ("CG2975_7_arena_claims", "R10/PPN/clock/orbital/WEP claims", False, "NO_ARENA_CLAIM_ALLOWED"),
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
            "DEC2975_0_sign",
            "Use the 2808-compatible q_loc-positive convention.",
            "T_q=Gamma_eff g-K_hat makes nabla_mu T_q exactly the unprojected q_loc expression.",
            "all future Delta_K rows use Delta_K=K_hat-K_metric",
        ),
        (
            "DEC2975_1_2206",
            "Treat 2206 as the negative-stress convention.",
            "the Ward zero route is sign-equivalent, but mixed signs would corrupt bounds.",
            "do not score with the 2206 sign",
        ),
        (
            "DEC2975_2_metric",
            "K_hat=K_metric is not proved.",
            "the corpus has a formal route and component list, not a source-backed component certificate.",
            "retain Delta_K",
        ),
        (
            "DEC2975_3_next",
            "The next derivation target is Gamma_eff scalar density ownership.",
            "without the full scalar density and metric dependence, K_metric components cannot be computed.",
            "run 2976 on Gamma_eff/K_vol first",
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
                "next_id": "NEXT2975_0_2976",
                "priority": "selected_primary",
                "next_doc": "2976-Y5-R2FR-Gamma-eff-scalar-density-owner-and-Kmetric-volume-component-or-DeltaK-first-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_Gamma_eff_scalar_density_owner_and_Kmetric_volume_component_or_DeltaK_first_bound_under_AX1090_2976.py",
                "objective": "Source or construct the explicit Gamma_eff scalar density, field content, units and metric dependence needed to compute the K_vol component of K_metric; if not, emit the first DeltaK_vol bound/input row.",
                "include": "Gamma_eff;scalar density;field content;units;metric dependence;K_vol;volume convention;DeltaK_vol;q_* interface;no-cancellation envelope",
                "exclude": "plateau axiom;bookkeeping stress claim;full K_metric certificate;full Z-basis scoring;Y5/Y6/PPN closure;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "copy_id": "COPY2975_0_metric",
                "source_output": str(OUTPUTS["metric"]),
                "branch_copy": str(BRANCH_OUTPUTS["metric_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2975_1_deltak",
                "source_output": str(OUTPUTS["deltak"]),
                "branch_copy": str(BRANCH_OUTPUTS["deltak_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2975_2_next",
                "source_output": str(OUTPUTS["next"]),
                "branch_copy": str(BRANCH_OUTPUTS["next_copy"]),
                "status": "copied",
            }
        ),
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources = all_rows["sources"]
    sign = all_rows["sign"]
    metric = all_rows["metric"]
    deltak = all_rows["deltak"]
    claims = all_rows["claims"]
    next_rows = all_rows["next"]

    checks = [
        ("VAL2975_0_sources_exist", all(row["exists"] for row in sources), "all cited local source paths exist", True),
        ("VAL2975_1_anchors_found", all(row["anchors_found"] for row in sources), "all cited source anchors found", True),
        (
            "VAL2975_2_canonical_sign_selected",
            any(row["sign_id"] == "SIGN2975_0_canonical" and row["status"] == "SELECTED_BOOKKEEPING_CONVENTION" for row in sign),
            "canonical q_loc-positive sign convention selected",
            True,
        ),
        (
            "VAL2975_3_2206_translated",
            any(row["sign_id"] == "SIGN2975_3_2206_translate" and row["status"] == "TRANSLATED_NOT_USED_FOR_SCORING" for row in sign),
            "opposite 2206 sign translated and excluded from scoring",
            True,
        ),
        (
            "VAL2975_4_metric_not_derived",
            any(row["metric_audit_id"] == "MR2975_6_verdict" and row["status"] == "NOT_DERIVED_DELTAK_RETAINED" for row in metric),
            "K_hat=K_metric remains unproved",
            True,
        ),
        (
            "VAL2975_5_deltak_rows_nonclaim",
            any(row["deltak_id"] == "DK2975_0_definition" for row in deltak) and all(not row["accepted_for_scoring"] for row in deltak),
            "Delta_K rows exist and remain nonclaim",
            True,
        ),
        (
            "VAL2975_6_claims_blocked_except_convention",
            all((row["claim_gate_id"] == "CG2975_0_sign" and row["condition_passed"]) or (not row["condition_passed"]) for row in claims),
            "all physics claim gates remain blocked except bookkeeping convention",
            True,
        ),
        (
            "VAL2975_7_next_target_written",
            bool(next_rows) and next_rows[0]["next_id"] == "NEXT2975_0_2976",
            "2976 Gamma_eff scalar density next target selected",
            True,
        ),
        ("VAL2975_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        (
            "VAL2975_9_csvs_parse",
            all(csv_parses(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"]) and all(csv_parses(path) for path in BRANCH_OUTPUTS.values()),
            "all generated CSV files parse",
            True,
        ),
        (
            "VAL2975_10_outputs_under_post_checkpoint",
            all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL2975_11_formalization_clean",
            not any(FORMALIZATION.rglob("*2975*")) if FORMALIZATION.exists() else True,
            "no 2975 outputs were written to formalization-workbench",
            True,
        ),
        ("VAL2975_12_doc_written", DOC.exists(), "2975 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2975_OVERALL", "passed": overall, "check": "2975 validation overall", "required": True}))
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
    text = f"""# 2975 — Gamma/Khat Sign Convention and Metric-Response Certificate, or Delta_K Bound Row

Status: `Y5_R2FR_2975_q_loc_positive_sign_locked_Khat_metric_response_not_derived_DeltaK_rows_written_nonclaim`

Claim ceiling: `no_Khat_equals_Kmetric_no_DeltaK_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The canonical branch sign is now fixed: `T_q^{{mu nu}} := Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}`, so `nabla_mu T_q^{{mu nu}}` is exactly the unprojected `q_loc` expression.
- The older `2206` sign is not a contradiction; it is the negative-stress convention and is translated rather than used for scoring.
- `K_hat = K_metric[Gamma_eff]` is still not derived: the corpus has a formal metric-response route and a component list, not a source-backed component certificate.
- `Delta_K^{{mu nu}} := K_hat^{{mu nu}} - K_metric^{{mu nu}}` is now the retained nonclaim residual feeding `eps_q_loc_component`.
- Next target is `Gamma_eff` scalar-density ownership and the first `K_vol`/`DeltaK_vol` component.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## Sign Convention Lock

{md_table(all_rows["sign"], ["sign_id", "object", "definition", "q_loc_relation", "status", "convention_selected", "parent_theorem"])}

## Metric-Response Certificate Audit

{md_table(all_rows["metric"], ["metric_audit_id", "object", "required_statement", "status", "parent_signed", "component_value_present"])}

## Delta_K Component Bound Rows

{md_table(all_rows["deltak"], ["deltak_id", "symbol", "definition_or_bound", "units", "status", "required_input", "upper_bound", "accepted_for_scoring"])}

## q_loc Bound Rollforward

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
        "sign": sign_rows(),
        "metric": metric_rows(),
        "deltak": deltak_rows(),
        "rollforward": rollforward_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["metric"], BRANCH_OUTPUTS["metric_copy"])
    shutil.copyfile(OUTPUTS["deltak"], BRANCH_OUTPUTS["deltak_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2975 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
