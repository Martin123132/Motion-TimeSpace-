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

CHECKPOINT = "2937"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2937-Y5-R2FR-ellJ-source-current-owner-theorem-or-Qbar-tau-R10-projection-contract-under-AX1090.md"

SRC_2936_DOC = ROOT / "2936-Y5-R2FR-R10-curve-promotion-QA-or-ellJ-source-current-projection-theorem-under-AX1090.md"
SRC_2936_ELLJ = RESIDUALS / "P8_Y5_R2FR_2936_ELLJ_SOURCE_CURRENT_PROJECTION_THEOREM_ATTEMPT.csv"
SRC_2936_MTS_ALPHA = RESIDUALS / "P8_Y5_R2FR_2936_MTS_ALPHA_PROJECTION_REQUIREMENTS.csv"
SRC_2936_NEXT = RESIDUALS / "P8_Y5_R2FR_2936_NEXT_TARGET.csv"
SRC_2936_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2936_VALIDATION.csv"

SRC_2934_DOC = ROOT / "2934-Y5-R2FR-dotG-to-kappa-projection-theorem-or-ellJ-owner-source-current-normalization-under-AX1090.md"
SRC_2934_ELLJ = RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv"
SRC_2934_LOG = RESIDUALS / "P8_Y5_R2FR_2934_LOG_DERIVATIVE_RESIDUAL_VECTOR.csv"
SRC_2934_THEOREM = RESIDUALS / "P8_Y5_R2FR_2934_DOTG_TO_KAPPA_PROJECTION_THEOREM_ATTEMPT.csv"

SRC_2924_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2932_CONSTANT = RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv"
SRC_2933_PROJECTION = RESIDUALS / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv"

