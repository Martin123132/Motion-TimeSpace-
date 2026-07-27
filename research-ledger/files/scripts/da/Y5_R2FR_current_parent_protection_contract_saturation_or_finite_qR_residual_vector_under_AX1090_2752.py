from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2752-Y5-R2FR-current-parent-protection-contract-saturation-or-finite-qR-residual-vector-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_CURRENT_CONTRACT_OR_FINITE_QR_VECTOR_2752"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2752_SOURCE_REGISTER.csv",
    "action": RESIDUALS / "P8_Y5_R2FR_2752_CURRENT_ACTION_CLAUSE_AUDIT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2752_CONTRACT_SATURATION_GATE.csv",
    "finite": RESIDUALS / "P8_Y5_R2FR_2752_FINITE_QR_RESIDUAL_VECTOR.csv",
    "ppn": RESIDUALS / "P8_Y5_R2FR_2752_PPN_RESIDUAL_PROJECTION_VECTOR.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2752_REFUSAL_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2752_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2752_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2752_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2752_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2752_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_local": LOCAL_BOUNDS / "finite_qR_residual_vector_2752_NONCLAIM.csv",
    "contract_source_weight": SOURCE_WEIGHT / "current_parent_contract_saturation_2752_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2752_FIRST_FINITE_QR_COMPONENT_OR_SOURCE_ZERO_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2752_0_2751_doc",
            "description": "2751 loop-breaker handoff into current contract saturation.",
            "source_path": "2751-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar-under-AX1090.md",
            "required_needles": "NEXT2751_0_2752;CON2751_6_joint_contract;VAL2751_OVERALL",
        },
        {
            "source_id": "SRC2752_1_2751_validation",
            "description": "2751 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2751_VALIDATION.csv",
            "required_needles": "VAL2751_OVERALL;True",
        },
        {
            "source_id": "SRC2752_2_2751_contract",
            "description": "2751 joint protection contract clauses.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2751_JOINT_PROTECTION_CONTRACT.csv",
            "required_needles": "CON2751_6_joint_contract;FAIL_CURRENT_CLAIM",
        },
        {
            "source_id": "SRC2752_3_2751_finite",
            "description": "2751 finite q_R/R_AB residual fallback slots.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2751_FINITE_QR_RESIDUAL_FALLBACK_GATE.csv",
            "required_needles": "FQR2751_0_qR_translation;FQR2751_5_tau",
        },
        {
            "source_id": "SRC2752_4_2749_doc",
            "description": "minimal weak-field parent action ansatz and lambda stress gate.",
            "source_path": "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
            "required_needles": "ANS2749_A_EH_lambdaR_silent;EUL2749_2_lambda_stress;VAL2749_OVERALL",
        },
        {
            "source_id": "SRC2752_5_2750_doc",
            "description": "lambda_R stress/constraint-class test.",
            "source_path": "2750-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test-under-AX1090.md",
            "required_needles": "STR2750_5_current;CLASS2750_5_second_class;VAL2750_OVERALL",
        },
        {
            "source_id": "SRC2752_6_2747_doc",
            "description": "q_R/delta_beta PPN control vector.",
            "source_path": "2747-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt-under-AX1090.md",
            "required_needles": "gamma-1 = q_R;Delta Mercury / Delta Mercury_GR = (2 q_R - delta_beta)/3;VAL2747_OVERALL",
        },
        {
            "source_id": "SRC2752_7_2716_doc",
            "description": "finite R_AB operator law and source-ready symbolic scaffold.",
            "source_path": "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            "required_needles": "LAW2716_0_finite_action;FZR2716_2_JEFF;VAL2716_OVERALL",
        },
        {
            "source_id": "SRC2752_8_2732_doc",
            "description": "anti-circling local-GR route rollup and finite residual route status.",
            "source_path": "2732-Y5-R2FR-local-GR-route-rollup-after-memory-closure-only-or-next-derivation-branch.md",
            "required_needles": "ROUTE2732_4_RAB_finite_residual;NC2732_3_Khat;VAL2732_OVERALL",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def action_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ACT2752_0_EH_core",
            "S_EH[g_obs]",
            "supplies standard GR weak-field operator if adopted",
            "CONDITIONAL_PASS_WITHIN_ANSATZ",
            "not an MTS derivation unless g_obs/readout/source ownership are parent-signed",
        ),
        (
            "ACT2752_1_matter_core",
            "S_matter[g_obs, psi]",
            "would give universal matter descent if g_obs is the only matter geometry",
            "UNSIGNED",
            "no theorem proves matter sees no R_AB/q marker, source prefactor, or worldtube charge",
        ),
        (
            "ACT2752_2_lambda_block",
            "int sqrt(-g) Lambda_R R_AB or Lambda_R[R_AB-C_AB]",
            "formally enforces R_AB=0/compatibility",
            "FORMAL_PASS_NOT_ORIGIN",
            "bare insertion does not provide parent sort, zero stress, or no derivative grammar",
        ),
        (
            "ACT2752_3_silent_sector",
            "S_silent[Phi,g_obs]",
            "could hide non-GR sectors if truly stress/source/readout silent",
            "UNSIGNED",
            "silence is asserted as a needed clause, not derived",
        ),
        (
            "ACT2752_4_boundary",
            "S_boundary",
            "must carry no R_AB boundary charge after elimination",
            "UNSIGNED",
            "source-worldtube/corner variational class remains open",
        ),
        (
            "ACT2752_5_current_action_verdict",
            "current minimal parent action",
            "useful conditional ansatz only",
            "NOT_ADOPTED_AS_PARENT_DERIVATION",
            "fails saturation because core protective clauses are unsigned",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "action_id": aid,
                "action_piece": piece,
                "what_it_would_supply": supply,
                "current_status": status,
                "blocker": blocker,
            }
        )
        for aid, piece, supply, status, blocker in specs
    ]


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SAT2752_0_parent_sorts",
            "R_AB/Lambda_R are algebraic compatibility auxiliaries",
            "FAIL",
            "2750/2751 retain candidate sort but no parent source signs it",
            "finite R_AB scalar countermodel remains legal",
        ),
        (
            "SAT2752_1_action_image",
            "ParentGenerate contains no independent R_AB derivative/source/counterterm slots",
            "FAIL",
            "current ansatz omits those slots by construction but does not prove the inventory exhaustive",
            "Z_R, J_eff, and tails remain live",
        ),
        (
            "SAT2752_2_matter_descent",
            "delta S_matter/delta R_AB=0",
            "FAIL",
            "universal g_obs matter action is not parent-derived and source markers/worldtube charge remain open",
            "J_R or beta_source/test can survive",
        ),
        (
            "SAT2752_3_boundary_descent",
            "delta B/delta R_AB=0 and Q_R/Pi_R vanish",
            "FAIL",
            "boundary/corner/source-support theorem missing",
            "exterior q_R hair can be set by boundary data",
        ),
        (
            "SAT2752_4_readout_closure",
            "readout-after-variation does not regenerate R_AB/q_R tails",
            "FAIL",
            "readout closure and hidden projector/history tails remain unproved",
            "finite tau/readout residuals remain possible",
        ),
        (
            "SAT2752_5_operator_exclusion",
            "D R_AB, D Lambda_R, G_vert, and boundary derivative terms are forbidden",
            "FAIL",
            "no-derivative grammar is exact conditional only",
            "finite Z_R branch remains mandatory fallback",
        ),
        (
            "SAT2752_6_EH_source_normalization",
            "EH/Newton coefficient and source normalization are parent-owned before fitting",
            "CONDITIONAL_ONLY",
            "EH core can give the left-hand operator if adopted, but kappa/source/readout ownership is not signed here",
            "Newton lane cannot be used to hide q_R source terms",
        ),
        (
            "SAT2752_7_joint_verdict",
            "all clauses close in one current parent action",
            "FAIL_CURRENT_CLAIM",
            "at least six claim-making clauses remain unsigned",
            "emit finite q_R/R_AB residual vector and keep local-GR claim blocked",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "saturation_id": sid,
                "required_clause": clause,
                "gate_result": result,
                "reason": reason,
                "effect_if_missing": effect,
                "closed_by_current_action": False,
            }
        )
        for sid, clause, result, reason, effect in specs
    ]


