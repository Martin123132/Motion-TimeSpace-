from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2843-Y5-R2FR-CAB-target-map-zero-or-finite-tauPPN-source-pack-under-AX1090.md"

SRC_2842_DOC = ROOT / "2842-Y5-R2FR-PPN-bridge-condition-closure-or-finite-tauPPN-profile-under-AX1090.md"
SRC_2842_CAB = RESIDUALS / "P8_Y5_R2FR_2842_CAB_TARGET_MAP_LEDGER.csv"
SRC_2842_TAU = RESIDUALS / "P8_Y5_R2FR_2842_FINITE_TAUPPN_PROFILE.csv"
SRC_2842_NEXT = RESIDUALS / "P8_Y5_R2FR_2842_NEXT_TARGET.csv"
SRC_2842_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2842_VALIDATION.csv"
SRC_1265 = ROOT / "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md"
SRC_1268 = ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md"
SRC_1270 = ROOT / "1270-Y5-R10-RAB-quotient-map-parent-sort-derivation-or-finite-ZR-first-source-row.md"
SRC_1882 = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"
SRC_11 = ROOT / "11-cell-current-origin-attempt.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2843_SOURCE_REGISTER.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_2843_CAB_ZERO_THEOREM_ATTEMPT.csv",
    "variational": RESIDUALS / "P8_Y5_R2FR_2843_CAB_VARIATIONAL_MEANING.csv",
    "profile_update": RESIDUALS / "P8_Y5_R2FR_2843_TAUPPN_PROFILE_WITH_CAB_AMPLITUDE.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2843_FINITE_TAUPPN_SOURCE_PACK.csv",
    "route_split": RESIDUALS / "P8_Y5_R2FR_2843_ROUTE_SPLIT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2843_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2843_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2843_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2843_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2843_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_pack_copy": LOCAL_BOUNDS / "RAB_CAB_finite_tauPPN_source_pack_2843_NONCLAIM.csv",
    "zero_copy": SOURCE_WEIGHT / "RAB_CAB_zero_theorem_attempt_2843_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2843_CAB_amplitude_law_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_CAB_TARGET_MAP_OR_AMPLITUDE_LAW_2843_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2843_0_2842_doc", SRC_2842_DOC, "C_R(r)=delta_R(r)+C_AB[Q](r);C_AB[Q]=0", "2842 target-map split and zero-route blocker"),
        ("SRC2843_1_2842_cab", SRC_2842_CAB, "CAB2842_1_zero_route;CAB2842_2_source_route", "2842 C_AB ledger"),
        ("SRC2843_2_2842_tau", SRC_2842_TAU, "TAUP2842_3_explicit_profile;TAUP2842_5_constant_limit", "2842 tau_PPN profile with target-map term"),
        ("SRC2843_3_2842_next", SRC_2842_NEXT, "NEXT2842_0_2843", "2842 selected C_AB target-map checkpoint"),
        ("SRC2843_4_2842_validation", SRC_2842_VALIDATION, "VAL2842_OVERALL", "2842 validation"),
        ("SRC2843_5_1265", SRC_1265, "AP1265_0_auxiliary_signature;AET1265_0_auxiliary_elimination", "auxiliary elimination conditional route"),
        ("SRC2843_6_1268", SRC_1268, "CAC1268_1_constraint_action;VAR1268_0_E_Lambda;VAR1268_2_aux_elimination", "second-class compatibility action"),
        ("SRC2843_7_1270", SRC_1270, "QSR1270_3_auxiliary_before_q;ROUTE1270_1_auxiliary_compatibility", "best non-smuggling route is auxiliary compatibility"),
        ("SRC2843_8_1882", SRC_1882, "C_R = R_AB = ln(T^2 S);C_R = 2(p-1)u;CRID1882_0_definitions", "C_R/R_AB and PPN residual identity"),
        ("SRC2843_9_10", SRC_10, "R_AB = ln(T^2 S);R_AB = 0", "observer map reciprocal-lock target"),
        ("SRC2843_10_11", SRC_11, "R_AB = -Q_R/r.;conserves Q_R but permits hair.", "boundary hair warning"),
    ]
    return [source_row(*spec) for spec in specs]


