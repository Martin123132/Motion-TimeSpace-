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

DOC = ROOT / "2844-Y5-R2FR-CAB-one-over-r-amplitude-law-or-parent-cancellation-theorem-under-AX1090.md"

SRC_2843_DOC = ROOT / "2843-Y5-R2FR-CAB-target-map-zero-or-finite-tauPPN-source-pack-under-AX1090.md"
SRC_2843_PROFILE = RESIDUALS / "P8_Y5_R2FR_2843_TAUPPN_PROFILE_WITH_CAB_AMPLITUDE.csv"
SRC_2843_PACK = RESIDUALS / "P8_Y5_R2FR_2843_FINITE_TAUPPN_SOURCE_PACK.csv"
SRC_2843_NEXT = RESIDUALS / "P8_Y5_R2FR_2843_NEXT_TARGET.csv"
SRC_2843_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2843_VALIDATION.csv"
SRC_2842_TAU = RESIDUALS / "P8_Y5_R2FR_2842_FINITE_TAUPPN_PROFILE.csv"
SRC_1268 = ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md"
SRC_1882 = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"
SRC_11 = ROOT / "11-cell-current-origin-attempt.md"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2844_SOURCE_REGISTER.csv",
    "flux_identity": RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv",
    "cancellation": RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv",
    "parent_contract": RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv",
    "route_split": RESIDUALS / "P8_Y5_R2FR_2844_ROUTE_SPLIT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2844_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2844_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2844_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2844_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2844_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_pack_copy": LOCAL_BOUNDS / "RAB_CAB_amplitude_source_pack_2844_NONCLAIM.csv",
    "flux_copy": SOURCE_WEIGHT / "RAB_CAB_green_flux_identity_2844_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2844_CAB_source_current_identity_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_CAB_AMPLITUDE_LAW_2844_NONCLAIM.csv",
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
        ("SRC2844_0_2843_doc", SRC_2843_DOC, "A_CAB = -sigma_R q_R_eff/(4 pi);VAL2843_OVERALL", "2843 selected amplitude cancellation target"),
        ("SRC2844_1_2843_profile", SRC_2843_PROFILE, "PROF2843_2_constant_amplitude;PROF2843_3_cancellation_law", "2843 C_AB amplitude profile rows"),
        ("SRC2844_2_2843_pack", SRC_2843_PACK, "PACK2843_0_A_CAB;PACK2843_2_q_R_eff", "2843 missing source pack"),
        ("SRC2844_3_2843_next", SRC_2843_NEXT, "NEXT2843_0_2844", "2843 handoff to 2844"),
        ("SRC2844_4_2843_validation", SRC_2843_VALIDATION, "VAL2843_OVERALL", "2843 validation"),
        ("SRC2844_5_2842_tau", SRC_2842_TAU, "TAUP2842_3_explicit_profile;TAUP2842_5_constant_limit", "2842 finite tauPPN profile"),
        ("SRC2844_6_1268", SRC_1268, "R_AB-C_AB=0;VAR1268_0_E_Lambda;VAR1268_2_aux_elimination", "auxiliary compatibility surface"),
        ("SRC2844_7_1882", SRC_1882, "C_R = R_AB = ln(T^2 S);C_R = 2(p-1)u", "weak-field reciprocal residual identity"),
        ("SRC2844_8_11", SRC_11, "R_AB = -Q_R/r.;conserves Q_R but permits hair.", "one-over-r hair and boundary warning"),
        ("SRC2844_9_10", SRC_10, "R_AB = ln(T^2 S);R_AB = 0", "observer map local GR target"),
    ]
    return [source_row(*spec) for spec in specs]


