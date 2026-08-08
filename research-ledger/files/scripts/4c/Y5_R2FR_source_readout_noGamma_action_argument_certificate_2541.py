from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CHECKPOINT_ID = "2541"
BRANCH_ID = "MTS_R2FR_SOURCE_READOUT_NOGAMMA_ARGUMENT_CERTIFICATE_2541"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2541-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2541_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_NO_SHADOW_2541_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "theorem": RESIDUALS / "P8_Y5_NO_SHADOW_2541_SRNG_THEOREM_ATTEMPT.csv",
    "p4_status": RESIDUALS / "P8_Y5_NO_SHADOW_2541_P4_DELTA_STATUS_AFTER_SRNG.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2541_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2541_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_NO_SHADOW_2541_REFUSAL_RUNNER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2541_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2541_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2541_VALIDATION.csv",
}

BRANCH_COPIES = {
    "certificate": POST_ROOT / "source-intake" / "beta-source" / "docs" / "SRNG_argument_certificate_2541_NONCLAIM.csv",
    "theorem": POST_ROOT / "source-intake" / "beta-source" / "docs" / "SRNG_theorem_attempt_2541_NONCLAIM.csv",
    "p4_status": POST_ROOT / "source-intake" / "local_bounds" / "P4_Delta_status_after_SRNG_2541_NONCLAIM.csv",
    "next": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "DOWNSTREAM_FUNCTOR2541_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    ("SRC2541_0_2540_doc", "2540-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md", "NEXT2540_0_selected", "2540 selected source/readout no-Gamma argument certificate"),
    ("SRC2541_1_2540_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2540_VALIDATION.csv", "VAL2540_OVERALL,PASS", "2540 validation anchor"),
    ("SRC2541_2_2540_slots", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2540_GAMMA_SLOT_SECTOR_AUDIT.csv", "NGSA2540_9_verdict", "current no-Gamma slot audit"),
    ("SRC2541_3_2540_theorem", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2540_NO_GAMMA_THEOREM_STACK.csv", "NGT2540_4_result", "current theorem stack input"),
    ("SRC2541_4_2540_p4", "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2540_P4_DELTA_COMPONENT_QUEUE.csv", "P4DQ2540_0_total", "current P4 component queue"),
    ("SRC2541_5_2376_doc", "2376-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md", "SRNG2376_6_verdict", "older SRNG certificate precedent"),
    ("SRC2541_6_2376_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2376_VALIDATION.csv", "VAL2376_OVERALL", "2376 validation anchor"),
    ("SRC2541_7_2376_certificate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv", "SRNG2376_6_verdict", "source/readout argument certificate precedent"),
    ("SRC2541_8_2376_theorem", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_SRNG_THEOREM_ATTEMPT.csv", "THM2376_3_SRNG_sum", "SRNG theorem attempt precedent"),
    ("SRC2541_9_2376_p4_status", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_P4_DELTA_STATUS_AFTER_SRNG.csv", "P4S2376_6_reduced_total", "P4 status after SRNG precedent"),
    ("SRC2541_10_2376_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2376_NEXT_TARGET.csv", "NEXT2376_0_selected", "downstream functor next target precedent"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "source_id": source_id,
                    "source_path": source_path,
                    "needle": needle,
                    "role": role,
                    "path_exists": str(path.exists()).lower(),
                    "needle_found": str(contains(path, needle)).lower(),
                    "status": "SOURCE_OK" if path.exists() and contains(path, needle) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def srng_argument_certificate() -> list[dict[str, object]]:
    rows = [
        (
            "SRNG2541_0_total_clause",
            "total source/readout branch",
            "parent-action restriction",
            "S_source uses Psi_src,e_obs,omega_LC[e_obs],A_owned,theta_src; O_clock/O_light/O_orbit/O_readout are downstream functors of solved observed fields",
            "Gamma_ind; source-only affine current; fitted readout mask inside variation; independent autoparallel law",
            "Source-Readout No-Gamma (SRNG): no source/readout object appears in the variational action with Gamma_ind as an argument.",
            "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "parent adoption or deeper quotient/naturality derivation",
        ),
        (
            "SRNG2541_1_source_worldtube",
            "source worldtube and GM support",
            "source action / support selector",
            "W_source=closure(supp J_H[tau]); J_H from same Hilbert/coframe matter action; compact support and fixed linking surfaces",
            "Gamma_ind current; fitted radius/source mask; boundary torsion; post-readout GM rescaling",
            "source support is selected from the Hilbert current of the same Gamma-free matter action, not by a new connection-sensitive source law",
            "CONDITIONAL_FROM_WORLDTUBE_SELECTOR_NOT_SIGNED",
            "Delta_source",
            "compactness, boundary/reference lock, M_H_ref and coupling descent are not parent-signed",
        ),
        (
            "SRNG2541_2_clock",
            "clock and frequency readout",
            "downstream observation functor",
            "O_clock[solution fields, e_obs, A_owned, theta_clock, tau]",
            "Gamma_ind probe term; source-labelled clock current; separate clock frame",
            "clock readout is not a term in S_ord; it reads the same solved observed coframe/gauge branch",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_clock",
            "clock model and tau/frame lock still need explicit parent signature",
        ),
        (
            "SRNG2541_3_light",
            "light, EM, Shapiro and deflection readout",
            "EM action plus downstream null/ray readout",
            "A_owned, e_obs/g_obs, omega_LC[e_obs], detector constants; WKB/null readout after variation",
            "affine Gamma_ind as optical connection; independent ray-autoparallel postulate",
            "light propagation is owned by EM/gauge plus metric/coframe readout, not by an independent affine connection",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_light",
            "Maxwell/WKB and detector readout need parent-side statement in MTS language",
        ),
        (
            "SRNG2541_4_orbit",
            "orbital/test-body readout",
            "test-body limit / downstream trajectory readout",
            "point/compact body action from same e_obs/g_obs matter branch; trajectory readout after variation",
            "independent Gamma_ind autoparallel law; fitted orbit frame; marker current inside source variation",
            "test-body motion must be the limit of Hilbert/coframe matter, not an added affine-autoparallel rule",
            "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "Delta_orbit",
            "test-body reduction and marker/domain map still need parent certificate",
        ),
        (
            "SRNG2541_5_boundary",
            "boundary/domain/improvement",
            "support and integration boundary policy",
            "fixed compact support, exact/projected-silent improvement, fixed reference boundary data",
            "Gamma-sensitive boundary current; readout-selected domain; cancellation by sign",
            "boundary terms do not enter Delta_abs if compact support and improvement flux are parent-fixed or projected exact",
            "NOT_CLOSED_REQUIRES_SEPARATE_BOUNDARY_CERTIFICATE",
            "Delta_boundary",
            "worldtube flux and improvement current zero theorem/bound is still live",
        ),
        (
            "SRNG2541_6_verdict",
            "all source/readout sectors",
            "certificate verdict",
            "source/readout can be made Gamma-free by SRNG as a single parent clause",
            "calling SRNG derived before quotient/naturality or parent adoption is signed",
            "SRNG is a clean parent-action contract that would zero Delta_source/clock/light/orbit, but it is not yet derived from deeper MTS primitives",
            "PARTIAL_CERTIFICATE_READY_NOT_DERIVED",
            "conditional: Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "derive SRNG from quotient/naturality or adopt it as a private working parent clause; boundary/projective remain separate",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "sector": sector,
            "object_type": obj_type,
            "allowed_arguments": allowed,
            "forbidden_arguments": forbidden,
            "certificate_clause": clause,
            "status": status,
            "closes_delta": closes,
            "remaining_gap": gap,
        }
        for row_id, sector, obj_type, allowed, forbidden, clause, status, closes, gap in rows
    ]


def srng_theorem_attempt() -> list[dict[str, object]]:
    rows = [
        (
            "THM2541_0_downstream_readout",
            "downstream readout lemma",
            "If O_i is evaluated after solving the variational problem and is not an action/current term, then O_i does not contribute delta S/delta Gamma_ind.",
            "EXACT_CONDITIONAL_LEMMA",
            "must prove clocks/light/orbits are downstream functors, not hidden action/source terms",
        ),
        (
            "THM2541_1_hilbert_source_selector",
            "Hilbert source selector lemma",
            "If W_source is selected from the support of the Hilbert current of the same Gamma-free matter action, it introduces no independent Gamma source current.",
            "EXACT_CONDITIONAL_LEMMA",
            "compactness, M_H_ref, boundary/reference lock and same-frame tau are unsigned",
        ),
        (
            "THM2541_2_orbit_test_body",
            "test-body no-autoparallel lemma",
            "If test-body motion is a limit of the same Hilbert/coframe matter action, an independent Gamma_ind autoparallel law is inadmissible.",
            "EXACT_CONDITIONAL_LEMMA",
            "test-body limit and marker/domain maps must be written in parent variables",
        ),
        (
            "THM2541_3_SRNG_sum",
            "SRNG zero sum",
            "Under SRNG plus the no-Gamma matter branch, Delta_source=Delta_clock=Delta_light=Delta_orbit=0 without cancellation.",
            "CONDITIONAL_THEOREM_READY",
            "SRNG is written here as a contract, not derived or adopted as active MTS parent action",
        ),
        (
            "THM2541_4_boundary_warning",
            "boundary warning",
            "SRNG does not by itself kill boundary/improvement/projective trace residuals unless those are separately fixed, exact, gauge, or bounded.",
            "LIMIT_EXPLICIT",
            "Delta_boundary and Delta_projective remain live",
        ),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "claim_piece": piece,
            "statement": statement,
            "result": result,
            "obstruction": obstruction,
        }
        for row_id, piece, statement, result, obstruction in rows
    ]


def p4_status_after_srng() -> list[dict[str, object]]:
    rows = [
        ("P4S2541_0_source", "Delta_source", "ZERO_IF_SRNG_PARENT_SIGNED_ELSE_BOUND", "SRNG_CONTRACT_NOT_SIGNED", "source/worldtube no-Gamma adoption or finite source-current bound"),
        ("P4S2541_1_clock", "Delta_clock", "ZERO_IF_DOWNSTREAM_CLOCK_FUNCTOR_SIGNED_ELSE_BOUND", "CLOCK_ARGUMENT_LIST_NOT_SIGNED", "clock readout parent functor or frequency residual bound"),
        ("P4S2541_2_light", "Delta_light", "ZERO_IF_EM_LIGHT_READOUT_SIGNED_ELSE_BOUND", "LIGHT_ARGUMENT_LIST_NOT_SIGNED", "EM/WKB/null readout certificate or PPN light bound"),
        ("P4S2541_3_orbit", "Delta_orbit", "ZERO_IF_TEST_BODY_LIMIT_SIGNED_ELSE_BOUND", "ORBIT_ARGUMENT_LIST_NOT_SIGNED", "test-body/marker parent map or orbital residual bound"),
        ("P4S2541_4_boundary", "Delta_boundary", "STILL_OPEN_SEPARATE_CERTIFICATE", "BOUNDARY_ZERO_OR_BOUND_MISSING", "boundary no-flux/improvement theorem or source-backed bound"),
        ("P4S2541_5_projective", "Delta_projective", "STILL_OPEN_PARALLEL_CERTIFICATE", "PROJECTIVE_TRACE_POLICY_MISSING", "projective gauge/fixed/unobservable certificate or residual policy"),
        ("P4S2541_6_reduced_total", "Delta_abs_reduced", "IF_SRNG_AND_MATTER_BRANCH_SIGNED_THEN_REDUCE_TO_DELTA_SPIN_BOUNDARY_PROJECTIVE", "REDUCTION_CONDITIONAL_ONLY", "SRNG adoption plus spin/boundary/projective closure"),
    ]
    return [
        {
            **no_claim(),
            "row_id": row_id,
            "component": component,
            "status_after_SRNG": status_after,
            "current_status": current,
            "needed_for_score": needed,
        }
        for row_id, component, status_after, current, needed in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "DEC2541_0_SRNG_contract",
            "SRNG source-readout no-Gamma contract is now explicit",
            "it forbids Gamma_ind in source/readout actions and keeps clocks/light/orbits downstream",
            "several leak paths can close together if adopted or derived",
            "CONTRACT_READY_NONCLAIM",
        ),
        (
            "DEC2541_1_no_public_promotion",
            "do not promote SRNG as current MTS theorem",
            "contract is written but not derived from deeper quotient/naturality or adopted in formal spine",
            "no local-GR/Newton/WEP/PPN claim",
            "NO_PROMOTION",
        ),
        (
            "DEC2541_2_best_next",
            "try to derive downstream observation functor naturality next",
            "if q/naturality forces readouts downstream, SRNG becomes less axiomatic",
            "otherwise adopt SRNG privately or fill P4 component bounds",
            "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT",
        ),
        (
            "DEC2541_3_public_policy",
            "no GitHub evidence update",
            "this is a private contract/derivation gate",
            "continue in post-checkpoint-work",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "decision": decision,
                "reason": reason,
                "consequence": consequence,
                "status": status,
            }
        )
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2541_0_SRNG_active", "SRNG active in parent action", "FAIL", "contract only"),
        ("CG2541_1_source_readout_zero", "Delta_source/clock/light/orbit theorem-zero", "FAIL", "zero only if SRNG parent-signed"),
        ("CG2541_2_boundary_projective", "boundary/projective residuals closed", "FAIL", "still open"),
        ("CG2541_3_P4_score", "P4 components score-ready", "FAIL", "no numeric units/maps/bounds yet"),
        ("CG2541_4_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection/EH/GM gates remain"),
        ("CG2541_5_github", "safe public evidence update", "FAIL", "private checkpoint only"),
    ]
    return [stamp({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}) for row_id, gate, status, effect in rows]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2541_0_contract_as_derivation", "SRNG is derived from MTS now", "false", "2541 writes the exact contract but does not derive it from deeper q/naturality"),
        ("REF2541_1_ignore_boundary", "source/readout no-Gamma also closes boundary/projective terms", "false", "boundary/improvement and projective trace are separate residual channels"),
        ("REF2541_2_autoparallel_import", "orbits use LC because GR says so", "false", "test-body motion must be derived as the Hilbert/coframe matter limit or residualized"),
        ("REF2541_3_local_gr", "2541 proves local GR/Newton", "false", "SRNG would close one connection subgate only; EH, GM normalization, boundary and projective gates remain"),
    ]
    return [stamp({"row_id": row_id, "claim": claim, "allowed": allowed, "reason": reason}) for row_id, claim, allowed, reason in rows]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2541_0_selected",
            "selected",
            "2542-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            "scripts/Y5_R2FR_downstream_observation_functor_naturality_or_SRNG_adoption_2542.py",
            "prove clocks/light/orbits/readouts are downstream natural functors of q-observed solved fields, not new source-current arguments",
            "if not derived, retain SRNG as private branch contract or fill P4 component bounds",
        ),
        (
            "NEXT2541_1_parallel",
            "parallel",
            "2542b-Y5-R2FR-boundary-projective-residual-split.md",
            "scripts/Y5_R2FR_boundary_projective_residual_split_2542b.py",
            "split boundary/improvement and projective trace into independent zero/bound policies",
            "retain E_boundary/Delta_projective residuals if unsigned",
        ),
        (
            "NEXT2541_2_fallback",
            "fallback",
            "2542c-Y5-R2FR-P4-source-readout-component-bounds.md",
            "scripts/Y5_R2FR_P4_source_readout_component_bounds_2542c.py",
            "fill Delta_source/clock/light/orbit units, weak-field maps and source-backed bounds",
            "keep nonclaim until same-frame and source-backed",
        ),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "priority": priority,
                "next_file": next_file,
                "next_script": next_script,
                "success_condition": success,
                "fallback_condition": fallback,
            }
        )
        for row_id, priority, next_file, next_script, success, fallback in rows
    ]


