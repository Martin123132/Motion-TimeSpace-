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

BRANCH_ID = "MTS_R2FR_CARRIER_EXCHANGE_LAW_OR_Q_SOURCE_BOUND_2278"
DOC = ROOT / "2278-Y5-R2FR-carrier-exchange-law-or-q-transport-source-bound.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2278_00_2277_doc",
        "source_key": "2277_doc",
        "source_path": ROOT / "2277-Y5-R2FR-WKB-carrier-transport-or-q-zero-selection-gate.md",
        "needles": ["QSG2277_2_exchange_needed", "FRI2277_0_Sq", "NEXT2277_0_primary"],
        "role": "handoff: carrier exchange law or finite S_q source bound selected",
    },
    {
        "source_id": "SRC2278_01_2277_validation",
        "source_key": "2277_validation",
        "source_path": OUT / "P8_Y5_BRR545_2277_VALIDATION.csv",
        "needles": ["VAL2277_OVERALL", "PASS"],
        "role": "confirms 2277 passed before 2278 starts",
    },
    {
        "source_id": "SRC2278_02_2277_q_selection",
        "source_key": "2277_q_selection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2277_Q_ZERO_SELECTION_GATE.csv",
        "needles": ["QSG2277_2_exchange_needed", "MISSING_CARRIER_EXCHANGE_LAW"],
        "role": "machine-readable q-zero exchange blocker",
    },
    {
        "source_id": "SRC2278_03_2277_q_source",
        "source_key": "2277_q_source",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2277_Q_TRANSPORT_SOURCE_LEDGER.csv",
        "needles": ["QTS2277_1_lambda", "QTS2277_3_boundary"],
        "role": "candidate exchange-source mechanisms",
    },
    {
        "source_id": "SRC2278_04_2277_residual",
        "source_key": "2277_residual_intake",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2277_FINITE_QR_RESIDUAL_INTAKE.csv",
        "needles": ["FRI2277_0_Sq", "MISSING_Q_TRANSPORT_SOURCE"],
        "role": "finite q_R residual input slots",
    },
    {
        "source_id": "SRC2278_05_2275_q_lift",
        "source_key": "2275_q_lift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2275_CARRIER_WEIGHT_Q_LIFT.csv",
        "needles": ["CWQ2275_0_target", "deltaW_T=deltaC_tt"],
        "role": "q tangent as temporal/radial carrier-weight transfer",
    },
    {
        "source_id": "SRC2278_06_reciprocal_charge",
        "source_key": "reciprocal_charge_source_neutrality",
        "source_path": ROOT / "06-reciprocal-charge-source-neutrality.md",
        "needles": ["Q_R=0 if source is reciprocal-neutral", "reciprocity remains conditional"],
        "role": "earlier reciprocal-neutrality route retained as conditional motivation, not claim",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2278_SOURCE_REGISTER.csv",
    "exchange_condition": OUT / "P8_Y5_PARENT_QLOC_2278_EXACT_EXCHANGE_CONDITION.csv",
    "exchange_solver": OUT / "P8_Y5_PARENT_QLOC_2278_RECIPROCAL_EXCHANGE_SOLVER.csv",
    "mechanism_audit": OUT / "P8_Y5_PARENT_QLOC_2278_EXCHANGE_MECHANISM_AUDIT.csv",
    "residual_bound": OUT / "P8_Y5_PARENT_QLOC_2278_SQ_QR_RESIDUAL_BOUND_TEMPLATE.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2278_PARENT_EXCHANGE_CONTRACT.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2278_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2278_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2278_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2278_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2278_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2278_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_condition": QUEUE / "JR2278_EXACT_CARRIER_EXCHANGE_CONDITION_NONCLAIM.csv",
    "queue_bound": QUEUE / "JR2278_SQ_QR_RESIDUAL_BOUND_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_carrier_exchange_q_source_refusal_2278.csv",
    "beta_docs": BETA_DOCS / "RAB_CARRIER_EXCHANGE_Q_SOURCE_2278_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
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
        path = Path(source["source_path"])
        text = read_text(path) if path.exists() else ""
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


def exchange_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "EXC2278_0_q_source",
            "object": "q transport source",
            "formula": "S_q := Dq = -D C_tt/(1-C_tt) + D C_rr/(1+C_rr)",
            "derivation": "differentiate q=ln[(1-C_tt)(1+C_rr)] along the local readout/transport direction D",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "condition_id": "EXC2278_1_q_zero_surface",
            "object": "q=0 surface",
            "formula": "q=0 iff C_rr=C_tt/(1-C_tt), hence 1+C_rr=1/(1-C_tt)",
            "derivation": "solve (1-C_tt)(1+C_rr)=1",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "condition_id": "EXC2278_2_tangent_lock",
            "object": "exact q-zero preservation",
            "formula": "on q=0, D C_rr = D C_tt/(1-C_tt)^2",
            "derivation": "differentiate C_rr=C_tt/(1-C_tt); equivalently set S_q=0 on the q=0 surface",
            "status": "EXACT_EXCHANGE_CONDITION",
            "valid_for_claim": False,
        },
        {
            "condition_id": "EXC2278_3_weight_lock",
            "object": "carrier-weight form",
            "formula": "D(s_R W_R K_R^2) = D(s_T W_T Omega_T^2)/(1-s_T W_T Omega_T^2)^2",
            "derivation": "substitute C_tt=s_T W_T Omega_T^2 and C_rr=s_R W_R K_R^2 into EXC2278_2",
            "status": "EXACT_WEIGHT_EXCHANGE_TARGET",
            "valid_for_claim": False,
        },
    ]


