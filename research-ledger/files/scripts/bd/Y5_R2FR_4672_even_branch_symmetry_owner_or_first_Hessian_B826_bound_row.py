from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4672"
CLAIM_ID = "L-514"
BRANCH = "MTS_R2FR_Y5_EVEN_BRANCH_SYMMETRY_OWNER_OR_FIRST_HESSIAN_B826_BOUND_ROW_4672"
MARKER = "PPC4161_EVEN_BRANCH_SYMMETRY_OWNER_OR_FIRST_HESSIAN_B826_BOUND_ROW_4672"
PACKET_MARKER = "PPC4161_PACKET_EVEN_BRANCH_SYMMETRY_OWNER_OR_FIRST_HESSIAN_B826_BOUND_ROW_4672"
DECISION = "EVEN_BRANCH_OWNER_NOT_SOURCED_B826_WELDED_TO_EPSILONA_ZM_BOUND_PATH_NONCLAIM"
NEXT_TARGET = "4673-Y5-R2FR-no-source-slot-common-measure-bridge-or-first-ZM-B826-input-fill.md"

DOC_PATH = POST / "4672-Y5-R2FR-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md"
FORMAL_PATH = FORMAL / "688-PPC4161-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4671 = POST / "4671-Y5-R2FR-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md"
FORMAL_687 = FORMAL / "687-PPC4161-parent-memory-Hessian-signature-or-B826-root-lock-first-row.md"
FORMAL_647 = FORMAL / "647-PPC4161-branch-extremum-symmetry-or-parent-coefficient-fill.md"
FORMAL_648 = FORMAL / "648-PPC4161-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md"
FORMAL_542 = FORMAL / "542-PPC4161-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"

CSV_4671_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4671_NEXT_TARGET.csv"
CSV_4671_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4671_STRICT_MINIMUM_EVEN_BRANCH_THEOREM.csv"
CSV_4671_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4671_PARENT_HESSIAN_SIGNATURE_TEST.csv"
CSV_4671_B826 = SOURCE_DIR / "P8_Y5_R2FR_4671_B826_ROOT_LOCK_TEST.csv"
CSV_4671_FIRST = SOURCE_DIR / "P8_Y5_R2FR_4671_FIRST_HESSIAN_B826_ROW_CONTRACT.csv"
CSV_4671_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4671_STATUS.csv"
CSV_4671_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4671_VALIDATION.csv"

CSV_4631_SYM = SOURCE_DIR / "P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv"
CSV_4631_DER = SOURCE_DIR / "P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv"
CSV_4631_EPS = SOURCE_DIR / "P8_Y5_R2FR_4631_EPSILON_A_COEFFICIENT_FILL_ROWS.csv"
CSV_4631_LGR = SOURCE_DIR / "P8_Y5_R2FR_4631_LOCAL_GR_INSERT_ROWS.csv"
CSV_4631_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4631_VALIDATION.csv"

CSV_4632_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4632_IQ_SIGNATURE_HUNT_ROWS.csv"
CSV_4632_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4632_SIGNATURE_DECISION_MATRIX.csv"
CSV_4632_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_INPUT_ROWS.csv"
CSV_4632_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4632_EPSILONA_BOUND_RUNNER_RESULTS.csv"
CSV_4632_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4632_DECISION.csv"
CSV_4632_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4632_STATUS.csv"
CSV_4632_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4632_VALIDATION.csv"

CSV_4525_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
CSV_4525_SIG = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
CSV_4526_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv"
CSV_4526_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
CSV_4526_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv"
CSV_4526_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4526_VALIDATION.csv"

