from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3269-Y5-R2FR-fixed-local-constants-superselection-for-DD-zero-or-coefficient-runner-under-AX1090.md"
DOC_3268 = ROOT / "3268-Y5-R2FR-parent-low-energy-coefficient-vector-or-explicit-residual-basis-under-AX1090.md"
COEFF_3268 = OUT / "P8_Y5_R2FR_3268_LOW_ENERGY_COEFFICIENT_VECTOR.csv"
PROJ_3268 = OUT / "P8_Y5_R2FR_3268_DD_PROJECTION_MATRIX.csv"
RESID_3268 = OUT / "P8_Y5_R2FR_3268_EXPLICIT_RESIDUAL_BASIS.csv"
DELTA_MATRIX = OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv"
CONST_UNIV = OUT / "P8_constant_sector_universality_CONTRACT.csv"
GLOBAL_SUPER = OUT / "P8_global_coupling_superselection_CONTRACT.csv"
KAPPA_SUPER = OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
MATTER_955 = OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
GUARDS_3008 = OUT / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3269_SOURCE_REGISTER.csv",
    "clauses": OUT / "P8_Y5_R2FR_3269_FIXED_CONSTANTS_SUPERSELECTION_CLAUSES.csv",
    "theorem": OUT / "P8_Y5_R2FR_3269_FIXED_CONSTANTS_ZERO_THEOREM.csv",
    "coefficient_schema": OUT / "P8_Y5_R2FR_3269_COEFFICIENT_RUNNER_SCHEMA.csv",
    "candidate_inputs": OUT / "P8_Y5_R2FR_3269_COEFFICIENT_CANDIDATE_INPUTS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3269_COEFFICIENT_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3269_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3269_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3269_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3269_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3269_3268_handoff",
            DOC_3268,
            "3268 low-energy coefficient fork and next target",
            ["fixed local constants", "C_g=C_hatm=C_e=0", "NEXT3268_0_3269"],
        ),
        (
            "SRC3269_coefficients_3268",
            COEFF_3268,
            "3268 C_g/C_hatm/C_e coefficient definitions",
            ["C3268_g", "C3268_hatm", "C3268_e"],
        ),
        (
            "SRC3269_projection_3268",
            PROJ_3268,
            "3268 D=RC projection and common-mode null direction",
            ["R3268_0_Dhatm", "R3268_2_null_common_mode"],
        ),
        (
            "SRC3269_delta_matrix_3265",
            DELTA_MATRIX,
            "two-arena DD delta matrix for coefficient runner",
            ["DM3265_0_MICROSCOPE", "DM3265_1_EOTWASH"],
        ),
        (
            "SRC3269_constant_sector",
            CONST_UNIV,
            "constant-sector universality/no-running contract",
            ["C1_superselection_independence", "C4_no_constant_running_from_local_MTS", "C7_empirical_fallback"],
        ),
        (
            "SRC3269_global_superselection",
            GLOBAL_SUPER,
            "global/superselection product-sector contract",
            ["GS0_configuration_factorization", "GS2_trivial_MTS_action_on_kappa", "GS7_scalar_branch_fallback"],
        ),
        (
            "SRC3269_kappa_superselection_analogue",
            KAPPA_SUPER,
            "analogue conditional theorem for constant kappa sector",
            ["T508_0_global_sector", "T508_1_topological_zeroform"],
        ),
        (
            "SRC3269_minimal_matter",
            MATTER_955,
            "minimal matter/source-normalization lemma",
            ["MMA955_5_minimal_schema", "MMA955_6_verdict"],
        ),
        (
            "SRC3269_coupling_guards",
            GUARDS_3008,
            "direct X/material/source vertex guard rows",
            ["CG3008_1_no_direct_X_vertex", "CG3008_6_guard_verdict"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "FC3269_0_product_split",
            "required_clause": "parent configuration splits into local dynamical sector and low-energy constant sector",
            "mathematical_form": "Q_parent^loc = Q_dyn^loc x K_SM, with Lambda_3,hatm,alpha_EM functions on K_SM only",
            "current_evidence": "constant/global superselection contracts state the split but mark it not parent-derived",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FC3269_1_local_generator_tangent",
            "required_clause": "local MTS generator X is tangent to Q_dyn^loc and has zero K_SM component",
            "mathematical_form": "pi_K* X = 0, so L_X f(K_SM)=0",
            "current_evidence": "kappa theorem gives an analogue; no signed Lambda_3/hatm/alpha_EM version exists",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FC3269_2_no_direct_constant_vertices",
            "required_clause": "ordinary matter has no direct alpha_EM(X), m_A(X), q_A X.J_A, or source-only weight vertex",
            "mathematical_form": "S_matter[psi,e_obs,theta_A] with theta_A fixed representation data, not theta_A(X)",
            "current_evidence": "3008 and 955 state this as a policy/lemma contract, not a parent theorem",
            "current_status": "POLICY_OR_CONDITIONAL_LEMMA_NOT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FC3269_3_connected_no_wall_branch",
            "required_clause": "the local branch is connected and does not cross a wall where representation constants jump",
            "mathematical_form": "dK_SM=0 on connected branch; no selector/domain wall changes K_SM",
            "current_evidence": "not explicitly signed for the three DD constants",
            "current_status": "MISSING_CONNECTED_BRANCH_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "FC3269_4_residual_separation",
            "required_clause": "arena scales and omitted channels remain explicit as s_k and epsilon_k, not hidden in C",
            "mathematical_form": "eta_k=s_k DeltaQ_k dot R C + epsilon_k",
            "current_evidence": "3267/3268 derive the residual law and residual basis",
            "current_status": "DERIVED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3269_0_fixed_constants_zero",
            "statement": "If FC3269_0 through FC3269_3 hold, then C_g=C_hatm=C_e=0 on the connected local branch.",
            "proof": "Lambda_3, hatm, and alpha_EM are functions only on K_SM. X has zero K_SM component. Therefore L_X ln Lambda_3=L_X ln hatm=L_X ln alpha_EM=0.",
            "DD_implication": "D_hatm=C_hatm-C_g=0 and D_e=C_e=0",
            "result_status": "EXACT_CONDITIONAL_THEOREM",
            "current_MTS_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "THM3269_1_DD_WEP_zero_corollary",
            "statement": "Under THM3269_0 plus residual silence, the dominant DD WEP source vanishes in every material pair.",
            "proof": "eta_k=s_k DeltaQ_k dot D + epsilon_k; D=0 and epsilon_k=0 give eta_k=0 independently of s_k.",
            "DD_implication": "the two-arena DD matrix becomes a zero-source consistency check rather than a fitted channel",
            "result_status": "CONDITIONAL_ZERO_ROUTE",
            "current_MTS_status": "RESIDUAL_EPSILONS_AND_PARENT_CLAUSES_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "THM3269_2_if_clause_fails",
            "statement": "If any fixed-constant clause fails, the theory remains testable by finite coefficients C_g,C_hatm,C_e, row scales s_k, and epsilons.",
            "proof": "3268 gave D=RC; 3267 gave eta_k=s_k DeltaQ_k dot D+epsilon_k. The runner evaluates exactly this normal form.",
            "DD_implication": "failed superselection is not hidden; it becomes an executable coefficient branch",
            "result_status": "FINITE_RUNNER_FALLBACK",
            "current_MTS_status": "RUNNER_BUILT_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def coefficient_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "case_id",
            "required": "true",
            "type": "string",
            "meaning": "candidate branch identifier",
            "valid_for_claim": "false",
        },
        {
            "field": "C_g,C_hatm,C_e",
            "required": "true",
            "type": "float",
            "meaning": "parent low-energy coefficient vector in DD convention",
            "valid_for_claim": "false",
        },
        {
            "field": "s_MICROSCOPE,s_EOTWASH",
            "required": "true",
            "type": "positive float or sourced interval lower bound",
            "meaning": "arena/source/readout scale factors",
            "valid_for_claim": "false",
        },
        {
            "field": "epsilon_MICROSCOPE,epsilon_EOTWASH",
            "required": "true",
            "type": "nonnegative float",
            "meaning": "omitted-channel residual absolute budgets",
            "valid_for_claim": "false",
        },
        {
            "field": "parent_source_path",
            "required": "true for claim",
            "type": "path or theorem id",
            "meaning": "source/proof for every nonzero or zero coefficient",
            "valid_for_claim": "false",
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE3269_0_fixed_constants_zero",
            "description": "conditional fixed-local-constants zero route",
            "C_g": "0.0",
            "C_hatm": "0.0",
            "C_e": "0.0",
            "s_MICROSCOPE": "1.0",
            "s_EOTWASH": "1.0",
            "epsilon_MICROSCOPE": "0.0",
            "epsilon_EOTWASH": "0.0",
            "parent_source_path": "THM3269_0 would be source if clauses were signed",
            "input_status": "CONDITIONAL_THEOREM_SMOKE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CASE3269_1_common_mode_smoke",
            "description": "common low-energy mass-scale shift invisible to dominant DD WEP",
            "C_g": "1.0e-8",
            "C_hatm": "1.0e-8",
            "C_e": "0.0",
            "s_MICROSCOPE": "1.0",
            "s_EOTWASH": "1.0",
            "epsilon_MICROSCOPE": "0.0",
            "epsilon_EOTWASH": "0.0",
            "parent_source_path": "none; smoke case demonstrates DD null direction",
            "input_status": "NONCLAIM_SMOKE_ROUTE_TO_CLOCK_G_NEWTON",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CASE3269_2_small_nonzero_DD_smoke",
            "description": "small finite DD coefficient vector to exercise runner below both bounds",
            "C_g": "0.0",
            "C_hatm": "1.0e-13",
            "C_e": "1.0e-13",
            "s_MICROSCOPE": "1.0",
            "s_EOTWASH": "1.0",
            "epsilon_MICROSCOPE": "0.0",
            "epsilon_EOTWASH": "0.0",
            "parent_source_path": "none; numerical runner smoke only",
            "input_status": "NUMERIC_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "CASE3269_3_bad_scale_refusal",
            "description": "finite coefficients but missing positive arena scale; runner must refuse claim stability",
            "C_g": "0.0",
            "C_hatm": "1.0e-13",
            "C_e": "1.0e-13",
            "s_MICROSCOPE": "0.0",
            "s_EOTWASH": "1.0",
            "epsilon_MICROSCOPE": "0.0",
            "epsilon_EOTWASH": "0.0",
            "parent_source_path": "none; bad scale guard case",
            "input_status": "REFUSAL_CASE_BAD_SCALE",
            "valid_for_claim": "false",
        },
    ]


