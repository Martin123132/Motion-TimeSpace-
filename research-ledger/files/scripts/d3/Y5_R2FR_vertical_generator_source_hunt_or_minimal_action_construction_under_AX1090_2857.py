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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2857-Y5-R2FR-vertical-generator-source-hunt-or-minimal-action-construction-under-AX1090.md"

SRC_2856_DOC = ROOT / "2856-Y5-R2FR-amp-current-continuity-variational-consistency-or-reject-under-AX1090.md"
SRC_2856_NEXT = RESIDUALS / "P8_Y5_R2FR_2856_NEXT_TARGET.csv"
SRC_2856_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2856_VALIDATION.csv"
SRC_2856_OBSTRUCTIONS = RESIDUALS / "P8_Y5_R2FR_2856_OBSTRUCTION_LEDGER.csv"
SRC_2856_CONDITIONAL = RESIDUALS / "P8_Y5_R2FR_2856_CONDITIONAL_THEOREM.csv"
SRC_1666_DOC = ROOT / "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md"
SRC_1665_CVG = RESIDUALS / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv"
SRC_1575_RAB_VERT = RESIDUALS / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv"
SRC_1022_VERTICAL_QUOTIENT = RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv"
SRC_1045_VERTICAL_LIFT = RESIDUALS / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
SRC_1505_DQ_TESTS = RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
SRC_727_DCDAGGER = RESIDUALS / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv"
SRC_727_FIELD_ACTION = RESIDUALS / "P8_Y5_R10_727_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
SRC_670_CERT = RESIDUALS / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv"
SRC_781_ACTION = RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv"
SRC_783_FIELD_MAP = RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv"
SRC_1282_DOUBLET = RESIDUALS / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2857_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_2857_EXISTING_GENERATOR_HUNT.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_2857_MINIMAL_DOUBLET_ACTION_ANSATZ.csv",
    "algebra": RESIDUALS / "P8_Y5_R2FR_2857_ANSATZ_ALGEBRA_CHECK.csv",
    "ownership": RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2857_REJECTION_OR_REENTRY_LEDGER.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2857_SOURCE_REQUEST_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2857_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2857_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2857_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2857_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2857_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ansatz_copy": LOCAL_BOUNDS / "RAB_MINIMAL_DOUBLET_ACTION_ANSATZ_2857_NONCLAIM.csv",
    "ownership_copy": SOURCE_WEIGHT / "RAB_VERTICAL_GENERATOR_OWNERSHIP_GATE_2857_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2857_minimal_doublet_action_consistency_NEXT.csv",
    "request_copy": BETA_DOCS / "RAB_VERTICAL_GENERATOR_SOURCE_REQUEST_2857_NONCLAIM.csv",
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
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2857_0_2856_doc", SRC_2856_DOC, "NEXT2856_0_2857;VAL2856_OVERALL", "2856 handoff"),
        ("SRC2857_1_2856_next", SRC_2856_NEXT, "NEXT2856_0_2857", "2857 selected"),
        ("SRC2857_2_2856_validation", SRC_2856_VALIDATION, "VAL2856_OVERALL", "2856 validation"),
        ("SRC2857_3_2856_obstructions", SRC_2856_OBSTRUCTIONS, "OBS2856_0_generator;OBS2856_1_action", "generator/action blockers"),
        ("SRC2857_4_2856_conditional", SRC_2856_CONDITIONAL, "CT2856_0_conditional_lemma;CT2856_1_integrated_corollary", "conditional theorem"),
        ("SRC2857_5_1666_doc", SRC_1666_DOC, "OLP1666_3_vertical_generator;THM1666_0_statement;BLK1666_1_parent_Omega", "parent object-language packet"),
        ("SRC2857_6_1665_cvg", SRC_1665_CVG, "CVG1665_0_dcdagger_map;CVG1665_7_verdict", "coupling vertical-generator audit"),
        ("SRC2857_7_1575_rab_vert", SRC_1575_RAB_VERT, "VERT1575_1_generator;VERT1575_5_verdict", "R_AB vertical generator attempt"),
        ("SRC2857_8_1022_vertical_quotient", SRC_1022_VERTICAL_QUOTIENT, "VQC1022_3_vertical_generator;VQC1022_7_verdict", "vertical quotient construction"),
        ("SRC2857_9_1045_vertical_lift", SRC_1045_VERTICAL_LIFT, "VLG1045_0_fixed_lift;VLG1045_4_verdict", "vertical lift descent gate"),
        ("SRC2857_10_1505_dq_tests", SRC_1505_DQ_TESTS, "DQT1505_2_apply_Dq;DQT1505_8_acceptance", "Dq verticality tests"),
        ("SRC2857_11_727_dcdagger", SRC_727_DCDAGGER, "DVM727_3_precise_map;DVM727_4_raise_index", "DCdagger to vertical generator map"),
        ("SRC2857_12_727_field_action", SRC_727_FIELD_ACTION, "Gamma_Khat_qloc_sector;matter_readout;boundary_edge", "field-by-field vertical action map"),
        ("SRC2857_13_670_cert", SRC_670_CERT, "VGC670_0_parent_Omega;VGC670_2_field_action;VGC670_6_matter_quotient", "vertical generator certificate"),
        ("SRC2857_14_781_action", SRC_781_ACTION, "MPC781_3_matter_action;MPC781_7_contract_verdict", "minimal parent coupling owner action"),
        ("SRC2857_15_783_field_map", SRC_783_FIELD_MAP, "FM783_1_Q;FM783_7_q_loc", "coupling owner field map"),
        ("SRC2857_16_1282_doublet", SRC_1282_DOUBLET, "RCM1282_4_PPN_vector_lock;RCM1282_6_verdict", "response doublet component audit"),
        ("SRC2857_17_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign", "amplitude source/sign contract"),
    ]
    return [source_row(*spec) for spec in specs]


