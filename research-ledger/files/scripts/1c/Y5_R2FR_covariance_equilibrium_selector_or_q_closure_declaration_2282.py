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

BRANCH_ID = "MTS_R2FR_COVARIANCE_EQUILIBRIUM_SELECTOR_OR_Q_CLOSURE_2282"
DOC = ROOT / "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2282_00_2281_doc",
        "source_key": "2281_doc",
        "source_path": ROOT / "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
        "needles": ["NEXT2281_0_primary", "SELECTOR_GAP_IS_THE_MAIN_BLOCKER", "COVARIANCE_POSITIVITY_ALONE_NO_GO"],
        "role": "handoff selecting covariance-equilibrium selector or q closure declaration",
    },
    {
        "source_id": "SRC2282_01_2281_validation",
        "source_key": "2281_validation",
        "source_path": OUT / "P8_Y5_BRR545_2281_VALIDATION.csv",
        "needles": ["VAL2281_OVERALL", "PASS"],
        "role": "confirms 2281 passed before 2282 starts",
    },
    {
        "source_id": "SRC2282_02_2281_selector_gap",
        "source_key": "2281_selector_gap",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2281_COVARIANCE_MANIFOLD_SELECTOR_GAP.csv",
        "needles": ["CSG2281_1_metric_compatibility", "CSG2281_4_direct_penalty"],
        "role": "machine-readable selector-gap audit",
    },
    {
        "source_id": "SRC2282_03_02_local_reduction",
        "source_key": "02_motion_load_local_GR",
        "source_path": ROOT / "02-motion-load-local-GR-reduction.md",
        "needles": ["T^2 S = 1", "p = 1", "parent origin of reciprocal routing = missing"],
        "role": "early conditional local-GR reduction via reciprocal routing",
    },
    {
        "source_id": "SRC2282_04_03_parent_origin",
        "source_key": "03_reciprocal_parent_origin",
        "source_path": ROOT / "03-reciprocal-routing-parent-origin.md",
        "needles": ["G^t_t = G^r_r", "A B = 1", "reciprocity = theorem target"],
        "role": "vacuum stress balance route and no-GR-import warning",
    },
    {
        "source_id": "SRC2282_05_09_hamiltonian",
        "source_key": "09_hamiltonian_cell",
        "source_path": ROOT / "09-hamiltonian-radial-cell-derivation.md",
        "needles": ["J_tr = T sqrt(S)", "generic symplectic or Liouville phase-volume preservation does not derive p=1", "local GR branch remains promising but conditional"],
        "role": "Hamiltonian route rejects generic phase-volume selector",
    },
    {
        "source_id": "SRC2282_06_10_observer_contract",
        "source_key": "10_observer_contract",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "exact no-smuggling contract for reciprocal observer-cell selector",
    },
    {
        "source_id": "SRC2282_07_action_principle",
        "source_key": "action_principle",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["GR is the low-frequency limit", "coarse-grained covariance", "standard matter"],
        "role": "corpus EH/IR language; useful but circular if used to derive the GR branch itself",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2282_SOURCE_REGISTER.csv",
    "equivalence": OUT / "P8_Y5_PARENT_QLOC_2282_Q_OBSERVER_CELL_EQUIVALENCE.csv",
    "selector_audit": OUT / "P8_Y5_PARENT_QLOC_2282_SELECTOR_ROUTE_AUDIT.csv",
    "closure_declaration": OUT / "P8_Y5_PARENT_QLOC_2282_Q_CLOSURE_DECLARATION.csv",
    "parent_inputs": OUT / "P8_Y5_PARENT_QLOC_2282_PARENT_SELECTOR_INPUT_CONTRACT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2282_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2282_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2282_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2282_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2282_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2282_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_equivalence": QUEUE / "JR2282_Q_OBSERVER_CELL_EQUIVALENCE_NONCLAIM.csv",
    "queue_closure": QUEUE / "JR2282_Q_CLOSURE_DECLARATION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_covariance_selector_refusal_2282.csv",
    "beta_docs": BETA_DOCS / "RAB_COVARIANCE_SELECTOR_2282_NONCLAIM.csv",
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


def equivalence_rows() -> list[dict[str, Any]]:
    return [
        {
            "equivalence_id": "QOE2282_0_definitions",
            "object": "covariance-to-observer map",
            "formula": "T^2=1-C_T; S=1+C_R; q=C_R-C_T/(1-C_T)",
            "derived_result": "T^2 S=(1-C_T)(1+C_R)",
            "status": "DEFINITIONAL_MAP",
            "valid_for_claim": False,
        },
        {
            "equivalence_id": "QOE2282_1_q_zero_to_reciprocity",
            "object": "q=0 branch",
            "formula": "q=0 iff C_R=C_T/(1-C_T)",
            "derived_result": "S=1/(1-C_T), hence T^2 S=1",
            "status": "EXACT_EQUIVALENCE",
            "valid_for_claim": False,
        },
        {
            "equivalence_id": "QOE2282_2_reciprocity_to_q_zero",
            "object": "observer-cell reciprocity",
            "formula": "T^2 S=1 iff (1-C_T)(1+C_R)=1",
            "derived_result": "C_R=C_T/(1-C_T), hence q=0",
            "status": "EXACT_EQUIVALENCE",
            "valid_for_claim": False,
        },
        {
            "equivalence_id": "QOE2282_3_strain_relation",
            "object": "reciprocal strain",
            "formula": "R_AB=ln(T^2 S)=ln(1+(1-C_T)q)",
            "derived_result": "small q gives R_AB=(1-C_T)q+O(q^2)",
            "status": "Q_IS_RESCALED_OBSERVER_CELL_STRAIN",
            "valid_for_claim": False,
        },
        {
            "equivalence_id": "QOE2282_4_ppn_link",
            "object": "local PPN gamma lane",
            "formula": "S_p=(1-L)^(-p), T^2=1-L",
            "derived_result": "T^2 S_p=1 over variable L requires p=1, so gamma=1 in the weak-field lane",
            "status": "CONDITIONAL_ON_RECIPROCAL_CELL_SELECTOR",
            "valid_for_claim": False,
        },
    ]


def selector_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_id": "SEL2282_0_covariance_positivity",
            "candidate_selector": "covariance positivity/coarse-graining",
            "test": "does positivity choose C_R=C_T/(1-C_T)?",
            "result": "NO_GO",
            "reason": "positivity supplies allowed cone/coercivity, not the exact reciprocal observer-cell branch",
            "current_status": "REJECTED_AS_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_1_metric_compatibility",
            "candidate_selector": "metric compatibility plus observer-cell reciprocity",
            "test": "does the observer coframe impose R_AB=ln(T^2S)=0?",
            "result": "EQUIVALENT_TARGET_NOT_PARENT_DERIVED",
            "reason": "q=0 is exactly R_AB=0, but the parent origin of preserving the radial observer configuration cell remains absent",
            "current_status": "BEST_NON_GR_SELECTOR_TARGET",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_2_EH_vacuum",
            "candidate_selector": "Einstein-Hilbert static areal vacuum",
            "test": "G^t_t=G^r_r implies (AB)'=0 and asymptotic flatness gives AB=1",
            "result": "CONDITIONAL_SELECTOR_IF_EH_IR_ACCEPTED",
            "reason": "this derives reciprocity inside GR/EH vacuum, but it is circular if used as the proof that MTS derives GR",
            "current_status": "USEFUL_CONSISTENCY_CHECK_NOT_PARENT_PROOF",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_3_hamiltonian_liouville",
            "candidate_selector": "generic Hamiltonian/Liouville preservation",
            "test": "full phase cell J_q J_p=1",
            "result": "NO_GO",
            "reason": "full phase-volume preservation holds for every p and does not force J_q=1",
            "current_status": "REJECTED_AS_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_4_entropy_extremum",
            "candidate_selector": "entropy/free-energy extremum",
            "test": "partial F_eff/partial q=0 at q=0",
            "result": "POSSIBLE_BUT_UNWRITTEN",
            "reason": "MTS has entropy/dissipation motifs, but no explicit F_eff[C] selects q=0",
            "current_status": "OPEN_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_5_bianchi_source",
            "candidate_selector": "Bianchi/source consistency",
            "test": "conservation plus matter readout forces R_AB=0",
            "result": "POSSIBLE_BUT_NEEDS_SOURCE_MAP",
            "reason": "requires T_q, source normalization, worldtube/Hilbert equality, and boundary flux closure",
            "current_status": "OPEN_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2282_6_direct_q_penalty",
            "candidate_selector": "direct q-stiffness penalty",
            "test": "V(q)=1/2 M_q^2 q^2",
            "result": "CLOSURE_ONLY",
            "reason": "suppresses q after choosing the target but does not explain why the target is q=0",
            "current_status": "DEMOTED_TO_DISCIPLINED_CLOSURE",
            "valid_for_claim": False,
        },
    ]


