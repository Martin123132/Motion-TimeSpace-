from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1872"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1872-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1872_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_PARENT_QLOC_1872_CR_ZERO_THEOREM_AUDIT.csv",
    "failed_proof_ledger": OUT / "P8_Y5_PARENT_QLOC_1872_FAILED_ZERO_PROOF_LEDGER.csv",
    "absolute_bound_inputs": OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
    "absolute_bound_rows": OUT / "P8_Y5_PARENT_QLOC_1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv",
    "residual_vector": OUT / "P8_Y5_PARENT_QLOC_1872_LOCAL_RESIDUAL_VECTOR_INSERT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1872_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1872_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1872_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1872_VALIDATION.csv",
}

SOURCE_NEEDLES = {
    "1871_doc": {
        "path": ROOT / "1871-Y5-R2FR-QR-normalization-convention-lock-or-source-denominator-row.md",
        "needles": [
            "CANONICAL_C_R_DENOMINATOR_CONVENTION_LOCKED_NONCLAIM",
            "CR_ZERO_OR_ABSOLUTE_TAIL_BOUND_SELECTED_NEXT",
            "q_R = C_R c^2/(2 G M_*)",
        ],
    },
    "1871_denominator": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1871_SOURCE_DENOMINATOR_ROW_NONCLAIM.csv",
        "needles": [
            "SD1871_0_canonical_C_R_denominator",
            "q_R = C_R c^2/(2 G M_*)",
            "SYMBOLIC_CONVENTION_LOCK_READY_NONCLAIM",
        ],
    },
    "05_reciprocity": {
        "path": ROOT / "05-reciprocity-theorem-attempt.md",
        "needles": [
            "Asymptotic flatness alone does not kill `Q_R`",
            "R_AB ~ Q_R/r",
            "W R_AB' = 0",
        ],
    },
    "06_source_neutrality": {
        "path": ROOT / "06-reciprocal-charge-source-neutrality.md",
        "needles": [
            "delta S_boundary = [W R_AB' + Pi_R] delta R_AB",
            "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1",
            "source neutrality parent-derived",
        ],
    },
    "13_ppn_benchmark": {
        "path": ROOT / "13-local-closure-PPN-benchmark.md",
        "needles": [
            "R_AB approx q_R L",
            "gamma approx 1 + q_R",
            "R_AB=0 and Q_R=0 are closure assumptions",
        ],
    },
    "1577_nocharge": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv",
        "needles": [
            "MISSING_PARENT_NO_CHARGE_THEOREM",
            "MISSING_BOUNDARY_VARIATION_CLASS",
            "NOT_DERIVED_CURRENT_CORPUS",
        ],
    },
    "1640_boundary_silence": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT.csv",
        "needles": [
            "PIR_ZERO_NOT_PROVED_BOUNDARY_SILENCE_UNSIGNED",
            "boundary object-language",
            "hidden-tail theorem or absolute residual bound",
        ],
    },
    "1583_tail_bound": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1583_FIRST_FINITE_TAIL_BOUND_LEDGER.csv",
        "needles": [
            "MISSING_GAUGE_BOUND_OR_ZERO",
            "MISSING_SOURCE_BOUND_OR_ZERO",
            "MISSING_BOUNDARY_BOUND_OR_ZERO",
        ],
    },
    "1852_ppn_observable": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv",
        "needles": [
            "PPN1852_0_cassini_gamma",
            "6.7e-05",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
        ],
    },
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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
                "usable_for_1872": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": "external_cassini_ppn_gamma",
            "source_path": "https://pubmed.ncbi.nlm.nih.gov/14508481/ ; DOI https://doi.org/10.1038/nature01997",
            "required_needles": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "source_exists": True,
            "needle_check": "SOURCE_STRING_PRESENT_IN_LOCAL_1852;WEB_SEARCH_SNIPPET_CONFIRMED;PUBMED_DIRECT_OPEN_BLOCKED_BY_RECAPTCHA",
            "usable_for_1872": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_0_asymptotic_flatness",
            "zero_route": "finite exterior energy plus R_AB(infinity)=0",
            "would_require": "show every 1/r tail coefficient is excluded",
            "found_relation": "R_AB=C_R/r is asymptotically flat and finite-energy in the current radial model",
            "status": "ZERO_ROUTE_REJECTED",
            "missing_piece": "none; route fails constructively because C_R/r survives",
            "consequence": "asymptotic flatness cannot prove C_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_1_free_boundary",
            "zero_route": "free/proper source boundary variation",
            "would_require": "the physical source boundary has free delta R_AB and no independent Pi_R slot",
            "found_relation": "delta S_boundary=[W R_AB' + Pi_R] delta R_AB; Pi_R=0 would imply Q_cur=0 and C_R=0",
            "status": "CONDITIONAL_ROUTE_FOUND_NOT_PARENT_SIGNED",
            "missing_piece": "parent-signed variation class for matter/source worldtubes",
            "consequence": "cannot claim C_R=0 yet, but this remains the cleanest derivation route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_2_source_neutrality",
            "zero_route": "matter couples only to A=T^2 and L, not independently to R_AB",
            "would_require": "quotient-invariant parent matter action with no representative R_AB boundary/readout slot",
            "found_relation": "source neutrality is named but explicitly not parent-derived",
            "status": "CONDITIONAL_ROUTE_FOUND_NOT_PARENT_SIGNED",
            "missing_piece": "parent action descent and no-marker/readout theorem",
            "consequence": "promising structural route, still unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_3_auxiliary_constraint",
            "zero_route": "R_AB is auxiliary/closure-only rather than propagating hair",
            "would_require": "no W(R_AB')^2 kinetic owner or an algebraic constraint setting R_AB=0",
            "found_relation": "current 05/1581 branch contains a radial current equation, so the hair mode exists unless separately killed",
            "status": "NOT_AVAILABLE_IN_CURRENT_BRANCH",
            "missing_piece": "parent elimination theorem or explicit closure demotion",
            "consequence": "do not silently switch to closure after deriving a current",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_4_hidden_tail",
            "zero_route": "hidden domain/readout/EFT tails project to zero locally",
            "would_require": "absolute residual-vector theorem showing all non-C_R tails vanish independently",
            "found_relation": "1583/1640 keep hidden-tail and no-cancellation rows unsigned",
            "status": "MISSING_ABSOLUTE_RESIDUAL_VECTOR",
            "missing_piece": "gauge/source/boundary/readout/higher-order absolute bounds or zeros",
            "consequence": "even C_R small cannot be scored by cancellation credit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CZA1872_5_verdict",
            "zero_route": "C_R=0 theorem",
            "would_require": "parent-signed free boundary/source-neutral/no-marker route",
            "found_relation": "no route closes from the current corpus without an extra closure axiom",
            "status": "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "missing_piece": "boundary silence parent contract or absolute tail-bound fallback",
            "consequence": "move to parent boundary-silence contract; keep bound rows nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def failed_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "FP1872_0_boundary_class",
            "blocker": "BOUNDARY_VARIATION_CLASS_UNSIGNED",
            "why_it_matters": "Pi_R=0 follows only if the physical matter boundary variation is free/proper and has no independent reciprocal source slot",
            "needed_evidence": "parent action variation including matter, measure/coframe/connection descent, and boundary terms",
            "fallback_if_unresolved": "treat Pi_R or C_R as a residual coefficient to be source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "FP1872_1_object_language",
            "blocker": "NO_INDEPENDENT_RAB_SLOT_UNSIGNED",
            "why_it_matters": "source neutrality requires proving matter/readout cannot independently couple to R_AB",
            "needed_evidence": "quotient-invariant matter action using only descended fields plus no representative Weyl/disformal coefficient",
            "fallback_if_unresolved": "local branch becomes closure/residual-vector branch, not derived GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "FP1872_2_kappa_sign",
            "blocker": "KAPPA_AND_SIGN_ORIENTATION_UNSIGNED",
            "why_it_matters": "C_R=-Q_cur/kappa_W and Q_cur=-Pi_R fix whether Pi_R bounds transfer with plus/minus and kappa_W",
            "needed_evidence": "oriented worldtube convention and W normalization from the parent radial kinetic term",
            "fallback_if_unresolved": "use absolute-value C_R bound only; do not substitute Pi_R sign in claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "FP1872_3_same_frame_mass",
            "blocker": "MSTAR_SOURCE_FRAME_UNSIGNED",
            "why_it_matters": "q_R=C_R c^2/(2GM_*) is only meaningful when M_* is the same parent source mass used by the Newtonian observer map",
            "needed_evidence": "M_* source-mass convention derived before orbital GM backfill",
            "fallback_if_unresolved": "keep all PPN numbers symbolic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "FP1872_4_no_cancellation",
            "blocker": "ABSOLUTE_RESIDUAL_VECTOR_MISSING",
            "why_it_matters": "a small fitted gamma residual cannot hide cancellation among gauge/source/boundary/readout terms",
            "needed_evidence": "absolute residual-vector budget for all local contributions",
            "fallback_if_unresolved": "bound rows remain engineering targets only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def absolute_bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "ABI1872_0_C_R",
            "quantity": "C_R_abs",
            "required_for_formula": "|q_R| = |C_R| c^2/(2 G M_*)",
            "current_value": "MISSING_C_R_VALUE_OR_ZERO_THEOREM",
            "units": "length if R_AB is dimensionless",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_C_R_SOURCE",
            "status": "MISSING_SOURCE_BOUND_OR_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ABI1872_1_PiR",
            "quantity": "Pi_R_abs",
            "required_for_formula": "|C_R| = |Pi_R|/|kappa_W| after signed boundary convention",
            "current_value": "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM",
            "units": "kappa_W*length after projection",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_PiR_SOURCE",
            "status": "MISSING_BOUNDARY_BOUND_OR_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ABI1872_2_Mstar",
            "quantity": "M_star_same_frame",
            "required_for_formula": "|C_R| <= (2 G M_*/c^2) |Delta gamma|_max",
            "current_value": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS",
            "units": "mass",
            "source_path": "MISSING_PARENT_SOURCE_MASS_PATH",
            "status": "MISSING_SOURCE_MASS_CALIBRATION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ABI1872_3_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "required_for_formula": "|q_R| <= |Delta gamma|_max if all other tails are zero-bounded",
            "current_value": "6.7e-05 conservative Cassini row from 1852",
            "units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv"),
            "status": "EXTERNAL_OBSERVABLE_SOURCE_STRING_PRESENT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ABI1872_4_no_cancellation",
            "quantity": "absolute_local_residual_vector",
            "required_for_formula": "|Delta_gamma_total| >= |q_R| without cancellation credit or full absolute budget",
            "current_value": "MISSING_ABSOLUTE_VECTOR_GUARD",
            "units": "dimensionless residual budget",
            "source_path": str(OUT / "P8_Y5_PARENT_QLOC_1583_FIRST_FINITE_TAIL_BOUND_LEDGER.csv"),
            "status": "MISSING_NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def absolute_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ABR1872_0_qR_from_C_R",
            "target": "q_R_abs",
            "formula": "|q_R| = |C_R| c^2/(2 G M_*)",
            "observable_bound": "|Delta gamma|_max = 6.7e-05 conservative Cassini row",
            "implied_bound": "|C_R| <= (2 G M_*/c^2) 6.7e-05 only after same-frame M_* and no-cancellation are signed",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "doi": "https://doi.org/10.1038/nature01997",
            "current_status": "BOUND_TEMPLATE_READY_NONCLAIM",
            "blocked_by": "MISSING_C_R_VALUE_OR_ZERO_THEOREM;MISSING_SAME_FRAME_MSTAR;MISSING_NO_CANCELLATION_GUARD",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ABR1872_1_PiR_from_C_R",
            "target": "Pi_R_abs",
            "formula": "if Q_cur=-Pi_R and C_R=-Q_cur/kappa_W, then |Pi_R| <= |kappa_W| |C_R|",
            "observable_bound": "|Delta gamma|_max = 6.7e-05 conservative Cassini row",
            "implied_bound": "|Pi_R| <= |kappa_W| (2 G M_*/c^2) 6.7e-05 after sign/kappa/M_* locks",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "doi": "https://doi.org/10.1038/nature01997",
            "current_status": "BOUND_TEMPLATE_READY_NONCLAIM",
            "blocked_by": "MISSING_BOUNDARY_SIGN_ORIENTATION;MISSING_KAPPA_W;MISSING_SAME_FRAME_MSTAR;MISSING_NO_CANCELLATION_GUARD",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ABR1872_2_exact_zero",
            "target": "local_GR_exact_condition",
            "formula": "C_R=0 -> q_R=0 -> Delta gamma_C_R=0",
            "observable_bound": "automatic under any finite gamma bound",
            "implied_bound": "requires parent-signed C_R=0/Pi_R=0 theorem, not numeric fitting",
            "source_url": "internal theorem target",
            "doi": "not_applicable",
            "current_status": "EXACT_ROUTE_IDENTIFIED_NOT_PROVED",
            "blocked_by": "MISSING_PARENT_C_R_ZERO_THEOREM_OR_PiR_ZERO_THEOREM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "LRV1872_0_C_R_tail",
            "component": "Delta_gamma_C_R",
            "expression": "C_R c^2/(2 G M_*)",
            "absolute_bound_or_zero_needed": "C_R=0 theorem or |C_R| bound plus M_*",
            "status": "INSERTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "LRV1872_1_gauge_tail",
            "component": "Delta_gamma_gauge",
            "expression": "observer/radial-coordinate residual",
            "absolute_bound_or_zero_needed": "gauge map zero or bound",
            "status": "MISSING_FROM_1583",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "LRV1872_2_source_readout",
            "component": "Delta_gamma_source_readout",
            "expression": "source denominator plus matter/readout projection residual",
            "absolute_bound_or_zero_needed": "source/readout zero or bound",
            "status": "MISSING_FROM_1583",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "LRV1872_3_boundary_hidden",
            "component": "Delta_gamma_boundary_hidden",
            "expression": "worldtube/corner/hidden-tail residual",
            "absolute_bound_or_zero_needed": "boundary/hidden-tail silence theorem or bound",
            "status": "MISSING_FROM_1583_1640",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1872_0_zero_theorem",
            "claim": "C_R=0 or Pi_R=0 is proven",
            "status": "BLOCKED",
            "reason": "boundary/source-neutral/no-marker routes remain parent-unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1872_1_absolute_bound",
            "claim": "finite C_R tail is empirically bounded well enough for PPN pass",
            "status": "BLOCKED",
            "reason": "bound formulas are staged, but C_R/Pi_R value, M_*, and no-cancellation vector are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1872_2_R10_guard",
            "claim": "C_R/r tail can be scored in R10 alpha(lambda)",
            "status": "FORBIDDEN",
            "reason": "C_R/r is massless PPN/orbital hair; finite-range R10 needs Z_R and M_R^2",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1872_3_symbolic_progress",
            "claim": "1872 creates a safe nonclaim local residual insertion",
            "status": "ALLOW_INTERNAL_HANDOFF_ONLY",
            "reason": "C_R residual has a canonical formula and explicit blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1872_0_result",
            "decision": "CR_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "reason": "asymptotic flatness fails as a zero theorem, and boundary/source-neutral routes remain unsigned",
            "consequence": "no derived local-GR claim yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1872_1_bound",
            "decision": "ABSOLUTE_CR_TAIL_BOUND_LEDGER_READY_NONCLAIM",
            "reason": "Cassini gamma source string and 1871 C_R denominator provide a symbolic bound template",
            "consequence": "PPN/orbital branch can now demand C_R, M_*, no-cancellation, and source rows explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1872_2_next",
            "decision": "BOUNDARY_SILENCE_PARENT_CONTRACT_SELECTED_NEXT",
            "reason": "the least-scrutiny path is still a real derivation of Pi_R=0/no independent R_AB slot, not a fitted tail",
            "consequence": "1873 should write the exact parent-action boundary contract required to prove C_R=0, or demote this route to residual closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1872_0_primary",
            "target_doc": "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
            "target_script": "scripts/Y5_R2FR_boundary_silence_parent_contract_for_CR_zero_or_residual_closure_1873.py",
            "objective": "write the exact parent-action contract that would force Pi_R=0/C_R=0 through matter descent, source boundary variation, and no independent R_AB readout; if any clause is unsigned, demote to residual closure.",
            "selection_status": "selected",
            "success_condition": "parent-signed boundary silence theorem or explicit closure-only demotion with residual-vector requirements.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1872_1_empirical_parallel",
            "target_doc": "1873b-Y5-R2FR-Cassini-CR-tail-bound-source-row-smoke-runner.md",
            "target_script": "scripts/Y5_R2FR_Cassini_CR_tail_bound_source_row_smoke_runner_1873b.py",
            "objective": "separately turn the nonclaim C_R bound template into a smoke runner once C_R/M_*/no-cancellation inputs exist.",
            "selection_status": "held_parallel",
            "success_condition": "runner blocks until all numeric/source inputs are real and same-frame.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "zero_audit": zero_audit_rows(),
        "failed_proof_ledger": failed_proof_rows(),
        "absolute_bound_inputs": absolute_bound_input_rows(),
        "absolute_bound_rows": absolute_bound_rows(),
        "residual_vector": residual_vector_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    columns = [
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "parent_signed",
        "numeric_value_present",
        "score_allowed",
    ]
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in columns:
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
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1872_NEXT_TARGET_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["absolute_bound_rows"], QUEUE / "JR1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["residual_vector"], QUEUE / "JR1872_LOCAL_RESIDUAL_VECTOR_INSERT_NONCLAIM.csv")


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
            "validation_id": "VAL1872_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1872"]) == "true" for row in sources) else "FAIL",
            "detail": "all local source paths and external source strings are recorded",
            "valid_for_claim": False,
        }
    )

    zero = rows_by_name["zero_audit"]
    checks.append(
        {
            "validation_id": "VAL1872_1_zero_verdict",
            "status": "PASS"
            if any(row["status"] == "ZERO_ROUTE_REJECTED" for row in zero)
            and any(row["status"] == "CR_ZERO_NOT_PROVED_CURRENT_CORPUS" for row in zero)
            else "FAIL",
            "detail": "asymptotic flatness zero route rejected and no zero theorem claimed",
            "valid_for_claim": False,
        }
    )

    failed = rows_by_name["failed_proof_ledger"]
    required_blockers = {
        "BOUNDARY_VARIATION_CLASS_UNSIGNED",
        "NO_INDEPENDENT_RAB_SLOT_UNSIGNED",
        "KAPPA_AND_SIGN_ORIENTATION_UNSIGNED",
        "MSTAR_SOURCE_FRAME_UNSIGNED",
        "ABSOLUTE_RESIDUAL_VECTOR_MISSING",
    }
    checks.append(
        {
            "validation_id": "VAL1872_2_failed_proof_blockers",
            "status": "PASS" if required_blockers.issubset({row["blocker"] for row in failed}) else "FAIL",
            "detail": "proof blockers are explicit",
            "valid_for_claim": False,
        }
    )

    inputs = rows_by_name["absolute_bound_inputs"]
    checks.append(
        {
            "validation_id": "VAL1872_3_bound_inputs",
            "status": "PASS"
            if any(row["quantity"] == "Delta_gamma_abs_max" and "6.7e-05" in row["current_value"] for row in inputs)
            and all(bool_string(row["score_allowed"]) == "false" for row in inputs)
            else "FAIL",
            "detail": "Cassini bound source string is present but every input remains unscored",
            "valid_for_claim": False,
        }
    )

    bounds = rows_by_name["absolute_bound_rows"]
    checks.append(
        {
            "validation_id": "VAL1872_4_bound_rows",
            "status": "PASS"
            if any("|C_R| <= (2 G M_*/c^2) 6.7e-05" in row["implied_bound"] for row in bounds)
            and any(row["current_status"] == "EXACT_ROUTE_IDENTIFIED_NOT_PROVED" for row in bounds)
            and all(bool_string(row["valid_prediction_row"]) == "false" for row in bounds)
            else "FAIL",
            "detail": "absolute C_R/Pi_R/gamma bound templates exist and remain nonclaim",
            "valid_for_claim": False,
        }
    )

    residual = rows_by_name["residual_vector"]
    checks.append(
        {
            "validation_id": "VAL1872_5_residual_vector",
            "status": "PASS"
            if any(row["component"] == "Delta_gamma_C_R" and row["status"] == "INSERTED_NONCLAIM" for row in residual)
            and all(bool_string(row["valid_for_claim"]) == "false" for row in residual)
            else "FAIL",
            "detail": "C_R tail is inserted into local residual vector as nonclaim",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1872_6_claim_gates",
            "status": "PASS"
            if any(row["status"] == "FORBIDDEN" for row in claims)
            and any(row["status"] == "ALLOW_INTERNAL_HANDOFF_ONLY" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "no physics claim allowed; only internal handoff is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1872_7_decision",
            "status": "PASS"
            if any(row["decision"] == "CR_ZERO_NOT_PROVED_CURRENT_CORPUS" for row in decisions)
            and any(row["decision"] == "ABSOLUTE_CR_TAIL_BOUND_LEDGER_READY_NONCLAIM" for row in decisions)
            and any(row["decision"] == "BOUNDARY_SILENCE_PARENT_CONTRACT_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger chooses boundary-silence parent contract next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1872_8_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1872_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1873 target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1872_9_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1872_10_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["absolute_bound_rows"].name,
        QUARANTINE / OUTPUTS["absolute_bound_rows"].name,
        QUEUE / "JR1872_CR_PIR_DELTAGAMMA_BOUND_ROWS_NONCLAIM.csv",
        QUEUE / "JR1872_LOCAL_RESIDUAL_VECTOR_INSERT_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1872_11_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1872_12_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1872*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1872_13_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1872_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1872_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1872 C_R zero theorem or absolute tail-bound row checkpoint",
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
    content = f"""# 1872 - C_R Zero Theorem Or Absolute Tail Bound Row

**Private status:** nonclaim checkpoint. No derived local-GR, PPN, orbital, R10, WEP, clock, EM, or cosmology pass is claimed.

## Result

1872 tried the theorem route first. The verdict is useful but not the magic door:

```text
asymptotic flatness + finite exterior energy  !=  C_R=0
R_AB = C_R/r survives unless a boundary/source theorem kills it.
```

The clean route remains:

```text
free/proper boundary variation + no independent R_AB matter/readout slot
=> Pi_R = 0
=> Q_cur = 0
=> C_R = 0
=> q_R = 0
=> Delta gamma_C_R = 0
```

But the parent action has not signed the boundary variation class, the no-independent-`R_AB` object language, hidden-tail silence, or the absolute no-cancellation residual vector. So 1872 does **not** prove local GR.

What it does add is the safe fallback bound language:

```text
q_R = C_R c^2/(2GM_*)
|C_R| <= (2GM_*/c^2) |Delta gamma|_max
|Delta gamma|_max = 6.7e-05  # conservative local 1852 Cassini row
```

That row is source-string-backed but not claim-ready because `C_R`, same-frame `M_*`, and the no-cancellation residual vector are still missing.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## C_R Zero Audit

{markdown_table(rows_by_name["zero_audit"])}

## Failed Proof Ledger

{markdown_table(rows_by_name["failed_proof_ledger"])}

## Absolute Bound Inputs

{markdown_table(rows_by_name["absolute_bound_inputs"])}

## Bound Rows

{markdown_table(rows_by_name["absolute_bound_rows"])}

## Residual Vector Insert

{markdown_table(rows_by_name["residual_vector"])}

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
