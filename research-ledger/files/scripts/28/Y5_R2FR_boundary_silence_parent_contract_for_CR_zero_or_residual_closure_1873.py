from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1873"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1873_SOURCE_REGISTER.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_1873_BOUNDARY_SILENCE_PARENT_CONTRACT.csv",
    "conditional_proof": OUT / "P8_Y5_PARENT_QLOC_1873_CONDITIONAL_CR_ZERO_PROOF.csv",
    "unsigned_ledger": OUT / "P8_Y5_PARENT_QLOC_1873_UNSIGNED_CLAUSE_LEDGER.csv",
    "closure_demotion": OUT / "P8_Y5_PARENT_QLOC_1873_RESIDUAL_CLOSURE_DEMOTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1873_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1873_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1873_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1873_VALIDATION.csv",
}

SOURCE_NEEDLES = {
    "1872_doc": {
        "path": ROOT / "1872-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md",
        "needles": [
            "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "ABSOLUTE_CR_TAIL_BOUND_LEDGER_READY_NONCLAIM",
            "BOUNDARY_SILENCE_PARENT_CONTRACT_SELECTED_NEXT",
        ],
    },
    "1635_pir_zero_contract": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1635_PIR_ZERO_THEOREM_CONTRACT.csv",
        "needles": [
            "EXACT_CONDITIONAL_THEOREM_NOT_PROMOTED",
            "PIR_ZERO_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED",
            "Pi_R=0 => Q_R=0",
        ],
    },
    "1635_matter_descent": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1635_MATTER_DESCENT_SIGNATURE_GATE.csv",
        "needles": [
            "PIR_ZERO_STACK_NOT_CLOSED_CURRENT_CORPUS",
            "PIR_BOUNDARY_ZERO_UNSIGNED",
            "NO_MARKER_CONSTANT_OWNER_UNSIGNED",
        ],
    },
    "1636_object_language": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1636_RAB_OBJECT_LANGUAGE_AUDIT.csv",
        "needles": [
            "OBJECT_LANGUAGE_CONTRACT_READY_NOT_DERIVED",
            "BOUNDARY_OBJECT_LANGUAGE_MISSING",
            "RAB_VERTICALITY_OBJECT_LANGUAGE_UNSIGNED",
        ],
    },
    "1636_forbidden_slots": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1636_FORBIDDEN_RAB_SLOT_LEDGER.csv",
        "needles": [
            "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED",
            "BOUNDARY_SLOT_NOT_CLASSIFIED",
            "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
        ],
    },
    "1637_no_slot_grammar": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR.csv",
        "needles": [
            "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS",
            "BOUNDARY_SLOT_NOT_PARENT_SIGNED",
            "HIDDEN_TAIL_NOT_CLOSED",
        ],
    },
    "1637_obstructions": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1637_NO_SLOT_OBSTRUCTION_LEDGER.csv",
        "needles": [
            "ACTIVE_OBSTRUCTION",
            "boundary reciprocal momentum Pi_R is not syntactically excluded",
            "non-Hilbert/source-support/domain/readout tails can bypass visible no-slot grammar",
        ],
    },
    "1640_boundary_silence": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT.csv",
        "needles": [
            "PIR_ZERO_NOT_PROVED_BOUNDARY_SILENCE_UNSIGNED",
            "BOUNDARY_OBJECT_LANGUAGE_UNSIGNED",
            "HIDDEN_TAIL_UNSIGNED",
        ],
    },
    "1872_failed_proof": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1872_FAILED_ZERO_PROOF_LEDGER.csv",
        "needles": [
            "BOUNDARY_VARIATION_CLASS_UNSIGNED",
            "NO_INDEPENDENT_RAB_SLOT_UNSIGNED",
            "ABSOLUTE_RESIDUAL_VECTOR_MISSING",
        ],
    },
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, payload in SOURCE_NEEDLES.items():
        path = payload["path"]
        ok, detail = path_has_needles(path, payload["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(payload["needles"]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1873": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_0_parent_domain",
            "contract_clause": "A parent quotient q:Phi_parent->Q_obs exists before matter/readout, and v_R is a vertical representative direction in ker(Dq).",
            "mathematical_role": "lets R_AB variation be tested as a pure representative variation instead of an observed physical perturbation",
            "required_signature": "parent construction of q, Q_obs, v_R and Dq[v_R]=0 or parent elimination of R_AB",
            "current_status": "UNSIGNED_PARENT_DOMAIN",
            "if_signed": "bulk matter descent becomes meaningful",
            "if_unsigned": "R_AB remains a physical local/PPN residual channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_1_matter_descent",
            "contract_clause": "S_matter=sum_A Sbar_A[Psi_A,e_obs(q(Phi)),omega(q(Phi)),theta_A]+dB_A[q(Phi)] with no direct R_AB argument.",
            "mathematical_role": "gives delta_{v_R} S_matter_bulk=0 by chain rule",
            "required_signature": "quotient-invariant matter functor and descended measure/coframe/connection",
            "current_status": "UNSIGNED_MATTER_DESCENT",
            "if_signed": "direct bulk J_R source is killed",
            "if_unsigned": "direct S_matter[...,R_AB] counterterm survives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_2_geometry_stack",
            "contract_clause": "The observed metric/coframe, measure, spin connection, derivative operator, and clock/readout geometry all descend through q.",
            "mathematical_role": "removes Weyl/disformal/frame leakage that would make rods and clocks see R_AB",
            "required_signature": "no representative coframe/connection/readout coefficient",
            "current_status": "UNSIGNED_GEOMETRY_STACK",
            "if_signed": "geometry-frame contribution to Pi_R is zero",
            "if_unsigned": "frame leak can source local gamma/clock/WEP residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_3_constants_no_marker",
            "contract_clause": "Representation constants, masses, EM coefficients, material markers, and source labels are invariant under v_R.",
            "mathematical_role": "kills visible coefficient and composition-dependent source terms",
            "required_signature": "Lie_{v_R} theta_A=0 plus no f_R(R_AB), m_A(R_AB), alpha(R_AB), w_A(R_AB)",
            "current_status": "UNSIGNED_NO_MARKER_CONSTANT_OWNER",
            "if_signed": "constant/material/source-weight Pi_R channels vanish",
            "if_unsigned": "EM/mass/clock/source-weight counterterms remain legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_4_variation_order",
            "contract_clause": "Variation is taken on the parent action before source selectors, local projection, fitting, or readout reduction.",
            "mathematical_role": "prevents post-variation selectors from manufacturing the primary R_AB source",
            "required_signature": "single pre-readout Hilbert source owner and no pre-action source weights",
            "current_status": "PARTIAL_CONDITIONAL_PRE_ACTION_LEAK_SURVIVES",
            "if_signed": "post-readout source rescaling cannot create Pi_R",
            "if_unsigned": "pre-action weights w_A(R_AB)S_A survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_5_boundary_silence",
            "contract_clause": "Worldtube/boundary/readout terms are quotient-only, proper/exact, or zero-projection under v_R; no independent B_R[R_AB] or Pi_R slot exists.",
            "mathematical_role": "kills the edge term Pi_R after the bulk chain-rule result",
            "required_signature": "oriented worldtube variation and boundary object-language theorem",
            "current_status": "UNSIGNED_BOUNDARY_SILENCE",
            "if_signed": "Pi_R=0 and therefore Q_cur=0",
            "if_unsigned": "Q_cur=-Pi_R leaves massless C_R/r hair open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_6_hidden_tail_silence",
            "contract_clause": "Hidden/domain/source-support/radiative/readout EFT reductions do not reintroduce local R_AB dependence, or are absolutely bounded.",
            "mathematical_role": "stabilizes the visible no-slot theorem under projection and effective reduction",
            "required_signature": "hidden-tail theorem or explicit absolute residual bound",
            "current_status": "UNSIGNED_HIDDEN_TAIL_SILENCE",
            "if_signed": "zero theorem survives local projection",
            "if_unsigned": "local-GR proof is unstable under hidden/readout tails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1873_7_no_cancellation",
            "contract_clause": "All local residual components are zero independently or bounded in an absolute vector; cancellation credit is forbidden.",
            "mathematical_role": "turns C_R=0 into a real local-GR result rather than a fitted gamma cancellation",
            "required_signature": "absolute residual-vector owner for gauge/source/boundary/readout/higher-order terms",
            "current_status": "UNSIGNED_ABSOLUTE_RESIDUAL_VECTOR",
            "if_signed": "Delta gamma_C_R=0 can be combined safely with other zero rows",
            "if_unsigned": "PPN/local-GR remains closure/residual-bounded only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def conditional_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_0_vertical_variation",
            "premise": "BSC1873_0 through BSC1873_2 signed",
            "operation": "vary S_matter along v_R in ker(Dq)",
            "result": "delta_{v_R} S_matter_bulk = 0",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_1_no_visible_source",
            "premise": "BSC1873_3 and BSC1873_4 signed",
            "operation": "exclude visible coefficients, markers, source-only weights, and post-readout source creation",
            "result": "J_R_visible = 0",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_2_boundary_silence",
            "premise": "BSC1873_5 signed",
            "operation": "evaluate worldtube boundary variation under v_R",
            "result": "Pi_R = 0",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_3_charge_tail_chain",
            "premise": "Pi_R=0 plus 1871 convention Q_cur=-Pi_R and C_R=-Q_cur/kappa_W",
            "operation": "propagate boundary silence into exterior reciprocal hair",
            "result": "Q_cur=0, C_R=0, q_R=0",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_4_local_gr_projection",
            "premise": "BSC1873_6 and BSC1873_7 signed",
            "operation": "insert C_R=0 into absolute local residual vector",
            "result": "Delta gamma_C_R=0 without cancellation credit",
            "status": "CONDITIONAL_EXACT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "PROOF1873_5_verdict",
            "premise": "all BSC1873 clauses parent-signed",
            "operation": "promote conditional theorem",
            "result": "local reciprocal-hair branch reduces to GR in this sector",
            "status": "THEOREM_READY_IF_PARENT_CONTRACT_SIGNED_NOT_CURRENTLY_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def unsigned_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "unsigned_id": "UNS1873_0_parent_domain",
            "missing_clause": "parent q/v_R verticality or R_AB elimination",
            "evidence": "1635 MDSG verticality and 1636 object-language rows remain unsigned",
            "effect": "cannot classify R_AB as pure representative gauge/vertical data",
            "required_next_evidence": "derive q and ker(Dq) from MTS primitives or demote R_AB to residual field",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "unsigned_id": "UNS1873_1_matter_geometry",
            "missing_clause": "matter/measure/coframe/connection descent",
            "evidence": "matter functor and geometry stack are contracts, not parent derivations",
            "effect": "direct R_AB and frame-leak countermodels survive",
            "required_next_evidence": "parent action functor proof or coefficient-bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "unsigned_id": "UNS1873_2_constants_source_weight",
            "missing_clause": "no marker/constants/source-only weights",
            "evidence": "1309/1635/1637 keep coefficients and pre-action weights legal unless signed",
            "effect": "EM/mass/clock/WEP/source residuals can source Pi_R",
            "required_next_evidence": "operator algebra theorem or finite coefficient priors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "unsigned_id": "UNS1873_3_boundary",
            "missing_clause": "boundary/worldtube object-language silence",
            "evidence": "1640 verdict says Pi_R zero boundary-silence theorem is not proved",
            "effect": "Q_cur=-Pi_R keeps C_R/r hair alive",
            "required_next_evidence": "oriented worldtube boundary theorem or Pi_R_abs bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "unsigned_id": "UNS1873_4_hidden_residual",
            "missing_clause": "hidden-tail and no-cancellation residual vector",
            "evidence": "1583/1640/1872 keep hidden and absolute-vector rows missing",
            "effect": "local-GR pass can be faked by cancellation unless blocked",
            "required_next_evidence": "absolute residual vector with all components zero/bounded independently",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def closure_demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "RCD1873_0_current_status",
            "route": "derived local reciprocal-hair GR reduction",
            "status": "DEMOTED_TO_RESIDUAL_CLOSURE_UNTIL_PARENT_CONTRACT_SIGNED",
            "reason": "at least one required boundary-silence parent contract clause is unsigned; in fact all high-risk clauses remain unsigned",
            "allowed_language": "conditional theorem / closure branch / residual-bound branch",
            "forbidden_language": "derived local GR pass; PPN pass; Q_R/C_R/Pi_R zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "RCD1873_1_closure_axiom_form",
            "route": "explicit closure if adopted later",
            "status": "CLOSURE_AXIOM_MUST_BE_LABELLED",
            "reason": "one may impose C_R=0/R_AB=0 locally, but that is not the same as deriving it from the parent action",
            "allowed_language": "closure-local-GR benchmark",
            "forbidden_language": "fundamental derivation unless BSC1873 clauses are proven",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "RCD1873_2_empirical_fallback",
            "route": "finite residual coefficient",
            "status": "BOUND_RUNNER_ROUTE_HELD_NONCLAIM",
            "reason": "1872 staged C_R/Pi_R/Cassini templates but C_R, M_*, kappa_W, and no-cancellation are missing",
            "allowed_language": "future source-bound residual coefficient",
            "forbidden_language": "current empirical PPN safety score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1873_0_conditional_theorem",
            "claim": "the exact C_R=0 theorem follows if all BSC1873 clauses are parent-signed",
            "status": "ALLOW_CONDITIONAL_INTERNAL_THEOREM",
            "reason": "the logical chain is clean once the parent contract premises are granted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1873_1_current_derivation",
            "claim": "MTS currently derives local GR in the C_R/Pi_R branch",
            "status": "BLOCKED",
            "reason": "required parent contract clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1873_2_closure",
            "claim": "local branch may be treated as closure for benchmarking",
            "status": "ALLOW_ONLY_IF_EXPLICITLY_LABELLED_CLOSURE",
            "reason": "closure is useful for tests but not a derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1873_3_empirical_score",
            "claim": "finite residual tail passes PPN",
            "status": "BLOCKED",
            "reason": "C_R/Pi_R/M_*/kappa/no-cancellation inputs are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1873_0_contract",
            "decision": "BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED",
            "reason": "1873 lists the clauses required to force Pi_R=0/C_R=0 without smuggling in a plateau or closure axiom",
            "consequence": "we now know the precise theorem we must prove",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1873_1_demotion",
            "decision": "CURRENT_LOCAL_CR_ZERO_ROUTE_DEMOTED_TO_RESIDUAL_CLOSURE",
            "reason": "the parent action does not currently sign verticality, matter descent, no markers, boundary silence, hidden-tail silence, or no-cancellation",
            "consequence": "no derived local-GR claim from this branch yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1873_2_next",
            "decision": "PARENT_DOMAIN_VERTICALITY_OR_EXPLICIT_RESIDUAL_FIELD_SELECTED_NEXT",
            "reason": "the first contract clause controls whether R_AB is a representative direction or a physical residual field",
            "consequence": "1874 should attempt q/v_R construction from MTS primitives; if it fails, treat R_AB as an explicit residual field with coefficient bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1873_0_primary",
            "target_doc": "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md",
            "target_script": "scripts/Y5_R2FR_parent_domain_verticality_for_RAB_or_explicit_residual_field_1874.py",
            "objective": "try to construct q:Phi_parent->Q_obs and v_R in ker(Dq) for R_AB from MTS primitives; if not possible, classify R_AB as an explicit residual field requiring coefficient bounds.",
            "selection_status": "selected",
            "success_condition": "parent-signed R_AB verticality/elimination theorem, or explicit residual-field classification with bound requirements.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1873_1_parallel_bound",
            "target_doc": "1874b-Y5-R2FR-CR-tail-residual-bound-runner-inputs.md",
            "target_script": "scripts/Y5_R2FR_CR_tail_residual_bound_runner_inputs_1874b.py",
            "objective": "prepare numeric/source input checks for C_R, Pi_R, kappa_W, M_*, and no-cancellation once derivation route is exhausted.",
            "selection_status": "held_parallel",
            "success_condition": "runner blocks until every input is real, sourced, same-frame, and non-cancelling.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_contract": parent_contract_rows(),
        "conditional_proof": conditional_proof_rows(),
        "unsigned_ledger": unsigned_ledger_rows(),
        "closure_demotion": closure_demotion_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in ["valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "parent_signed", "numeric_value_present"]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["parent_contract"], QUEUE / "JR1873_BOUNDARY_SILENCE_PARENT_CONTRACT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["closure_demotion"], QUEUE / "JR1873_RESIDUAL_CLOSURE_DEMOTION_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1873_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1873_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1873"]) == "true" for row in sources) else "FAIL",
            "detail": "all contract sources exist and contain required needles",
            "valid_for_claim": False,
        }
    )

    contract = rows_by_name["parent_contract"]
    required_statuses = {
        "UNSIGNED_PARENT_DOMAIN",
        "UNSIGNED_MATTER_DESCENT",
        "UNSIGNED_GEOMETRY_STACK",
        "UNSIGNED_NO_MARKER_CONSTANT_OWNER",
        "PARTIAL_CONDITIONAL_PRE_ACTION_LEAK_SURVIVES",
        "UNSIGNED_BOUNDARY_SILENCE",
        "UNSIGNED_HIDDEN_TAIL_SILENCE",
        "UNSIGNED_ABSOLUTE_RESIDUAL_VECTOR",
    }
    checks.append(
        {
            "validation_id": "VAL1873_1_contract_coverage",
            "status": "PASS" if required_statuses == {row["current_status"] for row in contract} else "FAIL",
            "detail": "parent contract covers all local C_R zero clauses",
            "valid_for_claim": False,
        }
    )

    proof = rows_by_name["conditional_proof"]
    checks.append(
        {
            "validation_id": "VAL1873_2_conditional_proof",
            "status": "PASS"
            if any(row["result"] == "Q_cur=0, C_R=0, q_R=0" for row in proof)
            and any(row["status"] == "THEOREM_READY_IF_PARENT_CONTRACT_SIGNED_NOT_CURRENTLY_SIGNED" for row in proof)
            else "FAIL",
            "detail": "conditional proof chain reaches C_R=0 but is not promoted",
            "valid_for_claim": False,
        }
    )

    unsigned = rows_by_name["unsigned_ledger"]
    checks.append(
        {
            "validation_id": "VAL1873_3_unsigned_ledger",
            "status": "PASS"
            if len(unsigned) == 5
            and any(row["missing_clause"] == "boundary/worldtube object-language silence" for row in unsigned)
            else "FAIL",
            "detail": "unsigned clauses are explicit",
            "valid_for_claim": False,
        }
    )

    closure = rows_by_name["closure_demotion"]
    checks.append(
        {
            "validation_id": "VAL1873_4_closure_demotion",
            "status": "PASS"
            if any(row["status"] == "DEMOTED_TO_RESIDUAL_CLOSURE_UNTIL_PARENT_CONTRACT_SIGNED" for row in closure)
            and any(row["status"] == "CLOSURE_AXIOM_MUST_BE_LABELLED" for row in closure)
            else "FAIL",
            "detail": "current C_R route is demoted to labelled closure/residual branch",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1873_5_claim_gates",
            "status": "PASS"
            if any(row["status"] == "ALLOW_CONDITIONAL_INTERNAL_THEOREM" for row in claims)
            and any(row["status"] == "BLOCKED" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "conditional theorem allowed internally; current claims blocked",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1873_6_decision",
            "status": "PASS"
            if any(row["decision"] == "BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED" for row in decisions)
            and any(row["decision"] == "CURRENT_LOCAL_CR_ZERO_ROUTE_DEMOTED_TO_RESIDUAL_CLOSURE" for row in decisions)
            else "FAIL",
            "detail": "decision ledger states contract and demotion",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1873_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1873_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1874 target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1873_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1873_9_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["parent_contract"].name,
        QUARANTINE / OUTPUTS["closure_demotion"].name,
        QUEUE / "JR1873_BOUNDARY_SILENCE_PARENT_CONTRACT_NONCLAIM.csv",
        QUEUE / "JR1873_RESIDUAL_CLOSURE_DEMOTION_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1873_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1873_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1873_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1873 boundary-silence parent contract or residual closure checkpoint",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1873 - Boundary Silence Parent Contract For C_R Zero Or Residual Closure

**Private status:** nonclaim checkpoint. No derived local-GR, PPN, orbital, R10, WEP, clock, EM, or cosmology pass is claimed.

## Result

1873 states the exact parent-action contract needed to make the `C_R=0` route real.

Conditional theorem:

```text
q exists, v_R in ker(Dq)
S_matter and geometry descend through q
no R_AB constants/markers/source weights
boundary/worldtube/readout terms have no independent R_AB or Pi_R slot
hidden/readout tails vanish independently
=> Pi_R=0
=> Q_cur=0
=> C_R=0
=> q_R=0
=> Delta gamma_C_R=0
```

That theorem is clean **if** the clauses are signed. Current corpus status: not signed. Therefore this checkpoint demotes the current local `C_R=0` route to an explicit residual/closure branch until the parent contract is proven.

This is not bad news, chume; it is the theory getting honest about the exact door it has to walk through.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Contract

{markdown_table(rows_by_name["parent_contract"])}

## Conditional Proof

{markdown_table(rows_by_name["conditional_proof"])}

## Unsigned Clause Ledger

{markdown_table(rows_by_name["unsigned_ledger"])}

## Closure Demotion

{markdown_table(rows_by_name["closure_demotion"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