def finite_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "QRV2752_0_qR",
            "q_R",
            "linear reciprocal PPN residual",
            "gamma-1=q_R",
            "dimensionless",
            "Cassini/gamma;light;Shapiro;Mercury",
            "TRANSLATION_READY_VALUE_NOT_PREDICTED",
            "derive q_R=0 or source finite q_R through R_AB profile",
        ),
        (
            "QRV2752_1_delta_beta",
            "delta_beta",
            "second-order PPN residual",
            "beta-1=delta_beta",
            "dimensionless",
            "Mercury;PPN",
            "TRANSLATION_READY_VALUE_NOT_PREDICTED",
            "derive beta=1 or source finite second-order coefficient",
        ),
        (
            "QRV2752_2_mercury_combo",
            "2 q_R - delta_beta",
            "perihelion combination",
            "DeltaMercury/DeltaMercury_GR=(2 q_R-delta_beta)/3",
            "dimensionless",
            "Mercury perihelion",
            "CONTROL_COMBO_READY_NONCLAIM",
            "do not treat Mercury degeneracy as local-GR proof",
        ),
        (
            "QRV2752_3_ZR",
            "Z_R",
            "finite reciprocal gradient stiffness",
            "coefficient of 0.5 h^ij D_iR_ABD_jR_AB",
            "parent action density units missing",
            "R10;PPN;clock;orbital",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_COEFFICIENT",
            "source/derive Z_R or keep q_R closure-only",
        ),
        (
            "QRV2752_4_MR2",
            "M_R^2",
            "finite reciprocal mass/Hessian",
            "ell_R=sqrt(Z_R/M_R^2)",
            "same frame as Z_R over length^2",
            "R10;PPN;clock;orbital",
            "MISSING_RANGE_HESSIAN",
            "source/derive mass gap or no finite-range score is possible",
        ),
        (
            "QRV2752_5_Jeff",
            "J_eff",
            "effective source after matter/boundary/readout leakage",
            "(-Z_R Delta_h + M_R^2)R_AB=J_eff",
            "Euler source conjugate to dimensionless R_AB",
            "all local arenas",
            "MISSING_SOURCE_ZERO_OR_COMPONENT_BOUND",
            "split into matter, boundary, readout/history, projector, constants",
        ),
        (
            "QRV2752_6_boundary",
            "B_R/Q_R/Pi_R",
            "boundary and source-worldtube charge",
            "boundary data in Green solution for R_AB",
            "boundary momentum/charge normalization missing",
            "PPN;orbital;R10",
            "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "derive no-charge theorem or source finite boundary row",
        ),
        (
            "QRV2752_7_tau_vector",
            "tau_PPN/tau_R10/tau_clock/tau_orbital",
            "arena projection kernels",
            "observable_i=tau_i R_AB_profile or PPN dictionary when linearized",
            "arena-specific",
            "PPN;R10;clock;orbital",
            "MISSING_PROJECTION_KERNELS_EXCEPT_PPN_CONTROL",
            "fill projection kernels only after internal coefficient/source side exists",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "vector_id": vid,
                "symbol": symbol,
                "role": role,
                "formula_or_mapping": formula,
                "units_status": units,
                "observable_link": observable,
                "current_status": status,
                "next_input_needed": need,
            }
        )
        for vid, symbol, role, formula, units, observable, status, need in specs
    ]


