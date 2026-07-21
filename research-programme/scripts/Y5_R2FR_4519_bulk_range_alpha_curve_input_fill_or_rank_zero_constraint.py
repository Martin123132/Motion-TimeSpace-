from __future__ import annotations

import csv
import io
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4519"
CLAIM_ID = "L-361"
MARKER = "PPC4161_BULK_RANGE_ALPHA_CURVE_INPUT_FILL_OR_RANK_ZERO_CONSTRAINT_4519"
PACKET_MARKER = "PPC4161_PACKET_BULK_RANGE_ALPHA_CURVE_INPUT_FILL_OR_RANK_ZERO_CONSTRAINT_4519"
DECISION = "FINITE_RANGE_VS_RANK_ZERO_BRANCH_CLASSIFIER_DERIVED_INPUT_PACKS_STAGED_NONCLAIM"
NEXT_TARGET = "4520-Y5-R2FR-rank-zero-source-current-silence-or-alpha-input-acquisition.md"

FORMAL_PATH = FORMAL / "535-PPC4161-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md"
DOC_PATH = POST / "4519-Y5-R2FR-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4519_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4519_SOURCE_REGISTER.csv"
BRANCH_CLASSIFIER = SOURCE_DIR / "P8_Y5_R2FR_4519_FINITE_RANGE_OR_RANK_ZERO_BRANCH_CLASSIFIER.csv"
ALPHA_INPUT_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4519_ALPHA_LAMBDA_INPUT_CONTRACT.csv"
RANK_ZERO_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv"
BOUND_CURVE_GATE = SOURCE_DIR / "P8_Y5_R2FR_4519_BOUND_CURVE_ADMISSION_GATE.csv"
BRANCH_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4519_BRANCH_STATUS.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4519_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4519_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4519_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4519_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4519_DECISION.csv"

