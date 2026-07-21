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

CHECKPOINT = "4518"
CLAIM_ID = "L-360"
MARKER = "PPC4161_DOMAIN_R11_SILENCE_OR_BULK_RANGE_ALPHA_CURVE_4518"
PACKET_MARKER = "PPC4161_PACKET_DOMAIN_R11_SILENCE_OR_BULK_RANGE_ALPHA_CURVE_4518"
DECISION = "DOMAIN_R11_FACTORISATION_TEST_DERIVED_BULK_RANGE_ALPHA_CURVE_SCAFFOLD_STAGED_NONCLAIM"
NEXT_TARGET = "4519-Y5-R2FR-bulk-range-alpha-curve-input-fill-or-rank-zero-constraint.md"

FORMAL_PATH = FORMAL / "534-PPC4161-domain-R11-silence-or-bulk-range-alpha-curve.md"
DOC_PATH = POST / "4518-Y5-R2FR-domain-R11-silence-or-bulk-range-alpha-curve.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4518_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4518_SOURCE_REGISTER.csv"
R11_FACTOR_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4518_DOMAIN_R11_FACTORISATION_THEOREM.csv"
R11_INVENTORY = SOURCE_DIR / "P8_Y5_R2FR_4518_DOMAIN_R11_OPERATOR_INVENTORY.csv"
R11_VERDICT = SOURCE_DIR / "P8_Y5_R2FR_4518_DOMAIN_R11_VERDICT.csv"
BULK_ALPHA_SCAFFOLD = SOURCE_DIR / "P8_Y5_R2FR_4518_BULK_RANGE_ALPHA_CURVE_SCAFFOLD.csv"
BRANCH_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4518_BRANCH_DECISION_MATRIX.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4518_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4518_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4518_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4518_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4518_DECISION.csv"

