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

BRANCH_ID = "MTS_R2FR_NONLINEAR_PHASE_EXCHANGE_OR_Q_OPERATOR_2279"
DOC = ROOT / "2279-Y5-R2FR-nonlinear-phase-exchange-coefficients-or-q-residual-operator.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2279_00_2278_doc",
        "source_key": "2278_doc",
        "source_path": ROOT / "2278-Y5-R2FR-carrier-exchange-law-or-q-transport-source-bound.md",
        "needles": ["EXC2278_3_weight_lock", "EMA2278_0_lambda_phase_mixing", "NEXT2278_0_primary"],
        "role": "handoff: nonlinear exchange coefficients or q residual operator selected",
    },
    {
        "source_id": "SRC2279_01_2278_validation",
        "source_key": "2278_validation",
        "source_path": OUT / "P8_Y5_BRR545_2278_VALIDATION.csv",
        "needles": ["VAL2278_OVERALL", "PASS"],
        "role": "confirms 2278 passed before 2279 starts",
    },
    {
        "source_id": "SRC2279_02_2278_condition",
        "source_key": "2278_exchange_condition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2278_EXACT_EXCHANGE_CONDITION.csv",
        "needles": ["EXC2278_2_tangent_lock", "EXACT_WEIGHT_EXCHANGE_TARGET"],
        "role": "machine-readable q-zero exchange target",
    },
    {
        "source_id": "SRC2279_03_2278_mechanism",
        "source_key": "2278_mechanism",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2278_EXCHANGE_MECHANISM_AUDIT.csv",
        "needles": ["EMA2278_0_lambda_phase_mixing", "EMA2278_3_relaxation_lock"],
        "role": "candidate exchange mechanisms to audit",
    },
    {
        "source_id": "SRC2279_04_2278_residual",
        "source_key": "2278_residual_bound",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2278_SQ_QR_RESIDUAL_BOUND_TEMPLATE.csv",
        "needles": ["SQR2278_1_q_residual", "G_q"],
        "role": "finite q_R residual operator template",
    },
    {
        "source_id": "SRC2279_05_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "λ |ψ|^{n−1}", "n = 4/3"],
        "role": "parent nonlinear psi action/equation and exponent",
    },
    {
        "source_id": "SRC2279_06_axio_phase",
        "source_key": "axio_phase_dynamics",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "field-theory" / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md",
        "needles": ["phase topology", "nonlinear phase dynamics", "curvature saturation"],
        "role": "corpus support for nonlinear phase dynamics as a motif, not a local-GR proof",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2279_SOURCE_REGISTER.csv",
    "nonlinear_projection": OUT / "P8_Y5_PARENT_QLOC_2279_NONLINEAR_PHASE_PROJECTION_AUDIT.csv",
    "exchange_coefficients": OUT / "P8_Y5_PARENT_QLOC_2279_EXCHANGE_COEFFICIENT_LEDGER.csv",
    "q_operator": OUT / "P8_Y5_PARENT_QLOC_2279_Q_RESIDUAL_OPERATOR_TEMPLATE.csv",
    "operator_inputs": OUT / "P8_Y5_PARENT_QLOC_2279_Q_OPERATOR_INPUT_CONTRACT.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2279_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2279_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2279_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2279_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2279_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2279_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_projection": QUEUE / "JR2279_NONLINEAR_PHASE_PROJECTION_AUDIT_NONCLAIM.csv",
    "queue_operator": QUEUE / "JR2279_Q_RESIDUAL_OPERATOR_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_nonlinear_phase_exchange_refusal_2279.csv",
    "beta_docs": BETA_DOCS / "RAB_NONLINEAR_PHASE_EXCHANGE_2279_NONCLAIM.csv",
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


def nonlinear_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "NPP2279_0_variational_sign",
            "object": "nonlinear force from potential",
            "formula": "delta[(lambda/n)|psi|^n]/delta psi = lambda sign(psi)|psi|^(n-1)",
            "result": "ACTION_EQUATION_SIGN_GUARD",
            "meaning": "the corpus equation often writes lambda |psi|^(n-1); for action-grade work the sign/psi factor must be fixed before coefficients are claimed",
            "valid_for_claim": False,
        },
        {
            "projection_id": "NPP2279_1_exchange_projection",
            "object": "mode exchange coefficient",
            "formula": "E_I^lambda proportional to <N(psi) sin(phi_I)>_phase or the equivalent action-angle projection",
            "result": "COEFFICIENT_DEFINITION_ONLY",
            "meaning": "this is the quantity that would feed E_T/E_R in EXC2278_3",
            "valid_for_claim": False,
        },
        {
            "projection_id": "NPP2279_2_independent_phase_zero",
            "object": "independent uniform phases",
            "formula": "<N(sum_J a_J cos phi_J) sin(phi_I)> = 0 by phi_I -> -phi_I parity when phases are uncorrelated",
            "result": "NO_DIRECTED_EXCHANGE_FROM_RANDOM_PHASE_AVERAGE",
            "meaning": "random smoothing alone does not generate the temporal/radial exchange lock",
            "valid_for_claim": False,
        },
        {
            "projection_id": "NPP2279_3_phase_locked_route",
            "object": "phase-locked or boundary-correlated carriers",
            "formula": "E_I^lambda = lambda integral dPhi P_locked(Phi) N(psi(Phi)) sin(phi_I)",
            "result": "POSSIBLE_BUT_REQUIRES_LOCK_DISTRIBUTION",
            "meaning": "nonzero exchange is possible only after specifying a non-random phase distribution, boundary condition, or memory kernel",
            "valid_for_claim": False,
        },
    ]