FORMAL_534 = FORMAL / "534-PPC4161-domain-R11-silence-or-bulk-range-alpha-curve.md"
POST_4518 = POST / "4518-Y5-R2FR-domain-R11-silence-or-bulk-range-alpha-curve.md"
ALPHA_4518 = SOURCE_DIR / "P8_Y5_R2FR_4518_BULK_RANGE_ALPHA_CURVE_SCAFFOLD.csv"
BRANCH_4518 = SOURCE_DIR / "P8_Y5_R2FR_4518_BRANCH_DECISION_MATRIX.csv"
RANGE_2210 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv"
RANGE_2211 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2211_HESSIAN_VS_RANGE_LEMMA.csv"
RANGE_DEMOTER = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2211_RANGE_BRANCH_DEMOTER.csv"
RZ_CONTRACT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2212_RANK_ZERO_CONSTRAINT_CONTRACT.csv"
RZ_THEOREM = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2213_RANK_ZERO_SOURCE_CURRENT_THEOREM_ATTEMPT.csv"
CONSTRAINT_2264 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2264_CONDITIONAL_CONSTRAINT_THEOREM.csv"
CONSTRAINT_GATES = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv"
LOCAL_RANK_CERT = SOURCE_DIR / "P8_Y5_R10_901_LOCAL_RANK_ZERO_CERTIFICATE.csv"
BOUND_STATUS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2209_BOUND_CURVE_STATUS.csv"
BOUND_PROMOTION = SOURCE_DIR / "P8_Y5_R10_1342_BOUND_CURVE_PROMOTION_GATE.csv"
EOTWASH_POINTS = SOURCE_DIR / "P8_Y5_R10_1499_EOTWASH2020_ALPHA_LAMBDA_POINTS_NONCLAIM.csv"
REVIEWED_CANDIDATE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv"
MTS_ALPHA_TEMPLATE = SOURCE_DIR / "R10_alpha_lambda_curve_MTS_source_normalization.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4519_00_formal534", "4518 formal handoff", FORMAL_534, "PPC4161_DOMAIN_R11_SILENCE_OR_BULK_RANGE_ALPHA_CURVE_4518", "4518 handoff"),
        ("SRC4519_01_post4518", "4518 post handoff", POST_4518, "NT4518_0", "declares 4519 target"),
        ("SRC4519_02_alpha4518", "4518 alpha scaffold", ALPHA_4518, "BAR4518_3_alpha_definition", "alpha formula"),
        ("SRC4519_03_branch4518", "4518 branch decision", BRANCH_4518, "BD4518_2_rank_zero", "rank-zero branch"),
        ("SRC4519_04_range2210", "range operator derivation", RANGE_2210, "ROD2210_1_generalized_range_spectrum", "finite range operator law"),
        ("SRC4519_05_range2211", "Hessian/range lemma", RANGE_2211, "HVR2211_2_rank_zero_constraint_case", "rank-zero case"),
        ("SRC4519_06_demoter2211", "range branch demoter", RANGE_DEMOTER, "RBD2211_1_response_doublet_constraint", "constraint promoted fork"),
        ("SRC4519_07_rzcontract", "rank-zero contract", RZ_CONTRACT, "RZC2212_5_verdict", "rank-zero route verdict"),
        ("SRC4519_08_rztheorem", "rank-zero theorem attempt", RZ_THEOREM, "RZS2213_2_rank_zero_silence_theorem", "rank-zero silence theorem"),
        ("SRC4519_09_constraint2264", "conditional constraint theorem", CONSTRAINT_2264, "THM2264_0_constraint_statement", "constraint theorem"),
        ("SRC4519_10_constraintgates", "constraint algebra gates", CONSTRAINT_GATES, "CAG2263_6_verdict", "constraint gate verdict"),
        ("SRC4519_11_localrankcert", "local rank-zero certificate", LOCAL_RANK_CERT, "LRZ901_3_verdict", "local rank certificate verdict"),
        ("SRC4519_12_boundstatus", "bound curve status", BOUND_STATUS, "BCS2209_3_curve_verdict", "bound curve missing verdict"),
        ("SRC4519_13_boundpromotion", "bound promotion gate", BOUND_PROMOTION, "GATE1342_1_full_curve", "full curve gate"),
        ("SRC4519_14_eotwashpoints", "EotWash nonclaim points", EOTWASH_POINTS, "R10EW2020_3_text_threshold_anchor", "anchor/visual nonclaim points"),
        ("SRC4519_15_reviewedcandidate", "reviewed candidate curve", REVIEWED_CANDIDATE, "REVIEWED_QA_CANDIDATE_NONCLAIM", "candidate curve nonclaim"),
        ("SRC4519_16_mtsalpha", "MTS alpha template", MTS_ALPHA_TEMPLATE, "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION", "MTS alpha template missing prediction"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def branch_classifier_rows() -> List[Dict[str, object]]:
    return [
        {
            "classifier_id": "FRC4519_0_operator_split",
            "branch": "pre-branch local operator",
            "mathematical_test": "L_AB=-Z_AB Delta + M_AB + lower terms on the physical quotient",
            "if_passes": "classify by rank/sign of Z_AB and generalized spectrum M v=mu^2 Z v",
            "if_fails": "operator not yet owned; no alpha or rank-zero claim",
            "status": "CLASSIFIER_DERIVED",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "FRC4519_1_finite_range",
            "branch": "finite-range Yukawa",
            "mathematical_test": "rank(Z_AB)>0 on a physical source-coupled quotient and mu_i^2>0",
            "if_passes": "lambda_i=1/mu_i and alpha_i(lambda_i) must be scored against R10 bound curve",
            "if_fails": "do not fabricate lambda from M_AB alone",
            "status": "FINITE_RANGE_CONTRACT_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "FRC4519_2_rank_zero",
            "branch": "rank-zero algebraic constraint",
            "mathematical_test": "rank(Z_AB)=0 on physical quotient and M_AB is invertible or first-class constrained",
            "if_passes": "no Yukawa alpha exists; solve algebraic residual M_AB Z^B=J_A+B_A+C_A+R_A",
            "if_fails": "null/wrong-sign/massless directions need separate PPN/stability handling",
            "status": "RANK_ZERO_ROUTE_CONDITIONAL_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "FRC4519_3_spectral_memory",
            "branch": "spectral/nonlocal memory",
            "mathematical_test": "operator has spectral measure d rho(mu) rather than finite matrix Z/M",
            "if_passes": "alpha(lambda) becomes an envelope over spectral weights and charges",
            "if_fails": "not relevant",
            "status": "DEFERRED_UNTIL_KERNEL_OWNED",
            "valid_for_claim": False,
        },
        {
            "classifier_id": "FRC4519_4_current_verdict",
            "branch": "current corpus",
            "mathematical_test": "Z_AB rank/sign, M_AB lock, source split, charges and bound curve",
            "if_passes": "none currently pass",
            "if_fails": "stage both input packs; make no R10/local-GR claim",
            "status": "NO_BRANCH_SELECTED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def alpha_input_rows() -> List[Dict[str, object]]:
    return [
        {"input_id": "AIC4519_0_Z", "quantity": "Z_X or Z_AB eigenvalue", "formula_role": "normalizes kinetic operator and alpha denominator", "required_evidence": "parent action/principal symbol with units", "current_status": "MISSING_PARENT_Z", "valid_for_claim": False},
        {"input_id": "AIC4519_1_M", "quantity": "M_X^2 or M_AB eigenvalue", "formula_role": "sets mu^2 and lambda=sqrt(Z/M^2)", "required_evidence": "parent Hessian/operator mass on same quotient domain", "current_status": "MISSING_PARENT_M", "valid_for_claim": False},
        {"input_id": "AIC4519_2_Qsource", "quantity": "Q_X^S", "formula_role": "source charge in alpha numerator", "required_evidence": "same-frame source-normalized charge integral, not inferred from bound", "current_status": "MISSING_SOURCE_CHARGE_ZERO_OR_VALUE", "valid_for_claim": False},
        {"input_id": "AIC4519_3_qtest", "quantity": "q_X^T", "formula_role": "test charge in alpha numerator", "required_evidence": "test-body response/source charge theorem or value", "current_status": "MISSING_TEST_CHARGE_ZERO_OR_VALUE", "valid_for_claim": False},
        {"input_id": "AIC4519_4_calibration", "quantity": "G_N^obs M_S m_T", "formula_role": "Newton denominator and same-frame calibration", "required_evidence": "pre-readout Hilbert mass/current calibration", "current_status": "CONDITIONAL_CALIBRATION_NOT_FULLY_SIGNED", "valid_for_claim": False},
        {"input_id": "AIC4519_5_bound_curve", "quantity": "alpha_bound(lambda)", "formula_role": "R10 acceptance bound", "required_evidence": "full digitized/source-backed curve or official table", "current_status": "FULL_CURVE_MISSING_VISUAL_POINTS_NONCLAIM", "valid_for_claim": False},
        {"input_id": "AIC4519_6_interpolation", "quantity": "interpolation rule", "formula_role": "evaluate bound at predicted lambda", "required_evidence": "declared log-log or official interpolation over in-domain lambda", "current_status": "PRIVATE_CANDIDATE_ONLY", "valid_for_claim": False},
    ]


def rank_zero_residual_rows() -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RZR4519_0_normal_form",
            "component": "algebraic rank-zero equation",
            "formula": "M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector",
            "zero_condition": "M_AB invertible/first-class and RHS=0",
            "fallback": "Z_alg = M^{-1}(J+B+CDB+R)",
            "valid_for_claim": False,
        },
        {"residual_id": "RZR4519_1_J", "component": "J_A source current", "formula": "ordinary/source/memory/readout source projection into eliminated direction", "zero_condition": "Dq[v_Z]=0, matter/source descent, no marker/current-owner theorem", "fallback": "|M^{-1}J|", "valid_for_claim": False},
        {"residual_id": "RZR4519_2_B", "component": "B_A boundary/corner", "formula": "worldtube, corner, reference and projector flux terms", "zero_condition": "proper/no-flux boundary with no source-reference charge", "fallback": "|M^{-1}B|", "valid_for_claim": False},
        {"residual_id": "RZR4519_3_CDB", "component": "C_A^CDB connection/domain/boundary derivative tails", "formula": "hidden derivative/principal-symbol or lower-order tails", "zero_condition": "CDB terms zero/topological or included in owned constraint algebra", "fallback": "|M^{-1}CDB|", "valid_for_claim": False},
        {"residual_id": "RZR4519_4_R", "component": "R_A source/readout/projector residual", "formula": "readout, projector, source-normalization reentry", "zero_condition": "observed descent and fixed readout protocol", "fallback": "|M^{-1}R|", "valid_for_claim": False},
        {"residual_id": "RZR4519_5_observable", "component": "local observable residual", "formula": "E_local <= K_obs ||Z_alg|| + direct source-tail terms", "zero_condition": "Z_alg=0 and direct source tails zero", "fallback": "finite local residual vector for PPN/R10/clocks/orbits", "valid_for_claim": False},
    ]


def bound_curve_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "BCG4519_0_anchor",
            "object": "EotWash alpha=1 threshold anchors",
            "current_evidence": "anchors exist but are not dense curves",
            "admission": "provenance only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BCG4519_1_visual_points",
            "object": "visual/manual curve candidates",
            "current_evidence": "nonclaim approximate points with review caveats",
            "admission": "private smoke only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BCG4519_2_full_curve",
            "object": "claim-ready alpha_bound(lambda)",
            "current_evidence": "missing",
            "admission": "required before R10 scoring",
            "valid_for_claim": False,
        },
        {
            "gate_id": "BCG4519_3_MTS_prediction",
            "object": "alpha_X(lambda_X)",
            "current_evidence": "formula exists; Z/M/charges missing",
            "admission": "required before comparison",
            "valid_for_claim": False,
        },
    ]