def closure_declaration_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "QCD2282_0_status",
            "item": "q-stiffness local branch",
            "declaration": "DISCIPLINED_CLOSURE_UNTIL_SELECTOR_THEOREM",
            "reason": "operator form is conditionally natural, but q=0 selector is not parent-signed",
            "allowed_use": "internal residual bounds and local-test bookkeeping only",
            "forbidden_use": "derived local-GR/Newton claim",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCD2282_1_equivalence_gain",
            "item": "q=0 meaning",
            "declaration": "Q_ZERO_EQUALS_RADIAL_OBSERVER_CELL_RECIPROCITY",
            "reason": "q=0 iff T^2S=1 iff R_AB=0",
            "allowed_use": "route unification between q-stiffness and observer-cell work",
            "forbidden_use": "treat equivalence as parent proof",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCD2282_2_EH_consistency",
            "item": "EH/Schwarzschild consistency",
            "declaration": "CONSISTENCY_CHECK_ONLY",
            "reason": "EH vacuum selects AB=1, but using it to derive MTS->GR is circular unless EH was already independently derived",
            "allowed_use": "check that the target branch matches GR",
            "forbidden_use": "hide GR import inside the selector",
            "valid_for_claim": False,
        },
        {
            "closure_id": "QCD2282_3_next_attempt",
            "item": "parent selector theorem",
            "declaration": "RADIAL_CELL_CURRENT_OR_CONSTRAINT_OWNER_REQUIRED",
            "reason": "the non-circular selector must produce J_q=1 or R_AB=0 directly",
            "allowed_use": "next derivation target",
            "forbidden_use": "claim closure as derivation",
            "valid_for_claim": False,
        },
    ]