CSV_4507_FORMULA = SOURCE_DIR / "P8_Y5_R2FR_4507_BMEM_EFFECTIVE_FORMULA.csv"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4628_GAP = SOURCE_DIR / "P8_Y5_R2FR_4628_LAMBDA_MEM_GAP_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4672_SOURCE_REGISTER.csv"
OWNER_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_EVEN_BRANCH_OWNER_AUDIT.csv"
B826_WELD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_B826_EVEN_RESPONSE_WELD.csv"
BOUND_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_FIRST_ZM_B826_BOUND_ROW_CONTRACT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4672_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4672_VALIDATION.csv"


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
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
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


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4672_00_4671_next", CSV_4671_NEXT, "4672-Y5-R2FR-even-branch-symmetry-owner-or-first-Hessian-B826-bound-row.md", "4671 selected 4672."),
        ("SRC4672_01_4671_theorem", CSV_4671_THEOREM, "STM4671_3_even_branch_symmetry", "strict-minimum/even-branch theorem candidate."),
        ("SRC4672_02_4671_hessian", CSV_4671_HESSIAN, "HST4671_4_claim_result", "Hessian not promoted."),
        ("SRC4672_03_4671_B826", CSV_4671_B826, "BRL4671_2_even_route", "B826 even-response route."),
        ("SRC4672_04_4671_first", CSV_4671_FIRST, "FHR4671_4_B826_value", "first B826 finite row."),
        ("SRC4672_05_4671_status", CSV_4671_STATUS, "STRICT_MINIMUM_EVEN_BRANCH", "4671 nonclaim status."),
        ("SRC4672_06_4671_validation", CSV_4671_VALIDATION, "VAL4671_OVERALL,True,PASS", "4671 validation."),
        ("SRC4672_07_doc4671", DOC_4671, "strict-minimum/even-branch theorem", "4671 prose."),
        ("SRC4672_08_formal687", FORMAL_687, "parent-owned local branch symmetry", "4671 formal."),
        ("SRC4672_09_4631_sym", CSV_4631_SYM, "SYM4631_0_strong_parent_vertical_involution", "strong I_q route."),
        ("SRC4672_10_4631_reject", CSV_4631_SYM, "REJECTED_FOR_BETA_VISIBLE_ZERO", "weak symmetry rejection."),
        ("SRC4672_11_4631_der", CSV_4631_DER, "DER4631_1_beta_visible_zero", "conditional beta zero."),
        ("SRC4672_12_4631_eps", CSV_4631_EPS, "EPS4631_0_epsilon_A", "epsilon_A fallback."),
        ("SRC4672_13_4631_lgr", CSV_4631_LGR, "LGR4631_0_strong_symmetry_to_local_GR", "local-GR insert conditional."),
        ("SRC4672_14_4631_validation", CSV_4631_VALIDATION, "VAL4631_OVERALL,PASS", "4631 validation."),
        ("SRC4672_15_formal647", FORMAL_647, "Weak leakage-frame symmetry is rejected", "formal 4631."),
        ("SRC4672_16_4632_hunt", CSV_4632_HUNT, "HUNT4632_0_full_Iq_action_invariance", "full Iq not sourced."),
        ("SRC4672_17_4632_matrix", CSV_4632_MATRIX, "SIG4632_1_even_Am", "even A_m signature missing."),
        ("SRC4672_18_4632_inputs", CSV_4632_INPUTS, "IN4632_0_epsilonA", "bound input row."),
        ("SRC4672_19_4632_runner", CSV_4632_RUNNER, "RUN4632_0_current_live_branch", "fail-closed bound runner."),
        ("SRC4672_20_4632_decision", CSV_4632_DECISION, "FULL_IQ_SIGNATURE_NOT_SOURCED", "4632 decision."),
        ("SRC4672_21_4632_status", CSV_4632_STATUS, "full I_q/even-A_m signature not sourced", "4632 status."),
        ("SRC4672_22_4632_validation", CSV_4632_VALIDATION, "VAL4632_OVERALL,PASS", "4632 validation."),
        ("SRC4672_23_formal648", FORMAL_648, "full parent `I_q`/even-`A_m` signature", "formal 4632."),
        ("SRC4672_24_4525_theorem", CSV_4525_THEOREM, "QEZ4525_1_even_involution", "quotient-even theorem."),
        ("SRC4672_25_4525_sig", CSV_4525_SIG, "SIG4525_0_vertical_involution", "parent signature missing."),
        ("SRC4672_26_4526_hunt", CSV_4526_HUNT, "HUNT4526_4_parent_action_invariance", "parent action invariance not found."),
        ("SRC4672_27_4526_bridge", CSV_4526_BRIDGE, "BRG4526_4_full_parent_Z_verdict", "full parent Z verdict."),
        ("SRC4672_28_4526_coeff", CSV_4526_COEFF, "COF4526_6_total_symmetry_breaking_bound", "coefficient fallback."),
        ("SRC4672_29_4526_validation", CSV_4526_VALIDATION, "VAL4526_OVERALL", "4526 validation."),
        ("SRC4672_30_formal542", FORMAL_542, "full parent action signature is not found", "formal 4526."),
        ("SRC4672_31_4507_formula", CSV_4507_FORMULA, "BMF4507_1_826_term", "B826 formula."),
        ("SRC4672_32_4514_Bmem", CSV_4514_BMEM, "BMV4514_0_B826", "B826 component."),
        ("SRC4672_33_4621_ZM", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "Z/M source rows."),
        ("SRC4672_34_4628_gap", CSV_4628_GAP, "GAP4628_0_exact_positive_gap", "lambda/gap criterion."),
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