SRC_2909_PROOF = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv"
SRC_2909_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR.csv"
SRC_2642_PROOF = RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv"
SRC_2642_ARENA = RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_ARENA_PROJECTION_SKELETON.csv"
SRC_2642_BOUNDS = RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv"
SRC_2664_ZERO = RESIDUALS / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_ZERO_PROOF_AUDIT.csv"
SRC_2664_GATE = RESIDUALS / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_INPUT_GATE.csv"
SRC_2664_FIRST = RESIDUALS / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"
SRC_2665_LOCK = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
SRC_2665_GATE = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2937_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2937_ELLJ_OWNER_THEOREM_ATTEMPT.csv",
    "ledger": RESIDUALS / "P8_Y5_R2FR_2937_SOURCE_CURRENT_CLAUSE_LEDGER.csv",
    "r10_contract": RESIDUALS / "P8_Y5_R2FR_2937_QBAR_TAU_R10_PROJECTION_CONTRACT.csv",
    "transfer": RESIDUALS / "P8_Y5_R2FR_2937_DOTG_R10_NEWTON_TRANSFER_MAP.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_2937_NUMERIC_ACQUISITION_QUEUE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2937_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2937_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2937_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2937_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2937_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "EllJ_source_current_owner_theorem_attempt_2937_NONCLAIM.csv",
    "r10_contract_copy": LOCAL_BOUNDS / "Qbar_tau_R10_projection_contract_2937_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR2937_QBAR_TAU_CG_NUMERIC_ACQUISITION_NEXT_NONCLAIM.csv",
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
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2937_00_2936_doc", SRC_2936_DOC, "NEXT2936_0_2937;ell_J/source-current owner theorem;Validation overall: `True`", "2936 selected ellJ/source-current theorem"),
        ("SRC2937_01_2936_ellj", SRC_2936_ELLJ, "EJP2936_4_projection_zero;NOT_DERIVED", "latest ellJ projection block"),
        ("SRC2937_02_2936_mts_alpha", SRC_2936_MTS_ALPHA, "APR2936_6_alpha_predicted;NOT_SCORE_READY", "MTS R10 alpha projection requirements"),
        ("SRC2937_03_2936_next", SRC_2936_NEXT, "NEXT2936_0_2937", "machine-readable 2937 handoff"),
        ("SRC2937_04_2936_validation", SRC_2936_VALIDATION, "VAL2936_OVERALL;True", "2936 validation"),
        ("SRC2937_05_2934_doc", SRC_2934_DOC, "D_t ln G_eff - D_t ln kappa_MTS", "dotG-to-kappa residual identity"),
        ("SRC2937_06_2934_ellj", SRC_2934_ELLJ, "EJO2934_5_verdict;OWNER_THEOREM_NOT_DERIVED", "ellJ owner audit"),
        ("SRC2937_07_2934_log", SRC_2934_LOG, "LDR2934_5_identity;LDR2934_6_bound_formula", "log-derivative residual vector"),
        ("SRC2937_08_2934_theorem", SRC_2934_THEOREM, "DTP2934_3_source_current_descent;DTP2934_4_ellJ_owner", "conditional dotG projection theorem"),
        ("SRC2937_09_2924_contract", SRC_2924_CONTRACT, "RED2924_3_universal_matter_descent;RED2924_8_worldtube_source_measure", "MTS-to-EH/source measure contract"),
        ("SRC2937_10_2932_constant", SRC_2932_CONSTANT, "KLC2932_3_ellJ_owner;KLC2932_5_coupling_total", "kappa/ellJ constant proof audit"),
        ("SRC2937_11_2933_projection", SRC_2933_PROJECTION, "PG2933_2_log_derivative;PG2933_5_verdict", "dotG projection gate"),
        ("SRC2937_12_2909_proof", SRC_2909_PROOF, "PROOF2909_1_JM_Hilbert_owner;PROOF2909_2_external_vacuum", "source-current descent proof attempt"),
        ("SRC2937_13_2909_residual", SRC_2909_RESIDUAL, "RES2909_0_JM_descent;RES2909_3_source_weight", "source-current residual vector"),
        ("SRC2937_14_2642_proof", SRC_2642_PROOF, "SCI2642_0_master_identity;SCI2642_1_JH_descent", "master source-current identity"),
        ("SRC2937_15_2642_arena", SRC_2642_ARENA, "ARENA2642_0_Newton_orbital;ARENA2642_2_R10", "arena projection skeleton"),
        ("SRC2937_16_2642_bounds", SRC_2642_BOUNDS, "SCB2642_0_master;SCB2642_1_eps_JH_Z_abs", "component bound pack"),
        ("SRC2937_17_2664_zero", SRC_2664_ZERO, "SCZ2664_2_absent_quotient_zero;SCZ2664_5_source_shadow_blocker", "Qbar_XH zero proof audit"),
        ("SRC2937_18_2664_gate", SRC_2664_GATE, "QG2664_0_parent_rhoX;QG2664_5_units", "Qbar_XH input gate"),
        ("SRC2937_19_2664_first", SRC_2664_FIRST, "Qbar_XH", "first Qbar source row nonclaim"),
        ("SRC2937_20_2665_lock", SRC_2665_LOCK, "HLOCK2665_0_target;HLOCK2665_5_commutator_stress", "Hamiltonian PiM Qbar lock"),
        ("SRC2937_21_2665_gate", SRC_2665_GATE, "PDG2665_0_same_frame;PDG2665_5_projector", "projector denominator gate"),
        ("SRC2937_22_1009_doc", SRC_1009_DOC, "PCS1009_2_universal_matter;PCS1009_6_mass_projector_PiM", "parent current-chain action contract"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    base_sources = ";".join(str(path) for path in [SRC_2936_ELLJ, SRC_2934_ELLJ, SRC_2934_LOG, SRC_2909_PROOF, SRC_2665_LOCK])
    rows = [
        {
            "theorem_id": "EJO2937_0_master_conditional_theorem",
            "claim": "ell_J is a fixed parent source-current normalization, not a post-readout fit knob",
            "exact_statement": (
                "If S_matter descends through one observed metric/coframe, J_H is the same Hilbert/worldtube current in H_tau and stress, "
                "Pi_M commutes with the relevant source flux, H_ref is fixed, and ell_J is selected before observational readout, then "
                "D_t ln ell_J = D_A ln ell_J = 0 on the local weak-field branch."
            ),
            "derivation_status": "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "current_mts_status": "NOT_PARENT_SIGNED",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "the premises are individually named but not jointly signed by a parent action",
            "source_paths": base_sources,
        },
        {
            "theorem_id": "EJO2937_1_matter_descent",
            "claim": "ordinary matter uses one public observed metric/coframe and one source current",
            "exact_statement": "S_matter = Sbar[q(Phi), psi, theta] with no source-only weight, no hidden representative marker, and no direct X/Z matter vertex.",
            "derivation_status": "CONDITIONAL_DESCENT_LEMMA_AVAILABLE",
            "current_mts_status": "UNSIGNED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "common matter syntax, theta/no-marker rule, and Dq verticality are not parent-signed together",
            "source_paths": f"{SRC_2642_PROOF};{SRC_2909_PROOF};{SRC_1009_DOC}",
        },
        {
            "theorem_id": "EJO2937_2_Ward_source_identity",
            "claim": "the same source current is conserved through quotient and projection",
            "exact_statement": "nabla_mu T^{mu nu}=0, d(Pi_M J_H)=0, and delta(Pi_M J_H)=Pi_M delta J_H up to explicitly retained boundary/projector residuals.",
            "derivation_status": "IDENTITY_CONTRACT_READY",
            "current_mts_status": "UNSIGNED_WITH_RETAINED_RESIDUALS",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "Pi_M commutator, projector stress, boundary tails, and non-Hilbert channels remain unfilled",
            "source_paths": f"{SRC_2642_BOUNDS};{SRC_2665_LOCK};{SRC_2665_GATE}",
        },
        {
            "theorem_id": "EJO2937_3_worldtube_measure_glue",
            "claim": "source mass is the parent worldtube measure before orbital fitting",
            "exact_statement": "M_source[W] = H_tau[S_outer] - H_ref = integral_W rho_H dV_H, with W=closure(supp J_H[tau]) on the same observed frame.",
            "derivation_status": "FORMAL_SELECTOR_CONDITIONAL",
            "current_mts_status": "UNSIGNED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "H_tau integrability, H_ref lock, same-frame J_H, tau, compact support, and regularity are open",
            "source_paths": f"{SRC_2924_CONTRACT};{SRC_2665_LOCK};{SRC_2665_GATE}",
        },
        {
            "theorem_id": "EJO2937_4_reference_and_units",
            "claim": "ell_J and C_source cannot be absorbed into measured GM/readout after the fact",
            "exact_statement": "ell_J, H_ref, tau, source domain, and R_frame are fixed before readout; hence D_t ln C_source = D_t ln R_frame = 0 when the same-source theorem holds.",
            "derivation_status": "REQUIRED_REFERENCE_POLICY_EXACT",
            "current_mts_status": "UNSIGNED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "unit/reference owner is named, but measured-GM absorption and frame/reference derivatives are not killed",
            "source_paths": f"{SRC_2934_LOG};{SRC_2933_PROJECTION};{SRC_2932_CONSTANT}",
        },
        {
            "theorem_id": "EJO2937_5_projection_zero_consequence",
            "claim": "dotG, R10, Newton and local-GR source projections share one owner",
            "exact_statement": "Under EJO2937_1..4, p_J D_t ln ell_J=0, Qbar_XH and tau_R10 are parent support integrals, and C_source is transfer-stable.",
            "derivation_status": "CONSEQUENCE_NOT_CURRENTLY_FIRING",
            "current_mts_status": "BLOCKED_NONCLAIM",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "missing owner clauses block dotG-to-kappa transfer and R10 alpha scoring",
            "source_paths": f"{SRC_2936_MTS_ALPHA};{SRC_2936_ELLJ};{SRC_2934_ELLJ}",
        },
        {
            "theorem_id": "EJO2937_6_verdict",
            "claim": "current MTS closes ell_J/source-current owner theorem",
            "exact_statement": "A current claim would require every prerequisite above to be parent-signed or source-bounded.",
            "derivation_status": "THEOREM_ROUTE_SHARPENED_BUT_NOT_CLOSED",
            "current_mts_status": "OWNER_THEOREM_NOT_DERIVED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "retain closure-only branch plus numeric acquisition rows",
            "source_paths": base_sources,
        },
    ]
    return [add_common(row) for row in rows]


def source_current_clause_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCL2937_0_parent_q", "quotient map q", "q(Phi) defines the public observed metric/coframe and matter readout", "MISSING_PARENT_Q_SIGNATURE", SRC_2642_PROOF, "construct q and Dq basis or retain observed leakage"),
        ("SCL2937_1_vertical_generator", "vertical generator v_X/v_Z", "v in ker(Dq) for residual directions used by local/R10 source tests", "MISSING_DQ_VERTICALITY_CERTIFICATE", SRC_2909_PROOF, "map residual basis to actual vertical generator"),
        ("SCL2937_2_matter_action", "S_matter", "S_matter=Sbar[q(Phi),psi,theta] with no source-only preweights", "UNSIGNED", SRC_1009_DOC, "sign common matter descent clause"),
        ("SCL2937_3_source_current", "J_H/rho_H", "Hilbert/worldtube current is the same object in stress tensor, H_tau and R10 source charge", "MISSING_PARENT_SOURCE_CURRENT_DESCENT", SRC_2909_RESIDUAL, "derive J_H owner or fill source-current residual"),
        ("SCL2937_4_projector", "Pi_M^H", "Pi_M^H fixed-variable list commutes with source flux or carries explicit commutator residual", "RETAINED_PROJECTOR_OBSTRUCTION", SRC_2665_LOCK, "derive d(Pi_M J_H)=0 or source bound the commutator"),
        ("SCL2937_5_worldtube", "W_source", "W_source=closure(supp J_H[tau]) on parent-owned Hamiltonian slice", "MISSING_PARENT_WORLDTUBE_SELECTOR", SRC_2665_GATE, "derive source-domain selector and compact support"),
        ("SCL2937_6_reference", "H_ref/M_H_ref", "H_ref fixed and M_H_ref stable before alpha/dotG/orbital readout", "MISSING_REFERENCE_LOCK", SRC_2665_GATE, "derive H_tau integrability/reference silence"),
        ("SCL2937_7_ellJ", "ell_J", "source-current normalization scale fixed before readout", "NAMED_NOT_OWNED", SRC_2934_ELLJ, "prove D_t ln ell_J=0 or carry drift residual"),
        ("SCL2937_8_Qbar", "Qbar_XH", "Qbar_XH(lambda)=Pi_M^H[Q_bulk+Q_edge+Q_shadow]/M_H_ref with all pieces parent-owned", "NOT_SCORE_READY", SRC_2665_LOCK, "fill Qbar inputs or prove zero"),
        ("SCL2937_9_tau", "tau_R10", "R10 material/test/readout projection derived from same source-current convention", "MISSING_ARENA_PROJECTION", SRC_2936_MTS_ALPHA, "derive R10 support/readout kernel"),
    ]
    return [
        add_common(
            {
                "clause_id": clause_id,
                "object": obj,
                "required_signature": required,
                "current_status": status,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "next_action": next_action,
            }
        )
        for clause_id, obj, required, status, source_path, next_action in rows
    ]