FORMAL_533 = FORMAL / "533-PPC4161-domain-bulk-species-source-tail-or-coefficient-fill.md"
POST_4517 = POST / "4517-Y5-R2FR-domain-bulk-species-source-tail-or-coefficient-fill.md"
THEOREM_4517 = SOURCE_DIR / "P8_Y5_R2FR_4517_DOMAIN_PROJECTOR_DOUBLE_ZERO_NOFLUX_THEOREM.csv"
Y5_4517 = SOURCE_DIR / "P8_Y5_R2FR_4517_Y5_UPDATED_CLOSURE_MAP.csv"
R11_GATE_4517 = SOURCE_DIR / "P8_Y5_R2FR_4517_R11_DOMAIN_SILENCE_GATE.csv"
DOMAIN_VECTOR_4517 = SOURCE_DIR / "P8_Y5_R2FR_4517_DOMAIN_PROJECTOR_COEFFICIENT_VECTOR.csv"
R11_EXEC = SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv"
R11_TEMPLATE = SOURCE_DIR / "R11_nonEH_operator_vector_TEMPLATE.csv"
DOUBLE_ZERO_R11 = SOURCE_DIR / "P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv"
DOMAIN_NOVECTOR = SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv"
DOMAIN_ALPHA3 = SOURCE_DIR / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
BULK_FILL = SOURCE_DIR / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv"
BULK_POSITIVE = SOURCE_DIR / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv"
YUKAWA_3694 = SOURCE_DIR / "P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv"
YUKAWA_4032 = SOURCE_DIR / "P8_Y5_R2FR_4032_YUKAWA_HAIR_BOUND_INPUT.csv"
YUKAWA_2209 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2209_QLOC_TO_YUKAWA_SOURCE_MAP_ATTEMPT.csv"
RANGE_2210 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv"
RANGE_2211 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2211_HESSIAN_VS_RANGE_LEMMA.csv"

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
        ("SRC4518_00_formal533", "4517 formal handoff", FORMAL_533, "PPC4161_DOMAIN_BULK_SPECIES_SOURCE_TAIL_OR_COEFFICIENT_FILL_4517", "4517 handoff"),
        ("SRC4518_01_post4517", "4517 post handoff", POST_4517, "NT4517_0", "declares 4518 target"),
        ("SRC4518_02_theorem4517", "4517 domain theorem", THEOREM_4517, "DPN4517_5_domain_row_verdict", "domain verdict"),
        ("SRC4518_03_y5_4517", "4517 Y5 closure map", Y5_4517, "CONDITIONAL_DOMAIN_DOUBLE_ZERO_NOFLUX_ZERO", "domain row conditional closure"),
        ("SRC4518_04_r11gate4517", "4517 R11 gate", R11_GATE_4517, "R11D4517_1_executable_vector", "R11 executable vector gate"),
        ("SRC4518_05_domainvector4517", "4517 domain coefficient vector", DOMAIN_VECTOR_4517, "R11_EH_operator_ledger", "domain R11 coefficient target"),
        ("SRC4518_06_r11exec", "R11 executable vector", R11_EXEC, "source_normalization_operator", "current executable R11 vector"),
        ("SRC4518_07_r11template", "R11 template", R11_TEMPLATE, "source_normalization_operator", "template fallback"),
        ("SRC4518_08_doublezero", "double-zero R11 variation", DOUBLE_ZERO_R11, "V2_R11_variation", "factorized R11 zero identity"),
        ("SRC4518_09_domain_novector", "domain no-vector theorem", DOMAIN_NOVECTOR, "T4_R11_operator_silence", "R11 no-vector blocker"),
        ("SRC4518_10_domain_alpha3", "domain alpha3 theorem", DOMAIN_ALPHA3, "N5_R11_operator_silence", "R11 alpha3 blocker"),
        ("SRC4518_11_bulkfill", "bulk range fill row", BULK_FILL, "FB557_0_bulk_memory_range_zero_or_Yukawa_bound", "bulk alpha fallback"),
        ("SRC4518_12_bulkpositive", "bulk positive operator", BULK_POSITIVE, "BMR557_5_mass_gap_not_enough", "mass gap guard"),
        ("SRC4518_13_yukawa3694", "Yukawa arena runner rows", YUKAWA_3694, "YBR3694_1_R10_Newton", "R10 alpha runner shape"),
        ("SRC4518_14_yukawa4032", "Yukawa hair bound input", YUKAWA_4032, "YUK4032_1_force", "Yukawa force formula"),
        ("SRC4518_15_yukawa2209", "q_loc to Yukawa map", YUKAWA_2209, "YSM2209_3_charge_normalization", "charge normalization gate"),
        ("SRC4518_16_range2210", "range operator derivation", RANGE_2210, "ROD2210_1_generalized_range_spectrum", "operator spectrum range owner"),
        ("SRC4518_17_range2211", "Hessian/range lemma", RANGE_2211, "HVR2211_1_finite_range_case", "finite range theorem"),
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


def r11_factor_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "R11F4518_0_exact_factor_test",
            "object": "domain R11 source-normalization operator",
            "statement": "A retained domain R11 operator is locally silent on the double-zero branch iff its local contribution is Sigma_loc-factorized or independently topological/no-flux.",
            "formula": "S_R11,D=sum_A int sqrt(-g) [Sigma_loc c_A O_A + S_top,A]; Y_loc=0 => delta(Sigma_loc O_A)=0",
            "zero_route": "Sigma_loc=G_AB Y^A Y^B, Y_loc=0, delta Sigma_loc=0, and every non-topological O_A is multiplied by Sigma_loc",
            "fallback": "any unfactorized O_A must carry coefficient, units, weak-field map and source path",
            "status": "EXACT_CONDITIONAL_FACTORISATION_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "R11F4518_1_no_absorption",
            "object": "measured-G/source normalization",
            "statement": "An unfactorized domain R11 operator cannot be absorbed into fitted G_N or cancelled against a different source tail.",
            "formula": "|c_domain_R11| <= sum_A |c_A O_A| componentwise unless a parent Ward identity removes the component",
            "zero_route": "componentwise theorem-zero only",
            "fallback": "absolute coefficient vector and arena maps",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "R11F4518_2_current_inventory_verdict",
            "object": "current R11 vector",
            "statement": "The current executable R11 vector is wired but not a factorized inventory: relevant domain rows are retained as missing or conditional.",
            "formula": "source_normalization_operator, vector_preferred_frame, projector_domain_stress are not all claim-valid zero rows",
            "zero_route": "not currently satisfied",
            "fallback": "move to executable coefficient fill or bulk/range alpha(lambda)",
            "status": "LIVE_DOMAIN_R11_SILENCE_NOT_CLOSED",
            "valid_for_claim": False,
        },
    ]