def zero_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ZC2843_0_definition",
            "delta_R=R_AB-C_AB[Q]",
            "A zero proof must act on C_AB[Q], not merely on delta_R or R_AB.",
            "OPEN_TARGET_MAP_TERM",
            "definition exposes C_AB as an independent target-map contribution until parent-signed",
            False,
        ),
        (
            "ZC2843_1_aux_constraint",
            "S_aux=integral mu Lambda_R (R_AB-C_AB[Q])",
            "Varying Lambda_R gives R_AB=C_AB[Q].",
            "TARGET_EQUATION_NOT_ZERO_THEOREM",
            "the compatibility block equates R_AB to the target; it does not prove the target itself vanishes",
            False,
        ),
        (
            "ZC2843_2_local_GR_requirement",
            "C_R=R_AB=delta_R+C_AB[Q]",
            "Local GR/PPN suppression requires the observed C_R projection to vanish or be bounded.",
            "ZERO_OF_OBSERVED_COMBINATION_REQUIRED",
            "zeroing only the incompatibility residual delta_R can still leave C_R=C_AB[Q]",
            False,
        ),
        (
            "ZC2843_3_possible_zero_route",
            "C_AB[Q]=0",
            "This would recover the 2841 constant q_R_eff bridge in the long-range/no-boundary limit.",
            "POSSIBLE_BUT_NOT_DERIVED",
            "no parent action row currently signs target-map zero in the local exterior branch",
            False,
        ),
        (
            "ZC2843_4_possible_projection_zero",
            "P_PPN C_AB[Q]=0",
            "A weaker proof could show C_AB is nonzero but invisible to the local PPN projection.",
            "POSSIBLE_BUT_NOT_DERIVED",
            "requires an explicit projection operator and exterior solution class",
            False,
        ),
        (
            "ZC2843_5_zero_verdict",
            "derive C_AB[Q]=0",
            "The zero theorem is not available from the current source stack.",
            "NOT_PROVED",
            "carry C_AB into the finite tau_PPN profile or derive a parent amplitude cancellation law",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "zero_id": zero_id,
                "object": obj,
                "attempt": attempt,
                "current_status": status,
                "blocker_or_next_need": blocker,
                "target_zero_closed": closed,
                "zero_theorem_closed": False,
                "control_only": True,
            }
        )
        for zero_id, obj, attempt, status, blocker, closed in specs
    ]