def branch_copy_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for copy_id, destination in BRANCH_COPIES.items():
        source = OUTPUTS[copy_id]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": rel(source),
                    "destination_path": rel(destination),
                    "destination_exists": str(destination.exists()).lower(),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return True, "git modified-file count for formalization-workbench is 0"
        return False, f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or row.get("copy_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() in {"true", "pass", "passed", "ready", "yes", "1"}:
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}))

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2541_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2541_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2541_02_outputs_exist", all(path.exists() for path in generated), "all 2541 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2541_03_csv_parse", parse_ok, parse_detail)

    cert = read_csv(outputs["certificate"])
    theorem = read_csv(outputs["theorem"])
    p4 = read_csv(outputs["p4_status"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])

    add(
        "VAL2541_04_SRNG_written",
        any(row["row_id"] == "SRNG2541_0_total_clause" and row["status"] == "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED" for row in cert),
        "SRNG total contract written as nonclaim",
    )
    add(
        "VAL2541_05_SRNG_not_promoted",
        any(row["row_id"] == "SRNG2541_6_verdict" and row["status"].endswith("NOT_DERIVED") for row in cert),
        "SRNG not promoted as derived",
    )
    add(
        "VAL2541_06_theorem_limits",
        any(row["row_id"] == "THM2541_4_boundary_warning" and row["result"] == "LIMIT_EXPLICIT" for row in theorem),
        "boundary/projective limitation explicit",
    )
    add(
        "VAL2541_07_p4_status_components",
        len(p4) >= 7 and any(row["row_id"] == "P4S2541_6_reduced_total" for row in p4),
        "source/readout/boundary/projective P4 status rows present",
    )
    add(
        "VAL2541_08_next_derivation_selected",
        any(row["row_id"] == "DEC2541_2_best_next" and row["status"] == "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT" for row in decisions)
        and any(row["row_id"] == "NEXT2541_0_selected" for row in next_rows),
        "downstream observation functor derivation selected next",
    )
    add(
        "VAL2541_09_local_claims_block",
        any(row["row_id"] == "CG2541_4_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
        "local GR/Newton claim gate remains false",
    )
    add(
        "VAL2541_10_github_blocked",
        any(row["row_id"] == "CG2541_5_github" and row["gate_status"] == "FAIL" for row in gates),
        "public GitHub evidence update remains blocked",
    )

    copy_rows = read_csv(outputs["copies"])
    add("VAL2541_11_branch_copies", all(row.get("destination_exists") == "true" for row in copy_rows), "all nonclaim branch copies exist")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2541_12_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2541_13_formalization_untouched", formal_ok, formal_detail)
    add("VAL2541_14_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        stamp(
            {
                "row_id": "VAL2541_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2541 valid: SRNG source/readout no-Gamma certificate written nonclaim, conditional zero effect recorded, boundary/projective/P4 retained, downstream functor derivation selected" if overall else "one or more validation gates failed",
            }
        )
    )
    return rows