def flux_identity_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FLUX2844_0_decomposition",
            "C_AB(r)=A_CAB/r+C_AB_reg(r)",
            "outside a compact source, split the PPN-relevant monopole from regular/tail terms",
            "DECOMPOSITION_CONTRACT",
            "A_CAB is the only piece that shifts the constant gamma/PPN residual in the long-range limit",
            True,
        ),
        (
            "FLUX2844_1_surface_amplitude",
            "A_CAB=-(1/(4*pi))*lim_{R->infty} integral_{S_R} R^2 partial_r C_AB dOmega",
            "Gauss extraction of the 1/r coefficient for the sign convention C_AB=A_CAB/r+...",
            "DERIVED_SYMBOLIC_IDENTITY",
            "requires exterior differentiability and no angular monopole ambiguity",
            True,
        ),
        (
            "FLUX2844_2_source_charge",
            "if Laplacian C_AB=-rho_CAB, then A_CAB=(1/(4*pi))*integral rho_CAB d^3x plus boundary/corner terms",
            "turns amplitude into an integrated target-source charge",
            "DERIVED_CONDITIONAL_IDENTITY",
            "operator/sign/boundary convention must be parent-owned before use",
            True,
        ),
        (
            "FLUX2844_3_deltaR_amplitude",
            "A_delta=sigma_R*q_R_eff/(4*pi)",
            "from the 2842/2843 finite Green profile in the ell_R >> r_PPN limit",
            "DERIVED_CONDITIONAL_FROM_PRIOR_PROFILE",
            "sigma_R and q_R_eff are still not source-normalized",
            True,
        ),
        (
            "FLUX2844_4_local_ppn_amplitude",
            "A_total=A_delta+A_CAB=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
            "where Q_CAB:=4*pi*A_CAB under the same Green convention",
            "DERIVED_CONDITIONAL_IDENTITY",
            "only valid once C_AB and delta_R use the same exterior radial convention",
            True,
        ),
        (
            "FLUX2844_5_local_suppression_condition",
            "A_total=0 <=> Q_CAB=-sigma_R*q_R_eff",
            "exact one-over-r cancellation condition for the local gamma/PPN channel",
            "DERIVED_SYMBOLIC_TARGET",
            "this is a target source-current identity, not yet a parent theorem",
            True,
        ),
    ]
    return [
        nonclaim(
            {
                "flux_id": flux_id,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "caveat": caveat,
                "mathematical_identity_recorded": identity,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for flux_id, formula, meaning, status, caveat, identity in specs
    ]


def cancellation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CANCEL2844_0_theorem_statement",
            "If Q_CAB=-sigma_R*q_R_eff, C_AB_reg and H_R are PPN-silent, ell_R>>r_PPN, and other PPN channels close, then the 1/r gamma residual vanishes.",
            "EXACT_CONDITIONAL_THEOREM",
            "the cancellation theorem is mathematically clean but not parent-signed",
            True,
            False,
        ),
        (
            "CANCEL2844_1_parent_source_identity",
            "derive Q_CAB+sigma_R*q_R_eff=0 from parent source/current conservation",
            "NOT_DERIVED",
            "no source-current identity currently ties the target-map charge to the delta_R Green charge",
            False,
            False,
        ),
        (
            "CANCEL2844_2_target_zero_branch",
            "A_CAB=0",
            "INSUFFICIENT_ALONE",
            "if q_R_eff remains nonzero, A_CAB=0 leaves the sigma_R*q_R_eff term in delta_p_const",
            False,
            False,
        ),
        (
            "CANCEL2844_3_delta_zero_branch",
            "q_R_eff=0",
            "INSUFFICIENT_ALONE",
            "if A_CAB remains nonzero, the C_AB target still shifts the PPN residual",
            False,
            False,
        ),
        (
            "CANCEL2844_4_projection_zero_branch",
            "P_PPN(C_AB_reg+H_R)=0 and P_PPN(A_total/r)=0",
            "POSSIBLE_BUT_NOT_DERIVED",
            "needs a real projection operator and arena map, not post-hoc invisibility",
            False,
            False,
        ),
        (
            "CANCEL2844_5_verdict",
            "amplitude cancellation law",
            "CONDITION_DERIVED_PARENT_PROOF_MISSING",
            "the exact condition is now Q_CAB=-sigma_R*q_R_eff; the missing object is the parent identity that enforces it",
            True,
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "cancel_id": cancel_id,
                "target": target,
                "status": status,
                "reason": reason,
                "conditional_theorem_recorded": theorem,
                "parent_theorem_closed": closed,
                "control_only": True,
            }
        )
        for cancel_id, target, status, reason, theorem, closed in specs
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("CONTRACT2844_0_operator", "same exterior Green operator for delta_R and C_AB monopole sector", "L_CAB must share the PPN 1/r normalization or the Q_CAB formula changes", "MISSING_PARENT_OPERATOR"),
        ("CONTRACT2844_1_source_current", "Q_CAB=-sigma_R*q_R_eff", "integrated target source must cancel the finite Green charge", "MISSING_SOURCE_CURRENT_IDENTITY"),
        ("CONTRACT2844_2_boundary", "boundary/corner flux vanishes or is included in Q_CAB", "otherwise conserved hair shifts A_CAB", "MISSING_BOUNDARY_FLUX_LAW"),
        ("CONTRACT2844_3_regular_tail", "r*(C_AB_reg+H_R)->0 across PPN arenas", "regular/tail terms must not mimic a 1/r residual", "MISSING_TAIL_BOUND"),
        ("CONTRACT2844_4_range", "ell_R>>r_PPN or finite-range correction explicitly retained", "the constant-limit formula assumes the exponential is unity", "MISSING_RANGE_HIERARCHY"),
        ("CONTRACT2844_5_sign", "sigma_R sign and Green convention fixed by parent action", "cancellation is sign-sensitive", "MISSING_SIGN_CONVENTION"),
        ("CONTRACT2844_6_measured_GM", "M_source/GM convention matches PPN U=GM/r", "the PPN residual amplitude is measured relative to orbital GM", "MISSING_GM_CONVENTION"),
        ("CONTRACT2844_7_full_vector", "beta/preferred/source/endpoint/clock channels close with the same branch", "gamma-only cancellation is not local GR", "MISSING_FULL_VECTOR_CLOSURE"),
    ]
    return [
        nonclaim(
            {
                "contract_id": contract_id,
                "required_clause": clause,
                "why_needed": why,
                "current_status": status,
                "closed": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for contract_id, clause, why, status in specs
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("PACK2844_0_Q_CAB", "Q_CAB=4*pi*A_CAB", "integrated target-map monopole charge", "same charge convention as q_R_eff", "MISSING_PARENT_INPUT", "derive from target current or source it as finite row"),
        ("PACK2844_1_J_CAB", "rho_CAB or J_CAB", "local source density generating C_AB", "operator-dependent density", "MISSING_SOURCE_DENSITY", "define parent target source functional"),
        ("PACK2844_2_L_CAB", "L_CAB", "operator acting on target map in exterior branch", "differential operator", "MISSING_OPERATOR", "prove Laplacian/Yukawa/common-kernel form"),
        ("PACK2844_3_B_CAB", "boundary flux", "surface/corner contribution to A_CAB", "charge", "MISSING_BOUNDARY_INPUT", "prove zero or include in Q_CAB"),
        ("PACK2844_4_q_R_eff", "q_R_eff", "finite delta_R Green charge", "same charge convention as Q_CAB", "MISSING_SOURCE_NORMALIZATION", "fill prior finite R_AB pack"),
        ("PACK2844_5_tail_bound", "C_AB_reg,H_R", "regular/tail/homogeneous residual bound in PPN arenas", "dimensionless profile", "MISSING_TAIL_BOUND", "derive projection-zero or finite bound"),
        ("PACK2844_6_arena_map", "P_PPN", "projection from local exterior profile to PPN observable vector", "operator/map", "MISSING_ARENA_PROJECTION", "define full local test map"),
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
            "ROUTE2844_0_parent_current",
            "derive Q_CAB=-sigma_R*q_R_eff from parent source-current conservation",
            "SELECTED_NEXT_DERIVATION_TARGET",
            "this is the cleanest route because it makes local GR suppression a charge-balance theorem",
            True,
        ),
        (
            "ROUTE2844_1_operator_identity",
            "prove C_AB is generated by the same Green kernel with opposite compact charge",
            "SECONDARY_DERIVATION_TARGET",
            "would close the amplitude law if paired with boundary silence",
            False,
        ),
        (
            "ROUTE2844_2_finite_rows",
            "source Q_CAB, q_R_eff, boundary flux and full PPN residual vector",
            "FALLBACK_NONCLAIM",
            "needed if no parent current identity exists",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "route": route,
                "status": status,
                "reason": reason,
                "selected_for_next_work": selected,
                "selected_for_claim": False,
            }
        )
        for route_id, route, status, reason, selected in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    specs = [
        ("GATE2844_0_sources", "source-anchor control", all(row["path_exists"] and row["anchors_found"] for row in rows["sources"]), "source anchors for this checkpoint exist"),
        ("GATE2844_1_flux_identity", "symbolic flux identity", True, "Green/Gauss amplitude identity recorded as conditional math only"),
        ("GATE2844_2_parent_current", "parent source-current theorem", False, "Q_CAB=-sigma_R*q_R_eff not parent-derived"),
        ("GATE2844_3_finite_pack", "finite amplitude source pack", False, "Q_CAB, q_R_eff, boundary and arena projection remain missing"),
        ("GATE2844_4_local_GR", "local GR / PPN claim", False, "gamma cancellation alone is insufficient and even gamma cancellation is not parent-signed"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": False,
                "status": "CONTROL_OR_SYMBOLIC_PASS_NONCLAIM" if control_passed and gate_id in {"GATE2844_0_sources", "GATE2844_1_flux_identity"} else "BLOCKED",
                "reason": reason,
                "control_check_passed": control_passed,
            }
        )
        for gate_id, claim, control_passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2844_0_real_progress",
            "The local gamma suppression condition is now an exact charge-balance target.",
            "ACCEPTED_SYMBOLIC_NONCLAIM",
            "A_total=0 iff Q_CAB=-sigma_R*q_R_eff under the shared Green convention",
            "hunt for the parent current identity",
        ),
        (
            "DEC2844_1_not_enough",
            "Do not treat A_CAB=0 or q_R_eff=0 alone as sufficient.",
            "LOCKED",
            "either one can leave the other one-over-r amplitude alive",
            "carry both amplitudes until a theorem or source row closes them",
        ),
        (
            "DEC2844_2_best_next",
            "Build the source-current identity checkpoint next.",
            "SELECTED",
            "the missing proof is no longer vague: it is the parent origin of Q_CAB+sigma_R*q_R_eff=0",
            "create 2845 current identity or finite input rows",
        ),
        (
            "DEC2844_3_no_public_claim",
            "No local-GR/Newton/PPN/R10/WEP/clock/orbital claim.",
            "LOCKED",
            "the theorem is conditional and source pack rows remain missing",
            "keep private",
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
                "next_id": "NEXT2844_0_2845",
                "status": "selected_primary",
                "target_doc": "2845-Y5-R2FR-CAB-source-current-identity-or-finite-amplitude-inputs-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_CAB_source_current_identity_or_finite_amplitude_inputs_under_AX1090_2845.py",
                "mission": "try to derive Q_CAB+sigma_R*q_R_eff=0 from parent source/current conservation, shared Green kernel and boundary silence; otherwise stage finite Q_CAB/q_R_eff/local PPN rows as nonclaim inputs",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2844_0_source_pack", OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"], "portable nonclaim C_AB amplitude source pack"),
        ("COPY2844_1_flux_identity", OUTPUTS["flux_identity"], BRANCH_OUTPUTS["flux_copy"], "portable Green/Gauss amplitude identity"),
        ("COPY2844_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2844_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
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
        "parent_theorem_closed",
        "closed",
        "source_backed",
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
        ("VAL2844_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2844_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2844_2_flux_condition", any(row["flux_id"] == "FLUX2844_5_local_suppression_condition" and "Q_CAB=-sigma_R*q_R_eff" in row["formula"] for row in rows_by_name["flux_identity"]), "Q_CAB charge-balance condition recorded"),
        ("VAL2844_3_parent_not_closed", not any(row["parent_theorem_closed"] for row in rows_by_name["cancellation"]), "parent cancellation theorem remains unclaimed"),
        ("VAL2844_4_contract_blocked", not any(row["closed"] for row in rows_by_name["parent_contract"]), "parent amplitude contract clauses remain open"),
        ("VAL2844_5_source_pack_blocked", not any(row["accepted_ready"] for row in rows_by_name["source_pack"]), "finite amplitude source pack remains unaccepted"),
        ("VAL2844_6_next_target_2845", any(row["next_id"] == "NEXT2844_0_2845" and row["selected"] for row in rows_by_name["next"]), "2845 source-current identity target selected"),
        ("VAL2844_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2844_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2844_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2844_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2844_11_no_claim_flags", no_claim_flags(rows_by_name), "no source/claim/closed flags are true"),
        ("VAL2844_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2844_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2844_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2844_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2844_OVERALL",
            "passed": overall,
            "detail": "2844 derives the symbolic Green/flux amplitude condition A_total=0 iff Q_CAB=-sigma_R*q_R_eff, refuses a parent cancellation claim, and selects the parent source-current identity as the next target.",
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
    content = f"""# 2844 - Y5 R2FR C_AB One-Over-r Amplitude Law Or Parent Cancellation Theorem Under AX1090

Status: `Y5_R2FR_2844_green_flux_amplitude_condition_derived_parent_current_identity_missing_nonclaim`

## Private Verdict

2844 makes the local-GR target sharper. The cancellation condition is no longer vague.

Decompose the target map:

```text
C_AB(r)=A_CAB/r+C_AB_reg(r)
```

For the convention `C_AB=A_CAB/r+...`, the monopole coefficient is:

```text
A_CAB=-(1/(4*pi))*lim_(R->infty) integral_(S_R) R^2 partial_r C_AB dOmega
```

If the parent target equation has the local exterior source convention:

```text
L_CAB C_AB ~ Laplacian C_AB = -rho_CAB
```

then:

```text
A_CAB=(1/(4*pi))*integral rho_CAB d^3x + boundary/corner flux
```

Define `Q_CAB:=4*pi*A_CAB` in that shared Green convention. The 2843 constant-limit residual becomes:

```text
A_total = sigma_R*q_R_eff/(4*pi) + A_CAB
        = (sigma_R*q_R_eff + Q_CAB)/(4*pi)
```

So the exact one-over-r suppression condition is:

```text
Q_CAB = -sigma_R*q_R_eff
```

That is the good news. The bad news, honestly: current sources do **not** derive this parent source-current identity. So 2844 records a real conditional theorem, not a claim. The next target is to hunt the parent identity that could force `Q_CAB+sigma_R*q_R_eff=0`.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Green / Flux Identity

{markdown_table(rows["flux_identity"], ["flux_id", "formula", "status", "caveat", "mathematical_identity_recorded", "valid_for_claim"])}

## Cancellation Theorem Attempt

{markdown_table(rows["cancellation"], ["cancel_id", "target", "status", "reason", "conditional_theorem_recorded", "parent_theorem_closed", "valid_for_claim"])}

## Parent Amplitude Contract

{markdown_table(rows["parent_contract"], ["contract_id", "required_clause", "current_status", "why_needed", "closed", "valid_for_claim"])}

## C_AB Amplitude Source Pack

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
    rows["flux_identity"] = flux_identity_rows()
    rows["cancellation"] = cancellation_rows()
    rows["parent_contract"] = parent_contract_rows()
    rows["source_pack"] = source_pack_rows()
    rows["route_split"] = route_split_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "flux_identity", "cancellation", "parent_contract", "source_pack", "route_split", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2844_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2844_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
