from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1871"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1871-Y5-R2FR-QR-normalization-convention-lock-or-source-denominator-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1871_SOURCE_REGISTER.csv",
    "symbol_split": OUT / "P8_Y5_PARENT_QLOC_1871_QR_SYMBOL_SPLIT_CONVENTION.csv",
    "derivation": OUT / "P8_Y5_PARENT_QLOC_1871_CANONICAL_CR_DENOMINATOR_DERIVATION.csv",
    "collision": OUT / "P8_Y5_PARENT_QLOC_1871_SIGN_KAPPA_COLLISION_AUDIT.csv",
    "denominator_row": OUT / "P8_Y5_PARENT_QLOC_1871_SOURCE_DENOMINATOR_ROW_NONCLAIM.csv",
    "ppn_handoff": OUT / "P8_Y5_PARENT_QLOC_1871_PPN_HANDOFF_ROW_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1871_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1871_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1871_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1871_VALIDATION.csv",
}

SOURCE_NEEDLES = {
    "1870_doc": {
        "path": ROOT / "1870-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md",
        "needles": [
            "CONDITIONAL_QR_TO_qR_DENOMINATOR_FORMULA_FOUND",
            "QR_NORMALIZATION_CONVENTION_LOCK_SELECTED_NEXT",
        ],
    },
    "1870_denominator_gate": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1870_DENOMINATOR_CONVENTION_GATE.csv",
        "needles": [
            "q_R_hat=-Q_R/(2*kappa_W*G*M)+O(GM/r)",
            "q_R=Q_R*c^2/(2*G*M_*)",
            "MISSING_CONVENTION_LOCK",
        ],
    },
    "1581_profile": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1581_QRHAT_PROFILE_DERIVATION.csv",
        "needles": [
            "W(r)=kappa_W r^2",
            "R_AB(r)=R_AB(infinity)-Q_R/(kappa_W r)+O(r^-2)",
            "q_R_hat=R_AB/(2U_N)=-Q_R/(2 kappa_W G M)+O(GM/r)",
        ],
    },
    "1582_denominator": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1582_SOURCE_DENOMINATOR_CONTRACT.csv",
        "needles": [
            "MISSING_QR_VALUE_OR_ZERO_THEOREM",
            "MISSING_WEIGHT_NORMALIZATION",
            "MISSING_SOURCE_DENOMINATOR_CONVENTION",
        ],
    },
    "1638_chain": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1638_PIR_TO_QR_QRLOCAL_CHAIN.csv",
        "needles": [
            "Q_R = -Pi_R",
            "R_AB ~ Q_R/r",
            "q_R = N_R Q_R = -N_R Pi_R",
        ],
    },
    "1638_blockers": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1638_QR_NORMALIZATION_BLOCKER_LEDGER.csv",
        "needles": [
            "W_RAB_EQUATION_NORMALIZATION",
            "N_R_DENOMINATOR_FOR_QR_TO_qR",
            "LOCAL_SOURCE_MASS_AND_L_N_CONVENTION",
        ],
    },
    "1639_denominator": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1639_NR_DENOMINATOR_DERIVATION.csv",
        "needles": [
            "q_R = Q_R c^2/(2 G M_*)",
            "q_R = -Pi_R c^2/(2 G M_*)",
            "N_R_CONDITIONAL_DERIVED",
        ],
    },
    "1639_template": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE.csv",
        "needles": [
            "|q_R| = |Q_R| c^2/(2 G M_*)",
            "MISSING_PARENT_Pi_R_ZERO_THEOREM",
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
        source_path = payload["path"]
        ok, detail = path_has_needles(source_path, payload["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "required_needles": " ; ".join(payload["needles"]),
                "source_exists": source_path.exists(),
                "needle_check": detail,
                "usable_for_1871": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def symbol_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "symbol_id": "SYM1871_0_Qcur",
            "canonical_symbol": "Q_cur",
            "old_aliases": "Q_R in W(r) dR_AB/dr = Q_R; current charge; integration constant",
            "definition": "radial-current charge in the equation W(r) dR_AB/dr = Q_cur",
            "units_or_dimension": "kappa_W times tail coefficient units",
            "canonical_relation": "Q_cur = kappa_W r^2 dR_AB/dr at large r",
            "allowed_use": "derive exterior tail after W normalization is stated",
            "blocked_use": "do not put Q_cur directly into q_R = Q_R c^2/(2GM_*) without the -1/kappa_W tail map",
            "status": "SYMBOL_SPLIT_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "symbol_id": "SYM1871_1_Ctail",
            "canonical_symbol": "C_R",
            "old_aliases": "Q_R in R_AB ~ Q_R/r; tail coefficient",
            "definition": "coefficient of the exterior 1/r reciprocal strain profile R_AB(r)=C_R/r+O(r^-2)",
            "units_or_dimension": "length when R_AB is dimensionless",
            "canonical_relation": "C_R = -Q_cur/kappa_W under W=kappa_W r^2 and R_AB(infinity)=0",
            "allowed_use": "preferred source-denominator input for PPN/orbital handoffs",
            "blocked_use": "not a parent-sourced numeric value; not a theorem-zero",
            "status": "CANONICAL_TAIL_SYMBOL_SELECTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "symbol_id": "SYM1871_2_PiR",
            "canonical_symbol": "Pi_R",
            "old_aliases": "boundary momentum; reciprocal boundary charge",
            "definition": "boundary conjugate object appearing in delta S_boundary=[W R_AB' + Pi_R] delta R_AB",
            "units_or_dimension": "same as Q_cur after orientation and W convention are fixed",
            "canonical_relation": "Q_cur = -Pi_R only after the boundary orientation/sign convention is signed",
            "allowed_use": "exact-GR route if Pi_R=0 is parent-signed; finite-tail bound route if |Pi_R| is source-bounded",
            "blocked_use": "do not identify Pi_R with C_R until kappa_W and sign orientation are fixed",
            "status": "BOUNDARY_RELATION_SYMBOLIC_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "symbol_id": "SYM1871_3_qR",
            "canonical_symbol": "q_R",
            "old_aliases": "q_R_hat if c=1 and U_N is dimensionless; local reciprocal load coefficient",
            "definition": "dimensionless local residual amplitude defined by R_AB=q_R L_N with L_N=2GM_*/(r c^2)",
            "units_or_dimension": "dimensionless",
            "canonical_relation": "q_R = C_R c^2/(2 G M_*)",
            "allowed_use": "PPN/orbital residual handoff after C_R and same-frame M_* are defined",
            "blocked_use": "not R10 alpha(lambda); massless 1/r hair is not finite-range Yukawa data",
            "status": "CANONICAL_LOCAL_AMPLITUDE_SELECTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_0_current_equation",
            "input": "W(r) dR_AB/dr = Q_cur",
            "operation": "rename the current/integration constant so it is not confused with the tail coefficient",
            "output": "Q_cur := W(r) dR_AB/dr",
            "assumptions": "static exterior; same radial cell as 1581; ordinary current not killed",
            "status": "CANONICAL_RENAME",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_1_asymptotic_weight",
            "input": "W(r)=kappa_W r^2[1+O(GM/r)]",
            "operation": "solve the large-r derivative equation",
            "output": "dR_AB/dr = Q_cur/(kappa_W r^2)+O(r^-3)",
            "assumptions": "kappa_W is not numerically sourced; sign convention follows 1581 derivative",
            "status": "CONDITIONAL_ASYMPTOTIC_WEIGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_2_tail_coefficient",
            "input": "dR_AB/dr = Q_cur/(kappa_W r^2), R_AB(infinity)=0",
            "operation": "integrate from infinity to r",
            "output": "R_AB(r)=C_R/r+O(r^-2), with C_R=-Q_cur/kappa_W",
            "assumptions": "constant asymptotic offset removed by local vacuum boundary condition; tails still nonclaim",
            "status": "TAIL_MAP_CONDITIONAL_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_3_newtonian_load",
            "input": "L_N(r)=2GM_*/(r c^2)",
            "operation": "use the same-frame source load, not observed orbital-GM backfill",
            "output": "R_AB=q_R L_N defines q_R",
            "assumptions": "M_* is the parent source mass appearing in the observer-map Newtonian limit",
            "status": "SOURCE_DENOMINATOR_CONVENTION_SELECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_4_canonical_amplitude_law",
            "input": "R_AB=C_R/r and L_N=2GM_*/(r c^2)",
            "operation": "match the common 1/r radial dependence",
            "output": "q_R = C_R c^2/(2 G M_*) = -Q_cur c^2/(2 kappa_W G M_*)",
            "assumptions": "C_R and M_* are in the same frame and units; no cancellation budget assumed",
            "status": "CANONICAL_DENOMINATOR_ROW_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "DER1871_5_boundary_substitution",
            "input": "Q_cur = -Pi_R",
            "operation": "substitute only if boundary orientation/sign convention is parent-signed",
            "output": "q_R = Pi_R c^2/(2 kappa_W G M_*) under the 1581 current convention",
            "assumptions": "the sign flips relative to 1639 if 1639's Q_R meant tail coefficient rather than current charge",
            "status": "BOUNDARY_SUBSTITUTION_SIGN_LOCK_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def collision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "collision_id": "COL1871_0_QR_overload",
            "object": "Q_R",
            "observed_collision": "1581 uses Q_R as W-current charge; 1639 uses Q_R as exterior 1/r tail coefficient",
            "repair": "reserve Q_cur for the current charge and C_R for the tail coefficient",
            "mathematical_relation": "C_R=-Q_cur/kappa_W",
            "status": "OVERLOAD_DETECTED_REPAIRED_BY_SYMBOL_SPLIT",
            "convention_locked": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "collision_id": "COL1871_1_sign",
            "object": "Pi_R sign",
            "observed_collision": "Q_cur=-Pi_R plus C_R=-Q_cur/kappa_W gives C_R=Pi_R/kappa_W, while 1639 wrote q_R=-Pi_R c^2/(2GM_*)",
            "repair": "treat 1639's Q_R=-Pi_R as a tail-coefficient convention until boundary orientation is re-derived",
            "mathematical_relation": "q_R = C_R c^2/(2GM_*); Pi_R substitution is held",
            "status": "SIGN_ORIENTATION_NOT_PARENT_LOCKED",
            "convention_locked": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "collision_id": "COL1871_2_kappa",
            "object": "kappa_W",
            "observed_collision": "tail-coefficient formula hides kappa_W; current-charge formula requires it",
            "repair": "all future score rows must state whether input amplitude is C_R or Q_cur",
            "mathematical_relation": "N_C=c^2/(2GM_*), N_Q=-c^2/(2kappa_W GM_*)",
            "status": "KAPPA_DEPENDENCE_EXPLICIT",
            "convention_locked": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "collision_id": "COL1871_3_qhat",
            "object": "q_R_hat",
            "observed_collision": "1581 q_R_hat omits c^2 because it uses U_N in c=1 style, while 1639 uses L_N=2GM/(r c^2)",
            "repair": "use q_R as the canonical dimensionless load amplitude; q_R_hat is an alias only in c=1 or after explicit unit conversion",
            "mathematical_relation": "q_R = c^2 q_R_hat if q_R_hat denominator is 2GM/r in SI units; q_R=q_R_hat in c=1",
            "status": "UNIT_ALIAS_LOCKED_NONCLAIM",
            "convention_locked": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def denominator_row() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SD1871_0_canonical_C_R_denominator",
            "canonical_prediction_variable": "q_R",
            "input_amplitude": "C_R",
            "formula": "q_R = C_R c^2/(2 G M_*)",
            "equivalent_current_charge_formula": "q_R = -Q_cur c^2/(2 kappa_W G M_*)",
            "boundary_formula_held": "if Q_cur=-Pi_R then q_R=Pi_R c^2/(2 kappa_W G M_*), pending boundary sign lock",
            "required_inputs": "C_R or Q_cur; kappa_W if using Q_cur; same-frame M_*; G and c convention; no-cancellation residual budget",
            "units": "C_R:length, Q_cur:kappa_W*length, M_*:mass, q_R:dimensionless",
            "source_paths": ";".join(str(SOURCE_NEEDLES[key]["path"]) for key in ["1581_profile", "1638_chain", "1639_denominator"]),
            "current_status": "SYMBOLIC_CONVENTION_LOCK_READY_NONCLAIM",
            "convention_locked": True,
            "numeric_value_present": False,
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def ppn_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "PPN1871_0_massless_tail",
            "arena": "PPN/orbital",
            "amplitude_input": "C_R",
            "prediction_template": "Delta gamma ~= q_R = C_R c^2/(2 G M_*)",
            "blocked_by": "MISSING_NUMERIC_C_R_OR_ZERO_THEOREM;MISSING_SAME_FRAME_MSTAR;MISSING_NO_CANCELLATION_BUDGET;MISSING_EXTERNAL_BOUND_SOURCE",
            "routing_rule": "massless 1/r tail routes to PPN/orbital, not R10 alpha(lambda)",
            "current_status": "HANDOFF_TEMPLATE_READY_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "PPN1871_1_exact_GR_route",
            "arena": "local GR reduction",
            "amplitude_input": "C_R=0 or Pi_R=0 with signed boundary relation",
            "prediction_template": "C_R=0 -> q_R=0 -> Delta gamma=0",
            "blocked_by": "MISSING_PARENT_C_R_ZERO_THEOREM_OR_PiR_ZERO_THEOREM",
            "routing_rule": "derive theorem-zero before claiming local-GR recovery",
            "current_status": "EXACT_GR_ROUTE_CLARIFIED_NOT_PROVED",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "handoff_id": "PPN1871_2_R10_guard",
            "arena": "R10",
            "amplitude_input": "C_R",
            "prediction_template": "do not convert C_R/r massless hair into alpha(lambda)",
            "blocked_by": "FINITE_RANGE_OWNER_MISSING_ZR_MR2_LAMBDA",
            "routing_rule": "only Z_R>0 and M_R^2>0 finite Yukawa branch may enter R10 alpha(lambda)",
            "current_status": "R10_MASSLESS_HAIR_GUARD_RETAINED",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1871_0_symbolic_convention",
            "claim": "Q_R normalization convention is now safe enough for nonclaim handoff rows",
            "status": "ALLOW_SYMBOLIC_HANDOFF_ONLY",
            "reason": "C_R separates tail coefficient from Q_cur; q_R denominator is explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1871_1_local_GR",
            "claim": "local GR recovered",
            "status": "BLOCKED",
            "reason": "C_R=0/Pi_R=0 is not parent-signed and no residual no-cancellation theorem exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1871_2_PPN_score",
            "claim": "PPN residual score can be computed",
            "status": "BLOCKED",
            "reason": "numeric C_R or source-bound Pi_R, same-frame M_*, and external gamma/orbital bound are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1871_3_R10_score",
            "claim": "R10 alpha(lambda) can be scored from this massless tail",
            "status": "FORBIDDEN",
            "reason": "C_R/r is a massless PPN/orbital hair; R10 needs finite Z_R/M_R^2/lambda branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1871_0_result",
            "decision": "CANONICAL_C_R_DENOMINATOR_CONVENTION_LOCKED_NONCLAIM",
            "reason": "the apparent 1581/1639 denominator collision is repaired by distinguishing current charge Q_cur from tail coefficient C_R",
            "consequence": "future PPN/orbital handoffs should use C_R; future current/boundary handoffs must include -1/kappa_W and sign orientation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1871_1_blocker",
            "decision": "SIGN_AND_PARENT_INPUTS_STILL_BLOCK_LOCAL_CLAIM",
            "reason": "Pi_R substitution, kappa_W numeric normalization, C_R value/zero theorem, M_* source frame, and no-cancellation budget are not parent-signed",
            "consequence": "do not claim local GR, PPN, orbital, R10, WEP, clock, or EM pass from 1871",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1871_2_next",
            "decision": "CR_ZERO_OR_ABSOLUTE_TAIL_BOUND_SELECTED_NEXT",
            "reason": "once C_R is canonical, the sharp next fork is theorem-zero C_R=0/Pi_R=0 versus source-bounded finite C_R",
            "consequence": "1872 should either prove C_R=0 from boundary silence or stage source-ready C_R/Pi_R/Delta_gamma bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1871_0_primary",
            "target_doc": "1872-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md",
            "target_script": "scripts/Y5_R2FR_CR_zero_theorem_or_absolute_tail_bound_row_1872.py",
            "objective": "try to prove C_R=0 from boundary silence/source neutrality; if not, stage source-ready absolute C_R/Pi_R/Delta_gamma bound rows using the 1871 denominator convention.",
            "selection_status": "selected",
            "success_condition": "parent-signed C_R=0/Pi_R=0 theorem, or nonclaim bound ledger with C_R, M_*, Delta gamma source, no-cancellation envelope, and units explicit.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1871_1_parallel_range",
            "target_doc": "1871c-Y5-R2FR-ZR-MR2-range-owner-or-Yukawa-row.md",
            "target_script": "scripts/Y5_R2FR_ZR_MR2_range_owner_or_Yukawa_row_1871c.py",
            "objective": "separately source Z_R/M_R^2/lambda_range for the finite R10 branch; do not mix with C_R/r massless hair.",
            "selection_status": "held_parallel",
            "success_condition": "same-normalized finite-range owner or explicit blocker.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "symbol_split": symbol_split_rows(),
        "derivation": derivation_rows(),
        "collision": collision_rows(),
        "denominator_row": denominator_row(),
        "ppn_handoff": ppn_handoff_rows(),
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
    parsed: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        parsed.append(f"{path.name}:{len(rows)}")
    return True, ";".join(parsed)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1871_NEXT_TARGET_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["denominator_row"], QUEUE / "JR1871_CANONICAL_CR_DENOMINATOR_ROW_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_with_validation = generated_without_validation + [OUTPUTS["validation"]]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    source_rows = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1871_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1871"]) == "true" for row in source_rows) else "FAIL",
            "detail": "all cited sources exist and contain required needles",
            "valid_for_claim": False,
        }
    )

    derivation = rows_by_name["derivation"]
    checks.append(
        {
            "validation_id": "VAL1871_1_C_R_map",
            "status": "PASS"
            if any("C_R=-Q_cur/kappa_W" in row["output"] for row in derivation)
            and any("q_R = C_R c^2/(2 G M_*)" in row["output"] for row in derivation)
            else "FAIL",
            "detail": "canonical tail-coefficient denominator map is derived conditionally",
            "valid_for_claim": False,
        }
    )

    collision = rows_by_name["collision"]
    checks.append(
        {
            "validation_id": "VAL1871_2_QR_overload_detected",
            "status": "PASS"
            if any(row["status"] == "OVERLOAD_DETECTED_REPAIRED_BY_SYMBOL_SPLIT" for row in collision)
            and any(row["status"] == "SIGN_ORIENTATION_NOT_PARENT_LOCKED" for row in collision)
            else "FAIL",
            "detail": "Q_R overload is repaired symbolically but sign orientation remains blocked",
            "valid_for_claim": False,
        }
    )

    denom = rows_by_name["denominator_row"]
    checks.append(
        {
            "validation_id": "VAL1871_3_denominator_row",
            "status": "PASS"
            if len(denom) == 1
            and denom[0]["current_status"] == "SYMBOLIC_CONVENTION_LOCK_READY_NONCLAIM"
            and bool_string(denom[0]["convention_locked"]) == "true"
            and bool_string(denom[0]["score_ready"]) == "false"
            else "FAIL",
            "detail": "one symbolic denominator convention row exists and remains unscored",
            "valid_for_claim": False,
        }
    )

    ppn = rows_by_name["ppn_handoff"]
    checks.append(
        {
            "validation_id": "VAL1871_4_handoffs_blocked",
            "status": "PASS"
            if any(row["current_status"] == "HANDOFF_TEMPLATE_READY_NONCLAIM" for row in ppn)
            and any(row["current_status"] == "R10_MASSLESS_HAIR_GUARD_RETAINED" for row in ppn)
            and all(bool_string(row["score_ready"]) == "false" for row in ppn)
            else "FAIL",
            "detail": "PPN handoff exists but R10 route is guarded and all rows remain blocked",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1871_5_claim_gates",
            "status": "PASS"
            if any(row["status"] == "ALLOW_SYMBOLIC_HANDOFF_ONLY" for row in claims)
            and any(row["status"] == "FORBIDDEN" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "symbolic handoff allowed, every physics claim blocked or forbidden",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1871_6_decision",
            "status": "PASS"
            if any(row["decision"] == "CANONICAL_C_R_DENOMINATOR_CONVENTION_LOCKED_NONCLAIM" for row in decisions)
            and any(row["decision"] == "CR_ZERO_OR_ABSOLUTE_TAIL_BOUND_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger selects C_R zero theorem or absolute tail bound next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1871_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1871_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1872 target is selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1871_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1871_9_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["denominator_row"].name,
        QUARANTINE / OUTPUTS["denominator_row"].name,
        QUEUE / "JR1871_CANONICAL_CR_DENOMINATOR_ROW_NONCLAIM.csv",
        QUEUE / "JR1871_NEXT_TARGET_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1871_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1871_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1871*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1871_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1871_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1871_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1871 QR normalization convention lock or source-denominator row checkpoint",
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
    content = f"""# 1871 - QR Normalization Convention Lock Or Source Denominator Row

**Private status:** nonclaim checkpoint. No local-GR, PPN, orbital, R10, WEP, clock, EM, or cosmology pass is claimed.

## Result

1871 resolves the immediate notation trap:

```text
Q_cur := W(r) dR_AB/dr
W(r) = kappa_W r^2
R_AB(r) = C_R/r + O(r^-2)
C_R = -Q_cur/kappa_W
L_N = 2GM_*/(r c^2)
q_R = C_R c^2/(2GM_*) = -Q_cur c^2/(2 kappa_W GM_*)
```

So the apparent 1581/1639 collision is not yet a physics contradiction. It is an overloaded-symbol problem: old rows used `Q_R` both as the radial current charge and as the exterior `1/r` tail coefficient. This checkpoint selects `C_R` as the canonical tail input for future PPN/orbital handoffs.

The grim bit, kept explicit: `Pi_R` sign/orientation, `kappa_W`, same-frame `M_*`, `C_R=0` or finite `C_R`, and the no-cancellation residual budget are still not parent-signed. So this is progress on the coupling language, not a local-GR claim.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Symbol Split

{markdown_table(rows_by_name["symbol_split"])}

## Canonical Derivation

{markdown_table(rows_by_name["derivation"])}

## Collision Audit

{markdown_table(rows_by_name["collision"])}

## Denominator Row

{markdown_table(rows_by_name["denominator_row"])}

## PPN Handoff

{markdown_table(rows_by_name["ppn_handoff"])}

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