def delta_rows() -> list[dict[str, str]]:
    return read_csv(DELTA_MATRIX)


def runner_rows() -> list[dict[str, Any]]:
    deltas = delta_rows()
    row_by_arena = {
        "MICROSCOPE": deltas[0],
        "EOTWASH": deltas[1],
    }
    rows: list[dict[str, Any]] = []
    for row in candidate_rows():
        cg = float(row["C_g"])
        chatm = float(row["C_hatm"])
        ce = float(row["C_e"])
        d_hatm = chatm - cg
        d_e = ce
        s_micro = float(row["s_MICROSCOPE"])
        s_eot = float(row["s_EOTWASH"])
        eps_micro = float(row["epsilon_MICROSCOPE"])
        eps_eot = float(row["epsilon_EOTWASH"])
        predictions: dict[str, tuple[float, float, float, str]] = {}
        for label, delta_row in row_by_arena.items():
            s = s_micro if label == "MICROSCOPE" else s_eot
            eps = eps_micro if label == "MICROSCOPE" else eps_eot
            dqhat = float(delta_row["Delta_Qhatm_prime"])
            dqe = float(delta_row["Delta_Qe_prime"])
            bound = float(delta_row["eta_abs_bound"])
            eta_core = s * (dqhat * d_hatm + dqe * d_e)
            eta_abs_plus_eps = abs(eta_core) + eps
            status = "pass_bound" if s > 0 and eta_abs_plus_eps <= bound else "fail_or_refuse"
            predictions[label] = (eta_core, eta_abs_plus_eps, bound, status)
        row_scale_ok = s_micro > 0 and s_eot > 0
        pass_bounds = row_scale_ok and all(item[3] == "pass_bound" for item in predictions.values())
        rows.append(
            {
                "case_id": row["case_id"],
                "input_status": row["input_status"],
                "D_hatm": f"{d_hatm:.12e}",
                "D_e": f"{d_e:.12e}",
                "eta_MICROSCOPE_core": f"{predictions['MICROSCOPE'][0]:.12e}",
                "eta_MICROSCOPE_abs_plus_epsilon": f"{predictions['MICROSCOPE'][1]:.12e}",
                "eta_MICROSCOPE_bound": f"{predictions['MICROSCOPE'][2]:.12e}",
                "eta_EOTWASH_core": f"{predictions['EOTWASH'][0]:.12e}",
                "eta_EOTWASH_abs_plus_epsilon": f"{predictions['EOTWASH'][1]:.12e}",
                "eta_EOTWASH_bound": f"{predictions['EOTWASH'][2]:.12e}",
                "row_scale_ok": bool_str(row_scale_ok),
                "passes_numeric_bounds": bool_str(pass_bounds),
                "claim_status": "NONCLAIM_SMOKE" if pass_bounds else "REFUSE_OR_FAIL",
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    zero_runner = next(row for row in runner_rows() if row["case_id"] == "CASE3269_0_fixed_constants_zero")
    bad_scale = next(row for row in runner_rows() if row["case_id"] == "CASE3269_3_bad_scale_refusal")
    return [
        {
            "gate_id": "CG3269_0_conditional_zero_theorem",
            "gate": "fixed-constants DD zero theorem derived",
            "passed": "true",
            "reason": "THM3269_0 proves C_g=C_hatm=C_e=0 if product-sector clauses are signed",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3269_1_current_parent_signature",
            "gate": "constant/superselection/no-direct-vertex clauses are parent-signed in current MTS",
            "passed": "false",
            "reason": "source contracts mark them not_parent_derived, not_derived, or policy_not_parent_theorem",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3269_2_zero_runner_smoke",
            "gate": "zero candidate predicts zero eta in both arenas",
            "passed": zero_runner["passes_numeric_bounds"],
            "reason": f"eta_MICROSCOPE={zero_runner['eta_MICROSCOPE_core']}; eta_EOTWASH={zero_runner['eta_EOTWASH_core']}",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3269_3_bad_scale_refusal",
            "gate": "runner refuses zero/negative arena scales",
            "passed": bool_str(bad_scale["row_scale_ok"] == "false" and bad_scale["claim_status"] == "REFUSE_OR_FAIL"),
            "reason": "s_MICROSCOPE=0 makes source/readout normalization non-invertible",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3269_4_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "fixed constants help WEP source coupling but do not close EH reduction, source mass, PPN, clock, or residual-sector gates",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3269_0",
            "verdict": "FIXED_CONSTANTS_ZERO_THEOREM_CONDITIONAL_RUNNER_BUILT",
            "what_moved": "The DD zero route is now an exact product-sector theorem with named clauses; failed clauses fall into an executable coefficient runner.",
            "best_next": "attack the direct-vertex/no-hidden-constant clause: prove ordinary matter constants are representation data only, not MTS fields",
            "fallback_next": "fill C_parent, s_k, epsilon_k rows with real source bounds and keep branch as finite comparator",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3269_0_3270",
            "selected": "primary",
            "target_doc": "3270-Y5-R2FR-no-direct-visible-constant-vertex-or-finite-coefficient-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3270_no_direct_visible_constant_vertex_or_finite_coefficient_fill.py",
            "objective": "Try to prove ordinary matter constants are fixed representation data with no alpha_EM(X), m_A(X), source-only weight, or hidden-frame vertex; otherwise fill finite coefficient rows.",
            "guardrail": "Do not infer fixed constants from covariance alone; relative source weights and direct constant vertices are live countermodels until excluded.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = source_register()
    runners = runner_rows()
    zero = next(row for row in runners if row["case_id"] == "CASE3269_0_fixed_constants_zero")
    bad = next(row for row in runners if row["case_id"] == "CASE3269_3_bad_scale_refusal")
    no_claims = all(row["claim_allowed"] == "false" for row in promotion_gate_rows())
    validations = [
        {
            "check_id": "VAL3269_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3269_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3269_2_outputs_parse",
            "check": "all 3269 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3269_3_zero_candidate_zero_eta",
            "check": "zero candidate predicts zero eta in both arenas",
            "passed": bool_str(
                float(zero["eta_MICROSCOPE_core"]) == 0.0
                and float(zero["eta_EOTWASH_core"]) == 0.0
                and zero["passes_numeric_bounds"] == "true"
            ),
            "detail": f"{zero['eta_MICROSCOPE_core']};{zero['eta_EOTWASH_core']};passes={zero['passes_numeric_bounds']}",
        },
        {
            "check_id": "VAL3269_4_bad_scale_refused",
            "check": "bad scale candidate is refused",
            "passed": bool_str(bad["row_scale_ok"] == "false" and bad["claim_status"] == "REFUSE_OR_FAIL"),
            "detail": f"row_scale_ok={bad['row_scale_ok']};claim_status={bad['claim_status']}",
        },
        {
            "check_id": "VAL3269_5_claim_gates_false",
            "check": "no 3269 claim gate allows WEP/local-GR promotion",
            "passed": bool_str(no_claims),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3269_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3269_7_overall",
            "check": "3269 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3269_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    clauses = clause_rows()
    theorem = theorem_rows()
    schema = coefficient_schema_rows()
    candidates = candidate_rows()
    runners = runner_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    content = f"""# 3269 - Fixed local constants superselection for DD zero or coefficient runner under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3269` derives the fixed-local-constants DD zero route as an exact conditional theorem.
- If `Lambda_3`, `hatm`, and `alpha_EM` live in a parent constant sector `K_SM`, and the local MTS generator has no `K_SM` component, then `C_g=C_hatm=C_e=0`.
- That implies `D_hatm=D_e=0`, so the dominant DD WEP source is zero before explicit `epsilon_k` residuals.
- Current MTS still does **not** parent-sign the required product-sector/no-direct-vertex clauses, so no WEP/local-GR claim is promoted.
- The fallback is now executable: finite `C_parent`, `s_k`, and `epsilon_k` rows run through `eta_k=s_k DeltaQ_k dot R C + epsilon_k`.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Fixed-Constants Superselection Clauses
{md_table(clauses, ["clause_id", "required_clause", "mathematical_form", "current_evidence", "current_status", "valid_for_claim"])}

## Fixed-Constants Zero Theorem
{md_table(theorem, ["theorem_id", "statement", "proof", "DD_implication", "result_status", "current_MTS_status", "valid_for_claim"])}

## Coefficient Runner Schema
{md_table(schema, ["field", "required", "type", "meaning", "valid_for_claim"])}

## Coefficient Candidate Inputs
{md_table(candidates, ["case_id", "description", "C_g", "C_hatm", "C_e", "s_MICROSCOPE", "s_EOTWASH", "epsilon_MICROSCOPE", "epsilon_EOTWASH", "input_status", "valid_for_claim"])}

## Coefficient Runner Results
{md_table(runners, ["case_id", "input_status", "D_hatm", "D_e", "eta_MICROSCOPE_core", "eta_MICROSCOPE_abs_plus_epsilon", "eta_MICROSCOPE_bound", "eta_EOTWASH_core", "eta_EOTWASH_abs_plus_epsilon", "eta_EOTWASH_bound", "row_scale_ok", "passes_numeric_bounds", "claim_status", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register())
    write_csv(OUTPUTS["clauses"], clause_rows())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["coefficient_schema"], coefficient_schema_rows())
    write_csv(OUTPUTS["candidate_inputs"], candidate_rows())
    write_csv(OUTPUTS["runner"], runner_rows())
    write_csv(OUTPUTS["promotion"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