def table(headers: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    cert = read_csv(outputs["certificate"])
    theorem = read_csv(outputs["theorem"])
    p4 = read_csv(outputs["p4_status"])
    decisions = read_csv(outputs["decision"])
    gates = read_csv(outputs["claims"])
    next_rows = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2541 - Source-Readout noGamma Action-Argument Certificate

## Result

The source/readout no-Gamma certificate is now explicit:

`SRNG`: source support, clocks, light, orbits and readout maps may use the observed coframe/metric, `omega_LC[e_obs]`, owned gauge fields, constants and solved fields, but not an independent `Gamma_ind` argument inside the variational source/action.

Under SRNG plus the no-Gamma ordinary matter branch:

`Delta_source = Delta_clock = Delta_light = Delta_orbit = 0`

without cancellation.

But SRNG is a private contract, not yet a derived parent theorem. Boundary/improvement and projective trace also remain separate residual channels. So this improves the connection route, but it does not close local GR/Newton.

## SRNG Argument Certificate

{table(["row_id", "sector", "status", "closes_delta", "remaining_gap"], cert)}

## SRNG Theorem Attempt

{table(["row_id", "claim_piece", "result", "obstruction"], theorem)}

## P4 Delta Status After SRNG

{table(["row_id", "component", "status_after_SRNG", "current_status", "needed_for_score"], p4)}

## Decision Ledger

{table(["row_id", "decision", "status", "consequence"], decisions)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], gates)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["certificate"])}`
- `{rel(outputs["theorem"])}`
- `{rel(outputs["p4_status"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a real structural gain. We now have a compact clause that would zero the source/readout Gamma components together. The remaining honest question is whether SRNG can be derived from downstream observation functor naturality, or whether it must stay as a private parent-action restriction with P4 fallback bounds.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    write_csv(OUTPUTS["certificate"], srng_argument_certificate())
    write_csv(OUTPUTS["theorem"], srng_theorem_attempt())
    write_csv(OUTPUTS["p4_status"], p4_status_after_srng())
    write_csv(OUTPUTS["decision"], decision_ledger())
    write_csv(OUTPUTS["claims"], claim_gates())
    write_csv(OUTPUTS["refusal"], refusal_runner())
    write_csv(OUTPUTS["next"], next_target())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