def hunt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HUNT2857_0_dcdagger_map",
            "DCdagger -> Omega-flat vertical generator",
            str(SRC_727_DCDAGGER),
            "DVM727_3_precise_map;DVM727_4_raise_index",
            "FORMAL_MAP_EXISTS",
            "gives v_X=Omega^{-1}[(DC_X)^dagger X] if parent Omega exists",
            "MISSING_PARENT_OMEGA_AND_FIELD_ACTION",
            False,
        ),
        (
            "HUNT2857_1_rab_generator",
            "R_AB vertical generator v_R",
            str(SRC_1575_RAB_VERT),
            "VERT1575_1_generator;VERT1575_5_verdict",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "v_R=partial_rho_R plus compensators is the closest R-sector precedent",
            "R_AB remains coframe-visible unless quotient/constraint route closes",
            False,
        ),
        (
            "HUNT2857_2_quotient_map",
            "canonical q: Conf_parent -> Q_obs",
            str(SRC_1022_VERTICAL_QUOTIENT),
            "VQC1022_0_q_map;VQC1022_3_vertical_generator",
            "CONDITIONAL_QUOTIENT_CONTRACT",
            "would make Dq[v_X]=0 meaningful",
            "actual field-by-field v_X and q(Phi) are missing",
            False,
        ),
        (
            "HUNT2857_3_matter_lift",
            "matter/readout vertical lift",
            str(SRC_1045_VERTICAL_LIFT),
            "VLG1045_0_fixed_lift;VLG1045_1_gauge_lift",
            "CLEAN_OPTIONS_NOT_PARENT_SIGNED",
            "fixed or gauge lift could protect ordinary matter",
            "no parent map assigns the lift for every matter species",
            False,
        ),
        (
            "HUNT2857_4_minimal_action_contract",
            "minimal parent coupling owner action",
            str(SRC_781_ACTION),
            "MPC781_7_contract_verdict",
            "CANDIDATE_ACTION_CONTRACT_ONLY",
            "action language already exists for quotient-invariant matter/source/readout",
            "not adopted as current MTS action",
            False,
        ),
        (
            "HUNT2857_5_component_map",
            "response doublet / physical residual lock",
            str(SRC_1282_DOUBLET),
            "RCM1282_6_verdict",
            "COMPONENT_MAP_NOT_CLOSED",
            "warns that Z/doublet variables must lock to full q_loc/PPN/coupling vector",
            "full physical residual vector is not parent-signed",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "hunt_id": hunt_id,
                "candidate": candidate,
                "source_path": source_path,
                "source_anchors": anchors,
                "status": status,
                "useful_content": useful,
                "blocking_gap": gap,
                "accepted_generator_source": accepted,
                "control_only": True,
            }
        )
        for hunt_id, candidate, source_path, anchors, status, useful, gap, accepted in specs
    ]


