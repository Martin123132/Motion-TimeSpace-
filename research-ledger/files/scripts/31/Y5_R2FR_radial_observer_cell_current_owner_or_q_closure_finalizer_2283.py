from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_RADIAL_CELL_OWNER_OR_Q_CLOSURE_FINALIZER_2283"
DOC = ROOT / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2283_00_2282_doc",
        "source_key": "2282_doc",
        "source_path": ROOT / "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
        "needles": ["NEXT2282_0_primary", "Q_ZERO_IDENTIFIED_WITH_RADIAL_OBSERVER_CELL_RECIPROCITY", "DISCIPLINED_CLOSURE"],
        "role": "handoff selecting radial-cell owner or q closure finalizer",
    },
    {
        "source_id": "SRC2283_01_2282_validation",
        "source_key": "2282_validation",
        "source_path": OUT / "P8_Y5_BRR545_2282_VALIDATION.csv",
        "needles": ["VAL2282_OVERALL", "PASS"],
        "role": "confirms 2282 passed before 2283 starts",
    },
    {
        "source_id": "SRC2283_02_2282_inputs",
        "source_key": "2282_parent_inputs",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2282_PARENT_SELECTOR_INPUT_CONTRACT.csv",
        "needles": ["PIC2282_0_cell_current", "MISSING_PARENT_CURRENT", "MISSING_SOURCE_NORMALIZATION_THEOREM"],
        "role": "machine-readable missing selector inputs",
    },
    {
        "source_id": "SRC2283_03_cell_current_11",
        "source_key": "11_cell_current",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["cell_current_origin_no_charge_obstruction", "Q_R = constant", "ordinary cell-current conservation"],
        "role": "ordinary cell-current route and no-charge obstruction",
    },
    {
        "source_id": "SRC2283_04_constraint_07",
        "source_key": "07_nonprop_constraint",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["nonpropagating_reciprocity_constraint_clean_but_parent_origin_open", "S_constraint = integral lambda_R R_AB", "why does the parent motion-load action contain lambda_R ln(T^2 S)?"],
        "role": "clean multiplier constraint but parent origin open",
    },
    {
        "source_id": "SRC2283_05_lambdaR_2267",
        "source_key": "2267_lambdaR",
        "source_path": ROOT / "2267-Y5-R2FR-RAB-lambdaR-origin-or-backreaction-elimination.md",
        "needles": ["POSTHOC_MULTIPLIER_REJECTED_AS_STANDALONE_DERIVATION", "lambda_R D_A R_AB", "REDUCED_CONFIGURATION_OR_QUOTIENT_IS_BEST_ROUTE"],
        "role": "post-hoc multiplier backreaction and reduced-configuration escape",
    },
    {
        "source_id": "SRC2283_06_reduced_2268",
        "source_key": "2268_reduced_config",
        "source_path": ROOT / "2268-Y5-R2FR-RAB-reduced-configuration-parametrization-or-finite-stiffness-row.md",
        "needles": ["REDUCED_CONFIGURATION_NOT_DERIVED_CURRENT_CORPUS", "FINITE_STIFFNESS_QR_SCHEMA_OPENED", "J_q=T sqrt(S)=sqrt(AB)=exp(q/2)"],
        "role": "reduced configuration seed and finite stiffness fallback",
    },
    {
        "source_id": "SRC2283_07_radial_2269",
        "source_key": "2269_radial_cell",
        "source_path": ROOT / "2269-Y5-R2FR-radial-cell-conservation-theorem-or-qR-stiffness-coefficient.md",
        "needles": ["RADIAL_CELL_THEOREM_NOT_DERIVED_CURRENT_CORPUS", "REJECTED_NO_CHARGE_OBSTRUCTION", "M_R^2"],
        "role": "direct radial-cell theorem failure and finite coefficient intake",
    },
    {
        "source_id": "SRC2283_08_gauge_2228",
        "source_key": "2228_gauge_noether",
        "source_path": ROOT / "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md",
        "needles": ["NO_ACCEPTED_ZERO_CHARGE_ORIGIN", "FIRST_CLASS_CONTRACT_ONLY", "R_AB=0 may be used only as explicit benchmark closure"],
        "role": "gauge/Noether shortcuts rejected; first-class contract only",
    },
    {
        "source_id": "SRC2283_09_psi_2270",
        "source_key": "2270_psi_quotient",
        "source_path": ROOT / "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md",
        "needles": ["PSI_QUOTIENT_NOT_CLOSED", "q is the temporal/radial covariance mismatch", "MISSING_STIFFNESS_PULLBACK"],
        "role": "primitive psi quotient route and finite stiffness inputs not closed",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2283_SOURCE_REGISTER.csv",
    "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2283_RADIAL_CELL_OWNER_AUDIT.csv",
    "closure_finalizer": OUT / "P8_Y5_PARENT_QLOC_2283_Q_CLOSURE_FINALIZER.csv",
    "finite_intake": OUT / "P8_Y5_PARENT_QLOC_2283_FINITE_Q_RESIDUAL_INTAKE_CONTRACT.csv",
    "benchmark_rules": OUT / "P8_Y5_PARENT_QLOC_2283_LOCAL_BENCHMARK_RULES.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2283_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2283_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2283_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2283_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2283_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2283_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_owner": QUEUE / "JR2283_RADIAL_CELL_OWNER_AUDIT_NONCLAIM.csv",
    "queue_finite": QUEUE / "JR2283_FINITE_Q_RESIDUAL_INTAKE_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_radial_cell_owner_closure_refusal_2283.csv",
    "beta_docs": BETA_DOCS / "RAB_Q_CLOSURE_FINALIZER_2283_NONCLAIM.csv",
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
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


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
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "RCO2283_0_identity",
            "candidate_owner": "exact identity",
            "test": "J_q=T sqrt(S)=exp(q/2), so J_q=1 iff q=0 iff R_AB=0",
            "result": "IDENTIFIES_TARGET_ONLY",
            "failure_or_gap": "identity is not a parent law selecting the target",
            "final_status": "NONCLAIM_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_1_ordinary_current",
            "candidate_owner": "conserved radial cell current",
            "test": "partial_r(W partial_r R_AB)=0 gives W R_AB'=Q_R",
            "result": "REJECTED_NO_CHARGE_OBSTRUCTION",
            "failure_or_gap": "conservation makes Q_R constant, not zero; exterior R_AB=-Q_R/r hair survives",
            "final_status": "NOT_OWNER",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_2_topological_zero_charge",
            "candidate_owner": "topological/no-charge theorem",
            "test": "Q_R=int rho_R=0 by source representation or cohomology",
            "result": "POSSIBLE_BUT_UNSUPPLIED",
            "failure_or_gap": "no parent source representation, cohomology class, or boundary theorem sets Q_R=0",
            "final_status": "FUTURE_CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_3_posthoc_multiplier",
            "candidate_owner": "lambda_R R_AB added after variables are physical",
            "test": "delta_Y S contains lambda_R D_Y R_AB",
            "result": "REJECTED_BACKREACTION",
            "failure_or_gap": "post-hoc multiplier enforces the constraint but changes the physical equations unless escape gates close",
            "final_status": "NOT_STANDALONE_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_4_first_class_constraint",
            "candidate_owner": "first-class reciprocal constraint",
            "test": "C_R=R_AB with differentiable generator, zero/proper boundary charge, bracket closure, degree count, matter descent",
            "result": "VIABLE_IN_PRINCIPLE_NOT_PRESENT",
            "failure_or_gap": "parent phase space/generator/boundary charge/bracket/degree count/matter map are missing",
            "final_status": "PROMOTION_CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_5_reduced_configuration",
            "candidate_owner": "pre-variation reduced configuration",
            "test": "A=exp(2Phi), B=exp(-2Phi), q=0 before variation",
            "result": "BEST_SEED_NOT_DERIVED",
            "failure_or_gap": "avoids multiplier backreaction but parent reason q is absent/frozen is missing",
            "final_status": "CONDITIONAL_SEED_ONLY",
            "valid_for_claim": False,
        },
        {
            "owner_id": "RCO2283_6_psi_quotient",
            "candidate_owner": "psi covariance quotient or vertical q",
            "test": "psi->C_munu->(Phi,q) map makes q absent, vertical, or minimized",
            "result": "NOT_CLOSED",
            "failure_or_gap": "current psi action gives covariance ansatz but no temporal/radial channel relation or q Hessian/source leg",
            "final_status": "ROOT_ROUTE_OPEN_NOT_AVAILABLE",
            "valid_for_claim": False,
        },
    ]


