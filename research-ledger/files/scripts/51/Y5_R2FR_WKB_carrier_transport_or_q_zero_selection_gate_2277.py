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

BRANCH_ID = "MTS_R2FR_WKB_CARRIER_TRANSPORT_OR_Q_ZERO_SELECTION_2277"
DOC = ROOT / "2277-Y5-R2FR-WKB-carrier-transport-or-q-zero-selection-gate.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2277_00_2276_doc",
        "source_key": "2276_doc",
        "source_path": ROOT / "2276-Y5-R2FR-parent-multimode-permission-or-scalar-only-no-go.md",
        "needles": ["WKB2276_2_smoothed_covariance", "WDC2276_1_transport", "NEXT2276_0_primary"],
        "role": "handoff: multimode WKB route conditionally open, transport gate selected",
    },
    {
        "source_id": "SRC2277_01_2276_validation",
        "source_key": "2276_validation",
        "source_path": OUT / "P8_Y5_BRR545_2276_VALIDATION.csv",
        "needles": ["VAL2276_OVERALL", "PASS"],
        "role": "confirms 2276 passed before 2277 starts",
    },
    {
        "source_id": "SRC2277_02_2276_wkb",
        "source_key": "2276_wkb",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2276_WKB_COVARIANCE_DERIVATION.csv",
        "needles": ["WKB2276_2_smoothed_covariance", "W_I=a_I^2/(2 epsilon^2)"],
        "role": "machine-readable WKB covariance and weight definition",
    },
    {
        "source_id": "SRC2277_03_2276_contract",
        "source_key": "2276_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2276_WEIGHT_DYNAMICS_CONTRACT.csv",
        "needles": ["WDC2276_1_transport", "MISSING_WEIGHT_DYNAMICS"],
        "role": "weight dynamics contract to close or refuse",
    },
    {
        "source_id": "SRC2277_04_2275_q_lift",
        "source_key": "2275_q_lift",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2275_CARRIER_WEIGHT_Q_LIFT.csv",
        "needles": ["CWQ2275_0_target", "deltaW_T=deltaC_tt"],
        "role": "q tangent as temporal/radial carrier-weight transfer",
    },
    {
        "source_id": "SRC2277_05_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "∂²_t ψ – c² ∇²ψ + γ ∂_t ψ + λ |ψ|^{n−1} = 0", "– γ ψ (∂_t ψ)"],
        "role": "parent psi equation/action used for WKB transport and action-consistency audit",
    },
    {
        "source_id": "SRC2277_06_2271_formulas",
        "source_key": "2271_formulas",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv",
        "needles": ["PBF2271_1_q_tangent", "PBF2271_3_q_zero_channel_relation"],
        "role": "q tangent and exact q=0 channel relation",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2277_SOURCE_REGISTER.csv",
    "wkb_transport": OUT / "P8_Y5_PARENT_QLOC_2277_WKB_EIKONAL_TRANSPORT_DERIVATION.csv",
    "action_consistency": OUT / "P8_Y5_PARENT_QLOC_2277_ACTION_DAMPING_CONSISTENCY_AUDIT.csv",
    "q_selection": OUT / "P8_Y5_PARENT_QLOC_2277_Q_ZERO_SELECTION_GATE.csv",
    "q_source": OUT / "P8_Y5_PARENT_QLOC_2277_Q_TRANSPORT_SOURCE_LEDGER.csv",
    "residual_intake": OUT / "P8_Y5_PARENT_QLOC_2277_FINITE_QR_RESIDUAL_INTAKE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2277_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2277_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2277_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2277_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2277_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2277_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_transport": QUEUE / "JR2277_WKB_TRANSPORT_GATE_NONCLAIM.csv",
    "queue_qsource": QUEUE / "JR2277_Q_TRANSPORT_SOURCE_LEDGER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_WKB_transport_q_selection_refusal_2277.csv",
    "beta_docs": BETA_DOCS / "RAB_WKB_TRANSPORT_Q_SELECTION_2277_NONCLAIM.csv",
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


def wkb_transport_rows() -> list[dict[str, Any]]:
    return [
        {
            "transport_id": "WTD2277_0_equation",
            "object": "parent equation-level WKB input",
            "formula": "partial_t^2 psi - c^2 Laplacian psi + gamma partial_t psi + lambda |psi|^(n-1)=0",
            "derivation": "use the corpus equation as the equation-level source; variational status of damping is audited separately",
            "status": "EQUATION_LEVEL_INPUT",
            "valid_for_claim": False,
        },
        {
            "transport_id": "WTD2277_1_eikonal",
            "object": "leading O(epsilon^-2) eikonal",
            "formula": "(partial_t S_I)^2 - c^2 |grad S_I|^2 = 0",
            "derivation": "insert psi_I=a_I exp(i S_I/epsilon); leading kinetic terms give -S_t^2+c^2|grad S|^2=0",
            "status": "DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "transport_id": "WTD2277_2_amplitude_transport",
            "object": "next O(epsilon^-1) transport",
            "formula": "partial_t(a_I^2 S_I,t) - c^2 div(a_I^2 grad S_I) + gamma a_I^2 S_I,t = R_lambda,I",
            "derivation": "the kinetic wave operator gives the conservative wave-action current; damping/source/nonlinear terms are placed in R_lambda,I unless action-consistent",
            "status": "DERIVED_WITH_SOURCE_LEDGER",
            "valid_for_claim": False,
        },
        {
            "transport_id": "WTD2277_3_weight_transport",
            "object": "carrier weight W_I=a_I^2/(2 epsilon^2)",
            "formula": "partial_t(W_I S_I,t) - c^2 div(W_I grad S_I) + gamma W_I S_I,t = R_W,I",
            "derivation": "multiply W_I by the same transport law; constants cancel into the residual normalization",
            "status": "CARRIER_TRANSPORT_FORM_DERIVED",
            "valid_for_claim": False,
        },
        {
            "transport_id": "WTD2277_4_interpretation",
            "object": "what transport does and does not do",
            "formula": "D_I W_I + W_I div_ray(v_I) + gamma W_I S_I,t = R_W,I",
            "derivation": "transport evolves each carrier along its own ray; it does not by itself impose a temporal/radial weight-lock",
            "status": "NO_Q_ZERO_SELECTION_BY_TRANSPORT_ALONE",
            "valid_for_claim": False,
        },
    ]


def action_consistency_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ADC2277_0_total_derivative",
            "issue": "damping term in written Lagrangian",
            "statement": "For constant gamma, -gamma psi partial_t psi = -(gamma/2) partial_t(psi^2), a boundary term.",
            "impact": "it cannot by itself produce bulk damping gamma partial_t psi from a standard conservative variation",
            "required_fix": "open-system/Rayleigh dissipation term, gamma time-dependence/boundary rule, doubled-field formalism, or treat damping equation as phenomenological",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ADC2277_1_transport_status",
            "issue": "gamma in WKB transport",
            "statement": "The gamma term can be included at equation level, but it is not parent-action-signed until the damping variational principle is fixed.",
            "impact": "transport law is useful but cannot be claim-grade parent derivation",
            "required_fix": "derive nonconservative transport from a signed parent action or explicitly demote gamma to source/residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "ADC2277_2_nonlinear_term",
            "issue": "lambda |psi|^(n-1) in WKB",
            "statement": "The nonlinear term can couple phases and amplitudes beyond the simple independent carrier transport.",
            "impact": "it may become the missing temporal/radial carrier exchange source, but the current corpus does not derive that exchange law",
            "required_fix": "phase-average nonlinear term into explicit R_W,T and R_W,R source/exchange rows",
            "valid_for_claim": False,
        },
    ]