def ansatz_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ANS2857_0_doublet",
            "local amplitude doublet",
            "A = (C_AB, delta_R)",
            "the two 1/r amplitude channels are treated as coordinates of one local parent doublet",
            "CONSTRUCTED_NONCLAIM",
        ),
        (
            "ANS2857_1_generator",
            "vertical amplitude generator",
            "v_amp = partial_C + sigma_R partial_R",
            "this is the exact generator coefficient demanded by 2856",
            "CONSTRUCTED_NONCLAIM_TUNING_RISK",
        ),
        (
            "ANS2857_2_quotient_invariant",
            "quotient invariant amplitude",
            "U_amp = delta_R - sigma_R C_AB; v_amp[U_amp]=0",
            "a parent action depending only on U_amp would make v_amp a redundancy",
            "CONDITIONAL_ALGEBRA_VALID",
        ),
        (
            "ANS2857_3_action",
            "minimal doublet action",
            "S_amp = 1/2 <U_amp, L_U U_amp> - <J_U, U_amp> + boundary",
            "Euler split gives the required source ratio without independent rescaling",
            "ANSATZ_ONLY_NOT_PARENT_ACTION",
        ),
        (
            "ANS2857_4_source_split",
            "source current split",
            "J_CAB = -sigma_R J_U; J_R = J_U",
            "therefore J_CAB + sigma_R J_R = 0, or dK_amp if boundary/improvement is retained",
            "CONDITIONAL_ALGEBRA_VALID",
        ),
        (
            "ANS2857_5_boundary",
            "boundary/improvement term",
            "K_amp = 0 for compact/proper branch, otherwise K_amp retained and sourced",
            "keeps the integrated theorem honest",
            "BOUNDARY_NOT_PROVEN",
        ),
        (
            "ANS2857_6_reduced_mode",
            "physical degree count",
            "only U_amp is physical; the orthogonal gauge coordinate is unobservable",
            "prevents one extra local pole if the quotient action is parent-owned",
            "DEGREE_COUNT_NOT_PROVEN",
        ),
        (
            "ANS2857_7_claim_guard",
            "no-tuning guard",
            "sigma_R and v_amp must come from parent sign/quotient data before A_total is read out",
            "otherwise the ansatz is just cancellation by design",
            "REQUIRED_FOR_ANY_FUTURE_CLAIM",
        ),
    ]
    return [
        nonclaim(
            {
                "ansatz_id": ansatz_id,
                "object": obj,
                "minimal_form": form,
                "purpose": purpose,
                "status": status,
                "parent_owned": False,
                "accepted_for_claim": False,
                "control_only": True,
            }
        )
        for ansatz_id, obj, form, purpose, status in specs
    ]