def exchange_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "ECL2279_0_target",
            "target": "close EXC2278_3",
            "coefficient_formula": "E_T^lambda,E_R^lambda must satisfy D(s_R W_R K_R^2)=D(s_T W_T Omega_T^2)/(1-s_T W_T Omega_T^2)^2",
            "current_status": "TARGET_ONLY",
            "missing_inputs": "phase-lock distribution; projector definitions P_T/P_R; nonlinear sign convention; smoothing kernel",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "ECL2279_1_random_phase",
            "target": "random-phase nonlinear exchange",
            "coefficient_formula": "E_T^lambda=E_R^lambda=0 at directed-action projection level under independent uniform phases",
            "current_status": "DERIVED_ZERO_FOR_RANDOM_PHASE_EXCHANGE",
            "missing_inputs": "does not prove q=0; it proves random phase averaging cannot be the exchange source",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "ECL2279_2_locked_phase",
            "target": "locked-phase nonlinear exchange",
            "coefficient_formula": "E_A^lambda=lambda <P_A N(psi)>_locked for A in {T,R}",
            "current_status": "UNSOURCED_COEFFICIENT_FAMILY",
            "missing_inputs": "P_locked; P_A; amplitude scaling; n=4/3 regularization at psi=0; source path",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "ECL2279_3_boundary_memory",
            "target": "boundary/memory exchange",
            "coefficient_formula": "E_A^bdry=<J_A^cell · n>_boundary or memory-kernel transfer",
            "current_status": "UNSOURCED_FLUX_FAMILY",
            "missing_inputs": "cell boundary, current J_A, no-flux/reciprocal-flux theorem, memory kernel",
            "valid_for_claim": False,
        },
    ]


def q_operator_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "QOP2279_0_transport_relaxation",
            "operator": "first-order residual transport",
            "formula": "D q + kappa_q q = S_q",
            "bound": "|q(t)| <= exp(-K)t |q(0)| + integral exp(-K(t-s)) |S_q(s)| ds when kappa_q>=K>0",
            "status": "OPERATOR_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "operator_id": "QOP2279_1_elliptic_stiffness",
            "operator": "local stiffness residual",
            "formula": "L_q q = -nabla_i(Z_q nabla^i q)+M_q^2 q = S_q",
            "bound": "||q|| <= ||L_q^{-1}|| ||S_q|| if Z_q>0, M_q^2>0 and boundary conditions are fixed",
            "status": "STIFFNESS_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "operator_id": "QOP2279_2_local_observable",
            "operator": "observable projection",
            "formula": "R_local=P_obs q",
            "bound": "||R_local|| <= ||P_obs|| ||L_q^{-1}|| ||S_q||",
            "status": "OBSERVABLE_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
    ]