def q_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "QSG2277_0_q_definition",
            "target": "q=ln[(1-C_tt)(1+C_rr)]",
            "condition": "q=0 iff (1-C_tt)(1+C_rr)=1",
            "transport_test": "Dq=-D C_tt/(1-C_tt)+D C_rr/(1+C_rr)",
            "result": "SELECTION_REQUIRES_Dq=0_ON_Q0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "QSG2277_1_weight_form",
            "target": "carrier weights",
            "condition": "C_tt=s_T W_T Omega_T^2; C_rr=s_R W_R K_R^2",
            "transport_test": "insert W_T and W_R transport laws into Dq",
            "result": "INDEPENDENT_TRANSPORT_DOES_NOT_LOCK_WEIGHT_RATIO",
            "valid_for_claim": False,
        },
        {
            "gate_id": "QSG2277_2_exchange_needed",
            "target": "local GR q-zero preservation",
            "condition": "R_W,T and R_W,R must obey a reciprocal exchange law making Dq=0 when q=0",
            "transport_test": "S_q := -D C_tt/(1-C_tt)+D C_rr/(1+C_rr)",
            "result": "MISSING_CARRIER_EXCHANGE_LAW",
            "valid_for_claim": False,
        },
        {
            "gate_id": "QSG2277_3_residual_route",
            "target": "finite q_R",
            "condition": "if S_q != 0, local residual satisfies transport/stiffness balance such as L_q q_R = S_q",
            "transport_test": "requires operator L_q, boundary conditions, and source projection",
            "result": "RESIDUAL_SOURCE_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
    ]