def parent_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "PIC2282_0_cell_current",
            "needed_input": "conserved radial observer-cell current",
            "required_formula": "d J_cell=0 with J_q=T sqrt(S)=1 after no-charge/no-hair boundary conditions",
            "current_status": "MISSING_PARENT_CURRENT",
            "blocks": "non-circular selector for q=0",
            "valid_for_claim": False,
        },
        {
            "input_id": "PIC2282_1_multiplier",
            "needed_input": "parent-origin constraint multiplier",
            "required_formula": "lambda_R ln(T^2S) with lambda_R sourced by symmetry/regularity, not fitted",
            "current_status": "MISSING_MULTIPLIER_ORIGIN",
            "blocks": "constraint route to R_AB=0",
            "valid_for_claim": False,
        },
        {
            "input_id": "PIC2282_2_gauge_redundancy",
            "needed_input": "observer-splitting gauge redundancy",
            "required_formula": "R_AB is pure gauge only after quotient-visible observables are invariant",
            "current_status": "MISSING_GAUGE_QUOTIENT_PROOF",
            "blocks": "gauge route to q=0",
            "valid_for_claim": False,
        },
        {
            "input_id": "PIC2282_3_boundary_silence",
            "needed_input": "no reciprocal exterior hair",
            "required_formula": "boundary charge Q_R=0 and no radial reciprocal stress tail",
            "current_status": "MISSING_NO_HAIR_THEOREM",
            "blocks": "local PPN/R10 residual bounds",
            "valid_for_claim": False,
        },
        {
            "input_id": "PIC2282_4_source_map",
            "needed_input": "same source normalization for Newton/PPN",
            "required_formula": "worldtube/Hilbert mass equality and measured-GM pullback",
            "current_status": "MISSING_SOURCE_NORMALIZATION_THEOREM",
            "blocks": "Newtonian mechanics derivation",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2282_0_q_observer_equivalence",
            "claim": "q=0 is equivalent to T^2S=1 and R_AB=0 under the declared covariance-observer map",
            "gate_pass": True,
            "reason": "direct algebra using T^2=1-C_T and S=1+C_R",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2282_1_parent_selector",
            "claim": "the current corpus parent-selects q=0 non-circularly",
            "gate_pass": False,
            "reason": "radial observer-cell current, multiplier origin, or gauge quotient proof remains missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2282_2_EH_selector",
            "claim": "EH vacuum can select AB=1",
            "gate_pass": True,
            "reason": "static areal vacuum stress balance gives AB=1 if EH/GR vacuum is already accepted",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2282_3_q_closure_declaration",
            "claim": "q-stiffness is closure-only until selector theorem is parent-signed",
            "gate_pass": True,
            "reason": "equivalence and selector audit identify missing theorem",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2282_4_local_gr_newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "reason": "selector, boundary, source normalization, beta/PPN and Newton source gates remain open",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2282_0_equivalence_as_proof",
            "attempted_claim": "Because q=0 equals T^2S=1, local GR is derived.",
            "runner_result": "BLOCKED",
            "blocked_by": "equivalence identifies the target; it does not parent-select it",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2282_1_EH_import",
            "attempted_claim": "Use GR/EH vacuum AB=1 as the non-circular proof that MTS derives GR.",
            "runner_result": "BLOCKED",
            "blocked_by": "EH route is circular unless EH/operator and extra-sector silence were independently proven",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2282_2_q_penalty_derivation",
            "attempted_claim": "A q penalty/stiffness term derives the local-GR selector.",
            "runner_result": "BLOCKED",
            "blocked_by": "penalty suppresses deviations after target selection; it does not select the target",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2282_3_local_gr_newton",
            "attempted_claim": "MTS has derived local GR/Newton mechanics.",
            "runner_result": "BLOCKED",
            "blocked_by": "radial-cell selector and source normalization remain missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2282_0_gain",
            "decision": "Q_ZERO_IDENTIFIED_WITH_RADIAL_OBSERVER_CELL_RECIPROCITY",
            "reason": "q=0 iff T^2S=1 iff R_AB=0, so the new q-selector and old reciprocal-cell problem are the same gate.",
            "next_action": "merge q-stiffness route with radial-cell current/constraint owner search.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2282_1_closure",
            "decision": "Q_STIFFNESS_DEMOTED_TO_DISCIPLINED_CLOSURE_FOR_NOW",
            "reason": "conditional stiffness is natural, but the selector target is not parent-signed.",
            "next_action": "use for nonclaim residual bookkeeping only.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2282_2_EH_status",
            "decision": "EH_VACUUM_SELECTOR_IS_CONSISTENCY_NOT_DERIVATION",
            "reason": "AB=1 follows from GR/EH vacuum, but using that as parent proof would smuggle in GR.",
            "next_action": "keep no-GR-import guard active.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2282_3_next",
            "decision": "RADIAL_CELL_CURRENT_OWNER_NEXT",
            "reason": "this is the cleanest non-circular route to a selector theorem.",
            "next_action": "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2282_0_primary",
            "next_target": "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
            "script": "scripts/Y5_R2FR_radial_observer_cell_current_owner_or_q_closure_finalizer_2283.py",
            "objective": "attempt a non-circular parent owner for J_q=T sqrt(S)=1 / R_AB=0 via conserved radial cell current, constraint multiplier, or gauge quotient; otherwise finalize q-stiffness as closure-only",
            "selection_status": "selected",
            "success_condition": "parent-signed current/constraint/gauge theorem selects R_AB=0 without GR import, or closure-only status remains explicit with local-GR/Newton claims blocked",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_equivalence": OUTPUTS["equivalence"],
        "queue_closure": OUTPUTS["closure_declaration"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["selector_audit"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for radial-cell selector and q-closure follow-up work",
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

    prior_text = read_text(OUT / "P8_Y5_BRR545_2281_VALIDATION.csv")
    prior_ok = "VAL2281_OVERALL" in prior_text and "PASS" in prior_text

    equivalence = equivalence_rows()
    selectors = selector_audit_rows()
    closure = closure_declaration_rows()
    inputs = parent_input_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()

    q_equivalence = any(row["equivalence_id"] == "QOE2282_1_q_zero_to_reciprocity" for row in equivalence)
    strain_relation = any(row["equivalence_id"] == "QOE2282_3_strain_relation" and "R_AB" in row["formula"] for row in equivalence)
    positivity_rejected = any(row["selector_id"] == "SEL2282_0_covariance_positivity" and row["result"] == "NO_GO" for row in selectors)
    eh_guarded = any(row["selector_id"] == "SEL2282_2_EH_vacuum" and row["current_status"] == "USEFUL_CONSISTENCY_CHECK_NOT_PARENT_PROOF" for row in selectors)
    liouville_rejected = any(row["selector_id"] == "SEL2282_3_hamiltonian_liouville" and row["result"] == "NO_GO" for row in selectors)
    closure_declared = any(row["closure_id"] == "QCD2282_0_status" and row["declaration"] == "DISCIPLINED_CLOSURE_UNTIL_SELECTOR_THEOREM" for row in closure)
    inputs_missing = all(row["current_status"].startswith("MISSING") and row["valid_for_claim"] is False for row in inputs)
    equivalence_not_claim = any(row["claim_id"] == "CG2282_0_q_observer_equivalence" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    selector_blocked = any(row["claim_id"] == "CG2282_1_parent_selector" and row["gate_pass"] is False for row in claims)
    local_blocked = any(row["claim_id"] == "CG2282_4_local_gr_newton" and row["gate_pass"] is False for row in claims)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    next_selected = any(row["route_id"] == "NEXT2282_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = (
        not any(not ignored_environment_path(path) for path in FORMALIZATION.rglob("*2282*"))
        if FORMALIZATION.exists()
        else True
    )

    checks = [
        ("VAL2282_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2282_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2282_2_prior_validation", prior_ok, "2281 validation passes"),
        ("VAL2282_3_q_equivalence", q_equivalence, "q=0 to observer-cell reciprocity equivalence written"),
        ("VAL2282_4_strain_relation", strain_relation, "R_AB strain relation written"),
        ("VAL2282_5_positivity_rejected", positivity_rejected, "covariance positivity rejected as selector"),
        ("VAL2282_6_eh_guarded", eh_guarded, "EH selector guarded against GR import"),
        ("VAL2282_7_liouville_rejected", liouville_rejected, "generic Liouville selector rejected"),
        ("VAL2282_8_closure_declared", closure_declared, "q-stiffness closure declaration written"),
        ("VAL2282_9_inputs_missing", inputs_missing, "parent selector inputs remain missing"),
        ("VAL2282_10_equivalence_not_claim", equivalence_not_claim, "equivalence is not promoted to claim"),
        ("VAL2282_11_selector_blocked", selector_blocked, "parent selector claim remains blocked"),
        ("VAL2282_12_local_blocked", local_blocked, "local GR/Newton claim remains blocked"),
        ("VAL2282_13_refusal_blocks", refusal_blocks, "refusal runner blocks overclaims"),
        ("VAL2282_14_next_selected", next_selected, "2283 target selected"),
        ("VAL2282_15_csv_parse", csvs_parse, "all generated 2282 CSVs parse"),
        ("VAL2282_16_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2282_17_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2282_18_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2282_19_formalization_no_2282", formalization_clean, "formalization-workbench has no 2282 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2282_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2282 proves q=0 is equivalent to radial observer-cell reciprocity, rejects positivity/Liouville/EH-import overclaims, declares q-stiffness closure-only until selector theorem, and selects 2283",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    equivalence = equivalence_rows()
    selectors = selector_audit_rows()
    closure = closure_declaration_rows()
    inputs = parent_input_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2282 - Y5/R2FR Covariance Equilibrium Selector Or q Closure Declaration",
        "",
        "## Verdict",
        "",
        "The selector problem has been de-duplicated. Under the covariance-observer map `T^2=1-C_T` and `S=1+C_R`, the condition `q=0` is exactly the old radial observer-cell reciprocity condition: `q=0 ⇔ T^2S=1 ⇔ R_AB=ln(T^2S)=0`. This is a real simplification because the q-stiffness branch and the earlier motion-load branch are now the same local-GR gate.",
        "",
        "But this is not yet a derivation of local GR. It identifies the target manifold; it does not parent-select it. Covariance positivity and generic Liouville preservation do not select it, and EH/Schwarzschild vacuum selects it only if GR/EH has already been accepted. Therefore `q`-stiffness is declared a disciplined closure until a non-circular parent owner for `J_q=T sqrt(S)=1` is derived.",
        "",
        "The next non-circular route is narrow: conserved radial observer-cell current, parent-origin constraint multiplier, or genuine observer-splitting gauge quotient. Without one of those, the local-GR/Newton claim stays blocked.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## q Observer-Cell Equivalence",
        table(["equivalence_id", "object", "formula", "derived_result", "status", "valid_for_claim"], equivalence),
        "",
        "## Selector Route Audit",
        table(["selector_id", "candidate_selector", "test", "result", "reason", "current_status", "valid_for_claim"], selectors),
        "",
        "## q Closure Declaration",
        table(["closure_id", "item", "declaration", "reason", "allowed_use", "forbidden_use", "valid_for_claim"], closure),
        "",
        "## Parent Selector Input Contract",
        table(["input_id", "needed_input", "required_formula", "current_status", "blocks", "valid_for_claim"], inputs),
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
        "This is a good kind of demotion. We did not lose the route; we found that the q route and the reciprocal-cell route are one route. The hard problem is no longer scattered across names. It is: derive `J_q=1` from parent motion-time geometry without importing GR. If that theorem closes, the q-stiffness operator becomes a natural residual suppressor around the derived local-GR branch. If it does not, the q sector remains a useful closure, not a derivation.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["equivalence"], equivalence_rows())
    write_csv(OUTPUTS["selector_audit"], selector_audit_rows())
    write_csv(OUTPUTS["closure_declaration"], closure_declaration_rows())
    write_csv(OUTPUTS["parent_inputs"], parent_input_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["equivalence"], COPY_TARGETS["queue_equivalence"])
    shutil.copyfile(OUTPUTS["closure_declaration"], COPY_TARGETS["queue_closure"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["selector_audit"], COPY_TARGETS["beta_docs"])
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
