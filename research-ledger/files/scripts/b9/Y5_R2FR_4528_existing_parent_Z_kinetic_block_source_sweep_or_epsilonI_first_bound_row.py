from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4528"
CLAIM_ID = "L-370"
MARKER = "PPC4161_EXISTING_PARENT_Z_KINETIC_BLOCK_SOURCE_SWEEP_OR_EPSILONI_FIRST_BOUND_ROW_4528"
PACKET_MARKER = "PPC4161_PACKET_EXISTING_PARENT_Z_KINETIC_BLOCK_SOURCE_SWEEP_OR_EPSILONI_FIRST_BOUND_ROW_4528"
DECISION = "EXISTING_PARENT_SWEEP_FINDS_FORMAL_SGK_AND_CONSTRAINT_ROUTES_BUT_NO_PARENT_SIGNED_AA0_KVERT0_EPSILONI_BOUND_ROW_STAGED"
NEXT_TARGET = "4529-Y5-R2FR-positive-SGK-parent-signature-map-or-epsilonI-Kvert-value-source.md"

FORMAL_PATH = FORMAL / "544-PPC4161-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md"
DOC_PATH = POST / "4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4528_SOURCE_REGISTER.csv"
SWEEP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_EXISTING_PARENT_SOURCE_SWEEP.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_EPSILONI_FIRST_BOUND_ROW.csv"
KVERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_KVERT_CLASSIFIER_INPUT_ROWS.csv"
BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_BRANCH_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4528_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4528_VALIDATION.csv"

DOC_4527 = POST / "4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md"
FORMAL_4527 = FORMAL / "543-PPC4161-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md"
VALIDATION_4527 = SOURCE_DIR / "P8_Y5_BRR545_4527_VALIDATION.csv"
ACTION_4527 = SOURCE_DIR / "P8_Y5_R2FR_4527_ACTION_ODD_FORCE_THEOREM.csv"
PRINCIPAL_4527 = SOURCE_DIR / "P8_Y5_R2FR_4527_AUXILIARY_Z_PRINCIPAL_SYMBOL_TEST.csv"
COEFF_4527 = SOURCE_DIR / "P8_Y5_R2FR_4527_COEFFICIENT_UPDATE_ROWS.csv"

