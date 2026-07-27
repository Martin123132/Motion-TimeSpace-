from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_FINITE_Q_RESIDUAL_COEFFICIENT_SOURCE_OR_LOCAL_BENCHMARK_RUNNER_2284"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2284_00_2283_doc",
        "source_key": "2283_closure_finalizer",
        "source_path": ROOT / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
        "needles": [
            "FINITE_Q_RESIDUAL_ROUTE_IS_NEXT_EXECUTABLE_PATH",
            "CLOSURE_ONLY_UNTIL_FIRST_CLASS_OR_PSI_QUOTIENT_THEOREM",
            "NEXT2283_0_primary",
        ],
        "role": "handoff: q/R_AB closure-only and finite q residual route selected",
    },
    {
        "source_id": "SRC2284_01_2283_validation",
        "source_key": "2283_validation",
        "source_path": OUT / "P8_Y5_BRR545_2283_VALIDATION.csv",
        "needles": ["VAL2283_OVERALL", "PASS"],
        "role": "confirms 2283 passed before 2284 starts",
    },
    {
        "source_id": "SRC2284_02_2283_finite_intake",
        "source_key": "2283_finite_q_intake",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2283_FINITE_Q_RESIDUAL_INTAKE_CONTRACT.csv",
        "needles": ["FQI2283_0_Mq2", "MISSING_PARENT_STIFFNESS_COEFFICIENT", "FQI2283_3_Pobs"],
        "role": "machine-readable finite q residual input contract",
    },
    {
        "source_id": "SRC2284_03_2268_finite_stiffness",
        "source_key": "2268_finite_stiffness_template",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2268_FINITE_STIFFNESS_QR_ROW.csv",
        "needles": ["FSQ2268_0_algebraic_stiffness_template", "q_R=j_R/M_R^2", "SCHEMA_READY_PARENT_INPUTS_MISSING"],
        "role": "finite stiffness template and no-gradient guard seed",
    },
    {
        "source_id": "SRC2284_04_2269_stiffness_intake",
        "source_key": "2269_qR_stiffness_intake",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2269_QR_STIFFNESS_COEFFICIENT_INTAKE.csv",
        "needles": ["SCI2269_0_MR2", "SCI2269_1_jR", "SCI2269_3_no_gradient"],
        "role": "later finite q coefficient intake rows",
    },
    {
        "source_id": "SRC2284_05_2270_stiffness_source",
        "source_key": "2270_psi_stiffness_source_attempt",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2270_STIFFNESS_SOURCE_ATTEMPT.csv",
        "needles": ["SSA2270_0_MR2_pullback", "MISSING_PSI_TO_Q_PULLBACK", "SSA2270_1_jR_source"],
        "role": "psi pullback and matter q-source gaps",
    },
    {
        "source_id": "SRC2284_06_2229_ppn_requirements",
        "source_key": "2229_ppn_benchmark_requirements",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2229_PPN_BENCHMARK_REQUIREMENTS.csv",
        "needles": ["PPN2229_0_gamma", "PPN2229_6_R10", "PPN2229_7_WEP_clock"],
        "role": "closure-lane local observable requirements",
    },
    {
        "source_id": "SRC2284_07_2229_doc",
        "source_key": "2229_local_closure_benchmark",
        "source_path": ROOT / "2229-Y5-R2FR-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
        "needles": ["closure benchmark is not derivation", "Next target is a deviation budget", "source normalization"],
        "role": "benchmark policy and missing local gates",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2284_SOURCE_REGISTER.csv",
    "finite_audit": OUT / "P8_Y5_PARENT_QLOC_2284_FINITE_Q_INPUT_SOURCE_AUDIT.csv",
    "formula_ledger": OUT / "P8_Y5_PARENT_QLOC_2284_Q_RESIDUAL_FORMULA_LEDGER.csv",
    "projection_contract": OUT / "P8_Y5_PARENT_QLOC_2284_OBSERVABLE_PROJECTION_CONTRACT.csv",
    "branch_runner": OUT / "P8_Y5_PARENT_QLOC_2284_CLOSURE_VS_FINITE_BRANCH_RUNNER.csv",
    "benchmark_policy": OUT / "P8_Y5_PARENT_QLOC_2284_BENCHMARK_POLICY.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2284_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2284_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2284_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2284_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2284_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2284_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_finite_audit": (
        OUTPUTS["finite_audit"],
        QUEUE / "JR2284_FINITE_Q_INPUT_SOURCE_AUDIT_NONCLAIM.csv",
    ),
    "queue_projection_contract": (
        OUTPUTS["projection_contract"],
        QUEUE / "JR2284_OBSERVABLE_PROJECTION_CONTRACT_NONCLAIM.csv",
    ),
    "branch_wep_refusal": (
        OUTPUTS["refusal"],
        MICROSCOPE / "RAB_finite_q_residual_refusal_2284.csv",
    ),
    "beta_benchmark_policy": (
        OUTPUTS["benchmark_policy"],
        BETA_DOCS / "RAB_FINITE_Q_BENCHMARK_POLICY_2284_NONCLAIM.csv",
    ),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2284_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2284*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def finite_input_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "FQA2284_0_Mq2",
            "quantity": "M_q^2 or M_R^2",
            "required_definition": "positive algebraic q stiffness from parent action Hessian in the same normalization as J_q",
            "source_attempt": "2268 schema, 2269 coefficient intake, 2270 psi pullback attempt",
            "current_evidence": "only schema rows exist; no parent coefficient value or symbolic derivation is sourced",
            "status": "MISSING_PARENT_STIFFNESS_COEFFICIENT",
            "blocks": "finite q_R amplitude and every local prediction row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FQA2284_1_jq",
            "quantity": "j_q or j_R",
            "required_definition": "coefficient of the q-source/readout leg J_q=j_q L+O(L^2) in the same frame as M_q^2",
            "source_attempt": "2269 source intake and 2270 matter q-source map",
            "current_evidence": "matter/readout variation in q direction remains missing",
            "status": "MISSING_PARENT_SOURCE_COEFFICIENT",
            "blocks": "q_R=j_q/M_q^2 residual amplitude",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FQA2284_2_no_gradient",
            "quantity": "no-gradient/no-hair guard",
            "required_definition": "operator and boundary proof that no nabla q term or boundary q momentum generates Q_R/r hair",
            "source_attempt": "2268 no-gradient guard and 2269 operator inventory row",
            "current_evidence": "operator inventory is absent; if a gradient term exists the branch needs a Yukawa/hair projection instead",
            "status": "MISSING_OPERATOR_BOUNDARY_INVENTORY",
            "blocks": "PPN, R10, clock, and orbital residual envelope",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FQA2284_3_Pobs",
            "quantity": "P_obs projection matrix",
            "required_definition": "linearized observable map from q_R and any hair/range parameters into gamma, beta, R10, clocks, orbital residuals",
            "source_attempt": "2229 PPN benchmark requirements plus 2283 finite residual intake",
            "current_evidence": "arena list exists but no sourced projection coefficients exist",
            "status": "MISSING_OBSERVABLE_PROJECTION",
            "blocks": "empirical local robustness pass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FQA2284_4_source_norm",
            "quantity": "Newton/source normalization",
            "required_definition": "worldtube/Hilbert mass equality or explicit source-normalization residual rows so fitted GM does not hide q effects",
            "source_attempt": "2229 missing local gates and 2283 finite residual intake",
            "current_evidence": "source bridge remains listed as missing",
            "status": "MISSING_SOURCE_NORMALIZATION_THEOREM",
            "blocks": "Newton mechanics derivation and orbital/PPN normalization",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FQA2284_5_bounds",
            "quantity": "external local bounds",
            "required_definition": "PPN/R10/clocks/orbital bounds used only as comparators after parent coefficients are sourced",
            "source_attempt": "2229 local observable requirements",
            "current_evidence": "bounds can be acquired later but cannot supply M_q^2, j_q, or q_R",
            "status": "COMPARATOR_ONLY_NOT_THEORY_INPUT",
            "blocks": "claim eligibility until theory coefficients exist",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def formula_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "QRF2284_0_algebraic_parent_block",
            "branch": "finite_nonpropagating_q",
            "formula": "L_q=-1/2 M_q^2 q^2 + J_q q",
            "variation_or_limit": "M_q^2 q = J_q",
            "weak_field_residual": "if J_q=j_q L+O(L^2), then q=q_R L+O(L^2) with q_R=j_q/M_q^2",
            "required_inputs": "M_q^2;j_q;normalization;units;source path",
            "status": "FORMULA_SCHEMA_READY_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "formula_id": "QRF2284_1_gradient_branch",
            "branch": "finite_range_or_hair_q",
            "formula": "L_q=-1/2 Z_q (nabla q)^2 -1/2 M_q^2 q^2 + J_q q plus boundary terms",
            "variation_or_limit": "Z_q box q - M_q^2 q + J_q = 0, with possible boundary charge",
            "weak_field_residual": "range lambda_q=sqrt(Z_q/M_q^2) or Q_R/r hair must be projected separately",
            "required_inputs": "Z_q;M_q^2;j_q;boundary charge;arena Green function",
            "status": "NOT_SCORE_READY_OPERATOR_INVENTORY_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "formula_id": "QRF2284_2_closure_benchmark",
            "branch": "explicit_closure_control",
            "formula": "q=0 equivalent to R_AB=0 equivalent to J_q=T sqrt(S)=1",
            "variation_or_limit": "allowed only as assumed closure benchmark after 2283 finalizer",
            "weak_field_residual": "gamma=1 inside closure lane only; beta=1 remains benchmark control",
            "required_inputs": "explicit closure label and no parent-derivation claim",
            "status": "CLOSURE_BENCHMARK_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "formula_id": "QRF2284_3_source_norm_guard",
            "branch": "Newton_orbital_normalization",
            "formula": "observed GM must be tied to the same source charge that enters L and q-source rows",
            "variation_or_limit": "otherwise fitted GM can absorb part of q_R and fake a local pass",
            "weak_field_residual": "source-normalization residual must be carried as its own channel",
            "required_inputs": "worldtube/Hilbert equality or explicit delta_GM row",
            "status": "MISSING_SOURCE_NORMALIZATION_THEOREM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def projection_contract_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "POB2284_0_gamma",
            "PPN gamma_minus_1",
            "dimensionless",
            "linear coefficient C_gamma_q in gamma-1 = C_gamma_q q_R + C_gamma_hair Q_R + ...",
            "Cassini/local gamma bound",
            "MISSING_C_GAMMA_AND_QR",
        ),
        (
            "POB2284_1_beta",
            "PPN beta_minus_1",
            "dimensionless",
            "second-order coefficient C_beta_q in beta-1 = C_beta_q q_R + C_beta_2 q_R^2 + ...",
            "perihelion/range/PPN beta bounds",
            "MISSING_SECOND_ORDER_SOURCE_CLOSURE",
        ),
        (
            "POB2284_2_R10",
            "short-range alpha(lambda)",
            "dimensionless curve",
            "map finite q range or hair into Yukawa-like alpha(lambda) only after Z_q,M_q^2,j_q are sourced",
            "R10/Eot-Wash comparator curve",
            "MISSING_RANGE_AND_COUPLING_MAP",
        ),
        (
            "POB2284_3_clocks",
            "clock/redshift residual",
            "dimensionless or fractional frequency",
            "coframe/matter descent coefficient C_clock_q times q_R plus source-normalization residual",
            "clock/redshift/local position invariance tests",
            "MISSING_MATTER_COFRAME_DESCENT",
        ),
        (
            "POB2284_4_orbital",
            "orbital residuals",
            "arena specific",
            "map q_R and delta_GM into perihelion, ranging, and acceleration residuals",
            "solar-system/orbital comparators",
            "MISSING_SOURCE_NORMALIZATION_AND_BETA_MAP",
        ),
        (
            "POB2284_5_Gdot",
            "Gdot/G or source drift",
            "yr^-1",
            "stationarity or drift law for the source-normalization channel",
            "lunar laser/ranging/pulsar-style comparators",
            "MISSING_SOURCE_STATIONARITY_THEOREM",
        ),
        (
            "POB2284_6_WEP",
            "WEP/matter-universality residual",
            "dimensionless",
            "composition-dependent q-coupling coefficients must vanish or be bounded",
            "MICROSCOPE/Eotvos comparators",
            "MISSING_UNIVERSAL_MATTER_COUPLING",
        ),
    ]
    return [
        {
            "projection_id": projection_id,
            "observable": observable,
            "units": units,
            "required_projection": required_projection,
            "comparator_arena": comparator_arena,
            "current_status": current_status,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for projection_id, observable, units, required_projection, comparator_arena, current_status in entries
    ]


def branch_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2284_0_closure_branch",
            "branch": "explicit_q_zero_closure_benchmark",
            "inputs": "q=0/R_AB=0 imposed as closure; no finite q coefficients required",
            "allowed_output": "GR-lane control values and regression benchmarks only",
            "blocked_output": "derived local-GR/Newton claim",
            "current_status": "RUNNABLE_BENCHMARK_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN2284_1_algebraic_finite_q",
            "branch": "finite_nonpropagating_q_residual",
            "inputs": "M_q^2, j_q, units, q_R=j_q/M_q^2, P_obs, source normalization",
            "allowed_output": "arena residual predictions after all parent inputs are sourced",
            "blocked_output": "any local pass/fail score before parent coefficients and projection matrix exist",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN2284_2_gradient_or_hair_q",
            "branch": "finite_range_or_boundary_hair_q",
            "inputs": "Z_q, M_q^2, j_q, boundary charge, range/hair projection",
            "allowed_output": "R10/PPN/orbital residual envelope once operator inventory is sourced",
            "blocked_output": "hiding Q_R/r hair inside q=0 closure",
            "current_status": "BLOCKED_OPERATOR_BOUNDARY_INVENTORY_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN2284_3_comparator_bounds",
            "branch": "external_local_bounds",
            "inputs": "published local bounds plus sourced parent predictions",
            "allowed_output": "screen abs(prediction) <= bound after coefficients exist",
            "blocked_output": "using bounds to define M_q^2, j_q, or q_R",
            "current_status": "COMPARATOR_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def benchmark_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "POL2284_0_label_closure",
            "rule": "Every q=0/R_AB=0 run must be labelled explicit closure benchmark.",
            "reason": "2283 finalized the parent selector as closure-only until a new theorem appears.",
            "allowed": True,
            "forbidden": "advertise as derived local GR/Newton",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2284_1_separate_finite_branch",
            "rule": "Finite q residual rows must be kept separate from closure controls.",
            "reason": "q physical residuals need coefficients and observable projection, not closure rhetoric.",
            "allowed": True,
            "forbidden": "merge finite residuals into the q=0 branch",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2284_2_no_bounds_as_coefficients",
            "rule": "Experimental local bounds are comparators only and cannot define M_q^2, j_q, q_R, Z_q, or Q_R.",
            "reason": "a theory predicts residuals first; experiments screen them second.",
            "allowed": False,
            "forbidden": "fit parent coefficients from bounds and call them derived",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2284_3_no_GR_import",
            "rule": "Do not import Schwarzschild AB=1 or Einstein vacuum as the selector proof.",
            "reason": "that tests consistency with GR but does not derive the MTS parent action.",
            "allowed": False,
            "forbidden": "use GR as the non-circular q=0 theorem",
            "valid_for_claim": False,
        },
        {
            "policy_id": "POL2284_4_source_norm_separate",
            "rule": "Carry source normalization as an explicit channel until worldtube/Hilbert equality is proven.",
            "reason": "otherwise measured GM may hide finite q effects.",
            "allowed": True,
            "forbidden": "silently absorb residuals into fitted Newtonian mass",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2284_0_sources_backed",
            "claim": "2284 is source-backed as a nonclaim checkpoint",
            "gate_pass": True,
            "reason": "source register cites 2283, 2268, 2269, 2270, and 2229 ledgers",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2284_1_finite_coefficients_sourced",
            "claim": "M_q^2 and j_q are parent-sourced",
            "gate_pass": False,
            "reason": "only schema/input rows exist; parent Hessian and matter q-source remain missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2284_2_no_gradient_guard",
            "claim": "no-gradient/no-hair theorem is proven",
            "gate_pass": False,
            "reason": "operator and boundary inventory remains missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2284_3_projection_matrix",
            "claim": "P_obs maps q_R into local observables",
            "gate_pass": False,
            "reason": "projection contract is written but coefficients are not sourced",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2284_4_source_normalization",
            "claim": "Newton/source normalization is derived",
            "gate_pass": False,
            "reason": "worldtube/Hilbert source equality or explicit residual source channel is still missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2284_5_local_gr_newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "reason": "closure branch is nonclaim and finite residual branch is input-blocked",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2284_0_claim_q_zero_derived",
            "attempted_claim": "q=0/R_AB=0 is derived local GR",
            "runner_result": "REFUSED_CLOSURE_ONLY",
            "blocked_by": "2283 finalizer: no current parent owner for J_q=1",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2284_1_score_finite_q",
            "attempted_claim": "finite q residual branch can be locally scored now",
            "runner_result": "REFUSED_INPUTS_MISSING",
            "blocked_by": "M_q^2, j_q, no-gradient guard, P_obs, and source normalization are missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2284_2_use_bound_as_theory",
            "attempted_claim": "local bounds can set q_R or M_q^2",
            "runner_result": "REFUSED_COMPARATOR_NOT_COEFFICIENT",
            "blocked_by": "benchmark policy forbids experimental bounds as parent coefficients",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2284_3_ignore_hair",
            "attempted_claim": "gradient or boundary q hair can be ignored",
            "runner_result": "REFUSED_OPERATOR_INVENTORY_MISSING",
            "blocked_by": "no-gradient/no-hair guard is not proven",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2284_0_route",
            "decision": "FINITE_Q_RESIDUAL_ROUTE_IS_THE_NEXT_TESTABLE_LOCAL_PATH",
            "reason": "q=0 is closure-only; finite q can become predictive if coefficients and projections are sourced",
            "next_action": "build source/projection pack instead of relitigating the same q=0 proof shortcuts",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2284_1_current_result",
            "decision": "NO_LOCAL_GR_CLAIM_FROM_2284",
            "reason": "M_q^2, j_q, no-gradient guard, P_obs, and source normalization are still missing",
            "next_action": "carry all rows as nonclaim until sourced",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2284_2_benchmark",
            "decision": "CLOSURE_BENCHMARK_REMAINS_USEFUL_BUT_NOT_DERIVATION",
            "reason": "it checks whether the rest of the framework lands on the GR lane once q is explicitly closed",
            "next_action": "keep it as a regression control alongside finite residual tests",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2284_3_next",
            "decision": "BUILD_FINITE_Q_PROJECTION_MATRIX_OR_INPUT_SOURCE_PACK_NEXT",
            "reason": "the next leap is to connect q_R/hair/range/source-normalization channels to actual local observables",
            "next_action": "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2284_0_primary",
            "next_target": "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md",
            "script": "scripts/Y5_R2FR_finite_q_PPN_R10_projection_matrix_or_input_source_pack_2285.py",
            "objective": "derive or source the P_obs projection matrix for q_R, Q_R hair, finite range, source normalization, clocks, PPN, R10, and orbital residuals; otherwise leave a source-ready acquisition pack with claims blocked",
            "selection_status": "selected",
            "success_condition": "either the finite q local residual matrix becomes source-backed nonclaim-ready, or every missing coefficient/projection is explicitly queued with no local-GR/Newton claim",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
        "claim_allowed",
        "score_eligible",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for finite q residual local benchmark intake",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    finite_rows = read_csv(OUTPUTS["finite_audit"])
    formula_rows = read_csv(OUTPUTS["formula_ledger"])
    projection_rows = read_csv(OUTPUTS["projection_contract"])
    runner_rows = read_csv(OUTPUTS["branch_runner"])
    policy_rows = read_csv(OUTPUTS["benchmark_policy"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    refusal_runner_rows = read_csv(OUTPUTS["refusal"])
    decision_ledger_rows = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    checks = [
        (
            "VAL2284_0_sources_exist",
            all(row["exists"] == "True" for row in source_rows),
            "all cited source paths exist",
        ),
        (
            "VAL2284_1_needles_present",
            all(row["needles_present"] == "True" for row in source_rows),
            "all cited source needles are present",
        ),
        (
            "VAL2284_2_prior_validation",
            validation_pass(OUT / "P8_Y5_BRR545_2283_VALIDATION.csv"),
            "2283 validation passes before 2284",
        ),
        (
            "VAL2284_3_missing_inputs_preserved",
            all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in finite_rows)
            and any("MISSING_PARENT_STIFFNESS_COEFFICIENT" in row["status"] for row in finite_rows)
            and any("MISSING_OBSERVABLE_PROJECTION" in row["status"] for row in finite_rows),
            "finite input rows remain missing/nonclaim until sourced",
        ),
        (
            "VAL2284_4_formula_ratio_present",
            any("q_R=j_q/M_q^2" in row["weak_field_residual"] for row in formula_rows),
            "formula ledger records the finite algebraic residual ratio",
        ),
        (
            "VAL2284_5_gradient_guard_present",
            any("gradient" in row["branch"] or "hair" in row["branch"] for row in formula_rows),
            "formula ledger carries gradient/hair guard rather than ignoring it",
        ),
        (
            "VAL2284_6_projection_contract_complete",
            {row["observable"] for row in projection_rows}
            >= {
                "PPN gamma_minus_1",
                "PPN beta_minus_1",
                "short-range alpha(lambda)",
                "clock/redshift residual",
                "orbital residuals",
                "Gdot/G or source drift",
                "WEP/matter-universality residual",
            },
            "projection contract covers PPN, R10, clocks, orbital, Gdot/source, and WEP",
        ),
        (
            "VAL2284_7_closure_branch_labelled",
            any(
                row["branch"] == "explicit_q_zero_closure_benchmark"
                and "derived local-GR/Newton claim" in row["blocked_output"]
                for row in runner_rows
            ),
            "q=0 branch is labelled closure benchmark and blocks derivation claims",
        ),
        (
            "VAL2284_8_finite_branch_blocked",
            any(row["branch"] == "finite_nonpropagating_q_residual" and row["current_status"] == "BLOCKED_INPUTS_MISSING" for row in runner_rows),
            "finite residual branch is not score-ready while inputs are missing",
        ),
        (
            "VAL2284_9_no_bounds_as_coefficients",
            any("cannot define M_q^2" in row["rule"] for row in policy_rows)
            and any("REFUSED_COMPARATOR_NOT_COEFFICIENT" in row["runner_result"] for row in refusal_runner_rows),
            "external bounds are comparator-only, never theory coefficients",
        ),
        (
            "VAL2284_10_local_claim_blocked",
            any(row["claim_id"] == "CG2284_5_local_gr_newton" and row["gate_pass"] == "False" for row in gate_rows),
            "local GR/Newton claim remains blocked",
        ),
        (
            "VAL2284_11_next_selected",
            any(row["next_target"] == "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md" for row in next_rows),
            "2285 projection/source-pack target selected",
        ),
        (
            "VAL2284_12_csv_parse",
            all(csv_parses(path) for path in all_generated_before_validation),
            "all generated 2284 CSVs parse before validation file",
        ),
        (
            "VAL2284_13_no_claim_flags",
            generated_claim_flags_false(all_generated_before_validation),
            "all generated claim/score flags remain false",
        ),
        (
            "VAL2284_14_branch_copies",
            all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows),
            "branch/queue copies exist and parse",
        ),
        (
            "VAL2284_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        ),
        (
            "VAL2284_16_formalization_no_2284",
            not formalization_has_2284_artifacts(),
            "formalization-workbench has no non-venv 2284 artifacts",
        ),
        (
            "VAL2284_17_formalization_untouched",
            not formalization_touched_since_start(),
            "formalization-workbench untouched during 2284 run",
        ),
        (
            "VAL2284_18_decision_nonclaim",
            any(row["decision"] == "NO_LOCAL_GR_CLAIM_FROM_2284" for row in decision_ledger_rows),
            "decision ledger keeps 2284 nonclaim",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2284_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2284 converts q-closure failure into a finite-q residual coefficient/projection runner while keeping local GR/Newton claims blocked",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    finite_audit: list[dict[str, Any]],
    formula_ledger: list[dict[str, Any]],
    projection_contract: list[dict[str, Any]],
    branch_runner: list[dict[str, Any]],
    benchmark_policy: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2284 - Y5/R2FR Finite q Residual Coefficient Source Or Local Benchmark Runner

## Verdict

This checkpoint stops trying to smuggle a derived local-GR result out of the unresolved `q=0/R_AB=0` route. After 2283, that lane is an explicit closure benchmark only.

The serious next path is finite residual physics. The minimal algebraic branch is

`L_q=-1/2 M_q^2 q^2 + J_q q`, with `J_q=j_q L+O(L^2)`, so `q=q_R L+O(L^2)` and `q_R=j_q/M_q^2`.

That formula is useful but not yet a prediction. The parent action still has to supply `M_q^2`, `j_q`, a no-gradient/no-hair guard or range/hair branch, the observable projection `P_obs`, and Newton/source normalization. Until then, local GR/Newton recovery remains blocked and all local tests are comparator contracts rather than claim rows.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Finite q Input Source Audit
{table(["input_id", "quantity", "required_definition", "source_attempt", "current_evidence", "status", "blocks", "score_ready", "valid_for_claim"], finite_audit)}

## q Residual Formula Ledger
{table(["formula_id", "branch", "formula", "variation_or_limit", "weak_field_residual", "required_inputs", "status", "score_ready", "valid_for_claim"], formula_ledger)}

## Observable Projection Contract
{table(["projection_id", "observable", "units", "required_projection", "comparator_arena", "current_status", "score_ready", "valid_for_claim"], projection_contract)}

## Closure vs Finite Branch Runner
{table(["runner_id", "branch", "inputs", "allowed_output", "blocked_output", "current_status", "score_ready", "valid_for_claim"], branch_runner)}

## Benchmark Policy
{table(["policy_id", "rule", "reason", "allowed", "forbidden", "valid_for_claim"], benchmark_policy)}

## Claim Gates
{table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claim_gates)}

## Refusal Runner
{table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is actually a forward move, not a retreat. The old proof route is closed unless a genuinely new parent theorem appears. The finite-`q` route gives us something harder and cleaner: derive the missing coefficients, project them into actual local observables, and let the local tests judge the residuals. That is the route with less hand-waving and more physics.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    source_register = source_register_rows()
    finite_audit = finite_input_audit_rows()
    formula_ledger = formula_ledger_rows()
    projection_contract = projection_contract_rows()
    branch_runner = branch_runner_rows()
    benchmark_policy = benchmark_policy_rows()
    claim_gates = claim_gate_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_register)
    write_csv(OUTPUTS["finite_audit"], finite_audit)
    write_csv(OUTPUTS["formula_ledger"], formula_ledger)
    write_csv(OUTPUTS["projection_contract"], projection_contract)
    write_csv(OUTPUTS["branch_runner"], branch_runner)
    write_csv(OUTPUTS["benchmark_policy"], benchmark_policy)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["finite_audit"],
        OUTPUTS["formula_ledger"],
        OUTPUTS["projection_contract"],
        OUTPUTS["branch_runner"],
        OUTPUTS["benchmark_policy"],
        OUTPUTS["claim_gates"],
        OUTPUTS["refusal"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        source_register,
        finite_audit,
        formula_ledger,
        projection_contract,
        branch_runner,
        benchmark_policy,
        claim_gates,
        refusal,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2284 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