def algebra_rows() -> list[dict[str, Any]]:
    specs = [
        ("ALG2857_0_invariant", "v_amp[U_amp] = partial_C(delta_R - sigma_R C_AB) + sigma_R partial_R(delta_R - sigma_R C_AB)", "-sigma_R + sigma_R = 0, so U_amp is invariant under v_amp", "ALGEBRA_PASS_CONDITIONAL"),
        ("ALG2857_1_normalization", "if another convention writes v_amp = a partial_C + b partial_R", "U_amp is invariant only when b/a = sigma_R, so the ratio must be parent-owned before readout", "NORMALIZATION_GUARD"),
        ("ALG2857_2_source_split", "S_src=-<J_U, delta_R - sigma_R C_AB>", "J_CAB=-sigma_R J_U and J_R=J_U, hence J_CAB + sigma_R J_R = 0", "ALGEBRA_PASS_CONDITIONAL"),
        ("ALG2857_3_improvement", "S_src=-<J_U,U_amp> + boundary/improvement", "J_CAB + sigma_R J_R = dK_amp when improvement current is retained", "ALGEBRA_PASS_CONDITIONAL"),
        ("ALG2857_4_charge", "Q_CAB + sigma_R q_R_eff = boundary/improvement integral", "the leading amplitude vanishes only if the boundary/improvement integral is zero or included", "BOUNDARY_CONDITIONAL"),
        ("ALG2857_5_tuning_guard", "sigma_R and U_amp must be fixed by parent operator/quotient before fitting", "otherwise this is a designed cancellation, not a derivation", "CLAIM_BLOCKER"),
    ]
    return [
        nonclaim(
            {
                "algebra_id": algebra_id,
                "check": check,
                "result": result,
                "status": status,
                "algebra_passed": status.startswith("ALGEBRA_PASS") or status == "BOUNDARY_CONDITIONAL",
                "parent_owned": False,
                "control_only": True,
            }
        )
        for algebra_id, check, result, status in specs
    ]