def operator_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "QOI2279_0_phase_lock",
            "input": "P_locked or phase distribution",
            "required_for": "nonzero nonlinear exchange coefficients",
            "current_status": "MISSING_PHASE_LOCK_DISTRIBUTION",
            "valid_for_claim": False,
        },
        {
            "input_id": "QOI2279_1_projectors",
            "input": "P_T/P_R carrier projectors",
            "required_for": "separating nonlinear source into temporal/radial exchange",
            "current_status": "MISSING_CARRIER_PROJECTORS",
            "valid_for_claim": False,
        },
        {
            "input_id": "QOI2279_2_kappa_or_Lq",
            "input": "kappa_q or L_q/G_q",
            "required_for": "finite S_q-to-q_R bound",
            "current_status": "MISSING_Q_RESIDUAL_OPERATOR",
            "valid_for_claim": False,
        },
        {
            "input_id": "QOI2279_3_regularization",
            "input": "n=4/3 nonlinearity regularization near psi=0",
            "required_for": "well-defined phase averages and linearizations",
            "current_status": "MISSING_NONLINEAR_REGULARIZATION",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2279_0_nonlinear_exchange_claim",
            "attempted_claim": "The nonlinear lambda term derives the required temporal/radial exchange.",
            "runner_result": "BLOCKED",
            "blocked_by": "random phases give directed zero; locked-phase coefficients require unsourced distribution/projectors",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2279_1_q_operator_claim",
            "attempted_claim": "A finite q_R residual operator is sourced and coercive.",
            "runner_result": "BLOCKED",
            "blocked_by": "kappa_q/L_q/G_q, positivity, boundary conditions, and observable map are missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2279_2_local_gr_claim",
            "attempted_claim": "MTS has derived the local GR limit.",
            "runner_result": "BLOCKED",
            "blocked_by": "no parent-signed exchange law and no finite q_R bound",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2279_0_random_phase_zero",
            "claim": "independent random phase average does not supply directed exchange",
            "gate_pass": True,
            "reason": "phase parity makes the directed sine/action projection vanish",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2279_1_locked_exchange",
            "claim": "locked nonlinear phase exchange closes EXC2278_3",
            "gate_pass": False,
            "reason": "locked phase distribution/projectors/coefficient values are missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2279_2_q_operator",
            "claim": "S_q is mapped through a sourced q residual operator",
            "gate_pass": False,
            "reason": "kappa_q or L_q/G_q is only a template",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2279_3_local_GR",
            "claim": "derived local GR limit",
            "gate_pass": False,
            "reason": "exchange law or residual bound remains unclosed",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2279_0_gain",
            "decision": "RANDOM_PHASE_NONLINEAR_EXCHANGE_REJECTED",
            "reason": "ordinary smoothing/random phases cannot be the hidden source of the q-zero carrier exchange.",
            "next_action": "do not rely on generic nonlinearity to close q=0.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2279_1_open_route",
            "decision": "LOCKED_PHASE_OR_MEMORY_KERNEL_ROUTE_REMAINS_OPEN",
            "reason": "the corpus has nonlinear phase-dynamics motifs, but the exact locked distribution/coefficient map is absent.",
            "next_action": "derive phase-lock distribution/projectors or demote exchange to residual source.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2279_2_backstop",
            "decision": "Q_OPERATOR_BACKSTOP_STAGED",
            "reason": "if exchange does not close, q_R can still be bounded through Dq+kappa_q q=S_q or L_q q=S_q once the operator is sourced.",
            "next_action": "derive kappa_q/L_q/G_q and boundary/observable maps.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2279_3_next",
            "decision": "PHASE_LOCK_DISTRIBUTION_OR_Q_OPERATOR_OWNER_NEXT",
            "reason": "this is now the least ambiguous next gate.",
            "next_action": "2280-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2279_0_primary",
            "next_target": "2280-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md",
            "script": "scripts/Y5_R2FR_phase_lock_distribution_or_q_residual_operator_owner_2280.py",
            "objective": "derive a parent phase-lock/memory distribution and carrier projectors that make nonlinear exchange nonzero and test EXC2278_3, or derive the owner of kappa_q/L_q/G_q for residual q_R bounds",
            "selection_status": "selected",
            "success_condition": "locked-phase coefficients close q-zero exchange, or a sourced q residual operator maps S_q to q_R without claiming a pass",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_projection": OUTPUTS["nonlinear_projection"],
        "queue_operator": OUTPUTS["q_operator"],
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
            "reason": "branch copy for downstream phase-lock and q-operator audits",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2278_VALIDATION.csv")
    prior_ok = "VAL2278_OVERALL" in prior_text and "PASS" in prior_text

    projection = nonlinear_projection_rows()
    coeffs = exchange_coefficient_rows()
    qop = q_operator_rows()
    inputs = operator_input_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()

    sign_guard = any(row["projection_id"] == "NPP2279_0_variational_sign" for row in projection)
    random_zero = any(row["projection_id"] == "NPP2279_2_independent_phase_zero" for row in projection)
    locked_missing = any(row["coefficient_id"] == "ECL2279_2_locked_phase" and row["current_status"] == "UNSOURCED_COEFFICIENT_FAMILY" for row in coeffs)
    operator_templates = len(qop) >= 3 and all(row["valid_for_claim"] is False for row in qop)
    inputs_missing = all(row["current_status"].startswith("MISSING") and row["valid_for_claim"] is False for row in inputs)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    locked_claim_blocked = any(row["claim_id"] == "CG2279_1_locked_exchange" and row["gate_pass"] is False for row in claims)
    qop_claim_blocked = any(row["claim_id"] == "CG2279_2_q_operator" and row["gate_pass"] is False for row in claims)
    local_claim_blocked = any(row["claim_id"] == "CG2279_3_local_GR" and row["gate_pass"] is False for row in claims)
    random_zero_not_promoted = any(row["claim_id"] == "CG2279_0_random_phase_zero" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    next_selected = any(row["route_id"] == "NEXT2279_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*2279*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2279_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2279_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2279_2_prior_validation", prior_ok, "2278 validation passes"),
        ("VAL2279_3_sign_guard", sign_guard, "nonlinear variational sign guard written"),
        ("VAL2279_4_random_phase_zero", random_zero, "random phase directed exchange zero derived"),
        ("VAL2279_5_locked_missing", locked_missing, "locked phase coefficient family remains unsourced"),
        ("VAL2279_6_operator_templates", operator_templates, "q residual operator templates written nonclaim"),
        ("VAL2279_7_inputs_missing", inputs_missing, "phase/projector/operator inputs remain missing"),
        ("VAL2279_8_refusal_blocks", refusal_blocks, "refusal runner blocks exchange/operator/local-GR claims"),
        ("VAL2279_9_locked_claim_blocked", locked_claim_blocked, "locked nonlinear exchange claim remains blocked"),
        ("VAL2279_10_qop_claim_blocked", qop_claim_blocked, "q residual operator claim remains blocked"),
        ("VAL2279_11_local_claim_blocked", local_claim_blocked, "local GR claim remains blocked"),
        ("VAL2279_12_random_zero_not_promoted", random_zero_not_promoted, "random-phase zero is not promoted to local-GR evidence"),
        ("VAL2279_13_next_selected", next_selected, "2280 target selected"),
        ("VAL2279_14_csv_parse", csvs_parse, "all generated 2279 CSVs parse"),
        ("VAL2279_15_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2279_16_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2279_17_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2279_18_formalization_no_2279", formalization_clean, "formalization-workbench has no 2279 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2279_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2279 rejects random-phase nonlinear averaging as the carrier exchange source, leaves locked-phase exchange and q residual operator unsourced, blocks local-GR claims, and selects 2280",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    projection = nonlinear_projection_rows()
    coeffs = exchange_coefficient_rows()
    qop = q_operator_rows()
    inputs = operator_input_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2279 - Y5/R2FR Nonlinear Phase Exchange Coefficients Or q Residual Operator",
        "",
        "## Verdict",
        "",
        "This checkpoint rules out the easy hope. Generic nonlinear phase averaging does not automatically provide the temporal/radial exchange lock. With independent uniform phases, the directed exchange projection vanishes by parity, so random smoothing cannot be the hidden source of `S_q=0`.",
        "",
        "A locked-phase, memory-kernel, or boundary-correlated distribution could still provide nonzero exchange coefficients, but those objects are not yet sourced. The fallback is now explicit: if exchange does not close, solve a residual equation such as `Dq+kappa_q q=S_q` or `L_q q=S_q`, but `kappa_q/L_q/G_q` are still only templates.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## Nonlinear Phase Projection Audit",
        table(["projection_id", "object", "formula", "result", "meaning", "valid_for_claim"], projection),
        "",
        "## Exchange Coefficient Ledger",
        table(["coefficient_id", "target", "coefficient_formula", "current_status", "missing_inputs", "valid_for_claim"], coeffs),
        "",
        "## q Residual Operator Template",
        table(["operator_id", "operator", "formula", "bound", "status", "valid_for_claim"], qop),
        "",
        "## q Operator Input Contract",
        table(["input_id", "input", "required_for", "current_status", "valid_for_claim"], inputs),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
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
        "This is a useful negative result. The nonlinearity is not magic dust; without phase locking it does not generate the required exchange. The live route is now either a parent phase-lock/memory distribution with projectors, or a real q residual operator. That is a narrower and more testable gap than the old vague coupling problem.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["nonlinear_projection"], nonlinear_projection_rows())
    write_csv(OUTPUTS["exchange_coefficients"], exchange_coefficient_rows())
    write_csv(OUTPUTS["q_operator"], q_operator_rows())
    write_csv(OUTPUTS["operator_inputs"], operator_input_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["nonlinear_projection"], COPY_TARGETS["queue_projection"])
    shutil.copyfile(OUTPUTS["q_operator"], COPY_TARGETS["queue_operator"])
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
