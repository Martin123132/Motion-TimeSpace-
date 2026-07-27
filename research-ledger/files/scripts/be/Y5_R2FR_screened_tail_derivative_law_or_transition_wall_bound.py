from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1746"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1746 - Screened Tail Derivative Law Or Finite Transition Wall Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1746_0_1745_doc",
        "source_key": "1745_tail_handoff",
        "source_path": ROOT / "1745-Y5-R2FR-fixed-point-double-zero-for-pL-pT-or-DeltaK-component-row.md",
        "needles": ["TAIL_DERIVATIVE_LAW_IS_NEXT_DOMINO", "transition-wall countermodel"],
    },
    {
        "source_id": "SRC1746_1_1378_derivation",
        "source_key": "1378_transition_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
        "needles": ["DER1378_4_exponential_support_law", "CONDITIONAL_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1746_2_1378_branch",
        "source_key": "1378_gradient_branch",
        "source_path": RESIDUALS / "P8_Y5_R10_1378_CONDITIONAL_GRADIENT_RELAXATION_BRANCH.csv",
        "needles": ["GRB1378_2_support_law", "Delta_grad_m<=A_S U_B/ell_tr"],
    },
    {
        "source_id": "SRC1746_3_1379_doc",
        "source_key": "1379_parent_signature",
        "source_path": ROOT / "1379-Y5-R10-RAB-gradient-completion-parent-signature-or-transition-closure-runner.md",
        "needles": ["GPA1379_8_verdict", "closure-only runner schema"],
    },
    {
        "source_id": "SRC1746_4_1379_audit",
        "source_key": "1379_gradient_parent_signature_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        "needles": ["GPA1379_8_verdict", "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW"],
    },
    {
        "source_id": "SRC1746_5_1379_formula",
        "source_key": "1379_formula_feed",
        "source_path": RESIDUALS / "P8_Y5_R10_1379_CONDITIONAL_FORMULA_FEED.csv",
        "needles": ["CFF1379_1_support", "Delta_grad_m<=A_S U_B/ell_tr"],
    },
    {
        "source_id": "SRC1746_6_1592_theorem",
        "source_key": "1592_canonical_transition_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv",
        "needles": ["CTT1592_2_static_exterior_solution", "CTT1592_3_amplitude_law"],
    },
    {
        "source_id": "SRC1746_7_1592_source_pack",
        "source_key": "1592_canonical_source_acquisition",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1592_QNORM_CANONICAL_SOURCE_ACQUISITION.csv",
        "needles": ["CSA1592_0_mu_m2", "CSA1592_11_boundary_shell"],
    },
    {
        "source_id": "SRC1746_8_1534_nohair",
        "source_key": "1534_positive_operator_nohair",
        "source_path": ROOT / "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md",
        "needles": ["NH1534_6_verdict", "positive source-free operator"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_SOURCE_REGISTER.csv",
    "tail_derivative_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
    "parent_signature_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_PARENT_SIGNATURE_GATE.csv",
    "transition_wall_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_TRANSITION_WALL_BOUND.csv",
    "canonical_source_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1746_VALIDATION.csv",
}


COPY_MAP = {
    "tail_derivative_theorem": "R2FR_1746_TAIL_DERIVATIVE_THEOREM.csv",
    "parent_signature_gate": "R2FR_1746_PARENT_SIGNATURE_GATE.csv",
    "transition_wall_bound": "R2FR_1746_TRANSITION_WALL_BOUND.csv",
    "canonical_source_rows": "R2FR_1746_CANONICAL_SOURCE_ROWS.csv",
    "runner_refusal": "R2FR_1746_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1746_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1746_CLAIM_GATE.csv",
    "next_target": "R2FR_1746_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def tail_derivative_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "TD1746_0_target_condition",
            "claim": "the q_loc-safe scalar double-zero branch needs a tail derivative law",
            "calculation": "if f=F(D_L^2), then nabla f=F'(D_L^2) 2 D_L nabla D_L; p=2 gradient needs |nabla D_L|=O(U_B/L_tr)",
            "result": "TAIL_DERIVATIVE_CONDITION_IDENTIFIED",
            "status": "EXACT_REQUIREMENT",
            "missing_to_promote": "MISSING_PARENT_DERIVED_D_L_TAIL",
        },
        {
            "theorem_id": "TD1746_1_exponential_tail_solution",
            "claim": "the conditional gradient-relaxation branch satisfies the tail derivative law",
            "calculation": "from kappa_m Box eta - L0^-2 F2 eta=0, static decaying eta=A_S exp(-d/ell_tr), U_B=exp(-d/ell_tr), so |nabla U_B|=U_B/ell_tr",
            "result": "SCREENED_TAIL_DERIVATIVE_LAW_DERIVED_CONDITIONALLY",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "missing_to_promote": "MISSING_PARENT_KAPPA_OR_MU;MISSING_FIELD_STATUS;MISSING_SOURCE_SILENCE;MISSING_BOUNDARY_CLASS",
        },
        {
            "theorem_id": "TD1746_2_canonical_gap_rewrite",
            "claim": "the clean invariant version uses mu_m^2 and ell_tr=1/sqrt(mu_m^2)",
            "calculation": "canonical quadratic branch gives (Box-mu_m^2)phi=0 in source-free exterior; phi<=Phi_S exp(-d/ell_tr), |nabla phi|<=Phi_S exp(-d/ell_tr)/ell_tr plus corrections",
            "result": "KAPPA_F2_SPLIT_REPLACED_BY_CANONICAL_GAP",
            "status": "CONDITIONAL_CANONICAL_THEOREM_NONCLAIM",
            "missing_to_promote": "MISSING_SOURCE_BACKED_MU_M2;MISSING_PHI_S;MISSING_DOMAIN_DISTANCE;MISSING_CORRECTIONS",
        },
        {
            "theorem_id": "TD1746_3_positive_operator_generalization",
            "claim": "positive source-free operators support exponential/Agmon-type local decay",
            "calculation": "a coercive massive operator with no source, no zero mode and controlled boundary data gives decay and derivative estimates with constants set by the gap/domain",
            "result": "GENERAL_ROUTE_EXISTS_BUT_CONSTANTS_UNSIGNED",
            "status": "THEOREM_ROUTE_NOT_PARENT_SIGNED",
            "missing_to_promote": "MISSING_OPERATOR_GAP;MISSING_NO_SOURCE;MISSING_NO_ZERO_MODE;MISSING_BOUNDARY_DATA",
        },
        {
            "theorem_id": "TD1746_4_wall_counterbranch",
            "claim": "if local support intersects a sharp transition wall, p=2 gradient still fails",
            "calculation": "with |nabla U_B|=O(1/L_wall), nabla f=O(U_B/L_wall); this is a retained finite wall residual, not a local-GR proof",
            "result": "FINITE_TRANSITION_WALL_BOUND_REQUIRED_IF_TAIL_NOT_SIGNED",
            "status": "NO_GO_GUARD_AND_FALLBACK",
            "missing_to_promote": "MISSING_WALL_WIDTH;MISSING_SUPPORT_OVERLAP;MISSING_PROJECTION_NORM;MISSING_AMPLITUDE",
        },
    ]
    for row in rows:
        row.update({"branch_id": BRANCH_ID, "valid_for_claim": no(), "claim_allowed": no(), "score_ready": no()})
    return rows


def parent_signature_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PSG1746_0_action_slot", "parent action contains the canonical scalar-memory kinetic slot", "CANDIDATE_ACTION_SLOT_NOT_PARENT_SIGNED", "tail theorem remains closure-only"),
        ("PSG1746_1_field_status", "phi/eta is a parent varied field before projection/readout", "FIELD_STATUS_CANDIDATE_NOT_SIGNED", "Euler equation cannot be adopted as corpus theorem"),
        ("PSG1746_2_mu_gap", "mu_m^2>0 is source-backed with units and sign", "MISSING_SOURCE_BACKED_CANONICAL_GAP", "ell_tr and tail profile cannot score"),
        ("PSG1746_3_source_silence", "J_c and residual source terms vanish or are bounded", "EULER_FORM_DERIVED_SOURCE_MAP_MISSING", "source-supported hair can survive"),
        ("PSG1746_4_boundary_shell", "boundary/shell terms are no-flux, projected out, or explicitly bounded", "MISSING_SHELL_CLOSURE", "wall/boundary residual may dominate"),
        ("PSG1746_5_stress_routing", "gradient stress is retained or separately bounded", "STRESS_ROUTING_GUARD_REQUIRED", "cannot use gradient term and delete its stress"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        }
        for gate_id, requirement, status, effect in rows
    ]