def classify_r11(row: Mapping[str, str]) -> str:
    family = row.get("operator_family", "")
    value = row.get("coefficient_value", "")
    status = row.get("derivation_status", "")
    if family == "projector_domain_stress" and value.startswith("0_IF_PARENT_OWNS_METRIC_INDEPENDENT"):
        return "CONDITIONAL_TOPOLOGICAL_PROJECTOR_NOT_PARENT_OWNED"
    if family == "source_normalization_operator":
        return "MISSING_SIGMA_FACTORISATION_OR_EXECUTABLE_COEFFICIENT"
    if family == "vector_preferred_frame":
        return "MISSING_NO_VECTOR_THEOREM_OR_COEFFICIENT_PRODUCTS"
    if status == "retained_out_of_scope_for_473":
        return "GLOBAL_R11_FAMILY_RETAINED_OUTSIDE_DOMAIN_MINIMUM"
    return "RETAINED_OR_TEMPLATE"


def r11_inventory_rows() -> List[Dict[str, object]]:
    domain_families = {"vector_preferred_frame", "source_normalization_operator", "projector_domain_stress"}
    rows: List[Dict[str, object]] = []
    for row in read_csv(R11_EXEC):
        family = row.get("operator_family", "")
        if family not in domain_families:
            continue
        rows.append(
            {
                "inventory_id": f"R11INV4518_{len(rows)}_{family}",
                "operator_family": family,
                "coefficient_symbol": row.get("coefficient_symbol"),
                "operator_form": row.get("operator_form"),
                "affected_rows": row.get("affected_rows"),
                "current_value": row.get("coefficient_value"),
                "factorisation_test": "is local contribution Sigma_loc * O_A or independently topological/no-flux?",
                "4518_status": classify_r11(row),
                "fallback": row.get("predicted_residual_or_bound_source"),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def r11_verdict_rows() -> List[Dict[str, object]]:
    return [
        {
            "verdict_id": "R11V4518_0_domain_R11",
            "question": "Is c_domain_source_normalization_operator theorem-zero now?",
            "answer": "NO_CURRENT_CORPUS",
            "because": "the current R11 vector has domain rows wired but not Sigma_loc-inventoried or claim-valid executable",
            "effect": "4517 domain closure remains conditional, not claim-live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "verdict_id": "R11V4518_1_what_would_close",
            "question": "What would close it?",
            "answer": "FULL_FACTORISED_INVENTORY_OR_EXECUTABLE_VECTOR",
            "because": "each domain R11 operator must be Sigma_loc-factorized/topological or have coefficient units maps source path and bounds",
            "effect": "4519 should either fill the inventory or pivot to bulk/range alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bulk_alpha_rows() -> List[Dict[str, object]]:
    return [
        {
            "alpha_id": "BAR4518_0_operator",
            "object": "finite-range operator",
            "formula": "(-Z_AB Delta + M_AB) X^B = J_A; M_AB v_i^B = mu_i^2 Z_AB v_i^B; lambda_i=1/mu_i",
            "needed_inputs": "parent Z_AB, M_AB, quotient domain, units, source split J_A",
            "status": "RANGE_OWNER_LAW_IMPORTED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_1_one_mode",
            "object": "single scalar-equivalent mode",
            "formula": "lambda_X=sqrt(Z_X/M_X^2) for Z_X>0, M_X^2>0",
            "needed_inputs": "Z_X, M_X^2, same branch convention",
            "status": "ONE_MODE_REDUCTION_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_2_yukawa_solution",
            "object": "potential",
            "formula": "V_X(r)=-[Q_X^S q_X^T/(4*pi Z_X)] exp(-r/lambda_X)/r",
            "needed_inputs": "source charge Q_X^S, test charge q_X^T, normalization Z_X",
            "status": "FORCE_LAW_CONVENTION_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_3_alpha_definition",
            "object": "source-normalized alpha(lambda)",
            "formula": "alpha_X(lambda_X)=[Q_X^S q_X^T/(4*pi Z_X)]/[G_N^obs M_S m_T]",
            "needed_inputs": "same-frame G_N^obs, M_S, m_T, Q_X^S, q_X^T, Z_X",
            "status": "ALPHA_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_4_residual",
            "object": "R10 acceleration residual",
            "formula": "|delta a/a_N|=|alpha_X(lambda_X)| exp(-r/lambda_X)(1+r/lambda_X)",
            "needed_inputs": "arena radius r, lambda_X, alpha_X(lambda_X)",
            "status": "R10_RESIDUAL_FORMULA_READY",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_5_zero_guard",
            "object": "what is actually zero",
            "formula": "Q_X^S=0 or q_X^T=0 or parent removes X => alpha_X=0; M_X^2>0 alone does not imply alpha_X=0",
            "needed_inputs": "source/test charge zero theorem or no-field theorem",
            "status": "MASS_GAP_NOT_ENOUGH_GUARD",
            "valid_for_claim": False,
        },
        {
            "alpha_id": "BAR4518_6_bound_rule",
            "object": "claim rule",
            "formula": "claim only if full alpha_bound(lambda) curve exists and |alpha_X(lambda)| <= alpha_bound(lambda) over the tested range",
            "needed_inputs": "digitized/source-backed R10 bound curve, interpolation rule, provenance",
            "status": "BOUND_RULE_READY_BOUND_CURVE_MISSING",
            "valid_for_claim": False,
        },
    ]


def branch_decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "branch_id": "BD4518_0_domain_R11",
            "route": "close domain R11 silence",
            "current_result": "not closed",
            "reason": "factorized inventory/executable vector missing",
            "next_input": "domain R11 operator inventory with Sigma_loc factor flag or coefficient rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BD4518_1_bulk_range",
            "route": "build alpha(lambda)",
            "current_result": "formula scaffold ready",
            "reason": "bulk/range theorem needs Z/M, charges, and R10 bound curve",
            "next_input": "fill Z_X,M_X^2,Q_X^S,q_X^T,Z_X normalization and bound curve",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BD4518_2_rank_zero",
            "route": "rank-zero constraint escape",
            "current_result": "allowed but unproved",
            "reason": "if Z_AB has no physical quotient rank, no Yukawa lambda exists and source silence must be algebraic",
            "next_input": "rank certificate for Z_AB and constraint algebra",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {"audit_id": "PA4518_0_R11_theorem", "clause": "R11 Sigma factorization theorem", "status": "DERIVED_CONDITIONAL", "reason": "double-zero product variation proves local silence if every retained operator is Sigma factorized", "valid_for_claim": False},
        {"audit_id": "PA4518_1_inventory", "clause": "current R11 inventory", "status": "NOT_CLOSED", "reason": "domain rows are missing coefficients or parent-owned zero flags", "valid_for_claim": False},
        {"audit_id": "PA4518_2_alpha", "clause": "bulk/range alpha(lambda)", "status": "FORMULA_DERIVED_VALUES_MISSING", "reason": "alpha formula is written but Z/M/charges/bound curve are missing", "valid_for_claim": False},
        {"audit_id": "PA4518_3_mass_gap", "clause": "positive mass gap", "status": "NOT_SUFFICIENT", "reason": "mass gap sets range but source/test charge sets amplitude", "valid_for_claim": False},
        {"audit_id": "PA4518_4_claim", "clause": "local GR/R10 claim", "status": "NOT_CLAIMED", "reason": "R11 and alpha(lambda) remain nonclaim", "valid_for_claim": False},
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4518_0_domain_R11", "claim": "domain R11 silence live", "passed": False, "blocker": "factorized operator inventory or executable coefficient vector missing", "valid_for_claim": False},
        {"gate_id": "CG4518_1_domain_Y5", "claim": "domain/projector Y5 row claim-live", "passed": False, "blocker": "4517 zero route still depends on CG4518_0 plus boundary source charge", "valid_for_claim": False},
        {"gate_id": "CG4518_2_R10", "claim": "bulk/range R10 pass", "passed": False, "blocker": "Z/M/charges/bound curve missing; mass gap alone forbidden", "valid_for_claim": False},
        {"gate_id": "CG4518_3_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "source-normalization and R11/alpha tails remain nonclaim", "valid_for_claim": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "exact domain R11 Sigma-factorization test; domain R11 inventory verdict; source-normalized bulk/range alpha(lambda) formula scaffold",
            "not_derived": "live domain R11 silence, source/test charges, Z/M range values, R10 bound curve, rank-zero constraint certificate",
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
            "decision_id": "DEC4518_0",
            "decision": DECISION,
            "because": "domain R11 silence cannot be promoted from the current executable vector, so the exact factorization test and the bulk/range alpha(lambda) formula are written as the next executable contracts",
            "effect": "4519 can either fill/factorize domain R11 rows or move directly into alpha(lambda) input acquisition without changing the theory standard",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4518_0",
            "target_file": NEXT_TARGET,
            "task": "fill the bulk/range alpha(lambda) inputs or prove the rank-zero constraint branch; only return to domain R11 if a factorized operator inventory can be supplied",
            "success_condition": "one of: domain R11 factorized inventory closes, alpha(lambda) has Z/M/charges/bounds, or rank-zero certificate proves no Yukawa branch",
            "avoid": "using M_X^2>0 as alpha=0 or hiding source-normalization in fitted G_N",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        R11_FACTOR_THEOREM,
        R11_INVENTORY,
        R11_VERDICT,
        BULK_ALPHA_SCAFFOLD,
        BRANCH_DECISION,
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
    theorem_ok = any(row["theorem_id"] == "R11F4518_0_exact_factor_test" for row in all_rows["theorem"])
    inventory_ok = len(all_rows["inventory"]) >= 3
    verdict_ok = any(row["answer"] == "NO_CURRENT_CORPUS" for row in all_rows["verdict"])
    alpha_ok = any(row["alpha_id"] == "BAR4518_3_alpha_definition" for row in all_rows["alpha"])
    guard_ok = any(row["alpha_id"] == "BAR4518_5_zero_guard" for row in all_rows["alpha"])
    gates_blocked = all(str(row.get("passed")) == "False" for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed"):
                if key in row and str(row[key]).lower() != "false":
                    flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks = [
        ("VAL4518_00_sources", sources_ok, "all source paths exist and source needles are found"),
        ("VAL4518_01_theorem", theorem_ok, "R11 factorization theorem exists"),
        ("VAL4518_02_inventory", inventory_ok, "domain R11 inventory has at least three relevant rows"),
        ("VAL4518_03_verdict", verdict_ok, "domain R11 is not falsely promoted"),
        ("VAL4518_04_alpha", alpha_ok, "bulk/range alpha(lambda) definition exists"),
        ("VAL4518_05_mass_gap_guard", guard_ok, "mass gap not enough guard exists"),
        ("VAL4518_06_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4518_07_nonclaim_flags", flags_false, "all claim flags remain false"),
        ("VAL4518_08_csv_parse", parsed_ok, ";".join(details)),
        ("VAL4518_09_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4518_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {"validation_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4518_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4518 domain R11 silence or bulk/range alpha curve",
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
            "local_gr_newton_r2fr_domain_R11_or_alpha_curve",
            "4518 derives the exact domain R11 Sigma-factorization test and audits the current R11 executable vector. Domain R11 silence is not live-closed because the domain rows are wired but not Sigma_loc-inventoried or claim-valid executable. The fallback bulk/range alpha(lambda) scaffold is derived: alpha_X=[Q_X^S q_X^T/(4*pi Z_X)]/[G_N^obs M_S m_T] with Yukawa residual |delta a/a_N|=|alpha_X| exp(-r/lambda_X)(1+r/lambda_X); mass gap alone is explicitly not alpha=0.",
            "4518 source register, R11 factorization theorem, R11 operator inventory, R11 verdict, bulk alpha scaffold, branch decision matrix, parent audit, claim gates, status and validation.",
            "private_domain_R11_factorization_and_alpha_curve_scaffold_nonclaim",
            NEXT_TARGET,
            "claiming domain R11 silence from wired placeholders, using positive mass gap as fifth-force zero, or absorbing alpha(lambda) into fitted G_N.",
            "local_gr_newton_r2fr_domain_R11_or_alpha_curve",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "fill bulk/range alpha(lambda) inputs or prove rank-zero constraint; return to domain R11 only with a factorized inventory.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    inventory: Sequence[Mapping[str, object]],
    verdict: Sequence[Mapping[str, object]],
    alpha: Sequence[Mapping[str, object]],
    branch: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4518 - Domain R11 Silence Or Bulk/Range Alpha Curve

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4518 attacks the exact hard gate left by 4517.

Domain R11 silence is not yet live-closed. The correct test is:

`S_R11,D=sum_A int sqrt(-g) [Sigma_loc c_A O_A + S_top,A]; Y_loc=0 => delta(Sigma_loc O_A)=0`.

So a domain R11 operator is locally silent only if every retained non-topological domain operator is `Sigma_loc`-factorized, or if it is independently topological/no-flux. The current executable R11 vector is wired, but the relevant domain rows are still missing zero proofs or coefficient products.

The fallback is now an actual alpha-curve formula rather than a vague fifth-force sentence:

`V_X(r)=-[Q_X^S q_X^T/(4*pi Z_X)] exp(-r/lambda_X)/r`,

`alpha_X(lambda_X)=[Q_X^S q_X^T/(4*pi Z_X)]/[G_N^obs M_S m_T]`,

`|delta a/a_N|=|alpha_X(lambda_X)| exp(-r/lambda_X)(1+r/lambda_X)`.

Mass gap alone is not enough: `M_X^2>0` gives a range, not zero amplitude. Zero needs `Q_X^S=0`, `q_X^T=0`, or a parent no-field/source-silence theorem.

## Source Register

{table(sources)}

## Domain R11 Factorisation Theorem

{table(theorem)}

## Domain R11 Operator Inventory

{table(inventory)}

## Domain R11 Verdict

{table(verdict)}

## Bulk/Range Alpha Curve Scaffold

{table(alpha)}

## Branch Decision Matrix

{table(branch)}

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
    theorem = r11_factor_theorem_rows()
    inventory = r11_inventory_rows()
    verdict = r11_verdict_rows()
    alpha = bulk_alpha_rows()
    branch = branch_decision_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "inventory": inventory,
        "verdict": verdict,
        "alpha": alpha,
        "branch": branch,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(R11_FACTOR_THEOREM, theorem)
    write_csv(R11_INVENTORY, inventory)
    write_csv(R11_VERDICT, verdict)
    write_csv(BULK_ALPHA_SCAFFOLD, alpha)
    write_csv(BRANCH_DECISION, branch)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, theorem, inventory, verdict, alpha, branch, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4518 Domain R11 Silence Or Bulk/Range Alpha Curve

Marker: `{MARKER}`  
4518 derives the exact domain R11 `Sigma_loc` factorization test and audits the current executable R11 vector. Domain R11 silence is not claim-live because the relevant rows are wired but not fully factorized or executable. The fallback bulk/range route is now concrete: `alpha_X(lambda_X)=[Q_X^S q_X^T/(4*pi Z_X)]/[G_N^obs M_S m_T]` and `|delta a/a_N|=|alpha_X| exp(-r/lambda_X)(1+r/lambda_X)`. A positive mass gap supplies range only, not zero amplitude.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4518 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has a hard decision fork: either supply a factorized domain R11 inventory, or fill the bulk/range alpha curve inputs. This prevents further circling around source-normalization without equations.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