def q_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "QTS2277_0_gamma",
            "source": "damping/source gamma",
            "possible_role": "could damp temporal/radial carrier weights differently if gamma is channel-dependent",
            "current_status": "gamma appears scalar/universal and variationally unsigned",
            "needed_for_q_zero": "channel-specific or exchange-balanced contribution to S_q",
            "valid_for_claim": False,
        },
        {
            "source_id": "QTS2277_1_lambda",
            "source": "nonlinear lambda term",
            "possible_role": "could couple carrier phases/amplitudes and supply temporal-radial exchange",
            "current_status": "no phase-averaged nonlinear exchange coefficients derived",
            "needed_for_q_zero": "explicit R_W,T and R_W,R satisfying S_q=0 or bounded S_q",
            "valid_for_claim": False,
        },
        {
            "source_id": "QTS2277_2_smoothing",
            "source": "smoothing/phase averaging",
            "possible_role": "could suppress cross/leakage terms and reduce S_q residual",
            "current_status": "kernel and cross-phase leakage bound missing",
            "needed_for_q_zero": "kernel theorem or numeric epsilon_smooth bound",
            "valid_for_claim": False,
        },
        {
            "source_id": "QTS2277_3_boundary",
            "source": "local cell boundary flux",
            "possible_role": "could enforce reciprocal carrier flux balance",
            "current_status": "no boundary condition or no-flux theorem for W_T/W_R",
            "needed_for_q_zero": "parent-signed local cell flux law",
            "valid_for_claim": False,
        },
    ]