def qbar_tau_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "R10C2937_0_Qbar_XH",
            "quantity": "Qbar_XH(lambda;source)",
            "contract_formula": "Qbar_XH = Pi_M^H[Q_X_bulk^H(lambda)+Q_X_edge^H(lambda)+Q_X_shadow^H(lambda)] / M_H_ref",
            "units": "dimensionless after M_H_ref normalization",
            "required_inputs": "rho_X or Q_X pieces; W_source; Pi_M^H; M_H_ref; fixed reference; units map",
            "current_status": "CONTRACT_ONLY_NOT_SCORE_READY",
            "source_path": str(SRC_2665_LOCK),
        },
        {
            "contract_id": "R10C2937_1_tau_R10",
            "quantity": "tau_R10(lambda;test,readout)",
            "contract_formula": "tau_R10 = R_R10[Q_X_test(lambda), geometry, material, readout] / R_R10[ordinary_mass_reference]",
            "units": "dimensionless arena projection",
            "required_inputs": "test material map; plate/sphere geometry; readout kernel; same source-current convention; lambda support kernel",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": str(SRC_2936_MTS_ALPHA),
        },
        {
            "contract_id": "R10C2937_2_alpha_kappa",
            "quantity": "alpha_kappa(lambda)",
            "contract_formula": "alpha_kappa(lambda)=K_X(lambda)*Qbar_XH(lambda;source)*(tau_R10(lambda)*c_g + E_tail_abs(lambda))",
            "units": "dimensionless Yukawa strength comparator",
            "required_inputs": "K_X(lambda); Qbar_XH; tau_R10; c_g or zero theorem; tail/contact envelope; real bound curve",
            "current_status": "NOT_SCORE_READY",
            "source_path": str(SRC_2936_MTS_ALPHA),
        },
        {
            "contract_id": "R10C2937_3_cg",
            "quantity": "c_g",
            "contract_formula": "c_g=0 only if quotient-invariant matter plus no representative Weyl/disformal/source marker is parent-signed; otherwise use finite bound row",
            "units": "dimensionless or operator-normalized by arena map",
            "required_inputs": "geometry zero proof or source-backed finite value; no-shadow frame certificate",
            "current_status": "ZERO_NOT_CLAIMED",
            "source_path": str(SRC_2664_ZERO),
        },
        {
            "contract_id": "R10C2937_4_tail",
            "quantity": "E_tail_abs(lambda)",
            "contract_formula": "absolute sum of retained boundary, shadow, readout and projector tails projected into the R10 kernel",
            "units": "dimensionless alpha-equivalent envelope",
            "required_inputs": "component tails from source-current bound pack; R10 support/readout projection",
            "current_status": "VALUES_MISSING",
            "source_path": str(SRC_2642_BOUNDS),
        },
        {
            "contract_id": "R10C2937_5_claim_gate",
            "quantity": "R10 pass condition",
            "contract_formula": "valid only when abs(alpha_kappa(lambda_i)) <= alpha_bound(lambda_i) for source-backed curve rows and no placeholder inputs remain",
            "units": "claim gate",
            "required_inputs": "valid Qbar/tau/c_g/tail/K_X rows; valid bound curve; interpolation QA; source paths",
            "current_status": "CLAIM_BLOCKED",
            "source_path": str(SRC_2664_GATE),
        },
    ]
    return [add_common(row) for row in rows]


