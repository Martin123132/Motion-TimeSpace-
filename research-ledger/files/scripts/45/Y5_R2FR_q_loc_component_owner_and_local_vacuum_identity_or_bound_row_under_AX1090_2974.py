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

CHECKPOINT = "2974"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2974-Y5-R2FR-q_loc-component-owner-and-local-vacuum-identity-or-bound-row-under-AX1090.md"

SRC_2973_DOC = ROOT / "2973-Y5-R2FR-Z-basis-physical-lock-map-and-NZ-normalization-or-q_loc-first-component-under-AX1090.md"
SRC_2973_NEXT = RESIDUALS / "P8_Y5_R2FR_2973_NEXT_TARGET.csv"
SRC_2973_QLOC = RESIDUALS / "P8_Y5_R2FR_2973_QLOC_FIRST_COMPONENT_ROW_NONCLAIM.csv"
SRC_2973_LOCK = RESIDUALS / "P8_Y5_R2FR_2973_Z_BASIS_PHYSICAL_LOCK_ATTEMPT.csv"
SRC_2973_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2973_VALIDATION.csv"

SRC_1010_DOC = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
SRC_2190_GATE = BETA_DOCS / "PARENT_GAMMAKHAT_QLOC_DERIVATION_GATE_2190_NONCLAIM.csv"
SRC_2191_CERT = BETA_DOCS / "PARENT_QLOC_THEOREM_ZERO_CERTIFICATE_2191_NONCLAIM.csv"
SRC_2206_WARD = BETA_DOCS / "PARENT_QLOC_WARD_IDENTITY_2206_NONCLAIM.csv"
SRC_2207_KMR = BETA_DOCS / "PARENT_QLOC_KHAT_METRIC_RESPONSE_AUDIT_2207_NONCLAIM.csv"
SRC_2799_ACTION = BETA_DOCS / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv"
SRC_2808_METRIC = BETA_DOCS / "GAMMA_KHAT_METRIC_RESPONSE_2808_NONCLAIM.csv"
SRC_2801_OBS = BETA_DOCS / "QLOC_OBSERVABLE_MAP_2801_NONCLAIM.csv"
SRC_2802_COEFF = BETA_DOCS / "QLOC_FIRST_COEFFICIENT_2802_NONCLAIM.csv"
SRC_2803_BODY = BETA_DOCS / "QLOC_BODY_MOMENT_IDENTITY_2803_NONCLAIM.csv"
SRC_2810_UNITS = BETA_DOCS / "PLOC_QDELTAK_UNIT_UPDATE_2810_NONCLAIM.csv"
SRC_2811_BOUND = BETA_DOCS / "PLOC_QDELTAK_BOUND_INTERFACE_2811_NONCLAIM.csv"
SRC_2812_ROLL = BETA_DOCS / "CPLOC_CCOMM_QDELTAK_BOUND_2812_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2974_SOURCE_REGISTER.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2974_QLOC_OWNER_IDENTITY_AUDIT.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2974_LOCAL_VACUUM_ZERO_THEOREM_STATUS.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_2974_QLOC_BOUND_DECOMPOSITION_NONCLAIM.csv",
    "observable": RESIDUALS / "P8_Y5_R2FR_2974_QLOC_OBSERVABLE_INTERFACE_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2974_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2974_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2974_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2974_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2974_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "identity_copy": PARENT_ACTION / "q_loc_owner_identity_2974_NOT_DERIVED.csv",
    "bound_copy": LOCAL_BOUNDS / "q_loc_bound_decomposition_2974_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2974_GammaKhat_metric_response_owner_next_NONCLAIM.csv",
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
        ("SRC2974_00_2973_doc", SRC_2973_DOC, "NEXT2973_0_2974;conditional zero lemma", "2973 selected the q_loc owner/identity target"),
        ("SRC2974_01_2973_next", SRC_2973_NEXT, "NEXT2973_0_2974", "machine handoff target"),
        ("SRC2974_02_2973_qloc", SRC_2973_QLOC, "QLOC2973_0_definition;QLOC2973_6_bound_row", "q_loc first component row"),
        ("SRC2974_03_2973_lock", SRC_2973_LOCK, "LOCK2973_0_q_loc;LOCK2973_6_full_vector", "full Z lock remains failed"),
        ("SRC2974_04_2973_validation", SRC_2973_VALIDATION, "VAL2973_OVERALL", "2973 validation"),
        ("SRC2974_05_1010_doc", SRC_1010_DOC, "GKT1010_0_variational_route;QRES1010_0_q_loc_vector", "older q_loc action-existence checkpoint"),
        ("SRC2974_06_2190_gate", SRC_2190_GATE, "DG2190_0_identity_target;DG2190_9_verdict", "Gamma/Khat/q_loc derivation gate"),
        ("SRC2974_07_2191_cert", SRC_2191_CERT, "TZ2191_0_action_owner;TZ2191_8_all_or_nothing", "q_loc theorem-zero certificate requirements"),
        ("SRC2974_08_2206_ward", SRC_2206_WARD, "WID2206_0_define_stress;WID2206_4_current_verdict", "Ward identity route"),
        ("SRC2974_09_2207_kmr", SRC_2207_KMR, "KMR2207_0_candidate_density_exists;KMR2207_5_overall", "K_hat metric-response audit"),
        ("SRC2974_10_2799_action", SRC_2799_ACTION, "GKT2799_0_variational_route;GKT2799_6_verdict", "GK action existence theorem attempt"),
        ("SRC2974_11_2808_metric", SRC_2808_METRIC, "MRD2808_0_action;MRD2808_6_verdict", "metric-response identity and Delta_K obstruction"),
        ("SRC2974_12_2801_obs", SRC_2801_OBS, "QMAP2801_0_K_PPN;QMAP2801_7_Gdot", "q_loc observable map"),
        ("SRC2974_13_2802_coeff", SRC_2802_COEFF, "COEFF2802_0_stress_balance_normalizer;COEFF2802_6_verdict", "first q_loc coefficient kernels"),
        ("SRC2974_14_2803_body", SRC_2803_BODY, "BMI2803_0_body_moment;BMI2803_5_verdict", "body moment identity"),
        ("SRC2974_15_2810_units", SRC_2810_UNITS, "QDU2810_0_DeltaK;QDU2810_4_acceleration", "P_loc/Delta_K unit update"),
        ("SRC2974_16_2811_bound", SRC_2811_BOUND, "QB2811_0_CPloc;QB2811_5_score_gate", "P_loc Delta_K bound interface"),
        ("SRC2974_17_2812_roll", SRC_2812_ROLL, "QBR2812_0_operator_zero_branch;QBR2812_3_score_gate", "C_Ploc/C_comm roll-forward bound"),
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


def identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ID2974_0_q_loc_definition",
            "q_loc^nu",
            "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "DEFINITION_AVAILABLE",
            "definition exists but does not by itself prove zero",
            SRC_2973_QLOC,
        ),
        (
            "ID2974_1_sign_convention",
            "T_GK sign",
            "2808 uses T_GK=Gamma_eff g-K_metric; 2206 uses the opposite sign convention in one row.",
            "SIGN_CONVENTION_LOCK_REQUIRED",
            "zero proof survives a global sign, but Delta_K bound rows require one fixed convention",
            SRC_2206_WARD,
        ),
        (
            "ID2974_2_metric_response",
            "K_hat=K_metric[Gamma_eff]",
            "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} plus boundary convention",
            "MISSING_METRIC_RESPONSE_CERTIFICATE",
            "current K_hat symbol is not component-matched to the metric response",
            SRC_2207_KMR,
        ),
        (
            "ID2974_3_Ward_Euler",
            "local vacuum identity",
            "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_GK^nu",
            "CONDITIONAL_IDENTITY_ONLY",
            "needs S_GK, Helmholtz integrability, Euler equations and source-current silence",
            SRC_2799_ACTION,
        ),
        (
            "ID2974_4_projector",
            "P_loc owner",
            "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, and [P_loc,nabla] terms zero or retained",
            "MISSING_PLOC_OWNER_COMMUTATOR",
            "P_loc may add commutator/domain/readout leakage",
            SRC_2811_BOUND,
        ),
        (
            "ID2974_5_boundary",
            "compact-local boundary silence",
            "integral_boundary Delta(theta_GK,Q_GK,tau)=0 or fixed topological subtraction",
            "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE",
            "boundary and symplectic work can feed local force/source rows",
            SRC_2191_CERT,
        ),
        (
            "ID2974_6_qstar",
            "q_* normalization",
            "Z_q=q_loc/q_* with declared units, local norm and measure",
            "MISSING_QSTAR_AND_NORM",
            "no finite dimensionless score until q_* and local norm are sourced",
            SRC_2973_QLOC,
        ),
        (
            "ID2974_7_verdict",
            "q_loc zero theorem",
            "all owner, metric-response, Ward, projector, boundary and q_* clauses close",
            "NOT_DERIVED_BOUND_ROW_REQUIRED",
            "retain q_loc as explicit residual with an absolute no-cancellation envelope",
            SRC_2190_GATE,
        ),
    ]
    return [
        add_common(
            {
                "identity_id": row_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "blocking_gap": gap,
                "source_path": str(source),
                "parent_signed": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, obj, statement, status, gap, source in rows
    ]


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "THM2974_0_conditional_shape",
            "If S_GK is diffeo-invariant, K_hat=K_metric, E_A=0, B_GK=0, P_loc is q-basic/covariantly fixed, and boundary flux vanishes, then q_loc^nu=0.",
            "MATHEMATICALLY_VALID_CONDITIONAL",
            "not parent-signed for current MTS symbols",
        ),
        (
            "THM2974_1_unprojected_identity",
            "With T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}, nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_metric^{mu nu}.",
            "IDENTITY_AVAILABLE_AFTER_SIGN_LOCK",
            "requires one fixed stress sign/volume convention",
        ),
        (
            "THM2974_2_DeltaK_gap",
            "q_loc=P_loc(nabla_mu T_GK^{mu nu}) + P_loc nabla_mu(K_metric^{mu nu}-K_hat^{mu nu}) plus projector/connection terms.",
            "DELTA_K_GAP_RETAINED",
            "K_hat=K_metric is missing",
        ),
        (
            "THM2974_3_on_shell_zero",
            "E_A=0 and compact-local source/boundary silence would kill the Ward term.",
            "CONDITIONAL_NOT_CURRENTLY_CLOSED",
            "source-current zero and boundary no-flux are not signed",
        ),
        (
            "THM2974_4_verdict",
            "q_loc^nu=0 is not adopted in the current branch.",
            "THEOREM_ZERO_NOT_CLAIMED",
            "use bound decomposition until owner certificates are real",
        ),
    ]
    return [
        add_common(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "status": status,
                "gap": gap,
                "conditional_valid": theorem_id != "THM2974_4_verdict",
                "parent_adopted": False,
                "source_path": str(SRC_2808_METRIC if theorem_id in {"THM2974_1_unprojected_identity", "THM2974_2_DeltaK_gap"} else SRC_2799_ACTION),
            }
        )
        for theorem_id, statement, status, gap in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QB2974_0_master",
            "eps_q_loc_component",
            "||Z_q|| <= q_*^{-1}(eps_Ward + eps_DeltaK + eps_Ploc_comm + eps_boundary)",
            "dimensionless",
            "MISSING_QSTAR_AND_COMPONENT_BOUNDS",
            SRC_2973_QLOC,
        ),
        (
            "QB2974_1_Ward",
            "eps_Ward",
            "C_Ploc ||sum_A E_A nabla Phi^A + B_GK||_U",
            "force-density norm",
            "MISSING_EULER_SOURCE_BOUNDARY_ZERO_OR_BOUND",
            SRC_2799_ACTION,
        ),
        (
            "QB2974_2_DeltaK",
            "eps_DeltaK",
            "C_Ploc D_Delta with D_Delta from component derivatives of Delta_K=K_hat-K_metric",
            "force-density norm",
            "MISSING_DELTAK_COMPONENTS_AND_KMETRIC_MATCH",
            SRC_2811_BOUND,
        ),
        (
            "QB2974_3_Ploc_comm",
            "eps_Ploc_comm",
            "(C_comm_parallel+C_comm_domain+C_comm_boundary)||Delta_K|| plus [P_loc,nabla]T_GK terms",
            "force-density norm",
            "MISSING_PLOC_COVARIANT_FIXED_THEOREM_OR_CCOMM_VALUES",
            SRC_2812_ROLL,
        ),
        (
            "QB2974_4_boundary",
            "eps_boundary",
            "compact-collar surface/symplectic flux and body-moment traction terms",
            "force-density or body-force norm",
            "MISSING_BOUNDARY_SILENCE_OR_TRACTION_BOUND",
            SRC_2803_BODY,
        ),
        (
            "QB2974_5_no_cancellation",
            "absolute envelope",
            "no negative credit between Ward, Delta_K, P_loc commutator and boundary rows unless a parent identity proves cancellation",
            "guardrail",
            "NO_CANCELLATION_GUARD_ACTIVE",
            SRC_2812_ROLL,
        ),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "bound_or_definition": expression,
                "units": units,
                "status": status,
                "source_path": str(source),
                "lower_bound": 0,
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "finite_value_present": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for bound_id, symbol, expression, units, status, source in rows
    ]