def residual_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "FRI2277_0_Sq",
            "quantity": "S_q",
            "meaning": "q-transport source S_q=-D C_tt/(1-C_tt)+D C_rr/(1+C_rr)",
            "required_source": "phase-averaged W_T/W_R transport with gamma/lambda/smoothing terms",
            "current_value": "MISSING_Q_TRANSPORT_SOURCE",
            "units": "inverse length or inverse time depending on D",
            "valid_for_claim": False,
        },
        {
            "input_id": "FRI2277_1_Lq",
            "quantity": "L_q",
            "meaning": "local q residual operator/stiffness converting S_q into q_R",
            "required_source": "parent Hessian or effective transport-stiffness law",
            "current_value": "MISSING_Q_RESIDUAL_OPERATOR",
            "units": "operator units",
            "valid_for_claim": False,
        },
        {
            "input_id": "FRI2277_2_boundary",
            "quantity": "q boundary conditions",
            "meaning": "cell/exterior condition for solving finite q_R",
            "required_source": "local vacuum boundary theorem or arena-specific condition",
            "current_value": "MISSING_Q_BOUNDARY_CONDITION",
            "units": "dimensionless q or flux",
            "valid_for_claim": False,
        },
        {
            "input_id": "FRI2277_3_observable",
            "quantity": "q_R observable map",
            "meaning": "map from q_R to PPN/R10/clock/orbital residual vector",
            "required_source": "metric readout and local arena projector",
            "current_value": "MISSING_OBSERVABLE_PROJECTION",
            "units": "arena-specific",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2277_0_transport_claim",
            "attempted_claim": "A_MTS transport has been fully derived as a parent-action theorem.",
            "runner_result": "BLOCKED",
            "blocked_by": "damping term is variationally unsigned and nonlinear phase-averaged source is missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2277_1_q_zero_claim",
            "attempted_claim": "WKB transport selects q=0 in local vacuum.",
            "runner_result": "BLOCKED",
            "blocked_by": "independent carrier transport does not impose temporal/radial weight-lock; exchange law missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2277_2_local_gr_claim",
            "attempted_claim": "MTS has derived the local GR limit.",
            "runner_result": "BLOCKED",
            "blocked_by": "q=0 selection and finite q_R residual equation remain unsourced",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2277_0_eikonal_transport",
            "claim": "equation-level WKB eikonal and carrier transport forms are derived",
            "gate_pass": True,
            "reason": "leading and next-order WKB equations are written from the corpus wave equation",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2277_1_parent_action_transport",
            "claim": "transport is parent-action signed",
            "gate_pass": False,
            "reason": "damping term is a total derivative for constant gamma unless an open-system principle is supplied",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2277_2_q_zero_selection",
            "claim": "transport selects q=0",
            "gate_pass": False,
            "reason": "no carrier exchange law forces Dq=0 on the q=0 surface",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2277_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "no exact q-zero selection theorem or finite q_R bound exists",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2277_0_gain",
            "decision": "WKB_TRANSPORT_FORM_DERIVED_AT_EQUATION_LEVEL",
            "reason": "The carrier weights obey a wave-action transport equation with gamma/nonlinear residual sources.",
            "next_action": "Use this as the source ledger for q-transport, not as a local-GR claim.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2277_1_blocker",
            "decision": "TRANSPORT_DOES_NOT_SELECT_Q_ZERO_BY_ITSELF",
            "reason": "Independent temporal/radial carrier transport does not enforce the q=0 weight relation.",
            "next_action": "derive a carrier exchange/reciprocity law or retain S_q as finite residual source.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2277_2_action_warning",
            "decision": "DAMPING_VARIATIONAL_STATUS_MUST_BE_FIXED",
            "reason": "The written -gamma psi partial_t psi term is boundary-like for constant gamma.",
            "next_action": "either supply an open-system action or demote gamma transport to equation-level phenomenology.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2277_3_next",
            "decision": "CARRIER_EXCHANGE_LAW_OR_Q_SOURCE_BOUND_NEXT",
            "reason": "This is the coupling lock needed to make q=0 derivable, or q_R testable.",
            "next_action": "2278-Y5-R2FR-carrier-exchange-law-or-q-transport-source-bound.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2277_0_primary",
            "next_target": "2278-Y5-R2FR-carrier-exchange-law-or-q-transport-source-bound.md",
            "script": "scripts/Y5_R2FR_carrier_exchange_law_or_q_transport_source_bound_2278.py",
            "objective": "derive a temporal/radial carrier exchange law that makes S_q=0 on q=0, or stage a source-backed finite S_q/q_R residual bound",
            "selection_status": "selected",
            "success_condition": "parent exchange law gives Dq=0 in local vacuum, or S_q is converted into a bounded q_R residual with all source/operator/projection inputs tracked",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_transport": OUTPUTS["wkb_transport"],
        "queue_qsource": OUTPUTS["q_source"],
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
            "reason": "branch copy for downstream carrier-exchange and q-source-bound audits",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2276_VALIDATION.csv")
    prior_ok = "VAL2276_OVERALL" in prior_text and "PASS" in prior_text

    transport = wkb_transport_rows()
    action = action_consistency_rows()
    q_selection = q_selection_rows()
    q_source = q_source_rows()
    intake = residual_intake_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()

    eikonal_written = any(row["transport_id"] == "WTD2277_1_eikonal" for row in transport)
    weight_transport_written = any(row["transport_id"] == "WTD2277_3_weight_transport" for row in transport)
    damping_audited = any(row["audit_id"] == "ADC2277_0_total_derivative" for row in action)
    q_gate_blocks = any(row["result"] == "MISSING_CARRIER_EXCHANGE_LAW" for row in q_selection)
    q_source_nonclaim = all(row["valid_for_claim"] is False for row in q_source)
    intake_missing = all(row["valid_for_claim"] is False and row["current_value"].startswith("MISSING") for row in intake)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusal)
    parent_transport_blocked = any(row["claim_id"] == "CG2277_1_parent_action_transport" and row["gate_pass"] is False for row in claims)
    q_zero_blocked = any(row["claim_id"] == "CG2277_2_q_zero_selection" and row["gate_pass"] is False for row in claims)
    local_claim_blocked = any(row["claim_id"] == "CG2277_3_local_GR" and row["gate_pass"] is False for row in claims)
    equation_level_not_promoted = any(row["claim_id"] == "CG2277_0_eikonal_transport" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2277_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2277*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2277_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2277_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2277_2_prior_validation", prior_ok, "2276 validation passes"),
        ("VAL2277_3_eikonal_written", eikonal_written, "WKB eikonal equation written"),
        ("VAL2277_4_weight_transport", weight_transport_written, "carrier weight transport equation written"),
        ("VAL2277_5_damping_audited", damping_audited, "gamma damping action consistency audit written"),
        ("VAL2277_6_q_gate_blocks", q_gate_blocks, "q-zero selection requires missing carrier exchange law"),
        ("VAL2277_7_q_source_nonclaim", q_source_nonclaim, "q transport source ledger remains nonclaim"),
        ("VAL2277_8_intake_missing", intake_missing, "finite q_R residual inputs remain missing"),
        ("VAL2277_9_refusal_blocks", refusal_blocks, "refusal runner blocks transport/q-zero/local-GR claims"),
        ("VAL2277_10_parent_transport_blocked", parent_transport_blocked, "parent-action transport claim remains blocked"),
        ("VAL2277_11_q_zero_blocked", q_zero_blocked, "q-zero selection claim remains blocked"),
        ("VAL2277_12_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2277_13_equation_level_not_promoted", equation_level_not_promoted, "equation-level transport is not promoted to claim-grade"),
        ("VAL2277_14_next_selected", next_selected, "2278 target selected"),
        ("VAL2277_15_csv_parse", csvs_parse, "all generated 2277 CSVs parse"),
        ("VAL2277_16_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2277_17_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2277_18_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2277_19_formalization_no_2277", formalization_clean, "formalization-workbench has no 2277 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2277_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2277 derives equation-level WKB carrier transport, audits damping/action consistency, shows transport alone does not select q=0, stages S_q/q_R residual inputs, and selects 2278",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    transport = wkb_transport_rows()
    action = action_consistency_rows()
    q_selection = q_selection_rows()
    q_source = q_source_rows()
    intake = residual_intake_rows()
    refusal = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2277 - Y5/R2FR WKB Carrier Transport Or q-Zero Selection Gate",
        "",
        "## Verdict",
        "",
        "This checkpoint gets a real transport law, but it does not close local GR. From the corpus wave equation, the WKB carrier phases satisfy `(partial_t S_I)^2-c^2|grad S_I|^2=0`, and the carrier weights obey a wave-action transport equation. That is genuine structure.",
        "",
        "But independent transport of `W_T` and `W_R` does not force the q-zero relation `(1-C_tt)(1+C_rr)=1`. To preserve q=0, the theory still needs a temporal/radial carrier exchange law making `S_q=-D C_tt/(1-C_tt)+D C_rr/(1+C_rr)` vanish on q=0, or else `S_q` becomes the finite q_R residual source to bound.",
        "",
        "There is also a ruthless action warning: the written `-gamma psi partial_t psi` term is a boundary term for constant gamma, so damping in the transport law is equation-level until an open-system or nonconservative parent principle is supplied.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## WKB Eikonal / Transport Derivation",
        table(["transport_id", "object", "formula", "derivation", "status", "valid_for_claim"], transport),
        "",
        "## Action / Damping Consistency Audit",
        table(["audit_id", "issue", "statement", "impact", "required_fix", "valid_for_claim"], action),
        "",
        "## q-Zero Selection Gate",
        table(["gate_id", "target", "condition", "transport_test", "result", "valid_for_claim"], q_selection),
        "",
        "## q-Transport Source Ledger",
        table(["source_id", "source", "possible_role", "current_status", "needed_for_q_zero", "valid_for_claim"], q_source),
        "",
        "## Finite q_R Residual Intake",
        table(["input_id", "quantity", "meaning", "required_source", "current_value", "units", "valid_for_claim"], intake),
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
        "The story is now very concrete: WKB transport gives lawful carriers, but the GR limit needs a coupling/exchange law between the temporal and radial carrier budgets. That is exactly the coupling hunch, now in equations. The next step is not more broad philosophy; it is `S_q`: derive it as zero from carrier exchange, or source it and bound q_R.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["wkb_transport"], wkb_transport_rows())
    write_csv(OUTPUTS["action_consistency"], action_consistency_rows())
    write_csv(OUTPUTS["q_selection"], q_selection_rows())
    write_csv(OUTPUTS["q_source"], q_source_rows())
    write_csv(OUTPUTS["residual_intake"], residual_intake_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["wkb_transport"], COPY_TARGETS["queue_transport"])
    shutil.copyfile(OUTPUTS["q_source"], COPY_TARGETS["queue_qsource"])
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