def exchange_solver_rows() -> list[dict[str, Any]]:
    return [
        {
            "solver_id": "RXS2278_0_free_source_split",
            "target": "split free transport plus exchange",
            "formula": "D C_tt=F_T+E_T; D C_rr=F_R+E_R",
            "condition": "S_q=( -F_T/(1-C_tt)+F_R/(1+C_rr) ) + ( -E_T/(1-C_tt)+E_R/(1+C_rr) )",
            "status": "DEFINITION",
            "valid_for_claim": False,
        },
        {
            "solver_id": "RXS2278_1_exchange_condition",
            "target": "exchange needed for S_q=0",
            "formula": "-E_T/(1-C_tt)+E_R/(1+C_rr) = -S_q_free",
            "condition": "S_q_free=-F_T/(1-C_tt)+F_R/(1+C_rr)",
            "status": "EXACT_REQUIRED_EXCHANGE",
            "valid_for_claim": False,
        },
        {
            "solver_id": "RXS2278_2_one_parameter_family",
            "target": "general exchange family",
            "formula": "choose E_T arbitrary, then E_R=(1+C_rr)*(E_T/(1-C_tt)-S_q_free)",
            "condition": "without an additional conservation/detailed-balance law, exchange is underdetermined",
            "status": "UNDERDETERMINED_WITHOUT_PARENT_LAW",
            "valid_for_claim": False,
        },
        {
            "solver_id": "RXS2278_3_conservative_exchange_example",
            "target": "if weighted exchange conservation is imposed",
            "formula": "with a_T E_T + a_R E_R=0, solve E_T=a_R(1+C_rr)S_q_free/[a_T(1-C_tt)+a_R(1+C_rr)]",
            "condition": "a_T,a_R and the conserved exchange budget must be parent-signed",
            "status": "CONDITIONAL_CLOSURE_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
    ]


def mechanism_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism_id": "EMA2278_0_lambda_phase_mixing",
            "candidate": "nonlinear lambda phase mixing",
            "how_it_could_help": "phase-averaged nonlinear terms could transfer amplitude between temporal and radial carriers",
            "current_failure": "no coefficients R_W,T and R_W,R have been derived from |psi|^(n-1)",
            "next_needed": "compute phase-averaged exchange coefficients and test EXC2278_3",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "EMA2278_1_boundary_flux",
            "candidate": "local cell boundary/no-flux reciprocity",
            "how_it_could_help": "boundary conditions could impose the weighted exchange conservation needed by RXS2278_3",
            "current_failure": "no parent-signed W_T/W_R cell-flux law exists",
            "next_needed": "derive boundary flux from action/current, not from desired q=0",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "EMA2278_2_reciprocal_neutrality",
            "candidate": "reciprocal source neutrality",
            "how_it_could_help": "earlier R_AB/Q_R neutrality route would set the reciprocal source to zero",
            "current_failure": "previous route remains conditional and not carrier-transport-derived",
            "next_needed": "map Q_R neutrality to S_q=0 with source path and equations",
            "valid_for_claim": False,
        },
        {
            "mechanism_id": "EMA2278_3_relaxation_lock",
            "candidate": "q relaxation/detailed balance",
            "how_it_could_help": "a term S_q=-kappa_q q makes q=0 an invariant/stable surface",
            "current_failure": "kappa_q and its parent origin are missing",
            "next_needed": "derive kappa_q from nonlinear transport or keep as finite residual parameter",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SQR2278_0_source_norm",
            "quantity": "S_q source norm",
            "bound": "||S_q|| <= ||S_q_free|| + ||S_q_exchange_error||",
            "required_inputs": "phase-averaged F_T,F_R,E_T,E_R; common D convention; units",
            "claim_gate": "all terms sourced or parent-zero with no cancellation",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SQR2278_1_q_residual",
            "quantity": "finite q_R",
            "bound": "||q_R|| <= ||G_q|| (||S_q|| + ||boundary_q||)",
            "required_inputs": "q operator inverse/coercivity G_q, boundary condition, same-frame norm",
            "claim_gate": "G_q and boundary sourced and positive/coercive",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SQR2278_2_observable",
            "quantity": "local observable residual",
            "bound": "||R_local|| <= K_obs ||q_R||",
            "required_inputs": "PPN/R10/clock/orbital projection norm K_obs and arena tolerance",
            "claim_gate": "observable map and tolerance sourced before any pass/fail statement",
            "valid_for_claim": False,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PEC2278_0_common_readout_D",
            "requirement": "define the local readout/transport derivative D shared by C_tt, C_rr, q, and observables",
            "current_status": "MISSING_COMMON_D_CONVENTION",
            "why_needed": "S_q is meaningless as a claim-grade source without a fixed transport/readout direction",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PEC2278_1_exchange_budget",
            "requirement": "derive the conserved or dissipative budget that relates E_T and E_R",
            "current_status": "MISSING_EXCHANGE_CONSERVATION_OR_DISSIPATION_LAW",
            "why_needed": "RXS2278_2 is underdetermined without an extra parent law",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PEC2278_2_phase_average_coefficients",
            "requirement": "compute lambda/gamma/smoothing contributions to F_T,F_R,E_T,E_R",
            "current_status": "MISSING_PHASE_AVERAGED_EXCHANGE_COEFFICIENTS",
            "why_needed": "the exact exchange target must be sourced, not selected after the fact",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PEC2278_3_q_residual_operator",
            "requirement": "derive L_q or G_q converting finite S_q into q_R",
            "current_status": "MISSING_Q_RESIDUAL_OPERATOR",
            "why_needed": "if q=0 is not exact, local tests require a bounded q_R",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2278_0_exchange_claim",
            "attempted_claim": "A parent carrier exchange law has been derived.",
            "runner_result": "BLOCKED",
            "blocked_by": "exact exchange condition written, but E_T/E_R budget and coefficients are not parent-signed",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2278_1_q_zero_claim",
            "attempted_claim": "q=0 is preserved in local vacuum.",
            "runner_result": "BLOCKED",
            "blocked_by": "EXC2278_2 is a target condition, not a derived law",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2278_2_qR_bound_claim",
            "attempted_claim": "finite q_R residual is bounded for local tests.",
            "runner_result": "BLOCKED",
            "blocked_by": "S_q, G_q, boundary, and observable projection inputs remain missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2278_0_exact_condition",
            "claim": "exact algebraic exchange condition for q-zero preservation is derived",
            "gate_pass": True,
            "reason": "D C_rr = D C_tt/(1-C_tt)^2 follows by differentiating q=0",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2278_1_parent_exchange",
            "claim": "parent theory supplies the required carrier exchange law",
            "gate_pass": False,
            "reason": "exchange budget and phase-averaged coefficients are missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2278_2_finite_qR_bound",
            "claim": "finite q_R source bound is score-ready",
            "gate_pass": False,
            "reason": "S_q/G_q/boundary/observable inputs remain placeholders",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2278_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "q-zero preservation is a target, not a parent-signed theorem",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2278_0_gain",
            "decision": "EXACT_EXCHANGE_CONDITION_DERIVED",
            "reason": "The temporal/radial carrier lock needed for q=0 is now an explicit formula, not a vague coupling.",
            "next_action": "Use EXC2278_2/3 as the mandatory target for any parent exchange derivation.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2278_1_blocker",
            "decision": "PARENT_EXCHANGE_LAW_UNSIGNED",
            "reason": "The general exchange solution is underdetermined until a conserved/dissipative budget is supplied.",
            "next_action": "derive exchange coefficients from nonlinear phase averaging or boundary/current laws.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2278_2_backstop",
            "decision": "S_Q_RESIDUAL_BOUND_STAGED",
            "reason": "If exchange is not exact, S_q is the local residual source feeding finite q_R.",
            "next_action": "source S_q, G_q, boundary, and observable projection inputs before scoring.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2278_3_next",
            "decision": "NONLINEAR_PHASE_EXCHANGE_OR_Q_RESIDUAL_OPERATOR_NEXT",
            "reason": "The next best derivation target is the source of E_T/E_R or the operator that bounds their mismatch.",
            "next_action": "2279-Y5-R2FR-nonlinear-phase-exchange-coefficients-or-q-residual-operator.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2278_0_primary",
            "next_target": "2279-Y5-R2FR-nonlinear-phase-exchange-coefficients-or-q-residual-operator.md",
            "script": "scripts/Y5_R2FR_nonlinear_phase_exchange_coefficients_or_q_residual_operator_2279.py",
            "objective": "derive phase-averaged nonlinear/boundary exchange coefficients E_T,E_R that satisfy the exact q-zero condition, or derive L_q/G_q for a finite S_q-to-q_R bound",
            "selection_status": "selected",
            "success_condition": "parent-sourced E_T/E_R closes EXC2278_3, or S_q is mapped through a sourced q residual operator with all local-test inputs still nonclaim until numeric",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_condition": OUTPUTS["exchange_condition"],
        "queue_bound": OUTPUTS["residual_bound"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["decision"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for downstream exchange-coefficient and q-residual audits",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2277_VALIDATION.csv")
    prior_ok = "VAL2277_OVERALL" in prior_text and "PASS" in prior_text

    condition = exchange_condition_rows()
    solver = exchange_solver_rows()
    mechanisms = mechanism_audit_rows()
    residual = residual_bound_rows()
    contract = parent_contract_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()

    exact_condition = any("D C_rr = D C_tt/(1-C_tt)^2" in row["formula"] for row in condition)
    weight_condition = any(row["condition_id"] == "EXC2278_3_weight_lock" for row in condition)
    underdetermined = any(row["status"] == "UNDERDETERMINED_WITHOUT_PARENT_LAW" for row in solver)
    mechanisms_nonclaim = all(row["valid_for_claim"] is False for row in mechanisms)
    residual_nonclaim = all(row["valid_for_claim"] is False for row in residual)
    contract_missing = all(row["valid_for_claim"] is False and row["current_status"].startswith("MISSING") for row in contract)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusal)
    parent_exchange_blocked = any(row["claim_id"] == "CG2278_1_parent_exchange" and row["gate_pass"] is False for row in claims)
    local_claim_blocked = any(row["claim_id"] == "CG2278_3_local_GR" and row["gate_pass"] is False for row in claims)
    exact_not_promoted = any(row["claim_id"] == "CG2278_0_exact_condition" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2278_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2278*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2278_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2278_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2278_2_prior_validation", prior_ok, "2277 validation passes"),
        ("VAL2278_3_exact_condition", exact_condition, "exact q-zero exchange tangent condition written"),
        ("VAL2278_4_weight_condition", weight_condition, "carrier-weight exchange target written"),
        ("VAL2278_5_underdetermined", underdetermined, "exchange solver remains underdetermined without parent law"),
        ("VAL2278_6_mechanisms_nonclaim", mechanisms_nonclaim, "candidate mechanisms remain nonclaim"),
        ("VAL2278_7_residual_nonclaim", residual_nonclaim, "S_q/q_R residual bound template remains nonclaim"),
        ("VAL2278_8_contract_missing", contract_missing, "parent exchange contract inputs remain missing"),
        ("VAL2278_9_refusal_blocks", refusal_blocks, "refusal runner blocks exchange/q-zero/q_R claims"),
        ("VAL2278_10_parent_exchange_blocked", parent_exchange_blocked, "parent exchange claim remains blocked"),
        ("VAL2278_11_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2278_12_exact_not_promoted", exact_not_promoted, "exact algebraic condition is not promoted to parent claim"),
        ("VAL2278_13_next_selected", next_selected, "2279 target selected"),
        ("VAL2278_14_csv_parse", csvs_parse, "all generated 2278 CSVs parse"),
        ("VAL2278_15_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2278_16_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2278_17_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2278_18_formalization_no_2278", formalization_clean, "formalization-workbench has no 2278 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2278_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2278 derives the exact carrier exchange condition for q-zero preservation, shows parent exchange is underdetermined without a budget law, stages S_q/q_R residual bounds, and selects 2279",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    condition = exchange_condition_rows()
    solver = exchange_solver_rows()
    mechanisms = mechanism_audit_rows()
    residual = residual_bound_rows()
    contract = parent_contract_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2278 - Y5/R2FR Carrier Exchange Law Or q-Transport Source Bound",
        "",
        "## Verdict",
        "",
        "This checkpoint gets the coupling lock into exact algebra. Since `q=ln[(1-C_tt)(1+C_rr)]`, q-zero preservation requires `S_q=Dq=0`. On the q=0 surface this is exactly `D C_rr = D C_tt/(1-C_tt)^2`.",
        "",
        "That is a real derivation of the target exchange law. But it is not yet a parent theorem: the exchange sources `E_T,E_R` are underdetermined unless the parent theory supplies an exchange budget, boundary/no-flux law, nonlinear phase-mixing coefficient, or equivalent detailed-balance principle. So local GR remains blocked, but the missing coupling is now a concrete equation.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Exact Exchange Condition",
        table(["condition_id", "object", "formula", "derivation", "status", "valid_for_claim"], condition),
        "",
        "## Reciprocal Exchange Solver",
        table(["solver_id", "target", "formula", "condition", "status", "valid_for_claim"], solver),
        "",
        "## Exchange Mechanism Audit",
        table(["mechanism_id", "candidate", "how_it_could_help", "current_failure", "next_needed", "valid_for_claim"], mechanisms),
        "",
        "## S_q / q_R Residual Bound Template",
        table(["bound_id", "quantity", "bound", "required_inputs", "claim_gate", "valid_for_claim"], residual),
        "",
        "## Parent Exchange Contract",
        table(["contract_id", "requirement", "current_status", "why_needed", "valid_for_claim"], contract),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
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
        "This is not circling. The coupling problem has collapsed to one precise condition: parent dynamics must make the carrier exchange tangent to the q=0 surface. If it cannot, the source `S_q` is the retained residual that has to be bounded. The next attack is to compute the exchange coefficients from nonlinear phase averaging or derive the q residual operator.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["exchange_condition"], exchange_condition_rows())
    write_csv(OUTPUTS["exchange_solver"], exchange_solver_rows())
    write_csv(OUTPUTS["mechanism_audit"], mechanism_audit_rows())
    write_csv(OUTPUTS["residual_bound"], residual_bound_rows())
    write_csv(OUTPUTS["parent_contract"], parent_contract_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["exchange_condition"], COPY_TARGETS["queue_condition"])
    shutil.copyfile(OUTPUTS["residual_bound"], COPY_TARGETS["queue_bound"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
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