def transfer_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "transfer_id": "TR2937_0_dotG_to_kappa",
            "arena": "dotG/Mercury/MESSENGER",
            "transfer_formula": "D_t ln G_eff - D_t ln kappa_MTS = p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame",
            "needed_zero_or_bound": "D_t ln ell_J=0; D_t ln C_source=0; D_t ln R_frame=0 or component bounds",
            "current_status": "TRANSFER_BLOCKED_NONCLAIM",
            "source_path": str(SRC_2934_LOG),
        },
        {
            "transfer_id": "TR2937_1_R10",
            "arena": "short-range inverse-square/R10",
            "transfer_formula": "alpha_kappa(lambda)=K_X Qbar_XH(tau_R10*c_g+E_tail_abs)",
            "needed_zero_or_bound": "Qbar_XH, tau_R10, c_g/K_X/tail and real curve must be source-backed",
            "current_status": "NOT_SCORE_READY",
            "source_path": str(SRC_2936_MTS_ALPHA),
        },
        {
            "transfer_id": "TR2937_2_Newton_orbital",
            "arena": "Newton/orbital/GM",
            "transfer_formula": "Delta_GM_orb <= Pi_GM[Delta_rankzero_source_abs] with measured-GM absorption guard",
            "needed_zero_or_bound": "worldtube source measure, Pi_GM response kernel, source transfer convention",
            "current_status": "PROJECTION_SCHEMA_READY_VALUES_MISSING",
            "source_path": str(SRC_2642_ARENA),
        },
        {
            "transfer_id": "TR2937_3_PPN",
            "arena": "PPN gamma/beta/preferred frame",
            "transfer_formula": "Delta_PPN_vec <= Pi_PPN[Delta_rankzero_source_abs] + boundary alpha3 row",
            "needed_zero_or_bound": "Pi_PPN, alpha3 boundary coefficients, beta nonlinear source response",
            "current_status": "PROJECTION_SCHEMA_READY_VALUES_MISSING",
            "source_path": str(SRC_2642_ARENA),
        },
        {
            "transfer_id": "TR2937_4_clocks_EM",
            "arena": "clocks/time/EM",
            "transfer_formula": "clock or alpha_EM drift <= Pi_clock/EM[Delta_rankzero_source_abs] + E_DqZ",
            "needed_zero_or_bound": "clock observable map, EM/fine-structure readout map, DqZ projection",
            "current_status": "OBSERVED_DESCENT_VALUES_MISSING",
            "source_path": str(SRC_2642_ARENA),
        },
        {
            "transfer_id": "TR2937_5_local_GR",
            "arena": "local GR reduction",
            "transfer_formula": "q_loc residual vanishes only if matter/source current, projector, boundary and readout residuals vanish or are bounded below PPN thresholds",
            "needed_zero_or_bound": "single parent current owner plus local residual vector bound",
            "current_status": "LOCAL_GR_NOT_CLAIMED",
            "source_path": str(SRC_2909_RESIDUAL),
        },
    ]
    return [add_common(row) for row in rows]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2937_0_Qbar_XH", "Qbar_XH(lambda;source)", "dimensionless", "R10/source", "MISSING_PARENT_SOURCE_CURRENT_AND_PROJECTOR_LOCK", SRC_2664_GATE),
        ("ACQ2937_1_tau_R10", "tau_R10(lambda;test,readout)", "dimensionless", "R10/test", "MISSING_ARENA_PROJECTION", SRC_2936_MTS_ALPHA),
        ("ACQ2937_2_cg", "c_g", "dimensionless/operator-normalized", "local geometry/R10", "ZERO_PROOF_OR_NUMERIC_BOUND_REQUIRED", SRC_2664_ZERO),
        ("ACQ2937_3_KX", "K_X(lambda)", "alpha-equivalent kernel factor", "R10 kernel", "MISSING_PARENT_KERNEL_NORMALIZATION", SRC_2936_MTS_ALPHA),
        ("ACQ2937_4_tail", "E_tail_abs(lambda)", "dimensionless alpha-equivalent", "boundary/readout/projector tails", "COMPONENT_VALUES_MISSING", SRC_2642_BOUNDS),
        ("ACQ2937_5_ellJ_drift", "D_t ln ell_J", "per year or zero theorem", "dotG/kappa", "OWNER_THEOREM_NOT_DERIVED", SRC_2934_ELLJ),
        ("ACQ2937_6_Csource_drift", "D_t ln C_source", "per year or zero theorem", "dotG/Newton", "SOURCE_CURRENT_NORMALIZATION_NOT_FIXED", SRC_2934_LOG),
        ("ACQ2937_7_PiM_commutator", "d(Pi_M J_H) and delta Pi_M stress", "source-normalized residual", "Newton/PPN/R10", "RETAINED_PROJECTOR_OBSTRUCTION", SRC_2665_LOCK),
        ("ACQ2937_8_worldtube_glue", "M_source[W]-H_tau+H_ref", "mass/source-normalized residual", "Newton/orbital/local_GR", "MISSING_WORLDTUBE_SOURCE_MEASURE", SRC_2924_CONTRACT),
    ]
    return [
        add_common(
            {
                "acquisition_id": acquisition_id,
                "quantity": quantity,
                "units": units,
                "arena": arena,
                "status": status,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "numeric_value": "MISSING_PARENT_INPUT",
                "valid_for_claim": False,
                "next_action": "derive zero/owner theorem first; if it fails, acquire source-backed numeric bound",
            }
        )
        for acquisition_id, quantity, units, arena, status, source_path in specs
    ]