def ownership_rows() -> list[dict[str, Any]]:
    specs = [
        ("OWN2857_0_sigma", "sigma_R is fixed by parent operator/Green sign before readout", "OPEN", "CONTRACT2844_5_sign remains missing"),
        ("OWN2857_1_q", "q(Phi_parent) excludes the vertical amplitude coordinate", "OPEN", "FM783/VQC1022 say q is needed but not owned"),
        ("OWN2857_2_generator", "v_amp is the actual Omega-raised generator, not chosen after desired cancellation", "OPEN", "DVM727 formal map exists but parent Omega/DC are missing"),
        ("OWN2857_3_action", "S_amp depends on U_amp because of parent symmetry, not because we wrote it so", "OPEN", "minimal action is an ansatz, not current corpus action"),
        ("OWN2857_4_boundary", "K_amp and B terms are zero/exact or included in the charge", "OPEN", "boundary differentiability/silence missing"),
        ("OWN2857_5_matter", "ordinary matter/source/readout only see quotient variables", "OPEN", "matter descent and source weights are unsigned"),
        ("OWN2857_6_full_vector", "same branch closes full PPN/local vector", "OPEN", "response doublet/full vector lock not closed"),
    ]
    return [
        nonclaim(
            {
                "ownership_id": ownership_id,
                "required_owner": owner,
                "status": status,
                "why_open": why,
                "ownership_closed": False,
                "control_only": True,
            }
        )
        for ownership_id, owner, status, why in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RR2857_0_reentry", "If OWN2857_0 through OWN2857_6 close", "promote minimal doublet ansatz into parent-action theorem candidate", "not active"),
        ("RR2857_1_reject", "If v_amp only exists because we choose it to cancel A_total", "reject theorem-zero route as closure/tuning", "active guard"),
        ("RR2857_2_fallback", "If parent ownership remains open", "use finite source rows in 2853 strict runner", "active fallback"),
        ("RR2857_3_scope", "If generator owns amplitude only but not matter/readout/full vector", "keep gamma/amplitude result isolated, no local-GR claim", "active guard"),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "condition": condition,
                "action": action,
                "status": status,
                "control_only": True,
            }
        )
        for route_id, condition, action, status in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2857_0_parent_sigma", "operator/sign owner", "source line fixing sigma_R in the amplitude doublet before any local fit"),
        ("REQ2857_1_parent_q", "quotient map", "explicit q(Phi_parent) showing U_amp is quotient-visible and v_amp is vertical"),
        ("REQ2857_2_parent_omega", "symplectic generator", "parent Omega and DC operator proving v_amp=Omega^{-1} DCdagger rather than chosen by hand"),
        ("REQ2857_3_parent_action", "amplitude action", "source action depending on U_amp=delta_R-sigma_R C_AB or an equivalent parent invariant"),
        ("REQ2857_4_boundary", "boundary/improvement theorem", "K_amp/B_CAB/B_R compact, exact, zero, or included in Q definitions"),
        ("REQ2857_5_full_vector", "same-branch full local vector", "beta/preferred/source/clock/orbital/q_loc closures in same quotient branch"),
    ]
    return [
        nonclaim(
            {
                "request_id": request_id,
                "needed_source": needed,
                "minimum_content": content,
                "status": "OPEN_SOURCE_REQUEST",
                "accepted_only_if": "exact source path plus equation/table anchor plus convention; no after-the-fact cancellation",
                "control_only": True,
            }
        )
        for request_id, needed, content in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2857_0_hunt_done", "existing generator source hunt completed", "PASS_CONTROL_ONLY", "formal map exists but no accepted generator source"),
        ("CG2857_1_ansatz_math", "minimal doublet ansatz algebra works conditionally", "PASS_CONTROL_ONLY", "source split can yield current identity if parent owns it"),
        ("CG2857_2_generator_claim", "v_amp is parent-owned", "BLOCKED", "Omega/DC/q/action owner missing"),
        ("CG2857_3_theorem_zero", "Q_CAB + sigma_R q_R_eff = 0 theorem claimed", "BLOCKED", "boundary and ownership clauses open"),
        ("CG2857_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "matter/source/full-vector ownership open"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2857_0_existing_hunt", "No existing accepted vertical generator source was found.", "NO_ACCEPTED_SOURCE", "older corpus has formal DCdagger/Omega map but not parent Omega/DC/q/action ownership"),
        ("DEC2857_1_ansatz", "Constructed the minimal amplitude-doublet action ansatz.", "CONDITIONAL_LEAP_FORWARD", "U_amp=delta_R-sigma_R C_AB gives the desired source identity without independent source rescaling if parent-owned"),
        ("DEC2857_2_claim_status", "Do not claim theorem-zero/local-GR.", "LOCKED", "the ansatz is not yet parent action; it could still be cancellation by construction"),
        ("DEC2857_3_next", "Next target is a consistency gate for the minimal doublet action.", "SELECTED_2858", "test whether the ansatz can be made non-tunable and compatible with the existing quotient/matter/full-vector contracts"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2857_0_2858",
                "status": "selected_primary",
                "target_doc": "2858-Y5-R2FR-minimal-amplitude-doublet-action-consistency-gate-or-reject-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_amplitude_doublet_action_consistency_gate_or_reject_under_AX1090_2858.py",
                "mission": "test whether the minimal U_amp=delta_R-sigma_R C_AB parent-action ansatz is non-tunable, quotient-compatible, matter-descending, boundary-silent, and full-vector compatible; reject it as closure-only if any owner clause remains arbitrary",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2857_0_ansatz", OUTPUTS["ansatz"], BRANCH_OUTPUTS["ansatz_copy"], "minimal doublet action ansatz nonclaim copy"),
        ("COPY2857_1_ownership", OUTPUTS["ownership"], BRANCH_OUTPUTS["ownership_copy"], "vertical generator ownership gate nonclaim copy"),
        ("COPY2857_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2858"),
        ("COPY2857_3_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "vertical generator source request copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
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
        "accepted_generator_source",
        "parent_owned",
        "accepted_for_claim",
        "ownership_closed",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
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
        ("VAL2857_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2857_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2857_2_hunt_has_formal_map", any(row["status"] == "FORMAL_MAP_EXISTS" for row in rows_by_name["hunt"]), "existing DCdagger/Omega formal map was found"),
        ("VAL2857_3_no_accepted_generator", not any(row["accepted_generator_source"] for row in rows_by_name["hunt"]), "no existing generator source is accepted for claim"),
        ("VAL2857_4_ansatz_constructed", len(rows_by_name["ansatz"]) >= 8, "minimal doublet action ansatz is written"),
        ("VAL2857_5_algebra_checked", len(rows_by_name["algebra"]) >= 6 and any(row["status"] == "CLAIM_BLOCKER" for row in rows_by_name["algebra"]), "algebra checks include tuning guard"),
        ("VAL2857_6_ownership_open", not any(row["ownership_closed"] for row in rows_by_name["ownership"]), "all ownership gates remain open"),
        ("VAL2857_7_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2857_8_next_target_2858", any(row["next_id"] == "NEXT2857_0_2858" and row["selected"] for row in rows_by_name["next"]), "2858 consistency gate selected"),
        ("VAL2857_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2857_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2857_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2857_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2857_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2857_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2857_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2857_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2857_OVERALL",
            "passed": overall,
            "detail": "2857 finds a formal but unowned vertical-generator map, constructs the minimal amplitude-doublet action ansatz as nonclaim, and selects a consistency/rejection gate for 2858.",
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
    content = f"""# 2857 - Y5 R2FR Vertical Generator Source Hunt Or Minimal Action Construction Under AX1090

Status: `Y5_R2FR_2857_formal_generator_found_minimal_doublet_ansatz_constructed_nonclaim`

## Private Verdict

This was not another circle. The old corpus already contains the correct category of object:

`v_X = Omega^{-1}[(DC_X)^dagger X]`

So the vertical generator is not mystical. It is the symplectic dual of a parent constraint/current variation. The problem is that current MTS does not yet supply the parent `Omega`, the exact `DC`, the field-by-field action, the quotient map, or the boundary/matter descent needed to make this actual rather than formal.

The constructive leap is the minimal amplitude-doublet ansatz:

`U_amp = delta_R - sigma_R C_AB`

with a parent action depending on `U_amp` only:

`S_amp = 1/2 <U_amp, L_U U_amp> - <J_U, U_amp> + boundary`

This algebraically gives `J_CAB = -sigma_R J_U`, `J_R = J_U`, hence `J_CAB + sigma_R J_R = 0` up to retained improvement/boundary terms.

That is a serious candidate mechanism. But it is not yet a proof, because the same ansatz could be a cancellation designed after the target was known. The next gate must test whether `U_amp` is forced by the parent quotient/action structure rather than chosen to save the local branch.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Existing Generator Hunt

{markdown_table(rows["hunt"], ["hunt_id", "candidate", "status", "useful_content", "blocking_gap", "accepted_generator_source", "valid_for_claim"])}

## Minimal Doublet Action Ansatz

{markdown_table(rows["ansatz"], ["ansatz_id", "object", "minimal_form", "purpose", "status", "parent_owned", "valid_for_claim"])}

## Ansatz Algebra Check

{markdown_table(rows["algebra"], ["algebra_id", "check", "result", "status", "algebra_passed", "parent_owned", "valid_for_claim"])}

## Parent Ownership Gate

{markdown_table(rows["ownership"], ["ownership_id", "required_owner", "status", "why_open", "ownership_closed", "valid_for_claim"])}

## Rejection Or Reentry Ledger

{markdown_table(rows["reentry"], ["route_id", "condition", "action", "status", "valid_for_claim"])}

## Source Request Ledger

{markdown_table(rows["requests"], ["request_id", "needed_source", "minimum_content", "accepted_only_if", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

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
    rows["hunt"] = hunt_rows()
    rows["ansatz"] = ansatz_rows()
    rows["algebra"] = algebra_rows()
    rows["ownership"] = ownership_rows()
    rows["reentry"] = reentry_rows()
    rows["requests"] = request_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "hunt", "ansatz", "algebra", "ownership", "reentry", "requests", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2857_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2857_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