def closure_finalizer_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "QCF2283_0_finalizer",
            "item": "q/R_AB local selector",
            "final_status": "CLOSURE_ONLY_UNTIL_FIRST_CLASS_OR_PSI_QUOTIENT_THEOREM",
            "reason": "all current owner routes are rejected, contract-only, or conditional seeds",
            "allowed_use": "private benchmark, residual bookkeeping, finite residual coefficient intake",
            "forbidden_use": "derived local-GR/Newton/PPN claim",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCF2283_1_benchmark",
            "item": "R_AB=0 / J_q=1 benchmark",
            "final_status": "ALLOWED_AS_EXPLICIT_ASSUMED_CLOSURE",
            "reason": "useful for checking whether the rest of the framework lands on the GR lane under the closure",
            "allowed_use": "gamma/beta/conservation/matter-universality benchmark ledgers",
            "forbidden_use": "advertise as parent derivation",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCF2283_2_finite_branch",
            "item": "finite q residual branch",
            "final_status": "PROMOTED_TO_NEXT_EXECUTABLE_NONCLAIM_ROUTE",
            "reason": "if q is physical rather than killed, the theory must source and bound q_R instead of hiding it",
            "allowed_use": "derive/source M_R^2, j_R, no-gradient guard, P_obs, then compare to local tests",
            "forbidden_use": "use experimental bounds as theory coefficients",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCF2283_3_reentry",
            "item": "future derivation re-entry",
            "final_status": "REENTRY_CONTRACT_RETAINED",
            "reason": "a real first-class constraint/no-charge theorem or psi quotient can reopen the derived local-GR branch",
            "allowed_use": "future proof work if new parent-action evidence appears",
            "forbidden_use": "looping the same current/multiplier/gauge shortcuts without new input",
            "valid_for_claim": False,
        },
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "FQI2283_0_Mq2",
            "quantity": "M_q^2 or M_R^2",
            "required_definition": "positive algebraic/transverse q stiffness from parent action Hessian in same normalization as q source",
            "current_status": "MISSING_PARENT_STIFFNESS_COEFFICIENT",
            "blocks": "finite q_R=q source/stiffness value",
            "valid_for_claim": False,
        },
        {
            "input_id": "FQI2283_1_jq",
            "quantity": "j_q or j_R",
            "required_definition": "first q-source/readout leg J_q=j_q L+O(L^2) or equivalent same-frame source coefficient",
            "current_status": "MISSING_PARENT_SOURCE_COEFFICIENT",
            "blocks": "finite q_R residual amplitude",
            "valid_for_claim": False,
        },
        {
            "input_id": "FQI2283_2_no_gradient",
            "quantity": "no-gradient/no-hair guard",
            "required_definition": "prove no nabla q boundary momentum generates Q_R/r hair, or bound that hair separately",
            "current_status": "MISSING_OPERATOR_BOUNDARY_INVENTORY",
            "blocks": "local PPN/R10 residual envelope",
            "valid_for_claim": False,
        },
        {
            "input_id": "FQI2283_3_Pobs",
            "quantity": "observable projection P_obs",
            "required_definition": "map q_R into gamma-1, beta-1, Gdot/source normalization, R10 alpha(lambda), clocks, orbital residuals",
            "current_status": "MISSING_OBSERVABLE_PROJECTION",
            "blocks": "empirical robustness pass",
            "valid_for_claim": False,
        },
        {
            "input_id": "FQI2283_4_source_norm",
            "quantity": "Newton/source normalization",
            "required_definition": "worldtube/Hilbert mass equality or explicit residual rows so fitted G does not hide q effects",
            "current_status": "MISSING_SOURCE_NORMALIZATION_THEOREM",
            "blocks": "Newton mechanics derivation",
            "valid_for_claim": False,
        },
        {
            "input_id": "FQI2283_5_comparator_bounds",
            "quantity": "local experimental bounds",
            "required_definition": "PPN/R10/clocks/orbital bounds may only screen sourced q residuals, not define them",
            "current_status": "COMPARATOR_ONLY",
            "blocks": "claim eligibility until theory coefficients exist",
            "valid_for_claim": False,
        },
    ]