def claim_gate_rows(theorem_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]], queue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conditional_shape = any(row["theorem_id"] == "EJO2937_0_master_conditional_theorem" and row["derivation_status"] == "EXACT_CONDITIONAL_THEOREM_WRITTEN" for row in theorem_rows)
    current_owner_closed = all(str(row.get("application_to_current_mts")) == "True" for row in theorem_rows)
    qbar_tau_valid = all(str(row.get("valid_for_claim")).lower() == "true" for row in contract_rows)
    queue_claim_ready = all(str(row.get("valid_for_claim")).lower() == "true" and "MISSING" not in str(row.get("numeric_value")) for row in queue_rows)
    rows = [
        ("CG2937_0_conditional_theorem_shape", "conditional ellJ/source-current owner theorem is written", conditional_shape, "PASS_CONDITIONAL_NONCLAIM" if conditional_shape else "FAIL"),
        ("CG2937_1_current_owner", "current MTS parent-signs matter/Ward/worldtube/reference clauses", current_owner_closed, "BLOCKED_NONCLAIM"),
        ("CG2937_2_Qbar_tau", "Qbar_XH and tau_R10 are source-backed claim rows", qbar_tau_valid, "BLOCKED_NONCLAIM"),
        ("CG2937_3_numeric_inputs", "all queue quantities are numeric or theorem-zero with sources", queue_claim_ready, "BLOCKED_NONCLAIM"),
        ("CG2937_4_dotG_transfer", "dotG/G bound can be transferred to kappa_MTS", False, "BLOCKED_BY_ELLJ_CSOURCE_RFRAME"),
        ("CG2937_5_R10", "R10 alpha pass can be claimed", False, "BLOCKED_BY_QBAR_TAU_CG_TAIL"),
        ("CG2937_6_local_GR", "local GR/PPN branch can be claimed", False, "BLOCKED_BY_SOURCE_CURRENT_PROJECTOR_RESIDUALS"),
        ("CG2937_7_public_claim", "any public R10/local-GR/Newton claim allowed from 2937", False, "NO_PUBLIC_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "blocks_claim": not passed or gate_id != "CG2937_0_conditional_theorem_shape",
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2937_0_theorem_attempt",
            "decision": "keep the conditional owner theorem",
            "reason": "the derivation is mathematically clean as an if-and-only-if style transfer contract",
            "next_action": "do not use it as a current MTS claim until parent clauses are signed",
        },
        {
            "decision_id": "DEC2937_1_current_status",
            "decision": "block current ellJ/source-current owner claim",
            "reason": "matter descent, Ward/source identity, worldtube source measure, PiM commutator, and reference lock remain unsigned",
            "next_action": "retain every residual as explicit closure or source-acquisition row",
        },
        {
            "decision_id": "DEC2937_2_best_route",
            "decision": "attack H_tau/worldtube/source-measure glue next",
            "reason": "this is lower-scrutiny than fitting R10 first because it tries to derive the shared Newton/GR source object before empirical scoring",
            "next_action": "2938 should prove M_source[W]=H_tau-H_ref=int_W rho_H dV_H or produce the exact closure-only axiom",
        },
        {
            "decision_id": "DEC2937_3_secondary_route",
            "decision": "prepare Qbar/tau finite rows only if derivation fails",
            "reason": "numeric local bounds are useful, but they cannot replace the owner theorem if the goal is GR/Newton derivability",
            "next_action": "keep Qbar/tau/c_g acquisition rows nonclaim",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2937_0_2938",
                "priority": "selected_primary",
                "next_doc": "2938-Y5-R2FR-Htau-worldtube-source-measure-ellJ-reference-lock-or-Qbar-tau-first-value-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_Htau_worldtube_source_measure_ellJ_reference_lock_or_Qbar_tau_first_value_under_AX1090_2938.py",
                "objective": "Prove the shared source-measure glue M_source[W]=H_tau[S]-H_ref=int_W rho_H dV_H with fixed ell_J/reference, or demote it to explicit closure and then start Qbar/tau finite acquisition.",
                "include": "H_tau integrability; H_ref lock; W_source support; same observed coframe; Pi_M fixed variables; ell_J fixed-reference policy; measured-GM absorption guard",
                "exclude": "R10/local-GR/Newton claim; fitted-GM absorption; invented source values; GitHub action; formalization-workbench edits",
            }
        )
    ]


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    ledger_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    transfer_rows: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2937 - Y5 R2FR: ellJ source-current owner theorem or Qbar/tau R10 projection contract under AX1090