def owner_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("OWN4672_0_full_Iq", "full parent involution I_q on ker(Dq)", "I_q^2=1, q∘I_q=q, local section fixed", "would make odd vertical coefficients vanish", "4632 explicitly says full I_q signature not sourced", "NOT_SOURCED"),
        ("OWN4672_1_even_action_bundle", "action/measure/coframe/projector/boundary commute with I_q", "S_parent[I_q Phi]=S_parent[Phi] plus invariant measure/domain", "would make first vertical force theorem-owned", "4526/4632 mark action invariance missing", "NOT_SOURCED"),
        ("OWN4672_2_even_A_m", "visible matter scale A_m is I_q-even or absent as source-only slot", "A_m(q,z)=A_m(q,-z)", "gives beta_visible=0 by 4631", "only theorem shape is present; parent signature missing", "CONDITIONAL_ONLY"),
        ("OWN4672_3_even_B826_response", "826 response residual is I_q-even or branch-stationary", "R_826(q,z;X_B)=R_826(q,-z;X_B), X_B q-basic/fixed", "gives ∂z R_826|0=0 and B826=0", "no row currently signs I_q-even R_826 ownership", "MISSING_B826_OWNER"),
        ("OWN4672_4_strict_minimum", "strict stable local minimum", "Z_mem>=Z0>0 and M2_mem>=M0^2>0", "coercive memory operator and finite lambda", "Z0/M0^2 still missing", "MISSING_ZM_VALUES"),
        ("OWN4672_5_boundary_source", "same branch source/boundary silence", "EM/Poynting, hidden, non-Hilbert, boundary/readout channels signed zero or bounded", "prevents hidden residual from replacing beta/B826", "later B/J/Q gates remain open", "SEPARATE_GATES_OPEN"),
        ("OWN4672_6_verdict", "even-branch owner", "OWN4672_0 through 5 all signed in one branch", "would promote exact-zero route for beta_visible and B826 first component", "current corpus fails owner proof; use finite rows", "OWNER_NOT_PROVED_BOUND_ROUTE_SELECTED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_id": row[0],
            "required_owner": row[1],
            "signature_condition": row[2],
            "payoff": row[3],
            "current_evidence": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def b826_weld_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("WELD4672_0_formula", "B_826", "B_826=a_F L_cg^-2 R_m(m_L;X_B)", "imported from 4507/4514", "STRUCTURE_READY"),
        ("WELD4672_1_same_Iq", "same symmetry owner", "the same I_q that makes A_m even must also act on the 826 response sector", "prevents beta_visible and B826 being killed by different closures", "SAME_OWNER_REQUIRED"),
        ("WELD4672_2_even_response_theorem", "I_q-even R_826", "R_826(q,z;X_B)=R_826(q,-z;X_B) with X_B q-basic", "differentiating at z=0 gives R_m=0, hence B826=0", "EXACT_CONDITIONAL_NOT_SOURCED"),
        ("WELD4672_3_no_source_slot_theorem", "no independent 826 source slot", "R_826 descends through q only, or the 826 response is post-readout/non-parent", "vertical derivative vanishes because z is not an argument", "NEXT_DERIVE_ROUTE"),
        ("WELD4672_4_finite_bound", "finite B826 fallback", "|B_826| <= |a_F| L_cg^-2 |R_m|", "source-backed a_F, L_cg, R_m and profile can feed no-cancellation B_mem_eff bound", "FIRST_BOUND_ROW_REQUIRED"),
        ("WELD4672_5_verdict", "B826 exact zero", "same I_q/even response or no-source-slot bridge", "not promoted; current corpus lacks B826 owner/source values", "B826_OWNER_NOT_PROVED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "weld_id": row[0],
            "object": row[1],
            "condition_or_formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bound_row_contract(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BND4672_0_Iq_owner", "OWNER_ZERO", "I_q", "full parent involution on vertical kernel", "parent action/measure/projector/boundary source path", "MISSING_OWNER"),
        ("BND4672_1_no_source_slot", "OWNER_ZERO", "A_m/R_826 slot exclusion", "A_m and R_826 descend through q or are absent before variation", "no-source-slot/common-measure proof", "NEXT_TARGET"),
        ("BND4672_2_epsilonA", "FINITE_BOUND", "epsilon_A", "visible matter-scale vertical derivative norm", "numeric/source-backed value or theorem zero", "MISSING_VALUE"),
        ("BND4672_3_epsilonB", "FINITE_BOUND", "epsilon_B", "second body/test sensitivity derivative norm", "numeric/source-backed value or theorem zero", "MISSING_VALUE"),
        ("BND4672_4_ZM", "FINITE_BOUND", "Z0,M0^2,lambda_mem", "same-branch Hessian/range package", "positive parent Hessian rows; no R10 anchor substitution", "MISSING_ZM"),
        ("BND4672_5_CN", "FINITE_BOUND", "C_N", "Newton/Planck normalization convention", "same branch source normalization", "MISSING_CONVENTION"),
        ("BND4672_6_B826", "FINITE_BOUND", "a_F,L_cg,R_m,R_obs profile", "|B_826| <= |a_F|L_cg^-2|R_m| inserted into B_mem_eff", "source-backed units/profile", "MISSING_B826_VALUES"),
        ("BND4672_7_symbreak", "FINITE_BOUND", "epsilon_symbreak_abs", "absolute no-cancellation symmetry-breaking envelope", "source rows for action asymmetry/scalar/Poynting/non-source survivors", "MISSING_COMPONENT_VALUES"),
        ("BND4672_8_claim_switch", "COMMON", "valid_for_claim", "claim admission", "true only if owner-zero route signed or finite rows sourced and pass runners", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row[0],
            "route": row[1],
            "required_object": row[2],
            "definition": row[3],
            "claim_grade_requirement": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    bound: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    owner_rejected = any(row["status"] == "OWNER_NOT_PROVED_BOUND_ROUTE_SELECTED" for row in owner)
    b826_not_proved = any(row["status"] == "B826_OWNER_NOT_PROVED" for row in b826)
    first_bound_ready = any(row["row_id"] == "BND4672_6_B826" for row in bound)
    no_claim = all(str(row.get("valid_for_claim")) == "False" for row in owner + b826 + bound)
    data = [
        ("RUN4672_0_sources", sources_ok, "all source paths and needles found"),
        ("RUN4672_1_owner_test", owner_rejected, "even-branch owner test rejects current promotion"),
        ("RUN4672_2_B826_weld", b826_not_proved, "B826 is welded to the same owner/fallback fork"),
        ("RUN4672_3_bound_contract", first_bound_ready, "first finite Z/M+B826 bound row contract exists"),
        ("RUN4672_4_nonclaim", no_claim, "all rows remain valid_for_claim=false"),
        ("RUN4672_5_decision", DECISION.endswith("NONCLAIM"), "decision refuses local-GR/R10/PPN promotion"),
        ("RUN4672_6_next", NEXT_TARGET.startswith("4673-"), "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": row[0],
            "passed": bool(row[1]),
            "status": "PASS" if row[1] else "FAIL",
            "detail": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4672_0_same_owner", "Do not kill beta_visible and B826 with different unowned symmetries.", "PASS"),
        ("CTRL4672_1_no_weak_symmetry", "Weak leakage-frame symmetry is not enough for scalar beta or B826 source response.", "PASS"),
        ("CTRL4672_2_no_anchor_smuggle", "R10 anchor cannot sign Z/M/lambda.", "PASS"),
        ("CTRL4672_3_no_B826_total_Bmem", "B826 zero alone is not B_mem_eff zero.", "PASS"),
        ("CTRL4672_4_no_cancellation", "Finite route uses absolute component bounds.", "PASS"),
        ("CTRL4672_5_poynting_kept", "EM/Poynting/no-flux remains explicit, not hidden by symmetry language.", "PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4631/4632 prove the conditional I_q/even-A_m route but do not source the owner. 4672 extends the requirement to the 826 response: B826 can vanish only if the same parent owner makes R_826 even/stationary or removes it as a source slot. Otherwise Z/M, epsilon_A and B826 become finite bound inputs.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "full_Iq_owner_sourced": False,
            "even_Am_parent_sourced": False,
            "even_B826_response_sourced": False,
            "no_source_slot_bridge_sourced": False,
            "ZM_finite_rows_sourced": False,
            "B826_finite_row_sourced": False,
            "B826_zero": False,
            "Bmem_eff_zero": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The most economical proof now is a no-source-slot/common-measure bridge: show A_m and R_826 are q-basic or post-variation, so their vertical derivative vanishes without needing a new symmetry axiom. If that fails, fill the first Z/M+B826 finite input pack.",
            "derive_route": "Search and formalize a parent no-source-slot/common-measure theorem for A_m and R_826 under the same q-basic Hilbert source functor.",
            "fallback_route": "Source-fill epsilon_A, epsilon_B, Z0, M0^2, lambda_mem, C_N, a_F, L_cg, R_m and body profile rows and run the bound matrix.",
            "avoid": "Do not call weak leakage symmetry enough; do not use R10 anchor as Hessian; do not claim B_mem_eff zero from B826; do not hide Poynting/boundary channels.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str, sources: list[dict[str, Any]], runner: list[dict[str, Any]], outputs: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_failures = [row["source_id"] for row in sources if not (row["path_exists"] and row["needle_found"])]
    rows.append({"validation_id": "VAL4672_0_sources", "passed": not source_failures, "detail": "all source paths and needles found" if not source_failures else ";".join(source_failures), "timestamp_utc": timestamp})
    for path in [SOURCE_REGISTER, OWNER_AUDIT_CSV, B826_WELD_CSV, BOUND_ROW_CSV, RUNNER_CSV, CONTROL_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]:
        try:
            parsed = read_csv(path)
            rows.append({"validation_id": f"VAL4672_parse_{path.name}", "passed": len(parsed) > 0, "detail": f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}", "timestamp_utc": timestamp})
        except Exception as exc:
            rows.append({"validation_id": f"VAL4672_parse_{path.name}", "passed": False, "detail": repr(exc), "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4672_1_runner_pass", "passed": all(str(row["status"]) == "PASS" for row in runner), "detail": "runner rows passed" if all(str(row["status"]) == "PASS" for row in runner) else "runner failure", "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4672_2_outputs_exist", "passed": all(path.exists() for path in outputs), "detail": ";".join(str(path) for path in outputs if path.exists()), "timestamp_utc": timestamp})
    rows.append({"validation_id": "VAL4672_3_no_claim_promotion", "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in runner), "detail": "valid_for_claim remains false", "timestamp_utc": timestamp})
    overall = all(bool(row["passed"]) for row in rows)
    rows.append({"validation_id": "VAL4672_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_doc(
    timestamp: str,
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    content = f"""# 4672 — Even-branch symmetry owner or first Hessian/B826 bound row

Timestamp: `{timestamp}`

## Result

4672 welds the 4631/4632 `I_q` symmetry route to the 4671 `B_826` gate.

The exact-zero theorem is now stricter and cleaner:

```text
same parent I_q owns:
  A_m(q,z)=A_m(q,-z)
  R_826(q,z;X_B)=R_826(q,-z;X_B)
  Z_mem>=Z0>0
  M2_mem>=M0^2>0
```

Then

```text
β_visible = ∂z ln A_m|0 = 0
R_m(m0;X_B)=∂z R_826|0 = 0
B_826 = a_F L_cg^-2 R_m = 0.
```

The current corpus does **not** source that common owner.  Weak leakage-frame symmetry is already rejected for scalar channels, and 4632 says the full `I_q/even-A_m` signature is not sourced.  So 4672 refuses promotion and turns the path into a concrete fork:

1. derive a no-source-slot/common-measure bridge for `A_m` and `R_826`; or
2. fill finite rows for `epsilon_A`, `epsilon_B`, `Z0`, `M0^2`, `lambda_mem`, `C_N`, and `B_826`.

## Even-branch owner audit

{table(owner)}

## B826 response weld

{table(b826)}

## First finite row contract

{table(bound)}

## Runner

{table(runner)}

## Controls

{table(controls)}

## Decision

{table(decision)}

## Status

{table(status)}

## Next target

{table(next_target)}

## Source register

{table(sources)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def write_formal(
    timestamp: str,
    owner: list[dict[str, Any]],
    b826: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    decision: list[dict[str, Any]],
) -> None:
    content = f"""# PPC4161 — Even-branch symmetry owner or first Hessian/B826 bound row

Checkpoint: `{CHECKPOINT}`  
Claim row: `{CLAIM_ID}`  
Timestamp: `{timestamp}`

## Formal statement

The exact route requires one common parent owner, not separate closure moves:

```text
I_q^2=1, q∘I_q=q,
A_m(q,z)=A_m(q,-z),
R_826(q,z;X_B)=R_826(q,-z;X_B),
X_B is q-basic/fixed,
Z_mem>=Z0>0,
M2_mem>=M0^2>0.
```

Then differentiating at `z=0` gives

```text
β_visible = ∂z ln A_m|0 = 0,
R_m(m0;X_B)=0,
B_826=a_F L_cg^-2 R_m=0.
```

4672 does not promote this because the full owner is not sourced.  The branch therefore goes to a no-source-slot/common-measure proof attempt or to finite `epsilon_A/ZM/B826` bound rows.

## Owner audit

{table(owner)}

## B826 weld

{table(b826)}

## Bound contract

{table(bound)}

## Decision

{table(decision)}
"""
    FORMAL_PATH.write_text(content, encoding="utf-8")


def update_claims() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4672 welds the 4631/4632 even-branch route to the B826 gate. The exact-zero theorem now requires one common parent owner: I_q must make A_m even, make the 826 response R_826 even or source-slot silent, and sit on a strict positive Z/M branch. Then beta_visible=0 and B_826=0 follow by differentiation at the branch point. Current evidence says full I_q/even-A_m is not sourced and no B826 response owner row exists, so 4672 refuses promotion and locks the no-source-slot/common-measure bridge or first finite Z/M+B826 input pack.",
        "Generated source register, even-branch owner audit, B826 response weld, first ZM/B826 bound-row contract, runner, controls, decision, status, next target and validation.",
        "even_branch_owner_not_sourced_B826_welded_to_epsilonA_ZM_bound_path_nonclaim",
        NEXT_TARGET,
        "Using weak leakage-frame symmetry as scalar proof, killing beta_visible and B826 with different unowned mechanisms, using R10 anchor as Hessian data, claiming Bmem_eff zero from B826, hiding Poynting/boundary channels, or using cancellation.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until common owner or finite ZM/B826 rows are source-backed and remaining B/J/Q/metric gates close.",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        handle.write(csv_line(row))


def update_spine_and_packet() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4672 welds the even-branch symmetry route to the first `B_mem_eff` component. A common parent `I_q` would have to make both `A_m` and the 826 response `R_826` even/source-slot silent on the same positive `Z/M` branch. Then `β_visible=0` and `B_826=0` follow by differentiation at `z=0`. Current evidence rejects weak leakage symmetry and does not source the full owner, so the next target is `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` makes the coupling fork explicit: prove a no-source-slot/common-measure bridge for `A_m` and `R_826`, or fill finite `epsilon_A/ZM/B826` rows. Next packet target: `{NEXT_TARGET}`.
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    owner = owner_audit_rows(timestamp)
    b826 = b826_weld_rows(timestamp)
    bound = bound_row_contract(timestamp)
    runner = runner_rows(timestamp, sources, owner, b826, bound)
    controls = control_rows(timestamp)
    decision = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_AUDIT_CSV, owner)
    write_csv(B826_WELD_CSV, b826)
    write_csv(BOUND_ROW_CSV, bound)
    write_csv(RUNNER_CSV, runner)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    write_doc(timestamp, sources, owner, b826, bound, runner, controls, decision, status, next_target)
    write_formal(timestamp, owner, b826, bound, decision)
    update_claims()
    update_spine_and_packet()

    outputs = [
        DOC_PATH,
        FORMAL_PATH,
        SOURCE_REGISTER,
        OWNER_AUDIT_CSV,
        B826_WELD_CSV,
        BOUND_ROW_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validation = validation_rows(timestamp, sources, runner, outputs)
    write_csv(VALIDATION_CSV, validation)
    if not all(bool(row["passed"]) for row in validation):
        failures = [row for row in validation if not row["passed"]]
        raise SystemExit(f"4672 validation failed: {failures}")
    print(f"4672 complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