def transition_wall_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "TWB1746_0_wall_gradient_residual",
            "residual": "Q_wall_grad",
            "bound_form": "Q_wall_grad <= C_proj C_F A_S^2 U_B |nabla U_B| <= C_wall A_S^2 U_B/L_wall",
            "zero_or_small_route": "prove local test support lies in exponential tail, or source L_wall/support-overlap bound",
            "needed_inputs": "MISSING_C_PROJ;MISSING_C_F;MISSING_A_S;MISSING_U_B;MISSING_L_WALL;MISSING_SUPPORT_OVERLAP",
            "status": "BOUND_FORM_ONLY_NONCLAIM",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "TWB1746_1_shell_boundary_residual",
            "residual": "Q_shell_boundary",
            "bound_form": "Q_shell_boundary <= C_shell A_B U_B^pB/(L0^2 L_wall) + retained boundary/projector terms",
            "zero_or_small_route": "exact projector/no-flux theorem or finite shell contribution",
            "needed_inputs": "MISSING_C_SHELL;MISSING_A_B;MISSING_pB;MISSING_L0;MISSING_BOUNDARY_PROJECTOR",
            "status": "BOUND_FORM_ONLY_NONCLAIM",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
    ]


def canonical_source_rows() -> list[dict[str, Any]]:
    rows = [
        ("CSR1746_0_mu_m2", "mu_m^2", "canonical mass gap; ell_tr=1/sqrt(mu_m^2)", "MISSING_SOURCE_BACKED_CANONICAL_GAP"),
        ("CSR1746_1_Phi_S", "Phi_S", "boundary/source amplitude for exterior tail", "MISSING_CANONICAL_AMPLITUDE"),
        ("CSR1746_2_domain_distance", "d", "distance from local support to active transition/source boundary", "MISSING_DOMAIN_DISTANCE"),
        ("CSR1746_3_beta_source_test", "beta_source*beta_test", "finite exchange coupling product if source not zero", "PRODUCT_LAW_READY_VALUES_MISSING"),
        ("CSR1746_4_epsilon_tail", "epsilon_tail", "hidden frame/readout/boundary/non-EH tail envelope", "MISSING_TAIL_ENVELOPE"),
        ("CSR1746_5_projection_norms", "N_div;N_G;N_D;A_ref", "operator/projection/normalization bridge to observables", "MISSING_OPERATOR_PROJECTION_NORMS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "current_status": status,
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        }
        for row_id, quantity, definition, status in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1746_0_tail_law_adoption",
            "runner": "screened-tail derivative law",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "tail law is conditionally derived but not parent-signed through action/field/gap/source/boundary package",
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1746_1_wall_bound",
            "runner": "finite transition-wall residual",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "wall bound has no sourced amplitudes, support overlap, projection norms or arena thresholds",
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1746_0_tail_math",
            "decision": "TAIL_DERIVATIVE_LAW_DERIVED_CONDITIONALLY",
            "reason": "the exponential/canonical massive branch gives |nabla U_B|=U_B/ell_tr and therefore preserves p=2 gradients",
            "next_action": "parent-sign the canonical gap/source/boundary package before using it as a live local branch",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1746_1_not_claimed",
            "decision": "DO_NOT_PROMOTE_LOCAL_GR",
            "reason": "the exact law is conditional; source coupling, boundary shell, stress routing and projection norms are not closed",
            "next_action": "keep runners blocked and stage source rows",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1746_2_best_next",
            "decision": "TARGET_PARENT_GAP_COUPLING_OR_WALL_BOUND",
            "reason": "the next falsifiable hinge is mu_m^2/Phi_S/source-silence/boundary-shell, not more words about screening",
            "next_action": "try to source/derive canonical gap and coupling-zero package, or fill finite wall-bound rows",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("GATE1746_0_tail_law", "screened-tail derivative law is parent-signed", "BLOCKED_PARENT_SIGNATURE"),
        ("GATE1746_1_pL_pT_gradient", "pL/pT gradient power can be promoted to 2", "BLOCKED_SOURCE_BOUNDARY_PACKAGE"),
        ("GATE1746_2_wall_bound", "transition-wall residual is bounded below local tests", "BLOCKED_VALUES_MISSING"),
        ("GATE1746_3_local_GR", "local GR/Newton/PPN branch is derived", "BLOCKED_RESIDUAL_VECTOR_INCOMPLETE"),
        ("GATE1746_4_empirical", "R10/WEP/clock/orbital scoring can run", "BLOCKED_NONCLAIM_INPUTS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": blocker,
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        }
        for gate_id, claim, blocker in claims
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1746_0_primary",
            "next_target": "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md",
            "script": "scripts/Y5_R2FR_canonical_gap_coupling_source_silence_or_wall_bound_row.py",
            "objective": "try to parent-sign/source mu_m^2, Phi_S, beta_source beta_test, source silence, and boundary-shell clauses; otherwise fill finite wall-bound rows",
            "success_condition": "source-backed nonclaim canonical rows or exact zero theorems for the gap/coupling/source package, with wall-bound fallback retained",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1746_1_DeltaK",
            "next_target": "1747b-Y5-R2FR-DeltaK-component-operator-norm-bound.md",
            "script": "scripts/Y5_R2FR_DeltaK_component_operator_norm_bound.py",
            "objective": "continue the retained Khat/DeltaK residual path if the canonical source package remains blocked",
            "success_condition": "first source-backed S_Delta operator norm row or a stricter refusal ledger",
            "selection_status": "held_fallback",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "tail_derivative_theorem": tail_derivative_theorem_rows(),
        "parent_signature_gate": parent_signature_gate_rows(),
        "transition_wall_bound": transition_wall_bound_rows(),
        "canonical_source_rows": canonical_source_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1746_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1746_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"claim_allowed", "gate_pass", "score_allowed", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {"claim_allowed", "gate_pass", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1746_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1746_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1746*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    theorem = rows_map["tail_derivative_theorem"]
    gates = rows_map["parent_signature_gate"]
    walls = rows_map["transition_wall_bound"]
    canonical = rows_map["canonical_source_rows"]
    runners = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1746_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1746_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more required source needles missing"),
        check("VAL1746_2_tail_law_conditional", any(row["theorem_id"] == "TD1746_1_exponential_tail_solution" and row["result"] == "SCREENED_TAIL_DERIVATIVE_LAW_DERIVED_CONDITIONALLY" for row in theorem), "exponential tail derivative law is conditionally derived", "tail derivative theorem missing"),
        check("VAL1746_3_canonical_gap", any(row["theorem_id"] == "TD1746_2_canonical_gap_rewrite" for row in theorem), "canonical gap rewrite included", "canonical gap rewrite missing"),
        check("VAL1746_4_wall_guard", any(row["theorem_id"] == "TD1746_4_wall_counterbranch" for row in theorem), "finite wall counterbranch retained", "wall counterbranch missing"),
        check("VAL1746_5_parent_gates_blocked", all(row["claim_allowed"] == "False" and row["score_ready"] == "False" for row in gates), "parent signature gates remain nonclaim", "parent signature gate opened"),
        check("VAL1746_6_wall_bounds_nonclaim", all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in walls), "wall bound rows remain nonclaim", "wall bound row became claim-ready"),
        check("VAL1746_7_canonical_sources_present", {"mu_m^2", "Phi_S", "beta_source*beta_test"}.issubset({row["quantity"] for row in canonical}), "canonical source rows include gap/amplitude/coupling", "canonical source rows incomplete"),
        check("VAL1746_8_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runners), "all claim runners refuse", "one or more runners opened a claim"),
        check("VAL1746_9_decision_next", any(row["decision_id"] == "DEC1746_2_best_next" and row["decision"] == "TARGET_PARENT_GAP_COUPLING_OR_WALL_BOUND" for row in decisions), "decision selects parent gap/coupling or wall bound", "decision next route missing"),
        check("VAL1746_10_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1746_11_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1746_12_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked claim-ready or score-ready", "a missing row is marked ready"),
        check("VAL1746_13_next_selected", any(row["route_id"] == "NEXT1746_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects canonical gap/coupling source package", "next target missing selected primary route"),
        check("VAL1746_14_csv_parse", parsed_ok, "all generated 1746 CSVs parse", "one or more generated 1746 CSVs failed to parse"),
        check("VAL1746_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1746_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1746_17_formalization_untouched", formalization_untouched(), "no 1746 outputs found under formalization-workbench", "1746 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1746_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1746 screened-tail derivative law or finite wall-bound validation" if overall else "one or more 1746 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- The tail law itself is derivable: the exponential/canonical massive branch gives `|nabla U_B|=U_B/ell_tr`, which is exactly the condition 1745 needed.",
        "- This is real mathematical progress, but not a live local-GR claim because the parent action has not signed the canonical gap, field status, source silence, boundary/shell class, stress routing, or projection norms.",
        "- The useful canonical language is now `mu_m^2`, `ell_tr=1/sqrt(mu_m^2)`, `Phi_S`, `beta_source beta_test`, and tail envelopes; this is cleaner than arbitrary `kappa_m/F2` bookkeeping.",
        "- If the parent package fails, the correct fallback is a finite transition-wall residual bound, not a hidden plateau axiom.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Tail Derivative Theorem",
        markdown_table(rows_map["tail_derivative_theorem"], ["theorem_id", "claim", "result", "status", "missing_to_promote"]),
        "",
        "## Parent Signature Gates",
        markdown_table(rows_map["parent_signature_gate"], ["gate_id", "requirement", "current_status", "claim_effect"]),
        "",
        "## Transition Wall Bounds",
        markdown_table(rows_map["transition_wall_bound"], ["bound_id", "residual", "bound_form", "status", "needed_inputs"]),
        "",
        "## Canonical Source Rows",
        markdown_table(rows_map["canonical_source_rows"], ["row_id", "quantity", "definition", "current_status"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The grim bit got less grim here. The gradient trap is not fatal if the local branch really is a massive screened tail: the derivative law follows automatically. The hard part is now ownership, not calculus: the same parent action must supply the gap, silence the source/coupling legs or bound them, keep the boundary shell honest, and retain the stress it introduced.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1746_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1746 validation FAIL")
    print("1746 validation PASS")


if __name__ == "__main__":
    main()