Status: `Y5_R2FR_2937_conditional_ellJ_owner_theorem_written_current_MTS_blocked_Qbar_tau_R10_contract_staged_2938_source_measure_next`

Claim ceiling: `conditional_theorem_yes_current_ellJ_owner_no_dotG_transfer_no_R10_no_Newton_no_local_GR_no_GitHub_claim`

2937 takes the coupling/source-current door seriously. The useful result is a clean conditional theorem: if the parent action owns one public matter descent, one conserved source current, one worldtube mass measure, one fixed projector/reference list, and one pre-readout `ell_J`, then the dangerous drift terms vanish and the same owner feeds dotG, R10, Newton/orbital and local-GR checks. The current corpus does **not** yet sign those premises, so 2937 is a nonclaim checkpoint.

Core identity retained from 2934:

`D_t ln G_eff - D_t ln kappa_MTS = p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame`.

## Source Register

{md_table(source_rows, ["source_id", "source_type", "source_path", "path_exists", "anchors_found", "role"])}

## ellJ Owner Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim", "derivation_status", "current_mts_status", "condition_passed", "application_to_current_mts", "blocking_gap"])}

## Source-Current Clause Ledger

{md_table(ledger_rows, ["clause_id", "object", "required_signature", "current_status", "next_action"])}