def variational_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VAR2843_0_aux_action",
            "S_aux=integral mu_parent Lambda_R (R_AB-C_AB[q,theta,top])",
            "parent compatibility block proposed by 1268",
            "CONDITIONAL_ACTION_FORM",
            "parent necessity remains unsigned",
        ),
        (
            "VAR2843_1_E_Lambda",
            "delta_Lambda S_aux=0 -> R_AB-C_AB[q,theta,top]=0",
            "sets the auxiliary surface",
            "EXACT_WITHIN_CANDIDATE",
            "this is a target equation, not C_AB=0",
        ),
        (
            "VAR2843_2_E_R",
            "delta_R S_total=0 -> Lambda_R+J_R+dB_R/dR_AB+readout_regen_terms=0",
            "kills Lambda_R only when sources, boundary and readout regeneration vanish",
            "SOURCE_SILENCE_REQUIRED",
            "same unsigned protection stack as 1265/1268",
        ),
        (
            "VAR2843_3_exact_surface",
            "delta_R=R_AB-C_AB=0 and C_R=R_AB=C_AB",
            "if the auxiliary block is exact, C_AB becomes the exterior reciprocal target",
            "C_AB_STILL_OBSERVABLE_UNLESS_ZERO_OR_PROJECTED_OUT",
            "local GR needs C_AB PPN projection zero or cancellation",
        ),
        (
            "VAR2843_4_finite_surface",
            "C_R(r)=delta_R(r)+C_AB(r)",
            "finite source/profile branch must carry both terms",
            "PROFILE_CONTRACT_UPDATED",
            "future tau_PPN rows must include C_AB amplitude and regular tail",
        ),
    ]
    return [
        nonclaim(
            {
                "variational_id": row_id,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_blocker": blocker,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for row_id, formula, meaning, status, blocker in specs
    ]


def profile_update_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PROF2843_0_general_profile",
            "delta_p(r)=sigma_R*q_R_eff*c^2*exp(-r/ell_R)/(8*pi*G*M_source)+c^2*r*(H_R(r)+C_AB(r))/(2*G*M_source)",
            "2842 profile retained with C_AB explicit",
            "DERIVED_CONDITIONAL_PROFILE",
            "all amplitudes and source conventions remain missing",
        ),
        (
            "PROF2843_1_CAB_decomposition",
            "C_AB(r)=A_CAB/r+C_AB_reg(r)",
            "minimal exterior decomposition needed for PPN constant-limit testing",
            "DERIVED_REQUIREMENT",
            "A_CAB and C_AB_reg are not sourced",
        ),
        (
            "PROF2843_2_constant_amplitude",
            "if ell_R>>r_PPN and H_R,C_AB_reg negligible: delta_p_const=c^2/(2*G*M_source)*(sigma_R*q_R_eff/(4*pi)+A_CAB)",
            "C_AB contributes an independent constant PPN amplitude",
            "DERIVED_CONDITIONAL_LIMIT",
            "cannot use 2841 bridge unless A_CAB=0 or a cancellation law is parent-derived",
        ),
        (
            "PROF2843_3_cancellation_law",
            "local-GR gamma suppression needs sigma_R*q_R_eff/(4*pi)+A_CAB -> 0 in the PPN exterior limit",
            "the safer derivation target is an amplitude law, not a silent target-zero axiom",
            "NEW_DERIVATION_TARGET_NONCLAIM",
            "requires parent compatibility/source equation for A_CAB",
        ),
        (
            "PROF2843_4_qRhat_with_CAB",
            "q_R_hat_const=-c^2/(G*M_source)*(sigma_R*q_R_eff/(4*pi)+A_CAB)",
            "constant q_R_hat bridge corrected by target-map amplitude",
            "DERIVED_CONDITIONAL_LIMIT",
            "not numeric and not source-backed",
        ),
    ]
    return [
        nonclaim(
            {
                "profile_id": profile_id,
                "formula": formula,
                "role": role,
                "status": status,
                "blocker": blocker,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for profile_id, formula, role, status, blocker in specs
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("PACK2843_0_A_CAB", "A_CAB", "coefficient of the 1/r exterior target-map term C_AB=A_CAB/r+...", "same units as C_R*r", "MISSING_PARENT_INPUT", "derive or source from parent target map"),
        ("PACK2843_1_CAB_reg", "C_AB_reg(r)", "regular/non-1/r exterior tail of C_AB", "dimensionless", "MISSING_PROFILE_INPUT", "source exterior solution or projection bound"),
        ("PACK2843_2_q_R_eff", "q_R_eff", "compact-source amplitude in delta_R Green profile", "source-dependent", "MISSING_SOURCE_NORMALIZATION", "fill finite R_AB normalization pack"),
        ("PACK2843_3_ell_R", "ell_R", "range in exp(-r/ell_R)", "length", "MISSING_RANGE", "derive or bound range hierarchy for PPN arenas"),
        ("PACK2843_4_sigma_R", "sigma_R", "sign convention for the R_AB Green profile", "dimensionless sign", "MISSING_SIGN", "source action sign"),
        ("PACK2843_5_H_R", "H_R(r)", "homogeneous/boundary exterior solution", "dimensionless", "MISSING_BOUNDARY_CLASS", "no-boundary-charge theorem or finite boundary row"),
        ("PACK2843_6_GM", "M_source / measured GM", "PPN U=GM/r convention and mass renormalization rule", "mass or GM", "MISSING_GM_CONVENTION", "tie source mass to measured orbital GM"),
        ("PACK2843_7_b_R", "b_R", "no-shadow/readout coefficient controlling other PPN channels", "dimensionless or source-specific", "MISSING_NO_SHADOW_INPUT", "derive no-shadow clause or bound channel"),
        ("PACK2843_8_full_vector", "PPN residual vector", "beta, gamma, preferred-frame, source, endpoint and clock channels", "dimensionless vector", "MISSING_ARENA_PROJECTION", "must not score gamma alone"),
        ("PACK2843_9_source_paths", "source anchors", "local proof/data path for every coefficient", "path+anchor", "MISSING_SOURCE_PATHS", "required before valid_for_claim=true"),
    ]
    return [
        nonclaim(
            {
                "pack_id": pack_id,
                "quantity": quantity,
                "description": desc,
                "units_or_type": units,
                "current_status": status,
                "next_action": action,
                "accepted_ready": False,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for pack_id, quantity, desc, units, status, action in specs
    ]


def route_split_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE2843_0_target_zero",
            "prove C_AB[Q]=0 or P_PPN C_AB[Q]=0",
            "parent target-map theorem or explicit projection-zero theorem",
            "BLOCKED_NOT_PARENT_SIGNED",
            "cleanest if true, but current compatibility equation gives R_AB=C_AB rather than C_AB=0",
            False,
        ),
        (
            "ROUTE2843_1_amplitude_cancellation",
            "derive A_CAB=-sigma_R*q_R_eff/(4*pi)",
            "parent exterior amplitude law tying target map to finite source amplitude",
            "SELECTED_NEXT_DERIVATION_TARGET",
            "this would suppress the PPN 1/r piece without pretending C_AB is absent",
            True,
        ),
        (
            "ROUTE2843_2_finite_pack",
            "source A_CAB, q_R_eff, ell_R, H_R and full PPN vector",
            "real finite source/profile rows with arena projections",
            "FALLBACK_NONCLAIM",
            "needed if no cancellation/zero theorem exists",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "route": route,
                "requirements": req,
                "status": status,
                "reason": reason,
                "selected_for_next_work": selected,
                "selected_for_claim": False,
            }
        )
        for route_id, route, req, status, reason, selected in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    specs = [
        ("GATE2843_0_sources", all(row["path_exists"] and row["anchors_found"] for row in rows["sources"]), "source anchors for this checkpoint exist"),
        ("GATE2843_1_CAB_zero", False, "C_AB zero theorem not parent-signed"),
        ("GATE2843_2_CAB_amplitude", False, "A_CAB amplitude/cancellation law not derived"),
        ("GATE2843_3_finite_pack", False, "finite source pack remains missing/nonclaim"),
        ("GATE2843_4_PPN_claim", False, "PPN/local-GR claim requires full vector, measured GM, range, boundary and C_AB terms"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": False,
                "status": "CONTROL_SOURCE_CHECK_ONLY" if gate_id == "GATE2843_0_sources" and passed else "BLOCKED",
                "reason": reason,
                "control_check_passed": passed,
            }
        )
        for gate_id, passed, reason in specs
        for claim in [gate_id.replace("GATE2843_", "")]
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2843_0_zero_attempt",
            "Do not claim C_AB[Q]=0.",
            "REJECTED_FOR_NOW",
            "the auxiliary compatibility equation gives R_AB=C_AB, not target zero",
            "carry C_AB explicitly",
        ),
        (
            "DEC2843_1_profile_contract",
            "Update tau_PPN profile contract with A_CAB.",
            "ACCEPTED_SYMBOLIC_NONCLAIM",
            "the 1/r component of C_AB shifts the same constant PPN amplitude as q_R_eff",
            "future local tests must include A_CAB",
        ),
        (
            "DEC2843_2_best_next",
            "Attack the amplitude law before fitting finite rows.",
            "SELECTED",
            "a parent law A_CAB=-sigma_R*q_R_eff/(4*pi) would be a real derivation-style route to local GR",
            "build 2844 amplitude-law/cancellation checkpoint",
        ),
        (
            "DEC2843_3_public_status",
            "No R10, PPN, WEP, clock, orbital, Newton/GR or local-GR claim.",
            "LOCKED",
            "all physics rows are symbolic/nonclaim and source pack remains missing",
            "keep private until gates close",
        ),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": action,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2843_0_2844",
                "status": "selected_primary",
                "target_doc": "2844-Y5-R2FR-CAB-one-over-r-amplitude-law-or-parent-cancellation-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_CAB_one_over_r_amplitude_law_or_parent_cancellation_theorem_under_AX1090_2844.py",
                "mission": "decompose C_AB(r) into A_CAB/r plus regular tail and try to derive A_CAB=-sigma_R*q_R_eff/(4*pi), A_CAB=0, or a projection-zero theorem; otherwise keep finite pack blocked",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2843_0_source_pack", OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"], "portable nonclaim finite source pack"),
        ("COPY2843_1_zero_attempt", OUTPUTS["zero_attempt"], BRANCH_OUTPUTS["zero_copy"], "portable C_AB zero theorem failure ledger"),
        ("COPY2843_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2843_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(src),
                    "copy_path": str(dst),
                    "purpose": purpose,
                    "exists": dst.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_ready",
        "target_zero_closed",
        "zero_theorem_closed",
        "selected_for_claim",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "numeric_prediction", "alpha_predicted", "predicted_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2843_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2843_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2843_2_zero_not_closed", not any(row["target_zero_closed"] for row in rows_by_name["zero_attempt"]), "C_AB zero theorem remains unclaimed"),
        ("VAL2843_3_variational_target_not_zero", any(row["variational_id"] == "VAR2843_1_E_Lambda" and "not C_AB=0" in row["claim_blocker"] for row in rows_by_name["variational"]), "E_Lambda interpreted as target equation, not zero theorem"),
        ("VAL2843_4_profile_has_A_CAB", any(row["profile_id"] == "PROF2843_2_constant_amplitude" and "A_CAB" in row["formula"] for row in rows_by_name["profile_update"]), "A_CAB constant-limit correction recorded"),
        ("VAL2843_5_source_pack_blocked", not any(row["accepted_ready"] for row in rows_by_name["source_pack"]), "finite source pack remains unaccepted"),
        ("VAL2843_6_next_target_2844", any(row["next_id"] == "NEXT2843_0_2844" and row["selected"] for row in rows_by_name["next"]), "2844 amplitude-law target selected"),
        ("VAL2843_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2843_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2843_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2843_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2843_11_no_claim_flags", no_claim_flags(rows_by_name), "no score/source/claim/closed flags are true"),
        ("VAL2843_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2843_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2843_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2843_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2843_OVERALL",
            "passed": overall,
            "detail": "2843 refuses C_AB target-zero, rewrites the local PPN profile with A_CAB, identifies the amplitude-cancellation law as the next derivation target, and keeps all finite source rows nonclaim.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2843 - Y5 R2FR C_AB Target Map Zero Or Finite tauPPN Source Pack Under AX1090

Status: `Y5_R2FR_2843_CAB_zero_not_proved_A_CAB_amplitude_law_selected_nonclaim`

## Private Verdict

2843 blocks the tempting shortcut cleanly: the current corpus does **not** prove `C_AB[Q]=0`.

The auxiliary compatibility route gives:

```text
S_aux = integral mu_parent Lambda_R (R_AB - C_AB[Q])
delta_Lambda S_aux = 0  ->  R_AB = C_AB[Q]
```

That is a target equation, not a target-zero theorem. Since the observed weak-field channel still uses:

```text
C_R(r) = R_AB(r) = delta_R(r) + C_AB(r)
```

the finite local profile must keep `C_AB` alive until a parent action either zeros it, projects it out, or fixes its amplitude.

The useful new result is the constant-limit correction. If:

```text
C_AB(r) = A_CAB/r + C_AB_reg(r)
```

then in the long-range/no-boundary/local exterior limit:

```text
delta_p_const = c^2/(2 G M_source) * (sigma_R q_R_eff/(4 pi) + A_CAB)
q_R_hat_const = -c^2/(G M_source) * (sigma_R q_R_eff/(4 pi) + A_CAB)
```

So the next real derivation target is not a silent plateau axiom. It is an amplitude law:

```text
A_CAB = -sigma_R q_R_eff/(4 pi)
```

or a stronger target-zero/projection-zero theorem. No R10, PPN, WEP, clock, orbital, Newton/GR, or local-GR claim is made.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## C_AB Zero Theorem Attempt

{markdown_table(rows["zero_attempt"], ["zero_id", "object", "current_status", "blocker_or_next_need", "target_zero_closed", "valid_for_claim"])}

## Variational Meaning

{markdown_table(rows["variational"], ["variational_id", "formula", "status", "claim_blocker", "valid_for_claim"])}

## tauPPN Profile With C_AB Amplitude

{markdown_table(rows["profile_update"], ["profile_id", "formula", "status", "blocker", "valid_for_claim"])}

## Finite tauPPN Source Pack

{markdown_table(rows["source_pack"], ["pack_id", "quantity", "units_or_type", "current_status", "next_action", "accepted_ready", "valid_for_claim"])}

## Route Split

{markdown_table(rows["route_split"], ["route_id", "route", "status", "reason", "selected_for_next_work", "selected_for_claim", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["zero_attempt"] = zero_attempt_rows()
    rows["variational"] = variational_rows()
    rows["profile_update"] = profile_update_rows()
    rows["source_pack"] = source_pack_rows()
    rows["route_split"] = route_split_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "zero_attempt", "variational", "profile_update", "source_pack", "route_split", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2843_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2843_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