def observable_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS2974_0_PPN", "K_PPN", "Delta_PPN^a <= K_PPN^a ||q_loc||_D", "MISSING_WEAK_FIELD_METRIC_SOLUTION", SRC_2801_OBS),
        ("OBS2974_1_WEP", "K_WEP", "eta_AB <= K_WEP^{AB} ||q_loc||_D", "MISSING_SOURCE_TEST_BODY_PROJECTION", SRC_2802_COEFF),
        ("OBS2974_2_clock", "K_clock", "|delta nu/nu| <= K_clock ||q_loc||_D", "MISSING_CLOCK_READOUT_MAP", SRC_2801_OBS),
        ("OBS2974_3_orbital", "K_orbital", "|delta a_r| or |d ln mu_obs/dt| <= K_orbital ||q_loc||_D", "MISSING_ORBITAL_SOURCE_MODEL", SRC_2801_OBS),
        ("OBS2974_4_source", "K_source", "|epsilon_mu| <= K_source ||q_loc||_D", "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT", SRC_2801_OBS),
        ("OBS2974_5_body_moment", "I_A^i", "I_A^i=int_Sigma q_loc^i sqrt(gamma)d^3x", "BODY_MOMENT_IDENTITY_CONDITIONAL_NOT_ZERO", SRC_2803_BODY),
    ]
    return [
        add_common(
            {
                "observable_id": observable_id,
                "coefficient_symbol": symbol,
                "map_form": map_form,
                "status": status,
                "source_path": str(source),
                "finite_numeric_value": False,
                "accepted_for_scoring": False,
            }
        )
        for observable_id, symbol, map_form, status, source in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2974_0_action", "S_GK parent action exists", False, "MISSING_PARENT_ACTION_OWNER"),
        ("CG2974_1_metric_response", "K_hat equals K_metric", False, "MISSING_METRIC_RESPONSE_CERTIFICATE"),
        ("CG2974_2_sign", "single Gamma/Khat stress sign convention", False, "SIGN_CONVENTION_LOCK_REQUIRED"),
        ("CG2974_3_Ward", "Ward/Euler local-vacuum zero", False, "WARD_EULER_CLOSURE_CONDITIONAL_ONLY"),
        ("CG2974_4_projector_boundary", "P_loc and boundary silence", False, "PLOC_BOUNDARY_OPEN"),
        ("CG2974_5_qstar", "q_* and norm sourced", False, "QSTAR_NORM_MISSING"),
        ("CG2974_6_local_GR", "local GR/Newton reduction", False, "LOCAL_GR_NOT_DERIVED"),
        ("CG2974_7_arena_claims", "R10/PPN/clock/orbital/WEP claims", False, "NO_ARENA_CLAIM_ALLOWED"),
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
            "DEC2974_0_conditional_success",
            "The q_loc zero route is mathematically coherent as a conditional Ward/metric-response theorem.",
            "2808/2799 show the exact unprojected identity and on-shell route.",
            "keep the derivation route alive",
        ),
        (
            "DEC2974_1_not_adopted",
            "The theorem is not parent-signed for current MTS.",
            "S_GK, K_hat=K_metric, Helmholtz, source-current, P_loc, boundary and q_* clauses remain open.",
            "do not claim q_loc=0 or local GR",
        ),
        (
            "DEC2974_2_bound_row",
            "A first absolute q_loc bound decomposition is now the honest fallback.",
            "it isolates Ward, Delta_K, P_loc commutator and boundary terms without cancellation.",
            "fill Delta_K/sign convention first",
        ),
        (
            "DEC2974_3_next",
            "The next hinge is Gamma/Khat sign and metric-response ownership.",
            "without a fixed convention and K_hat=K_metric certificate, every q_loc bound is symbolic.",
            "run 2975 on sign/Delta_K/metric-response",
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
                "next_id": "NEXT2974_0_2975",
                "priority": "selected_primary",
                "next_doc": "2975-Y5-R2FR-GammaKhat-sign-convention-and-metric-response-certificate-or-DeltaK-bound-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_GammaKhat_sign_convention_and_metric_response_certificate_or_DeltaK_bound_row_under_AX1090_2975.py",
                "objective": "Lock one Gamma/Khat stress sign and volume convention, then try to prove K_hat=K_metric[Gamma_eff]; if not, emit the first Delta_K component/bound rows feeding eps_q_loc_component.",
                "include": "Gamma_eff;K_hat;K_metric;T_GK sign;volume convention;Delta_K;Helmholtz symmetry;C_Ploc;C_comm;D_Delta;no-cancellation envelope",
                "exclude": "plateau axiom;bookkeeping stress claim;full Z-basis scoring;Y5/Y6/PPN closure;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "copy_id": "COPY2974_0_identity",
                "source_output": str(OUTPUTS["identity"]),
                "branch_copy": str(BRANCH_OUTPUTS["identity_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2974_1_bound",
                "source_output": str(OUTPUTS["bound"]),
                "branch_copy": str(BRANCH_OUTPUTS["bound_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2974_2_next",
                "source_output": str(OUTPUTS["next"]),
                "branch_copy": str(BRANCH_OUTPUTS["next_copy"]),
                "status": "copied",
            }
        ),
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources = all_rows["sources"]
    identity = all_rows["identity"]
    theorem = all_rows["theorem"]
    bound = all_rows["bound"]
    claims = all_rows["claims"]
    next_rows = all_rows["next"]

    checks = [
        ("VAL2974_0_sources_exist", all(row["exists"] for row in sources), "all cited local source paths exist", True),
        ("VAL2974_1_anchors_found", all(row["anchors_found"] for row in sources), "all cited source anchors found", True),
        (
            "VAL2974_2_sign_guard",
            any(row["identity_id"] == "ID2974_1_sign_convention" and row["status"] == "SIGN_CONVENTION_LOCK_REQUIRED" for row in identity),
            "Gamma/Khat sign convention guard is explicit",
            True,
        ),
        (
            "VAL2974_3_theorem_not_adopted",
            any(row["theorem_id"] == "THM2974_4_verdict" and row["status"] == "THEOREM_ZERO_NOT_CLAIMED" for row in theorem),
            "q_loc zero theorem remains nonclaim",
            True,
        ),
        (
            "VAL2974_4_bound_decomposition",
            any(row["bound_id"] == "QB2974_0_master" for row in bound) and all(not row["accepted_for_scoring"] for row in bound),
            "q_loc bound decomposition exists and remains nonclaim",
            True,
        ),
        (
            "VAL2974_5_no_cancellation",
            any(row["bound_id"] == "QB2974_5_no_cancellation" and row["status"] == "NO_CANCELLATION_GUARD_ACTIVE" for row in bound),
            "absolute no-cancellation guard present",
            True,
        ),
        ("VAL2974_6_claims_blocked", all(not row["condition_passed"] and not row["claim_allowed"] for row in claims), "all claim gates remain blocked", True),
        (
            "VAL2974_7_next_target_written",
            bool(next_rows) and next_rows[0]["next_id"] == "NEXT2974_0_2975",
            "2975 Gamma/Khat sign and metric-response next target selected",
            True,
        ),
        ("VAL2974_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        (
            "VAL2974_9_csvs_parse",
            all(csv_parses(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"]) and all(csv_parses(path) for path in BRANCH_OUTPUTS.values()),
            "all generated CSV files parse",
            True,
        ),
        (
            "VAL2974_10_outputs_under_post_checkpoint",
            all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL2974_11_formalization_clean",
            not any(FORMALIZATION.rglob("*2974*")) if FORMALIZATION.exists() else True,
            "no 2974 outputs were written to formalization-workbench",
            True,
        ),
        ("VAL2974_12_doc_written", DOC.exists(), "2974 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2974_OVERALL", "passed": overall, "check": "2974 validation overall", "required": True}))
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
    text = f"""# 2974 — q_loc Component Owner and Local-Vacuum Identity, or Bound Row

Status: `Y5_R2FR_2974_q_loc_zero_conditional_not_parent_signed_bound_decomposition_written_nonclaim`

Claim ceiling: `no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The good news: the `q_loc` zero route is mathematically coherent as a Ward/metric-response theorem.
- The bad news: it is still not parent-signed for actual MTS symbols because `S_GK`, `K_hat=K_metric`, Helmholtz, source-current silence, `P_loc`, boundary silence, and `q_*` are all open.
- A sign-convention guard is now explicit: `2808` and `2206` use opposite stress signs, so `2975` must lock a single `T_GK` convention before scoring `Delta_K`.
- The honest fallback is now written as an absolute bound decomposition for `eps_q_loc_component`, with no cancellation allowed between Ward, `Delta_K`, `P_loc` commutator, and boundary terms.
- This still does not derive local GR/Newton; it sharpens the next proof target to `Gamma_eff/K_hat` metric-response ownership.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## q_loc Owner Identity Audit

{md_table(all_rows["identity"], ["identity_id", "object", "statement", "status", "blocking_gap", "theorem_zero"])}

## Local-Vacuum Zero Theorem Status

{md_table(all_rows["theorem"], ["theorem_id", "statement", "status", "gap", "conditional_valid", "parent_adopted"])}

## q_loc Bound Decomposition

{md_table(all_rows["bound"], ["bound_id", "symbol", "bound_or_definition", "units", "status", "upper_bound", "accepted_for_scoring"])}

## Observable Interface

{md_table(all_rows["observable"], ["observable_id", "coefficient_symbol", "map_form", "status", "finite_numeric_value", "accepted_for_scoring"])}

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
        "identity": identity_rows(),
        "theorem": theorem_rows(),
        "bound": bound_rows(),
        "observable": observable_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["identity"], BRANCH_OUTPUTS["identity_copy"])
    shutil.copyfile(OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2974 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