def branch_status_rows() -> List[Dict[str, object]]:
    return [
        {"branch_status_id": "BST4519_0_finite_range", "branch": "finite range", "status": "INPUT_PACK_READY_NOT_FILLED", "next_input": "Z_X,M_X^2,Q_X^S,q_X^T,Z_X normalization,bound curve", "valid_for_claim": False},
        {"branch_status_id": "BST4519_1_rank_zero", "branch": "rank zero", "status": "CONDITIONAL_THEOREM_READY_NOT_SIGNED", "next_input": "rank(Z)=0 certificate, M lock, RHS source/boundary/CDB/readout zero", "valid_for_claim": False},
        {"branch_status_id": "BST4519_2_constraint", "branch": "first-class constraint", "status": "ALLOWED_NOT_PROVED", "next_input": "primary/secondary constraint algebra and Dirac count", "valid_for_claim": False},
        {"branch_status_id": "BST4519_3_wrong_sign", "branch": "massless/wrong-sign", "status": "REJECT_OR_ROUTE_TO_PPN_IF_FOUND", "next_input": "stability/gauge proof or residual bounds", "valid_for_claim": False},
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {"audit_id": "PA4519_0_classifier", "clause": "finite-range/rank-zero classifier", "status": "DERIVED", "reason": "operator rank and generalized spectrum decide whether alpha(lambda) exists", "valid_for_claim": False},
        {"audit_id": "PA4519_1_alpha", "clause": "alpha input pack", "status": "READY_NOT_FILLED", "reason": "formula and columns are specified but parent values are missing", "valid_for_claim": False},
        {"audit_id": "PA4519_2_rank_zero", "clause": "rank-zero algebraic residual", "status": "DERIVED_CONDITIONAL", "reason": "normal form written but rank/source/boundary/CDB/descent not signed", "valid_for_claim": False},
        {"audit_id": "PA4519_3_bound_curve", "clause": "R10 bound data", "status": "NOT_CLAIM_READY", "reason": "anchors and visual candidates cannot replace full curve", "valid_for_claim": False},
        {"audit_id": "PA4519_4_claim", "clause": "local GR/R10", "status": "NOT_CLAIMED", "reason": "no branch selected and no inputs claim-valid", "valid_for_claim": False},
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4519_0_branch", "claim": "branch selected", "passed": False, "blocker": "Z_AB rank/sign and M_AB lock missing", "valid_for_claim": False},
        {"gate_id": "CG4519_1_alpha", "claim": "R10 finite-range alpha pass", "passed": False, "blocker": "alpha inputs and full bound curve missing", "valid_for_claim": False},
        {"gate_id": "CG4519_2_rank_zero", "claim": "rank-zero local silence", "passed": False, "blocker": "rank certificate and RHS zero not parent-signed", "valid_for_claim": False},
        {"gate_id": "CG4519_3_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "source/rank/alpha gates remain nonclaim", "valid_for_claim": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "finite-range versus rank-zero branch classifier; alpha(lambda) input contract; rank-zero algebraic residual vector; bound-curve admission gate",
            "not_derived": "Z/M/rank certificate, source/test charges, full R10 bound curve, rank-zero RHS silence, local-GR claim",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4519_0",
            "decision": DECISION,
            "because": "4518 supplied the alpha formula but no values; existing rank-zero work supplies a conditional alternative. The correct next move is branch selection by Z-rank, not more vague source-tail auditing.",
            "effect": "4520 can pursue rank-zero source-current silence or fill alpha inputs with a defined schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4519_0",
            "target_file": NEXT_TARGET,
            "task": "try rank-zero source-current silence first; if rank-zero fails, fill alpha input acquisition rows for Z/M/source/test charges and bound curve",
            "success_condition": "rank-zero RHS zero theorem closes or alpha(lambda) gets source-backed nonplaceholder inputs",
            "avoid": "using visual bound points for claims or deriving lambda from M_AB without Z_AB",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        BRANCH_CLASSIFIER,
        ALPHA_INPUT_CONTRACT,
        RANK_ZERO_RESIDUAL,
        BOUND_CURVE_GATE,
        BRANCH_STATUS,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    details = []
    parsed_ok = True
    for path in csv_paths:
        try:
            details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover
            parsed_ok = False
            details.append(f"{path.name}:FAIL:{exc}")
    sources_ok = all(row["exists"] and row["needle_found"] for row in all_rows["sources"])
    classifier_ok = any(row["classifier_id"] == "FRC4519_2_rank_zero" for row in all_rows["classifier"])
    alpha_ok = len(all_rows["alpha_inputs"]) == 7
    rank_ok = any(row["residual_id"] == "RZR4519_0_normal_form" for row in all_rows["rank"])
    bound_ok = any(row["gate_id"] == "BCG4519_2_full_curve" for row in all_rows["bound"])
    gates_blocked = all(str(row.get("passed")) == "False" for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed"):
                if key in row and str(row[key]).lower() != "false":
                    flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks = [
        ("VAL4519_00_sources", sources_ok, "all source paths exist and source needles are found"),
        ("VAL4519_01_classifier", classifier_ok, "rank-zero branch classifier exists"),
        ("VAL4519_02_alpha_inputs", alpha_ok, "alpha input contract has seven required rows"),
        ("VAL4519_03_rank_residual", rank_ok, "rank-zero algebraic residual vector exists"),
        ("VAL4519_04_bound_gate", bound_ok, "full bound curve admission gate exists"),
        ("VAL4519_05_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4519_06_nonclaim_flags", flags_false, "all claim flags remain false"),
        ("VAL4519_07_csv_parse", parsed_ok, ";".join(details)),
        ("VAL4519_08_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4519_09_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {"validation_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4519_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4519 bulk/range alpha curve input fill or rank-zero constraint",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_range_or_rank_branch",
            "4519 derives the finite-range versus rank-zero branch classifier. If rank(Z_AB)>0 and mu_i^2>0, the theory has a Yukawa alpha(lambda) branch requiring Z/M/source/test charges and a full R10 bound curve. If rank(Z_AB)=0 and M_AB is invertible or first-class constrained, no Yukawa alpha exists; the branch becomes an algebraic residual M_AB Z^B=J_A+B_A+C_A^CDB+R_A. Current corpus selects neither branch, so both input packs are staged nonclaim.",
            "4519 source register, branch classifier, alpha input contract, rank-zero residual vector, bound curve gate, branch status, parent audit, claim gates, status and validation.",
            "private_range_or_rank_branch_classifier_nonclaim",
            NEXT_TARGET,
            "using visual R10 points for claims, deriving lambda from M_AB without Z_AB, or declaring rank-zero local silence without RHS zero.",
            "local_gr_newton_r2fr_range_or_rank_branch",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "try rank-zero source-current silence first; otherwise fill alpha(lambda) inputs.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    classifier: Sequence[Mapping[str, object]],
    alpha_inputs: Sequence[Mapping[str, object]],
    rank: Sequence[Mapping[str, object]],
    bound: Sequence[Mapping[str, object]],
    branch_status: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4519 - Bulk/Range Alpha Curve Input Fill Or Rank-Zero Constraint

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4519 prevents the two possible routes from being mixed.

Finite range exists only if the parent operator has real physical principal symbol:

`L_AB=-Z_AB Delta + M_AB`, with `rank(Z_AB)>0` and `M_AB v_i = mu_i^2 Z_AB v_i`.

Then `lambda_i=1/mu_i` and the R10 object is `alpha_i(lambda_i)`.

Rank-zero is different. If `rank(Z_AB)=0` on the physical quotient, there is no Yukawa range to score. The branch becomes:

`M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector`.

It is silent only if `M_AB` is locked and the whole right-hand side vanishes in the same parent branch. Current evidence does not select either route, so 4519 stages both input packs as nonclaim.

## Source Register

{table(sources)}

## Finite-Range Or Rank-Zero Branch Classifier

{table(classifier)}

## Alpha(lambda) Input Contract

{table(alpha_inputs)}

## Rank-Zero Algebraic Residual Vector

{table(rank)}

## Bound Curve Admission Gate

{table(bound)}

## Branch Status

{table(branch_status)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    classifier = branch_classifier_rows()
    alpha_inputs = alpha_input_rows()
    rank = rank_zero_residual_rows()
    bound = bound_curve_gate_rows()
    branch_status = branch_status_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "classifier": classifier,
        "alpha_inputs": alpha_inputs,
        "rank": rank,
        "bound": bound,
        "branch_status": branch_status,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BRANCH_CLASSIFIER, classifier)
    write_csv(ALPHA_INPUT_CONTRACT, alpha_inputs)
    write_csv(RANK_ZERO_RESIDUAL, rank)
    write_csv(BOUND_CURVE_GATE, bound)
    write_csv(BRANCH_STATUS, branch_status)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, classifier, alpha_inputs, rank, bound, branch_status, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4519 Bulk/Range Alpha Curve Input Fill Or Rank-Zero Constraint

Marker: `{MARKER}`  
4519 derives the branch classifier for the bulk/range source tail. If `rank(Z_AB)>0` and `M_AB v=mu^2 Z_AB v`, the branch is finite-range and requires a real `alpha(lambda)` input pack. If `rank(Z_AB)=0`, no Yukawa range exists; the branch is algebraic with residual `M_AB Z^B=J_A+B_A+C_A^CDB+R_A`. Current evidence selects neither branch, so no R10/local-GR claim is made.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4519 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now separates finite-range scoring from rank-zero algebraic elimination. The next useful move is rank-zero source-current silence; if that fails, fill the alpha(lambda) inputs.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