## Qbar/tau R10 Projection Contract

{md_table(contract_rows, ["contract_id", "quantity", "contract_formula", "required_inputs", "current_status"])}

## dotG/R10/Newton Transfer Map

{md_table(transfer_rows, ["transfer_id", "arena", "transfer_formula", "needed_zero_or_bound", "current_status"])}

## Numeric Acquisition Queue

{md_table(queue_rows, ["acquisition_id", "quantity", "units", "arena", "status", "numeric_value", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["claim_gate_id", "claim", "condition_passed", "status", "blocks_claim", "claim_allowed"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{next(row["passed"] for row in validation if row["validation_id"] == "VAL2937_OVERALL")}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    ledger_rows = source_current_clause_ledger_rows()
    contract_rows = qbar_tau_contract_rows()
    transfer_rows = transfer_map_rows()
    queue_rows = acquisition_queue_rows()
    claim_rows = claim_gate_rows(theorem_rows, contract_rows, queue_rows)
    decision = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem_rows)
    write_csv(OUTPUTS["ledger"], ledger_rows)
    write_csv(OUTPUTS["r10_contract"], contract_rows)
    write_csv(OUTPUTS["transfer"], transfer_rows)
    write_csv(OUTPUTS["queue"], queue_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    shutil.copy2(OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"])
    shutil.copy2(OUTPUTS["r10_contract"], BRANCH_OUTPUTS["r10_contract_copy"])
    shutil.copy2(OUTPUTS["queue"], BRANCH_OUTPUTS["queue_copy"])
    branch_rows = [
        add_common(
            {
                "copy_id": copy_id,
                "source_path": str(source_path),
                "copy_path": str(copy_path),
                "source_exists": source_path.exists(),
                "copy_exists": copy_path.exists(),
                "valid_for_claim": False,
            }
        )
        for copy_id, source_path, copy_path in [
            ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"]),
            ("r10_contract_copy", OUTPUTS["r10_contract"], BRANCH_OUTPUTS["r10_contract_copy"]),
            ("queue_copy", OUTPUTS["queue"], BRANCH_OUTPUTS["queue_copy"]),
        ]
    ]
    write_csv(OUTPUTS["branches"], branch_rows)

    generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_exist = all(str(row["path_exists"]).lower() == "true" for row in source_rows)
    anchors_ok = all(str(row["anchors_found"]).lower() == "true" for row in source_rows)
    theorem_shape = any(row["theorem_id"] == "EJO2937_0_master_conditional_theorem" and row["derivation_status"] == "EXACT_CONDITIONAL_THEOREM_WRITTEN" for row in theorem_rows)
    current_blocked = any(row["theorem_id"] == "EJO2937_6_verdict" and row["current_mts_status"] == "OWNER_THEOREM_NOT_DERIVED" for row in theorem_rows)
    contract_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" and str(row["claim_allowed"]).lower() == "false" for row in contract_rows)
    queue_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" and "MISSING" in str(row["numeric_value"]) for row in queue_rows)
    transfer_blocks = all("BLOCKED" in row["current_status"] or "MISSING" in row["current_status"] or "NOT_SCORE_READY" in row["current_status"] or "LOCAL_GR_NOT_CLAIMED" in row["current_status"] for row in transfer_rows)
    claims_blocked = all(str(row["claim_allowed"]).lower() == "false" for row in claim_rows)
    outputs_under_root = all(is_under(path, ROOT) for path in generated_csvs + [DOC])
    formalization_clean = not any(FORMALIZATION.rglob("*2937*")) if FORMALIZATION.exists() else True
    csvs_parse = all(csv_parses(path) for path in generated_csvs)
    branches_exist = all(row["copy_exists"] for row in branch_rows)

    validation = [
        {"validation_id": "VAL2937_0_sources_exist", "passed": sources_exist, "check": "all cited local source paths exist", "required": True},
        {"validation_id": "VAL2937_1_anchors_found", "passed": anchors_ok, "check": "all source anchors found", "required": True},
        {"validation_id": "VAL2937_2_theorem_shape", "passed": theorem_shape, "check": "conditional ellJ owner theorem written", "required": True},
        {"validation_id": "VAL2937_3_current_blocked", "passed": current_blocked, "check": "current MTS owner theorem remains blocked", "required": True},
        {"validation_id": "VAL2937_4_contract_nonclaim", "passed": contract_nonclaim, "check": "Qbar/tau contract rows remain nonclaim", "required": True},
        {"validation_id": "VAL2937_5_queue_nonclaim", "passed": queue_nonclaim, "check": "numeric acquisition queue remains missing/nonclaim", "required": True},
        {"validation_id": "VAL2937_6_transfer_blocks", "passed": transfer_blocks, "check": "dotG/R10/Newton/local-GR transfers remain blocked or value-missing", "required": True},
        {"validation_id": "VAL2937_7_claims_blocked", "passed": claims_blocked, "check": "no empirical or local-GR claim allowed", "required": True},
        {"validation_id": "VAL2937_8_branches_exist", "passed": branches_exist, "check": "branch copy files exist", "required": True},
        {"validation_id": "VAL2937_9_csvs_parse", "passed": csvs_parse, "check": "all generated CSV files parse", "required": True},
        {"validation_id": "VAL2937_10_outputs_under_post_checkpoint", "passed": outputs_under_root, "check": "all generated outputs are under post-checkpoint-work", "required": True},
        {"validation_id": "VAL2937_11_formalization_clean", "passed": formalization_clean, "check": "no 2937 outputs were written to formalization-workbench", "required": True},
    ]
    overall = all(row["passed"] is True for row in validation)
    validation.append({"validation_id": "VAL2937_OVERALL", "passed": overall, "check": "2937 validation overall", "required": True})
    validation = [add_common(row) for row in validation]
    write_csv(OUTPUTS["validation"], validation)
    write_doc(source_rows, theorem_rows, ledger_rows, contract_rows, transfer_rows, queue_rows, claim_rows, decision, next_rows, branch_rows, validation)

    print(f"wrote {DOC}")
    print(f"validation overall: {overall}")


if __name__ == "__main__":
    main()