def ppn_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPN2752_0_gamma", "gamma_minus_1", "q_R", "dimensionless", "Cassini/gamma", "CONTROL_TRANSLATION_READY"),
        ("PPN2752_1_beta", "beta_minus_1", "delta_beta", "dimensionless", "PPN beta/Mercury", "CONTROL_TRANSLATION_READY"),
        ("PPN2752_2_mercury_fraction", "DeltaMercury_over_GR", "(2 q_R - delta_beta)/3", "dimensionless", "Mercury perihelion", "CONTROL_COMBO_READY"),
        ("PPN2752_3_light", "light_bending_residual", "theta_GR*q_R/2", "arcsec", "solar light bending", "CONTROL_TRANSLATION_READY"),
        ("PPN2752_4_shapiro", "Shapiro_residual", "delay_GR*q_R/2", "microseconds", "Shapiro delay", "CONTROL_TRANSLATION_READY"),
        ("PPN2752_5_verdict", "PPN vector score", "requires numeric/theorem-zero q_R and delta_beta", "mixed", "PPN", "NOT_SCORE_READY"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "projection_id": pid,
                "observable": observable,
                "projection_formula": formula,
                "units": units,
                "arena": arena,
                "status": status,
            }
        )
        for pid, observable, formula, units, arena, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2752_0_sources", "load 2751/2749/2750/2747/2716/2732 sources", "PASS", "all required source needles found"),
        ("RUN2752_1_contract", "current action saturates joint protection contract", "FAIL_CURRENT_CLAIM", "parent sorts, action-image, matter, boundary, readout, and operator clauses remain unsigned"),
        ("RUN2752_2_EH_core", "EH weak-field core", "PASS_CONDITIONAL_NOT_MTS_DERIVATION", "can serve as control core only if action/readout/source ownership is signed"),
        ("RUN2752_3_finite_vector", "finite q_R/R_AB vector emitted", "PASS_NONCLAIM_VECTOR", "symbolic vector lists all live residual components and missing inputs"),
        ("RUN2752_4_ppn_projection", "PPN projection", "PASS_CONTROL_ONLY", "q_R/delta_beta projection is ready but values are missing"),
        ("RUN2752_5_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "contract failed and finite vector is not score-ready"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "runner_id": rid,
                "test": test,
                "current_status": status,
                "detail": detail,
            }
        )
        for rid, test, status, detail in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2752_0_contract", "current parent action signs local protection contract", "BLOCKED_NO_CLAIM", "joint contract saturation fails"),
        ("GATE2752_1_qR_zero", "q_R=0 derived", "BLOCKED_NO_CLAIM", "R_AB=O(L^2) not parent-derived"),
        ("GATE2752_2_beta_zero", "delta_beta=0 derived", "BLOCKED_NO_CLAIM", "second-order beta completion not parent-derived"),
        ("GATE2752_3_finite_score", "finite residual vector score-ready", "BLOCKED_NO_CLAIM", "Z_R/M_R^2/J_eff/boundary/tau values missing"),
        ("GATE2752_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "neither exact theorem nor finite bound pass exists"),
        ("GATE2752_5_public", "public/GitHub update", "BLOCKED_PRIVATE", "not requested and not claim-safe"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2752_0_contract",
            "current contract saturation",
            "FAIL_CURRENT_CLAIM",
            "the minimal action remains a conditional ansatz, not a parent-signed protection theorem",
        ),
        (
            "DEC2752_1_finite_vector",
            "finite q_R/R_AB vector",
            "EMIT_NONCLAIM_VECTOR",
            "all residual components are now listed explicitly so the branch cannot hide in q_R=0 language",
        ),
        (
            "DEC2752_2_ppn",
            "PPN control lane",
            "USE_FIRST_FOR_BOUNDS_ONCE_QR_EXISTS",
            "q_R/delta_beta map is the cleanest first empirical pressure test, but the theory still lacks a value",
        ),
        (
            "DEC2752_3_next",
            "next target",
            "NEXT_2753_FIRST_FINITE_QR_COMPONENT_BOUND_OR_SOURCE_ZERO",
            "attack the first finite residual component: derive q_R/source-zero from J_eff, or create a source-ready finite q_R component row without scoring it",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2752_0_2753",
                "status": "selected_primary",
                "target_doc": "2753-Y5-R2FR-first-finite-qR-component-bound-or-source-zero-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_finite_qR_component_bound_or_source_zero_theorem_under_AX1090_2753.py",
                "mission": "take the finite q_R/R_AB vector seriously: first try source-zero for J_eff/q_R; if not derivable, create the first source-ready nonclaim finite q_R component row tied to the 2747 PPN control bounds",
                "acceptance": "either a parent-signed source-zero/q_R-zero theorem appears, or q_R/J_eff gains a structured row with missing source, units, normalization, and projection inputs named explicitly",
                "forbidden": "do not claim local GR; do not treat q_R=0 as closure; do not score placeholders; do not edit formalization-workbench; no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2752_0_finite_local", "source_table": rel(OUTPUTS["finite"]), "copy_path": rel(BRANCH_OUTPUTS["finite_local"]), "purpose": "local-bound finite qR/RAB vector", "exists": BRANCH_OUTPUTS["finite_local"].exists()}),
        nonclaim({"copy_id": "BR2752_1_contract_source_weight", "source_table": rel(OUTPUTS["contract"]), "copy_path": rel(BRANCH_OUTPUTS["contract_source_weight"]), "purpose": "source-weight contract saturation failure", "exists": BRANCH_OUTPUTS["contract_source_weight"].exists()}),
        nonclaim({"copy_id": "BR2752_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for first finite qR component/source-zero", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    action_ok = any(row["action_id"] == "ACT2752_5_current_action_verdict" and row["current_status"] == "NOT_ADOPTED_AS_PARENT_DERIVATION" for row in action)
    contract_ok = any(row["saturation_id"] == "SAT2752_7_joint_verdict" and row["gate_result"] == "FAIL_CURRENT_CLAIM" for row in contract) and all(row["closed_by_current_action"] is False for row in contract)
    finite_ok = {"q_R", "delta_beta", "Z_R", "M_R^2", "J_eff", "B_R/Q_R/Pi_R", "tau_PPN/tau_R10/tau_clock/tau_orbital"}.issubset({row["symbol"] for row in finite})
    ppn_ok = any(row["projection_id"] == "PPN2752_0_gamma" and row["projection_formula"] == "q_R" for row in ppn) and any(row["projection_id"] == "PPN2752_5_verdict" and row["status"] == "NOT_SCORE_READY" for row in ppn)
    runner_ok = any(row["runner_id"] == "RUN2752_1_contract" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in runner) and any(row["runner_id"] == "RUN2752_3_finite_vector" and row["current_status"] == "PASS_NONCLAIM_VECTOR" for row in runner)
    gate_ok = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in gates) and any(row["claim_gate_id"] == "GATE2752_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    decision_ok = any(row["decision_id"] == "DEC2752_3_next" and row["result"] == "NEXT_2753_FIRST_FINITE_QR_COMPONENT_BOUND_OR_SOURCE_ZERO" for row in decisions)
    next_ok = next_target[0]["selected"] is True and "2753" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [action, contract, finite, ppn, runner, gates, decisions, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2752_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_1_current_action", "passed": action_ok, "detail": "current action remains conditional/not adopted", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_2_contract_fails", "passed": contract_ok, "detail": "joint protection contract saturation fails current claim", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_3_finite_vector", "passed": finite_ok, "detail": "finite qR/RAB residual vector contains required slots", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_4_ppn_projection", "passed": ppn_ok, "detail": "PPN qR/delta_beta projection vector is control-ready but not score-ready", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_5_runner", "passed": runner_ok, "detail": "runner blocks contract claim and emits nonclaim vector", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_6_claim_gates", "passed": gate_ok and no_claim_flags_ok, "detail": "claim gates remain closed and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_7_decision_next", "passed": decision_ok and next_ok, "detail": "2753 first finite qR component/source-zero selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2752_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2752_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2752_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2752 tests current parent protection saturation, rejects local-GR promotion, emits finite qR/RAB residual vector, and selects first finite qR component/source-zero next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2752 - Y5 R2/f(R): Current Parent Protection Contract Saturation Or Finite q_R Residual Vector Under AX1090

Status: `Y5_R2FR_2752_current_contract_fails_finite_qR_vector_emitted_nonclaim`

## Private Verdict

2752 takes the non-circular fork selected by 2751.

The current minimal parent action is useful, but it does not saturate the protection contract. The EH core is a good control backbone, and the `Lambda_R R_AB` block gives a formal constraint equation, but the parent action still does not sign the clauses that would make the local-GR branch a derivation: parent sorts, action-image exhaustion, matter descent, boundary descent, readout closure, and operator exclusion.

So this checkpoint refuses to spend local-GR credit. Instead it emits the finite residual vector that must be bounded or theorem-zeroed:

`q_R`, `delta_beta`, `Z_R`, `M_R^2`, `J_eff`, `B_R/Q_R/Pi_R`, and `tau_i`.

The cleanest first empirical/control lane is still PPN because `gamma-1=q_R`, `beta-1=delta_beta`, and `DeltaMercury/DeltaMercury_GR=(2 q_R-delta_beta)/3` are already available from 2747. But the theory has not predicted `q_R` or `delta_beta`; the vector is therefore nonclaim.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Current Action Clause Audit

{markdown_table(data["action"], ["action_id", "action_piece", "what_it_would_supply", "current_status", "blocker", "valid_for_claim"])}

## Contract Saturation Gate

{markdown_table(data["contract"], ["saturation_id", "required_clause", "gate_result", "reason", "effect_if_missing", "closed_by_current_action", "valid_for_claim"])}

## Finite q_R/R_AB Residual Vector

{markdown_table(data["finite"], ["vector_id", "symbol", "role", "formula_or_mapping", "units_status", "observable_link", "current_status", "next_input_needed", "valid_for_claim"])}

## PPN Residual Projection Vector

{markdown_table(data["ppn"], ["projection_id", "observable", "projection_formula", "units", "arena", "status", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the right kind of unpleasant result. The current action does not yet give us derived local GR, but it now tells us exactly what the finite failure mode is. That is better than a foggy closure: either 2753 kills the first source component by theorem, or it becomes the first bounded q_R row. No magic, no embarrassment, no hidden fitted-GR backfill.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    action = action_rows()
    contract = contract_rows()
    finite = finite_rows()
    ppn = ppn_rows()
    runner = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["action"], action)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["finite_local"], finite)
    write_csv(BRANCH_OUTPUTS["contract_source_weight"], contract)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, action, contract, finite, ppn, runner, gates, decisions, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "action": action,
        "contract": contract,
        "finite": finite,
        "ppn": ppn,
        "runner": runner,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2752 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