CLASSIFIER_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_FINITE_RANGE_OR_RANK_ZERO_BRANCH_CLASSIFIER.csv"
DOC_1009 = POST / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
DOC_1192 = POST / "1192-Y5-R10-parent-phi-source-or-active-Gamma-bound-first-score-row.md"
DOC_1563 = POST / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md"
GRAMMAR_1563 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv"
FALLBACK_1563 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv"
DOC_1565 = POST / "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md"
DOC_1619 = POST / "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md"
NORMAL_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv"
GAPS_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv"
SILENCE_1619 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1619_LOCAL_SILENCE_THEOREM.csv"
DOC_1621 = POST / "1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md"
GATE_1621 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv"
FINITE_1621 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4528_00_formal4527", "4527 formal handoff", FORMAL_4527, "PPC4161_SCALAR_ACTION_ASYMMETRY_COEFFICIENT_OR_AUXILIARY_Z_PRINCIPAL_SYMBOL_HUNT_4527", "action/principal-symbol law"),
        ("SRC4528_01_post4527", "4527 post handoff", DOC_4527, "4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md", "declared 4528 target"),
        ("SRC4528_02_val4527", "4527 validation", VALIDATION_4527, "VAL4527_OVERALL", "previous validation pass"),
        ("SRC4528_03_action4527", "4527 action theorem", ACTION_4527, "AOF4527_1_first_force", "A_A law"),
        ("SRC4528_04_principal4527", "4527 principal symbol test", PRINCIPAL_4527, "APS4527_1_principal_symbol", "Kvert classifier"),
        ("SRC4528_05_coeff4527", "4527 coefficient rows", COEFF_4527, "COF4527_0_A_odd_force", "coefficient input"),
        ("SRC4528_06_classifier4519", "4519 range/rank classifier", CLASSIFIER_4519, "FRC4519_1_finite_range", "finite range route"),
        ("SRC4528_07_total_action1009", "1009 parent action guard", DOC_1009, "DEC1009_0_contract_not_parent_action", "total action not promoted"),
        ("SRC4528_08_aux_caution1192", "1192 parentless auxiliary caution", DOC_1192, "D1192_1_phi_source_not_parent_signed", "no closure constraint shortcut"),
        ("SRC4528_09_sgk_doc1619", "1619 formal SGK mechanism", DOC_1619, "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED", "formal mechanism not promoted"),
        ("SRC4528_10_sgk_normal1619", "1619 normal form", NORMAL_1619, "NF1619_1_parent_action_density", "normal-form action density"),
        ("SRC4528_11_sgk_gaps1619", "1619 parent signature gaps", GAPS_1619, "GAP1619_1_exchange_symmetry", "exchange symmetry gap"),
        ("SRC4528_12_sgk_silence1619", "1619 local silence theorem", SILENCE_1619, "LS1619_2_zero_theorem", "conditional silence theorem"),
        ("SRC4528_13_constraint_doc1621", "1621 constraint-first route", DOC_1621, "NO_POLE_NOT_DERIVED_CURRENT_MTS", "constraint-first unsigned"),
        ("SRC4528_14_constraint_gate1621", "1621 no-pole gate", GATE_1621, "CFG1621_4_no_kinetic_pole", "no kinetic pole not signed"),
        ("SRC4528_15_finite1621", "1621 finite coefficients", FINITE_1621, "FCR1621_1_Z_kinetic_residue", "finite kinetic residue row"),
        ("SRC4528_16_aux_doc1563", "1563 auxiliary grammar", DOC_1563, "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "no-derivative grammar unsigned"),
        ("SRC4528_17_grammar1563", "1563 no-derivative grammar CSV", GRAMMAR_1563, "GRAM1563_0_no_DRAB", "derivative ban unsigned"),
        ("SRC4528_18_fallback1563", "1563 finite fallback", FALLBACK_1563, "FALL1563_0_ZR", "finite ZR fallback"),
        ("SRC4528_19_doc1565", "1565 finite ZR protection", DOC_1565, "TO1565_3_operator_contradiction", "derivative term creates finite response"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "line": line_of(path, needle),
                "evidence_snippet": snippet(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def sweep_rows() -> list[dict[str, Any]]:
    return [
        {
            "sweep_id": "SWE4528_0_total_parent_guard",
            "question": "Does the corpus have one signed total parent action whose vertical quadratic expansion can be trusted?",
            "source": str(DOC_1009),
            "evidence": "1009 refuses promotion of a total parent action without sector certificates.",
            "result": "NO_TOTAL_PARENT_ACTION_PROMOTED",
            "effect_on_AA_Kvert": "cannot declare A_A=0 or Kvert=0 from a total action slogan",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_1_positive_SGK_mechanism",
            "question": "Is there an existing formal action class that gives double-zero / F1=0?",
            "source": str(DOC_1619),
            "evidence": "positive auxiliary / response-doublet S_GK gives metric response, Helmholtz readiness and F1=0 in a calculable formal class",
            "result": "FORMAL_MECHANISM_FOUND_NOT_PARENT_SIGNED",
            "effect_on_AA_Kvert": "best candidate route for A_A=0, but not current-MTS proof",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_2_SGK_exchange_gap",
            "question": "Does SGK sign the exchange/vertical symmetry and source-current clauses?",
            "source": str(GAPS_1619),
            "evidence": "GAP1619 rows keep parent doublets, exchange symmetry, matter-even readout, boundary and positivity unsigned/formal",
            "result": "PARENT_SIGNATURE_GAPS_REMAIN",
            "effect_on_AA_Kvert": "A_A=0 remains conditional; source-current zero cannot be inherited",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_3_constraint_first_no_pole",
            "question": "Does constraint-first auxiliary elimination prove no kinetic pole?",
            "source": str(GATE_1621),
            "evidence": "CFG1621_4 records no independent Z/R_AB kinetic residue as NOT_PARENT_SIGNED",
            "result": "NO_KINETIC_POLE_NOT_PARENT_SIGNED",
            "effect_on_AA_Kvert": "Kvert=0 not proved; finite Yukawa/source branch remains live",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_4_no_derivative_grammar",
            "question": "Does the auxiliary grammar ban vertical derivative operators?",
            "source": str(GRAMMAR_1563),
            "evidence": "GRAM1563_0_no_DRAB and related grammar rows are REQUIRED_UNSIGNED",
            "result": "DERIVATIVE_BAN_EXACT_CONDITIONAL_UNSIGNED",
            "effect_on_AA_Kvert": "operator grammar supplies proof shape, not a current Kvert=0 theorem",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_5_finite_fallback_rows",
            "question": "If Kvert is nonzero or not signed zero, are finite rows staged?",
            "source": str(FINITE_1621),
            "evidence": "FCR1621 rows stage kinetic residue, mass/range, source current, Dq leakage, source weight and boundary tail",
            "result": "FINITE_RESIDUAL_ROWS_EXIST_BUT_VALUES_MISSING",
            "effect_on_AA_Kvert": "nonzero Kvert has a test route but not a score-ready one",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_6_no_closure_auxiliary",
            "question": "Can we add a new auxiliary constraint to force the result?",
            "source": str(DOC_1192),
            "evidence": "1192 refuses parentless auxiliary constraints without stress/Ward/matter readout",
            "result": "NEW_AUXILIARY_CLOSURE_REJECTED",
            "effect_on_AA_Kvert": "only existing parent variables/actions can promote A_A=0/Kvert=0",
            "valid_for_claim": False,
        },
        {
            "sweep_id": "SWE4528_7_current_verdict",
            "question": "Current 4528 source sweep verdict",
            "source": str(DOC_PATH),
            "evidence": "formal SGK and constraint-first routes are real, but no existing parent source currently signs A_A=0 and Kvert=0 for MTS",
            "result": "NO_PARENT_SIGNED_AA0_KVERT0_FIRST_BOUND_ROWS_STAGED",
            "effect_on_AA_Kvert": "continue by parent-signing SGK or filling epsilon_I/Kvert values",
            "valid_for_claim": False,
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EPS4528_0_action_defect_input",
            "quantity": "epsilon_I",
            "definition": "dimensionless normalized parent action asymmetry under candidate vertical involution I_q",
            "formula": "epsilon_I = ||S_parent[Phi]-S_parent[I_q Phi]||/(V_loc E_ref)",
            "source_needed": "one existing parent action density, local domain volume, reference energy density, and I_q map",
            "current_value": "MISSING_NUMERIC_ACTION_DEFECT",
            "units": "dimensionless",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EPS4528_1_force_conversion",
            "quantity": "A_bound",
            "definition": "bound on vertical action-odd force norm",
            "formula": "||A|| <= (C_I/ell_z) epsilon_I",
            "source_needed": "collar Lipschitz constant C_I and vertical radius ell_z in same norm as A_A",
            "current_value": "MISSING_CI_AND_ELLZ",
            "units": "force-density or action-gradient units",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EPS4528_2_rank_zero_observable",
            "quantity": "deltaO_rank_zero_from_epsilonI",
            "definition": "observable residual if Kvert=0 but action asymmetry survives",
            "formula": "|delta O_a| <= ||K_obs,a|| m_min^-1 (||A||+sum_abs(other_RHS))",
            "source_needed": "m_min, K_obs,a, other RHS norms, and arena-specific observable limit",
            "current_value": "MISSING_MMIN_KOBS_RHS",
            "units": "arena-specific",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EPS4528_3_finite_range_from_Kvert",
            "quantity": "alpha_lambda_from_Kvert",
            "definition": "observable branch if Kvert has positive physical rank",
            "formula": "M_AB v_i = mu_i^2 Z_AB v_i; lambda_i=1/mu_i; alpha_i=K_i Qbar_iS qbar_iT/(G_N M_S m_T M_i^2)",
            "source_needed": "Z_AB, M_AB, eigenvalues, source/test charges, response coefficient and real bound curve",
            "current_value": "MISSING_Z_M_Q_QBAR_BOUND_CURVE",
            "units": "dimensionless alpha at length lambda_i",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EPS4528_4_no_cancellation_guard",
            "quantity": "epsilon_total_abs",
            "definition": "absolute envelope for action/symbol/source/boundary failures",
            "formula": "epsilon_total_abs <= |epsilon_I term| + |Kvert finite branch| + |J_source| + |B_boundary| + |R_readout| + |Poynting_wave|",
            "source_needed": "every component theorem-zero or numeric/source-backed; no signed cancellation",
            "current_value": "SCHEMA_READY_VALUES_MISSING",
            "units": "declared per arena",
            "valid_for_claim": False,
        },
    ]


def kvert_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "KVI4528_0_existing_parent_action",
            "needed_input": "existing S_parent sector that owns the Z/R/local residual variables",
            "candidate_source": "1619 SGK formal normal form; 1621 constraint-first route",
            "current_status": "FORMAL_OR_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_sourced": "continue to Kvert extraction",
            "if_not": "epsilon_I/Kvert fallback remains",
            "valid_for_claim": False,
        },
        {
            "row_id": "KVI4528_1_Kvert_zero",
            "needed_input": "K_AB^{mu nu}=0 on physical vertical quotient",
            "candidate_source": "1563 no-derivative grammar; 1621 no-pole route",
            "current_status": "REQUIRED_UNSIGNED",
            "if_sourced": "rank-zero branch becomes parent-supported",
            "if_not": "finite-range/stability branch remains live",
            "valid_for_claim": False,
        },
        {
            "row_id": "KVI4528_2_AA_zero",
            "needed_input": "A_A=delta S_odd/delta z^A|0 = 0",
            "candidate_source": "1619 exchange symmetry / even readout; 4195 leakage parity bridge via 4526",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_sourced": "first vertical force closes",
            "if_not": "rank-zero residual gets action-odd numerator",
            "valid_for_claim": False,
        },
        {
            "row_id": "KVI4528_3_Mlock",
            "needed_input": "M_AB coercive or constraint-owned after gauge/constraint removal",
            "candidate_source": "1619 positive operator formal class; 4525 Morse-Bott requirement",
            "current_status": "FORMAL_CANDIDATE_VALUES_MISSING",
            "if_sourced": "algebraic residual bound becomes scoreable",
            "if_not": "m_min row remains blocked",
            "valid_for_claim": False,
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR4528_0_promote_SGK",
            "branch": "try to parent-sign the 1619 positive SGK normal form",
            "why": "it is the cleanest existing formal mechanism for double-zero/F1=0 and metric response",
            "status": "SELECTED_NEXT_SOURCE_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BR4528_1_constraint_first",
            "branch": "try to parent-sign constraint-first/no-pole/no-derivative grammar",
            "why": "it could prove Kvert=0 without finite Yukawa/source hair",
            "status": "PARALLEL_CONDITIONAL_ROUTE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BR4528_2_epsilon_bound",
            "branch": "fill epsilon_I and Kvert value rows if parent signing fails",
            "why": "turns the residual into a finite scoreable local-test vector",
            "status": "FALLBACK_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BR4528_3_current_verdict",
            "branch": "current evidence",
            "why": "formal routes exist but no source proves A_A=0 and Kvert=0",
            "status": "NO_LOCAL_GR_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4528_0_sweep",
            "gate": "existing parent source sweep completed",
            "status": "PASS",
            "detail": "formal SGK, constraint-first, no-derivative and total-action guard sources checked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4528_1_AA_zero",
            "gate": "A_A=0 parent-signed",
            "status": "BLOCKED_NOT_FOUND",
            "detail": "SGK/evenness route remains formal/conditional",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4528_2_Kvert_zero",
            "gate": "Kvert=0 parent-signed",
            "status": "BLOCKED_NOT_FOUND",
            "detail": "no-kinetic/no-derivative grammar remains required unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4528_3_bound_row",
            "gate": "epsilon_I first bound row staged",
            "status": "PASS_NONCLAIM",
            "detail": "bound form exists; values and units still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4528_4_local_GR",
            "gate": "local GR/Newton/R10/PPN claim",
            "status": "BLOCKED",
            "detail": "requires source-backed parent-Z signature or score-ready residual values",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4528_0",
            "decision": DECISION,
            "meaning": "The existing corpus contains real formal mechanisms, especially 1619 SGK and 1621 constraint-first/no-pole, but no current source signs A_A=0 and Kvert=0 for MTS. The next move is to parent-sign SGK or source epsilon_I/Kvert values.",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "claim_status": "private_conditional_nonclaim_source_sweep_bound_row_staged",
            "created_at_utc": now(),
            "next_target": NEXT_TARGET,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "try to map 1619 positive SGK normal form to existing MTS parent variables; otherwise source epsilon_I and Kvert numeric/interval rows",
            "why": "SGK is the most promising existing non-closure mechanism; if it cannot be parent-signed, the bound rows make the failure empirically scoreable.",
            "valid_for_claim": False,
        }
    ]


def validate(sources: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER,
        SWEEP_CSV,
        BOUND_CSV,
        KVERT_CSV,
        BRANCH_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_issues: list[str] = []
    for path in csv_paths:
        try:
            rows = read_csv(path)
            if not rows:
                parse_issues.append(f"{path.name}:empty")
        except Exception as error:
            parse_issues.append(f"{path.name}:{error}")
    sweep_results = {row.get("result") for row in read_csv(SWEEP_CSV)}
    bound_ids = {row.get("bound_id") for row in read_csv(BOUND_CSV)}
    kvert_ids = {row.get("row_id") for row in read_csv(KVERT_CSV)}
    rows = [
        {
            "validation_id": "VAL4528_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all source paths exist and source needles are found",
        },
        {
            "validation_id": "VAL4528_01_sweep",
            "status": "PASS" if {"FORMAL_MECHANISM_FOUND_NOT_PARENT_SIGNED", "NO_KINETIC_POLE_NOT_PARENT_SIGNED", "NO_PARENT_SIGNED_AA0_KVERT0_FIRST_BOUND_ROWS_STAGED"}.issubset(sweep_results) else "FAIL",
            "detail": "sweep records formal SGK, unsigned no-pole, and current verdict",
        },
        {
            "validation_id": "VAL4528_02_bound_rows",
            "status": "PASS" if {"EPS4528_0_action_defect_input", "EPS4528_1_force_conversion", "EPS4528_4_no_cancellation_guard"}.issubset(bound_ids) else "FAIL",
            "detail": "epsilon_I first bound rows present",
        },
        {
            "validation_id": "VAL4528_03_kvert_rows",
            "status": "PASS" if {"KVI4528_1_Kvert_zero", "KVI4528_2_AA_zero"}.issubset(kvert_ids) else "FAIL",
            "detail": "Kvert and A_A classifier rows present",
        },
        {
            "validation_id": "VAL4528_04_claims_blocked",
            "status": "PASS" if all(str(row.get("valid_for_claim", "")).lower() == "false" for row in gates) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "validation_id": "VAL4528_05_csv_parse",
            "status": "PASS" if not parse_issues else "FAIL",
            "detail": ";".join(parse_issues) if parse_issues else "all generated CSV files parse and have rows",
        },
        {
            "validation_id": "VAL4528_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append({"validation_id": "VAL4528_OVERALL", "status": overall, "detail": "4528 parent Z source sweep and epsilonI first bound row"})
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    sweep: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    kvert: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4528 — Existing Parent Z Kinetic Block Source Sweep Or EpsilonI First Bound Row

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}`  
Status: private conditional non-claim; source sweep complete, first bound row staged.

## What Moved

4528 performs the sweep 4527 asked for. It finds real machinery, but not a pass:

- `1619` gives a strong formal positive-auxiliary / response-doublet `S_GK` normal form with double-zero behaviour.
- `1621` and `1563` give the clean no-pole / no-derivative / second-class auxiliary route.
- `1009` and `1192` keep the firewall up: no total parent action is promoted, and no new parentless auxiliary constraint is allowed.

So the current answer is precise:

```text
A_A = 0       not parent-signed yet
Kvert = 0     not parent-signed yet
SGK route     best existing derivation candidate
epsilon_I     first nonclaim bound row staged
```

## Existing Parent Source Sweep

{table(sweep)}

## EpsilonI First Bound Rows

{table(bounds)}

## Kvert Classifier Inputs

{table(kvert)}

## Branch Decision

{table(branches)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Sources

{table(sources)}

## Validation

{table(validation)}

## Next

`{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_parent_Z_sweep",
        "claim": "4528 source-sweeps the existing parent-Z kinetic/action routes, identifies SGK and constraint-first mechanisms as real but unsigned, and stages the first epsilon_I bound row.",
        "current_evidence": "Generated parent source sweep, epsilonI bound rows, Kvert classifier rows, branch decision, claim gates and validation P8_Y5_BRR545_4528_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_source_sweep_bound_row_staged",
        "next_test": NEXT_TARGET,
        "key_risk": "SGK and constraint-first routes are formal/conditional, not parent-signed MTS facts; epsilon_I/Kvert values are missing.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Promoting a formal normal-form candidate or no-derivative grammar into local-GR recovery without parent signatures or numeric residual bounds.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    sweep = sweep_rows()
    bounds = bound_rows()
    kvert = kvert_rows()
    branches = branch_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SWEEP_CSV, sweep)
    write_csv(BOUND_CSV, bounds)
    write_csv(KVERT_CSV, kvert)
    write_csv(BRANCH_CSV, branches)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, sweep, bounds, kvert, branches, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4528 Existing Parent Z Kinetic Block Source Sweep Or EpsilonI First Bound Row

Marker: `{MARKER}`  
The source sweep finds real formal machinery but not a local-GR pass: `1619` SGK is the strongest existing positive auxiliary/response-doublet normal form, and `1621/1563` give a clean conditional no-pole/no-derivative route. Neither currently parent-signs `A_A=0` and `Kvert=0`, so 4528 stages the first `epsilon_I`/`Kvert` bound rows and selects SGK parent-signature mapping as the next derivation target.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4528 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has a concrete source-sweep result: no existing parent source proves `A_A=0`/`Kvert=0`, but the SGK formal normal form is the best candidate to try to promote. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