def benchmark_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "LBR2283_0_label",
            "rule": "Any run using R_AB=0/J_q=1 must be labelled closure benchmark.",
            "reason": "owner theorem is not derived",
            "allowed": True,
            "valid_for_claim": False,
        },
        {
            "rule_id": "LBR2283_1_derived_vs_assumed",
            "rule": "Tables must separate derived identities, assumed closure conditions, and externally tested residuals.",
            "reason": "avoid converting algebraic equivalence into a physics proof",
            "allowed": True,
            "valid_for_claim": False,
        },
        {
            "rule_id": "LBR2283_2_no_bound_as_coefficient",
            "rule": "Never use PPN/R10/clock bounds as M_q^2, j_q, or q_R values.",
            "reason": "bounds screen a theory prediction; they are not the parent theory",
            "allowed": False,
            "valid_for_claim": False,
        },
        {
            "rule_id": "LBR2283_3_no_GR_import",
            "rule": "Do not use Schwarzschild AB=1 or Einstein vacuum as the non-circular selector proof.",
            "reason": "that is a consistency check unless EH was independently derived",
            "allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2283_0_owner_exhaustion",
            "claim": "current/constraint/gauge/psi owner routes have been audited",
            "gate_pass": True,
            "reason": "source-backed owner audit records current hair, multiplier backreaction, first-class missing contract, reduced seed, and psi quotient gap",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2283_1_parent_owner",
            "claim": "J_q=1 has a non-circular parent owner in the current corpus",
            "gate_pass": False,
            "reason": "no current no-charge theorem, first-class generator, harmless multiplier, reduced-configuration origin, or psi quotient proof is supplied",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2283_2_closure_finalized",
            "claim": "q/R_AB sector is finalized as closure-only until new theorem input",
            "gate_pass": True,
            "reason": "closure ledger states allowed and forbidden uses",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2283_3_finite_route_ready",
            "claim": "finite residual route has a clear input contract",
            "gate_pass": True,
            "reason": "M_q^2, j_q, no-gradient guard, P_obs, source normalization and comparator rules are listed",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2283_4_local_gr_newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "reason": "local selector is closure-only and finite q residual coefficients/source normalization are missing",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2283_0_current_owner",
            "attempted_claim": "ordinary radial-cell current conservation derives J_q=1",
            "runner_result": "REJECTED_NO_CHARGE_OBSTRUCTION",
            "blocked_by": "Q_R constant/hair survives without a parent zero-charge theorem",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2283_1_multiplier_owner",
            "attempted_claim": "lambda_R R_AB post-hoc multiplier derives local GR",
            "runner_result": "REJECTED_BACKREACTION",
            "blocked_by": "lambda_R D_A R_AB modifies physical equations unless escape gates close",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2283_2_gauge_owner",
            "attempted_claim": "gauge/Noether shortcut sets R_AB=0",
            "runner_result": "BLOCKED_CONTRACT_ONLY",
            "blocked_by": "first-class phase space/generator/boundary charge/bracket/degree count/matter map missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2283_3_psi_owner",
            "attempted_claim": "psi covariance map makes q absent/vertical",
            "runner_result": "BLOCKED",
            "blocked_by": "temporal/radial covariance channel relation and quotient map are not derived",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2283_4_local_gr_newton",
            "attempted_claim": "MTS has derived local GR/Newton mechanics",
            "runner_result": "BLOCKED",
            "blocked_by": "q closure is assumed, not derived; finite residual route lacks coefficients and observable maps",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2283_0_owner_verdict",
            "decision": "NO_CURRENT_PARENT_OWNER_FOR_JQ_EQUALS_ONE",
            "reason": "all currently available non-circular owner routes are rejected or contract-only",
            "next_action": "stop looping the same selector proof unless new parent-action evidence appears",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2283_1_closure_policy",
            "decision": "R_AB_ZERO_IS_EXPLICIT_CLOSURE_BENCHMARK",
            "reason": "the closure is useful for benchmarking the GR lane but cannot be presented as derived",
            "next_action": "label closure assumptions in every local benchmark",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2283_2_executable_route",
            "decision": "FINITE_Q_RESIDUAL_ROUTE_IS_NEXT_EXECUTABLE_PATH",
            "reason": "if q is physical, MTS must predict and bound q rather than hide it",
            "next_action": "source M_q^2, j_q, no-gradient guard and observable projection rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2283_3_next",
            "decision": "FINITE_Q_RESIDUAL_COEFFICIENT_SOURCE_NEXT",
            "reason": "this converts the closure failure into a testable residual programme",
            "next_action": "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2283_0_primary",
            "next_target": "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
            "script": "scripts/Y5_R2FR_finite_q_residual_coefficient_source_or_local_benchmark_runner_2284.py",
            "objective": "source or explicitly mark missing the finite q residual inputs M_q^2, j_q, no-gradient/no-hair guard, P_obs, and Newton/source-normalization map, then define closure benchmark versus finite-residual test branches without claims",
            "selection_status": "selected",
            "success_condition": "finite q residual rows become source-backed nonclaim inputs, or every missing coefficient/projection is carried into a local benchmark runner with claims blocked",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_owner": OUTPUTS["owner_audit"],
        "queue_finite": OUTPUTS["finite_intake"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["closure_finalizer"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for closure finalizer and finite-q residual follow-up",
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
                if "gate_pass" in row and row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_text = read_text(OUT / "P8_Y5_BRR545_2282_VALIDATION.csv")
    prior_ok = "VAL2282_OVERALL" in prior_text and "PASS" in prior_text

    owners = owner_audit_rows()
    closure = closure_finalizer_rows()
    finite = finite_intake_rows()
    rules = benchmark_rule_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()

    current_rejected = any(row["owner_id"] == "RCO2283_1_ordinary_current" and row["result"] == "REJECTED_NO_CHARGE_OBSTRUCTION" for row in owners)
    multiplier_rejected = any(row["owner_id"] == "RCO2283_3_posthoc_multiplier" and row["result"] == "REJECTED_BACKREACTION" for row in owners)
    first_class_missing = any(row["owner_id"] == "RCO2283_4_first_class_constraint" and row["result"] == "VIABLE_IN_PRINCIPLE_NOT_PRESENT" for row in owners)
    psi_not_closed = any(row["owner_id"] == "RCO2283_6_psi_quotient" and row["result"] == "NOT_CLOSED" for row in owners)
    closure_finalized = any(row["closure_id"] == "QCF2283_0_finalizer" and row["final_status"] == "CLOSURE_ONLY_UNTIL_FIRST_CLASS_OR_PSI_QUOTIENT_THEOREM" for row in closure)
    finite_contract = len(finite) >= 6 and all(row["valid_for_claim"] is False for row in finite)
    benchmark_rules = len(rules) >= 4
    owner_claim_blocked = any(row["claim_id"] == "CG2283_1_parent_owner" and row["gate_pass"] is False for row in claims)
    finite_route_not_claimed = any(row["claim_id"] == "CG2283_3_finite_route_ready" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    local_blocked = any(row["claim_id"] == "CG2283_4_local_gr_newton" and row["gate_pass"] is False for row in claims)
    refusal_blocks = all(row["score_eligible"] is False and row["valid_for_claim"] is False for row in refusals)
    next_selected = any(row["route_id"] == "NEXT2283_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = (
        not any(not ignored_environment_path(path) for path in FORMALIZATION.rglob("*2283*"))
        if FORMALIZATION.exists()
        else True
    )

    checks = [
        ("VAL2283_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2283_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2283_2_prior_validation", prior_ok, "2282 validation passes"),
        ("VAL2283_3_current_rejected", current_rejected, "ordinary current route rejected by no-charge obstruction"),
        ("VAL2283_4_multiplier_rejected", multiplier_rejected, "post-hoc multiplier route rejected by backreaction"),
        ("VAL2283_5_first_class_missing", first_class_missing, "first-class constraint route remains contract-only"),
        ("VAL2283_6_psi_not_closed", psi_not_closed, "psi quotient route remains not closed"),
        ("VAL2283_7_closure_finalized", closure_finalized, "q/R_AB closure finalizer written"),
        ("VAL2283_8_finite_contract", finite_contract, "finite q residual input contract written nonclaim"),
        ("VAL2283_9_benchmark_rules", benchmark_rules, "closure benchmark rules written"),
        ("VAL2283_10_owner_claim_blocked", owner_claim_blocked, "parent owner claim remains blocked"),
        ("VAL2283_11_finite_route_not_claimed", finite_route_not_claimed, "finite route is prepared but not claimed"),
        ("VAL2283_12_local_blocked", local_blocked, "local GR/Newton claim remains blocked"),
        ("VAL2283_13_refusal_blocks", refusal_blocks, "refusal runner blocks owner/local overclaims"),
        ("VAL2283_14_next_selected", next_selected, "2284 target selected"),
        ("VAL2283_15_csv_parse", csvs_parse, "all generated 2283 CSVs parse"),
        ("VAL2283_16_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2283_17_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2283_18_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2283_19_formalization_no_2283", formalization_clean, "formalization-workbench has no 2283 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2283_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2283 rejects current/multiplier/gauge/psi owner claims, finalizes q/R_AB as closure-only until a first-class or psi-quotient theorem, opens finite q residual coefficient intake, and selects 2284",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    owners = owner_audit_rows()
    closure = closure_finalizer_rows()
    finite = finite_intake_rows()
    rules = benchmark_rule_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2283 - Y5/R2FR Radial Observer-Cell Current Owner Or q Closure Finalizer",
        "",
        "## Verdict",
        "",
        "This checkpoint is the closure finalizer for the current `J_q=1` proof route. Ordinary radial-cell current conservation gives `Q_R` hair, not `Q_R=0`. A post-hoc `lambda_R R_AB` multiplier gives backreaction unless one of the known escape gates closes. Gauge/Noether remains only a first-class-constraint contract, and the primitive `psi` covariance map still does not remove or verticalize `q`.",
        "",
        "So the current corpus does not have a non-circular parent owner for `J_q=T sqrt(S)=1`. The honest status is: `R_AB=0/q=0` may be used as an explicit closure benchmark, not as a derived local-GR/Newton theorem.",
        "",
        "The executable next route is finite residual physics: source `M_q^2`, `j_q`, the no-gradient/no-hair guard, observable projection `P_obs`, and Newton/source normalization. If those can be derived and bounded, MTS can still survive local tests as a controlled finite-residual theory rather than by hiding the `q` channel.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Radial-Cell Owner Audit",
        table(["owner_id", "candidate_owner", "test", "result", "failure_or_gap", "final_status", "valid_for_claim"], owners),
        "",
        "## q Closure Finalizer",
        table(["closure_id", "item", "final_status", "reason", "allowed_use", "forbidden_use", "valid_for_claim"], closure),
        "",
        "## Finite q Residual Intake Contract",
        table(["input_id", "quantity", "required_definition", "current_status", "blocks", "valid_for_claim"], finite),
        "",
        "## Local Benchmark Rules",
        table(["rule_id", "rule", "reason", "allowed", "valid_for_claim"], rules),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is not a failure of the whole programme. It is the end of one over-looped proof route. The theory no longer gets to say local GR is derived from `q=0` unless a genuinely new first-class/no-charge or psi-quotient theorem appears. But it can now become more scientific: carry `q` as a finite residual, derive its coefficients, and make the local tests judge it.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["owner_audit"], owner_audit_rows())
    write_csv(OUTPUTS["closure_finalizer"], closure_finalizer_rows())
    write_csv(OUTPUTS["finite_intake"], finite_intake_rows())
    write_csv(OUTPUTS["benchmark_rules"], benchmark_rule_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["owner_audit"], COPY_TARGETS["queue_owner"])
    shutil.copyfile(OUTPUTS["finite_intake"], COPY_TARGETS["queue_finite"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["closure_finalizer"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
